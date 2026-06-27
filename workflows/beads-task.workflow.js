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
// Two load-bearing constraints (do not "simplify" away):
//   * pipeline()'s reduce stage is SYNCHRONOUS — it runs runGate() but CANNOT
//     await agent(). So the close-when-green step is a SEQUENTIAL pass AFTER the
//     pipeline, never inside reduce.
//   * runGate is FAIL-OPEN: a gate-internal error returns { ok:true, verdict:'error' }.
//     "Green" therefore means verdict === 'pass', NOT merely gate.ok — closing on
//     ok alone would close issues on a broken gate.

import { runGate, loadProfileName } from './lib/runner.js'
import * as BD from './lib/beads.js'

export const meta = {
  name: 'beads-task',
  description:
    'Beads-backed task workflow with cross-session memory: decompose a goal into ' +
    'acceptance-criteria-bearing beads issues under an epic (or resume a prior epic via ' +
    'args.epicId), query the blocker-aware ready queue, then per issue claim -> implement -> ' +
    'quality-gate -> close only when the gate verdict is pass. Closed issues are skipped on ' +
    'resume (the memory); degrades to native Task tools when bd is absent. Orthogonal to the ' +
    "Workflow tool's within-run runId resume.",
  phases: [
    { title: 'Detect', detail: 'detect beads vs native-Task backend (once)' },
    { title: 'Plan', detail: 'decompose the goal into acceptance-criteria issues (new epic only)' },
    { title: 'Ready', detail: 'bd ready — the blocker-aware workable queue for this epic' },
    { title: 'Execute', detail: 'per issue: claim -> work -> runGate -> close-when-green' },
    { title: 'Report', detail: 'roll up task ids + statuses; echo epicId for the next run' },
  ],
}

// ---- args (defensive: string | object | undefined) ------------------------
//   { goal: "..." }    objective to decompose (a bare string is treated as goal).
//   { epicId: "..." }  LINK KEY for cross-session memory — RESUME that epic.
//   { profile: "..." } maturity profile (gate + maturity target in descriptions).
//   { checks: [...] }  optional gate check subset (lint/typecheck/test/build).
//   { maxStages: N }   cap on issues executed this run (default 25).
let A = args
if (typeof A === 'string') { A = A.trim() ? { goal: A } : {} }
if (!A || typeof A !== 'object') A = {}

const GOAL = (typeof A.goal === 'string' && A.goal.trim()) ? A.goal.trim() : '(no goal — set args.goal)'
const EPIC_IN = (typeof A.epicId === 'string' && A.epicId.trim()) ? A.epicId.trim() : null
const PROFILE = (typeof A.profile === 'string' && A.profile.trim()) ? A.profile.trim() : loadProfileName()
const CHECKS = Array.isArray(A.checks) && A.checks.length ? A.checks : null
const MAX_STAGES = Number.isInteger(A.maxStages) && A.maxStages > 0 ? A.maxStages : 25

log(`beads-task: goal=${JSON.stringify(GOAL)} epicId=${EPIC_IN || '(new)'} profile=${PROFILE} maxStages=${MAX_STAGES}`)

const WORK_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['summary'],
  properties: {
    summary: { type: 'string' },
    changedFiles: { type: 'array', items: { type: 'string' } },
  },
}

// ---- Phase 1: detect backend (once) ---------------------------------------
phase('Detect')
const d = BD.detect()
const det = await agent(d.prompt, { schema: d.schema, label: 'bd:detect', phase: 'Detect', agentType: 'tech-lead' })
const backend = (det && det.backend === 'native') ? 'native' : 'beads'
log(`Backend: ${backend}`)

// ---- Phase 2: plan (new epic) or adopt the resumed epic id ----------------
let epicId = EPIC_IN
if (!EPIC_IN) {
  phase('Plan')
  const c = BD.createTasks({ goal: GOAL, profile: PROFILE })
  const created = await agent(c.prompt, { schema: c.schema, label: 'bd:create', phase: 'Plan', agentType: 'tech-lead' })
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
const q = BD.readyForEpic({ epicId })
const rq = await agent(q.prompt, { schema: q.schema, label: 'bd:ready', phase: 'Ready', agentType: 'tech-lead' })
const ready = (rq && Array.isArray(rq.ready)) ? rq.ready : []
const alreadyClosed = (rq && Array.isArray(rq.closed)) ? rq.closed.length : 0
log(`Ready: ${ready.length} workable now, ${alreadyClosed} already-closed (skipped = memory)`)

const stages = ready.slice(0, MAX_STAGES)
if (stages.length < ready.length) {
  log(`NOTE: capping at maxStages=${MAX_STAGES}; ${ready.length - stages.length} ready task(s) deferred — resume with args.epicId=${epicId}.`)
}

// ---- Phase 4: execute. claim+work+gate in a pipeline; close-when-green after.
phase('Execute')
const gated = await pipeline(
  stages,
  // stage 1 (map): claim, then do the work.
  (issue) => {
    const ac = Array.isArray(issue.acceptanceCriteria) ? issue.acceptanceCriteria : []
    const workPrompt =
      `${BD.claim({ id: issue.id }).prompt}\n\n` +
      'Then implement this task as a SURGICAL change that makes ALL of these acceptance criteria true:\n' +
      `${ac.map((a) => `  - ${a}`).join('\n') || '  (none specified)'}\n\n` +
      `GOAL CONTEXT: ${GOAL}\nReturn a short summary and the files you changed.`
    return agent(workPrompt, { label: `work:${issue.id}`, phase: 'Execute', schema: WORK_SCHEMA, agentType: 'general-purpose' })
  },
  // stage 2 (reduce, SYNC): gate this issue's scope. reduce CANNOT await agent(),
  // so the close call happens in the sequential pass below (see header constraint).
  (work, issue) => {
    const gate = runGate({ profile: PROFILE, checks: CHECKS })
    log(`Gate ${issue.id}: verdict=${gate.verdict} ok=${gate.ok} blocking=${gate.blocking_failures.length}`)
    return { issue, work, gate }
  },
)

// Close-when-green pass — SEQUENTIAL, after the pipeline. Green === verdict 'pass'
// (NOT gate.ok — runGate is fail-open and returns ok:true on a gate error).
const closed = []
for (const r of gated.filter(Boolean)) {
  if (r.gate.verdict !== 'pass') {
    closed.push({ id: r.issue.id, closed: false, reason: `gate not green (verdict=${r.gate.verdict})`, verdict: r.gate.verdict })
    log(`Leave open ${r.issue.id}: gate verdict=${r.gate.verdict}`)
    continue
  }
  const cl = BD.closeWhenGreen({ id: r.issue.id, gate: r.gate, acceptanceCriteria: r.issue.acceptanceCriteria })
  const res = await agent(cl.prompt, { schema: cl.schema, label: `bd:close:${r.issue.id}`, phase: 'Execute', agentType: 'tech-lead' })
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
