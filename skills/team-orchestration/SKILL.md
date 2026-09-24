---
name: team-orchestration
description: Orchestrate a multi-agent team to build something end-to-end — when the user wants to build with a team, orchestrate a team, spin up a team, run a multi-agent build, or coordinate subagents with quality gates. Detects the codebase maturity profile, staffs the right roster of role agents, activates a session sentinel so the gate hooks enforce checks automatically, decomposes the goal into acceptance-criteria-bearing tasks (beads or native Task tools), spawns worktree-isolated teammates per the profile, and tears the session down at the end. Use this for the /team command.
---

# Team Orchestration

You are the **tech-lead / orchestrator**. Turn a single goal into a sequenced set of
acceptance-criteria-bearing tasks, staff a maturity-matched team, and let the live
session gates enforce quality automatically. This skill is the brain behind `/team <goal>`.

## Solo-safe invariant

The gate hooks (`team_gate`) and `quality_gate.py` are **pure no-ops** until a session
sentinel marker exists. Installing this phase changes **nothing** for solo users — gates
only activate after step 3 below sets the sentinel, and they deactivate again at teardown
(step 6). Always pair a `set` with a `clear`.

## The 6-step orchestration loop

Run these in order. Steps 3 and 6 are owner-scoped: capture the session id once and reuse
the **same** id for both `set` and `clear`.

### 1. Detect the maturity profile

```
python3 scripts/team_profile_detect.py . --write
```

This deterministically classifies the repo as `greenfield`, `active`, or `legacy` and
writes the resolved profile. **Trust this output.** Per CLAUDE.md's "Think Before Coding",
ask the user to confirm or override **only if the detection is genuinely ambiguous** (e.g.
conflicting signals, or the user's stated intent contradicts the detected maturity). Do not
interrupt the flow with a question the script has already answered.

### 2. Pick the roster

Read the detected profile's `roles.required` and staff exactly those role agents. The
mapping from profile → required/optional roles → worktree isolation is in
[references/roster-matrix.md](references/roster-matrix.md). If the profile requires a role
you cannot staff, surface the gap rather than silently skipping it.

### 3. Activate the gates (set the sentinel)

```
python3 scripts/team_sentinel.py set --profile <P> --by tech-lead --session <id>
```

- `<P>` is the profile name from step 1 (`greenfield` / `active` / `legacy`).
- `--by tech-lead` is hardcoded: this skill is operated by the tech-lead/orchestrator role
  (consistent with `agents/tech-lead.md` owning the sentinel as its documented first action).
- `<id>` is **your current Claude session id** (from the runtime/session payload). Capture it
  once here and reuse the identical value at teardown so the `clear` is owner-scoped.

Once the sentinel is live, the gate hooks and `quality_gate.py` enforce the profile's checks
automatically — you do not invoke them per-task.

### 4. Decompose the goal into tasks

Break the goal into the **smallest independently verifiable units**. **Every task MUST carry**:
- explicit, checkable **acceptance criteria**, and
- a **maturity target** (the profile/scope the task is held to).

A task without acceptance criteria is not ready to assign.

Persist tasks to **beads** when `bd` is on PATH, otherwise **degrade to native Task tools**.
Detect first, then branch — do not assume `bd` exists. The command contract (bd 1.0.4:
`bd create` with `--acceptance` → `bd ready --exclude-type epic` → `bd update --claim` →
`bd close --reason`) and the native-Task fallback are documented in
[references/beads-contract.md](references/beads-contract.md). For an automated end-to-end
variant, see the `beads-task` workflow template (`workflows/beads-task.workflow.js`).

### 5. Spawn the teammates

Spawn each teammate directly via the **Agent tool's `name` parameter** — every session has
one implicit team, so there is no team setup or teardown tool call. Every spawn prompt is a
full [teammate brief](#teammate-brief); size waves per [Waves and scopes](#waves-and-scopes). Isolate
teammates in worktrees per the **profile's `isolation.worktree`** flag (the sentinel-resolved
profile is the runtime source of truth; roster-matrix.md documents the expected value per
profile). Because the sentinel is live, the **hooks + `quality_gate.py` enforce the gates
automatically** — each teammate's work is checked against the profile's blocking checks
without you wiring it up per task.

**Background semantics**: subagents run in the **background by
default** — a spawn is not a synchronous call that returns the result inline. You keep
orchestrating while teammates work and are notified as each finishes; the gates still fire
per teammate via the `SubagentStop` hook on completion. Teammates'
permission prompts surface in **your (main) session**, so stay responsive to them. Subagents
can nest to depth 3 (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`) and run up to 20 at once
(`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`) — size your parallel waves within those caps.

### 6. Teardown

At the end of the session — after every background teammate has reported completion, not
merely after the last spawn — clear the sentinel with the **same** session id from step 3:

```
python3 scripts/team_sentinel.py clear --session <id>
```

After teardown the gate hooks return to no-ops. Never leave a session active.

## Teammate brief

Teammates start with no history. Every spawn prompt carries, in this order:

1. **Objective** — the deliverable plus its acceptance criteria as a `/goal`-style condition.
2. **Write scope** — an explicit directory/file list: "write only inside …; do not touch …".
3. **Output** — the report path in the scratchpad and the reply format (see
   [Progress contract](#progress-contract)).
4. **Check after each unit** — the exact validator/test command to run after each completed
   unit, with its output pasted into the report.
5. **Out-of-scope findings** — "report them, don't fix them".
6. **Context** — worktree path, branch, do-not-commit rule, spec to read first.
7. **Autonomy block** (unattended runs only) — "You are operating autonomously. The user is
   not watching in real time … Stop only for destructive actions or genuine scope changes."

Full template: [references/teammate-brief.md](references/teammate-brief.md). Copy it; do
not paraphrase it per spawn.

## Waves and scopes

- 3–5 teammates per wave. More than that and review cost outgrows the parallelism win.
- Partition by file: no two teammates in a wave may write the same path. If two tasks need
  the same file, put them in different waves or merge them into one brief.
- The orchestrator owns shared files — `README.md`, `CHANGELOG.md`, manifests
  (`.claude-plugin/plugin.json`), catalogs (`SKILLS.md`), settings templates. Teammates never
  edit them; a teammate that needs a shared-file change lists the exact lines in its report,
  and the orchestrator applies them after the wave.
- Keep working while a wave runs (spawns are background by default); do not poll.
- Next wave starts only after every teammate in the current wave has reported and the
  [review loop](#review-loop) for that wave has passed.

## Progress contract

**Orchestrator → user**

- One line of intent when a wave starts ("Wave 2: three teammates on hooks, agents, docs").
- At most one short line per completed teammate.
- No narration of tool calls, spawns, or file reads.
- A closing recap that stands alone — the reader has none of the transcript: what was found,
  what changed (paths), what is next, and what was verified **with evidence** (the command and
  its output, not "validators pass").

**Teammate → orchestrator**

- First line of the reply is exactly one of `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT`
  / `BLOCKED`.
- Then at most 10 lines: paths touched, validator result, open findings, report path.
- `NEEDS_CONTEXT` names the missing fact; `BLOCKED` names the blocker and what was tried.
- Everything longer goes in the report file, not the reply.

## Review loop

After each wave, before the next:

1. Spawn `code-reviewer` with the diff scope (the wave's write scopes) and the wave's
   acceptance criteria. Tell it: report gaps only; it may run the project's checks
   (validators, tests, quality gate) read-only.
2. Fix every reported gap. Do not argue with the reviewer in the transcript; fix or record a
   deliberate deviation in the recap.
3. Re-send the diff to the **same** reviewer via `SendMessage` so it keeps its context; ask
   for a verdict on the fixes only.
4. Repeat until the reviewer returns PASS.
5. Cap at 3 rounds. On the third FAIL, stop and escalate to the user with the open findings
   verbatim — do not start the next wave.

## Verification

- Write each task's acceptance criteria as a `/goal`-style condition: one measurable end
  state, the check that proves it, the constraints. "Add validation" becomes "invalid inputs
  are rejected — `pytest tests/test_validation.py` passes — no changes outside `validation/`".
- For unattended runs set `/goal <condition>` on the session so it does not end on "looks
  done". On the `legacy` profile the Stop-hook gate is the fallback.
- Close a task only on validator output shown in the report. A claim without the command and
  its result is not verification.

## Which tool

- **Subagents** (this skill): focused workers with file-partitioned scopes, up to a handful
  per wave.
- **A Workflow** (`workflows/README.md`): when the job outgrows a handful of agents, when
  findings must be cross-checked against each other, or when a verdict must be
  machine-checkable (`schema` on the verifier). `review-changes` and
  `implement-task-with-gates` are the templates.
- **Agent teams** (`TeamCreate`): experimental and off in this toolkit; do not enable.

## Plans from superpowers

superpowers 6.4.1's `executing-plans` runs a written plan natively, without mid-plan review
pauses. When a plan comes from `writing-plans` / `executing-plans`, this skill's
[review loop](#review-loop) is the review layer: run it after each wave of the plan, not
only at the end.
