#!/usr/bin/env python3
"""Desktop-notification hook for Claude Code.

Fires an OS desktop notification when Claude needs your attention (the
`Notification` event: a permission prompt or an idle wait) and — opt-in — when
Claude finishes a turn (the `Stop` event). Reads the event JSON on stdin.

Env vars:
  CLAUDE_NOTIFY=0           disable all notifications
  CLAUDE_NOTIFY_ON_STOP=1   also notify when Claude finishes a turn (default: off)
  CLAUDE_NOTIFY_SOUND=name  macOS sound name (default: Ping; empty string = silent)
  CLAUDE_NOTIFY_DRYRUN=1    print the decision instead of firing (for testing)

Always exits 0 — a notify hook must never block or continue the turn.
"""
import json
import os
import shutil
import subprocess
import sys


def truncate(s, n=140):
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def is_on(name):
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


def decide(payload):
    """Return (title, body) to notify, or None to skip."""
    event = payload.get("hook_event_name", "")
    if event == "Stop":
        if not is_on("CLAUDE_NOTIFY_ON_STOP"):
            return None  # opt-in only
        if payload.get("background_tasks"):
            return None  # paused on background work, not truly done — don't ping
        return ("Claude Code — finished",
                truncate(payload.get("last_assistant_message") or "Turn complete."))
    # Notification (or any other attention event routed here)
    default_title = {
        "permission_prompt": "Claude needs permission",
        "idle_prompt": "Claude is waiting for you",
    }.get(payload.get("notification_type", ""), "Claude Code")
    return (payload.get("title") or default_title,
            truncate(payload.get("message") or "Claude needs your attention."))


def fire(title, body):
    sound = os.environ.get("CLAUDE_NOTIFY_SOUND", "Ping")
    if sys.platform == "darwin":
        tn = shutil.which("terminal-notifier")
        if tn:
            args = [tn, "-title", title, "-message", body, "-group", "claude-code"]
            if sound:
                args += ["-sound", sound]
            subprocess.run(args, timeout=8, check=False)
            return
        # Pass strings via argv so AppleScript needs no manual escaping.
        script = "on run argv\ndisplay notification (item 1 of argv) with title (item 2 of argv)"
        if sound:
            script += " sound name (item 3 of argv)"
        script += "\nend run"
        argv = [body, title] + ([sound] if sound else [])
        subprocess.run(["osascript", "-e", script] + argv, timeout=8, check=False)
        return
    ns = shutil.which("notify-send")
    if ns:
        subprocess.run([ns, title, body], timeout=8, check=False)


def main():
    if os.environ.get("CLAUDE_NOTIFY", "").strip().lower() in ("0", "false", "no", "off"):
        return
    raw = "" if sys.stdin.isatty() else sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        payload = {}
    decision = decide(payload)
    if os.environ.get("CLAUDE_NOTIFY_DRYRUN"):
        print("SKIP" if not decision else f"NOTIFY: {decision[0]} | {decision[1]}")
        return
    if decision:
        fire(*decision)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # never block the turn
    sys.exit(0)
