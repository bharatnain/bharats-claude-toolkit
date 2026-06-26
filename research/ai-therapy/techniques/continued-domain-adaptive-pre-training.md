# Continued / domain-adaptive pre-training

*State of the art as of June 2026. Written for a highly intelligent reader who will sponsor, staff, and judge this work — not write the training loop. Factual claims are labeled sourced (with URL + date), inference, or speculation; learning-design and org recommendations are labeled advisory — my reasoned read, not a sourced fact.*

---

## 1. What it is

You have a finished, general-purpose large language model — say a 7B or 70B open-weight model trained on trillions of tokens of the open internet. It is competent at everything and expert at nothing. You want it to *deeply know* a narrow world: your bank's products, ten years of radiology reports, your fifteen-year-old internal codebase, a body of case law, or a language the web barely covers.

**Continued pre-training** is the move where you take that already-trained model and keep training it — using the *same* learning objective it was originally built with (predict the next token over raw text), but now on *your* text. You are not teaching it a task. You are soaking it in a domain until that domain's vocabulary, idioms, and statistical regularities become part of its weights. A useful image: you are not filling a database, you are **moving the model's center of gravity** into your domain, so its instincts — which word tends to follow which, what "normal" looks like here — change.

The single most important distinction, and the one people get wrong most often:

| | **Continued pre-training (CPT / DAPT)** | **Fine-tuning (SFT / instruction tuning)** |
|---|---|---|
| What it changes | Knowledge, vocabulary, "how this domain talks" | Behavior, format, "how to respond" |
| Data | Raw text, billions of tokens, no labels | Curated prompt→answer pairs, thousands to millions |
| Objective | Next-token prediction (same as the original) | Next-token, but only scored on the "answer" part |
| Analogy | Send a sharp generalist to live in a new country for a year | Teach that person the script for one specific job |

A few terms now travel together, and the differences matter in 2026 (sourced — https://futureagi.com/blog/continued-llm-pretraining/, updated 2026-05-14; https://medium.com/data-science-collective/mid-training-the-vital-link-4e001f3337b4, Apr 2026):

- **CPT (continued / continual pre-training)** — the broad label. **DAPT (domain-adaptive pre-training)** — the older academic name, CPT aimed at a specific vertical. They mean the same thing.
- **Mid-training** — the framing frontier labs now prefer. Same machinery, but treated as a *deliberate, planned stage* between raw pre-training and post-training, where high-quality domain / code / math / long-context data is *blended in* while keeping enough general data to avoid forgetting. This re-framing — from "adapt the base after the fact" to "plan a domain phase into the pipeline" — is the single biggest conceptual shift since 2024 (sourced — same sources).

In a real production pipeline CPT comes *first* (absorb the domain), then instruction-tuning and preference alignment come *after* (shape behavior). CPT changes what the model *knows*; the later stages change what it *does*.

---

## 2. How it works

### The core loop is deceptively simple

Take the existing model's exact weights. Feed it your domain text. For every token it predicts the next one, you measure how wrong it was, and you nudge the weights to be slightly less wrong. Repeat over billions of tokens. That is the entire algorithm — identical to the original pre-training.

**The whole difficulty is that the model is already trained.** Resume training naively and two things break. Almost the entire field of CPT is about fixing them.

**Problem A — Catastrophic forgetting.** As you push the weights toward your domain, the model *abruptly* loses skills it already had. Train hard on medical text and it forgets how to write a Python function or do arithmetic. Gradient descent has no reason to protect "general competence" — it only cares about getting your new text right (sourced — https://arxiv.org/pdf/2403.08763).

**Problem B — The learning-rate cliff.** When the original training ended, the learning rate (how big each weight nudge is) had been annealed down to near zero — the model was carefully settled into a good spot. Resume at that floor and the model barely absorbs your domain. Resume at the original full rate and you blast it out of the good spot and wreck it.

### The mechanism that works — and one genuine controversy in it

The field converged on a small set of moves that, used together, reliably work. As of 2026 these are the defaults baked into the standard tooling. Treat the specific numbers below as **typical ranges from a handful of papers and practitioner blogs, not a measured universal standard** (inference — the ranges recur across sources but "converged community default" overstates the evidence).

**1. Use a much lower learning rate than the original.** Production practice is roughly **5–10× lower** than the original pre-training rate — about **5e-6 to 5e-5**. You are nudging, not rebuilding (sourced — https://futureagi.com/blog/continued-llm-pretraining/, 2026).

**2. Replay 5–20% general data into every batch.** This is the single most important defense against forgetting, and it is almost embarrassingly direct: while training on your domain text, mix in a slice of *general* web text (public corpora like FineWeb-Edu, RedPajama, Dolma). The model keeps practicing general skills while learning new ones, so it never fully overwrites them. The honest literature range is wider than a single number suggests — **1–5% can suffice to retain general knowledge; 10–30%+ is used for aggressive shifts and new-language adaptation** (sourced — https://arxiv.org/pdf/2403.08763; range qualification per verifier — "research consistently finds 5–10%" overstates convergence). *The intuition:* forgetting happens because the model has no incentive to keep old skills; replay manufactures the incentive, because old skills are tested every batch, so the gradients keep them alive.

**3. The learning-rate schedule — a known double-edged move, not settled consensus.** This is the one place where the popular recipe and the careful research findings genuinely tension, and you should know it. The widely-cited recipes (Ibrahim et al., 2403.08763; NVIDIA "Reuse, Don't Retrain," 2407.07263) describe **re-warming the learning rate back up — but only to about one-fifth to one-tenth of the original peak, never the full value — then cosine-decaying it down again**, and show this matches the quality of full retraining (sourced — https://arxiv.org/pdf/2403.08763; https://arxiv.org/pdf/2407.07263). **But the same body of work also flags that re-warming the LR *itself causes forgetting*** — the spike alone raises loss on the old distribution, *independent* of the new data (sourced — same papers, plus the dedicated re-warming study https://arxiv.org/abs/2308.04014, and "Beyond Cosine Decay: Infinite LR Schedules," https://arxiv.org/abs/2503.02844). So the modern picture is: re-warm-then-decay is a *recipe that works*, but the warmup is a hazard, and **WSD ("warmup-stable-decay") and "infinite" learning-rate schedules are increasingly preferred precisely to avoid the re-warming spike** while still allowing clean mid-run checkpointing. Anyone who presents re-warming as unambiguously good has not read the caveat (inference, grounded in the cited papers).

**4. Decontaminate and dedupe ferociously.** Before any training: strip near-duplicate documents (30–50% of raw corpora is duplicate junk) using n-gram overlap, embedding-cluster, and perplexity filters, and scrub anything that overlaps your evaluation benchmarks. Otherwise you "learn" the test and fool yourself — your reported gains are partly memorized test answers. This is integrity, not polish, and is now table-stakes prep (sourced — https://futureagi.com/blog/continued-llm-pretraining/, 2026).

### The 2025–2026 frontier — synthesizing training data for tiny corpora

A genuinely newer idea, and the reason CPT can now work even for *small* corpora. The problem: if your domain is a few hundred internal manuals, there is not enough text for next-token training to grip onto. A fact stated once, in one phrasing, barely moves the weights.

**Synthetic continued pre-training** — the **EntiGraph** method (ICLR 2025 oral) — fixes this. You hand a *capable* LLM (GPT-4, in the paper) your small seed corpus (~1.3M tokens) and have it (a) extract the salient entities, then (b) write fresh, diverse passages describing the *relationships between* those entities, effectively filling in the implicit knowledge graph behind your documents. The small seed becomes a large synthetic corpus (~455M tokens in their experiments), and *then* you do ordinary CPT on it. The honest payoff figure: the 455M-token synthetic corpus **recovers roughly 80% of the closed-book QA accuracy gain you would get from simply having the source documents available at inference** (sourced — https://arxiv.org/abs/2409.07431, ICLR 2025). So it substantially closes the gap — the knowledge becomes "parametric," usable without the documents in hand — but it does *not* fully match document-available performance, and if the documents *are* available at inference it compounds with retrieval rather than replacing it. *The intuition:* a fact you have seen once is fragile; the same fact restated fifty different ways becomes part of you.

### How you know it worked — the three-layer eval (now standard)

1. **Capability retention** — did it forget? (MMLU, HellaSwag, ARC). Target a drop of no more than ~1–2 points.
2. **Domain gain** — did it learn? (MedQA for medicine, FinQA for finance, LegalBench for law). Target a 5–10 point gain.
3. **Downstream usefulness** — does it help the real production pipeline (faithfulness, tool-use correctness, task completion)? You typically have to instruction-tune the checkpoint and test the actual task to see this.

Practitioners report that **most teams skip layer 3 and regret it** — they celebrate a benchmark bump and never check whether the product got better (sourced — https://futureagi.com/blog/continued-llm-pretraining/, 2026).

---

## 3. Why it works

### Why CPT works at all

A pre-trained model is not a database of facts; it is a compressed model of *how language and the world are structured*. That structure — grammar, reasoning patterns, world relationships — is general. A new domain is mostly the *same* structure with different vocabulary and a different fact distribution layered on top. So you do not rebuild the model; you only **shift** it, gently, toward the new distribution. CPT is cheap precisely because it reuses the expensive 99% (the structure) and pays only to adjust the last 1% (the domain skin). That is the whole economic argument — "Reuse, don't retrain" (sourced — https://arxiv.org/pdf/2407.07263).

### Why each naive alternative fails

**Train your domain model from scratch.** Fails on cost. Reproducing a base model means trillions of tokens and millions of dollars to re-learn grammar, arithmetic, and world knowledge you already had for free. You would pay full price to rebuild the 99% you did not need to touch.

**Just fine-tune (SFT) on domain Q&A.** Fails on *knowledge depth*. SFT teaches the model to *format* answers in your domain's style, but it sees too few tokens to absorb the domain's facts and vocabulary. It learns to *sound* like a doctor without *knowing* medicine. One paper that models the CPT/SFT trade-off explicitly reports an optimal split beating a code-specialist baseline by ~11.6% and lifting MedQA ~6.4% while cutting the token budget by up to 95% — but treat that as *one OpenReview submission's reported result*, not a general law (sourced, single-paper — https://openreview.net/forum?id=guUUlHPXRw).

**Resume at full learning rate, no replay.** Fails on *catastrophic forgetting*. You get a model fluent in your domain that can no longer add two numbers or write working code — net negative. This is exactly the failure the low-LR + replay (+ careful schedule) recipe exists to prevent.

**Just stuff documents into the prompt (RAG) and skip CPT.** This does not fail — it is often the *right* first move and far cheaper. But it has a ceiling: RAG gives the model facts to *read*, not facts it *understands*. The model never internalizes the domain's reasoning patterns or rare vocabulary, and it is limited by what retrieval surfaces per query. CPT and RAG are complements: CPT for deep, always-on domain fluency; RAG for fresh, specific, citable facts. The 2026 default for a serious vertical product is the **layered stack — CPT → SFT → preference-align (DPO) → RAG for recency**, not one instead of the others (inference, grounded in the synthetic-CPT and survey sources; layered-stack framing sourced — https://orq.ai/blog/finetuning-vs-rag, 2026; https://futureagi.com/blog/continued-llm-pretraining/, 2026).

---

## 4. People & resources

*Orders of magnitude, June 2026. Costs assume rented H100/H200 GPUs at roughly $2–4/GPU-hour (H100 cloud rents from ~$2.21/hr in 2026). Important caveat: the headline scale/cost table below comes from a single secondary source (FutureAGI) reproduced widely — treat every GPU/cost/wall-clock number as an order-of-magnitude estimate, not a measured fact (inference). Team-shape commentary is advisory.*

### Compute, time, money, data — by scale (sourced, order-of-magnitude — https://futureagi.com/blog/continued-llm-pretraining/, 2026)

| Scale | Domain tokens | GPUs | Wall-clock | Cost |
|---|---|---|---|---|
| **7B, LoRA** (parameter-efficient) | ~5B | 4–8 H100 | 1–3 days | hundreds to low thousands USD |
| **7B, full** weights | ~30B | 16–32 H100 | 3–10 days | low tens of thousands USD |
| **70B+, full** | 100B+ | 128–512 H100/H200 | 2–6 weeks | hundreds of thousands USD+ |

The span is enormous — three to four orders of magnitude in cost — and the lever is **LoRA vs. full training**. LoRA freezes the original weights and trains a small set of add-on parameters; it is far cheaper and forgets less, but caps how much new knowledge you can pack in. The standard 2026 playbook is **"LoRA first, graduate to full training only if results are insufficient."** In 2023–24 full CPT was the assumed path; in 2026 it is the exception you justify (sourced — https://futureagi.com/blog/continued-llm-pretraining/, 2026; https://www.spheron.network/blog/continuous-pretraining-llm-gpu-cloud-domain-adaptation/, 2026).

### The standard toolchain (2026) (sourced — same sources)

- **NVIDIA NeMo 2.0** — enterprise default; FP8, FSDP + tensor parallel, ships data-blending recipes, integrated with deployment.
- **Megatron-LM** — research-grade max throughput on H100/H200 clusters.
- **DeepSpeed (ZeRO-3)** — memory-efficient training on tighter budgets.
- **Axolotl** — config-driven, the de facto community-recipe layer for independent labs.
- **Unsloth** — 2–5× speedups on consumer/prosumer hardware via custom kernels.

PyTorch **FSDP2** sharding and **FP8** precision (mainstream since 2025) are what made the cost numbers above possible.

### Team size and roles (advisory)

CPT is one of the more *leverage-dense* activities in ML — a small team can do a lot, because the heavy lifting (the base model) is already done.

- **1–2 people for a LoRA-scale domain adaptation.** One ML engineer who owns the training run and the eval harness, with part-time data help. The tooling (Axolotl / Unsloth) has commoditized this into a genuinely small-team or solo-expert effort.
- **3–6 people for a serious full-weight 7B–70B program**, splitting into three skill clusters (a common, costly mistake is hiring one "LLM engineer" and assuming they cover all three):
  - **Data engineer(s)** — by far the highest-leverage role. Sourcing, dedup, decontamination, and especially building the domain↔general replay mixture. **Data quality and mixture decide success more than any training hyperparameter.** Budget the majority of human time here.
  - **Distributed-training / infra engineer** — owns the cluster, sharding, LR schedule, checkpointing, and restart-on-failure for multi-week runs. This is the scarce, expensive, gating role; if nobody has done multi-node H100 training you cannot fake it.
  - **Evaluation / domain owner** — builds and guards the three-layer eval, including the often-skipped downstream layer. The harness is engineering, but the *judgment* of "is this output actually right for our domain" must come from a real subject-matter expert, not the ML team.
- **10+ people** only when CPT is one stage of a larger foundation-model program (CPT → SFT → RLHF → serving), where serving, safety, and product integration add headcount.

### The single most important resource insight (advisory)

The scarce, expensive resource is **not GPUs — it is clean, well-mixed, decontaminated domain data.** Compute for CPT is cheap relative to base pre-training, and the tooling is mature. Projects that fail almost always fail on data: too small a corpus (reach for synthetic CPT / EntiGraph), a bad replay ratio (forgetting), or benchmark contamination (fooling yourself). If you have a fixed budget, spend it on data engineering and evaluation before bigger GPUs.

---

## 5. Scenarios & stories

The reality check up front (advisory): **for most teams, most of the time, CPT is the wrong tool** — not because it doesn't work, but because RAG fixes "the model doesn't know recent facts" at roughly 1% of the cost, and fine-tuning fixes "the model doesn't talk the way I want" far cheaper. CPT earns its keep in a narrow band. Here is where that band is.

### Where it is the RIGHT tool

**The Estonian government portal — language fluency the base never had.** A small EU member state wants a citizen assistant in fluent, idiomatic Estonian, a richly case-marked language the web barely covers. The cheap path — a frontier model with RAG over Estonian documents — retrieves the right facts but produces wooden, phrasebook Estonian. Fine-tuning on a few thousand examples sands the worst edges but cannot install fluency the base never had. CPT can: continue pre-training an open-weight model on a large Estonian web corpus, mixing in ~15% English to prevent forgetting, and the model's *instincts* for Estonian change. *Then* instruction-tune and add RAG. **The tell: the gap was the language itself, not the facts** — no amount of retrieval gives a model fluency it was never taught. This is the single clearest 2026 win for CPT (sourced — EstLLM, https://arxiv.org/pdf/2603.02041, 2026; Japanese/low-resource adaptation literature).

**The codebase that speaks its own dialect.** A fifteen-year-old internal platform with proprietary frameworks, in-house DSLs, and naming conventions found nowhere on GitHub. Even a strong frontier assistant hallucinates APIs and writes public-internet style, not house style. CPT on the monorepo — every merged pull request, every internal library — shifts those instincts; the model stops inventing plausible-but-fake functions because it has absorbed the *shape* of this codebase. **The tell: the structure and vocabulary are systematically under-represented in web data, and the corpus is large enough** (hundreds of millions of tokens, not three files) to move the model (advisory; corpus-size threshold matters — see the failure mode below).

**The "smaller model, served forever" economics play.** A company summarizes millions of specialized phone-call transcripts a day. The naive math — "just fine-tune a big off-the-shelf model, it's cheaper than pre-training" — ignores *inference* cost, which dominates over a deployed product's life. By baking the domain into pre-training, a **1B-parameter specialized model can outperform a 3B standard model** on domains far from web text, and once you have served roughly **1 trillion inference tokens, the smaller specialized model becomes cheaper to run** while matching or beating the bigger one. **The tell: enormous, sustained inference volume on a stable domain** (sourced — DatologyAI "the finetuner's fallacy," https://www.datologyai.com/blog/finetuners-fallacy, 2026).

**A better starting line for everything downstream.** A health-tech team's real goal is a clinical instruction-following assistant. They could fine-tune the base directly on labeled clinical tasks, but clinical text has its own grammar — drug names, ICD codes, the terse register of a discharge summary — the base handles shakily. So they first CPT on PubMed and de-identified clinical notes, *then* instruction-tune, and the final scores come out meaningfully higher than fine-tuning alone. **The tell: CPT here isn't the product — it's a force multiplier for the fine-tuning that follows**, justified only because the register is far from web English (advisory; the medical CPT-then-instruction-tune pattern is the documented 2026 standard).

### Where it is the WRONG tool

**BloombergGPT — the ~$10M cautionary tale.** In March 2023 Bloomberg trained a 50-billion-parameter model on 363 billion tokens, heavily weighted toward proprietary financial text — a ~$10M bet that domain pre-training would create a durable moat. By 2026 the retrospective verdict is blunt: **the strategy was largely invalidated.** When GPT-4 arrived it outperformed BloombergGPT on almost every public financial benchmark *with no access to Bloomberg's proprietary data*; on financial named-entity recognition BloombergGPT (60.82% F1) actually came in *behind* the general GPT-NeoX (60.98%) (sourced — https://beancount.io/bean-labs/research-logs/2026/05/05/bloomberggpt-large-language-model-finance, 2026-05-05; Yang et al., https://arxiv.org/abs/2305.05862; the "$10M / 363B tokens / 50B params" figures are correct, the "largely invalidated" verdict is a fair editorial characterization of the secondary sources, not a measured fact). Three lessons: **scale beats specialization when the frontier moves fast** (a frozen 2023 domain model was lapped by general models that simply got better — your hand-built moat is a depreciating asset); **CPT optimizes the wrong problem** here (brilliant at vocabulary and document recognition, useless at the arithmetic finance actually needed — delegate that to a tool); and **a bad tokenizer is a structural liability** no amount of domain text fixes. **The tell you're about to repeat it: your domain isn't actually under-represented on the web (finance is everywhere online), and your hard problem is reasoning or computation, not fluency.**

**The 12-megabyte corpus.** A team excited about CPT runs it on a niche corpus of a few million tokens. Result: too little signal to install new instincts, and enough off-distribution training to *degrade* general benchmarks by roughly 8–15 points if they skip replay (sourced as illustrative magnitude, blog-derived not a controlled study — https://futureagi.com/blog/continued-llm-pretraining/ and Spheron, 2026). The research is explicit: on **very small corpora (3–30M tokens), introducing domain data *late* via light continued pre-training beats baking it in** — and at that size you should usually skip CPT and reach for fine-tuning or RAG. **The tell: if your corpus fits in "a few thousand documents," you have a retrieval or fine-tuning problem, not a pre-training one.**

**"The model doesn't know about last week's launch."** Recency is a *retrieval* problem. RAG solves it at ~1% of the cost, updates instantly when facts change, and never risks forgetting. CPT to chase recency means retraining every time a fact changes — an absurd treadmill. **The tell: the gap is *facts that change*, not *language or structure that's stable.***

**"We want it to answer in our format and tone."** Format, schema, voice, and instruction-following are *fine-tuning's* job (input→output pairs, 1K–5M examples), not pre-training's. CPT teaches the model to *think* in your domain; it does not teach it to *behave* the way you want. **The tell: you can express what you want as example pairs.**

**The prototype that must ship this quarter.** CPT — even the cheap LoRA path — means days-to-weeks of GPU time, a serious data-prep pipeline, and a three-layer eval harness. For a prototype this is malpractice. **The tell: you haven't yet proven the product works with RAG plus a good prompt.** Always exhaust prompt-engineering and RAG first; they are hours, not weeks.

### The decision in one breath (advisory)

| The model's problem is… | Reach for | Not |
|---|---|---|
| Facts that change weekly | **RAG** | CPT |
| Output format / tone / instruction-following | **Fine-tuning** | CPT |
| It can't *speak* the language/code/register fluently, and you have ≥~300M tokens of it | **CPT** | RAG alone |
| You'll serve it billions of times and want a smaller, cheaper model | **CPT (specialized pretraining)** | a big fine-tuned model |
| The hard part is arithmetic / precise computation | **Tool use** | CPT |

---

## 6. Cross-industry usage & positioning (as of June 2026)

The mature view is **division of labor, not competition**: CPT/mid-training for vocabulary, syntax, and "thinking style" the base genuinely lacks; RAG for facts that change, are customer-specific, or must be cited; long context for reasoning over large document sets at inference (often itself enabled *by* CPT on long sequences). The default stack for a serious domain assistant is **CPT → instruction-tune → DPO/preference-align → RAG for recency** (sourced — https://futureagi.com/blog/continued-llm-pretraining/, 2026).

**Finance — table-stakes, but the strategy quietly inverted.** BloombergGPT (2023) minted the playbook and then aged badly (see Section 5). What finance does *now*: LoRA-based CPT on SEC filings, earnings transcripts, and news, paired with retrieval for any time-sensitive figure. The disciplined reference is **FINDAP / "Demystifying Domain-adaptive Post-training for Financial LLMs"** (Jan 2025), laying out CPT → instruction-tune → align; a vivid 2026 specialization is **MortgageLLM** (Nov 2025), DAPT plus "residual instruction transfer" for a single sub-vertical (sourced — https://arxiv.org/abs/2501.04961; https://arxiv.org/html/2511.21101v1).

**Healthcare & biomedicine — the canonical DAPT showcase**, because medical vocabulary genuinely diverges from web English. **Meditron-70B** is the reference open checkpoint: CPT on its GAP-Replay corpus (~48B tokens of PubMed articles/abstracts + internationally-recognized clinical *guidelines* + RedPajama replay) reaching ~70% MedQA — note it did **not** use MIMIC clinical notes (sourced, corrected per verifier — https://arxiv.org/pdf/2311.16079). **BioMistral** is built on PubMed Central (verify any specific MIMIC claim before repeating it). Important nuance: **Med-PaLM 2** reached 86.5% MedQA mostly through a strong base plus alignment, *not* heavy CPT — and that 86.5% is now a 2023-era figure; by 2026 successor open health models (the MedGemma line) report roughly **90–91% MedQA** (sourced/historical-flag — https://www.emergentmind.com/topics/med-palm-2). The lesson is even stronger now than when it was first made: at the frontier, raw base quality can substitute for heavy domain CPT. Cutting edge for 2026 is small-LM DAPT (7B-and-under posting double-digit MedQA gains).

**Legal — the cleanest "vocabulary truly diverges" case.** **SaulLM** is the flagship: SaulLM-7B → SaulLM-54B & SaulLM-141B (Mixtral-based, NeurIPS 2024) scaled CPT to **540B+ legal tokens**, then instruction-tuned and aligned, posting SOTA on LegalBench. Citation grammar, statute structure, and dense legal formality are exactly the "syntactic fluency" RAG can't inject (sourced — https://arxiv.org/abs/2407.19584). In practice, big legal-tech vendors lean on strong base models + heavy RAG over case-law databases rather than training their own (inference).

**Coding / dev tools — migrated *into* mid-training.** Code was the original CPT success (StarCoder2, DeepSeek-Coder via The Stack v2). In 2026 the action moved upstream: code is now 15–25% of frontier *pre-training* mixes, so much "code adaptation" is baked in at mid-training. The live frontier is **repository-level** pretraining (whole-repo context, ~64k windows) so the model reasons across files. A key mid-training finding: **timing beats mixture weights** — introduce specialized data *earlier* and you gain more in-domain while forgetting less (sourced — https://arxiv.org/pdf/2510.13697; https://openreview.net/forum?id=u7L9FOgG7t).

**Sovereign AI & regulated national industries — the fastest-growing CPT use case**, and arguably where it is most strategically vital, because a model that *thinks* in a specific language and legal/cultural context is something only weight-level adaptation delivers — RAG can't make a model fluent in Ukrainian or Italian regulatory prose. **Domyn (ex-iGenius) "Colosseum 355B"** — CPT on ~2.5T tokens over 3,000+ H100s on NVIDIA DGX Cloud for regulated finance and public administration, 50+ languages (Jan 2025); NVIDIA frames this as the reference architecture and states plainly that fine-tuning and RAG *cannot* achieve parameter-level knowledge integration. Also **Ukraine's Gemma-based national LLM** (beta spring 2026), **AMD Silo AI** (Poro/Viking, Finnish/Nordic/European), and **EstLLM** (sourced — https://developer.nvidia.com/blog/continued-pretraining-of-state-of-the-art-llms-for-sovereign-ai-and-regulated-industries-with-domyn-and-nvidia-dgx-cloud/, 2025-01-16; https://digitalstate.gov.ua/news/govtech/ukraine-moves-toward-a-sovereign-ai-model-national-llm-to-enter-beta-in-2026; https://arxiv.org/pdf/2603.02041).

**Customer support / telecom / enterprise back-office — low-glamour, high-volume.** **DACP** (Domain-Adaptive Continual Pre-Training for phone-conversation summarization, Oct 2025) is representative: CPT on call transcripts before task tuning. The pattern is CPT to internalize company/industry vocabulary, then RAG for anything customer-specific (sourced — https://arxiv.org/pdf/2510.05858).

**Defense — adopting via the sovereign/regulated channel** (data sovereignty, air-gapped deployment, classified vocabulary all favor weight-level adaptation over external retrieval). Concrete public models are thin; most evidence is the sovereign-AI overlap (inference).

**Science (proteins, genomics, chemistry) — a *different flavor* of DAPT** on non-text "languages." **ESM-DBP** domain-adapts a protein language model onto DNA-binding-protein sequences and beats the general model; genomic LMs apply the same logic to DNA; **EvoLlama** bridges protein encoders into LLMs. Any sequence with a "grammar" benefits (sourced — https://www.nature.com/articles/s41467-024-52293-7; https://arxiv.org/html/2412.11618v1).

**Robotics — the technique reborn as "pretrain on video, adapt to bodies."** Pretrain a **Vision-Language-Action** model on internet-scale unlabeled video (V-JEPA 2, GR00T N1, Physical Intelligence's π0) to learn world dynamics, then adapt with a few thousand robot demonstrations. **Cross-embodiment learning** (Open X-Embodiment: 22 robot bodies, 500+ tasks) is the 2026 unlock — one model across many bodies beats body-specific models (sourced — https://internet-pros.com/blog/vision-language-action-models-robotics-2026/; https://arxiv.org/html/2604.23001v1).

**The contrarian pressure (inference):** as frontier base models absorb more code/math/multilingual data at mid-training, the *marginal* value of separate downstream CPT keeps shrinking for any domain where the base is already decent (the BloombergGPT and Med-PaLM lessons). CPT remains clearly worth it where (a) vocabulary genuinely diverges from web text, (b) sovereignty/regulation forbids external retrieval, or (c) you need a language the base barely speaks. Elsewhere, cheaper LoRA-CPT + RAG usually wins.

---

## 7. Learning path for a technical leader

*You will sponsor, staff, and judge this work — not write the training loop. The goal is to reach for the cheap tool first, think in dials, and obsess over forgetting and clean evals.*

### Core mental models

- **MM1 — Gain vs. forgetting is the master tradeoff.** Data mix, learning rate, token count, and run length all trade domain *gain* against *catastrophic forgetting*. There is no "just make it better at X" — only "better at X, at some cost to Y, and here's where we set the dial."
- **MM2 — CPT is a *scaffold*, not a product.** The 2026 consensus: CPT yields a stronger *starting point*; you then instruction-tune on top, which converges faster and reaches higher quality. If someone proposes the CPT checkpoint itself as the deliverable, that's usually a misunderstanding.
- **MM3 — Match the tool to the *kind* of gap.** Volatile facts → **RAG** (~1% of CPT cost). Behavior/format → **SFT**. Domain vocabulary/reasoning the base structurally lacks → **CPT**. The leadership filter: **CPT is the right answer far less often than teams want it to be.**
- **MM4 — Replay is the cheapest insurance you can buy.** 5–20% general data per batch for vocabulary/style shifts, up to ~30–50% for aggressive or new-language shifts. Omitting replay to "save tokens" is the most common self-inflicted wound.
- **MM5 — Learning rate is a forgetting dial, and re-warming is dangerous.** Peak LR is much lower than base (~5e-6 to 5e-5). Counterintuitive but well-replicated: aggressively **re-warming the LR itself causes forgetting** — the spike alone raises old-distribution loss, independent of the new data. Modern recipes favor short/no warmup, a schedule consistent with how the base was trained, and increasingly **WSD / "infinite" schedules** for clean mid-run checkpointing.
- **MM6 — "Mid-training" is now a distinct, named thing.** *Pure CPT* = mostly domain data (max gain, max forgetting risk). *Mid-training* = a blended stage (~70–85% original-style + 15–30% domain) positioned before SFT. When a vendor says "we did continued pretraining," ask *which* — the risk profiles differ sharply.
- **MM7 — You can *predict* the tradeoff (scaling laws).** The **D-CPT Law** fits a formula over model size, token budget, and mixture ratio, letting teams *forecast* the gain/forgetting frontier and pick a ratio that holds general performance within tolerance, instead of running dozens of expensive sweeps. CPT-as-engineering, not CPT-as-alchemy.
- **MM8 — Decontamination is integrity, not a nicety.** If your corpus overlaps eval benchmarks, your "gains" are partly memorized test answers. n-gram dedup + benchmark decontamination *before* training is non-optional.

### Reading spine (in order)

1. **"Simple and Scalable Strategies to Continually Pre-train LLMs"** — Ibrahim et al., arXiv 2403.08763. *The* practitioner recipe (read it for both the re-warm+replay recipe *and* the caveat that re-warming causes forgetting).
2. **"Reuse, Don't Retrain"** — NVIDIA / Parmar et al., arXiv 2407.07263. Concrete mixing + LR guidance.
3. **"Continued LLM Pretraining in 2026"** — Future AGI blog. Best single current-state synthesis (frameworks, ranges, eval, costs, pitfalls).
4. **"D-CPT Law"** — arXiv 2406.01375. Read for the *idea*, skip the algebra.
5. **One domain case study close to yours** — e.g. DACP phone-summarization (arXiv 2510.05858).
6. **"Mid-training: The vital link"** — DS Collective, Apr 2026. Cements MM6.
7. *Optional:* **"Beyond Cosine Decay: Infinite LR Schedules"** — arXiv 2503.02844 (cements MM5).

*Framework names to recognize, not study:* NeMo 2.0, Megatron-LM, DeepSpeed/ZeRO-3, Axolotl, Unsloth; sharding via PyTorch FSDP2.

### Understanding checkpoints — you understand it when you can…

- …name the right tool (RAG/SFT/CPT) for a request and defend it in one sentence by the *gap type*. (The single most valuable skill.)
- …explain replay to a skeptic who wants to drop general data, with a concrete ratio.
- …describe the re-warming trap from memory.
- …classify a proposal in front of you as "pure CPT" vs. "mid-training."
- …read a three-layer results table and spot "domain up, MMLU down 6" (forgetting) or "everything suspiciously up" (decontamination failure).
- …size the bet — order-of-magnitude tokens/GPUs/time/dollars for a 7B LoRA run vs. a full 70B run, and why you start cheap.
- …name what would make you *kill* the project (gap is volatile facts → RAG; LoRA already closed it → full CPT is wasted).

### How to evaluate an expert in an interview

- **"How do you decide if CPT is even the right tool?"** *Strong:* asks what *kind* of gap (volatile facts vs. behavior vs. structural vocabulary), pushes back that most cases are RAG/SFT, tries LoRA/RAG first. *Red flag:* can't separate CPT from fine-tuning; thinks CPT makes a model follow instructions.
- **"Domain benchmarks rose 8 pts but MMLU dropped 5 — what happened?"** *Strong:* names **catastrophic forgetting** instantly; diagnoses (too little replay, LR too hot, too many epochs, harmful re-warming) and fixes via dials. *Red flag:* calls it a success.
- **"How do you set learning rate and schedule?"** *Strong:* much lower than base (~5e-6–5e-5) because near the optimum; knows the **re-warming hazard**; keeps schedule consistent with base or uses WSD/infinite. *Red flag:* wants to re-warm hot "so it learns faster" — a tell they haven't run a real one.
- **"Your data pipeline before a single training step?"** *Strong:* dedup → **decontamination against eval benchmarks** → quality filtering → mixture design, treating decontamination as integrity. *Red flag:* no decontamination and proud of high gains.
- **"How do you plan mixture ratio without burning the budget?"** *Strong:* scaling-law / predictive methods (D-CPT Law) from small runs, explicit tolerance. *Red flag:* picks by vibes, runs the full budget once.
- **"How do you know it worked?"** *Strong:* three layers — retention (≤1–2 pt drop), domain gain, **downstream usefulness** (instruction-tune the checkpoint, test the real task); calls skipping layer 3 the classic mistake. *Red flag:* only training loss, or domain metric with no retention check.

**Green flags overall:** volunteers *when CPT is wrong*; thinks in dials; has a real forgetting-recovery story; reaches for RAG/LoRA before full CPT; treats eval and decontamination as first-class.

---

## 8. Team notes

### The one-paragraph reality check (advisory)

For the overwhelming majority of teams, **CPT is the wrong first move and you do not need to hire for it.** The 2026 playbook is RAG first, then instruction/preference tuning, and CPT only if those demonstrably fail to absorb domain *fluency* (terminology, jargon, structure, a low-resource language). CPT is the most expensive, most fragile, and least-reused of the adaptation tools. Treat "we need continued pre-training" the way you'd treat "we need to build our own database engine" — occasionally true, usually a smell. The roles below matter only *after* you've ruled out RAG and fine-tuning.

### Roles & seniority (advisory)

**Default: no new headcount.** A strong applied-ML or LLM-platform person plus rented compute absorbs the occasional run. A dedicated team is justified only when CPT is a *recurring* product input (you ship a domain model line, serve a regulated vertical, or own a non-English market with no good base model). When it is justified, the work splits into three clusters — and a common mistake is hiring one "LLM engineer" and assuming they cover all three:

| Cluster | What they do | Seniority | Can an existing role absorb it? |
|---|---|---|---|
| **Distributed-training engineer** | Multi-node training, sharding (FSDP2 / ZeRO-3 / Megatron), throughput, FP8, checkpointing, debugging silent NCCL / loss-spike failures | Senior / Staff — the scarce, expensive one | Rarely. If nobody has done multi-node H100 training, you cannot fake it. |
| **Data engineer (corpus)** | Sourcing, dedup, decontamination, perplexity/embedding filtering, replay-mix blending, licensing hygiene | Mid–Senior with ML literacy | Often. A good data engineer + an ML reviewer covers it. |
| **Evaluation / domain owner** | Three-layer eval harness + owns domain ground truth | Mid–Senior, **must include a real domain expert** | Partly. The harness is engineering; the *judgment* of "is this output actually right" must come from a subject-matter expert. |

**The distributed-training person is the gate.** Everything else can be grown or rented. One Staff engineer who has genuinely shipped a multi-node CPT run is worth more than three generalists who've only done single-GPU LoRA.

### Hiring signals (advisory)

**Green flags:** has personally debugged a *failed* large run (loss spikes, divergence, a corrupted checkpoint, a dead node at hour 40) and tells the story concretely; talks unprompted about **catastrophic forgetting** and names mitigations (replay 5–20%, conservative LRs, PEFT to freeze base weights); names the real toolchain with opinions about single-node vs. cluster; **starts with "do we even need this?"**; treats evaluation as the product and insists on a downstream-task metric.

**Red flags:** reaches for full CPT immediately and can't say when *not* to; lists "pretraining" but has only ever run single-GPU LoRA notebooks; **no story about a run that broke** (big-model training is mostly failure recovery); quotes only benchmark gains with no concept of downstream eval; hand-waves catastrophic forgetting; wants to own a GPU cluster on day one for an unsized workload; conflates CPT with fine-tuning or RAG in conversation.

### Build vs. buy (default: rent) (advisory)

**Rent the compute, almost always.** CPT is bursty — you run it occasionally, then idle. Owning H100/H200 clusters only pays back at *continuous* utilization of roughly 64+ GPUs; below that, cloud is cheaper and you skip staffing and depreciation. **Buy/borrow the base model and frameworks** — NeMo 2.0, Megatron-LM, DeepSpeed, Axolotl, Unsloth, TRL exist and are good; owning the framework is not a moat. **Owning the *adapted weights and the domain corpus* is.** Cost anchors (sourced, order-of-magnitude): see the Section 4 table; H100 cloud from ~$2.21/hr in 2026; specialist GPU-cluster contractors ~$1,400–1,800/day.

**When owning it IS a real moat (advisory):** you hold a *proprietary, large, hard-to-replicate corpus* (e.g., decades of internal documents nobody else has), AND domain *fluency* — not just facts — is your differentiator, AND RAG/fine-tuning have measurably failed. Facts alone are not a moat (that's RAG). A non-English or low-resource language with no decent base model is the clearest legitimate case. Absent that, rent everything and don't build a team.

### Common failure modes

1. **Doing CPT when RAG would've worked** — the most expensive failure. Most "we need CPT" requests are retrieval problems.
2. **Catastrophic forgetting** — LR too high or replay skipped; the model gains the domain and loses general capability. 2026 tooling narrows this, but only if your engineer knows to use it.
3. **Skipping downstream evaluation** — the single most common mistake. A MedQA/FinQA/LegalBench bump is not the product; measure task completion, faithfulness, tool use.
4. **Garbage corpus** — no dedup, no decontamination → training on duplicates and test leakage → inflated, fake gains.
5. **One generalist hire** — expecting one person to cover distributed training *and* corpus engineering *and* domain evaluation. The domain-judgment piece in particular can't be done by the ML team alone.
6. **Owning hardware too early** — a cluster bought for a bursty workload sits idle between runs. Size on rented compute first.
7. **Treating CPT as the finish line** — it produces a better starting point, not a shippable assistant; it still needs instruction tuning + alignment + (usually) RAG.

### Bottom line (advisory)

Don't hire for this by default — rule out RAG, then fine-tuning, first. If you do need it, the gating hire is one Staff-level distributed-training engineer with a real failed-run story, paired with a data engineer and a domain expert who owns evaluation. Rent compute and frameworks; own only the corpus and resulting weights, and only when fluency, not facts, is the moat. **The failure that kills you isn't technical, it's strategic: spending six figures and weeks to solve a retrieval problem. Make someone defend "why not RAG?" before any budget is approved.**

---

## Sources

- Gupta/Ibrahim et al., *Simple and Scalable Strategies to Continually Pre-train LLMs* (re-warming + replay recipe, and the re-warming-causes-forgetting caveat) — https://arxiv.org/pdf/2403.08763
- Parmar et al. (NVIDIA), *Reuse, Don't Retrain: A Recipe for Continued Pretraining* — https://arxiv.org/pdf/2407.07263
- *On the re-warming hazard / continual pre-training under distribution shift* — https://arxiv.org/abs/2308.04014
- *Beyond Cosine Decay: Infinite / WSD LR Schedules* — https://arxiv.org/abs/2503.02844
- Yang et al., *Synthetic Continued Pretraining* (EntiGraph, ~80% recovery, GPT-4 generator), ICLR 2025 Oral — https://arxiv.org/abs/2409.07431
- *Continued LLM Pretraining in 2026: Frameworks, Strategies, Evaluation* — Future AGI (updated 2026-05-14) — https://futureagi.com/blog/continued-llm-pretraining/
- *Continuous Pretraining on GPU Cloud: Domain Adaptation Without Catastrophic Forgetting* (2026) — https://www.spheron.network/blog/continuous-pretraining-llm-gpu-cloud-domain-adaptation/
- DatologyAI, *The Finetuner's Fallacy: When to Pretrain with Your Finetuning Data* (2026) — https://www.datologyai.com/blog/finetuners-fallacy
- *BloombergGPT and the Limits of Domain-Specific LLMs in Finance* — Beancount.io (2026-05-05) — https://beancount.io/bean-labs/research-logs/2026/05/05/bloomberggpt-large-language-model-finance
- Yang et al., *BloombergGPT* — https://arxiv.org/abs/2305.05862
- *Modelling Optimal Trade-Off Between Continued Pre-Training and SFT* (single-paper result) — https://openreview.net/forum?id=guUUlHPXRw
- *D-CPT Law* — https://arxiv.org/abs/2406.01375
- *Mid-training: The vital link* — DS Collective (Apr 2026) — https://medium.com/data-science-collective/mid-training-the-vital-link-4e001f3337b4
- *Midtraining Bridges Pretraining and Posttraining Distributions* — https://openreview.net/forum?id=u7L9FOgG7t
- FINDAP, *Demystifying Domain-adaptive Post-training for Financial LLMs* (Jan 2025) — https://arxiv.org/abs/2501.04961
- *MortgageLLM: DAPT with Residual Instruction Transfer* (Nov 2025) — https://arxiv.org/html/2511.21101v1
- *SaulLM-54B & SaulLM-141B* (NeurIPS 2024) — https://arxiv.org/abs/2407.19584
- *MEDITRON-70B* (GAP-Replay: PubMed + clinical guidelines + RedPajama, no MIMIC) — https://arxiv.org/pdf/2311.16079
- *Med-PaLM 2 overview* (86.5% MedQA, now historical; 2026 successors ~90–91%) — https://www.emergentmind.com/topics/med-palm-2
- *On Pretraining for Project-Level Code Completion* — https://arxiv.org/pdf/2510.13697
- *Continued Pretraining for Sovereign AI (Domyn Colosseum 355B)* — NVIDIA (2025-01-16) — https://developer.nvidia.com/blog/continued-pretraining-of-state-of-the-art-llms-for-sovereign-ai-and-regulated-industries-with-domyn-and-nvidia-dgx-cloud/
- *EstLLM: Enhancing Estonian Capabilities via Continued Pretraining* (2026) — https://arxiv.org/pdf/2603.02041
- *Ukraine Moves Toward a Sovereign AI Model* — https://digitalstate.gov.ua/news/govtech/ukraine-moves-toward-a-sovereign-ai-model-national-llm-to-enter-beta-in-2026
- *DACP: Domain-Adaptive Continual Pre-Training for Phone Conversation Summarization* — https://arxiv.org/pdf/2510.05858
- *Domain-Adaptive Continued Pre-Training of Small Language Models* — https://arxiv.org/abs/2504.09687
- *Improving protein LM by domain-adaptive pretraining (ESM-DBP)* — https://www.nature.com/articles/s41467-024-52293-7
- *EvoLlama: Enhancing LLMs' Understanding of Proteins* — https://arxiv.org/html/2412.11618v1
- *Vision-Language-Action Models 2026* — https://internet-pros.com/blog/vision-language-action-models-robotics-2026/
- *Fine-Tuning vs RAG (2026 Guide)* — https://orq.ai/blog/finetuning-vs-rag
- Wang et al., *Continual Learning of LLMs: A Comprehensive Survey* (CSUR 2025) — https://github.com/Wang-ML-Lab/llm-continual-learning-survey
