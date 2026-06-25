// workflows/ai-therapy-techniques-masterclass.workflow.js
//
// Part 3: a deep "engineering techniques masterclass" for a technical leader. For every
// technique it explains what it is, how it works, why it works, the people/resources it
// takes, scenarios where it fits, its cross-industry usage & positioning (June 2026), a
// concepts+leadership learning path (no coding labs), and team-building notes. Then a
// sequenced Leader's Curriculum and an applied-LLM Team-Building Blueprint. Includes an
// emerging-techniques discovery step for June 2026.
//
// Returns structured markdown pieces; the main loop writes the files (agents are
// read-only). Runs on the built-in 'general-purpose' agent; each prompt carries its role.

export const meta = {
  name: 'ai-therapy-techniques-masterclass',
  description:
    'Engineering techniques masterclass for a technical leader. Emerging-tech discovery (June 2026) -> per-technique pipeline producing 8-part chapters (what/how/why, people+resources, scenarios, cross-industry usage, leader learning-path, team notes) with an accuracy+freshness verify -> cross-synthesis of a sequenced Leader\'s Curriculum + an applied-LLM Team-Building Blueprint + mental models + what\'s-new-2026. Lead signs off with a decisions log. Read-only; writes nothing itself.',
  phases: [
    { title: 'Discover', detail: 'scan emerging techniques for June 2026; lead ratifies the chapter list' },
    { title: 'Chapters', detail: 'per-technique pipeline: 5 parallel sub-agents -> verify -> assemble an 8-part chapter' },
    { title: 'Verify', detail: 'accuracy + June-2026 freshness gate on each chapter' },
    { title: 'Curriculum', detail: 'sequenced Leader\'s Curriculum across all techniques' },
    { title: 'Team', detail: 'applied-LLM Team-Building Blueprint + graduation path' },
    { title: 'Synthesize', detail: 'executive intro + mental models + glossary + what\'s-new-2026' },
    { title: 'Signoff', detail: 'lead reviews and signs off with a decisions log' },
  ],
}

const AT = 'general-purpose'

// ---- args -------------------------------------------------------------------
let A = args
if (typeof A === 'string') A = {}
if (!A || typeof A !== 'object') A = {}
const TODAY = (typeof A.today === 'string' && A.today.trim()) ? A.today.trim() : '2026-06-25'
const FRESH = `IMPORTANT: it is ${TODAY}. SEARCH THE WEB for the CURRENT state of the art as of June 2026 — do not rely on stale training knowledge. Reflect what is actually used/adopted now.`

log(`ai-therapy-techniques-masterclass: as of ${TODAY}`)

// ---- core techniques (hard-coded) ------------------------------------------
const CORE = [
  { slug: 'pretraining', name: 'Pre-training (a foundation model from scratch)' },
  { slug: 'continued-pretraining', name: 'Continued / domain-adaptive pre-training' },
  { slug: 'sft', name: 'Supervised fine-tuning (SFT)' },
  { slug: 'reward-modeling', name: 'Reward modeling' },
  { slug: 'rlhf', name: 'RLHF / RLAIF (reinforcement learning from human/AI feedback)' },
  { slug: 'dpo', name: 'DPO (Direct Preference Optimization)' },
  { slug: 'moe-routing', name: 'Mixture-of-Experts + dynamic model routing' },
  { slug: 'serving', name: 'Inference & serving at scale + latency engineering' },
  { slug: 'guardrails', name: 'Guardrails / two-pass safety classifiers' },
  { slug: 'crisis-classifiers', name: 'Crisis-detection classifiers' },
  { slug: 'llm-judge', name: 'LLM-as-judge evaluation harnesses' },
  { slug: 'eval-construction', name: 'Clinical eval & benchmark construction' },
  { slug: 'rag', name: 'RAG, memory & personalization' },
  { slug: 'data-pipelines', name: 'Clinical & outcomes-indexed data pipelines' },
  { slug: 'voice', name: 'Voice-to-voice / real-time speech loops' },
  { slug: 'prompt-orchestration', name: 'Prompt engineering & orchestration (applied-LLM craft)' },
]

// ---- schemas ----------------------------------------------------------------
const CLAIM = {
  type: 'object', additionalProperties: false,
  required: ['statement', 'label'],
  properties: {
    statement: { type: 'string' },
    label: { type: 'string', enum: ['sourced', 'inference', 'speculation', 'contested', 'advisory'] },
    source: { type: 'string' }, date: { type: 'string' },
  },
}
const DISCOVERY_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['emerging'],
  properties: {
    emerging: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['name', 'slug', 'whyImportant', 'adoption2026', 'recommendChapter'],
        properties: {
          name: { type: 'string' }, slug: { type: 'string' },
          whyImportant: { type: 'string' }, adoption2026: { type: 'string' },
          recommendChapter: { type: 'boolean' },
          sources: { type: 'array', items: { type: 'string' } },
        },
      },
    },
  },
}
const RATIFY_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['chapters', 'decisions'],
  properties: {
    chapters: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['name', 'slug', 'kind'],
        properties: { name: { type: 'string' }, slug: { type: 'string' }, kind: { type: 'string', enum: ['core', 'emerging'] } },
      },
    },
    decisions: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['decision', 'fork', 'rationale', 'confidence'],
        properties: { decision: { type: 'string' }, fork: { type: 'string' }, rationale: { type: 'string' }, confidence: { type: 'string' }, flagForUser: { type: 'boolean' } },
      },
    },
  },
}
const SUBFINDING_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['markdown'],
  properties: {
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
    corrections: { type: 'array', items: { type: 'string' } },
    flags: { type: 'array', items: { type: 'string' } },
  },
}
const CHAPTER_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['technique', 'slug', 'markdown', 'oneLine'],
  properties: {
    technique: { type: 'string' }, slug: { type: 'string' },
    oneLine: { type: 'string', description: 'one-sentence summary for the curriculum/team synthesizers' },
    markdown: { type: 'string', description: 'the full 8-part chapter markdown' },
    sources: { type: 'array', items: { type: 'string' } },
  },
}
const MD_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['markdown'],
  properties: { markdown: { type: 'string' }, sources: { type: 'array', items: { type: 'string' } } },
}
const SYNTH_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['executiveIntro', 'mentalModels', 'glossary', 'whatsNew2026'],
  properties: {
    executiveIntro: { type: 'string' }, mentalModels: { type: 'string' },
    glossary: { type: 'string' }, whatsNew2026: { type: 'string' },
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
        properties: { decision: { type: 'string' }, fork: { type: 'string' }, rationale: { type: 'string' }, confidence: { type: 'string' }, flagForUser: { type: 'boolean' } },
      },
    },
  },
}

const LABELS = `Label factual claims sourced(url+date) / inference / speculation; label learning-design and org recommendations as "advisory" (your reasoned intelligence). Plain language for a HIGHLY INTELLIGENT reader — simple words, real depth, never condescending, never jargon-as-fog.`

// ---- Phase 0: emerging-tech discovery + ratify -----------------------------
phase('Discover')
const discovery = await agent(
  `You are a discovery scout for AI/ML engineering techniques. ${FRESH}\n\nThe masterclass already covers these 16 CORE techniques:\n${CORE.map((c) => `- ${c.name}`).join('\n')}\n\nFind the NEW / EFFECTIVE / EMERGING techniques gaining real adoption as of June 2026 that are NOT already covered (e.g. test-time/inference-time compute & reasoning models, RLVR/GRPO and newer RL recipes, agentic RL & tool-use training, long-context & memory architectures, agentic-RAG, speculative decoding & serving accelerations, distillation/small-model specialization, LoRA/PEFT, quantization, synthetic data, state-space/Mamba & architecture shifts, multimodal, on-device, constitutional-AI/automated alignment). For each: why it matters and its actual June-2026 adoption. Recommend which deserve their own chapter.`,
  { label: 'discover-emerging', phase: 'Discover', schema: DISCOVERY_SCHEMA, agentType: AT },
)
const emergingProposed = ((discovery && discovery.emerging) || []).filter((e) => e && e.name)
const ratified = await agent(
  `You are the senior research lead. The masterclass will have a chapter per technique. Confirm the 16 CORE techniques and SELECT up to 6 of the proposed emerging techniques that genuinely deserve their own chapter as of June 2026 (merge duplicates, cut the marginal). Return the FINAL chapter list (core + selected emerging) and your decisions.\n\nCORE:\n${CORE.map((c) => `- ${c.name} [${c.slug}]`).join('\n')}\n\nPROPOSED EMERGING:\n${emergingProposed.map((e) => `- ${e.name} [${e.slug}] — ${e.whyImportant} (adoption: ${e.adoption2026}; recommend: ${e.recommendChapter})`).join('\n')}`,
  { label: 'ratify-chapters', phase: 'Discover', schema: RATIFY_SCHEMA, agentType: AT },
)
let chapters = (ratified && ratified.chapters && ratified.chapters.length) ? ratified.chapters : CORE.map((c) => ({ ...c, kind: 'core' }))
// de-dupe by slug, cap emerging at 6
const seen = new Set(); const core = []; const emerging = []
for (const ch of chapters) {
  if (!ch.slug || seen.has(ch.slug)) continue
  seen.add(ch.slug)
  ;(ch.kind === 'emerging' ? emerging : core).push(ch)
}
chapters = core.concat(emerging.slice(0, 6))
const ratifyDecisions = (ratified && ratified.decisions) || []
log(`Chapters ratified: ${chapters.length} (${emerging.slice(0, 6).length} emerging).`)

// ---- Phase 1-2: per-technique chapter pipeline -----------------------------
phase('Chapters')

function subAgents(ch) {
  const ctx = `TECHNIQUE: ${ch.name}\n${FRESH}\n${LABELS}`
  return [
    { k: 'mechanics', agentRole: 'tech-investigator',
      brief: `You are a deep technology investigator. Explain the MECHANICS for a smart non-implementer: (1) WHAT it is, (2) HOW it works — the actual mechanism/algorithm and the intuition (show the gears turning), (3) WHY it works — the underlying principle and why the naive alternative fails, (4) PEOPLE & RESOURCES — team size/roles, compute, time, money, data scale (orders of magnitude with basis).` },
    { k: 'scenarios', agentRole: 'eng-explainer',
      brief: `You are a technical translator. Write SCENARIOS & STORIES: concrete narratives of where this technique is appropriate and effective, and where it is the WRONG tool. Make them vivid and specific, not abstract.` },
    { k: 'cross-industry', agentRole: 'tech-investigator',
      brief: `You are a deep technology investigator. Write CROSS-INDUSTRY USAGE & POSITIONING: how and where this technique is used across ALL industries (healthcare, finance, legal, customer support, coding/dev tools, robotics, defense, consumer, science, etc.), where it is table-stakes vs. cutting-edge, who leads its use in each sector, and the state of the art as of June 2026.` },
    { k: 'curriculum', agentRole: 'curriculum-architect',
      brief: `You are a learning architect for a technical LEADER (not an implementer). Write the LEARNING PATH: the core mental models, a short sequenced concepts-only progression, a curated reading/watching spine (few, high-value), understanding-checkpoints ("you understand it when you can…"), and HOW TO EVALUATE AN EXPERT on this in an interview (questions, strong vs. weak answers, red flags). No coding labs.` },
    { k: 'team', agentRole: 'team-builder',
      brief: `You are an org/hiring strategist. Write TEAM NOTES for this technique: which roles/seniority it needs (or whether an existing role absorbs it), hiring signals & red flags, build-vs-buy (default to rent/buy unless owning it is a real moat), and common failure modes.` },
  ].map((s) => ({ ...s, prompt: `${s.brief}\n\n${ctx}` }))
}

async function researchChapter(ch) {
  const subs = subAgents(ch)
  const results = await parallel(subs.map((s) => () =>
    agent(s.prompt, { label: `ch:${ch.slug}:${s.k}`, phase: 'Chapters', schema: SUBFINDING_SCHEMA, agentType: AT })
      .then((r) => ({ k: s.k, r })),
  ))
  return { ch, subs: results.filter((x) => x && x.r) }
}

async function verifyChapter(res) {
  const text = res.subs.map((s) => `[${s.k}]\n${s.r.markdown}`).join('\n\n')
  const verdict = await agent(
    `You are an adversarial fact-checker with deep ML knowledge. ${FRESH} Scrutinize the technical content below about "${res.ch.name}". Flag: anything technically WRONG in the how/why; any plain-language simplification that has become MISLEADING; any cross-industry or state-of-the-art claim that is stale (not current to June 2026); and inference stated as fact. Return overall confidence + specific corrections.\n\n${text}`,
    { label: `verify:${res.ch.slug}`, phase: 'Verify', schema: VERIFY_SCHEMA, agentType: AT },
  )
  return { ...res, verdict }
}

async function assembleChapter(res) {
  const byk = {}; res.subs.forEach((s) => { byk[s.k] = s.r })
  const part = (k) => (byk[k] && byk[k].markdown) || '(missing)'
  const corr = res.verdict ? `VERIFIER (confidence ${res.verdict.overallConfidence}) CORRECTIONS — APPLY THESE:\n${(res.verdict.corrections || []).map((c) => `- ${c}`).join('\n')}` : ''
  const ch = await agent(
    `You are the lead editor + technical translator. Assemble the FINAL chapter on "${res.ch.name}" for a highly intelligent technical leader. ${LABELS} Apply the verifier corrections. Start with "# ${res.ch.name}". Produce these EIGHT sections in order with clear headers:
1. What it is
2. How it works
3. Why it works
4. People & resources
5. Scenarios & stories
6. Cross-industry usage & positioning (as of June 2026)
7. Learning path for a technical leader (mental models, reading spine, checkpoints, how to evaluate an expert)
8. Team notes (roles, hiring signals, build-vs-buy, failure modes)
End with a short "Sources" list. Also return a one-sentence oneLine summary.

RAW MATERIAL:
## mechanics\n${part('mechanics')}
## scenarios\n${part('scenarios')}
## cross-industry\n${part('cross-industry')}
## curriculum\n${part('curriculum')}
## team\n${part('team')}

${corr}`,
    { label: `assemble:${res.ch.slug}`, phase: 'Chapters', schema: CHAPTER_SCHEMA, agentType: AT },
  )
  // carry sources from subs if assembler omitted them
  const subSources = []
  res.subs.forEach((s) => (s.r.sources || []).forEach((u) => subSources.push(u)))
  return ch ? { ...ch, slug: ch.slug || res.ch.slug, _sources: Array.from(new Set(((ch.sources || []).concat(subSources)).filter(Boolean))) } : null
}

const builtChapters = (await pipeline(chapters, researchChapter, verifyChapter, assembleChapter)).filter(Boolean)
log(`Chapters built: ${builtChapters.length}/${chapters.length}.`)

// ---- Phase 3: cross-synthesis ----------------------------------------------
const digest = builtChapters.map((c) => `- ${c.technique} [${c.slug}]: ${c.oneLine || ''}`).join('\n')

phase('Curriculum')
const curriculum = await agent(
  `You are a learning architect for a highly intelligent technical LEADER (concepts + leadership, NO hands-on coding labs). ${LABELS} Design THE LEADER'S CURRICULUM across all the techniques below — a genuinely SEQUENCED roadmap, not a flat list: dependency order and what to learn first; a progression (foundations -> the training stack -> serving -> safety/eval -> data -> product craft -> the 2026 frontier); understanding-checkpoints at each stage; and a single curated reading spine. Make it a roadmap the leader could actually follow over, say, 8-12 weeks of part-time study. Output markdown starting "## The Leader's Curriculum".\n\nTECHNIQUES:\n${digest}`,
  { label: 'curriculum', phase: 'Curriculum', schema: MD_SCHEMA, agentType: AT },
)

phase('Team')
const teamBlueprint = await agent(
  `You are an org/hiring strategist. ${FRESH} ${LABELS} Design THE TEAM-BUILDING BLUEPRINT for an applied-LLM product org (use AI therapy as a worked example but keep it general). Cover: the core roles (applied-AI/ML, data, safety/eval, infra/serving, product, domain/clinical) and what each owns; the first-5 then first-15 HIRING SEQUENCE matched to stage/budget; interview signals per role; realistic budget ranges per role/level as of June 2026; build-vs-buy per capability (default rent/buy unless owning is a real moat); and the GRADUATION PATH — when (if ever) to move from renting models to training/owning them, the new roles/cost step-change that demands, and how to tell you're truly ready. Output markdown starting "## The Team-Building Blueprint".\n\nTECHNIQUES IN SCOPE:\n${digest}`,
  { label: 'team-blueprint', phase: 'Team', schema: MD_SCHEMA, agentType: AT },
)

phase('Synthesize')
const synth = await agent(
  `You are the lead editor + technical translator. ${LABELS} Write FOUR framing pieces for this engineering masterclass aimed at a technical leader:
1. executiveIntro — how to use this document; the single most important truth a leader should hold.
2. mentalModels — the handful of cross-cutting mental models that unlock everything else (the "if you get these, the rest clicks" ideas).
3. glossary — a tight plain-language glossary of the key terms.
4. whatsNew2026 — a short section on what's genuinely new/shifting in 2026 (the emerging techniques) and their trajectory.

TECHNIQUES:\n${digest}`,
  { label: 'synthesize', phase: 'Synthesize', schema: SYNTH_SCHEMA, agentType: AT },
)

// ---- Phase: lead sign-off --------------------------------------------------
phase('Signoff')
const signoff = await agent(
  `You are the senior research lead. Sign off on this engineering techniques masterclass on behalf of the user (away). Confirm: every chapter has all 8 parts including cross-industry usage; content is current to June 2026; the curriculum is genuinely sequenced with checkpoints; the team blueprint has a hiring sequence, interview signals, build-vs-buy, and a graduation path; emerging techniques were discovered and chaptered. Record your decisions log (flagForUser=true for close/consequential calls) and any acceptedGaps. Set signedOff=true.\n\nSUMMARY: ${builtChapters.length} chapters (${emerging.slice(0, 6).length} emerging), a sequenced curriculum, a team blueprint, mental models + glossary. As of ${TODAY}.`,
  { label: 'lead-signoff', phase: 'Signoff', schema: SIGNOFF_SCHEMA, agentType: AT },
)
log(`Sign-off: signedOff=${signoff && signoff.signedOff}.`)

// ---- collect sources --------------------------------------------------------
const allSources = []
builtChapters.forEach((c) => (c._sources || []).forEach((u) => allSources.push(u)))
emergingProposed.forEach((e) => (e.sources || []).forEach((u) => allSources.push(u)))
;(curriculum && curriculum.sources || []).forEach((u) => allSources.push(u))
;(teamBlueprint && teamBlueprint.sources || []).forEach((u) => allSources.push(u))

// ---- return -----------------------------------------------------------------
return {
  asOf: TODAY,
  chapterList: chapters,
  ratifyDecisions,
  executiveIntro: (synth && synth.executiveIntro) || '',
  mentalModels: (synth && synth.mentalModels) || '',
  glossary: (synth && synth.glossary) || '',
  whatsNew2026: (synth && synth.whatsNew2026) || '',
  curriculumMarkdown: (curriculum && curriculum.markdown) || '',
  teamBlueprintMarkdown: (teamBlueprint && teamBlueprint.markdown) || '',
  chapters: builtChapters.map((c) => ({ technique: c.technique, slug: c.slug, oneLine: c.oneLine, markdown: c.markdown })),
  signoff,
  sources: Array.from(new Set(allSources.filter(Boolean))),
}
