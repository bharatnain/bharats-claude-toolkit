# Agent-teams probe runbook

A one-time, post-build verification step for the experimental agent-teams event
hooks (`TaskCreated`, `TaskCompleted`, `TeammateIdle`).

## Why this probe exists

`hooks/team_gate.py` dispatches the three team events into
`branch_task_created`, `branch_task_completed`, and `branch_teammate_idle`. Those
branches read **specific fields** out of the event payload — most notably
`branch_task_created` reads `payload['task']`, then `task['acceptance_criteria']`
/ `task['acceptanceCriteria']`. **These field names were inferred from docs, not
observed from a live run.** Before trusting them in anger, you must capture the
real payloads once and confirm the shape matches. This runbook is that capture.

The hooks are safe to ship un-probed: they only fire under
`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, they are sentinel-gated (SOLO NO-OP
when no team session is active), and any runner/internal error **fails open**
(exit 0). The probe is about getting the field names right, not about safety.

## Steps

1. **Enable the experimental flag** (without it, the events never fire):
   ```bash
   export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
   ```
2. **Enable hook debug** so `team_gate.py` prints the stdin payload + the
   decision it would make, then exits 0 without acting:
   ```bash
   export GATE_HOOK_DEBUG=1
   ```
3. **Drive a small team through the lifecycle.** Start a team via `/team`
   (or spawn a single teammate), then:
   - create a task,
   - complete a task,
   - let a teammate go idle.
   This exercises `TaskCreated`, `TaskCompleted`, and `TeammateIdle` in turn.
4. **Read the real payloads.** Under `GATE_HOOK_DEBUG=1`, `team_gate.py` writes a
   `=== GATE_HOOK_DEBUG ===` block to stderr for each event, including the full
   stdin payload as pretty JSON. Capture the `TaskCreated`, `TaskCompleted`, and
   `TeammateIdle` payloads.
5. **Confirm the task-scope derivation matches the live fields.** Specifically
   verify, in the captured `TaskCreated` payload:
   - the task object lives at `payload['task']`, and
   - acceptance criteria live at `task['acceptance_criteria']` **or**
     `task['acceptanceCriteria']`.
   If the live payload nests the task elsewhere or names the criteria field
   differently, **edit those field names in `hooks/team_gate.py`**
   (`branch_task_created`) to match — that is the one place this probe expects you
   to adjust code.
6. **Turn enforcement on.** Once the field names are confirmed, unset debug so the
   branches actually act (block on missing acceptance criteria, reopen on gate
   failure, surface the next ready task on idle):
   ```bash
   unset GATE_HOOK_DEBUG
   ```

## Escape hatch

- Set `CLAUDE_TEAM_GATES=off` to disable the gates regardless of the sentinel.
- A runner error always **fails open** (the hook exits 0), so a broken gate can
  never wedge a session.
