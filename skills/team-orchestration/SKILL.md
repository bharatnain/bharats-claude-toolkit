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
Detect first, then branch — do not assume `bd` exists (it is not on PATH in this environment).
The command contract (`bd add` with acceptance criteria → `bd ready` → `bd update` →
`bd close`) and the native-Task fallback are documented in
[references/beads-contract.md](references/beads-contract.md).

### 5. Spawn the teammates

Spawn worktree-isolated teammates/subagents per the **profile's `isolation.worktree`** flag
(the sentinel-resolved profile is the runtime source of truth; roster-matrix.md documents the
expected value per profile). Because the sentinel is live, the **hooks + `quality_gate.py`
enforce the gates automatically** — each teammate's work is checked against the profile's
blocking checks without you wiring it up per task.

### 6. Teardown

At the end of the session, clear the sentinel with the **same** session id from step 3:

```
python3 scripts/team_sentinel.py clear --session <id>
```

After teardown the gate hooks return to no-ops. Never leave a session active.
