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
EXISTING = ["CLAUDE.md", ".claude/CLAUDE.md", "AGENTS.md", "CLAUDE.local.md", ".claude/settings.json", ".claude/settings.local.json",
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
    counts = {}
    for b in branches:
        if "/" in b: counts[b.split("/")[0] + "/"] = counts.get(b.split("/")[0] + "/", 0) + 1
    prefixes = sorted(counts, key=lambda k: (-counts[k], k))  # most common first
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
        pat = re.compile(rf"(\n*)<!-- setup-repo:{n} -->.*?<!-- /setup-repo:{n} -->(\n*)", re.S)
        if pat.search(out):
            out = pat.sub(lambda m: m.group(1) + _wrap(n, b) + m.group(2) if b else _gap(m, len(out)), out)
        elif b:
            out = out.rstrip("\n") + "\n\n" + _wrap(n, b) + "\n"
    return out

def _gap(m, size):
    """Newlines left where a removed block was: at most one blank line, none at the file's start."""
    if m.start() == 0:
        return ""
    if m.end() == size:
        return "\n"
    return "\n" * min(2, max(len(m.group(1)), len(m.group(2))))

RULE_GLOBS = {"python": ["**/*.py"], "typescript": ["**/*.{ts,tsx}"], "javascript": ["**/*.{js,jsx,mjs}"], "go": ["**/*.go"], "rust": ["**/*.rs"]}
RULE_LANGS = {"python": "python", "typescript": "typescript", "javascript": "javascript", "go": "go", "rust": "rust"}
# (edit glob for the hook `if` rule, languages that must be present, exact suffixes the hook lints).
# Permission-rule globs are gitignore-style (no brace expansion), so the JS glob is a broad pre-filter and the hook checks suffixes.
PY_GLOB, JS_GLOB = ("**/*.py", ("python",), ".py"), ("**/*.[jt]s*", ("typescript", "javascript"), ".js,.jsx,.ts,.tsx")
LINTER_GLOBS = {"ruff": PY_GLOB, "flake8": PY_GLOB, "pylint": PY_GLOB, "eslint": JS_GLOB, "biome": JS_GLOB, "prettier": JS_GLOB}

def _rule_content(lang):
    body = (REFS / "rules" / f"{RULE_LANGS[lang]}.md").read_text(encoding="utf-8")
    globs = ", ".join(f'"{g}"' for g in RULE_GLOBS[lang])
    return f"---\npaths: [{globs}]\n---\n\n{body}"

def _hookable_lint_cmd(profile):
    """(lint command without its target, edit glob, suffix list) when the linter's language is in the repo, else None."""
    lint = profile["commands"].get("lint")
    if not lint:
        return None
    cmd = lint["cmd"]
    for suffix in (" .", " ./..."):
        if cmd.endswith(suffix):
            cmd = cmd[: -len(suffix)]
            break
    for tok in cmd.split():
        if tok in LINTER_GLOBS:
            glob, langs, exts = LINTER_GLOBS[tok]
            return (cmd, glob, exts) if any(l in profile["languages"] for l in langs) else None
    return None

AUTOCOMPACT_PCT = "60"  # auto-compact fires at this percentage of the auto-compact window (machine-local, never shared)

def merge_local_settings(existing):
    """Add-only merge into .claude/settings.local.json: env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE when absent. None when env is not an object."""
    st = json.loads(json.dumps(existing)) if existing else {}
    env = st.setdefault("env", {})
    if not isinstance(env, dict): return None
    env.setdefault("CLAUDE_AUTOCOMPACT_PCT_OVERRIDE", AUTOCOMPACT_PCT)
    return st

def _settings_shape_error(st):
    perms = st.get("permissions", {})
    if not isinstance(perms, dict): return "permissions is not an object"
    if not isinstance(perms.get("allow", []), list): return "permissions.allow is not a list"
    hooks = st.get("hooks", {})
    if not isinstance(hooks, dict): return "hooks is not an object"
    post = hooks.get("PostToolUse", [])
    if not isinstance(post, list) or not all(isinstance(e, dict) and isinstance(e.get("hooks", []), list)
                                             and all(isinstance(h, dict) for h in e.get("hooks", [])) for e in post):
        return "hooks.PostToolUse is not a list of hook objects"
    return None

def merge_settings(existing, profile):
    st = json.loads(json.dumps(existing)) if existing else {}
    perms = st.setdefault("permissions", {}); allow = perms.setdefault("allow", [])
    for c in profile["commands"].values():
        rule = f"Bash({c['cmd']} *)"
        if rule not in allow: allow.append(rule)
    tp = (profile.get("team_profile") or {}).get("maturity") or "active"
    st.setdefault("effortLevel", "high" if tp == "legacy" else "medium")
    hook = _hookable_lint_cmd(profile)
    if hook:
        hooks = st.setdefault("hooks", {}); post = hooks.setdefault("PostToolUse", [])
        handler = {"type": "command", "command": "python3", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/lint_on_edit.py"], "if": f"Edit({hook[1]})", "timeout": 60}
        if not any(h.get("if") == handler["if"] for e in post for h in e.get("hooks", [])):
            post.append({"matcher": "Edit|Write", "hooks": [handler]})
    return st

def plan(profile):
    root = Path(profile["root"]); items = []; ex = profile["existing"]
    cur = (root / "CLAUDE.md").read_text(encoding="utf-8", errors="replace") if ex["CLAUDE.md"]["exists"] else None
    new = render_claude_md(profile, cur)
    if (root / "CLAUDE.md").is_symlink():
        items.append({"path": "CLAUDE.md", "action": "skip", "reason": "CLAUDE.md is a symlink; add the blocks to its target by hand", "content": None})
    else:
        items.append({"path": "CLAUDE.md", "action": "create" if cur is None else ("update" if new != cur else "skip"), "reason": "repo facts + verification block", "content": new})
    total = sum(profile["languages"].values()) or 1
    for lang, n in profile["languages"].items():
        if lang in RULE_GLOBS and n / total >= 0.05:
            rel = f".claude/rules/{RULE_LANGS[lang]}.md"
            if (root / rel).exists():
                items.append({"path": rel, "action": "skip", "reason": "exists; not owned", "content": None})
            elif not any(i["path"] == rel for i in items):
                items.append({"path": rel, "action": "create", "reason": f"{lang} path-scoped rules", "content": _rule_content(lang)})
    existing_st = None; reason = "allow rules for detected commands + lint hook + effortLevel"
    if ex[".claude/settings.json"]["exists"]:
        try:
            raw = (root / ".claude/settings.json").read_text(encoding="utf-8")
            parsed = json.loads(raw)
            if not isinstance(parsed, dict):
                raise json.JSONDecodeError("settings.json must be a JSON object", raw, 0)
            existing_st = parsed
        except (json.JSONDecodeError, UnicodeDecodeError, OSError) as e:
            items.append({"path": ".claude/settings.json", "action": "skip", "reason": f"unparseable: {e}", "content": None}); existing_st = "bad"
        if existing_st != "bad" and _settings_shape_error(existing_st):
            items.append({"path": ".claude/settings.json", "action": "skip", "reason": f"unexpected shape: {_settings_shape_error(existing_st)}", "content": None}); existing_st = "bad"
    hook_spec = _hookable_lint_cmd(profile); hook_cmd = hook_spec[0] if hook_spec else None
    if existing_st != "bad":
        merged_st = merge_settings(existing_st, profile)
        merged = json.dumps(merged_st, indent=2, ensure_ascii=False) + "\n"
        st_action = "skip" if existing_st is not None and merged_st == existing_st else ("create" if existing_st is None else "update")
        items.append({"path": ".claude/settings.json", "action": st_action, "reason": reason, "content": merged})
    if hook_cmd and existing_st != "bad":
        hook = (HERE / "lint_on_edit.py").read_text(encoding="utf-8").replace("__LINT_CMD__", hook_cmd).replace("__EXTS__", hook_spec[2])
        cur_hook = (root / ".claude/hooks/lint_on_edit.py").read_text(encoding="utf-8", errors="replace") if ex[".claude/hooks/lint_on_edit.py"]["exists"] else None
        hook_action = "skip" if cur_hook is not None and hook == cur_hook else ("create" if not ex[".claude/hooks/lint_on_edit.py"]["exists"] else "update")
        items.append({"path": ".claude/hooks/lint_on_edit.py", "action": hook_action, "reason": "lint on edit", "content": hook})
    local_rel = ".claude/settings.local.json"; existing_local = None
    if ex[local_rel]["exists"]:
        try:
            parsed = json.loads((root / local_rel).read_text(encoding="utf-8"))
            if not isinstance(parsed, dict): raise ValueError("settings.local.json must be a JSON object")
            existing_local = parsed
        except (ValueError, UnicodeDecodeError, OSError) as e:
            items.append({"path": local_rel, "action": "skip", "reason": f"unparseable: {e}", "content": None}); existing_local = "bad"
    if existing_local != "bad":
        merged_local = merge_local_settings(existing_local)
        if merged_local is None:
            items.append({"path": local_rel, "action": "skip", "reason": "unexpected shape: env is not an object", "content": None})
        else:
            local_action = "skip" if existing_local is not None and merged_local == existing_local else ("create" if existing_local is None else "update")
            items.append({"path": local_rel, "action": local_action, "reason": f"auto-compact at {AUTOCOMPACT_PCT}% of the window (machine-local)",
                          "content": json.dumps(merged_local, indent=2, ensure_ascii=False) + "\n"})
    tp = profile.get("team_profile")
    if tp:
        if ex[".claude/team-profile.json"]["exists"]:
            items.append({"path": ".claude/team-profile.json", "action": "skip", "reason": "exists; not overwritten", "content": None})
        else:
            items.append({"path": ".claude/team-profile.json", "action": "create", "reason": "team profile for /team", "content": json.dumps({"maturity": tp["maturity"], "detected_by": "setup-repo"}, indent=2) + "\n"})
    gi = (root / ".gitignore").read_text(encoding="utf-8", errors="replace") if (root / ".gitignore").exists() else ""
    missing = [l for l in (".claude/team-profile.json", ".claude/settings.local.json") if l not in gi]
    if missing:
        items.append({"path": ".gitignore", "action": "update" if gi else "create", "reason": "ignore machine-local files", "content": gi.rstrip("\n") + ("\n" if gi else "") + "".join(l + "\n" for l in missing)})
    recs = ["Turn on the sandbox (`/sandbox`) so allowlisted commands run inside OS boundaries.",
            "Project allow rules and hooks apply only after you trust this folder (workspace trust dialog).",
            "Set `syncClaudeAiSkills: true` in ~/.claude/settings.json if you want claude.ai skills here."]
    if cur is not None and "<!-- setup-repo:" not in cur and ex["CLAUDE.md"]["lines"] > 200:
        recs.append(f"CLAUDE.md is {ex['CLAUDE.md']['lines']} lines; the docs recommend under 200 — move reference material into .claude/rules/ or skills.")
    if any(l in ("typescript", "go", "rust") for l in profile["languages"]):
        recs.append("Install a code-intelligence plugin for typed languages (`/plugin` → code intelligence).")
    for lang in profile["languages"]:
        if lang == "python": recs.append("Toolkit skills that load themselves on .py files: python-patterns, python-testing, fastapi-patterns.")
        if lang in ("typescript", "javascript"): recs.append("Toolkit skills that load themselves on .ts/.tsx: react-patterns, react-best-practices, motion-*.")
    return {"root": str(root), "items": items, "recommendations": recs}

ALLOWED = ("CLAUDE.md", ".gitignore")

def _atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".setup-repo.")
    with os.fdopen(fd, "w", encoding="utf-8") as fh: fh.write(text)
    os.replace(tmp, path)

def apply(plan_dict, root):
    """Write the plan's items into `root` (plan_dict["root"] is ignored). Every target is checked before any write."""
    root = Path(root).resolve(); claude_dir = (root / ".claude").resolve(); todo = []; written = []
    if not claude_dir.is_relative_to(root):
        raise RuntimeError(f"refusing to write: .claude resolves outside the repo ({claude_dir})")
    for item in plan_dict["items"]:
        if item["action"] == "skip" or item["content"] is None: continue
        target = (root / item["path"]).resolve()
        if not (target in [root / a for a in ALLOWED] or target.is_relative_to(claude_dir)):
            raise RuntimeError(f"refusing to write outside allowed paths: {item['path']}")
        todo.append((item["path"], target, item["content"]))
    for rel, target, content in todo:
        _atomic_write(target, content); written.append(rel); print(f"wrote {rel}", flush=True)
    return written

def check(profile):
    return [i for i in plan(profile)["items"] if i["action"] != "skip" and i["content"] is not None
            and (not (Path(profile["root"]) / i["path"]).exists() or (Path(profile["root"]) / i["path"]).read_text(encoding="utf-8", errors="replace") != i["content"])]

def main(argv):
    ap = argparse.ArgumentParser(description="/setup-repo engine")
    ap.add_argument("cmd", choices=["detect", "plan", "apply", "check"]); ap.add_argument("--repo", default=".")
    ap.add_argument("--plan", help="apply: plan JSON file (default: compute now)")
    a = ap.parse_args(argv); prof = detect(a.repo)
    if a.cmd == "detect": print(json.dumps(prof, indent=2)); return 0
    if a.cmd == "plan": print(json.dumps(plan(prof), indent=2)); return 0
    if a.cmd == "apply":
        pl = json.load(open(a.plan)) if a.plan else plan(prof)
        apply(pl, a.repo)
        drift = check(detect(a.repo)); print("check: clean" if not drift else "check: DRIFT " + ", ".join(i["path"] for i in drift)); return 0 if not drift else 1
    drift = check(prof)
    for i in drift: print(f"{i['action']:6} {i['path']}  — {i['reason']}")
    print("check: clean" if not drift else f"check: {len(drift)} item(s) would change"); return 0 if not drift else 1

if __name__ == "__main__":
    try: sys.exit(main(sys.argv[1:]))
    except Exception as e:  # noqa: BLE001
        print(f"internal error: {e}", file=sys.stderr); sys.exit(2)
