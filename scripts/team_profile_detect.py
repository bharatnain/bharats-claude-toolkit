#!/usr/bin/env python3
"""Suggest a team-profile maturity (greenfield | active | legacy) for a repo.

STDLIB ONLY. This tool only SUGGESTS: it prints (and optionally writes) a
maturity plus the signals that drove it. It never invokes the gate runner,
never edits an existing profile, and never enforces anything.

CLI:
  team_profile_detect.py [ROOT] [--write] [--format {json,human}]

  ROOT       repo path to inspect (default: git toplevel of cwd)
  --write    atomically write ROOT/.claude/team-profile.json
  --format   output format (default: human)

Exit codes:
  0  normal
  2  internal error / ROOT is not a git repository

Heuristic (deterministic):
  repo_age_days = today - first_commit_date   (null first commit -> 0, i.e. new)

  greenfield  IF tracked_file_count < 50
              OR repo_age_days < 30
              OR (not ci_present AND not tests_present)
  legacy      IF (tests_present AND ci_present
                  AND tracked_file_count >= 400 AND repo_age_days >= 365)
              OR (repo_age_days >= 365 AND commits_last_90d < 10)   # low churn : age
  else        active

  Evaluated in order greenfield -> legacy -> active, so a tiny/new repo never
  classifies as legacy. `active` is the safe default when signals conflict.

Graceful degradation: under a shallow clone (no full history) first_commit_date
may be null and commits_last_90d may be undercounted. The detector still emits a
maturity from the file-count / tests / CI signals and never crashes or exits 2.
"""
import argparse
import datetime
import json
import os
import subprocess
import sys
import tempfile

# Threshold constants (locked).
GREENFIELD_MAX_FILES = 50
GREENFIELD_MAX_AGE_DAYS = 30
LEGACY_MIN_FILES = 400
LEGACY_MIN_AGE_DAYS = 365
LEGACY_LOW_CHURN_COMMITS = 10

TEST_DIR_NAMES = {"test", "tests", "__tests__", "spec"}
# Filename predicates for test files (checked against basenames).
_TEST_FILE_PREDICATES = (
    lambda b: b.startswith("test_") and b.endswith(".py"),
    lambda b: b.endswith("_test.py"),
    lambda b: b.endswith("_test.go"),
    lambda b: ".test." in b,
    lambda b: ".spec." in b,
)


def _git(root, *args):
    """Run a git command in `root`; return stdout (stripped) or None on failure."""
    try:
        out = subprocess.run(
            ["git", "-C", root, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return out.stdout.decode("utf-8", "replace").strip()


def _is_git_repo(root):
    return _git(root, "rev-parse", "--is-inside-work-tree") == "true"


def _git_toplevel(path):
    return _git(path, "rev-parse", "--show-toplevel")


def _tracked_files(root):
    """List of tracked file paths (relative). Empty list if unavailable."""
    out = _git(root, "ls-files")
    if not out:
        return []
    return [line for line in out.split("\n") if line]


def _detect_tests(tracked):
    """True if any tracked path looks like a test dir or test file."""
    for rel in tracked:
        parts = rel.split("/")
        base = parts[-1]
        if any(p in TEST_DIR_NAMES for p in parts[:-1]):
            return True
        if any(pred(base) for pred in _TEST_FILE_PREDICATES):
            return True
    return False


def _detect_ci(root):
    """True if .github/workflows has >=1 file OR .gitlab-ci.yml exists."""
    wf_dir = os.path.join(root, ".github", "workflows")
    if os.path.isdir(wf_dir):
        try:
            if any(os.path.isfile(os.path.join(wf_dir, e)) for e in os.listdir(wf_dir)):
                return True
        except OSError:
            pass
    if os.path.isfile(os.path.join(root, ".gitlab-ci.yml")):
        return True
    return False


def _first_commit_date(root):
    """ISO date (YYYY-MM-DD) of the first commit, or None if unavailable."""
    out = _git(root, "log", "--reverse", "--format=%cs")
    if not out:
        return None
    first = out.split("\n", 1)[0].strip()
    return first or None


def _commits_last_90d(root):
    """Count of commits in the last 90 days (0 if unavailable)."""
    out = _git(root, "log", "--since=90 days ago", "--oneline")
    if out is None:
        return 0
    if out == "":
        return 0
    return len([line for line in out.split("\n") if line])


def _repo_age_days(first_commit_date, today):
    """today - first_commit_date in days. Null/unparsable first commit -> 0 (new)."""
    if not first_commit_date:
        return 0
    try:
        d = datetime.date.fromisoformat(first_commit_date)
    except ValueError:
        return 0
    return (today - d).days


def gather_signals(root, today=None):
    """Collect all detection signals into a dict."""
    if today is None:
        today = datetime.date.today()
    tracked = _tracked_files(root)
    first_commit = _first_commit_date(root)
    return {
        "tests_present": _detect_tests(tracked),
        "ci_present": _detect_ci(root),
        "first_commit_date": first_commit,
        "tracked_file_count": len(tracked),
        "commits_last_90d": _commits_last_90d(root),
        "repo_age_days": _repo_age_days(first_commit, today),
    }


def classify(signals):
    """Apply the locked heuristic. Returns (maturity, [reason strings])."""
    files = signals["tracked_file_count"]
    age = signals["repo_age_days"]
    tests = signals["tests_present"]
    ci = signals["ci_present"]
    churn = signals["commits_last_90d"]

    # greenfield first.
    gf_reasons = []
    if files < GREENFIELD_MAX_FILES:
        gf_reasons.append("tracked_file_count %d < %d" % (files, GREENFIELD_MAX_FILES))
    if age < GREENFIELD_MAX_AGE_DAYS:
        gf_reasons.append("repo_age_days %d < %d" % (age, GREENFIELD_MAX_AGE_DAYS))
    if not ci and not tests:
        gf_reasons.append("no CI and no tests")
    if gf_reasons:
        return "greenfield", gf_reasons

    # then legacy.
    if tests and ci and files >= LEGACY_MIN_FILES and age >= LEGACY_MIN_AGE_DAYS:
        return "legacy", [
            "has tests + CI, tracked_file_count %d >= %d, repo_age_days %d >= %d"
            % (files, LEGACY_MIN_FILES, age, LEGACY_MIN_AGE_DAYS)
        ]
    if age >= LEGACY_MIN_AGE_DAYS and churn < LEGACY_LOW_CHURN_COMMITS:
        return "legacy", [
            "low churn:age (repo_age_days %d >= %d and commits_last_90d %d < %d)"
            % (age, LEGACY_MIN_AGE_DAYS, churn, LEGACY_LOW_CHURN_COMMITS)
        ]

    # default.
    return "active", ["middle ground: not greenfield, not legacy (safe default)"]


def _atomic_write(target_path, data):
    """Atomically write `data` (str) to target_path via temp-in-same-dir + replace."""
    target_dir = os.path.dirname(target_path)
    os.makedirs(target_dir, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=target_dir, prefix=".team-profile.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(data)
        os.replace(tmp, target_path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _render_human(maturity, signals, reasons, written_path):
    lines = []
    lines.append("Suggested maturity: %s" % maturity)
    lines.append("")
    lines.append("Why:")
    for r in reasons:
        lines.append("  - %s" % r)
    lines.append("")
    lines.append("Signals:")
    lines.append("  tests_present      : %s" % signals["tests_present"])
    lines.append("  ci_present         : %s" % signals["ci_present"])
    lines.append("  first_commit_date  : %s" % (signals["first_commit_date"] or "(unavailable)"))
    lines.append("  repo_age_days      : %d" % signals["repo_age_days"])
    lines.append("  tracked_file_count : %d" % signals["tracked_file_count"])
    lines.append("  commits_last_90d   : %d" % signals["commits_last_90d"])
    lines.append("")
    if written_path:
        lines.append("Wrote suggestion to %s" % written_path)
    else:
        lines.append("(suggestion only; pass --write to persist to .claude/team-profile.json)")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Suggest a team-profile maturity for a repo (suggests, never forces)."
    )
    ap.add_argument("root", nargs="?", default=None,
                    help="repo path (default: git toplevel of cwd)")
    ap.add_argument("--write", action="store_true",
                    help="atomically write ROOT/.claude/team-profile.json")
    ap.add_argument("--format", choices=["json", "human"], default="human")
    args = ap.parse_args(argv)

    try:
        if args.root is None:
            root = _git_toplevel(os.getcwd())
            if not root:
                print("error: cwd is not inside a git repository (and no ROOT given)",
                      file=sys.stderr)
                return 2
        else:
            root = os.path.abspath(args.root)
            if not _is_git_repo(root):
                print("error: %s is not a git repository" % root, file=sys.stderr)
                return 2

        signals = gather_signals(root)
        maturity, reasons = classify(signals)

        written_path = None
        if args.write:
            payload = {
                "maturity": maturity,
                "signals": signals,
                "detected_at": datetime.datetime.now(datetime.timezone.utc)
                .isoformat(timespec="seconds")
                .replace("+00:00", "Z"),
            }
            target = os.path.join(root, ".claude", "team-profile.json")
            _atomic_write(target, json.dumps(payload, indent=2, sort_keys=True) + "\n")
            written_path = target

        if args.format == "json":
            out = {
                "maturity": maturity,
                "signals": signals,
                "reasons": reasons,
                "written": written_path,
            }
            print(json.dumps(out, indent=2, sort_keys=True))
        else:
            print(_render_human(maturity, signals, reasons, written_path))

        return 0
    except Exception as e:  # never crash with a traceback; map to exit 2.
        print("internal error: %s" % e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
