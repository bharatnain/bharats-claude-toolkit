# Diffusion LLMs (dLLMs)

*State of the art as of late June 2026. Factual claims are labeled **(sourced)**, **(inference)**, or **(speculation)**; learning-design and organizational recommendations are labeled **(advisory)**.*

---

## 1. What it is

A diffusion LLM writes text **all at once and then fixes it up**, instead of writing it one word at a time from left to right.

The chatbots you know — GPT-style models, Claude, standard Gemini — are **autoregressive (AR)**: they predict the next word, append it, predict the next, and so on, strictly one token after another, never going back. A diffusion LLM instead starts from a blank or scrambled draft (a row of placeholder `[MASK]` tokens) and **iteratively cleans it up** over a handful of passes, filling in many words in parallel each pass. The idea is borrowed straight from image generators like Midjourney and Sora, which start from visual noise and progressively sharpen it into a picture. dLLMs do the same trick for text. **(sourced — arXiv 2506.17298)**

The headline payoff is **speed**. Because the model commits many tokens per step instead of one, it can generate far faster. Vendors report **1,000–2,100+ tokens/second** on a single high-end GPU, roughly **5–10x faster** than comparable AR models. **(sourced — arXiv 2506.17298; inceptionlabs.ai)** Read that number with care, though: it is a *best-case* figure — typically batch size of one, a single instance, and a fixed output length. In real serving, with batching and long context, the advantage shrinks and can vanish; one 2026 study found open dLLMs are often *slower* than AR models in practice (LLaDA-8B ran roughly 13.7x slower than LLaMA3-8B in a standard evaluation). **(sourced — arXiv 2510.18480)** So: the speed is real, but it is implementation-dependent, not automatic.

A second, quieter property matters too: a dLLM **sees context in both directions**. Because it works on the whole draft at once, when it fills a gap it knows what comes *after* the gap, not just before — unlike an AR model, which can only look backward. That makes dLLMs naturally good at editing, infilling, and satisfying rigid structure. **(sourced — Google DiffusionGemma blog)**

The notable systems in 2026:

- **Mercury / Mercury 2** (Inception Labs) — the first commercial dLLM; Mercury 2 (Feb 2026) is the first *reasoning-capable* diffusion model. **(sourced — businesswire.com, 2026-02-24)**
- **Gemini Diffusion** (Google DeepMind, research demo, May 2025) and the later open-weights **DiffusionGemma** (June 2026). These are two distinct things — see Section 6. **(sourced — blog.google)**
- **LLaDA / LLaDA 2.x** (Ant Group) — the leading open-weight family. **(sourced)**
- **Seed Diffusion** (ByteDance) — currently the speed leader at ~2,146 tok/s on H20 GPUs. **(sourced — huggingface.co/papers/2508.02193)**

The one-line mental model: **AR is a careful serial writer; diffusion is a fast parallel writer that drafts, then revises.** **(inference)**

---

## 2. How it works — mechanism and intuition

**The core object: masked denoising.**

Training is a fill-in-the-blanks game played at every difficulty at once:

1. Take a real sentence from the training data.
2. Randomly hide a fraction of its words — the fraction is itself chosen randomly each time, anywhere from "hide almost nothing" to "hide almost everything." Hidden words become a `[MASK]` token.
3. Show the model the Swiss-cheese sentence and ask it to **guess all the masked words at once** from the surrounding context.
4. Penalize wrong guesses; repeat across trillions of words.

Crucially the model sees context **in both directions** (bidirectional attention): a masked word in the middle is informed by words both before *and* after it. AR models can only ever look backward. **(sourced — arXiv 2506.17298)**

**Generation: denoising in steps.**

To produce an answer, the model starts with a row of all-`[MASK]` tokens and runs a few rounds:

- **Pass 1:** guess every blank at once. Most guesses are mediocre, but some it is very *confident* about.
- **Keep the confident ones, re-mask the shaky ones** — the key inference rule, often called confidence-based remasking.
- **Pass 2:** re-guess the remaining blanks, now helped by the words locked in during pass 1.
- Repeat until nothing is masked.

The intuition is solving a crossword. You don't fill squares strictly left to right — you fill the answers you're sure of, and those letters make the hard ones easier. Fewer passes means faster but rougher; more passes means slower but better. The number of denoising steps is the speed-versus-quality dial. **(sourced for the mechanism; inference for the crossword analogy)**

**Block diffusion — the 2026 production standard.**

Pure "denoise the whole answer at once" has two problems: the answer length must be fixed up front, and you lose the ability to reuse earlier computation. The dominant fix in 2026 is **block diffusion**: chop the output into small blocks (typically **32 tokens**), generate blocks left-to-right like an AR model, but run *diffusion in parallel inside each block*. This hybrid — sequential across blocks, parallel within them — partly restores **KV-caching** (reusing computation from earlier blocks), which is essential for real speed.

One precision the marketing tends to skip: this caching is **approximate and block-level, not the exact native cache AR models get for free**. Because attention is bidirectional, the cached keys and values for tokens that aren't finalized yet go *stale* on each denoising pass, so the cache is a lossy approximation that must be refreshed. This is a recurring theme — dLLM serving is its own engineering problem, not a solved one. **(sourced — arXiv 2512.17077; LLaDA 2.0 serving notes)**

**How they're built (training).** Two routes:

- **From scratch** — e.g. LLaDA 8B trained on ~2.3 trillion tokens. Expensive. **(sourced)**
- **Adapt an existing AR model** (the dominant 2026 pattern) — take a finished GPT/LLaMA-style model and continue-train it with the diffusion objective, gradually shifting its attention from backward-only to bidirectional. This needs roughly an *order of magnitude less* data. DiffuLLaMA, for instance, adapted with on the order of **~65 billion** tokens — well under 200B. **(sourced)** This cheap conversion path is why dLLMs proliferated so fast: you can convert frontier AR checkpoints instead of rebuilding from zero.

---

## 3. Why it works — the principle, and why the naive version fails

**The principle.** Most of the work in writing text is *understanding the constraints*, not the physical act of emitting tokens left to right. Once the meaning is pinned down, many words are nearly determined by their neighbors and can be settled in parallel. AR models impose a strict ordering that is **convenient for the math, not required by language**. Diffusion drops that ordering — trading a guaranteed-correct-but-serial recipe for a parallel one — then claws back the lost accuracy with a few refinement passes. **(inference, grounded in the mechanism)**

**Why the naive version fails (the central catch).** If you simply ask the model to guess *all* masked words at once and keep them all, you get garbage. This is the **conditional-independence problem**: predicting every blank simultaneously assumes each blank is independent of the others given the context. But words aren't independent. For "I'll have coffee ___ ___," one blank might independently prefer "with milk" and the other "or tea," yielding the incoherent "with tea." Each guess is locally reasonable; together they're nonsense. **(sourced)**

The fixes that make dLLMs actually work:

- **Iterative remasking** — don't commit all blanks at once. Lock in only high-confidence tokens, then re-predict the rest *conditioned on* what's now fixed. This re-introduces the dependencies you skipped. **(sourced)**
- **Block diffusion** — small blocks (32 tokens) bound how many tokens you're guessing "blind" at any moment, limiting the damage. **(sourced)**
- **More denoising steps** when quality matters; fewer when speed matters.

So the real trade is: AR *guarantees* it respects word-to-word dependencies (each token sees all prior ones), at the cost of being strictly serial. Diffusion *gambles* on parallelism and then pays down the resulting incoherence through refinement passes. The whole art is paying the smallest refinement bill for the most speed. **(inference)**

**Where they are still behind (mid-2026).** **(sourced)**

- **Raw quality:** dLLMs have not beaten the best AR models overall; they are closest in **code generation**, where rigid structure helps parallel guessing.
- **Fixed length:** classic dLLMs must pre-commit an output length. Too long → repetition, hallucination, wasted compute; too short → broken reasoning. (Active 2026 work makes them "length-aware," e.g. letting an end-of-sequence token decide when to stop.)
- **Reasoning / coordination:** long chains of reasoning suffer because the tokens lack the strict step-by-step dependency AR gets for free; accuracy degrades as generation length grows. Some 2026 work bolts an AR "plan" in front as a scaffold.
- **Alignment lag:** many dLLMs are less polished with RL post-training, partly explaining the remaining gap — and creating a real safety weakness (Section 6).

---

## 4. People & resources — team, compute, time, money, data

**Who builds these.** The field was opened commercially by **Inception Labs**, founded 2024 in Palo Alto by three academics who were early contributors to the underlying techniques: **Stefano Ermon** (Stanford), **Aditya Grover** (UCLA), and **Volodymyr Kuleshov** (Cornell). Ermon is a genuine pioneer of **score-based generative modeling** (Song & Ermon, NeurIPS 2019; Score-Based SDEs, ICLR 2021), foundational theory behind modern diffusion. Note that Inception's framing of him as "co-inventor of the methods behind Sora/Midjourney" is marketing shorthand: he co-developed the foundational diffusion *theory*; he did not build Sora or Midjourney. **(sourced for the publications; the "Sora/Midjourney" gloss is PR / inference, not a clean technical fact.)** The other serious players are large industrial labs: **Google DeepMind** (Gemini Diffusion / DiffusionGemma), **ByteDance** (Seed Diffusion), **Ant Group** (LLaDA). **(sourced)**

**Money.** Inception raised a **$50M seed round** — *not* a Series A — led by **Menlo Ventures**, with **Mayfield, Innovation Endeavors, M12** (Microsoft), **Snowflake Ventures, Databricks Investment**, and **NVentures** (NVIDIA) participating, plus angels **Andrew Ng** and **Andrej Karpathy**. **(sourced — TechCrunch / TradedVC / BusinessWire, 2025-11-06)** This is startup-scale capital, orders of magnitude below the multi-billion-dollar raises of frontier AR labs — and that contrast is the point. The diffusion bet is partly an *efficiency* bet (cheaper inference, faster output), so the capital story is "do more with less." **(sourced for the $50M; the framing is inference)**

**Compute and time — concrete anchors:** **(sourced unless noted)**

- **From scratch:** LLaDA 8B ≈ **0.13 million H800 GPU-hours** on ~2.3T tokens. At rough cloud rates (~$2/GPU-hr), order-of-magnitude **~$250K–$500K** in pure compute. *(GPU-hours sourced; dollar figure inferred from public pricing)*
- **Smaller from-scratch:** Dream 7B ≈ **96 NVIDIA H800 GPUs for 256 hours** (~24.6K GPU-hours) on ~580B tokens. *(sourced — arXiv 2508.15487 / HKU NLP. Note: H800, not H100.)*
- **Adapting an AR model (the cheap path):** TESS-2 *reports* roughly **250 H100-hours** for a light adaptation and **~2,000 H100-hours** for a heavier one — low thousands to low tens of thousands of dollars, a genuine order-of-magnitude saving versus from-scratch. *(GPU-hours reported in arXiv 2502.13917 but only medium-confidence on these exact numbers; dollar figures inferred.)*

**Data scale.** From-scratch dLLMs consume the same order as AR models — **trillions** of tokens (LLaDA: 2.3T). Adaptation needs **hundreds of billions or fewer** (DiffuLLaMA: ~65B). **(sourced)**

**Team size.** Not publicly disclosed, but the pattern is clear: a **small research team** — a handful of founding scientists plus modest engineering staff — can ship a competitive dLLM by *adapting* existing checkpoints, versus the hundreds-strong orgs behind frontier AR models. **(inference)**

**Hardware reality.** The speed numbers assume **datacenter GPUs** (H100 / H20 / H800). DiffusionGemma notably claims 700+ tok/s on a **consumer RTX 5090**, hinting at a near-term path to fast *local* text generation. **(sourced)**

---

## 5. Scenarios & stories — right tool, wrong tool

Everything good and bad about dLLMs traces back to the two facts from Section 1: they can be **fast** (many tokens per step) and they can **see both directions** (whole-canvas editing). Here is where that matters.

### Where it is the RIGHT tool

**1. Autocomplete that beats the developer's fingers.** A suggestion that arrives 2 seconds late is worthless — the human has already typed past it. A serial model generating a 40-token completion at 100 tok/s spends ~400ms before it even finishes; a diffusion model emitting that block in tens of milliseconds lands the suggestion while the cursor is still blinking. Short output, hard latency ceiling, quality only has to be "good enough to accept or reject." This is the canonical dLLM win, and code is the one domain where dLLMs have reached benchmark parity (see Section 6). **(sourced / inference)**

**2. The agent that gets more thinking done per second.** An agent loop chains dozens of calls — plan, call a tool, read the result, re-plan. Wall-clock time is the *sum* of those calls. Within a fixed latency budget ("the user will wait 8 seconds"), a faster model can take more steps — and more steps means more self-correction, more verification, *better answers through more iteration*, not just the same answer sooner. Picture a coding agent that, in the time a slow model drafts one fix, runs the tests, reads the failure, patches, and re-runs — twice. It won by getting more turns of the crank. **(sourced — Inception positions Mercury 2 for agentic stacks)**

**3. The voice assistant that doesn't leave dead air.** Natural conversation tolerates only ~200ms of silence before a pause feels wrong. A model needing 600ms to start speaking makes every exchange laggy; a dLLM that produces a short reply inside that window keeps the rhythm. Short turns, real-time cadence, conversational (not literary) quality — the sweet spot. **(sourced)**

**4. "Fill in the middle" jobs — editing, infilling, constrained generation.** This advantage comes from *bidirectionality*, not speed. Inserting a function that must fit the lines above *and* below; rewriting one clause so it reads cleanly into the next sentence; generating output that satisfies a rigid structure (a fixed start and end with the model owning only the middle). A left-to-right model is half-blind here; a diffusion model holds the document fixed except the gap and solves it with full knowledge of both sides. **When the task is "fit into a fixed surrounding context," diffusion isn't just faster — it's a better fit for the shape of the problem.** **(sourced for the vendor claims; inference for the framing)**

**5. The high-volume, latency-sensitive backend nobody sees.** RAG pipelines (retrieve → rerank → summarize) where latencies stack; moderation or classification at millions of short calls a day. Short, structured outputs where throughput beats polish and you want a reasoning step without blowing the latency budget. Mercury 2's pitch — tunable reasoning plus schema-aligned JSON at four-digit tok/s and ~$0.25/$0.75 per million tokens — aims precisely here. **(sourced — inceptionlabs.ai)**

### Where it is the WRONG tool

**1. The long-form essay, brief, or chapter.** A 4,000-word argument where paragraph 30 must honor a commitment from paragraph 3. Long-range coherence over long output is exactly diffusion's weakness; mid-2026 surveys are blunt that dLLMs still lag AR on complex reasoning, long-form coherence, and strict format adherence. Speed is no consolation if the thing drifts. **(sourced)**

**2. The genuinely hard, novel reasoning problem.** A competition-math proof, an unfamiliar multi-step logic puzzle, a long unbroken "if this, then that" chain. Even with reasoning dLLMs like Mercury 2, the center of gravity for the hardest deliberate reasoning is still AR, whose token-by-token chain naturally fits sequential deduction. Choose for correctness first; don't let the tok/s number seduce you where being fast and wrong is the worst outcome. **(inference, grounded in sourced quality caveats)**

**3. The single enormous prompt you read once and answer once.** dLLMs have made real long-context gains (DiffusionGemma advertises 256K; research models reach 128K) and even degrade *gracefully* past their trained length. But raw context size is not cheap serving. Their bidirectional, multi-pass attention creates a heavier memory profile — a December 2025 systems paper calls it a "memory footprint crisis" and notes dLLMs **can't batch at the token level** the way AR servers do. For one-shot "read this giant document and answer," a mature AR stack is often cheaper and simpler. **The speedup is per-request; it can be eaten alive by serving overhead at scale.** **(sourced — arXiv 2512.17077; 2510.18480)**

**4. The strict-determinism, audit-trail job.** Regulated document assembly, compliance pipelines, anything where "emit precisely this schema, no exceptions" is a hard requirement. Strict format adherence is a named dLLM weakness, and parallel refinement is less suited to *guaranteeing* an exact constrained string than constrained-decoding AR, which commits one validated token at a time. If you need a *guarantee* rather than a *very-likely*, lean AR. **(sourced for the weakness; advisory for the recommendation)**

**5. The small, occasional task where speed is irrelevant.** Summarizing a few emails an hour: latency is invisible and the exotic serving requirements are pure downside. **dLLMs earn their keep under latency or volume pressure. Remove both and the reason to choose them evaporates.** **(advisory)**

### Decision heuristic (advisory)

1. **Is latency the binding constraint?** Autocomplete, voice, tight agent loops, high-volume backends — if yes, a dLLM is a real candidate. If latency genuinely doesn't matter, you probably don't need one.
2. **Is the output short or structurally local?** Short completions, infilling, fit-into-context edits, schema outputs — strengths. Long narrative or long deduction — weaknesses.
3. **Have you confirmed parity on *your* task and *your* serving budget?** Vendor speed is real but per-request; the serving cost and the quality gap on hard/long tasks are also real. Benchmark on your own workload. There is no free lunch.

A compact way to remember it: **diffusion LLMs are a latency-and-locality tool, not a general upgrade.**

---

## 6. Cross-industry usage and positioning (June 2026)

**The one-paragraph version.** As of June 2026, dLLMs have crossed from research curiosity into real production — but only in a specific niche: places where **low latency matters more than peak intelligence**. They are table-stakes nowhere yet, cutting-edge in several places, and dominant in exactly one zone: fast, interactive code and agent loops.

**A scale for reading the map:** *Absent* (basically nobody) → *Experimental* (labs and a few pilots) → *Emerging* (real deployments by early adopters, still a minority) → *Cutting-edge / contested* (frontier actively being fought over). Nowhere is it yet **table-stakes**. That is the headline finding.

### The models that matter — and an important disambiguation

**Inception — Mercury 2** (launched 24 Feb 2026). The flagship commercial dLLM and the first *reasoning* diffusion model. ~1,009 tok/s on NVIDIA Blackwell (best-case), 128K context, native tool use, JSON output, ~$0.25 / $0.75 per million tokens. Critically **OpenAI-API-compatible** — a drop-in swap with no rewrite, which is the single biggest reason it spreads. Named customers: Zed (code editor), Wispr Flow (voice transcription), Skyvern (browser automation), OpenCall (voice agents), SearchBlox (enterprise search). **(sourced)**

**Google — two distinct things, often conflated:**
- **Gemini Diffusion** — a Google I/O *research demo* (20 May 2025), benchmarked against **Gemini 2.0 Flash-Lite**. This is the model that posted the parity numbers people quote: **HumanEval 89.6% vs 90.2%, MBPP 76.0% vs 75.8%**, and a ~**1,479 tok/s** figure. **(sourced)**
- **DiffusionGemma** — a later, *different* model (release **10 June 2026**, I/O recap **11 June 2026**): open-weights (Apache 2.0), a 26B Mixture-of-Experts, ~4x faster generation, on Hugging Face / Kaggle / Vertex. Critically, Google positions it as **research/local-only, NOT production-quality** — and it actually *trails* autoregressive Gemma 4 on most benchmarks (MMLU-Pro 77.6 vs 82.6; AIME 2026 69.1 vs 88.3). **(sourced)**

The benchmark-parity story belongs to the **2025 research demo**, not the **2026 open release**. Several write-ups blur the two; they are distinct, and Google still recommends AR Gemma 4 for production — a tell about the whole field's maturity.

**ByteDance — Seed Diffusion.** ~2,146 tok/s on H20 GPUs, the raw-speed leader on the code frontier. **(sourced)**

**Open source — LLaDA, Dream-7B, d3LLM.** Where most academic and on-device work lives, plus robotics variants (LLaDA-VLA, Dream-VLA). **(sourced)**

**Who leads:** Inception in *commercial reasoning production*; ByteDance in *raw speed*; Google in *open-weights scale and reach*; the LLaDA/Dream academic groups in *open research and new modalities*.

### Cross-industry walkthrough

- **Coding & dev tools — cutting-edge, and the closest thing to "winning."** Developers tolerate slightly lower peak quality if completions feel *instant*; editing code is inherently non-linear (the bidirectional fit); agent loops make latency compound. Zed ships Mercury; JetBrains flagged diffusion as a 2026 workflow shift; Red Hat published developer guidance. *Verdict: emerging-toward-standard for autocomplete and fast agent loops; not yet default for deep one-shot reasoning over a big codebase.* **(sourced for adoption; inference for "closest to winning")**
- **Customer support & consumer voice — emerging, fast.** "Feels instant" is the entire UX. OpenCall, Wispr Flow, and avatar products are named Mercury customers. *Verdict: emerging, strong product-market fit.* **(sourced)**
- **Robotics — experimental, architecturally exciting.** Robots plan action sequences where a later action constrains an earlier one — non-linear, which diffusion handles natively. LLaDA-VLA and Dream-VLA (vision-language-action) are cutting-edge research, not deployed product. *Verdict: experimental, watch closely.* **(sourced)**
- **Science (protein / DNA / drug design) — emerging, uniquely well-suited.** Diffusion has been table-stakes in protein/DNA *structure* design for years; the 2026 twist is that discrete diffusion *language* models are now fine-tuned to design sequences, because a base is constrained by what comes *after* it as well as before. A 2026 Benchling report shows biotech AI adoption crossing from pilots to operations (76% literature review, 71% protein-structure prediction), though much of that is broader AI. *Verdict: emerging, possibly where dLLM-style models matter most long-term.* **(sourced for stats; inference for "best-suited")**
- **Healthcare — experimental / cautious.** Latency helps at the bedside and biology adjacency helps, but explainability, correctness guarantees, and the FDA's tightening 2025–2026 AI bars favor caution. *Verdict: experimental; the regulatory ceiling is the gate.* **(sourced for regulatory direction; advisory on caution)**
- **Finance — experimental, internal-tooling-first.** Loves low latency and low cost-per-token, but shares healthcare's auditability demands. Expect internal, lower-stakes tooling (search, summarization, reranking) before anything touching trades. **(inference)**
- **Legal — mostly absent / experimental.** Legal rewards exactly what dLLMs are weakest at (maximum accuracy, careful long-form reasoning, zero confident errors) with latency a distant concern — the least natural fit. **(inference, grounded in the AR-vs-diffusion consensus)**
- **Defense — experimental, with a real concern.** Edge/on-device appeal is real (diffusion's advantage is strongest at low batch size on a single accelerator). But a string of 2026 papers (DIJA, DiffuGuard, "The Devil behind the mask") shows a *structural* safety weakness: because dLLMs fill many masked tokens *in parallel*, they can't do the token-by-token "stop and refuse" that AR models do, so AR-tuned jailbreak defenses break down. *Verdict: experimental; safety maturity is the gate.* **(sourced for the research; inference for positioning)**

### Settled vs still moving

**Settled (June 2026):** dLLMs are real, in production, fast (best-case), and cost-competitive. The "diffusion can't reason" objection is gone — Mercury 2 broke it in February. OpenAI-API compatibility makes trying one nearly free. **(sourced)**

**Still contested:** (1) *quality at the top end* — even Google won't call its diffusion model production-grade, and AR still wins deep reasoning and long-form; (2) *real-world speed* — open dLLMs are often *slower* in practice once KV-cache inefficiency and memory pressure are counted; (3) *safety* — the parallel-decoding jailbreak weakness is live and unsolved. **(sourced)**

---

## 7. Learning path for a technical leader

*For someone who decides, funds, hires, and challenges — not someone who writes the kernels. No coding labs. Your job is to know when the speed is worth the tradeoff, whether a vendor's claims are real, and whether an "expert" actually understands the failure modes.* **(advisory throughout this section)**

### Five mental models (90% of the understanding)

- **MM1 — Sequential vs. parallel.** AR is a writer who commits each word before seeing the next and can never revise (serial: slow but coherent). Diffusion is a sculptor: it roughs out the whole block, then refines everywhere at once (parallel: fast, but must work to stay self-consistent). *Everything else flows from this.*
- **MM2 — Denoising as "guess, keep, redo."** Trained by hiding words and learning to fill them in; at generation it predicts all blanks, **keeps** the confident ones, **re-blanks** the uncertain ones, and repeats. How many steps, and how aggressive the keep/redo policy, governs quality and speed.
- **MM3 — The parallelism tax.** Filling many blanks at once guesses each *as if the others don't exist* — the conditional-independence problem. More parallelism (speed) risks incoherence (quality). The whole frontier is about taxing this less.
- **MM4 — Bidirectional context cuts both ways.** Seeing the whole draft is great for editing, infilling, and structure — but it's *also why* dLLMs can't reuse the normal KV cache and *part of why* they struggle with strictly sequential reasoning. Strength and weakness share one root.
- **MM5 — Speed is a systems property, not just a model property.** Headline tok/s depends on GPU, batch size, sequence length, the keep/redo schedule, and caching tricks. Treat any single speed number like a single benchmark score.

### Reading spine (in order; concepts, not code)

1. **"A Survey on Diffusion Language Models" (arXiv 2508.10875)** — the best field map; skim intro + taxonomy. (`VILA-Lab/Awesome-DLMs` tracks updates.)
2. **A plain-English end-to-end explainer** — e.g. *Daily Dose of DS*, "Diffusion LLMs from the Ground Up."
3. **The Mercury paper (arXiv 2506.17298)** — the first widely-cited *commercial* dLLM writeup; read for what a real product claims and how it's measured.
4. **Gemini Diffusion announcement (Google, May 2025) + DiffusionGemma blog (June 2026)** — note the two are different models; the parity numbers (HumanEval 89.6 vs 90.2) belong to the 2025 demo.
5. **A counter-weight on agentic failure** — e.g. "The Bitter Lesson of Diffusion Language Models for Agentic Workflows" (arXiv 2601.12979) — where dLLMs fail today.
6. **One inference-engineering piece** — *Fast-dLLM* (KV cache + parallel decoding) or a 2026 consistency-distillation writeup.

*Classics to know by name (don't read in full): D3PM (Austin 2021), MDLM (Sahoo 2024), LLaDA (Nie 2025), Dream (Ye 2025).*

### Understanding checkpoints (self-test)

- Explain to a non-technical exec why dLLMs are faster, in two sentences, *without* using "parallel" as a magic word.
- Describe the **parallelism tax** and why speed and quality pull against each other.
- Explain why a dLLM **can't use the normal KV cache** and why that matters for serving cost.
- Name **three fitting use cases** and **two unfitting ones**, and defend each.
- Read a "2,000 tokens/sec" claim and list **four questions** that decide if it's real for *your* workload (GPU? batch size? sequence length? quality at that operating point?).
- State the honest mid-2026 verdict: production-grade for speed-critical generation and coding; *not yet* default for deep agentic reasoning; open-source tooling ≈ where AR was in early 2024.

### How to evaluate an expert in an interview

- **"Why is a dLLM faster — and what do you give up?"** *Strong:* serial-vs-parallel framing, then *immediately* volunteers the conditional-independence tradeoff, treats it as a tunable dial. *Red flag:* claims faster *and* strictly better with no downside.
- **"Walk me through one generation step."** *Strong:* start-from-masked → predict all blanks → keep confident, remask uncertain → repeat; notes the policy drives quality and step count. *Red flag:* describes left-to-right token prediction (that's AR — paradigm confusion).
- **"Why can't dLLMs use the AR KV-cache trick?"** *Strong:* ties to bidirectional attention (cached keys/values go stale each pass), cites 2026 workarounds *and* that they're lossy approximations. *Red flag:* doesn't know what a KV cache is.
- **"Where would you NOT deploy a dLLM today?"** *Strong:* long-horizon agentic planning, multi-step reasoning, self-correcting tool use. *Red flag:* "it works for everything, just faster."
- **"A vendor demos 2,000 tok/s. Is it meaningful for us?"** *Strong:* interrogates GPU, batch size, sequence length, and *quality at that operating point*; wants the speed–quality *curve* on *their* workload. *Red flag:* takes the number at face value.
- **(Stretch) "What changed in the last year to move dLLMs toward production?"** *Strong:* initialize-from-AR-then-continue-with-diffusion, block diffusion (~32-token blocks), consistency/distillation cutting step counts, adaptive KV caching. *Red flag:* only references 2023–2024 work; unaware of Mercury, Gemini Diffusion, Seed Diffusion, LLaDA-2.x. Stale knowledge is itself a signal.

**General red flags:** using "parallel / denoising / diffusion" as incantations; never volunteering a tradeoff; confusing *image* diffusion (continuous noise) with *text* diffusion (masking); presenting dLLMs as a wholesale AR replacement rather than a complementary speed/infilling tool; citing only their employer's model.

### Honest verdict (June 2026)

dLLMs are real, fast (best-case), and shipping — matching AR on coding benchmarks. Genuinely better for latency-critical generation, code, and infilling/editing. *Not yet* the right default for deep multi-step reasoning or long-horizon agents. Open-source ecosystem is functional but immature ("where AR open source was in early 2024"). Leadership posture: **pilot dLLMs where speed is the product, keep AR for the hard reasoning, re-evaluate every two quarters.** **(advisory)**

---

## 8. Team notes

*Staffing and org decisions if your team wants to use or build on dLLMs. Factual claims tagged; all role, hiring, and build-vs-buy recommendations are **(advisory)**.*

### Roles and seniority — or does an existing role absorb it?

The honest default: **no new role for most teams.** **(advisory)**

- **Using a dLLM via API (rent/buy path).** Mercury 2 is OpenAI-compatible — swap the base URL and key. Absorbed by whoever already owns your AR integration. The one genuinely new muscle is *latency-aware product design* — knowing which calls benefit from the speed (autocomplete, voice, agent loops) and which don't. New skill, not new headcount.
- **Self-hosting an open dLLM.** Here a real gap opens. dLLMs break the assumptions your serving stack is built on, so you need a **senior inference/systems engineer** comfortable below the framework line — CUDA-adjacent, vLLM/SGLang internals, memory profiling. A generalist who has only ever run `vllm serve` will struggle.
- **Training or fine-tuning a dLLM.** A **senior research engineer / applied scientist (ideally PhD-level)** with real diffusion *and* sequence-modeling depth. A specialist hire, not a stretch assignment. Postings for diffusion work cluster around ML/DL fundamentals + strong math + PyTorch internals, US contract rates ~$38–$96/hr. **(sourced — ziprecruiter.com, 2026-05-30)**

**Seniority bias:** dLLM tooling in mid-2026 sits roughly where open-source AR tooling sat in early 2024 — functional, improving fast, missing guardrails. **(sourced)** Immature ecosystems punish juniors (no Stack Overflow answer yet); pay for seniority that can read papers and source code. **(inference)**

### Hiring signals and red flags

**Green signals (self-host or training hire):**
- Can explain *why* dLLM throughput collapses at long context and large batch — not just quote a tok/s number. **(advisory)**
- Talks in **FLOPs per token**, not just tokens/sec — dLLMs have high GPU utilization but spend far more compute per token; conflating the two leads to over-promising. **(sourced — arXiv 2510.18480)**
- Has actually profiled GPU memory — dLLMs produce oscillating, expanding-and-contracting activation footprints that OOM-crash schedulers built for AR's monotonic growth. **(sourced — arXiv 2512.17077)**
- Treats inference hyperparameters (denoising steps, block size) as things tuned *per workload*. **(sourced — arXiv 2502.09992)**

**Red flags:**
- Quotes a vendor's "2,000 tok/s" as your production number. Those are typically batch-1, single-instance, fixed-length best cases; advantages shrink or vanish as batch size grows. **(sourced — arXiv 2510.18480)**
- Frames dLLMs as a universal AR replacement.
- Can't name a downside — the fixed-length-output and weak-KV-cache problems are well known; a real practitioner leads with them. **(sourced)**
- Resume conflates *image* diffusion with *text* diffusion — overlapping math, very different engineering. **(inference)**

### Build vs. buy (default = rent/buy)

- **Rent the API (right for ~95% of teams).** Mercury 2 ~$0.25 / 1M input, ~$0.75 / 1M output — roughly the price of a quantized fast AR model but ~5x faster generation, with 128K context, tool use, JSON. Also on Azure AI Foundry and OpenRouter. You get the speed with zero serving pain. **(sourced)**
- **Self-host an open model (LLaDA, Dream, Mercury Coder Mini 1.3B Apache-2.0)** *only if* you have a hard data-residency/privacy requirement or genuinely huge steady volume — and you staff the senior systems engineer above. Be warned: naïve self-hosting often runs *slower* than equivalent AR (LLaMA3-8B has shown ~13.7x higher throughput than LLaDA-8B in standard eval); the speed only materializes with specialized serving (block diffusion, KV-cache adaptations, SlowFast Sampling, Consistency dLLMs). **(sourced — arXiv 2510.18480; together.ai)**
- **Train your own — almost never.** Only if dLLM speed at *your* quality bar *is* the product (a coding-tool or real-time-voice company where per-call latency is the moat) and the frontier APIs can't hit your constraint. Even then, adapt an existing AR checkpoint rather than train from scratch. **(sourced)**

**Moat test:** owning is justified only when the model's behavior *is* your differentiation and rent can't deliver it. Speed alone isn't a moat once three vendors sell 1,000+ tok/s off the shelf. **(advisory)**

### Common failure modes

**Org / decision:**
- **Buying the benchmark, shipping the disappointment.** Headline speeds are batch-1 best cases; under production batching your AR baseline may match or beat the dLLM. Pilot on *your* traffic shape first. **(sourced — arXiv 2510.18480)**
- **Using a dLLM where AR is better.** For *short* outputs AR is usually faster — the dLLM pays for all its denoising passes regardless of length. dLLMs win on *longer* generations and interactive loops. **(sourced — seangoedecke.com)**
- **Ignoring long-context cost.** Weak KV-caching means dLLMs recompute attention over the whole context every pass; throughput drops sharply as length grows (one study: ~75% drop going 0-shot → 5-shot). Long-RAG-context is a bad fit. **(sourced)**
- **Treating speed as free quality.** The speed knob is a *tradeoff* — fewer passes means lower quality. Crank speed and skip eval and you ship worse output. **(sourced)**

**Engineering (self-host):** OOM crashes from AR-shaped schedulers on oscillating dLLM memory; fixed-length-output friction; hyperparameter sensitivity that silently degrades across workloads. **(sourced — arXiv 2512.17077; 2502.09992; seangoedecke.com)**

**Capability caveat:** reasoning on diffusion was an open question; Mercury 2 is marketed as the first *reasoning* dLLM, and code benchmarks roughly match AR (the 2025 Gemini Diffusion demo: HumanEval 89.6% vs 90.2%, MBPP 76.0% vs 75.8%). The gap is narrowing but verify on *your* tasks. **(sourced)**

### Bottom line

Rent the API and let your existing LLM-integration owner absorb it — right for nearly everyone, and the speed is genuinely useful for autocomplete, voice, and agent loops. Self-hosting needs a real senior systems engineer and can backfire on speed if understaffed. Training your own is justified only when low-latency generation *is* your product. The single most common mistake is believing the batch-1 benchmark — pilot on your own traffic first. **(advisory)**

---

## Sources

- Mercury: Ultra-Fast Language Models Based on Diffusion — https://arxiv.org/abs/2506.17298 — accessed 2026-06-25
- Diffusion LLMs from the Ground Up — Daily Dose of DS — https://www.dailydoseofds.com/diffusion-models-part-2/ — accessed 2026-06-25
- Seed Diffusion: A Large-Scale Diffusion Language Model — https://huggingface.co/papers/2508.02193 ; https://arxiv.org/pdf/2508.02193 — accessed 2026-06-25
- Dream 7B: Diffusion Large Language Models — https://arxiv.org/abs/2508.15487 ; https://hkunlp.github.io/blog/2025/dream/ — accessed 2026-06-26
- DiffusionGemma: 4x faster text generation — Google — https://blog.google/innovation-and-ai/technology/developers-tools/diffusion-gemma-faster-text-generation/ ; https://ai.google.dev/gemma/docs/diffusiongemma — accessed 2026-06-25
- Google I/O 2026 recap (DiffusionGemma, 2026-06-11) — https://luonghongthuan.com/en/blog/google-io-2026-agentic-gemini-diffusiongemma-2026-06-11/ — accessed 2026-06-25
- Inception raises $50M seed — TechCrunch (2025-11-06) — https://techcrunch.com/2025/11/06/inception-raises-50-million-to-build-diffusion-models-for-code-and-text/ — accessed 2026-06-26
- Inception Raises $50M Seed (investor list) — TradedVC — https://traded.co/vc/deal/inception-raises-50m-seed-funding-led-by-menlo-ventures-with-participation-from-top-investors/ — accessed 2026-06-26
- Inception Raises $50M — BusinessWire (2025-11-06) — https://www.businesswire.com/news/home/20251106570339/en/ — accessed 2026-06-26
- Inception Launches Mercury 2 — BusinessWire (2026-02-24) — https://www.businesswire.com/news/home/20260224034496/en/ — accessed 2026-06-25
- Introducing Mercury 2 — Inception — https://www.inceptionlabs.ai/blog/introducing-mercury-2 — accessed 2026-06-25
- TESS 2: A Large-Scale Generalist Diffusion Language Model — https://arxiv.org/pdf/2502.13917 — accessed 2026-06-25 (GPU-hour anchors medium-confidence)
- How Efficient Are Diffusion Language Models? (real-world speed caveats) — https://arxiv.org/html/2510.18480v3 — accessed 2026-06-25
- dLLM serving / memory-footprint crisis — https://arxiv.org/html/2512.17077 — accessed 2026-06-25
- Diffusion LLM with Native Variable Generation Lengths ([EOS]) — https://arxiv.org/html/2510.24605v1 — accessed 2026-06-25
- Think First, Diffuse Fast (AR plan conditioning) — https://arxiv.org/pdf/2603.13243 — accessed 2026-06-25
- Beyond Autoregression: Diffusion LLMs for Code Generation — https://arxiv.org/pdf/2509.11252 — accessed 2026-06-25
- A Survey on Diffusion Language Models — https://arxiv.org/abs/2508.10875 ; https://github.com/VILA-Lab/Awesome-DLMs — accessed 2026-06-25
- Score-based generative modeling: Song & Ermon (NeurIPS 2019); Score-Based SDEs (ICLR 2021) — foundational diffusion theory
- JetBrains AI — Why Diffusion Models Could Change Developer Workflows in 2026 — https://blog.jetbrains.com/ai/2025/11/why-diffusion-models-could-change-developer-workflows-in-2026/ — accessed 2026-06-25
- Red Hat Developer — Beyond the next token — https://developers.redhat.com/articles/2026/04/28/beyond-next-token-why-diffusion-llms-are-changing-game — accessed 2026-06-25
- d3LLM (ICML 2026) — https://github.com/hao-ai-lab/d3LLM — accessed 2026-06-25
- LLaDA-VLA — https://arxiv.org/pdf/2509.06932 ; Dream-VLA — https://arxiv.org/pdf/2512.22615 — accessed 2026-06-25
- DNA/protein diffusion LM design — https://arxiv.org/pdf/2603.17919 — accessed 2026-06-25
- IntuitionLabs — LLM benchmarks in life sciences (Benchling adoption) — https://intuitionlabs.ai/articles/large-language-model-benchmarks-life-sciences-overview — accessed 2026-06-25
- Safety/jailbreak research: DIJA — https://arxiv.org/pdf/2507.11097 ; DiffuGuard — https://arxiv.org/pdf/2509.24296 ; Jailbreaking LLDMs — https://arxiv.org/pdf/2507.19227 — accessed 2026-06-25
- Together AI — Consistency dLLMs (CDLM) — https://www.together.ai — accessed 2026-06-25
- Sean Goedecke — diffusion LLM tradeoffs — https://www.seangoedecke.com — accessed 2026-06-25
- ZipRecruiter — diffusion model engineer rates (2026-05-30) — https://www.ziprecruiter.com — accessed 2026-06-25
- Inference hyperparameter sensitivity — https://arxiv.org/abs/2502.09992 — accessed 2026-06-25
