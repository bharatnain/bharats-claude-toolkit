// workflows/review-changes.workflow.js
//
// TEMPLATE — copy this file and parameterize it for your repo. Run via the
// Workflow tool. See workflows/README.md.
//
// Flow: enumerate review dimensions -> parallel find-findings (one finder per
// dimension) -> adversarial verify (a code-reviewer agent per finding tries to
// REFUTE it) -> synthesize a single review. Pure review: runGate is available
// but not required, so it is not invoked here.

import { runGate } from './lib/runner.js' // available for an optional gate; see note below

export const meta = {
  name: 'review-changes',
  description:
    'Adversarial review of the working diff. Fan out one finder per review dimension, then have a code-reviewer agent try to refute each finding before it survives, then synthesize a single verdict. Read-only — never edits code. runGate is available but a pure review does not require it.',
  phases: [
    { title: 'Dimensions', detail: 'enumerate the review dimensions for this diff' },
    { title: 'Find', detail: 'parallel: one finder per dimension surfaces candidate findings' },
    { title: 'Verify', detail: 'adversarial: a code-reviewer agent tries to refute each finding' },
    { title: 'Synthesize', detail: 'merge surviving findings into one review verdict' },
  ],
}

// ---- args (defensive: string | object | undefined) -------------------------
// { target: "..." }      free-text description of WHAT to review (e.g. "the auth
//                        refactor on this branch"). A bare string arg is treated
//                        as the target. Default: "the current working diff".
// { dimensions: [...] }  optional override of the review dimensions.
// { maxFindings: 12 }    optional cap on findings sent to the verify phase.
let A = args
if (typeof A === 'string') { A = A.trim() ? { target: A } : {} }
if (!A || typeof A !== 'object') A = {}

const TARGET = (typeof A.target === 'string' && A.target.trim()) ? A.target.trim() : 'the current working diff'
const DIMENSIONS = (Array.isArray(A.dimensions) && A.dimensions.length)
  ? A.dimensions
  : ['correctness', 'security', 'error-handling', 'tests', 'simplicity/surgical-diff', 'performance']
const MAX_FINDINGS = Number.isInteger(A.maxFindings) && A.maxFindings > 0 ? A.maxFindings : 12

log(`review-changes: target=${JSON.stringify(TARGET)} dimensions=[${DIMENSIONS.join(', ')}] maxFindings=${MAX_FINDINGS}`)

const FINDING_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['findings'],
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['title', 'severity', 'location', 'evidence'],
        properties: {
          title: { type: 'string' },
          severity: { type: 'string', enum: ['critical', 'major', 'minor'] },
          location: { type: 'string', description: 'file:line or function the issue lives at' },
          evidence: { type: 'string', description: 'the concrete code construct proving the issue' },
        },
      },
    },
  },
}

const VERDICT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['refuted', 'confidence', 'reason'],
  properties: {
    refuted: { type: 'boolean', description: 'true if the finding is a FALSE ALARM (code is actually fine)' },
    confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
    reason: { type: 'string', description: 'why the finding is real, or why it is a false alarm — cite the code you read' },
  },
}

// ---- Phase 1: dimensions (fixed list above; no agent needed) ---------------
phase('Dimensions')

// ---- Phase 2: parallel find — one finder per dimension ---------------------
phase('Find')
const finderResults = await parallel(DIMENSIONS.map((dim) => () =>
  agent(
    `You are reviewing ${TARGET} along ONE dimension: ${dim}. READ-ONLY — do not edit, stage, or switch branches.
Inspect the diff (\`git diff\`, \`git diff --staged\`, and untracked files as relevant). Surface only REAL, evidence-backed candidate findings for the ${dim} dimension — quote the exact construct and give file:line. Do not invent issues; an empty findings array is a valid answer for a clean dimension.`,
    { label: `find:${dim}`, phase: 'Find', schema: FINDING_SCHEMA, agentType: 'code-reviewer' },
  ).then((r) => ({ dim, findings: (r && r.findings) || [] })),
))

// Flatten + cap (severity-ranked) so the verify phase can't spawn an unbounded swarm.
const sevRank = { critical: 0, major: 1, minor: 2 }
const allFindings = finderResults
  .filter(Boolean)
  .flatMap((r) => r.findings.map((f) => ({ ...f, dim: r.dim })))
  .sort((a, b) => (sevRank[a.severity] ?? 9) - (sevRank[b.severity] ?? 9))
const toVerify = allFindings.slice(0, MAX_FINDINGS)
const overflow = allFindings.slice(MAX_FINDINGS)
log(`Find: ${allFindings.length} candidate finding(s); verifying ${toVerify.length}${overflow.length ? `, ${overflow.length} passed through unverified` : ''}`)

// ---- Phase 3: adversarial verify — a code-reviewer refutes each finding ----
phase('Verify')
const verdicts = toVerify.length
  ? await parallel(toVerify.map((f) => () =>
      agent(
        `Adversarially REFUTE this code-review finding about ${TARGET}. READ-ONLY.
Read the CURRENT code and any tests yourself. Try HARD to show the code is actually fine: the concern is already handled elsewhere, the input cannot reach the construct, or the finding misread the code. A finding SURVIVES only if you can independently re-confirm it from the current code. Default to refuted=true if you cannot confirm it.

FINDING [${f.dim}/${f.severity}] ${f.title}
  location: ${f.location}
  evidence: ${f.evidence}`,
        { label: `verify:${f.dim}`, phase: 'Verify', schema: VERDICT_SCHEMA, agentType: 'code-reviewer' },
      ).then((v) => ({ finding: f, verdict: v })),
    ))
  : []

// Surviving = not refuted. A null/missing verdict surfaces as unverified (fail-safe toward reporting).
const survived = [
  ...verdicts.filter((x) => !(x.verdict && x.verdict.refuted === true)).map((x) => ({
    ...x.finding,
    unverified: !x.verdict,
    reConfirm: x.verdict && x.verdict.reason,
  })),
  ...overflow.map((f) => ({ ...f, unverified: true, reConfirm: null })),
].sort((a, b) => (sevRank[a.severity] ?? 9) - (sevRank[b.severity] ?? 9))
const refutedCount = verdicts.filter((x) => x.verdict && x.verdict.refuted === true).length

// ---- Phase 4: synthesize ----------------------------------------------------
phase('Synthesize')
log(`Review complete: ${survived.length} surviving finding(s) (${survived.filter((f) => f.severity === 'critical').length} critical), ${refutedCount} false alarm(s) dropped`)

return {
  target: TARGET,
  dimensions: DIMENSIONS,
  findings: survived,
  refuted: refutedCount,
  verdict: survived.some((f) => f.severity === 'critical') ? 'changes-requested'
    : survived.length ? 'comment'
    : 'approve',
}
