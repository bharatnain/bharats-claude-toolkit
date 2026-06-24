// workflows/ai-therapy-engineering-deep-dive.workflow.js
//
// Part 2 of the AI-therapy research program: an ENGINEERING deep-dive companion to the
// existing market report, written so a smart NON-technical reader understands what each
// technical choice actually means. Reuses the same agent team. Goes deepest on
// Slingshot/Ash, deep on the genuine builders, and gives a real technical read even of
// the GPT/Claude/Gemini "wrapper" vendors. Corrects compensation with a two-column
// floor-vs-likely-real model (top engineers reportedly clear >$1M; public figures are
// unreliable floors).
//
// Returns structured markdown pieces; the calling main loop assembles the final report
// and writes it to disk (research agents are read-only).
//
// Run via the Workflow tool. Same grammar as workflows/ai-therapy-research.workflow.js.
//
// NOTE: custom agent types in agents/*.md are not registered as runnable in every
// session, so we run on the built-in 'general-purpose' agent (full tools incl.
// WebSearch/WebFetch/Read). Each agent() prompt carries its role identity.

export const meta = {
  name: 'ai-therapy-engineering-deep-dive',
  description:
    'Engineering deep-dive companion to the AI-therapy market report, for a non-technical reader. Hard-coded technique list + company tiering (no charter dependency). Technique primer (plain-English, 6-question) -> per-company engineering deep dive (Slingshot deepest, builders deep, wrappers a real technical read; each grounded in its existing dossier) -> two-column floor-vs-likely-real compensation model -> global talent map -> adversarial verify -> synthesize. Lead signs off with a decisions log. Read-only; writes nothing itself.',
  phases: [
    { title: 'Primer', detail: 'plain-English 6-question explainer for each core technique' },
    { title: 'Company', detail: 'per-company engineering deep dive, grounded in existing dossiers' },
    { title: 'Comp', detail: 'two-column floor-vs-likely-real compensation model' },
    { title: 'Talent', detail: 'global map of who can actually do the hard techniques' },
    { title: 'Verify', detail: 'adversarial check of the high-stakes inferences' },
    { title: 'Synthesize', detail: 'executive intro + engineering-lens re-rating + moat synthesis' },
    { title: 'Signoff', detail: 'lead reviews and signs off with a decisions log' },
  ],
}

const AT = 'general-purpose'

// ---- args -------------------------------------------------------------------
let A = args
if (typeof A === 'string') A = {}
if (!A || typeof A !== 'object') A = {}
const TODAY = (typeof A.today === 'string' && A.today.trim()) ? A.today.trim() : '2026-06-24'
const DOSSIER_DIR = 'research/ai-therapy/companies'

// Insider premise (user-provided informed industry context — a credible premise to
// corroborate, NOT published fact).
const INSIDER = `INSIDER INPUT (informed industry context from the user — treat as a credible premise to corroborate and contextualize, not as published fact): at several of these firms, top engineers reportedly earn MORE THAN $1,000,000 total compensation; exact figures are undisclosed; the public figures (levels.fyi / H1B LCA, ~$200-225K) materially UNDERSTATE reality, especially for elite AI/ML talent and for equity/retention.`

log(`ai-therapy-engineering-deep-dive: as of ${TODAY}`)

// ---- techniques (hard-coded; not charter-derived) --------------------------
const TECHNIQUES = [
  { key: 'pretraining', name: 'Pre-training (a foundation model from scratch)' },
  { key: 'continued-pretrain', name: 'Continued / domain-adaptive pre-training (Slingshot\'s actual move on Qwen3-235B)' },
  { key: 'sft', name: 'Supervised fine-tuning (SFT)' },
  { key: 'reward-model', name: 'Reward modeling (teaching a model what "good" looks like)' },
  { key: 'rlhf', name: 'RLHF / RLAIF (reinforcement learning from human/AI feedback)' },
  { key: 'dpo', name: 'DPO (Direct Preference Optimization)' },
  { key: 'moe-routing', name: 'Mixture-of-Experts + dynamic model routing' },
  { key: 'serving', name: 'Inference & serving at scale + latency engineering' },
  { key: 'guardrails', name: 'Guardrails / two-pass safety classifiers' },
  { key: 'crisis', name: 'Crisis-detection classifiers (self-harm / suicide escalation)' },
  { key: 'llm-judge', name: 'LLM-as-judge evaluation harnesses' },
  { key: 'evals', name: 'Clinical eval & benchmark construction (VERA-MH, CTRS scoring)' },
  { key: 'rag', name: 'RAG, memory & personalization' },
  { key: 'data-pipeline', name: 'Clinical & outcomes-indexed data pipelines (the real moat)' },
  { key: 'voice', name: 'Voice-to-voice / real-time speech loops' },
  { key: 'wrapper-craft', name: 'Prompt engineering & orchestration (the craft of a good "wrapper")' },
]

// ---- companies (hard-coded tiering) ----------------------------------------
const COMPANIES = [
  { name: 'Slingshot AI (Ash)', slug: 'slingshot-ai', engTier: 1 },
  { name: 'Spring Health', slug: 'spring-health', engTier: 2 },
  { name: 'Limbic', slug: 'limbic', engTier: 2 },
  { name: 'Jimini Health (Sage)', slug: 'jimini-health', engTier: 2 },
  { name: 'ieso (Velora)', slug: 'ieso', engTier: 2 },
  { name: 'Wysa', slug: 'wysa', engTier: 2 },
  { name: 'Lyra Health', slug: 'lyra-health', engTier: 3 },
  { name: 'Talkspace', slug: 'talkspace', engTier: 3 },
  { name: 'SonderMind', slug: 'sondermind', engTier: 3 },
  { name: 'Youper', slug: 'youper', engTier: 3 },
  { name: 'Sonia', slug: 'sonia', engTier: 3 },
  { name: 'Headspace (Ebb)', slug: 'headspace', engTier: 3 },
  { name: 'BetterHelp (Teladoc)', slug: 'betterhelp', engTier: 3 },
  { name: 'Earkick', slug: 'earkick', engTier: 3 },
  { name: 'Woebot Health', slug: 'woebot-health', engTier: 3 },
  { name: 'Therabot (Dartmouth)', slug: 'therabot', engTier: 3 },
]

// ---- schemas ----------------------------------------------------------------
const CLAIM = {
  type: 'object', additionalProperties: false,
  required: ['statement', 'label'],
  properties: {
    statement: { type: 'string' },
    label: { type: 'string', enum: ['sourced', 'inference', 'speculation', 'contested'] },
    source: { type: 'string' }, date: { type: 'string' },
  },
}

const TECHNIQUE_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['technique', 'markdown'],
  properties: {
    technique: { type: 'string' },
    markdown: { type: 'string', description: 'a complete plain-English section answering all six questions: what-it-is+impact, skill set, difficulty(1-5)+why, who-can-do-it, cost, data requirement & scale' },
    difficulty: { type: 'number' },
    sources: { type: 'array', items: { type: 'string' } },
    claims: { type: 'array', items: CLAIM },
  },
}

const COMPANY_ENG_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['company', 'markdown', 'isWrapper'],
  properties: {
    company: { type: 'string' },
    markdown: { type: 'string', description: 'full per-company engineering section: which techniques they actually use, what that takes, difficulty/talent/cost/data for THEIR stack, written for a non-technical reader' },
    engineeringDifficulty: { type: 'number' },
    isWrapper: { type: 'boolean', description: 'true if they primarily build on a third-party model (GPT/Claude/Gemini) rather than train their own' },
    wrapperQuality: { type: 'string', description: 'if a wrapper: how sophisticated the wrapper really is (orchestration/eval/safety/cost engineering)' },
    talentNeeded: { type: 'string' },
    dataMoat: { type: 'string' },
    sources: { type: 'array', items: { type: 'string' } },
    claims: { type: 'array', items: CLAIM },
  },
}

const SUBFINDING_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['aspect', 'markdown'],
  properties: {
    aspect: { type: 'string' },
    markdown: { type: 'string' },
    sources: { type: 'array', items: { type: 'string' } },
    claims: { type: 'array', items: CLAIM },
  },
}

const VERIFY_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['overallConfidence', 'corrections'],
  properties: {
    overallConfidence: { type: 'string', enum: ['high', 'medium', 'low'] },
    corrections: { type: 'array', items: { type: 'string' }, description: 'specific claims to downgrade, fix, or flag, with why' },
    flags: { type: 'array', items: { type: 'string' } },
  },
}

const COMP_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['markdown'],
  properties: {
    markdown: { type: 'string', description: 'the full two-column compensation section: a market-level model + a per-company table with a DISCLOSED FLOOR column (public figures, labeled unreliable) beside a LIKELY REAL column (inferred total comp, elite ICs $1M+), with the method/basis shown. All inference, labeled.' },
    sources: { type: 'array', items: { type: 'string' } },
    claims: { type: 'array', items: CLAIM },
  },
}

const TALENT_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['markdown'],
  properties: {
    markdown: { type: 'string', description: 'global talent map: who in the world can actually do the hard techniques, named labs/orgs, geographic concentration, scarcity, and why these companies compete for / cannot afford that talent' },
    sources: { type: 'array', items: { type: 'string' } },
    claims: { type: 'array', items: CLAIM },
  },
}

const SYNTH_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['executiveIntro', 'partE'],
  properties: {
    executiveIntro: { type: 'string', description: 'a plain-English executive introduction that frames the whole engineering deep-dive for a non-technical decision-maker' },
    partE: { type: 'string', description: 'Part E: engineering-lens difficulty re-rating + where each company\'s real engineering moat is vs. commodity assembly' },
  },
}

const SIGNOFF_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['signedOff', 'decisionsLog'],
  properties: {
    signedOff: { type: 'boolean' },
    acceptedGaps: { type: 'array', items: { type: 'string' } },
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

const LABELS = `Label every claim sourced(url+date) / inference / speculation / contested. Never present an inference as disclosed fact. Where something isn't found, say "unknown — not found".`

// ---- Phase 1: technique primer (parallel) ----------------------------------
phase('Primer')
const primers = (await parallel(TECHNIQUES.map((t) => () =>
  agent(
    `You are a technical translator writing for a SMART NON-TECHNICAL reader (a CEO/investor, not an ML engineer). Explain the technique below so they understand what it MEANS and why it matters — accurate first, simple second; use a concrete analogy then say where it breaks.

TECHNIQUE: ${t.name}

Answer ALL SIX questions as a clean markdown section (start with "### ${t.name}"):
1. What it is + its impact (plain English; what choosing this changes about product/cost/moat/risk).
2. Skill set required (what kind of engineer/researcher).
3. Difficulty 1-5 and WHY (weekend project vs. eight-figure multi-year effort).
4. Who in the world can actually do it (any web team / a strong ML team / fewer than a few hundred people).
5. Cost — compute, training runs, infra, talent — in orders of magnitude with basis.
6. Data requirement & scale — what data, how much, how sourced, why it's a moat.
Calibrate hype: if marketing language inflates a modest technique, say so. As of ${TODAY}. ${LABELS}`,
    { label: `primer:${t.key}`, phase: 'Primer', schema: TECHNIQUE_SCHEMA, agentType: AT },
  ),
))).filter(Boolean)
log(`Primer: ${primers.length}/${TECHNIQUES.length} technique explainers done.`)

// ---- Phase 2: per-company engineering deep dive (pipeline) ------------------
phase('Company')

function companyEngBrief(co) {
  return `COMPANY: ${co.name}
GROUNDING: First READ the existing dossier at ${DOSSIER_DIR}/${co.slug}.md to ground yourself in what's already known, then go DEEPER with fresh web research. Do not repeat the dossier — extend it on the engineering.
TASK: Explain this company's ENGINEERING for a non-technical reader. Which of the core techniques (pre-training, continued pre-training, SFT, reward modeling, RLHF/RLAIF, DPO, MoE+routing, serving/latency, guardrails, crisis detection, LLM-as-judge, clinical evals, RAG/memory, data pipelines, voice, prompt/orchestration) do they ACTUALLY use, and what does each take in THEIR case — difficulty, the talent it requires, the cost, and the data scale. Be concrete about what's genuinely hard vs. commodity assembly. As of ${TODAY}. ${LABELS}`
}

async function researchCompanyEng(co) {
  if (co.engTier === 1) {
    // deepest: fan out to 4 sub-agents, then merge
    const aspects = [
      { k: 'training', brief: 'the TRAINING stack: continued pre-training + SFT + reward model + DPO/RL on the open-weight Qwen3-235B base — what each stage does, the compute, the data, and how hard it really is vs. a true from-scratch foundation model.' },
      { k: 'serving', brief: 'the SERVING/INFRA: Mixture-of-Experts dynamic routing (32B-235B within one dialogue), Nebius/Together infrastructure, latency engineering, retraining cadence (3-7x/week) and what that cadence implies about the team.' },
      { k: 'data-safety', brief: 'the DATA & SAFETY pipeline: the proprietary clinical dataset (provenance, scale, labeling, clinician comparisons), the two-pass guardrail architecture, crisis handling, and why the data is the real moat.' },
      { k: 'talent', brief: 'the TEAM & TALENT: what kind of engineers/researchers this stack requires, how many, where they come from, how scarce that talent is, and what it implies they must be paying.' },
    ]
    const subs = (await parallel(aspects.map((asp) => () =>
      agent(`You are a deep technology investigator. ${companyEngBrief(co)}\n\nFOCUS THIS PASS ON: ${asp.brief}`,
        { label: `eng:${co.slug}:${asp.k}`, phase: 'Company', schema: SUBFINDING_SCHEMA, agentType: AT }),
    ))).filter(Boolean)
    return { company: co, tier: 1, subs }
  }
  const rec = await agent(
    `You are a deep technology investigator. ${companyEngBrief(co)}` +
      (co.engTier === 3 ? `\n\nNOTE: this company likely builds primarily on a third-party model (GPT/Claude/Gemini). Do NOT dismiss it — give a REAL technical read of how sophisticated their wrapper is (orchestration, evals, safety, cost/latency engineering, any fine-tuning). Set isWrapper accurately and describe wrapperQuality.` : ''),
    { label: `eng:${co.slug}`, phase: 'Company', schema: COMPANY_ENG_SCHEMA, agentType: AT },
  )
  return { company: co, tier: co.engTier, rec }
}

async function verifyCompanyEng(res) {
  const text = res.subs
    ? res.subs.map((s) => `### ${s.aspect}\n${s.markdown}`).join('\n\n')
    : (res.rec && res.rec.markdown) || ''
  const verdict = await agent(
    `You are an adversarial fact-checker. Scrutinize the engineering claims below about ${res.company.name}. Flag anything stated as fact that is really inference, any inflated difficulty/talent/cost claim, any conflated entity, and any plain-English simplification that has become MISLEADING. Return overall confidence + a list of specific corrections.\n\n${text}`,
    { label: `verify:${res.company.slug}`, phase: 'Verify', schema: VERIFY_SCHEMA, agentType: AT },
  )
  return { ...res, verdict }
}

async function finalizeCompanyEng(res) {
  const raw = res.subs
    ? res.subs.map((s) => `### ${s.aspect}\n${s.markdown}\n\nSources: ${(s.sources || []).join(', ')}`).join('\n\n')
    : `${(res.rec && res.rec.markdown) || ''}\n\nSources: ${((res.rec && res.rec.sources) || []).join(', ')}`
  const corr = res.verdict ? `VERIFIER (confidence ${res.verdict.overallConfidence}) CORRECTIONS:\n${(res.verdict.corrections || []).map((c) => `- ${c}`).join('\n')}` : ''
  const md = await agent(
    `You are the lead editor + technical translator. Write the final ENGINEERING section for ${res.company.name} for a NON-TECHNICAL reader. Start with "## ${res.company.name}". Apply the verifier's corrections. Keep evidence labels. Be concrete about what's genuinely hard vs. commodity, the talent it takes, the cost, and the data scale. End with a one-line "Engineering moat:" verdict and a short Sources list.\n\nRAW FINDINGS:\n${raw}\n\n${corr}`,
    { label: `finalize:${res.company.slug}`, phase: 'Company', schema: COMPANY_ENG_SCHEMA, agentType: AT },
  )
  return md
}

const companyEng = (await pipeline(COMPANIES, researchCompanyEng, verifyCompanyEng, finalizeCompanyEng)).filter(Boolean)
log(`Company deep-dives: ${companyEng.length}/${COMPANIES.length} done.`)

// ---- Phase 3: compensation realism (two-column) ----------------------------
phase('Comp')
const compContext = COMPANIES.map((c) => `${c.name} (dossier: ${DOSSIER_DIR}/${c.slug}.md)`).join('; ')
const comp = await agent(
  `You are the people & compensation analyst. Build the COMPENSATION REALITY section for a non-technical reader. The existing market report listed public figures (~$200-225K TC) — those are UNRELIABLE FLOORS.

${INSIDER}

Produce a TWO-COLUMN model: for each company/role where possible (and at market level), a "DISCLOSED FLOOR" column (the public levels.fyi/H1B figures, explicitly labeled unreliable floor) BESIDE a "LIKELY REAL" column (inferred total compensation — elite ICs $1M+ cash+equity+retention). SHOW THE METHOD: frontier-lab comparables (OpenAI/Anthropic/DeepMind research engineers run ~$500K-$2M+ total comp — corroborate with public reporting), equity math at each company's valuation, retention/liquidity dynamics, and the insider premise above. Everything is INFERENCE with its basis shown — never present it as disclosed fact. Read company dossiers as needed: ${compContext}. As of ${TODAY}. ${LABELS}`,
  { label: 'compensation', phase: 'Comp', schema: COMP_SCHEMA, agentType: AT },
)
// verify the comp model (highest-stakes inference)
const compVerify = await agent(
  `You are an adversarial fact-checker. The compensation model below makes a strong inference (top engineers >$1M, public figures unreliable). Pressure-test it: are the frontier-lab comparables real and sourced? Is the equity math defensible? Is everything properly labeled as inference, not fact? Return overall confidence + specific corrections.\n\n${(comp && comp.markdown) || ''}`,
  { label: 'verify:comp', phase: 'Verify', schema: VERIFY_SCHEMA, agentType: AT },
)

// ---- Phase 4: global talent map --------------------------------------------
phase('Talent')
const talent = await agent(
  `You are a deep technology investigator. Build the GLOBAL TALENT MAP for a non-technical reader: who in the world can ACTUALLY do the hard techniques behind AI therapy (continued pre-training, RLHF/reward modeling, MoE serving, safety/eval engineering, clinical data pipelines). Name the real labs/orgs and the kinds of people; describe geographic concentration and scarcity; and explain why these AI-therapy companies must compete with frontier labs (and often cannot afford to) for that talent. Tie scarcity directly to the >$1M compensation reality. As of ${TODAY}. ${LABELS}`,
  { label: 'talent-map', phase: 'Talent', schema: TALENT_SCHEMA, agentType: AT },
)

// ---- Phase 6: synthesis (intro + Part E) -----------------------------------
phase('Synthesize')
const companyDigest = companyEng.map((c) => `- ${c.company}: difficulty ${c.engineeringDifficulty || '?'}/5${c.isWrapper ? ' (wrapper)' : ''} — moat: ${(c.dataMoat || '').slice(0, 160)}`).join('\n')
const synth = await agent(
  `You are the lead editor + technical translator. Write TWO things for a NON-TECHNICAL reader of an AI-therapy engineering deep-dive:
1. executiveIntro — a plain-English introduction that frames the whole document: what the reader will learn, the single most important engineering truth of this field, and how to read the technique/company/comp/talent sections.
2. partE — "Part E: Engineering-Lens Difficulty Re-Rating & Real Moats": rank where the genuine engineering is vs. commodity assembly, and state each company's real engineering moat in one line. Reconcile with the Part-1 difficulty ranking.

COMPANY DIGEST:\n${companyDigest}\n\nAs of ${TODAY}.`,
  { label: 'synthesize', phase: 'Synthesize', schema: SYNTH_SCHEMA, agentType: AT },
)

// ---- Phase 7: lead sign-off ------------------------------------------------
phase('Signoff')
const signoff = await agent(
  `You are the senior research lead. Sign off on this engineering deep-dive on behalf of the user (who is away). Confirm: every technique is explained in plain English; Slingshot/Ash is the deepest; builders are deep; wrappers got a real technical read; the compensation section properly presents floor-vs-likely-real as labeled inference (with the >$1M reality represented); the talent map names real orgs. Record your decisions log (each call you made, flagForUser=true for close/consequential ones) and any acceptedGaps. Set signedOff=true.

SUMMARY: ${companyEng.length} company sections, ${primers.length} technique explainers, a two-column comp model (verifier confidence: ${(compVerify && compVerify.overallConfidence) || '?'}), and a talent map. As of ${TODAY}.`,
  { label: 'lead-signoff', phase: 'Signoff', schema: SIGNOFF_SCHEMA, agentType: AT },
)
log(`Sign-off: signedOff=${signoff && signoff.signedOff}.`)

// ---- collect sources --------------------------------------------------------
function collectSources() {
  const all = []
  primers.forEach((p) => (p.sources || []).forEach((s) => all.push(s)))
  companyEng.forEach((c) => (c.sources || []).forEach((s) => all.push(s)))
  ;(comp && comp.sources || []).forEach((s) => all.push(s))
  ;(talent && talent.sources || []).forEach((s) => all.push(s))
  return Array.from(new Set(all.filter(Boolean)))
}

// ---- return: main loop writes these to disk --------------------------------
return {
  asOf: TODAY,
  executiveIntro: (synth && synth.executiveIntro) || '',
  techniques: primers.map((p) => ({ technique: p.technique, markdown: p.markdown })),
  companies: companyEng.map((c) => ({ company: c.company, markdown: c.markdown, difficulty: c.engineeringDifficulty, isWrapper: c.isWrapper })),
  compMarkdown: (comp && comp.markdown) || '',
  compConfidence: (compVerify && compVerify.overallConfidence) || null,
  talentMarkdown: (talent && talent.markdown) || '',
  partE: (synth && synth.partE) || '',
  signoff,
  sources: collectSources(),
}
