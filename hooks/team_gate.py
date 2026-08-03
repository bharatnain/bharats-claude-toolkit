#!/usr/bin/env python3
"""Team-mode quality-gate hook for Claude Code.

STDLIB ONLY. Mirrors hooks/notify.py: reads the event JSON on stdin, dispatches
by `hook_event_name`, and ALWAYS exits intentionally so a broken gate can never
wedge a session.

The CANONICAL question "are gates active?" is answered by scripts/team_sentinel.py
(single source of truth). When gates are inactive this hook is a SOLO NO-OP: it
exits 0 before doing any work on every branch EXCEPT Stop (teardown always runs).

Runner exit translation (scripts/quality_gate.py process exit -> hook exit):
  runner 0  -> allow      (exit 0)
  runner 1  -> BLOCK      (exit 2, blocking failures to stderr)
  runner 2  -> FAIL-OPEN  (exit 0, log to stderr) — never wedge a session.

Env:
  GATE_HOOK_DEBUG=1         print the stdin payload + the decision it WOULD
                            make, exit 0.
  CLAUDE_TOOLKIT_HOOKS=off  master off-switch for all toolkit hooks. This hook
                            SETS it for gate subprocesses: a gate command that
                            re-invokes `claude -p` must not re-fire these hooks
                            (recursion guard), or PostToolUse -> gate -> nested
                            edit -> PostToolUse could loop forever.
"""
import json
import os
import subprocess
import sys

# --- locate plugin root + make scripts/ importable -------------------------
HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_ROOT = os.path.dirname(HOOK_DIR)
SCRIPTS_DIR = os.path.join(PLUGIN_ROOT, "scripts")
QUALITY_GATE = os.path.join(SCRIPTS_DIR, "quality_gate.py")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import team_sentinel  # noqa: E402


def _eprint(msg):
    print(msg, file=sys.stderr)


# Bounded stdin read: a hook must never buffer unbounded input.
MAX_STDIN = 10 * 1024 * 1024  # 10 MiB


def _read_payload():
    raw = "" if sys.stdin.isatty() else sys.stdin.read(MAX_STDIN)
    try:
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def _bootstrap_path():
    """Hooks may run in a minimal env; ensure common user bin dirs are on PATH
    so `bd` and profile-configured gate tools are found."""
    home = os.path.expanduser("~")
    parts = os.environ.get("PATH", "").split(os.pathsep)
    for p in (os.path.join(home, ".local", "bin"), os.path.join(home, "bin"),
              "/opt/homebrew/bin", "/usr/local/bin"):
        if os.path.isdir(p) and p not in parts:
            parts.insert(0, p)
    os.environ["PATH"] = os.pathsep.join(parts)


CODE_EXTS = (
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".go", ".rs",
    ".java", ".kt", ".rb", ".php", ".c", ".h", ".cc", ".cpp", ".hpp",
    ".cs", ".swift", ".scala", ".m", ".mm",
)


def _is_code_file(path):
    return bool(path) and os.path.splitext(path)[1].lower() in CODE_EXTS


def _changed_code_paths(payload):
    """Best-effort: pull edited file paths out of a PostToolUse payload."""
    paths = []
    ti = payload.get("tool_input") or {}
    if isinstance(ti, dict):
        if ti.get("file_path"):
            paths.append(ti["file_path"])
        edits = ti.get("edits")
        if isinstance(edits, list):
            for e in edits:
                if isinstance(e, dict) and e.get("file_path"):
                    paths.append(e["file_path"])
    return paths


# --- runner --------------------------------------------------------------
def run_gate(extra_args, root):
    """Run quality_gate.py with --format json; return (rc, report_dict|None)."""
    cmd = [sys.executable, QUALITY_GATE] + extra_args + ["--format", "json"]
    if root:
        cmd.append(root)
    # Recursion guard: gate checks run profile-configured commands, which may
    # re-invoke claude; the nested session must not re-fire toolkit hooks.
    env = dict(os.environ, CLAUDE_TOOLKIT_HOOKS="off")
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    report = None
    try:
        report = json.loads(proc.stdout)
    except Exception:
        pass
    return proc.returncode, report, proc.stderr


def _blocking_failures(report):
    if not report:
        return []
    out = []
    for c in report.get("checks", []):
        if c.get("blocking") and c.get("status") in ("fail", "error"):
            out.append(f"{c.get('name')} ({c.get('tool')}): {c.get('status')}")
    return out


def translate(rc, report, runner_stderr):
    """Apply runner exit translation. Returns hook exit code."""
    if rc == 0:
        return 0  # allow
    if rc == 1:
        fails = _blocking_failures(report)
        if fails:
            _eprint("Quality gate BLOCKED — blocking failures:")
            for f in fails:
                _eprint(f"  - {f}")
        else:
            _eprint("Quality gate BLOCKED (runner exit 1).")
            if runner_stderr.strip():
                _eprint(runner_stderr.strip())
        return 2  # BLOCK
    # rc == 2 (or anything unexpected) -> fail-open
    _eprint("gate runner error, allowing")
    if runner_stderr.strip():
        _eprint(runner_stderr.strip())
    return 0


# --- per-event branches ---------------------------------------------------
def branch_post_tool_use(payload, root, debug):
    paths = _changed_code_paths(payload)
    if not any(_is_code_file(p) for p in paths):
        if debug:
            _eprint("DECISION: skip (no code files changed)")
        return 0  # skip — nothing to lint/typecheck
    args = ["--checks", "lint,typecheck", "--scope", "changed"]
    if debug:
        _eprint(f"DECISION: FAST LANE run -> quality_gate.py {' '.join(args)}")
        return 0
    rc, report, err = run_gate(args, root)
    return translate(rc, report, err)


def branch_subagent_stop(payload, root, debug):
    args = ["--scope", "changed"]  # profile defaults
    if debug:
        _eprint(f"DECISION: SubagentStop run -> quality_gate.py {' '.join(args)}")
        return 0
    rc, report, err = run_gate(args, root)
    return translate(rc, report, err)


def branch_pre_compact(payload, root, debug):
    """Snapshot the task graph; ALWAYS exit 0."""
    snap = os.path.join(root, ".claude", team_sentinel.SNAPSHOT_NAME) if root else None
    have_bd = _which("bd")
    if debug:
        _eprint(f"DECISION: PreCompact snapshot (bd={'yes' if have_bd else 'no'}) "
                f"-> {snap}")
        return 0
    if not snap:
        return 0
    try:
        os.makedirs(os.path.dirname(snap), exist_ok=True)
        content = None
        if have_bd:
            for sub in (["export"], ["list", "--json"], ["list"]):
                proc = subprocess.run([have_bd] + sub, capture_output=True,
                                      text=True)
                if proc.returncode == 0 and proc.stdout.strip():
                    content = proc.stdout
                    break
        if content is None:
            content = json.dumps({"note": "no task backend available",
                                  "ts": _now()}, indent=2) + "\n"
        _atomic_write(snap, content)
    except Exception as e:
        _eprint(f"PreCompact snapshot failed (ignored): {e}")
    return 0


def branch_stop(payload, root, debug):
    """TEARDOWN — runs even if gates currently inactive. Owner-only clear."""
    session_id = payload.get("session_id")
    if debug:
        _eprint(f"DECISION: Stop teardown -> clear(session_id={session_id!r})")
        return 0
    try:
        if root:
            team_sentinel.clear(root, session_id=session_id)
    except Exception as e:
        _eprint(f"Stop teardown failed (ignored): {e}")
    return 0


def branch_task_completed(payload, root, debug):
    """Phase-3 only. Run gate; exit 2 to reopen on runner-1."""
    args = ["--scope", "changed"]
    if debug:
        _eprint("DECISION: TaskCompleted run -> reopen on runner-1")
        return 0
    rc, report, err = run_gate(args, root)
    return translate(rc, report, err)


def branch_teammate_idle(payload, root, debug):
    """Phase-3 only. If `bd ready` has work, exit 2 with next task; else 0."""
    bd = _which("bd")
    if debug:
        _eprint(f"DECISION: TeammateIdle (bd={'yes' if bd else 'no'})")
        return 0
    if not bd:
        return 0
    try:
        proc = subprocess.run([bd, "ready"], capture_output=True, text=True)
        if proc.returncode == 0 and proc.stdout.strip():
            _eprint("Next ready task:")
            _eprint(proc.stdout.strip())
            return 2
    except Exception as e:
        _eprint(f"TeammateIdle check failed (ignored): {e}")
    return 0


def branch_task_created(payload, root, debug):
    """Phase-3 only. If task lacks acceptance criteria, exit 2 with guidance."""
    task = payload.get("task") or {}
    ac = None
    if isinstance(task, dict):
        ac = task.get("acceptance_criteria") or task.get("acceptanceCriteria")
    has_ac = bool(ac)
    if debug:
        _eprint(f"DECISION: TaskCreated (has_acceptance_criteria={has_ac})")
        return 0
    if not has_ac:
        _eprint("Task is missing acceptance criteria. Add a verifiable "
                "definition-of-done before starting work.")
        return 2
    return 0


# --- small stdlib helpers (kept local; STDLIB ONLY) ----------------------
def _which(name):
    import shutil
    return shutil.which(name)


def _now():
    import time
    return time.time()


def _atomic_write(path, text):
    import tempfile
    d = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".team-snapshot.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except Exception:
            pass
        raise


# Branches that are SOLO NO-OPs when gates are inactive (everything but Stop).
GATED = {
    "PostToolUse": branch_post_tool_use,
    "SubagentStop": branch_subagent_stop,
    "PreCompact": branch_pre_compact,
    "TaskCompleted": branch_task_completed,
    "TeammateIdle": branch_teammate_idle,
    "TaskCreated": branch_task_created,
}


def main():
    if os.environ.get("CLAUDE_TOOLKIT_HOOKS", "").strip().lower() in ("0", "false", "no", "off"):
        return 0  # disabled, or running inside a gate subprocess (recursion guard)
    debug = os.environ.get("GATE_HOOK_DEBUG", "").strip() in ("1", "true", "yes", "on")
    _bootstrap_path()
    payload = _read_payload()
    event = payload.get("hook_event_name", "")
    root = team_sentinel.find_repo_root()

    if debug:
        _eprint("=== GATE_HOOK_DEBUG ===")
        _eprint(f"event: {event}")
        _eprint(f"root: {root}")
        _eprint(f"gates_active: {team_sentinel.gates_active(root)}")
        _eprint("payload:")
        _eprint(json.dumps(payload, indent=2))

    if event == "Stop":
        return branch_stop(payload, root, debug)  # teardown always runs

    handler = GATED.get(event)
    if handler is None:
        return 0  # unknown / unwired event

    # SOLO NO-OP: zero work when gates are inactive.
    if not team_sentinel.gates_active(root):
        if debug:
            _eprint("DECISION: SOLO NO-OP (gates inactive)")
        return 0

    return handler(payload, root, debug)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001 — never wedge a session
        _eprint(f"team_gate internal error, allowing: {e}")
        sys.exit(0)
