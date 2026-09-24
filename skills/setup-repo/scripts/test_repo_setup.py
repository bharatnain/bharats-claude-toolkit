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
    assert tp is None or tp["maturity"] in ("greenfield", "active", "legacy")
