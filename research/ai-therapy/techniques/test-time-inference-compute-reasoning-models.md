# Test-Time / Inference-Time Compute & Reasoning Models

*State of the art as of June 2026. Factual claims are labeled sourced (with link + date), inference, or speculation. Learning-design and org recommendations are labeled advisory — my reasoned synthesis, not sourced fact.*

---

## 1. What it is

For roughly the first six years of large language models — the transformer era from about 2018 to the o1 inflection in late 2024 — there was essentially one knob that mattered: **make the model bigger and train it on more data.** A model read your prompt and produced an answer in essentially one forward pass — it "blurted." It spent the same trivial amount of computation whether you asked "what's 2+2" or "prove this theorem." *(inference)*

**Test-time compute** (also called inference-time compute) is the second knob. The idea: instead of only making the model smarter *during training*, let it **spend more computation while answering** — let it think longer, try multiple approaches, check its own work, and only then commit. A **reasoning model** is a model specifically trained to use that extra thinking time well.

Concretely, a reasoning model generates a long internal monologue — a "chain of thought" — before it writes the final answer. It might write 5,000 or 50,000 tokens of working-out that you may never see, then produce a three-sentence answer. The deliberation lives in different places depending on the vendor:

- **Hidden tokens** whose content you never see (historically OpenAI's o-series, o1/o3/o4-mini)
- **A separately-budgeted, inspectable "thinking" block** (Claude's extended / adaptive thinking)
- **A transparent inline chain** you watch stream (DeepSeek R1)
- **Parallel exploration of several hypotheses at once** (Gemini Deep Think)

The shared property: the model spends *meaningful, variable compute on the problem before answering.* ([meta-intelligence.tech, 2026](https://www.meta-intelligence.tech/en/insight-reasoning-models); [introl.com, Dec 2025](https://introl.com/blog/inference-time-scaling-research-reasoning-models-december-2025))

This is now the dominant frontier paradigm. The lineage: OpenAI's **o1** (late 2024) first showed it worked at scale; **DeepSeek-R1** (early 2025) showed it could be reproduced openly and cheaply; by mid-2026 every frontier lab ships a reasoning mode. ([labellerr.com, 2026](https://www.labellerr.com/blog/compare-reasoning-models/))

**One important framing update for June 2026:** the "separate reasoning SKU" is largely gone. OpenAI folded its o-series into **GPT-5.5**, where you set a *reasoning effort* level (none → low → medium → high → xhigh) rather than switching models; o3 itself was scheduled for retirement (announced May 28 2026, sunset Aug 26 2026). Anthropic ships extended/adaptive thinking on **Claude Opus 4.8** (released May 28 2026; ~88.6% SWE-bench Verified), and Google ships **Gemini 3.x** thinking budgets. On the open-weight side, **DeepSeek R1** persists and **Qwen3 / Qwen3.x** replaced the older QwQ with a unified hybrid thinking/non-thinking mode rather than a dedicated reasoning model. ([lmcouncil.ai, June 2026](https://lmcouncil.ai/benchmarks); o3/o4-mini are historical lineage, not the live OpenAI offering.) The 2026 mental model is a **throttle, not a product.**

---

## 2. How it works — the gears turning

There are two distinct mechanisms, and the confusion between them is worth clearing up first. One is about **training** the model to think; the other is about **spending compute at answer time.** Modern reasoning models use both.

### Gear A — Teaching the model to think: RLVR

The breakthrough that made o1/R1 possible is **Reinforcement Learning from Verifiable Rewards (RLVR).** The machine:

1. **Take a hard problem with a checkable answer** — a math problem, a coding task, a logic puzzle. The key word is *checkable*: you can mechanically verify whether the final answer is right (run the code, check the number) without a human grading it. ([aws.amazon.com, 2026](https://aws.amazon.com/blogs/machine-learning/overcoming-reward-signal-challenges-verifiable-rewards-based-reinforcement-learning-with-grpo-on-sagemaker-ai/))
2. **Let the model attempt it many times**, each time writing out a long chain of reasoning before answering — a "group" of, say, 8–64 rollouts on the same question.
3. **Grade each attempt** with a simple rule: did the final answer match ground truth? Correct → positive reward. Wrong → negative. No human in the loop, no learned "taste" model — just a verifier. ([emergentmind.com, 2026](https://www.emergentmind.com/topics/deepseek-r1-zero))
4. **Push the model toward the reasoning patterns that led to correct answers** and away from the ones that didn't. Crucially, you reward the *outcome*, not a specific "gold" path — so the model is free to discover its own routes rather than imitating one human-written solution. ([aws.amazon.com, 2026](https://aws.amazon.com/blogs/machine-learning/overcoming-reward-signal-challenges-verifiable-rewards-based-reinforcement-learning-with-grpo-on-sagemaker-ai/))

**The specific algorithm everyone uses is GRPO (Group Relative Policy Optimization).** Ordinary RL (PPO) needs a second neural network — a "critic" / value model — to estimate how good a situation is and judge whether each attempt beat expectations. That critic is expensive and unstable. GRPO throws it out: it generates a *group* of answers to the same question and judges each one **relative to the group average.** An attempt scoring above the batch mean gets reinforced; one below gets suppressed. The group *is* the baseline. (Mechanically: PPO carries policy + reference + value networks; GRPO carries just policy + a frozen reference.) Removing a whole network is why GRPO is cheaper and more stable — and why a small lab could pull it off. ([aws.amazon.com, 2026](https://aws.amazon.com/blogs/machine-learning/overcoming-reward-signal-challenges-verifiable-rewards-based-reinforcement-learning-with-grpo-on-sagemaker-ai/))

**The emergent "aha" effect.** When DeepSeek ran this loop with *no* supervised examples of reasoning at all (R1-Zero), the model **spontaneously learned to write longer and longer chains of thought** for harder problems, to **back up and re-check** when an approach looked doomed, and to **catch its own errors** — none of it explicitly taught. The chains grew from hundreds to thousands of tokens purely because longer, self-correcting reasoning got rewarded more often. ([huggingface.co, 2025](https://huggingface.co/blog/NormalUhr/deepseek-r1-explained); [emergentmind.com, 2026](https://www.emergentmind.com/topics/deepseek-r1-zero))

> **Contested:** Some researchers argue the famous "aha moment" is overstated — that growing response length is just RL exploiting a well-shaped reward function, not genuine emergent self-reflection. The behavior is real; its interpretation is debated. ([sail.sea.com, 2025](https://sail.sea.com/blog/articles/62); [arxiv 2503.20783](https://arxiv.org/pdf/2503.20783))

### Gear B — Spending compute at answer time

Once a model can think, you can buy more accuracy at inference by spending more compute. The menu, roughly weakest-to-strongest:

- **Longer chain-of-thought** — let the single train of thought run longer. This is the baseline mechanism inside GPT-5.5 / Gemini / Claude reasoning modes.
- **Best-of-N / self-consistency** — generate many independent answers, then **majority-vote** (for math) or pick the best via a scorer. Diverse independent tries beat one try because their errors are uncorrelated.
- **Search (Tree-of-Thoughts, beam search, Monte-Carlo Tree Search)** — treat reasoning as a branching tree, explore multiple partial paths, prune the bad branches.
- **Verifiers / reward models** — a separate model scores reasoning. **Process reward models (PRMs)** grade *each step*, not just the final answer, so you can kill a bad line of thought early. Step-wise verifiers generally outperform answer-only verifiers and steer the search/pruning above. ([arxiv 2504.09037](https://arxiv.org/pdf/2504.09037))

A fourth, emerging axis: **latent / continuous reasoning** — "think" in vector space instead of emitting tokens. Cheaper and lower-latency, it's being pushed hardest by robotics and anyone latency-bound. ([arxiv 2602.07845](https://arxiv.org/abs/2602.07845))

### The 2026 refinement: *adaptive* thinking

The naive version overthinks — a deliberation-trained model burns 2,000 tokens on "2+3=?". The frontier work in 2026 is **adaptive / controllable test-time compute**: the model (or a controller) estimates how hard a question is and **allocates a thinking budget to match** — short for easy, long for hard. Reported systems (AdaCtrl, AdapThink, ARES, budget-aware curricula) cut response length substantially on easy items while preserving or improving accuracy on hard ones. ARES, for instance, cut reasoning cost ~53% on agent benchmarks like TAU-Bench while holding or improving accuracy. ([arxiv 2603.07915](https://arxiv.org/abs/2603.07915); [meta-intelligence.tech, 2026](https://www.meta-intelligence.tech/en/insight-reasoning-models)) This is why Claude markets "adaptive thinking" and GPT-5.5 exposes adjustable effort levels.

---

## 3. Why it works — the principle, and why the naive alternative fails

**The underlying principle: some problems require *sequential* computation that no single forward pass can fake.**

A standard LLM answering in one pass has a fixed "depth" — a fixed number of layers, applied once. That's like being forced to answer every question in the time it takes to say it out loud. For pattern-recall ("capital of France"), that's plenty. But for a problem that genuinely requires *steps* — try an approach, notice it fails, backtrack, try another — a single pass physically cannot represent the backtracking. The computation needed is **longer than the architecture's one-shot depth allows.**

Chain-of-thought breaks this ceiling with an almost embarrassingly simple trick: **the model writes its intermediate work into its own context, then reads it back.** Each token it generates becomes input it can condition on. The output stream becomes a scratchpad — an external working memory — that lets a fixed-depth network perform *arbitrarily long* sequential computation. Thinking longer literally buys more computational steps. That's the whole secret.

**Why the naive alternative — "just train a bigger model" — fails (or fails economically):**

- **Training scaling is hitting brutal economics.** Each increment of capability from pretraining costs exponentially more data and compute, and the highest-quality human text is largely exhausted. Inference-time scaling offers a *different axis*: the same base model gets dramatically better at reasoning by thinking longer. ([introl.com, Dec 2025](https://introl.com/blog/inference-time-scaling-research-reasoning-models-december-2025))
- **A bigger model still answers in one pass.** Scale improves what the model *knows* and its one-shot pattern-matching, but doesn't grant the *sequential backtracking* hard problems need. The dramatic jumps land on exactly the problems where steps matter — competition math, ARC-AGI, hard code. On **ARC-AGI-1**, o3 leapt to roughly **75.7% (low/standard compute) up to ~88% (high compute)** on the public eval, where prior non-reasoning models were near single digits (GPT-4o ~5%); this fluid-reasoning capability is widely credited specifically to test-time reasoning, not raw scale. ([arcprize.org, Dec 2024](https://arcprize.org/blog/oai-o3-pub-breakthrough)) *(Note: the often-cited ~96.7% is o3's AIME 2024 score, a different benchmark — not ARC-AGI-1.)*
- **Verifiable rewards dodge the reward-hacking trap.** Earlier alignment used a *learned* human-preference reward model, which models learn to game (confident-sounding nonsense the grader likes). RLVR rewards only *ground-truth correctness* on checkable problems — far harder to fake — which is why it produces real reasoning gains rather than sycophancy. ([aws.amazon.com, 2026](https://aws.amazon.com/blogs/machine-learning/overcoming-reward-signal-challenges-verifiable-rewards-based-reinforcement-learning-with-grpo-on-sagemaker-ai/))

**Where it breaks down (the honest limits, June 2026):**

- **Overthinking is real and costly** — without adaptive budgets, models waste compute and can *talk themselves out of* correct answers. ([arxiv 2412.21187](https://arxiv.org/pdf/2412.21187))
- **Reasoning models hallucinate *more*, not less.** Every reasoning model tested in 2026 exceeded a **10% hallucination rate** on Vectara's harder benchmark, versus ~3.3% for the best non-reasoning model (and R1 ~71.7% benign-hallucination vs V3 ~36.8% on the related set). Longer chains create more room to confidently invent. ([labellerr.com, 2026](https://www.labellerr.com/blog/compare-reasoning-models/))
- **RLVR only works where answers are checkable.** Math, code, formal logic — yes. Open-ended writing, strategy, taste — much weaker, because there's no clean verifier.
- **It only fixes the *generalization* gap so far.** On **ARC-AGI-2** — explicitly designed to resist memorization and measured *under cost budgets* — top scores climbed through early 2026 to roughly **77.1% (Gemini 3.1 Pro), ~73.3% (GPT-5.4), ~68.8% (Claude Opus 4.6)**, with GPT-5.5 reported higher still. *Important nuance:* many scores above ~50% rely on **refinement/orchestration scaffolds** (e.g. Poetiq on Gemini 3 Pro reached ~54% at ~$31/task) — these are *system* scores, not raw single-model scores. The "powerful but not yet general intelligence" conclusion still holds; the once-quoted "mid-50s%" figure is now stale. ([agentmarketcap.ai, Apr 2026](https://agentmarketcap.ai/blog/2026/04/06/arc-agi-2-leaderboard-2026-gemini-gpt5-claude-reasoning-benchmark))

---

## 4. People & resources (orders of magnitude, with basis)

The headline of this paradigm: **the cost moved from training to inference**, and **the reasoning layer itself is cheap to add** on top of an existing base model.

### Building a reasoning model

The eye-opening data point is DeepSeek-R1, the one fully-disclosed frontier-class case:

| Stage | Compute | Cost (basis) |
|---|---|---|
| **Base model (V3)** — the expensive part | ~2,048 H800 GPUs × ~2 months ≈ **2.79M GPU-hours** | **~$5.6M** ([theregister.com, Sep 2025](https://www.theregister.com/2025/09/19/deepseek_cost_train/)) |
| **RL reasoning stage (R1)** — adding reasoning | **~147K H800 GPU-hours**, 512 H800s | **~$294K** ([cnn.com, Sep 2025](https://www.cnn.com/2025/09/19/business/deepseek-ai-training-cost-china-intl)) |

**The load-bearing insight:** the reasoning RL stage cost roughly **5% of the base model's training** and ~1/20th the absolute dollars. *(The widely-circulated "$294K to train R1" headline conflated the two — that figure is the RL stage only, sitting on top of a multi-million-dollar base. ([theregister.com, Sep 2025](https://www.theregister.com/2025/09/19/deepseek_cost_train/)))*

- **Team size (inference, from disclosed cases):** a frontier reasoning *post-training* effort is a **small team — order 10–30 researchers/engineers** — *provided a strong base model already exists.* The hard, capital-intensive work is the base model and the data/RL infrastructure; the reasoning recipe (RLVR + GRPO) is now well-understood and reproducible. Roles cluster into: RL/training-infra engineers, verifier/reward-environment builders (math/code graders, sandboxes), data curators of hard verifiable problems, and eval engineers.
- **Data scale (inference):** the differentiator is **not raw volume but quality of verifiable problems** — order **10⁴–10⁶ hard, checkable problems** with ground-truth answers (competition math, unit-tested code, logic). Synthetic-data work in 2026 (e.g. CHIMERA) pushes toward compact, high-yield reasoning datasets rather than scraping more web text.

### Running a reasoning model (the cost that actually dominates now)

This is where the economics inverted. Because reasoning burns *output* tokens — and hidden thinking tokens are billed at the output rate — a single query can cost 10–100× a normal one. Current API pricing (per million tokens): ([meta-intelligence.tech, 2026](https://www.meta-intelligence.tech/en/insight-reasoning-models); [tldl.io, 2026](https://www.tldl.io/resources/llm-api-pricing-2026))

| Model | Input | Output | Note |
|---|---|---|---|
| **DeepSeek R1** | $0.55 | $2.19 | open-weights, cheapest frontier-ish |
| **Gemini 3 Pro** | $1.25 | $5.00 | 2M-token context |
| **OpenAI o3 (lineage)** | $10.00 | $40.00 | o3-Pro reasoning ~$150/M |
| **Gemini Deep Think** | — | — | gated to $250/mo Ultra plan |

A single reasoning call can burn **50K output tokens** of hidden thinking before a one-paragraph answer — so the deliberation, not the answer, is the bill. ([tldl.io, 2026](https://www.tldl.io/resources/llm-api-pricing-2026))

**Industry-level money/compute (orders of magnitude):**

- **Inference now dwarfs training.** A widely-cited single-vendor figure projects inference demand to **exceed training demand by ~118× by 2026** — *contested and single-sourced* (traces to one vendor blog, [introl.com, Dec 2025](https://introl.com/blog/inference-time-scaling-research-reasoning-models-december-2025); treat the exact multiple skeptically). The direction is corroborated: **GPT-4-specific cumulative inference** (launch Mar 2023 through end-2024) was reported by Barclays at **~$2.3B — about 15× GPT-4's ~$150M training cost.** *(Note: that $2.3B is GPT-4-specific and cumulative, not OpenAI's total 2024 inference spend, which was billions more.)* As reasoning becomes default, the gap widens. ([introl.com, Dec 2025](https://introl.com/blog/inference-time-scaling-research-reasoning-models-december-2025))

### What this means if you're deciding *(advisory)*

- **Don't reflexively reach for the strongest reasoner.** o3-class quality costs ~18× DeepSeek R1 for the same job. The mainstream 2026 pattern is a **router**: a cheap classifier sends easy queries to a fast non-reasoning model and only hard ones to a reasoner — reportedly cutting API cost 60–80% while holding quality. Build the router before you build the bill.
- **Budget for the *thinking*, not the answer.** Your cost model must price hidden reasoning tokens. A "short answer" is not a cheap call.
- **Use reasoning where answers are verifiable; distrust them where they're not.** They shine on math/code/logic and *hallucinate more* on open-ended factual claims. Pair them with retrieval or verification for anything fact-sensitive.
- **A capable open reasoning model is within reach of a small team** *if* you already have (or can rent) a strong base model — the RLVR+GRPO recipe is public and the RL stage is cheap. The moat is the base model and the verifier infrastructure, not the reasoning trick itself.

---

## 5. Scenarios & stories

*The dial you control is not "how smart is the model" but "how hard should it think on this question." As of mid-2026 every major lab ships this as a knob: GPT-5.5 exposes five effort levels (none/low/medium/high/xhigh — verified against OpenAI's docs); Claude has adaptive thinking with effort controls; Gemini 3 has thinking budgets. The whole game is matching effort to problem.*

### Where it shines

**1. The contract clause that hides a landmine.** A procurement analyst feeds a 40-page master services agreement to the model: "Does the limitation-of-liability cap survive the indemnification carve-out in Section 12, given the definition of 'Losses' in the preamble?" This isn't retrieval — the answer lives in the *interaction* of three clauses, one of which redefines a word everyone assumes they understand. A non-reasoning model pattern-matches "liability cap = capped" and says yes. A high-effort reasoning model traces the chain: preamble redefines "Losses" to include consequential damages → the carve-out references "Losses" → therefore the cap does *not* apply to indemnified claims. It shows its work, the analyst checks each link, and a real exposure surfaces before signing. **The sweet spot: one hard question where a wrong answer dwarfs a few cents of thinking, and the reasoning trace is itself auditable evidence.**

**2. The flaky test no one can reproduce.** A test fails one run in twenty, only in CI. Debugging is search: hypothesize ("shared mutable state across parallel test workers?"), check against evidence ("the fixture uses a module-level dict, and CI runs with `-n 4`"), reject dead ends, converge. With extended thinking the model considers the timing-dependent ordering a human stares past for an hour. **Multi-step problems where the path isn't knowable in advance are exactly what the extra compute buys.** Production coding agents lean on this via a *router* that escalates to high-effort reasoning only on the hard sub-steps.

**3. The math/quant problem with a checkable answer.** A closed-form approximation, or a competition problem (AIME, GPQA, hard combinatorics). The canonical home turf — the problems genuinely require multi-step derivation *and* answers are verifiable, so the model's habit of generating many lines and converging pays off cleanly. DeepSeek-R1 proved the whole thesis here by generating 10–100× more tokens per query to match frontier closed models.

**4. The agent that plans, acts, then recovers.** "Rebook these 6 stranded shipments under the new carrier contract, respecting the embargo list and cold-chain constraints, flag anything you can't resolve." Each "what next, given what just happened?" is a small reasoning problem. The 2026 frontier (GPT-5.5's instruction persistence across long tasks, Claude's agent-tuned adaptive thinking) is built to think hard at branch points and coast on routine steps. **When a wrong turn compounds, paying for reasoning at decision points is cheap insurance.**

### Where it's the wrong tool

**5. Classifying ten thousand support tickets by topic.** Reaching for the strongest reasoner at high effort "to be safe" is a mistake on every axis: the task is shallow pattern-match, reasoning models *overthink* and can degrade accuracy by talking themselves out of a correct first instinct, and you pay more and wait longer. **High volume + low per-item difficulty + checkable rubric = use the smallest model that passes.**

**6. The autocomplete that must feel instant.** Inline completion needs tens of milliseconds. Reasoning is disqualified by physics — thinking tokens are real latency, and even "low effort" blows the budget. Production stacks split it: fast non-reasoning models for the keystroke loop, reasoning reserved for "explain this bug" when the human asks and will tolerate a pause. **Anywhere a human waits in a tight loop, latency is the product and reasoning is the enemy.**

**7. Looking up a fact you already have.** "Capital of Australia?" "Reformat this JSON." The reasoning machinery is pure waste — and occasionally harmful, manufacturing spurious complications ("well, administrative vs. largest city...") and getting stuck in thought loops, a documented 2026 failure mode. Use a non-reasoning model, RAG, or a database query.

**8. The decision that hinges on missing information.** "Should we raise a Series B now or wait six months?" Thirty seconds of thinking produces a confident, beautifully structured answer — and that's dangerous. The bottleneck isn't reasoning horsepower; it's facts the model lacks (your runway, the term sheet, the board's appetite). Extra compute makes the output more fluent and authoritative *without making it more correct* — false confidence. **Reasoning amplifies quality over the inputs it has; it does nothing for inputs it lacks.** The fix is to gather the facts (or have the model ask), not crank the dial. *(advisory)*

**9. Anything where you can't tell if it's right.** Using high-effort reasoning to write "research-backed" claims at scale and shipping the output unread because the trace "looks thorough." A long, confident chain-of-thought is persuasive to humans even when the conclusion is wrong, and on open-ended generation there's no checkable answer to catch it. **No verifier, no escalation — keep a human in the loop or don't trust the extra effort.** *(advisory)*

### The one rule under all nine stories *(advisory)*

Spend reasoning compute in proportion to *problem difficulty*, not problem *importance* or your anxiety. A high-stakes lookup is still a lookup. A low-stakes proof is still a proof. The mark of someone who understands the technique is not that they always reach for the biggest reasoning model — it's that they know when *not* to.

---

## 6. Cross-industry usage & positioning (as of June 2026)

**The one-paragraph version.** A reasoning model spends extra compute *at the moment you ask* — long chain of thought, sampling several candidates, and/or search/verify before answering. The bet, proven over 2024–2026, is that thinking longer at inference buys accuracy that making the model bigger does not. As of June 2026 this is the **default operating mode** of every major model. The industry's center of gravity shifted from "which model" to "**how much thinking to spend on this request**," and the dominant engineering problem is no longer *can it reason* but *how to avoid overpaying for reasoning you don't need.*

**Four "knobs" now coexist:** sequential long chain-of-thought (table-stakes); parallel sampling + aggregation (vote or pick with a verifier); search (MCTS/tree search where a checker exists); and latent/continuous reasoning (think in vector space — cheaper, lower-latency, emerging in robotics). **RLVR** is the engine behind the quality jumps, which is why **math, code, and formal logic improved fastest** — they have cheap, perfect verifiers.

**Benchmark snapshot (June 2026)** — a capability waterline, not a leaderboard to memorize:
- Claude Opus 4.8 ~88.6% SWE-bench Verified; ~96.7% USAMO 2026; top of the AA Intelligence Index. *(sourced: lmcouncil.ai, June 2026)*
- GPT-5.5 Pro (xhigh) ~100% on a *specific mock-AIME instance*, ~87.7% FrontierMath T1–3; notably token-efficient. *(single-source, perishable — read "~100%" as a contest instance, not a stable capability)*
- Claude Fable 5 (max) ~95% SWE-bench Verified *(corroborated, morphllm, June 2026)*; ~87.8% FrontierMath Tier 4 *(single-source)*.
- Gemini 3.1 Pro (high thinking) ~94% GPQA, ~46% Humanity's Last Exam. *(single-source)*
- Strong open-weight reasoners (DeepSeek R-series, Qwen3, GLM-5.2, GPT-OSS-120B) are good enough that air-gapped/on-prem reasoning is real.

> *Caveat:* exact version numbers and "who's #1 this week" churn at roughly a 40-day cadence. Treat the *capability tier* (all frontier labs cluster within a few points on most reasoning benchmarks) as durable; treat the specific ranking as perishable. *(inference)*

**The economic story that dominates 2026: routing, not raw reasoning.** Reasoning tokens are expensive and slow, so the winning pattern is the **tiered intelligence stack / model router**: cheap models for classification and FAQ, mid-tier for drafting, frontier reasoning *only* for the hard final decision. Enterprises running deliberate tiered routers report blended cost ~$2.31/M tokens vs ~$18.40/M a year earlier — an ~87% drop in effective cost-per-intelligence. Adaptive reasoning-effort selection (e.g. ARES) cuts cost ~53% on agent benchmarks while holding or improving accuracy. **Advisory:** if your org adopts one thing from this space in 2026, it's a **router + effort policy**, not a model upgrade — and an evaluation harness that measures accuracy *at each effort tier* so routing is data-driven, not vibes.

**Sector by sector:**

- **Coding / developer tools — most mature; table-stakes.** Tests are perfect verifiers. Every serious coding agent (Claude Code, OpenAI Codex, Gemini CLI, Cursor, Copilot, Devin) is reasoning-native and uses **test-time search** (generate many candidate patches, run the suite, keep what passes — the CodeMonkeys pattern). State of the art: agents that spend compute adaptively across a long horizon (explore → plan → patch → verify → repeat). Smart-contract auditing is a high-value niche (a bug found is worth real money, and there's a verifier).
- **Science & mathematics — cutting-edge, highest absolute compute spend.** The purest demonstration that test-time compute unlocks otherwise-impossible results. AlphaProof hit IMO silver (2024) via enormous search through a Lean verifier; by IMO 2025, Harmonic's Aristotle and DeepSeek-Prover reached gold-medal level, and systems have formalized solutions to open Erdős problems. Defining trait: compute budgets per problem (minutes-to-hours) that dwarf any other sector — acceptable because the answer is verifiable and valuable.
- **Healthcare / clinical — rapid, but gated; mid-maturity.** Test-time scaling beats parameter scaling for medical *reasoning* on hard cases. Key nuance: it helps reasoning-heavy tasks (differential diagnosis, triage logic) but **not reliably knowledge-intensive lookup** — thinking longer doesn't conjure facts the model never learned. Positioning: decision *support*, human-in-the-loop, regulated.
- **Finance — fast-adopting; bifurcated by data sovereignty.** Frontier reasoning for research and risk narratives with finance-specific process reward models; and a strong pull toward small (<7B) reasoning models on air-gapped hardware for latency and sovereignty. Reasoning for analysis is table-stakes; *autonomous* reasoning-driven trading remains contested and tightly governed (FSB monitoring).
- **Legal — table-stakes for analysis, cautious on autonomy.** Domain-adapted models hit high accuracy on clause extraction/classification; reasoning helps most on multi-step contract logic and cross-document consistency (Claude Opus 4.8 cited as leading legal reasoning). The bottleneck is hallucination liability, so **verification and citation-grounding** matter more than raw thinking depth. *(advisory)*
- **Customer support / enterprise ops — table-stakes, but as the *cheap* tier.** The story is restraint: route the vast majority of tickets to cheap non-reasoning models, escalate to reasoning only on complex/ambiguous cases. "Always-on max reasoning for support" is now an anti-pattern.
- **Robotics / embodied AI — cutting-edge, the hot 2026 frontier.** Test-time compute for embodied planners is task-contingent (helps some tasks a lot, others not at all); careful allocation can match stronger models at up to ~65% lower latency. The standout move is **latent/recurrent-depth reasoning in Vision-Language-Action models** — think in vector space so a robot can deliberate on hard manipulation and measure its own uncertainty without token latency. Real-time control can't afford long token streams, so robotics is *driving* the efficient/latent variants.
- **Defense / national security — active but opaque.** Multi-step planning, tool use, and verifier-gated autonomy map directly onto defense use cases, but specific deployments aren't well-sourced in open material. *(inference; low source confidence)*
- **Consumer — invisible and ubiquitous.** The everyday chatbot silently routes hard prompts to a thinking mode. Most users never see the dial; they just notice it's slower-but-smarter on math/planning. **Table-stakes, abstracted away.** *(inference)*

**Bottom line for a decision-maker *(advisory)*:** Reasoning is now a *setting, not a purchase* — ask "what's our effort + routing policy," not "do we need a reasoning model." The ROI lives in *restraint* (the biggest 2026 wins came from spending *less* thinking via routing). **Your verifier is your ceiling** — domains with cheap automatic checkers compound fast; domains without them still need grounding and human review. Don't over-index on this week's leaderboard; the durable differentiator is your orchestration, not your base model.

---

## 7. Learning path for a technical leader

*Concepts, not code. Current as of June 2026.*

### Core mental models (the load-bearing ideas)

1. **Two budgets, not one.** Intelligence now has two cost centers: train-time (one-time, amortized over all queries) and test-time (paid *per query*, every time). The strategic shift of 2024–2026: buying intelligence at test-time is often cheaper and faster to deploy than retraining a bigger model. *(inference)*
2. **Thinking = generating tokens you don't show the user (mostly).** A reasoning model produces a long hidden chain of thought — tries approaches, catches mistakes, backtracks — then writes a short answer. The "thinking" is not a different mechanism; it's the same next-token prediction, pointed inward first. *(inference)*
3. **The ability was *trained in*, but it's *spent* at test time.** Labs use RL to *teach* a model to reason well (training-time investment). The *amount* of reasoning on any query is chosen at test time. Don't conflate the two.
4. **More compute helps only when the model is *close*.** Test-time compute lifts performance most on problems the model can *almost* solve. It does little for problems far beyond its reach and can *hurt* on easy ones (overthinking). The single most important nuance leaders miss. *(inference, grounded in Snell et al. 2024)*
5. **Difficulty-adaptive allocation beats uniform spending.** Spending the *same* total compute, allocated by difficulty, can be ~4× more efficient than spending it uniformly. Product knobs ("reasoning effort: low/medium/high") are the crude commercial version. *(sourced — Snell et al.)*
6. **Two axes: sequential and parallel.** Make one chain *longer* (think deeper) or run *many* chains and pick a winner (think wider, then vote/verify). Different latency/cost profiles; they combine.
7. **The chain of thought is not a reliable confession.** Research consistently shows the visible chain can be a post-hoc story that omits the true cause. This matters enormously for anyone betting on CoT for safety, audit, or debugging. *(sourced — Anthropic faithfulness work; 2026 follow-ups)*

### Sequenced concepts-only progression

1. **CoT as a prompt trick** → "think step by step" improves math/logic. Verify: you can explain why intermediate steps help a next-token predictor.
2. **From prompt trick to trained behavior** → RL with *verifiable rewards* makes models reason without humans hand-writing steps; pure RL made models spontaneously self-correct. Verify: you can explain why *verifiable* rewards were the unlock and why math/code came first.
3. **Test-time compute as a scaling axis** → the Snell insight: inference compute can beat parameter compute. Verify: you can state the "only helps when the model is close" caveat unprompted.
4. **Selection strategies (parallel)** → best-of-N, self-consistency, verifiers (outcome vs. process reward models). Verify: you can explain scoring the *final answer* vs. *each step*.
5. **Search and depth (sequential)** → longer chains, self-refinement, tree/graph search. Verify: you can describe the latency cost of sequential vs. parallel.
6. **The control surface** → "reasoning effort" / "thinking budget" as the productized knob; adaptive allocation as the frontier. Verify: you can map a latency/cost SLA onto an effort setting.
7. **Agentic test-time compute** → reasoning over many tool calls and turns — the 2026 center of gravity. Verify: you can explain why agentic loops multiply per-query cost.
8. **Limits and risks** → overthinking, inverse scaling, unfaithful CoT, monitorability fragility. Verify: you can name a failure mode for each and what it means operationally.
9. **The horizon** → latent/continuous reasoning (thinking in vectors). Verify: you can explain the tradeoff (efficiency vs. loss of a readable chain) and why it's not yet default.

### Reading spine (few, high-value — read the first three even if nothing else)

1. **Snell et al., "Scaling LLM Test-Time Compute Optimally…"** ([arXiv:2408.03314](https://arxiv.org/abs/2408.03314), 2024) — the foundational result; *the* mental model. Read abstract + intro + the difficulty-adaptive section.
2. **DeepSeek-R1 paper** ([arXiv:2501.12948](https://arxiv.org/abs/2501.12948), Jan 2025) — how RLVR produces reasoning from scratch, incl. the "aha moment." Read the intro and R1-Zero discussion.
3. **A current model card / docs page** for one frontier reasoning model with effort controls (GPT-5.5 reasoning effort, Claude Opus extended thinking, or Gemini 3 thinking) — connects theory to the actual product knob. Read whichever your org uses.
4. **"Chain of Thought Monitorability"** ([arXiv:2507.11473](https://arxiv.org/pdf/2507.11473), 2025) — why visible reasoning is both useful and fragile. Essential for safety/audit claims.
5. **Anthropic, "Measuring Faithfulness in CoT"** + a 2026 open-weight follow-up ([arXiv:2603.22582](https://arxiv.org/html/2603.22582v1)) — the "don't trust the confession" case, with evidence.
6. **A survey for breadth, skim only** — "From System 1 to System 2" ([arXiv:2502.17419](https://arxiv.org/pdf/2502.17419)) or "A Survey on Latent Reasoning" ([arXiv:2507.06203](https://arxiv.org/html/2507.06203v2)). A map, not a read-through.
7. **One current benchmark/landscape page** (e.g. an LM Council roundup, June 2026) — who's winning on what *now*. Goes stale fast; re-check quarterly.

### Understanding checkpoints — "you understand it when you can…"

- **…explain to a CFO** why two systems with identical model names can have 10× different per-query costs (reasoning effort / token budget), and when that spend is worth it.
- **…predict the curve:** accuracy rises, plateaus, and can *decline* (overthinking) as a model thinks longer — and why incorrect answers often have *longer* chains.
- **…state the "close enough" rule:** why test-time compute is wasted on problems far beyond reach and counterproductive on trivial ones — so "high effort everywhere" is a budget leak.
- **…distinguish sequential from parallel** and say which your latency budget affords.
- **…separate train-time from test-time** as different cost events.
- **…resist the faithfulness trap:** why you cannot treat the visible chain as a guaranteed-true audit log — with one concrete compliance risk this creates.
- **…size the agentic multiplier:** why an agent reasoning over 30 tool calls can cost 100× a single Q&A.

### How to evaluate an expert (interview)

*Goal: separate someone who has operated with these systems from someone who read headlines. Look for caveats offered unprompted and 2026-current specifics.*

- **Q1 — "When does more test-time compute *not* help, or hurt?"** *Strong:* names three regimes — problems beyond competence (no lift), easy problems (overthinking degrades), tasks needing *knowledge the model lacks* (no fix). Notes wrong answers correlate with *longer* chains; connects to difficulty-adaptive allocation. *Red flag:* thinks it fixes knowledge gaps or hallucinations.
- **Q2 — "Training to reason vs. spending compute to reason — where does each cost land?"** *Strong:* cleanly separates RLVR training (one-time, amortized) from per-query inference (recurring); knows verifiable-reward RL (math/code first) is *why* reasoning emerged, and GRPO/R1 was the open inflection. *Red flag:* believes the model is "learning" during inference.
- **Q3 — "Sequential vs. parallel — tradeoff, and which for a low-latency product?"** *Strong:* sequential = one longer chain (serial latency grows); parallel = many chains + selection (better worst-case, higher peak cost, needs a good verifier); picks on the actual SLA. *Red flag:* doesn't know parallel needs a way to *pick the winner*.
- **Q4 — "How much would you trust the visible chain of thought as an audit trail?"** *Strong:* skeptical but precise — often useful, but can be an unfaithful post-hoc rationalization; monitorability is real but fragile and outcome-based RL can erode it. Treats it as signal, not proof. *Red flag:* wants to ship CoT to regulators as a literal explanation.
- **Q5 — "What changed in the last 6–12 months?" (currency check)** *Strong:* reasoning effort is now a standard product control; the frontier moved to agentic/long-horizon test-time compute and adaptive allocation; cost dropped enough that frontier reasoning is broadly accessible; active work on overthinking mitigation and latent reasoning (not yet production default). *Red flag:* cites only o1/o3 and R1 with no awareness of effort controls, agentic scaling, or the cost collapse.

*Cross-cutting red flags:* uses "reasoning / agentic / more tokens" interchangeably with no mechanics; can't connect to unit economics; quotes leaderboards as settled truth; thinks any single test-time strategy universally wins.

---

## 8. Team notes (roles, hiring signals, build-vs-buy, failure modes)

**The one-paragraph version.** A reasoning model spends extra compute at answer-time — buying big gains on math, code, planning, and multi-step agent work, at the cost of latency and 5–50× more tokens per task. As of mid-2026 the control surface has converged on a single dial (a reasoning effort / thinking budget parameter across OpenAI, Anthropic, Google). The strategic point: **this is overwhelmingly a configuration-and-evaluation discipline, not a model-building discipline.** The hard, valuable work — knowing *when* to spend reasoning tokens, proving the spend pays off, and stopping the model from burning money on trivia — lives at the application layer.

### Roles & seniority — does an existing role absorb this?

**Default: yes.** For ~90% of companies, test-time compute is a capability you *consume*, and the natural owner is the **AI / LLM application engineer** you already have. The skills that matter — choosing effort levels per task, building evals, reading an inference bill, controlling latency/cost — are the modern AI-engineer job description, not a separate hire. *(advisory)* In priority order, this technique demands:

- **Eval-first judgment (the real bar).** In 2026, LLM engineers are evaluated less on prompting and more on system-level judgment; "prompt engineering" without evaluation is junior-level. *(sourced)* For reasoning specifically, the core skill is running an A/B across effort levels and *proving* whether high effort moves your metric — because frequently it doesn't.
- **Cost/latency economics.** Reads an inference bill without help; knows what a tokens-per-second SLO costs at scale. *(sourced)* The same task can swing 5–8× in cost between effort levels.
- **Routing design.** Sending easy queries to cheap/fast settings and hard ones to deep reasoning — the single highest-leverage piece of work, and it's plumbing + evals, not ML.

**When you need a different / more senior role:** if you're *training or post-training your own reasoning model* (RLVR/GRPO, distillation of reasoning traces), you need a genuine **ML / research engineer with RL experience** — scarcer and pricier (2026 US: ML engineers ~$165k median base vs ~$145k for AI engineers; the RL-research tier sits well above both — *$165k/$145k sourced; RL premium inference*). If you're an *agent-heavy company*, you want a senior engineer who owns the **reasoning-vs-action budget** and orchestration — still an application/platform role, just senior. *(advisory)* **Seniority read:** one mid-to-senior AI engineer can own reasoning configuration for a whole product; the judgment to say "high effort is wasting money here" is a senior trait. *(advisory)*

### Hiring signals & red flags

**Green flags** *(advisory, grounded in the eval/cost findings):* talks about reasoning as a cost/quality tradeoff and reaches for an **eval** to decide it; has built **per-task routing** and can describe the trigger logic; can tell a story where they **turned reasoning down/off** and quality held while cost dropped (the strongest signal); understands token economics (reasoning models can generate ~18× more tokens; per-token price drops don't save you if count explodes); knows the **overthinking / stopping-criterion** problem and has mitigations.

**Red flags:** "Reasoning models are just better, always use high effort" — the costliest single misconception (*sourced: high effort can be 5–8× cost/latency for flat quality; one case hit 6+ min and ~13,700 reasoning tokens for a single page*). Treats the hidden CoT as trustworthy explanation — *(sourced: CoT can be post-hoc rationalization, not the real cause)*. Wants to train a reasoning model from scratch to "differentiate" without a data moat or a verifiable-reward domain. No eval harness. Conflates reasoning with reliability — a long, confident, wrong answer is the most dangerous mode, and reasoning makes it *more* convincing. *(sourced)*

### Build vs. buy — default to RENT, hard

- **Rent (frontier API with effort controls) — default for ~95% of orgs.** *(advisory)* The control surface ships built-in across OpenAI, Anthropic, Google *(sourced)*, frontier quality improves faster than you could chase, and the hard parts (training stability, reward hacking, faithfulness) stay someone else's problem. Your moat is *what you do with it*: routing, evals, domain prompts, retrieval, UX.
- **Buy/build a smaller fine-tuned model — narrow, conditional yes.** The 2026 pattern is **distillation**: a frontier teacher generates traces, you fine-tune a small student for ~10× cheaper inference (defensible cost band ~$35k–$120k, payback often 3–7 months at high volume). *(sourced)* **Critical caveat:** reasoning-heavy workloads are largely *outside* the distillation envelope in 2026 — small fine-tunes fall behind on multi-step reasoning faster than eval sets reveal, and distilled students tend to be **confidently wrong rather than appropriately uncertain.** *(sourced)* Distill the *routine* parts; keep frontier reasoning for the hard tail.
- **Own it end-to-end (RLVR/GRPO) — rare; a real moat only when** (1) you sit on a domain with **cheap automatic verification** (code against tests, math with checkable answers, proofs, a simulator — *RLVR/GRPO only works where you can mechanically verify, sourced*); (2) that domain is **your core product**, not a feature; and (3) you have RL talent and appetite for a research-grade effort. Outside that intersection, owning the model is cost masquerading as strategy. *(advisory)*

### Common failure modes *(technical modes sourced; org diagnosis advisory)*

1. **Overthinking trivia / no stopping criterion.** Models burn long chains on easy problems and sometimes under-reason hard ones ("computational imbalance"). *Org fix:* mandate per-task routing and a token budget; make "did we A/B the effort level?" a launch gate.
2. **Cost/latency blowout from default-high.** 5–8× cost and latency for *flat* quality; "just extract this" tasks are where reasoning actively hurts. *Org fix:* treat effort as per-route config, not a global default; put someone who reads the inference bill on the team.
3. **Confident wrong answers after long deliberation.** Long reasoning makes wrong answers *more* persuasive to reviewers. *Org fix:* keep verification/ground-truth checks independent of the model's own reasoning; never let the CoT be its own grader for high-stakes output.
4. **Trusting the chain-of-thought as truth.** CoT is often unfaithful, and models can drift to hide reasoning while keeping a clean trace. *Org fix:* if you need auditability, build external evals; don't treat the trace as compliance evidence.
5. **Reward hacking (only if you train your own).** Models exploit formatting quirks or memorized answers; detection methods exist but this is research-grade. *Org fix:* if you're not training models, you inherit the vendor's mitigations — itself a reason to rent.
6. **The org mis-hire.** Spinning up an RL/research function for a problem an app engineer plus an API dial would solve — the most expensive *organizational* failure. *Org fix:* require an explicit verifiable-reward + core-product justification before approving any "train our own reasoning model" headcount.

### Bottom line for staffing *(advisory)*

**Hire** one mid/senior AI application engineer with real eval discipline and cost-literacy — they absorb this technique entirely for most orgs. **Don't hire (yet)** RL/research engineers unless verifiable-reward domain + reasoning-is-the-product + payback math all line up. **Rent the model, own the routing and evals** — your defensibility is *when and how* you spend reasoning tokens, not the tokens themselves. The interview tell that predicts success: a candidate who has, at least once, made a product *better* by making the model reason *less.*

---

## Sources

- Snell et al., *Scaling LLM Test-Time Compute Optimally* — https://arxiv.org/abs/2408.03314 (2024)
- *DeepSeek-R1: Incentivizing Reasoning Capability via RL* — https://arxiv.org/abs/2501.12948 (Jan 2025)
- ARC Prize, *OpenAI o3 breakthrough* (ARC-AGI-1 figures) — https://arcprize.org/blog/oai-o3-pub-breakthrough (Dec 2024)
- agentmarketcap.ai, *ARC-AGI-2 leaderboard 2026* — https://agentmarketcap.ai/blog/2026/04/06/arc-agi-2-leaderboard-2026-gemini-gpt5-claude-reasoning-benchmark (Apr 2026)
- AWS, *Verifiable-rewards RL with GRPO on SageMaker* — https://aws.amazon.com/blogs/machine-learning/overcoming-reward-signal-challenges-verifiable-rewards-based-reinforcement-learning-with-grpo-on-sagemaker-ai/ (2026)
- Hugging Face, *DeepSeek-R1 explained* — https://huggingface.co/blog/NormalUhr/deepseek-r1-explained (2025); EmergentMind, *DeepSeek-R1-Zero* — https://www.emergentmind.com/topics/deepseek-r1-zero (2026)
- *Understanding the aha moment* (contested) — https://sail.sea.com/blog/articles/62 ; https://arxiv.org/pdf/2503.20783 (2025)
- meta-intelligence.tech, *Reasoning models insight* — https://www.meta-intelligence.tech/en/insight-reasoning-models (2026)
- introl.com, *Inference-time scaling* (118× figure — single-sourced/contested) — https://introl.com/blog/inference-time-scaling-research-reasoning-models-december-2025 (Dec 2025)
- labellerr.com, *Compare reasoning models* (hallucination rates) — https://www.labellerr.com/blog/compare-reasoning-models/ (2026)
- The Register, *DeepSeek training cost* — https://www.theregister.com/2025/09/19/deepseek_cost_train/ (Sep 2025); CNN — https://www.cnn.com/2025/09/19/business/deepseek-ai-training-cost-china-intl (Sep 2025)
- tldl.io, *LLM API pricing 2026* — https://www.tldl.io/resources/llm-api-pricing-2026 ; lmcouncil.ai benchmarks — https://lmcouncil.ai/benchmarks (June 2026)
- *Chain of Thought Monitorability* — https://arxiv.org/pdf/2507.11473 (2025); Anthropic, *Measuring Faithfulness in CoT* — https://www-cdn.anthropic.com/827afa7dd36e4afbb1a49c735bfbb2c69749756e/measuring-faithfulness-in-chain-of-thought-reasoning.pdf ; *Lie to Me (open-weight CoT faithfulness)* — https://arxiv.org/html/2603.22582v1 (2026)
- ARES (adaptive reasoning effort) — https://arxiv.org/abs/2603.07915 (2026); CodeMonkeys — https://arxiv.org/abs/2501.14723 (2025); DeepMind AlphaProof — Nature s41586-025-09833-y (2025)
- Medical test-time scaling: m1 — https://arxiv.org/abs/2504.00869 (2025); *test-time scaling vs knowledge-intensive lookup* — https://arxiv.org/abs/2509.06861 (2025)
- Recurrent-Depth VLA (latent reasoning, robotics) — https://arxiv.org/abs/2602.07845 (2026); AI21, *Long-horizon agentic test-time compute* — https://www.ai21.com/blog/test-time-compute-swe-bench/
