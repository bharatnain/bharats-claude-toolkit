#!/usr/bin/env python3
"""Cut a release: bump version, scaffold CHANGELOG, refresh manifest, tag. Stdlib only.

NO-SURPRISE guarantee: this script mutates the working tree and creates a LOCAL
git tag, but it NEVER `git commit` and NEVER `git push`. After its writes it
PRINTS the exact next commands for the human to run.

Output format note: like the report-family scripts (check_upstream.py, doctor.py)
this is an interactive human tool; it prints a plain human-readable plan. --dry-run
prints the same plan and writes/tags nothing (one shared code path).

Usage:
  python3 scripts/release.py --bump patch [--refresh-manifest] [--dry-run]
  python3 scripts/release.py --version 0.8.0 [--refresh-manifest] [--dry-run]
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"
CHANGELOG = ROOT / "CHANGELOG.md"
MANIFEST = ROOT / "THIRD_PARTY_SOURCES.json"

VERSION_LINE_RE = re.compile(r'"version"\s*:\s*"([^"]+)"')
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

# Standard re-sync footer line every recent CHANGELOG entry ends with.
RESYNC_LINE = (
    "- **Re-sync:** `git pull && bash scripts/bootstrap.sh`, then `/reload-plugins` "
    "(or restart Claude Code)."
)


def atomic_write(target: Path, text: str) -> None:
    """Write text to target atomically: mktemp in the same dir + os.replace.

    Mirrors bootstrap.sh's mktemp-in-same-dir + mv pattern so a failure mid-run
    never leaves the target half-written.
    """
    fd, tmp = tempfile.mkstemp(dir=str(target.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, target)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def read_current_version(plugin_text: str) -> str:
    """Regex-extract the current version from plugin.json text (single source of truth)."""
    m = VERSION_LINE_RE.search(plugin_text)
    if not m:
        raise ValueError(f'could not find a "version" key in {PLUGIN_JSON}')
    return m.group(1)


def compute_bumped(current: str, part: str) -> str:
    """Increment the chosen semver component, zeroing lower components."""
    if not SEMVER_RE.match(current):
        raise ValueError(f"current version {current!r} is not X.Y.Z; cannot --bump")
    major, minor, patch = (int(x) for x in current.split("."))
    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        minor, patch = minor + 1, 0
    else:  # patch
        patch += 1
    return f"{major}.{minor}.{patch}"


def validate_explicit(version: str, current: str) -> str:
    """Validate an explicit --version: X.Y.Z shape and != current (prefer > current)."""
    if not SEMVER_RE.match(version):
        raise ValueError(f"--version {version!r} must match X.Y.Z")
    if version == current:
        raise ValueError(f"--version {version!r} equals the current version; pick a new one")
    cur = tuple(int(x) for x in current.split(".")) if SEMVER_RE.match(current) else None
    new = tuple(int(x) for x in version.split("."))
    if cur is not None and new < cur:
        raise ValueError(f"--version {version} is lower than current {current}")
    return version


def surgical_version_replace(plugin_text: str, new_version: str) -> str:
    """Replace ONLY the version line value, preserving all other formatting."""
    new_text, n = VERSION_LINE_RE.subn(f'"version": "{new_version}"', plugin_text, count=1)
    if n != 1:
        raise ValueError("failed to surgically replace the version line in plugin.json")
    return new_text


def _git(args):
    """Run a git command at ROOT; return (returncode, stdout, stderr)."""
    proc = subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def changelog_bullets() -> list:
    """Bullets from `git log <lastTag>..HEAD --oneline`; full history if no tag."""
    rc, out, _ = _git(["describe", "--tags", "--abbrev=0"])
    last_tag = out.strip() if rc == 0 and out.strip() else None
    log_range = [f"{last_tag}..HEAD"] if last_tag else []
    rc, out, _ = _git(["log", *log_range, "--oneline"])
    if rc != 0:
        return []
    bullets = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        # Drop the leading short SHA ("a1b2c3d Subject" -> "Subject").
        parts = line.split(" ", 1)
        subject = parts[1].strip() if len(parts) == 2 else line
        bullets.append(f"- {subject}")
    return bullets


def build_changelog_section(version: str, bullets: list) -> str:
    """Render the new Keep-a-Changelog section text (heading + bullets + re-sync)."""
    today = datetime.date.today().isoformat()
    lines = [f"## [{version}] - {today}", ""]
    lines.extend(bullets if bullets else ["- (no commits since last tag)"])
    lines.append(RESYNC_LINE)
    return "\n".join(lines) + "\n"


def insert_changelog_section(changelog_text: str, section: str) -> str:
    """Insert the new section immediately before the first existing '## [' heading."""
    lines = changelog_text.splitlines(keepends=True)
    insert_at = None
    for i, line in enumerate(lines):
        if line.startswith("## ["):
            insert_at = i
            break
    block = section + "\n"  # blank line between new section and the next one
    if insert_at is None:
        # No existing entries: append after the header/intro.
        base = changelog_text if changelog_text.endswith("\n") else changelog_text + "\n"
        return base + "\n" + section
    return "".join(lines[:insert_at]) + block + "".join(lines[insert_at:])


def _inline_resolve_head(repo_url: str):
    """Fallback ls-remote HEAD resolver (used if check_upstream.resolve_head absent)."""
    try:
        proc = subprocess.run(
            ["git", "ls-remote", repo_url, "HEAD"],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except Exception:
        return None
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    return proc.stdout.split()[0].strip()


def get_resolve_head():
    """Reuse DRIFT's resolve_head from check_upstream.py if available; else fall back.

    Keeps the ls-remote logic in ONE place when check_upstream.py exists, while
    staying robust if that sibling Phase G script is not present.
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from check_upstream import resolve_head  # type: ignore
        return resolve_head
    except Exception:
        return _inline_resolve_head


def compute_manifest_updates(resolve_head):
    """Resolve each source's current upstream HEAD.

    Returns (manifest_dict, updates) where updates is a list of
    (repo, old_sha, new_sha_or_None). A source that cannot be resolved
    (new_sha is None) is LEFT UNCHANGED.
    """
    with open(MANIFEST, "r", encoding="utf-8") as f:
        data = json.load(f)
    updates = []
    for src in data.get("sources", []):
        repo = src.get("repo", "")
        old = src.get("upstream_head_at_manifest")
        new = resolve_head(repo) if repo else None
        updates.append((repo, old, new))
    return data, updates


def apply_manifest_updates(data, updates) -> str:
    """Apply resolved SHAs into the manifest dict and return serialized JSON text.

    Unresolved sources (new is None) are left unchanged. This file is data, so a
    full json.dump (indent=2, ensure_ascii=False, trailing newline) is acceptable
    and mirrors bootstrap.sh's settings re-dump.
    """
    new_by_repo = {repo: new for (repo, _old, new) in updates if new is not None}
    for src in data.get("sources", []):
        repo = src.get("repo", "")
        if repo in new_by_repo:
            src["upstream_head_at_manifest"] = new_by_repo[repo]
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def next_commands(version: str, refresh_manifest: bool) -> str:
    """The exact git commands the human runs to finish the release."""
    files = [".claude-plugin/plugin.json", "CHANGELOG.md"]
    if refresh_manifest:
        files.append("THIRD_PARTY_SOURCES.json")
    add = "git add " + " ".join(files)
    return (
        f"  {add}\n"
        f'  git commit -m "Release v{version}"\n'
        f"  git push && git push --tags"
    )


def main(argv):
    ap = argparse.ArgumentParser(
        description="Cut a release: bump version, scaffold CHANGELOG, optionally refresh "
        "the source manifest, and create a local tag. Never commits or pushes."
    )
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--bump", choices=["patch", "minor", "major"],
                   help="compute the next semver from the current version")
    g.add_argument("--version", help="set an explicit X.Y.Z version (> current)")
    ap.add_argument("--refresh-manifest", action="store_true",
                    help="re-resolve each source's upstream HEAD and update the manifest")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the full plan and write/tag nothing")
    args = ap.parse_args(argv)

    # ---- COMPUTE EVERYTHING FIRST (shared by dry-run and real run) ----
    plugin_text = PLUGIN_JSON.read_text(encoding="utf-8")
    current = read_current_version(plugin_text)
    if args.bump:
        new_version = compute_bumped(current, args.bump)
    else:
        new_version = validate_explicit(args.version, current)

    new_plugin_text = surgical_version_replace(plugin_text, new_version)

    bullets = changelog_bullets()
    section = build_changelog_section(new_version, bullets)
    changelog_text = CHANGELOG.read_text(encoding="utf-8")
    new_changelog_text = insert_changelog_section(changelog_text, section)

    manifest_data = None
    manifest_updates = []
    new_manifest_text = None
    if args.refresh_manifest:
        resolve_head = get_resolve_head()
        manifest_data, manifest_updates = compute_manifest_updates(resolve_head)
        new_manifest_text = apply_manifest_updates(manifest_data, manifest_updates)

    tag = f"v{new_version}"
    commands = next_commands(new_version, args.refresh_manifest)

    # ---- RENDER THE PLAN (printed in both modes) ----
    print(f"Release plan: {current} -> {new_version} (tag {tag})")
    print()
    print(f"plugin.json: set version to {new_version}")
    print()
    print(f"CHANGELOG.md: insert new section at top of entries:")
    for line in section.rstrip("\n").splitlines():
        print(f"    {line}")
    print()
    if args.refresh_manifest:
        print("THIRD_PARTY_SOURCES.json: upstream_head_at_manifest updates:")
        for repo, old, new in manifest_updates:
            if new is None:
                print(f"    UNCHANGED (unresolved) {repo}")
            elif new == old:
                print(f"    unchanged {repo}: {old}")
            else:
                print(f"    {repo}: {old} -> {new}")
        print()
    else:
        print("THIRD_PARTY_SOURCES.json: not touched (pass --refresh-manifest to update)")
        print()
    print(f"git tag (lightweight): {tag}")
    print()
    print("Next commands for you to run (this script does NOT commit or push):")
    print(commands)
    print()

    if args.dry_run:
        print("[dry-run] nothing written, no tag created.")
        return 0

    # ---- WRITE (atomic) THEN TAG ----
    atomic_write(PLUGIN_JSON, new_plugin_text)
    atomic_write(CHANGELOG, new_changelog_text)
    if args.refresh_manifest and new_manifest_text is not None:
        atomic_write(MANIFEST, new_manifest_text)

    # Lightweight tag (simplest, sufficient). Does NOT commit or push.
    rc, _out, err = _git(["tag", tag])
    if rc != 0:
        raise RuntimeError(f"git tag {tag} failed: {err.strip()}")

    print(f"Wrote files and created local tag {tag}.")
    print("Run the next commands above to finish the release.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:  # noqa: BLE001
        print(f"internal error: {e}", file=sys.stderr)
        sys.exit(2)
