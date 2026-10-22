export const meta = {
  name: 'implement-task-with-gates',
  description: 'Plan -> implement -> quality-gate -> bounded Critic fix-loop on blocking failures -> structured review -> integrate. The fix-loop iterates only on the gate\'s blocking_failures and is capped by the team maturity profile (more passes on legacy, fewer on greenfield) with a hard ceiling, so it is guaranteed to terminate. The reviewer returns a schema-bound {verdict, findings} and the script integrates only on verdict === "PASS".',
  phases: [
    { title: 'Plan', detail: 'turn the task into an implementation plan with verifiable success criteria' },
    { title: 'Implement', detail: 'apply the plan as a surgical change' },
    { title: 'Gate', detail: 'run the quality gate over the change; derive blocking_failures' },
    { title: 'Fix-loop', detail: 'bounded Critic loop: fix ONLY blocking_failures, re-gate, stop at the cap' },
    { title: 'Review', detail: 'code-reviewer checks the change against the success criteria; schema-bound PASS/FAIL verdict' },
    { title: 'Integrate', detail: 'land the change once the gate is green AND the review verdict is PASS' },
  ],
}

// workflows/implement-task-with-gates.workflow.js
//
// TEMPLATE (FLAGSHIP) — copy this file and parameterize it for your repo. Run
// via the Workflow tool. See workflows/README.md.
//
// Flow: plan -> implement -> quality gate -> a BOUNDED Critic fix-loop that
// iterates ONLY on blocking_failures and stops at a profile-driven max-iterations
// cap -> structured review (code-reviewer returns {verdict, findings} via schema)
// -> integrate. The loop ALWAYS terminates: the cap is read from the maturity
// profile (greenfield:1, active:2, legacy:3) and clamped to a hard ceiling even
// if the profile name is malformed.
//
// The Workflow runtime has NO module loading and NO Node/filesystem APIs, so the
// quality gate is a cheap agent() stage (model haiku, effort low) with a JSON
// schema. See workflows/README.md.

// ---- args (defensive: string | object | undefined) -------------------------
// { task: "..." }      free-text task description. A bare string arg is the task.
// { profile: "..." }   optional profile NAME ('legacy') or path, passed to the gate
//                      as --profile. Omitted: the gate resolves its own profile.
// { checks: [...] }    optional subset of {lint,typecheck,test,build} for the gate.
let A = args
if (typeof A === 'string') { A = A.trim() ? { task: A } : {} }
if (!A || typeof A !== 'object') A = {}

const TASK = (typeof A.task === 'string' && A.task.trim()) ? A.task.trim() : '(no task supplied — describe the change in args.task)'
const PROFILE = (typeof A.profile === 'string' && A.profile.trim()) ? A.profile.trim() : null
const CHECKS = Array.isArray(A.checks) && A.checks.length ? A.checks : null

// Loop cap by maturity, with a HARD safety ceiling so a malformed/unknown
// profile still terminates the workflow. The maturity comes from the gate result
// (the profile quality_gate.py actually used), so the cap is computed after the
// first gate run.
const CAP_BY_PROFILE = { greenfield: 1, active: 2, legacy: 3 }
const HARD_CEILING = 5

log(`implement-task-with-gates: task=${JSON.stringify(TASK)} profile=${PROFILE || '(gate default)'} checks=${CHECKS ? CHECKS.join(',') : 'all'}`)

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

// Structured verdict for the review phase. The script branches on `verdict`,
// never on prose, so a reviewer that writes "looks fine but..." cannot slip a
// FAIL through as a PASS.
const REVIEW_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['verdict', 'findings'],
  properties: {
    verdict: { type: 'string', enum: ['PASS', 'FAIL'], description: 'PASS only if every success criterion is met and no finding affects correctness' },
    findings: {
      type: 'array',
      description: 'gaps only — omit praise and optional style remarks',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['file', 'line', 'summary'],
        properties: {
          file: { type: 'string' },
          line: { type: ['integer', 'null'], description: 'line number, or null when the gap is not line-anchored' },
          summary: { type: 'string' },
        },
      },
    },
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
// ---- Phase 1: plan ----------------------------------------------------------
phase('Plan')
const plan = await agent(
  `Plan the implementation of this task as a SURGICAL change (touch only what the task requires; match existing style). Produce ordered steps and a list of VERIFIABLE success criteria (the checks that will prove it is done).

TASK: ${TASK}`,
  { label: 'plan', phase: 'Plan', schema: PLAN_SCHEMA, agentType: 'bharats-claude-toolkit:planner' },
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
let gate = await runGate({ profile: PROFILE, checks: CHECKS, label: 'gate', phase: 'Gate' })
log(`Gate (initial): verdict=${gate.verdict} ok=${gate.ok} blocking_failures=${gate.blocking_failures.length} maturity=${gate.maturity}`)

const MAX_FIX_ITERS = Math.min(CAP_BY_PROFILE[gate.maturity] ?? 2, HARD_CEILING)
log(`Fix-loop cap: maxFixIters=${MAX_FIX_ITERS}`)

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

  gate = await runGate({ profile: PROFILE, checks: CHECKS, label: `gate:pass${iter}`, phase: 'Fix-loop' })
  log(`Gate (after pass ${iter}): verdict=${gate.verdict} ok=${gate.ok} blocking_failures=${gate.blocking_failures.length}`)
}

// NOTE: the gate is fail-open, so a gate-internal error (verdict 'error', ok true)
// counts as green here; a gate that never ran (verdict 'not-run') does not. Set
// FAIL_OPEN_ON_ERROR=false to block on errors too.
const gateGreen = gate.ok && gate.blocking_failures.length === 0
if (!gateGreen) {
  log(`Fix-loop exhausted (${iter}/${MAX_FIX_ITERS} passes) with ${gate.blocking_failures.length} blocking failure(s) remaining — NOT integrating.`)
}

// ---- Phase 5: structured review (only on a green gate) ----------------------
phase('Review')
let review = null
if (gateGreen) {
  review = await agent(
    `Review the working diff for this task against its success criteria. READ-ONLY: you may run the project's own checks (tests, linters, validators, quality gate) but must not edit, stage, or switch branches. Report GAPS ONLY — anything that breaks a success criterion, a correctness bug, or a change outside the task's scope. Return verdict "PASS" only when every criterion holds and no finding affects correctness; otherwise "FAIL" with line-anchored findings.

TASK: ${TASK}

SUCCESS CRITERIA:
${criteria.map((c) => `  - ${c}`).join('\n')}

CHANGED FILES (per implementer): ${((impl && impl.changedFiles) || []).join(', ') || '(unknown — inspect git diff)'}`,
    { label: 'review', phase: 'Review', schema: REVIEW_SCHEMA, agentType: 'bharats-claude-toolkit:code-reviewer' },
  )
  log(`Review: verdict=${(review && review.verdict) || 'none'} findings=${((review && review.findings) || []).length}`)
} else {
  log('Skipping review — gate is not green.')
}
// A missing/malformed verdict is NOT a pass: only the structured field decides.
const reviewPassed = !!(review && review.verdict === 'PASS')

// ---- Phase 6: integrate (only on a green gate AND a PASS verdict) -----------
phase('Integrate')
let integration = null
if (gateGreen && reviewPassed) {
  integration = await agent(
    `The quality gate is GREEN for this task. Integrate the change: ensure the working tree is coherent, the build is green, and the change is ready to land. Report what you did.

TASK: ${TASK}`,
    { label: 'integrate', phase: 'Integrate', schema: DONE_SCHEMA, agentType: 'bharats-claude-toolkit:integrator' },
  )
  log(`Integrate: ${(integration && integration.summary) || 'done'}`)
} else {
  log(gateGreen ? 'Skipping integrate — review verdict is not PASS.' : 'Skipping integrate — gate is not green.')
}

return {
  task: TASK,
  profile: PROFILE || gate.maturity,
  plan: { steps, successCriteria: criteria },
  implementation: impl,
  fixLoop: { passes: iter, cap: MAX_FIX_ITERS, exhausted: !gateGreen && iter >= MAX_FIX_ITERS },
  gate: { ok: gate.ok, verdict: gate.verdict, blocking_failures: gate.blocking_failures, checks: gate.checks },
  review,
  integrated: gateGreen && reviewPassed,
  integration,
}
