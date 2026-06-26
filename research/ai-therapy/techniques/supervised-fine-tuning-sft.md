# Supervised fine-tuning (SFT)

*A field guide for a technical leader who funds, evaluates, and staffs this work — not who writes the training loop. State of the art as of June 2026. Factual claims are labeled **sourced** (with a URL and access date in the Sources list), **inference** (a reasonable deduction from sourced facts), or **speculation** (forward-looking, lower confidence). Learning-design and org recommendations are labeled **advisory** — my reasoned judgment, not established fact.*

---

## 1. What it is

A pretrained language model is a brilliant autocomplete engine and nothing more. It has read a large slice of the internet and learned one trick exquisitely well: predict the next word. That trick does not make it answer you. Ask a raw pretrained model a question and it might reply with three more questions — because, in the text it learned from, a question is often followed by more questions. It is not being difficult. It is doing exactly what it was built to do.

**Supervised fine-tuning is the step that turns that autocomplete engine into something that follows instructions.** You show the model thousands of worked examples — *here is a request, here is the ideal response* — and nudge its internal weights so that, going forward, it produces responses shaped like the ones you showed it.

The word **"supervised"** carries the key idea: every training example comes with a known-correct answer, written or vetted by a human (or by a strong model standing in for one). That is the contrast with the steps that usually come *after* SFT — preference optimization (DPO) and reinforcement learning (RL/GRPO/RLVR) — where the model generates its own attempts and gets *scored*, rather than being handed the gold answer to copy.

One sentence to keep in your pocket: **SFT is imitation.** You are not teaching the model new facts about the world. You are teaching it a *reflex* — a default way of responding it will reach for without being told. That single word explains both why SFT is so good at some jobs and so dangerous at others. (inference — widely held framing, not a single citation)

SFT is the foundation layer of essentially every modern post-training pipeline. The canonical 2026 recipe across nearly every industry is: **base model → SFT (teach the format and base skill) → DPO/RL (refine quality, reasoning, and taste).** SFT is rarely the *end* of the pipeline anymore, but it is almost always the *first stage* — and for a large class of narrow, well-specified problems it is the *entire* solution. (sourced)

---

## 2. How it works

The core loop is almost embarrassingly simple. It is the same next-word prediction the model was already doing — just on curated data, with one crucial twist.

**The chat template.** Each training example is wrapped in a fixed format using special marker tokens that say "the user's turn starts here," "the assistant's turn starts here," "this turn ends here" (for example, Llama-3's `<|start_header_id|>` and `<|eot_id|>`). Getting this template *exactly* right matters more than it sounds. A template mismatch — using a slightly different marker than the base model expects — is one of the most common production bugs, and it makes the model spray stray special tokens into the middle of otherwise fine sentences. The same data trained under the wrong template gives worse results, silently. (sourced)

**The twist — loss masking.** The model is shown the whole conversation, prompt plus answer, but it is only *graded* on the answer. The training signal is cross-entropy loss — a measure of "how surprised was the model by the correct next token?" — summed **only over the answer tokens**, with the prompt tokens masked out (their gradient zeroed). The formula labs actually use:

> L = − Σ over answer tokens of log p(correct next token | everything before it)

The intuition: you do not want to teach the model to *generate the user's question*. You want it to generate the *answer* to whatever question shows up. Masking the prompt says, in effect, "don't waste learning capacity memorizing the inputs; learn the mapping from input to good output." Drop the masking and the model burns capacity learning to predict user questions, dilutes the real signal, and gets worse. (sourced)

**Then it is ordinary gradient descent.** Compute that loss, backpropagate, nudge the weights a tiny step in the direction that would have made the right answer more likely, and repeat over the dataset for a few passes. A common starting point is **2–3 epochs**; push much past that and the model starts memorizing examples verbatim and overfitting. (sourced) Treat that as a starting-point heuristic, not a law — the right number of epochs depends heavily on your dataset size and method. (advisory)

**The capacity trick — LoRA / QLoRA — is how this got cheap.** Full fine-tuning updates all of the model's billions of weights, which needs enormous GPU memory. The dominant 2026 method instead **freezes the original weights and injects tiny trainable "adapter" matrices** alongside them. The math: instead of changing a big weight matrix W, you learn two skinny matrices B and A and add their product, so the effective weight becomes W + BA. If W is 4096×4096 (about 16.8 million numbers), a rank-16 adapter has about 131,000 trainable numbers instead — roughly a 120× reduction, often well under 1% of the model. B is initialized to zero (A to random values), so at the very start BA = 0 and the model behaves *identically* to the base, then learns the adjustment without a sudden "gradient shock." **QLoRA** adds 4-bit quantization of the frozen base, shrinking memory further. (sourced — the arithmetic and the zero-init are verified against the original LoRA paper)

A widely-cited 2026 starting recipe: rank 16–32, alpha = 2×rank, learning rate around 2e-4, 3 epochs, adapters placed on the attention projections (and optionally the feed-forward layers). (sourced) Two honest caveats: these are *starting points*, not universal laws — optimal learning rate and epochs are very dataset- and method-dependent — and "rank-stabilized" LoRA (which scales alpha by the square root of the rank) is now common and changes the alpha guidance. (advisory)

**How a practitioner knows it worked:** watch two curves. Training loss should fall smoothly; a sudden spike usually means the learning rate is too high or a bad batch slipped in. Held-out *evaluation* loss should keep falling too — if it bottoms out and turns back up into a U-shape, you have overfit and should have stopped earlier. (advisory)

---

## 3. Why it works

**The underlying principle.** The pretrained model already *contains* the knowledge and the language competence. SFT is not installing new facts — it is teaching *behavior and format*: "when you see a request, your job is to produce a helpful, well-shaped completion." This is why a few thousand to a few hundred thousand examples suffice, against the *trillions* of tokens used in pretraining. You are redirecting a capability the model already has, not building a new one.

The cleanest evidence is the **LIMA** finding (Meta, 2023): roughly **1,000** carefully curated examples can produce a strikingly capable assistant. The lesson that follows — repeated as a rule of thumb across 2026 — is that **quality and diversity beat raw volume**: "10,000 high-quality, diverse, correctly-formatted examples beat 1,000,000 mediocre ones." (sourced)

**Why the naive alternatives fail.**

- *Just prompt the base model.* Without SFT it does not reliably answer in the right shape; you fight its autocomplete instincts on every single query. SFT bakes the assistant behavior into the weights so you stop fighting.
- *Train on the whole conversation without masking.* The model spends capacity learning to predict user inputs, the signal gets diluted, and answers get worse.
- *Pour in millions of scraped Q&A pairs.* The model faithfully imitates whatever you show it — including the mistakes. Noisy, inconsistent data teaches inconsistency and caps your quality ceiling. (sourced for the LIMA-style quality argument; the failure-mode reasoning is inference)

**The honest caveat — SFT's known limitation, and how the story matured.** An influential January 2025 study, Chu et al.'s **"SFT Memorizes, RL Generalizes,"** argued that SFT tends to *memorize* its training distribution and generalizes poorly to genuinely out-of-distribution problems, while reinforcement learning generalizes better. That single framing drove two years of research toward SFT-then-RL pipelines.

By mid-2026 the picture is more nuanced and the pendulum has partly swung back. A 2025 follow-up — informally "Debunk the Myth of SFT Generalization" — showed that much of SFT's apparent weakness was an artifact of training on *frozen, identical prompts*; add prompt diversity and SFT generalizes well. Other work found that intermediate SFT checkpoints can beat RL models out-of-distribution, and that RL fine-tuning partly works by *healing* the forgetting that SFT introduces. The current, more accurate consensus: **SFT's job is to instill the format and core skill; its generalization is far better than the 2025 headline suggested if your data is diverse; RL is a complement, not a replacement, and crucially SFT is what stabilizes the output format so that RL is even trainable on top of it.** (sourced — all three papers verified and accurately characterized)

So the state of the art is *not* "SFT vs. RL." It is **"SFT as the mandatory foundation, then layer preference/RL on top."** (inference)

---

## 4. People & resources

There are two very different worlds here. Pick the row that matches your scale.

| | Small team / domain adaptation | Frontier lab post-training |
|---|---|---|
| **People** | 1–3 (one ML engineer + one domain expert/data curator) | tens of researchers + hundreds–thousands of human annotators/contractors |
| **Data scale** | ~1k–50k curated examples | ~1M+ examples (Tülu 3's open SFT mixture: **939,344 examples**, English-dominated with a smaller multilingual component) |
| **Compute** | 1 GPU (QLoRA: a 70B model fits in roughly 46GB on one A100; a 7B LoRA run needs around 12GB) | large GPU clusters |
| **Time** | hours (Unsloth benchmark: 70B QLoRA in ~4.2 hrs *on a small ~1k-example set*; 7B in 4–12 hrs) | days–weeks per recipe iteration |
| **Money** | tens to low-thousands of dollars of GPU rental | the dominant cost is **human data**, not compute |

*Basis and caveats:* the data-scale figure is the published Tülu 3 mixture — **939,344** examples (corrected from a widely-copied off-by-one of 939,343), and best described as English-dominated with a smaller multilingual (Aya) component rather than the often-repeated "70+ languages," which the mixture card does not prominently support. (sourced) The VRAM, time, and single-GPU figures come from 2026 fine-tuning guides and Unsloth benchmarks; treat the ~4.2-hour figure as tied to a small dataset and a specific GPU, not a universal constant. (sourced)

**Where the money actually goes.** For small teams the bottleneck is *not* GPUs — it is producing or sourcing high-quality labeled examples and building the evaluation harness *before* training starts. The strong 2026 workflow is: (1) confirm fine-tuning is even the right tool (versus prompting or RAG), (2) build your evaluation set *first*, (3) then curate data with production-grade rigor — deduplicate, quality-filter, and deliberately cover edge cases. (sourced / advisory)

**Roles you actually need (small team).** An ML engineer who owns the training and evaluation loop and the toolchain; a domain expert who defines what "good output" means and vets examples; and — easy to forget — whoever owns the *evaluation*, because without a held-out eval you cannot tell improvement from overfitting. (advisory)

**Toolchain, June 2026.** **Unsloth** for speed on consumer or single GPUs; **Axolotl** for YAML-driven, reproducible pipelines; **Hugging Face TRL** for custom training objectives; **LLaMA-Factory** as another widely-adopted open-source option. (sourced)

**One notable market shift.** OpenAI is **winding down its hosted fine-tuning platform** through 2026 (new-customer/inactive cutoffs around May–July 2026, full new-job shutdown around Jan 6, 2027), pushing teams toward fine-tuning open-weight models themselves on rented GPUs — which is exactly what the LoRA/QLoRA + Unsloth/Axolotl stack enables. Where reinforcement fine-tuning is still offered, it is billed by wall-clock training time (for example, around $100/hr for an o4-mini-class model), reflecting that RL is far costlier than plain SFT. (sourced)

---

## 5. Scenarios & stories

The framing, story structure, and the closing heuristic below are **advisory** — my reasoned synthesis. The factual patterns threaded through (cost ranges, accuracy figures, the form-versus-facts and forgetting findings, the default 2026 stacks) are **sourced**. The named-company vignettes are **illustrative composites** built to make sourced patterns concrete.

### Where SFT is the right tool

**Story 1 — One rigid shape, ten thousand times a day.** A mid-size insurer reads messy adjuster notes and must emit a strict JSON object: claim type, severity code, body-part enum, an "attorney involved" flag. A frontier model with a three-page prompt got it right 94% of the time. The other 6% — a stray markdown fence, a hallucinated enum, a chatty preamble — broke the downstream system, and at their volume 6% was thousands of failures a day. They collected ~2,000 corrected input→JSON pairs from their own logs, fine-tuned a small open model, and the format problem essentially vanished: the model now *reflexively* speaks their exact dialect of JSON. As a bonus, the small model cost an order of magnitude less per call. *Why SFT and not the alternatives:* prompting had plateaued; RAG is irrelevant (no external knowledge to fetch); there is one correct output per input, so there is nothing for a preference method to chew on. Fine-tuning is for form, not facts.

**Story 2 — Distilling the genius into something you can afford.** A consumer app uses a frontier model to triage and rewrite customer messages. Quality is great; the bill is brutal and the latency makes the UI sluggish. The dominant 2026 cost-reduction pattern is **distillation via SFT**: run the expensive model over hundreds of thousands of real tickets, capture its outputs, and train a small model to imitate it *on your specific traffic*. The reported economics are stark — inference landing roughly 12–40× cheaper per token, latency a fraction of the frontier model's, often within a couple of accuracy points on the narrow task. The teacher model *is* your labeling oracle, so you have effectively unlimited high-quality examples. Imitation is exactly the right loss.

**Story 3 — Teaching the agent the house grammar of tool calls.** A team building a coding/ops agent kept watching it call internal tools with subtly wrong argument structures, skip a required confirmation step, or invent functions that did not exist. They fine-tuned on a few thousand *good* multi-step traces — the exact sequence of tool calls, in their schema. This bakes the team's conventions into the model as muscle memory so the prompt no longer has to police every detail. *The caveat that marks the boundary:* SFT made the agent *fluent and well-formed*; it did not, by itself, make it *good at deciding* on genuinely novel multi-step problems. That is where teams layer RL on top. SFT was step one, not the finish line.

**Story 4 — The voice that has to be exactly this voice.** A legal-tech product drafts a specific kind of document: same register, same hedging, same clause ordering, the same refusal to give advice it is not allowed to give. Few-shot prompting got the tone "close," but "close" wandered across a long output, and the wandering was exactly what reviewers flagged. Fine-tuning on a curated set of gold documents made the style a *default* rather than something to be reminded of token by token. Consistent tone, structure, and refusal patterns over long outputs is a canonical fine-tuning use case, and one prompting genuinely struggles to hold.

### Where SFT is the wrong tool

**Story 5 — The confident liar.** A SaaS company wanted a support bot that "knows our product," and someone proposed fine-tuning on the entire docs site. Two things went wrong. The knowledge was **volatile** — docs changed weekly, and every change meant the model was now confidently wrong with no way to update short of retraining. And SFT is a *form* teacher, not a *fact* teacher: it taught the model to *sound* like the docs without reliably *recalling* them. The bot got more fluent and more wrong at the same time. The 2026 consensus: put volatile knowledge in retrieval, put stable behavior in fine-tuning, and stop forcing one tool to do both jobs. RAG consistently beats fine-tuning for factual recall.

**Story 6 — Reaching for SFT before the cheap tools were exhausted.** A startup, three weeks in, decided the model "wasn't good enough" and spun up a fine-tuning project — with no evaluation set, a prompt they had barely iterated on, and a few dozen hand-written examples. The blunt 2026 guidance: *most teams asking about fine-tuning should not fine-tune yet — they should fix their prompts, build a real RAG pipeline, and write evals, in that order.* Non-negotiable prerequisites: an eval harness built *before* the first training run, and at minimum a few hundred high-quality examples matching the production format exactly. And the real cost is not training compute — it is data curation, evaluation, and owning the 12-month lifecycle of a model that now needs versioning, monitoring, and periodic retraining. The startup that skips evals cannot even *tell* whether the fine-tune helped.

**Story 7 — Using SFT where the answer is a *preference*, not a *fact*.** A team wanted their assistant to be warmer, to refuse harmful requests more gracefully, to pick the *better* of two plausible replies — and discovered they had no single "correct output." They had *judgments between options*. That is the wrong shape for SFT's imitation loss. This is the territory of preference methods (DPO and relatives are the 2026 default for tone, refusal behavior, and "which answer is better"). SFT can set a baseline voice, but you cannot fine-tune your way to nuanced preference behavior from single-target examples — the loss function does not represent what you care about.

**Story 8 — Cloning demonstrations on a hard reasoning task, and capping the ceiling.** A quant team wanted a model to solve a class of multi-step *verifiable* problems (the answer is checkably right or wrong). They gathered worked solutions and ran SFT. It learned to *imitate the solution paths in the dataset* — quirks included — and plateaued well short of the bar. The 2026 evidence on reasoning is consistent: accuracy climbs from SFT to RFT to full RL (one cross-lingual study: ~46% SFT → ~67% RFT → ~72% RL). The mechanism is intuitive — SFT is *behavioral cloning*, so it inherits "exposure bias" and copies demonstrated paths rather than discovering better ones, which bites hardest on complex reasoning. When the answer is verifiable, optimizing for *getting it right* beats imitating *how someone else got it right*. The trap is subtle: SFT *works* — it just quietly caps your ceiling on exactly the tasks where you most want headroom.

**Story 9 — The narrow fine-tune that gave the model amnesia.** A team fine-tuned a small open model hard on one domain and shipped it. In production it was great at the domain and noticeably *worse at everything else* — basic reasoning, instruction-following, even tone slipped. This is **catastrophic forgetting**, and it is a live trap in 2026, not a solved problem. Narrow single-domain SFT routinely degrades general capability, and — this is the *established* empirical finding, not a contrarian surprise — the effect tends to get *more* severe at larger model scale, not less. A common assumption is that parameter-efficient methods like LoRA sidestep this by freezing most weights; recent work shows that assumption is shaky in continual-learning settings, where LoRA can still lose meaningful general capability. The lesson is not "never fine-tune" — it is that aggressive single-domain SFT has a real, measurable cost to the rest of the model, and you only catch it if your eval set covers capabilities *outside* the target domain. (Which is yet another reason Story 6's "build evals first" is non-negotiable.)

### The one-paragraph heuristic

Reach for SFT when the task is **behavior-bound and stable** and there is a **clear, single right output** to imitate: a fixed output format, a domain dialect, a house style, a set of tool-call conventions, or a big model's behavior you want to distill into a cheap small one. Reach *past* it — to RAG for changing facts, to prompting for still-shifting requirements, to preference tuning for matters of taste and refusal, to reinforcement fine-tuning for hard verifiable reasoning. And before any of it, build the eval harness, exhaust prompting and RAG, and gather a few hundred production-faithful examples — because the expensive part of SFT was never the training run. It is owning what you trained.

---

## 6. Cross-industry usage & positioning (as of June 2026)

**The one-line positioning.** SFT is the oldest and most boring part of the modern post-training stack — and *precisely because* it is boring and reliable, it is the universal substrate everything else is built on. It teaches a model to follow instructions and produce a format; it does **not** teach the model which of two valid answers a human prefers. That gap is what DPO and RL fill. So SFT is almost always the *first* stage, rarely the last. (sourced)

**How it is delivered: PEFT is the default.** Across virtually every industry except frontier-lab pretraining, SFT is done with parameter-efficient fine-tuning, not full-weight updates. LoRA trains small low-rank adapters (~1% of parameters) for most of full fine-tuning's quality in a lightweight, swappable package. QLoRA adds 4-bit quantization of the frozen base, dropping a 7B-class fine-tune to single-consumer-GPU memory. (One often-quoted framing — "from ~56GB to ~6GB" — is directionally right, but the 56GB upper bound is one specific point estimate; full 7B fine-tuning is cited anywhere from ~40 to ~120GB depending on optimizer and precision, so treat the headline number as soft. — sourced with caveat.) **Multi-adapter serving** (S-LoRA and successors) lets one GPU serve thousands of LoRA adapters at once, which is what makes "one base model, hundreds of tenant-specific SFTs" economical for SaaS and enterprise. PEFT is the single biggest reason SFT went from a frontier-lab activity to a commodity any team can run. (sourced; the "biggest reason" claim is inference)

**The maturity curve.** Table-stakes (commodity): format/style/instruction adaptation of an open model; LoRA/QLoRA on a 7B–70B model for a domain task; the SFT-then-DPO production pipeline; distilling a big reasoning model's traces into a small SFT student (near-commodity). Cutting-edge but standardizing: SFT on multimodal / vision-language-action models for robotics. Frontier-lab practice: SFT as the stabilizer before large-scale RL on frontier reasoning models. Cutting-edge research: self-distillation SFT in data-scarce scientific domains. (inference, grounded in the sector evidence below)

**Sector by sector.**

- **Coding / developer tools — the most mature SFT-heavy domain.** Open-weight coding models are the clearest showcase. Models such as Qwen3-Coder-Next, DeepSeek V4, GLM-5, Kimi K2.5 (with K2.6 just emerging), MiniMax M2.5, and Nemotron are trained through explicit multi-stage pipelines: **SFT → reinforcement fine-tuning → agentic RL.** Distillation is central — strong teachers generate reasoning/code traces, and SFT transfers those into smaller deployable students. Qwen3-Coder-Next reports roughly 70.6% on SWE-Bench Verified. (Note: by mid-2026 SWE-Bench Verified is flagged for contamination concerns and SWE-Bench Pro is the emerging successor, so single-number comparisons on Verified deserve a grain of salt.) *Leaders:* Alibaba (Qwen), DeepSeek, Zhipu/Z.ai (GLM), Moonshot (Kimi), NVIDIA (Nemotron). (sourced; specific minor version numbers corrected per verifier)
- **Healthcare / clinical.** SFT is the baseline-establishing step: clinicians write prompt-response pairs and the model is SFT'd to lock in correct medical style and content. Consensus: SFT alone suffices for simple rule-based classification; SFT-then-DPO is needed for triage, clinical reasoning, and summarization. Privacy and data sovereignty drive heavy use of LoRA on smaller, locally-deployable open models (Llama-class is the dominant base). *Leaders:* academic medical-informatics groups; venues like JMIR and npj Digital Medicine. (sourced)
- **Finance.** Long history here. BloombergGPT (50B) was the from-scratch flagship, but successors FinGPT and PIXIU showed that *SFT on open models beat BloombergGPT* in zero/few-shot settings — itself the lesson of the era: targeted SFT often outperforms expensive from-scratch domain pretraining. Sentiment, NER, and news classification are the bread-and-butter tasks; FinLoRA benchmarks established LoRA as the standard delivery method. *Leaders:* Bloomberg, the open FinGPT/PIXIU communities. (sourced)
- **Legal — a weaker example for an SFT-centric story than it first appears.** Deployment is becoming real: the HSBC–Harvey deal (announced 2026-01-20) is described in primary sources as a *rollout/pilot beginning to bring Harvey into HSBC's legal function*, not a completed global deployment. Importantly, Harvey is primarily a **RAG/agentic retrieval** product over legal documents; there is *no* public evidence that SFT-on-legal-corpora "underpins" it. Legal LLM tooling in fact leans heavily on RAG rather than domain SFT — so use legal as a *contrast* case, not a poster child. (sourced, corrected per verifier)
- **Defense / government / sovereign.** SFT is the mechanism for building classified-network domain models. Scale AI's **Defense Llama** (built on Llama 3, dating to Nov 2024) was adapted on military doctrine, international humanitarian law, and DoD-aligned policy — though note, per Scale's own materials, it used **SFT *plus* RLHF** (RLHF set tone), so this flagship "SFT" case is really SFT+RL; treat the sharp SFT-vs-RL line as a simplification here. Palantir AIP lets agencies run self-hosted fine-tuned models on classified networks. *Leaders:* Scale AI, Palantir, defense research labs. Sovereign-LLM strategy (nations fine-tuning their own models) is a named 2026 trend. (sourced, framing corrected per verifier)
- **Robotics — the fastest-moving SFT frontier.** Vision-Language-Action (VLA) models are *the* breakthrough architecture of the 2026 robot wave, and SFT is structurally central: models like π0 (pi-zero) initialize from a VLM backbone, pretrain on cross-embodiment robot data, then **SFT on a small set of high-quality teleoperation demonstrations** from the specific target robot/task. The frontier is going beyond SFT with online RL, but SFT-on-teleoperation-data remains the indispensable adaptation step. *Leaders:* Physical Intelligence (π0), OpenVLA, NVIDIA/Allen AI (MolmoAct), the LeRobot ecosystem. (sourced)
- **Customer support / consumer / general enterprise.** The largest-by-volume, least-glamorous use: SFT (almost always LoRA) to adapt tone, brand voice, format compliance, and product knowledge. The paper-consensus is that style tuning, format compliance, and safety are best handled by SFT-then-DPO — exactly the support/consumer profile. Multi-adapter serving makes per-customer SFT economical. (sourced / inference)
- **Science (biology, chemistry, reasoning).** Two distinct roles: (1) *reasoning distillation* — SFT on reasoning traces from teacher models to transfer chain-of-thought into smaller, cheaper models, now standard; and (2) *self-distillation SFT where labels are scarce* — e.g., a Dec-2025 method does self-distillation SFT of protein language models, generating their own filtered synthetic training data because real annotated protein data is far harder to get than text. Genuinely cutting-edge. (sourced)

**The platform/vendor landscape.** A notable 2026 shift in *who* offers hosted SFT. OpenAI is winding down its fine-tuning platform (closed to new users, limited runway for existing ones) while still documenting SFT and offering Reinforcement Fine-Tuning on reasoning models. Google Vertex AI offers SFT on Gemini 2.5 (Pro and Flash-Lite) and on open models like Llama 3.1 — *but* the Gemini 2.5 SFT endpoints have an announced retirement (around Oct 16–17, 2026), with migration to the Gemini 3.x line, so "Google as a stable primary SFT destination" is itself in flux. Anthropic Claude via Amazon Bedrock is the other primary closed-source destination, and H2O.ai-style vendors offer fine-tuning-as-a-service on private data. The tidy "managed closed-source SFT consolidated around Google + Anthropic/Bedrock" story is real but shakier than it sounds — it is better read as an **inference** than a settled fact, given the Gemini 2.5 retirement. (sourced for the individual moves; the consolidation framing corrected to inference per verifier)

**Bottom line for this section.** SFT is the universal, table-stakes foundation of post-training — present in essentially every deployed LLM/VLA system across every industry — almost always delivered via LoRA/QLoRA, almost always followed by DPO (and sometimes RL/RFT). The frontier of SFT *itself* has moved to three places: reasoning-trace distillation into small models, teleoperation-data SFT for robot VLAs, and self-distillation SFT in data-scarce scientific domains. The "SFT memorizes" critique that dominated 2025 has matured: SFT generalizes fine when the data and optimization are good, and it is indispensable as the stabilizing first stage that makes everything downstream possible. (inference, grounded in the above)

---

## 7. Learning path for a technical leader

*For a leader who decides, funds, and evaluates SFT work — not who writes the training loop. No coding labs.*

### Core mental models (the spine)

- **M1 — SFT is imitation, not understanding.** The model copies the *distribution of your answers*. This explains its strength (format, style, behavior) and its failure mode: it faithfully imitates your mistakes, your biases, even your uncertainty. (inference)
- **M2 — Quality dominates quantity (the LIMA lesson).** ~1,000 excellent curated examples can align a large model well. The job is curation, not collection. (sourced — LIMA, Meta 2023)
- **M3 — Decide *whether* to fine-tune before spending a dollar on data.** The escalation ladder: **prompt → RAG → SFT → preference/RL.** Most "we need fine-tuning" requests are solved a rung lower. SFT earns its place for a *consistent behavior/format/style* prompting can't hold, or for distilling a big model into a cheaper one. (advisory)
- **M4 — Knowledge versus behavior.** SFT is excellent at changing *how* a model responds; unreliable and risky for injecting *new facts* (hallucination plus forgetting). Facts usually belong in RAG, not weights. (inference)
- **M5 — No free lunch: forgetting.** Push hard on a narrow domain and the model loses general ability. The defenses are mostly restraint: lower learning rates, fewer epochs, LoRA adapters that leave base weights untouched, keep some general data in the mix. (sourced)
- **M6 — The evaluation harness is the product.** You cannot tell SFT worked without measuring it. Mature teams build the eval set *before* the first run: held-out cases, LLM-as-judge against the base model, and a general-capability regression check. (advisory)

### Sequenced concept progression (concepts only)

1. **Post-training landscape** — where SFT sits versus pre-training, RAG, prompting, DPO, RL. *Verify:* you can draw the escalation ladder and say what each rung buys.
2. **Instruction tuning & chat templates** — why the exact template/special tokens matter. *Verify:* explain why a template mismatch makes identical data give different results.
3. **Loss masking** — you score the model only on *response* tokens. *Verify:* say what goes wrong without it.
4. **Data: sourcing, curation, synthetic generation, judge-filtering** — the 2026 default is *synthetic data from a stronger model, then judge-filtered*; the filter is the highest-leverage step. *Verify:* explain why unfiltered synthetic data can be worse than a smaller filtered set.
5. **Full fine-tune versus PEFT (LoRA/QLoRA)** — the VRAM-versus-fidelity tradeoff. *Verify:* state in cost/risk terms when you'd reach past LoRA to full fine-tuning.
6. **Training knobs that matter** — learning rate, epochs (over-training equals forgetting), packing. *Verify:* name the two or three knobs most likely to cause a regression.
7. **Evaluation & regression-guarding** — held-out evals, judge-versus-base, capability retention. *Verify:* describe a pass/fail gate that stops a bad model shipping.
8. **SFT versus RL — the 2026 nuance** — the old "SFT memorizes, RL generalizes" slogan is now *contested*; hybrid SFT+RL is the frontier. *Verify:* explain why "just do RL" is an oversimplification.

### Curated reading/watching spine (few, high-value)

1. **Nathan Lambert — *RLHF Book* (rlhfbook.com)**, Instruction Tuning + Synthetic Data/Distillation chapters. Best free, current, leader-readable reference. (sourced, accessed 2026-06-25)
2. **LIMA: "Less Is More for Alignment" (Meta, 2023)** — the foundational data-quality argument. Abstract + conclusions. (sourced)
3. **Hugging Face TRL `SFTTrainer` docs** — for the *vocabulary* (packing, loss masking, chat templates), not to code from. (sourced, accessed 2026-06-25)
4. **One 2026 SFT-vs-RL paper** — e.g., *Debunk the Myth of SFT Generalization* (arXiv 2510.00237). Intro + conclusions only. (sourced, accessed 2026-06-25)
5. **One catastrophic-forgetting piece** — Cameron Wolfe's writing, or a 2026 "how learning rates regulate catastrophic overtraining" paper. (sourced, accessed 2026-06-25)
6. **One 2026 tooling comparison** — Unsloth / Axolotl / TRL / LLaMA-Factory plus the OpenAI hosted-API wind-down. (sourced, accessed 2026-06-25)

*Advisory: if they read one thing, the RLHF Book instruction-tuning chapter; if two, add LIMA.*

### Understanding checkpoints ("you understand it when you can…")

- …explain in 60 seconds **why most "we need to fine-tune" requests should start with prompting or RAG** — and name where SFT genuinely wins.
- …say **why 1,000 great examples beat 100,000 scraped ones**, and what "great" concretely means (correct, production-representative, edge-case-covering, deduplicated).
- …explain **why a model that aced the demo can be worse than base in production** (overfit, forgot general skills, eval set didn't match traffic).
- …describe **LoRA versus full fine-tune** in business terms (cost, risk, fit).
- …state **what you'd measure to decide ship/no-ship**, including a general-capability regression check.
- …push back, with a reason, on **"SFT just memorizes, so use RL"** — and explain why it's "it depends."
- …name **what synthetic data buys and where it bites** (cheap consistent scale versus inheriting the teacher's blind spots; the judge filter is mandatory).

### How to evaluate an expert (interview)

Goal: find judgment about **when *not* to fine-tune, how to guard quality, and how to reason under cost** — not definition recall.

- **Q1 — "A team wants to fine-tune so the model 'knows our internal policies.' How do you respond?"** *Strong:* questions whether SFT is the right tool; proposes RAG for the *facts* (policies change), SFT only for consistent *behavior/format*; evals before training; flags the forgetting risk of stuffing facts into weights. *Red flag:* can't separate teaching *behavior* from teaching *facts*; "more data is always better."
- **Q2 — "How much data, and where does it come from in 2026?"** *Strong:* quality over quantity (LIMA); synthetic generation from a stronger model *with a judge/filter step* as the default, filter as highest leverage; dedup, production-representativeness, edge cases. *Red flag:* no filtering of synthetic data; assumes distillation output is automatically good.
- **Q3 — "LoRA, QLoRA, or full fine-tune — how do you choose?"** *Strong:* frames it as VRAM-versus-fidelity-versus-cost, not a default; LoRA/QLoRA as starting point; full only for narrow high-stakes quality or very large data volumes; notes adapters reduce forgetting. *Red flag:* "full is obviously best," no cost/forgetting awareness.
- **Q4 — "The fine-tune looks great in the demo. What would make you refuse to ship?"** *Strong:* evals built *before* training; held-out set mirroring production; judge-versus-base; explicit general-capability regression check; wary of demo-overfit. *Red flag:* no held-out evaluation; vibes as acceptance criterion.
- **Q5 — "Someone says 'SFT memorizes, RL generalizes — skip SFT, do RL.' Your response?"** *Strong:* knows the slogan, knows it's *contested as of 2026*; depends on data/task/model; hybrid SFT-then-RL is the common pipeline; RL is costlier, less stable, needs a good SFT start. *Red flag:* treats RL as a magic upgrade, no cost/instability awareness.
- **Q6 (depth) — "What settings most often cause a fine-tune to *regress*?"** *Strong:* learning rate too high, too many epochs (over-train → forgetting); mismatched chat template silently corrupting everything; not masking the prompt. Defaults to restraint. *Red flag:* unaware of the chat-template footgun or the over-training/forgetting link.

**Green flags:** default instinct is "do we even need to fine-tune?"; obsessive about data quality and evaluation (the eval harness *is* the deliverable); comfortable saying "it depends" on SFT-versus-RL and explaining the dependency; thinks in cost/risk/forgetting; knows the 2026 landscape without being a tool fanboy. (advisory)

---

## 8. Team notes

*Org and learning-design judgments are **advisory**; factual claims are **sourced** / **inference** as labeled.*

**One-breath framing.** You take a model that already exists (open-weight like Llama / Qwen / DeepSeek, or a hosted base) and continue training it on your own "here is an input, here is the output I want" examples. It teaches **behavior** — format, tone, routing, a consistent way of responding — not **facts**. The dominant 2026 recipe is base → SFT → (optionally) DPO, and SFT itself is almost always LoRA/QLoRA. The single most important framing for an org: **SFT is a behavior tool, not a knowledge tool.** If the problem is "the model doesn't know our current pricing/docs/inventory," that's RAG; SFT will burn money and still be wrong because the facts change. (sourced)

### Who does this — role & seniority

**Default: an existing role absorbs it. Do not open a "Fine-Tuning Engineer" req as your first move.** (advisory) The title exists, and roughly half of placed ML engineers now do some fine-tuning alongside other work (sourced), but the mechanics have been commoditized by managed platforms and the LoRA toolchain — *"the barrier is now skill and data, not compute."* (sourced) The hard part is dataset design and evaluation, which are skills, not a job title.

By company stage (advisory):
- **Pre-product / first model (0–1):** No dedicated hire. A mid-to-senior ML/AI engineer (or a strong generalist who has shipped LLM features) runs SFT on a managed platform as one tool among prompting and RAG. The job is ~70% "build a clean dataset and an honest eval harness," 30% "click train." If your team can't yet *measure* whether a fine-tune beats the base model, hiring a specialist is premature — you'll just have a faster way to ship regressions.
- **Repeatable need / several models in production:** A senior ML engineer or applied scientist who *owns the eval-and-data pipeline* as a named responsibility. This is where the role justifies itself — not because training is hard, but because *deciding what to train on and proving it helped* is hard and recurring. (sourced for the role split)
- **SFT is a core moat (dozens of adapters, or it's your product):** Now you build a small team and care about serving infrastructure — multi-LoRA serving so hundreds of adapters share a GPU (the LoRAX/Predibase pattern). Most companies never reach here, and that's correct. (sourced)

**Seniority signal:** SFT is dangerous in junior hands not because the code is hard but because the *judgment* is — a junior reports "+8% on my task!" and never notices the model got dumber at everything else. You want someone senior enough to be skeptical of their own wins. (advisory)

### Hiring signals & red flags (advisory)

**Green flags:** talks about *data before method* (curation, dedup, "500 great examples beat 50k scraped ones"); has an *evaluation story with teeth* (held-out comparison against base, regression checks on tasks the fine-tune *didn't* target, a production canary — the 2026 playbook of gap-testing, paired comparison, confidence intervals, canary); *reaches for the cheaper tool first* and can say why fine-tuning was the right call; comfortable with LoRA/QLoRA as default and can name when full is actually needed (rarely); treats SFT as *one stage in a pipeline* (knows where DPO fits).

**Red flags:** *method-first, data-second* (fluent in PPO/DPO/GRPO trivia, vague on "how did you build the dataset and know it worked?"); *no regression awareness* (never been bitten by catastrophic forgetting — *the* most common silent failure); *wants to fine-tune for knowledge* ("teach the model our documents" — disqualifying for a senior role; that's a RAG problem); *wants to self-host GPU training on day one* with no moat reason (conflates "I can run the loop" with "this creates value"); *no production-eval experience* — *"most fine-tune evaluation proves the model moved, not that it improved."* (sourced for the eval-playbook and "moved not improved" lines)

### Build vs. buy — default to rent (advisory)

**Rent the training infrastructure. Own only the data and the evaluation.** Managed SFT is cheap and operationally trivial: open-weight managed LoRA SFT runs roughly **$0.48–$0.50 per 1M training tokens** on models up to ~16B (Together AI, Fireworks), with serving baked in (sourced); frontier hosted options price small models as the value pick (e.g., a GPT-4.1-Nano-class run cited around $0.20/1M tokens) (sourced); and if you genuinely need many fine-tunes, multi-LoRA servers let hundreds of adapters share one GPU — though even Predibase, the poster child, was acquired and repositioned, a reminder that pure-play fine-tuning vendors are consolidating (sourced).

The genuine **build** cases — and notice all three live in *data and evaluation*, not training infra: (1) **data gravity / compliance** (training data legally can't leave your environment — regulated health, defense, finance; self-hosting is a deliberate compliance purchase, not an efficiency play); (2) **volume of adapters is your product** (vendor serving markup dominates your COGS, so owning the multi-LoRA serving layer is the moat); (3) **a frontier-beating niche model is your differentiator** (the well-supported 2026 thesis that a small fine-tune on proprietary data can out-perform the frontier on your specific task, cheaper and faster — here the moat is the proprietary dataset and eval loop, which you own regardless; you can still rent the GPUs). The buy/build line: **rent the compute, own the data and the judgment.** (sourced for the cost/thesis facts; the framing is advisory)

### Common failure modes

1. **Catastrophic forgetting (the silent killer).** The model improves on the target task and quietly degrades on everything else — general reasoning, instruction-following, even safety. Larger models resist it somewhat better; more training data makes it worse. (sourced) *Org mitigation:* mandate a held-out general-capability eval and a paired comparison against base before any fine-tune ships. (advisory)
2. **"It moved, so it improved."** Teams celebrate a target-metric bump that's really noise or overfitting, with no confidence intervals and no production canary. The fix is process, not talent: bootstrap CIs, gap testing across multiple sets, canary on real traffic. (sourced)
3. **Fine-tuning a knowledge gap.** Using SFT to inject facts that change — expensive, brittle, stale the moment they're baked into weights. This is a RAG problem wearing an SFT costume. (sourced)
4. **Skipping the cheaper rungs.** Reaching for fine-tuning when better prompting, or prompting + RAG, would have closed the gap for a fraction of the cost. The 2026 consensus is explicitly that these are *not* a ladder you must climb — the strongest setup most teams ship is fine-tune for format + RAG for facts + a short system prompt for steering, chosen deliberately. (sourced)
5. **Emergent misalignment from messy data.** Narrow or low-coherence fine-tuning data can break the model's broader alignment and coherence, not just its task performance. (sourced) *Org implication:* dataset review is a safety control, not just a quality nicety. (advisory)
6. **Buying GPUs to prove you can fine-tune.** The most expensive org failure: standing up self-hosted training infra before there's a moat reason, when a managed LoRA run costs cents per million tokens. You've hired for and capitalized a commodity. (advisory)
7. **Maintenance debt nobody scoped.** Base models get deprecated; your fine-tune is married to a specific base version. Someone has to own re-tuning when the base moves — a standing cost teams routinely forget to budget. (inference)

### Bottom line for a hiring/org decision

Don't hire a fine-tuning specialist first — give SFT to a skeptical, senior-enough ML/AI engineer as one tool, and judge them on dataset and eval discipline, not training-loop fluency. Rent the training (managed LoRA SFT is a cents-per-million-tokens commodity). Own the data and the eval loop — that's where the moat and the real skill live. Promote it to a team only when you have a compliance, volume-of-adapters, or proprietary-niche reason that rent economics can't serve. The competence you're actually hiring for is not "can fine-tune a model" — that's a button now. It's *"can tell whether a fine-tune helped, and knows when not to fine-tune at all."* (advisory)

---

## Sources

- LIMA: "Less Is More for Alignment," Meta, 2023 (the ~1,000-example data-quality argument).
- Chu et al., "SFT Memorizes, RL Generalizes," January 2025 (the framing that drove SFT-then-RL pipelines).
- "Debunk the Myth of SFT Generalization," arXiv 2510.00237, 2025 (prompt-diversity rebuttal).
- "RL Heals OOD Forgetting," arXiv 2509.12235, 2025 (RL partly heals SFT-induced forgetting).
- "Beyond English-Centric Training," September 2025 (cross-lingual SFT→RFT→RL figures: 46.3 / 66.8 / 71.5).
- Tülu 3 open SFT mixture (allenai/tulu-3-sft-mixture, Hugging Face): **939,344** examples, English-dominated with a smaller multilingual (Aya) component.
- LoRA original paper (Hu et al., 2021): low-rank adapters, B-initialized-to-zero; QLoRA (Dettmers et al., 2023): 4-bit quantized base.
- Hugging Face TRL `SFTTrainer` documentation, huggingface.co/docs/trl/sft_trainer (accessed 2026-06-25).
- Nathan Lambert, *RLHF Book*, rlhfbook.com — Instruction Tuning and Synthetic Data/Distillation chapters (accessed 2026-06-25).
- Unsloth fine-tuning benchmarks and 2026 fine-tuning guides (VRAM, time, ~4.2-hr 70B-QLoRA figure on a small dataset); spheron.network, dev.to/ultraduneai (accessed 2026-06-25).
- OpenAI fine-tuning wind-down and Reinforcement Fine-Tuning (~$100/hr wall-clock for o4-mini-class); OpenAI platform docs (accessed 2026-06-25).
- Google Vertex AI SFT on Gemini 2.5 (Pro/Flash-Lite, with announced ~Oct 16–17 2026 retirement) and open models; Vertex AI docs (accessed 2026-06-25).
- Anthropic Claude fine-tuning via Amazon Bedrock; AWS docs (accessed 2026-06-25).
- Coding-model pipelines and SWE-Bench Verified (~70.6% Qwen3-Coder-Next; Verified contamination concerns, SWE-Bench Pro emerging), model cards and benchmark coverage (accessed 2026-06-25).
- Healthcare/clinical SFT consensus: JMIR, npj Digital Medicine (2025–2026).
- Finance: BloombergGPT, FinGPT, PIXIU, FinLoRA benchmarks (2023–2026).
- Legal: HSBC–Harvey announcement, 2026-01-20 (rollout/pilot; Harvey is primarily RAG/agentic) — HSBC, Harvey, Law.com, Artificial Lawyer.
- Defense: Scale AI Defense Llama (Llama 3, Nov 2024, SFT + RLHF); Palantir AIP; WARBENCH (2026).
- Robotics VLAs: π0 / Physical Intelligence, OpenVLA, MolmoAct (NVIDIA/Allen AI), LeRobot ecosystem (2025–2026).
- Science: reasoning-trace distillation; self-distillation SFT of protein language models (Dec 2025).
- Managed SFT pricing: Together AI / Fireworks (~$0.48–$0.50 per 1M tokens); OpenAI fine-tuning (~$0.20/1M for a Nano-class model); eesel.ai, docs.fireworks.ai, pricepertoken.com (accessed 2026-06-25).
- Multi-LoRA serving (S-LoRA / LoRAX / Predibase); awesomeagents.ai (accessed 2026-06-25).
- Fine-tuned-LLM evaluation playbook ("moved vs improved," gap testing, CIs, canary); futureagi.com/blog/evaluating-fine-tuned-llms-2026 (accessed 2026-06-25).
- Catastrophic forgetting (severity rises with scale): arXiv 2308.08747 and 2026 follow-ups; arXiv 2406.04836.
- Emergent misalignment from narrow/low-coherence data: arXiv 2511.20104.
- Prompting-vs-RAG-vs-fine-tuning ("not a ladder"): thenewstack.io, bigdataboutique.com (2026).
- Fine-Tuning Engineer role/market data: secondtalent.com (2026).
- LoRA/QLoRA practitioner guides: effloow.com, sitepoint.com, futureagi.com (2026).
