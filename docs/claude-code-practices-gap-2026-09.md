# Claude Code practice review — what this toolkit should change (2026-09-24)

Scope: current official guidance (code.claude.com docs for memory, best practices, skills,
subagents, agent teams, workflows, hooks, `/goal`, features overview; Claude Code 2.1.280),
Anthropic engineering/model-guide writing (context engineering, harness design, multi-agent
research, Opus 5.5 / Fable 5.1 prompting guides), and the three skill-authoring standards
this toolkit touches (mattpocock `writing-for-agents`, superpowers `writing-skills`,
Anthropic `skill-creator` / agentskills.io). Mapped against every surface in this repo.
Research notes with URLs: session scratchpad `research-cc-practices.md`,
`research-agent-practice.md`. Nothing below is applied yet; each item names the surface,
the guidance it comes from, and the concrete tweak.

## The four findings that matter most

1. **The skill listing is over budget, which is why vendored skills don't fire.** Every
   model-invocable skill's description loads on every request. This plugin contributes 134
   of them, ~79k chars (~20k tokens). The docs' listing budget is a small fraction of the
   context window and entries get truncated, "which can strip the keywords Claude needs".
   The 30-day usage report (`scripts/skill_usage.py`) shows 3 of 134 vendored skills fired.
   **Tweak:** cap model-invocable skills at roughly 40. Set `disable-model-invocation: true`
   on the business-domain tiers (sales/CS/revops, marketing, C-suite/finance) so they cost
   nothing until invoked with `/name`, or move them to a second plugin that is registered
   but not enabled. Confirm the listing size with `/context` before and after.
2. **`model: opus` now means Opus 5.5, whose default effort is `medium`.** The reviewer,
   tech-lead, integrator and architect agents say "Effort: high" in prose, which the harness
   ignores. **Tweak:** set `effort: high` (reviewer: `xhigh`) in agent frontmatter; the
   model guides say effort is the lever, prompt exhortation is not.
3. **Project CLAUDE.md carries no project facts and loads twice.** `./CLAUDE.md` is the
   same Karpathy rules file bootstrap installs at `~/.claude/CLAUDE.md`, so in this repo it
   is duplicated context with zero repo-specific content (validators, catalog regen, release
   flow, beads gotchas). **Tweak:** keep the behavioural rules at user level only; replace
   the project file with a ≤60-line repo file (commands Claude can't guess, repo etiquette,
   gotchas, a compaction-preservation line) and move path-conditional guidance into
   `.claude/rules/`.
4. **The orchestration surface lacks the three contracts the guidance now expects:** a
   teammate brief template (objective, output format, tools/sources, boundaries, file scope,
   report path), a progress-update contract (opening intent line, at most one line between
   waves, a closing recap that stands alone, DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT /
   BLOCKED status), and a review loop (adversarial reviewer told "gaps only" → fix →
   re-review until PASS, with the reviewer allowed to run the project's checks). All three
   had to be improvised by hand during this week's sweep.

## Surface-by-surface

### `CLAUDE.md` (project) and `~/.claude/CLAUDE.md` (user, installed by bootstrap)

Guidance: target under 200 lines; include commands Claude can't guess, style that differs
from defaults, test runners, repo etiquette, env quirks, gotchas; exclude anything derivable
from code; one `IMPORTANT` line at most; tell Claude what to preserve on compaction; use
`/doctor` for trim proposals; `/init` suggests improvements to an existing file.

- Keep the Karpathy rules as the **user-level** file (they are preferences, not project
  facts). Drop the "Merge with project-specific instructions" line; it is doing nothing.
- Replace the **project** `CLAUDE.md` with repo facts only:
  validators (`validate_skills.py --strict-yaml`, `--check-catalog` / `--catalog`,
  `validate_assets.py`, `validate_profiles.py`), tests (`uv run --with pytest pytest skills/_lib`),
  release flow (`release.py --bump` then commit → tag → push), branch/PR etiquette
  (`claude/*` branches, merge commits, tag after the release commit), beads gotchas
  (`bd create --deps` one id per flag, worktrees share the main checkout's store), vendored-
  skill re-apply procedure (`git diff <first-vendor-commit>..HEAD -- skills/<name>`), and
  "When compacting, preserve the list of modified files, validator results and open beads ids".
- Add a **compaction-preservation** sentence to the user-level file too (the best-practices
  page recommends it; it costs one line).
- Run `/doctor` on the result once and prune what it flags as derivable.

### `.claude/rules/` (new surface)

Guidance: one topic per file; `paths:` frontmatter loads a rule only when Claude touches
matching files; unconditional rules load like CLAUDE.md, so keep those few.

- `rules/skills.md` (`paths: skills/**`): frontmatter contract (name == dir, description
  40–1024 chars, combined with `when_to_use` ≤1,536), link-neutralization rule (no links
  that escape the skill dir), `metadata.source` convention, "keep `SKILL.md` under 500
  lines, references in `references/`", partner/affiliate-link rule for marketing sources.
- `rules/hooks-scripts.md` (`paths: hooks/**, scripts/**`): stdlib only, bounded stdin,
  exit-code contract (0 allow / 2 block), fail-open policy and which hooks must fail
  closed, `--format human|json` vs `text|github` families.
- `rules/agents.md` (`paths: agents/**`): frontmatter fields to use (`effort`, `tools`,
  `permissionMode`), no boilerplate defense blocks, descriptions lead with the use case.

### `agents/*.md` (8 role agents)

Guidance: frontmatter now carries `effort`, `permissionMode`, `maxTurns`, `omitClaudeMd`,
`memory`, `background`, `isolation`; descriptions should say what and when; guardrails
belong in hooks, not prose; a fresh-context reviewer must be told to report gaps only.

- Move "Effort: high" prose into `effort:` frontmatter on every agent (see finding 2).
- Delete the six-bullet "Prompt Defense Baseline" block from all eight files. It is
  advisory text repeated per spawn; the docs are explicit that enforcement belongs in
  `PreToolUse` hooks / `permissions.deny`, which this repo already has.
- `code-reviewer`: widen the Bash allowlist to "the project's own verification commands
  (tests, linters, validators, quality gate), read-only", and add "flag only gaps that
  affect correctness or the stated criteria; treat the rest as optional" per the
  best-practices callout. Its gate was vacuous twice this week because it could only run
  `quality_gate.py`, which detects no stack here.
- `tech-lead`: remove the hand-written sentinel JSON "FIRST ACTION"; the skill's
  `team_sentinel.py set` is the single mechanism. Decide whether this agent still exists
  as a subagent at all: the skill already casts the main session as tech-lead.
- Consider `memory: project` on `code-reviewer` and `integrator` so repeated findings
  persist, and `omitClaudeMd: true` on none (they need the repo file above).
- Descriptions: the ecc-derived "Use PROACTIVELY" phrasing is fine; make sure each
  states the use case first (spec-miner and code-architect already do).

### `skills/team-orchestration/` (the `/team` brain)

Guidance: brief = objective + output format + tools/sources + boundaries; teammates don't
inherit the lead's history; file-partitioned scopes; 3–5 workers per wave; an external
evaluator because self-grading skews positive; `/goal`-style conditions (one measurable end
state, a stated check, constraints); async lead keeps working; time budgets speed teams;
final message stands alone.

- Add `references/teammate-brief.md`: the template used this week (scope = directories
  the agent may write; report path in scratchpad; validator to run after each unit;
  "report, don't fix" for out-of-scope findings; the autonomy block for unattended runs).
- Add a **progress contract** section: opening line of intent; one short line per wave;
  status vocabulary; closing recap that stands alone; surface evidence (validator output),
  not assertions.
- Add the **review loop**: spawn `code-reviewer` on the diff with the acceptance criteria,
  fix, re-review via `SendMessage` to the same reviewer until PASS; cap at three rounds,
  then escalate to the user.
- Add a **verification** paragraph: write each task's acceptance criteria as a `/goal`
  condition; for unattended runs set `/goal` (or the legacy profile's Stop-hook gate) so the
  session doesn't end on "looks done".
- Add the **orchestration ladder**: subagents for focused workers; a Workflow when the job
  outgrows a handful of agents or findings need cross-checking; agent teams stay off.
- Fold the beads CLI gotchas into `references/beads-contract.md` (they are in memory only).
- Note superpowers 6.4.1: `executing-plans` no longer pauses mid-plan; if a user runs plans
  through superpowers, this skill's gates are the review layer.

### `commands/` (3 files)

Guidance: commands are merged into skills and still work, but "prefer a skill for new
work" because skills support supporting files, `argument-hint`, `disable-model-invocation`.

- Migrate `doctor`, `team`, `toolkit` to `skills/<name>/SKILL.md` with
  `disable-model-invocation: true` (user-invoked, zero listing cost) and `argument-hint`.
  `team` already delegates to `team-orchestration`; the migration is mechanical.

### `skills/` catalog (134 vendored skills)

Guidance: description is the only always-loaded text; put the key use case first;
`when_to_use` for trigger phrases; `paths:` for file-scoped skills; `context: fork` for
skills that should not pollute the main context; `/skill-doctor` and `claude plugin eval`.

- Apply finding 1 (demote the business tiers). Candidates for `paths:` scoping instead:
  `python-patterns`/`python-testing` (`**/*.py`), `fastapi-patterns`, `postgres-patterns`
  (`**/*.sql`), `react-*`/`motion-*` (`**/*.{tsx,jsx}`), `rego-skill` (`**/*.rego`).
- Move long-running research skills (`market-research`, `competitive-intel`, `repo-scan`,
  `production-audit`, `threat-model`, `vuln-*`) to `context: fork` so their file reads stay
  out of the main window.
- Grow `evals/` from one case to one per always-on skill family; wire `claude plugin eval`
  into the release checklist.
- Keep the house authoring standard (`writing-for-agents`) but record the resolved
  conflicts in `rules/skills.md`: descriptions say what and when (spec/docs), triggers
  phrased as `when_to_use`, no user-invoked skill calls another user-invoked skill.

### `hooks/` and `settings.json`

Guidance: hooks fire before every permission mode and beat deny rules; hooks that crash fail
open unless they exit 2; deny rules match command text only, so layer with `/sandbox`;
`if:` filters keep hook cost down; put guardrails in hooks, not CLAUDE.md.

- `secret_scan.py`: it is a guardrail, so make its own internal error exit 2 (fail closed)
  while keeping `beads_init`/`notify` fail-open. Document the split in `hooks-security.md`.
- Add a `permissions.deny` block to the settings template for credential paths
  (`Read(./.env)`, `Read(./.env.*)`, `Read(~/.ssh/**)`, `Read(~/.aws/**)`, cloud SA files)
  so the layer exists even where hooks are disabled.
- Add `if:` filters where matchers are broad (the Stop teardown hook runs on every turn).
- Expose in the template, commented: `syncClaudeAiSkills: false` (claude.ai skill sync can
  silently inflate the skill listing), `autoMemoryEnabled`, `workflowSizeGuideline`.

### `workflows/`

Guidance: workflows for jobs that outgrow a handful of subagents or need cross-checking;
`schema` forces structured subagent output; `label`/`phase` for observability; 16
concurrent by default.

- Add `schema` to the reviewer/verify agents in `review-changes` and
  `implement-task-with-gates` so verdicts are machine-checkable.
- Document in the README when `/team` (subagents) vs a workflow is the right tool, using
  the docs' ladder.

### Output style (new, optional surface)

Guidance: response length/format belongs in an output style, not CLAUDE.md; plugins can
ship `outputStyles`.

- Ship one `toolkit` output style: intent line first, no tool-call narration, evidence over
  assertion, closing recap that stands alone, bullets only for parallel items. This is the
  progress contract for humans, kept out of every agent prompt.

### Memory

Guidance: CLAUDE.md is what you write, auto memory is what Claude learns; `MEMORY.md`
loads first 200 lines / 25 KB; topic files on demand.

- Nothing to change in the repo. Keep repo-derivable facts out of memory (they are), and
  move the two beads gotchas from memory into `references/beads-contract.md` (above) so
  other machines get them.

### `README.md` and `docs/`

- Add a short "Working with this toolkit" section: the explore → plan → implement → verify
  → review loop as the docs describe it, `/goal` for unattended runs, `/btw` for side
  questions, `/clear` between tasks, and where each surface lives (CLAUDE.md vs rules vs
  skills vs hooks) using the docs' feature table.
- `docs/hooks-security.md`: add the fail-open/fail-closed split above.

## Prioritised list

| # | Tweak | Surface | Effort | Why now |
|---|---|---|---|---|
| 1 | Demote business-domain skills to user-invoked (or second plugin) | skills/, settings | M | Listing over budget; skills not firing |
| 2 | `effort:` frontmatter on all agents; reviewer `xhigh` | agents/ | S | Opus 5.5 default is `medium` |
| 3 | Repo-specific project CLAUDE.md; Karpathy rules user-level only | CLAUDE.md | S | Duplicate context, zero repo facts |
| 4 | `.claude/rules/` for skills, hooks/scripts, agents | new | S | Keeps CLAUDE.md short; path-scoped |
| 5 | Teammate brief + progress contract + review loop in team-orchestration | skill | M | Improvised by hand this week |
| 6 | Reviewer may run project checks; "gaps only" wording | agents/ | S | Gate was vacuous |
| 7 | Remove Prompt Defense boilerplate; single sentinel mechanism | agents/ | S | Advisory text; two mechanisms |
| 8 | secret_scan fails closed; `permissions.deny` credential paths | hooks, settings | S | Guardrail layering |
| 9 | `paths:` / `context: fork` on the skills that qualify | skills/ | M | Context cost |
| 10 | Migrate 3 commands to skills | commands/ | S | Docs prefer skills |
| 11 | Output style + README "working with the toolkit" | new, README | S | Progress contract for humans |
| 12 | Workflow `schema` on verdict agents; evals per skill family | workflows/, evals/ | M | Machine-checkable gates |

Items 1–4 and 6–8 are a single small PR. Item 5 is its own PR. Items 9–12 can follow.
