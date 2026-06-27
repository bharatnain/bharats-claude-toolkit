# Beads contract (with native-Task fallback)

Step 4 of the orchestration loop persists tasks. Beads (`bd`) is **optional**: detect it,
then branch. `bd` is not guaranteed on PATH (it is absent in this environment), so the skill
must check before using it and degrade gracefully when it's missing.

## Detect first

```bash
command -v bd >/dev/null 2>&1 && echo "beads" || echo "native"
```

- If `bd` is present → use the **beads contract** below.
- If `bd` is absent → use the **native Task tools fallback**.

Never assume `bd` exists.

## Beads contract (bd 1.0.4 command surface)

Each task is decomposed with explicit acceptance criteria and a maturity target before it is
persisted. The lifecycle — verified against **bd 1.0.4**; note the commands are
`create` / `--deps`, NOT the older `add` / `--depends-on`:

| Step | Command | Purpose |
|---|---|---|
| Create | `bd create "<title>" --type task --acceptance "<criteria>" [--parent <epic>] [--labels <label>] [--deps "<prereq-id>"] --json` | Create the task. Acceptance criteria go in the first-class `--acceptance` flag (JSON field `acceptance_criteria`); put the maturity target in `--description`. `--deps "<id>"` records that this task is **blocked by** `<id>` (the prerequisite), so it stays out of `bd ready` until that id closes. `--json` returns the new id. |
| Ready | `bd ready [--parent <epic>] [--label <label>] --exclude-type epic --json` | Surface the workable queue — open tasks whose blockers are all closed. `bd ready` has **no `--type` flag**; scope with `--parent` / `--label` and drop the epic with `--exclude-type epic`. Add `--claim` to atomically claim the first match. |
| Update | `bd update <id> --claim` (start) · `bd update <id> --status <s> --append-notes "<note>"` (progress) | `--claim` is idempotent (sets assignee=you, status=in_progress). Record progress as a teammate advances a task. |
| Close | `bd close <id> --reason "<why>"` | Mark done — **only** once the task's acceptance criteria are met and the live gate is green for its scope. Close **exits non-zero and refuses** if the issue is still blocked by open issues; do not `--force` — report the blocker instead. |
| List | `bd list --all [--parent <epic>] [--label <label>] --exclude-type epic --json` | Inspect the full set including closed — e.g. to partition open vs done when resuming. Like `ready`, scope by `--parent` / `--label`; `bd list` also has no `--type` flag. |

Acceptance criteria are mandatory at create time: a beads task created without `--acceptance`
is not ready to assign.

**`bd init` safety:** when a tool initializes beads in a repo, use
`bd init --quiet --non-interactive --skip-agents --skip-hooks`. A bare `bd init` writes
`CLAUDE.md` / `AGENTS.md` / `.claude/` and installs git hooks — which would clobber an existing
project. `bd init` does not gitignore `.beads/` itself, so add that line separately.

## Native Task tools fallback

When `bd` is absent, persist the same decomposition using the runtime's native **Task**
tools instead. The mapping is one-to-one:

| Beads step | Native equivalent |
|---|---|
| `bd create` | Create a task carrying the title, acceptance criteria, and maturity target. |
| `bd ready` | List tasks and select those whose dependencies are satisfied. |
| `bd update --claim` | Update a task's status to in-progress / record progress as work advances. |
| `bd close` | Mark the task completed once acceptance criteria + the live gate verdict are satisfied. |

The contract is identical — only the persistence backend changes. Acceptance criteria and
maturity targets travel with the task either way, so teammates can act on a task without the
orchestrator's in-session context.
