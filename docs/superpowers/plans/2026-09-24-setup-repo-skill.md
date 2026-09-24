# `/setup-repo` Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A user-invoked `/setup-repo` skill that detects a repo's stack, proposes a plan, and on one yes writes a repo-facts CLAUDE.md, path-scoped rules, project permissions + a lint-on-edit hook, a team profile and effort default, idempotently.

**Architecture:** A stdlib Python CLI (`repo_setup.py`) with three subcommands — `detect` (evidence-only JSON profile), `plan` (JSON plan + rendered contents, marker-block aware), `apply` (atomic writes, then `check`) — driven by a short SKILL.md. Templates live in `references/`. Tests use pytest on fixture repos created in `tmp_path`.

**Tech Stack:** Python 3.10+ stdlib only (json, re, subprocess, pathlib, tempfile); pytest via `uv run --quiet --python 3.12 --with pytest pytest`; existing `scripts/team_profile_detect.py` (`gather_signals(root)`, `classify(signals)`).

**Spec:** `docs/superpowers/specs/2026-09-24-setup-repo-skill-design.md`

## Global Constraints

- Stdlib only; no network; the script never writes outside `CLAUDE.md`, `.claude/`, and `.gitignore` of the target repo.
- Commands are only reported when evidenced by a config file; every command carries its `source`.
- `CLAUDE.md` edits touch only text between `<!-- setup-repo:<block> -->` and `<!-- /setup-repo:<block> -->`.
- `.claude/settings.json` merge is add-only; `effortLevel` set only if absent.
- Skill frontmatter: `name: setup-repo`, `disable-model-invocation: true`, `argument-hint: "[--check]"`; SKILL.md under 120 lines.
- Exit codes: 0 clean, 1 drift or plan pending, 2 internal error.
- Repo rules: validators green (`python3 scripts/validate_skills.py --strict-yaml`, `--check-catalog` after `--catalog`); commit with the session's attribution trailer.

## File Structure

- `skills/setup-repo/SKILL.md` — the procedure Claude follows (detect → plan → confirm → apply → evidence).
- `skills/setup-repo/scripts/repo_setup.py` — detector, planner, applier, check; CLI.
- `skills/setup-repo/scripts/lint_on_edit.py` — hook copied into target repos; runs the configured lint command on the edited file.
- `skills/setup-repo/scripts/test_repo_setup.py` — pytest suite with fixture builders.
- `skills/setup-repo/references/claude-md-blocks.md` — the four owned blocks as templates with `{placeholders}` the planner fills (never left unfilled).
- `skills/setup-repo/references/rules/{python,typescript,go,rust}.md` — rule bodies; planner prepends `paths:` frontmatter.

---

### Task 1: Detector — languages, package manager, existing files

**Files:**
- Create: `skills/setup-repo/scripts/repo_setup.py`
- Test: `skills/setup-repo/scripts/test_repo_setup.py`

**Interfaces:**
- Produces: `detect(root: Path) -> dict` with keys `languages` (dict ext→count, top 5), `package_manager` (str|None), `existing` (dict of path→{"exists": bool, "lines": int}), `git` (dict), `commands` (dict, filled in Task 2), `team_profile` (Task 3), `size` (int tracked files).
- Produces: `LANG_EXT = {"python": [".py"], "typescript": [".ts", ".tsx"], "javascript": [".js", ".jsx", ".mjs"], "go": [".go"], "rust": [".rs"], "ruby": [".rb"]}`.

- [ ] **Step 1: Write the failing tests**

```python
# skills/setup-repo/scripts/test_repo_setup.py
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import repo_setup as rs

def make_repo(tmp_path, files):
    root = tmp_path / "repo"; root.mkdir()
    for rel, text in files.items():
        p = root / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text)
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init"], cwd=root, check=True)
    return root

PY_UV = {"pyproject.toml": '[project]\nname="x"\n[tool.pytest.ini_options]\ntestpaths=["tests"]\n[tool.ruff]\nline-length=100\n',
         "uv.lock": "", "src/app.py": "x=1\n", "tests/test_app.py": "def test_x(): pass\n"}

def test_detect_languages_and_pm(tmp_path):
    root = make_repo(tmp_path, PY_UV)
    p = rs.detect(root)
    assert p["languages"]["python"] == 2
    assert p["package_manager"] == "uv"
    assert p["existing"]["CLAUDE.md"]["exists"] is False
    assert p["size"] == 4

def test_detect_empty_repo(tmp_path):
    root = make_repo(tmp_path, {"README.md": "hi\n"})
    p = rs.detect(root)
    assert p["languages"] == {} and p["package_manager"] is None
```

- [ ] **Step 2: Run to verify failure**

Run: `uv run --quiet --python 3.12 --with pytest pytest -q skills/setup-repo/scripts/test_repo_setup.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'repo_setup'`

- [ ] **Step 3: Implement detector core**

```python
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

def detect(root):
    root = Path(root).resolve()
    files = _tracked(root)
    return {"root": str(root), "languages": _languages(files), "package_manager": _package_manager(root),
            "existing": _existing(root), "commands": {}, "git": {}, "team_profile": None, "size": len(files)}
```

- [ ] **Step 4: Run tests → PASS**

Run: `uv run --quiet --python 3.12 --with pytest pytest -q skills/setup-repo/scripts/test_repo_setup.py`
Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add skills/setup-repo/scripts/repo_setup.py skills/setup-repo/scripts/test_repo_setup.py
git commit -m "feat(setup-repo): detector core (languages, package manager, existing files)"
```

---

### Task 2: Detector — evidenced commands

**Files:**
- Modify: `skills/setup-repo/scripts/repo_setup.py` (add `_commands`, wire into `detect`)
- Test: `skills/setup-repo/scripts/test_repo_setup.py`

**Interfaces:**
- Produces: `profile["commands"]: dict[str, {"cmd": str, "source": str}]` with keys among `test`, `lint`, `format`, `typecheck`, `build`.

- [ ] **Step 1: Write the failing tests**

```python
NODE_PNPM = {"package.json": json.dumps({"name": "x", "scripts": {"test": "vitest run", "lint": "eslint .", "build": "tsc -p .", "typecheck": "tsc --noEmit"}}),
             "pnpm-lock.yaml": "", "src/index.ts": "export const a=1\n"}

def test_commands_python_uv(tmp_path):
    p = rs.detect(make_repo(tmp_path, PY_UV))["commands"]
    assert p["test"] == {"cmd": "uv run pytest", "source": "pyproject.toml"}
    assert p["lint"] == {"cmd": "uv run ruff check .", "source": "pyproject.toml"}
    assert "build" not in p

def test_commands_node_pnpm(tmp_path):
    p = rs.detect(make_repo(tmp_path, NODE_PNPM))["commands"]
    assert p["test"] == {"cmd": "pnpm test", "source": "package.json"}
    assert p["typecheck"] == {"cmd": "pnpm typecheck", "source": "package.json"}
    assert p["build"] == {"cmd": "pnpm build", "source": "package.json"}

def test_commands_makefile(tmp_path):
    p = rs.detect(make_repo(tmp_path, {"Makefile": "test:\n\tgo test ./...\nlint:\n\tgolangci-lint run\n", "go.mod": "module x\n", "main.go": "package main\n"}))["commands"]
    assert p["test"] == {"cmd": "make test", "source": "Makefile"}
```

- [ ] **Step 2: Run → FAIL** (`KeyError: 'test'`)

- [ ] **Step 3: Implement**

```python
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
        has_pytest = "[tool.pytest" in py or (root / "pytest.ini").exists() or any((root / d).is_dir() for d in ("tests", "test"))
        if has_pytest and "test" not in cmds:
            cmds["test"] = {"cmd": f"{prefix}pytest", "source": "pyproject.toml" if "[tool.pytest" in py else ("pytest.ini" if (root / "pytest.ini").exists() else "tests/")}
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
```

In `detect`, replace `"commands": {}` with `"commands": _commands(root, _package_manager(root))`.

- [ ] **Step 4: Run → 5 passed**
- [ ] **Step 5: Commit** — `git commit -am "feat(setup-repo): evidenced command detection"`

---

### Task 3: Detector — git facts and team profile

**Files:**
- Modify: `skills/setup-repo/scripts/repo_setup.py`
- Test: `skills/setup-repo/scripts/test_repo_setup.py`

**Interfaces:**
- Produces: `profile["git"] = {"default_branch": str, "remote_host": str|None, "branch_prefixes": [str], "merge_style": "merge"|"squash"|"unknown"}`; `profile["team_profile"] = {"maturity": str, "signals": dict}` or `None` when `team_profile_detect` is unavailable.

- [ ] **Step 1: Write the failing tests**

```python
def test_git_facts(tmp_path):
    root = make_repo(tmp_path, PY_UV)
    subprocess.run(["git", "checkout", "-qb", "claude/feature-x"], cwd=root, check=True)
    g = rs.detect(root)["git"]
    assert g["default_branch"] in ("main", "unknown")
    assert "claude/" in g["branch_prefixes"]
    assert g["merge_style"] == "unknown"

def test_team_profile_present(tmp_path):
    tp = rs.detect(make_repo(tmp_path, PY_UV))["team_profile"]
    assert tp is None or tp["maturity"] in ("greenfield", "active", "legacy")
```

- [ ] **Step 2: Run → FAIL** (`KeyError: 'default_branch'`)

- [ ] **Step 3: Implement**

```python
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
    except Exception:  # noqa: BLE001
        return None
```

Wire into `detect`: `"git": _git_facts(root), "team_profile": _team_profile(root)`. If `classify` returns a tuple (name, reasons), extend `_profile_name` with `if isinstance(result, (tuple, list)): return str(result[0])` — check `python3 -c "import sys;sys.path.insert(0,'scripts');import team_profile_detect as t;print(t.classify(t.gather_signals('.')))"` once and keep only the branch that matches.

- [ ] **Step 4: Run → 7 passed**
- [ ] **Step 5: Commit** — `git commit -am "feat(setup-repo): git facts + team profile detection"`

---

### Task 4: Planner — CLAUDE.md marker blocks

**Files:**
- Create: `skills/setup-repo/references/claude-md-blocks.md`
- Modify: `skills/setup-repo/scripts/repo_setup.py`
- Test: `skills/setup-repo/scripts/test_repo_setup.py`

**Interfaces:**
- Produces: `render_claude_md(profile: dict, existing_text: str|None) -> str` and `BLOCKS = ("verify", "etiquette", "working", "compaction")`; markers `<!-- setup-repo:{block} -->` / `<!-- /setup-repo:{block} -->`.

- [ ] **Step 1: Write the template**

```markdown
<!-- skills/setup-repo/references/claude-md-blocks.md — sections separated by "## block:<name>" -->
## block:header
# {repo_name}

{one_liner}

## block:verify
## Verify before done
{command_lines}
- Paste the command and its output as evidence; do not claim a pass you did not run.

## block:etiquette
## Etiquette
- Default branch `{default_branch}`; branches `{branch_prefix}<topic>`; PRs merged with {merge_style} commits; no force-push.

## block:working
## How work flows here
- Explore → plan (plan mode for multi-file changes) → implement → run the check above.
- Unattended runs: `/goal <the check passes and git status is clean>`.
- Before merge: `code-reviewer` on the diff against the task's acceptance criteria.
- Multi-file or multi-agent work: `/team <goal>` (team profile: {maturity}); parallel sessions use worktrees.
- Tasks live in beads (`bd`), auto-initialised per repo.
- Effort: `{effort}` for build work; `high` for design, debugging and review.

## block:compaction
## Compaction
When compacting, preserve: files modified this session, the last check result, open task ids, and decisions stated exactly.
```

- [ ] **Step 2: Write the failing tests**

```python
def test_render_claude_md_new(tmp_path):
    prof = rs.detect(make_repo(tmp_path, PY_UV))
    text = rs.render_claude_md(prof, None)
    assert "<!-- setup-repo:verify -->" in text and "uv run pytest" in text
    assert "{" not in text.replace("{", "", 0) or "{repo_name}" not in text
    assert text.count("\n") < 60

def test_render_claude_md_preserves_user_text(tmp_path):
    prof = rs.detect(make_repo(tmp_path, PY_UV))
    existing = "# My repo\n\nKeep this line.\n\n<!-- setup-repo:verify -->\nold\n<!-- /setup-repo:verify -->\n"
    text = rs.render_claude_md(prof, existing)
    assert "Keep this line." in text and "old" not in text
    assert text.count("<!-- setup-repo:verify -->") == 1
    assert "<!-- setup-repo:working -->" in text  # missing blocks appended

def test_render_omits_unknown_blocks(tmp_path):
    prof = rs.detect(make_repo(tmp_path, {"README.md": "x\n"}))
    text = rs.render_claude_md(prof, None)
    assert "setup-repo:verify" not in text and "setup-repo:working" in text
```

- [ ] **Step 3: Run → FAIL** (`AttributeError: render_claude_md`)

- [ ] **Step 4: Implement**

```python
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
```

- [ ] **Step 5: Run → 10 passed**
- [ ] **Step 6: Commit** — `git add -A skills/setup-repo && git commit -m "feat(setup-repo): CLAUDE.md marker-block renderer + templates"`

---

### Task 5: Planner — rules, settings merge, hook file, plan assembly

**Files:**
- Create: `skills/setup-repo/references/rules/python.md`, `typescript.md`, `go.md`, `rust.md`
- Create: `skills/setup-repo/scripts/lint_on_edit.py`
- Modify: `skills/setup-repo/scripts/repo_setup.py`
- Test: `skills/setup-repo/scripts/test_repo_setup.py`

**Interfaces:**
- Produces: `plan(profile: dict) -> dict` = `{"root": str, "items": [{"path": str, "action": "create"|"update"|"skip", "reason": str, "content": str|None}], "recommendations": [str]}`; `RULE_GLOBS = {"python": ["**/*.py"], "typescript": ["**/*.{ts,tsx}"], "javascript": ["**/*.{js,jsx,mjs}"], "go": ["**/*.go"], "rust": ["**/*.rs"]}`; `merge_settings(existing: dict, profile: dict) -> dict`.

- [ ] **Step 1: Write the rule templates** (each ≤20 lines; python shown, others analogous with the language's runner)

```markdown
<!-- skills/setup-repo/references/rules/python.md -->
# Python rules
- Run the repo's test command after changes; add a test for every bug fix.
- Prefer explicit types on public functions; no bare `except`.
- Keep modules under ~300 lines; split by responsibility.
- Never edit lockfiles by hand.
```

- [ ] **Step 2: Write the hook file**

```python
#!/usr/bin/env python3
"""PostToolUse hook: run the repo's lint command on the file Claude just edited. Stdlib only.
Reads the hook JSON on stdin, finds tool_input.file_path, runs LINT_CMD (set by /setup-repo)
with the file appended, prints findings to stdout (they enter context), always exits 0."""
import json, os, shlex, subprocess, sys
LINT_CMD = os.environ.get("SETUP_REPO_LINT_CMD", "__LINT_CMD__")

def main():
    try:
        payload = json.loads(sys.stdin.read(1024 * 1024) or "{}")
    except Exception:  # noqa: BLE001
        return 0
    path = (payload.get("tool_input") or {}).get("file_path")
    if not path or not os.path.isfile(path) or LINT_CMD.startswith("__"):
        return 0
    try:
        p = subprocess.run(shlex.split(LINT_CMD) + [path], capture_output=True, text=True, timeout=60)
        out = (p.stdout + p.stderr).strip()
        if p.returncode != 0 and out:
            print(f"lint ({LINT_CMD}) on {path}:\n{out[:4000]}")
    except Exception:  # noqa: BLE001
        pass
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Write the failing tests**

```python
def test_plan_items_python(tmp_path):
    prof = rs.detect(make_repo(tmp_path, PY_UV))
    pl = rs.plan(prof)
    paths = {i["path"]: i for i in pl["items"]}
    assert paths["CLAUDE.md"]["action"] == "create"
    assert paths[".claude/rules/python.md"]["action"] == "create" and paths[".claude/rules/python.md"]["content"].startswith("---\npaths:")
    st = json.loads(paths[".claude/settings.json"]["content"])
    assert "Bash(uv run pytest *)" in st["permissions"]["allow"]
    assert st["effortLevel"] == "medium"
    hook = st["hooks"]["PostToolUse"][0]
    assert hook["matcher"] == "Edit|Write" and hook["if"] == "Edit(**/*.py)"
    assert paths[".claude/hooks/lint_on_edit.py"]["content"].count("uv run ruff check") == 1
    assert any("sandbox" in r for r in pl["recommendations"])

def test_plan_settings_add_only(tmp_path):
    root = make_repo(tmp_path, PY_UV)
    (root / ".claude").mkdir(); (root / ".claude/settings.json").write_text(json.dumps({"effortLevel": "high", "permissions": {"allow": ["Bash(ls *)"]}}))
    st = json.loads({i["path"]: i for i in rs.plan(rs.detect(root))["items"]}[".claude/settings.json"]["content"])
    assert st["effortLevel"] == "high" and st["permissions"]["allow"][0] == "Bash(ls *)"

def test_plan_skips_existing_rule(tmp_path):
    root = make_repo(tmp_path, PY_UV)
    (root / ".claude/rules").mkdir(parents=True); (root / ".claude/rules/python.md").write_text("mine\n")
    item = {i["path"]: i for i in rs.plan(rs.detect(root))["items"]}[".claude/rules/python.md"]
    assert item["action"] == "skip"
```

- [ ] **Step 4: Run → FAIL** (`AttributeError: plan`)

- [ ] **Step 5: Implement**

```python
RULE_GLOBS = {"python": ["**/*.py"], "typescript": ["**/*.{ts,tsx}"], "javascript": ["**/*.{js,jsx,mjs}"], "go": ["**/*.go"], "rust": ["**/*.rs"]}
RULE_LANGS = {"python": "python", "typescript": "typescript", "javascript": "typescript", "go": "go", "rust": "rust"}

def _rule_content(lang):
    body = (REFS / "rules" / f"{RULE_LANGS[lang]}.md").read_text(encoding="utf-8")
    globs = ", ".join(f'"{g}"' for g in RULE_GLOBS[lang])
    return f"---\npaths: [{globs}]\n---\n\n{body}"

def merge_settings(existing, profile):
    st = json.loads(json.dumps(existing)) if existing else {}
    perms = st.setdefault("permissions", {}); allow = perms.setdefault("allow", [])
    for c in profile["commands"].values():
        rule = f"Bash({c['cmd']} *)"
        if rule not in allow: allow.append(rule)
    tp = (profile.get("team_profile") or {}).get("maturity") or "active"
    st.setdefault("effortLevel", "high" if tp == "legacy" else "medium")
    lint = profile["commands"].get("lint")
    top = max(profile["languages"], key=profile["languages"].get) if profile["languages"] else None
    if lint and top in RULE_GLOBS:
        hooks = st.setdefault("hooks", {}); post = hooks.setdefault("PostToolUse", [])
        glob = RULE_GLOBS[top][0]
        entry = {"matcher": "Edit|Write", "if": f"Edit({glob})", "hooks": [{"type": "command", "command": "python3", "args": [".claude/hooks/lint_on_edit.py"], "timeout": 60}]}
        if not any(e.get("if") == entry["if"] for e in post): post.append(entry)
    return st

def plan(profile):
    root = Path(profile["root"]); items = []; ex = profile["existing"]
    cur = (root / "CLAUDE.md").read_text(encoding="utf-8", errors="replace") if ex["CLAUDE.md"]["exists"] else None
    new = render_claude_md(profile, cur)
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
        try: existing_st = json.loads((root / ".claude/settings.json").read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            items.append({"path": ".claude/settings.json", "action": "skip", "reason": f"unparseable: {e}", "content": None}); existing_st = "bad"
    if existing_st != "bad":
        merged = json.dumps(merge_settings(existing_st, profile), indent=2) + "\n"
        items.append({"path": ".claude/settings.json", "action": "create" if existing_st is None else "update", "reason": reason, "content": merged})
    lint = profile["commands"].get("lint")
    if lint:
        hook = (HERE / "lint_on_edit.py").read_text(encoding="utf-8").replace("__LINT_CMD__", lint["cmd"])
        items.append({"path": ".claude/hooks/lint_on_edit.py", "action": "create" if not ex[".claude/hooks/lint_on_edit.py"]["exists"] else "update", "reason": "lint on edit", "content": hook})
    tp = profile.get("team_profile")
    if tp:
        items.append({"path": ".claude/team-profile.json", "action": "create" if not ex[".claude/team-profile.json"]["exists"] else "update", "reason": "team profile for /team", "content": json.dumps({"maturity": tp["maturity"], "detected_by": "setup-repo"}, indent=2) + "\n"})
    gi = (root / ".gitignore").read_text(encoding="utf-8", errors="replace") if (root / ".gitignore").exists() else ""
    if ".claude/team-profile.json" not in gi:
        items.append({"path": ".gitignore", "action": "update" if gi else "create", "reason": "ignore the machine-local team profile", "content": gi.rstrip("\n") + ("\n" if gi else "") + ".claude/team-profile.json\n"})
    recs = ["Turn on the sandbox (`/sandbox`) so allowlisted commands run inside OS boundaries.",
            "Project allow rules and hooks apply only after you trust this folder (workspace trust dialog)."]
    if any(l in ("typescript", "go", "rust") for l in profile["languages"]):
        recs.append("Install a code-intelligence plugin for typed languages (`/plugin` → code intelligence).")
    for lang in profile["languages"]:
        if lang == "python": recs.append("Toolkit skills that load themselves on .py files: python-patterns, python-testing, fastapi-patterns.")
        if lang in ("typescript", "javascript"): recs.append("Toolkit skills that load themselves on .ts/.tsx: react-patterns, react-best-practices, motion-*.")
    return {"root": str(root), "items": items, "recommendations": recs}
```

- [ ] **Step 6: Run → 13 passed**
- [ ] **Step 7: Commit** — `git add -A skills/setup-repo && git commit -m "feat(setup-repo): planner (rules, settings merge, lint hook, recommendations)"`

---

### Task 6: Applier, check, CLI

**Files:**
- Modify: `skills/setup-repo/scripts/repo_setup.py`
- Test: `skills/setup-repo/scripts/test_repo_setup.py`

**Interfaces:**
- Produces: `apply(plan_dict) -> list[str]` (paths written), `check(profile) -> list[dict]` (plan items with action != skip = drift), CLI `repo_setup.py detect|plan|apply|check [--repo PATH] [--plan FILE] [--json]`.

- [ ] **Step 1: Write the failing tests**

```python
def test_apply_then_check_clean(tmp_path):
    root = make_repo(tmp_path, PY_UV)
    written = rs.apply(rs.plan(rs.detect(root)))
    assert "CLAUDE.md" in written and (root / ".claude/hooks/lint_on_edit.py").exists()
    assert rs.check(rs.detect(root)) == []           # idempotent
    for p in written: assert p == "CLAUDE.md" or p.startswith(".claude/") or p == ".gitignore"

def test_cli_check_exit_code(tmp_path):
    root = make_repo(tmp_path, PY_UV)
    r = subprocess.run([sys.executable, str(Path(rs.__file__)), "check", "--repo", str(root)], capture_output=True, text=True)
    assert r.returncode == 1 and "CLAUDE.md" in r.stdout
    rs.apply(rs.plan(rs.detect(root)))
    r = subprocess.run([sys.executable, str(Path(rs.__file__)), "check", "--repo", str(root)], capture_output=True, text=True)
    assert r.returncode == 0
```

- [ ] **Step 2: Run → FAIL** (`AttributeError: apply`)

- [ ] **Step 3: Implement**

```python
ALLOWED = ("CLAUDE.md", ".gitignore")

def _atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".setup-repo.")
    with os.fdopen(fd, "w", encoding="utf-8") as fh: fh.write(text)
    os.replace(tmp, path)

def apply(plan_dict):
    root = Path(plan_dict["root"]); written = []
    for item in plan_dict["items"]:
        if item["action"] == "skip" or item["content"] is None: continue
        rel = item["path"]
        if not (rel in ALLOWED or rel.startswith(".claude/")):
            raise RuntimeError(f"refusing to write outside allowed paths: {rel}")
        _atomic_write(root / rel, item["content"]); written.append(rel)
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
        for p in apply(pl): print(f"wrote {p}")
        drift = check(detect(a.repo)); print("check: clean" if not drift else "check: DRIFT " + ", ".join(i["path"] for i in drift)); return 0 if not drift else 1
    drift = check(prof)
    for i in drift: print(f"{i['action']:6} {i['path']}  — {i['reason']}")
    print("check: clean" if not drift else f"check: {len(drift)} item(s) would change"); return 0 if not drift else 1

if __name__ == "__main__":
    try: sys.exit(main(sys.argv[1:]))
    except Exception as e:  # noqa: BLE001
        print(f"internal error: {e}", file=sys.stderr); sys.exit(2)
```

- [ ] **Step 4: Run → 15 passed**
- [ ] **Step 5: Commit** — `git commit -am "feat(setup-repo): apply, check, CLI"`

---

### Task 7: SKILL.md, catalog, smoke run

**Files:**
- Create: `skills/setup-repo/SKILL.md`
- Modify: `SKILLS.md` (regenerated), `README.md` (one bullet under "Working with this toolkit"), `CHANGELOG.md` (`[Unreleased]`)

**Interfaces:**
- Consumes: CLI from Task 6.

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: setup-repo
description: Set up a repository for efficient Claude Code work — detect the stack and its test/lint commands, then write a repo-facts CLAUDE.md with a verification block, path-scoped rules, project permissions and a lint-on-edit hook, a team profile and effort default. Idempotent; `--check` reports drift only.
disable-model-invocation: true
argument-hint: "[--check]"
---

# /setup-repo

Engine: `scripts/repo_setup.py` (stdlib). Run every command from the repo root.

1. `python3 <skill>/scripts/repo_setup.py detect` → read the JSON. If `commands` is empty, say so and still continue (only the working/compaction blocks will be written).
2. `python3 <skill>/scripts/repo_setup.py plan` → present it as a list: `action path — reason`, then the `recommendations`. Show the rendered CLAUDE.md verbatim (it is short).
3. With `--check`: run `check` instead of `plan`, print its output, stop.
4. Ask once: "Apply these N changes?" On yes run `apply` (it re-checks and prints `check: clean`); paste that line as evidence. On no, stop.
5. Close with a short **how to use this setup** note (≤6 lines, from the profile): the check to run before done; `/goal <check passes>` for unattended runs; `/team <goal>` for multi-file work (team profile: <maturity>); effort `<effort>` for build work, `high` for design/review. Then the **status dashboard option**: "Enable the status dashboard with `/board` (shows waiting-on-you, in-flight work, sessions and PRs; refreshes after every turn)." Then the next steps: trust the folder if this is its first session; `/reload-plugins` or restart; run `/context` to confirm what loads.

`<skill>` is this skill's directory (`${CLAUDE_PLUGIN_ROOT}/skills/setup-repo` when installed as a plugin). Never edit CLAUDE.md text outside the `<!-- setup-repo:* -->` markers by hand from this skill; users own the rest.
```

- [ ] **Step 2: Validate + catalog**

Run: `python3 scripts/validate_skills.py --strict-yaml && python3 scripts/validate_skills.py --catalog && python3 scripts/validate_skills.py --check-catalog`
Expected: `0 errors`, `SKILLS.md is up to date`

- [ ] **Step 3: Smoke on this repo**

Run: `python3 skills/setup-repo/scripts/repo_setup.py check --repo .`
Expected: exit 1 listing `CLAUDE.md update` (the toolkit's CLAUDE.md has no markers yet) — do not apply here; the toolkit's CLAUDE.md is hand-maintained.

- [ ] **Step 4: Docs** — README bullet: "`/setup-repo` prepares any repo (CLAUDE.md facts + check, rules, permissions, lint hook, team profile); `--check` shows drift." CHANGELOG `[Unreleased]`: "Added: `/setup-repo` skill (engine `skills/setup-repo/scripts/repo_setup.py`, 15 tests)."

- [ ] **Step 5: Commit** — `git add -A && git commit -m "feat: /setup-repo skill + docs"`

---

## Self-review

Spec coverage: detect (T1–T3), plan incl. markers/rules/settings/hook/team profile/recommendations (T4–T5), apply+check+exit codes (T6), skill (incl. the closing how-to-use note and the `/board` option) + docs + smoke (T7). Error handling: unparseable settings → skip item (T5); no stack → verify/etiquette omitted (T4 test); write outside allowed paths raises (T6). Idempotency test present (T6). No placeholders remain; names (`detect`, `plan`, `apply`, `check`, `render_claude_md`, `merge_settings`, `RULE_GLOBS`) are consistent across tasks.
