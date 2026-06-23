# Roster matrix

Maps each maturity profile to its required + optional role agents and its worktree
isolation. These values mirror `team-profiles/*.json` — the **sentinel-resolved profile is
the runtime source of truth** (isolation is driven entirely by the profile's
`isolation.worktree` flag). This table is documentation, not a second place to edit.

| Profile | Required roles | Optional roles | Worktree isolation |
|---|---|---|---|
| `greenfield` | `tech-lead` | `code-reviewer`, `test-engineer` | no (`worktree: false`) |
| `active` | `tech-lead`, `code-reviewer` | `integrator`, `test-engineer` | no (`worktree: false`) |
| `legacy` | `tech-lead`, `code-reviewer`, `integrator`, `test-engineer` | — | yes (`worktree: true`) |

## How to use this

1. After step 1 of the loop, read the detected profile's `roles.required`.
2. Staff exactly those roles from `agents/` (e.g. `agents/tech-lead.md`,
   `agents/code-reviewer.md`, `agents/integrator.md`, `agents/test-engineer.md`).
3. Optional roles are staffed only when the work warrants them (e.g. add a
   `test-engineer` on `greenfield` when a task needs tests).
4. Spawn teammates in isolated git worktrees **only** when the profile's
   `isolation.worktree` is `true` (legacy). Greenfield and active work directly on the
   integration branch.

## Notes

- `tech-lead` is always required and is the orchestrator running this skill — it works on
  the integration branch, never gets its own worktree, and reads other worktrees read-only.
- If a required role cannot be staffed, surface the gap rather than silently dropping it.
- If you ever find this table disagreeing with `team-profiles/*.json`, the JSON (as resolved
  by the sentinel) wins — fix the table.
