#!/usr/bin/env python3
"""Secret-scanning PreToolUse hook for Claude Code.

STDLIB ONLY. Mirrors hooks/notify.py: reads the event JSON on stdin. Fires on
PreToolUse for Write|Edit|MultiEdit and scans the INCOMING content (not the
file on disk) so a leaked credential is blocked before it ever lands.

Exit contract (same convention as hooks/team_gate.py):
  exit 0  -> allow (no findings, disabled, or internal error — fail open)
  exit 2  -> BLOCK the tool call; findings are printed to stderr for Claude.

Env vars:
  CLAUDE_SECRET_SCAN=0     disable the scanner entirely
  CLAUDE_TOOLKIT_HOOKS=off master off-switch for all toolkit hooks; also set by
                           team_gate.py for gate subprocesses (recursion guard)
  SECRET_SCAN_DEBUG=1      print the decision instead of blocking (for testing)
"""
import json
import os
import re
import sys

# Bounded stdin read: a hook must never buffer unbounded input. An oversized
# payload truncates -> JSON parse fails -> {} -> allow (fail-open contract).
MAX_STDIN = 10 * 1024 * 1024  # 10 MiB


def _off(name):
    return os.environ.get(name, "").strip().lower() in ("0", "false", "no", "off")

# High-precision patterns first; the last two are broader and get the
# placeholder filter applied to their matched value.
PATTERNS = [
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), False),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{22,})"), False),
    ("Slack token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}"), False),
    ("Stripe secret key", re.compile(r"\bsk_live_[0-9A-Za-z]{24,}"), False),
    ("Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}"), False),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"), False),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"), False),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"), False),
    ("DB URL with credentials", re.compile(r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqp)://[^:/\s]+:([^@\s]+)@"), True),
    ("Hardcoded credential assignment", re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password|passwd)\b\s*[:=]\s*[\"']([A-Za-z0-9_\-./+=]{20,})[\"']"), True),
]

# A broad-pattern match whose captured value looks like a template/example is
# not a leak. Keeps docs, samples, and .env.example writes from false-blocking.
PLACEHOLDER_MARKERS = (
    "example", "changeme", "change-me", "placeholder", "your", "dummy",
    "sample", "xxxx", "****", "<", "${", "{{",
)


def _is_placeholder(value):
    v = value.lower()
    return any(m in v for m in PLACEHOLDER_MARKERS)


def _read_payload():
    raw = "" if sys.stdin.isatty() else sys.stdin.read(MAX_STDIN)
    try:
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def _incoming_content(payload):
    """Extract the text this tool call is about to write."""
    tool = payload.get("tool_name", "")
    ti = payload.get("tool_input") or {}
    if tool == "Write":
        return ti.get("content") or ""
    if tool == "Edit":
        return ti.get("new_string") or ""
    if tool == "MultiEdit":
        return "\n".join((e.get("new_string") or "") for e in ti.get("edits") or [])
    return ""


def scan(content):
    """Return a list of (line_number, pattern_name) findings."""
    findings = []
    for i, line in enumerate(content.splitlines(), 1):
        for name, rx, filter_placeholders in PATTERNS:
            m = rx.search(line)
            if not m:
                continue
            if filter_placeholders and _is_placeholder(m.group(1)):
                continue
            findings.append((i, name))
            break  # one finding per line is enough
    return findings


def main():
    if _off("CLAUDE_TOOLKIT_HOOKS") or _off("CLAUDE_SECRET_SCAN"):
        return 0
    payload = _read_payload()
    if payload.get("hook_event_name") not in ("PreToolUse", None):
        return 0
    findings = scan(_incoming_content(payload))
    if not findings:
        if os.environ.get("SECRET_SCAN_DEBUG"):
            print("ALLOW: no secrets found")
        return 0
    path = (payload.get("tool_input") or {}).get("file_path", "<unknown file>")
    lines = "\n".join(f"  - line {n}: {name}" for n, name in findings)
    msg = (
        f"BLOCKED: potential secrets in content headed for {path}:\n{lines}\n"
        "Use environment variables or a secrets manager instead of hardcoding "
        "credentials. If this is intentional (e.g. a test fixture), the user "
        "can disable the scanner with CLAUDE_SECRET_SCAN=0."
    )
    if os.environ.get("SECRET_SCAN_DEBUG"):
        print(msg)
        return 0
    print(msg, file=sys.stderr)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # fail open — never wedge a session
