// workflows/design-panel.workflow.js
//
// TEMPLATE — copy this file and parameterize it for your repo. Run via the
// Workflow tool. See workflows/README.md.
//
// Flow: run architect + code-architect + planner in PARALLEL on the same design
// problem, then synthesize their three perspectives into a single design. No
// gate stage (this is a design/exploration flow, nothing is built).

export const meta = {
  name: 'design-panel',
  description:
    'Convene a three-seat design panel — architect (system design), code-architect (codebase-grounded blueprint), planner (sequenced build plan) — on one design problem in parallel, then synthesize their perspectives into a single coherent design with the disagreements called out. Read-only — produces a design, builds nothing.',
  phases: [
    { title: 'Panel', detail: 'architect + code-architect + planner reason on the problem in parallel' },
    { title: 'Synthesize', detail: 'merge the three perspectives into one design, surfacing disagreements' },
  ],
}

// ---- args (defensive: string | object | undefined) -------------------------
// { target: "..." }       the design problem / feature to design. A bare string
//                         arg is the target. Default: a placeholder prompting
//                         the caller to supply one.
// { constraints: "..." }  optional free-text constraints (budget, deadline,
//                         stack limits) fed to every panelist.
let A = args
if (typeof A === 'string') { A = A.trim() ? { target: A } : {} }
if (!A || typeof A !== 'object') A = {}

const TARGET = (typeof A.target === 'string' && A.target.trim()) ? A.target.trim() : '(no design problem supplied — set args.target)'
const CONSTRAINTS = (typeof A.constraints === 'string' && A.constraints.trim()) ? A.constraints.trim() : ''

log(`design-panel: target=${JSON.stringify(TARGET)}${CONSTRAINTS ? ` constraints=${JSON.stringify(CONSTRAINTS)}` : ''}`)

const PERSPECTIVE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['recommendation', 'rationale', 'risks'],
  properties: {
    recommendation: { type: 'string', description: 'this seat\'s recommended approach' },
    rationale: { type: 'string', description: 'why, grounded in this seat\'s lens' },
    risks: { type: 'array', items: { type: 'string' }, description: 'risks/tradeoffs this seat sees' },
  },
}

const constraintLine = CONSTRAINTS ? `\nCONSTRAINTS: ${CONSTRAINTS}` : ''

// ---- Phase 1: parallel panel ------------------------------------------------
phase('Panel')
const seats = [
  {
    label: 'architect',
    agentType: 'architect',
    brief: `You are the SYSTEM ARCHITECT seat. Design the high-level system: components, boundaries, data flow, scalability and failure modes. Focus on the architecture, not the line-level code.`,
  },
  {
    label: 'code-architect',
    agentType: 'code-architect',
    brief: `You are the CODE ARCHITECT seat. Ground the design in THIS codebase's existing patterns and conventions. Give a concrete implementation blueprint: which files/modules change, the interfaces, and a build order.`,
  },
  {
    label: 'planner',
    agentType: 'planner',
    brief: `You are the PLANNER seat. Turn the design into a sequenced, dependency-ordered plan with verifiable milestones and the risks that could derail delivery.`,
  },
]

const panel = await parallel(seats.map((seat) => () =>
  agent(
    `${seat.brief}

DESIGN PROBLEM: ${TARGET}${constraintLine}

Read whatever you need (READ-ONLY — design only, build nothing). Return your recommendation, rationale, and risks from your seat's lens.`,
    { label: seat.label, phase: 'Panel', schema: PERSPECTIVE_SCHEMA, agentType: seat.agentType },
  ).then((r) => ({ seat: seat.label, perspective: r })),
))

const perspectives = panel.filter(Boolean)
log(`Panel: ${perspectives.length}/${seats.length} seat(s) reported`)

// ---- Phase 2: synthesize ----------------------------------------------------
phase('Synthesize')
const DESIGN_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['design', 'disagreements', 'openQuestions'],
  properties: {
    design: { type: 'string', description: 'the single synthesized design the panel converges on' },
    disagreements: { type: 'array', items: { type: 'string' }, description: 'points where the seats disagreed and how it was resolved' },
    openQuestions: { type: 'array', items: { type: 'string' }, description: 'questions the panel could not settle' },
  },
}

const brief = perspectives.map((p) =>
  `### ${p.seat}\nRecommendation: ${p.perspective && p.perspective.recommendation}\nRationale: ${p.perspective && p.perspective.rationale}\nRisks: ${((p.perspective && p.perspective.risks) || []).join('; ')}`,
).join('\n\n')

const synthesis = await agent(
  `Synthesize the three design-panel perspectives below into ONE coherent design for the problem. Reconcile their recommendations, explicitly call out where they disagreed and how you resolved it, and list any open questions. Do not just concatenate — converge.

DESIGN PROBLEM: ${TARGET}${constraintLine}

PANEL PERSPECTIVES:
${brief}`,
  { label: 'synthesize', phase: 'Synthesize', schema: DESIGN_SCHEMA, agentType: 'architect' },
)

log(`Synthesize: ${((synthesis && synthesis.disagreements) || []).length} disagreement(s), ${((synthesis && synthesis.openQuestions) || []).length} open question(s)`)

return {
  target: TARGET,
  constraints: CONSTRAINTS || null,
  perspectives,
  design: (synthesis && synthesis.design) || '',
  disagreements: (synthesis && synthesis.disagreements) || [],
  openQuestions: (synthesis && synthesis.openQuestions) || [],
}
