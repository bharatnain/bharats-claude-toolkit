#!/usr/bin/env python3
"""SessionStart hook: make beads (bd) the per-repo task store (hard default).

Fires once per session (registered with matcher "startup"). When the session is
in a git repo and `bd` is on PATH, it ensures `.beads/` exists — an idempotent
`bd init` run with `--skip-agents --skip-hooks` so it NEVER writes
CLAUDE.md / AGENTS.md / .claude/ or installs git hooks into the user's repo — and
gitignores `.beads/`. It then returns an `additionalContext` directive telling the
session to use beads for task tracking (this is the behavioral half of the hard
default).

Env:
  CLAUDE_BEADS=off|0|false|no   disable entirely — no init, no directive, full
                                fallback to native Task tools.

Always exits 0 — a SessionStart hook must never block session startup. Reads the
event JSON on stdin and uses payload.cwd (falling back to $CLAUDE_PROJECT_DIR,
then the process cwd), walking up to the enclosing git repo root.

Command vocabulary: skills/team-orchestration/references/beads-contract.md.
"""
import json
import os
import shutil
import subprocess
import sys

DIRECTIVE = (
    "This project uses beads (bd) for task tracking - prefer `bd ready` to find "
    "work, `bd create` to add tasks (with `--acceptance`), `bd update <id> --claim` "
    "to start, and `bd close <id> --reason` to finish. If bd is unavailable, fall "
    "back to the native Task tools with the same acceptance-criteria discipline."
)


def beads_disabled():
    return os.environ.get("CLAUDE_BEADS", "").strip().lower() in ("0", "false", "no", "off")


def find_repo_root(start):
    """Walk up to the first dir containing a `.git` entry (file OR dir, so
    worktrees and submodules resolve), mirroring team_sentinel / runner.js."""
    try:
        d = os.path.abspath(start)
    except Exception:
        return None
    while True:
        if os.path.exists(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def gitignore_beads(root):
    """Append `.beads/` to <root>/.gitignore if not already present. Idempotent."""
    gi = os.path.join(root, ".gitignore")
    try:
        lines = []
        if os.path.exists(gi):
            with open(gi, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
        if any(ln.strip() in (".beads", ".beads/") for ln in lines):
            return
        with open(gi, "a", encoding="utf-8") as f:
            if lines and lines[-1].strip():
                f.write("\n")
            f.write(".beads/\n")
    except Exception:
        pass  # never block


def ensure_beads(root, bd):
    """Idempotent: init `.beads/` if absent (safe flags), then gitignore it.
    Returns True iff `.beads/` exists afterwards."""
    if not os.path.isdir(os.path.join(root, ".beads")):
        try:
            subprocess.run(
                [bd, "init", "--quiet", "--non-interactive", "--skip-agents", "--skip-hooks"],
                cwd=root, capture_output=True, timeout=30, check=False,
            )
        except Exception:
            return False
    gitignore_beads(root)
    return os.path.isdir(os.path.join(root, ".beads"))


def emit_context():
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": DIRECTIVE,
        }
    }))


def main():
    if beads_disabled():
        return
    raw = "" if sys.stdin.isatty() else sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    start = payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    bd = shutil.which("bd")
    if not bd:
        return  # native Task tools remain the default
    root = find_repo_root(start)
    if not root:
        return  # not a git repo — do not litter arbitrary dirs with .beads/
    if ensure_beads(root, bd):
        emit_context()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # never block session start
    sys.exit(0)
