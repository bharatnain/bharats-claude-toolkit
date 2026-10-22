export const meta = {
  name: 'beads-task',
  description: 'Beads-backed task workflow with cross-session memory: decompose a goal into acceptance-criteria-bearing beads issues under an epic (or resume a prior epic via args.epicId), query the blocker-aware ready queue, then per issue claim -> implement -> quality-gate -> close only when the gate verdict is pass. Closed issues are skipped on resume (the memory); degrades to native Task tools when bd is absent. Orthogonal to the Workflow tool\'s within-run runId resume.',
  phases: [
    { title: 'Detect', detail: 'detect beads vs native-Task backend (once)' },
    { title: 'Plan', detail: 'decompose the goal into acceptance-criteria issues (new epic only)' },
    { title: 'Ready', detail: 'bd ready — the blocker-aware workable queue for this epic' },
    { title: 'Execute', detail: 'per issue: claim -> work -> quality gate -> close-when-green' },
    { title: 'Report', detail: 'roll up task ids + statuses; echo epicId for the next run' },
  ],
}

// workflows/beads-task.workflow.js
//
// TEMPLATE (FLAGSHIP) — beads-backed task workflow with CROSS-SESSION memory.
//
// Flow: detect backend -> (new) decompose the goal into acceptance-criteria-bearing
// beads issues under one epic, or (resume) reuse args.epicId -> query the
// blocker-aware READY queue -> per ready issue: claim -> work -> quality-gate ->
// close ONLY when the gate is green -> report. A later run with the same epicId
// skips closed issues and picks up newly-unblocked ones — that is the memory.
// Degrades to native Task tools when `bd` is absent (every prompt is backend-aware).
//
// This is a TEMPLATE: copy it, rename meta.name, and adapt the work prompt / agent
// types / args for your repo.
//
// The Workflow runtime has NO module loading and NO Node/filesystem APIs, so every
// shell-touching step (the quality gate, every `bd` command) is a cheap
// agent() stage (model haiku, effort low) with a JSON schema. See workflows/README.md.
//
// Load-bearing constraint (do not "simplify" away): the gate is FAIL-OPEN (see
// runGate below) — a gate-internal error returns { ok:true, verdict:'error' }.
// "Green" therefore means verdict === 'pass', NOT merely gate.ok — closing on ok
// alone would close issues on a broken gate.

// ---- args (defensive: string | object | undefined) ------------------------
//   { goal: "..." }    objective to decompose (a bare string is treated as goal).
//   { epicId: "..." }  LINK KEY for cross-session memory — RESUME that epic.
//   { profile: "..." } maturity profile NAME or path (gate --profile + maturity
//                      target in descriptions). Omitted: the gate resolves its own.
//   { checks: [...] }  optional gate check subset (lint/typecheck/test/build).
//   { maxStages: N }   cap on issues executed this run (default 25).
let A = args
if (typeof A === 'string') { A = A.trim() ? { goal: A } : {} }
if (!A || typeof A !== 'object') A = {}

const GOAL = (typeof A.goal === 'string' && A.goal.trim()) ? A.goal.trim() : '(no goal — set args.goal)'
const EPIC_IN = (typeof A.epicId === 'string' && A.epicId.trim()) ? A.epicId.trim() : null
const PROFILE = (typeof A.profile === 'string' && A.profile.trim()) ? A.profile.trim() : null
const CHECKS = Array.isArray(A.checks) && A.checks.length ? A.checks : null
const MAX_STAGES = Number.isInteger(A.maxStages) && A.maxStages > 0 ? A.maxStages : 25

log(`beads-task: goal=${JSON.stringify(GOAL)} epicId=${EPIC_IN || '(new)'} profile=${PROFILE || '(gate default)'} maxStages=${MAX_STAGES}`)

const WORK_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['summary'],
  properties: {
    summary: { type: 'string' },
    changedFiles: { type: 'array', items: { type: 'string' } },
  },
}

// ---- quality gate (inlined: Workflow scripts cannot import) -----------------
// An agent() stage shells scripts/quality_gate.py and returns raw facts (exit code
// + parsed report); the verdict is derived HERE so the semantics stay in code.
// quality_gate.py resolves the profile itself when --profile is omitted
// ($CLAUDE_TEAM_PROFILE, then .claude/team-profile.json, then built-in "active").
// Keep this block identical across the *.workflow.js files that use it.
//
// FAIL-OPEN: a gate-internal error (exit 2 or unparsable output) yields
// { ok: true, verdict: 'error' } so a broken gate never wedges the flow. A gate
// agent that never returned (skipped or died) yields { ok: false, verdict:
// 'not-run' }: no gate ran, so nothing may count as green. Flip FAIL_OPEN_ON_ERROR to false for fail-CLOSED CI. Callers that must not
// act on a broken gate test verdict === 'pass', not ok.
const FAIL_OPEN_ON_ERROR = true
const GATE_CHECKS = ['lint', 'typecheck', 'test', 'build']
const GATE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['exitCode', 'parsed', 'checks'],
  properties: {
    exitCode: { type: ['integer', 'null'], description: 'process exit code of quality_gate.py' },
    parsed: { type: 'boolean', description: 'true iff stdout was a valid JSON report' },
    verdict: { type: ['string', 'null'], description: "the report's verdict field" },
    maturity: { type: ['string', 'null'], description: "maturity of the profile the gate used ('active' for the built-in)" },
    raw: { type: 'string', description: 'first 500 chars of stdout/stderr, only when not parsed' },
    checks: {
      type: 'array',
      items: {
        type: 'object',
        required: ['name', 'status', 'blocking'],
        properties: {
          name: { type: 'string' },
          status: { type: 'string' },
          blocking: { type: 'boolean' },
          detail: { type: 'string' },
        },
      },
    },
  },
}

async function runGate({ profile, checks, scope, label, phase: ph } = {}) {
  const csv = Array.isArray(checks) ? checks.filter((c) => GATE_CHECKS.includes(c)).join(',') : ''
  const cmd = 'python3 scripts/quality_gate.py --format json' + (csv ? ` --checks ${csv}` : '') + (scope === 'all' ? ' --scope all' : '')
  const profileStep = profile
    ? `Profile: "${profile}". If it contains "/" or ends in ".json" treat it as a path (relative to the repo root), otherwise the path is team-profiles/${profile}.json. If that file exists append \`--profile <path>\` to the command; if not, omit --profile.`
    : 'No profile was requested: do NOT pass --profile (the gate resolves its own).'
  const r = await agent(
    `Run the repo's quality gate and report the result. Do NOT fix, edit, stage or retry anything.
1. cd "$(git rev-parse --show-toplevel)"
2. Run: ${cmd}
   ${profileStep}
   Capture stdout and the exit code (e.g. \`...; echo "exit=$?"\`).
3. Report: exitCode (the process exit code); parsed (true iff stdout is a valid JSON report); verdict (the report's "verdict"); checks (the report's "checks" array, each item's name/status/blocking/detail, detail truncated to 300 chars); maturity (if the report's "profile" is a path to an existing file, the "maturity" string in that JSON file, else "active"). If stdout was not valid JSON set parsed=false, checks=[] and raw to its first 500 chars.`,
    { label: label || 'gate', phase: ph, schema: GATE_SCHEMA, model: 'haiku', effort: 'low' },
  )
  const gateError = (raw) => ({ ok: FAIL_OPEN_ON_ERROR, verdict: 'error', blocking_failures: [], checks: [], maturity: 'active', raw: raw || '' })
  if (!r) return { ok: false, verdict: 'not-run', blocking_failures: [], checks: [], maturity: 'active', raw: '' }
  if (typeof r.exitCode !== 'number' || r.exitCode === 2 || !r.parsed) return gateError(r && r.raw)
  const gateChecks = Array.isArray(r.checks) ? r.checks : []
  return {
    ok: r.exitCode === 0,
    verdict: typeof r.verdict === 'string' ? r.verdict : (r.exitCode === 0 ? 'pass' : 'fail'),
    // derived here: checks where blocking === true && status in {fail, error}
    blocking_failures: gateChecks.filter((c) => c && c.blocking === true && (c.status === 'fail' || c.status === 'error')),
    checks: gateChecks,
    maturity: (typeof r.maturity === 'string' && r.maturity) ? r.maturity : 'active',
    raw: '',
  }
}
// ---- beads (`bd`) agent stages ----------------------------------------------
// COMMAND VOCABULARY + the native-Task fallback live ONCE in
// skills/team-orchestration/references/beads-contract.md (verified for bd 1.0.4).
// Link keys for cross-session memory: a run's issues hang off one epic, tagged
// with BD_LABEL and a BD_TITLE_PREFIX, so the epic is rediscoverable if its id is lost.
const BD_LABEL = 'beads-workflow'
const BD_TITLE_PREFIX = 'wf:'

// Shared preamble prepended to every bd prompt.
const BD_PREAMBLE = [
  'You are performing a task-tracking operation for a workflow.',
  'BACKEND: if `command -v bd` succeeds, use beads (bd 1.0.4); otherwise use the',
  'native Task tools with the same discipline. Command source of truth:',
  'skills/team-orchestration/references/beads-contract.md.',
  'bd 1.0.4 surface — create:',
  `\`bd create "<title>" --type task --acceptance "<criteria>" [--parent <epic>] [--labels ${BD_LABEL}] [--deps "<prereq-id>"] --json\``,
  '(a bare --deps id means THIS task is BLOCKED BY that id; ONE id per --deps flag — wire extra',
  'blockers afterwards with `bd dep add <task> <blocker>`); ready:',
  `\`bd ready [--parent <epic>] [--label ${BD_LABEL}] --exclude-type epic --json\``,
  '(bd ready has NO --type flag); claim: `bd update <id> --claim`; close:',
  '`bd close <id> --reason "<why>"` (close FAILS if blocked by open issues — report it, do NOT --force).',
  'Return ONLY the JSON described by the schema — no prose.',
].join(' ')

const BD_OPTS = { agentType: 'bharats-claude-toolkit:tech-lead', model: 'haiku', effort: 'low' }

const TASK_REF = {
  type: 'object', additionalProperties: false, required: ['id', 'title'],
  properties: {
    id: { type: 'string' },
    title: { type: 'string' },
    acceptanceCriteria: { type: 'array', items: { type: 'string' } },
  },
}

// Which backend is live: { backend: 'beads' | 'native' }.
function bdDetect() {
  return agent(
    `${BD_PREAMBLE}\n\nOPERATION: detect the task backend. Run \`command -v bd\`. Return {"backend":"beads"} if bd is on PATH, else {"backend":"native"}.`,
    {
      ...BD_OPTS, label: 'bd:detect', phase: 'Detect',
      schema: {
        type: 'object', additionalProperties: false, required: ['backend'],
        properties: { backend: { type: 'string', enum: ['beads', 'native'] } },
      },
    },
  )
}

// Decompose a goal into acceptance-criteria-bearing issues under one epic.
// acceptanceCriteria is REQUIRED (minItems 1) in both the schema and the prompt,
// mirroring the contract's "mandatory at create time".
function bdCreateTasks(goal, maturity) {
  return agent(
    `${BD_PREAMBLE}\n\nOPERATION: decompose this GOAL into the smallest independently verifiable tasks, ` +
    'each with explicit, checkable ACCEPTANCE CRITERIA (mandatory — a task without acceptance ' +
    `criteria is invalid) and the maturity target ${maturity} in its --description.\n` +
    `GOAL: ${goal}\n` +
    `First create the epic: \`bd create "${BD_TITLE_PREFIX} ${goal}" --type epic --labels ${BD_LABEL} --json\` and capture its id as epicId.\n` +
    `For each task run \`bd create "<title>" --type task --parent <epicId> --labels ${BD_LABEL} ` +
    '--acceptance "<criteria>" [--deps "<prereq task id>"] --json` and capture its id. Wire --deps so a ' +
    'task that depends on another is BLOCKED BY it. Return the epicId and the created tasks.',
    {
      ...BD_OPTS, label: 'bd:create', phase: 'Plan',
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
    },
  )
}

// The workable queue + open/closed partition for resume. Closed issues are the
// cross-session memory (skip them). Scoped by epic id.
function bdReady(epicId) {
  return agent(
    `${BD_PREAMBLE}\n\nOPERATION: report the task queue for epic "${epicId}" so the workflow ` +
    `can RESUME. Run \`bd ready --parent ${epicId} --exclude-type epic --json\` for the workable set, and ` +
    `\`bd list --all --parent ${epicId} --exclude-type epic --json\` to partition the rest by status. Closed tasks ` +
    'are DONE — skip them (that is the cross-session memory). Return ready/open/closed arrays.',
    {
      ...BD_OPTS, label: 'bd:ready', phase: 'Ready',
      schema: {
        type: 'object', additionalProperties: false, required: ['ready', 'open', 'closed'],
        properties: {
          ready: { type: 'array', items: TASK_REF },
          open: { type: 'array', items: TASK_REF },
          closed: { type: 'array', items: TASK_REF },
        },
      },
    },
  )
}

// Atomically take a task before working it. status 'claim-failed' => not claimed.
function bdClaim(id) {
  return agent(
    `${BD_PREAMBLE}\n\nOPERATION: claim task "${id}" before working it. Run \`bd update ${id} --claim\`. ` +
    `Return {"id":"${id}","status":"<new status>"}; if the command fails (e.g. already claimed) return status "claim-failed".`,
    {
      ...BD_OPTS, label: `bd:claim:${id}`, phase: 'Execute',
      schema: {
        type: 'object', additionalProperties: false, required: ['id', 'status'],
        properties: { id: { type: 'string' }, status: { type: 'string' } },
      },
    },
  )
}

// Close ONLY when the gate is green (verdict === 'pass', NOT merely ok — the gate
// is fail-open and returns verdict:'error', ok:true on a gate error) AND every
// acceptance criterion is met. The call site ALSO guards on verdict === 'pass';
// this prompt is defense in depth.
function bdCloseWhenGreen(id, gate, acceptanceCriteria) {
  const crit = (acceptanceCriteria || []).map((c) => `  - ${c}`).join('\n')
  return agent(
    `${BD_PREAMBLE}\n\nOPERATION: close task "${id}" ONLY if it is truly done.\n` +
    `Quality gate verdict: ${gate.verdict} (ok=${gate.ok}). The gate is GREEN only when verdict === "pass" ` +
    '(a verdict of "error" is the fail-open state and is NOT green).\n' +
    `Acceptance criteria (every one must be demonstrably met):\n${crit || '  (none provided)'}\n` +
    'RULE: if the gate is green AND every acceptance criterion is met, run ' +
    `\`bd close ${id} --reason "acceptance criteria met; gate pass"\` and report closed=true. ` +
    'If `bd close` exits non-zero (blocked by open issues), report closed=false with the blocker as the ' +
    'reason — do NOT use --force. If the gate is not green or any criterion is unmet, leave the task OPEN, ' +
    'report closed=false, and name the failing gate/criterion in reason.',
    {
      ...BD_OPTS, label: `bd:close:${id}`, phase: 'Execute',
      schema: {
        type: 'object', additionalProperties: false, required: ['id', 'closed', 'reason'],
        properties: { id: { type: 'string' }, closed: { type: 'boolean' }, reason: { type: 'string' } },
      },
    },
  )
}

// ---- Phase 1: detect backend (once) ---------------------------------------
phase('Detect')
const det = await bdDetect()
const backend = (det && det.backend === 'native') ? 'native' : 'beads'
log(`Backend: ${backend}`)

// ---- Phase 2: plan (new epic) or adopt the resumed epic id ----------------
let epicId = EPIC_IN
if (!EPIC_IN) {
  phase('Plan')
  const maturity = PROFILE
    ? `"${PROFILE}"`
    : '(the repo\'s current maturity: the "maturity" field of .claude/team-profile.json, or "active" if that file is absent)'
  const created = await bdCreateTasks(GOAL, maturity)
  epicId = (created && created.epicId) || null
  const n = (created && Array.isArray(created.tasks)) ? created.tasks.length : 0
  log(`Plan: epic=${epicId} created ${n} task(s)`)
}

if (!epicId) {
  log('No epic id resolved — nothing to execute.')
  return { goal: GOAL, epicId: null, backend, profile: PROFILE, resumed: !!EPIC_IN, stages: [], tasks: [], remaining: [], verdict: 'noop' }
}

// ---- Phase 3: blocker-aware ready queue -----------------------------------
phase('Ready')
const rq = await bdReady(epicId)
const ready = (rq && Array.isArray(rq.ready)) ? rq.ready : []
const alreadyClosed = (rq && Array.isArray(rq.closed)) ? rq.closed.length : 0
log(`Ready: ${ready.length} workable now, ${alreadyClosed} already-closed (skipped = memory)`)

const stages = ready.slice(0, MAX_STAGES)
if (stages.length < ready.length) {
  log(`NOTE: capping at maxStages=${MAX_STAGES}; ${ready.length - stages.length} ready task(s) deferred — resume with args.epicId=${epicId}.`)
}

// ---- Phase 4: execute. claim -> work -> gate per issue; close-when-green after.
phase('Execute')
const gated = await pipeline(
  stages,
  async (issue) => {
    const claim = await bdClaim(issue.id)
    if (!claim || claim.status === 'claim-failed') {
      log(`Skip ${issue.id}: claim failed`)
      return { issue, skipped: 'claim failed' }
    }
    const ac = Array.isArray(issue.acceptanceCriteria) ? issue.acceptanceCriteria : []
    const work = await agent(
      `Implement task ${issue.id} ("${issue.title}") as a SURGICAL change that makes ALL of these acceptance criteria true:\n` +
      `${ac.map((a) => `  - ${a}`).join('\n') || '  (none specified)'}\n\n` +
      `GOAL CONTEXT: ${GOAL}\nReturn a short summary and the files you changed.`,
      { label: `work:${issue.id}`, phase: 'Execute', schema: WORK_SCHEMA, agentType: 'general-purpose' },
    )
    const gate = await runGate({ profile: PROFILE, checks: CHECKS, label: `gate:${issue.id}`, phase: 'Execute' })
    log(`Gate ${issue.id}: verdict=${gate.verdict} ok=${gate.ok} blocking=${gate.blocking_failures.length}`)
    return { issue, work, gate }
  },
)

// Close-when-green pass — SEQUENTIAL, after the pipeline. Green === verdict 'pass'
// (NOT gate.ok — the gate is fail-open and returns ok:true on a gate error).
const closed = []
for (const r of gated.filter(Boolean)) {
  if (r.skipped) {
    closed.push({ id: r.issue.id, closed: false, reason: r.skipped, verdict: 'skipped' })
    continue
  }
  if (r.gate.verdict !== 'pass') {
    closed.push({ id: r.issue.id, closed: false, reason: `gate not green (verdict=${r.gate.verdict})`, verdict: r.gate.verdict })
    log(`Leave open ${r.issue.id}: gate verdict=${r.gate.verdict}`)
    continue
  }
  const res = await bdCloseWhenGreen(r.issue.id, r.gate, r.issue.acceptanceCriteria)
  closed.push({ id: r.issue.id, closed: !!(res && res.closed), reason: (res && res.reason) || '', verdict: r.gate.verdict })
}

// ---- Phase 5: report -------------------------------------------------------
phase('Report')
const done = closed.filter((c) => c.closed)
const remaining = closed.filter((c) => !c.closed).map((c) => c.id)
log(`beads-task done: epic=${epicId} ${done.length}/${closed.length} closed. Resume the rest with args.epicId=${epicId}.`)

return {
  goal: GOAL,
  epicId,                 // <- persist THIS to resume the epic next run (memory)
  backend,
  profile: PROFILE,
  resumed: !!EPIC_IN,
  stages: stages.map((s) => s.id),
  tasks: closed,          // [{ id, closed, reason, verdict }]
  remaining,
  verdict: closed.length && closed.every((c) => c.closed) ? 'all-closed' : 'partial',
}
