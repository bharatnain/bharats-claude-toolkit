// workflows/implement-task-with-gates.workflow.js
//
// TEMPLATE (FLAGSHIP) — copy this file and parameterize it for your repo. Run
// via the Workflow tool. See workflows/README.md.
//
// Flow: plan -> implement -> runGate -> a BOUNDED Critic fix-loop that iterates
// ONLY on blocking_failures and stops at a profile-driven max-iterations cap ->
// integrate. The loop ALWAYS terminates: the cap is read from the maturity
// profile (greenfield:1, active:2, legacy:3) and clamped to a hard ceiling even
// if the profile name is malformed.

import { runGate, loadProfileName } from './lib/runner.js'

export const meta = {
  name: 'implement-task-with-gates',
  description:
    'Plan -> implement -> quality-gate -> bounded Critic fix-loop on blocking failures -> integrate. The fix-loop iterates only on the gate\'s blocking_failures and is capped by the team maturity profile (more passes on legacy, fewer on greenfield) with a hard ceiling, so it is guaranteed to terminate.',
  phases: [
    { title: 'Plan', detail: 'turn the task into an implementation plan with verifiable success criteria' },
    { title: 'Implement', detail: 'apply the plan as a surgical change' },
    { title: 'Gate', detail: 'runGate over the change; derive blocking_failures' },
    { title: 'Fix-loop', detail: 'bounded Critic loop: fix ONLY blocking_failures, re-gate, stop at the cap' },
    { title: 'Integrate', detail: 'land the change once the gate is green (or the cap is hit)' },
  ],
}

// ---- args (defensive: string | object | undefined) -------------------------
// { task: "..." }      free-text task description. A bare string arg is the task.
// { profile: "..." }   optional profile NAME ('legacy') or path; overrides the
//                      resolved active profile for BOTH the gate and the loop cap.
// { checks: [...] }    optional subset of {lint,typecheck,test,build} for the gate.
let A = args
if (typeof A === 'string') { A = A.trim() ? { task: A } : {} }
if (!A || typeof A !== 'object') A = {}

const TASK = (typeof A.task === 'string' && A.task.trim()) ? A.task.trim() : '(no task supplied — describe the change in args.task)'
const PROFILE = (typeof A.profile === 'string' && A.profile.trim()) ? A.profile.trim() : loadProfileName()
const CHECKS = Array.isArray(A.checks) && A.checks.length ? A.checks : null

// Loop cap by maturity, with a HARD safety ceiling so a malformed/unknown
// profile still terminates the workflow.
const CAP_BY_PROFILE = { greenfield: 1, active: 2, legacy: 3 }
const HARD_CEILING = 5
const MAX_FIX_ITERS = Math.min(CAP_BY_PROFILE[PROFILE] ?? 2, HARD_CEILING)

log(`implement-task-with-gates: task=${JSON.stringify(TASK)} profile=${PROFILE} maxFixIters=${MAX_FIX_ITERS} checks=${CHECKS ? CHECKS.join(',') : 'all'}`)

const PLAN_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['steps', 'successCriteria'],
  properties: {
    steps: { type: 'array', items: { type: 'string' }, description: 'ordered, surgical implementation steps' },
    successCriteria: { type: 'array', items: { type: 'string' }, description: 'verifiable checks that prove the task is done' },
  },
}

const DONE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['summary', 'changedFiles'],
  properties: {
    summary: { type: 'string' },
    changedFiles: { type: 'array', items: { type: 'string' } },
  },
}

// ---- Phase 1: plan ----------------------------------------------------------
phase('Plan')
const plan = await agent(
  `Plan the implementation of this task as a SURGICAL change (touch only what the task requires; match existing style). Produce ordered steps and a list of VERIFIABLE success criteria (the checks that will prove it is done).

TASK: ${TASK}`,
  { label: 'plan', phase: 'Plan', schema: PLAN_SCHEMA, agentType: 'planner' },
)
const steps = (plan && plan.steps) || []
const criteria = (plan && plan.successCriteria) || []
log(`Plan: ${steps.length} step(s), ${criteria.length} success criterion(ia)`)

// ---- Phase 2: implement -----------------------------------------------------
phase('Implement')
const impl = await agent(
  `Implement this task by applying the plan below as a SURGICAL change. Edit only files the task requires; do not refactor adjacent code. When done, report a one-line summary and the list of files you changed.

TASK: ${TASK}

PLAN:
${steps.map((s, i) => `  ${i + 1}. ${s}`).join('\n')}

SUCCESS CRITERIA (make these true):
${criteria.map((c) => `  - ${c}`).join('\n')}`,
  { label: 'implement', phase: 'Implement', schema: DONE_SCHEMA, agentType: 'general-purpose' },
)
log(`Implement: ${(impl && impl.summary) || '(no summary)'} — ${((impl && impl.changedFiles) || []).length} file(s)`)

// ---- Phase 3+4: gate + bounded Critic fix-loop ------------------------------
phase('Gate')
let gate = runGate({ profile: PROFILE, checks: CHECKS })
log(`Gate (initial): verdict=${gate.verdict} ok=${gate.ok} blocking_failures=${gate.blocking_failures.length}`)

phase('Fix-loop')
let iter = 0
// Loop ONLY while there are blocking failures AND we are under the cap. The
// `iter < MAX_FIX_ITERS` bound is what guarantees termination regardless of the
// gate's behavior.
while (!gate.ok && gate.blocking_failures.length && iter < MAX_FIX_ITERS) {
  iter += 1
  const failsList = gate.blocking_failures
    .map((c) => `  - [${c.name}] ${c.status}: ${(c.detail || '').split('\n')[0]}`)
    .join('\n')
  log(`Fix-loop pass ${iter}/${MAX_FIX_ITERS}: fixing ${gate.blocking_failures.length} blocking failure(s)`)

  await agent(
    `You are the Critic fix-loop. The quality gate is RED. Fix ONLY the blocking failures listed below — make the smallest change that turns each one green. Do NOT touch unrelated code, do NOT chase advisory/non-blocking warnings, do NOT widen scope. After fixing, the gate will be re-run automatically.

BLOCKING FAILURES (gate verdict=${gate.verdict}):
${failsList}`,
    { label: `fix:pass${iter}`, phase: 'Fix-loop', schema: DONE_SCHEMA, agentType: 'general-purpose' },
  )

  gate = runGate({ profile: PROFILE, checks: CHECKS })
  log(`Gate (after pass ${iter}): verdict=${gate.verdict} ok=${gate.ok} blocking_failures=${gate.blocking_failures.length}`)
}

const gateGreen = gate.ok && gate.blocking_failures.length === 0
if (!gateGreen) {
  log(`Fix-loop exhausted (${iter}/${MAX_FIX_ITERS} passes) with ${gate.blocking_failures.length} blocking failure(s) remaining — NOT integrating.`)
}

// ---- Phase 5: integrate (only on a green gate) ------------------------------
phase('Integrate')
let integration = null
if (gateGreen) {
  integration = await agent(
    `The quality gate is GREEN for this task. Integrate the change: ensure the working tree is coherent, the build is green, and the change is ready to land. Report what you did.

TASK: ${TASK}`,
    { label: 'integrate', phase: 'Integrate', schema: DONE_SCHEMA, agentType: 'integrator' },
  )
  log(`Integrate: ${(integration && integration.summary) || 'done'}`)
} else {
  log('Skipping integrate — gate is not green.')
}

return {
  task: TASK,
  profile: PROFILE,
  plan: { steps, successCriteria: criteria },
  implementation: impl,
  fixLoop: { passes: iter, cap: MAX_FIX_ITERS, exhausted: !gateGreen && iter >= MAX_FIX_ITERS },
  gate: { ok: gate.ok, verdict: gate.verdict, blocking_failures: gate.blocking_failures, checks: gate.checks },
  integrated: gateGreen,
  integration,
}
