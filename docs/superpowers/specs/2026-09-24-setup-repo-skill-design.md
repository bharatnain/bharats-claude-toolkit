# `/setup-repo` skill — design (2026-09-24)

## Purpose

One user-invoked skill that makes any repository an efficient place to do Claude Code work,
using the toolkit's own conventions: a short repo-facts `CLAUDE.md` with a verification
command, path-scoped rules, project permissions and a lint-on-edit hook, a team profile and
model/effort defaults, and a "how work flows here" section. Idempotent and re-runnable;
`--check` reports drift without changing anything.

Composes, does not duplicate: Claude Code's `/init` (CLAUDE.md bootstrap), the toolkit's
`codebase-onboarding` (long-form onboarding guide), `doctor` (toolkit install health), and
`team_profile_detect.py` (maturity profile).

## Invocation

- `/setup-repo` — detect, print the plan, apply after one confirmation, then re-check.
- `/setup-repo --check` — detect and print drift only (what would change); exit 0/1.
- Skill frontmatter: `disable-model-invocation: true`, `argument-hint: "[--check]"`.
- Location: `skills/setup-repo/` with `SKILL.md`, `scripts/repo_setup.py` (stdlib only),
  `scripts/lint_on_edit.py` (the hook copied into repos), `references/` templates,
  `scripts/test_repo_setup.py` (pytest, fixture repos under `scripts/fixtures/`).

## Components

### 1. Detector (`scripts/repo_setup.py detect`)

Deterministic, read-only, stdlib. Emits JSON:

- `languages`: counts by extension for the top 5 (`py`, `ts`, `tsx`, `js`, `go`, `rs`, `rb`, …).
- `package_manager`: from lockfiles/config (`uv.lock`, `poetry.lock`, `requirements*.txt`,
  `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `bun.lock*`, `go.mod`, `Cargo.toml`).
- `commands`: `test`, `lint`, `format`, `typecheck`, `build` — only when evidenced by config
  (`pyproject.toml` tool tables, `package.json` scripts, `Makefile` targets, `pytest.ini`,
  `ruff.toml`, `tsconfig.json`, `.eslintrc*`, `go.mod`, `Cargo.toml`). Each command carries
  its `source` file. Nothing is guessed.
- `ci`: paths under `.github/workflows/`, `.gitlab-ci.yml`, etc.
- `git`: default branch, remote host, whether PR merges are merge/squash (from recent
  history), branch-name prefixes in use.
- `existing`: presence and line counts of `CLAUDE.md`, `.claude/CLAUDE.md`, `AGENTS.md`,
  `CLAUDE.local.md`, `.claude/rules/*.md`, `.claude/settings.json`, `.claude/hooks/*`,
  `.claude/team-profile.json`, `.beads/`.
- `team_profile`: result of `team_profile_detect.py` (imported, not shelled) — `greenfield`,
  `active`, or `legacy` with signals.
- `size`: tracked file count; monorepo hint when multiple package roots exist.

### 2. Planner (`repo_setup.py plan`, consumed by the skill)

Turns the profile into a plan: a list of `{path, action(create|update|skip), reason}` plus
rendered file contents. Rules:

- `CLAUDE.md`: if absent, create from the template (≤60 lines). If present, keep every line
  the setup does not own and insert or replace only the blocks between
  `<!-- setup-repo:<block> -->` and `<!-- /setup-repo:<block> -->` markers. Blocks: `verify`
  (detected commands + "do not cite a vacuous pass"), `etiquette` (branch/PR facts from git),
  `working` (how work flows here: explore→plan→implement→verify with the named check; `/goal`
  for unattended runs; `code-reviewer` before merge; `/team` for multi-file work; worktrees
  for parallel sessions; beads task store; effort guidance), `compaction` (one line). No
  architecture overviews, no directory listings, no placeholders: a block whose facts are
  unknown is omitted, not stubbed.
- `.claude/rules/<lang>.md`: from `references/rules/<lang>.md` for each detected language
  with ≥5% of files; `paths:` frontmatter set to that language's globs. Existing files with
  the same name are left untouched (reported as `skip`).
- `.claude/settings.json`: add-only merge. `permissions.allow` gains `Bash(<cmd> *)` for each
  detected command; `hooks.PostToolUse` gains one entry with matcher `Edit|Write` and
  `if` scoped to the detected language's files, running `.claude/hooks/lint_on_edit.py`
  (copied in; stdlib; runs the detected lint/format command on `tool_input.file_path`, exits
  0 always, prints findings to stdout so they enter context). `effortLevel` set from the team
  profile (`legacy` → `high`, otherwise `medium`) only if absent. `env.CLAUDE_CODE_SUBAGENT_MODEL`
  is not set (subagent model stays per-agent frontmatter).
- `.claude/team-profile.json`: written via the detector; `.gitignore` gains it if absent.
- Recommendations (printed, never written): toolkit skills relevant to the stack (noting the
  `paths:`-scoped ones load themselves), a code-intelligence plugin for typed languages,
  `/sandbox` if not enabled, `syncClaudeAiSkills` note, and the workspace-trust reminder
  (project allow rules and hooks apply only after the folder is trusted).

### 3. Applier (`repo_setup.py apply --plan <json>`)

Writes exactly the planned files atomically (temp + replace), never outside `CLAUDE.md`,
`.claude/`, and `.gitignore`. Then re-runs `check` and prints the drift report (must be
empty). Exit codes: 0 clean, 1 drift/plan pending, 2 internal error.

### 4. Skill (`SKILL.md`)

Steps for Claude: run `detect`; read the JSON; run `plan`; present the plan to the user as
a file list with one line of why each and the recommendations; on yes run `apply`; paste the
post-apply `check` output as evidence; close with the three things the user should do next
(trust the folder if new, restart or `/reload-plugins`, run `/context`). With `--check`,
stop after printing drift. Under 120 lines; the templates and detection rules live in
`references/` and the script.

## Data flow

`detect` → profile JSON (scratchpad) → `plan` → plan JSON + rendered contents → user yes →
`apply` → files → `check` → drift report (evidence).

## Error handling

- Not a git repo, or no recognisable stack: detector still emits a profile; planner writes
  only the `working` and `compaction` blocks and says why the rest was skipped.
- Malformed existing `.claude/settings.json`: plan marks it `skip` with the parse error;
  nothing else is blocked.
- Existing `CLAUDE.md` without markers and over 200 lines: planner appends the owned blocks
  and prints the docs' pruning advice; it never deletes user text.
- Any write failure aborts the apply before the next file; partial state is reported.

## Testing

- `scripts/test_repo_setup.py`: fixture repos `python-uv`, `node-pnpm`, `mixed-mono`, `empty`.
  Assert detected commands and sources, plan actions, marker-preserving CLAUDE.md updates,
  add-only settings merge, idempotency (`apply` twice → second `check` empty), and that no
  file outside the allowed paths is touched.
- `validate_skills.py --strict-yaml` and `--check-catalog` green; SKILLS.md regenerated.
- Smoke: run `/setup-repo --check` on this toolkit and `/setup-repo` on one real repo.

## Out of scope

Installing plugins, editing user-level settings, running `/init` (the skill links to it for
prose refinement), generating tests, and anything under `src/`.
