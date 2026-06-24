// workflows/ai-therapy-research.workflow.js
//
// Autonomous, lead-driven research program for the AI-therapy field. Runs end to end
// with NO human in the loop: a senior research lead makes every judgment call (scope,
// depth, conflicts, sufficiency, sign-off) and logs each one. Produces verified,
// evidence-labeled per-company dossiers plus a cross-company master report.
//
// Returns structured markdown — the calling main loop writes it to disk. The research
// agents are read-only, so file writing happens outside the workflow.
//
// Run via the Workflow tool. See workflows/design-panel.workflow.js for grammar.

export const meta = {
  name: 'ai-therapy-research',
  description:
    'Autonomous AI-therapy field research run, driven by a senior research lead that makes every decision in the user\'s place. Charter -> discover/ratify roster -> per-company parallel dimension research (tech/clinical/business/people) -> adversarial verify -> dossier -> cross-company synthesis -> lead sign-off with a bounded follow-up pass. Produces evidence-labeled dossiers and a master report. Read-only research; writes nothing itself.',
  phases: [
    { title: 'Charter', detail: 'lead sets success criteria, per-dimension bar, tier policy' },
    { title: 'Discover', detail: 'scout proposes roster + tiers; lead ratifies' },
    { title: 'Research', detail: 'per-company parallel dimension sweep (pipeline)' },
    { title: 'Verify', detail: 'adversarial fact-check, evidence labels, citations' },
    { title: 'Dossier', detail: 'synthesize each company into an evidence-labeled dossier' },
    { title: 'Synthesize', detail: 'cross-company report: tables, rankings, motivations matrix, exec summary' },
    { title: 'Signoff', detail: 'lead reviews vs charter, commissions bounded follow-up or signs off' },
  ],
}

// NOTE: the custom agent definitions in agents/*.md are not registered as runnable
// agent types in every session, so we run on the built-in 'general-purpose' agent
// (full tool access incl. WebSearch/WebFetch). Each agent() prompt already carries its
// role identity and evidence-labeling discipline, so specialization is preserved.
const AT = 'general-purpose'

// ---- args (defensive) -------------------------------------------------------
// { seedRoster: [{name, whatItIs, tier}], today: "YYYY-MM-DD", focus: "..." }
let A = args
if (typeof A === 'string') { A = A.trim() ? { focus: A } : {} }
if (!A || typeof A !== 'object') A = {}

const TODAY = (typeof A.today === 'string' && A.today.trim()) ? A.today.trim() : 'the current date'
const FOCUS = (typeof A.focus === 'string' && A.focus.trim())
  ? A.focus.trim()
  : 'Technology and mental-health deep dive: technologies used, AI/ML techniques, company journey, team and compensation, funding and AI investment, business drivers behind tech decisions, engineering difficulty sizing, and stated-vs-real motivations.'

const SEED = Array.isArray(A.seedRoster) && A.seedRoster.length ? A.seedRoster : [
  { name: 'Slingshot AI (Ash app)', whatItIs: 'Foundation-model-for-psychology startup; Ash is its consumer AI-therapy app', tier: 1 },
  { name: 'Spring Health', whatItIs: 'Enterprise mental-health benefits platform with AI care navigation/matching', tier: 1 },
  { name: 'Woebot Health', whatItIs: 'CBT chatbot for mental health', tier: 2 },
  { name: 'Wysa', whatItIs: 'AI mental-health chatbot + human coaching', tier: 2 },
  { name: 'Lyra Health', whatItIs: 'Enterprise mental-health benefits + AI', tier: 2 },
  { name: 'Limbic', whatItIs: 'Clinical AI for mental healthcare (NHS / triage)', tier: 2 },
  { name: 'Sonia', whatItIs: 'AI therapist app', tier: 2 },
  { name: 'Youper', whatItIs: 'AI emotional-health assistant', tier: 2 },
  { name: 'Talkspace', whatItIs: 'Teletherapy with AI features', tier: 3 },
  { name: 'Headspace (Ebb)', whatItIs: 'Meditation app with the Ebb AI companion', tier: 3 },
  { name: 'Earkick', whatItIs: 'AI mental-health companion', tier: 3 },
]

const DIMENSION_BAR = `Cover, per company and labeled by evidence type (sourced[url+date] / inference / speculation):
1 Overview & journey  2 Technology stack & architecture  3 AI/ML techniques & models
4 Clinical/therapeutic approach  5 Safety, regulation & evidence  6 Engineering difficulty (1-5)
7 Team & org  8 Compensation (data vs estimate)  9 Funding & AI investment
10 Business model & business drivers  11 Stated-vs-real motivations  12 Differentiation, risks & moat`

log(`ai-therapy-research: ${SEED.length} seed companies, as of ${TODAY}`)

// ---- schemas ----------------------------------------------------------------
const CLAIM = {
  type: 'object', additionalProperties: false,
  required: ['statement', 'label'],
  properties: {
    statement: { type: 'string' },
    label: { type: 'string', enum: ['sourced', 'inference', 'speculation', 'contested'] },
    source: { type: 'string', description: 'URL of the supporting source, or empty' },
    date: { type: 'string', description: 'date of the source/fact if freshness-sensitive, or empty' },
  },
}

const CHARTER_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['successCriteria', 'dimensionBar', 'tierPolicy', 'escalationRule', 'decisions'],
  properties: {
    successCriteria: { type: 'string' },
    dimensionBar: { type: 'string' },
    tierPolicy: { type: 'string' },
    escalationRule: { type: 'string' },
    decisions: { type: 'array', items: { type: 'string' } },
  },
}

const ROSTER_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['roster'],
  properties: {
    roster: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['name', 'whatItIs', 'tier', 'rationale'],
        properties: {
          name: { type: 'string' },
          whatItIs: { type: 'string' },
          tier: { type: 'number' },
          rationale: { type: 'string' },
          sources: { type: 'array', items: { type: 'string' } },
        },
      },
    },
  },
}

const RATIFY_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['roster', 'decisions'],
  properties: {
    roster: ROSTER_SCHEMA.properties.roster,
    decisions: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['decision', 'fork', 'rationale', 'confidence'],
        properties: {
          decision: { type: 'string' }, fork: { type: 'string' },
          rationale: { type: 'string' }, confidence: { type: 'string' },
          flagForUser: { type: 'boolean' },
        },
      },
    },
  },
}

const FINDINGS_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['dimension', 'summary', 'claims'],
  properties: {
    dimension: { type: 'string' },
    summary: { type: 'string' },
    claims: { type: 'array', items: CLAIM },
    openQuestions: { type: 'array', items: { type: 'string' } },
    difficultyRating: { type: 'number', description: '1-5 engineering difficulty (tech dimension only)' },
    difficultyRationale: { type: 'string' },
    statedMotivation: { type: 'string', description: 'business dimension only' },
    realMotivation: { type: 'string', description: 'business dimension only' },
    motivationConfidence: { type: 'string' },
  },
}

const VERIFY_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['verdicts', 'overallConfidence'],
  properties: {
    overallConfidence: { type: 'string', enum: ['high', 'medium', 'low'] },
    verdicts: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['claim', 'label', 'justification'],
        properties: {
          claim: { type: 'string' },
          label: { type: 'string', enum: ['sourced', 'inference', 'speculation', 'contested', 'unsupported'] },
          source: { type: 'string' }, date: { type: 'string' },
          justification: { type: 'string' },
        },
      },
    },
    flags: { type: 'array', items: { type: 'string' } },
  },
}

const DOSSIER_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['company', 'markdown', 'oneLineSummary'],
  properties: {
    company: { type: 'string' },
    oneLineSummary: { type: 'string' },
    markdown: { type: 'string', description: 'full per-company dossier in markdown, all 12 dimensions, evidence-labeled' },
    difficultyRating: { type: 'number' },
    totalRaised: { type: 'string' },
    confidence: { type: 'string' },
    sources: { type: 'array', items: { type: 'string' } },
  },
}

const REPORT_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['reportMarkdown'],
  properties: {
    reportMarkdown: { type: 'string', description: 'full master report markdown: exec summary, landscape, difficulty ranking, funding/comp table, stated-vs-real motivations matrix, common patterns' },
    sourcesMarkdown: { type: 'string', description: 'consolidated dated source list in markdown' },
  },
}

const SIGNOFF_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['signedOff', 'decisionsLog'],
  properties: {
    signedOff: { type: 'boolean' },
    acceptedGaps: { type: 'array', items: { type: 'string' } },
    followUpCompanies: { type: 'array', items: { type: 'string' }, description: 'companies with critical gaps needing one more pass (cap honored by orchestrator)' },
    decisionsLog: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['decision', 'fork', 'rationale', 'confidence'],
        properties: {
          decision: { type: 'string' }, fork: { type: 'string' },
          rationale: { type: 'string' }, confidence: { type: 'string' },
          flagForUser: { type: 'boolean' },
        },
      },
    },
  },
}

// ---- Phase 0: Charter -------------------------------------------------------
phase('Charter')
const charter = await agent(
  `You are the senior research lead for an autonomous research run. The user is asleep and will not be consulted. Set the CHARTER for a "super thorough" deep dive into the AI-therapy field.

FOCUS: ${FOCUS}
DEFAULT DIMENSION BAR (you may tighten it):
${DIMENSION_BAR}

Define: precise success criteria for a report the user can "trust deeply and that has true depth"; the per-dimension bar (what each dimension must contain to count as done); the tier policy (how much effort Tier 1 vs 2 vs 3 gets); and the escalation rule — what you will DO when evidence is thin, given that escalating to the user is NOT an option. List the key decisions you are making in this charter.`,
  { label: 'charter', phase: 'Charter', schema: CHARTER_SCHEMA, agentType: AT },
)
const BAR = (charter && charter.dimensionBar) || DIMENSION_BAR
log(`Charter set. ${(charter && charter.decisions || []).length} charter decision(s).`)

// ---- Phase 1: Discover + ratify --------------------------------------------
phase('Discover')
const seedList = SEED.map((s) => `- ${s.name} (${s.whatItIs}) [seed tier ${s.tier}]`).join('\n')
const discovered = await agent(
  `You are the discovery scout. Validate and EXPAND this seed roster of AI-therapy companies, disambiguating entities (note: Ash is Slingshot AI's product — same company). Add real players the seed missed (competitors, incumbents adding AI therapy, notable newcomers). Assign each a tier: 1 = anchor/full sweep, 2 = substantial, 3 = field scan. Give a rationale and seed source URLs for each. As of ${TODAY}.

SEED ROSTER:
${seedList}`,
  { label: 'discover', phase: 'Discover', schema: ROSTER_SCHEMA, agentType: AT },
)
const proposed = (discovered && discovered.roster) || SEED.map((s) => ({ ...s, rationale: 'seed' }))

const ratified = await agent(
  `You are the senior research lead. The discovery scout proposed this roster. RATIFY it: confirm, amend tiers, add/cut subjects as your judgment dictates — you have full authority and the user will not be consulted. Keep it focused enough to go deep on the anchors. Record each non-trivial call you make as a decision (decision / fork / rationale / confidence / flagForUser).

PROPOSED ROSTER:
${proposed.map((r) => `- ${r.name} (${r.whatItIs}) tier ${r.tier} — ${r.rationale}`).join('\n')}`,
  { label: 'ratify-roster', phase: 'Discover', schema: RATIFY_SCHEMA, agentType: AT },
)
const roster = (ratified && ratified.roster && ratified.roster.length) ? ratified.roster : proposed
const leadDecisions = (ratified && ratified.decisions) || []
log(`Roster ratified: ${roster.length} companies (${roster.filter((r) => r.tier === 1).length} Tier-1).`)

// ---- dimension briefs -------------------------------------------------------
const DIMS = [
  { key: 'tech', agentType: AT,
    brief: `Investigate dimensions 2 (technology stack & architecture), 3 (AI/ML techniques & models: foundation model vs own, fine-tuning/RLHF/RAG/guardrails/evals/proprietary data), and 6 (engineering difficulty). Give a 1-5 difficultyRating with difficultyRationale.` },
  { key: 'clinical', agentType: AT,
    brief: `Investigate dimensions 4 (therapeutic approach & modalities, how technique is encoded, human-in-the-loop) and 5 (safety, crisis handling, clinical evidence/trials, FDA & regulatory status with dates).` },
  { key: 'business', agentType: AT,
    brief: `Investigate dimensions 1 (journey), 9 (funding & AI investment, rounds/investors/valuation/dates), 10 (business model & the business drivers behind tech decisions), and 11 (stated-vs-real motivations). Fill statedMotivation, realMotivation, and motivationConfidence.` },
  { key: 'people', agentType: AT,
    brief: `Investigate dimensions 7 (founders, key technical/clinical hires, headcount & org shape) and 8 (compensation bands; label DATA vs ESTIMATE; use levels.fyi / H1B LCA / posted ranges / Glassdoor; role-level only).` },
]

function researchCompany(co) {
  const tier = co.tier || 3
  const ctx = `COMPANY: ${co.name}\nWHAT IT IS: ${co.whatItIs}\nAS OF: ${TODAY}\nDIMENSION BAR:\n${BAR}\n\nLabel every claim sourced(url+date)/inference/speculation. Do not invent precision. If a fact isn't found, say so.`
  if (tier >= 3) {
    // lighter combined pass for field-scan tier
    return parallel([
      () => agent(`You are a multi-disciplinary analyst doing a focused field-scan pass. ${DIMS[0].brief} ${DIMS[2].brief}\n\n${ctx}`,
        { label: `research:${co.name}:tech+biz`, phase: 'Research', schema: FINDINGS_SCHEMA, agentType: AT }),
      () => agent(`You are a multi-disciplinary analyst doing a focused field-scan pass. ${DIMS[1].brief} ${DIMS[3].brief}\n\n${ctx}`,
        { label: `research:${co.name}:clin+people`, phase: 'Research', schema: FINDINGS_SCHEMA, agentType: AT }),
    ]).then((r) => ({ company: co, tier, findings: r.filter(Boolean) }))
  }
  // full sweep for tier 1 & 2
  return parallel(DIMS.map((d) => () =>
    agent(`${d.brief}\n\n${ctx}`,
      { label: `research:${co.name}:${d.key}`, phase: 'Research', schema: FINDINGS_SCHEMA, agentType: d.agentType }),
  )).then((r) => ({ company: co, tier, findings: r.filter(Boolean) }))
}

function findingsToText(res) {
  return res.findings.map((f) =>
    `## ${f.dimension}\n${f.summary}\n${(f.claims || []).map((c) => `- [${c.label}] ${c.statement}${c.source ? ` (${c.source}${c.date ? `, ${c.date}` : ''})` : ''}`).join('\n')}` +
    (f.difficultyRating ? `\nDifficulty: ${f.difficultyRating}/5 — ${f.difficultyRationale || ''}` : '') +
    (f.statedMotivation ? `\nStated motivation: ${f.statedMotivation}\nReal motivation (${f.motivationConfidence || '?'}): ${f.realMotivation || ''}` : ''),
  ).join('\n\n')
}

// ---- Phases 2-4: research -> verify -> dossier (pipeline) -------------------
async function verifyStage(res) {
  const text = findingsToText(res)
  const verdict = await agent(
    `You are the adversarial fact-checker. Try to REFUTE the key claims below about ${res.company.name}. For each material claim return a verdict (claim / label / source+date / justification). Default to a weaker label when support is thin; mark unsupported claims. Flag stale figures, marketing laundered as fact, conflated entities, and regulatory overstatement.\n\nFINDINGS:\n${text}`,
    { label: `verify:${res.company.name}`, phase: 'Verify', schema: VERIFY_SCHEMA, agentType: AT },
  )
  return { ...res, text, verdict }
}

async function dossierStage(res) {
  const verdictText = res.verdict
    ? `VERIFIER OVERALL CONFIDENCE: ${res.verdict.overallConfidence}\nVERDICTS:\n${(res.verdict.verdicts || []).map((v) => `- [${v.label}] ${v.claim}${v.source ? ` (${v.source}${v.date ? `, ${v.date}` : ''})` : ''} — ${v.justification}`).join('\n')}\nFLAGS: ${(res.verdict.flags || []).join('; ')}`
    : 'No verifier pass available.'
  const dossier = await agent(
    `You are the lead editor. Write the full per-company DOSSIER for ${res.company.name} in markdown, covering all 12 dimensions. Carry the verifier's labels through — sourced/inference/speculation/contested/unsupported. Where a fact wasn't found, write "unknown — not found". Include a "Stated vs. real motivations" subsection and an "Engineering difficulty (X/5)" subsection. End with a "Sources" list of URLs used.

RAW FINDINGS:\n${res.text}\n\n${verdictText}`,
    { label: `dossier:${res.company.name}`, phase: 'Dossier', schema: DOSSIER_SCHEMA, agentType: AT },
  )
  return dossier
}

const dossiers = (await pipeline(roster, researchCompany, verifyStage, dossierStage)).filter(Boolean)
log(`Dossiers built: ${dossiers.length}/${roster.length}.`)

// ---- Phase 5: cross-company synthesis --------------------------------------
phase('Synthesize')
const dossierDigest = dossiers.map((d) =>
  `### ${d.company}\nSummary: ${d.oneLineSummary}\nDifficulty: ${d.difficultyRating || '?'}/5 | Raised: ${d.totalRaised || '?'} | Confidence: ${d.confidence || '?'}`,
).join('\n\n')
const fullDossiers = dossiers.map((d) => `===== ${d.company} =====\n${d.markdown}`).join('\n\n')

const report = await agent(
  `You are the lead editor. Synthesize these verified company dossiers into ONE master report (markdown) on the AI-therapy field, as of ${TODAY}. Include, in order:
1. Executive summary (read-this-first; every claim traceable to a dossier).
2. Landscape overview.
3. Engineering difficulty ranking (table: company | difficulty /5 | why).
4. Funding & compensation comparison (table: company | total raised | latest valuation | notable comp bands).
5. Stated-vs-real motivations matrix (table: company | stated | likely real | confidence).
6. Common technical patterns across the field.
7. Risks & open questions.
Preserve evidence labels; show gaps as "unknown — not found", never blank. Also return a consolidated dated sources list as sourcesMarkdown.

DOSSIER DIGEST:\n${dossierDigest}\n\nFULL DOSSIERS:\n${fullDossiers}`,
  { label: 'synthesize-report', phase: 'Synthesize', schema: REPORT_SCHEMA, agentType: AT },
)

// ---- Phase 5.5: lead sign-off + bounded follow-up --------------------------
phase('Signoff')
let signoff = await agent(
  `You are the senior research lead. Review the master report below against the charter. Decide: is it good enough to ship to the user, or do up to THREE companies have critical gaps warranting one more targeted pass? Record your decisions log (every call you made on the user's behalf, flagForUser=true for close/consequential ones). List acceptedGaps you are knowingly shipping, and followUpCompanies (≤3) if any need another pass.

CHARTER SUCCESS CRITERIA: ${(charter && charter.successCriteria) || FOCUS}

REPORT:\n${(report && report.reportMarkdown) || ''}`,
  { label: 'lead-signoff', phase: 'Signoff', schema: SIGNOFF_SCHEMA, agentType: AT },
)

let finalReport = report
const followUps = ((signoff && signoff.followUpCompanies) || []).slice(0, 3)
if (followUps.length) {
  log(`Lead commissioned a bounded follow-up on: ${followUps.join(', ')}`)
  const targets = roster.filter((r) => followUps.some((f) => r.name.toLowerCase().includes(f.toLowerCase()) || f.toLowerCase().includes(r.name.toLowerCase())))
  const patched = (await pipeline(targets.length ? targets : roster.filter((r) => followUps.includes(r.name)), researchCompany, verifyStage, dossierStage)).filter(Boolean)
  // merge patched dossiers over the originals
  const byName = {}
  dossiers.forEach((d) => { byName[d.company] = d })
  patched.forEach((d) => { byName[d.company] = d })
  const merged = Object.values(byName)
  const mergedFull = merged.map((d) => `===== ${d.company} =====\n${d.markdown}`).join('\n\n')
  finalReport = await agent(
    `You are the lead editor. Re-synthesize the master report after a follow-up pass patched some dossiers. Same structure as before (exec summary, landscape, difficulty ranking, funding/comp table, stated-vs-real motivations matrix, common patterns, risks). Return reportMarkdown and sourcesMarkdown. As of ${TODAY}.\n\nDOSSIERS:\n${mergedFull}`,
    { label: 're-synthesize-report', phase: 'Synthesize', schema: REPORT_SCHEMA, agentType: AT },
  ) || report
  // one more sign-off to close the loop and finalize the decisions log
  signoff = await agent(
    `You are the senior research lead. The follow-up pass is done and the report re-synthesized. Provide the FINAL decisions log (cumulative — include earlier roster/charter calls too), set signedOff=true, and list any acceptedGaps that remain. Do not request more follow-ups.\n\nREPORT:\n${(finalReport && finalReport.reportMarkdown) || ''}`,
    { label: 'lead-final-signoff', phase: 'Signoff', schema: SIGNOFF_SCHEMA, agentType: AT },
  ) || signoff
}

log(`Sign-off: signedOff=${signoff && signoff.signedOff}. ${(signoff && signoff.decisionsLog || []).length} logged decision(s).`)

// ---- return: main loop writes these to disk --------------------------------
return {
  asOf: TODAY,
  charter,
  roster,
  ratifyDecisions: leadDecisions,
  dossiers: dossiers.map((d) => ({ company: d.company, markdown: d.markdown })),
  reportMarkdown: (finalReport && finalReport.reportMarkdown) || '',
  sourcesMarkdown: (finalReport && finalReport.sourcesMarkdown) || '',
  signoff,
}
