#!/usr/bin/env python3
"""Quality gate runner: detect stacks, run lint/typecheck/test/build per a team
profile, and emit a pass/fail verdict. Stdlib only.

Exit codes: 0 = all blocking checks pass (advisory/skipped failures allowed);
1 = >=1 blocking check failed or errored; 2 = internal error / not a git repo.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

SCHEMA = "quality_gate/v1"
ALL_CHECKS = ["lint", "typecheck", "test", "build"]
DETAIL_LIMIT = 2048

# Built-in "active" profile: every check blocking, scope changed.
BUILTIN_PROFILE = {
    "checks": {
        "lint": {"blocking": True, "scope": "changed"},
        "typecheck": {"blocking": True, "scope": "changed"},
        "test": {"blocking": True, "scope": "changed"},
        "build": {"blocking": True, "scope": "changed"},
    }
}


# ---------------------------------------------------------------------------
# git helpers (all best-effort; failures degrade gracefully)
# ---------------------------------------------------------------------------
def run_git(root, args):
    """Run a git subcommand in root. Return (ok, stdout) — ok False on any error."""
    try:
        proc = subprocess.run(
            ["git"] + args,
            cwd=str(root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except Exception:
        return False, ""
    if proc.returncode != 0:
        return False, ""
    return True, proc.stdout


def git_toplevel(cwd):
    ok, out = run_git(cwd, ["rev-parse", "--show-toplevel"])
    if not ok:
        return None
    top = out.strip()
    return top or None


def compute_base(root, base_arg):
    if base_arg:
        return base_arg
    ok, out = run_git(root, ["merge-base", "@", "@{u}"])
    if ok and out.strip():
        return out.strip()
    return "HEAD"


def compute_changed_files(root, base):
    """Union of base...HEAD diff, unstaged diff, and untracked files. Each git
    invocation is guarded; any failure contributes nothing rather than aborting."""
    files = set()
    for args in (
        ["diff", "--name-only", f"{base}...HEAD"],
        ["diff", "--name-only"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        ok, out = run_git(root, args)
        if not ok:
            continue
        for line in out.splitlines():
            line = line.strip()
            if line:
                files.add(line)
    return sorted(files)


# ---------------------------------------------------------------------------
# stack detection
# ---------------------------------------------------------------------------
def detect_stacks(root):
    stacks = []
    if (root / "package.json").is_file():
        stacks.append("node")
    if (root / "pyproject.toml").is_file() or (root / "setup.cfg").is_file():
        stacks.append("python")
    if (root / "go.mod").is_file():
        stacks.append("go")
    if (root / "Cargo.toml").is_file():
        stacks.append("rust")
    return stacks


def read_package_scripts(root):
    try:
        data = json.loads((root / "package.json").read_text(encoding="utf-8"))
    except Exception:
        return {}
    scripts = data.get("scripts")
    return scripts if isinstance(scripts, dict) else {}


def node_pm(root):
    if (root / "pnpm-lock.yaml").is_file():
        return "pnpm"
    if (root / "yarn.lock").is_file():
        return "yarn"
    return "npm"


def python_module_importable(mod):
    try:
        proc = subprocess.run(
            [sys.executable, "-c", f"import {mod}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return False
    return proc.returncode == 0


def cargo_has_clippy():
    """clippy present iff `cargo clippy --version` succeeds."""
    if not shutil.which("cargo"):
        return False
    try:
        proc = subprocess.run(
            ["cargo", "clippy", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return False
    return proc.returncode == 0


# ---------------------------------------------------------------------------
# check planning
# A planned check is a dict: name, tool, cmd (list|None), scoped (bool), stack,
# detail (optional pre-set note). cmd None ⇒ graceful skip (tool/script absent).
# ---------------------------------------------------------------------------
def py_targets(changed_files, root):
    """Changed *.py files that exist, repo-relative, for lint/typecheck scoping."""
    out = []
    for f in changed_files:
        if f.endswith(".py") and (root / f).is_file():
            out.append(f)
    return out


def py_test_targets(changed_files, root):
    """Changed paths that look like tests, for pytest scoping."""
    out = []
    for f in changed_files:
        if not f.endswith(".py"):
            continue
        base = os.path.basename(f)
        if base.startswith("test_") or base.endswith("_test.py") or "test" in f.split("/"):
            if (root / f).is_file():
                out.append(f)
    return out


def plan_node(root, checks, scope, changed_files):
    scripts = read_package_scripts(root)
    pm = node_pm(root)
    planned = []
    script_for = {
        "lint": "lint",
        "typecheck": "typecheck",
        "test": "test",
        "build": "build",
    }
    for name in checks:
        if name == "node":
            continue
        key = script_for[name]
        entry = key in scripts
        if name == "typecheck" and not entry:
            if "type-check" in scripts:
                key = "type-check"
                entry = True
        tool = f"{pm} run {key}"
        if not entry:
            planned.append({"name": name, "tool": pm, "cmd": None,
                            "scoped": False, "stack": "node",
                            "detail": f"no '{key}' script in package.json"})
            continue
        cmd = [pm, "run", key]
        planned.append({"name": name, "tool": tool, "cmd": cmd,
                        "scoped": False, "stack": "node", "detail": ""})
    return planned


def plan_python(root, checks, scope, changed_files):
    planned = []
    targets = py_targets(changed_files, root) if scope == "changed" else []
    for name in checks:
        if name == "lint":
            if shutil.which("ruff"):
                cmd = ["ruff", "check"]
                scoped = False
                if scope == "changed" and targets:
                    cmd = cmd + targets
                    scoped = True
                planned.append({"name": name, "tool": "ruff", "cmd": cmd,
                                "scoped": scoped, "stack": "python", "detail": ""})
            elif shutil.which("flake8"):
                cmd = ["flake8"]
                scoped = False
                if scope == "changed" and targets:
                    cmd = cmd + targets
                    scoped = True
                planned.append({"name": name, "tool": "flake8", "cmd": cmd,
                                "scoped": scoped, "stack": "python", "detail": ""})
            else:
                planned.append({"name": name, "tool": "ruff", "cmd": None,
                                "scoped": False, "stack": "python",
                                "detail": "no ruff or flake8 on PATH"})
        elif name == "typecheck":
            if shutil.which("mypy"):
                cmd = ["mypy"]
                scoped = False
                if scope == "changed" and targets:
                    cmd = cmd + targets
                    scoped = True
                planned.append({"name": name, "tool": "mypy", "cmd": cmd,
                                "scoped": scoped, "stack": "python", "detail": ""})
            elif shutil.which("pyright"):
                cmd = ["pyright"]
                scoped = False
                if scope == "changed" and targets:
                    cmd = cmd + targets
                    scoped = True
                planned.append({"name": name, "tool": "pyright", "cmd": cmd,
                                "scoped": scoped, "stack": "python", "detail": ""})
            else:
                planned.append({"name": name, "tool": "mypy", "cmd": None,
                                "scoped": False, "stack": "python",
                                "detail": "no mypy or pyright on PATH"})
        elif name == "test":
            if shutil.which("pytest"):
                cmd = ["pytest"]
                scoped = False
                test_targets = py_test_targets(changed_files, root) if scope == "changed" else []
                if scope == "changed" and test_targets:
                    cmd = cmd + test_targets
                    scoped = True
                planned.append({"name": name, "tool": "pytest", "cmd": cmd,
                                "scoped": scoped, "stack": "python", "detail": ""})
            else:
                planned.append({"name": name, "tool": "pytest", "cmd": None,
                                "scoped": False, "stack": "python",
                                "detail": "no pytest on PATH"})
        elif name == "build":
            if python_module_importable("build"):
                planned.append({"name": name, "tool": "python -m build",
                                "cmd": [sys.executable, "-m", "build"],
                                "scoped": False, "stack": "python", "detail": ""})
            else:
                planned.append({"name": name, "tool": "python -m build", "cmd": None,
                                "scoped": False, "stack": "python",
                                "detail": "build module not importable"})
    return planned


def plan_go(root, checks, scope, changed_files):
    planned = []
    has_go = bool(shutil.which("go"))
    spec = {
        "lint": ("go vet ./...", ["go", "vet", "./..."]),
        "typecheck": ("go build ./...", ["go", "build", "./..."]),
        "test": ("go test ./...", ["go", "test", "./..."]),
        "build": ("go build ./...", ["go", "build", "./..."]),
    }
    for name in checks:
        tool, cmd = spec[name]
        if not has_go:
            planned.append({"name": name, "tool": "go", "cmd": None,
                            "scoped": False, "stack": "go",
                            "detail": "no go on PATH"})
            continue
        detail = ""
        if name == "typecheck":
            detail = "Go has no separate typecheck phase; mapped to `go build ./...`"
        planned.append({"name": name, "tool": tool, "cmd": cmd,
                        "scoped": False, "stack": "go", "detail": detail})
    return planned


def plan_rust(root, checks, scope, changed_files):
    planned = []
    has_cargo = bool(shutil.which("cargo"))
    clippy = cargo_has_clippy() if has_cargo else False
    spec = {
        "lint": ("cargo clippy", ["cargo", "clippy"]),
        "typecheck": ("cargo check", ["cargo", "check"]),
        "test": ("cargo test", ["cargo", "test"]),
        "build": ("cargo build", ["cargo", "build"]),
    }
    for name in checks:
        tool, cmd = spec[name]
        if not has_cargo:
            planned.append({"name": name, "tool": "cargo", "cmd": None,
                            "scoped": False, "stack": "rust",
                            "detail": "no cargo on PATH"})
            continue
        if name == "lint" and not clippy:
            planned.append({"name": name, "tool": "cargo clippy", "cmd": None,
                            "scoped": False, "stack": "rust",
                            "detail": "clippy component not present"})
            continue
        planned.append({"name": name, "tool": tool, "cmd": cmd,
                        "scoped": False, "stack": "rust", "detail": ""})
    return planned


STACK_PLANNERS = {
    "node": plan_node,
    "python": plan_python,
    "go": plan_go,
    "rust": plan_rust,
}


# ---------------------------------------------------------------------------
# profile resolution
# ---------------------------------------------------------------------------
def load_profile(profile_arg, root):
    """Return (profile_dict, profile_label). Honors resolution order; raises
    ValueError('explicit') if an explicit --profile path is malformed (→ exit 2)."""
    # (1) explicit --profile
    if profile_arg:
        p = Path(profile_arg)
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            raise ValueError(f"cannot read profile {profile_arg}: {e}")
        if not isinstance(data, dict):
            raise ValueError(f"profile {profile_arg} is not a JSON object")
        return data, str(p)
    # (2) env
    env_path = os.environ.get("CLAUDE_TEAM_PROFILE")
    if env_path:
        try:
            data = json.loads(Path(env_path).read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data, env_path
            raise ValueError("not an object")
        except Exception as e:
            print(f"warning: ignoring malformed $CLAUDE_TEAM_PROFILE ({e}); "
                  f"using built-in active defaults", file=sys.stderr)
    # (3) ROOT/.claude/team-profile.json
    default_path = root / ".claude" / "team-profile.json"
    if default_path.is_file():
        try:
            data = json.loads(default_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data, str(default_path)
            raise ValueError("not an object")
        except Exception as e:
            print(f"warning: ignoring malformed {default_path} ({e}); "
                  f"using built-in active defaults", file=sys.stderr)
    # (4) built-in
    return BUILTIN_PROFILE, "builtin:active"


def check_is_blocking(profile, name):
    checks = profile.get("checks")
    if not isinstance(checks, dict):
        return False
    entry = checks.get(name)
    if not isinstance(entry, dict):
        return False
    return bool(entry.get("blocking", False))


# ---------------------------------------------------------------------------
# execution
# ---------------------------------------------------------------------------
def truncate_detail(text):
    if text is None:
        return ""
    b = text.encode("utf-8", "replace")
    if len(b) <= DETAIL_LIMIT:
        return text
    marker = "\n...[truncated]"
    keep = DETAIL_LIMIT - len(marker.encode("utf-8"))
    return b[:keep].decode("utf-8", "ignore") + marker


def run_check(planned, root):
    """Execute one planned check. Return result dict with status/exit_code/etc."""
    name = planned["name"]
    tool = planned["tool"]
    cmd = planned["cmd"]
    scoped = planned["scoped"]
    pre_detail = planned.get("detail", "")

    if cmd is None:
        # graceful skip: tool/script absent
        return {
            "name": name, "tool": tool, "status": "skipped",
            "scoped": False, "duration_ms": 0, "exit_code": None,
            "detail": pre_detail, "stack": planned["stack"],
        }

    start = time.monotonic()
    try:
        proc = subprocess.run(
            cmd, cwd=str(root),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        )
    except Exception as e:
        duration = int((time.monotonic() - start) * 1000)
        return {
            "name": name, "tool": tool, "status": "error",
            "scoped": scoped, "duration_ms": duration, "exit_code": None,
            "detail": truncate_detail(f"failed to run {tool}: {e}"),
            "stack": planned["stack"],
        }
    duration = int((time.monotonic() - start) * 1000)
    status = "pass" if proc.returncode == 0 else "fail"
    detail = (pre_detail + ("\n" if pre_detail else "")) + (proc.stdout or "")
    return {
        "name": name, "tool": tool, "status": status,
        "scoped": scoped, "duration_ms": duration, "exit_code": proc.returncode,
        "detail": truncate_detail(detail.strip()),
        "stack": planned["stack"],
    }


# ---------------------------------------------------------------------------
# output
# ---------------------------------------------------------------------------
def build_human(report):
    lines = []
    rows = [("name", "tool", "status", "blocking", "scoped", "duration_ms")]
    for c in report["checks"]:
        rows.append((
            c["name"], c["tool"], c["status"],
            "yes" if c["blocking"] else "no",
            "yes" if c["scoped"] else "no",
            str(c["duration_ms"]),
        ))
    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    for idx, r in enumerate(rows):
        line = "  ".join(r[i].ljust(widths[i]) for i in range(len(r)))
        lines.append(line)
        if idx == 0:
            lines.append("  ".join("-" * widths[i] for i in range(len(r))))
    s = report["summary"]
    total = len(report["checks"])
    lines.append("")
    lines.append(
        f"{total} checks: {s['passed']} passed, {s['failed']} failed, "
        f"{s['skipped']} skipped ({s['blocking_failed']} blocking failed) "
        f"— verdict: {report['verdict']}"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# orchestration
# ---------------------------------------------------------------------------
def build_report(root, profile, profile_label, scope, base, changed_files,
                 stacks, planned_checks, dry_run):
    checks_out = []
    summary = {"passed": 0, "failed": 0, "skipped": 0, "blocking_failed": 0}

    for planned in planned_checks:
        name = planned["name"]
        blocking = check_is_blocking(profile, name)
        if dry_run:
            cmd = planned["cmd"]
            if cmd is None:
                detail = planned.get("detail", "") or "tool/script absent"
                status = "skipped"
            else:
                detail = "DRY RUN — would execute: " + " ".join(cmd)
                status = "skipped"
            result = {
                "name": name, "tool": planned["tool"], "status": status,
                "scoped": planned["scoped"] if cmd is not None else False,
                "duration_ms": 0, "exit_code": None,
                "detail": truncate_detail(detail),
            }
        else:
            result = run_check(planned, root)
            result.pop("stack", None)

        result["blocking"] = blocking
        status = result["status"]
        if status == "pass":
            summary["passed"] += 1
        elif status == "skipped":
            summary["skipped"] += 1
        elif status == "fail":
            summary["failed"] += 1
            if blocking:
                summary["blocking_failed"] += 1
        elif status == "error":
            # error on blocking check counts as blocking failure
            summary["failed"] += 1
            if blocking:
                summary["blocking_failed"] += 1

        # order keys consistently
        checks_out.append({
            "name": result["name"],
            "tool": result["tool"],
            "blocking": blocking,
            "status": status,
            "scoped": result["scoped"],
            "duration_ms": result["duration_ms"],
            "exit_code": result["exit_code"],
            "detail": result["detail"],
        })

    verdict = "fail" if summary["blocking_failed"] > 0 else "pass"
    exit_code = 1 if verdict == "fail" else 0

    report = {
        "schema": SCHEMA,
        "root": str(root),
        "profile": profile_label,
        "scope": scope,
        "base": base,
        "changed_files": changed_files,
        "stack": stacks,
        "summary": summary,
        "checks": checks_out,
        "verdict": verdict,
        "exit_code": exit_code,
    }
    return report


def parse_checks_arg(value):
    parts = [p.strip() for p in value.split(",") if p.strip()]
    for p in parts:
        if p not in ALL_CHECKS:
            raise argparse.ArgumentTypeError(
                f"invalid check '{p}'; allowed: {','.join(ALL_CHECKS)}")
    # preserve canonical order, drop dups
    return [c for c in ALL_CHECKS if c in parts]


def main(argv):
    ap = argparse.ArgumentParser(description="Quality gate runner")
    ap.add_argument("root", nargs="?", default=None)
    ap.add_argument("--profile", default=None, metavar="PATH")
    ap.add_argument("--scope", choices=["changed", "all"], default="changed")
    ap.add_argument("--base", default=None, metavar="REF")
    ap.add_argument("--checks", type=parse_checks_arg, default=list(ALL_CHECKS),
                    metavar="CSV")
    ap.add_argument("--format", choices=["human", "json"], default="human")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    # ROOT resolution
    if args.root:
        root = Path(args.root).resolve()
    else:
        top = git_toplevel(Path.cwd())
        if not top:
            print("error: not a git repository (no ROOT given and "
                  "`git rev-parse --show-toplevel` failed)", file=sys.stderr)
            return 2
        root = Path(top).resolve()

    if not root.is_dir():
        print(f"error: ROOT is not a directory: {root}", file=sys.stderr)
        return 2

    checks = args.checks

    # profile
    try:
        profile, profile_label = load_profile(args.profile, root)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    # scope / changed files
    scope = args.scope
    if scope == "changed":
        base = compute_base(root, args.base)
        changed_files = compute_changed_files(root, base)
    else:
        base = args.base
        changed_files = []

    # stack detection + planning
    stacks = detect_stacks(root)
    planned_checks = []
    for stack in stacks:
        planner = STACK_PLANNERS[stack]
        planned_checks.extend(planner(root, checks, scope, changed_files))

    report = build_report(root, profile, profile_label, scope, base,
                          changed_files, stacks, planned_checks, args.dry_run)

    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(build_human(report))

    return report["exit_code"]


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:  # noqa: BLE001
        print(f"internal error: {e}", file=sys.stderr)
        sys.exit(2)
