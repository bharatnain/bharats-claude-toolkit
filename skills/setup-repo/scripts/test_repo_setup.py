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

def test_git_facts(tmp_path):
    root = make_repo(tmp_path, PY_UV)
    subprocess.run(["git", "checkout", "-qb", "claude/feature-x"], cwd=root, check=True)
    g = rs.detect(root)["git"]
    assert g["default_branch"] in ("main", "unknown")
    assert "claude/" in g["branch_prefixes"]
    assert g["merge_style"] == "unknown"

def test_team_profile_present(tmp_path):
    tp = rs.detect(make_repo(tmp_path, PY_UV))["team_profile"]
    assert tp is not None and tp["maturity"] in ("greenfield", "active", "legacy") and isinstance(tp["signals"], dict)

def test_render_claude_md_new(tmp_path):
    prof = rs.detect(make_repo(tmp_path, PY_UV))
    text = rs.render_claude_md(prof, None)
    assert "<!-- setup-repo:verify -->" in text and "uv run pytest" in text
    assert "{repo_name}" not in text and "{command_lines}" not in text
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

def test_render_removes_collapsed_block_cleanly(tmp_path):
    prof = rs.detect(make_repo(tmp_path, {"README.md": "x\n"}))
    existing = "Keep this line.\n\n<!-- setup-repo:verify -->\nold\n<!-- /setup-repo:verify -->\n\nSome text after.\n"
    text = rs.render_claude_md(prof, existing)
    assert "setup-repo:verify" not in text
    assert "Keep this line.\n\nSome text after." in text
    assert "\n\n\n" not in text

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

def test_plan_hook_command_strips_dot(tmp_path):
    prof = rs.detect(make_repo(tmp_path, PY_UV))
    pl = rs.plan(prof)
    paths = {i["path"]: i for i in pl["items"]}
    content = paths[".claude/hooks/lint_on_edit.py"]["content"]
    assert "uv run ruff check" in content
    assert "check ." not in content
    st = json.loads(paths[".claude/settings.json"]["content"])
    assert st["hooks"]["PostToolUse"][0]["if"] == "Edit(**/*.py)"

def test_plan_no_hook_for_make_lint(tmp_path):
    root = make_repo(tmp_path, {"Makefile": "test:\n\tgo test ./...\nlint:\n\tgolangci-lint run\n", "go.mod": "module x\n", "main.go": "package main\n"})
    pl = rs.plan(rs.detect(root))
    paths = {i["path"]: i for i in pl["items"]}
    assert ".claude/hooks/lint_on_edit.py" not in paths
    st = json.loads(paths[".claude/settings.json"]["content"])
    assert "hooks" not in st

def test_plan_rules_js_and_ts(tmp_path):
    files = dict(NODE_PNPM)
    files.update({"src/a.js": "var a=1\n", "src/b.js": "var b=1\n", "src/c.js": "var c=1\n"})
    root = make_repo(tmp_path, files)
    pl = rs.plan(rs.detect(root))
    paths = {i["path"]: i for i in pl["items"]}
    assert paths[".claude/rules/javascript.md"]["action"] == "create"
    assert paths[".claude/rules/typescript.md"]["action"] == "create"
    assert paths[".claude/rules/javascript.md"]["content"].startswith('---\npaths: ["**/*.{js,jsx,mjs}"]')
    assert paths[".claude/rules/typescript.md"]["content"].startswith('---\npaths: ["**/*.{ts,tsx}"]')

def test_plan_second_run_is_all_skip(tmp_path):
    root = make_repo(tmp_path, PY_UV)
    pl = rs.plan(rs.detect(root))
    for item in pl["items"]:
        if item["content"] is not None:
            p = root / item["path"]; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(item["content"])
    pl2 = rs.plan(rs.detect(root))
    assert pl2["items"]
    assert all(i["action"] == "skip" for i in pl2["items"])

def test_plan_skips_unparseable_settings(tmp_path):
    root = make_repo(tmp_path, PY_UV)
    (root / ".claude").mkdir(); (root / ".claude/settings.json").write_text("{not json")
    pl = rs.plan(rs.detect(root))
    paths = {i["path"]: i for i in pl["items"]}
    assert paths[".claude/settings.json"]["action"] == "skip"
    assert paths["CLAUDE.md"]["action"] == "create"
    assert paths[".claude/rules/python.md"]["action"] == "create"
