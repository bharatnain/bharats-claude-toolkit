#!/usr/bin/env python3
"""Health check for Bharat's Claude Toolkit setup. Stdlib only.

Prints a scannable checklist; every line is prefixed with a ✓/✗/⚠ glyph,
states what was checked, and — for failures/warnings — carries the exact fix
inline. The full list always prints regardless of outcome.

Exit code: 0 if healthy; 1 ONLY if a CRITICAL item fails (user settings.json
invalid OR the toolkit plugin not enabled); 2 on internal error via the
__main__ guard. Non-critical failures/warnings never flip the exit code.

Output-format note: the validate_* family uses --format text|github (CI
annotations); the interactive/report family (check_upstream.py, doctor.py)
uses --format human|json. doctor is an interactive health command, so
human|json is the deliberate, DRIFT-consistent choice.
"""
import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO_SETTINGS = ROOT / "settings.json"
USER_SETTINGS = Path.home() / ".claude" / "settings.json"
TEAM_CONTEXT = ROOT / ".claude" / "team-context.json"

TOOLKIT_PLUGIN = "bharats-claude-toolkit@bharats-claude-toolkit-dev"
BOOTSTRAP_FIX = "run bash scripts/bootstrap.sh"

GLYPHS = {"ok": "✓", "fail": "✗", "warn": "⚠"}


def result(check, status, critical, detail, fix=""):
    return {"check": check, "status": status, "critical": critical,
            "detail": detail, "fix": fix}


def load_json(path):
    """Return (data, error). data is None on any failure; error is a string."""
    if not path.exists():
        return None, "missing"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, str(e)
    except OSError as e:
        return None, str(e)


def run_checks():
    checks = []

    # --- CRITICAL 1: user settings exists + valid JSON ---
    user, user_err = load_json(USER_SETTINGS)
    if user_err == "missing":
        checks.append(result(
            "user settings", "fail", True,
            f"{USER_SETTINGS} does not exist", BOOTSTRAP_FIX))
    elif user_err is not None:
        checks.append(result(
            "user settings", "fail", True,
            f"{USER_SETTINGS} is not valid JSON: {user_err}",
            f"fix the JSON in {USER_SETTINGS}"))
    else:
        checks.append(result(
            "user settings", "ok", True,
            f"{USER_SETTINGS} exists and is valid JSON"))

    # --- CRITICAL 2: toolkit plugin enabled ---
    if user is None:
        checks.append(result(
            "toolkit enabled", "fail", True,
            f"cannot confirm '{TOOLKIT_PLUGIN}' — user settings unreadable",
            BOOTSTRAP_FIX))
    else:
        enabled = user.get("enabledPlugins", []) or []
        if TOOLKIT_PLUGIN in enabled:
            checks.append(result(
                "toolkit enabled", "ok", True,
                f"'{TOOLKIT_PLUGIN}' is in enabledPlugins"))
        else:
            checks.append(result(
                "toolkit enabled", "fail", True,
                f"'{TOOLKIT_PLUGIN}' not in enabledPlugins", BOOTSTRAP_FIX))

    # --- NON-critical: marketplaces + plugins present (diff vs repo) ---
    repo, repo_err = load_json(REPO_SETTINGS)
    if repo_err is not None:
        checks.append(result(
            "marketplaces+plugins", "warn", False,
            f"cannot read repo settings ({REPO_SETTINGS}): {repo_err}", ""))
    elif user is None:
        checks.append(result(
            "marketplaces+plugins", "warn", False,
            "cannot diff — user settings unreadable", BOOTSTRAP_FIX))
    else:
        repo_mkt = repo.get("extraKnownMarketplaces", {}) or {}
        repo_plugins = repo.get("enabledPlugins", []) or []
        user_mkt = user.get("extraKnownMarketplaces", {}) or {}
        user_plugins = set(user.get("enabledPlugins", []) or [])

        missing_mkt = [k for k in repo_mkt if k not in user_mkt]
        missing_plugins = [p for p in repo_plugins if p not in user_plugins]

        if not missing_mkt and not missing_plugins:
            checks.append(result(
                "marketplaces+plugins", "ok", False,
                "all repo marketplaces and plugins present in user settings"))
        else:
            parts = []
            if missing_mkt:
                parts.append("marketplaces: " + ", ".join(missing_mkt))
            if missing_plugins:
                parts.append("plugins: " + ", ".join(missing_plugins))
            checks.append(result(
                "marketplaces+plugins", "warn", False,
                "missing from user settings — " + "; ".join(parts),
                BOOTSTRAP_FIX))

    # --- NON-critical: required tools via shutil.which ---
    is_mac = platform.system() == "Darwin"
    tool_specs = [
        ("python3", "fail", "install Python 3 from python.org or your package manager"),
        ("node", "fail", "brew install node (or see nodejs.org)" if is_mac
         else "install Node.js (see nodejs.org)"),
        ("git", "fail", "install git from git-scm.com or your package manager"),
        ("gh", "fail", "brew install gh (or see cli.github.com)"),
        ("bd", "warn", "OPTIONAL — curl -sSL "
         "https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash"),
    ]
    for name, absent_status, hint in tool_specs:
        if shutil.which(name):
            checks.append(result(f"tool: {name}", "ok", False, "found on PATH"))
        else:
            checks.append(result(
                f"tool: {name}", absent_status, False,
                "not found on PATH", hint))

    # --- NON-critical: notifier (platform-appropriate) ---
    if is_mac:
        if shutil.which("osascript") or shutil.which("terminal-notifier"):
            checks.append(result(
                "notifier", "ok", False,
                "osascript/terminal-notifier available"))
        else:
            checks.append(result(
                "notifier", "warn", False,
                "no macOS notifier found", "brew install terminal-notifier"))
    elif platform.system() == "Linux":
        if shutil.which("notify-send"):
            checks.append(result("notifier", "ok", False, "notify-send available"))
        else:
            checks.append(result(
                "notifier", "warn", False,
                "no notify-send found", "apt install libnotify-bin"))
    else:
        if shutil.which("notify-send") or shutil.which("terminal-notifier"):
            checks.append(result("notifier", "ok", False, "a notifier is available"))
        else:
            checks.append(result(
                "notifier", "warn", False,
                "no notifier found for this platform",
                "install a desktop notifier"))

    # --- A/V optionals (OPTIONAL; absence is ⚠, never ✗/critical) ---
    if shutil.which("ffmpeg"):
        checks.append(result("A/V: ffmpeg", "ok", False, "OPTIONAL — found on PATH"))
    else:
        checks.append(result(
            "A/V: ffmpeg", "warn", False, "OPTIONAL — not found on PATH",
            "brew install ffmpeg (or see ffmpeg.org)" if is_mac
            else "install ffmpeg (see ffmpeg.org)"))

    if os.environ.get("FAL_KEY"):
        checks.append(result("A/V: FAL_KEY", "ok", False, "OPTIONAL — set in env"))
    else:
        checks.append(result(
            "A/V: FAL_KEY", "warn", False, "OPTIONAL — not set in env",
            "export FAL_KEY=<your fal.ai key>"))

    # --- NON-critical: stale team-context ---
    if TEAM_CONTEXT.exists():
        checks.append(result(
            "team-context", "warn", False,
            f"{TEAM_CONTEXT} exists — it may gate solo work",
            f"rm {TEAM_CONTEXT}"))
    else:
        checks.append(result(
            "team-context", "ok", False,
            "no stale .claude/team-context.json"))

    return checks


def compute_exit_code(checks):
    for c in checks:
        if c["critical"] and c["status"] == "fail":
            return 1
    return 0


def print_human(checks):
    for c in checks:
        glyph = GLYPHS[c["status"]]
        print(f"{glyph} {c['check']}: {c['detail']}")
        if c["status"] in ("fail", "warn") and c["fix"]:
            print(f"  → fix: {c['fix']}")


def print_json(checks, exit_code):
    payload = {
        "healthy": exit_code == 0,
        "exit_code": exit_code,
        "checks": checks,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main(argv):
    ap = argparse.ArgumentParser(
        description="Health check for Bharat's Claude Toolkit setup.")
    ap.add_argument("--format", choices=["human", "json"], default="human")
    args = ap.parse_args(argv)

    checks = run_checks()
    exit_code = compute_exit_code(checks)

    # Always print the full checklist before returning the exit code.
    if args.format == "json":
        print_json(checks, exit_code)
    else:
        print_human(checks)

    return exit_code


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:  # noqa: BLE001
        print(f"internal error: {e}", file=sys.stderr)
        sys.exit(2)
