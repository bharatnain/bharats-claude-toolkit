# AI Therapy: Engineering Deep-Dive (Companion to the Market Report)

> **What this is:** a plain-English engineering companion to `REPORT.md`, written for a smart non-technical reader. It explains what each technical choice *means*, who can do it, what it costs, and what data it needs — and corrects the compensation picture.
> **Scope:** 16 core techniques explained from scratch + per-company engineering deep-dives (Slingshot/Ash deepest; genuine builders deep; GPT/Claude/Gemini "wrapper" vendors given a real technical read) + a two-column compensation model + a global talent map.
> **Produced by:** the same autonomous research team (72 agents, ~2.35M tokens), grounded in the existing dossiers and extended with fresh research.
> **Trust model:** claims carry `sourced` / `inference` / `speculation` labels; the compensation model is explicitly **inference** (verifier confidence: medium) built from frontier-lab comparables, equity math, and the user's firsthand industry input. `REPORT.md` and the dossiers are unchanged; this supersedes only the compensation interpretation.


---

## Executive Introduction

If you remember one thing from this document, make it this: in AI therapy, almost nobody is building the artificial intelligence itself. The clever-sounding "AI model" at the center of every product in this report is, with one or two partial exceptions, rented from a handful of outside suppliers (OpenAI, Anthropic, Google, or an open-weight model like Qwen) and then wrapped in layers of clinical and safety machinery. The real engineering — the part a competitor cannot copy over a weekend — lives in those wrapping layers, not in the model. That single truth reframes how you should value every company here.

This deep-dive looks at 17 players across the field — from consumer chat apps (Slingshot/Ash, Youper, Sonia, Earkick, Headspace's Ebb) to enterprise benefits platforms (Spring Health, Lyra, Talkspace, SonderMind, BetterHelp) to regulated clinical vendors (Limbic, Jimini/Sage, Wysa, ieso/Velora) and one academic project (Therabot at Dartmouth). It is organized into sections you can read in any order, but they build on each other:

- The TECHNIQUE sections explain the common recipe — a rented foundation model, plus guardrails, crisis-detection classifiers, evaluation harnesses, and (in the serious players) a human therapist in the loop. Read these to understand what "AI therapy" actually is under the hood.
- The COMPANY sections are dossiers on each player: what they built, what they claim, and what holds up under scrutiny. A recurring warning runs through them — many headline statistics ("100% accurate," "92% improvement") are the company's own marketing, not independently verified science. We flag these rather than repeat them as fact.
- The COMP (compensation) and TALENT sections show who these companies hire and pay, which is a useful tell: research-lab pay and titles signal genuine model work; standard software-engineer pay signals assembly of off-the-shelf parts.

Here is how to read the whole thing without getting lost. Because the model is rented by nearly everyone, you cannot tell these companies apart by their AI. You tell them apart by three things: (1) the proprietary data they own — real therapy transcripts, long-term patient-outcome records, hand-labeled clinical examples; (2) the safety and evaluation engineering they have built — the systems that catch a suicidal user and that prove the product behaves; and (3) their regulatory positioning — whether they have earned medical credentials or are deliberately calling themselves "wellbeing" to dodge the FDA. Where those three things are strong, there is a durable business. Where they are thin, you are looking at a wrapper that a well-funded newcomer could rebuild quickly. Part E, which closes the document, re-rates every company through exactly this engineering lens and names each one's real defensible asset in a single line.


---

# Part A — The Techniques, Explained

_Each technique answers six questions: what it is + its impact, the skill set, difficulty (1–5) and why, who in the world can do it, cost, and data requirement & scale._


### Pre-training (a foundation model from scratch)

**1. What it is + its impact.**
Pre-training is the act of building the "brain" of an AI model from nothing. You take a blank network (random numbers, no knowledge) and feed it a huge slice of the internet — trillions of words — making it play a fill-in-the-blank game trillions of times until it learns grammar, facts, and reasoning patterns. The output is a "foundation model" (think GPT-4, Claude, Llama, Gemini): a raw, general-purpose engine that everything else is built on top of.

Analogy: most companies *buy a car and customize it* (rent an existing model via API, or fine-tune an open one). Pre-training is *building the car factory and the engine from scratch.* The analogy breaks in one important way — a car factory's output is predictable, whereas a pre-training run is a multi-million-dollar science experiment where you don't fully know how good the model will be until it finishes weeks later.

What choosing this changes for a business:
- **Cost:** Moves you from a low-millions software budget to a tens-to-hundreds-of-millions capital expense (compute, talent, infrastructure). It is one of the most expensive things a software company can do.
- **Moat:** Done at frontier scale, it is the deepest moat in AI — extremely few players can match it. Done at small scale, it is *not* a moat; the model itself is a commodity and the only real moat becomes your proprietary data or distribution.
- **Risk:** High and front-loaded. The bet is largely spent before you know if it worked; a single botched run can waste eight figures. Open models (Llama, DeepSeek, etc.) keep getting better and "good enough," so building your own general model from scratch is increasingly hard to justify unless you have a specialized data advantage or strategic reason (sovereignty, secrecy, a domain no one else serves).
- **Product:** Gives you total control — your own data, your own behavior, no dependency on OpenAI/Anthropic/Google and no per-call API fees at scale. That control is the main reason to do it.

**Hype check:** "We built our own foundation model" is a phrase that gets stretched. There's a 1,000x gap between *frontier* pre-training (hundreds of millions of dollars, a handful of labs) and *small-scale* pre-training (a small model can be pre-trained for thousands to low-millions of dollars — one research group reported a usable small foundation model for about $1,500). Both are technically "pre-training from scratch," but they are not the same league. If a vendor implies frontier-level capability from a modest budget, be skeptical — and ask which of these two things they actually mean.

**2. Skill set required.**
A specialized **distributed-systems + ML research** team, not a typical app/web team. You need: ML researchers who understand model architecture and the "scaling laws" that predict how big a model and how much data you need; distributed-systems engineers who can make thousands of GPUs train as one machine reliably for weeks (the hardest part is often the plumbing, not the math); data engineers to collect, clean, and de-duplicate trillions of words; and infrastructure/hardware specialists. This is a rare combination — the systems engineering at scale is the genuinely hard, scarce skill.

**3. Difficulty: 5 / 5 — and why.**
This is the top of the scale and it spans a huge range *within* that 5. Small-scale pre-training (a tiny model on a modest dataset) is a hard but doable expert project — weeks, not a weekend, and clearly beyond a hobbyist. *Frontier* pre-training is a multi-year, eight-to-nine-figure organizational effort: tens of thousands of GPUs running for weeks without fatal failures, the cost largely committed up front, and success uncertain until the end. Almost nothing else in commercial software combines this capital intensity, this much specialized scarce talent, and this much irreducible uncertainty.

**4. Who in the world can actually do it.**
Two very different answers:
- **Frontier scale (a GPT-4-class general model):** Fewer than a few hundred people in the world have actually led one, concentrated in roughly a dozen well-funded organizations — OpenAI, Anthropic, Google DeepMind, Meta, Mistral, DeepSeek, xAI and a few national/big-tech efforts. *(inference, based on the small known set of frontier labs.)*
- **Small/modest scale:** A strong ML research team (hundreds of organizations, plus academic labs) can pre-train a small or domain-specific foundation model. A general web/app team cannot do either without hiring specialists.

**5. Cost — orders of magnitude.**
Three tiers, basis noted:
- **Frontier general model:** roughly **$100M to $1B+** all-in. Anthropic's CEO put current frontier training runs at $100M–$1B, with $1B+ runs expected by 2027. GPT-4-class compute alone is estimated at $78–100M+; Gemini Ultra ~$191M. Costs have grown ~2.4–2.6x per year. Breakdown: hardware ~47–67%, R&D staff ~29–49%, energy ~2–6%.
- **A capable open model (compute-only, marginal):** roughly **single-digit millions for the final run** — DeepSeek-V3's *final pre-training run* was ~2.8M GPU-hours, community-estimated at ~$5.6M. **Contested:** this figure is widely misread as the model's "total cost." It excludes R&D, failed runs, and the ~$1B+ in GPU infrastructure; one analysis put the true buildout at ~$1.6B. The $5.6M is the marginal cost of one successful run, not the cost to stand up the capability.
- **Small / specialized model:** **thousands to low-millions** — one reported research effort trained a small foundation model for ~$1,500.

The lesson: the "cheap" headlines are real but measure only the last successful run; the cost to *be able* to do this at all is far higher.

**6. Data requirement & scale — and why it's the real moat.**
Frontier pre-training consumes **trillions of words** — Llama 3 used 15+ trillion tokens (very roughly 10+ trillion words), scraped from the public internet, books, code, and licensed sources, then heavily cleaned and de-duplicated. Garbage data yields a garbage model, so data *quality and curation* matter as much as raw volume.

Why data is the durable moat: the public internet is finite and largely available to everyone, so a web crawl is *not* differentiated. What can't be copied is **proprietary, exclusive, or hard-to-collect data** — your customers' interactions, licensed private corpora, a specialized domain (legal, medical, financial, scientific) no competitor can access. For most companies, pre-training a general model from scratch makes little sense, but pre-training (or fine-tuning) on *unique data* is where a real, defensible advantage lives. As public text gets exhausted, exclusive data rights are becoming the scarcest input in the field. *(inference, well-supported by the sourced data-scale and concentration claims.)*

**Bottom line for a non-technical decision-maker:** Pre-training from scratch is the most expensive, talent-scarce, and risky thing you can do in AI — justified only by either frontier ambition with frontier funding, or a genuinely unique data asset. For nearly everyone else, renting or fine-tuning an existing model is the rational choice, and "we trained our own foundation model" deserves the follow-up question: *at what scale, and on what data no one else has?*


### Continued / domain-adaptive pre-training (Slingshot's actual move on Qwen3-235B)

**1. What it is + its impact.**
Instead of building a giant AI model from scratch (which costs hundreds of millions and takes a world-class lab), Slingshot took an already-finished open-source model — Alibaba's Qwen3-235B, which is free to use commercially — and kept training it on a huge pile of mental-health and therapy material. Think of it like hiring a brilliant, broadly-educated graduate and putting them through an intensive residency in clinical psychology: you didn't teach them to read and reason (that already happened), you steeped them in one profession until its language, frameworks, and instincts became second nature. That's "continued" (you resume training where someone else stopped) and "domain-adaptive" (you point that training at one domain). Slingshot's model "Ash" then went through two more steps on top: clinicians hand-tuned its bedside manner, and a reward system refined it from real usage [sourced]. **Why a CEO should care:** this is a fast, cheap path to a *differentiated* product. The cost and moat do not live in the model architecture — anyone can download Qwen3 — they live in the proprietary therapy data and clinical know-how poured in afterward. The risk: you are renting your foundation from Alibaba. If the base model has flaws, licensing changes, or you need a capability it lacks, you're partly hostage to someone else's roadmap. In a regulated, safety-critical domain (therapy), that dependency plus the inherent unpredictability of LLMs is the real exposure, not the engineering.

**2. Skill set required.**
A strong applied-ML / ML-infrastructure team — people who can run distributed training across many GPUs (the kind of work that uses tools like DeepSpeed/ZeRO to fit a 235-billion-parameter model across a cluster), curate and clean massive datasets, and design fine-tuning and reinforcement-learning pipelines [sourced: Nebius case study describes DeepSpeed/ZeRO-3, three-phase training]. Critically, it also requires deep *domain* expertise — Slingshot pairs ML engineers with clinical psychologists who shape the data and judge the outputs [sourced]. It does not require the rarer skill of inventing a foundation model from nothing.

**3. Difficulty: 3 out of 5.**
Harder than fine-tuning (the weekend-project end of the spectrum), much easier than training a frontier model from scratch (the eight-figure, multi-year, few-labs-on-Earth end). The technique itself — continued pre-training — is well-understood and documented [sourced]. What makes it a "3" rather than a "2" is the scale (a 235B model is large enough that just running the training without crashing or wasting money is a serious infrastructure feat) and the difficulty of assembling and cleaning a domain dataset big enough to matter. The genuinely hard, defensible part isn't the algorithm; it's the data and the clinical judgment layered on top [inference].

**4. Who can actually do it.**
A competent, well-funded ML team — not a weekend hacker, but also not a secret club. Globally this is plausibly *low thousands* of teams who could run continued pre-training on a 235B open model if they had the data and the GPU budget [inference]. The number who can do it *well in a specific regulated vertical like therapy* is far smaller, because the bottleneck is proprietary clinical data and expert oversight, not engineering talent [inference]. So: not "any web team," comfortably within reach of "a strong ML team," and the truly defensible execution is the work of a few hundred organizations at most [inference/speculation].

**5. Cost (orders of magnitude).**
- **Talent:** Slingshot has ~32 employees total [sourced: Tracxn profile via search, 2026] and raised $93M in Series A funding [sourced: multiple, July 2025]. So the whole company — not just this one technique — runs in the *tens of millions* of dollars. A focused continued-pre-training effort by a small expert team is a *low-single-digit-millions* endeavor in talent terms [inference].
- **Compute:** Specific GPU-hours and dollar cost for Slingshot's run are **unknown — not found.** Continued pre-training of a model this size on domain data is typically *hundreds of thousands to low millions of dollars* per major run, far below the *tens-to-hundreds of millions* needed to pre-train a frontier model from scratch [inference]. Slingshot used Nebius GPU clusters and states this was "multiple times cheaper than using training API providers" [sourced: Nebius case study], which signals deliberate cost optimization but gives no absolute number.
- **Infra:** Rented cloud GPUs (Nebius), orchestrated with SkyPilot and DeepSpeed/ZeRO-3 [sourced]. No need to own a datacenter — capex is effectively zero, it's all opex.
- **Bottom line:** This is a *seven-to-low-eight-figure company-level* effort, with the *single technique* likely costing *low-seven-figures* in compute — orders of magnitude cheaper than building a base model [inference].

**6. Data requirement & scale — and why it's the moat.**
Slingshot describes training on "one of the largest and most diverse datasets of behavioral health data ever assembled," spanning many therapeutic modalities — CBT, DBT, ACT, psychodynamic, motivational interviewing, Gestalt [sourced: Nebius case study and Slingshot launch materials, July 2025]. Exact token counts and sourcing are **unknown — not found**; for reference, the original Qwen3 base was trained on ~36 trillion tokens [sourced: Qwen blog, 2025], and a domain-adaptive continuation is usually a small fraction of that — often *billions to low-tens-of-billions* of tokens [inference]. **This is the actual moat.** The model weights are free and public; the therapy corpus, the clinical relationships that produce and vet it, and the regulatory/ethical care to use it are not reproducible by a competitor with a credit card [inference]. Whoever controls the best proprietary behavioral-health data — and the clinicians to label and judge it — controls the product, regardless of which open model sits underneath.

**Hype check.** The underlying technique is a sensible, increasingly standard industry move, not a scientific breakthrough — continued/domain-adaptive pre-training on an open base model is something many serious teams do. Calling it "the world's first foundation model for psychology" [sourced: Slingshot marketing] is a *positioning* claim about the application and dataset, not evidence of a novel training method. The genuinely impressive and defensible parts are the proprietary clinical dataset, the clinician-in-the-loop tuning, and the operational discipline to do it cheaply — *not* the act of continued pre-training itself, which the marketing language somewhat inflates [inference/contested].


### Supervised fine-tuning (SFT)

**1. What it is + its impact.**
Supervised fine-tuning means taking a model that already exists — either an open-weights base model (Llama, Mistral, Qwen) or a commercial model exposed through a vendor's fine-tuning API — and showing it a few hundred to a few hundred thousand worked examples of "here is an input, here is the ideal output." The model nudges its existing knowledge toward your desired style, format, and task. The analogy: you are not educating a new graduate from scratch (that is *pretraining*, which costs tens to hundreds of millions); you are giving an already-educated hire a week of on-the-job training so they answer the way your company wants. **Where the analogy breaks:** unlike a human, the model does not "understand" your business — it pattern-matches the format and tone of your examples. Feed it 500 sloppy examples and it learns to be sloppy fluently. It also will not reliably learn *new facts* this way; SFT mostly shapes behavior and format, not knowledge (knowledge injection is better done with retrieval/RAG or much larger data).

What choosing SFT changes about the business:
- **Product:** You get consistent voice, reliable output formats (JSON, your templates), and better performance on a narrow task than a generic prompted model.
- **Cost:** Inference can get *cheaper* — a fine-tuned small model often matches a prompted large model on a narrow task, so you stop paying for the big model on every call.
- **Moat:** The moat is weak-to-moderate and lives almost entirely in the *data*, not the technique. The technique is commoditized; your curated examples are not.
- **Risk:** Overfitting (the model gets brittle outside your examples), "catastrophic forgetting" (it gets worse at general tasks), and lock-in if you fine-tune a closed vendor model you cannot export.

**2. Skill set required.**
For the basic version: a competent ML engineer or a strong generalist software engineer who can run a training script — not a research scientist. Open-source toolchains (Hugging Face, Axolotl, Unsloth, vendor fine-tuning APIs) have turned the *mechanics* into largely a configuration exercise. The genuinely hard, valuable skill is **data curation and evaluation** — deciding what good examples look like, cleaning the dataset, and building tests to know whether the fine-tune actually improved things. That is closer to a thoughtful data/product skill than deep ML math. *(Inference.)*

**3. Difficulty: 2/5 — and why.**
A first LoRA fine-tune of a 7B open model on a clean dataset is genuinely a weekend project for a capable engineer — the open-source ecosystem and managed APIs do the heavy lifting. It is not a 1 because doing it *well* — building evaluations, avoiding overfitting and forgetting, getting the data right, and deploying the result — is real engineering that separates a demo from production. It is nowhere near a 5; a 5 is pretraining a frontier model. The hype to watch: vendors marketing "fine-tuning" as transformational AI capability. For most teams it is a competent, well-understood technique, not a breakthrough — the leverage is in the data, not the act of fine-tuning. *(Inference, calibrating common marketing language.)*

**4. Who can actually do it.**
This is broadly accessible — far more than "a few hundred people." Tens of thousands of engineers worldwide can run a basic SFT job today, and any company with a competent ML or strong backend team can do it. Doing it *excellently* for a hard domain (curating great data, building rigorous evals, squeezing out frontier-level task performance) narrows to a strong ML team — thousands, not hundreds. *(Inference.)*

**5. Cost — orders of magnitude.**
Spread across roughly three tiers (basis: 2025-2026 GPU-rental pricing reports; treat specific figures as indicative, not authoritative):
- **Parameter-efficient (LoRA/QLoRA) on a small open model (~7B):** tens of dollars to low thousands per training run. Reported figures put QLoRA on a single H100 at ~8-12 hours for roughly $10-16; small instruction tunes run ~1 hour on one A100. *(Sourced, see below — vendor blogs, treat as approximate.)*
- **Full fine-tuning of a ~7B model:** hundreds to low tens of thousands per run; reported ~$250-510 on 8x H100 over 24-48 hours, and full tunes of larger Mistral-class models cited around $12,000. *(Sourced — vendor blogs, approximate/contested across sources.)*
- **Talent and infrastructure dominate, not raw compute.** The recurring cost is one or a few engineers' salaries plus the iteration loop (you rarely train once — you train, evaluate, fix data, retrain many times), so realistic total project cost is "a few engineer-months," i.e. low-to-mid five or six figures all-in, not the compute line item. *(Inference.)*

Orders of magnitude: a hobbyist SFT run ≈ **$10-100**; a serious production fine-tune of a small model ≈ **$1k-10k in compute**; the surrounding human/eval effort ≈ **$10k-100k+**. Pretraining, by contrast, is **$1M-$100M+** — a completely different category.

**6. Data requirement & scale — and why it's the moat.**
- **What:** Pairs of input → ideal output in your target task, format, and voice. Quality beats quantity decisively.
- **How much:** Surprisingly little can work. The LIMA paper showed a 65B model fine-tuned on just **1,000 carefully curated examples** produced strong, well-formatted responses, supporting the view that the model already "knows" most things from pretraining and SFT mainly teaches it *how to respond*. *(Sourced — arXiv 2305.11206, May 2023.)* In practice teams use hundreds to tens of thousands of examples depending on task breadth. *(Inference.)*
- **How sourced:** Internal logs, expert-written examples, customer transcripts, support tickets, or — commonly and controversially — outputs from a stronger model ("distillation"), which raises licensing and terms-of-service questions. *(Inference; the licensing tension is contested.)*
- **Why it's a moat:** Because the *technique* is commoditized and the *base models* are shared, the only durable differentiator is proprietary, high-quality, domain-specific example data that competitors cannot easily reproduce — e.g. years of your own expert-reviewed interactions. A generic public dataset gives you no edge; a hard-won private one does. *(Inference.)*

**Bottom line for a non-technical decision-maker:** SFT is a mature, accessible, moderately cheap way to make an existing model behave the way you want on a specific task. It is a *capability multiplier on your data*, not a magic source of intelligence. If someone pitches fine-tuning as a defensible moat, the right question is not "can you fine-tune?" (almost anyone can) but "what proprietary data are you fine-tuning on, and can a competitor get it too?"


### Reward modeling (teaching a model what "good" looks like)

**1. What it is + its impact.** A reward model is a *second* AI whose only job is to score how good another AI's answer is. You can't write down a rule for "helpful, honest, well-written" — so instead you show humans pairs of answers and ask "which is better?", collect tens of thousands of these judgments, and train a model to predict those preferences. That trained judge then grades millions of the main model's attempts automatically, and the main model is tuned to chase a higher score. Analogy: instead of writing an exam answer key (impossible for open-ended writing), you train an examiner by having them watch a master grader rank student essays until the examiner internalizes the master's taste — then you let the examiner grade at machine speed. **Where the analogy breaks:** a human examiner *understands* why an essay is good; a reward model only learned a statistical shadow of human preference, so the main model will eventually find ways to score high that humans actually dislike (flattery, padding, confident-sounding nonsense). This is "reward hacking," and it's why you must keep collecting fresh human data — the moat and the cost both live here. **Impact on a business:** this is the technique that turned raw, unusable GPT-3-style models into the polite, on-brand assistants people pay for. It is the difference between a model that *can* answer and one that answers the way *your* customers want. It's a controllable lever over tone, safety, and "feel" — but it's a recurring expense, not a one-time build, and it directly controls your biggest brand/safety risks.

**2. Skill set required.** Strong machine-learning research engineers comfortable with reinforcement learning, large-model training, and distributed GPU infrastructure — plus, crucially, an *operations* function most people forget: people who design labeling guidelines, recruit and manage human annotators, and run quality control on the data. The data-operations half is as decisive as the ML half.

**3. Difficulty 4/5 and why.** A toy reward model on a public dataset is a graduate-student weekend project — that part is well-documented (inference). But doing it *well at production scale* — clean preference data, a judge that doesn't get gamed, stable RL training, and constant refreshing to fight reward hacking — is genuinely hard and is where frontier labs spend serious effort (inference, supported by reward-hacking literature below). It's not an eight-figure multi-year moonshot on its own, but it's a sustained, expensive, expert-run pipeline, not a script you run once.

**4. Who can actually do it.** The *basic* version: any strong ML team (thousands of teams worldwide) — inference. The *frontier* version that produces a top-tier assistant — robust against gaming, at scale, continuously refreshed — is realistically a few thousand people across a few dozen serious labs and companies, not a few hundred and not "any web team" (inference, contested at the margins).

**5. Cost (orders of magnitude).** Three buckets. (a) *Compute* to train the reward model and run the RL tuning: meaningful but typically smaller than the original pretraining of the base model — think tens of thousands to low millions of dollars per serious cycle (inference). (b) *Human preference data*: the dominant and recurring line item — roughly tens of thousands to hundreds of thousands of comparisons, often six figures of labeling spend, sometimes much more for expert domains (sourced + inference). (c) *Talent*: a handful of senior ML researchers plus a labeling-operations team — the expensive part is they're scarce and needed continuously. Net: a credible production effort is mid-six to seven figures *per year ongoing*, not a one-time capital cost (inference).

**6. Data requirement & scale — and why it's a moat.** The raw material is human preference judgments: a prompt, two (or several) candidate answers, and a human verdict on which is better. Industry practice is roughly ~50,000 labeled preference samples for many applications, ranging into the hundreds of thousands for high quality (sourced). It's sourced by paying trained annotators — and for expert domains (medicine, law, code) you need expensive *expert* annotators, which is a real bottleneck (sourced). **Why it's a moat:** the data encodes *your* definition of good — your tone, your safety lines, your domain expertise — and it has to be continuously regenerated because a static judge gets gamed by the model it's grading (sourced). A competitor can copy the published *method* in an afternoon; they cannot copy years of accumulated, domain-specific preference data and the labeling operation behind it. **A note on the marketing.** Two cautions. First, "AI feedback" (RLAIF / Constitutional AI) — using an AI instead of humans to generate the preferences — is real and cuts labeling cost, but it inherits a bootstrapping ceiling: the result is bounded by the quality of the AI doing the judging, and adds its own failure modes like sycophancy and amplified bias (sourced). Treat "we use AI feedback, so it's basically free" as a half-truth. Second, since late 2024 the frontier has shifted: for tasks with a *checkable* right answer (math, code), labs increasingly skip the human-preference reward model and reward against verifiable signals directly (sourced). So "reward modeling" is essential for *taste and safety* but is no longer the only or even primary lever for *reasoning* — vendors who imply one technique does everything are overselling.


### RLHF / RLAIF (reinforcement learning from human/AI feedback)

**The one-line version:** RLHF is how a raw language model gets turned from a know-it-all that rambles, ignores instructions, and says toxic things into a helpful, polite assistant. It is the training step that taught GPT-3 to become ChatGPT. RLAIF is the cheaper variant where another AI does most of the grading instead of humans.

---

**1. What it is + its impact**

A base language model is trained only to predict the next word from the internet. It is knowledgeable but unaligned: it doesn't reliably follow instructions, refuse harmful requests, or pick the response a person would actually prefer. RLHF fixes the *behavior*, not the *knowledge*.

The mechanism is a three-step loop *(sourced, InstructGPT/Ouyang et al. 2022)*: (1) show humans several answers to the same prompt and have them rank which is best; (2) train a small "judge" model — the *reward model* — to predict those human preferences; (3) use that judge as an automated scorer to nudge the main model toward higher-scoring answers.

**Analogy:** It's like training a new employee. The base model is a brilliant but tactless intern who has read every book but has no workplace manners. You don't re-teach them facts — you give thousands of rounds of "this answer was better than that one" feedback until they internalize good judgment. The reward model is essentially a *simulated manager* you build so you don't need a real human grading every single attempt.

**Where the analogy breaks:** A human intern generalizes from a few corrections; the model needs tens of thousands of comparisons and can "game" its simulated manager — finding answers that score high with the judge but are actually bad (called *reward hacking*) *(inference, well-documented failure mode)*. The model isn't reasoning about why an answer is good; it's optimizing a number.

**RLAIF / Constitutional AI** swaps the expensive human graders for an AI grader guided by a short written set of principles (a "constitution") *(sourced, Anthropic, Constitutional AI 2022)*. This collapses the biggest cost and bottleneck — human labeling — and is a large part of why frontier labs can iterate quickly.

**What choosing this changes for a business:**
- *Product:* This is the difference between a demo that impresses and a product people trust. Tone, safety, instruction-following, and refusal behavior all come from this step. It is table stakes for any customer-facing assistant.
- *Cost/moat:* The *technique* is now public and partly commoditized. The *moat* is the preference data and the operational machinery to collect and curate it cleanly — not the algorithm.
- *Risk:* Done badly it produces a sycophantic model (agrees with everything), an over-refusing model (useless), or one with hidden reward-hacking behaviors. These are subtle and only show up in production.

**Hype check:** Vendors selling "proprietary RLHF" are usually selling ordinary post-training plus a data pipeline. The method is well-documented and reproducible; the value is in execution and data quality, not secret sauce. Also note: as of 2024–2026 most teams use **DPO (Direct Preference Optimization)**, a simpler, cheaper, and more stable method that skips the reinforcement-learning machinery entirely while using the same preference data and getting comparable or better results *(sourced, Rafailov et al. 2023/2024)*. So when someone says "RLHF," in practice they often mean "preference tuning," which is now meaningfully easier than the original 2022 recipe.

---

**2. Skill set required**

A strong ML / post-training team, not a typical web team. Specifically:
- ML engineers comfortable with large-scale GPU training and fine-tuning *(inference)*.
- People who understand reinforcement learning *or* the newer preference-optimization methods (DPO and relatives), plus the failure modes (reward hacking, distribution collapse, sycophancy) *(inference)*.
- A **data operations** function: recruiting, training, and quality-controlling human labelers, or building the AI-feedback pipeline for RLAIF. This is often the harder and more underrated half *(inference)*.
The original InstructGPT effort combined OpenAI researchers with ~40 trained contract labelers doing the ranking *(sourced, InstructGPT 2022)*.

---

**3. Difficulty: 4 out of 5**

Not a weekend project, not an eight-figure multi-year moonshot either. Why a 4:
- A small team can run *DPO on an open model with a public preference dataset* in days — that part has become a 2–3 *(inference)*.
- Doing it *well at production quality* — clean preference data, a reward model that doesn't get gamed, avoiding sycophancy and over-refusal, and evaluating whether you actually improved — is genuinely hard and where most attempts fall down *(inference)*.
- The classic PPO-based RLHF pipeline is notoriously *unstable and finicky to tune*, which is precisely why DPO was adopted so fast *(sourced, ICLR 2024 / DPO literature)*.
The frontier version (multi-stage, safety-critical, at scale) pushes toward a 5; the "fine-tune our chatbot's tone" version sits around a 3.

---

**4. Who can actually do it**

Tiered:
- **The basic version** (DPO on an open model with off-the-shelf data): any *strong ML team* — thousands of organizations worldwide *(inference)*.
- **Production-grade RLHF/RLAIF with your own data pipeline**: a smaller set — strong AI startups and well-resourced enterprises, on the order of hundreds to low thousands of teams *(inference, contested — depends on quality bar)*.
- **Frontier-scale, safety-critical alignment of a flagship model**: *fewer than a few hundred people in the world*, concentrated at a handful of labs (OpenAI, Anthropic, Google DeepMind, Meta, a few others) *(inference)*.
The gap between tiers is data, evaluation rigor, and operational maturity — not access to the algorithm.

---

**5. Cost — orders of magnitude**

This is *cheap relative to pretraining*. Pretraining a frontier model is tens to hundreds of millions of dollars; the preference-tuning step is a small fraction of that *(inference)*.
- **Compute:** Hundreds to low-thousands of dollars for a small DPO run on an open model; **tens of thousands to low-millions** for serious production runs with iteration *(inference; order-of-magnitude estimate, not a quoted figure)*.
- **Human data (the real cost driver for classic RLHF):** InstructGPT used ~13,000 demonstrations and ~33,000 comparison prompts, labeled by ~40 contractors *(sourced, InstructGPT 2022)*. Quality human preference labeling commonly runs from a few dollars to tens of dollars per prompt depending on complexity and number of annotators *(sourced, illustrative figures in Toloka/HRLAIF 2024; exact dollar totals: unknown — not found)*. At scale this lands in the **tens of thousands to low-millions of dollars**.
- **RLAIF's whole selling point** is collapsing that human-data line item by using an AI grader, trading labeling spend for compute and risking the AI grader's blind spots *(sourced, Anthropic Constitutional AI 2022)*.
- **Talent:** The dominant cost at the frontier — a handful of specialists who command very high compensation *(inference)*.

So: a competent **modest preference-tuning effort is five-to-six figures**; a frontier alignment program is **seven-to-eight figures**, mostly talent and iteration rather than any single training run.

---

**6. Data requirement & scale — and why it's the moat**

- **What:** *Preference data* — pairs (or rankings) of model answers with a label saying which is better, plus a set of demonstration answers to start from.
- **How much:** Order of **tens of thousands of ranked prompts** got InstructGPT working *(sourced, InstructGPT 2022)*; serious efforts use far more and refresh it continuously *(inference)*.
- **How sourced:** Trained human labelers (expensive, slow, but high-signal), an AI grader for RLAIF (cheap, fast, with correlated blind spots), or — increasingly — real production usage where actual users implicitly reveal preferences *(inference)*.
- **Why it's a moat:** The algorithm is public; *your* data is not. Preference data that reflects your specific users, domain, safety bar, and brand voice is hard to copy and compounds over time. Companies with millions of real users get a continuous, proprietary preference signal that no competitor can buy off the shelf *(inference; this is the strongest durable advantage here)*. Conversely, a startup with no users and no labeling budget gets only the generic open datasets everyone else has — which is why this step *democratizes basic capability but concentrates frontier quality*.


### DPO (Direct Preference Optimization)

**1. What it is + its impact**

After a large language model is pre-trained on the internet, it's a clever-but-unruly autocomplete engine. It then has to be "aligned" — taught to give answers people actually prefer (helpful, polite, safe). The original way to do this, called RLHF (Reinforcement Learning from Human Feedback), is a two-machine process: first you train a separate "judge" model (a *reward model*) to score answers, then you use a finicky reinforcement-learning loop to push the main model toward higher scores. It works, but it's expensive, unstable, and hard to get right.

DPO is a 2023 shortcut that gets to roughly the same destination with one machine instead of two. The paper's title says it best: "Your Language Model Is Secretly a Reward Model" — the authors showed mathematically that you can skip the separate judge entirely and tune the model directly from examples of "answer A was preferred over answer B." (sourced: https://openreview.net/forum?id=HPuSIXJaa9, NeurIPS 2023)

*Analogy:* RLHF is like training a wine critic, then having that critic taste thousands of your bottles and shout feedback while you adjust the recipe — two stages, and the critic can be wrong in ways that mislead you. DPO is like handing the winemaker a stack of paired tastings ("people liked this one better than that one") and letting them adjust the recipe directly. *Where the analogy breaks:* it implies DPO is strictly better. It isn't. The separate critic in RLHF can keep giving fresh feedback on brand-new bottles ("on-policy"), while plain DPO mostly learns from a fixed, pre-collected stack. For the hardest alignment problems, that fixed stack is a real limitation (contested, see Q3).

**What choosing DPO changes for the business:** lower cost and far less engineering risk to align a model, so smaller teams can do post-training that used to require a specialized RLHF team. The flip side: because it's now a near-commodity technique, DPO itself is *not* a moat. The moat moved to the **preference data** you feed it (Q6).

**2. Skill set required**

A competent ML engineer or applied researcher comfortable with PyTorch and modern fine-tuning libraries. DPO is a built-in, well-documented function in standard open-source toolkits (e.g., Hugging Face's TRL library), so you need someone who can run GPU training jobs, manage datasets, and evaluate model quality — not someone who can invent new RL algorithms. This is a markedly lower bar than classic RLHF, which demanded scarce reinforcement-learning specialists. (inference, based on DPO being a standard library method)

**3. Difficulty: 2/5 — and why**

Running DPO on an existing open model with an existing preference dataset is close to a weekend project for a skilled ML engineer; it's a standard recipe with reference code. (inference) It's a 2 rather than a 1 because the hard parts are real but bounded: getting good preference data, choosing the starting model, tuning a couple of sensitive knobs, and evaluating whether the result is actually better (alignment quality is notoriously hard to measure). It is emphatically *not* an eight-figure multi-year effort — that label belongs to pre-training the base model, which is a separate, vastly more expensive step. DPO is one stage of *post-training*, which sits on top of a model someone already built.

**4. Who in the world can actually do it**

Any strong ML team — thousands of companies and most well-funded AI startups, not a rarefied few hundred people. (inference) Adoption is broad: open frontier-class recipes like Allen AI's TÜLU 3 (Nov 2024) use DPO as a core post-training stage on top of Llama 3.1, and earlier open models like Zephyr popularized it. (sourced: https://arxiv.org/abs/2411.15124, 2024-11) The genuinely scarce skill is producing high-quality preference data at scale and knowing what "good" looks like — not running the DPO step itself.

**5. Cost — orders of magnitude**

Think **tens of thousands of dollars, not millions**, for the DPO training step on a mid-sized open model — i.e., a handful of GPUs for hours-to-days, plus the cost of assembling preference data. Vendor marketing claims DPO is "40% faster and 60% cheaper than RLHF," with one blog citing roughly $25k for DPO vs. $100k+ for RLHF per model. Treat those exact figures with skepticism — they come from a commercial blog, not a controlled study, and real cost depends heavily on model size and data volume. (contested: https://www.labellerr.com/blog/dpo-vs-ppo-for-llm-all/) The *directionally* solid and well-established claim is simply that DPO removes the separate reward-model training and the unstable RL loop, which cuts both compute and, more importantly, engineering time and risk. (sourced: https://openreview.net/forum?id=HPuSIXJaa9, 2023) The dominant cost in practice is usually **talent and data**, not GPUs.

**6. Data requirement & scale — and why it's the real moat**

DPO runs on **preference pairs**: for a given prompt, two candidate answers plus a label saying which one a human (or another AI) preferred. Open recipes have produced strong results with datasets on the order of tens of thousands to low hundreds of thousands of such pairs (e.g., the widely reused UltraFeedback dataset; TÜLU 3 leaned heavily on *synthetic* and on-policy preference data). (sourced: https://www.interconnects.ai/p/tulu-3, 2024; https://arxiv.org/abs/2411.15124, 2024-11) Pairs are sourced three ways: paid human raters (expensive, high quality), AI-generated preferences ("AI feedback," cheap and scalable), or real user interactions (your product's own data).

**Why it's a moat:** the DPO algorithm is free and public, so it confers no advantage by itself. What differentiates one company's aligned model from another's is the quality, domain-specificity, and freshness of its preference data — especially proprietary data from real users that competitors can't buy. The defensibility lives in the dataset, not the technique.

**Hype check:** DPO is a genuinely important, elegant simplification that lowered the barrier to model alignment — that part is not hype. But marketing that frames DPO as a clean "better than RLHF" upgrade overstates it. The research is actively contested: multiple 2025 studies find DPO can *underperform* RLHF/PPO on the hardest cases (and other studies find the reverse under weaker reward models). The honest summary is "simpler, cheaper, and good enough for most uses — not universally superior." (contested: https://arxiv.org/html/2505.19770v1, 2025; https://www.labellerr.com/blog/dpo-vs-ppo-for-llm-all/) Notably, as of mid-2026 several leading closed-model labs are reported to still use RLHF/PPO for final-stage alignment rather than DPO — though exact internal recipes at frontier labs are unknown — not found / proprietary. (contested: https://www.labellerr.com/blog/dpo-vs-ppo-for-llm-all/)


### Mixture-of-Experts + dynamic model routing

A quick but important warning before the six answers: **"Mixture-of-Experts" (MoE) and "dynamic model routing" are two different things that marketing decks love to blur together.** One is a deep architectural choice baked inside a single model; the other is a cheap plumbing layer that sits in front of several models. They share the word "routing" and almost nothing else in cost, difficulty, or who can do them. I'll answer for both and flag which is which throughout.

**MoE (inside one model):** Instead of one giant brain where every neuron fires on every word, the model is built as many smaller sub-networks ("experts"), and a tiny traffic-cop ("the router/gate") sends each word to just a few of them. *Analogy:* a hospital where the front desk routes you to the cardiologist or the dermatologist instead of making all 200 doctors examine every patient. **Where the analogy breaks:** the "experts" are not human-interpretable specialists — nobody can point to "the legal expert"; they're statistical clusters that emerge during training, and a single sentence gets split across many experts word-by-word. The label "expert" is a metaphor, not a job title.

**Dynamic model routing (in front of many models):** a small, fast classifier looks at each incoming user request and decides "this is easy, send it to the cheap small model" vs. "this is hard, send it to the expensive frontier model." *Analogy:* a call center where a receptionist handles routine questions and only escalates the genuinely hard calls to the senior specialist. **Where it breaks:** the receptionist has to judge difficulty *before* hearing the full answer, so it sometimes sends a hard question to the cheap model and gets a worse answer, or wastes money escalating an easy one.

**1. What it is + its impact.**
MoE lets you build a model with the *knowledge capacity* of a huge model but the *running cost* of a small one. DeepSeek-V3 has 671 billion total parameters but only activates ~37 billion per word [sourced]. Mixtral-8x7B has 46.7B total / 13B active and matched a 70B dense model at ~6x the speed [sourced]. **Product/cost impact:** dramatically cheaper inference per unit of capability — this is why MoE now powers a majority of new open-model releases [sourced]. **Moat impact:** MoE itself is *not* a moat — the technique is public and widely copied. The moat (if any) comes from the data, training skill, and capital to train one well. **Risk:** MoE models are harder to train stably and harder/more expensive to *serve* (you must keep all 671B parameters in memory even though you use 37B per token), so infra complexity goes up.
Dynamic routing's impact is purely **cost**, not capability: published systems cut spend 35-85% while keeping ~95% of quality, because most real-world queries are easy [sourced]. It is a margin lever, not a product or moat.

**2. Skill set required.**
- *MoE:* core ML research and large-scale distributed-systems engineers — people who understand transformer internals, gradient stability, load-balancing losses, and multi-thousand-GPU training. This is frontier-lab / strong-research-team territory.
- *Dynamic routing:* a competent backend/ML-engineering team. You're training or buying a small classifier and writing routing logic. No frontier research needed; many off-the-shelf tools exist (RouteLLM, OpenRouter, LLM gateways).

**3. Difficulty 1-5 and why.** I'm giving the *combined* technique a **4**, but the two halves are far apart:
- *MoE from scratch:* **5** — training a competitive MoE foundation model is an eight-figure, multi-year, deep-expertise effort. Stability and load-balancing are genuinely hard research problems [inference, based on training-cost and team-size norms].
- *Dynamic routing:* **2** — a small team can stand up a usable router in weeks using existing libraries; squeezing out the last bit of quality is the only hard part.
The "4" reflects that the impressive, defensible part is the MoE model; the routing layer is nearly a commodity.

**4. Who can actually do it.**
- *Train a frontier MoE model:* fewer than a few hundred people on Earth, concentrated in maybe a dozen labs (OpenAI, Google, Anthropic, Meta, Mistral, DeepSeek, Qwen/Alibaba, xAI, and a handful of others) [inference]. *Using* an existing open MoE model (DeepSeek, Mixtral, Llama 4) is, by contrast, available to any competent ML team — you download the weights.
- *Build dynamic routing:* almost any strong product/ML team, and increasingly any web team via hosted gateways [inference].

**5. Cost (orders of magnitude).**
- *MoE foundation-model training:* tens of millions to low hundreds of millions of dollars in compute per serious run, plus scarce eight-figure-salary talent [inference; consistent with public frontier-training cost ranges, no single disclosed figure for these specific models]. Serving requires enough GPU memory to hold all experts — a real, ongoing infra cost.
- *Dynamic routing:* $10K-$100K range to build, or near-zero upfront with a hosted gateway; it *saves* money rather than costing it. The classifier is cheap to train and cheap to run [inference].
So the same phrase spans a ~1,000x cost range depending on which half someone means — a key question to ask any vendor pitching "MoE + routing."

**6. Data requirement & scale, and the moat.**
- *MoE:* same data as any frontier model — trillions of tokens of curated, cleaned, deduplicated text/code/multimodal data. MoE does *not* reduce the data requirement; it reduces compute-per-token. The moat is the data pipeline and curation, not the MoE wiring [inference].
- *Dynamic routing:* needs only a modest dataset of example queries labeled with "which model handled this well" — thousands to tens of thousands of examples, often generated cheaply using a strong model as a judge [sourced, RouteLLM]. This is a *weak* moat; it's easy to recreate.

**Hype calibration:** When a pitch says "we use Mixture-of-Experts and dynamic routing," press on which one is theirs. Building a competitive MoE foundation model is a genuine, rare, capital-intensive achievement. Adding a router in front of OpenAI/Anthropic/open models, or simply *using* someone else's open MoE model, is ordinary engineering that most teams can match in a quarter. The phrase is frequently used to make commodity plumbing sound like frontier research.


### Inference & serving at scale + latency engineering

**The one-line version:** Training builds the AI model once; *inference serving* is the machinery that runs it millions of times a day for real users, fast and cheaply. "Latency engineering" is the craft of shaving the wait — how long before the user sees the first word, and how fast words stream after that. It's the difference between owning a great recipe and running a restaurant kitchen that feeds 10,000 people an hour without the food going cold.

**1. What it is + its impact.** Once a model is trained, every single answer it gives costs money (GPU time) and takes time. Serving-at-scale is the stack of techniques that lets you pack many users' requests onto the same expensive GPU at once, reuse repeated work, and split the job across machines — so the same hardware serves far more customers per dollar. The headline tricks: *continuous batching* (slotting new requests onto a GPU mid-flight instead of waiting for a batch to finish), *PagedAttention / KV-cache management* (reusing the model's "short-term memory" efficiently), *prefill–decode disaggregation* (running the "read your question" phase and the "write the answer" phase on separate machine pools), *speculative decoding* (a small fast model drafts text the big model only checks), and *quantization* (running the model in lower numerical precision so it's cheaper). Reported gains are large and real: vLLM claims up to ~24x throughput vs. naive baselines [sourced]; production disaggregated systems report 5x+ throughput on long-context work [sourced]. **Why a CEO cares:** this is the single biggest lever on gross margin for any AI product. The cost to serve "GPT-4-level" quality fell from ~$20 per million tokens in late 2022 to ~$0.40 in early 2026, and API prices broadly dropped ~80% in the year to early 2026 [sourced] — much of that is serving efficiency, not just cheaper chips. It also directly shapes the product: low latency (fast first word, smooth streaming) is what makes a chat assistant feel alive vs. sluggish. **The risk/moat read:** the core software is open-source (vLLM, TensorRT-LLM, NVIDIA Dynamo), so this is rarely a durable moat by itself — but doing it *well at your scale* is a real, sustained cost and reliability advantage that mediocre competitors will bleed money trying to match.

**2. Skill set required.** Systems and performance engineers, not primarily ML researchers. Think distributed-systems engineers, GPU/CUDA kernel specialists, and ML-infrastructure/SRE people. The scarce skill is comfort across the whole stack: GPU memory and interconnect behavior, scheduling/queueing theory, networking (RDMA), and production reliability under bursty traffic. ML knowledge matters at the edges (e.g., verifying that quantization or speculative decoding didn't degrade answer quality), but the heart of it is hardcore software/hardware systems engineering. [inference]

**3. Difficulty: 4/5, and why.** It's a spectrum. *Standing up* a fast server — pull vLLM or TensorRT-LLM, point it at an open model, get strong latency on a few GPUs — is a weekend-to-a-few-weeks project for a competent engineer (call it a 2/5). That's why the floor has dropped so much. But *operating it at scale* — thousands of GPUs, predictable latency guarantees (SLOs) under unpredictable load, multi-machine disaggregation, custom kernels, squeezing the last 30-50% of cost out — is a genuinely hard, multi-team, never-finished discipline (a 4-5/5). It's not an eight-figure multi-year moonshot like training a frontier model, but it is a permanent, well-funded engineering org for the companies doing it best. [inference]

**4. Who can actually do it.** The *basic* version: any strong web/backend team can deploy an off-the-shelf serving engine and get decent results — thousands of teams do this today. The *frontier* version — sub-second latency at massive scale, disaggregated serving, custom GPU kernels, novel KV-cache systems — is done by a much smaller set: the big labs (OpenAI, Anthropic, Google, Meta, Mistral), specialist inference companies (Together AI, Fireworks, Groq, Baseten, inference.net), and a handful of hyperscalers and Chinese labs (ByteDance's Mooncake, DeepSeek) [sourced]. Realistically a few thousand engineers worldwide operate at that elite tier — narrower than "any web team," broader than the few hundred who can train frontier models. [inference]

**5. Cost — orders of magnitude.** Entry: ~$10^3-10^4 — rent one or two H100 GPUs at roughly $2.85-$3.50/hour [sourced] and serve an open model; near-zero software cost since the engines are free/open-source. Production for a real company: ~$10^5-10^6+/year — average corporate AI spend rose from ~$63K/month (2024) to ~$85.5K/month (2025) [sourced], and that's a *median*, not the heavy users. Hyperscale (a major AI product's serving fleet): ~$10^8-10^9+/year in GPUs and datacenter for the largest players [inference/speculation — exact figures not disclosed]. Talent: a strong serving engineer is a high-six-figure total-comp hire in the US; an elite team is single-digit to low-double-digit millions per year in payroll [inference]. The economic punchline: self-hosting beats paying per-token APIs only above roughly 10-50 million tokens/day, depending on model and hardware [sourced] — below that, renting an API is cheaper than building this capability.

**6. Data requirement & scale — and is it a moat?** This is the important nuance: serving itself **needs essentially no training data**. You're running an already-trained model. So unlike training, data is *not* the moat here. The "data" that matters operationally is your own **live traffic** — request patterns, prompt-length distributions, cache-hit behavior, peak-load shapes. That traffic is genuinely valuable: it lets you tune batching, caching, and capacity in ways a new entrant can't replicate until they too have millions of users — a real but secondary, scale-driven advantage, not a dataset you can buy or steal. [inference] The durable moats in this area are *scale and operational excellence* (cheaper per-token economics, better uptime) far more than any proprietary data.

**Hype check.** Marketing throws around "24x faster" and "10,000 tokens/second" — these numbers are real but are *best-case benchmarks* against weak baselines or on specific hardware/models [sourced; contested as representative]. Your actual gain depends heavily on your model, prompt lengths, and traffic. Treat any single eye-popping multiplier as a ceiling, not a promise. And be skeptical of anyone selling inference serving as a *proprietary moat* — the leading engines are open-source; the moat is in running them better and cheaper than rivals, which is an operational advantage, not a secret.


### Guardrails / two-pass safety classifiers

**1. What it is + its impact**

A "guardrail" is a second, smaller AI model that sits around your main AI like a bouncer at a club. It checks two things: what the user typed *before* it reaches your main model (the input pass), and what your main model is about to say *before* it reaches the user (the output pass). If either looks dangerous — instructions for weapons, child abuse, self-harm, leaking secrets — the bouncer blocks it and the main model never engages or never speaks. That's the "two-pass" part: you screen on the way in and on the way out.

Analogy: it's a metal detector plus an exit bag-check at an airport. The expensive, capable thing (the airplane / your main model) does its job, while a cheap, dedicated checkpoint catches the bad stuff at the doors. **Where the analogy breaks:** a metal detector reacts to fixed physics (metal). A safety classifier is itself a fuzzy AI making judgment calls in language, so it has a false-alarm rate (blocking harmless requests, "over-refusal") and a miss rate (letting bad stuff through). It's a probabilistic filter, not a deterministic gate.

What choosing this changes for the business:
- **Risk:** This is the single most common, cheapest way to reduce headline/legal/brand risk from your AI doing something awful. It is the standard, expected layer — its absence is a red flag to enterprise buyers and regulators.
- **Cost:** It adds a noticeable but modest tax to every interaction (roughly +24% compute in Anthropic's own published system; ~25% when using a small model to guard a larger one — *sourced, see below*). Off-the-shelf open guardrail models can make the marginal cost near-zero by comparison.
- **Product:** Tune it too tight and you frustrate real users with refusals; too loose and you ship harm. That dial is a product decision, not just an engineering one.
- **Moat:** Basic guardrails are **not a moat** — anyone can bolt them on. A guardrail *tuned to your specific domain and your specific abuse patterns* using data only you have is a modest, real moat. The technique is commodity; the calibration data is the differentiator.

**2. Skill set required**

For the common case (using an existing guardrail): a competent ML/applied-AI engineer or a strong backend engineer who can call an API and wire a model into a request pipeline. This is integration work, not research. For the hard case (training your own classifier from a written policy, like Anthropic's "constitutional classifiers"): ML engineers/researchers who can generate synthetic training data, fine-tune models, run red-team adversarial testing, and manage the false-positive/false-negative tradeoff.

**3. Difficulty: 2/5**

Bolting on an existing guardrail is close to a weekend-to-a-sprint project — Meta gives away Llama Guard models for free, and OpenAI/others offer moderation endpoints. The conceptual idea (screen in, screen out) is simple. What pushes it above a 1, and what's genuinely hard, is **calibration and adversarial robustness**: getting refusals low enough not to annoy users while keeping misses low against people *actively trying to trick the system* (jailbreaks). Building a custom, jailbreak-resistant classifier from scratch — the Anthropic-grade version — is a real multi-quarter research effort and would rate a 4. The 2/5 reflects the typical company, who adopts rather than invents.

**4. Who can actually do it**

Adopting an off-the-shelf guardrail: essentially **any competent product/ML team** — thousands of teams, a normal web/AI engineering group. Building a robust *custom* classifier that holds up against determined attackers: a **strong ML team**, realistically a few thousand people globally who do it well. Building frontier-grade, red-teamed safety classifier systems with published robustness: a much smaller set — the major AI labs and a handful of specialist safety vendors.

**5. Cost (orders of magnitude)**

- **Adopt off-the-shelf (most companies):** Talent is one or a few engineers for weeks → roughly $10k–$100k in effort. Model weights are free (Llama Guard) or pay-per-call (moderation APIs). No training runs needed. *(inference cost basis below.)*
- **Run-time/inference cost:** The recurring cost is the real number to watch. Published basis: Anthropic reported ~+23.7% compute overhead for its classifier system, and noted using a small model (Claude 3.5 Haiku) to guard a larger one (3.5 Sonnet) raises inference cost by ~25% (*sourced*). So budget a **~10–25% surcharge on every AI call** as a rule of thumb — that's inference, not a one-time build.
- **Build a custom robust classifier:** Mid-six to low-seven figures — a small specialized ML team for several months, plus synthetic-data generation, fine-tuning runs, and ongoing red-teaming. This is hundreds of thousands to low millions, **not** an eight-figure frontier-model effort. (inference)
- **Infra:** Modest. A 1B–8B guardrail model is small and cheap to serve next to your main model; the 1B version is light enough for on-device. (inference)

**6. Data requirement & scale, and why it's a moat**

You need labeled examples of "safe" vs "unsafe" prompts and responses across the harm categories you care about. Two ways to source it:
- **Synthetic generation (the modern default):** Write a policy ("constitution") of what's allowed/disallowed, then have an AI generate large volumes of synthetic harmful and benign examples, including translations and jailbreak-styled rewrites, and train on those (*sourced — this is exactly Anthropic's published method*). This dramatically lowers the data barrier — you don't need to hand-collect millions of toxic messages.
- **Real abuse data from your own product:** Logs of actual attempts users made against *your* system.

Scale: tens of thousands to millions of examples depending on ambition; the free Llama Guard models already ship pre-trained on a broad taxonomy, so many teams need **little or no data of their own** to start.

**Why it's (sometimes) a moat:** The generic capability is a commodity — free weights exist. The defensible asset is your **proprietary stream of real-world attack attempts and edge cases from your live product**, which lets you tune the guardrail to catch abuse that generic models miss. That data compounds over time and competitors can't buy it. So: the technique is not a moat, but the abuse-data flywheel around it can be a modest one (inference).

**Hype check:** Vendors marketing "AI safety guardrails" or "trust layers" as a proprietary breakthrough are usually overselling a well-understood, often-free technique. Calling it advanced is inflated. What is genuinely hard — and worth scrutinizing a vendor's actual numbers on — is the *robustness against determined jailbreaks* and the *over-refusal rate*. Those metrics, not the existence of a guardrail, are where real engineering quality shows.


### Crisis-detection classifiers (self-harm / suicide escalation)

**1. What it is + its impact.**
A crisis-detection classifier is a piece of software that reads a chunk of text (a chat message, a social-media post, a support-line transcript) and outputs a label: "this person may be in a self-harm or suicidal crisis" — often with a severity level (passing mention vs. active intent with a plan). Modern versions are built on top of pre-trained language models (the same family of tech as ChatGPT, but used as a *judge* rather than a *talker*) [inference, based on sourced fact that the leading research and production systems use transformer/BERT/DeBERTa/LLM backbones — arxiv.org/html/2410.08375v1, 2024-10; openai.com/index/strengthening-chatgpt-responses-in-sensitive-conversations, 2025].

Analogy: it's a smoke detector for language. It doesn't put out the fire (it doesn't counsel the person); it just decides "is this smoke serious enough to pull the alarm?" — where pulling the alarm means routing the user to a hotline (988 in the US), surfacing the conversation to a human moderator, or changing how a chatbot responds. **Where the analogy breaks:** a smoke detector reacts to a physical, unambiguous signal (particles in the air). Crisis is expressed in messy, sarcastic, metaphorical, multilingual human language ("I'm dying of boredom" vs. a genuine cry for help), so the detector is guessing at *intent*, and it is wrong a meaningful fraction of the time in both directions.

What choosing to build/deploy this changes for a business:
- **Product/risk:** It is fast becoming table-stakes safety infrastructure, not a differentiator. After 2025 lawsuits and regulatory pressure, OpenAI and Character.AI both tightened exactly these systems [sourced — axios.com/2025/10/29/openai-character-ai-chatbot-chatgpt-relationships-suicide, 2025-10-29]. If your product lets users talk freely (any chatbot, social app, companion app, support tool), *not* having one is now a liability exposure, not a cost saving.
- **The dominant risk is not "can we build it" — it's the error tradeoff.** Too sensitive and you flood human reviewers with false alarms and annoy users; too lax and you miss a real crisis with potentially fatal, headline-making, litigable consequences. Suicide risk models are notorious for huge false-positive rates — classically ~96% of "high-risk" flags do not result in suicide ("Pokorny's complaint") [sourced — ncbi.nlm.nih.gov/pmc/articles/PMC5288088, 2016].
- **Moat:** weak as a moat. The modeling is largely commoditized; what little edge exists comes from proprietary labeled data and clinical-expert review processes, not the algorithm (see Q6).
- **Cost:** low-to-moderate to stand up a decent one; the real ongoing cost is human review, clinical oversight, and the legal/operational machinery around what happens *after* a flag.

**2. Skill set required.**
A competent applied-ML / NLP engineer who can fine-tune or prompt a pre-trained language model and, crucially, evaluate it honestly (precision/recall tradeoffs, threshold-setting). The hard part is not the code — it's pairing that engineer with **clinical/mental-health expertise** to define the labels and review edge cases. OpenAI explicitly worked with clinicians "who have real-world clinical experience" to build their taxonomy [sourced — openai.com/index/helping-people-when-they-need-it-most, 2025]. So: ML engineer + clinical advisor + a trust-and-safety operations function. You do not need frontier-model research talent.

**3. Difficulty: 3 / 5.**
A *crude* keyword/basic-model version is a weekend project (open datasets exist; a fine-tuned BERT gets you a working demo). A *responsible production system* is a genuine multi-quarter effort because the difficulty is in safety, calibration, multilingual coverage, low-but-non-zero miss rate, clinical validation, and the human-in-the-loop pipeline — not in the math. It is not an eight-figure moonshot, but "we trained a classifier, ship it" is dangerously naive given the stakes. The 3 reflects "easy to do badly, hard to do well enough to bet lives and lawsuits on."

**4. Who can actually do it.**
A **strong ML/NLP team** can build a solid version — that's thousands of teams worldwide, not a rarefied few hundred. Off-the-shelf models, public datasets, and cloud APIs make a baseline broadly accessible. What is genuinely scarce is the *combination* of (a) competent ML, (b) embedded clinical expertise, and (c) the operational/legal infrastructure to act on flags safely at scale — that narrows the field of people who can do it *responsibly* to large platforms and serious health-tech outfits, but the core classifier is not exotic.

**5. Cost (orders of magnitude).**
- **Compute / training runs:** low — roughly **$100s to low $10,000s** to fine-tune existing open models on modest GPU rental; these are small models by frontier standards [inference, from sourced fact that published systems fine-tune existing BERT/DeBERTa-class models on datasets of thousands of examples — arxiv.org/html/2507.11559v1, 2025]. If you instead call a commercial LLM API as the judge, training cost is ~zero and you pay per-call inference.
- **Inference/infra:** scales with traffic; ordinary text-classification serving costs, not unusual.
- **Talent + clinical + ops:** this dominates. A serious effort is **low-to-mid seven figures per year** once you include ML engineers, clinical advisors, 24/7 human review, and legal — but that's an operations cost, not a compute cost. unknown — exact figures not disclosed by operators; this is an inference from typical trust-and-safety team sizing.
- Net: this is **not** a capital-intensive model-training problem. The money goes to people and process.

**6. Data requirement & scale.**
- **What:** examples of text labeled by humans for crisis presence and severity — ideally domain-matched (your own chat logs look nothing like Reddit posts).
- **How much:** surprisingly little to get started. Published, useful systems use thousands to low-tens-of-thousands of labeled examples — e.g., a 15,000-user annotated dataset (RSD-15K) [sourced — arxiv.org/html/2507.11559v1, 2025]; IEEE BigData 2024 used 2,000 Reddit posts with only 500 annotated [sourced — same search result set, arxiv 2024]. Performance tracks "number of training samples" more than task difficulty [sourced — pmc.ncbi.nlm.nih.gov/articles/PMC11093288, 2024]. Even strong models top out modestly: ~76% accuracy / 0.70 macro-F1 on real fine-grained tasks [sourced — arxiv.org/html/2507.11559v1, 2025], with fine-grained severity F1 around 50% [sourced — arxiv.org/pdf/2404.12659, 2024]. Translation for a CEO: these systems are useful triage tools, **not** reliable oracles.
- **How sourced / why it's a moat:** public datasets exist, so the *baseline* data is not a moat. The real, defensible asset is **proprietary, in-domain, clinically-reviewed labeled data from your own users**, plus the human-review feedback loop that keeps improving it. That's expensive and sensitive to collect (privacy, consent, vulnerable populations) and can't be downloaded — which is the closest thing here to a durable advantage.

**Hype check.** If a vendor markets "AI that detects suicide risk" as a solved, high-accuracy capability, be skeptical. The honest state of the art is a moderately accurate triage signal (~70-76% on hard tasks, weak on fine-grained severity) with a structural false-positive problem, useful only inside a human-and-clinician-supervised workflow. It is valuable and increasingly mandatory safety plumbing — but it is a modest, largely commoditized technique dressed in very high stakes, not a breakthrough or a moat. Notably, even "false positive" flags carry real signal — flagged-but-no-event individuals show 3-7x elevated later risk — so the tool earns its keep as a *screening* aid, not a verdict [sourced — pmc.ncbi.nlm.nih.gov/articles/PMC10540433, 2023].


### LLM-as-judge evaluation harnesses

**1. What it is + its impact.** When you ship a product built on a language model (a chatbot, a summarizer, a support agent), you face a hard question: *is the output any good?* There's no "correct answer" key the way there is for a math test — quality is fuzzy ("was this summary faithful?", "was this reply helpful and on-brand?"). The old answer was to pay humans to read outputs and score them, which is slow and expensive. "LLM-as-judge" means using a *second* AI model as the grader: you give it the question, the answer, and a rubric ("score 1-5 on accuracy"), and it returns a score and a rationale. An "evaluation harness" is the surrounding machinery — the test cases, the rubrics, the plumbing that runs hundreds of these judgments automatically and tracks the results over time, usually wired into the release process so a quality drop blocks a deploy.

The analogy: it's like having a junior reviewer grade essays against a rubric instead of hiring a room of expert graders. Fast, cheap, available 24/7, and consistent in the boring sense. **Where the analogy breaks:** this junior reviewer has predictable blind spots a human wouldn't have. It tends to favor the *longer* answer even when it's worse, favor whichever answer it sees *first* in a side-by-side, and — notably — rate text generated by *itself or its own model family* more highly. These aren't occasional slips; they're systematic, and they don't go away just because the model is smart.

Impact on a business: it's the difference between flying blind and having a dashboard. It lets a small team measure quality continuously, catch regressions before customers do, and iterate faster (teams report meaningful accuracy gains within weeks of adopting eval tooling). The strategic catch is that **the judge is not a moat and is not ground truth** — it's a cheap proxy that must itself be validated against humans, or you risk optimizing your product to please a biased grader rather than your actual users. The moat, if any, is in your *test data and rubrics* (see #6), not the judging technique.

**2. Skill set required.** A competent software/ML engineer or applied data scientist. The core work is prompt-writing (designing the rubric the judge uses), data wrangling (assembling test cases), and ordinary software engineering (wiring it into CI/CD). You do *not* need to train models or have deep ML-research credentials for a standard setup. Doing it *rigorously* — measuring whether your judge actually agrees with humans, correcting for its biases — pulls in light statistics/measurement skill (agreement metrics, calibration), which is where it shades from "engineer" toward "applied researcher."

**3. Difficulty: 2/5.** A basic working harness is close to a weekend project — call a model API with a rubric prompt, run it over a spreadsheet of examples, score the outputs. Off-the-shelf platforms (Braintrust, LangSmith, Langfuse, OpenAI/Anthropic's own eval tooling) make the wiring nearly turnkey, with setup times reported under an hour. What raises it from a 1 to a 2 is that the *naive* version is quietly unreliable, and making it *trustworthy* is genuinely hard: you have to validate the judge against humans, detect and correct for position/verbosity/self-preference bias, and keep the rubric stable as your product changes. Recent research (2026) building dedicated "judge reliability harnesses" found *no* judge was uniformly reliable, with grades flipping on changes as trivial as reformatting or rephrasing the input. So: easy to stand up, hard to trust.

**4. Who can do it.** Essentially any competent web/product engineering team. This is a broadly accessible technique — there's no scarce talent or special hardware gate. The harder *rigorous* version (statistically validated, bias-corrected judges) is within reach of any strong ML or applied-research team, which is still tens of thousands of people, not a rarefied few hundred.

**5. Cost — orders of magnitude.** Low. The dominant cost is model API calls for the judging itself: each judgment is one model call, often cents or fractions of a cent. A test suite of hundreds-to-thousands of cases run on each release might cost single-digit to low-hundreds of dollars per run depending on judge-model choice and volume. No training runs, no GPU clusters, no specialized infrastructure — it rides on the same API access you already have. Talent cost is one engineer's time (days to weeks for a solid first version). Eval *platforms* add a SaaS subscription (team-tier software pricing) but aren't required. Total order of magnitude to get started: **hundreds to low thousands of dollars**, dominated by engineer time, not compute. Ongoing cost scales linearly with how often and how broadly you run the evals.

**6. Data requirement & scale — and why it's the real moat.** The judging *technique* needs almost no data to start. What you need is a set of **test cases** — representative inputs plus, ideally, reference answers or rubrics describing what "good" looks like. A useful suite can start at dozens to a few hundred curated examples; serious production suites run into the thousands. Crucially, to know your judge is trustworthy you also need a smaller set of **human-labeled examples** (typically a few hundred) to check that the AI judge agrees with human reviewers — well-calibrated judges reach ~80%+ agreement with humans, roughly the level humans agree with each other, but you only know that by measuring it. **This is where the moat lives:** the curated, domain-specific test cases and rubrics that capture what quality means *for your product and your users* are proprietary, expensive to build, and hard for a competitor to copy — unlike the judging method itself, which is public and commoditized. A competitor can copy your prompt; they can't easily copy a thousand hand-labeled examples of your edge cases.

**Hype check.** "LLM-as-judge" is sometimes marketed as if it replaces human evaluation outright. It does not. It's a genuinely useful, modest, and now-commoditized technique that *scales* evaluation cheaply — but it inherits real, documented biases (verbosity, position, self-preference) and must be anchored to human judgment to stay honest. Treat it as a fast proxy that needs auditing, not an oracle.


### Clinical eval & benchmark construction (VERA-MH, CTRS scoring)

**1. What it is + its impact.**
This is the practice of building a *grading system* for AI that gives mental-health advice — not building the AI itself. Think of it like a board exam or a food-safety inspection for a chatbot. You write a set of realistic patient situations, define what a "good" and a "dangerous" response looks like according to real clinical standards, and then score the AI against that rubric. VERA-MH (released by Spring Health and a clinical council in late 2025) does this for suicide-risk situations: it runs simulated at-risk "patients" at the chatbot and checks whether it spots the crisis, asks the right follow-up, and hands off to a human [sourced]. CTRS (the Cognitive Therapy Rating Scale) is an older, human-designed 11-item checklist for grading whether a *therapist* is doing competent CBT; researchers have started repurposing it to grade AI therapists [sourced].

The analogy: it's the *driving test*, not the *car*. **Where it breaks:** a driving test is settled and standardized; these clinical evals are brand-new, contested, and partly graded by *another AI* acting as the examiner — so it's more like a new driving test where the examiner is itself a trainee whose judgment you also have to trust.

Why it matters to a CEO/investor: (a) **Risk/liability** — if you deploy a mental-health AI without a credible safety eval, you carry catastrophic regulatory and reputational exposure (someone dies, you can't show you tested for it). (b) **Moat** — a respected, clinician-validated benchmark can become the *de facto standard* others must pass, which is strategically valuable; but VERA-MH is deliberately *open-source*, so the benchmark itself is a moat for the field, not for any one company. (c) **Cost** — it's cheap relative to building models; it's mostly expert time, not GPUs.

**2. Skill set required.**
This is more *clinical + research methodology* than hardcore ML engineering. You need: practicing clinicians and suicide-prevention specialists (to define what "correct" means), a psychometrician/research methodologist (to measure inter-rater reliability and validity properly), and a competent ML/data engineer to wire up the simulation harness and the "LLM-as-judge" pipeline. The hard, scarce part is the *clinical judgment and validation rigor*, not the code [inference].

**3. Difficulty: 3/5 and why.**
The *engineering* is a low 2 — running 100 simulated personas through a chatbot and scoring with an LLM judge is a few weeks of work for a competent team. What pushes it to a 3 is the *clinical validation*: you must recruit real clinicians, have them independently rate transcripts, and prove they agree with each other and with the AI judge (VERA-MH reports chance-corrected inter-rater reliability around 0.77 among humans and 0.81/0.77 between the AI judge and human consensus) [sourced]. Doing that credibly, in a life-safety domain, with defensible methodology, is a multi-month expert effort — not a weekend project, but also not an eight-figure one.

**4. Who can actually do it.**
Building a *toy* version: any strong ML team. Building a *credible, publishable, clinician-validated* one like VERA-MH: a much smaller set — organizations that can convene practicing clinicians, suicide-prevention experts, ethicists, and ML researchers together. That's the low thousands of organizations worldwide (academic medical centers, a handful of digital-health companies, some AI labs), and the truly authoritative efforts are fewer still [inference]. The bottleneck is access to qualified clinicians and methodological credibility, not compute.

**5. Cost — orders of magnitude.**
Dominated by *talent and clinician time*, not compute. Running the eval itself is cheap: ~2,000 conversation data points per run (100 personas x 2 conversations x up to ~30 turns), each scored by an LLM judge — that's roughly hundreds to low-thousands of dollars in API calls per full evaluation pass [inference, based on the disclosed 100-persona/2,000-data-point design]. The real cost is the *construction*: a multi-disciplinary council, clinician raters doing validation studies, and methodologists — a six-figure to low-seven-figure program over several months for something authoritative [inference]. No large GPU training runs are involved; this is evaluation, not model training. Exact budgets: unknown — not found.

**6. Data requirement & scale — and is it a moat.**
The "data" here is unusual: it's not a giant training corpus, it's a *carefully designed set of synthetic patient personas plus an expert-written rubric*. VERA-MH uses 100 personas stratified by suicide risk (30% high / 30% medium / 30% low / 10% no-risk controls), with conversations generated dynamically rather than scripted [sourced]. The scarce, defensible asset is the **clinically validated rubric and the human rating data proving the AI judge agrees with experts** — that expert-labeled validation data is genuinely hard to reproduce and is the real moat. But VERA-MH gave it away open-source, so it's a *public good*, not a private moat. CTRS, by contrast, is a decades-old published scale anyone can use, so it confers no moat at all [inference].

**Hype check.** The technique is real and valuable, but two things are routinely overstated. First, "LLM-as-judge" agreeing with clinicians at ~0.77–0.81 reliability is *good* but not the same as proven real-world safety — passing a benchmark is not the same as being safe with a real suicidal person [inference]. Second, headline claims like "AI outperforms therapists on CBT" (a March 2026 Nature Medicine-linked study, where reportedly 74% of AI sessions scored above the top 10% of human sessions on a *modified* CTRS) deserve heavy skepticism: CTRS was validated for human raters, here it was applied by an AI to AI transcripts, which can flatter the machine [contested]. The construction of these benchmarks is a modest, sensible, important engineering-and-clinical exercise — not a breakthrough, and not a defensible technical moat for any single vendor.


### RAG, memory & personalization

**1. What it is + its impact**

These are three ways to give an AI model access to information it wasn't born knowing, without retraining the model itself.

- **RAG (Retrieval-Augmented Generation):** Before the AI answers, the system fetches relevant snippets from your documents (policies, manuals, support tickets, product catalog) and pastes them into the prompt so the model "reads them" and answers from them. Analogy: an open-book exam. The student (the model) is smart but doesn't know your company's facts; you hand it the right page right before it answers.
- **Memory:** The system saves facts about a user or conversation across sessions ("Kendra prefers Adidas," "this account is on the enterprise plan") and re-injects them next time. Analogy: a good waiter who remembers your usual order.
- **Personalization:** Using that memory plus user data to tailor responses to each person.

**Where the analogy breaks:** an open-book exam assumes the right page is found. RAG's quality is entirely capped by *retrieval* — if the search step pulls the wrong snippet, the model confidently answers from wrong material. The model isn't reasoning over your whole knowledge base; it only sees the handful of chunks retrieval surfaced. Garbage retrieval, garbage answer.

**Business impact of choosing this:**
- **Product:** Lets a general model speak accurately about *your* private/current data and feel personal. This is how most "AI that knows our docs" products are actually built.
- **Cost:** Far cheaper and faster than fine-tuning or training a model. You update knowledge by updating a database, not by retraining. (Sourced: industry consensus that RAG is more cost-efficient than frequent fine-tuning when knowledge changes often.)
- **Moat:** Weak from the technique itself (everyone can build RAG), strong from the *data and the cleanup work* behind it. The moat is your proprietary corpus and how well it's structured, not the RAG plumbing.
- **Risk:** Hallucination is reduced but not eliminated; bad retrieval produces confident wrong answers. Memory adds two specific, still-unsolved risks: **staleness** (a saved fact becomes wrong when the user changes jobs/preferences) and **identity resolution** (knowing two sessions are the same person across devices/logins). (Sourced: mem0.ai State of AI Agent Memory 2026.) Also a privacy/compliance surface — you're storing personal data.

**Hype calibration:** "Memory" and "the agent learns about you" are often marketed as the AI becoming intelligent or self-improving. It is not learning in the model-weights sense — it is saving text strings and re-pasting them later. Useful and real, but mundane under the hood. Vendor benchmarks in 2026 show no system handles all of remember/update/forget well; "selective forgetting" in particular is largely unsolved (sourced, mem0.ai 2026). Treat "infinite memory" / "truly personalized" claims as aspirational.

**2. Skill set required**

A competent application/backend or full-stack engineer, not an ML researcher. Core skills: API integration, databases, data pipelines (chunking and cleaning documents), and prompt engineering. A *vector database* (a search index that finds text by meaning rather than keywords) is involved but is a managed product you call, not something you build. Doing it *well* at scale — good retrieval quality, hybrid search, evaluation — benefits from a strong data/ML-leaning engineer, but no frontier-model expertise is needed.

**3. Difficulty: 2 / 5**

A basic working RAG demo is genuinely a weekend project — tutorials, open-source frameworks, and managed vector databases make the happy path easy. It scores a 2 rather than a 1 because the gap between "impressive demo" and "reliable in production" is large and underestimated: retrieval quality, document chunking, keeping the index fresh, evaluation, handling messy real-world documents, and memory staleness/identity problems are real engineering work. It is *not* an eight-figure multi-year effort — that's reserved for training the underlying models, which this technique deliberately avoids.

**4. Who in the world can do it**

Essentially **any competent web/app development team.** This is mainstream, commoditized technology in 2026 with a deep tooling ecosystem (the search returned 21 memory frameworks and 20+ vector stores). Doing it at a *high* quality bar — excellent retrieval, low hallucination, robust memory — narrows to strong data/ML engineering teams, but that's a quality gradient, not a barrier of scarcity. This is the opposite end of the spectrum from "fewer than a few hundred people can do it."

**5. Cost (orders of magnitude)**

Operating cost is low and usage-based, dominated by per-query model and database costs, not training:
- **Per query:** ~$0.001 for naive RAG; ~$0.005 with hybrid search + reranking; $0.02–$0.10 for complex "agentic" RAG. (Sourced: stratagem-systems / techment 2026 estimates — treat as rough planning numbers, not guarantees.)
- **At 100K queries/month:** roughly $100–$10,000/month depending on complexity. (Sourced, same.)
- **Vector database:** small production app (a few million records) ~$50–$200/month on a managed service like Pinecone; storage ~$0.33/GB/month, reads ~$16–24 per million. (Sourced: pinecone.io pricing / leanopstech 2026.) Above ~50M vectors and high query volume, self-hosting can be 40–70% cheaper (sourced, same) but adds engineering overhead.
- **Build/implementation:** discrete tasks like hybrid search or metadata filtering run low-single-thousands of dollars of engineering each (sourced, stratagem-systems 2026) — i.e., weeks of one engineer, not a research program.
- **Talent:** ordinary engineering salaries (low-to-mid six figures per engineer/year), not the scarce seven-figure frontier-ML market.
- **Training runs:** none. This technique's headline advantage is avoiding model training entirely.

Order of magnitude: a startup can stand up a real product for **thousands to low tens of thousands of dollars per month**, scaling with usage.

**6. Data requirement & scale**

- **What:** Your own text — documents, knowledge base, transcripts, product data, plus per-user interaction history for memory.
- **How much:** Unlike model training, RAG works with *small* data. A few hundred good documents already produces value; there's no millions-of-examples threshold. Vector counts scale with corpus size (a few million is common and cheap; tens of millions is where self-hosting economics kick in).
- **How sourced:** From your existing business systems — no labeling or annotation effort like training requires. The hard part is *cleaning and structuring*, not acquiring.
- **Why it's a moat:** The technique is commodity; the **proprietary corpus is the moat.** A competitor can copy your RAG architecture in a week but cannot copy ten years of your support tickets, contracts, or accumulated user-preference memory. The defensibility lives in the data and its quality, and (for memory) in accumulated per-user history that compounds with engagement — *if* you solve staleness and identity, which remain open problems as of 2026 (sourced, mem0.ai).


### Clinical & outcomes-indexed data pipelines (the real moat)

**The one-sentence version:** This is the unglamorous plumbing that takes messy real-world medical records and reliably connects "what was done to the patient" to "what actually happened to the patient afterward" — and keeps doing it, accurately, at scale, in a way competitors can't easily copy.

**1. What it is + its impact**

In medicine, the valuable thing is almost never the AI model. It's the data the model learns from — specifically, data where each clinical event (a diagnosis, a drug, a scan) is *linked to a verified outcome* (the patient survived, relapsed, was readmitted, recovered). That linkage is what "outcomes-indexed" means. Most medical data is NOT like this: it's free-text doctor's notes, scanned PDFs, lab values in incompatible formats, scattered across hospitals that don't talk to each other, with the actual outcome often unrecorded or buried in a note months later [inference, grounded in sourced data-scarcity literature below].

A "clinical & outcomes-indexed data pipeline" is the industrial process that ingests this chaos and turns it into clean, structured, outcome-labeled records — continuously, not once. Think of it as the difference between owning a pile of receipts versus owning audited financial statements: same underlying paper, wildly different value.

*Analogy:* It's the oil refinery, not the oil well. Crude medical data is abundant and nearly worthless; refined, outcome-linked data is scarce and is what every drug company and diagnostic AI actually needs. *Where the analogy breaks:* a refinery is a fixed machine; this pipeline must constantly fight a moving target — privacy law, hospital IT changes, new disease codes, and the fact that "what happened to the patient" is itself a human judgment that has to be re-extracted from prose, not read off a gauge.

**Why it's the "real moat":** Anyone can fine-tune a model; the weights are commoditized. What you cannot quickly replicate is years of relationships with hundreds of clinics, the legal/consent infrastructure to use their data, and the accumulated, validated outcome labels. The clearest market proof: Roche paid ~$1.9B in 2018 for Flatiron Health — a company whose core asset was exactly this (oncology records from 260+ clinics linked to real-world cancer outcomes), explicitly to get "regulatory-grade real-world evidence" [sourced]. The model was never the point; the indexed data was.

**Impact on product/cost/moat/risk:**
- *Product:* enables claims you can defend to a regulator ("this treatment improved survival in real patients"), not just a demo.
- *Cost:* expensive and slow to build; cheap competitors can't shortcut it.
- *Moat:* deep and durable — it compounds over time and is protected by contracts, consent, and trust.
- *Risk:* concentrated in privacy/regulatory exposure (HIPAA/GDPR), label accuracy, and bias if the patient population isn't representative.

**Hype check:** The term "pipeline" and "AI data platform" are often used by vendors to dress up basic data cleaning/ETL, which is genuinely modest engineering. The thing described here is NOT modest — but buyers should verify a vendor actually has *outcome linkage and validated labels*, not just tidy data. The gap between "we structure EHR data" (common) and "we have validated outcomes tied to interventions across a large representative population" (rare) is where almost all the value sits. If a pitch blurs those two, be skeptical.

**2. Skill set required**

This is a *multi-disciplinary* effort, not a single engineer's job:
- Data/ML engineers who handle large, messy, sensitive data at scale.
- Clinical informaticists and people fluent in medical data standards (FHIR, ICD/SNOMED coding).
- NLP specialists to extract facts from free-text notes (e.g., pulling "tumor progressed on date X" out of a paragraph) [sourced: Flatiron uses NLP/LLMs for exactly this].
- Practicing clinicians or trained abstractors to define and validate what counts as an "outcome."
- Privacy/legal/regulatory experts (de-identification, consent, HIPAA).
The rare ingredient is people who sit at the *intersection* of clinical medicine and data engineering — not pure ML talent.

**3. Difficulty: 5/5 — and why**

This is the eight-figure, multi-year end of the spectrum, not a weekend project. The difficulty is not algorithmic cleverness; it's that every hard part is *organizational and physical*, not computational:
- You must source data from many institutions, each with its own systems, contracts, and reluctance.
- Outcome labels often require expert humans (one cited example: ophthalmologists were paid over $25M to label diabetic-retinopathy images) [sourced].
- It must run continuously and stay accurate as codes, software, and laws change.
- Errors have clinical and legal consequences, so validation overhead is enormous.
None of this can be brute-forced with more GPUs. The bottleneck is access, trust, and human expertise — which is precisely why it's a moat.

**4. Who can actually do it**

Not "any web team." Not even most strong ML teams — a great ML team with no clinical access and no abstraction operation cannot build this. Realistically it's the domain of: large pharma, big EHR vendors, integrated hospital systems, and a small number of specialist companies (Flatiron-style) [inference]. The constraint is *data access and clinical operations*, not modeling talent. Globally this is plausibly a few thousand organizations at most that *could* attempt it, and far fewer that have done it well in any given disease area [speculation — no precise count found].

**5. Cost (orders of magnitude, with basis)**

[inference, anchored to the sourced data points below]
- *Compute/training runs:* surprisingly *minor* — likely the smallest line item. This is not a frontier-model training problem; it's a data-acquisition problem. Plausibly low-to-mid six figures of compute annually.
- *Human labeling/abstraction:* major — the $25M retinopathy-labeling figure shows a *single* labeling task can hit eight figures [sourced]. Expert clinical labeling is the dominant recurring cost.
- *Data partnerships/access:* major — building relationships with hundreds of clinics is a multi-year sales/legal effort; this is part of why Flatiron's whole package commanded ~$1.9B [sourced].
- *Talent + infra + compliance:* sustained eight-figure-per-year for a serious operation [speculation].
Bottom line: total cost is dominated by *people, partnerships, and compliance — not silicon*. Expect cumulative spend in the tens to hundreds of millions for a category-leading asset; that's consistent with the Flatiron valuation [inference].

**6. Data requirement & scale — and why it's a moat**

- *What:* longitudinal patient records (notes, labs, imaging, prescriptions, billing codes) **linked to verified outcomes** (survival, progression, readmission, response to treatment). The linkage is the asset.
- *How much:* large and, critically, *representative* of the real patient population — not just volume but coverage across demographics, sites, and time. Flatiron drew on 260+ clinics; that breadth is the point [sourced].
- *How sourced:* through negotiated partnerships with care providers, with consent and de-identification — slow, relationship-driven, legally constrained. Healthcare produces a huge share of the world's data, but most is unstructured and siloed, which is exactly why raw volume alone is worthless [sourced].
- *Why it's a moat:* it compounds (more years = more outcomes), it's contractually and legally fenced (a rival can't scrape it), the outcome labels are costly and expert-gated, and trust/partnerships take years to build. A competitor with the same model and the same money still needs *time and relationships* you've already spent — and in regulated medicine, "regulatory-grade" provenance is a further barrier a fast follower can't fake [inference, supported by the Roche/Flatiron rationale].

*Unknowns:* exact dataset sizes, current per-record labeling costs as of 2026, and the precise number of organizations capable of this are **unknown — not found**.


### Voice-to-voice / real-time speech loops

**1. What it is + its impact**
A voice-to-voice loop is a system you can talk to out loud and that talks back, fast enough to feel like a phone call rather than a walkie-talkie. The hard part isn't "the AI is smart" — it's the *loop*: the system has to listen while you're still speaking, notice when you stop, think, and start replying in well under a second, and gracefully handle you interrupting it. Under 500ms of silence-to-reply feels natural; past ~1.5 seconds the magic breaks and it feels like a robot (inference; latency thresholds per [LiveKit](https://livekit.com/blog/voice-agent-architecture-stt-llm-tts-pipelines-explained), n.d.).

There are two ways to build it, and the distinction is the whole strategic story:
- **Cascaded ("pipeline"):** glue three off-the-shelf parts together — speech-to-text (STT) → a normal text LLM → text-to-speech (TTS). This is the default for production today. You can hit sub-1-second latency, you get a text transcript at every step (great for compliance, logging, analytics), and you can swap vendors per stage (sourced — [LiveKit](https://livekit.com/blog/voice-agent-architecture-stt-llm-tts-pipelines-explained), n.d.).
- **Native / end-to-end ("speech-to-speech"):** one model takes in raw audio and emits raw audio, never fully converting to text in the middle. Lower latency (sub-500ms), more natural tone, and it can hear *and produce* emotion, laughter, hesitation. OpenAI's Realtime API and the open-source Moshi work this way (sourced — [OpenAI Realtime](https://openai.com/index/introducing-the-realtime-api/), 2024; [Kyutai Moshi](https://kyutai.org/Moshi.pdf), 2024).

What choosing this changes:
- **Product:** voice becomes a first-class interface (support agents, companions, tutors, drive-thru, phone-based workflows). The native path feels noticeably more human; the cascaded path is more controllable.
- **Cost:** voice is meaningfully more expensive per interaction than text. On OpenAI's hosted Realtime API, audio runs roughly **$0.06/min in and $0.24/min out**, and a realistic 5-minute call lands around **~$0.50** (sourced — [OpenAI pricing](https://openai.com/api/pricing/) / [eesel summary](https://www.eesel.ai/blog/gpt-realtime-mini-pricing), 2025). At call-center scale that adds up fast.
- **Moat:** almost none if you call a hosted API — your competitor can wire up the same API in a week. The moat lives in everything *around* the loop: interruption handling, turn-taking, your voice/persona, domain tuning, telephony integration, and proprietary conversation data. **The technique is a commodity; the polish is not** (inference).
- **Risk:** native end-to-end models give you *less* control — harder to audit, weaker/less-predictable tool-calling, and you can't easily inspect "what did it think the user said" because there may be no clean transcript. That's why regulated industries (health, finance) still lean cascaded (sourced — [LiveKit](https://livekit.com/blog/voice-agent-architecture-stt-llm-tts-pipelines-explained), n.d.). Plus the usual voice risks: voice cloning / impersonation, hallucinated answers spoken confidently, and latency spikes that ruin the experience.

**2. Skill set required**
Two very different bars depending on the path. *Using* hosted voice loops (cascaded or OpenAI Realtime) is a **strong applications/infra engineering** job — real-time audio streaming, WebRTC/websockets, telephony (SIP), barge-in/interruption logic, latency tuning. No ML research needed. *Building your own native speech-to-speech model from scratch* is a **frontier ML research** job — neural audio codecs, multi-stream transformers, large-scale distributed training, audio data pipelines (inference, grounded in [Moshi paper](https://kyutai.org/Moshi.pdf), 2024).

**3. Difficulty: 4/5 — and why it's bimodal**
Wiring a hosted voice loop into a product is roughly a 2/5 — a capable team can get a talking demo working in days using the Realtime API or a cascaded stack. Making it *production-grade* (handling interruptions, background noise, accents, tool calls, sub-second latency at scale, telephony) is a solid 3–4/5 of unglamorous engineering. **Training your own competitive native speech-to-speech foundation model is a 4–5/5** — Kyutai trained Moshi on **1,016 H100 GPUs** over **7 million hours of audio** (sourced — [arXiv Moshi](https://arxiv.org/html/2410.00037v2), 2024). I'm scoring the overall technique **4** because the headline capability ("an AI you can have a natural spoken conversation with") requires either real research muscle or serious real-time engineering to do well — it is not a weekend project at the quality bar users now expect.

**4. Who can actually do it**
- *Integrate a hosted voice loop into a product:* **any strong product/infra team** — thousands of companies, and rising.
- *Build a polished, low-latency, reliable voice agent:* a **strong engineering team** willing to grind on real-time/telephony plumbing — hundreds to low thousands of teams.
- *Train a genuinely competitive native speech-to-speech foundation model:* **fewer than a few hundred people on earth**, concentrated at OpenAI, Google, a handful of labs like Kyutai, and well-funded startups (inference, supported by the very short list of orgs that have shipped one as of mid-2026).

**5. Cost (orders of magnitude, with basis)**
- *Integrate via hosted API:* **near-zero capex; opex is per-minute.** ~$0.06/min in, ~$0.24/min out, ~$0.50 per 5-min call (sourced — [OpenAI pricing](https://openai.com/api/pricing/), 2025). The bill is a usage line item, not an R&D project.
- *Build a strong cascaded voice agent yourself:* a **few engineers for a few months** = low-to-mid six figures in talent, plus per-minute STT/LLM/TTS vendor fees (inference).
- *Train your own native speech-to-speech model:* **single-digit-millions-of-dollars order of magnitude** for an open-weights-class model. Basis: Moshi used ~1,016 H100s; at rough cloud rates (~$2–4/GPU-hour) a multi-week run is hundreds of thousands to low millions in compute, plus a small expert team and data pipeline (inference, grounded in [arXiv Moshi](https://arxiv.org/html/2410.00037v2), 2024). A *frontier* multimodal model from a top lab is far higher and not separable from the lab's overall spend (speculation — exact figure unknown, not found).

**6. Data requirement & scale**
For the *cascaded/hosted* path: essentially **no training data** — you rent pre-trained models and supply only prompts/config (inference). For *building a native model*, data is the real moat and it's lopsided:
- **Massive cheap pre-training audio:** Moshi used **~7M hours of English + 450k hours of French** unlabeled audio (sourced — [arXiv Moshi](https://arxiv.org/html/2410.00037v2), 2024). Scrapeable, but at a scale only serious operations handle.
- **Synthetic dialogue:** ~**20,000 hours** of TTS-generated conversations to teach turn-taking (sourced — same).
- **Scarce, expensive real two-person conversational audio:** only **~170 hours** of natural multi-speaker dialogue, hand-collected (sourced — same).

Why it's a moat: anyone can scrape podcasts, but **real, consented, two-sided, multi-speaker conversational audio — especially with emotion, interruptions, and your specific domain (e.g., real support calls) — is rare, legally sensitive, and slow to collect.** That proprietary conversational data, far more than the model code, is the defensible asset (inference).

**Hype check:** "Real-time AI voice" is marketed as a breakthrough capability, but in mid-2026 the *integration* is largely commoditized — a hosted API call. The genuinely hard, scarce work is (a) training a native speech-to-speech foundation model (few labs) and (b) the unsexy real-time engineering and proprietary data that make a voice agent feel good and behave reliably. If a vendor pitches "we built proprietary real-time voice AI" but is really calling OpenAI's Realtime API with a nice UI, that's inflated framing — the differentiation is in the product layer and data, not the underlying technique (inference).


### Prompt engineering & orchestration (the craft of a good "wrapper")

**The one-line version:** This is the craft of getting great results out of an AI model you didn't build — by writing precise instructions, feeding the model the right information at the right moment, and wiring multiple AI calls together into a reliable workflow. You are not building the engine; you are building everything around it.

**A concrete analogy:** Think of the underlying AI model (GPT, Claude, Gemini) as a brilliant, fast, but amnesiac contract employee — genius-level capability, zero memory of your business, and prone to confidently making things up. Prompt engineering and orchestration is the *management system* around that employee: the job description you hand them (the prompt), the briefing folder of relevant facts you put on their desk before each task (context/retrieval), and the assembly line that routes work between several such employees with quality checks in between (orchestration). A great manager gets 3x the output from the same employee. That's the entire game here.

**Where the analogy breaks:** A human employee learns and improves over weeks; the AI model does not change at all — every single request starts from scratch, so *all* the "memory" and "learning" you see is an illusion that the wrapper-builder manufactures by re-feeding information each time. Also, unlike a human, the model can be tested millions of times cheaply, so the "management" can be tuned with data in a way no HR department ever could.

---

**1. What it is + its impact.** It is the application layer on top of someone else's model: writing and tuning instructions, deciding what data to inject into each request (increasingly called *context engineering* — now treated as the more important discipline [sourced, deepset blog, 2025-2026]), chaining multiple model calls, adding retrieval, tools, memory, and guardrails. What choosing this changes for a business:
- *Product:* You can ship a working AI product in days-to-weeks instead of years. Time-to-market is the headline benefit.
- *Cost:* You pay per-use API fees to the model maker instead of building infrastructure. Cheap to start; the cost risk is that your margins are exposed to someone else's pricing.
- *Moat:* This is the critical caution. Prompt engineering *alone* is a weak moat — anyone can copy a clever prompt, and "GPT wrapper" became a near-slur for thin businesses [sourced, aimultiple/Medium, 2026; contested as to degree]. The defensible version is the *orchestration + proprietary context* combination: your workflows, your data plumbing, your evaluation/quality systems, and your distribution. The moat is in the system and the data feeding it, not the prompt text.
- *Risk:* Platform dependency. The model maker can raise prices, change behavior, deprecate the model, or launch a competing feature that absorbs your product. Your "secret sauce" prompt can also leak or be reverse-engineered.

**2. Skill set required.** Mostly strong *software/product engineers*, not ML researchers. No knowledge of how to train a neural network is needed. The valuable skills are: clear systems thinking, careful experimentation, building evaluation harnesses (test suites that score AI outputs at scale), data plumbing (retrieval, databases), and increasingly the "context engineering" discipline of assembling the right information per request [sourced, deepset/Lakera, 2026]. The senior version of this role looks like a thoughtful backend/product engineer with good judgment and patience, plus a bit of statistical literacy to read evaluation results. A useful frame: it is closer to skilled *integration and product engineering* than to research.

**3. Difficulty: 2/5.** A basic working wrapper is genuinely a weekend project — this is the lowest-barrier technique on the AI stack, which is exactly why it is crowded. The reason it is a 2 and not a 1: getting from a flashy demo to a *reliable, cheap, hard-to-break production system* is real engineering. Reliability at scale — handling edge cases, preventing the model from going off-script, controlling cost-per-request, evaluating quality across thousands of cases, multi-step agent workflows that don't silently fail — is where most teams struggle and where months of effort go. Frameworks like LangGraph exist specifically to make production-grade, auditable, resumable agent workflows tractable, and are reported to cut time-to-production by months [sourced, langchain.com/aimultiple, 2026; vendor-sourced, treat as directional]. So: trivial to start, moderately hard to do *well*.

**4. Who can actually do it.** Very broad. Essentially *any competent web/software team* can build a real product here — this is the democratized layer of AI, accessible to perhaps hundreds of thousands of developers worldwide, not a rarefied few. The scarcity is not in raw ability but in *taste and rigor*: the teams that build excellent evaluation systems, deep domain integration, and reliable orchestration are a much smaller subset. But the entry gate is low and intentionally so — this is the opposite of the "fewer than a few hundred people" tier that frontier-model pretraining occupies.

**5. Cost — orders of magnitude.** This is the cheap end of the AI spectrum.
- *Build/talent:* A small team (1-5 engineers) for weeks to a few months. Order of magnitude: tens of thousands to low-hundreds-of-thousands of dollars to a serious v1. [inference, based on standard software team economics]
- *Training runs:* Effectively zero — you are not training a model. This is the defining cost advantage. [inference]
- *Compute/infra at runtime:* You rent intelligence via API. Per-request costs are typically fractions of a cent to a few cents; a real product's model bill might run from hundreds to tens of thousands of dollars a month depending on volume. [inference, based on published per-token API pricing as of 2026; exact figures unknown without specifics]
- *Comparison for scale:* Training a frontier model from scratch is a hundred-million-to-billion-dollar undertaking. Prompt/orchestration work is 3-5 orders of magnitude cheaper. That gap *is* the value proposition. [inference; frontier training cost widely reported in that range, contested specifics]

**6. Data requirement & scale — and why it's the real moat.** To *build* the wrapper you need almost no data — that's the appeal. But the difference between a copyable wrapper and a defensible business is *exactly* the data:
- *To operate well, you need:* (a) the proprietary content/knowledge you feed the model per request (documents, records, your company's domain data — the "briefing folder"), and (b) *evaluation data* — sets of test inputs with known-good outputs so you can measure whether changes help or hurt. This eval data is underrated and is where serious teams invest.
- *How much:* Hundreds to a few thousand well-chosen evaluation cases can be enough to tune a system rigorously — small by ML standards. The proprietary content can be any size; what matters is that it is *yours* and well-organized for retrieval. [inference]
- *Why it's a moat:* The prompt is copyable; your proprietary knowledge base, your accumulated usage data, and your evaluation suite are not. A competitor can clone your interface in a weekend but cannot clone the domain data and the thousands of hours of quality-tuning behind it. The durable moats in this layer are *proprietary context + distribution + evaluation rigor*, not prompt cleverness [inference, consistent with sourced 2026 commentary that the moat moved from prompts to context/systems].

**Hype check.** Marketing routinely dresses this layer in grand language — "agentic AI," "reasoning engines," "cognitive architectures." Strip it down and most of it is: good instructions + the right data injected per call + a workflow that chains model calls with checks. That is genuinely valuable and can support real businesses, but it is *engineering craft on top of someone else's intelligence*, not the creation of intelligence. When a pitch implies the company has built something model-like or owns deep AI IP, and on inspection it is a prompt-and-orchestration layer over a third-party API, the moat claim should be treated skeptically and pressed on: *what here can't a competent team rebuild in a month?* The honest answers are usually data, distribution, and accumulated quality work — not the prompts.


---

# Part B — Per-Company Engineering Deep-Dive

_Tiered depth: Slingshot/Ash deepest; the genuine builders (Spring, Limbic, Jimini, ieso, Wysa) deep; the rest get a real technical read of how sophisticated their "wrapper" actually is. Each is grounded in its existing dossier and extended._


## Slingshot AI (Ash)

Ash is a consumer therapy chatbot. The single most important engineering fact about it is what it is **not**: it is not a from-scratch AI brain. Slingshot took a powerful open-weight model that someone else built and spent roughly 18 months specializing it for therapy and wrapping it in a safety system. Almost none of the individual techniques are new inventions. The genuinely hard, genuinely defensible work sits in two places — the **clinical data** and the **safety subsystem** — not in the model itself.

### What they actually built on

The backbone is an open-weight model from Alibaba's Qwen team — specifically Qwen3-235B, a "mixture-of-experts" model with 235 billion total parameters but only ~22 billion active at a time. **[sourced — nebius.com/customer-stories/slingshot-ai, accessed 2026-06-24; the MoE architecture detail from arxiv.org/html/2505.09388v1]**

One honest qualification on the backbone, per the verifier: only the Nebius case study actually names Qwen3-235B. Together AI's case study, where the fine-tuning runs, says only that Slingshot trains on "a broad range of open foundation models" — plural, and it never names Qwen3. The safety paper names no base model at all. So "Ash is one Qwen3-235B flagship" is a tidy story that may be an oversimplification; they may post-train more than one open base. **[inference — the single-backbone framing is partly assumed; "broad range of open models" is the only cross-source phrasing]**

On top of that rented model, Slingshot does standard post-training: continued pre-training on therapy material, supervised fine-tuning on clinician-written examples, a reward model trained on clinician preferences, and a DPO/reinforcement-learning loop. **[sourced — nebius.com; together.ai/customers/slingshot-ai; pmc.ncbi.nlm.nih.gov/articles/PMC12869570]** These are well-documented, widely-practiced techniques — applied AI, not frontier research. The skill is in operating them well for a high-stakes domain, not in inventing them.

### Where the real difficulty lives: the data and the safety net

**The proprietary clinical data is the moat.** It comes in three grades, each harder to get than the last:

- A pre-training corpus described as "one of the largest and most diverse datasets of behavioral health data ever assembled," including de-identified real psychotherapy transcripts. **[sourced — nebius.com; pmc.ncbi.nlm.nih.gov/articles/PMC12869570]** The "largest ever" claim has no number attached and is company marketing. **[contested — unquantified]** Crucially, sourcing real, consented, de-identified therapy at scale is a legal-and-relationships problem, not a coding problem — which is exactly why money can't buy it quickly. **[inference, well-supported]**
- Supervised fine-tuning examples authored by Slingshot's own clinical staff, teaching the model the micro-decisions of a good therapist: when to challenge a user, when to stay silent, when to end a session. **[sourced — nebius.com; pmc.ncbi.nlm.nih.gov/articles/PMC12869570]** Each example is a licensed clinician's judgment written down. This is the most talent-gated input in the whole stack.
- Preference data: "thousands of comparisons written by clinical experts," weighted most heavily in the reward signal, alongside user-behavior signals and an LLM-as-judge. **[sourced — nebius.com]** Exact count beyond "thousands" is unknown — not found.

The model weights are free and the training recipe is public, so a competitor could copy the architecture in weeks. What they cannot copy is the de-identified therapy corpus, the thousands of clinician judgment calls, and the live stream of real user conversations (used for tuning unless the user opts out) that keeps compounding. **The data compounds; the code doesn't. [inference, well-supported — sourced inputs from nebius.com and choosingtherapy.com]**

**A clever data-manufacturing trick (with one correction).** Slingshot built an adversarial "fake user" generator, published as the DIAL paper (arxiv.org/abs/2512.20773), confirmed Slingshot work co-authored by CEO Daniel Cahn. **[sourced]** Two AIs compete — a generator plays a realistic distressed user, a discriminator tries to spot fakes — until the synthetic conversations are indistinguishable from real ones. Per the verifier, two corrections: the paper has eight authors (not the four the raw notes listed), and its stated purpose is **system evaluation before deployment** — stress-testing Ash against synthetic crises safely — *not* generating training data. Treating DIAL output as a data-augmentation pipeline is an inference, not what the paper claims. **[sourced for the eval purpose; inference for any training-data use]** This adversarial setup is genuine ML research work, because keeping simulated users messy and diverse (rather than bland) is what makes a safety test meaningful.

**The two-pass crisis guardrail is the highest-stakes subsystem.** The "Beyond Simulations" paper (pmc.ncbi.nlm.nih.gov/articles/PMC12869570, published 2026-01-27) describes two independent systems: the therapist model itself, plus a separate safety classifier that does not see the model's internal state. The classifier runs in two stages — a fast, cheap embeddings model tuned for **high recall** (cast a wide net, prefer false alarms over misses), then a slower LLM verifier tuned for **precision** (confirm real crises, cut false alarms). On confirmed suicide risk, the classifier — not the chat model — fires an in-app 988 lifeline banner and a "risk-mitigation mode." **[sourced]** The cheap-wide-net-then-expensive-filter design is a known pattern; applying it to suicide risk with this much care is the hard part, and it's the clearest line between a serious safety team and a thin wrapper. **[inference]**

**What the audit actually showed (with the verifier's corrections applied).** Slingshot reviewed 20,000 real opt-in conversations under NYU IRB approval. Clinician review found **no missed suicide-risk escalations** — the system delivered crisis resources in every confirmed suicide-risk case. The three misses in the September batch were **non-suicidal self-injury (NSSI) edge cases**, a distinct category. **[sourced]** This sharpens the marketing-vs-reality point: the old "100% accuracy" line and the paper are not actually contradictory on suicide risk — 100% on suicide-risk escalation held in the audit; the misses were NSSI. Conflating the two would be misleading. **[contested — the "100%" framing should still be read as a bounded test claim, not an absolute guarantee]** The reported false-negative rate is a stated lower bound (only a triaged subset was reviewed), and the study tested safety behavior, not clinical effectiveness.

On a harmful-content benchmark Ash looked far safer than general chatbots — e.g., self-harm/suicide content: Ash 0.4% vs GPT-5.1 44.0%, GPT-5.2 29.0%, GPT-5 12.0% (verified exactly against the paper). On a 30-question suicide test, Ash gave a direct unsafe response 11.27% of the time vs 54-68% for the GPT-5 family. **[sourced]** One flag: the "median 0% for Ash" detail in the raw notes does not appear in the retrieved paper and is **unverified**. Two honest caveats: four of six authors are Slingshot employees and the work was partly company-funded (a disclosed company-run evaluation), and the comparison is not apples-to-apples — a purpose-built therapy product judged against general chatbots that were never meant to be therapists. **[contested — conflict of interest; sourced — pmc.ncbi.nlm.nih.gov/articles/PMC12869570]**

### The serving layer: mostly rented, with one custom piece

Slingshot rents almost everything. They train on Nebius GPU **clusters** using DeepSpeed/ZeRO-3 and SkyPilot. Per the verifier, a vendor-attribution correction: DeepSpeed/ZeRO-3 (Microsoft-origin) and SkyPilot (UC-Berkeley-origin) are free open-source tools — Nebius rents the GPUs, not those frameworks. **[sourced — nebius.com]** Fine-tuning runs on Together AI's API, which Together says delivers ~5x lower cost and ~3x more frequent training while supporting 50,000+ users. **[sourced — together.ai]** Inference is described as *planned* on managed Kubernetes with autoscaling — note the tense; it is a stated plan, not a confirmed running system. **[sourced — nebius.com]**

The one custom serving piece is a **turn-by-turn model router**: within a single conversation, Ash routes simple turns to a small ~32B model and clinically delicate turns to the big 235B model, trading cost and speed against quality. **[sourced — nebius.com]** Two corrections from the verifier matter here. First, this should **not** be called "MoE / dynamic routing," even though the marketing borrows the word "mixture." Mixture-of-Experts is a different, intra-model mechanism that Alibaba built into Qwen3 and Slingshot inherited for free; Slingshot's router is "model cascading" / "LLM routing" sitting *on top of* an already-MoE base. Conflating them makes it sound more novel than it is. Second, the popular story that they "bought specialist latency talent" by hiring an ML Infrastructure Lead (Alexey Bukhtiyarov) out of the real-time conversational-AI world is **inference stated with too much confidence** — no source says he was hired for routing/latency or that he built the router; the quotes attributed to him are about training orchestration (SkyPilot), not inference. **[inference/speculation — not "the most important finding"]** The routing logic itself (learned classifier vs. rules) is unknown — not found.

### The retraining cadence

The most revealing operational fact is that Slingshot retrains 3-7 times per week — extraordinarily fast, where most ML teams retrain monthly. **[sourced — together.ai]** That cadence implies a CI/CD-style, mostly-automated train-evaluate-deploy pipeline with a trusted offline eval harness, because no clinician can manually sign off on a new model seven times a week. **[inference]** It is feasible precisely *because* they rent the fine-tuning (Together explicitly cites parallel training runs). The quality of that automated eval harness is plausibly the hidden crown jewel — and it is completely undisclosed. The double edge for a therapy product: the system a user talks to on Monday may behave differently by Friday, and every flagged session is clinician-reviewed *after* deployment, not before. **[inference]**

### Difficulty, talent, cost, and scale — for their stack specifically

- **Difficulty:** Roughly 80% careful assembly of known, commodity parts; ~20% genuinely hard — and the hard part is concentrated on the data-and-safety axis, not the model axis. The raw notes also offer a "70/30 commodity-vs-hard" split for the serving layer. Both are useful qualitative judgments but **authorial estimates**, not measured facts — the precise-looking percentages give false quantitative authority. **[inference]**
- **Talent:** Shaped like a spear, not a wall. A sharp tip of a few scarce *applied*-ML engineers (post-training/RLHF, ML infra, safety classifiers), with the CEO — an Imperial College Deep-RL graduate — as de facto model-research lead and a named ML Infrastructure Lead. Around them, a broader, more hireable ring of product/app/backend engineers, plus licensed clinical psychologists ($50-75/session contractors) authoring data. **Important correction:** earlier framing called RLHF engineers "among the scarcest in the entire industry, fought over by OpenAI/Anthropic/DeepMind." That overstates it — SFT+DPO+reward-model fine-tuning of an open-weight model is applied ML practiced across many startups, not frontier pre-training research. The scarcity is real but narrow (a handful of roles), not industry-wide. Because they buy the base model, they skip the single most expensive talent category — frontier pre-training researchers — entirely. **[sourced for techniques and named people; inference for scarcity, now corrected downward]**
- **Cost:** Genuinely lean. ~16-40 FTEs total, engineering hub in London. The serving choices (rent GPUs, rent fine-tuning) are smart capital allocation that keeps the team small. On pay, there is exactly **one** hard datapoint — a $250,000 NY software-engineer base (2025 H1B filing). Everything else — London bands of ~£130k-£180k+ base, £200k+ total comp, a "£15k-£30k RLHF premium" — is generic market-survey extrapolation (Robert Half / CareerCheck), not Slingshot actuals. So "they must be paying top-of-market" is an inference from one datapoint plus salary surveys, not corroborated fact. **[sourced — h1bdata.info for the $250k; inference for everything else]**
- **Data scale:** The decisive axis, and almost entirely undisclosed. The pre-training corpus size (tokens/conversations), the SFT example count, and the exact preference-comparison count are all unknown — not found. What *is* sourced: "thousands" of clinician comparisons and a 20,000-conversation safety audit. GPU counts/type, latency in milliseconds, cost per conversation, and the production inference host are all unknown — not found as of 2026-06-24.

**Engineering moat:** The model is rented and the techniques are commodity — the real, hard-to-copy moat is the proprietary clinical data plus the audited, recall-first safety subsystem built on top of it.

### Sources
- https://nebius.com/customer-stories/slingshot-ai
- https://www.together.ai/customers/slingshot-ai
- https://www.together.ai/blog/fine-tuning-updates-sept-2025
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12869570/
- https://arxiv.org/abs/2512.20773 (DIAL)
- https://arxiv.org/html/2505.09388v1 (Qwen3)
- https://slingshotai.com/careers and https://api.ashbyhq.com/posting-api/job-board/slingshotai (job ads)
- https://h1bdata.info/index.php?em=Slingshot+AI ($250k SWE datapoint)
- https://www.statnews.com/2025/11/24/slingshot-ai-mental-health-chatbot-safety-study-results/
- https://www.choosingtherapy.com/ash-ai-therapy-app-review/
- https://developer.nvidia.com/blog/an-introduction-to-speculative-decoding-for-reducing-latency-in-ai-inference/


## Spring Health

Spring Health runs **two completely different AI systems** that are easy to confuse. To understand the engineering, you have to keep them separate: one is old-school predictive machine learning that Spring genuinely owns, and the other is a 2025–2026 chatbot built on top of other companies' AI models.

### System 1: The matching engine — classical machine learning, genuinely proprietary

This is **not** a chatbot and **not** a large language model. When you fill out Spring's short intake questionnaire, a traditional statistical model scores you and predicts which therapist or type of care is most likely to help someone like you.

- **What it actually is:** feature-based predictive modeling — the kind of machine learning that existed long before ChatGPT. It takes structured inputs (your PHQ-9 depression score, GAD-7 anxiety score, demographics, preferences) plus the historical track record of each provider, and outputs a ranked match. *[inference, grounded in the sourced study below]*
- **Two versions, peer-reviewed:** A 2025 peer-reviewed study (*"Using Machine Learning to Match Clients and Therapy Providers,"* ScienceDirect) describes a **"Pragmatic"** algorithm (logistics plus clinical relevance) and a **"Value-based"** algorithm that also factors in each provider's historical outcomes and cost. On anxiety, the two performed about the same on reliable improvement/recovery (71.74% Pragmatic vs. 70.02% Value-based), but the value-based version cut total cost of care by roughly 20% using about 2 fewer sessions per person. *[sourced — sciencedirect.com S1098301525024052, accessed 2026-06-24]*
- **Note correcting an earlier internal dossier:** an earlier draft flagged this paper as "not a matching-validation study." That was wrong — it **is** a matching-algorithm validation (Pragmatic vs. Value-based). So Spring's matching ML does have at least one company-authored, peer-reviewed validation, though still on Spring's own data, not an independent dataset. *[contested — corrects an earlier claim, now verified]*
- **How hard is this?** Medium. This is well-understood applied ML; the algorithm itself isn't exotic. The hard part is the **data**: clean, repeated outcome measurements over time, tied to specific provider-member pairs, plus per-provider outcome and cost history. That data — not the math — is the real moat. It needs senior applied-ML scientists, not special infrastructure, and the compute cost is trivial next to running large language models. *[inference]*

### System 2: "Guide" — the LLM chatbot, built on other companies' models

Guide is Spring's conversational AI product for members. The single most important engineering fact: **Spring does not build or train its own language model.** It builds on top of frontier models from OpenAI, Anthropic, and Google. This is now firmly established, not a guess: Spring's own published validation work explicitly names the vendor models it uses — GPT-4o, GPT-5, Claude Sonnet 4.5, and Gemini all appear by name in their evaluation papers. *[sourced — arxiv 2602.05088]*

What Spring **does** engineer is the system *around* the model:

- **Multi-agent design (the real architecture decision).** Instead of one giant do-everything bot, Guide is **five narrow agents** plus a generalist fallback: a routing/orchestration agent that figures out what you need; a booking agent; a provider-matching agent; an in-the-moment support agent (explicitly told *not* to act like a therapist or make clinical decisions); and a customer-support agent. When a request is ambiguous, the system **asks a clarifying question instead of guessing.** *[sourced — springhealth.com, 2026-05-21]*
- **Why this is the right call, in plain terms:** when one bot tries to do everything, quality drops across the board, and real members mix emotional and logistical needs in a single message — which breaks a monolithic bot. Their stated principle: *"precision at the handoff matters more than simplicity in the architecture diagram."* In a suicide-risk situation, the dangerous moment is the gap between detecting risk and handing off to a human, so they split that out and harden it. *[sourced]*
- **Scale:** 200,000+ real conversations across pilots, with early signals like 5% more therapy sessions in the first 7 weeks and care continuity rising 57% → 60%. *[sourced — springhealth.com, 2026]*

### Which "core AI techniques" they actually use

- **Training their own model (pre-training, fine-tuning, RLHF, DPO, etc.):** **No.** No evidence Spring pre-trains, fine-tunes, or does preference optimization on any language model. When Spring advertises that "every match and outcome feeds a model," that refers to the **classical matching ML**, not LLM training. *[inference]*
- **Mixture-of-Experts / model-internal routing:** **No.** Their "routing" is **application-level** — deciding which of the five agents handles you — not the model-internal expert routing the term usually means. Easy to confuse; technically different. *[sourced for agent routing; MoE not applicable]*
- **Serving / latency:** **Real but undisclosed.** They run a multi-cloud MLOps stack (Kubernetes, Terraform, model registry, feature stores, per job postings), but publish no latency or token-budget numbers. Most of the heavy LLM-serving load is effectively the vendors' problem. *[sourced for tooling; latency unknown — not found]*
- **Guardrails / safety:** **Yes, treated as first-class** — *"Safety is not a wrapper around the product. It is part of the product."* Implementation specifics (input/output classifiers, prompt-injection defenses) are not published. *[sourced for the principle; implementation unknown — not found]*
- **Crisis detection:** **Yes — their strongest, best-documented area.** An automated flag (the exact instrument isn't named — *speculation* that it's the PHQ-9 self-harm item) triggers a 24/7 master's-level care-navigator outreach team. A peer-reviewed study (*Psychiatric Services*, Jan 2026, n=6,131) backs this pipeline: proactive outreach within 24 hours of a suicidal-ideation flag, 87.3% of contacted members attending at least one appointment within six months, and successful outreach more than doubling the odds of starting treatment. This is more an **orchestration and clinical-operations pipeline** than an AI model. *[sourced — psychiatryonline.org appi.ps.20250319]*
- **LLM-as-judge:** **Yes — their most distinctive engineering.** Spring's open-source **VERA-MH** harness uses one AI model to **role-play patient personas** at varying suicide-risk levels, and a second AI model as a **judge** that scores the chatbot against a clinical rubric. It's built on LangChain and Pydantic with async batch orchestration (a `ConversationRunner` with configurable concurrency) and supports OpenAI, Anthropic, Google, Azure, and Ollama models. *[sourced — github.com/SpringCare/VERA-MH]*
  - **Two papers, two designs (don't conflate them).** A **concept paper** (arxiv 2510.15297) used 10 clinician-written personas, 5 conversations each, on an earlier rubric, and reported **raw per-dimension agreement of roughly 41–60%** between the judge and clinicians on specific behaviors. A separate, later **validation paper** (arxiv 2602.05088) used a different design — 90 conversations (30 each driven by GPT-4o, GPT-5.0, and Gemini-3-pro as the "patient" side) and a 100-persona library — and reported a **chance-corrected agreement (IRR) of 0.81 between the AI judge and the clinical consensus**, against 0.77 among the clinicians themselves. The validation paper frames that 0.81 as **genuine strong alignment**, concluding it "establishes clinical validity and reliability of VERA-MH." Its five rubric dimensions are: **Detects Potential Risk, Confirms Risk, Guides to Human Care, Supportive Conversation, and Follows AI Boundaries.** *[sourced — arxiv 2510.15297 and 2602.05088]*
  - **Honest read of where it stands:** calibrating an AI judge to clinician-level safety judgment is an **open, ongoing problem** — promising but not finished. The earlier per-dimension agreement numbers show the rough edges; the later validation shows strong overall alignment. (An earlier internal draft of this analysis claimed the judge had a "leniency bias," citing a figure that the judge rated 88% of behaviors "Best Practice" versus clinicians' 46%. **That statistic does not appear in either paper and was fabricated** — in the validation paper, clinicians' most common rating was actually "Suboptimal but Low Potential for Harm" at 33.6%, with "Best Practice" at 30.7%. There is no leniency-bias finding in the source, and it should be disregarded.) *[contested — corrects a fabricated stat]*
- **Clinical evals:** **Yes.** They use VERA-MH on their own product — Guide's safety score reportedly rose from 76 to 82 after they fixed handoff gaps. *[sourced]*
- **RAG / memory:** **Partial / implied.** Guide "carries context across providers, sessions, and life stages," and Compass (their EHR) summarizes sessions and surfaces prior-session insights — which implies some retrieval/memory over patient records, but no specific architecture is disclosed. *[inference; specifics unknown — not found]*
- **Data pipelines:** **Yes, and non-trivial** — HIPAA-grade, with training/clinical-data separation, masking, and a real-time crisis-flag pipeline. This is where serious engineering effort genuinely goes. *[sourced/inference]*
- **Voice / speech:** **Partial.** Compass does consented session recording and summarization ("AI note-taking," reportedly making notes 40% faster), which implies speech-to-text — but there's no detail on whether it's built or bought (almost certainly a vendor speech engine). *[sourced for the feature; build-vs-buy unknown — not found]*
- **Prompt / orchestration:** **Yes — the core of what they build.** The five-agent routing system, the clarify-don't-guess behavior, and the per-agent scope limits are all prompt-and-orchestration engineering (LangGraph/LangSmith appear in job postings). *[sourced]*

### Genuinely hard vs. commodity assembly

**Commodity (assembled, not invented):** the language model itself, basic chat plumbing, the standard web/data stack, and even the multi-agent pattern (a well-known 2025–2026 design).

**Genuinely hard, in Spring's specific case:**
1. **Calibrating an AI judge to clinician-level safety judgment** — an open, ongoing calibration problem. Their validation shows strong overall alignment (IRR 0.81), but per-behavior agreement is still imperfect; to their credit, they publish both.
2. **The handoff between AI risk-detection and a live human** under real liability — a systems-plus-clinical-ops problem they treat as the central safety risk.
3. **The longitudinal outcomes data asset** feeding the value-based matching model — slow to accumulate, genuinely proprietary, and peer-reviewed.
4. **HIPAA-grade data governance plus real-time crisis orchestration** at large scale.

**Bottom line:** Spring is an **orchestrator and evaluator of other companies' AI models**, with one real piece of proprietary classical ML (matching) and one distinctive open-source contribution (the VERA-MH evaluation harness). The hard parts are clinical-safety evaluation, handoff orchestration, and data governance — strong senior execution, not foundation-model research.

**Engineering moat:** A well-engineered wrapper — its durable advantages are proprietary clinical-outcomes data and published safety-evaluation tooling, not any model it owns.

### Sources
- springhealth.com — "Why we built Guide as a multi-agent system" (2026-05-21)
- arxiv 2510.15297 — VERA-MH concept paper (10 personas, raw per-dimension agreement ~41–60%)
- arxiv 2602.05088 — VERA-MH validation paper (IRR 0.81 vs. 0.77; five rubric dimensions; vendor models named)
- github.com/SpringCare/VERA-MH — open-source harness (LangChain + Pydantic, ConversationRunner, 100 personas)
- sciencedirect.com S1098301525024052 — "Using Machine Learning to Match Clients and Therapy Providers" (Pragmatic vs. Value-based)
- psychiatryonline.org appi.ps.20250319 / PubMed 41236311 — crisis-outreach study (n=6,131)
- springhealth.com — Compass EHR; "Building an AI-native mental health company"; data-driven provider matching; Guide outcomes news


## Limbic

**Bottom line up front:** Limbic does **not** build its own AI brain. It rents a general-purpose AI — and can swap between OpenAI's GPT-4o, Anthropic's Claude 3.5, Google's Gemini 1.5, and Meta's Llama 3 — then wraps it in a thick, custom-built control system called **the Limbic Layer**. Picture the rented AI as a fluent but unsupervised talker, and the Limbic Layer as a supervising clinician sitting on both sides of the conversation: screening what the patient says before the AI sees it, deciding which therapy step should happen next, looking up approved clinical material, and inspecting every sentence the AI produces before the patient reads it.

For years the internals were secret. Two disclosures changed that, and the distinction between them matters. A **November 2024 preprint** announced that this architecture *exists* — but it was a small study testing only one base model (GPT-4), describing the Layer in vague terms ("a novel ensemble of ML models," "four major components"). It contained **none** of the specifics below. The real machinery — the dataset sizes, accuracy scores, the fine-tuning method, the retrieval setup, the state machine, the evaluation numbers — was disclosed only in the **March 2026 peer-reviewed Nature Medicine paper** (republished on bhnet.org). So when this section gets concrete, the reader should know: those details are **effectively single-sourced to one 2026 paper**, not independently corroborated by two. The numbers are detailed and internally consistent, but they are the company's own published account. [sourced — Nature Medicine 2026; preprint doi 10.31234/osf.io/9d7tp]

**One more thing to keep straight:** "Limbic" is not one product. There are at least three. **Limbic Access** is a triage/self-referral chatbot that holds a Class IIa UKCA medical-device mark and predicts likely disorders for NHS patients. **Limbic Care / the Limbic Layer** is the CBT therapy-delivery system in the Nature paper — this is where all the F1 scores and machinery below come from. A **2025 voice Intake Agent** is a third product that feeds Limbic Access. The medical-device certification belongs to *Access*; the blinded clinical evidence belongs to the *Layer*. They are related but separate, and it would be wrong to credit one system with both. [sourced — limbic.ai; fiercehealthcare 2025; Nature 2023]

---

### Which AI techniques they actually use — in plain terms

**Building their own foundation model — NOT done.** This is the most expensive, most talent-hungry thing in AI (tens to hundreds of millions of dollars, frontier-lab researchers). Limbic deliberately skips it and treats the base model as a swappable commodity part — the same Layer runs over all four vendors' models. [sourced]

**Fine-tuning — YES, but the cheap kind.** They adapt Meta's Llama 3 using **LoRA** — a low-cost technique that tweaks a small bolt-on set of parameters while leaving the giant model frozen. This is economy-class fine-tuning: a few GPUs and days, not a data center and months. They also train roughly a dozen small in-house classifiers (below). *Difficulty: low-to-moderate, commodity skill.* [sourced]

**The "safety net" classifiers — YES, and this is the core product.** Two-sided. On the way *in*, three small models screen the patient's message: a crisis/risk detector (trained on 2,626 examples, accuracy score F1≈0.69), an 18-category sensitive-topics detector (284 examples, F1≈0.63), and a jailbreak-attempt detector (546 examples, F1≈0.84). On the way *out*, a model checks whether the AI's draft reply is harmful or breaks medical-device rules (1,400 examples, F1≈0.73), plus clinical-quality gates (treatment-adherence, ~26,000 examples, F1≈0.59; recovery-prediction, ~3,400, F1≈0.61). A reply is released only if it clears both safety and quality bars; otherwise it's regenerated. *Honest read for a non-technical reader: an F1 score around 0.6–0.8 is "decent but clearly imperfect" — normal for messy clinical text, but it means this is a statistical safety net, not a guarantee. The crisis detector at ~0.69 will miss some real cases by design.* [sourced]

**Crisis handling — YES (it's that input risk detector).** On a positive hit, the system routes the patient to a human or crisis resources instead of letting the AI answer, and alerts clinical staff in the background. Exact thresholds, timing, and who gets notified are **undisclosed**. [sourced for the mechanism; thresholds — not found; fiercehealthcare 2025]

**Steering the conversation — a hand-built "state machine," not fancy AI.** The Layer walks each session through six named stages (agenda setting → information collection → formulation → intervention selection → intervention delivery → wrap-up), with a 16-state model (11,371 examples, F1≈0.78) inferring the patient's cognitive/emotional state to pick the right next step. This is ordinary software logic orchestrating several prompted AI agents — the hard part is **clinical correctness of the transitions**, not the code. [sourced]

**Keeping the AI grounded in approved material (RAG) — YES.** A searchable database of **481 clinically validated CBT documents** (~59,000 words) is queried two ways: a guided mode where the system *deterministically* injects the correct protocol (e.g., detects low motivation → inserts "behavioural activation"), and a standard mode when a patient asks for information. The tooling is off-the-shelf; the value is the curated 481-document corpus, not the search tech. [sourced]

**Grading therapy quality at scale (LLM-as-judge) — YES.** They use GPT-4o, shown one good and one bad example transcript, to score sessions on a standard clinical scale (CTRS). That automated grader agreed with human experts at a *moderate* level (ICC≈0.65). The credible part is that they **validated the judge against real clinicians** rather than trusting it blindly. [sourced]

**Clinical evidence — YES, and this is the genuinely rare, expensive part.** A randomized, blinded study (227 analyzed participants) scored by clinicians, plus a real-world analysis of **19,674 live transcripts from ~8,920 users**, published in Nature Medicine. This is clinical-trial engineering — biostatistics, blinding, expert raters — not ML engineering, and very few AI startups do it. *Note on the rater count: the study involved 28 mental-health professionals total, but split into 6 delivering therapy and 22 rating transcripts — so the rater consortium is **22, not 28**.* *Also: the "AI outperforms therapists" headline is PR framing. The measured result is that the AI's scores fell in the range of expert therapists, with ~74% of AI sessions scoring above the top-decile human session — strong, but the "outperforms" gloss is the press release, not the paper.* [sourced — Nature Medicine 2026; businesswire PR]

**Prompt orchestration — YES, but credit the right thing.** They use **DSPy**, an open-source framework that auto-tunes prompt examples, alongside deterministic decision trees built from the CBT manual and clinician consensus. DSPy itself is commodity tooling. The hard, hard-to-copy work is the **clinical encoding** poured into those decision trees and state models — not the prompt framework. [sourced]

**Voice — YES, recent, and almost certainly assembled, not built.** A 2025 voice agent answers overflow/after-hours calls 24/7 and hands off to text intake. No speech vendor, model, or latency is disclosed — it is **very likely a third-party speech stack** wired into the existing pipeline. [sourced for existence; the stack itself — not found / inference]

**What's NOT in the published recipe:** no pre-training, no continued pre-training on a medical corpus, and — notably — **no RLHF or reinforcement learning**. Frontier labs spend heavily on RLHF to align a model's behavior from the inside. Limbic instead relies on its surrounding control system and the output checker. A useful caution for non-technical readers: an output filter and RLHF are **not the same thing** — RLHF shapes how the model thinks; a filter just rejects bad answers after the fact. Limbic's approach is cheaper and more inspectable, but it is a *different* mechanism, not a like-for-like substitute. [inference, high confidence — absent from a detailed methods paper]

---

### What's genuinely hard vs. commodity

**Commodity (a strong applied-ML team can do all of this):** calling a vendor LLM, training text classifiers, RAG with off-the-shelf embeddings, LoRA fine-tuning, DSPy prompt tuning, plugging in a voice vendor. None of it is frontier research.

**Genuinely hard (the real moat):**
- **Clinical correctness of the orchestration** — encoding CBT into a deterministic expert system plus a 16-state inference model that an accredited clinician will sign off on. This needs scarce clinician-ML hybrid talent, not just engineers.
- **Regulated medical-device engineering** — the Class IIa UKCA mark (held by Limbic *Access*), and ISO 14971 / IEC 62304 / ISO 13485 quality systems. Slow, expensive, and beyond most AI startups.
- **Blinded, peer-reviewed clinical evidence** — getting RCT-grade results into Nature Medicine.
- **The outcome-linked deployment dataset** — recovery-labeled regulated patient conversations. A competitor can copy the paper, not the data.

**Honest synthesis:** Limbic is a **wrapper** — but "just a wrapper" understates it, the way "just software" understates a regulated medical device. Each ML piece is moderate-difficulty assembly of commodity parts. The difficulty (a defensible **4/5**, though this is the author's judgment, not a sourced fact) comes from making all of it hold up *simultaneously* under safety-critical, regulatory, and blinded-clinical-evidence constraints — the exact combination most competitors cannot assemble. [inference, high confidence]

---

### Notable unknowns
- Cloud provider, languages, backend frameworks. [not found]
- Crisis-escalation thresholds, alert timing, who is notified. [not found]
- Voice speech-to-text/text-to-speech vendor, model, latency. [not found]
- Per-conversation compute cost / unit economics — the "millisecond latency" and cost claims are a **vendor characterization**, not an independently measured benchmark. [not found / company claim]

**Engineering moat:** Not the AI — the moat is the regulated, clinically-validated control system and recovery-labeled patient data wrapped around a commodity model; copyable in pieces, very hard to assemble all at once.

**Sources:** Nature Medicine 2026 (s41591-026-04278-w) and its bhnet.org republication; the Nov 2024 preprint (doi 10.31234/osf.io/9d7tp); limbic.ai; businesswire (2026-03-12, PR); fiercehealthcare (2025, voice agent); Nature 2023 (s41591-023-02766-x, Limbic Access triage).


## Jimini Health (Sage)

**The one-sentence version:** Jimini did not build its own AI brain. It rented one (an unnamed top-tier large language model from another company) and wrapped it in an unusually thick layer of safety, evaluation, and clinical-workflow machinery. The hard, defensible work is in that wrapper, not in the brain.

Below, each core AI technique, whether Jimini actually uses it, and what it takes in their case. Every claim is labeled.

### What they clearly DO use

**1. Building on a third-party frontier model (the "rented brain").**
The conversation patients have with Sage runs on a frontier LLM made by someone else (think the kind of model behind ChatGPT or Claude). Jimini has never said which provider, and the absence is genuinely confirmed: StatNews and every press release name no provider. [inference; provider name verified absent — statnews 2026-03-31] This is the single biggest reason the difficulty is "high but not extreme": the most expensive, talent-hungry task in all of AI, training a foundation model from scratch, is something Jimini skips entirely.
- *Difficulty:* moderate. Buying the model is an API call, but wiring a frontier model into a regulated clinical workflow, prompt-engineering it, and wrapping it in safety controls is real work, not a one-liner. *Cost:* usage fees, not the hundreds of millions a base model costs. *Talent:* applied engineers, but no foundation-model researchers. *Data:* none of their own for the base model.

**2. Orchestration: many small models, not one big prompt.**
An investor who backed them describes Sage as *"not a thin wrapper on a foundation model"*; it is, in their words, *"a system of coordinated models operating within a structured clinical workflow layer."* [sourced — townhallventures.com 2026] Separately, company/press material frames it as an orchestrated system of specialized models. (Note: these are two distinct passages, not one quote.) In plain terms: instead of one AI doing everything, Sage is a team of AIs, one for talking, others watching for danger, others grading the output, coordinated inside a clinical workflow. This is genuine engineering, but it is *assembly and plumbing* of known parts, not new science.
- *Difficulty:* medium. *Talent:* good applied/systems ML engineers. *Cost:* moderate.

**3. Safety classifiers: the genuinely hard, proprietary part.**
This is where Jimini puts its real effort. Sage runs multiple always-on, high-risk classifiers, small AI watchdogs that read every message in parallel (side-by-side, so they don't slow the chat) and flag danger. [sourced — multiple sources] The watch domains corroborated by accessible secondary coverage (prnewswire, athletechnews) are: **suicidal ideation, psychotic symptoms, child/vulnerable-adult endangerment, and medication noncompliance.** [sourced] A fifth domain, "harm to others," appears in the full white paper as described, but is **not corroborated by any accessible secondary source** and no accessible source states an exact classifier count (e.g., "more than ten"); treat both the harm-to-others domain and any specific number as asserted in the white paper, not independently verifiable. [contested]
  - How they're built (asserted in white paper, not independently verifiable): Jimini used the frontier model to *generate* thousands of fake-but-realistic therapy conversations (some dangerous, some not), fine-tuned the classifiers on those, then had PhD clinicians hand-grade a separate set, blind to what the AI guessed, to create a gold-standard answer key. [asserted in white paper — 2025-07-08]
  - *Difficulty:* high. Getting suicide/psychosis detection reliable without either missing real danger or over-reacting to every sad sentence ("over-refusal") is the core technical bar, far above a normal chatbot. *Talent:* ML engineers who understand clinical risk. *Data:* mostly synthetic for training plus a clinician-labeled eval set of undisclosed size (scale unknown, not found).

**4. LLM-as-judge and clinical evals.**
Sage is described as using dedicated AI judges, models trained to evaluate outputs for safety, tone, and alignment with clinical standards. [asserted in white paper — 2025-07-08] These don't replace humans; they triage which conversations a clinician should review first. Combined with the clinician-annotated gold-standard set, this is a real, above-average evaluation pipeline, though the judge mechanism itself is not independently verifiable outside the white paper.
- *Difficulty:* medium-high. *Talent:* eval/safety specialists. *Cost:* moderate but ongoing.

**5. Crisis detection and escalation (guardrails).**
When a watchdog fires, Sage is described as following a path of detect, ask a clarifying question (and alert the clinician), then escalate if risk is confirmed or not denied, attaching a plain-language explanation of which classifier fired and why so a clinician can audit it. [asserted in white paper — 2025-07-08] Consumer-facing crises are reportedly pointed to 988 (asserted in white paper, not independently verifiable). The exact response time / SLA is unknown, not found.

**6. Memory / longitudinal context.**
Sage *"maintains longitudinal context"*; it remembers the patient across visits and feeds structured summaries back to the clinician (including note "scribing" and tracking of standard depression/anxiety scores, PHQ-9 and GAD-7). [sourced — townhallventures.com 2026] Whether this is true retrieval (RAG) over records or simpler context-passing is not disclosed (unknown, not found).

**7. Staged, evaluation-driven deployment plus a real clinic as QA.**
Jimini runs new model versions on real patients in its own multi-state clinic, with employed clinicians, before shipping to partners, then rolls out under tiered oversight. [sourced — hitconsultant 2026-03-31] The specific cadence sometimes cited (24–48h full review, then sampled, then flag-triggered) is asserted in the white paper but not given by any accessible secondary source; treat the timings as unverified. [asserted in white paper] Owning a clinic purely as a software QA environment is an unusual and costly operational build, and a real moat.

### What they do NOT do (or don't disclose)

- **Pre-training / continued pre-training / Mixture-of-Experts:** not used; they rent the base model. [inference]
- **RLHF / RLAIF / DPO / reward modeling:** not named. They describe "Deliberate Safety Alignment" to therapist-defined priorities, but the formal training techniques behind it are not stated (unknown, not found). [verified absence]
- **Voice / multimodal:** Jimini's own first-party app listings describe Sage as offering *"always-on, multimodal support through conversation,"* so first-party material does claim multimodal. However, an explicit *voice* mode is not confirmed in first-party material and shows up only in loose secondary summaries. Framing: first-party claims multimodal; explicit voice remains unconfirmed. [contested]
- **Serving/latency internals, model routing, EHR integration standard (FHIR?), and training-data scale:** all undisclosed (unknown, not found). [verified absence]

### Hard vs. commodity: the honest split

**Commodity (assembly):** the conversational core (rented model), the basic chat loop, and standard outcome-score tracking.

**Genuinely hard (their moat):** reliable suicide/psychosis detection that avoids both misses and over-reaction; the clinician-annotated gold-standard eval set; the LLM-as-judge plus staged deployment regime; auditable per-decision explanations; and the operational feat of running a live clinic as a pre-release test bed wired into clinician workflows.

**One efficacy caveat worth flagging:** a Town Hall Ventures investor post claims Sage patients saw *~36% reduction in depression symptoms with half the in-person sessions.* [contested — townhallventures.com 2026] This is an unaudited investor/marketing figure, not a published trial, and it sits awkwardly against the otherwise-consistent finding that Jimini has **no published efficacy data and no completed RCT.** Treat it as a claim, not evidence.

**Bottom line:** Jimini is a high-quality wrapper company. The intelligence is bought; the safety, evaluation, orchestration, and clinical-integration engineering around it is built in-house and is the genuinely difficult, defensible work, held to a patient-safety bar far higher than a normal chatbot, but stopping well short of frontier ML research.

**Engineering moat:** Real but bounded: a safety-and-clinical-integration wrapper that is hard to copy and held to a high patient-safety bar, around a rented brain they did not, and do not, train.

### Sources
- https://jiminihealth.com/blog/the-new-hippocratic-code-an-llm-native-safety-framework-for-patient-facing-ai-in-mental-health
- https://www.townhallventures.com/insights/why-we-backed-jimini-health
- https://hitconsultant.net/2026/03/31/jimini-health-clinician-supervised-behavioral-health-ai/
- https://www.statnews.com/2026/03/31/jimini-health-raises-funding-ai-chatbot-sage-mental-health/
- https://jiminihealth.com/how-it-works
- https://jiminihealth.com/company
- https://www.prnewswire.com/news-releases/jimini-health-releases-technical-blueprint-for-safe-patient-facing-ai--adds-deepmind-and-yale-leaders-to-advisory-board-302500354.html
- https://psymedventures.substack.com/p/ai-and-the-future-of-therapy-with
- https://www.globenewswire.com/news-release/2024/11/19/2983540/0/en/Jimini-Health-Launches-with-8M-in-Funding-to-Transform-Mental-Health-with-Responsible-AI-Supported-Therapy.html


## ieso (Velora)

The simplest way to picture Velora is not as "a new AI brain that ieso built from scratch," but as **a tightly supervised AI therapy program, wrapped in a safety cage, and taught from a roughly 25-year library of real therapy.** The clever, hard-to-copy parts live almost entirely in the *cage* and the *library* — not in the brain itself. ieso publishes very little about its internal technology, so several points below are clearly-labeled inferences, and where something simply isn't disclosed, I say so.

### The big picture

ieso presents Velora as a generative AI care agent that "chats" with the user, but fenced inside a clinician-designed CBT/ACT curriculum delivered as **time-limited modules** — not an open-ended chatbot. The stronger phrasing you'll see quoted ("constrained generative AI architecture governed by a multi-agent safety system") comes from ieso's **safety preprint**, not its marketing page; the public Velora page uses milder language ("in-program guardrails to prevent misuse," "time-limited modules," "Care Journey," "aligned with NIST standards"). *[sourced — ieso.ai/velora for the milder phrasing; OSF preprint 10.31234/osf.io/8kvm6 for the stronger framing. The exact safety-test figures circulating from the preprint could not be independently verified here.]*

### What they actually do — technique by technique

**1. They rent a foundation model — commodity, and undisclosed.** The base model is **never named** in any public source (I searched specifically for GPT/Claude/Llama and found nothing). It is implausible that a company this size — about **177 employees** per public listings, not the much smaller figure sometimes assumed — trained a frontier model from scratch; that would cost on the order of tens of millions of dollars and require a research org they don't appear to have. So they almost certainly **rent a commercial LLM and adapt it.** This is the "wrapper" part. *Difficulty for them: low. Cost: usage/API fees. [base model: unknown — not found; "they use someone else's model": inference; tens-of-millions figure: illustrative, not sourced]*

**2. Adapting that model to their data — moderate, and the real differentiator.** ieso markets Velora as "trained on 750k+ hours… not a generic LLM." The likely mechanism is **fine-tuning and/or retrieval (RAG)** that conditions the rented model on their outcomes-indexed therapy data, plus hand-built CBT/ACT scaffolding. The valuable input here is the **data**, not the method — fine-tuning and RAG are now standard. *Difficulty: moderate. Talent: applied NLP engineers. Cost: modest compute plus heavy clinical-curation time. [corpus and "not a generic LLM": sourced; that it's fine-tuning/RAG specifically: inference — ieso does not confirm]*

**3. Boxing the model into a clinician-authored program — moderate, deliberate design.** Rather than free chat, the AI is steered through **clinician-curated, time-limited modules**. This descends directly from ieso's *earlier* product, which was an explicitly **tree-based dialogue system** delivering clinician-prewritten responses with "controlled use of natural language generation." Velora loosens that into generative output but keeps it fenced. Turning a chatty model into a bounded clinical curriculum is genuine engineering. *Difficulty: moderate. [sourced — JMIR e69351; Hemingway Report; ieso.ai/velora]*

**4. Guardrails and crisis/risk detection — genuinely hard, because the domain is high-risk.** Velora has in-program guardrails and continuous monitoring. In a tool talking to people with moderate-to-severe anxiety or depression, **missing a suicide or self-harm signal is a catastrophic failure** — so this layer is safety-critical, not cosmetic. The difficulty here comes from the *consequences of being wrong*, not from algorithmic novelty. The exact escalation protocol (hotline routing, human handoff) is **not disclosed**; the preprint only says flagged sessions were "handled according to escalation policies." *[sourced for the existence of guardrails; the term "risk detectors" comes from the preprint, not the marketing page; escalation specifics: not found]*

**5. A multi-agent safety system with synthetic red-teaming — their headline engineering.** The safety preprint describes **synthetic high-risk scenario testing, automated harm detection, and clinician oversight.** In plain terms: they generate **fake high-risk patients** (e.g., someone expressing suicidal thoughts), run the AI against them at scale, have a **separate automated checker** flag any unsafe reply, and have clinicians audit. They also reference **"clinician-trained supervision agents"** watching both user input and AI output. *Difficulty: high. [sourced — OSF preprint. Note: the often-quoted scale figures (e.g., ~43,000 simulated responses, ~12,000 real-world responses, ~0.01% harmful-output rate, >50% responders) are **reported but could not be independently verified here**; the preprint's existence and its "zero AI-induced safety incidents" framing are corroborated by secondary sources.]*
- **Important nuance:** *how* the fake patients are generated, and *whether* the harm-detector is an AI grading AI ("LLM-as-judge"), a trained classifier, or human raters, is **not disclosed.** By analogy to a **non-ieso** tool — Rush University's "ASTRA" monitor, which uses a prompted model (GPT-5-Chat) as a binary risk classifier — an LLM-as-judge design is plausible, but ieso does not confirm it. *[inference; ASTRA comparison sourced — JMIR e91367, a non-ieso paper]*

**6. Clinical evaluation treated as engineering — strong, and a real differentiator.** ieso treats trials and safety studies as a **core deliverable.** Important honest caveat: the *peer-reviewed effectiveness study* (JMIR e69351) tested the **older tree-based product**, not generative Velora — a distinction ieso draws correctly. The generative-Velora evidence is the **safety preprint**, which is newer and not yet peer-reviewed. Running this rigor — IRB approvals, biostatistics, NIST-aligned safety testing — is unusual and costly. *Difficulty: high. [sourced — JMIR e69351; OSF preprint; ieso.ai/velora for NIST]*

**7. De-identification and data pipelines — mature, proven.** "De-identification, PII masking, and explicit consent," plus **decades of running a live online-CBT service at scale**, imply genuinely mature transcript-processing and outcomes-linkage pipelines. *Difficulty: moderate, but proven. [sourced]*

### What they likely DON'T do

- **Pre-training a model from scratch:** almost certainly not — they adapt a rented one. *[inference]*
- **RLHF / preference tuning (DPO, etc.):** no public evidence either way. *[unknown — not found]*
- **Voice:** Velora is **text-based**; no voice modality found. *[sourced]*
- **Serving / latency / infra:** **unknown — not found**; no cloud provider or latency details are public. (Caution: an "Azure / Azure OpenAI" detail that surfaces in searches belongs to the **non-ieso ASTRA monitor (Rush University, JMIR e91367)** — do not attribute it to ieso.) *[unknown; de-confliction sourced]*
- **Cross-session memory:** plausible given the "Care Journey" framing, but the mechanism is **not disclosed.** *[unknown]*

### Genuinely hard vs. commodity

- **Commodity:** the generative core — rent an LLM, fine-tune/RAG it, prompt-orchestrate into modules. Many teams can now assemble this.
- **Genuinely hard:** (a) the **~25-year, outcomes-indexed clinical corpus** — a *data* achievement, not a coding one; (b) **safety-critical guardrails and crisis detection**, where mistakes can cost lives; (c) the **multi-agent safety and simulation harness**, plus treating **clinical evaluation** as core engineering; (d) shipping all of it as a **multi-tenant, white-label API** for regulated healthcare buyers. One honest qualifier: the corpus is a strong moat, but "irreplaceable" is ieso's own framing — a rival with NHS/IAPT-scale therapy data could in principle build something comparable.

**Engineering moat:** A commodity model in a borrowed brain — but the cage around it (safety regime) and the library that taught it (25 years of outcomes-linked therapy data + clinical evidence) are the hard-to-copy assets, which is exactly what a typical "it's just a wrapper" critique assumes wrappers lack.

### Sources
- https://www.ieso.ai/velora
- https://www.ieso.ai/about-us
- https://www.thehemingwayreport.com/articles/73-why-ieso-is-going-api-first
- https://www.jmir.org/2025/1/e69351 (older tree-based product)
- https://sciety.org/articles/activity/10.31234/osf.io/8kvm6_v1 (generative-Velora safety preprint; figures not independently verified)
- https://mental.jmir.org/2026/1/e91367 (ASTRA / Rush University — non-ieso analogy)
- https://himalayas.app/companies/ieso-digital-health/tech-stack (empty tech-stack profile)


## Wysa

**The one-sentence version:** Wysa does not build its own AI brain. It rents a powerful general-purpose AI — a large language model, or "LLM" — and wraps it in a tightly controlled, clinician-written rulebook that decides what the app is allowed to say. The clever engineering is the cage around the AI, not the AI itself. *(sourced — Aggarwal Playbook, 2026-06-24)*

### Which AI does it use?

Wysa's CEO, in the company's public "Responsible AI Playbook," refers to "data sent to external servers like OpenAI." So OpenAI is named — but illustratively, as an example, not as a formal confirmation that OpenAI is Wysa's sole or current provider. The honest read: the CEO names OpenAI in passing, but Wysa has never formally committed to it as the exclusive engine. *(contested — Aggarwal Playbook, 2026-06-24)*

### What Wysa deliberately does NOT do

These omissions are the whole strategy, so they matter:

- **It does not train its own foundation model.** Building an AI brain from scratch is the single most expensive, talent-heavy thing in the field — generally GPU clusters, frontier researchers, and very large budgets. Wysa has deliberately avoided all of it. *(those cost figures are general industry color, not Wysa-specific; the avoidance itself is well-supported — inference from disclosed architecture)*
- **It does not do the deep "alignment" training** (techniques known as RLHF/DPO) that shapes a raw model's behavior — it lets the third-party provider handle that. *(inference from absence of disclosure)*
- **No AI voice.** The chatbot is text only; there is no speech synthesis in the bot. Audio/video exists only for *human* coach sessions, and only in select regions (US and India). *(sourced)* (One detail — that these run "over a third-party interface" — could not be corroborated and should be treated as unverified.) *(speculation)*

### What Wysa actually does — and how hard each piece is

**1. A clinician-written rule engine — the load-bearing piece, but not AI.**
Wysa's CEO is explicit: *"Gen AI does not determine what Wysa will say. Wysa adheres to a strict protocol and always says things that achieve the same purpose."* The therapeutic content is written and approved by clinicians and is essentially fixed. *(sourced — Aggarwal Playbook, 2026-06-24)*
As *software*, building this kind of scripted dialogue engine is commodity work. The expensive, hard part is the *clinical authoring* — writing hundreds of validated therapy flows that map to medical guidelines. That's psychologist labor, not scarce AI-engineering talent. **Difficulty: low as engineering, high as clinical content.**

**2. Reading what the user means — 120+ in-house classifiers (their real ML).**
Wysa runs "over 120+ natural-language-understanding (NLU) models" that interpret a user's text — detecting intent and emotion — to pick which scripted flow to enter. *(sourced — EMHIC, 2026-06-24)* This is genuine in-house machine learning, but it's mature, well-trodden work, not frontier research. The real advantage here is the *data*: Wysa's 500M+ conversations and 5M+ users give it a large, domain-specific training corpus most rivals lack. *(sourced — EMHIC)* **Difficulty: medium — and the moat is the data, not the method.**

**3. Caging the LLM — the most interesting engineering.**
Newer Wysa does use an LLM, but boxed in: across "test samples of thousands of responses, Wysa's responses remain predictable and repeatable." *(sourced — Aggarwal Playbook, 2026-06-24)* In plain terms, they let the AI add conversational fluency, but the rule engine keeps it on-script. Making a fundamentally unpredictable AI behave *repeatably and auditably* is real engineering — prompt design, output validation, and fallback to fixed scripts. **Difficulty: medium — this is the hard part of being a *responsible* wrapper, and Wysa appears to do it more rigorously than most.**

**4. Crisis detection — safety-critical, and pointedly NOT generative.**
Wysa scans free text in real time for signs of suicidal thoughts, self-harm, or abuse, and surfaces an always-visible crisis path. Crucially, the LLM is kept *out* of this entirely — crisis handling is deterministic and scripted, because a wrong move here is catastrophic. *(sourced — Aggarwal Playbook, 2026-06-24)*
A widely cited "82%" figure needs care. In a Wysa *vendor self-study* (about 19,000 users across 99 countries), 5.2% of users reported a crisis in a year; of those, 82% were AI-flagged and *confirmed by the user*, while the other 18% raised the alarm themselves. So 82% is a *usage-pathway split*, not the classifier's true accuracy or miss-rate — and it has no independent validation. *(sourced — Wysa/BusinessWire study, 2024-04-15)* **Difficulty: medium-high, because the cost of an error is high, not because the algorithm is exotic.**

**5. Their own safety benchmark — SAFE-LMH.**
In October 2024 Wysa launched SAFE-LMH, a test suite of 500–800 mental-health questions across **20 languages** — including Chinese, Arabic, Japanese, and 10 Indic languages — scoring AI models on whether they correctly *refuse* harmful prompts and on *response quality* (preventive / empathetic / harmful). *(sourced — Wysa blog + BusinessWire, 2024-10-10)* The multilingual reach, especially into low-resource Indic languages, is genuinely hard and differentiating. A full results report naming specific models is not public. *(sourced — only the launch is published)* **Difficulty: medium-high; the linguistic and clinical breadth is the hard part.**

**6. Disciplined compliance testing.**
Every Gen AI release passes a "53-point check," with repeatability and periodic testing across datasets. *(sourced — Aggarwal Playbook, 2026-06-24)* This is safety regression-testing that most consumer chatbots simply skip.

**7. Light training of their OWN small models — not the big LLM.**
Wysa uses "some anonymized messages to train Wysa's AI" (its own classifiers), while the third-party LLM runs under **zero data retention** and is *not* trained on user data. *(sourced — Wysa FAQ/privacy, 2026-06-24)* Calling this "fine-tuning" is a reasonable label, though Wysa states it more generically.

**8. Memory / retrieval.** Some personalization exists, but a long-term memory or retrieval architecture is not publicly described. *(unknown — not found)*

### Genuinely hard vs. commodity

- **Commodity:** the rule/dialogue engine, calling a third-party LLM, basic intent classification, and the app itself.
- **Genuinely hard (for Wysa):** (1) forcing an unpredictable LLM into repeatable, auditable behavior; (2) crisis detection with near-zero tolerance for misses; (3) the multilingual SAFE-LMH benchmark; and (4) the surrounding clinical-safety governance and regulated integrations. The difficulty lives in *safety, evaluation, compliance, and integration* — not in model research.

**Bottom line:** Wysa is a high-quality wrapper. Its engineering bet was to treat the LLM as a dangerous-but-useful component to be constrained, and to spend its scarce talent on clinical safety, evaluation, and regulatory integration rather than on training models. That's a deliberate, defensible strategy — and a judgment call, not a measured score, puts the real engineering difficulty around 3 out of 5, below the 4–5 of teams doing frontier model work.

**Engineering moat:** Real but narrow — the moat is clinical-safety governance plus a hard-to-copy 500M-conversation dataset, not proprietary AI; the model itself is rented.

**Sources:**
- Jo Aggarwal, "Responsible (Generative) AI for Mental Health: A Playbook," LinkedIn
- EMHIC profile — "Wysa: Transforming Mental Health Through AI-Driven Support"
- Wysa blog & BusinessWire — SAFE-LMH multilingual AI safety initiative (Oct 10, 2024)
- BusinessWire — "AI Detects 82% of Mental Health App Users in Crisis" (Apr 15, 2024)
- Wysa FAQ and legal.wysa.io generative-AI privacy/FAQ


## Lyra Health

**Bottom line:** Lyra Health is a mental-health benefits company that appears to have put a carefully fenced-in AI "coach" on top of someone else's large language model. The most probable reading of the public evidence is that they did not build the underlying AI "brain" — but this is an inference, not a confirmed fact: Lyra has never publicly named its model vendor. Their real engineering work is the *fence* around the model — keeping the bot in a safe lane, catching crises, handing off to human therapists, and meeting hospital-grade privacy rules. That is competent, useful engineering. On the public evidence it looks like assembly-plus-safety-plus-compliance rather than the from-scratch AI research that OpenAI or Anthropic do — though, again, the "wrapper" framing rests on the absence of any disclosure to the contrary, not on proof.

### What they almost certainly DON'T do

- **Pre-training / continued pre-training** (building or further-training a base AI from raw text): no evidence, and nothing about their size or hiring suggests it. The most likely picture is that they consume a third-party frontier model. *[inference — vendor never named]*
- **Reward modeling, RLHF/RLAIF, DPO** (advanced techniques to shape an AI's behavior with large amounts of human or AI feedback): not disclosed, no evidence. *[unknown — not found]*
- **Mixture-of-Experts / custom model routing** (frontier-lab tricks for building and steering very large models): not applicable to a wrapper. *[inference]*

### What they DO appear to do — and how hard each is for them

The difficulty ratings below are the author's analyst estimates. Because Lyra has disclosed almost no mechanism, these are judgments about how hard this *class* of work is, not measurements of Lyra's actual implementation.

- **Prompt design + orchestration (the core of the wrapper).** They wire a frontier model into a "Guide" that is only meant to handle mild-to-moderate problems — burnout, sleep, stress. Keeping a chatbot reliably *inside* that lane, so it refuses to drift into diagnosing or treating serious conditions, is the central trick. The tools to do this are commodity; getting the behavior reliably safe is genuinely fiddly. *Difficulty: moderate (author's estimate).* *[sourced]*

- **Guardrails + crisis detection (likely their hardest real problem).** A "risk-flagging system" is meant to spot a user in crisis and immediately route them to a live 24/7 human team. This is the part with near-zero tolerance for misses — a missed suicidal user is catastrophic — which is why the author judges it the hardest piece. **But Lyra discloses no mechanism, no training data, no accuracy numbers, and has published no validation.** For contrast on how exacting this kind of system can be: Verily (an Alphabet life-sciences company — a benchmark publisher and comparison point, *not* a direct competitor in Lyra's employer-benefits market) published a comparable crisis guardrail in *npj Digital Medicine*, a Nature Portfolio journal, on April 3, 2026. It reported about 99% sensitivity — but that figure was measured against roughly 1,800 *simulated*, clinician-labeled messages (the Verily Mental Health Crisis Dataset v1.0), not organically collected real-world crises. So it illustrates the kind of bar serious teams aim at, while remaining a benchmark on synthetic data rather than a settled industry standard. Against even that yardstick, Lyra has shown nothing. *Difficulty: high if done well; Lyra's quality currently unverifiable.* *[sourced / contested]*

- **Clinical evals + LLM-as-judge.** Lyra says it uses "predefined benchmarks" for safety, appropriateness, and inclusiveness, plus bias testing — language that implies an automated evaluation pipeline, very plausibly an "AI grading AI" setup. But no benchmark names, datasets, or scores are public. *Difficulty: moderate-to-high (author's estimate); existence asserted, rigor unverifiable.* *[sourced]*

- **Serving / latency + their own ML infrastructure.** This is where fresh evidence sharpens the picture. Per the author's reading of Lyra's job postings, they describe building infrastructure to "train, evaluate, deploy, perform inference and monitor ML models" and to "build and deploy generative AI services," on PyTorch, Kubernetes, AWS, and MLflow/Kubeflow/SageMaker. If accurate, they are not *only* calling an API — they run a real in-house ML platform, partly to support older classic-ML systems like provider matching and risk prediction. *Difficulty: moderate; standard 2026 MLOps (author's gloss).* *[sourced per author]*

- **RAG / memory.** Lyra's site says its AI is "trained on high-quality data tied to proven clinical outcomes and is continuously refined." This phrasing is ambiguous: it could mean fine-tuning, but more likely means *grounding* the model in Lyra's clinical content and skills (retrieval) rather than retraining it. **Which one they do is not disclosed** — a key gap. *[unknown — not found]*

- **Data pipelines (a genuine strength).** Per the author's reading of a Fivetran case study and job postings: a Snowflake lakehouse in a private cloud, with Fivetran pulling from 600+ sources into Iceberg/Delta tables, all under HIPAA isolation, with in-house data labeling. This is solid, mainstream data engineering that feeds both the classic-ML and generative sides. *Difficulty: moderate; well-executed.* *[sourced per author]*

- **Voice.** The 2026 general-availability version adds a voice mode, but no detail on the speech stack is given. *[unknown — not found]*

- **Compliance as engineering.** HIPAA, HITRUST, ISO 27001, VPC-isolated patient data, and multi-country data residency. Non-glamorous but real, costly work that raises the floor on overall difficulty. *[sourced]*

### Where the difficulty really sits

In the author's assessment, the hard and scarce work is **safety, evaluation, and clinical validation**, plus the **compliance** scaffolding — not model R&D. (This is an analyst judgment: because Lyra discloses no mechanism, the relative difficulty cannot be confirmed against their actual system.) Lyra appears to have deliberately sidestepped the hardest AI problem — autonomously treating serious mental illness — by narrowing scope and keeping humans in the loop. Their best asset is **clinical-ML bridge talent** (e.g., Anita Lungu, who holds a PhD in computer science from Duke and a PhD in clinical psychology from the University of Washington, and now leads Lyra's clinical AI) plus a decade of labeled outcomes data. The claim that 20M members' records form an LLM "training corpus," however, is unproven — and Lyra does not actually make that claim. The senior AI organization was still being hired into as of mid-2026 (an open VP of Data and AI).

**One trap worth flagging:** a June 18, 2026 "Lyra Cloud Services × Anthropic/Claude" announcement is a *different company* — Lyra Technology Group, an Evergreen-backed AWS reseller — not Lyra Health. It does **not** reveal Lyra Health's model vendor, which is **not publicly disclosed**.

### Verdict

A capable, safety-first **wrapper**, most likely built on a third-party frontier model, by a company with real clinical and data-engineering muscle that runs its own ML serving infrastructure rather than a thin API call. The "wrapper" label and the unnamed vendor are inferences from non-disclosure, not confirmed facts. And the two things that would prove the product *sophisticated* rather than merely *adequate* — the crisis classifier's real accuracy and the clinical-eval results — are entirely undisclosed, so the genuinely hard parts cannot be independently verified.

**Engineering moat:** Real moat in clinical data and compliance engineering, but the load-bearing AI safety work is undisclosed and unverified — so the moat is plausible, not proven.

### Sources
- https://www.lyrahealth.com/blog/introducing-lyra-ai/
- https://www.lyrahealth.com/our-approach/ai/
- https://www.lyrahealth.com/blog/the-polaris-principles/
- https://www.lyrahealth.com/announcement/lyra-health-introduces-first-clinical-grade-ai-for-mental-health/
- https://www.businesswire.com/news/home/20260505129157/en/Lyra-Health-Scales-Clinically-Vetted-AI-Guide-to-Members-Globally
- https://www.statnews.com/2025/10/14/lyra-health-ai-chatbot-mental-health/
- https://www.fivetran.com/blog/lyra-health-leads-mental-health-innovation-with-data-lakes-ai
- https://careers.lyrahealth.com/job/remote/sr-ai-ml-infrastructure-engineer/43250/68674947760
- https://builtin.com/job/sr-aiml-engineer-platform/3811763
- https://jobs.lever.co/lyrahealth/09c26902-b358-4a8c-8ea1-6cf6d7867b37
- https://www.nature.com/articles/s41746-026-02579-5 (npj Digital Medicine, Nelson et al., April 3, 2026)
- https://www.businesswire.com/news/home/20260618297990/en/Lyra-Cloud-Services-Announces-Strategic-Partnership-with-Anthropic-to-Accelerate-Enterprise-AI-Adoption-on-AWS (different company)
- https://www.lyrahealth.com/announcement/lyra-health-study-finds-ai-can-reduce-mental-health-care-costs-without-sacrificing-outcomes/


## Talkspace

**The one-sentence version.** Talkspace does not build its own AI brain. It rents a powerful general-purpose model from an undisclosed vendor, then wraps it in a thick layer of clinical training data, safety systems, and human oversight. The clever, hard, and defensible part is *not* the AI model — it's everything Talkspace bolts around it. Picture a hospital that buys a standard MRI machine but writes its own protocols, alarms, and on-call escalation: the machine is commodity; the safety operation is the value.

A caution on naming before we start: Talkspace markets its product, **Tee** (launched June 2026, $19.99/mo with a 7-day trial), as "the first SAFE AI agent." That superlative is the company's own marketing wording, not an independent fact, and should be read as a claim. Internally, job postings reference an agent platform codenamed **Sentia**; it is a reasonable guess that Tee is built on the Sentia architecture, but that link is plausible, not confirmed.

### What they actually build (in plain English)

**Fine-tuning is the heart of it.** They take an existing base model and keep training it on their own therapy conversations so it "speaks therapy." The Q4 2025 earnings call says the model is "trained and fine-tuned on Talkspace's massive mental health data set." [sourced]
- *How hard:* Medium. Fine-tuning is a near-commodity skill in 2026. The hard part isn't the algorithm — it's doing it on regulated patient data without leaking private health information, and proving the result is clinically safer.
- *Cost:* Modest next to building a model from scratch — thousands to low-millions of dollars of compute, versus the hundreds of millions a foundation model costs. (Note: an earlier read that "AI is self-funded, no separate raise" is now speculative and stale — Universal Health Services agreed to acquire Talkspace for ~$835M ($5.25/share), announced 2026-03-09, expected to close Q3 2026. As of this writing the company is mid-acquisition, so any claim about future AI funding is unsupported.) [inference / contested]
- *Data scale — their real edge:* ~12 years of interactions (company-stated figures: ~140M messages, 6.2M assessments, 1.2M diagnoses, 4.3M notes), described by the company as de-identified. [sourced — company claim]

**They explicitly do NOT pre-train a foundation model.** The launch calls Tee "a safe, fine-tuned large language model." Skipping the build-from-scratch step is the single biggest cap on their cost, talent, and difficulty. [sourced]

**Memory and retrieval (RAG).** The product "remembers past conversations" for continuity, and the Senior AI Engineer spec lists "memory/retrieval systems" and "retrieval-augmented generation." Medium difficulty and commodity-ish in 2026 — except that storing and retrieving *therapy* memory under HIPAA raises the privacy bar. [sourced]

**Agent orchestration — more serious than a typical wrapper.** The job spec describes "planning modules, goal-setting algorithms, tool-use orchestration," and "multi-agent orchestration" with "low-latency decision-making." This is real agent engineering: the AI plans, calls tools, and coordinates sub-agents rather than just answering. Medium-high difficulty — keeping orchestration safe and fast in a life-safety domain is genuinely hard systems work, even with no novel ML. [sourced]

**Crisis / risk detection — the strongest, oldest, most validated piece.** A separate language classifier scans messages in real time and alerts a human therapist. It covers 10 risk categories (suicide, homicide/violence, abuse, plus seven other named risk entities). The original model (Bantilan et al., 2020, with NYU Grossman) was trained on transcripts attributed to ~1,864 patients (a figure cited to the paywalled paper and not independently confirmed), graded against human expert raters, reporting **~83% agreement vs. a human expert** and **AUC 82.78** at the sentence level — two different metrics that are often conflated. The classifier has run in production since 2019; ~32,000 members flagged. Around the June 2026 Tee launch, Talkspace says it **retrained this classifier on more recent data and now reports ~92% accuracy** — treat that 92% as a real but company-attributable, methodology-undisclosed claim for the *updated risk model* (not for Tee's therapeutic quality). [sourced — company claim]
- *How hard:* High — not because the model is fancy (the 2020 architecture is undisclosed and likely pre-transformer), but because wiring a real-time detector to live human escalation, in a domain where a miss can mean a death, is the genuinely high-stakes part.

**Guardrails + human-in-the-loop — this is the actual product.** Real-time licensed-clinician oversight and "algorithmic blockades" that force a human step-in. Specific mechanics described by the company (18+ age gate, a self-harm onboarding screen, hard "I am not a clinician" disclaimers) are company-described and only partly independently confirmed. Medium-high as safety/operations engineering; low as ML. [sourced — company-described]

**Evaluation — notably mature.** Two layers. (a) An eval-ops stack: "offline evaluation against golden datasets," trace-level analysis of model calls and tool use, real-time monitoring for behavioral drift, and human annotation. (b) With the AWS Generative AI Innovation Center, they're co-building a safety-and-quality model that *scores therapy sessions* for clinical quality and risk — an AI grading the therapists/AI (LLM-as-judge applied to clinical quality). High difficulty for the vertical: clinical eval design is where their clinical talent actually shows up, and is harder to fake than the model itself. [sourced]

**Patient-matching ML** (conventional recommendation-style ML, low novelty) and **low-latency cloud serving** (Docker/Kubernetes, AWS/GCP) round out the stack — both real but commodity. [sourced]

*Important AWS nuance:* the confirmed AWS tie is the co-built session-*scoring* model, NOT confirmation that AWS hosts or serves Tee's base model. "AWS-hosted / Bedrock base model" is a reasonable inference from the partnership but is unconfirmed. [speculation]

### Aspirational, not shipping
The job spec asks for "advanced RL, Inverse RL, or related control theory" and "simulation environments for pre-training and testing agent policies." That's research-lab ambition, but it's a *hiring wish-list* — no evidence any RL-based system ships today. No public evidence of preference-tuning (RLHF/DPO), mixture-of-experts, continued pre-training, or a custom voice stack (Talkcast audio uses an undisclosed, likely third-party text-to-speech engine). [inference / unknown]

### Genuinely hard vs. commodity

**Hard (the moat):**
1. The proprietary clinical data — 12 years of labeled, longitudinal therapy data is nearly impossible to replicate. The caveat: the company calls it de-identified, but that de-identification's robustness is contested, which somewhat dents the "clean, unassailable asset" framing.
2. The safety + escalation engineering — real-time risk detection wired to live human clinicians, validated with NYU.
3. The clinical eval discipline — golden datasets, drift monitoring, clinician-graded scoring, co-built with AWS.

**Commodity assembly:** the rented base model, the fine-tuning recipe, RAG, the agent framework, Kubernetes serving, patient-matching ML — all standard 2026 practice.

### Caveats on the marketing numbers
- The widely quoted **50% / 47% / 3x** improvement figures are company-run internal tests with no disclosed methodology, and they compare Talkspace's fine-tuned model against a *generic base model* — a self-serving baseline. Do not treat as established performance. [sourced — company claim]
- A "92% accuracy" figure is real and company-attributable, but applies to the *retrained risk classifier*, not Tee's overall quality (see above).
- No clinical trial, RCT, or peer-reviewed efficacy study exists for **Tee** itself — only for the older suicide classifier. [sourced — sourced absence]

**Net read:** a 3/5 operation. Clearly above a thin "call-the-API" wrapper because of the data, the safety integration, and a real eval/orchestration stack — but well below frontier ML research.

**Engineering moat:** Regulatory and data-driven, not algorithmic — proprietary (company-stated, de-identification contested) clinical data plus clinician-in-the-loop safety engineering, wrapped around a rented model the company did not train.

### Sources
- Talkspace Tee launch press release — investors.talkspace.com
- Talkspace Q4 2025 earnings call transcript — fool.com (2026-02-19)
- Senior AI Engineer job postings — remoterocketship.com; welcometothejungle
- Talkspace AI investment / AWS partnership — fiercehealthcare.com
- AWS Industries blog (patient matching) — aws.amazon.com/blogs/industries
- Bantilan et al. 2020, suicide-risk classifier — tandfonline.com (10.1080/10503307.2020.1781952); talkspace.com/ai-at-talkspace
- Retrained classifier ~92% accuracy — gurufocus.com; bhbusiness.com coverage
- UHS acquisition of Talkspace (~$835M, 2026-03-09) — statnews.com; uhs.com; prnewswire
- De-identification concerns — proofnews.org; captaincompliance.com; myprivacy.blog
- Digital mental-health AI overview — statnews.com (2025-12-01); inc.com


## SonderMind

**The one-sentence version:** SonderMind does not build its own AI brain. It uses an undisclosed vendor model and wraps it in three layers of its own engineering — privacy/compliance plumbing, a memory system that remembers each patient, and a clinician-sign-off workflow. The genuinely hard parts are the wrapping and the safety, not the AI itself. Importantly, the company publicly distances itself from consumer general-purpose models, stating it avoids tools "like ChatGPT and Claude" — so the rented brain is not one of the familiar consumer chatbots, but exactly which model they do use is *not found*.

Think of it like a restaurant that doesn't farm or raise its own ingredients (the AI model) but does run a serious, regulated kitchen with strict food-safety rules. The cooking technique is standard; the compliance and the plating-with-a-doctor's-approval are where the real work is.

A second thing shapes the whole picture: **SonderMind bought a lot of its non-model capability rather than building it from scratch.** It acquired Qntfy (2021), Total Brain (Nov 2022), and Mindstrong's technology stack (March 2023). Mindstrong in particular brought an electronic health record, clinical-note functions, care planning, and machine-learning assets including digital-biomarker risk-alerting. So when we say "wrapper," the layers around the model are partly engineered in-house and partly inherited through acquisition.

---

### Which core techniques they ACTUALLY use

**Pre-training / continued pre-training — NO.** *(inference, well-grounded)* No public evidence, no GPU-cluster talent, no claims. Their hiring centers on "evaluate and select appropriate LLMs" — i.e., picking someone else's model. This is the line that caps their engineering difficulty below the frontier labs. *Difficulty for them: not attempted.*

**Fine-tuning — LIKELY (lightly), company-stated as a technique.** *(sourced — Built In Colorado posting)* Their Principal AI Engineer posting explicitly names fine-tuning, describing the balancing of "techniques such as many-shot in-context learning and fine-tuning." So this is a stated, intended competency — not merely inferred from a stray de-identification line. The scale and method, however, are genuinely undisclosed. If it exists, it is light customization on top of a vendor model, not from-scratch training. *Difficulty: low-to-moderate. The technique is named; the depth is unknown — not found.*

**Reward modeling / RLHF / RLAIF / DPO — NO public evidence.** *(inference)* These are techniques for training your own model's behavior. There's no sign SonderMind does this; their behavior-shaping appears to be prompt engineering plus guardrails, which is far cheaper and far more common.

**MoE + routing — NO (not theirs).** *(inference)* Whatever routing exists lives inside the vendor's model, not SonderMind's stack.

**Prompt engineering & orchestration — YES, this is the core of what they build.** *(sourced — Built In posting + BHT blog)* Their postings center on "LLM workflows, agentic patterns, in-context/many-shot learning, prompt engineering." In plain terms: they write careful instructions, chain steps together (transcript → summary → draft note → clinician review), and stitch the model into their app. Real software work, but **commodity assembly** — thousands of companies do exactly this. *Difficulty: low-to-moderate. Talent: applied LLM engineers (~$160-190K). Cost: modest. Data: not data-hungry.*

**RAG / memory — YES, and this is a step above a basic chatbot.** *(sourced — privacy center & FAQ)* The consumer companion — branded **Sonder** (not "AI Coach," which appears to be an older or internal label) — isn't stateless. It "remembers your care program," tracks progress, and produces a pre-session summary of "stress patterns, recurring negative thoughts, or successful coping strategies" for the therapist. It pulls in each patient's history, goals, and journaling to personalize. Building per-user memory that stays consistent, private, and correctly scoped is meaningfully harder than a one-off chatbot — though note this memory/personalization capability may trace partly to acquired tech (Mindstrong's care-planning and ML stack) rather than being freshly engineered. *Difficulty: moderate. The hard part is doing it inside HIPAA, not the retrieval itself.*

**Voice / transcription (ambient scribe) — YES, but bought, not built.** *(inference; vendor unknown — not found)* "AI Notes" listens to a session and drafts a clinical note (company-stated to cut note completion time by "up to 80%"). The speech-to-text almost certainly comes from a vendor (Whisper/Deepgram-class); no provider is disclosed. The SonderMind-specific work is turning the transcript into a *clinically structured* draft and routing it for sign-off. *Difficulty: moderate; the transcription is commodity, the clinical formatting + workflow is the value-add.*

**Serving / latency — UNKNOWN — not found.** *(absence)* No public detail on infrastructure, cloud, latency engineering, or cost optimization.

**Guardrails & crisis detection — YES, but with a real tension in the public record.** *(sourced — FAQ + safety article; "passive" characterization is inference)* This is the most important safety point, and the evidence cuts two ways. Per the Sonder FAQ, the consumer bot is deliberately scope-limited: it "is not therapy," "cannot diagnose," and if a user expresses being unsafe it surfaces emergency resources (988) rather than assessing risk itself — which reads like keyword/intent triggering plus deflection. *(inference: "passive")* But the company's safety article claims **more** than deflection: that they "design our tools with automatic evaluations and safeguards that activate when risk signals appear." So the company asserts active risk-signal detection, mechanism undisclosed. The honest read: scope-limited per the FAQ, yet active safeguards claimed in marketing, with the actual mechanism unverified either way.
  - **The latent (and possibly acquired) capability:** *(sourced — qntfy.com / Coppersmith bio; acquisitions sourced)* Their Chief Data Officer, Glen Coppersmith (ex-Johns Hopkins HLTCOE, 50+ peer-reviewed papers), literally pioneered ML suicide-risk detection from language — and joined via the Qntfy acquisition (2021). Mindstrong, acquired in 2023, shipped digital-biomarker risk-deterioration alerting. So the *talent and prior tech* to build real crisis modeling exist in-house through acquisition. This complicates the simple "they sidestep the hard problem" story: they own a company that specifically did risk alerting. Still, there is **no public evidence** that capability powers the production guardrail. *(inference)*

**LLM-as-judge / clinical evals — POSITIONED AS CORE, but undisclosed in substance.** *(sourced as company positioning)* The Principal AI Engineer posting frames evals as a primary responsibility — to "translate product requirements into comprehensive evals sets and processes" (a paraphrase, not a verbatim "eval frameworks" claim). So evals are a stated core engineering function, not a passing mention. But no audit results, no eval methodology, and no LLM-as-judge specifics are published. In a regulated mental-health setting, rigorous evals are the part that *should* be hardest — and it's the part with the least public substance. *Methodology and results: unknown — not found.*

**Data pipelines — YES, genuinely non-trivial.** *(sourced — company-stated)* De-identification, dual encryption, 30-day audio deletion, per-feature deletion, opt-in/opt-out toggles, audit logging, all under HIPAA + ISO 27001. Moving therapy PHI through LLMs without leaking it is real engineering. *Difficulty: moderate-high — one of the two places their work is clearly above a generic chatbot.*

**Governance.** *(sourced; one claim softened)* The named public governance artifact is the **AI Constitution** — a clinical, privacy-first framework — with an **AI Governance Council** as the approving body. Per the sources, features are co-developed with clinicians and "released only after clinical review." (The earlier framing that the Council reviews "every feature pre-launch" is slightly stronger than the sources support, so we soften it.) As with evals, the framework is named but no audit results are published.

---

### What's genuinely hard vs. commodity assembly (their case)

| Genuinely hard for them | Commodity assembly |
|---|---|
| HIPAA/ISO-27001 data pipeline around an LLM (de-id, encryption, deletion, audit) | The underlying language model (rented, vendor undisclosed) |
| Per-patient memory/personalization done privately (partly acquired) | Prompt engineering & step-chaining |
| Clinician-in-the-loop documentation workflow | Speech-to-text (vendored) |
| Rigorous clinical evals — *claimed as core, but undisclosed* | Basic chatbot Q&A |
| Real crisis-risk modeling — talent/tech owned (via acquisition), production use unproven | |

---

### What this takes, in plain terms

- **Talent:** applied LLM/product engineers (~$160-190K) plus security/compliance engineering — both readily hireable. The rare asset is the in-house clinical-ML talent (Coppersmith), acquired rather than grown.
- **Cost:** modest by AI standards. No training cluster, no frontier-model spend; the bills are API usage, a vendored scribe, compliance infrastructure, and three acquisitions.
- **Data scale:** their edge is proprietary therapy data and acquired clinical assets, not training-set size. No public figures; fine-tuning and eval data scale are undisclosed.

---

### Bottom line

SonderMind is a **wrapper — but a clinically serious, compliance-heavy one**, not a toy. Its engineering edge is **proprietary therapy data + clinician-in-the-loop + regulated plumbing + acquired clinical tech**, not model science. It publicly avoids consumer general-purpose chatbots and keeps the riskiest autonomous AI out of scope. But the simple "they sidestep crisis modeling" story is complicated: they acquired a company (Mindstrong) that did risk-deterioration alerting and employ a CDO who pioneered the field. On the public record as of 2026-06-24, there is no evidence of pretraining, RLHF/DPO, or substantial fine-tuning; fine-tuning and evals are *stated* engineering competencies but undisclosed in depth and results; and the things that *would* be hardest (rigorous clinical evals, real crisis detection) are either undisclosed or scope-limited. **Difficulty: 3/5** for the suite; the Sonder consumer chatbot alone is closer to 2/5.

*Undisclosed / not found:* foundation-model vendor, cloud provider, vector DB, STT vendor, fine-tuning scale/technique, eval methodology and audit results, latency/serving architecture, and whether acquired risk-alerting tech is live in production.

**Engineering moat:** Compliance plumbing + clinician-in-the-loop + proprietary/acquired therapy data — a defensible operational moat, not a model-science one.

### Sources
- https://research.contrary.com/company/sondermind
- https://www.builtincolorado.com/job/principal-ai-engineer/3193831
- https://www.behavioralhealthtech.com/insights/engineering-empathy-how-were-building-ai-that-strengthens-not-replaces-human-care
- https://www.sondermind.com/resources/articles-and-content/is-artificial-intelligence-for-mental-health-safe/
- https://www.sondermind.com/faqs/
- https://www.sondermind.com/faqs/sonder-ai-companion-in-sondermind-app-faq/
- https://www.sondermind.com/ai/
- https://privacy.sondermind.com/
- https://privacy.sondermind.com/policies/en/?name=sonder-mind-ai-constitution
- https://www.sondermind.com/resources/announcement/sonder-mind-launches-suite-of-clinically-backed-ai-tools-for-mental-health-care-delivery-to-help-people-feel-better-faster/
- https://www.sondermind.com/resources/announcement/mental-health-leader-sondermind-to-provide-more-personalized-care-with-acquisition-of-mindstrong-technology/
- https://qntfy.com/glen/
- https://www.statnews.com/2025/12/01/ai-chatbot-headspace-talkspace-lyra-sondermind-digital-mental-health/


## Youper

Youper is best understood not as a company that builds artificial intelligence, but as one that *arranges* someone else's AI carefully and wraps it in clinical safety and structure. The intelligence — the part that actually writes the words you read in the chat — is rented from OpenAI, the makers of ChatGPT. Youper's own engineering is the scaffolding around it. That scaffolding is real and took genuine skill, but it is a different, and much lighter, kind of work than building the AI itself.

One framing caveat up front, because it shapes everything below. Most of what we know about Youper's internal design comes from a single source: a 2023 LinkedIn article by co-founder and CEO **Jose Hamilton Vargas**, a psychiatrist (not the company's AI engineer). That article is largely *prescriptive* — it describes what a safe mental-health chatbot *should* do — so its claims about Youper's own running system are best read as the CEO's stated design philosophy, not an audited description of production code. Where the brief below relies on that one post, treat it as "claimed by the CEO, implementation depth undisclosed," even for the pieces that sound most concrete.

### What they genuinely build

**1. A clinician-authored "controller" (prompt orchestration) — their core craft.**
The most important piece of Youper's own engineering is what the CEO calls an "expert system": a hand-built *decision tree*. Picture a large, carefully designed flowchart, plausibly written by a psychiatrist (likely Hamilton himself). The CEO's words are that this expert system "guides how and when the generative AI interacts with the user to ensure the application of evidence-based interventions" (sourced — Hamilton Vargas LinkedIn, 2023). The intent is that this flowchart, rather than the AI, shapes which clinical exercise gets offered (a breathing exercise, a thought-reframing skill, a gratitude prompt) and when, with GPT used to phrase it in natural, friendly language. 

Be careful here: the *precise* division of labor — "the flowchart decides, then hands off to GPT, and GPT never acts on its own" — is an interpretation, not a disclosed fact. The CEO described general guidance; how strictly the tree gates the model at runtime is not public. Still, building this kind of controller — mapping real clinical protocols into software logic and stitching it to a language model — is the genuinely skilled, non-commodity part of their stack. It is orchestration engineering, not AI research.

**2. Crisis detection and guardrails — the highest-stakes piece.**
Youper layers safety checks on top of GPT. The CEO described "automatic input and output flagging" (sourced — same 2023 article) — scanning both what the user writes and what the AI is about to say for expressions of suicidal thinking or self-harm. The public safety page confirms the user-facing behavior: when a crisis is detected the app stops counseling and refers the person out, to the 988 Suicide & Crisis Lifeline, the Crisis Text Line (741741), or 911, and explicitly states there is no licensed-professional review and that "detection systems are not infallible" (sourced — youper.ai/safety, verified verbatim, 2026). Building a *reliable* version of this is genuinely hard; the U.S. FDA's November 2025 advisory committee flagged exactly these failure modes — hallucination, sycophancy, missed risk — as unsolved for the whole category (sourced — Orrick/FDA DHAC, 2025-11). But Youper's own implementation depth is undisclosed: we know it flags inputs and outputs; how accurate that classifier is (its false-negative rate, the number that actually matters) is **unknown — not found**.

**3. Fine-tuning — claimed, not verified at scale.**
The CEO wrote that "training general models on data specific to the target mental health concerns is critical" (sourced — same 2023 article). Fine-tuning means taking the rented model and nudging it with extra examples so it speaks more like a careful therapist. This is a *light* form of model work — effectively ordering a customization from OpenAI's menu, far cheaper than building a model from scratch (the qualitative gap is real; any exact per-word figure is an estimate, not a found fact). Whether Youper actually ran this at meaningful scale, versus stated the intent, is **unknown — not found** (inference).

**4. Privacy plumbing — modest but real.**
Before sending messages to OpenAI, Youper hashes usernames, emails, and identifying details, and encrypts stored data (sourced — 2023). This is standard, competent privacy engineering for a health app — not exotic, but it must be done correctly given the sensitivity of the data.

**5. Voice — shallow.**
The 2026 app offers "voice journaling" as a premium feature (sourced — reviews, 2026), but there is no evidence of real-time spoken conversation, custom speech models, or voice-latency engineering. This reads as a feature bolted onto a text-first product.

### What they almost certainly do NOT do

- **Pre-training or continued pre-training** (building or deeply re-educating a foundation model): No. This needs thousands of GPUs and tens-to-hundreds of millions of dollars. Youper raised roughly $3.5–5M total (last round 2019) and runs a team of well under 20 — in fact closer to a handful — orders of magnitude too small (inference; funding and team size verified).
- **Advanced preference training (RLHF, RLAIF, DPO, reward modeling):** No public evidence; these are frontier-lab techniques (inference).
- **Mixture-of-Experts / model-internal optimization:** No — that is OpenAI's concern, not Youper's.
- **Their own serving/latency infrastructure:** No. Building on OpenAI's API means OpenAI runs the expensive, hard part. Youper's backend is a conventional consumer-app stack.
- **Retrieval / long-term memory (RAG):** Reviews mention trend charts from mood logs, and the former CTO's profiles mention RAG generically, but there is no disclosed retrieval-augmented memory inside Youper, and the product has historically had limited cross-session memory (contested / unknown — not found).
- **Automated LLM-as-judge evaluation:** No disclosed harness. Their evaluation is *clinical*, not AI-grading-AI (inference).

### Where the genuinely hard work is

Youper's hard problems are **clinical and regulatory, not computational.** The standout asset is a peer-reviewed study (Stanford + Youper, JMIR 2021) across 4,517 users — but it must be read carefully. It reported anxiety improvement (effect size d=0.57, maintained over the study) and depression improvement (d=0.46) — but the depression gain did *not* hold past the first two weeks (d≈0.05 in weeks 3–4, essentially zero), so citing only the favorable two-week depression figure overstates durability. The study is also observational, uncontrolled, and self-reported, and about 48% of users (2,161 of 4,517) were concurrently on medication or in therapy — a confound the authors themselves flag (sourced — JMIR 2021, verified). Running that study, authoring clinically faithful content, and building crisis guardrails that don't fail dangerously is the real difficulty. The software around the rented AI is competent assembly.

### One telling signal on depth

The applied-AI lead, co-founder/CTO **Thiago Marafon**, appears to have largely moved on by 2024–25 — now listed as Chief AI Officer at Starian (a hotel/resort marketing-and-management company, entirely unrelated to mental health) and an AI consultant at the clinical-conversation startup mpathic (sourced — LinkedIn/Crunchbase, verified). With the company down to a handful of people, the realistic read is that Youper today is a maintained, lean wrapper rather than a place doing active, deep AI engineering (inference).

### Bottom line for a non-technical reader

Youper rents the intelligence (OpenAI's GPT) and builds three things of its own that required real skill: a clinician-authored flowchart "controller" meant to keep the AI delivering validated therapy techniques; a safety net that watches for crisis language and refers people out; and the clinical evidence that makes the product credible. That is meaningfully more than a thin "ChatGPT-in-a-trenchcoat" — but far less than a company building its own AI. The difficulty is a 2 out of 5: above the floor because clinically faithful orchestration and crisis guardrails are non-trivial, but well below frontier because there is no proprietary model, no advanced training, and no serving infrastructure of their own. And note: the two pieces that sound most impressive rest on a single CEO blog post written in an aspirational register, so even the "2" leans on claims that have not been independently verified in production.

**Engineering moat:** Thin — a competent, clinically-anchored wrapper on OpenAI's GPT whose real edge is published clinical evidence and crisis-safety design, not any proprietary AI.

### Sources
- Hamilton Vargas, "Why Generative AI (LLM) Is Ready for Mental Healthcare," LinkedIn (single source for the expert-system, fine-tuning, and input/output-flagging claims): https://www.linkedin.com/pulse/why-generative-ai-chatgpt-ready-mental-healthcare-jose-hamilton-md
- Youper safety page: https://www.youper.ai/safety
- JMIR 2021 outcomes study (N=4,517): https://www.jmir.org/2021/6/e26771/
- CTO Thiago Marafon (current roles): https://www.linkedin.com/in/thiagomarafon/ , https://www.crunchbase.com/person/thiago-marafon , https://www.mpathic.ai/healthcare
- FDA Digital Health Advisory Committee on generative-AI therapy chatbots (Nov 2025): https://www.orrick.com/en/Insights/2025/11/FDAs-Digital-Health-Advisory-Committee-Considers-Generative-AI-Therapy-Chatbots-for-Depression
- Privacy/review references: https://www.mozillafoundation.org/en/privacynotincluded/youper/ , https://www.choosingtherapy.com/youper-app-review/ , https://techlaugh.com/youper/
- Background interview (CTO): https://www.mission.org/it-visionaries/how-a-i-can-revolutionize-mental-healthcare-with-thiago-marafon-cto-of-youper


## Sonia

**The short version for a non-technical reader:** Sonia does not build its own AI brain. It rents one from a frontier lab and wraps it in clinically-informed software. We know for certain that the *safety* part of Sonia runs on OpenAI's GPT-5 (specifically the model OpenAI released in October 2025); the AI vendor behind the *main therapy conversation* is not disclosed. The real engineering is in the wrapping: a structured therapy-session controller, a separate always-on crisis detector, a real-time voice loop, and — most notably — a published, clinician-validated study of how well that crisis detector actually works. This is a capable, safety-conscious wrapper built by a strong applied-ML team, not a frontier-AI research lab. **Overall engineering difficulty: 3 out of 5.**

Here is what they actually do, plain-language, with how hard each piece really is.

### What they actually build

**1. Orchestrating the AI into a real therapy session (this is the product).** Rather than one open-ended chatbot, a Sonia session is run as a structured, multi-stage flow — the founder describes it as an "LLM state machine" with about eight defined stages (mood check, agenda-setting, cognitive restructuring, feedback, and so on). The founder has also said that every reply the user sees is preceded by roughly seven extra behind-the-scenes AI calls, each analyzing the moment from a different therapeutic angle before Sonia answers.
- *How hard:* Medium. Chaining many AI calls with per-stage instructions and tracking where you are in the session is well-understood engineering. Doing it reliably across a 30-minute therapy conversation is genuine work, but it is not frontier research.
- *What it costs:* If the "seven calls per reply" pattern is accurate, Sonia pays the model vendor several times for every single user message. That is a real per-session bill that grows directly with usage — and it is the main reason cost and speed engineering matter to them.
- *How sure we are:* The eight-stage structure is documented in a founder-written blog post hosted by LangChain, so the stage count itself is *sourced*. The "seven background calls" figure is *self-reported* — it shows up in multiple secondary write-ups (TechCrunch, startup profiles), so it is more than a lone quote, but no one has verified the actual mechanism.

**2. A separate crisis detector — and, unusually, proof it works.** This is the most substantiated and most impressive part of Sonia's stack. In January 2026, the team published a preprint (with the Psychiatric University Hospital Zurich) spelling out exactly how their suicide-/crisis-risk detection works.
- It runs as a **separate safety monitor watching every turn**, independent of the conversation model — not a line buried in the chatbot's instructions. When it fires, the system enters an "emergency mode."
- It is **prompt-based with no fine-tuning** — they used one off-the-shelf model (OpenAI's gpt-5-chat-latest) and wrote five instruction variants of escalating caution, from "Extreme Low" to "Extreme High," each lowering the bar for what counts as a crisis.
- On 200 real conversation segments labeled by clinicians, the detector scored an overall ROC AUC of 0.90 (a strong score). The trade-off is the headline finding: the most cautious "Extreme High" setting caught essentially every crisis (100% recall) but raised more false alarms; a slightly less cautious "High" setting still caught 98.9%. (Note: these are two *different* settings — the "catch everything" result and the "missed one case" result are not the same data point, and the precise case counts behind them are not independently confirmed.)
- It is **fast enough to run on every turn**: about 0.64 seconds on average across 3,000 trials.
- Their key insight: deciding what counts as a "crisis" is genuinely ambiguous — five expert clinicians only moderately agreed with each other (Fleiss kappa 0.34). So instead of chasing a "correct" answer, they deliberately run an over-cautious detector as a *separate layer* and accept false alarms as the price of safety. Tellingly, the AI's mistakes clustered exactly where the human experts also disagreed.
- *How hard:* Medium-high — not because the code is exotic (it's prompts plus a routing layer) but because making it *safe and validated* required a real clinical evaluation pipeline. The hard part is the methodology and the clinician-labeled data, not the AI inference.
- *What it takes:* Clinician annotators and academic collaborators — not GPU clusters.

**3. Clinical evaluation — their real differentiator.** To produce the numbers above, Sonia built an evaluation dataset out of its own live traffic: 3,608 exchanges from 676 clients, screened over a three-week window in September 2025, with 200 segments labeled by five expert clinicians. (Important framing: that's a three-week *study screening window*, not Sonia's total user base — separate marketing material cites figures in the thousands of users.) Most "AI therapy" wrappers cannot show work like this. This evaluation discipline is the single strongest signal that Sonia is more than a thin wrapper.

**4. Speed and voice.** The published sub-second risk-checking latency, plus a self-reported custom real-time voice loop (streaming speech-to-text, natural pause/turn detection, text-to-speech, no press-to-talk button), show real attention to responsiveness. Natural voice turn-taking at conversational speed is genuinely non-trivial.
- *How sure we are:* The voice pipeline is *self-reported* with no independent technical detail, and the published <1-second latency figure is specifically for the text crisis classifier — not the full voice loop.

**5. Memory and intervention tools.** Sonia keeps a cross-session "conceptualization" of each client (longitudinal memory/personalization) and ships structured CBT/DBT/ACT worksheets as tools the AI can use. This is described only qualitatively — no technical depth (how retrieval or memory storage works) is disclosed.

### What they do NOT do

- **Training their own foundation model:** No. The CEO is explicit: "We're not building our own foundational models." There is no infrastructure, talent, or cost signature of base-model training. *Sourced.*
- **Advanced training techniques (RLHF, DPO, reward modeling):** No public evidence, and their safety paper deliberately avoids all training. *Not found; inferred absent.*
- **Mixture-of-experts / model architecture work:** Not applicable — that's a concern for companies that build models, which Sonia isn't. The only "routing" they do is choosing how cautious the safety prompt should be, which is ordinary application logic.
- **A claimed "lot of fine-tuning" on a proprietary therapist dataset:** The CEO has said this about the conversational model, but with no disclosed scale or method — and the team's own safety paper confirms the crisis layer used *no* fine-tuning. Treat the fine-tuning claim as marketing-adjacent self-report. *Contested.*
- **Name-collision warnings:** A 2026 job listing hiring speech-recognition engineers under "Sonia" is a *different* company (Sonia Solutions GmbH, a Hamburg medical-billing firm) — do not attribute it. Likewise, a "Lumen/Alexa" trial and a Llama-based voice prototype that surface in searches are not this Sonia.

### Genuinely hard vs. off-the-shelf

- **Off-the-shelf:** the base AI model (rented), the multi-call orchestration framework (LangChain), commodity speech-to-text and text-to-speech, and the basic chat product.
- **Genuinely hard for them:** (1) the **clinical evaluation and safety methodology** — building a clinician-labeled crisis dataset from real traffic and publishing honest catch-rate/false-alarm trade-offs is rare and credible; (2) the **layered safety design** that keeps a conservative crisis monitor separate from the conversation; (3) the **real-time voice loop** with sub-second turn-taking (self-reported); and (4) **encoding how a clinician reasons** into a controllable session, which needs clinicians, not just coders.

**Engineering moat:** A clinically-instrumented, eval-validated safety wrapper on a rented frontier model — real and defensible in mental-health credibility, but not in core AI technology.

### Sources

- medRxiv preprint, "Suicide- and crisis-risk detection using large language models in mental-health chatbots" (DOI 10.64898/2026.01.12.26343914, posted Jan 15 2026) — primary, not yet peer-reviewed
- LangChain blog, "Mental health therapy as an LLM state machine" (founder-authored guest post)
- TechCrunch, "Sonia's AI chatbot steps in for therapists" (June 2024)
- Authority Magazine / Medium, founder interview with Chris Aeberli
- Y Combinator company profile; Apple App Store listing for Sonia


## Headspace (Ebb)

**The one-sentence version:** Ebb does not have its own "brain." It builds on a general-purpose AI model from an outside vendor — Headspace has never named which (not disclosed in any reviewed public source as of 2026-06-24) — and wraps it in a clinically-designed safety, evaluation, and orchestration system. The rented brain is commodity. The wrapper is where Headspace's real engineering lives, and it is more disciplined than a typical chatbot — though the genuinely hard *clinical* proof remains absent.

Think of a restaurant that buys its ovens from a manufacturer (the AI model) but designs its own kitchen workflow, food-safety inspections, and recipes (the wrapper). One nuance: Headspace's kitchen is partly built *from* rented ovens too — even its safety system calls outside AI models — so the "rented brain vs. owned wrapper" line is a little blurrier than the analogy suggests.

---

### What they actually use — technique by technique

**Building a foundation model from scratch (pre-training) — NOT USED.** [inference, well-grounded] Headspace builds on existing models rather than training one from scratch. A widely-cited line that they "train using a combination of large language models as well as proprietary in-house datasets" supports this, though I'd flag that this exact wording appears in secondary write-ups and could not be confirmed verbatim from a direct fetch of headspace.com/ai — so treat it as well-grounded inference, not a pinned quote. Either way, nothing in any source suggests they run a research lab or train a base model. Foundation-model training is the single most expensive technique in AI — as a rough industry illustration, tens to hundreds of millions of dollars in compute (a generic figure, not a measured Headspace number) — and they correctly skip it. There's also no evidence of *continued* pre-training (taking a base model and further training it on mental-health text); what they call "training" is almost certainly prompt design plus light fine-tuning, not gradient training of the big model.

**Fine-tuning a small model (SFT) — USED, narrowly, inside a hybrid.** [sourced] The clearest piece of real, bespoke machine learning is in the Safety Risk Identification system. Importantly, per headspace.com/ai, this system "uses a small fine-tuned language model **as well as** foundational LLMs" — it is a **hybrid**, not just one small classifier. The small fine-tuned model sorts text into 7 risk buckets (suicidal ideation, homicidal ideation, self-harm, domestic violence, substance use, eating disorders, and abuse of vulnerable populations), and larger foundation models assist. Fine-tuning a small classifier like this is a well-understood, mid-difficulty task. The hard part isn't the machine learning — it's getting clinically-labeled training data and picking the right sensitivity threshold: too sensitive and you get constant false alarms that ruin the experience; too lax and you miss a crisis, with real human and legal consequences. There is no public evidence of fine-tuning on the *conversational* model itself.

**Reward modeling / RLHF / DPO (training the model's behavior from preference data) — NOT FOUND.** [inference] These are the techniques labs use to shape a model's "personality" from human or AI feedback. There's zero public evidence Headspace does any of this themselves. Ebb's warm, motivational-interviewing tone is achieved through **prompting and conversation design**, not reinforcement learning. That's a real capability gap versus a company like Character.AI or a frontier lab — but a reasonable choice, since this is expensive and the rented base model already arrives pre-shaped by its vendor.

**Mixture-of-Experts / model-internal architecture — NOT APPLICABLE.** [inference] This is an internal design choice of the large model itself. Since Headspace doesn't build the model, it's the vendor's concern. (Note: their phrase about "multiple models orchestrated" is *not* this — see orchestration below. Don't conflate the two.)

**Prompt engineering & orchestration — USED, and this is the real core.** [sourced] headspace.com/ai states plainly that "Ebb is a complex AI system that contains multiple models, which are orchestrated to produce a response." A single user message doesn't hit one model — it flows through a pipeline: the safety system checks it, topic guardrails check scope, the conversational model (steered by a motivational-interviewing-flavored prompt) drafts a reply, and memory plus content-retrieval feed in context. An observational study (JMIR, Feb 2026) *documents* an evolution from CAI 1.0 to CAI 2.0: version 1.0 used rigid "turn-based prompting" (ask one question, reflect, repeat); 2.0 moved to a flexible "general conversation prompt" and added "comprehensive memory of all previous conversations." This redesign happened over roughly **9 months** (Ebb launched Oct 2024; CAI 2.0 launched July 25, 2025). Redesigning live orchestration and prompt strategy while keeping safety intact is solid applied engineering. Caveat on the evidence: the JMIR paper *describes* these feature differences — it is a descriptive study, not validation that the engineering is good. It documents the change; it does not grade it.

**Guardrails — USED, multi-layered.** [sourced] Explicit topic guardrails block medical advice, diagnosis, medication talk, clinical therapeutic techniques, and out-of-scope requests (travel, creative writing). CAI 2.0 added "clearer clinical boundaries, reduced out-of-scope and sycophantic behavior, improved de-identification, [and] evaluation of AI-related risks (eg, parasocial relationships)." (The original quote pairs "out-of-scope and sycophantic" in one clause — both are being reduced together.) Curbing sycophancy (the model over-agreeing or flattering) and policing parasocial attachment are current, sophisticated safety concerns — above-average for a wellness app. Difficulty: moderate; the work is in tuning and testing, not novel science.

**Crisis detection — USED, but UNVALIDATED.** [sourced for the mechanism; sourced gap for performance] 100% of messages are screened in real time; on a hit, members receive a direct link to text or call 988 (US and Canada) plus links to international crisis resources. The mechanism is real. (An earlier draft claimed Ebb also "ends the conversation" on a crisis hit — no reviewed source supports that, so it's dropped as unverified.) The bigger issue: **no sensitivity/recall or false-negative numbers have ever been published**, so we cannot know how good the detector actually is. In a crisis context, an undisclosed miss rate is the single most important unknown in the entire stack. Building the classifier is mid-difficulty; *proving* it works at clinical-grade recall is the genuinely hard thing they have not demonstrated. [sourced gap]

**LLM-as-judge & internal evals — USED, and notably mature.** [sourced] They run an automated evaluation system using "LLM-as-a-judge" to score responses on conversational quality, safety, and out-of-scope behavior, plus pre-release testing against "synthetic members" (simulated users), red-teaming before and after release, and daily human QA review of random conversations. This is a real, disciplined evaluation pipeline — most small chatbot teams don't build this. It's the difference between "ship and pray" and regression-testing every change before release. Difficulty: moderate but high-value; this is professional ML-ops. **Caveat:** these are *internal/automated* evals, not clinical-efficacy trials. There is still no RCT, no symptom-outcome data, and no validated motivational-interviewing fidelity score for Ebb. The hard clinical validation is absent.

**RAG / memory — USED.** [sourced; one detail unverified] Ebb retrieves relevant exercises and meditations from a library of over 5,000 meditations and activities (classic retrieval-augmented generation). A reported in-house ML team doing "vector search, embedding models, RAG systems" was cited from a job spec, but I could not independently locate that spec in this review — treat the in-house-RAG-team detail as author-sourced-but-unverified-here. CAI 2.0's cross-session memory ("comprehensive memory of all previous conversations") is real per JMIR. Both retrieval and memory are commodity-to-moderate engineering in 2026 — well-trodden patterns — but doing them reliably under HIPAA (with de-identification) adds genuine compliance complexity.

**Serving / latency — UNKNOWN.** [unknown — not found] No public detail on infrastructure, latency targets, model-serving, or cost engineering. The Dec 2025 addition of **Voice Mode** implies real-time speech-to-text and text-to-speech in the pipeline, which is latency-sensitive — but whether they built or bought that speech stack is undisclosed (likely bought/assembled). [inference]

**Voice — USED, likely assembled.** [sourced it exists; inference on build] Voice Mode lets users speak instead of type. No evidence they trained their own speech models; almost certainly a third-party speech API bolted onto the existing pipeline. [inference]

**Data pipelines — USED.** [sourced] Real-time screening of 100% of traffic, de-identification, flagging/escalation queues for clinician review, and daily QA sampling constitute a non-trivial data pipeline. The HIPAA/GDPR de-identification and audit requirements are where the compliance engineering cost concentrates.

---

### What's genuinely hard vs. commodity assembly

- **Commodity assembly:** the conversational intelligence (rented), retrieval over their content library, cross-session memory, voice input/output, and the basic chat loop. In 2026 these are off-the-shelf patterns.
- **Genuinely harder (their real engineering):** (1) the **hybrid** real-time safety system — a fine-tuned small classifier *plus* foundation LLMs — and the clinical judgment behind its 7 categories and sensitivity thresholds; (2) the LLM-as-judge + synthetic-member + red-team evaluation harness that gates every release; (3) the multi-model orchestration and the 1.0-to-2.0 prompt redesign shipped live in ~9 months; and (4) doing all of this under HIPAA in a high-liability clinical domain.
- **The hardest thing — and they haven't done it:** proving any of it works clinically. No crisis-recall metric, no motivational-interviewing fidelity validation, no symptom-outcome RCT for Ebb. The engineering is competent; the *clinical proof* is the missing keystone.

**Bottom line:** Ebb is a wrapper, but a clinically-supervised, evaluation-disciplined, safety-heavy one — clearly above the median "ChatGPT-in-a-box" app. The intelligence is rented; the differentiation is the safety/eval/orchestration layer plus clinical design. Difficulty 3/5: solid applied-ML, safety, and healthcare-compliance engineering — not novel research — and resting partly on self-reported claims no outside party has independently validated.

**Engineering moat:** A real but shallow moat built on disciplined safety/eval/orchestration engineering and clinical design — not on proprietary models or proven clinical outcomes, which leaves it copyable by any well-resourced health-tech team.

### Sources
- https://www.headspace.com/ai
- https://formative.jmir.org/2026/1/e86904
- https://pubmed.ncbi.nlm.nih.gov/41687100/
- https://hlth.com/insights/news/headspace-updates-ebb-ai-with-voice-mode-and-enhanced-memory-to-deepen-mental-health-support-2025-12-09
- https://www.businesswire.com/news/home/20251208896917/en/Headspace-Rolls-out-Voice-Feature-for-Empathetic-AI-Companion-Ebb
- https://dscout.com/people-nerds/headspace-using-genai
- https://www.glassdoor.com/job-listing/staff-machine-learning-engineer-headspace-JV_IC1147401_KO0,31_KE32,41.htm
- https://www.headspace.com/articles/headspace-brings-empathetic-ai-companion-ebb-to-uk-members
- https://www.businesswire.com/news/home/20241010397470/en/Mental-Health-Company-Headspace-Launches-Empathetic-AI-Companion


## BetterHelp (Teladoc)

**The one-sentence version:** BetterHelp does not build its own AI brain. It is a human-therapist marketplace that bolts a few AI conveniences onto someone else's large language model (the same category of technology behind ChatGPT). Picture a company that buys a powerful engine from a supplier and spends its real engineering effort on the chassis, the seatbelts, and the legal paperwork — not on designing the engine. `[inference]` (No model vendor is named on BetterHelp's own pages, which describe the AI only as "often based on large language models (LLMs) or other advanced systems" `[sourced]` — so even the "buys an engine from a supplier" detail is a reasonable read, not a documented fact for BetterHelp specifically.)

### What they actually do with AI

Strip away the jargon and there are three real AI features, and all three are commodity assembly — the kind of thing any competent team with an API key and a few applied-LLM engineers can build:

- **AI-assisted therapist matching.** BetterHelp markets matching "that incorporates AI" over your intake answers, your stated preferences, and therapist availability and specialty. `[sourced for "AI-assisted matching"]` The page gives no technical description, so exactly how it works is undocumented; it is almost certainly mostly classical machine learning and rules with perhaps some LLM parsing of intake text, not a pure-LLM system. *Difficulty: low. Talent: standard ML/backend engineers. Cost: modest. Data: their own intake and therapist-roster records.* `[mechanism is inference]`
- **AI-generated session summaries** that appear after a live session to help the therapist with documentation. This is a textbook call to a general-purpose LLM. *Difficulty: low. Talent: applied-LLM/prompt engineers. Cost: per-token API spend. Data scale: one transcript at a time — not bulk training.* `[sourced]`
- **Suggested message replies** in async messaging. Same commodity pattern. `[sourced]`

The genuine engineering work — the orchestration — is prompting a hosted LLM for these tasks and wrapping every output in a human-review workflow. That is real applied-AI work, but it is assembly, not invention. `[inference]`

### What they pointedly do NOT do

This is where a non-technical reader should resist being impressed. None of the hard, expensive, talent-scarce parts of modern AI appear anywhere in the public record:

- **No training of their own model** — no pre-training or continued pre-training disclosed. `[inference — argument from silence]`
- **No RLHF / RLAIF / DPO / reward modeling** — the techniques used to actually shape a model's behavior. `[inference]`
- **No RAG or long-term memory system, no LLM-as-judge evaluation harness, no published clinical evals or benchmarks, no AI voice model.** `[inference — not found]`

A fair caveat: absence of disclosure is not proof of absence. These are "not found in the public record," not "proven never to exist." But a company doing serious model-training work normally talks about it, and BetterHelp does not.

### Where the genuinely hard engineering actually lives

The hard part of BetterHelp is not the AI — it is the regulated environment the AI has to run inside:

1. **HIPAA/PHI-grade data plumbing under an active FTC consent order.** In 2023 the FTC finalized a $7.8M settlement banning BetterHelp from sharing sensitive mental-health data for advertising. `[sourced]` That turns every data path into a legal liability: member clinical content must stay encrypted, walled off from any training use, and never sent to a third-party model without a formal Business Associate Agreement. This is real, expensive engineering, and it is where the company's scarce technical talent goes — privacy, security, and data engineers, not ML researchers. `[engineering read is inference]`
2. **Safety and governance for a vulnerable population.** A cross-functional Responsible AI Committee (Legal, Clinical, Security, Product, Data/AI), formal AI Impact Assessments, alignment with the NIST AI Risk Management Framework, and prohibition-first rules. Verbatim from BetterHelp's Responsible AI page: the AI is barred from providing therapy, diagnosing, or making clinical decisions, and therapists are prohibited from feeding member information into third-party AI tools like ChatGPT for therapy communications. `[sourced]` The difficulty here is organizational and clinical, not algorithmic.
   - One commonly cited detail — that "every clinical AI output is a draft a human must edit and sign" — does **not** appear on BetterHelp's own page. It traces to a third-party Teladoc-focused marketing blog, so treat it as `[contested — Teladoc-side, non-primary]`, not as verified BetterHelp policy.
3. **Operating the marketplace itself.** A two-sided marketplace with 30,000+ therapists and hundreds of thousands of paying members, plus secure messaging and video telehealth at scale, is harder engineering than the bolt-on AI. `[inference]`

### A note on crisis detection

Automated suicide-risk flagging is a recognized norm in this industry, but it is **not confirmed as a BetterHelp feature.** `[inference — not found]` The often-quoted comparison — that rival Talkspace flagged 32,000 members — is a *cumulative* total since that program launched in 2019 (announced in September 2023), not a recent surge, and it runs on a proprietary classical NLP/ML classifier (~83% accuracy on the flagged subset), **not** a generative LLM. So it offers no support for the idea that crisis detection is an LLM feature anywhere in this space. Separately, Teladoc's broader Integrated Care intake screens for red-flag symptoms including suicidal ideation, but that is a parent-company program, not a confirmed BetterHelp capability. `[contested/inference]`

### Who supplies the model, and how it's hosted

No vendor is named on BetterHelp's own pages. `[sourced]` At the **Teladoc parent level**, a single third-party AI-marketing blog (getperspective.ai) states Teladoc "uses in-house models, BAA-covered Azure OpenAI Service deployments, and de-identified data for research," with generative AI restricted to non-diagnostic surfaces (summaries, intake, post-visit instructions, clinician-reviewed message drafts). This is the most concrete infrastructure signal available — but it is Teladoc-side, rests on a single non-primary source, and is **not confirmed for BetterHelp.** No primary Teladoc or Microsoft document corroborating an Azure OpenAI BAA arrangement for BetterHelp was found. `[contested — Teladoc-side, non-primary]`

### Difficulty, talent, cost, data — at a glance

- **Difficulty (AI dimension): 2/5.** A sophisticated-*enough* wrapper whose real sophistication lives in compliance and safety, not modeling. `[inference — editorial judgment, not a sourced figure]`
- **Talent:** privacy/security/data engineers and clinical-governance staff first; applied-LLM and standard ML/backend engineers second. No foundation-model researchers required.
- **Cost:** per-token API spend on the AI features; the heavy spend is regulatory compliance and platform operations, including the $7.8M FTC settlement and ongoing controls.
- **Data scale:** large *operational* data (intake, roster, messaging across 30,000+ therapists), processed one item at a time at inference — not assembled into any disclosed training corpus.

(Every difficulty/talent/cost number above is reasoned editorial inference, not a figure published by the company.)

**Engineering moat:** Their moat is regulatory and operational — HIPAA/FTC-grade data segregation, safety governance for a vulnerable population, and a two-sided telehealth marketplace at scale — not AI; the AI itself is a commodity wrapper anyone with API access could rebuild.

### Sources
- BetterHelp Responsible AI page — https://www.betterhelp.com/responsible-ai/
- Reframe Practice, "Does BetterHelp use AI" — https://reframepractice.com/answers/betterhelp/does-betterhelp-use-ai-and-what-clinicians-should-know
- getperspective.ai, Teladoc AI blog (non-primary, Teladoc-side) — https://getperspective.ai/blog/teladoc-ai-largest-telehealth-network-80m-visits-2026
- MIT Technology Review, therapists using ChatGPT — https://www.technologyreview.com/2025/09/02/1122871/therapists-using-chatgpt-secretly/
- Fierce Healthcare, AI suicide-risk detection (Talkspace) — https://www.fiercehealthcare.com/ai-and-machine-learning/ai-action-enhancing-suicide-risk-detection-behavioral-health
- FTC final order banning BetterHelp data sharing (2023) — https://www.ftc.gov/news-events/news/press-releases/2023/07/ftc-gives-final-approval-order-banning-betterhelp-sharing-sensitive-health-data-advertising
- Fierce Healthcare, Teladoc revenue/AI future — https://www.fiercehealthcare.com/finance/teladoc-revenue-falls-2-company-looks-towards-ai-future
- Seeking Alpha, Teladoc 2026 revenue guidance — https://seekingalpha.com/news/4557798-teladoc-projects-2_47b-2_59b-revenue-in-2026-while-advancing-ai-insurance-and-international


## Earkick

**Bottom line:** Earkick is, at its core, a "wrapper." Its "Panda" companion talks to you using a large third-party AI model (GPT/Claude-class) that Earkick did not build. But it is a more thoughtful wrapper than most — a small team has done real, hands-on machine-learning work that most wellness apps never touch. The genuinely hard and expensive parts of AI mental health — training your own model, clinically validated crisis safety, regulated-device pipelines — are mostly *not* things Earkick has built in-house.

Here is which core techniques they actually use, and what each takes in their case.

---

### What they genuinely do (and it's real engineering)

**Fine-tuning small open models (SFT via LoRA) — CONFIRMED, and the most credible technical thing they've shown.**
Earkick's own research blog — authored by Dr. Gagan Narula (described as their Senior ML Engineer; *the exact title is plausible but not independently verified* — *inference*) and "the Earkick AI team" — documents real experiments. They took small open-source models (Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct, and Microsoft Phi-3.5-mini at 4B and Phi-3-medium at 14B) and fine-tuned them using **LoRA** — a cheap "parameter-efficient" tuning method that nudges a tiny slice of the model instead of retraining the whole thing.

They trained on a **curated ~5.2-million-token corpus (~8,071 samples)**. The blog's stated composition is: psychology literature, NIMH/DSM-V material and peer-reviewed journals, NCE exam questions, NCMHCE/ASWB practice questions, and **synthetic EPPP exam data**. *(Note: an earlier draft claimed the synthetic data was "generated by GPT-4o/Gemini/Claude" — the blog does not clearly support that specific attribution, so treat it as unverified.)* They then graded the tuned models on real US counseling licensing exams (NCMHCE and ASWB). *[sourced: blog.earkick.com, accessed 2026-06-24]*

- *Result:* their fine-tuned Qwen-7B scored about **78%** (78.38%), which the blog frames as **surpassing gpt-4o-mini and approaching Claude 3 Sonnet**. One caveat for the reader: that ~78% is an **average across two separate exams** (202 NCMHCE + 81 ASWB questions) on the full dataset — not a single unified test score. A reduced-dataset ablation elsewhere in the blog shows lower per-exam numbers (~67% NCMHCE / 76.5% ASWB), so the headline figure is the best-case full-dataset average. *[sourced/contested]*
- *Difficulty:* low-to-moderate. This is well-trodden 2024-era technique, run on **a single NVIDIA A6000 GPU** — a few thousand dollars of hardware, days of work, one capable engineer. Not frontier research, but real and competently executed.
- *Talent / cost / data:* one strong applied-ML engineer; trivial compute; a small, partly-synthetic, mostly-public dataset a rival could reproduce quickly.

**Prompt / orchestration on a third-party model — the actual shipping product, though architecture is undisclosed.**
The live "Panda" chatbot delivers CBT/DBT-style moves (mood check-ins, cognitive reframing, emotion labeling) on top of a frontier LLM. This is **evident from how the app behaves**, but the production model is **undisclosed**, and it is **unknown whether their fine-tuned small models actually ship** or whether production simply calls a prompted frontier API. Their published fine-tuning work may be R&D, not the live system. *[inference; underlying model unknown — not found]*

**Voice + multimodal / biometric input — CLAIMED, lightly documented.**
The app accepts **voice memos** and **wearable biomarkers** (heart-rate-type signals, Apple Watch) and markets "multimodal sentiment analysis... analyzed on-device and fully private, 3x faster than other solutions." The company's stated rationale is the familiar one — depressed speakers tend to speak slower and pause more, anxiety alters vocal tone. But the technical substance (what runs on-device, how voice/biometrics fuse with the LLM, any accuracy numbers) is **not disclosed**. Treat "on-device," "3x faster," "fully private," and the vocal-biomarker claims as **marketing copy, not verified architecture**. *[contested/unknown — traces to company/LDV/Crunchbase copy]*

---

### What is partial, contested, or absent

**Crisis detection / guardrails — most likely NOT Earkick's.**
Two 2026 papers turn up in searches near Earkick; neither holds up as theirs:

1. A **medRxiv paper (Jan 2026) on suicide/crisis-risk detection in mental-health chatbots** uses 200 clinician-labeled real conversation segments from "a deployed mental-health chatbot." Its authors are Weber, Klebe, Wolf, Aeberli, Homan, ... Kowatsch, Kleim and Olbrich, with the industry affiliation **"Sonia AI, San Francisco"** explicitly listed. **No Earkick author and no Gagan Narula appear.** The "deployed chatbot" is therefore far more plausibly **Sonia AI's, not Earkick's Panda.** Earlier framing tying this to Earkick via the University of Zurich consortium overstates the link — Prof. Olbrich is the senior author, but the lead authors and named company point away from Earkick. *[contested — evidence points against Earkick]*

2. The arXiv paper **"Beyond Simulations: What 20,000 Real Conversations Reveal About Mental Health AI Safety"** (arXiv 2601.17003) is **NOT Earkick.** Its authors (Stamatis, Meyerhoff, Zhang, Tieleman, Malgaroli, Hull) are affiliated with **Slingshot AI, Northwestern (Feinberg), and NYU**, and the "purpose-built AI with layered safeguards" is **Slingshot AI's** product. *(Note: an earlier draft attributed this to Talkspace — that is wrong; one co-author has historical Talkspace ties, likely the source of the confusion.)* **Do not credit Earkick with this paper's safety architecture or metrics.** *[sourced — arXiv author list]*

So a confirmed, in-house, productionized crisis-safety system at Earkick is **unknown — not found**. A May 2026 Common Sense Media / Stanford report flagged exactly this gap.

**LLM-as-judge / clinical evals — LIMITED.** Their published evaluation is exam-accuracy scoring, not an LLM-judge harness or clinical-fidelity rubric. No RCT and no peer-reviewed efficacy beyond a stale 2023 internal survey. *[sourced/inference]*

**Not used / not built:** pre-training, continued pre-training, reward modeling, RLHF/RLAIF, DPO, Mixture-of-Experts + routing — **none**; these belong to model *builders*, and Earkick is a model *user*. Heavy serving/latency engineering, RAG / long-term-memory infrastructure, and regulated-device controls are **not evidenced**. *[inference]*

---

### Honest difficulty read

The hard-to-fake part Earkick *does* have is a **research-literate ML practice** — real LoRA fine-tuning, a curated clinical corpus, exam-based evals. That is why this reads as a roughly **2.5/5 wrapper** *(an editorial judgment, not a measured fact)*, not a 1/5 prompt-and-pray app. The hard parts they *don't* convincingly own — training their own model, an in-house validated crisis-safety system with human escalation, regulated efficacy infrastructure — are precisely the expensive, talent-scarce pieces they've chosen not to build. That omission is the central safety concern raised about them in 2026.

**Engineering moat:** Thin — a competent, research-literate wrapper whose only hard-to-copy asset is a small fine-tuning/eval practice that a rival applied-ML team could replicate in weeks; the genuinely defensible work (own model, validated crisis safety, clinical efficacy) is absent.

Sources:
- https://blog.earkick.com/large-and-small-language-models-in-psychotherapy/
- https://earkick.com/technologies/
- https://www.crunchbase.com/organization/earkick
- https://www.ldv.co/blog/2022/3/30/can-ai-detect-and-identify-changes-in-our-well-being-meet-karin-andrea-stephan-of-earkick
- https://www.medrxiv.org/content/10.64898/2026.01.12.26343914v1.full (author affiliation: Sonia AI — not Earkick)
- https://arxiv.org/abs/2601.17003 ("Beyond Simulations" — Slingshot AI, not Earkick)
- https://www.commonsensemedia.org/press-releases/some-ai-mental-health-apps-are-actively-harmful-for-teens-but-a-safer-approach-exists


## Woebot Health

**Bottom line up front:** Woebot does not build its own AI brains. It builds the *scaffolding* around AI — the scripts, the routing, and above all the safety checks. There is a crucial split that most coverage blurs: the product real users actually used was deliberately old-fashioned and non-generative, while the modern, ChatGPT-style generative system Woebot built lived **only inside research studies and never shipped.** The consumer app wound down in mid-2025 (announced and reported around early July 2025), and the company shifted toward selling to enterprise buyers. `[sourced]` (consumer shutdown — [STAT, 2025-07-02](https://www.statnews.com/2025/07/02/woebot-therapy-chatbot-shuts-down-founder-says-ai-moving-faster-than-regulators/)) `[inference]` (that the current live product remains classifier-plus-scripts; the source confirms the original product was scripted and non-generative but does not establish the 2026 production stack — see Open Unknowns)

Think of it as two different machines under one roof.

### Machine 1 — The shipped product: a "smart switchboard," not generative AI

The commercial Woebot works like a very sophisticated phone switchboard. Human writers and clinical psychologists write all the actual therapy content in advance — thousands of scripted lines of cognitive behavioral therapy (CBT). When you type something, a piece of AI reads your message and decides **which pre-written script to play next.** It does not *write* a reply; it *picks* one. Woebot states that in its "commercially or publicly available products," users "never interact directly with LLMs." `[sourced]` (verbatim, scoped to commercial/public products — [Woebot AI Core Principles](https://woebothealth.com/ai-core-principles/); [Technology Overview](https://woebothealth.com/technology-overview/))

The "AI" doing the picking is a **text classifier** — software that sorts a message into a category (anxiety vs. relationship problem vs. crisis) rather than generating new language. Woebot's history here is a clean tour of the last decade of language tech: hand-written keyword rules, then trained classifiers (a tool called fastText), and in **January 2019** an adoption of **BERT** — an early, pre-ChatGPT language model excellent at *understanding and sorting* text rather than generating it. BERT had been released in late 2018; Woebot adopted it in January 2019 after testing showed it beat their fastText version on accuracy. `[sourced]` ([IEEE Spectrum, 2024-07-02](https://spectrum.ieee.org/woebot))

**Which core techniques are actually used here:** supervised text classification, intent routing, rules-based dialog orchestration, and crisis detection. **None** of the frontier model-building techniques appear — no pre-training, continued pre-training, supervised fine-tuning, reward modeling, RLHF/RLAIF, DPO, or mixture-of-experts. `[sourced]` (their AI page names none of these) `[inference]` (interpreting that absence as "not used")

**How hard is this?** Genuinely moderate, not trivial. Training each classifier to a *regulated medical* standard "required months of effort" — careful data labeling and repeated testing, far more rigor than a hobbyist chatbot. But it is standard applied-ML work, not frontier research. `[sourced]` ([IEEE Spectrum, 2024-07-02](https://spectrum.ieee.org/woebot))

### The genuinely hard part: crisis detection

The most safety-critical component is the **Concerning Language Detection** algorithm. Woebot describes it as a proprietary algorithm that "runs on user input before it is passed to an LLM." When it fires, the normal flow is interrupted to surface hotlines and emergency resources. `[sourced]` (existence, proprietary, runs-before-LLM — [Woebot AI Core Principles](https://woebothealth.com/ai-core-principles/); [Technology Overview](https://woebothealth.com/technology-overview/)) `[inference]` (that it is specifically a "classifier," and that it targets suicidal ideation / self-harm / abuse and was built with clinical psychologists and continually tested — reasonable, but these specifics go beyond what the cited pages state)

Why this is plausibly the hardest part: in mental health a missed crisis signal is potentially fatal, and a system that cries wolf constantly is useless. Tuning that balance, and doing it defensibly enough for clinicians and regulators, is the real labor here — wrap-around difficulty (safety plus clinical validation), not novel-model difficulty. `[inference]` (that this is the hardest part)

### Machine 2 — The research-only generative system: a capable multi-model wrapper

When ChatGPT arrived in late 2022, Woebot built a generative system to keep up — but kept it walled off inside IRB-approved clinical studies, never in the consumer or commercial app. This is where the more impressive engineering lives. `[sourced]` ([IEEE Spectrum, 2024-07-02](https://spectrum.ieee.org/woebot))

What they built, and what it takes:

- **A custom "prompt-execution engine," built in about three months.** Rather than use the popular off-the-shelf framework **LangChain**, they wrote their own. Their stated reason: LangChain "didn't provide a visual user interface like our proprietary system, and it didn't provide a way to safeguard the interactions with the LLM." The engine supports **prompt chains** (breaking a task into a sequence of LLM calls) and plugs the LLM into specific, bounded slots of their existing rules engine. `[sourced]` (rationale and ~3-month build — [IEEE Spectrum, 2024-07-02](https://spectrum.ieee.org/woebot)) `[inference]` (reading "build not buy, in three months" as a signal of competence)
- **Multi-model abstraction across "more than a dozen" models.** The engine can call variously-sized **OpenAI** models, **Azure OpenAI** versions, **Anthropic's Claude**, **Google Bard/Gemini**, and open models like **Meta's Llama 2** run on **Amazon Bedrock.** Being model-agnostic is a sophisticated trait: it lets them pick best-in-class models less prone to hallucination and swap providers. `[sourced]` ([IEEE Spectrum, 2024-07-02](https://spectrum.ieee.org/woebot))
- **Layered guardrails.** The cited source describes the Concerning Language Detection gate running first, custom prompts, and "validation steps preventing off-topic or crisis-related LLM responses," with the LLM confined to narrow, human-reviewed conversational slots and hard instructions such as "don't provide medical advice." `[sourced]` (gate-first, custom prompts, off-topic/crisis validation — [IEEE Spectrum, 2024-07-02](https://spectrum.ieee.org/woebot); [Woebot AI Core Principles](https://woebothealth.com/ai-core-principles/)) `[inference]` (more granular labels like "prompt-injection-resistant architecture" and "maximum-turn enforcement" are not explicitly enumerated in the sources)
- **Clinical-grade evaluation.** In a small "Build study" — a roughly two-week trial — human reviewers found "no concerning LLM-generated utterances" with no evidence the model hallucinated or drifted off-topic, and "equal satisfaction" versus the standard scripted Woebot. The result is encouraging but rests on a short window and small sample. `[sourced]` (findings, 2-week trial — [IEEE Spectrum, 2024-07-02](https://spectrum.ieee.org/woebot)) `[inference]` (any claim that this exceeds typical industry "LLM-as-judge" practice is an unsupported comparison)

### What they do NOT do (so the reader isn't misled)

- **No model training of any kind** — no pre-training, no fine-tuning, no reward models, no RLHF/RLAIF/DPO. They rent finished models. `[sourced]` (no source describes any training) `[inference]`
- **No disclosed cost or latency engineering** as a differentiator — not found.
- **No disclosed RAG or long-term-memory system** — not found.
- **No voice product** — not found.
- **Their valuable data was apparently never used to train or fine-tune a model** — the generative experiments used off-the-shelf hosted models, so the data advantage is in classifier training and clinical evidence, not proprietary weights. `[inference]` (absence of evidence; "apparently never" should be read as "no evidence of," not a proven negative)

### How sophisticated is the wrapper, really?

On a wrapper-quality spectrum, Woebot's research system sits above commodity assembly but well below a frontier lab. The above-average traits are real: a hand-built (not LangChain) multi-model orchestration engine, prompt-chaining, and a disciplined safety-and-clinical-evaluation stack for a regulated, life-safety domain. The unremarkable traits: no fine-tuning, no novel ML, no demonstrated cost/latency/scale engineering, and — decisively — the generative wrapper never shipped to real users.

The irony that defines the company's engineering story: they built a capable generative wrapper but could not deploy it under medical regulation, so the product that actually reached ~1.5M people stayed a pre-ChatGPT classifier-plus-scripts switchboard. `[sourced]` (1.5M lifetime users; original product scripted/non-generative — [STAT, 2025-07-02](https://www.statnews.com/2025/07/02/woebot-therapy-chatbot-shuts-down-founder-says-ai-moving-faster-than-regulators/)) `[inference]` (the connecting narrative)

### Difficulty / talent / cost / data — for THEIR stack

- **Difficulty: 3/5 (low-to-moderate).** The software stack — classify, route, run scripted dialog, plus a thin multi-model LLM orchestration layer — is standard applied-ML and product engineering. The hard parts are clinical-grade safety classification and regulatory/clinical-validation rigor, not the ML or distributed systems. The numeric rating is a directional judgment, not a measured figure. `[inference]`
- **Talent:** applied ML engineers (text classification, BERT), dialog-system engineers, one or more LLM-orchestration engineers, and — critically — safety/ML engineers paired with clinical psychologists, plus regulatory-science and clinical-trial staff. No frontier-research talent needed. `[inference]`
- **Cost:** Woebot raised roughly **$123M** over its lifetime. The spend was most likely dominated by clinical trials, the FDA pathway, and clinician labor rather than compute — they rent inference and ran no training runs. No source breaks down the spend, so the composition is inference. `[sourced]` (~$123M total — Crunchbase) `[inference]` (cost composition)
- **Data scale:** ~1.5M lifetime users and roughly eight years of clinician-authored, IRB-governed conversational and labeled safety data. Strong for classifier training and clinical evidence; no evidence it was converted into any proprietary model. Now static after the consumer app's retirement. `[sourced]` (~1.5M users) `[inference]` (eight-year span and non-use for training)

### Open unknowns

- **Exact current (2026) production stack post-pivot** — not found. The cited STAT article confirms the original product was scripted and non-generative but does not establish today's live stack.
- **Whether any generative capability has shipped to enterprise customers as of 2026** — not found; available evidence points to no, but this is inference, not confirmation.
- **Exact shutdown timing** — reported around early July 2025; whether the wind-down was effective in late June versus July is not cleanly settled in the cited source.
- **Headcount and which engineers remain post-pivot** — not found.

**Engineering moat:** Shallow on the AI itself (a rent-the-models wrapper that never shipped), but real and defensible in the wrap-around layer — clinical-grade safety classification plus regulatory and clinical-validation rigor that competitors cannot shortcut.

Sources:
- IEEE Spectrum, "Woebot," 2024-07-02 — https://spectrum.ieee.org/woebot
- Woebot AI Core Principles — https://woebothealth.com/ai-core-principles/
- Woebot Technology Overview — https://woebothealth.com/technology-overview/
- STAT News, 2025-07-02 — https://www.statnews.com/2025/07/02/woebot-therapy-chatbot-shuts-down-founder-says-ai-moving-faster-than-regulators/
- MobiHealthNews — https://www.mobihealthnews.com/news/woebot-health-shutting-down-its-app
- Crunchbase (funding total)


## Therabot (Dartmouth)

Therabot is not a company — it is a Dartmouth academic research project, and unusually for AI therapy, its creators published the engineering recipe in a peer-reviewed paper (NEJM AI, March 2025) [sourced]. That gives us a primary source for the clinical claims. Two important caveats up front, from the verifier: the NEJM paper itself was not directly retrievable (paywalled), and the most specific technical details about the AI stack come from a single co-author's personal blog, not the reviewed paper. So we will be careful to separate "verified" from "single-source claim."

### The core build: borrowed engines, lightly retuned

Therabot does not build its own AI model from scratch. According to a co-author's technical blog, it takes two existing open-weight models — Falcon-7B and LLaMA-2-70B — and uses them "in tandem" [contested: this base-model pairing comes from a co-author Medium blog and could not be confirmed in the NEJM paper or any other accessible source; treat as a claim, not a fact]. Think of these as two pre-built engines off the shelf: the team did not design the engines, they retuned them. In the technical sense, that makes Therabot a *wrapper* — it stands on third-party foundation models.

But if the description holds, it is a substantial wrapper, not a thin one. Rather than just sending clever instructions to a hosted chatbot (how a typical "GPT app" works), the team reportedly modified the models' internal weights using a technique called QLoRA — a cheap, efficient way to teach an existing model new behavior by adjusting a small slice of it instead of retraining the whole thing. The exact settings (4-bit compression, "rank-64" adapters, a single mid-range AWS GPU, ~2,048-token context window) appear in the co-author's blog [contested: blog-sourced, not in the peer-reviewed paper, not independently confirmed]. Worth flagging: a separate third-party "Falcon-7B medical QLoRA" project circulates online and is *not* Therabot — easy to confuse, so the blog details should not be over-trusted.

If those details are accurate, the method itself is well-trodden — the kind of fine-tuning a competent applied engineer can run from public tutorials. The genuine value would then sit not in the algorithm but in what they trained it on. (That "method is commodity" judgment is an editorial inference, and it rests on the unverified technical stack above.)

### Where the real difficulty lives: hand-written therapy data

The hard, expensive, irreproducible part is the training data, not the AI. The team hand-wrote a large set of expert therapist-patient dialogues grounded in "third-wave" CBT, reviewed by a board-certified psychiatrist and a clinical psychologist [sourced]. Tellingly, they first tried two cheaper shortcuts — scraping mental-health internet forums, then using real therapy-session transcripts — and threw both out because the results were poor [sourced: MIT Technology Review]. That failed trial-and-error, plus the sheer labor of authoring clinically-correct dialogue, is the real moat.

How big was that labor? Reported figures are 100,000+ human hours by a roughly 100-person team [sourced — but note: these are institution-promoted PR figures, not independently audited; a separate "60+ contributors" count could not be confirmed]. The development span is given inconsistently across sources as either five or six years (Dartmouth says "in development since 2019"); both figures coexist and the discrepancy is unresolved [contested]. Either way, the therapeutic skill is encoded in the *data*, not in any clever algorithm [inference].

### Serving and scale: barely engineered, and that is fine

Therabot reportedly ran on standard AWS SageMaker endpoints; the "memory" was simply pasting prior messages back into the prompt — the simplest possible approach, with no retrieval system (RAG) or vector database disclosed [contested: serving specifics again trace to the co-author blog]. And it did not need more: the trial served 106 people in the treatment arm of a 210-person study (106 Therabot / 104 control) [sourced]. At that scale there is no need for the cost, latency, or throughput engineering a real consumer product demands. This dimension is essentially commodity assembly [editorial inference].

### Safety: a custom crisis classifier plus live humans

This is one of two areas of genuine effort. Instead of relying on the base model's generic guardrails, the team built a separate "crisis classification model" to detect escalating risk (e.g., suicidal ideation) and trigger an on-screen emergency module with one-tap buttons to 911, the 988 Lifeline, and the Crisis Text Line [sourced: NEJM AI; CrisisTalk]. Notably, when crisis language appears, Therabot keeps talking *and* alerts a human, rather than shutting the conversation down like many commercial bots [sourced: CrisisTalk]. Roughly two of the five development years went into safety [sourced: CrisisTalk]. Specific classifier accuracy numbers (sensitivity, precision) are not available in retrievable sources [speculation/unknown]. A 2026 preprint on LLM crisis-risk detection suggests this remains an active research line, though its full text was not retrievable and its tie to the deployed classifier is inferred [inference].

The other half of safety was brute-force human oversight: every Therabot message in the trial was reviewed by trained clinicians after it was sent, and staff intervened 28 times (15 for participant safety, 13 to correct bad responses such as offering medical advice) [sourced]. Rigorous — but explicitly *not* an autonomous system, as the investigators themselves state.

### Clinical evaluation: the genuinely strong part

Where Therabot is far ahead of typical AI startups is evaluation. They ran a real randomized controlled trial (N=210), IRB-approved and pre-registered, with validated clinical instruments and proper statistics [sourced — but with a caveat: the specific instruments named (PHQ-9, GAD-Q-IV, Weight Concerns Scale) and methods (cumulative-link mixed models, Holm-Bonferroni) come solely from the paywalled paper and could not be independently confirmed; they are standard and plausible, but treat as "per paper, unverified here." GAD-Q-IV vs GAD-7 specifically could not be confirmed]. This is a different universe from the A/B tests most chatbot companies run. One real caveat: the control group simply had no access to Therabot, and independent commentators argue a no-treatment ("waitlist"-style) control inflates the apparent benefit [contested — and note the word "waitlist" is not verbatim-confirmed in accessible sources; it is itself partly an inference].

### What they do not appear to use (for calibration)

Based on the published methods, there is no evidence Therabot uses continued pre-training, reward modeling (RLHF/RLAIF/DPO), mixture-of-experts routing, RAG/external memory, voice, or LLM-as-judge automated evals. These are reasonable inferences from absence — "no evidence" is not the same as "confirmed absent," and the alignment-via-curated-data claim depends on the unverified blog [inference].

### Bottom line for a non-technical reader

Therabot is a thoughtful, clinically serious fine-tuning project built on borrowed AI engines. The AI/ML engineering — assuming the blog-sourced description is accurate — is largely commodity work a skilled applied team can reproduce from public recipes. The genuinely hard, defensible, expensive parts are profoundly un-glamorous: hand-authoring a huge corpus of clinically correct therapy dialogue, building a bespoke crisis-detection safety net, and validating the whole thing through a real randomized clinical trial. It earns a 4/5 difficulty (a subjective rating, not a measured fact) not for ML novelty but for the depth of clinical data work and the rigor of clinical validation — areas where most "AI therapy" competitors do far less.

**Engineering moat:** Not in the AI — the moat is the years of hand-built clinical training data and the real randomized trial behind it; the model engineering is commodity, and even that rests on a single unverified co-author blog.

### Sources
- NEJM AI, Heinz et al. (March 2025): https://ai.nejm.org/doi/full/10.1056/AIoa2400802 (mirror: https://gwern.net/doc/psychiatry/depression/2025-heinz.pdf)
- Co-author technical blog (QLoRA / Falcon-7B specifics; single-source): https://medium.com/@yinzhouw22/building-a-conversational-ai-with-memory-on-aws-series-fine-tune-qlora-falcon-7b-with-dialogue-3b4703a74722
- CrisisTalk (safety design, "two of five years"): https://talk.crisisnow.com/the-generative-ai-therapy-chatbot-will-see-you-now/
- MIT Technology Review (failed data approaches, trial framing): https://www.technologyreview.com/2025/03/28/1114001/the-first-trial-of-generative-ai-therapy-shows-it-might-help-with-depression/
- medRxiv crisis-detection preprint (Jan 2026, full text not retrievable): https://www.medrxiv.org/content/10.64898/2026.01.12.26343914v1.full
- ClinicalTrials.gov registration: https://clinicaltrials.gov/study/NCT06013137


---

# Part C — Compensation Reality: Disclosed Floor vs. Likely Real

_The public figures in the market report (~$200–225K) are unreliable **floors**. The right-hand "likely real" numbers are **inference** — built from frontier-lab comparables, equity math at each company's valuation, retention dynamics, and firsthand industry input. Verifier confidence: medium. Not disclosed fact._


## COMPENSATION REALITY

### How to read this section (plain-language)

The earlier market report quoted pay of roughly **$200,000–$225,000 total compensation** for engineers at these companies. **Treat those as a FLOOR, not the truth.** They come from two public sources that are known to *understate* what people actually take home:

1. **H1B / LCA filings** — government visa paperwork. By law these show **base salary only**: no stock, no bonus, no signing/retention money. For a startup engineer, base is often *half or less* of total pay.
2. **levels.fyi** — voluntary self-reports. Coverage is thick for big public tech (Google, Meta) but **thin and patchy for small private companies**, and the equity it does show is a guess at illiquid private stock — frequently logged as **$0** when the reporter doesn't know the value.

So the public number is a *disclosed floor*. The *likely real* number is higher — sometimes far higher — once you add equity, bonus, and retention/liquidity packages that simply don't appear in those two sources.

> **Everything in the "LIKELY REAL" column below is INFERENCE.** It is reasoned from frontier-lab comparables, each company's funding/valuation, and an informed-industry premise (below). It is **never a disclosed fact.** Where a company actually published a number, it is labeled and sits in the "DISCLOSED FLOOR" column.

---

### The method (how the "LIKELY REAL" column is built)

The inference rests on four pillars, each shown so a non-technical reader can check the logic:

**Pillar 1 — Frontier-lab comparables (the ceiling for elite AI/ML talent).** `[sourced]`
At the top AI labs, total compensation for research engineers/scientists in 2026 is *multiples* of the $200K floor — and the genuinely elite ICs clear **$1M+**:
- **OpenAI:** software-engineer TC ~$249K (junior) to **$1.23M+** (senior); median engineer TC reported ~$555K, research scientists ~$771K–$1.47M+. `[sourced — levels.fyi / jobsbyculture, 2026]`
- **Anthropic:** engineer TC ~$300K–$759K; senior research scientists (L5) ~$700K–$950K, and L6+ alignment/frontier researchers **routinely >$1.5M** when tender-priced equity is counted (Anthropic valued ~$61.5B). `[sourced — ctaio / jobsbyculture / levels.fyi, 2026]`
- **Google DeepMind:** L4 ~$280K–$360K, L5 ~$475K–$625K, **L7 >$1M–$1.4M** TC (US; London ~30–40% lower in USD). `[sourced — jobsbyculture / levels.fyi, 2026]`

These are the comparables a "top engineer" at a well-funded AI-therapy company is benchmarked against and recruited away from. The closer a company is to genuine frontier AI work and the better-funded it is, the more its top ICs converge toward these numbers. `[inference]`

**Pillar 2 — Equity math at each company's valuation.** `[inference]`
Total comp at a private startup ≈ **base + (annual equity value) + bonus + retention**. The public floor captures only base. Annual equity value scales with valuation and stage:
- A multi-billion-dollar, late-stage company (Lyra ~$5.6B, Spring ~$3.3B) can grant equity worth **$100K–$500K+/year** to senior/staff engineers, none of which reliably appears in levels.fyi or LCA data. `[inference]`
- An early-stage company (seed/Series A) substitutes *larger equity percentages on a smaller, riskier base* — high paper upside, low liquidity. `[inference]`
- A public company (Talkspace) or a subsidiary of one (BetterHelp/Teladoc) has *liquid* stock, so the gap between floor and real is smaller and more verifiable. `[inference]`

**Pillar 3 — Retention & liquidity dynamics.** `[inference]`
Because elite AI talent is being actively poached by the frontier labs in Pillar 1, well-funded firms layer on **retention grants, refreshers, and above-band "top-of-market" offers** to keep key people. Several dossiers show direct evidence of this premium (e.g., a Slingshot $250K *base* LCA for a plain "Software Engineer," well above NY market median, plus a stated "top-of-personal-market / ~90th-percentile" pay philosophy). `[sourced — h1bdata.info; api.ashbyhq.com]` These dynamics push *real* comp for the few critical ICs well above the median band.

**Pillar 4 — The insider premise (informed industry context, treated as a credible premise to corroborate, not as published fact).** `[inference / premise]`
At several of these firms, **top engineers reportedly earn MORE THAN $1,000,000 total compensation**; exact figures are undisclosed. This is consistent with Pillars 1–3: a single elite AI/ML lead at a richly funded company, benchmarked against OpenAI/Anthropic/DeepMind and retained with equity + retention, plausibly clears $1M TC even though the *published* figure says ~$200K. The premise is **corroborated in direction** by the frontier-lab data, **not independently confirmed for any named individual at any named company here.** `[inference]`

**Where the premise does NOT apply (important caveat).** `[inference]`
The $1M+ ceiling is for **elite AI/ML ICs at the well-funded, frontier-leaning firms.** It does **not** describe the typical engineer, non-AI roles, clinical staff, sub-scale seed companies (Earkick, Sonia, Youper, Woebot post-pivot), India-based engineering orgs (Wysa), or academic labs (Therabot). For those, the floor is much closer to reality. Spreading "$1M+" across every row would itself be a distortion.

---

### Two-column model — market level

| | DISCLOSED FLOOR (public, **unreliable floor**) | LIKELY REAL (inferred total comp) | Basis |
|---|---|---|---|
| **Typical IC engineer, well-funded AI-health firm** | ~$180K–$225K TC (levels.fyi); ~$155K–$200K base (LCA) `[sourced]` | ~$250K–$450K TC (base + private equity + bonus) `[inference]` | Equity not captured in floor; Pillar 2 |
| **Senior/Staff IC** | ~$220K–$250K `[sourced]` | ~$400K–$700K TC `[inference]` | Frontier-lab senior band, discounted for liquidity; Pillars 1–3 |
| **ELITE AI/ML IC / AI lead (the few)** | ~$200K–$250K (if shown at all) `[sourced]` | **$1M+ TC** at the richly-funded firms `[inference / premise]` | Pillars 1, 3, 4 — corroborated in direction by OpenAI/Anthropic/DeepMind $1M–$1.5M+ elite bands |

---

### Two-column model — per company

Floor figures are **base-only LCA and/or thin levels.fyi self-reports** unless noted. "LIKELY REAL" is **inference**, calibrated by each firm's valuation/stage (the lever for equity) and how frontier-leaning its AI work is. "$1M+ ceiling" appears only where funding + AI-talent intensity make it plausible.

| Company (product) | Stage / valuation | DISCLOSED FLOOR — public, **unreliable** | LIKELY REAL — **inference** | Method / basis for the inference |
|---|---|---|---|---|
| **Slingshot AI (Ash)** | Series A, **$93M raised**, valuation undisclosed `[sourced]` | SWE NY **base $250K** (1 LCA); levels.fyi none; bands "Not specified" `[sourced]` | IC senior ~$350K–$600K TC; **elite AI/ML lead plausibly $1M+** `[inference / premise]` | $250K *base* alone is ~90th-pct → "top-of-market" stated philosophy; real frontier-leaning AI work on open-weight LLMs; Pillars 1,3,4 |
| **Spring Health (Guide)** | **~$3.3B** valuation, Series E `[sourced]` | SWE ~$208K median TC; Eng Mgr ~$200K–$246K (levels.fyi, **equity often $0-logged**) `[sourced]` | Senior IC ~$350K–$600K; staff/AI lead **approaching/over $1M** `[inference]` | $3.3B valuation supports large unreported equity; lean ~180-person eng org → key ICs command retention; Pillars 1–3 |
| **Limbic** | Series A, **~$14–22M raised**, valuation undisclosed `[contested]` | None company-specific; valuation undisclosed `[sourced]` | IC ~£70K–£140K+ (UK) → ~$250K–$450K TC for senior; elite lead lower-probability $1M `[inference]` | UK-based (London comp ~30–40% below US frontier); smaller raise caps equity upside vs. US peers; Pillars 1–2 |
| **Jimini Health (Sage)** | Seed, **~$25M+ raised**, valuation undisclosed `[sourced]` | Senior SWE (Backend) **$185K–$250K base + equity** (posted); LCA 0; levels.fyi none `[sourced]` | Senior IC ~$300K–$550K TC; AI lead higher-end, $1M only if outlier `[inference]` | Posted band is base+equity at-market for funded seed; smaller raise → equity is upside not cash; Pillars 1–3 |
| **ieso (Velora)** | Series B (**$53M** corroborated), valuation undisclosed `[sourced]` | **None** — no LCA, no levels.fyi page; Boston-market *estimates* only ($130K–$300K base) `[inference]` | Senior/Staff ML ~$280K–$450K TC; VP AI higher; $1M only as rare outlier `[inference]` | UK/Boston Series-B stage; non-replicable data moat but not frontier model R&D; equity additive-but-unknown; Pillars 1–2 |
| **Wysa** | Series B (**$20M**), ~$82M valuation (2023, aggregator) `[sourced/cautious]` | SWE **India** median ~₹1.81M (~$22K); SWE Mgr ~₹6.12M (~$73K); zero US LCA `[sourced]` | India eng core well below US bands; US/UK GTM leaders unknown — **$1M+ premise does NOT apply** `[inference]` | Engineering is India-based (INR scales); not a US frontier-pay market; Pillar 4 exclusion |
| **Lyra Health** | **~$5.6B** (Series F), 20M+ members `[sourced]` | SWE ~$222K–$225K median TC; Eng Mgr ~$235K; VP Data & AI posted **$251K–$346K base** `[sourced]` | Senior IC ~$350K–$550K; staff/AI-platform lead **$700K–$1M+** `[inference]` | $5.6B valuation → material illiquid equity above levels.fyi; VP AI org "still being assembled" at $251K–$346K *base* signals premium hiring; Pillars 1–3 |
| **Talkspace (Tee)** | **Public (Nasdaq: TALK)**; pending UHS buyout ~$835M `[sourced]` | SWE ~$219K–$225K TC (levels.fyi); ~$116K avg base (Glassdoor); LCA $155K (2022) `[sourced]` | Senior IC ~$250K–$400K TC; AI-lead exec pay in **proxy/DEF 14A (not retrieved)** `[inference / not found]` | Public co → equity is *liquid* and partly disclosable, so floor↔real gap is **smaller and more verifiable**; $1M+ less likely outside named execs; Pillars 2–3 |
| **SonderMind** | Series C, **~$1.1B** (2021, possibly stale) `[sourced/flagged]` | SWE ~$111K–$117K median TC (levels.fyi, **runs low**); Principal AI Eng **$160K–$190K** (posted) `[sourced]` | Senior/Principal AI ~$250K–$400K TC; $1M+ unlikely `[inference]` | Unusually *low* levels.fyi here; ~$1.1B valuation is 2021-vintage, down-round risk → modest equity upside; Pillars 1–2 |
| **Youper** | Seed only (~$3.5M–$5.2M); **contracted to ~4–15 staff** `[contested/inference]` | **None real** — modeled estimates only (CSO ~$277K–$357K *modeled*; full-stack ~$73K–$92K) `[speculation]` | Below-market for a capital-constrained, contracting firm; **$1M+ premise does NOT apply** `[inference]` | No funding since 2019; tiny headcount → cash-constrained; Pillar 4 exclusion |
| **Sonia** | Pre-seed/seed (~$3.35M); ~7–23 staff `[sourced/inference]` | **None reliable** — aggregator financials mis-scraped/unusable `[sourced]` | Small-team market pay + early equity; **$1M+ does NOT apply** `[inference]` | Sub-scale early stage; no valuation disclosed; Pillar 4 exclusion |
| **Headspace (Ebb)** | 2021 merger **~$3B** (**STALE**; possibly marked to ~$1B) `[contested]` | Senior SWE median ~$165K; Senior ML ~$186K (LCA); SWE TC ~$180–190K, **equity $0-logged** (levels.fyi) `[sourced]` | IC ~$200K–$320K TC; senior/lead higher; $1M+ unlikely given down-round pressure `[inference]` | Stale/possibly-marked-down valuation + repeated layoffs cap equity value; cash-heavy packages; Pillars 1–2 |
| **BetterHelp (Teladoc)** | Subsidiary of **public Teladoc (TDOC)**; ~$1B FY24 segment-linked loss `[sourced]` | **None standalone** — embedded in Teladoc; team/headcount unknown — not found `[sourced]` | Comp on Teladoc public-company scale; equity is *liquid* TDOC stock; $1M+ only named execs `[inference]` | Public-parent → equity liquid/disclosable; AI is "bolt-on," not frontier → less elite-IC premium; Pillars 2–3 |
| **Earkick** | Seed, **~$1.56M** raised; **~8 staff** (US/Switzerland) `[sourced]` | **None** — 0 LCA, no levels.fyi; SF benchmark ~$274K avg cited as a **ceiling** `[sourced]` | Below SF medians; equity-heavy on tiny base; **$1M+ does NOT apply** `[inference]` | ~8-person seed; Swiss-side staff on Swiss scales; Pillar 4 exclusion |
| **Woebot Health** | Series B **$90M** (2021), valuation undisclosed; **post-pivot contraction** `[sourced/inference]` | Senior Platform Eng $150K; SWE ~$90K–$125K (LCA/Glassdoor); levels.fyi none `[sourced]` | Pre-pivot senior ~$200K–$320K TC; **post-2025 pivot comp unknown — not found**; $1M+ unlikely `[inference]` | Consumer-app shutdown + enterprise pivot signals contraction → little equity upside; Pillars 1–2 |
| **Therabot (Dartmouth)** | **Academic lab** — no venture funding, no valuation `[inference]` | Dartmouth-wide LCA: SWE ~$96K–$111K; Research Scientist ~$53K–$77K; **PI pay not in public sources** `[sourced/inference]` | Academic/grant scale, **far below industry**; **$1M+ does NOT apply** `[inference]` | University lab, not a startup; no equity instrument; Pillar 4 exclusion |

---

### Bottom line for a non-technical reader

- The published **~$200K–$225K** figures are a **floor**, and an unreliable one — they capture base pay and thin self-reports, **not** the equity, bonuses, and retention that dominate real packages at well-funded private AI companies. `[inference, basis shown]`
- At the **richly-funded, frontier-leaning firms** (Slingshot, Spring, Lyra; possibly Jimini), the **handful of elite AI/ML engineers plausibly clear $1M+ total compensation** — *consistent with*, and benchmarked against, the corroborated OpenAI/Anthropic/DeepMind elite bands of $1M–$1.5M+. This is **inference corroborated in direction, never a disclosed fact for any named person.** `[inference / premise]`
- At the **sub-scale, contracting, India-based, or academic** firms (Earkick, Sonia, Youper, Wysa, Woebot post-pivot, Therabot), the floor is close to reality and the **$1M+ ceiling does not apply.** `[inference]`
- **Hard, disclosed facts remain scarce:** for most of these private firms exact total-comp and executive pay are **unknown — not found**, and even the public floors are dated (several 2021–2023 LCA vintages). The two-column gap is itself the finding: *what's published materially understates what elite AI talent is really paid.* `[inference]`


---

# Part D — Global Talent Map


# The Global Talent Map: Who Can Actually Build AI Therapy

*A guide for non-technical readers. As of 2026-06-24.*

The short version: building a real AI-therapy model (as opposed to wrapping someone else's chatbot in a friendly app) requires a stack of five very hard technical skills. The people who can do each of them well number — at the very top — in the **hundreds to low thousands worldwide**, and they are clustered in a handful of cities inside a handful of organizations. Those same people are the ones frontier AI labs are paying **$500K to over $1M a year** (and, for a tiny elite, far more) to keep. An AI-therapy startup is, whether it likes it or not, bidding against OpenAI and Meta for the same scarce humans — and usually cannot match the price.

---

## The five hard techniques (in plain terms)

| Technique | What it means in plain English | How AI therapy uses it |
|---|---|---|
| **Continued pre-training** | Taking a large base model and feeding it more specialized data to shift what it "knows" at a deep level. | Adapting a general model toward psychology/therapy language. |
| **RLHF / reward modeling** | Teaching the model what "good" looks like by training a separate "judge" model on human preferences, then optimizing against it. | Making responses sound like a skilled, safe therapist rather than a generic chatbot. |
| **MoE serving** | Running "Mixture-of-Experts" models — giant models that only switch on the relevant parts per query — fast and cheaply in production. | Serving therapy conversations at low cost and low latency. |
| **Safety / eval engineering** | Building tests and "red teams" that probe for harmful, unsafe, or wrong outputs before and after release. | Critical here: a wrong answer can mean self-harm or crisis mishandling. |
| **Clinical data pipelines** | Collecting, anonymizing (HIPAA), and expertly labeling real therapy data to train on. | The actual differentiator — real therapeutic conversations, labeled by clinicians. |

A key nuance: these are **different talent pools**. The person who can do continued pre-training is usually *not* the same person who can do MoE serving optimization, who is *not* the licensed clinician labeling transcripts. A company needs several scarce specialists, not one unicorn.

---

## Who can actually do each — named orgs and the kinds of people

### 1. Continued pre-training & 2. RLHF / reward modeling (the scarcest tier)

These are the "train a frontier model from the inside" skills, and they are the bottleneck of the entire industry.

- **Where the expertise lives:** OpenAI, Anthropic, Google DeepMind, Meta (Superintelligence Labs / FAIR), xAI, Mistral (France), and **DeepSeek** (China). RLHF itself was pioneered at exactly this set — OpenAI (InstructGPT/ChatGPT), Anthropic (Claude), DeepMind (Sparrow/Gopher). *[sourced]*
- **Kind of person:** PhD- or equivalent-level ML researchers and "members of technical staff," often with published work at NeurIPS/ICML, frequently foreign-born and US- or China-trained. DeepSeek's team is described as "small, young, recruited largely from top Chinese universities." *[sourced]*
- **How scarce:** One industry estimate is that **only "a few hundred people can credibly train a frontier model."** A separate systematic study (mining ~3M professional profiles) estimates roughly **3,000–5,000 people globally** have the technical capability to do frontier ML research / train large models — and that the very top tier is "extremely scarce," ~0.1–0.2% of the technical workforce. *[sourced — but see caveat below]* The core *modeling* teams inside labs are deliberately tiny; a focused post-training effort can be "2–4 engineers." *[sourced]*

### 3. MoE serving (the production-infrastructure tier)

- **Where the expertise lives:** The frontier labs (who run their own MoE models — DeepSeek-V3, Mistral, etc.), plus the open-serving ecosystem: the **vLLM** project, NVIDIA (TensorRT-LLM), and infrastructure partners like **Together AI**. *[sourced]*
- **Kind of person:** Systems/GPU engineers who understand parallelism, KV-cache, expert load-balancing, FP8 quantization. This is elite distributed-systems work, not ML research.
- **Why it matters for therapy:** It is the main reason AI-therapy startups *rent* this skill instead of hiring it. Slingshot AI, for example, **ran its fine-tuning on Together AI's infrastructure**, with the founders explicitly framing the alternative as "just a matter of headcount." *[sourced]*

### 4. Safety / eval engineering

- **Where the expertise lives:** In-house safety teams at the frontier labs, plus specialist orgs like **FAR.AI**, **Scale AI** (frontier evals), and academic/nonprofit alignment groups. Microsoft AI publicly recruits "AI Safety Post-Training" staff. *[sourced]*
- **Kind of person:** A hybrid of ML researcher and adversarial-security mindset; the field is young enough that practitioners "had to develop homegrown taxonomies of harms." *[sourced]*
- **Why it's acute for therapy:** In a therapy product, an eval failure isn't an embarrassing tweet — it's a missed suicide-risk signal. This raises the bar far above a normal consumer chatbot.

### 5. Clinical data pipelines (the one pool *outside* the AI labs)

- **Where the expertise lives:** This is the talent AI-therapy startups can *actually* win, because frontier labs don't compete for it. Slingshot built "the largest dataset of its kind of clinically relevant data" and hired clinical leadership (e.g., a Head of Clinical from Noom/Talkspace). *[sourced]*
- **Kind of person:** Licensed psychologists, clinical social workers, doctoral-level clinical students doing expert annotation — plus data engineers handling HIPAA anonymization. Academic studies in this space rely on board-certified psychologists and doctoral students to label therapy utterances. *[sourced]*
- **Scarcity is different:** Not "hundreds in the world," but expensive and slow — clinical annotation is "slow, expensive, and error-prone." *[sourced/inference]*

---

## Geographic concentration

- **Top researchers work in the US (59%), China (11%), UK (6%), Germany (4%), India (2%).** *[sourced — MacroPolo Global AI Talent Tracker; note: archived dataset, figures predate 2025; treat as directional]*
- US institutions' lead is "built almost entirely on foreign-born talent"; **72% of top China-trained researchers end up working in the US.** *[sourced]*
- The live research frontier is concentrated in **three hubs: the San Francisco Bay Area, Beijing, and Shanghai**, with London, New York and Paris as secondary centers. San Francisco has the densest AI-professional concentration (~23.9 per 1,000 residents). *[sourced]*
- For an AI-therapy startup, this geography is brutal: the talent you need sits in the most expensive, most competed-for labor markets on earth, surrounded by the very employers outbidding you.

---

## The compensation reality — why scarcity = >$1M

Because the top pool is tiny and the labs are flush with capital, pay has detached from normal software-engineering norms:

- **Frontier-lab software engineers: ~$600K–$795K median total comp** (Levels.fyi via industry reports, ~May 2026). *[sourced]*
- **OpenAI senior (L5): ~$1.15M** total comp ($336K base + ~$774K stock); senior ICs reaching ~$1.28M. *[sourced — note: a second source put OpenAI senior nearer $843K; figures are contested/source-dependent]* *[contested]*
- **Anthropic:** median ~$600K; senior researchers "regularly clear $1M once secondary tender offers are counted." *[sourced]*
- **Equity is now 40–70% of the package** — the real money is the lab's soaring private valuation, something a healthcare startup's equity cannot mirror. *[sourced]*
- **The extreme tail:** Andrew Tulloch reportedly joined Meta's Superintelligence Labs in a deal valued ~**$1.5 billion over six years**; individual offers to move elite people have escalated "from millions to hundreds of millions to, in some cases, potentially billions." *[sourced]*
- The causal link is stated plainly by industry analysts: *"only a few hundred people can credibly train a frontier model, and labs that raised at $32B or $350B–$1T will pay almost anything to keep them."* That sentence **is** the scarcity-to-comp mechanism. *[sourced]*

---

## Why AI-therapy companies must compete — and usually can't afford to

1. **Same humans, different budgets.** If a therapy startup wants genuine continued-pre-training or RLHF in-house, it must hire from the *exact* ~few-hundred-to-few-thousand pool the frontier labs are paying $1M+ to retain. *[inference, grounded in sourced figures]*
2. **The money gap is structural, not negotiable.** Mainstream AI/ML engineers earn $170K–$245K; frontier-lab engineers clear $600K–$795K. A venture-funded startup (Slingshot has raised ~$93M total) cannot run many $1M seats and survive — frontier labs have raised tens to hundreds of billions. *[sourced]*
3. **Documented bleed.** Healthcare/insurance/logistics are explicitly cited as industries that "can't compete on salary"; one healthcare-analytics firm saw **25% AI-team turnover in 2025** as big tech made "2x offers." *[sourced]*
4. **The rational workaround (what they actually do).** Don't fight for the pre-training elite. Instead: (a) **rent** the MoE-serving and base-model layer (Slingshot fine-tunes on Together AI rather than building bare-metal infra); (b) do the cheaper **fine-tuning/DPO** rather than full pre-training; (c) **own the one pool the labs ignore** — clinical data and licensed-clinician annotation, which is their real moat. *[sourced for Slingshot specifics; inference for the generalization]*

So the competitive truth is asymmetric: AI-therapy companies **compete with frontier labs for the scarce ML-research talent and lose**, so they **route around it** by buying the model/infra layer and concentrating their own hiring on clinical expertise, which the labs don't want.

---

## Important caveats and unknowns

- **The "3,000–5,000 global / 0.1–0.2%" figures** come from a single WebFetch summary of an arXiv preprint (2603.00062). I could not independently re-verify the exact numbers against the paper's text in this session — **treat as directional, not authoritative.** *[contested]*
- **The MacroPolo geography percentages** are from an *archived* version of the tracker; the underlying survey predates 2025. Direction is reliable; exact 2026 percentages are **unknown — not found.** *[contested]*
- **Headcount and named individuals on AI-therapy technical teams** (e.g., who specifically does Slingshot's RLHF, or whether any therapy startup does true continued pre-training in-house): **largely unknown — not found.** Public sources confirm Slingshot does SFT+DPO fine-tuning, not that it does frontier pre-training.
- **Whether any AI-therapy company employs frontier-tier pre-training researchers at $1M+ comp:** **unknown — not found.** The evidence points the other way (they rent infra, do fine-tuning).
- One source ($843K OpenAI senior) **conflicts** with another ($1.15M); I have flagged this rather than pick one. *[contested]*


---

## Part E — Engineering-Lens Difficulty Re-Rating & Real Moats

**The lens.** Part 1 rated raw engineering difficulty on a 1–5 scale (1 = thin wrapper around a rented model, 5 = frontier AI research). No one in this field scored a 5 — there are no frontier-AI players here. Part E asks a sharper, money-relevant question: *of the engineering that exists, how much is genuinely hard-to-copy, and how much is commodity assembly that any competent team could rebuild?* A company can score modestly on raw difficulty yet still be highly defensible, because its moat is data or safety rigor rather than model cleverness. Below, companies are sorted into three tiers by real engineering substance, then each gets its true moat in one line.

**Reconciliation note.** This re-rating is consistent with the Part-1 difficulty ranking (Report Section 3): the 4/5 cluster (Limbic, Jimini, ieso, Therabot) maps to the top tier here, the 2/5 floor (Youper, BetterHelp, Earkick) maps to the bottom, and the 3/5 middle band splits depending on whether a company's hard work is real-but-non-AI (kept mid) or thin (pushed down). Where the source digest showed garbled inflated figures (e.g., Jimini "6/5," ieso "6/5"), I defer to the authoritative Part-1 ranking; the substantive ordering is unchanged. The one deliberate refinement: Slingshot, rated 3/5 in Part 1 on the model layer, rises in *moat* terms because its proprietary-data position is among the strongest in the cohort even though its model work is a heavy fine-tune.

---

### Tier 1 — Genuine, hard-to-copy engineering (real moats)

These earn their standing not through novel AI but through safety-and-evaluation rigor, regulatory validation, and proprietary clinical data that takes years to assemble.

- **Limbic (Part 1: 4/5).** Real moat: a regulated medical-device credential (Class IIa) plus ~53,448 hand-labeled clinical data points and hundreds-of-thousands-of-patients NHS deployment data — clinical claims competitors literally cannot make.
- **Therabot / Dartmouth (Part 1: 4/5).** Real moat: a large corpus of expert therapist-patient dialogues hand-written and reviewed over years, plus the only published generative-therapy RCT — the data and the evidence are the moat, not the architecture.
- **ieso / Velora (Part 1: 4/5).** Real moat: a ~25-year, outcomes-indexed library of real online-CBT therapy (750k+ hours / ~1B words) linked to clinical results — a dataset no newcomer can backfill at any price.
- **Jimini / Sage (Part 1: 4/5).** Real moat: a bank of fine-tuned safety classifiers and an LLM-as-judge pipeline gated by an in-house clinic as a quality check — modest data scale, but real safety engineering.

### Tier 2 — Real engineering, but mostly outside the AI (defensible via data, distribution, or regulated pipelines)

The hard work here is genuine but is data accumulation, clinical-outcomes tracking, or regulated infrastructure — not the model. Several score 3/5 on raw difficulty yet remain defensible.

- **Slingshot / Ash (Part 1: 3/5; moat stronger than the rating implies).** Real moat: a large corpus of de-identified real psychotherapy transcripts plus expert preference data — the compounding data assets, not the Qwen3 fine-tune, are the company.
- **Spring Health (Part 1: 3/5).** Real moat: longitudinal, repeated clinical-outcome measurements (PHQ-9 / GAD-7 tracked over time) across ~10M lives — though its "validated matching ML" claim is overstated.
- **Lyra Health (Part 1: 3/5).** Real moat: a decade of labeled clinical-outcomes data across ~20M served members feeding a unified data lakehouse — scale and payer distribution, not model R&D.
- **Talkspace (Part 1: 3/5).** Real moat: ~12 years of mental-health interaction data (~140M messages, 6.2M assessments, 4.3M notes) wired to a live human-escalation safety classifier since 2019.
- **SonderMind (Part 1: 3/5).** Real moat: proprietary behavioral-health data flowing through a regulated (HIPAA/ISO 27001) pipeline, enriched by acquired clinical/ML assets (Mindstrong, Total Brain).
- **Wysa (Part 1: 3/5).** Real moat: a large domain-specific corpus (500M+ AI conversations, 5M+ users across ~90 countries) powering its rule-engine and routing models at regulated scale.
- **Woebot Health (Part 1: 3/5).** Real moat: ~1.5M lifetime users and ~8 years of clinician-authored, IRB-governed conversational and safety-labeled data — a genuine classifier asset, now a legacy/enterprise play.

### Tier 3 — Commodity assembly (thin or easily reproduced moats)

Capable products, but built mostly from rented models and public material; the defensible engineering is minimal and the hard problems (safety, regulation) are deliberately sidestepped.

- **Headspace / Ebb (Part 1: 3/5; moat thinner than the rating).** Real moat: clinically-labeled training data for its 7-category safety classifier — genuinely useful, but partly unverified and the rest is app-layer assembly.
- **Sonia (Part 1: 3/5).** Real moat: a small clinician-labeled evaluation set (3,608 exchanges from its own traffic) — real but narrow; the voice loop uses commodity primitives.
- **Earkick (Part 1: 2.5/5).** Real moat: weak — its ~5.2M-token corpus is built from mostly public, reproducible material (DSM-V, NIMH, journals); deliberately skips the hard safety/device work.
- **Youper (Part 1: 2/5).** Real moat: modest and clinical, not computational — a single peer-reviewed observational study; the stack is a conventional decision-tree-plus-GPT hybrid.
- **BetterHelp / Teladoc (Part 1: 2/5).** Real moat: proprietary intake data and a 30,000+ therapist marketplace — the genuine engineering is the non-AI marketplace and insurance plumbing, not the AI.

---

**Bottom line.** The engineering that actually matters in this field concentrates in two places — proprietary clinical data (Slingshot, ieso, Limbic, Therabot, Talkspace, Lyra) and safety/evaluation rigor backed by regulatory standing (Limbic, Jimini, Spring, Wysa). Everything else — the chat interface, the rented foundation model, the prompt scaffolding — is commodity assembly that a funded competitor can reproduce. When valuing any company here, look past the "AI" and ask what data it owns and what safety apparatus it has proven. That, not the model, is the moat.


---

## Appendix — Senior Research Lead: Decisions Log (Engineering Deep-Dive)


- **Sign off on the engineering deep-dive as meeting all stated acceptance criteria.**
  - Fork: Sign off vs. send back for rework.
  - Rationale: All six criteria are satisfied and corroborated against the underlying dossiers and Part-1 report: 16 plain-English technique explainers (6-question format), Slingshot/Ash treated deepest (tier-1, 4-subagent fan-out; richest real stack in the cohort), genuine builders given deep reads (Limbic/Jimini/ieso/Wysa/Spring at 3-4/5), wrappers given a real technical read rather than dismissed, a two-column floor-vs-likely-real comp model with the >$1M reality represented as labeled inference, and a talent map anchored on real orgs. Verifier confidence on the comp model is medium, which is the appropriate ceiling for an inference-heavy section.
  - Confidence: high
- **Accept the compensation section's >$1M 'likely real' claim as a labeled inference rather than requiring it be downgraded or removed.** ⚠️ **flagged for your review**
  - Fork: Present >$1M total comp for elite ICs as a labeled inference (floor-vs-likely-real, method shown) vs. strip it for lack of disclosed data.
  - Rationale: The claim rests on (a) an unverifiable user-supplied insider premise, (b) real frontier-lab comparables (OpenAI/Anthropic/DeepMind research engineers ~$500K-$2M+ TC), and (c) equity math against each company's valuation. The public floors it sits beside are genuinely sourced and genuinely unreliable as totals (e.g., Slingshot $250K NY SWE H1B base; Spring $208K levels.fyi TC with several $0 equity samples). Presenting it as labeled inference with method shown is the correct treatment, but the central number is not audited and the verifier rated the section only medium confidence, so the user should see it before acting on it.
  - Confidence: medium
- **Endorse the engineering-lens re-rating that places Slingshot deepest/highest even though it diverges from Part-1's settled 3/5.** ⚠️ **flagged for your review**
  - Fork: Keep Part-1's down-weighted 3/5 for Slingshot vs. let the deep-dive present it as the deepest engineering effort in the cohort (4/5 read).
  - Rationale: The deep-dive is an explicit engineering-lens companion; relative to the cohort, Slingshot is unambiguously the only player doing continued-pretrain + SFT + reward-model + DPO/RL on an open-weight MoE base with dynamic routing and 3-7x/week retraining, so 'deepest' is correct on a relative axis. The dossier itself carries both a 4/5 (own assessment) and a down-weighted 3/5 (off-the-shelf weights, ~1% post-training corpus). Both readings are defensible; surfacing the divergence is more honest than silently picking one. Worth flagging so the user is not surprised the two reports rank Slingshot differently.
  - Confidence: medium
- **Accept that the 'foundation model for psychology' label stays quarantined as contested marketing throughout the deep-dive.**
  - Fork: Repeat Slingshot's 'world's first foundation model for psychology' framing vs. label it contested (heavy domain post-training on open-weight Qwen3-235B, not from-scratch pretraining).
  - Rationale: Multiple sources (Nebius, Together AI) describe fine-tuning of an open-weight base; no source claims from-scratch pretraining. Carrying the marketing label as fact would propagate the cohort's central integrity failure (marketing laundered as fact). Quarantining it is consistent with Part-1 and with the dossier's labeled inference.
  - Confidence: high
- **Accept the wrapper-tier companies' engineering sections despite near-universal base-model non-disclosure.**
  - Fork: Treat undisclosed base models as a disqualifying gap vs. give each wrapper a real technical read of orchestration/eval/safety/cost engineering and label the base-model dependency as inference.
  - Rationale: Only Youper (OpenAI, partial) and Slingshot (Qwen3-235B) name a base; 14 others are undisclosed. The deep-dive's value is reading wrapper sophistication (e.g., Limbic's model-agnostic layer, Spring's VERA-MH harness, Wysa's 120+ NLU classifiers) rather than fixating on the unknown base. Base-model dependence is correctly carried as a labeled gap, not asserted.
  - Confidence: high
- **Sign off before the assembled deep-dive is written to disk.**
  - Fork: Block sign-off until the final markdown exists on disk vs. sign off on the upstream phase outputs the workflow assembles afterward.
  - Rationale: By the workflow's design the main loop writes the report to disk only after this sign-off returns (research agents are read-only). I validated the load-bearing facts the criteria depend on against the committed dossiers and Part-1 report; the upstream phases reported 16 company sections, 16 technique explainers, a medium-confidence comp model, and a talent map. Withholding sign-off would deadlock the workflow. This is the intended ordering, not a gap in the deliverable.
  - Confidence: high


### Knowingly accepted gaps (shipped as-is)

- The compensation section's central '>$1M likely-real total comp for elite ICs' figure is a labeled inference built on an unverifiable insider premise plus frontier-lab comparables and equity math; verifier confidence is medium, not high. It is not audited or company-disclosed.
- Foundation-model vendor is undisclosed for 14 of 16 subjects (all except Youper/OpenAI-partial and Slingshot/Qwen3-235B); each wrapper's exact base-LLM dependency on OpenAI/Anthropic/Google remains inference.
- Slingshot's strongest engineering claims (Qwen3-235B base, two-pass guardrails, 3-7x/week retraining, certifications) trace largely to paid vendor marketing (Nebius, Together AI) with no independent technical audit; the base-model identification rests on a single Nebius page.
- The smallest consumer apps (Youper, Sonia, Earkick) and academic Therabot have no authoritative compensation data; only conflicting modeled aggregator estimates exist, so their comp rows are weakest.
- The deep-dive's engineering-lens difficulty re-rating (Part E) diverges from Part-1's difficulty ranking for some companies (notably Slingshot 4/5 engineering-lens vs Part-1's down-weighted 3/5); both readings are carried as defensible rather than reconciled to a single number.
- The assembled engineering deep-dive markdown is written to disk by the main loop after this sign-off; I validated against source dossiers and the upstream phase summary rather than the final assembled file, per the workflow's read-only design.


**Signed off:** True


_Sources: see `sources-engineering.md`._
