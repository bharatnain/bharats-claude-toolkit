# Workflows

Runnable **templates** for the Workflow tool. Each `*.workflow.js` orchestrates a
multi-agent flow using the Workflow grammar primitives (`agent()`, `parallel()`,
`pipeline()`, `log()`, `phase()`), and the gate-bearing ones consult the quality gate
through a cheap `agent()` stage.

> **These files are TEMPLATES.** Copy a `.workflow.js` into your own workflow,
> rename `meta.name`, and parameterize the prompts / agent types / args for your
> repo. They are written to run as-is for a demo, but the intent is that you
> adapt them — they are starting points, not a fixed library.

There is **no `package.json`** here and there are **no dependencies**. The Workflow
runtime is plain JavaScript with **no module loading and no filesystem / Node.js APIs**:
no `import`, `require`, `process` or `node:*`, and `Date.now()`, `Math.random()` and an
argless `new Date()` throw. `export const meta = {...}` must be the **first statement**
and a pure literal (no variables, calls, concatenation or template strings). Anything that
must touch the shell (the quality gate, `bd`) is therefore an `agent()` stage with a JSON
`schema` (`model: 'haiku'`, `effort: 'low'`), and shared helpers are inlined into each
template. `scripts/validate_assets.py` (check `W3`) enforces these constraints.

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
| `review-changes.workflow.js` | Adversarial review of the working diff; findings are schema-bound (`file`, `line`, `summary`) and each refutation returns a structured `verdict` (`CONFIRMED`/`REFUTED`) | none | `target`, `dimensions[]`, `maxFindings` |
| `implement-task-with-gates.workflow.js` **(flagship)** | Plan → implement → gate → bounded Critic fix-loop → schema-bound review (`{verdict: PASS/FAIL, findings[]}`) → integrate only on `PASS` | **required** | `task`, `profile`, `checks[]` |
| `migrate-sweep.workflow.js` | Mechanical migration swept across sites, gated per site | **required (per site)** | `target`, `sites[]`, `profile`, `checks[]`, `maxSites` |
| `design-panel.workflow.js` | architect + code-architect + planner in parallel → synthesize | none | `target`, `constraints` |
| `beads-task.workflow.js` **(flagship)** | Beads-backed: decompose → ready → claim → gate → close-when-green, **resumable by epic id** (cross-session memory) | **required (per issue)** | `goal`, `epicId`, `profile`, `checks[]`, `maxStages` |

The templates use `agentType` strings that map to the existing `agents/`
definitions — `code-reviewer`, `architect`, `code-architect`, `planner`,
`integrator`, `tech-lead` — so the panel/review flows reuse the Phase-F1 role agents rather
than inventing new ones. Plugin agents resolve only by their namespaced name, so
the scripts write `bharats-claude-toolkit:code-reviewer`; if you copy a template
into a repo that defines these agents under `.claude/agents/`, drop the prefix.
(Implementation/transform steps use `general-purpose`.)

## Subagents vs workflow

Reach for **subagents** (the `/team` skill, `skills/team-orchestration/`) for focused
workers with file-partitioned scopes — a handful per wave. Reach for a **workflow** when
the job outgrows a handful of agents, when findings must be cross-checked against each
other (as `review-changes` does with its refute pass), or when a verdict must be
machine-checkable: pass a `schema` to the verifying `agent()` call and branch on the
returned field, never on prose. Keep `label` and `phase` on every `agent()` call so runs
are observable. Two knobs bound a workflow's size: the `workflowSizeGuideline` setting
(`small` <5 agents, `medium` <10 — the default, `large` <50, `unrestricted`) and
`CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` (default 16). Agent teams stay off.

## The quality-gate stage

The gate-bearing templates inline one `runGate({ profile, checks, scope, label, phase })`
helper (keep the copies identical). It spawns a `haiku` / `effort: 'low'` agent that runs

```
python3 scripts/quality_gate.py --format json [--checks <csv>] [--scope all] [--profile <path>]
```

from the repo root and returns raw facts through a JSON schema (`exitCode`, `parsed`,
`verdict`, `checks[]`, `maturity`). The verdict object is then **derived in script code**
so the semantics stay deterministic:

```js
const g = await runGate({ profile, checks })
// g => { ok, verdict, blocking_failures, checks, maturity, raw }
```

### Inputs (all optional)

- **`scope`** — pass `'all'` to add `--scope all`; otherwise the gate default (`changed`)
  applies. The gate computes the changed set from the repo itself, so no file list is passed.
- **`profile`** — a profile **NAME** (e.g. `'legacy'`, resolved to
  `<repo root>/team-profiles/<name>.json`) or an explicit **path**. If it does not resolve
  to an existing file, `--profile` is omitted. When **no profile is given**, `--profile` is
  omitted and `quality_gate.py` resolves its own (`$CLAUDE_TEAM_PROFILE`, then
  `.claude/team-profile.json`, then the built-in `active` defaults).
- **`checks`** — array of `lint` / `typecheck` / `test` / `build`, passed as `--checks <csv>`.
  Omitted means the gate runs all four.

### Return — `{ ok, verdict, blocking_failures, checks, maturity, raw }`

- **`ok`** — `true` iff the gate exit code is `0`.
- **`verdict`** — the report's `verdict`, or `'error'` on a gate-internal failure.
- **`blocking_failures`** — **derived in script**: checks where
  `blocking === true && status ∈ {fail, error}` (the same rule the team_gate hook uses).
- **`checks`** — the report's `checks` array (or `[]`).
- **`maturity`** — `maturity` of the profile file the gate used (`'active'` for the built-in);
  `implement-task-with-gates` reads its fix-loop cap from this.

### Exit-code → semantics

| Gate exit | Result |
| --- | --- |
| `0` | `{ ok: true,  verdict: 'pass' (or parsed), blocking_failures: [] }` |
| `1` | `{ ok: false, verdict: 'fail', blocking_failures: [...] }` |
| `2` (gate internal error) | **fail-open** → `{ ok: true, verdict: 'error', blocking_failures: [] }` |
| unparsable output | treated like exit 2 (**fail-open**) |
| the gate agent never returned (skipped or died) | **fail-closed** → `{ ok: false, verdict: 'not-run', blocking_failures: [] }` |

### Fail-open vs fail-closed (exit 2)

A gate **exit 2** means the gate itself hit an internal error (not "your code failed" —
"the gate broke"). The helper treats this as **FAIL-OPEN**: `ok: true, verdict: 'error'`,
matching the team_gate hook's *"never wedge the developer"* philosophy. For stricter CI
flip the constant in the inlined helper to fail-**closed**:

```js
const FAIL_OPEN_ON_ERROR = false
```

`beads-task` additionally requires `verdict === 'pass'` before closing an issue, so a gate
error never closes work even while fail-open.

> **Behaviour change vs the old `lib/runner.js`:** the profile is no longer resolved in JS.
> The old `loadProfileName()` also honoured `.claude/team-context.json`; the gate stage
> relies on `quality_gate.py`'s own resolution instead, so pass `args.profile` to pick one
> explicitly.

## Structured verdicts

Both verdict-bearing templates bind the reviewer's output with a `schema` and decide on
the structured field only:

- `implement-task-with-gates` — after the gate is green, a `code-reviewer` returns
  `{ verdict: 'PASS' | 'FAIL', findings: [{ file, line, summary }] }` against the plan's
  success criteria; the change is integrated only when `verdict === 'PASS'`. A missing or
  malformed verdict is treated as not-PASS.
- `review-changes` — each finder returns `findings[{ title, severity, file, line, summary }]`;
  each refuter returns `{ verdict: 'CONFIRMED' | 'REFUTED', confidence, reason }`, and only
  `REFUTED` drops a finding.

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
script is sandboxed (no shell), it can't run `bd` itself — each operation (detect, create,
ready, claim, close) is a `haiku` / `effort: 'low'` `agent()` stage whose prompt carries the
`bd` command contract and whose JSON `schema` returns the result (the native Task tools are
the fallback when `bd` is absent). The command vocabulary lives once in
[`skills/team-orchestration/references/beads-contract.md`](../skills/team-orchestration/references/beads-contract.md).

**The memory is an epic id.** The first run decomposes the goal into acceptance-criteria-bearing
issues under a `wf:`-prefixed **epic** (labelled `beads-workflow`) and returns its `epicId`. Pass
that `epicId` back as `args.epicId` on a later run: the workflow queries the blocker-aware
`bd ready` queue, **skips already-closed issues** (the memory), and picks up newly-unblocked
ones. This is orthogonal to the Workflow tool's own **within-run** `runId` resume — `runId`
resumes one interrupted execution; `epicId` resumes the *task set* days later in a fresh session.

An issue is **closed only when its acceptance criteria are met AND the gate verdict is `pass`**
(not merely `ok` — the gate stage is fail-open and returns `verdict:'error', ok:true` on a gate error).
The caller must persist `result.epicId` to resume; otherwise a re-run creates a duplicate epic.
