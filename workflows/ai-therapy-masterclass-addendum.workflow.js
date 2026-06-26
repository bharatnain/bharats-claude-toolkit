// workflows/ai-therapy-masterclass-addendum.workflow.js
//
// Addendum to the engineering masterclass: builds 8 additional technique chapters
// (Constitutional AI 2.0 + 7 previously-cut sidebars), then RE-synthesizes the Leader's
// Curriculum, Team Blueprint, and framing over the FULL ~30-technique set, adds a
// spend/compensation guidance section (data WITH caveats + explicit tech-lead decisions),
// and gets a clean final lead sign-off. Read-only; the main loop writes files.
//
// args: { today, existingDigest: [{technique, slug, oneLine}] }

export const meta = {
  name: 'ai-therapy-masterclass-addendum',
  description:
    'Add 8 technique chapters (Constitutional AI 2.0 + distillation, SSM/Mamba, long-context memory, agent-eval/observability, diffusion LLMs, on-device inference, any-to-any multimodal) in the same 8-section format, then re-synthesize the Leader\'s Curriculum, Team Blueprint, mental models/glossary/what\'s-new over the full ~30-technique set, add spend/comp guidance (data with caveats + tech-lead decisions), and get a clean lead sign-off. Read-only.',
  phases: [
    { title: 'Chapters', detail: 'build 8 new 8-section chapters -> verify -> assemble' },
    { title: 'Curriculum', detail: 're-sequence the Leader\'s Curriculum over the full set' },
    { title: 'Team', detail: 're-derive the Team-Building Blueprint over the full set' },
    { title: 'Synthesize', detail: 'intro + mental models + glossary + what\'s-new-2026' },
    { title: 'Spend', detail: 'spend & compensation guidance — data with caveats + tech-lead decisions' },
    { title: 'Signoff', detail: 'lead resolves caveats and signs off cleanly' },
  ],
}

const AT = 'general-purpose'
let A = args; if (typeof A === 'string') A = {}; if (!A || typeof A !== 'object') A = {}
const TODAY = (typeof A.today === 'string' && A.today.trim()) ? A.today.trim() : '2026-06-25'
const FRESH = `IMPORTANT: it is ${TODAY}. SEARCH THE WEB for the CURRENT state of the art as of June 2026 — do not rely on stale training knowledge.`
const LABELS = `Label factual claims sourced(url+date) / inference / speculation; label learning-design and org recommendations "advisory". Plain language for a HIGHLY INTELLIGENT reader — simple words, real depth, no jargon-as-fog.`
const existingDigest = Array.isArray(A.existingDigest) ? A.existingDigest : []

const NEW = [
  { slug: 'constitutional-ai-deliberative-alignment', name: 'Constitutional AI 2.0 & Deliberative Alignment' },
  { slug: 'distillation-small-model-specialization', name: 'Distillation & Small-Model Specialization (incl. on-policy distillation)' },
  { slug: 'ssm-mamba-architectures', name: 'Hybrid SSM / Mamba Architectures (the post-Transformer shift)' },
  { slug: 'long-context-memory-architectures', name: 'Long-Context Memory Architectures & Context Engineering' },
  { slug: 'agent-evaluation-observability', name: 'Agent Evaluation & Observability (trajectory-level)' },
  { slug: 'diffusion-llms', name: 'Diffusion LLMs (dLLMs)' },
  { slug: 'on-device-edge-inference', name: 'On-Device / Edge LLM Inference' },
  { slug: 'any-to-any-multimodal', name: 'Native Any-to-Any Multimodal Models' },
]

log(`masterclass-addendum: ${NEW.length} new chapters, as of ${TODAY}`)

const CLAIM = { type: 'object', additionalProperties: false, required: ['statement', 'label'],
  properties: { statement: { type: 'string' }, label: { type: 'string', enum: ['sourced', 'inference', 'speculation', 'contested', 'advisory'] }, source: { type: 'string' }, date: { type: 'string' } } }
const SUB = { type: 'object', additionalProperties: false, required: ['markdown'], properties: { markdown: { type: 'string' }, sources: { type: 'array', items: { type: 'string' } }, claims: { type: 'array', items: CLAIM } } }
const VERIFY = { type: 'object', additionalProperties: false, required: ['overallConfidence', 'corrections'], properties: { overallConfidence: { type: 'string', enum: ['high', 'medium', 'low'] }, corrections: { type: 'array', items: { type: 'string' } }, flags: { type: 'array', items: { type: 'string' } } } }
const CHAPTER = { type: 'object', additionalProperties: false, required: ['technique', 'slug', 'markdown', 'oneLine'], properties: { technique: { type: 'string' }, slug: { type: 'string' }, oneLine: { type: 'string' }, markdown: { type: 'string' }, sources: { type: 'array', items: { type: 'string' } } } }
const MD = { type: 'object', additionalProperties: false, required: ['markdown'], properties: { markdown: { type: 'string' }, sources: { type: 'array', items: { type: 'string' } } } }
const SYNTH = { type: 'object', additionalProperties: false, required: ['executiveIntro', 'mentalModels', 'glossary', 'whatsNew2026'], properties: { executiveIntro: { type: 'string' }, mentalModels: { type: 'string' }, glossary: { type: 'string' }, whatsNew2026: { type: 'string' } } }
const SIGNOFF = { type: 'object', additionalProperties: false, required: ['signedOff', 'decisionsLog'], properties: { signedOff: { type: 'boolean' }, acceptedGaps: { type: 'array', items: { type: 'string' } }, decisionsLog: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['decision', 'fork', 'rationale', 'confidence'], properties: { decision: { type: 'string' }, fork: { type: 'string' }, rationale: { type: 'string' }, confidence: { type: 'string' }, flagForUser: { type: 'boolean' } } } } } }

// ---- Phase 1: build 8 new chapters -----------------------------------------
phase('Chapters')
function subs(ch) {
  const ctx = `TECHNIQUE: ${ch.name}\n${FRESH}\n${LABELS}`
  return [
    { k: 'mechanics', brief: 'Explain MECHANICS for a smart non-implementer: (1) WHAT it is, (2) HOW it works — mechanism/algorithm + intuition, (3) WHY it works — the principle and why the naive alternative fails, (4) PEOPLE & RESOURCES — team/roles, compute, time, money, data scale (orders of magnitude with basis).' },
    { k: 'scenarios', brief: 'Write SCENARIOS & STORIES: concrete narratives of where this technique is appropriate and effective, and where it is the WRONG tool.' },
    { k: 'cross-industry', brief: 'Write CROSS-INDUSTRY USAGE & POSITIONING across ALL industries (healthcare, finance, legal, customer support, coding/dev tools, robotics, defense, consumer, science), where it is table-stakes vs cutting-edge, who leads, and the June-2026 state of the art.' },
    { k: 'curriculum', brief: 'Write the LEARNING PATH for a technical LEADER (not an implementer): core mental models, a short concepts-only progression, a curated reading spine, understanding-checkpoints, and HOW TO EVALUATE AN EXPERT in an interview (questions, strong vs weak answers, red flags). No coding labs.' },
    { k: 'team', brief: 'Write TEAM NOTES: roles/seniority needed (or whether an existing role absorbs it), hiring signals & red flags, build-vs-buy (default rent/buy unless owning is a real moat), and common failure modes.' },
  ].map((s) => ({ ...s, prompt: `${s.brief}\n\n${ctx}` }))
}
async function research(ch) {
  const r = (await parallel(subs(ch).map((s) => () => agent(s.prompt, { label: `ch:${ch.slug}:${s.k}`, phase: 'Chapters', schema: SUB, agentType: AT }).then((x) => ({ k: s.k, x }))))).filter((y) => y && y.x)
  return { ch, subs: r }
}
async function verify(res) {
  const text = res.subs.map((s) => `[${s.k}]\n${s.x.markdown}`).join('\n\n')
  const v = await agent(`You are an adversarial fact-checker with deep ML knowledge. ${FRESH} Scrutinize the content about "${res.ch.name}". Flag anything technically WRONG, any misleading simplification, any stale (not June-2026) claim, and inference stated as fact. Return confidence + specific corrections.\n\n${text}`, { label: `verify:${res.ch.slug}`, phase: 'Chapters', schema: VERIFY, agentType: AT })
  return { ...res, v }
}
async function assemble(res) {
  const byk = {}; res.subs.forEach((s) => { byk[s.k] = s.x })
  const p = (k) => (byk[k] && byk[k].markdown) || '(missing)'
  const corr = res.v ? `VERIFIER (${res.v.overallConfidence}) — APPLY:\n${(res.v.corrections || []).map((c) => `- ${c}`).join('\n')}` : ''
  const ch = await agent(`You are the lead editor + technical translator. Assemble the FINAL chapter on "${res.ch.name}" for a highly intelligent technical leader. ${LABELS} Apply verifier corrections. Start "# ${res.ch.name}". Produce EIGHT sections: 1 What it is, 2 How it works, 3 Why it works, 4 People & resources, 5 Scenarios & stories, 6 Cross-industry usage & positioning (June 2026), 7 Learning path for a technical leader (mental models, reading spine, checkpoints, how to evaluate an expert), 8 Team notes. End with "Sources". Return a one-sentence oneLine too.\n\n## mechanics\n${p('mechanics')}\n## scenarios\n${p('scenarios')}\n## cross-industry\n${p('cross-industry')}\n## curriculum\n${p('curriculum')}\n## team\n${p('team')}\n\n${corr}`, { label: `assemble:${res.ch.slug}`, phase: 'Chapters', schema: CHAPTER, agentType: AT })
  const src = []; res.subs.forEach((s) => (s.x.sources || []).forEach((u) => src.push(u)))
  return ch ? { ...ch, slug: ch.slug || res.ch.slug, _sources: Array.from(new Set(((ch.sources || []).concat(src)).filter(Boolean))) } : null
}
const newChapters = (await pipeline(NEW, research, verify, assemble)).filter(Boolean)
log(`New chapters built: ${newChapters.length}/${NEW.length}`)

// ---- full digest (existing + new) ------------------------------------------
const fullDigest = existingDigest.concat(newChapters.map((c) => ({ technique: c.technique, slug: c.slug, oneLine: c.oneLine })))
const digestStr = fullDigest.map((d) => `- ${d.technique}: ${d.oneLine || ''}`).join('\n')

// ---- Phase 2-4: re-synthesis over the full set -----------------------------
phase('Curriculum')
const curriculum = await agent(`You are a learning architect for a highly intelligent technical LEADER (concepts + leadership, NO coding labs). ${LABELS} Design THE LEADER'S CURRICULUM across the FULL technique set below — genuinely SEQUENCED, not a flat list: dependency order, what to learn first, a progression (foundations -> training stack -> serving -> safety/eval/alignment -> data -> product craft -> the 2026 frontier), understanding-checkpoints, and a curated reading spine, as an 8-12 week part-time roadmap. Integrate the 8 newly added techniques (Constitutional AI 2.0, distillation, SSM/Mamba, long-context, agent-eval, diffusion LLMs, on-device, multimodal) into the right places. Output markdown starting "## The Leader's Curriculum".\n\nTECHNIQUES:\n${digestStr}`, { label: 'curriculum', phase: 'Curriculum', schema: MD, agentType: AT })

phase('Team')
const team = await agent(`You are an org/hiring strategist. ${FRESH} ${LABELS} Design THE TEAM-BUILDING BLUEPRINT for an applied-LLM product org (AI therapy as worked example, kept general): core roles and what each owns; first-5 then first-15 HIRING SEQUENCE matched to stage/budget; interview signals per role; realistic June-2026 budget ranges; build-vs-buy per capability (default rent/buy unless owning is a real moat); and the GRADUATION PATH from renting to training/owning models. Account for the full technique set incl. the 8 new ones. Output markdown starting "## The Team-Building Blueprint".\n\nTECHNIQUES:\n${digestStr}`, { label: 'team', phase: 'Team', schema: MD, agentType: AT })

phase('Synthesize')
const synth = await agent(`You are the lead editor + technical translator. ${LABELS} Write: 1 executiveIntro (how to use this; the single most important truth), 2 mentalModels (the cross-cutting ideas that unlock the rest), 3 glossary (tight plain-language), 4 whatsNew2026 (what's genuinely new/shifting in 2026, now including Constitutional AI 2.0/deliberative alignment, diffusion LLMs, SSM/Mamba, on-device, any-to-any multimodal, agent-eval). Account for the full ~30-technique set.\n\nTECHNIQUES:\n${digestStr}`, { label: 'synthesize', phase: 'Synthesize', schema: SYNTH, agentType: AT })

// ---- Phase 5: spend & comp guidance (data WITH caveats + decisions) ---------
phase('Spend')
const spend = await agent(`You are the senior research lead acting as a technical leader's advisor. The user asked: regarding SPEND, add the data WITH CAVEATS and make intelligent tech-lead decisions. Read the existing compensation/spend analysis in research/ai-therapy/ENGINEERING-DEEP-DIVE.md and research/ai-therapy/REPORT.md for grounding. ${FRESH} ${LABELS}

Write a "Spend & Compensation Guidance" section that: (1) states the relevant spend/comp DATA — engineering comp bands (disclosed floor vs. likely-real >$1M for elite ICs), build cost per technique tier (rent vs. fine-tune vs. train), and infra/compute spend — each WITH ITS CAVEAT (what's sourced vs inferred, why public figures understate); and (2) makes EXPLICIT TECH-LEAD DECISIONS/RECOMMENDATIONS: a default budget posture, where to spend vs. save, what to rent vs. own, the comp bands to actually budget for key roles, and the decision rule for each. Be decisive — this resolves the earlier open caveats by converting them into stated decisions. Output markdown starting "## Spend & Compensation Guidance".`, { label: 'spend-guidance', phase: 'Spend', schema: MD, agentType: AT })

// ---- Phase 6: clean sign-off -----------------------------------------------
phase('Signoff')
const signoff = await agent(`You are the senior research lead. The 8 new chapters are added, the curriculum/team/blueprint are re-synthesized over the full ~30-technique set, and spend/comp is now resolved into a guidance section with caveats + explicit decisions. Give a CLEAN final sign-off: set signedOff=true. Record the decisions log (flagForUser=true for consequential calls) and any genuinely-residual caveats (should be few — most prior caveats are now resolved into the spend guidance). As of ${TODAY}.\n\nNEW CHAPTERS: ${newChapters.map((c) => c.technique).join('; ')}`, { label: 'lead-signoff', phase: 'Signoff', schema: SIGNOFF, agentType: AT })
log(`Sign-off: signedOff=${signoff && signoff.signedOff}`)

const allSources = []
newChapters.forEach((c) => (c._sources || []).forEach((u) => allSources.push(u)))
;[curriculum, team, spend].forEach((x) => (x && x.sources || []).forEach((u) => allSources.push(u)))

return {
  asOf: TODAY,
  newChapters: newChapters.map((c) => ({ technique: c.technique, slug: c.slug, oneLine: c.oneLine, markdown: c.markdown })),
  curriculumMarkdown: (curriculum && curriculum.markdown) || '',
  teamBlueprintMarkdown: (team && team.markdown) || '',
  executiveIntro: (synth && synth.executiveIntro) || '',
  mentalModels: (synth && synth.mentalModels) || '',
  glossary: (synth && synth.glossary) || '',
  whatsNew2026: (synth && synth.whatsNew2026) || '',
  spendGuidanceMarkdown: (spend && spend.markdown) || '',
  signoff,
  sources: Array.from(new Set(allSources.filter(Boolean))),
}
