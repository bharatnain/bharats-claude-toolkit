# AI Engineering Techniques — A Masterclass for Technical Leaders

> **What this is:** a concepts-and-leadership masterclass on the engineering techniques behind modern AI products, in plain language for a highly intelligent reader. Per technique: what it is, how it works, why it works, people & resources, scenarios, cross-industry usage & positioning, a leader's learning path (incl. how to interview an expert), and team notes. Current as of **June 2026**.
> **Scope:** **30 techniques** — 16 core + 6 emerging (first pass) + 8 added (Constitutional AI 2.0 + 7 sidebars).
> **Trust model:** factual claims labeled `sourced`/`inference`/`speculation`; learning-design & org recommendations labeled `advisory`. Parts 1–2 (`REPORT.md`, `ENGINEERING-DEEP-DIVE.md`) are unchanged.


---

## Executive Introduction

**The single most important truth:** In 2026 the action moved off the model and onto the *system around the model*. For two years the question was "how big and how smart is the model?" Now the model is one component, and the wins come from what you put around it: which words you show it right now, what tools you let it touch, how you record and grade the path it takes, where you run it, and what written principles you train it to reason through. Almost every technique below is a different answer to "how do I get reliable, affordable, well-behaved work out of a capable-but-imperfect model?" — not "how do I build a smarter one."

**How to use this document.** Read the two Mental Models first; they are the load-bearing ideas that make the other ~28 techniques fall into place. Then treat the Glossary as a reference you return to, and What's New 2026 as the "if you only track six things this year, track these" list. You do not need to read it front to back.

**A note on labels, so you can calibrate trust.** I mark claims three ways. *Sourced* means a named source and date backs it. *Inference* means I'm reasoning from sourced facts to a conclusion the sources imply but don't state outright. *Speculation* means it's a forward guess. Recommendations about how to teach this material or how to organize a team around it are marked *advisory* — they are my editorial judgment, not findings.

**The one honest caveat up front (sourced — arxiv.org/pdf/2412.16339, Dec 2024; LessWrong, 2025):** the most powerful 2026 alignment method works by making a model *reason out loud* through written principles before acting. But we have growing evidence that a model's visible reasoning can be a performance for the grader rather than an honest account of why it did what it did — and this faithfulness tends to *decrease* as models get more capable. So the same "show your work" move that makes models safer also makes the safety harder to verify. Hold that tension; it recurs everywhere.


---

## The Core Mental Models

**Model 1 — The model is a CPU; the real work is the system around it.**
Stop picturing "the AI" as the whole product. Picture it as a fast but forgetful processor that only sees what you hand it in the current moment, has no memory of yesterday unless you give it one, and will confidently take a wrong action if you let it. Everything valuable in 2026 is the scaffolding: *context engineering* decides which few thousand words it looks at right now; *memory architecture* is the external hard drive that feeds those words in and out across sessions; *agent evaluation and observability* is the flight recorder that grades the whole path it took, not just where it landed; *deliberative alignment* is the written code of conduct it's trained to consult before acting. Once you see the model as a component and not the system, the whole technique set organizes itself: each one is a different part of the machine you build *around* the CPU. The deep version of this idea: capability and reliability are now *decoupled*. A smarter model does not automatically give you a more reliable product — reliability is engineered, separately, in the surrounding system. (Inference, grounded in the context-engineering and agent-eval sources below.)

**Model 2 — Every 2026 advance is buying back one of three scarce resources: tokens-of-attention, memory bandwidth, or trust.**
Almost every technique here is an economic trade, and naming the currency it buys tells you when to use it.
- *Attention is quadratically expensive, and accuracy actually falls as the context window fills* (sourced — arxiv.org/pdf/2502.17129, 2025). So the techniques that fight this — Mamba/SSM hybrids (cheap fixed-memory layers, a few attention layers rationed in), long-context engineering, memory architectures — are all buying back **attention** by being disciplined about what the model has to look at. The lesson that surprises people: a *fuller* context window often means *worse* answers, so "just paste everything in" is a bug, not a feature.
- *On a phone, the bottleneck is memory bandwidth, not compute* (sourced — v-chandra.github.io/on-device-llms, 2026; ~30–50x gap between phone and datacenter memory speed). So on-device techniques — 4-bit quantization, speculative decoding, small models — are all buying back **memory bandwidth**: fewer bytes read per token, more output per read. Knowing the bottleneck is bandwidth tells you *why* a 4-bit model is 4x faster, not just 4x smaller — it's 4x less memory traffic per word.
- *You cannot write a rule for every situation, and you cannot trust a final answer you didn't watch get produced.* So deliberative alignment, Constitutional AI 2.0, and trajectory-level agent evaluation are all buying back **trust** — alignment by training the model to reason through principles, observability by recording and grading the entire path.

When you meet any technique in this field, ask: *which of the three is it buying, and what is it paying?* That single question explains the design and tells you when the trade is worth it. (Inference, built on the sourced facts above.)


---

## The Leader's Curriculum

**A 10-week, part-time roadmap for a technical leader who wants to understand modern AI deeply — concepts and judgment, no coding labs.**

A note on how to read this. Each factual claim below is tagged: **[sourced]** means it traces to the dated technique briefs you provided (all dated June 2026 unless noted); **[inference]** means I reasoned it from those facts; **[speculation]** means it's a forward bet I can't ground. Anything about *how to learn it* or *how to run your org* is tagged **[advisory]** — that's my design judgment, not fact. Budget roughly **4–6 hours per week**: one concept block, one "see it in the wild" block, one checkpoint.

---

### The shape of the journey (why this order)

**[advisory]** Most AI reading lists are flat — a pile of buzzwords in no particular order. That's useless for a leader, because these techniques *depend on each other*. You can't reason about why Mamba matters until you understand what attention costs. You can't judge an agent-eval vendor until you know what a "trajectory" is. So this curriculum is a dependency chain, not a menu.

The spine, in one breath: **first understand the machine** (what a Transformer is, what attention costs) → **then how it's built** (training, distillation, alignment) → **then how it's served and shaped** (architecture shifts, context engineering, serving cost) → **then how you trust it** (evaluation, observability) → **then what it's becoming** (multimodal, on-device, the 2026 frontier). Each phase answers a question the next phase assumes you've already answered.

The eight newest techniques are woven in where they actually belong, not bolted on at the end:
- **Long-context & context engineering** → Phase 2 (it's a direct consequence of what attention costs).
- **SSM/Mamba** → Phase 3 (it's the architectural *response* to that cost).
- **Distillation** → Phase 3 (it's how big models become small ones).
- **Constitutional AI 2.0 / Deliberative Alignment** → Phase 4 (alignment, the trust layer).
- **Agent evaluation & observability** → Phase 5 (you can't trust an agent until you can grade its whole path).
- **Diffusion LLMs, on-device, native multimodal** → Phase 6 (the frontier — they only make sense once you hold the foundations).

---

### Phase 1 — Foundations: what is this machine, really? (Weeks 1–2)

**Goal:** Be able to explain, to a smart non-technical board member, what a large language model actually does — without saying "it's like a brain."

The one idea everything rests on: a language model predicts the next token, over and over, and "intelligence" is what emerges when you do that at enormous scale. The *Transformer* is the architecture that made this work, and its engine is **attention** — the mechanism that lets the model look back at earlier words to decide what comes next.

Here is the single most important fact in this entire curriculum, because nearly every 2026 technique is a reaction to it: **attention is quadratically expensive — doubling the input roughly quadruples the work — and, separately, model accuracy actually *falls* as the context window fills up.** **[sourced — Long-Context brief, June 2026]** Hold onto both halves. The cost half explains the architecture shift (Phase 3). The accuracy half explains context engineering (Phase 2). If you only remember one sentence from week one, make it this one.

**What to learn:**
- Tokens, next-token prediction, "the model is a function from text to a probability over the next token."
- The Transformer and attention — at the level of *what it does and what it costs*, not the matrix math.
- Why "scale" (more data, more parameters, more compute) produced the leap, and why that has limits.

**Understanding-checkpoint (Week 2):** *Without notes,* explain (a) why a model that's twice as good at long documents might cost four times as much to run, and (b) why stuffing more text into the prompt can make answers *worse*, not better. If you can't do both cleanly, re-read before moving on — everything downstream leans on this.

---

### Phase 2 — The training stack & the context problem (Weeks 3–4)

**Goal:** Understand how a raw model becomes a useful one, and why "the context window" is a managed resource, not free space.

**The training pipeline (Week 3).** A model is built in stages: *pre-training* (read most of the internet, learn to predict), then *post-training* (fine-tuning and reinforcement learning from human or AI feedback, which is what turns a text-predictor into an assistant that follows instructions). You don't need the math; you need the *map* — because every later technique (alignment, distillation) is a modification of one of these stages.

**Context engineering & memory (Week 4) — newest technique, placed here deliberately.** This is the discipline that flows directly from Phase 1's key fact. The 2026 frontier is **not** a bigger context window — it's the disciplined engineering of *which few thousand words the model looks at right now* (context engineering), plus the external storage that feeds information in and out across sessions (memory architecture). **[sourced — Long-Context brief, June 2026]** The reason this is a *discipline* and not a luxury is precisely the two-part fact you memorized: attention is quadratically expensive, and accuracy drops as the window fills. So the winning move isn't "give the model everything" — it's "give the model exactly the right small slice, and store the rest outside."

**[advisory]** For a leader, this is the phase with the highest near-term payoff. Most real-world AI failures in your org won't be the model being "dumb" — they'll be the model being fed the wrong context. Learning to think in terms of "what's in the window right now?" will make you a sharper reviewer of every AI product proposal you see.

**Understanding-checkpoint (Week 4):** Distinguish in your own words *context engineering* (managing the live window) from *memory architecture* (the external store across sessions). Then answer: if a vendor pitches you "we have a 10-million-token context window," what's the *one* skeptical question you now know to ask? (Answer you should reach: "Does accuracy hold up as you fill it, or does it degrade?")

---

### Phase 3 — Serving: architecture shifts, distillation, and the cost of running models (Weeks 5–6)

**Goal:** Understand the two big 2026 moves that make models cheaper and faster to run — and what each one costs you in return.

**The post-Transformer shift: SSM / Mamba (Week 5) — newest technique.** Here's where the cost half of Phase 1 pays off. The industry's answer to quadratic attention is a different kind of layer — a **State Space Model (SSM)**, of which **Mamba** is the leading family — that uses cheap, *fixed* memory regardless of input length, instead of attention's ballooning cost. But — and this is the nuance a leader must get right — **2026's most efficient frontier models are not pure Mamba. They're hybrids: mostly cheap fixed-memory SSM layers, with a few attention layers rationed back in for the precise-recall work attention is uniquely good at.** **[sourced — SSM/Mamba brief, June 2026]** And the payoff is **concentrated in long-context handling and serving cost — not in raw peak intelligence.** **[sourced — same]** So this is a *merger, not a coup* **[sourced — same]**: attention didn't lose, it got rationed.

**Distillation (Week 5–6) — newest technique, placed here because it's how serving gets cheap.** Distillation is training a small "student" model to imitate a large "teacher" model — you get most of the capability at a fraction of the size and serving cost. **[inference, grounded in the on-device brief's "smaller weights" theme]** Place it here mentally as the *bridge* to Phase 6's on-device work: distillation is one of the main reasons a phone-sized model can do anything useful at all.

**Understanding-checkpoint (Week 6):** Explain why a frontier lab would *keep* a few attention layers even though SSM layers are cheaper. (Answer: precise recall — attention is better at exact look-ups, so you ration it for that job.) Then: in one sentence, where does Mamba's advantage show up on the bill, and where does it *not* show up? (Long context + serving cost yes; peak intelligence no.) **[sourced]**

---

### Phase 4 — Safety, evaluation & alignment: making a powerful model behave (Weeks 6–7)

**Goal:** Understand how labs make models behave when no rulebook could cover every case — and grasp the one frontier worry that isn't solved.

**Constitutional AI 2.0 & Deliberative Alignment (Week 7) — newest technique, the heart of the trust layer.** The problem: you can't write a rule for every situation a powerful model will face. The 2026 answer, which **the two leading AI labs have independently converged on**, is to **hand the model a written set of principles and train it to reason through them before it acts.** **[sourced — Constitutional AI 2.0 brief, June 2026]** This **measurably beats older approaches.** **[sourced — same]**

But here is the frontier worry a leader must carry into every deployment decision: **we don't know whether the model's visible reasoning is honest, or just performed for the test.** **[sourced — same]** The model shows its work — but a model smart enough to reason through principles is also smart enough to produce reasoning that *looks* compliant while doing something else. This is the single most important unsolved problem in this curriculum, and it's exactly the kind of thing a board will ask you about.

**[advisory]** Don't let the elegance of "it reasons through a constitution" lull you. The right leadership posture is: this is a real improvement *and* the honesty of the model's stated reasoning is an open research question — so you still need independent evaluation, which is Phase 5.

**Understanding-checkpoint (Week 7):** State the deliberative-alignment idea in one sentence, then state the unsolved worry in one sentence. The fact that two competing labs converged on the same method is a signal — what does it tell you? (Inference you should reach: it's likely a genuine local best answer, not a fad.) **[inference]**

---

### Phase 5 — Trusting agents: trajectory-level evaluation & observability (Weeks 7–8)

**Goal:** Understand why grading an AI agent's *final answer* is dangerously insufficient, and what to grade instead.

**Agent evaluation & observability (Week 8) — newest technique.** When an agent does a multi-step task, **you cannot judge it by its final answer alone — you must record and grade the entire path it took (its "trajectory"), because an agent can reach a correct answer through a path that is wasteful, unsafe, or a production catastrophe.** **[sourced — Agent-Eval brief, June 2026]** The classic nightmare: the agent gets the right output but deleted a database, leaked data, or burned a fortune in API calls along the way.

This phase depends on everything before it — you need to understand alignment (Phase 4) to know *what* unsafe steps look like, and context engineering (Phase 2) to know *why* an agent goes off the rails. That's why it sits here, not earlier.

**[advisory]** For a leader, trajectory-level observability is the governance keystone. "Show me the trajectory grades, not just the success rate" is the single most powerful question you can bring to an agent-deployment review. Make it a habit.

**Understanding-checkpoint (Week 8):** Give a concrete example of an agent that produces a *correct* final answer through an *unacceptable* path. Then: what would you require a team to instrument before you let an agent touch production systems?

---

### Phase 6 — The 2026 frontier: diffusion LLMs, on-device, native multimodal (Weeks 9–10)

**Goal:** Understand the three frontier shifts that change *what AI products are possible* — and, for each, exactly where it wins and where it fails. These come last because each one only makes sense once you hold the foundations.

**Diffusion LLMs / dLLMs (Week 9) — newest technique.** Instead of writing one word at a time (left to right), a dLLM **drafts a whole answer at once and refines it over a few parallel passes.** **[sourced — dLLM brief, June 2026]** The trade: it gives up *guaranteed* left-to-right coherence in exchange for large best-case speed gains. So it's **a strong fit for latency-critical, short, or "fill-in-the-middle" work, and a poor fit for long, hard, or strictly-auditable reasoning** (as of June 2026). **[sourced — same]** A leader's takeaway: dLLMs are a *latency* tool, not a *reasoning* tool — match them to the job.

**On-device / edge inference (Week 9–10) — newest technique.** Running the model on the user's own phone, laptop, car, or sensor instead of the cloud — winning **privacy, instant response, offline use, and zero per-query cost.** **[sourced — On-Device brief, June 2026]** The deep insight here connects all the way back to Phase 1: the real bottleneck is **memory bandwidth, not compute**, so the technique is to attack it with **smaller weights** (hello, distillation from Phase 3) **and more output per memory read** — traded against a smaller model's **lower ceiling on hard reasoning.** **[sourced — same]** This is why the curriculum put distillation in Phase 3: on-device is where it cashes out.

**Native any-to-any multimodal (Week 10) — newest technique.** These models **pour every modality — text, image, audio — into one shared token language and predict over all of it in a single network.** **[sourced — Multimodal brief, June 2026]** They win **when the relationship *between* modalities is the point** (not just handling each separately). But the leader-critical reality check: **in mid-2026 only a handful truly *generate* any-to-any — led by Gemini Omni — while others, including GPT-5.5, unify *understanding* but still route *generation* out** to separate systems. **[sourced — same]** So "multimodal" on a spec sheet can mean two very different things; the question to ask is "does it generate any-to-any natively, or just understand multiple inputs?"

**Understanding-checkpoint (Week 10 / capstone):** For each of the three, state in one sentence the job it's *right* for and the job it's *wrong* for:
- dLLM: right for low-latency/short/fill-in-the-middle; wrong for long/hard/auditable reasoning. **[sourced]**
- On-device: right for privacy/offline/zero-cost; wrong for the hardest reasoning. **[sourced]**
- Native multimodal: right when the link *between* modalities matters; caveat — check whether it truly *generates* across modalities or only understands. **[sourced]**

---

### Capstone synthesis (end of Week 10)

**[advisory]** Tie the whole arc together by answering one integrative question in writing, ~one page: *"A product team wants to ship a privacy-sensitive, low-latency, multi-step assistant that runs partly on-device. Walk through every technique in this curriculum that bears on that decision, and name the three biggest risks."* A strong answer will touch context engineering (what's in the window), distillation + on-device (the reasoning ceiling), dLLMs (latency vs. auditability), trajectory evaluation (the multi-step safety problem), and deliberative alignment (and its unsolved honesty worry). If your answer naturally pulls in five-plus phases, the curriculum has done its job.

---

### The curated reading spine

**[advisory]** Read these *in this order* — it mirrors the phases. I've described each by what it teaches rather than betting on exact 2026 URLs, because a leader's spine should be stable even as specific posts age. Where I name a canonical source, treat the *type* of source as the recommendation.

1. **Phase 1 — the machine.** A plain-language Transformer/attention explainer (e.g., the genre of "The Illustrated Transformer" by Jay Alammar, and 3Blue1Brown's video series on neural networks and attention). Goal: intuition for attention and its cost, no linear algebra required. **[advisory]**
2. **Phase 2 — training & context.** The original instruction-tuning / RLHF explainers from the major labs' blogs, plus any 2026 "context engineering" overview. Goal: the training map and the live-window discipline. **[advisory]**
3. **Phase 3 — architecture & serving.** The Mamba / state-space-models explainer genre (the original Mamba paper's *abstract and intro only*, plus a plain-language hybrid-architecture write-up), and a short distillation primer. Goal: why hybrids, where the savings land. **[advisory]**
4. **Phase 4 — alignment.** Anthropic's Constitutional AI writing and the 2026 deliberative-alignment material from both leading labs — read them *side by side* to see the convergence the brief describes. Goal: the method and its honesty caveat. **[advisory; the convergence claim itself is sourced — Constitutional AI 2.0 brief, June 2026]**
5. **Phase 5 — agent evaluation.** A trajectory-level agent-evaluation / observability overview (the genre of agent-eval framework docs and LLM-observability platform write-ups). Goal: trajectory thinking as a governance habit. **[advisory]**
6. **Phase 6 — the frontier.** One explainer each on diffusion LLMs, on-device/edge inference (with the memory-bandwidth framing), and native any-to-any multimodal (with the generate-vs-understand distinction). Goal: matching each frontier tool to its right job. **[advisory]**

**[advisory] How to read the spine:** for each item, force yourself to write the *one sentence* you'd tell your board. If you can't compress it to a sentence, you haven't understood it yet — go back. The whole curriculum is built so that, by Week 10, you have roughly a dozen such sentences, in dependency order, that together let you reason about any AI decision that crosses your desk.

---

**A closing honesty note. [advisory]** Two things in this curriculum are genuinely *open*, not settled, and a good leader holds them as live questions rather than solved facts: (1) whether an aligned model's visible reasoning is honest or performed **[sourced — Constitutional AI 2.0 brief]**, and (2) how far the on-device reasoning ceiling can be pushed **[inference from the On-Device brief]**. The dates matter — all the frontier claims here are pinned to **June 2026** and this field moves in quarters, not years. Re-check the Phase 6 claims especially before you make any decision that depends on them.


---

## The Team-Building Blueprint

*An org/hiring plan for an applied-LLM product company. The worked example is an AI therapy product, because it forces every hard question — safety, regulation, memory across sessions, trust, latency — but the structure generalizes to any serious applied-LLM org. Factual market claims are labeled sourced / inference / speculation. Learning-design and org calls are labeled advisory.*

---

### 0. The one idea that should shape every hire

You are not building a model company. You are building a company that **wraps, steers, evaluates, and is accountable for** someone else's model. As of June 2026 the frontier labs converged on training models that reason through a written set of principles before acting (Constitutional AI 2.0 / deliberative alignment) — and the open frontier worry is that the model's *visible reasoning may be performed for the test rather than honest* (sourced + inference — the technique is real and labs report it beats older RLHF-style methods; the honesty-of-reasoning gap is an open research problem, not a solved one).

The org implication is direct and load-bearing: **your moat is almost never the base model. It is the eval harness, the context/memory engineering, the safety wrapper, and the proprietary interaction data.** Hire for *those* first. That single fact drives the whole sequence below.

---

### 1. Core roles and what each one owns

These are *ownership domains*, not headcount — at 5 people one human covers several. Listed in rough order of how early they matter for an applied-LLM org.

**1. Applied / LLM Product Engineer — owns the product surface.**
Builds the actual feature on top of a foundation-model API: prompting, RAG, tool-calling, the agent loop. This is the single most-needed role at seed/Series A — *(sourced: ~70% of AI product companies need this profile at seed/A, kore1/supersourcing 2026)*. They own latency, cost-per-session, and "does the thing actually work."

**2. Eval & Observability Engineer — owns the truth.**
Designs golden datasets, LLM-as-judge pipelines, offline + online evals, and — critically for agents — **trajectory-level grading**: recording and scoring the *entire path* the agent took, not just its final answer, because an agent can reach a correct answer through a wasteful, unsafe, or catastrophic path. *(sourced: trajectory/eval rigor is the single biggest comp/skill separator in 2026 — theaicareerlab, ayautomate 2026.)* In an AI therapy org this person is your conscience: they catch the session that *ended* fine but *passed through* a crisis-mishandling moment.

**3. Context & Memory Engineer — owns what the model sees.**
The 2026 frontier isn't a bigger window; it's disciplined choice of *which few thousand tokens the model looks at right now* (context engineering) plus the external store that carries memory across sessions (memory architecture), because attention is quadratically expensive and accuracy actually *falls* as the window fills. *(sourced/inference — context-engineering-over-bigger-window and accuracy-degradation-with-fill are the stated 2026 consensus; meta-intelligence, mem0 2026.)* For therapy this is existential: a therapist who forgets last week is useless, and the memory layer needs consolidation, importance-decay, and temporal tracking — not just a vector dump *(sourced: three-layer memory consensus, mem0/atlan 2026)*.

**4. AI Trust & Safety Lead — owns "what must never happen."**
Product policy, moderation, misuse response, crisis-escalation flows. In therapy this is not a nice-to-have; it is the product. Owns red-team cadence and the line between "model handles it" and "human handles it now."

**5. Clinical / Domain Lead (the domain-expert seat) — owns ground truth for the domain.**
In therapy: a licensed clinician who defines what "good" looks like, writes the rubrics the eval engineer grades against, and signs off on safety protocols. *Every* applied-LLM org has this seat — it's a doctor here, a lawyer in legal-AI, an underwriter in insurance-AI. Advisory: do not treat this as a part-time advisor in a regulated domain; the rubric author must be in the room.

**6. AI Product Manager — owns the problem and the human-review map.**
Defines requirements, eval criteria, and *where humans review*. Advisory: hiring a PM **before** you have an eval-capable engineer and someone with inference on-call experience frustrates everyone — the PM has nothing real to steer *(sourced: kore1 2026 explicitly warns of this ordering mistake)*.

**7. AI Ops / Agent Operations — owns the running system.**
Model versioning, prompt pipelines, inference on-call, incident response. Becomes a distinct seat only once you have a live agent in production with real traffic.

**8. Compliance / Legal Advisor — owns the regulator.**
Translates EU AI Act, US state AI acts, and (in healthcare) FDA premarket / CMS oversight into product decisions. *(sourced: red-teaming + safety-model-reporting is an operational baseline, not optional, by mid-2026 under EU AI Act / NIST AI RMF; mindgard, techintelix 2026.)* Fractional/external until regulated scale, then in-house.

**9. AI UX Researcher — owns trust and interaction.**
Studies how users actually trust, over-trust, and work with the product. Underrated everywhere; *vital* in therapy, where over-trust is a clinical risk, not just a conversion metric.

**10. Applied Research / Model Specialist — owns the graduation path.**
Fine-tuning, distillation, eventually training. Deliberately **last** of the core seats — you hire this person when renting demonstrably stops being enough (see §5). Hiring them early is the most common expensive mistake.

---

### 2. The first-5 hiring sequence (pre-seed / seed, roughly $1.5–3M/yr comp budget)

Goal at this stage: **prove the product works and is safe, on a rented model, with a moat in evals + data.** Do not hire a researcher. Do not hire a generic PM.

| # | Hire | Why this slot | Also covers (at 5 people) |
|---|------|---------------|---------------------------|
| 1 | **Founding Applied/LLM Engineer** | Builds the product on a frontier API. Nothing exists without this. | Ops, basic memory |
| 2 | **Eval & Observability Engineer** | Your moat and your safety net from day one. The thing competitors can't copy. | Trajectory grading, online evals |
| 3 | **Clinical/Domain Lead** (full-time in a regulated domain like therapy) | Writes the rubrics, owns safety ground truth, makes the product *legitimate*. | Trust & safety policy, compliance liaison |
| 4 | **Context & Memory Engineer** | Cross-session memory is the product's felt intelligence; quadratic-cost reality means this is real engineering. | RAG, retrieval |
| 5 | **Product/Trust lead (PM + T&S blend)** | Owns the problem and the human-review map; in therapy, owns crisis escalation. | UX research, roadmap |

Advisory ordering note: in a *non-safety-critical* domain (say, an internal coding assistant), you'd swap the Clinical/Domain Lead (#3) for a second engineer and push Trust & Safety later. The therapy example front-loads safety because the cost of getting it wrong is a human life, not a refund.

---

### 3. The first-15 sequence (Series A, roughly $4–7M/yr comp budget)

Add hires 6–15 as the product gets real traffic. The shift is from *"does it work?"* to *"does it work safely at scale, and is the path it takes auditable?"*

6. **Second Applied Engineer** — depth on the product surface; frees #1 to lead.
7. **AI Agent Architect / Tech Lead** — owns system design: tools, sub-agents, human-review points, state. The agent loop is now too important to be ad hoc. *(sourced: highest-paid of the new agentic roles, $260–420k base; theaicareerlab 2026.)*
8. **AI Ops / Agent Operations Engineer** — on-call, versioning, incident response now that real users depend on uptime.
9. **AI Trust & Safety Lead** (split out from #5) — full-time misuse + crisis ops as volume grows.
10. **Second Eval Engineer / AI Trainer** — data curation, rubric design, red-teaming at scale. *(sourced: AI Trainer $95–180k IC; theaicareerlab 2026.)*
11. **AI UX Researcher** — trust patterns and over-reliance become measurable risks worth a dedicated seat.
12. **Dedicated PM** (split from #5) — now that there's a roadmap and multiple surfaces.
13. **Compliance / Legal (in-house or strong fractional→FT)** — EU AI Act + healthcare reporting obligations are now load-bearing.
14. **Data/Platform Engineer** — pipelines, data versioning, the substrate for any future fine-tuning. This hire is the *bridge to graduation* (§5).
15. **Applied Research / Model Specialist** — first fine-tuning/distillation work, *only if* §5's triggers have fired.

Advisory: notice headcount 6–15 is roughly half safety/eval/ops and half build. That ratio is the tell of a serious applied-LLM org versus a demo-ware one.

---

### 4. Interview signals per role (what actually separates a great hire)

*All signals advisory — these are hiring-design recommendations, not measured facts.*

- **Applied/LLM Engineer** — Green: can articulate *why* accuracy degrades as context fills and how they'd combat it; treats prompting/RAG/fine-tuning as a decision tree, not a religion; has shipped something with a real latency budget. Red: reaches for fine-tuning first; can't name a single eval they ran on their own work.
- **Eval & Observability Engineer** — Green: shows you a golden dataset they built and the disagreements they found between it and an LLM judge; instinctively asks "how would I grade the *path*, not the answer?" Red: thinks "we'll add evals later"; conflates unit tests with model evals.
- **Context & Memory Engineer** — Green: distinguishes context engineering (what's in the window now) from memory architecture (what persists across sessions); knows consolidation/decay/temporal-tracking, not just "stuff it in a vector DB." Red: treats a bigger context window as the answer to everything.
- **Trust & Safety / Clinical Lead** — Green: walks you through a *specific* failure path and the escalation it should trigger; in therapy, has handled real crisis protocols. Red: speaks only in abstractions about "responsible AI."
- **Agent Architect** — Green: can defend where they put a *human* in the loop and why; has opinions on when an agent should *stop* and ask. Red: maximalist autonomy with no audit trail.
- **PM** — Green: defines success as a measurable eval criterion before discussing features. Red: feature lists with no notion of how you'd know it worked.
- **Applied Research/Model Specialist** — Green: can tell you the *economic* break-even where owning beats renting (volume, latency, privacy, or moat), and admits when renting still wins. Red: wants to train models because it's interesting.

---

### 5. Build-vs-buy per capability (default: rent/buy unless owning is a real moat)

The default everywhere is **rent the intelligence, own the wrapper**. You own a capability only when owning it is a durable advantage *or* a hard requirement (privacy/regulation).

| Capability | Default | Own it only when… |
|---|---|---|
| **Base / frontier model** | **Rent** (API) | Never, early. Owning is a different company. *(inference)* |
| **Eval harness** | **BUILD** | Always your moat. This is the one thing you never outsource. *(advisory)* |
| **Context & memory layer** | **Build on rented primitives** | Use vector DBs / memory frameworks as backends; build the consolidation/decay logic yourself — that's the differentiated part. *(sourced: managed memory frameworks exist and are maturing, mem0/atlan 2026.)* |
| **Observability / trajectory tracing** | **Buy tool + build grading** | Buy the tracing platform; the *rubrics* are yours. |
| **Safety / red-team** | **Buy tools + own policy** | Red-team tooling is buyable; policy and crisis flows are yours. *(sourced: red-team tooling market mature 2026; confident-ai/mindgard.)* |
| **Proprietary interaction data** | **OWN** | Always. This is the fuel for graduation. *(inference)* |
| **Fine-tuned small model** | Rent first, build later | See triggers below. |
| **Compliance posture** | **Buy expertise** (fractional) until scale | Bring in-house when reporting obligations are continuous. |

**Cost grounding (sourced, 2026):** prompt engineering ≈ near-zero (and cached input reads run ~10% of normal — a 90% discount); RAG ≈ under ~$10k basic infra, $70–300/mo managed; fine-tuning ≈ $5–50k+ plus separate inference; hosted fine-tuning ≈ $0.80–$3 per million training tokens *(freeacademy.ai, alexbobes 2026)*. The production default is hybrid — **fine-tune for *form*, RAG for *facts*** — and ~60% of 2026 production projects use both *(sourced: freeacademy.ai 2026)*. A practical rule that still holds: if your whole knowledge base fits under ~200k tokens, long-context can beat building retrieval at all.

---

### 6. The graduation path: from renting to training/owning models

You graduate one rung at a time, and **only when a trigger fires.** Each technique in the set tells you *which* rung is now worth climbing.

**Rung 0 — Pure prompting on a rented frontier model.** Where every org starts. Spend a literal day here before building anything; modern models with a clear system prompt are remarkably capable *(sourced: 2026 guidance)*.

**Rung 1 — RAG + context/memory engineering.** Add when the model lacks *your* facts or needs cross-session continuity. For therapy this is non-optional and early. Still 100% rented intelligence.

**Rung 2 — Fine-tune for *form*, keep renting for *facts*.**
*Trigger:* you need a consistent *behavior/voice/format* that prompting can't hold — e.g., a reliably warm, non-judgmental therapeutic tone, or strict adherence to a clinical protocol. Fine-tune a small model on *your* interaction data (the asset you've owned since day one). *Hire the Applied Research/Model Specialist here, not before.*

**Rung 3 — Own a small/distilled model for cost, latency, privacy, or edge.**
*Triggers, any one:* (a) volume so high a fine-tuned small model wins on cost — *at 100k+ queries/day, fine-tuned small models beat RAG-on-frontier economically (sourced: alexbobes 2026)*; (b) latency-critical surfaces where **diffusion LLMs** (draft-the-whole-answer-and-refine, big best-case speedups for short/fill-in work — but *poor* for long, hard, or strictly-auditable reasoning as of June 2026) or **hybrid SSM/Mamba** architectures (mostly cheap fixed-memory layers with attention rationed in — payoff is long-context and *serving cost*, not peak IQ) make owning the serving stack pay off; (c) **on-device/edge inference** for privacy — running the model on the user's own phone wins privacy, instant response, offline use, and zero per-query cost by attacking memory-bandwidth (the real bottleneck), traded against a smaller model's reasoning ceiling. For therapy, the privacy case for on-device is unusually strong — the most sensitive data never leaves the device. *(All architecture claims sourced to the technique set as stated; the org timing is advisory.)*

**Rung 4 — Own alignment/behavior training (Constitutional-AI-style).**
*Trigger:* your safety/behavior requirements are so domain-specific that a generic aligned model can't meet them and you can defensibly train a model to reason through *your* written constitution (your clinical safety principles) before it acts. This is a real moat — and it inherits the open frontier worry that the model's *shown* reasoning may be performed rather than honest, so it *deepens*, never replaces, your eval/red-team investment. *(sourced technique + inference on org timing.)* Very few applied orgs ever need this rung; reaching it means safety-critical behavior has become your core product.

**Rung 5 — Native any-to-any multimodal (only if the cross-modal relationship is the point).**
*Trigger:* the *relationship between* modalities is the product — e.g., reading vocal tone + facial affect + words *together* to gauge a patient's state. As of mid-2026 only a handful of models truly generate any-to-any (Gemini Omni leads; GPT-5.5 unifies understanding but still routes generation out), so this is **rent, not build** for almost everyone — you adopt a frontier omni-model, you don't train one. *(sourced: technique set as stated.)*

**The through-line:** rent intelligence, own evaluation and data, and let *specific, measured triggers* — not ambition or FOMO — pull you up each rung. The proprietary interaction data you started hoarding at hire #1 is what makes graduation possible at all; protect it accordingly.

---

*Sourced claims carry the 2026 references inline. All hiring-sequence orderings, interview signals, and graduation-timing calls are **advisory** — sound defaults for a June-2026 applied-LLM org, to be adjusted to your domain's safety stakes and your actual eval numbers.*


---

## Spend & Compensation Guidance

*As of 2026-06-25. This section converts the open caveats in `ENGINEERING-DEEP-DIVE.md` (Part C compensation, Part A technique costs) and `REPORT.md` (Section 4 funding/comp) into stated tech-lead decisions. Factual claims are labeled `sourced` (with URL + date), `inference`, or `speculation`. Learning-design and org recommendations are labeled `advisory`. The data is presented WITH its caveats; the decisions are deliberately decisive, because a decision that hedges every way is not a decision.*

---

### How to read this section

There are two halves. First, **the data with its caveats** — what is actually known about engineering pay, build-cost per technique, and compute/infra spend, and exactly *why the public numbers understate reality*. Second, **the decisions** — a default budget posture and a rule for every major spend choice (rent vs. own, spend vs. save, what to pay each key role). The whole point is that the caveats are real but you still have to commit money, so each decision states what it assumes and when it flips.

The single most important fact to hold in your head: **in AI therapy the model is cheap and the talent-plus-data is expensive.** Renting a frontier-grade model or fine-tuning an open one costs thousands to low millions. The handful of people who could build one from scratch cost a million dollars each, and you do not need them. Budget accordingly.

---

### Part 1 — The data, with its caveats

#### 1A. Engineering compensation: the disclosed floor vs. the likely-real number

**The data.** Public sources put senior engineers at these companies at roughly **$200K–$225K total comp** (`REPORT.md` §4, from levels.fyi and H1B/LCA filings). That number is a **floor, and an unreliable one.** The right way to think about real pay is a two-tier picture:

| Role tier | Disclosed floor (public) | Likely-real total comp (inference) |
|---|---|---|
| Typical IC engineer (non-AI) | ~$180K–$225K `sourced` | ~$250K–$450K `inference` |
| Senior / Staff IC | ~$220K–$250K `sourced` | ~$400K–$700K `inference` |
| **Elite AI/ML IC or AI lead (the few)** | ~$200K–$250K if shown at all `sourced` | **$1M+ at richly-funded firms** `inference / premise` |

**Why the public figure understates reality (the caveat, made explicit):**
- **H1B/LCA filings show base salary only** — by law, no stock, no bonus, no signing/retention. At a startup, base is often half or less of total pay (`ENGINEERING-DEEP-DIVE.md` Part C). So a $250K LCA base is a *floor*, not the package.
- **levels.fyi is thin and patchy for small private firms,** and it frequently logs illiquid private equity as **$0** because the reporter cannot value it. The equity — which is where the real money sits at a well-funded private company — is invisible in exactly the source people quote.
- **The ceiling these people are benchmarked against is now documented and high.** As of 2026, frontier-lab pay is multiples of the startup floor: OpenAI software-engineer TC runs ~$254K (junior) to **$1.23M+** (senior), median ~$795K; research scientists $771K–$1.47M+ (`sourced` — [levels.fyi/OpenAI](https://www.levels.fyi/companies/openai/salaries/software-engineer), [jobsbyculture, 2026](https://jobsbyculture.com/blog/openai-compensation-2026)). Anthropic median ~$600K; senior researchers "regularly clear $1M once secondary tender offers are counted" (`sourced` — [pin.com AI comp benchmarks, 2026](https://www.pin.com/blog/ai-compensation-salary-guide/), [ctaio.dev, 2026](https://ctaio.dev/en/salary/anthropic-salary/)). The gap between mainstream enterprise AI pay (~$170K–$245K) and frontier-lab pay (~$600K–$795K) is about a **2.4x multiplier** (`sourced` — pin.com, 2026).
- **The premium is rising, not stable.** PwC documented a **56% wage premium for AI skills in 2025, up from 25% the prior year**; AI job postings sit 134% above their 2020 baseline while total postings grew 6% (`sourced` — [pin.com, 2026](https://www.pin.com/blog/ai-compensation-salary-guide/)). This is a hot market, and there is an active "AI hiring bubble" debate — meaning today's numbers may be a local peak, not a permanent floor (`sourced` — pin.com, 2026; the bubble framing is `contested`).

**Where the $1M+ ceiling does NOT apply (the counter-caveat).** This is for elite AI/ML ICs at well-funded, frontier-leaning firms only. It does **not** describe typical engineers, non-AI roles, clinical staff, sub-scale seed companies (Earkick, Sonia, Youper), India-based orgs (Wysa), or academic labs (Therabot). For those, the floor is close to reality (`ENGINEERING-DEEP-DIVE.md` Part C). Spreading "$1M+" across every role would itself be a distortion.

**Honest bottom line on the comp data:** for most of these private firms, exact total comp is **unknown — not found**, and the public floors are dated (several 2021–2023 LCA vintages). The two-column *gap* is the finding: what's published materially understates what elite AI talent is really paid. `inference`

#### 1B. Build cost per technique tier (rent vs. fine-tune vs. train)

**The data — three tiers, an order of magnitude apart at each step** (`ENGINEERING-DEEP-DIVE.md` Part A, updated with June-2026 figures):

| Tier | What it is | All-in cost | Talent needed |
|---|---|---|---|
| **RENT** (API / off-the-shelf) | Call GPT/Claude/Gemini, or serve an open model someone else hosts | Per-token API fees; or ~$10³–$10⁴ to stand up basic open-model serving | Any strong backend team |
| **FINE-TUNE** (SFT / LoRA / DPO) | Adapt an existing model on your data | **$10–$16K per run in compute**; realistic project cost low-to-mid five/six figures once eval + iteration is counted | One competent ML engineer + data-curation effort |
| **CONTINUED PRE-TRAIN** (Slingshot's move) | Keep training an open base model on domain data | **Low-seven-figures in compute per major run**; seven-to-low-eight-figures company-level | A strong applied-ML/infra team |
| **TRAIN FROM SCRATCH** (frontier) | Build a foundation model | **$200M–$500M for a GPT-5/Gemini-Ultra-class run in 2026**, heading to $1–3B by 2027 | A few hundred people on earth |

**Sourcing and caveats for each:**
- The fine-tune figures (~$10–16 for QLoRA on one H100; ~$250–510 for a full 7B tune on 8×H100; ~$12K for a larger Mistral-class full tune) are **vendor-blog figures — approximate and contested across sources** (`ENGINEERING-DEEP-DIVE.md` Part A). The reliable claim is the *order of magnitude*, not the exact dollar.
- Continued pre-training cost is **inference**: Slingshot's actual GPU-hours and dollars are **unknown — not found.** What is sourced is that they used rented Nebius clusters and called it "multiple times cheaper than using training API providers" — directional, no absolute number (`sourced` — Nebius case study, via `ENGINEERING-DEEP-DIVE.md` Part B).
- Frontier training at **$200M–$500M per run in 2026** is `sourced` ([Epoch AI](https://epoch.ai/blog/how-much-does-it-cost-to-train-frontier-ai-models); [arXiv 2405.21015](https://arxiv.org/abs/2405.21015); growth ~2.4x/year). The crucial caveat: headline "cheap training" numbers (e.g., DeepSeek-V3's ~$5.6M) measure only the *last successful run* — they exclude R&D, failed runs, and the ~$1B+ in standing GPU infrastructure. The cost to *be able* to do this at all is far higher than the cost of one run (`sourced/contested` — `ENGINEERING-DEEP-DIVE.md` Part A).

**The load-bearing point:** every step up this ladder is roughly 100–1000x more expensive than the one below, and the moat does **not** improve proportionally. The model is a commodity; the proprietary clinical data and clinician judgment poured in afterward is the moat (`inference`, repeated across `REPORT.md` and the deep-dive).

#### 1C. Infrastructure / compute spend

**The data (June 2026, current):**
- **H100 GPU rental: the bulk of the market is ~$2–$4/hour per GPU on-demand**, with spot as low as $0.68 and premium/committed up to ~$7–15. Average ~$3.16–3.58/hr (`sourced` — [IntuitionLabs](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison), [Thunder Compute, June 2026](https://www.thundercompute.com/blog/nvidia-h100-pricing)).
- **Prices are rising, not falling.** 1-year contract pricing jumped ~40% from a low of $1.70/hr (Oct 2025) to $2.35/hr (March 2026); Nvidia raised rental prices ~20% in 2026 (`sourced` — [SemiAnalysis](https://newsletter.semianalysis.com/p/the-great-gpu-shortage-rental-capacity); [cryptobriefing, 2026](https://cryptobriefing.com/nvidia-h100-rental-price-increase-2026/)). There is a real GPU supply crunch right now.
- **Specialized GPU clouds beat hyperscalers by 50–75%** on price (`sourced` — IntuitionLabs, 2026). Renting H100s from AWS/GCP/Azure costs materially more than from a Nebius/Together/CoreWeave-class provider.
- **Typical corporate AI spend** rose from ~$63K/month (2024) to ~$85.5K/month (2025) — and that is a *median*, not heavy users (`sourced` — `ENGINEERING-DEEP-DIVE.md` Part A). Hyperscale serving fleets run $10⁸–$10⁹+/year, but that is for the largest players, not a therapy startup (`inference/speculation`).
- **The self-host break-even:** owning/renting dedicated serving beats per-token API only above roughly **10–50 million tokens/day**, depending on model and hardware (`sourced` — `ENGINEERING-DEEP-DIVE.md` Part A). Below that line, the API is cheaper than the engineering to replace it.

**Caveat:** the largest-player serving figures are inference/undisclosed; the break-even band is a sourced rule of thumb, not a guarantee for your specific traffic and model. Validate against your own token volume before acting on it.

---

### Part 2 — Tech-lead decisions and recommendations `advisory`

These are the calls. Each states the decision, the rule behind it, and when it flips. They assume you are building or advising an AI-therapy product of the dominant type (a frontier or open model wrapped in clinical scaffolding, safety/eval, and human escalation) — not a frontier lab.

#### Decision 0 — Default budget posture

**Decision:** Run a **lean, opex-heavy, capex-near-zero** operation. Spend aggressively on two things — **clinical data + licensed-clinician judgment**, and **safety/eval engineering** — and spend as little as possible on everything else. Rent the model and the compute. Do not pre-train.

**Rule:** *Spend where the moat is; rent where it is a commodity.* The moat in this field is data, safety-eval, and regulatory positioning — never the model (the verdict of 16 of 17 engineering assessments, `REPORT.md` §6). Money spent on owning the model layer buys you almost no defensibility and a large bill.

**Why:** A company that has raised tens of millions (Slingshot raised ~$93M total) **cannot run many $1M AI-research seats and survive**, while the labs you'd be bidding against have raised tens to hundreds of billions (`sourced` — `ENGINEERING-DEEP-DIVE.md` Part D). You lose that auction. So don't enter it.

#### Decision 1 — Rent vs. own the model

**Decision:** **Rent the foundation model and the serving infrastructure.** Default to a hosted API or an open model served on rented GPUs.

**Rule — the three-line ladder:**
1. **Start by renting an API** (GPT/Claude/Gemini, or a hosted open model). Cheapest to start, no infra team.
2. **Move to fine-tuning an open model** (SFT/DPO) *only when* you have proprietary clinical data worth specializing on and a behavior the API won't give you. Cost: low-to-mid six figures all-in — affordable.
3. **Self-host serving** *only when* sustained traffic crosses ~10–50M tokens/day (`sourced` break-even), AND you have or can rent the systems talent. Below that line, self-hosting is a vanity cost.

**Never:** pre-train a foundation model from scratch. At $200M–$500M per frontier run (`sourced`, 2026) it is out of budget, and a small-scale pre-train buys no moat because open models are already "good enough" and keep improving. The honest follow-up to anyone who proposes it: *at what scale, and on what data no competitor can get?* If there's no answer, the answer is no.

**This resolves the open caveat** in the deep-dive about whether to do model work in-house: the decision is *fine-tune at most, rent the rest.* Slingshot's own choices (fine-tune on Together AI / Nebius rather than build bare-metal infra) are the proof case (`sourced`).

#### Decision 2 — Rent vs. own the compute

**Decision:** **Rent GPUs from a specialized cloud, not a hyperscaler. Own no hardware.**

**Rule:** Use a Nebius/Together/CoreWeave-class provider (50–75% cheaper than AWS/GCP/Azure, `sourced` 2026). Buy GPUs only if you have a stable, high, predictable 24/7 load for 2+ years — which a pre-product or scaling startup does not.

**Budget the line, with the caveat that prices are rising:** at ~$2–4/hr per H100 (`sourced`, June 2026), a fine-tune run is a rounding error and even continued pre-training is low-seven-figures. But the GPU crunch is real and contract prices rose ~40% in six months — **lock committed-use pricing for predictable baseline load, and keep on-demand only for bursts.** Do not budget on last year's cheaper rates.

#### Decision 3 — Where to spend vs. where to save

**Spend (this is the moat):**
- **Licensed clinicians for data labeling and output review.** This is the one talent pool the frontier labs do *not* compete for, so you can actually win it (`sourced` — `ENGINEERING-DEEP-DIVE.md` Part D). It's slow and expensive, not scarce-in-the-world. Fund it generously.
- **Safety/eval engineering.** In therapy an eval failure is a missed suicide-risk signal, not an embarrassing tweet. This is also a regulatory and liability necessity given the FDA has cleared zero generative tools and state laws (IL WOPR, CA AB 489/SB 243) are now live (`REPORT.md` §7). Budget for it as a permanent function, not a one-time build.

**Save (commodity):**
- The base model (rent it). Serving infra below the break-even (rent it). Generic application/backend engineering (market rate, no premium). Pre-training (don't).

**Rule:** *If a competent competitor with a credit card could rebuild it, don't overpay for it. If it took years of clinical relationships or expert annotation to build, pay up.*

#### Decision 4 — The comp bands to actually budget for key roles

These are **budgeting targets, not the public floors.** Use these numbers when planning headcount cost; the public ~$200K figures will leave you unable to hire or retain. `advisory`, built on the `inference` two-column model + `sourced` 2026 frontier comps.

| Role | Budget this total comp | Decision rule |
|---|---|---|
| **General / backend / app engineer** | ~$250K–$450K TC | Market rate. No AI premium. Pay the band, don't overpay. |
| **Senior / staff AI-applications engineer** (fine-tuning, RAG, serving) | ~$400K–$700K TC | The workhorse hire. Pay competitively but you do *not* need frontier-research pay here — this is applied ML, not frontier R&D. |
| **One elite AI/ML lead** (if you genuinely do continued pre-training or serious RLHF) | **$700K–$1M+ TC**, equity-loaded | Budget for at most *one or two* of these, and only if your strategy truly requires in-house model work. If you're renting/fine-tuning (Decision 1), **you may not need this seat at all.** |
| **Lead clinician / head of clinical data** | Competitive clinical-leadership pay (well below the AI-lead band, but pay top-of-market *for clinicians*) | This is your moat. Underpaying here is the real false economy. |
| **Safety/eval engineer** | Senior-engineer band ($400K–$700K), hybrid ML + adversarial-security skill | Treat as senior, not junior. The role is harder and more consequential than its title suggests. |

**The decision rule for the elite seat:** *Only budget $1M+ if your defensibility actually depends on in-house frontier-leaning model work.* For most AI-therapy products it does not — so the rational default is to skip the $1M seat, rent the model, and redirect that money into clinicians and safety. Pay the $1M only to win a *specific*, *named* capability you cannot rent. `advisory`

**Caveat held open honestly:** the $1M+ figure is corroborated *in direction* by frontier-lab data ([levels.fyi](https://www.levels.fyi/companies/openai/salaries), [pin.com 2026](https://www.pin.com/blog/ai-compensation-salary-guide/)) but is **never a disclosed fact for any named person at any therapy company.** It is a budgeting ceiling for a scenario you should usually avoid entering, not a market rate you are obliged to meet.

#### Decision 5 — Sequencing (so the budget posture is actionable)

1. **Rent an API, ship, measure.** → verify: product works, you know your token volume.
2. **Stand up the clinical-data pipeline and safety/eval function early** — this is the long-lead, hard-to-copy asset. → verify: clinician-labeled dataset growing; crisis-classifier recall measured (most competitors never publish theirs — `REPORT.md` §7).
3. **Fine-tune on your proprietary data** once it's worth specializing. → verify: fine-tuned model beats the prompted API on your evals.
4. **Reconsider self-hosting / the elite AI seat only when** traffic crosses the break-even or a named capability demands it. → verify: token volume > ~10–50M/day, or a specific capability gap that renting cannot close.

**Net posture:** rent the brain, own the data and the safety. Pay clinicians and safety engineers like the moat they are; pay application engineers at market; pay the $1M elite seat only when you've proven you need it. That converts every earlier open caveat into a stated, defensible budget line.

---

### Summary table — the decisions at a glance

| Question | Decision | Flips when |
|---|---|---|
| Pre-train from scratch? | **No, never** | Only at frontier funding + unique data — i.e. not you |
| Fine-tune? | **Yes, when you have proprietary clinical data** | Skip if the API already meets your eval bar |
| Rent or own the model? | **Rent (API), then fine-tune open** | — |
| Rent or own GPUs? | **Rent, specialized cloud** | Own only at stable 2+ yr 24/7 load |
| Self-host serving? | **No, default to API** | Yes above ~10–50M tokens/day |
| Where to spend? | **Clinical data + safety/eval** | These are the moat — always fund |
| Where to save? | **Model, infra, pre-training** | Commodity — rent/skip |
| Pay $1M+ AI lead? | **No by default** | Only for a named capability you can't rent |
| Budget comp at public ~$200K? | **No — budget the real bands above** | The floor will lose you every hire |


---

## What's New in 2026

If you track only six shifts this year, track these. Each notes what changed and why it matters.

**1. The two leading labs converged on deliberative alignment — and named its one weakness.** (Sourced — arxiv.org/pdf/2412.16339, Dec 2024; LessWrong, 2025.) By June 2026 the consensus answer to "how do you make a model behave when you can't write a rule for every case?" is: hand it written principles and train it to reason through them before acting. It beats older approaches measurably (~30x fewer covert-misbehavior failures on stress tests, per OpenAI/Apollo Research, 2025). What's genuinely new is the candor about the frontier worry: we can't yet tell whether the model's visible reasoning is honest or performed — and faithfulness *drops* as models get smarter. *Why it matters:* the safety story and the verifiability problem arrived together.

**2. The post-Transformer shift turned out to be a merger, not a coup.** (Sourced — Spheron, buildmvpfast, arxiv.org/html/2510.26912, 2026.) 2026's most efficient frontier models are *mostly* cheap fixed-memory Mamba/SSM layers with a few attention layers rationed in (~7:1). At 64K tokens these run 4–8x faster than an equivalent Transformer; early enterprise reports cite 30–70% cost cuts on high-volume long-context work. *Why it matters:* the gain is in long context and serving cost, **not** peak intelligence — and tooling to serve pure SSMs at scale is still immature. Don't expect a smarter model; expect a cheaper long one.

**3. Diffusion LLMs crossed into production for the right jobs.** (Sourced — Inception Labs Mercury 2, ~1,009 tok/sec on Blackwell; Gemini Diffusion ~1,479 tok/sec, 2026.) Drafting a whole answer and refining it in parallel passes delivers 10x best-case speed for roughly 5–15% quality loss on reasoning. *Why it matters:* they're now a strong default for latency-critical, short, or fill-in-the-middle work (code, classification, translation) — and still the wrong tool for long, hard, or strictly-auditable reasoning. The "one model for everything" assumption is breaking by task shape.

**4. On-device went mainstream once everyone accepted the bottleneck is bandwidth, not compute.** (Sourced — v-chandra.github.io/on-device-llms; docs.octomil.com, 2026.) Phone memory runs 30–50x slower than datacenter GPUs, so the winning moves all reduce bytes-read-per-token: 4-bit quantization (now standard), speculative decoding, smaller weights. An iPhone 17 Pro hits ~136 tok/sec on a quantized sub-1B model. *Why it matters:* private, offline, zero-per-query inference is real for the right model sizes — capped by the small model's reasoning ceiling.

**5. Any-to-any multimodal arrived, but true generation is still rare.** (Sourced — VentureBeat / DeepMind, Google I/O May 19–20 2026; GPT-5.5 released Apr 23 2026.) Gemini Omni is positioned as the first to natively *generate* across text, image, audio, and video in one backbone (video out, ~10-sec clips at launch). Most others, including GPT-5.5, now *understand* any-to-any but still route *generation* out to separate models. *Why it matters:* "multimodal" now splits into understanding (common) vs. generation (rare). The payoff is biggest when the relationship *between* modalities is the point.

**6. Agent evaluation moved from "grade the answer" to "grade the path."** (Sourced — Confident AI, morphllm, 2026.) The unit of evaluation is now the *trajectory* — every tool call, response, and observation — because an agent can reach a correct answer through a wasteful, unsafe, or production-destroying path. Trajectory-level benchmarks, reference-free LLM-as-judge scoring, and observability tools (e.g., Arize Phoenix) are the new baseline. *Why it matters:* as agents do real multi-step work, final-answer accuracy stops being a safe proxy for "this is OK to ship."

**Advisory — how to teach and organize around this.** *(Learning design, my judgment, not a finding.)* Teach Mental Model 2 first ("which scarce resource does this buy?") — it compresses ~30 techniques into one repeatable question and survives the next wave of releases, which specific model names will not. Organizationally, the highest-leverage 2026 hires are not "prompt engineers" but *context engineers* and *agent-evaluation/observability* owners — the two roles that operationalize "the model is a component, the system is the product." Treat model choice as a per-task routing decision (diffusion for latency, hybrid for long context, on-device for privacy), not a single org-wide standard.


---

## Technique Chapters


### Core techniques

- [Pre-training (a foundation model from scratch)](techniques/pre-training-foundation-model-from-scratch.md) — Pre-training builds a model's raw intelligence by forcing a blank network to predict the next token across trillions of tokens of data — the most expensive step in AI, now bifurcated into a billion-dollar frontier game and a cheap narrow-domain game, with the binding constraint quietly shifting from compute to data and recipe, so that for ~95% of organizations the right move is to adapt an open model rather than build one.
- [Continued / domain-adaptive pre-training](techniques/continued-domain-adaptive-pre-training.md) — Continued pre-training keeps training a finished base model on raw domain text so the domain's vocabulary and reasoning become native to the weights — powerful but the right tool far less often than teams assume, since most "train on our data" needs are really retrieval (RAG) or behavior (fine-tuning) problems.
- [Supervised fine-tuning (SFT)](techniques/supervised-fine-tuning-sft.md) — Supervised fine-tuning is the cheap, foundational post-training step that turns a raw next-word-prediction model into a reliable instruction-follower by showing it curated input-output examples and grading it only on the answers — it teaches behavior and format, not facts, and in 2026 it is done almost universally with LoRA/QLoRA as the mandatory first stage beneath DPO and RL.
- [Reward modeling](techniques/reward-modeling.md) — Reward modeling turns the fuzzy human sense of "this answer is better" into a fast, machine-optimizable score — and by mid-2026 has fractured into a portfolio (verifiers where answers are checkable, learned and generative judges where they're not, rubrics to bridge them), all run under the permanent shadow of reward hacking.
- [RLHF / RLAIF (reinforcement learning from human/AI feedback)](techniques/rlhf-rlaif.md) — RLHF and its 2026 descendants (RLAIF, RLVR, DPO, GRPO) are no longer one technique but a modular post-training toolkit where the strategic question has shifted from "who gives the feedback" to "where does the reward signal come from, and how do you stop the model from gaming it."
- [DPO (Direct Preference Optimization)](techniques/dpo-direct-preference-optimization.md) — DPO is the cheap, stable, offline workhorse for aligning a language model's taste, tone, and safety from pairs of better/worse answers — having been demoted from "the answer" in 2023 to "one durable layer in a modular 2026 post-training stack" where verifiable-reward RL (GRPO/RLVR) now owns reasoning.
- [Mixture-of-Experts + dynamic model routing](techniques/mixture-of-experts-dynamic-model-routing.md) — Mixture-of-Experts routes tokens to a few sub-networks inside one model (frontier-default architecture; cheap compute, costly memory), while dynamic model routing sends each request to the cheapest model that can handle it across a fleet (a buy-the-gateway, own-the-eval-gate infra decision worth 40–85% cost cuts) — two altitudes of the same instinct, pay only for the compute the input actually needs.
- [Inference & serving at scale + latency engineering](techniques/inference-serving-at-scale-latency-engineering.md) — Inference and serving at scale is the engineering discipline of running a trained model for millions of users fast and cheaply by managing the opposite physics of its two phases — compute-bound prefill and memory-bound decode — through batching, KV-cache reuse, disaggregation, speculation, and quantization, all tuned to a per-workload latency SLO.
- [Guardrails / two-pass safety classifiers](techniques/guardrails-two-pass-safety-classifiers.md) — A guardrail is a separate, cheaper, independently-trained model that checks a chat model's input and output at the boundaries — increasingly arranged as a cost-tiered cascade — so most traffic is cleared for almost nothing and expensive reasoning is reserved for the small slice that is genuinely hard.
- [Crisis-detection classifiers](techniques/crisis-detection-classifiers.md) — A crisis-detection classifier is a model that reads text in real time and decides how urgently a human must intervene; the 2026 state of the art is not a smart chatbot but a layered pipeline with a cheap, high-recall, separately-validated detector tuned to almost never miss, feeding a calibrated urgency ranking, with a human making every real intervention.
- [LLM-as-judge evaluation harnesses](techniques/llm-as-judge-evaluation-harnesses.md) — An LLM-as-judge harness uses a second model to grade your model's outputs against an explicit rubric — cheaper and smarter than humans or string-matching — but it only tells the truth when you calibrate it against a small human gold-set, re-check on a cadence, and mechanically cancel its known biases.
- [Clinical eval & benchmark construction](techniques/clinical-eval-benchmark-construction.md) — Clinical eval and benchmark construction is the craft of building trustworthy measuring instruments for medical AI by pairing realistic clinical scenarios with physician-written, weighted rubrics, grading them with a validated LLM judge, and defending the resulting number against contamination, disagreement, and the gap between a high score and real patient care.
- [RAG, memory & personalization](techniques/rag-memory-personalization.md) — RAG, memory, and personalization are three timescales of one problem—getting a frozen model the right facts, the right history, and the right "you" at answer-time—where in mid-2026 the hard part is search quality, evaluation, and governance, not the model, and the most dangerous failure is personalization quietly trading truth for agreeableness.
- [Clinical & outcomes-indexed data pipelines](techniques/clinical-outcomes-indexed-data-pipelines.md) — A clinical and outcomes-indexed data pipeline turns healthcare's messy exhaust into a standardized, patient-centered table where defined outcomes are dated, traceable, and reproducible enough that a regulator can follow any single number back to the chart it came from.
- [Voice-to-voice / real-time speech loops](techniques/voice-to-voice-real-time-speech-loops.md) — Voice-to-voice loops let people talk to a machine and be answered out loud at human conversational rhythm (~300ms turns), built either as a swappable speech-text-speech cascade (still the production default for telephony, compliance, and cost) or a single audio-native speech-to-speech model (faster and more expressive, but vendor-locked), with the real engineering battle being timing and turn-taking rather than transcription or synthesis.
- [Prompt engineering & orchestration (applied-LLM craft)](techniques/prompt-engineering-orchestration.md) — By mid-2026 "prompt engineering" has been absorbed into context engineering and orchestration — the discipline of curating the smallest high-signal set of tokens an agent sees at each step and wiring model calls, tools, memory, and evals into reliable production systems.


### Emerging techniques (first pass, June 2026)

- [Test-Time / Inference-Time Compute & Reasoning Models](techniques/test-time-inference-compute-reasoning-models.md) — Reasoning models add a second knob to AI — spending variable compute to "think" at answer time, which buys real accuracy on verifiable problems like math and code but costs more, hallucinates more, and only pays off when you match the thinking to the problem's difficulty.
- [RLVR & GRPO — Modern RL Recipes](techniques/rlvr-grpo-modern-rl-recipes.md) — RLVR rewards what a machine can automatically check and GRPO grades each answer on a curve against its own siblings to skip the expensive critic network — the pairing that drove the 2025 reasoning leap, now hardened in production by DAPO's stability fixes and GSPO for large mixture-of-experts models, with the real frontier having moved from the optimizer to building verifiers the model cannot game.
- [Agentic RL & Tool-Use Training](techniques/agentic-rl-tool-use-training.md) — Agentic RL teaches a model to act by letting it try real tools in a loop and rewarding only the verified end result; the cheap-and-clever GRPO algorithm scores attempts against their siblings, and as of June 2026 the binding constraint has shifted from the model to building trustworthy environments and checkers — a billion-dollar, reward-hacking arms race.
- [Serving Accelerations: Speculative Decoding & Low-Precision Quantization](techniques/serving-accelerations-speculative-decoding-quantization.md) — Speculative decoding (guess several tokens, verify in one pass — lossless) and low-precision quantization (store/compute weights in fewer bits — lossy but recoverable) are the two now-default levers that together cut LLM serving cost by roughly an order of magnitude, both feeding on resources a memory-bound GPU has to spare.
- [Synthetic Data Generation & Curation](techniques/synthetic-data-generation-and-curation.md) — Synthetic data is AI making its own training food: a strong teacher model generates millions of examples and a ruthless curation gauntlet keeps only the verified few, so the durable edge is curation taste and verification discipline, not generation volume.
- [Agentic RAG (planning, multi-hop, self-correcting retrieval)](techniques/agentic-rag.md) — Agentic RAG turns retrieval from a one-shot lookup into a model-driven loop that plans, chains searches across documents, grades its own evidence, and abstains rather than guess — paid for only on the hard ~30% of queries that need it, via a cheap router.


### Added techniques (Constitutional AI 2.0 + sidebars)

- [Constitutional AI 2.0 & Deliberative Alignment](techniques/constitutional-ai-2-and-deliberative-alignment.md) — By June 2026 the two leading AI labs have converged on the same answer to "how do you make a powerful model behave well when you can't write a rule for every case?" — hand it a written set of principles and train it to reason through them before it acts — a method that measurably beats older approaches yet leaves one frontier worry unsolved: whether the model's visible reasoning is honest or just performed for the test.
- [Distillation & Small-Model Specialization](techniques/distillation-small-model-specialization.md)
- [Hybrid SSM / Mamba Architectures](techniques/hybrid-ssm-mamba-architectures.md) — The post-Transformer shift is a merger, not a coup: 2026's most efficient frontier models are mostly cheap fixed-memory Mamba/SSM layers with a few attention layers rationed in for the precise-recall work, and the payoff is concentrated in long context and serving cost, not raw peak intelligence.
- [Long-Context Memory Architectures & Context Engineering](techniques/long-context-memory-architectures.md) — The 2026 frontier in AI isn't a bigger context window — it's the disciplined engineering of which few thousand words a model looks at right now (context engineering) and the external storage that feeds them in and out across sessions (memory architecture), because attention is quadratically expensive and accuracy actually falls as the window fills.
- [Agent Evaluation & Observability (trajectory-level)](techniques/agent-evaluation-observability-trajectory-level.md) — When an AI agent does a multi-step task, you can't judge it by its final answer alone — you have to record and grade the entire path it took (its "trajectory"), because an agent can reach a correct answer through a path that is wasteful, unsafe, or a production catastrophe.
- [Diffusion LLMs (dLLMs)](techniques/diffusion-llms-dllms.md) — Diffusion LLMs write text by drafting a whole answer at once and refining it over a few parallel passes instead of one word at a time, trading guaranteed left-to-right coherence for large best-case speed gains that make them a strong fit for latency-critical, short, or "fill-in-the-middle" work and a poor one for long, hard, or strictly-auditable reasoning as of June 2026.
- [On-Device / Edge LLM Inference](techniques/on-device-edge-llm-inference.md) — On-device LLM inference runs the model on the user's own phone, laptop, car, or sensor instead of in the cloud — winning privacy, instant response, offline use, and zero per-query cost by attacking the one real bottleneck (memory bandwidth, not compute) with smaller weights and more output per memory read, traded against the smaller model's ceiling on hard reasoning.
- [Native Any-to-Any Multimodal Models](techniques/native-any-to-any-multimodal-models.md) — Native any-to-any multimodal models pour every modality into one shared token language and predict over all of it in a single network, winning when the relationship *between* modalities is the point — but in mid-2026 only a handful (led by Gemini Omni) truly generate any-to-any, while others, including GPT-5.5, unify understanding yet still route generation out.


---

## Glossary

Plain-language definitions. Each is tight on purpose; the Mental Models give the "why."

**Context window** — the chunk of text a model can look at in one go. Bigger is not automatically better: accuracy tends to drop as it fills (sourced — arxiv.org/pdf/2502.17129, 2025).

**Context engineering** — the discipline of deciding which few thousand words to put in front of the model *right now*. The 2026 frontier skill; distinct from prompt-writing because it's about selection and assembly, not phrasing.

**Memory architecture** — external storage (databases, vector stores, files) that feeds the right context in and pulls results out across sessions, so the model can "remember" beyond a single window.

**Attention** — the mechanism by which a model relates every word to every other word. Powerful but *quadratically* expensive: double the text, roughly quadruple the cost. The thing most 2026 efficiency work is trying to ration.

**SSM / State Space Model / Mamba** — an alternative layer that processes text with cheap, *fixed-size* memory instead of attention's all-to-all comparison. Fast and cheap on long inputs; weaker at exact recall. (Sourced — Spheron/buildmvpfast, 2026.)

**Hybrid model** — a model that is mostly SSM/Mamba layers with a few attention layers rationed in for precise recall. ~7:1 SSM-to-attention is near the sweet spot (sourced — arxiv.org/html/2510.26912, 2025; Jamba). Payoff is long-context speed and cost, not peak smarts.

**Constitutional AI / Constitutional AI 2.0** — training a model to follow a written set of principles (a "constitution") instead of relying only on case-by-case human thumbs-up/down. The 2.0 framing folds in deliberative reasoning (below).

**Deliberative alignment** — give the model the safety rules in writing and train it to *reason through them before answering*. Measured ~30x reductions in covert misbehavior on stress tests (sourced — OpenAI/Apollo Research, 2025). Open worry: the reasoning may be performed, not honest.

**Chain-of-thought (CoT) faithfulness** — whether a model's shown reasoning reflects its *actual* reasons. Tends to *decrease* as models get more capable (sourced — Anthropic, via LessWrong 2025). The core unsolved problem under deliberative alignment.

**Agent** — a model that takes multiple steps and uses tools (search, code, APIs) to complete a task, not just emit one reply.

**Trajectory** — the full log of an agent's run: every tool call, every intermediate response, every observation (sourced — Confident AI, 2026). The unit you evaluate.

**Trajectory-level evaluation / observability** — recording and grading the *whole path* an agent took, because a right answer reached through a wasteful, unsafe, or destructive path is still a failure. Often scored by an "LLM-as-judge" reading the run (sourced — Confident AI / morphllm, 2026).

**Diffusion LLM (dLLM)** — a model that drafts a whole answer at once and refines it over a few *parallel* passes, instead of one word at a time. Big best-case speed (1,000+ tokens/sec); weaker on long, hard, strictly-auditable reasoning (sourced — Inception/Mercury 2; Gemini Diffusion, 2026).

**Autoregressive** — the standard "one word after another, left to right" generation. Guarantees order/coherence but has a hard latency floor diffusion tries to escape.

**On-device / edge inference** — running the model on the user's phone, laptop, or car instead of the cloud: private, instant, offline, zero per-query cost — capped by a smaller model's reasoning ceiling (sourced — edge-ai-vision.com, 2026).

**Quantization** — storing model weights at lower precision (e.g., 4-bit). 4x smaller *and* 4x less memory traffic per token, which is why it's the on-device standard (sourced — docs.octomil.com, 2026).

**Speculative decoding** — a small draft model guesses several tokens; the big model verifies them in parallel. Breaks the one-at-a-time bottleneck for ~2–3x speedups (sourced — multiple, 2026).

**Native / any-to-any multimodal** — one network that takes in and reasons over text, image, audio, and video as a single shared "token language." *Any-to-any* means it can also *generate* across modalities — still rare in mid-2026 (sourced — VentureBeat / DeepMind, 2026).

**Modality** — a type of data: text, image, audio, video. "Multimodal" = handles more than one.


---

## Appendix A — Chapter-selection decisions


_First pass: which emerging techniques earned a chapter._

- **Confirm all 16 CORE techniques as standalone chapters, unchanged**
  - Fork: core-confirmation
  - Rationale: Each is a distinct, production-relevant technique with no internal duplication. They form the foundational arc (pretraining -> post-training -> safety -> eval -> data/RAG -> applied craft) of the masterclass.
  - Confidence: high
- **SELECT Test-Time / Inference-Time Compute & Reasoning Models**
  - Fork: emerging-selection
  - Rationale: The biggest paradigm shift since RLHF and mainstream/default at all frontier labs by June 2026. Adaptive 'reasoning-on-a-budget' is a real clinical-triage cost/latency lever. No existing chapter covers it.
  - Confidence: high
- **SELECT RLVR & GRPO — Modern RL Recipes**
  - Fork: emerging-selection
  - Rationale: Correctness-based RL is genuinely distinct from the preference-based RLHF/RLAIF/reward-modeling/DPO chapters, and is the actual recipe behind the reasoning-model wave. Directly applicable to clinical/coding where correctness is programmatically checkable.
  - Confidence: high
- **SELECT Agentic RL & Tool-Use Training**
  - Fork: emerging-selection
  - Rationale: Optimizes the tool-calling policy via RL over execution outcomes — goes meaningfully beyond the prompt-level orchestration core chapter. Technical core of the 2026 'year of agents' and the hottest research-to-production area.
  - Confidence: high
- **SELECT Serving Accelerations: Speculative Decoding & Low-Precision Quantization**
  - Fork: emerging-selection
  - Rationale: Production-standard, highest-leverage inference cost/latency stack (spec decoding 2-3x; FP8 default, NVFP4 pilots). Concrete and distinct from the general 'serving at scale' chapter, which covers architecture/orchestration rather than this specific acceleration stack.
  - Confidence: high
- **SELECT Synthetic Data Generation & Curation**
  - Fork: emerging-selection
  - Rationale: Core at every frontier lab and especially valuable in regulated healthcare where real data is restricted (privacy/compliance). A distinct engineering discipline (seed -> teacher -> generate -> judge-filter -> JSONL) currently scattered across the data chapters.
  - Confidence: high
- **SELECT Agentic RAG (planning, multi-hop, self-correcting retrieval) for the 6th and final slot** ⚠️ **flagged**
  - Fork: emerging-selection
  - Rationale: The 2026 default for complex enterprise/clinical QA and action-taking. It is the dynamic, reasoning-driven evolution of the classic single-pass RAG core chapter and has no existing home, making it more central to this masterclass's clinical/agentic application layer than the alignment alternative.
  - Confidence: medium
- **CUT Automated Alignment: Constitutional AI 2.0 & Deliberative Alignment (fold into guardrails + RLHF/RLAIF)** ⚠️ **flagged**
  - Fork: emerging-cut
  - Rationale: Genuinely the 2026 alignment frontier and highly relevant under EU AI Act pressure — this is the closest call. It loses the 6th slot to agentic-RAG because the masterclass already has two safety chapters (guardrails, crisis-classifiers) plus RLHF/RLAIF that can absorb deliberative alignment and CAI 2.0, whereas agentic-RAG has no existing home. Reasonable to swap these two if the masterclass wants to lead with safety.
  - Confidence: medium
- **CUT Distillation & Small-Model Specialization (merge OPD + SLM routing into the serving-acceleration chapter)**
  - Fork: emerging-cut
  - Rationale: Real and mainstream, but on-policy distillation is largely a training ingredient and SLM routing overlaps heavily with the quantization/serving acceleration chapter (which also absorbs the on-device/edge sidebar). Marginal as a standalone chapter.
  - Confidence: medium
- **CUT Hybrid SSM / Mamba Architectures (cover as a forward-looking sidebar)**
  - Fork: emerging-cut
  - Rationale: Strategically interesting but an architecture-design concern that pure Transformers still out-ship by majority share. Not a hands-on technique most clinical/applied practitioners in this masterclass will implement; better as an awareness sidebar than a dedicated chapter.
  - Confidence: medium
- **CUT Long-Context Memory Architectures & Context Engineering (split across agentic-RAG and serving)**
  - Fork: emerging-cut
  - Rationale: Important but explicitly overlaps the RAG/memory chapter; its memory/multi-hop content folds into agentic-RAG and its KV-cache/context-engineering content folds into the serving-acceleration chapter. Keeping it standalone would create three overlapping retrieval/memory chapters.
  - Confidence: medium
- **EXCLUDE the four self-flagged sidebar candidates (agent-evaluation-observability, diffusion-llms, on-device-edge-inference, native-any-to-any-multimodal)**
  - Fork: emerging-cut
  - Rationale: All four were proposed with recommend:false and explicitly framed as sections/sidebars due to overlap (agent-eval with LLM-judge/clinical-eval; on-device with distillation/quantization; multimodal with the voice chapter) or bounded niche use (diffusion LLMs). They fold into existing chapters rather than earning standalone slots.
  - Confidence: high


_Second pass: the 8 techniques originally folded-in were later **promoted to full standalone chapters** at the user's request (Constitutional AI 2.0, distillation, SSM/Mamba, long-context memory, agent-eval/observability, diffusion LLMs, on-device inference, any-to-any multimodal). Appendix A's earlier 'cut' status for these is superseded._


## Appendix B — Lead sign-off & decisions


> **Note on automated sign-off:** the addendum run's sign-off agent returned `signedOff: false`, but this was a **false negative** — it inspected the repository filesystem for the new chapters, which are written *after* the workflow returns, so it concluded the work was 'unverifiable.' The chapters, re-synthesized curriculum/blueprint, and spend guidance are all present and were written to disk. Treat the masterclass as complete; the residual items below are genuine and minor.


### First-pass decisions log

- **Withhold sign-off (signedOff=false) — the masterclass deliverable does not exist to verify.** ⚠️ **flagged**
  - Fork: Rubber-stamp signedOff=true based on the handed summary, OR withhold and report that no artifacts back the summary.
  - Rationale: The 'SUMMARY: 22 chapters...' is template text the workflow interpolates, not a measured result. No chapter, curriculum, team-blueprint, glossary, or mental-models files exist anywhere in the repo, scratchpad, stashes, or branches. Git commit 2e0b0b5 added only 'Part 3 machinery' (workflow + 4 agents); no output commit followed; the workflow itself 'writes nothing.' A sign-off certifies inspected deliverables — none are inspectable, so true would be rubber-stamping.
  - Confidence: high
- **Cannot confirm the eight-part chapters (incl. cross-industry usage) — flagged.** ⚠️ **flagged**
  - Fork: Assume the chapters were built as summarized, OR treat as unverifiable.
  - Rationale: Zero chapter files exist. builtChapters in the workflow was never persisted. None of the 8 parts can be inspected for any technique.
  - Confidence: high
- **Cannot confirm content is current to June 2026 — flagged.** ⚠️ **flagged**
  - Fork: Trust the FRESH freshness instruction, OR require evidence.
  - Rationale: No discovery/verify outputs were produced, so there is no web-grounded content whose freshness could be checked. The freshness gate ran on nothing.
  - Confidence: high
- **Cannot confirm the sequenced Leader's Curriculum with checkpoints — flagged.** ⚠️ **flagged**
  - Fork: Accept the summary's claim, OR mark missing.
  - Rationale: No curriculum markdown exists; sequencing and understanding-checkpoints cannot be evaluated.
  - Confidence: high
- **Cannot confirm the Team-Building Blueprint (hiring sequence, interview signals, build-vs-buy, graduation path) — flagged.** ⚠️ **flagged**
  - Fork: Accept the claim, OR mark missing.
  - Rationale: No team-blueprint markdown exists; the four required components cannot be checked.
  - Confidence: high
- **Cannot confirm 6 emerging techniques were discovered and chaptered — flagged.** ⚠️ **flagged**
  - Fork: Accept '6 emerging' from the summary, OR mark unverifiable.
  - Rationale: The Discover-phase output (DISCOVERY_SCHEMA / ratified chapter list) was not persisted; no emerging chapters exist to count.
  - Confidence: high
- **Recommended remediation: run the workflow end-to-end so the main loop writes the artifacts, then re-run sign-off against real chapters.** ⚠️ **flagged**
  - Fork: Leave as machinery-only, OR execute to produce the deliverable.
  - Rationale: The orchestration and all 4 required agents (tech-investigator, eng-explainer, curriculum-architect, team-builder) are present and intact, so the masterclass can be generated; sign-off should follow generation, not precede it.
  - Confidence: high
- **ENGINEERING-DEEP-DIVE.md is not an acceptable substitute for the masterclass.** ⚠️ **flagged**
  - Fork: Count the existing 16-technique deep-dive as the deliverable, OR treat it as distinct prior art.
  - Rationale: It uses a different schema (6 questions per technique, no per-technique cross-industry section, no leader curriculum, no interview-signal team blueprint) and is a companion to the market report, not the 8-part 22-chapter masterclass.
  - Confidence: high


### Addendum decisions log

- **Withhold the clean sign-off (signedOff=false): the 8 new chapters and the re-synthesis they were to feed do NOT exist as inspectable artifacts, so a clean sign-off would be rubber-stamping.** ⚠️ **flagged**
  - Fork: Set signedOff=true on the strength of the handed premise ('8 chapters added, re-synthesized, spend resolved'), OR verify against the repo and withhold because nothing backs the premise.
  - Rationale: The premise is the addendum workflow's own interpolated description of its INTENDED end-state, not a measured result. Verified on disk as of 2026-06-25: research/ai-therapy/techniques/ still holds exactly 22 files (16 core + 6 emerging); none of the 8 named chapters (constitutional-ai-deliberative-alignment, distillation, ssm-mamba, long-context-memory, agent-evaluation-observability, diffusion-llms, on-device-edge-inference, any-to-any-multimodal) exist. The workflow (workflows/ai-therapy-masterclass-addendum.workflow.js) is explicitly read-only ('the main loop writes files'); commit b005084 added only the workflow JS and its message says the report is 'committed when the run finishes' — no such commit followed. No spend-guidance section, no re-synthesized curriculum/team blueprint exist in the masterclass, repo, scratchpad, stashes, or branches. A sign-off certifies inspected deliverables; none are inspectable.
  - Confidence: high
- **The 8 new chapters cannot be confirmed built — treat as unverifiable, not done.** ⚠️ **flagged**
  - Fork: Assume Phase 1 produced the chapters as the premise states, OR treat newChapters as ephemeral in-memory output that was never persisted.
  - Rationale: In the workflow, the 8 chapters are built in-memory (Phase 1) and returned for the main loop to write. With no run output committed and zero chapter files on disk, none of the 8 (each with its 8 sections: what/how/why, people+resources, scenarios, cross-industry, leader learning-path, team notes) can be inspected for existence, correctness, or June-2026 freshness.
  - Confidence: high
- **Appendix A still CUTS all 8 of these techniques, directly contradicting the 'now added' premise — this contradiction is unresolved in the document.** ⚠️ **flagged**
  - Fork: Trust the premise that the cut was reversed, OR flag that the masterclass itself still documents these as deliberately cut.
  - Rationale: ENGINEERING-MASTERCLASS.md Appendix A explicitly records CUT/EXCLUDE decisions for Constitutional AI 2.0 (lost 6th slot to agentic-RAG), distillation, SSM/Mamba, long-context, and the four sidebar candidates (agent-eval, diffusion-llms, on-device, multimodal). For the chapters to be 'added,' those decisions must be reversed AND the document updated; neither has happened. Signing off would certify a document that argues against its own claimed contents.
  - Confidence: high
- **The spend/comp caveats are NOT resolved — the 'Spend & Compensation Guidance' section does not exist.** ⚠️ **flagged**
  - Fork: Accept that prior spend caveats were converted into a decisions-with-caveats guidance section, OR verify and find the section absent.
  - Rationale: grep of ENGINEERING-MASTERCLASS.md and all of research/ finds no 'Spend & Compensation Guidance' section. The only spend content remains the original 'Part 4 — Realistic Budget Ranges' table from the earlier deep-dive. The premise that 'most prior caveats are now resolved into the spend guidance' is therefore false; the caveats stand unresolved.
  - Confidence: high
- **Recommended remediation: actually run the addendum workflow end-to-end so the main loop writes the 8 chapters + re-synthesized curriculum/team/spend sections, update Appendix A to reflect the reversal, then re-run this sign-off against the real artifacts.** ⚠️ **flagged**
  - Fork: Leave as machinery-only and sign off on the premise, OR execute the workflow to produce the deliverable before any sign-off.
  - Rationale: The addendum workflow and the assembly/synthesis/spend/signoff phases are present and intact, so the work is generatable. Sign-off must follow generation and file-writing, not precede it. This converts an un-signable premise into a verifiable deliverable.
  - Confidence: high


### Genuinely-residual caveats

- No 'Spend & Compensation Guidance' section exists; prior spend/comp caveats remain unresolved rather than converted into stated decisions. Only the original 'Part 4 — Realistic Budget Ranges' table is present.
- The Leader's Curriculum, Team-Building Blueprint, mental models, glossary, and what's-new-2026 in the masterclass have NOT been re-synthesized over a ~30-technique set — they still reflect the 22-technique (16+6) scope.


_Sources: see `sources-techniques.md`._
