## block:header
# {repo_name}

{one_liner}

## block:verify
## Verify before done
{command_lines}
- Paste the command and its output as evidence; do not claim a pass you did not run.

## block:etiquette
## Etiquette
- Default branch `{default_branch}`; branches `{branch_prefix}<topic>`; PRs merged with {merge_style} commits; no force-push.

## block:working
## How work flows here
- Explore → plan (plan mode for multi-file changes) → implement → run the check above.
- Unattended runs: `/goal <the check passes and git status is clean>`.
- Before merge: `code-reviewer` on the diff against the task's acceptance criteria.
- Multi-file or multi-agent work: `/team <goal>` (team profile: {maturity}); parallel sessions use worktrees.
- Tasks live in beads (`bd`), auto-initialised per repo.
- Effort: `{effort}` for build work; `high` for design, debugging and review.

## block:compaction
## Compaction
When compacting, preserve: files modified this session, the last check result, open task ids, and decisions stated exactly.
