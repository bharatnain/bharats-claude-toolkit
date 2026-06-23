#!/usr/bin/env python3
"""Self-test / CI gate for scripts/quality_gate.py. Stdlib only.

Builds synthetic git fixtures under tempfile.mkdtemp() and asserts cases (a)-(e),
invoking the runner via subprocess. Prints PASS/FAIL per case; exits 0 iff all
assertions hold, else 1.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RUNNER = str(Path(__file__).resolve().parent / "quality_gate.py")


def git_init(path):
    env = dict(os.environ)
    env["GIT_AUTHOR_NAME"] = "selftest"
    env["GIT_AUTHOR_EMAIL"] = "selftest@example.com"
    env["GIT_COMMITTER_NAME"] = "selftest"
    env["GIT_COMMITTER_EMAIL"] = "selftest@example.com"
    subprocess.run(["git", "init", "-q"], cwd=path, env=env, check=True)
    subprocess.run(["git", "add", "-A"], cwd=path, env=env, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init", "--allow-empty"],
                   cwd=path, env=env, check=True)
    return env


def run_runner(root_args, extra_env=None):
    """Invoke runner with --format json. Return (returncode, parsed_json|None, raw)."""
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    proc = subprocess.run(
        [sys.executable, RUNNER] + root_args,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env,
    )
    parsed = None
    try:
        parsed = json.loads(proc.stdout)
    except Exception:
        parsed = None
    return proc.returncode, parsed, proc.stdout + proc.stderr


def write(path, name, content):
    p = Path(path) / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def blocking_profile(path):
    """Write a profile making all checks blocking; return its path."""
    prof = {
        "checks": {
            "lint": {"blocking": True, "scope": "all"},
            "typecheck": {"blocking": True, "scope": "all"},
            "test": {"blocking": True, "scope": "all"},
            "build": {"blocking": True, "scope": "all"},
        }
    }
    pp = Path(path) / "profile.json"
    pp.write_text(json.dumps(prof), encoding="utf-8")
    return str(pp)


def sanitized_path_env():
    """A PATH containing only the python bindir + an empty temp dir, so that
    shutil.which() finds neither ruff/flake8/mypy/pyright/pytest, and git remains
    reachable (git resolved from its own dir)."""
    empty = tempfile.mkdtemp(prefix="qg_emptybin_")
    py_bin = os.path.dirname(sys.executable)
    git_path = shutil.which("git")
    dirs = [empty, py_bin]
    if git_path:
        dirs.append(os.path.dirname(git_path))
    return os.pathsep.join(dirs), empty


def check_schema_and_exit(parsed, rc, errors):
    """Case (e) invariants, applied to every case."""
    if parsed is None:
        errors.append("json did not parse")
        return
    if parsed.get("schema") != "quality_gate/v1":
        errors.append(f"schema != quality_gate/v1 (got {parsed.get('schema')})")
    if parsed.get("exit_code") != rc:
        errors.append(f"json exit_code {parsed.get('exit_code')} != returncode {rc}")


def case_a():
    """python fixture with a failing blocking check → exit 1, verdict fail.
    Build a fake ruff on PATH that always exits 1."""
    d = tempfile.mkdtemp(prefix="qg_a_")
    try:
        write(d, "pyproject.toml", "[project]\nname='x'\nversion='0'\n")
        write(d, "mod.py", "x = 1\n")
        git_init(d)
        # fake bin dir with a ruff that fails
        fakebin = Path(d) / "fakebin"
        fakebin.mkdir()
        ruff = fakebin / "ruff"
        ruff.write_text("#!/bin/sh\necho 'E001 fake lint error'\nexit 1\n")
        ruff.chmod(0o755)
        prof = blocking_profile(d)
        env = {"PATH": str(fakebin) + os.pathsep + os.environ.get("PATH", "")}
        rc, parsed, raw = run_runner(
            [d, "--profile", prof, "--scope", "all", "--checks", "lint", "--format", "json"],
            extra_env=env,
        )
        errors = []
        check_schema_and_exit(parsed, rc, errors)
        if rc != 1:
            errors.append(f"expected exit 1, got {rc}")
        if parsed and parsed.get("verdict") != "fail":
            errors.append(f"expected verdict fail, got {parsed.get('verdict')}")
        if parsed:
            lint = next((c for c in parsed["checks"] if c["name"] == "lint"), None)
            if not lint or lint["status"] != "fail":
                errors.append(f"lint status not fail: {lint}")
        return errors
    finally:
        shutil.rmtree(d, ignore_errors=True)


def case_b():
    """All python tools absent (sanitized PATH) → every check skipped, verdict
    pass, exit 0."""
    d = tempfile.mkdtemp(prefix="qg_b_")
    empty = None
    try:
        write(d, "pyproject.toml", "[project]\nname='x'\nversion='0'\n")
        write(d, "mod.py", "x = 1\n")
        git_init(d)
        prof = blocking_profile(d)
        path_val, empty = sanitized_path_env()
        env = {"PATH": path_val}
        rc, parsed, raw = run_runner(
            [d, "--profile", prof, "--scope", "all", "--format", "json"],
            extra_env=env,
        )
        errors = []
        check_schema_and_exit(parsed, rc, errors)
        if rc != 0:
            errors.append(f"expected exit 0, got {rc} :: {raw[:400]}")
        if parsed and parsed.get("verdict") != "pass":
            errors.append(f"expected verdict pass, got {parsed.get('verdict')}")
        if parsed:
            for c in parsed["checks"]:
                if c["status"] != "skipped":
                    errors.append(f"check {c['name']} status {c['status']} != skipped")
        return errors
    finally:
        shutil.rmtree(d, ignore_errors=True)
        if empty:
            shutil.rmtree(empty, ignore_errors=True)


def case_c():
    """Passing fixture: fake ruff that exits 0 → exit 0."""
    d = tempfile.mkdtemp(prefix="qg_c_")
    try:
        write(d, "pyproject.toml", "[project]\nname='x'\nversion='0'\n")
        write(d, "mod.py", "x = 1\n")
        git_init(d)
        fakebin = Path(d) / "fakebin"
        fakebin.mkdir()
        ruff = fakebin / "ruff"
        ruff.write_text("#!/bin/sh\nexit 0\n")
        ruff.chmod(0o755)
        prof = blocking_profile(d)
        env = {"PATH": str(fakebin) + os.pathsep + os.environ.get("PATH", "")}
        rc, parsed, raw = run_runner(
            [d, "--profile", prof, "--scope", "all", "--checks", "lint", "--format", "json"],
            extra_env=env,
        )
        errors = []
        check_schema_and_exit(parsed, rc, errors)
        if rc != 0:
            errors.append(f"expected exit 0, got {rc} :: {raw[:400]}")
        if parsed and parsed.get("verdict") != "pass":
            errors.append(f"expected verdict pass, got {parsed.get('verdict')}")
        return errors
    finally:
        shutil.rmtree(d, ignore_errors=True)


def case_d():
    """Non-git path → exit 2."""
    d = tempfile.mkdtemp(prefix="qg_d_")
    try:
        # not a git repo; pass it explicitly as ROOT
        rc, parsed, raw = run_runner([d, "--format", "json"])
        errors = []
        # ROOT explicitly given and IS a dir, but has no git history. The runner
        # still resolves changed_files best-effort (all git calls fail → empty),
        # detects no stacks, and emits pass. To force exit-2 we point at a
        # subdir that does not exist? No — spec case (d) is "non-git path → 2".
        # Per spec, exit 2 only occurs when ROOT is unresolved (no positional +
        # cwd not a git repo). So invoke with NO positional from a non-git cwd.
        rc2, parsed2, raw2 = run_runner_in_cwd([], d)
        if rc2 != 2:
            errors.append(f"expected exit 2 from non-git cwd, got {rc2} :: {raw2[:400]}")
        return errors
    finally:
        shutil.rmtree(d, ignore_errors=True)


def run_runner_in_cwd(args, cwd):
    env = dict(os.environ)
    proc = subprocess.run(
        [sys.executable, RUNNER] + args,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        env=env, cwd=cwd,
    )
    return proc.returncode, None, proc.stdout + proc.stderr


def case_e():
    """JSON has schema=='quality_gate/v1' and json['exit_code'] == process
    returncode. Asserted on a dedicated dry-run invocation against this repo's
    own toolkit (a real git repo)."""
    repo_root = str(Path(__file__).resolve().parent.parent)
    rc, parsed, raw = run_runner([repo_root, "--dry-run", "--format", "json"])
    errors = []
    check_schema_and_exit(parsed, rc, errors)
    return errors


CASES = [
    ("a", case_a),
    ("b", case_b),
    ("c", case_c),
    ("d", case_d),
    ("e", case_e),
]


def main():
    all_ok = True
    for label, fn in CASES:
        errors = fn()
        ok = not errors
        print(f"{'PASS' if ok else 'FAIL'} {label}")
        if not ok:
            all_ok = False
            for e in errors:
                print(f"    {label}: {e}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
