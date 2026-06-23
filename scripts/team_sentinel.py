#!/usr/bin/env python3
"""Canonical team-context resolver — single source of truth.

STDLIB ONLY. Importable module + CLI. Hooks, the /team skill, and workflows
all call into here to decide whether team-mode quality gates are active.

A repo is "team-active" when a marker file exists and is fresh:

    <repo>/.claude/team-context.json
      {active, started_by, session_id, pid, profile, started_at}

The marker is written by the orchestrator session that starts a team run and
torn down (owner-only) when that same session stops.

Hard escape hatch: CLAUDE_TEAM_GATES=off always wins (gates off everywhere),
CLAUDE_TEAM_GATES=on forces gates on regardless of the marker.

CLI:
  team_sentinel.py status  [ROOT] [--profile P]
  team_sentinel.py set     [ROOT] [--profile P] [--by NAME] [--session S]
  team_sentinel.py clear    [ROOT] [--session S] [--force]
"""
import argparse
import json
import os
import sys
import tempfile
import time

MAX_AGE_HOURS = 12
MARKER_NAME = "team-context.json"
SNAPSHOT_NAME = "team-snapshot.json"


# --------------------------------------------------------------------------
# repo / path resolution
# --------------------------------------------------------------------------
def find_repo_root(start=None):
    """Walk up from `start` (default cwd) to the dir containing a `.git`
    entry (dir for normal repos, file for worktrees). Returns abspath or None."""
    cur = os.path.abspath(start or os.getcwd())
    while True:
        if os.path.exists(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


def _resolve_root(root):
    if root:
        return os.path.abspath(root)
    return find_repo_root()


def marker_path(root):
    return os.path.join(root, ".claude", MARKER_NAME)


# --------------------------------------------------------------------------
# marker IO
# --------------------------------------------------------------------------
def read_marker(root):
    """Return the parsed marker dict, or None if missing/invalid."""
    try:
        with open(marker_path(root), "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return None


def _atomic_write(path, data):
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".team-context.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
            fh.write("\n")
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except Exception:
            pass
        raise


# --------------------------------------------------------------------------
# staleness
# --------------------------------------------------------------------------
def _pid_alive(pid):
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return False
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _is_stale(marker):
    """Stale = pid not alive OR age > MAX_AGE_HOURS."""
    if not _pid_alive(marker.get("pid")):
        return True
    started_at = marker.get("started_at")
    try:
        age_hours = (time.time() - float(started_at)) / 3600.0
    except (TypeError, ValueError):
        return True
    return age_hours > MAX_AGE_HOURS


# --------------------------------------------------------------------------
# public API
# --------------------------------------------------------------------------
def gates_active(root=None):
    """True iff team-mode quality gates should enforce in `root`."""
    env = os.environ.get("CLAUDE_TEAM_GATES", "").strip().lower()
    if env == "off":
        return False  # hard escape hatch, always wins
    if env == "on":
        return True
    root = _resolve_root(root)
    if not root:
        return False
    marker = read_marker(root)
    if not marker:
        return False
    if marker.get("active") is not True:
        return False
    return not _is_stale(marker)


def set_active(root, profile, started_by, session_id):
    """Atomically write the active marker. Returns the written dict."""
    root = _resolve_root(root)
    if not root:
        raise RuntimeError("cannot resolve repo root")
    data = {
        "active": True,
        "started_by": started_by,
        "session_id": session_id,
        "pid": os.getpid(),
        "profile": profile,
        "started_at": time.time(),
    }
    _atomic_write(marker_path(root), data)
    return data


def clear(root, session_id=None, force=False):
    """Delete the marker only if `force` or marker.session_id == session_id.
    Returns True if a marker was removed, False otherwise."""
    root = _resolve_root(root)
    if not root:
        return False
    path = marker_path(root)
    marker = read_marker(root)
    if marker is None:
        return False
    if not force and marker.get("session_id") != session_id:
        return False  # owner-only teardown
    try:
        os.remove(path)
        return True
    except Exception:
        return False


def resolve_profile(root=None):
    """Resolve the effective profile name.

    1. marker.profile if active
    2. $CLAUDE_TEAM_PROFILE
    3. .claude/team-profile.json `maturity`
    4. "active"
    """
    root = _resolve_root(root)
    if root:
        marker = read_marker(root)
        if marker and marker.get("active") is True and marker.get("profile"):
            return marker["profile"]
    env = os.environ.get("CLAUDE_TEAM_PROFILE", "").strip()
    if env:
        return env
    if root:
        try:
            with open(os.path.join(root, ".claude", "team-profile.json"),
                      "r", encoding="utf-8") as fh:
                tp = json.load(fh)
            mat = tp.get("maturity")
            if mat:
                return mat
        except Exception:
            pass
    return "active"


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def main(argv):
    ap = argparse.ArgumentParser(description="Team-context resolver")
    ap.add_argument("command", choices=["status", "set", "clear"])
    ap.add_argument("root", nargs="?", default=None)
    ap.add_argument("--profile", default=None)
    ap.add_argument("--by", default=None, dest="by")
    ap.add_argument("--session", default=None)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)

    root = _resolve_root(args.root)

    if args.command == "status":
        active = gates_active(root)
        marker = read_marker(root) if root else None
        out = {
            "active": active,
            "profile": resolve_profile(root),
            "root": root,
            "marker": marker,
        }
        print(json.dumps(out, indent=2))
        return 0

    if args.command == "set":
        profile = args.profile or resolve_profile(root)
        data = set_active(root, profile, args.by or "cli", args.session)
        print(json.dumps(data, indent=2))
        return 0

    if args.command == "clear":
        removed = clear(root, session_id=args.session, force=args.force)
        print(json.dumps({"cleared": removed, "root": root}, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:  # noqa: BLE001
        print(f"error: {e}", file=sys.stderr)
        sys.exit(2)
