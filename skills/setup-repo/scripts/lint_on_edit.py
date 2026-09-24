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
