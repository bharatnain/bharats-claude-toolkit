# Pre-training (a foundation model from scratch)

*Labeling convention used throughout: **(sourced)** = a specific public claim with a URL/date in the Sources list; **(inference)** = my reasoning from sourced facts; **(speculation)** = informed guess beyond the evidence; **(contested)** = the field or the sources disagree, or the originating lab hasn't confirmed it; **(advisory)** = my reasoned judgment on learning design or org strategy, not a fact to be cited.*

---

## 1. What it is

Pre-training is the phase where a model learns the world from raw data — text, and increasingly images, audio, and video — *before* anyone teaches it to be helpful.

You take a blank neural network — billions of random numbers — and show it trillions of words, asking one absurdly simple question over and over: *given everything so far, what comes next?* No labels. No human grading. No "right answer" supplied by a person. The answer is already sitting in the data — the next word is whatever the author actually wrote. Out of that one repetitive game, the model is forced to build, on its own, an internal model of grammar, facts, reasoning patterns, code, arithmetic, and the statistical shape of human thought.

That trained network is the **foundation model** (also "base model"). It is the expensive, heavy, once-per-generation artifact. Everything else you've heard of — instruction tuning, RLHF, reasoning training, the chat personality — is comparatively cheap polish applied *afterward* to this base.

The defining trait is that pre-training is **self-supervised**: the data labels itself. That is the trick that let this scale to the entire internet, because no human has to annotate anything. A useful mental split: *pre-training* gives the model its raw intelligence and knowledge (90%+ of the compute and cost); *post-training* gives it manners and goal-direction (a sliver of the compute). This chapter is about the first part.

One sharp boundary worth fixing now, because most confusion in 2026 lives here. "From scratch" means starting from randomly-initialized weights — you own the architecture, the data mix, and every weight from the first token. It is *not* fine-tuning, *not* adding retrieval (RAG), *not* continued pre-training on someone else's checkpoint. Those all start from a model somebody already pre-trained. This chapter is about creating that starting point — and a recurring theme will be that doing so is the right call far less often than people's instincts suggest *(advisory)*.

---

## 2. How it works

### The core loop: next-token prediction

The entire learning algorithm is six steps, repeated trillions of times.

1. **Tokenize.** Text is chopped into "tokens" — sub-word chunks, roughly ¾ of a word each. A modern tokenizer has ~100k–200k distinct tokens; GPT-4o's `o200k_base` tokenizer has ~200,019 *(sourced)*. Every token gets an ID. "Strawberry" might be three tokens; "the" is one.
2. **Predict.** The model reads a sequence and outputs a probability distribution over *every possible next token* — a ~100k-way guess: "next token is 'cat' at 4%, 'dog' at 3%, …".
3. **Score the error.** Compare the guess to the token that actually came next. The penalty is **cross-entropy loss**: high probability on the true token means small penalty; confidently wrong means large penalty. That single number is the model's "wrongness" right now.
4. **Backpropagate.** Calculus runs *backward* through the network to compute, for each of the billions of weights, "if I nudge you this way, does the error go down?" — the **gradient**.
5. **Update.** An optimizer nudges every weight a tiny step downhill. AdamW has been the default for years; **Muon / MuonClip** is the notable 2026 shift, delivering roughly 2× token efficiency — demonstrated at trillion-parameter scale by Moonshot's Kimi K2 (~1T params on 15.5T tokens with zero loss spikes) *(sourced)*. Worth a precise note: at mid-2026, Muon is proven at frontier scale chiefly by Moonshot; AdamW and its variants remain the default at most other frontier labs. "Seriously competitive" is accurate; "AdamW is already replaced" would be premature *(inference)*.
6. **Repeat.** Each step processes a "batch" of millions of tokens at once.

That objective — next-token prediction plus backpropagation — has not fundamentally changed since 2018 *(inference; scoped deliberately to the **objective**, not the whole apparatus — the optimizer and architecture around it have changed materially, as the Muon and MoE notes here show)*. **Everything hard about modern pre-training is making this loop run on tens of thousands of chips for months without the answer drifting into garbage.**

### The architecture: the Transformer, now usually sparse

The network is a **Transformer**. Its key organ is **attention**: at each layer, every token looks back at the earlier tokens and decides which ones matter for predicting what comes next — "this pronoun refers to *that* noun thirty words ago." Stack ~50–100 such layers and the model composes simple relationships into deep ones.

The dominant 2026 shift is **Mixture-of-Experts (MoE)**. Instead of one giant dense network where every parameter fires on every token, the model holds many parallel "expert" sub-networks plus a tiny **router** that sends each token to just a few of them. This decouples *knowledge* (total parameters) from *cost* (active parameters per token).

- DeepSeek-V3: **671B total parameters, only 37B active per token** — you pay for 37B, you store knowledge in 671B *(sourced)*.
- Llama 4 Maverick: 400B total / 17B active, 128 experts *(sourced)*.
- The 2026 frontier reportedly runs into the **multi-trillion-parameter** range (Grok 5 targeting ~6T–10T total; an unconfirmed ~5T figure floated for Claude Opus, whose actual parameter count is undisclosed) — almost certainly MoE, since dense at that scale is economically impossible *(contested — these specific numbers are leaks and company claims, not lab-confirmed; the Opus figure in particular is unconfirmed)*.

A related, newer pattern is **mixture-of-transformers**: pairing distinct transformers (e.g., a reasoning transformer with an expert generation transformer) rather than just routing among feed-forward experts. NVIDIA's Cosmos 3 (below) is the marquee example.

### The data pipeline: where most of the *real* work now lives

Raw web text is mostly junk. Turning it into training fuel takes four stages *(sourced — FineWeb is the open reference recipe)*:

- **Filter** — discard spam, boilerplate, toxic content, and machine-generated sludge; keep coherent prose. Modern practice uses **model-based quality classifiers** (a small model scoring "is this worth training on?"), which now beat hand-written heuristics *(sourced — FineWeb-Edu)*.
- **Deduplicate** — the same text appearing 10,000 times teaches nothing and wastes compute; near-duplicates are collapsed.
- **Decontaminate** — remove anything resembling the benchmark tests, so evaluation isn't cheating.
- **Mix** — deliberately blend domains (web, code, math, books, multilingual) in tuned ratios. Code and math punch above their weight for reasoning. This mixture is one of the highest-leverage decisions in the whole run.

The single biggest change in 2025–2026 is **synthetic data**. Because high-quality human text is running out (see §3), labs now use existing models to *rewrite* good source text into better training data — turning a web page into clean Q&A, restructuring it pedagogically, matching the style to intended use. DatologyAI's BeyondWeb work showed a 3B model on good synthetic data beating an 8B model trained on the same token budget of older synthetic data, and **7.7× faster training** to a baseline *(sourced)*. The counterintuitive finding: the gain comes from *faithful rephrasing of good sources*, not from inventing novel content — and quality saturates with a small (~3B) rewriter model *(sourced)*.

### The schedule: curriculum and learning-rate annealing

Training isn't uniform. The modern recipe is **Warmup-Stable-Decay (WSD)** *(sourced)*: warm the learning rate up, hold it high through the bulk of training on the broad mix, then **anneal** — decay the learning rate sharply at the end while feeding the model the *highest-quality 10–20% of data* (top math, code, curated text) *(sourced)*. Intuition: early on you want big, exploratory steps over diverse data; at the end you want tiny, careful steps over your best material to "set" the knowledge. (An active 2026 thread argues that coupling the decay and the best-data injection actually *wastes* the best data, and proposes decoupling them via model averaging — *sourced, but not yet standard*.)

### The engineering that makes it physically possible

- **FP8 mixed precision.** The heavy matrix multiplies use 8-bit floating point instead of 16/32-bit — roughly halving memory and compute versus the old standard, with careful per-tile scaling to avoid blowing up. DeepSeek-V3 was the landmark first open model to do FP8 at scale *(sourced)*.
- **Parallelism, four ways at once.** No model or dataset fits on one chip. *Data parallelism* (model copies on different data), *tensor parallelism* (one layer split across chips), *pipeline parallelism* (different layers on different chips), and *expert parallelism* (MoE experts spread across chips). Orchestrating these across tens of thousands of GPUs — keeping them fed and synchronized — is the central systems problem. The efficiency metric is **MFU (Model FLOPs Utilization)**, the fraction of your hardware actually doing useful work; ~55% is a strong large-scale number, and poor networking silently drops you to 40–50% — i.e., you pay double *(sourced)*.
- **Fault tolerance.** On a 100,000-GPU cluster running for months, hardware *will* fail constantly. The system checkpoints frequently and resumes, or the run silently corrupts. Silent data corruption (NaNs propagating, bad updates) is a named, active 2026 reliability problem.

One myth to retire: it used to be said the model "never sees the same data twice in a way that lets it cheat." In the GPT-3-era single-epoch regime that held. It no longer does. With extreme overtraining (see §3), high-quality data is now *deliberately* repeated across multiple epochs; the data-wall literature explicitly models "repetition-adjusted" token stocks. Controlled repetition of good data is standard, not avoided *(sourced)*.

---

## 3. Why it works

### The deep principle: prediction forces understanding

To reliably predict the next token across all of human text, memorization is impossible — there are too many continuations and the model is far too small to store the internet verbatim. The only way to drive the loss down is to **discover the underlying generators of the text**: grammar, arithmetic, physical facts, causal and logical structure, the conventions of code. Compression *is* comprehension. The network is squeezed, by relentless pressure to predict, into building genuine internal models of how the world works — because that is the most compact way to be right. Translation, arithmetic, and reasoning **emerge** as side effects nobody explicitly programmed *(inference — this is the field's leading explanation, not a proven theorem)*.

### Why it works *at scale specifically*: scaling laws

Pre-training is unusual in that performance improves **smoothly and predictably** as you grow three things together — parameters, data, and compute. These **scaling laws** let labs run small experiments and *extrapolate* what a giant run will achieve before spending $100M. A useful rule of thumb: training cost in floating-point operations is roughly *6 × parameters × tokens*, which is why everything is budgeted in tokens and FLOPs, not gigabytes *(sourced — the Kaplan/Hoffmann scaling-law line of work)*.

The famous "Chinchilla" answer for a fixed compute budget was ~20 tokens per parameter *(sourced)*. **Almost nobody trains there anymore.** Because a model will be *served* billions of times, teams deliberately **overtrain** — smaller models on vastly more data — to lower the per-query inference cost. The **tokens-per-parameter ratio has exploded from ~10 in 2022 to ~300 in 2025** *(sourced)*, with extreme cases hitting 60,000:1 (Qwen3-0.6B on 36T tokens) *(sourced)*. The mental model: "optimal" depends on whether you're minimizing the *training bill* or the *lifetime serving bill* — and almost everyone now optimizes the latter.

### Why the naive alternatives fail

- **Why not supervised learning (label everything)?** No human could annotate trillions of tokens; you'd run out of money and people first. Self-supervision's whole point is that the data is its own label.
- **Why not a smaller model on the same data?** Below a certain capacity the model is forced to memorize surface patterns instead of discovering deep structure; reasoning and emergent abilities don't appear. Specific capabilities switch on only past certain thresholds.
- **Why not skip pre-training and train directly on your task?** Then the model has no world-model to build on; it overfits the narrow task and generalizes terribly. Pre-training's value is precisely that the general foundation transfers to *everything* downstream.
- **Why the data wall is the real 2026 constraint, not compute.** The usable stock of high-quality human text is ~**300 trillion tokens**, projected to be effectively exhausted somewhere between **2026 and 2032** (Epoch AI, 80% confidence) *(sourced)*. Naively you'd just train on more raw web — but repeating low-quality data plateaus performance and can cause distribution collapse. And MoE, by being more data-hungry, *accelerates* the wall rather than relieving it *(sourced)*. This is *why* synthetic data, multimodal data (images/video/audio carry information text doesn't), and smarter curation became the frontier instead of brute-force more-of-the-same.

---

## 4. People & resources

Two very different worlds exist in 2026, so I give both. *These are reasoned estimates synthesized from public reports, not single quoted figures, except where marked (sourced).*

### The frontier run (OpenAI / Google / Anthropic / Meta / xAI tier)

- **People: hundreds.** The Llama 3 paper lists **~560 authors** *(sourced)*. Realistically a **core pre-training team of ~30–80** doing the model/data/systems work, wrapped in a supporting org of hundreds — data engineering, cluster/infra/SRE, evaluation, safety *(inference)*.
- **Roles:** research scientists (architecture, scaling laws, data mixtures); ML/systems engineers (parallelism, FP8 kernels, fault tolerance — often the largest group); data engineers (the curation pipeline, increasingly the highest-leverage role); evaluation/benchmarking; and a 24/7 "babysitting" rotation watching loss curves for a run that can't be left alone for months.
- **Compute: tens of thousands of top GPUs for months.** Llama 3 405B used **~30.8M H100 GPU-hours** on ~16k H100s *(sourced)*. The frontier now sits on clusters like **xAI's Colossus**, with company announcements citing ~555,000 GPUs and ~$18B in chips *(sourced — company-stated GPU and dollar figures)*. The widely-repeated **~2 GW power figure is contested**: satellite-imagery analysis (Tom's Hardware) suggests Colossus 2 has only ~350 MW of cooling capacity, far short of the claimed gigawatt — treat the power number as an aspirational/disputed company claim, not verified operational capacity *(contested)*. OpenAI's Stargate is a comparable multi-hundred-billion-dollar buildout *(sourced)*.
- **Time:** the headline run is **weeks to a few months**; the *research and ablation* that precedes it often takes longer than the final run and is excluded from the cost-to-train figures labs quote *(inference)*.
- **Money:** **tens to hundreds of millions per flagship run, rising toward billions** for the largest. GPT-4-class compute was estimated at **$78–100M+**; Gemini Ultra ~$192M (Stanford AI Index 2025) *(sourced)*. Frontier final-run cost has grown roughly 2.4× per year since 2016, and projections put the largest runs above **$1B by 2027** *(sourced)*. All-in (R&D, salaries, amortized cluster) is several times the raw-compute figure.
- **Data: ~10–40 trillion tokens**, heavily filtered and increasingly synthetic. Llama 3: ~15T text tokens; DeepSeek-V3: 14.8T *(sourced)*.

### The efficient frontier (the DeepSeek lesson — the big 2026 story)

DeepSeek-V3 trained a GPT-4-class 671B MoE for **~2.788M H800 GPU-hours ≈ $5.6M in rental compute** *(sourced — DeepSeek's own report; this is the **final run only**, excluding failed runs, research salaries, data pipeline, and infrastructure, which dominate a real program's cost — hardware is 47–67% and R&D staff 29–49% of a frontier budget)*. That headline is the prize for being elite, not the entry ticket: hitting it required custom FP8 training, MoE load balancing, and bespoke communication kernels at ~23% MFU that most teams can't reach. Still, it proves the cost of a *given capability* is now driven by **algorithmic and data efficiency** far more than raw spend. A capable team here might be **dozens of people**, not hundreds *(inference)*.

### A serious open/academic base model (not frontier, but real)

People: ~5–20. Compute: hundreds to low-thousands of GPUs for weeks. Money: ~$100k–$10M. Data: 1–10T curated tokens *(advisory — synthesized from open reports like AI2's fully-open Olmo 3, trained on ~1,024 H100s)*. A 7B model from scratch is within reach of a well-funded startup or university lab; a frontier model is not.

### The honest bottom line *(advisory)*

Pre-training has **bifurcated**. Building a *frontier* model from scratch is a national-industrial-scale endeavor — billion-dollar clusters, hundreds of specialists, multi-year compounding research. But the cost of a given *capability level* is collapsing — what cost $100M in 2023 can be approached for single-digit millions in 2026 via MoE, FP8, and synthetic data. The binding constraint has quietly shifted from "can you afford the GPUs?" to **"do you have the data and the recipe?"** — which is exactly why data curation and synthetic-data generation, not raw compute, are where the labs now fight.

---

## 5. Scenarios & stories

By June 2026, "we need our own model, so we'll train one" is one of the most misapplied instincts in the field — not because pre-training stopped mattering, but because the set of situations that genuinely *need* it shrank to a few specific shapes. Here is what those shapes look like, and where the instinct goes wrong.

### Where it's the right tool

**1 — The genomics lab with a language nobody has modeled.** A computational-biology group wants a model that "speaks DNA": reads raw nucleotide sequences across thousands of species, predicts function, transfers to RNA and protein tasks. They look for a base model to fine-tune and find there isn't one that fits — DNA is not English. The tokenization, the sequence lengths (hundreds of thousands of base pairs), and the architecture (state-space / Hyena-style rather than vanilla transformers) are all different. Models like Nucleotide Transformer v3 and Evo 2 exist *because* someone pre-trained them from scratch on the genome *(sourced)*. When your modality is genuinely *new* — DNA, proteins, weather fields, sensor streams, chip netlists — there's nothing to stand on, so you must build the ground floor. This is the single most defensible case for from-scratch in 2026 *(advisory)*.

**2 — A nation that refuses to be a tenant.** A government wants a model fluent in its national language and dialects, encoding local law and culture, running on domestic infrastructure, legally its own. This "sovereign AI" buys something compute can't: control and accountability *(sourced)*. But notice the nuance, because it's the whole lesson: Singapore's SEA-LION trained its *first* models from scratch, then for v2 switched to **continued pre-training on top of Llama 3** (~48B tokens) — reproducing trillions of tokens of general knowledge just to reach a Southeast-Asian model was wasteful *(sourced)*. Even the textbook "good" case has largely *evolved away from* from-scratch, which now survives only where a team wants full control of data lineage end-to-end (e.g., Hebrew's Dicta-LM line) *(advisory)*.

**3 — A frontier lab pushing the actual ceiling.** OpenAI, Anthropic, Google DeepMind, DeepSeek, and a handful of others pre-train from scratch because that *is* their product — a model more capable than anything that exists. You cannot fine-tune your way to a new frontier. The price of admission rises every year ($100M–$1B band today, >$1B runs projected by 2027); it's the right tool for maybe a dozen organizations on Earth *(sourced + inference)*.

**4 — Bloomberg's bet (and why even this got contested).** Bloomberg pre-trained BloombergGPT (50B params, ~700B tokens, half a proprietary finance corpus) on the theory that a finance-native model beats a pile of narrow fine-tunes *(sourced)*. By 2026 this is genuinely **contested**: general open-weight models plus continued pre-training on the same finance corpus often match or beat a from-scratch domain model at a fraction of the cost, because the open base already absorbed the general knowledge the from-scratch model learned the hard way. The honest read: BloombergGPT was reasonable when built, and would likely be built as continued pre-training today *(inference / contested)*.

### Where it's the wrong tool

**5 — The startup that wants "our own model."** A 30-person company wants a model "trained on our data so it really understands our business." This is the most common and most expensive mistake in the field. A 70B-class from-scratch run is roughly $1.2M–$6M before staff — and buys a model *worse* than free open weights, because you can't afford the trillions of tokens and the team the open base already had *(sourced)*. Fine-tuning reaches good task performance with 1,000–10,000 examples in hours-to-days *(sourced)*. "Our data" almost never means "a new base intelligence" — it means "adapt an existing one" *(advisory)*.

**6 — "Our domain is too specialized for general models."** A legal-tech or medical-records team is convinced its jargon demands a from-scratch model. Almost always false: general models already saw enormous legal and medical text in their own pre-training; the gap is closed by continued pre-training or fine-tuning. The research even names the trap — the **"finetuner's fallacy"** — and the answer to "is domain data worth pre-training on from scratch?" is "rarely" *(sourced)*. The tell: if a competent open base, given your documents via RAG or a few thousand examples, gets 90% of the way there, from-scratch is buying the last 10% at 100× the cost — and often not even getting it *(advisory / inference)*.

**7 — Chasing DeepSeek's $5.6M headline.** Executives read "$5.6M, we can do that." Two traps, both covered in §4: that figure is the *final run only*, and reaching it required world-class systems engineering at an MFU most teams can't hit. The cheap number is the prize for being elite, not the entry ticket *(sourced + inference)*.

**8 — Pre-training to "keep the model current."** A team rebuilds from scratch each quarter to absorb new information. Wrong tool entirely. Currency is a RAG problem (look facts up at query time) or at most a light continued-pre-training refresh. Rebuilding the base to learn this week's news is like rebuilding a library because a new newspaper came out *(advisory)*.

### The 2026 decision rule *(advisory)*

Pre-train from scratch only when **all four** hold; otherwise continued pre-training, fine-tuning, or RAG is correct:

1. **No suitable base exists** — your modality or language is genuinely uncovered by open weights, OR you're a frontier lab defining new capability.
2. **You have a corpus in the trillions of tokens** that justifies relearning the world, not just billions of domain examples.
3. **Control is the product** — sovereignty, data lineage, or licensing make inheriting someone else's weights unacceptable, *and* continued pre-training can't satisfy that.
4. **You can absorb $1M–$1B+ and a top-tier systems team**, including failed runs.

If you're saying "we want our own model on our data," you want fine-tuning. If "we need current information," you want RAG. If "our language/domain is underserved," you almost certainly want continued pre-training on an open base — the path even sovereign programs converged to.

---

## 6. Cross-industry usage & positioning (as of June 2026)

The defining fact of 2026 is a **barbell, not a bell curve**. From-scratch pre-training has become *more* concentrated at the frontier (only a handful of labs can afford a true run, costs heading toward $1B+) *and simultaneously radically cheaper* in narrow domains. The middle ground — enterprises pre-training their own general-purpose LLM — has largely collapsed. For >95% of organizations, the right move is to adapt an open-weight model *(sourced + advisory)*.

**Coding / developer tools — table-stakes at the top, only for a few labs.** Code is one domain where from-scratch on code-heavy corpora is still live, because code is structured, abundant, and verifiable. DeepSeek-Coder (from scratch on ~2T tokens, ~87% code) and StarCoder pioneered it. But in 2026 *most* "coding models" are post-trained from general models (Code-Llama, Code-Qwen style), not pre-trained from scratch. From-scratch code pre-training is a frontier-lab move, not a dev-tools-company move *(sourced)*. (Notable exception proving the rule: Anysphere/Cursor reportedly training a 1.5T-parameter coding model from scratch on xAI's Colossus — because the base model *is* their product.)

**Consumer / general AI — the only true from-scratch frontier game.** OpenAI, Google, Anthropic, xAI, DeepSeek, Meta, Alibaba (Qwen), Amazon (Nova). For everyone else this is a *buy*, not *build*, market *(sourced)*.

**Robotics / physical AI — a genuine new from-scratch frontier.** The most active *new* from-scratch domain, because action trajectories and multimodal world dynamics don't exist in language corpora. **NVIDIA Cosmos 3** is the marquee example: an open "world foundation model" pre-trained on billions of multimodal samples (text, image, video, sound, action). Precisely, its architecture is a **mixture-of-transformers** pairing a reasoning transformer with an expert generation transformer — worth stating exactly, since it's the canonical example of that pattern. It was introduced by Jensen Huang at COMPUTEX 2026, with the technical report dated 2026-06-22 and press coverage clustering around June 1; treat any single "launch date" as approximate *(sourced; date approximate)*. Google DeepMind (Gemini Robotics + Veo world simulators) is the other leader. NVIDIA is positioning as the "pre-training infrastructure + base model" provider for the whole robotics industry — analogous to its GPU position *(sourced)*.

**Science (biology, weather, materials) — from-scratch is essential.** The modality (protein sequences, atmospheric fields, DNA) is alien to text models. Protein: the ESM family (ESMC on ~2.8B sequences); AlphaFold3 as the structure benchmark. Weather: Aurora (1M+ hours of weather/climate data), FengWu, ClimaX. The dominant 2026 science story is a **data wall, not a compute wall**: an analysis of 360+ biological foundation models found development *slowing since ~2021*, bottlenecked on diverse, well-curated data, not algorithms *(sourced)*.

**Defense / national security — adapt-and-integrate, mostly NOT from-scratch.** Counterintuitively, defense leaders integrate frontier models into operational platforms rather than pre-train. Project Maven (becoming a program of record by Sept 2026) integrates Claude via Palantir's AIP on AWS. Anduril (Lattice) and Palantir (Foundry/Ontology) lead the NGC2 battlefield program. The value is in *ontology, integration, and data provenance*, not from-scratch pre-training; where from-scratch matters in defense, it overlaps with sovereign AI *(sourced)*.

**Finance — mostly fine-tune; from-scratch is a legacy/edge case.** BloombergGPT and XuanYuan 2.0 were notable from-scratch efforts, but the 2026 consensus is that fine-tuning an open base captures most of the value at a fraction of the cost. From-scratch survives only where regulatory provenance over every training token is mandatory *(sourced)*.

**Healthcare — from-scratch only for non-text modalities.** For clinical *text*, fine-tuning wins. From-scratch is reserved for modalities far from anything a general model has seen — e.g., DentVFM (a dental vision foundation model), and imaging/genomic models *(sourced)*.

**Sovereign / national AI — a growing from-scratch driver, but mostly adapt.** Governments fund near-from-scratch pre-training for control and provenance (Canada's ~$890M sovereign-compute program; India targeting a homegrown model). But even here, only ~34% of sovereign initiatives are "model projects," and *most adapt open weights* for local languages. True from-scratch sovereign pre-training is the exception *(sourced)*.

**Enterprise — the new middle path that replaces from-scratch.** **Amazon Nova Forge** lets enterprises start from *early pre-training / mid-training checkpoints* and blend proprietary data *during* training — "from-scratch-like" domain depth without owning the full run, with explicit handling of catastrophic forgetting via data-mixing. ~$100K/yr subscription plus usage compute; early adopters in life sciences, finance, entertainment, travel. This is effectively "from-scratch-as-a-service from a checkpoint," and it's eating the use cases that used to justify a true from-scratch build *(sourced)*.

**A caution on the "$1,500 foundation model" claim.** A widely-discussed 2026 result — **HRM-Text**, reportedly trained for ~$1,500 in ~1.9 days on 16 GPUs, hitting ~60.7% MMLU / 84.5% GSM8K / 56.2% MATH — has been used as a headline proof that cheap from-scratch pre-training is democratized. **Treat this carefully**: the dollar/GPU/day and benchmark figures are accurately quoted from the source, but the example does *not* match this chapter's definition of pre-training. HRM-Text is not a standard Transformer trained with next-token prediction on raw web text — it uses a Hierarchical Recurrent (Hyena-style) architecture and trains *exclusively on instruction-response pairs with a task-completion objective and PrefixLM masking* on ~40B tokens. That makes it closer to a from-scratch *task-completion / distillation* run on curated instruction data than to "a blank network learns the world from raw text." The directional signal — small, narrow from-scratch models are getting cheap — is real; the specific example is a methodological mismatch and should not be cited as the canonical cheap-pre-training proof *(contested / corrected)*.

**Synthesis.** (1) Barbell: thriving at the $100M+ frontier and the sub-$10K narrow model, dying in the enterprise middle. (2) Architecture shifted: MoE and mixture-of-transformers are standard; pure dense is no longer the default for new runs. (3) The new from-scratch frontiers are *physical and scientific*, not linguistic. (4) Data, not compute, is the emerging wall. (5) "From-scratch-from-a-checkpoint" (Nova Forge) is the pragmatic enterprise frontier, collapsing build-vs-buy into a spectrum *(sourced + inference)*.

---

## 7. Learning path for a technical leader

*For someone who will fund, staff, and judge this work — not write the kernels. Concepts only, no labs. The goal is a working mental model and a sharp interview filter. The whole section is advisory.*

Pre-training is the one phase where the largest checks get written and the fewest people in your org understand what's happening. A 6–12 week run on a 10,000-GPU cluster is a single bet with a one-shot failure mode: a bad data mix or an optimizer instability discovered in week 5 can cost eight figures and a quarter. Your job is to ask the questions that surface those risks *before* the run starts — and to tell an expert from someone who's read the blog posts.

### Five core mental models

1. **Pre-training is compression, not teaching.** You're not teaching facts; you're forcing next-token prediction across trillions of tokens, and the only way to get good at that is to build an internal model of the data's patterns. The model is a lossy compression of its training data — which is why **data quality dominates everything**: garbage in, faithfully compressed garbage out.
2. **The compute budget is fixed; you spend it on two things.** Cost ≈ *6 × parameters × tokens* in FLOPs. Every architecture and data decision is a question of how to spend a fixed FLOP budget for the most capability. Scaling laws are the empirical curves telling you the best split between *bigger model* and *more data*.
3. **Compute-optimal is no longer what people build.** Chinchilla said ~20 tokens/param; almost nobody trains there. Because the model is *served* billions of times, teams **overtrain** smaller models on far more data to cut per-query cost. "Optimal" depends on whether you optimize the training bill or the lifetime serving bill — and almost everyone optimizes the latter.
4. **The bottleneck moved from compute to data.** There isn't enough high-quality human text to keep feeding ever-larger models, and MoE *accelerates* the wall. The frontier response is **synthetic data** — rephrasing web text into higher-density tokens.
5. **Sparsity is the default architecture.** Frontier models are sparse MoE (DeepSeek-V4 ~1.6T total / ~49B active; Kimi K2 ~1T / ~32B). MoE buys big-model knowledge at small-model serving cost — at the price of harder systems engineering and more data hunger.

### Sequenced concept progression

- **Stage 1 — Objective & unit of work:** next-token prediction and self-supervision; tokenization as a quiet design choice (multilingual coverage, math, code, cost-per-character); why everything is measured in tokens and FLOPs.
- **Stage 2 — Scaling as governing logic:** scaling laws; Chinchilla as baseline; *why the field left it* (inference-aware scaling, deliberate overtraining); the data wall.
- **Stage 3 — The data pipeline (where the real work is):** sourcing (Common Crawl, code, books); the cleaning recipe (language ID → dedup → quality filtering → mixing; FineWeb is the open reference); model-based quality filtering; data mixture as a top-leverage decision; synthetic data and its risks (collapse, contamination, homogenization).
- **Stage 4 — Architecture:** the Transformer block conceptually (what attention *does*); dense vs. sparse MoE (experts, router, active vs. total params); why MoE wins on serving economics and is painful to train; context length.
- **Stage 5 — The run as a systems problem:** 3D/4D parallelism; FP8 training; MFU; optimizers (AdamW default, Muon/MuonClip the 2026 shift); stability and fault tolerance (loss spikes, checkpointing, routine GPU failures).
- **Stage 6 — Knowing if it worked:** healthy loss curves; why loss isn't enough (benchmarks, contamination); the handoff — pre-training produces a *base model*; capability and safety come from a *separate* post-training phase you must never conflate with this one.

### Reading & watching spine (few sources, high value)

1. A good explainer of **Scaling Laws + Chinchilla** (Brenndoerfer's interactive writeups) — you need the *shape* of the curves, not the regression.
2. **"Beyond Chinchilla-Optimal: Accounting for Inference"** (abstract + intro) — *why* modern practice diverged from the textbook.
3. **FineWeb / FineWeb2 writeups** — the best concrete account of how a real pre-training dataset is built; skim for the pipeline stages.
4. **"BeyondWeb" (DatologyAI)** and/or HuggingFace's synthetic-data material — current synthetic-data state of the art and its limits.
5. **The Kimi K2 technical report** — the most readable recent frontier report covering MoE + Muon + stability at trillion-parameter scale; read the architecture and optimizer sections.
6. A current **MoE explainer** (Cameron Wolfe's nanoMoE / Raschka's MoE chapter) plus a 2026 open-model roundup for *who uses what now*.
7. *(Optional, only if you fund infra)* a distributed-training survey for the parallelism vocabulary.
- *Watching:* Karpathy's "Let's build GPT" / "State of GPT" remain the best visceral on-ramp.

### Understanding checkpoints

You understand the material when you can explain, in plain language to a non-expert: why next-token prediction with no labels can produce reasoning (and why that makes data quality the whole ballgame); the bigger-model-vs-more-data tradeoff *and* why a team trains "past optimal" (inference cost); why buying more GPUs doesn't fix the data wall; "active vs. total parameters" to your CFO, with MoE's serving win vs. training risk; three ways a multi-week run fails (loss spike / data bug / hardware failure) and their mitigations; that pre-training produces a *raw base model* and helpfulness is a separate post-training phase; and why a falling loss curve is necessary but not sufficient (benchmark contamination).

### How to evaluate an expert

The tell is **specificity about tradeoffs and failure modes**, not breadth of terms.

- **"Spend a fixed compute budget on a new run."** *Strong:* frames it as model-size-vs-tokens, *volunteers* training past Chinchilla for inference economics, asks your serving volume and latency before committing, names data mixture as co-equal. *Weak:* "20 tokens per parameter" and stops. *Red flag:* only talks model size and GPUs; never mentions inference cost or data.
- **"Highest-leverage decision, and why?"** *Strong:* **data** — composition, quality filtering, mixture — with a concrete example of a data change moving a benchmark, and opinions on synthetic data's payoff *and* collapse/contamination risk. *Red flag:* can't distinguish data *quality* work from data *quantity*; thinks scraping more web is the frontier.
- **"Why is every frontier model now MoE? What does it cost you?"** *Strong:* crisp on active-vs-total and the serving win, then *volunteers* the costs (routing/load-balancing instability, comms overhead, harder eval, worsened data wall). *Red flag:* confuses MoE with ensembling, or can't explain the router.
- **"Tell me about a run that went wrong."** *Strong:* a specific war story — a loss spike at a certain step, a data-pipeline bug poisoning a shard, a divergence traced to FP8 or the LR schedule — with monitoring, checkpoint-and-rollback, and what they changed; mentions hardware failures as routine. *Red flag:* has never seen a run fail.
- **"What's changed in pre-training in 12–18 months?"** *Strong:* FP8 as default, Muon/MuonClip for token efficiency, synthetic data maturing, compute-bound → data-bound, MoE as table stakes — and which they've *personally* used. *Red flag:* still describes the 2022–23 GPT-3/Chinchilla world as current.
- **"How do you know the base model is good, before post-training?"** *Strong:* loss curves *plus* a held-out eval suite, explicit on contamination and the limits of any single number, distinguishing base quality from instruction-tuned behavior. *Red flag:* conflates pre-training quality with chatbot helpfulness.

*Cross-cutting:* green flags are reasoning in tradeoffs unprompted, distinguishing *what the field publishes* from *what they've run*, comfort saying "it depends, here's on what," and treating data as first-class engineering. Red flags are vocabulary without tradeoffs, no real numbers from experience, treating pre-training as "just scaling," and being unable to say what they'd do differently next time.

**Calibration note for the leader.** The biggest practical risk in this domain is **funding a from-scratch pre-train at all.** For most organizations in 2026, continued pre-training, fine-tuning, or post-training on a strong open base is dramatically cheaper and lower-risk. A real expert tells you this unprompted and pushes back on a from-scratch mandate unless you have a genuine reason. **An "expert" eager to build from scratch without asking why is itself a red flag.**

---

## 8. Team notes

*What this is: taking a randomly-initialized network and training it on trillions of tokens to produce a base model — you own the architecture, the data mix, and every weight from the first token. The whole section is advisory.*

### The bottom line first

**For ~95% of organizations: do not do this. Rent or buy.** From-scratch pre-training is the single most capital-, talent-, and time-intensive technique in the ML stack. A frontier-class run costs $78M–$200M+ today (compute alone 47–67% of that) and requires a team you cannot assemble quickly — the relevant specialists are the most bid-on people in tech (median frontier comp ~$600K–$795K, 90th percentile clearing $1.28M+). Unless owning the base model is a genuine, durable moat, you are lighting money on fire that a fine-tune or continued-pre-training product would have saved.

**The narrow cases where building IS justified:** the base model itself is your *product* and differentiation (Cursor's code model; a frontier lab); you have data/modality/language nobody else has at scale AND you've proven a fine-tune can't capture it; regulatory/sovereignty constraints genuinely forbid using a vendor's weights (even then, "buy a checkpoint" usually beats "from scratch"); or you're a research lab whose *output is the open recipe* (Olmo's value is the transparency, not beating GPT). If you're not clearly in one of these, the rest is a warning.

### Roles & seniority — it's not a hire, it's a small specialized org

You cannot hire "an ML engineer" and expect a foundation model. The minimum viable team is three distinct disciplines that rarely live in one person:

1. **Pre-training Research Scientist / Engineer (the irreducible core).** Senior-to-Staff minimum, ideally someone who has *shipped a real run before* — the failure modes (loss spikes, divergence, data-mix decisions) are learned by surviving runs, not papers. Owns architecture, data mixture and curriculum, scaling-law experiments to de-risk the big run, hyperparameter/optimizer decisions, evaluation design. Highly operational, not whiteboard-only.
2. **Distributed Training / Infrastructure Engineer (co-equal, not support).** Staff/Principal systems engineer comfortable with thousands of GPUs. Owns multi-node orchestration, parallelism strategy, keeping utilization high (poor networking silently halves it), checkpointing, fault tolerance. At this scale, infra failures *are* research failures — a divergence can be a data problem or a transient hardware fault, and the team must tell them apart in real time.
3. **Data Engineering / Curation Lead.** Senior, with a curation-quality mindset. Owns sourcing, dedup, decontamination (keeping eval sets out of training), and the actual *mix*. Data quality directly causes or prevents loss divergence — a 2026 empirical finding, not folklore. ~90% of total project compute goes to experiments + final runs, but the *decisions that determine whether that compute is wasted* are largely data decisions.

Plus an **eval lead**, an **ML-platform / capacity owner** (procurement and reliability for the cluster contract), and a **technical lead** who has done this before and can make the go/no-go call. **Does an existing role absorb this? No — that's the trap.** Teams assume their strong applied-ML or platform engineers can "just scale up." They can't, and the gap shows up only after you've burned a month of cluster time. If you can't hire all three disciplines, you are not ready — and that's a perfectly good reason to choose continued pre-training instead.

### Hiring signals & red flags

*Strong signals:* has personally owned a run at >100B-token scale and can describe a loss spike they diagnosed and recovered from (war stories beat credentials); speaks fluently about the systems layer even if "research"; **scaling-law literacy** — can explain how they'd de-risk a $50M run with cheap small-scale experiments first (the single most important risk-control skill); data-mix opinions with measured receipts; for infra, has run jobs across hundreds+ of nodes and treats hardware failure as a design assumption.

*Red flags:* "pre-training" on a résumé that's actually fine-tuning or LoRA — *ask what they initialized from; if it's a checkpoint, it wasn't from scratch*; pure-research profile with no operational scars; no scaling-law / de-risking instinct (wants to jump straight to the big run); hand-waves data as "the boring part"; overpriced generalist riding the hot market (demand-to-supply ~3:1) — distinguish a true frontier specialist from a generalist with an inflated title.

### Build vs. buy / rent — a graded ladder (default to NOT building)

1. **Rent via API** (closed frontier models) — cheapest, fastest, vendor improves the base for free. Default for almost everyone.
2. **Buy + fine-tune open weights** — a 7B fine-tune can cost under ~$5 and hours of work. Covers most "sound like us / do our task" needs.
3. **Continued pre-training on a vendor checkpoint** — the genuinely important new 2026 middle option. Amazon **Nova Forge** productizes "open training": intermediate checkpoints from each stage, mix your proprietary data into the pre-training corpus, inject deep *domain knowledge* (not just task behavior), address catastrophic forgetting, ~$100K/yr + usage. **The right answer for most teams that think they want to pre-train** — ~80% of the "unique data" value at ~1% of the cost and risk.
4. **Pre-train from scratch** — only when the base model is your product/moat, or sovereignty genuinely forbids 1–3.

**The moat test:** before approving a from-scratch build, force the question — *"If a vendor shipped a checkpoint tomorrow that we could continued-pre-train, would we still build from scratch?"* If the honest answer is no, you don't have a moat, you have a budget you're about to waste. Fine-tuning is 1,000–10,000× cheaper than from-scratch; continued pre-training sits in between with most of the upside.

### Common failure modes

*Strategic (the expensive ones):* **building when you should have rented** (pre-training as ego/resume-building; the base commoditizes underneath you while you spend a year reaching parity); **hiring one "ML lead"** and discovering the missing disciplines mid-run; **underestimating experiment compute** (>90% of compute in mature efforts is the de-risking experiments, not "the run"); **no moat in the end** — frontier money for a model worse than what you could have rented.

*Technical (the painful ones):* **loss spikes / divergence** (still partly mysterious in 2026, traceable to data, hardware faults, precision, or optimizer/normalization); **data quality causing divergence** (noisy data *induces* loss divergence, distinct from LR-induced spikes); **silent data corruption** (NaN-propagating hardware faults — a named major reliability challenge requiring fault-tolerant systems); **GPU underutilization** (poor networking silently drops you to 40–50%, doubling cost with no alarm); **eval contamination** (test data leaking into training inflates your numbers — decontamination is a first-class data job); **catastrophic forgetting** (naive domain-knowledge addition erases general capability — the failure that pushes people toward continued-pre-training products).

### One-paragraph summary for a hiring manager

Pre-training from scratch is not a hire, it's a specialized org — minimum a pre-training research scientist, a distributed-training systems engineer, and a data-curation lead, all senior-plus, all scarce, all individually bid-on in the hottest talent market in tech. The bill runs $78M–$200M+ for frontier scale, and the decisions that determine whether that money is wasted (scaling-law de-risking, data mix, decontamination) are exactly the ones generalists get wrong. Default to renting an API or buying-and-adapting open weights; if you have genuinely unique data, use continued pre-training on a vendor checkpoint (e.g., Nova Forge) before considering from-scratch. Build from scratch *only* if the base model is your product or sovereignty forbids the alternatives — and apply the moat test before signing off.

---

## Sources

- Epoch AI — cost to train frontier models: https://epoch.ai/blog/how-much-does-it-cost-to-train-frontier-ai-models
- Epoch AI — data wall / high-quality token stock (exhaustion 2026–2032, 80% CI)
- Stanford AI Index 2025 — GPT-4 ~$78–100M+, Gemini Ultra ~$192M compute estimates
- DeepSeek-V3 Technical Report (671B/37B, FP8, ~2.788M H800 GPU-hours ≈ $5.6M final run): https://arxiv.org/html/2412.19437v1
- TechNode — DeepSeek V3 cost-cutting, May 2025: https://technode.com/2025/05/16/deepseek-reveals-cost-cutting-methods-for-v3-large-model-training-in-new-paper/
- ceramic.ai — DeepSeek cost/efficiency (~23% MFU) analysis: https://www.ceramic.ai/blog/re-deepseek
- cudocompute — cost breakdown (hardware 47–67%, R&D staff 29–49%): https://www.cudocompute.com/blog/what-is-the-cost-of-training-large-language-models
- Llama 3 paper — ~560 authors, 405B, ~30.8M H100 GPU-hours, ~15T tokens
- Kimi K2 technical report — MoE + Muon/MuonClip, ~1T params on 15.5T tokens, zero loss spikes: https://arxiv.org/html/2507.20534v1
- BeyondWeb / DatologyAI — synthetic data, 7.7× faster training, rephraser saturates ~3B: https://www.datologyai.com/blog/beyondweb
- FineWeb / FineWeb2 dataset writeups: https://arxiv.org/html/2506.20920v1 ; FineWeb-Edu (model-based filtering): https://www.emergentmind.com/topics/fineweb-edu-dataset
- "Beyond Chinchilla-Optimal: Accounting for Inference": https://arxiv.org/html/2401.00448v3
- aimultiple — LLM scaling laws (6·N·D FLOPs): https://aimultiple.com/llm-scaling-laws
- MoE data-wall acceleration: https://arxiv.org/abs/2605.17849
- xAI Colossus — company-stated ~555,000 GPUs / ~$18B (Jan–Feb 2026 announcements); ~2 GW power claim contested (Tom's Hardware satellite-imagery analysis suggesting ~350 MW cooling)
- Nucleotide Transformer v3, Dec 2025: https://instadeep.com/wp-content/uploads/2025/12/NT_v3.pdf
- Evo 2 / DNA foundation model benchmarking, Nature Comms 2025: https://www.nature.com/articles/s41467-025-65823-8
- SEA-LION v1 from-scratch → v2 continued pre-training on Llama 3 (~48B tokens), NVIDIA/Domyn: https://developer.nvidia.com/blog/continued-pretraining-of-state-of-the-art-llms-for-sovereign-ai-and-regulated-industries-with-domyn-and-nvidia-dgx-cloud/
- Lawfare — sovereign AI, 2025: https://www.lawfaremedia.org/article/sovereign-ai-in-a-hybrid-world--national-strategies-and-policy-responses
- Dicta-LM 3.0 (Hebrew sovereign LLM), 2026: https://arxiv.org/pdf/2602.02104
- "Reuse, Don't Retrain," 2024: https://arxiv.org/html/2407.07263v1
- "The Finetuner's Fallacy," 2026: https://arxiv.org/pdf/2603.16177
- BloombergGPT / domain-specific FM overview: https://arxiv.org/pdf/2409.04267
- aisuperior — cost to train LLM, 2026: https://aisuperior.com/cost-to-train-large-language-model/
- Label Your Data — pre-training vs fine-tuning, 2026: https://labelyourdata.com/articles/llm-fine-tuning/pre-training-vs-fine-tuning
- Galileo — LLM training cost, 2026: https://galileo.ai/blog/llm-model-training-cost
- HRM-Text ($1,500 / 16-GPU / 1.9-day; HRM/Hyena architecture, instruction-response + PrefixLM, ~40B tokens — corrected as a methodological mismatch): https://venturebeat.com/technology/researchers-say-they-trained-a-foundation-model-from-scratch-for-about-1-500 ; arXiv 2605.20613
- Amazon Nova Forge (three checkpoints, data-mixing, catastrophic forgetting): https://aws.amazon.com/blogs/aws/introducing-amazon-nova-forge-build-your-own-frontier-models-using-nova/ ; https://www.amazon.science/blog/amazon-nova-forge-open-training-paradigm-that-empowers-everyone-to-build-their-own-frontier-ai
- NVIDIA Cosmos 3 (mixture-of-transformers; COMPUTEX 2026 / report dated 2026-06-22, press clustering ~June 1): https://nvidianews.nvidia.com/news/nvidia-launches-cosmos-3-the-open-frontier-foundation-model-for-physical-ai ; https://www.hpcwire.com/aiwire/2026/06/01/nvidia-launches-cosmos-3-the-open-frontier-foundation-model-for-physical-ai/
- Biology / protein FMs (Biohub ESM): https://biohub.org/news/world-model-of-protein-biology/
- Weather FMs survey: https://arxiv.org/pdf/2501.06907
- Domain-specific FMs (healthcare/dental, finance): https://www.emergentmind.com/topics/domain-specific-foundation-models ; https://arxiv.org/html/2606.02914v1
- Code FMs (DeepSeek-Coder, Qwen3-Coder-Next, 2026 coding leaderboard): https://www.ibm.com/think/insights/code-llm ; https://www.morphllm.com/best-ai-model-for-coding
- Sovereign AI (CNAS index, India, Canada): https://interactives.cnas.org/reports/sovereign-ai-index/ ; https://ised-isde.canada.ca/site/ised/en/canadian-sovereign-ai-compute-strategy
- Defense (Maven, NGC2): https://defensescoop.com/2026/04/15/palantir-maven-smart-system-pentagon-program-transition-feinberg/ ; https://www.executivegov.com/articles/data-baseline-us-army-ngc2-palantir-anduril
- Build vs. buy economics: https://www.digitaldividedata.com/blog/enterprise-llm-training-services-build-buy-or-hybrid ; https://www.antino.com/blog/pre-training-vs-fine-tuning-vs-rag
- Open-model rosters / 2026 frontier landscape (Olmo 3, DeepSeek V4, Kimi K2, MoE roundups): https://codersera.com/blog/best-open-source-llm-2026-llama-4-qwen-3-5-deepseek-v4-gemma-4-mistral/ ; https://www.miniloop.ai/blog/best-open-source-llms-2026
- Distributed-training / fault-tolerance references: https://arxiv.org/pdf/2504.06095 ; https://link.springer.com/article/10.1007/s44336-026-00038-z
