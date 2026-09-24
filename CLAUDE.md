# bharats-claude-toolkit

Claude Code plugin + marketplace (vendored skills, role agents, hooks, scripts). Behavioural rules live in the user-level `~/.claude/CLAUDE.md` that `scripts/bootstrap.sh` installs from `templates/user-CLAUDE.md`; this file holds repo facts only.

## Verify before done

- `python3 scripts/validate_skills.py --strict-yaml`
- `python3 scripts/validate_skills.py --check-catalog` (regenerate with `--catalog`)
- `python3 scripts/validate_assets.py`
- `python3 scripts/validate_profiles.py`
- `uv run --quiet --python 3.12 --with pytest pytest -q skills/_lib`
- `scripts/quality_gate.py` detects no stack here, so its pass is vacuous; do not cite it as evidence.

## Release

- `python3 scripts/release.py --bump <level>`, commit, then `git tag vX.Y.Z`, then push. Never tag before the release commit.
- CHANGELOG edits go under `## [Unreleased]`.

## Etiquette

- Branches `claude/<topic>`; PRs to `main`, merged with merge commits; no force-push.
- Commit attribution trailer as configured for the session.

## Vendored skills

- Keep `name` == directory; keep disambiguated descriptions verbatim; neutralize links that escape the skill directory.
- To re-vendor: find local edits with `git diff $(git log --diff-filter=A --format=%H -- skills/<name>/SKILL.md | tail -1)..HEAD -- skills/<name>`, copy upstream, re-apply them, record the upstream HEAD in `THIRD_PARTY_SOURCES.json`.

## Beads

- `bd create ... --acceptance ... --deps <one id>`: one id per `--deps`; add more with `bd dep add`.
- In a worktree the store resolves to the main checkout's `.beads/`.
- `bd ready --exclude-type epic`; `bd close --reason "..."`.

## Team sessions

- `python3 scripts/team_sentinel.py set|clear --session <id>` is the only sentinel mechanism; always pair `set` with `clear`.

## Bootstrap

- `bash scripts/bootstrap.sh` merges `settings.json` into `~/.claude/settings.json` add-only, except repo-side `false` plugin values, which are enforced.

## Compaction

When compacting, preserve: the list of files modified this session, the last validator/test results, open task ids, and any decision stated exactly.
