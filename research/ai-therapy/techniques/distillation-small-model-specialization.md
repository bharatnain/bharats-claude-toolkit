# Distillation & Small-Model Specialization

*A chapter for technical leaders who decide, fund, and staff — not for engineers who implement. Plain language, real depth.*

Claim labels used throughout: **[sourced]** = backed by a primary source listed at the end, with date; **[inference]** = my reasoning from sourced facts; **[speculation]** = forward-looking guess; **[advisory]** = a recommendation about how to learn, hire, or organize.

---

## 1. What it is

Distillation is the practice of taking a large, expensive, capable AI model — the **teacher** — and using it to train a smaller, cheaper, faster model — the **student** — so that the student reproduces the teacher's behavior on the tasks you care about. Small-model specialization is the broader goal that distillation serves: instead of running one giant generalist for everything, you run a compact model that is very good at *your* narrow job and ignores the other 95% of what a frontier model can do.

Two ideas sit underneath the word, and confusing them is the single most common mistake leaders make.

**The first idea is compression.** A frontier model in 2026 might have hundreds of billions to over a trillion parameters. Most production tasks — classify this ticket, extract these fields, route this request, summarize this call — do not need that. Distillation lets you capture the slice of the teacher's competence that your task requires and bake it into a model that is one-tenth to one-hundredth the size. The student is cheaper to run (lower cost per request), faster (lower latency), and often deployable in places the teacher can never go — a phone, a car, a hospital's own servers, a laptop with no internet. **[inference]**

**The second idea is capability transfer, especially of reasoning.** This is the part that changed the field in 2025–2026. It turns out you can teach a *small* model to *reason* — to think step by step, to work through a math proof or a multi-step plan — by training it on the thinking traces of a large reasoning model. DeepSeek demonstrated this dramatically in early 2025: they generated 800,000 high-quality reasoning examples with their big R1 model and fine-tuned small off-the-shelf models (Qwen and Llama, from 1.5 billion up to 70 billion parameters) on those traces. The result was small models that punched far above their weight on hard reasoning benchmarks — their 32B distilled model beat OpenAI's o1-mini, and a later 8B distilled version matched a 235B model on a competition-math benchmark. **[sourced]** That is the headline that made every CTO start asking about distillation.

So when someone says "we should distill," ask which idea they mean: *make a known capability cheaper to serve*, or *move a hard capability (usually reasoning) into a model small enough to own and deploy*. They have different economics, different risks, and different teams.

**A crucial distinction in 2026: who you distill from.**

- **White-box distillation** — you have the teacher's internal numbers (its full probability distribution over the next word, called *logits*). This is richer and is what the cutting-edge methods rely on. You need either an open-weight teacher or to be the company that owns the closed teacher.
- **Black-box distillation** — you only have the teacher's *text output* (you call an API, you get words back). You cannot see its internal probabilities. Most companies distilling from GPT, Claude, or Gemini are in this regime. The major API providers offer "distillation" features that capture your production traffic through a big model and fine-tune a small model on it. **[sourced]** New research in late 2025 (Microsoft's "Black-Box On-Policy Distillation") pushed black-box methods much closer to white-box quality, which matters because most enterprises will never get logit access to a frontier closed model. **[sourced]**

One more term you will hear constantly: **on-policy distillation**. It is the most important recent advance and it gets its own treatment in Sections 2 and 3. The one-line version: instead of training the student on the teacher's transcripts, you let the *student* attempt the task in its own words, and the teacher grades every word the student wrote. This fixes a deep flaw in the older approach and has quietly become a standard ingredient in how frontier labs train their models. **[sourced]**

---

## 2. How it works (the mechanism + intuition)

Let me build this up in layers, because each layer fixes a problem in the one before it. This is the part of the chapter to read slowly; the rest follows from it.

### Layer 0: Hard labels vs. soft labels — the original insight

Imagine training a model to classify an image. The normal way uses a **hard label**: "this is a dog," full stop. The model is told the answer is 100% dog, 0% everything else.

Now imagine a strong teacher model looks at the same image and says: "I'm 90% sure it's a dog, 7% it's a wolf, 2% it's a fox, and a sprinkle on everything else." That richer answer is a **soft label** — a full *probability distribution* over all the possible answers, not a single winner.

The original distillation insight (Geoffrey Hinton and colleagues, 2015) was that the soft label teaches *far more* than the hard label. The hard label says only "dog." The soft label says "dog, but it's the kind of dog that looks a little like a wolf and nothing like a teapot." That tells the student about the *structure of the problem* — which things are similar, which mistakes are reasonable, where the boundaries are. Hinton called these the **dark knowledge** in the teacher: information the teacher has learned that never shows up in the hard label. **[inference, building on well-established prior work]**

For language models, the same thing applies at every single word. When a language model writes, at each step it produces a probability distribution over the entire vocabulary — "the next word is 60% *the*, 15% *a*, 8% *this*…". A hard label would say only "*the*." The soft label hands the student the whole distribution. Training the student to match those distributions, word by word, is **token-level distillation**, and it is the dense, information-rich core of the field. **[inference]**

This is also the answer to *"why does learning from a teacher beat learning from raw data?"* — but I'll save the full version for Section 3.

### Layer 1: Off-policy (the naive approach) and its hidden flaw

The straightforward way to distill a language model: have the teacher generate a big pile of high-quality answers (or full reasoning traces), then fine-tune the student to imitate them. This is **off-policy** distillation — "off-policy" because the training examples come from the *teacher's* behavior, not the student's. DeepSeek's 800k-example R1 distillation is exactly this: pure imitation of teacher transcripts, no reinforcement learning. **[sourced]** It works remarkably well and is the right starting point for most teams.

But it has a structural flaw that gets worse the longer the task. The student is only ever shown the *teacher's* path through the problem — the clean trajectory a strong model takes. In real use, the student makes its own little mistakes, and those mistakes lead it into situations the teacher never demonstrated. Having never seen "how to recover from this specific wrong turn," the student compounds the error. The Thinking Machines write-up describes this precisely: off-policy training teaches the student in states it rarely actually visits, causing **compounding errors** and sometimes mere style-mimicry without the underlying competence. **[sourced]** The analogy: learning to drive by watching videos of an expert who never crashes. The first time you drift toward the shoulder — a situation the expert never showed — you have no idea what to do.

### Layer 2: Reinforcement learning fixes the path but starves on feedback

The reinforcement-learning (RL) approach fixes the path problem. Here the student attempts the task itself, and you reward it for good final answers. Because the student is learning from *its own* attempts, it naturally encounters and learns to handle its own mistakes — it is **on-policy**. This is how reasoning models are typically pushed to their highest scores.

But RL has the opposite problem: the feedback is incredibly *sparse*. The student writes a 2,000-word reasoning trace and gets back essentially one bit of information — "right" or "wrong." It does not learn *which* of the 2,000 words was the fatal mistake. The Thinking Machines framing is sharp: RL delivers roughly **O(1) bits of feedback per episode**, no matter how long the episode. **[sourced]** That makes RL slow and compute-hungry — you need enormous numbers of attempts for the signal to add up.

### Layer 3: On-policy distillation — the synthesis

On-policy distillation takes the good half of each approach and throws away the bad half:

1. The **student** generates its own attempt at the task — its own reasoning trace, in its own words. (This is the *on-policy* part, borrowed from RL: the student learns in the states it actually visits.)
2. The **teacher** then reads the student's trace and grades **every single token** — at each word the student chose, the teacher says how probable *it* would have considered that word. (This is the dense *distillation* part: O(N) bits of feedback for an N-token trace, not O(1).) **[sourced]**

So the student is corrected *on its own mistakes, word by word*. When the student takes a wrong turn, the teacher immediately marks the exact token where the reasoning went off the rails — what the write-up calls the **"forking tokens."** No separate reward model is needed; the teacher's own probabilities *are* the reward signal. **[sourced]**

Mechanically, the grading uses a quantity called **reverse KL divergence** — a measure of how far the student's word-choices are from the teacher's. Minimizing it pulls the student toward the teacher's distribution. The "reverse" direction matters: it is **mode-seeking**, meaning the student commits to *one* good way the teacher would solve the problem rather than trying to blur together all of the teacher's possibilities. For tasks with a right answer, committing to one good path is exactly what you want. **[sourced]**

### Token-level vs. sequence-level; online vs. offline

Two more axes worth holding in your head, because vendors and papers slice them differently:

- **Token-level** feedback grades each word (dense, the modern default). **Sequence-level** feedback grades the whole answer as a unit (sparse, closer to classic RL). On-policy distillation is token-level on student-generated sequences — the best of both. **[sourced]**
- **Offline** distillation generates a fixed dataset of teacher outputs once, then trains on it (cheap, simple, off-policy). **Online / on-policy** distillation interleaves student-generation and teacher-grading in a live loop (more expensive per step because the teacher must keep scoring fresh student output, but vastly more sample-efficient). **[inference]**

### The intuition, in one image

Off-policy distillation is **studying the teacher's worked solutions.** RL is **taking the exam and seeing only your final grade.** On-policy distillation is **a tutor sitting beside you while you work, who taps the page the instant you write the wrong step and shows you the better one.** The tutor version is why it learns so fast and so cheaply — which Section 3 quantifies.

---

## 3. Why it works (the underlying principle)

There is one principle under all of this: **the bottleneck in training a model is not data, it is the *amount of usable feedback per unit of effort*. Distillation works because a teacher provides denser, more informative feedback than raw labels or raw rewards ever can.** Everything else is a consequence.

Let me make the three reasons concrete.

**Reason 1 — A distribution carries more information than a single answer.** A hard label is one number: the right answer. A teacher's soft label is a whole shape: the right answer *and how confident to be* and *which wrong answers are near-misses* and *which are absurd*. Training on the shape lets the student learn the geometry of the problem in far fewer examples. This is why a distilled small model can sometimes outperform a same-sized model trained from scratch on the *original* data: it is learning from a smarter signal, not just more text. Meta's Llama 3.2 1B and 3B models were built exactly this way — pruned down from a larger Llama and then distilled using the *logits* of both an 8B and a 70B teacher; Google's Gemma 2 2B went further and replaced ordinary next-word training *entirely* with distillation from a larger model. The reported lesson across these efforts: **distillation from a larger teacher can buy more capability than simply adding parameters.** **[sourced]**

**Reason 2 — Dense feedback beats sparse feedback by orders of magnitude.** This is the on-policy distillation argument, and it shows up as raw money. Recall the numbers from Thinking Machines' replication of the Qwen3 recipe **[sourced]**:

- Reaching strong reasoning performance via **reinforcement learning** took roughly **17,920 GPU-hours**.
- Reaching *comparable or better* performance via **on-policy distillation** took roughly **1,800 GPU-hours** — and slightly higher accuracy (74.4% vs. 67.6% on the competition-math benchmark).
- Depending on how you account for teacher and dataset costs, that is between a **9× and 30× reduction in compute**; on a pure GPU-hours basis, about **18×**. **[sourced]**
- In a self-distillation experiment, on-policy distillation learned a target policy **7–10× faster**, for a cumulative **50–100× compute reduction**. **[sourced]**

Why so much cheaper? Because RL is paying for the same final accuracy with one bit of feedback per attempt, while on-policy distillation gets a bit per *token*. Same destination, thousands of times more sign-posts along the way. **[inference from sourced numbers]**

**Reason 3 — On-policy fixes the distribution-mismatch problem.** A model trained only on the teacher's clean transcripts is being tested on its own messy outputs — a mismatch between the world it learned in and the world it works in. The instant it makes its first uncorrected mistake, it is off the map. By training the student on *its own* trajectories, on-policy distillation guarantees the training distribution and the deployment distribution are the same one. This is the same insight behind the classic **DAgger** algorithm in imitation learning — and the Thinking Machines work explicitly traces its lineage there and to process-reward modeling. **[sourced]** This is also why off-policy distillation famously produces students that *sound* like the teacher (right style, right vocabulary) while being subtly, confidently wrong (wrong facts, broken reasoning): style is easy to copy from transcripts; robustness is not. **[sourced]**

**The principle, stated for a non-implementer:** *You are not buying a smaller model. You are buying a transfer of judgment from an expensive expert into a cheap apprentice, and the rate of transfer depends entirely on how rich the feedback is.* Transcripts are a decent textbook. Per-token grading of the apprentice's own work is a private tutor. The tutor is roughly an order of magnitude more efficient, and that single fact is reshaping how frontier models are trained — Qwen3, MiMo-V2-Flash, GLM-5, and DeepSeek-V4 all now use on-policy distillation as a core ingredient in their post-training, not as an exotic option. **[sourced]**

---

## 4. People & resources (orders of magnitude, with basis)

Numbers below are order-of-magnitude planning figures, not quotes. I give the basis for each so you can adjust to your situation. Treat these as **[inference]** built on the sourced cost figures and standard industry team shapes unless marked otherwise.

### The three tiers of effort

**Tier A — Black-box API distillation (the 80% case).**
*What it is:* You route production traffic through a frontier API (GPT, Claude, Gemini), collect the input/output pairs, and use the provider's built-in distillation/fine-tuning to produce a smaller hosted model.
- **Team:** 1–2 engineers, part-time. No ML PhD required. The provider hides the hard parts.
- **Time:** Days to a few weeks for a first working student.
- **Compute/money:** Often dominated by *data-collection* API spend, not training. Providers have run promotions giving away millions of free training tokens per day to seed adoption. **[sourced]** Training a distilled model costs the same as standard fine-tuning on these platforms — typically hundreds to low-thousands of dollars per run. **[inference]**
- **Data scale:** Thousands to low-tens-of-thousands of high-quality examples is often enough for a narrow task. **[inference]**
- **Payoff:** Per-request cost can drop roughly **10–25×** (e.g., GPT-4o → GPT-4o-mini class economics) at similar task quality. **[inference from published per-token pricing: ~$0.15/$0.60 per million tokens for a mini-class model]** **[sourced]**

**Tier B — Open-weight off-policy distillation (you own the student).**
*What it is:* You take an open teacher (or teacher traces) and fine-tune an open student (Qwen, Llama, Gemma, Phi) on your own hardware or rented GPUs, then deploy it yourself.
- **Team:** 2–5 people — at least one solid ML engineer who understands fine-tuning, plus data and infra support.
- **Time:** Several weeks to a couple of months including evaluation.
- **Compute/money:** A few hundred to a few thousand GPU-hours for a small student; **single-digit to low-tens of thousands of dollars** in rented compute for models in the 1B–14B range. The 70B class costs more. **[inference]** As a public anchor: the DeepSeek-R1 distillation produced six open models (1.5B–70B) from 800k generated examples — the *data generation* (running the big teacher) is the expensive part, the student fine-tuning is comparatively cheap. **[sourced]**
- **Data scale:** Tens of thousands to ~1 million examples for broad capability transfer; far fewer for a narrow task. **[sourced — DeepSeek used 800k]**

**Tier C — On-policy distillation (cutting edge, you run the live loop).**
*What it is:* The full tutor loop — student generates, teacher grades every token, repeat. This is where the 10–30× efficiency lives, but the engineering is harder.
- **Team:** 3–8 people with genuine post-training expertise — people who understand RL-style training loops, KL objectives, and serving a teacher and student simultaneously. This is a *research-engineering* skill, not a fine-tuning-script skill.
- **Time:** Weeks to a few months, plus real evaluation infrastructure.
- **Compute/money:** *Less* total compute than the RL alternative (the whole point — ~1,800 vs ~17,920 GPU-hours in the cited replication) **[sourced]**, but it requires running the teacher continuously during training, which is operationally heavier than a one-shot data dump. Mid-five to low-six figures of compute for serious runs. **[inference]**
- **Tooling note:** Thinking Machines built this on their **Tinker** training API, lowering the barrier; expect more such platforms through 2026. **[sourced]** **[speculation]** that by late 2026 on-policy distillation becomes a checkbox in major fine-tuning platforms, collapsing Tier C toward Tier B in difficulty.

### The cost shape to internalize

The expensive thing is almost never the student's training. It is **(a)** generating or grading with the teacher, and **(b)** building trustworthy *evaluation* — knowing whether your small model is actually good enough. Budget and staff for evaluation as a first-class line item, not an afterthought. **[advisory]**

---

## 5. Scenarios & stories (right tool / wrong tool)

### Where distillation is clearly the right tool

**The high-volume narrow workhorse.** A customer-support company runs 50 million ticket-classifications a month through a frontier model. The task is narrow and repetitive. They distill a small student; per-request cost falls more than 10×, latency drops, and behavior becomes more deterministic. This is the textbook win: **narrow, high-volume, latency-sensitive, well-specified.** The NVIDIA position paper makes exactly this argument — most agentic sub-tasks are "repetitive, narrow in scope," and a fine-tuned sub-10B model handles **80–90%** of them at lower cost and latency than a frontier model. **[sourced]** Their cited example: a 3.8B Phi-3-mini fine-tuned on financial NLP beat GPT-4o on 6 of 7 benchmarks at **29× lower cost.** **[sourced]**

**The data-can't-leave-the-building case.** A hospital cannot send patient records to a cloud API. A distilled small model runs *inside* the hospital's own infrastructure, analyzing records on-premises and never transmitting protected data. Distillation is what makes a model small enough to run where the data is forced to stay. **[sourced]**

**The on-device case.** Apple's on-device Foundation Models, Google's Gemini Nano on Pixel (Magic Cue, fully on-device), Meta's Llama 3.2 1B/3B for phones — all rely on distillation to fit capable behavior into a model that runs locally with no network. A model that ships in iOS or on a Tensor chip *must* be distilled; there is no other way to get frontier-flavored behavior into that footprint. **[sourced]**

**The reasoning-on-a-budget case.** You need multi-step reasoning (planning, math-like logic, structured extraction with chains of thought) but cannot afford to run a frontier reasoner per request. Distilling reasoning traces from a big reasoning model into a small student — exactly the DeepSeek-R1 playbook — gives you a fraction of the cost with most of the competence. **[sourced]**

### Where distillation is the *wrong* tool

**You need the frontier's full breadth.** If your product genuinely needs open-ended reasoning across unpredictable topics — a general assistant, an open research tool — distilling into a small model throws away the breadth that is the whole point. The small model is specialized; ask it something outside its lane and it fails confidently. **[inference]**

**The task isn't stable yet.** Distillation freezes a behavior into a model. If you are still discovering what the task even is — requirements shifting weekly — you will distill the wrong thing and re-do it. Stay on the flexible frontier model until the task stabilizes, *then* distill. **[advisory]**

**You have no real evaluation.** If you cannot measure whether the student is good enough, distillation is dangerous: it produces a model that *sounds* like the teacher (off-policy distillation is especially good at copying style) while being subtly wrong on facts or robustness. Without evaluation you will ship the confident-and-wrong failure mode and not notice. **[sourced — style-without-substance failure mode]**

**Volume is low.** If you serve a few thousand requests a day, the engineering and evaluation cost of distilling can exceed years of the API bill it saves. Just call the frontier model. **[advisory]**

**The legal/IP trap.** Distilling from a *closed competitor's* API may violate its terms of service, which typically forbid using outputs to train competing models. Anthropic's February 2026 disclosure explicitly flagged industrial-scale distillation as a security and IP concern, and major labs now actively defend against it. **[sourced]** Distill from models you are *licensed* to distill from (your own, or open-weight models with permissive licenses). **[advisory]**

### A cautionary tale

A team distilled a frontier model into a 7B student using the naive off-policy approach and shipped it. In testing on the teacher's clean examples it looked great. In production — facing real, messy user inputs the teacher's transcripts never covered — it drifted off the rails and compounded errors, while still *sounding* fluent and authoritative. They had reproduced the classic off-policy failure: right style, wrong substance, on inputs outside the training trajectory. The fix was on-policy distillation — let the student fail on its own inputs and have the teacher correct it token-by-token — after which robustness recovered. The lesson: **how you distill matters as much as whether you distill, and the failure is invisible until it meets reality.** **[inference, grounded in the sourced off-policy failure mode]**

---

## 6. Cross-industry usage & positioning (as of June 2026)

A field guide to who uses this, where it's table-stakes versus cutting-edge, and who leads.

**Healthcare.** *Table-stakes:* on-premises distilled small models for record analysis, coding/billing, and triage, chosen specifically so protected patient data never leaves the building. **[sourced]** *Cutting-edge:* distilling reasoning models for clinical decision support, gated behind heavy governance — regulators in 2026 increasingly demand documented **model lineage**, including the distillation process and data sources, for anything touching patient care. **[sourced]** Domain-tuned models like Palmyra-Med are cited as outperforming generalists at lower cost. **[sourced]**

**Finance.** *Table-stakes:* distilled small models for fraud detection, credit-risk scoring, and document processing inside VPC-isolated or on-prem environments to satisfy regulators. **[sourced]** The 29×-cheaper Phi-3-mini-beats-GPT-4o-on-financial-NLP result is the poster child. **[sourced]** Domain models like Palmyra-Fin follow the same logic. **[sourced]** *Leaders:* the regulated-LLM platform vendors and the labs shipping strong small open models.

**Legal.** *Table-stakes:* distilled models for clause extraction, classification, and review at volume, on controlled infrastructure for confidentiality. *Cutting-edge:* reasoning-distilled assistants for multi-step legal analysis — promising but governance-heavy, since lineage and auditability are demanded. **[inference, consistent with the sourced regulated-industry governance trend]**

**Customer support.** *Table-stakes, mature.* The clearest mass-market home for distillation: high-volume, narrow, latency-sensitive classification, routing, and drafting. This is the canonical "distill the frontier model into a mini" use case, and the API providers built distillation features largely for it. **[sourced]**

**Coding / developer tools.** *Cutting-edge moving fast.* Distilling reasoning models into smaller code models for autocomplete and agentic sub-tasks (lower latency, on-device or cheap-cloud). The "small models for agentic sub-tasks" thesis lands hardest here — most steps an agent takes are narrow and don't need a frontier brain. **[sourced]** *Leaders:* the open-weight model families (Qwen, DeepSeek, Llama) whose distilled variants developers fine-tune.

**Robotics.** *Cutting-edge / emerging.* On-policy and imitation-learning methods (the DAgger lineage that on-policy distillation descends from) are native to robotics, where compounding-error-on-your-own-trajectory has always been the central problem. Distilling large policy/vision-language models into small on-robot controllers is an active frontier. **[inference, grounded in the sourced DAgger lineage]**

**Consumer & on-device.** *Table-stakes and accelerating.* This is where distillation is now invisible infrastructure. Apple's on-device Foundation Models framework (iOS 26: system-wide writing tools, call screening, Visual Intelligence) and Apple's January 2026 deal to fall back to Gemini via Private Cloud Compute for harder tasks; Google's Gemini Nano on Pixel; Meta's distilled Llama 3.2 1B/3B; Microsoft's Phi family (90%+ of capability at ~5% of size). **[sourced]** *The governing fact of 2026:* a distilled 8B model now often outperforms a 2024-era 70B model, thanks to distillation, quantization, and better architectures stacked together. **[sourced]**

**Who leads, overall.**
- **Method leadership (on-policy distillation):** Thinking Machines Lab made it legible to the field and ships the Tinker platform; the Qwen3 team pioneered the production recipe; Microsoft Research pushed black-box on-policy distillation. **[sourced]**
- **Open distilled models people actually use:** DeepSeek (R1 distilled series), Alibaba's Qwen, Meta's Llama, Google's Gemma, Microsoft's Phi. **[sourced]**
- **Distillation-as-a-service:** OpenAI, Google, and the other API providers, for the black-box enterprise majority. **[sourced]**
- **Production adopters of on-policy distillation in post-training:** Qwen3, MiMo-V2-Flash, GLM-5, DeepSeek-V4 — it has crossed from research into how frontier models are actually built. **[sourced]**

**The positioning summary:** distillation for *cost/latency/privacy* is **table-stakes** across every regulated and high-volume industry — if you are not doing it where it fits, you are overpaying. Distillation for *reasoning transfer*, and especially **on-policy** distillation, is **cutting-edge but mainstreaming fast** — the labs use it, the platforms are starting to offer it, and the gap between "frontier lab technique" and "feature you can buy" is closing within 2026. **[inference]**

---

## 7. Learning path for a technical leader

No coding. The goal is to be able to *fund, scope, and challenge* this work credibly.

### Core mental models (the five you must own)

1. **Teacher → student transfer.** You are moving an expensive expert's judgment into a cheap apprentice. The model size shrinks; the goal is for the relevant *behavior* to survive.
2. **Soft labels carry "dark knowledge."** A full probability distribution teaches the *shape* of a problem — what's similar, what's a near-miss — which a single right answer cannot. This is why distilled small models can beat same-sized models trained on raw data.
3. **The feedback-density ladder.** Off-policy transcripts (rich but off the student's path) → RL (on the path but one bit of feedback) → **on-policy distillation** (on the path *and* a bit per token). Climbing this ladder is the story of the field, and each rung buys roughly an order of magnitude in efficiency.
4. **Distribution match.** A model must be trained on the kind of inputs it will face. On-policy methods enforce this by training the student on its *own* outputs; off-policy methods violate it and pay with brittle, style-over-substance students.
5. **The real cost is the teacher and the evaluation, not the student.** Plan accordingly.

### A concepts-only progression (in order)

1. Why a small model is cheaper, faster, and deployable where a big one isn't — the *business* case for compression.
2. Hard labels vs. soft labels; what "dark knowledge" means.
3. Off-policy distillation (imitate teacher transcripts) and its compounding-error / style-mimicry flaw.
4. Reinforcement learning's sparse-feedback problem (one bit per episode).
5. On-policy distillation as the synthesis: student generates, teacher grades every token; reverse-KL, forking tokens, mode-seeking.
6. White-box vs. black-box (logit access vs. text-only) and why most enterprises are black-box.
7. The economics: the 10–30× compute story, and the cost/latency/privacy wins of small specialists.
8. Governance: model lineage, licensing/IP limits on distilling from competitors, evaluation as a gate.

### A curated reading spine (few, high-value)

- **Thinking Machines Lab — "On-Policy Distillation" (Oct 27, 2025).** The single best plain-language-yet-rigorous explainer, with the cost numbers. Start here. **[sourced]**
- **DeepSeek-R1 model/report and the R1-Distill model cards (Jan 2025).** The proof that reasoning distills into small open models; concrete scale (800k examples, 1.5B–70B). **[sourced]**
- **NVIDIA — "Small Language Models are the Future of Agentic AI" (2025).** The clearest articulation of *why specialize*, with the 80–90% and 29× figures. **[sourced]**
- **Microsoft Research — "Black-Box On-Policy Distillation of LLMs" (Nov 2025).** Why the technique still works when you only have API text, which is the enterprise reality. **[sourced]**
- **A 2026 "Survey of On-Policy Distillation" and the awesome-on-policy-distillation list.** For breadth once the basics land. **[sourced]**

### Understanding checkpoints — *you understand it when you can…*

- …explain to a CFO why a smaller model can be *better* than a bigger one at a specific task, in one minute, without jargon.
- …draw the feedback-density ladder (off-policy → RL → on-policy) and say what each rung fixes and breaks.
- …explain why off-policy distillation produces fluent-but-wrong models, and why on-policy fixes it.
- …state when distillation is the *wrong* tool (unstable task, low volume, need for breadth, no evaluation, IP risk).
- …decide, for a given use case, between black-box API distillation, open-weight off-policy, and on-policy — and justify it on cost, control, and team capability.
- …name the two real cost centers (teacher + evaluation) and budget for them.

### How to evaluate an expert in an interview

Ask these, and listen for the structure of the answer, not the buzzwords.

**Q1. "Walk me through the difference between off-policy and on-policy distillation, and why we'd ever pay for the harder one."**
- *Strong:* Off-policy imitates teacher transcripts and breaks on the student's own mistakes (compounding error, style-over-substance); on-policy trains on the student's own outputs with dense per-token feedback, fixing the distribution mismatch; we pay for it because it's far more sample-efficient — order-of-magnitude less compute than RL for the same accuracy. Mentions it's now standard in frontier post-training (Qwen3, etc.).
- *Weak:* "On-policy is newer and better." No mechanism, no tradeoff.
- *Red flag:* Conflates on-policy distillation with plain RLHF, or thinks "on-policy" just means "more recent data."

**Q2. "What's a soft label and why does it teach more than a hard label?"**
- *Strong:* Full probability distribution; carries relative similarity / dark knowledge; lets the student learn problem structure in fewer examples; can beat same-sized models trained on raw data.
- *Weak:* "It's a probability instead of a yes/no." (True but shallow — can't say *why it helps*.)
- *Red flag:* Doesn't know the term, or thinks it's just label smoothing.

**Q3. "We want to distill GPT/Claude/Gemini into our own small model. What do you flag immediately?"**
- *Strong:* (a) **Legal/ToS** — distilling a competitor's outputs to train a competing model is typically prohibited; check licensing. (b) **Black-box constraint** — no logit access, so we're limited to text-output methods. (c) **Evaluation first** — without it we'll ship confident-wrong. (d) Asks whether the task is *stable* and *high-volume* enough to justify it.
- *Weak:* Jumps straight to "we'll fine-tune a Llama" with no mention of legality or evaluation.
- *Red flag:* Waves away the IP/ToS issue, or promises frontier-level *breadth* from a small student.

**Q4. "Where would you tell me *not* to distill?"**
- *Strong:* Low volume (API is cheaper than the engineering), unstable/ill-defined task, need for open-ended breadth, no reliable evaluation, IP-encumbered teacher. A senior person *volunteers* the wrong-tool cases.
- *Red flag:* Can't name a single situation where distillation is a bad idea. Distillation maximalists are a hiring risk.

**Q5. "Where does the cost actually go, and what's your rough budget shape?"**
- *Strong:* Student training is cheap; the money is in running/grading with the teacher and in building evaluation. Cites believable orders of magnitude and the on-policy ~10–30× efficiency vs. RL.
- *Red flag:* Thinks the student's GPU training run is the dominant cost, or has no feel for numbers at all.

**General red flags:** can't distinguish compression from reasoning-transfer; treats "distillation" as one monolithic thing; no opinion on evaluation; name-drops papers but can't explain the forking-token / reverse-KL intuition in plain words; dismissive of governance and licensing.

---

## 8. Team notes

### Roles and seniority

- **Tier A (black-box API distillation):** *No new role.* An existing senior backend or applied-ML engineer absorbs it. The provider handles the ML. Do *not* over-hire for this. **[advisory]**
- **Tier B (open-weight off-policy):** You need at least one genuine **ML / applied-research engineer** comfortable with fine-tuning, data pipelines, and evaluation. A data engineer and an infra/MLOps person round it out. 2–5 people. **[advisory]**
- **Tier C (on-policy distillation):** You need **post-training / RL-adjacent research engineers** — people who understand training loops, KL objectives, and serving a teacher and student together. This is scarce, expensive talent. 3–8 people, and at least one with real depth. **[advisory]**

The single most under-staffed role across all tiers is **evaluation engineering** — someone whose job is to know, rigorously, whether the student is good enough. Fund it explicitly. **[advisory]**

### Hiring signals & red flags

- **Green flags:** can explain *why* on-policy beats off-policy in plain words; volunteers the wrong-tool cases and the IP/legal constraints; talks about evaluation before talking about model architecture; has a feel for the cost numbers; knows distillation is now standard in frontier post-training, not exotic.
- **Red flags:** distillation maximalist with no failure cases; conflates the technique's variants; ignores licensing and governance; believes a small student can match a frontier model's *breadth*; thinks the student's training run is the main cost.

### Build vs. buy

- **Buy (managed distillation)** when you're black-box, your task is standard, and you value speed over control — most companies, most of the time. **[advisory]**
- **Build (own the student)** when privacy/on-prem is mandatory (healthcare, finance, defense), when you need on-device deployment, when per-request economics at your volume justify owning the model, or when the capability is core IP. **[advisory]**
- **Build the cutting edge (on-policy)** only when you have the rare talent *and* a stable, high-value capability worth squeezing the last order of magnitude out of. For most, **[speculation]** the right move is to *wait months* for on-policy distillation to become a platform feature rather than building the loop yourself. **[advisory]**

### Common failure modes

1. **Shipping an off-policy student that sounds right and is subtly wrong** — fluent, teacher-flavored, brittle on real inputs. The most common and most dangerous failure; invisible without strong evaluation. The fix is on-policy distillation and/or far better evaluation. **[sourced — style-without-substance failure mode]**
2. **No evaluation gate** — you can't tell if the student is good enough, so you ship on vibes.
3. **Distilling an unstable task** — requirements move, the frozen student is now wrong, you re-do everything.
4. **Over-engineering Tier A** — building a research team to do what an API checkbox does.
5. **Ignoring licensing/IP** — distilling a competitor's closed model in violation of its terms; a real and rising legal and security concern in 2026. **[sourced]**
6. **Chasing breadth from a small model** — specializing a model and then being surprised it fails outside its lane.
7. **Mis-budgeting** — funding the cheap part (student training) and starving the expensive parts (teacher inference, evaluation).

### The one-paragraph takeaway for a board

Distillation turns an expensive frontier model into a cheap, fast, deployable specialist by transferring the big model's *judgment* into a small one. For high-volume, narrow, or privacy-bound tasks it is now table-stakes and saves real money (often 10–30×). The 2025–2026 advance — **on-policy distillation**, where the small model attempts the task and the big model grades every word — closed most of the quality gap at roughly an order of magnitude less compute than reinforcement learning, and it is now used inside how frontier models themselves are built. The risks are not technical exotica; they are mundane and manageable: pick the right tasks, respect licensing, and — above all — invest in the evaluation that tells you whether the small model is actually good enough.

---

## Sources

- Thinking Machines Lab — *On-Policy Distillation* (Kevin Lu et al., Oct 27, 2025). https://thinkingmachines.ai/blog/on-policy-distillation/
- Thinking Machines Lab — blog index. https://thinkingmachines.ai/blog/
- DeepSeek — *DeepSeek-R1-Distill-Llama-70B* model card (Jan 2025). https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B
- DeepSeek — *DeepSeek-R1-Distill-Llama-8B* model card (Jan 2025). https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B
- BentoML — *The Complete Guide to DeepSeek Models: V3, R1, V4 and Beyond* (2025–2026). https://www.bentoml.com/blog/the-complete-guide-to-deepseek-models-from-v3-to-r1-and-beyond
- Ye, Dong, et al. (Microsoft Research) — *Black-Box On-Policy Distillation of Large Language Models* (arXiv, Nov 2025). https://arxiv.org/pdf/2511.10643
- *A Survey of On-Policy Distillation for Large Language Models* (arXiv, 2026). https://arxiv.org/html/2604.00626v2
- *Rethinking On-Policy Distillation of Large Language Models: Phenomenology, Mechanism, and Recipe* (arXiv, Apr 2026). https://arxiv.org/html/2604.13016v1
- *awesome-on-policy-distillation* curated list. https://github.com/chrisliu298/awesome-on-policy-distillation
- NVIDIA Research — *Small Language Models are the Future of Agentic AI* (2025), via The AI Insider. https://theaiinsider.tech/2025/08/18/thinking-small-small-language-models-could-reshape-agentic-ai/
- *Small Language Model Agents* knowledge base. https://agentwiki.org/small_language_model_agents
- OpenAI — *Model Distillation in the API* (2024–2025). https://openai.com/index/api-model-distillation/
- OpenAI — *GPT-4o mini: advancing cost-efficient intelligence*. https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/
- pricepertoken — *GPT-4o mini API Pricing 2026*. https://pricepertoken.com/pricing-page/model/openai-gpt-4o-mini
- Redis — *Model Distillation for LLMs: Cut Costs & Boost Speed in 2026*. https://redis.io/blog/model-distillation-llm-guide/
- *On-Device LLMs: State of the Union, 2026* (V. Chandra). https://v-chandra.github.io/on-device-llms/
- Edge AI and Vision Alliance — *On-Device LLMs in 2026: What Changed, What Matters, What's Next* (Jan 2026). https://www.edge-ai-vision.com/2026/01/on-device-llms-in-2026-what-changed-what-matters-whats-next/
- TrueFoundry — *LLM Deployment in Regulated Industries: HIPAA, SOC2 & GDPR Playbook for 2026*. https://www.truefoundry.com/blog/llm-deployment-in-regulated-industries-hipaa-soc2-and-gdpr-playbook-for-2026
- ModelOp — *SLM vs LLM* (AI governance). https://www.modelop.com/ai-governance/slm-vs-llm
- MachineLearningMastery — *Introduction to Small Language Models: The Complete Guide for 2026*. https://machinelearningmastery.com/introduction-to-small-language-models-the-complete-guide-for-2026/
