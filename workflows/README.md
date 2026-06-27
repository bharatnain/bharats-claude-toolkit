# Workflows

Runnable **templates** for the Workflow tool. Each `*.workflow.js` orchestrates a
multi-agent flow using the Workflow grammar primitives (`agent()`, `parallel()`,
`pipeline()`, `log()`, `phase()`), and the gate-bearing ones call a shared,
dependency-free helper (`lib/runner.js`) to consult the quality gate.

> **These files are TEMPLATES.** Copy a `.workflow.js` into your own workflow,
> rename `meta.name`, and parameterize the prompts / agent types / args for your
> repo. They are written to run as-is for a demo, but the intent is that you
> adapt them — they are starting points, not a fixed library.

There is **no `package.json`** here and there are **no dependencies**. `lib/runner.js`
uses only `node:` builtins (`node:child_process`, `node:fs`, `node:path`) and never
touches the network; `lib/beads.js` is pure (no `node:` imports at all). The templates
import `./lib/runner.js`, and the beads-backed one also `./lib/beads.js`.

## How to invoke

Run a template through the **Workflow tool**, passing the file path and an `args`
payload. The grammar exposes `agent`, `parallel`, `pipeline`, `log`, `phase`, and
the `args` global to the script; each template `export`s
`const meta = { name, description, phases }` for discovery.

`args` is normalized **defensively** in every template — you can pass:

- a **plain string** (treated as the task/target),
- an **object** (`{ task, target, profile, checks, ... }`), or
- **nothing** (defaults are applied).

A template never throws on a bare or empty `args`; it `log()`s the normalized args
at the start so a run is debuggable.

| Template | Purpose | Gate stage | Key args |
| --- | --- | --- | --- |
| `review-changes.workflow.js` | Adversarial review of the working diff | optional (available, not invoked) | `target`, `dimensions[]`, `maxFindings` |
| `implement-task-with-gates.workflow.js` **(flagship)** | Plan → implement → gate → bounded Critic fix-loop → integrate | **required** | `task`, `profile`, `checks[]` |
| `migrate-sweep.workflow.js` | Mechanical migration swept across sites, gated per site | **required (per site)** | `target`, `sites[]`, `profile`, `checks[]`, `maxSites` |
| `design-panel.workflow.js` | architect + code-architect + planner in parallel → synthesize | none | `target`, `constraints` |
| `beads-task.workflow.js` **(flagship)** | Beads-backed: decompose → ready → claim → gate → close-when-green, **resumable by epic id** (cross-session memory) | **required (per issue)** | `goal`, `epicId`, `profile`, `checks[]`, `maxStages` |

The templates use `agentType` strings that map to the existing `agents/`
definitions — `code-reviewer`, `architect`, `code-architect`, `planner`,
`integrator` — so the panel/review flows reuse the Phase-F1 role agents rather
than inventing new ones. (Implementation/transform steps use `general-purpose`.)

## The `runGate` contract

`lib/runner.js` exports `runGate`, `repoRoot`, and `loadProfileName`.

```js
import { runGate } from './lib/runner.js'

const g = runGate({ changedFiles, profile, checks })
// g => { ok, verdict, blocking_failures, checks, raw }
```

`runGate` shells:

```
python3 <repoRoot>/scripts/quality_gate.py --format json [flags...]
```

and derives the flags from its inputs:

### Inputs (all optional)

- **`changedFiles`** — the gate computes the changed set from git itself, so a
  file list is *not* passed through. The only thing this argument selects is the
  **scope flag**: pass `'all'` (or `{ scope: 'all' }`) to add `--scope all` and
  gate the whole project; otherwise scope is left at the runner default
  (`changed`).
- **`profile`** — either a profile **NAME** (e.g. `'legacy'`), resolved to
  `<repoRoot>/team-profiles/<name>.json`, **or** an explicit **path** to a
  profile file. If a name does **not** resolve to an existing file, `--profile`
  is **omitted** and the gate falls back to its built-in `active` defaults.
- **`checks`** — an array or CSV string of `lint` / `typecheck` / `test` /
  `build`. Passed as `--checks <csv>`. Omitted ⇒ the gate runs all four.

### Return — `{ ok, verdict, blocking_failures, checks, raw }`

- **`ok`** — `true` iff the runner exit code is `0`.
- **`verdict`** — the parsed `report.verdict`, or `'error'` on a runner-exit-2 /
  parse failure.
- **`blocking_failures`** — **derived by the runner**, not read from the gate:
  the checks where `blocking === true && status ∈ {fail, error}`. `quality_gate.py`
  emits no such top-level field, so the runner computes it with the **same rule
  the team_gate hook uses** — this keeps the JS and Python contracts identical.
- **`checks`** — the parsed `report.checks` array (or `[]`).
- **`raw`** — the unparsed stdout.

### Exit-code → semantics (same mapping as the hook)

| Runner exit | Result |
| --- | --- |
| `0` | `{ ok: true,  verdict: 'pass' (or parsed), blocking_failures: [] }` |
| `1` | `{ ok: false, verdict: 'fail', blocking_failures: [...] }` |
| `2` (gate internal error) | **fail-open** → `{ ok: true, verdict: 'error', blocking_failures: [] }` |
| unparsable stdout | treated as a parse failure → **fail-open** (same as exit 2) |

### Fail-open vs fail-closed (exit 2)

A runner **exit 2** means the gate itself hit an internal error (not "your code
failed" — "the gate broke"). `runGate` treats this as **FAIL-OPEN**:
`ok: true, verdict: 'error'`. This matches the team_gate hook's *"never wedge the
developer"* philosophy — a broken gate should not silently block all work.

If you are copying these templates into **stricter CI** and want a gate error to
**block** (fail-closed), flip the single constant at the top of `lib/runner.js`:

```js
const FAIL_OPEN_ON_ERROR = false
```

That makes exit 2 / unparsable output return `ok: false`, so a gate-internal
error blocks the flow.

## Profile & resolver helpers

`repoRoot()` and `loadProfileName()` are thin **JS re-implementations** of
`team_sentinel.py`'s resolvers. They exist so the JS workflow layer does not have
to shell Python on every call. **`scripts/team_sentinel.py` remains the canonical
resolver** (it is what the team_gate hook and gate consult); the JS mirrors its
precedence exactly. If you change the Python precedence, mirror it here too.

- **`repoRoot(startDir?)`** — walks up from `startDir` (default `process.cwd()`)
  to the first directory containing a `.git` **entry (file *or* dir**, so
  worktrees and submodules resolve), falling back to `process.cwd()`.
- **`loadProfileName(root?)`** — returns the active profile **name** by
  preference order, matching `team_sentinel.resolve_profile` exactly:
  1. **team-context marker** — `<root>/.claude/team-context.json` → `.profile`,
     but only when its `.active` is `true`;
  2. **`$CLAUDE_TEAM_PROFILE`** — used **raw** (no basename, no `.json` strip);
  3. **team-profile marker** — `<root>/.claude/team-profile.json` → `.maturity`;
  4. **`'active'`** — the safe default.

Each source is read defensively; a malformed or inactive marker falls through
to the next.

## The Critic fix-loop (flagship)

`implement-task-with-gates.workflow.js` runs a **bounded** Critic fix-loop after
the gate. It iterates **only on `blocking_failures`** (never advisory warnings)
and stops at a cap read from the maturity profile:

| Profile | Fix-loop passes |
| --- | --- |
| `greenfield` | 1 |
| `active` | 2 |
| `legacy` | 3 |
| (unknown/malformed) | 2 (default) |

A **hard ceiling of 5** clamps the cap even if the profile is malformed, and the
loop's `iter < cap` bound guarantees it **always terminates**. The change is only
integrated when the gate is green; if the loop is exhausted with blocking
failures remaining, the workflow stops short of integrating and reports the
remaining failures.

## Beads-backed memory (`beads-task.workflow.js`)

`beads-task.workflow.js` makes a workflow's tasks **durable across sessions** by persisting
them to [beads](../README.md#agentic-project-management-beads) (`bd`). Because a Workflow
script is sandboxed (no shell), it can't run `bd` itself — `lib/beads.js` returns
**prompt + schema pairs** that the spawned `agent()` runs against the `bd` CLI (or the native
Task tools when `bd` is absent). The command vocabulary lives once in
[`skills/team-orchestration/references/beads-contract.md`](../skills/team-orchestration/references/beads-contract.md).

**The memory is an epic id.** The first run decomposes the goal into acceptance-criteria-bearing
issues under a `wf:`-prefixed **epic** (labelled `beads-workflow`) and returns its `epicId`. Pass
that `epicId` back as `args.epicId` on a later run: the workflow queries the blocker-aware
`bd ready` queue, **skips already-closed issues** (the memory), and picks up newly-unblocked
ones. This is orthogonal to the Workflow tool's own **within-run** `runId` resume — `runId`
resumes one interrupted execution; `epicId` resumes the *task set* days later in a fresh session.

An issue is **closed only when its acceptance criteria are met AND the gate verdict is `pass`**
(not merely `ok` — `runGate` is fail-open and returns `verdict:'error', ok:true` on a gate error).
The caller must persist `result.epicId` to resume; otherwise a re-run creates a duplicate epic.
