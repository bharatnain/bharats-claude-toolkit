#!/usr/bin/env python3
"""Stop/SubagentStop hook: rebuild .claude/board/ when the repo opted in. Solo-safe, fail-open, silent.

Opt-in: the repo has a .claude/board/ directory (created by /board) or CLAUDE_BOARD=on.
Never prints to stdout (no context cost); errors go to stderr; always exits 0."""
import json, os, subprocess, sys
from pathlib import Path
MAX_STDIN = 10 * 1024 * 1024
HERE = Path(__file__).resolve().parent

def main():
    if os.environ.get("CLAUDE_TOOLKIT_HOOKS", "").strip().lower() in ("0", "false", "no", "off"): return 0
    raw = "" if sys.stdin.isatty() else sys.stdin.read(MAX_STDIN)
    try: payload = json.loads(raw) if raw.strip() else {}
    except Exception: payload = {}  # noqa: BLE001
    repo = Path(payload.get("cwd") or os.getcwd())
    if not (repo / ".claude/board").is_dir() and os.environ.get("CLAUDE_BOARD", "").lower() != "on": return 0
    try:
        subprocess.run([sys.executable, str(HERE.parent / "scripts" / "board.py"), "build", "--repo", str(repo), "--quiet"],
                       capture_output=True, text=True, timeout=15, env=dict(os.environ, CLAUDE_TOOLKIT_HOOKS="off"))
    except Exception as e:  # noqa: BLE001
        print(f"board_refresh: {e}", file=sys.stderr)
    return 0

if __name__ == "__main__":
    try: sys.exit(main())
    except Exception: sys.exit(0)  # noqa: BLE001
