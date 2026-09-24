#!/usr/bin/env python3
"""/setup-repo: detect a repo's stack, plan an optimal Claude Code setup, apply it. Stdlib only."""
import argparse, json, os, re, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLKIT_SCRIPTS = HERE.parents[2] / "scripts"  # skills/setup-repo/scripts -> repo root/scripts
LANG_EXT = {"python": [".py"], "typescript": [".ts", ".tsx"], "javascript": [".js", ".jsx", ".mjs"],
            "go": [".go"], "rust": [".rs"], "ruby": [".rb"]}
PM_FILES = [("uv.lock", "uv"), ("poetry.lock", "poetry"), ("Pipfile.lock", "pipenv"), ("requirements.txt", "pip"),
            ("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"), ("bun.lock", "bun"), ("bun.lockb", "bun"),
            ("package-lock.json", "npm"), ("go.mod", "go"), ("Cargo.toml", "cargo"), ("Gemfile.lock", "bundler")]
EXISTING = ["CLAUDE.md", ".claude/CLAUDE.md", "AGENTS.md", "CLAUDE.local.md", ".claude/settings.json",
            ".claude/team-profile.json", ".claude/hooks/lint_on_edit.py", ".beads", ".claude/rules"]

def _git(root, *args):
    try:
        p = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=20)
        return p.stdout.strip() if p.returncode == 0 else ""
    except Exception:  # noqa: BLE001
        return ""

def _tracked(root):
    out = _git(root, "ls-files")
    return [l for l in out.splitlines() if l]

def _languages(files):
    counts = {}
    for f in files:
        ext = os.path.splitext(f)[1]
        for lang, exts in LANG_EXT.items():
            if ext in exts:
                counts[lang] = counts.get(lang, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: -kv[1])[:5])

def _package_manager(root):
    for name, pm in PM_FILES:
        if (root / name).exists():
            return pm
    return None

def _existing(root):
    out = {}
    for rel in EXISTING:
        p = root / rel
        if p.is_file():
            out[rel] = {"exists": True, "lines": sum(1 for _ in p.open(encoding="utf-8", errors="replace"))}
        elif p.is_dir():
            out[rel] = {"exists": True, "lines": len(list(p.glob("*")))}
        else:
            out[rel] = {"exists": False, "lines": 0}
    return out

PM_RUN = {"uv": "uv run ", "poetry": "poetry run ", "pipenv": "pipenv run ", "pip": "", None: ""}
NODE_RUN = {"pnpm": "pnpm", "yarn": "yarn", "bun": "bun run", "npm": "npm run"}

def _read(root, rel):
    p = root / rel
    return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""

def _commands(root, pm):
    cmds = {}
    mk = _read(root, "Makefile")
    for target in ("test", "lint", "format", "typecheck", "build"):
        if re.search(rf"^{target}:", mk, re.M):
            cmds[target] = {"cmd": f"make {target}", "source": "Makefile"}
    pkg = _read(root, "package.json")
    if pkg:
        try:
            scripts = json.loads(pkg).get("scripts", {})
        except json.JSONDecodeError:
            scripts = {}
        runner = NODE_RUN.get(pm, "npm run")
        for target in ("test", "lint", "format", "typecheck", "build"):
            if target in scripts and target not in cmds:
                cmd = f"{runner} {target}" if not (runner == "npm run" and target == "test") else "npm test"
                if runner == "pnpm" and target == "test": cmd = "pnpm test"
                cmds[target] = {"cmd": cmd, "source": "package.json"}
    py = _read(root, "pyproject.toml")
    prefix = PM_RUN.get(pm, "")
    if py or (root / "pytest.ini").exists() or (root / "setup.cfg").exists():
        has_pytest = "[tool.pytest" in py or (root / "pytest.ini").exists()
        if has_pytest and "test" not in cmds:
            cmds["test"] = {"cmd": f"{prefix}pytest", "source": "pyproject.toml" if "[tool.pytest" in py else "pytest.ini"}
        if ("[tool.ruff" in py or (root / "ruff.toml").exists()) and "lint" not in cmds:
            cmds["lint"] = {"cmd": f"{prefix}ruff check .", "source": "pyproject.toml" if "[tool.ruff" in py else "ruff.toml"}
            cmds.setdefault("format", {"cmd": f"{prefix}ruff format .", "source": cmds["lint"]["source"]})
        if "[tool.mypy" in py and "typecheck" not in cmds:
            cmds["typecheck"] = {"cmd": f"{prefix}mypy .", "source": "pyproject.toml"}
    if (root / "go.mod").exists():
        cmds.setdefault("test", {"cmd": "go test ./...", "source": "go.mod"})
        cmds.setdefault("build", {"cmd": "go build ./...", "source": "go.mod"})
    if (root / "Cargo.toml").exists():
        cmds.setdefault("test", {"cmd": "cargo test", "source": "Cargo.toml"})
        cmds.setdefault("build", {"cmd": "cargo build", "source": "Cargo.toml"})
        cmds.setdefault("lint", {"cmd": "cargo clippy", "source": "Cargo.toml"})
    return cmds

def _git_facts(root):
    head = _git(root, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    default = head.split("/", 1)[1] if "/" in head else ("main" if _git(root, "rev-parse", "--verify", "-q", "main") else "unknown")
    remote = _git(root, "remote", "get-url", "origin")
    host = re.sub(r"^(git@|https?://)", "", remote).split(":")[0].split("/")[0] if remote else None
    branches = _git(root, "branch", "--format=%(refname:short)").splitlines()
    prefixes = sorted({b.split("/")[0] + "/" for b in branches if "/" in b})
    log = _git(root, "log", "--merges", "-n", "20", "--format=%s")
    style = "merge" if "Merge pull request" in log else ("squash" if _git(root, "log", "-n", "20", "--format=%s").count("(#") >= 3 else "unknown")
    return {"default_branch": default, "remote_host": host, "branch_prefixes": prefixes, "merge_style": style}

def _profile_name(result):
    if isinstance(result, (tuple, list)) and result:
        return str(result[0])
    if isinstance(result, dict):
        return result.get("maturity") or result.get("profile") or result.get("suggested")
    return str(result) if result else None

def _team_profile(root):
    sys.path.insert(0, str(TOOLKIT_SCRIPTS))
    try:
        import team_profile_detect as tpd  # noqa: PLC0415
        signals = tpd.gather_signals(root)
        name = _profile_name(tpd.classify(signals))
        return {"maturity": name, "signals": signals if isinstance(signals, dict) else {}} if name else None
    except Exception as e:  # noqa: BLE001
        print(f"setup-repo: team profile unavailable: {e}", file=sys.stderr)
        return None

def detect(root):
    root = Path(root).resolve()
    files = _tracked(root)
    return {"root": str(root), "languages": _languages(files), "package_manager": _package_manager(root),
            "existing": _existing(root), "commands": _commands(root, _package_manager(root)),
            "git": _git_facts(root), "team_profile": _team_profile(root), "size": len(files)}

BLOCKS = ("verify", "etiquette", "working", "compaction")
REFS = HERE.parent / "references"

def _templates():
    text = (REFS / "claude-md-blocks.md").read_text(encoding="utf-8")
    parts = re.split(r"^## block:(\w+)\n", text, flags=re.M)
    return {parts[i]: parts[i + 1].strip("\n") for i in range(1, len(parts), 2)}

def _block_text(name, profile):
    t = _templates()[name]
    cmds = profile["commands"]
    if name == "verify":
        if not cmds:
            return None
        lines = "\n".join(f"- `{c['cmd']}` ({k}; from `{c['source']}`)" for k, c in cmds.items())
        return t.replace("{command_lines}", lines)
    if name == "etiquette":
        g = profile["git"]
        if g["default_branch"] == "unknown":
            return None
        prefix = g["branch_prefixes"][0] if g["branch_prefixes"] else "claude/"
        return t.replace("{default_branch}", g["default_branch"]).replace("{branch_prefix}", prefix).replace("{merge_style}", g["merge_style"] if g["merge_style"] != "unknown" else "merge")
    if name == "working":
        tp = profile.get("team_profile") or {}
        maturity = tp.get("maturity") or "active"
        effort = "high" if maturity == "legacy" else "medium"
        return t.replace("{maturity}", maturity).replace("{effort}", effort)
    return t

def _wrap(name, body):
    return f"<!-- setup-repo:{name} -->\n{body}\n<!-- /setup-repo:{name} -->"

def render_claude_md(profile, existing_text):
    blocks = {n: _block_text(n, profile) for n in BLOCKS}
    if existing_text is None:
        root = Path(profile["root"])
        header = _templates()["header"].replace("{repo_name}", root.name).replace("{one_liner}", "Repo facts for Claude Code; behavioural rules live in the user-level CLAUDE.md.")
        parts = [header] + [_wrap(n, b) for n, b in blocks.items() if b]
        return "\n\n".join(parts) + "\n"
    out = existing_text
    for n, b in blocks.items():
        pat = re.compile(rf"<!-- setup-repo:{n} -->.*?<!-- /setup-repo:{n} -->", re.S)
        if pat.search(out):
            out = pat.sub(lambda m: _wrap(n, b) if b else "", out)
        elif b:
            out = out.rstrip("\n") + "\n\n" + _wrap(n, b) + "\n"
    return out
