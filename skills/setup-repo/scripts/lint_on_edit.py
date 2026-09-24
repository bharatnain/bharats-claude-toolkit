#!/usr/bin/env python3
"""PostToolUse hook: run the repo's lint command on the file Claude just edited. Stdlib only.
Reads the hook JSON on stdin, finds tool_input.file_path, runs LINT_CMD (set by /setup-repo)
with the file appended, returns findings as PostToolUse additionalContext JSON, always exits 0."""
import json, os, shlex, subprocess, sys
LINT_CMD = os.environ.get("SETUP_REPO_LINT_CMD", "__LINT_CMD__")

def main():
    try:
        payload = json.loads(sys.stdin.read(1024 * 1024) or "{}")
        path = (payload.get("tool_input") or {}).get("file_path")
    except Exception:  # noqa: BLE001
        return 0
    if not path or not os.path.isfile(path) or not LINT_CMD.strip() or LINT_CMD.startswith("__"):
        return 0
    try:
        p = subprocess.run(shlex.split(LINT_CMD) + [path], capture_output=True, text=True, timeout=60)
        out = (p.stdout + p.stderr).strip()
        if p.returncode != 0 and out:
            ctx = f"lint ({LINT_CMD}) on {path}:\n{out[:4000]}"
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": ctx}}))
    except Exception:  # noqa: BLE001
        pass
    return 0

if __name__ == "__main__":
    sys.exit(main())
