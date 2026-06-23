#!/usr/bin/env python3
"""Check vendored-skill upstreams for drift vs THIRD_PARTY_SOURCES.json. Stdlib only.

For each source in the manifest, runs `git ls-remote <repo> HEAD` and compares
the current upstream HEAD SHA against the recorded `upstream_head_at_manifest`.

Output-format split is INTENTIONAL: the report/interactive family of tools
(this script, doctor.py) uses --format human|json, while the validate_* family
(validate_skills.py, validate_assets.py) uses --format text|github. A maintainer
knows which to expect from which tool.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

LS_REMOTE_TIMEOUT = 20  # seconds, per source

STATUS_UP_TO_DATE = "up-to-date"
STATUS_UPDATE_AVAILABLE = "UPDATE-AVAILABLE"
STATUS_UNKNOWN = "unknown"


def resolve_head(repo):
    """Return the current upstream HEAD SHA for `repo`, or None on any failure.

    Never raises: timeouts, missing git, network errors, non-zero exit, and
    unparseable output all collapse to None so the caller's loop continues.
    """
    try:
        proc = subprocess.run(
            ["git", "ls-remote", repo, "HEAD"],
            capture_output=True,
            text=True,
            timeout=LS_REMOTE_TIMEOUT,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None
    except Exception:  # noqa: BLE001 - belt-and-suspenders; never crash a source
        return None

    if proc.returncode != 0:
        return None
    out = proc.stdout.strip()
    if not out:
        return None
    first = out.splitlines()[0].split()
    if not first:
        return None
    sha = first[0]
    # sanity-check it looks like a hex SHA
    if len(sha) < 7 or any(c not in "0123456789abcdefABCDEF" for c in sha):
        return None
    return sha


def build_results(manifest_path):
    """Return a list of per-source dicts in manifest order.

    A malformed manifest entry (missing repo or recorded SHA) never crashes the
    run: it is reported as status 'unknown'.
    """
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    results = []
    for s in data.get("sources", []):
        repo = s.get("repo")
        recorded = s.get("upstream_head_at_manifest")
        if not repo or not recorded:
            results.append({
                "repo": repo or "unknown",
                "recorded": recorded or "unknown",
                "current": "unknown",
                "status": STATUS_UNKNOWN,
            })
            continue
        current = resolve_head(repo)
        if current is None:
            results.append({
                "repo": repo,
                "recorded": recorded,
                "current": "unknown",
                "status": STATUS_UNKNOWN,
            })
            continue
        # Full-string SHA comparison; truncation is display-only.
        status = STATUS_UP_TO_DATE if current == recorded else STATUS_UPDATE_AVAILABLE
        results.append({
            "repo": repo,
            "recorded": recorded,
            "current": current,
            "status": status,
        })
    return results


def render_human(results):
    total = len(results)
    n = sum(1 for r in results if r["status"] == STATUS_UPDATE_AVAILABLE)
    k = sum(1 for r in results if r["status"] == STATUS_UNKNOWN)

    headline = f"{n} of {total} upstreams have updates available"
    if k:
        headline += f"; {k} could not be checked"

    lines = [headline, ""]
    lines.append("| repo | recorded | current | status |")
    lines.append("|---|---|---|---|")
    for r in results:
        rec = r["recorded"][:12] if r["recorded"] != "unknown" else "unknown"
        cur = r["current"][:12] if r["current"] != "unknown" else "unknown"
        lines.append(f"| {r['repo']} | {rec} | {cur} | {r['status']} |")

    if n > 0:
        lines.append("")
        lines.append(
            "Update: re-copy upstream + re-apply de-branding "
            "(see README “Maintaining vendored skills”)."
        )
    return "\n".join(lines)


def render_json(results):
    total = len(results)
    n = sum(1 for r in results if r["status"] == STATUS_UPDATE_AVAILABLE)
    k = sum(1 for r in results if r["status"] == STATUS_UNKNOWN)
    obj = {
        "summary": {"total": total, "update_available": n, "unknown": k},
        "sources": results,
    }
    return json.dumps(obj, indent=2)


def main(argv):
    ap = argparse.ArgumentParser(
        description="Check vendored-skill upstreams for drift vs the manifest."
    )
    # Report family uses human|json (NOT text|github); see module docstring.
    ap.add_argument("--format", choices=["human", "json"], default="human")
    ap.add_argument(
        "--fail-on-drift",
        action="store_true",
        help="exit 1 if any source is UPDATE-AVAILABLE; "
             "'unknown' sources alone do NOT trip this flag",
    )
    args = ap.parse_args(argv)

    root = Path(__file__).resolve().parent.parent
    manifest = root / "THIRD_PARTY_SOURCES.json"

    results = build_results(manifest)

    if args.format == "json":
        print(render_json(results))
    else:
        print(render_human(results))

    if args.fail_on_drift and any(r["status"] == STATUS_UPDATE_AVAILABLE for r in results):
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:  # noqa: BLE001
        print(f"internal error: {e}", file=sys.stderr)
        sys.exit(2)
