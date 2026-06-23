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

## Beads contract

Each task is decomposed with explicit acceptance criteria and a maturity target before it is
persisted. The lifecycle:

| Step | Command | Purpose |
|---|---|---|
| Add | `bd add "<title>" --description "<acceptance criteria + maturity target>"` | Create the task. The acceptance criteria and maturity target live in the description so the task is workable cold. Capture dependencies with `--depends-on <id>` where they exist. |
| Ready | `bd ready` | Surface the set of tasks whose dependencies are satisfied — the workable queue to assign to teammates. |
| Update | `bd update <id> ...` (e.g. `--claim`, status/notes) | Record progress as a teammate picks up and advances a task. |
| Close | `bd close <id>` | Mark done — **only** once the task's acceptance criteria are met and the live gate is green for its scope. |

Acceptance criteria are mandatory at `add` time: a beads task created without them is not
ready to assign.

## Native Task tools fallback

When `bd` is absent, persist the same decomposition using the runtime's native **Task**
tools instead. The mapping is one-to-one:

| Beads step | Native equivalent |
|---|---|
| `bd add` | Create a task carrying the title, acceptance criteria, and maturity target. |
| `bd ready` | List tasks and select those whose dependencies are satisfied. |
| `bd update` | Update a task's status to in-progress / record progress as work advances. |
| `bd close` | Mark the task completed once acceptance criteria + the live gate verdict are satisfied. |

The contract is identical — only the persistence backend changes. Acceptance criteria and
maturity targets travel with the task either way, so teammates can act on a task without the
orchestrator's in-session context.
