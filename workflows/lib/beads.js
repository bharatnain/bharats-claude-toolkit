// workflows/lib/beads.js
//
// Dependency-free PROMPT + SCHEMA factory for beads (`bd`) operations driven from
// a SANDBOXED Workflow script. A workflow script cannot shell; it can only spawn
// agents via agent(prompt, {schema}). So this module never runs `bd` itself — it
// returns the STANDARDIZED prompt strings + JSON output schemas that a spawned
// agent uses to run `bd` (or the native-Task fallback) and report structured
// results back to the workflow.
//
// COMMAND VOCABULARY + the native-Task fallback are defined ONCE in
// skills/team-orchestration/references/beads-contract.md (verified for bd 1.0.4:
// `bd create` / `--acceptance` / `--deps` / `bd ready --exclude-type epic` /
// `bd update --claim` / `bd close --reason`). This module references that contract;
// it does not restate the full command list.
//
// No package.json, no deps, no node: imports — pure string/object construction,
// matching the pure-Node posture of ./runner.js.

// Link keys for cross-session memory: a run's issues hang off one epic, tagged
// with LABEL and a TITLE_PREFIX, so the epic is rediscoverable if its id is lost.
export const LABEL = 'beads-workflow'
export const TITLE_PREFIX = 'wf:'

// Shared preamble prepended to every beads prompt. Tells the agent to detect the
// backend and use the verified bd 1.0.4 surface, or the native Task fallback.
export function contractPreamble() {
  return [
    'You are performing a task-tracking operation for a workflow.',
    'BACKEND: if `command -v bd` succeeds, use beads (bd 1.0.4); otherwise use the',
    'native Task tools with the same discipline. Command source of truth:',
    'skills/team-orchestration/references/beads-contract.md.',
    'bd 1.0.4 surface — create:',
    `\`bd create "<title>" --type task --acceptance "<criteria>" [--parent <epic>] [--labels ${LABEL}] [--deps "<prereq-id>"] --json\``,
    '(a bare --deps id means THIS task is BLOCKED BY that id); ready:',
    `\`bd ready [--parent <epic>] [--label ${LABEL}] --exclude-type epic --json\``,
    '(bd ready has NO --type flag); claim: `bd update <id> --claim`; close:',
    '`bd close <id> --reason "<why>"` (close FAILS if blocked by open issues — report it, do NOT --force).',
    'Return ONLY the JSON described by the schema — no prose.',
  ].join(' ')
}

// detect() — which backend is live. Returns { backend: 'beads' | 'native' }.
export function detect() {
  return {
    prompt: contractPreamble() +
      '\n\nOPERATION: detect the task backend. Run `command -v bd`. ' +
      'Return {"backend":"beads"} if bd is on PATH, else {"backend":"native"}.',
    schema: {
      type: 'object', additionalProperties: false, required: ['backend'],
      properties: { backend: { type: 'string', enum: ['beads', 'native'] } },
    },
  }
}

// createTasks() — decompose a goal into acceptance-criteria-bearing issues under
// one epic. acceptanceCriteria is REQUIRED (minItems 1) in both the schema and the
// prompt, mirroring the contract's "mandatory at create time".
export function createTasks({ goal, profile } = {}) {
  const g = String(goal == null ? '' : goal)
  return {
    prompt: contractPreamble() +
      '\n\nOPERATION: decompose this GOAL into the smallest independently verifiable tasks, ' +
      'each with explicit, checkable ACCEPTANCE CRITERIA (mandatory — a task without acceptance ' +
      `criteria is invalid) and the maturity target "${profile || 'active'}" in its --description.\n` +
      `GOAL: ${g}\n` +
      `First create the epic: \`bd create "${TITLE_PREFIX} ${g}" --type epic --labels ${LABEL} --json\` and capture its id as epicId.\n` +
      `For each task run \`bd create "<title>" --type task --parent <epicId> --labels ${LABEL} ` +
      '--acceptance "<criteria>" [--deps "<prereq task id>"] --json` and capture its id. Wire --deps so a ' +
      'task that depends on another is BLOCKED BY it. Return the epicId and the created tasks.',
    schema: {
      type: 'object', additionalProperties: false, required: ['epicId', 'tasks'],
      properties: {
        epicId: { type: 'string' },
        tasks: {
          type: 'array',
          items: {
            type: 'object', additionalProperties: false,
            required: ['id', 'title', 'acceptanceCriteria'],
            properties: {
              id: { type: 'string' },
              title: { type: 'string' },
              acceptanceCriteria: { type: 'array', minItems: 1, items: { type: 'string' } },
              dependsOn: { type: 'array', items: { type: 'string' } },
            },
          },
        },
      },
    },
  }
}

// readyForEpic() — the workable queue + open/closed partition for resume. Closed
// issues are the cross-session memory (skip them). Scope by epic id, else by label.
export function readyForEpic({ epicId } = {}) {
  const id = epicId ? String(epicId) : ''
  const scope = id ? `--parent ${id} ` : `--label ${LABEL} `
  return {
    prompt: contractPreamble() +
      `\n\nOPERATION: report the task queue for epic "${id || '(by label ' + LABEL + ')'}" so the workflow ` +
      `can RESUME. Run \`bd ready ${scope}--exclude-type epic --json\` for the workable set, and ` +
      `\`bd list --all ${scope}--exclude-type epic --json\` to partition the rest by status. Closed tasks ` +
      'are DONE — skip them (that is the cross-session memory). Return ready/open/closed arrays.',
    schema: {
      type: 'object', additionalProperties: false, required: ['ready', 'open', 'closed'],
      properties: {
        ready: { type: 'array', items: taskRef() },
        open: { type: 'array', items: taskRef() },
        closed: { type: 'array', items: taskRef() },
      },
    },
  }
}

// claim() — atomically take a task before working it.
export function claim({ id } = {}) {
  return {
    prompt: contractPreamble() +
      `\n\nOPERATION: claim task "${id}" before working it. Run \`bd update ${id} --claim\`. ` +
      `Return {"id":"${id}","status":"<new status>"}.`,
    schema: idStatusSchema(),
  }
}

// closeWhenGreen() — close ONLY when the gate is green (verdict === 'pass', NOT
// merely ok — runGate is fail-open and returns verdict:'error', ok:true on a gate
// error) AND every acceptance criterion is met. The template must ALSO guard the
// call site on gate.verdict === 'pass'; this prompt is defense in depth.
export function closeWhenGreen({ id, gate, acceptanceCriteria } = {}) {
  const verdict = (gate && gate.verdict) || 'unknown'
  const ok = !!(gate && gate.ok)
  const crit = (acceptanceCriteria || []).map((c) => `  - ${c}`).join('\n')
  return {
    prompt: contractPreamble() +
      `\n\nOPERATION: close task "${id}" ONLY if it is truly done.\n` +
      `Quality gate verdict: ${verdict} (ok=${ok}). The gate is GREEN only when verdict === "pass" ` +
      '(a verdict of "error" is the fail-open state and is NOT green).\n' +
      `Acceptance criteria (every one must be demonstrably met):\n${crit || '  (none provided)'}\n` +
      'RULE: if the gate is green AND every acceptance criterion is met, run ' +
      `\`bd close ${id} --reason "acceptance criteria met; gate pass"\` and report closed=true. ` +
      'If `bd close` exits non-zero (blocked by open issues), report closed=false with the blocker as the ' +
      'reason — do NOT use --force. If the gate is not green or any criterion is unmet, leave the task OPEN, ' +
      'report closed=false, and name the failing gate/criterion in reason.',
    schema: {
      type: 'object', additionalProperties: false, required: ['id', 'closed', 'reason'],
      properties: {
        id: { type: 'string' },
        closed: { type: 'boolean' },
        reason: { type: 'string' },
      },
    },
  }
}

// ---- shared schema fragments ----------------------------------------------
function taskRef() {
  return {
    type: 'object', additionalProperties: false, required: ['id', 'title'],
    properties: {
      id: { type: 'string' },
      title: { type: 'string' },
      acceptanceCriteria: { type: 'array', items: { type: 'string' } },
    },
  }
}

function idStatusSchema() {
  return {
    type: 'object', additionalProperties: false, required: ['id', 'status'],
    properties: { id: { type: 'string' }, status: { type: 'string' } },
  }
}
