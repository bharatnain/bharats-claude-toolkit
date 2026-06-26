# Native Any-to-Any Multimodal Models

*State of the art as of June 2026. Factual claims are labeled sourced (with URL + date), inference, or speculation. Learning-design and org judgments are labeled advisory. Written in plain language for a reader who decides and funds this work rather than implements it.*

---

## 1. What it is

A **native any-to-any multimodal model** is a single neural network that takes in any mix of text, images, audio, and video, reasons over all of it inside one set of learned weights, and — in the fullest version — produces several of those forms back, with no glue code stitching separate specialist models together.

The word that carries the weight is **native**. The old way to "do multimodal" was a *pipeline of specialists*: a speech recognizer turned voice into text, a language model reasoned over the text, a separate image generator drew a picture, a text-to-speech model spoke the answer. Each box was a different model with its own training, and text was the universal exchange format passed between them — a committee with a coordinator. *(sourced: arxiv.org/html/2505.02567v5, 2026)*

A native model deletes the committee. Everything lives in **one shared internal language** the model thinks in directly. The technical phrase you will see is **"early fusion in a unified backbone"**: all modalities are turned into tokens early and flow through the *same* transformer, rather than being processed separately and merged late. The payoff is that the model keeps information a pipeline throws away at every handoff — it can hear the sarcasm in your voice and let that shape its reply, because your tone was never flattened into a transcript. *(sourced: arxiv.org/html/2505.02567v5, 2026; emergentmind.com NMMs topic, 2026)*

**One distinction worth holding onto, because vendors blur it:**

- **Native input *understanding*** — one model genuinely reasons over mixed inputs (a chart + a voice note + a video clip together). This is now *mature and widespread* in mid-2026. *(sourced: arxiv.org/html/2605.25343v1, 2026)*
- **Native any-to-any *generation*** — the *same* model emits new images, audio, or video natively, not by calling a separate generator. This is the *cutting edge*, and only a handful of systems do it truly end-to-end. *(sourced: venturebeat.com Gemini Omni, 2026-05-19)*

This distinction matters more than any product name. **The "omni" in a product name does not prove native any-to-any generation.** *(inference, per verifier)* GPT-4**o** and Gemini **Omni** both signal multimodal ambition, but they sit at different points on the spectrum.

**The frontier as of mid-2026:**

- **Gemini Omni** (Google DeepMind), announced at Google I/O on **2026-05-19** — accepts text, image, audio, and video in one prompt and, crucially, **generates video natively inside the same reasoning core** rather than chaining Google's separate Veo/Imagen/Lyria models. It is the current high-water mark for true any-to-any *generation*. *(sourced: venturebeat.com, 2026-05-19; orbilontech.com, 2026)*
- **GPT-5.5** (OpenAI, codename "Spud"), released **2026-04-23** — OpenAI's first model to **unify text, image, audio, and video on the *input/understanding* side in one architecture**. "Watch this video and summarize what was decided" is now one call, where GPT-5 had to route to a separate audio model. **Correction worth stating plainly (sourced: verifier, 2026):** GPT-5.5 is *not* native any-to-any on the *output* side — it does not natively emit audio or video, and image generation still routes to a separate generator. Its context window is **1M tokens (API)**, not 400K; the 400K figure is only the Codex surface cap, a throughput/cost decision, not the model spec. *(sourced: verifier, 2026; teamday.ai/blog/gpt-5-5-launch, 2026, which is promotional and inflates the output and context claims)*
- **Open models:** **Emu3.5** (34.1B parameters), Qwen3.5-Omni, DeepSeek Janus, Show-o2, BLIP3o-NeXT, Molmo, GLM-4.5V — these match or beat earlier proprietary models on text-to-image, image editing, and interleaved generation, and are openly documented so we can see inside them. **Note (sourced: verifier, 2026):** Emu3.5 generates interleaved **text + image** outputs only — it ingests audio/video during training but does *not* generate them. *(sourced: arxiv.org/html/2510.26583v1, 2026; siliconflow.com, 2026)*

The honest framing: the genuinely native end-to-end *generation* systems are still a minority. Much of the field reaches the same user-facing result by orchestrating specialized models behind a unified front door. For most buyers the *result* is what matters; for latency, cost, and capability ceilings, the architecture difference is real, and it is the live research debate of 2026. *(inference)*

---

## 2. How it works

### The one trick that makes it possible: turn *everything* into tokens

A language model already works by predicting "the next token" — the next chunk — over and over. Native multimodal models extend exactly this machinery to *everything* by converting every kind of data into discrete tokens that live in one shared vocabulary.

- **Text** → tokens the normal way (sub-word pieces, e.g. byte-pair encoding).
- **Images** → tokens via a **visual tokenizer**. This is the crucial part. A learned component builds a fixed dictionary — a **codebook** — of visual "words," chops an image into a grid of patches, and replaces each patch with the nearest codebook entry. A picture becomes a sequence of integers, exactly as text becomes a sequence of integers. *(sourced: arxiv.org/html/2505.02567v5, 2026; PMC12893917 / Nature, 2025–26)*
- **Audio and video** → tokens the same way, with the time dimension added.

> **Intuition:** Think of it as inventing a single alphabet that can spell a sentence, a sunset, a chord, and a clip of someone waving — all in the same letters. Once everything is "spelled" in one alphabet, the model neither knows nor cares which modality a token came from. It just predicts the next letter. "Describe this photo, then draw a cartoon version" becomes one long sentence in this universal alphabet, and the model continues the sentence.

### Concrete example — Emu3.5 (open, so we can see the gears)

Emu3.5 is a plain **decoder-only transformer** (64 layers, 5,120-dim, 34.1B params) trained with **one objective: next-token prediction** using ordinary cross-entropy loss — the *same* loss as a text LLM. Its vocabulary is **282,926 tokens**: ~151,854 text tokens (reusing the Qwen tokenizer) plus **131,072 vision tokens**. Visual tokens are treated as discrete symbols *identical in kind* to words. *(sourced: arxiv.org/html/2510.26583v1, 2026)*

**Correction on the tokenizer (sourced: verifier, 2026):** Emu3.5's visual tokenizer is **IBQ** (Index-Backpropagation Quantization), with a codebook of 131,072 entries and a downsample factor of 16 — *not* the VQ-VAE / VQ-GAN family. The general idea (learned codebook, nearest-entry lookup) is the same family of technique, but the specific component in Emu3.5 is IBQ. The earlier draft named the wrong tokenizer for this exact model; this matters because Emu3.5 is the worked example.

So when Emu3.5 "generates an image," it is literally **writing image tokens one at a time**, then a decoder turns that token grid back into pixels. Same act as writing a sentence — and again, for Emu3.5 the generated modalities are **text and image only**. *(sourced: arxiv.org/html/2510.26583v1, 2026; verifier, 2026)*

### The catch this exposes, and the two fixes

Generating an image token-by-token is **slow** (a 1024×1024 image is a huge number of tokens), and historically autoregressive image quality lagged diffusion models. The field's 2026 answer is to blend in **diffusion** — the iterative "start from noise, denoise step by step" method that powers high-fidelity generators:

1. **Discrete Diffusion Adaptation (DiDA)** in Emu3.5: instead of predicting image tokens strictly left-to-right, it lets the image's tokens be refined **in parallel, attending to each other bidirectionally**, while keeping the causal text flow. This gives roughly a **20× inference speedup** with quality comparable to Gemini 2.5 Flash on image generation. *(sourced: arxiv.org/html/2510.26583v1, 2026)*
2. **Hybrid AR+diffusion architectures** generally: one transformer trained with *both* a next-token-prediction loss (good for text, reasoning, ordering) *and* a diffusion loss (good for image/video fidelity). Gemini Omni is described as combining transformer, diffusion, and temporal modules in one training graph, generating picture and spatial audio *together* so footsteps land on the right frame and lips match speech. *(sourced: arxiv.org/html/2505.02567v5, 2026; orbilontech.com, 2026)*

### Four ways to tokenize images — the live design fork

There is a genuine fork in the road, and different labs pick differently *(sourced: arxiv.org/html/2505.02567v5, 2026)*:

| Approach | How the image is encoded | Good at | Weak at |
|---|---|---|---|
| **Pixel-based (VQ-GAN / IBQ-style)** | Reconstruction-optimized codebook | Faithful detail, easy to slot into an LLM vocabulary | Very long sequences; weak semantics |
| **Semantic (CLIP/SigLIP)** | Text-aligned concept features | Cross-modal *understanding*, alignment with words | Hard to control at the pixel level |
| **Learnable queries (Q-Former)** | Compact learned summary tokens | Short sequences | Extra compute |
| **Hybrid / decoupled (e.g. Janus)** | Semantic path for understanding, pixel path for generation | Best of both | Two systems to maintain |

> **Intuition for the fork:** a tokenizer tuned to *redraw* an image perfectly captures texture but not meaning; a tokenizer tuned to *match images to words* captures meaning but blurs detail. Understanding wants meaning; generation wants detail. One tokenizer rarely nails both — the central unsolved tension below.

---

## 3. Why it works

### The principle: a shared representation enables transfer and grounding

There is one deep idea underneath: **if every modality lives in the same internal space, the model can reason *across* them before committing to an answer.** Gemini Omni can weigh a character image, a background prompt, and an audio track against each other *before* generating anything, because all three are tokens in one space the same transformer attends over. *(sourced: orbilontech.com, 2026)*

Two payoffs follow:

- **Cross-modal transfer.** Concepts learned in one modality strengthen the others. Seeing millions of captioned images teaches the *word* "rust" and the *look* of rust at once; they reinforce each other because they share representational machinery. Some 2026 work even finds that training a model to *generate* images improves its *understanding* of them. *(sourced: arxiv.org/html/2601.21406v1, 2026)*
- **No lossy handoffs.** This is the decisive practical argument. In a pipeline, every boundary between models is a translation, and translation loses information. A vision model collapses a picture into a paragraph; the language model then reasons over the *paragraph*, having lost the actual pixels, the exact timing of a waveform, the temporal correlations in a video. A chain of models loses pixel relationships, waveform data, and temporal correlations *at every handoff*; a unified model retains them throughout. *(sourced: mygreatlearning.com, 2026)*

> **Intuition:** A pipeline is a relay of translators who each speak only two languages — every baton-pass goes through a lossy summary, and nuance evaporates. A native model is one polyglot who hears, sees, and speaks everything at once and never summarizes for a colleague.

### Why the naive alternatives fail

**Naive alternative #1 — Glue specialists together (the pre-2024 pipeline).** It fails on:

- *Information loss at every seam* (above).
- *No joint reasoning.* The parts cannot negotiate. The video generator cannot ask the audio generator "what exactly did the voice say at 0.4s?", so lips drift out of sync. Native models keep them in one space, so audio and frames stay aligned by construction. *(sourced: orbilontech.com, 2026)*
- *Brittleness and cost.* Many models to host, route, and version. With a unified model, a mixed text+video+audio+screenshot task is closer to "one call" than an orchestration of several. *(sourced: teamday.ai/blog/gpt-5-5-launch, 2026 — promotional; treat as directional)*

**Naive alternative #2 — Use the cheapest visual tokens (early native models like Chameleon/Emu3 with low-level codes).** Treating images as low-level reconstruction codes *does* unify everything under next-token prediction, but there is a **semantic-level mismatch**: low-level pixel codes and high-level word tokens do not align well, which hurts cross-modal learning and makes scaling sample-inefficient. The 2026 fix moved toward higher-level, text-aligned visual semantics (ViT/SigLIP-derived), used by BLIP3o-NeXT, X-Omni, NextFlow, Kelix, and others. *(sourced: arxiv.org search results 2026; arxiv.org/html/2602.09843v1 "Kelix," 2026)*

### The honest caveat — the gap that is still open

There is a real, unsolved tension as of mid-2026: the **understanding-vs-generation gap**. Autoregressive token prediction excels at *reasoning and understanding*; diffusion excels at *high-fidelity generation*. They model the world differently — discrete-sequential vs. continuous-joint-distribution — and forcing one transformer to be great at both remains hard. Multiple 2026 papers exist specifically to *measure* and *close* this gap (UEval, "Quantifying the Gap between Understanding and Generation," Kelix, UniFork). *(sourced: arxiv.org/pdf/2601.22155, 2026; arxiv.org/pdf/2602.02140, 2026; arxiv.org/html/2602.09843v1, 2026)*

> **Inference (mine):** this is why hybrid AR+diffusion designs dominate the frontier in 2026 — nobody has a clean single-objective model that is simultaneously best-in-class at both reasoning and pixel fidelity. It is also why GPT-5.5 unifies *understanding* but still routes *generation* out: unifying input is solved; unifying high-fidelity output across all four modalities is not.

---

## 4. People & resources

The numbers below are **orders of magnitude**, anchored to the one fully-documented open model (Emu3.5) plus public industry norms. Frontier proprietary models (Gemini Omni, GPT-5.5) are larger but undisclosed — those figures are inference and labeled as such.

### Data scale (most concrete, from Emu3.5) *(sourced: arxiv.org/html/2510.26583v1, 2026)*

- **>13 trillion multimodal tokens** of training data total.
- **63 million videos** (~790 years of footage) with transcripts.
- **500M+ image–text pairs**, 30M video–text pairs, ~27M any-to-image samples, 3T text-only tokens.
- *Basis:* roughly **10× the data plumbing of a text-only LLM**, because you also need aligned image/video/audio pairs, not just scraped text. **Inference:** frontier closed models likely use comparable-or-larger corpora.

### Compute

- Emu3.5 pre-trained in two stages (10T tokens at 32K context, then 3T at higher resolution up to 1024×1024), using tensor parallelism (TP=8) and context parallelism across a distributed cluster. *(sourced: arxiv.org/html/2510.26583v1, 2026)*
- **Order of magnitude (inference):** training a ~30–40B native multimodal model is a **thousands-of-GPUs, multi-week** run — roughly **10²⁴–10²⁵ FLOPs**, in the **single-digit-millions of dollars** range for one full run, *excluding* failed runs, ablations, and data pipeline build-out. Frontier omni models (Gemini Omni / GPT-5.5 scale): **inference** puts these in the **tens-to-hundreds of millions of dollars** all-in, consistent with public frontier-LLM training-cost reporting.
- **Why more expensive than a text LLM (inference):** video tokens are bulky (long sequences → quadratic attention cost), and you train on *two* objectives (next-token + diffusion). Serving is also harder — there is active 2026 research (vLLM-Omni) on "disaggregated serving" just to run these efficiently. *(sourced: arxiv.org/pdf/2602.02204, 2026)*

### Team & roles (advisory — typical shape, not from a single source)

- **Pretraining / architecture researchers** (4–10): the transformer, the loss blend, the fusion strategy.
- **Tokenizer / representation specialists** (2–5): the VQ/IBQ + diffusion-decoder team — *disproportionately important*, since the tokenizer choice (Section 2's fork) caps quality.
- **Data engineering** (5–15+): often the **largest** group. Sourcing, cleaning, deduplicating, captioning, and *aligning* image/audio/video/text at trillion-token scale is the dominant practical bottleneck. **Advisory:** budget more here than feels reasonable.
- **Infrastructure / distributed-systems engineers** (3–10): cluster orchestration, parallelism, fault tolerance over multi-week runs.
- **Post-training / alignment** (3–8): instruction tuning, RLHF, and reinforcement methods now extended to *visual generation* (e.g. UniGRPO, ParaUni, 2026). *(sourced: arxiv.org/pdf/2603.23500, arxiv.org/pdf/2512.05422, 2026)*
- **Evaluation** (2–5): multimodal benchmarks are immature and contested; building trustworthy evals is real work (UEval, BEAR). *(sourced: arxiv.org/pdf/2601.22155, arxiv.org/pdf/2510.08759, 2026)*

> **Advisory takeaway on resourcing:** the leverage is *not* in the transformer (it is nearly a stock LLM). It is in (a) the **visual tokenizer**, (b) the **data pipeline**, and (c) the **AR+diffusion blend**. A smart team underinvests in data plumbing and tokenizer quality at its peril — that is where native multimodal projects actually succeed or fail.

### Time

- **Inference / advisory:** for an experienced lab with infrastructure in place, a frontier-quality native multimodal model is roughly a **6–12 month** effort end to end (research + data + training + post-training + eval). The single largest training run is **weeks**, but the data and ablation work consume most of the calendar.

---

## 5. Scenarios & stories

*Where this technique shines, and where it is the wrong tool.*

### Where it is the RIGHT tool

**The live interpreter booth that finally felt human.** A conference ran multilingual sessions on a classic pipeline (speech-to-text → translate → text-to-speech). Every interpreted voice came out flat and a half-beat late — rising pitch, a nervous pause, a laugh all died the moment audio became a transcript. A native speech-to-speech omni model hears the *audio itself* — prosody, emphasis, emotion — and generates translated speech carrying the same energy at sub-200ms-class response times. **Why native is right:** the value lives precisely in the information a transcript destroys, and latency is non-negotiable. *(sourced: brain.co, 2026; ai-media ISE 2026)*

**The accessibility tool that watches *and* listens.** An assistant for deaf and hard-of-hearing users must watch sign-language gestures, track surrounding speech, and reason about how gesture and speech *relate in time* — exactly the relationship a pipeline loses when each stream is processed in its own box. **Why native is right:** the answer depends on the *interaction* between modalities, not each independently.

**The art director's conversational editing session.** With Gemini Omni, a creative describes a scene, sees a clip, then says "same character, now make it dusk, have her glance left." The model keeps the character consistent because prior frames, spoken intent, and new instruction all live in one working memory; a stitched pipeline loses the thread. **Why native is right:** the workflow is a cross-modal conversation where state and consistency carry forward. (Real limit: clips capped at 10 seconds at launch — fine for social, not film.) *(sourced: venturebeat.com, 2026-05-19)*

**The support copilot that reads the screenshot, hears the frustration, and acts.** A customer pastes an error screenshot, records a voice note, and types a follow-up. One native model ingests all three together — no separate OCR, transcriber, or orchestration layer, fewer integration seams, one audit surface. **Why native is right:** input is heterogeneous and the cost of building/maintaining the pipeline outweighs the unified call (depends on volume/margins — see below).

### Where it is the WRONG tool

**The bank that needs to prove what was said.** Compliance requires a verbatim transcript of every interaction, the ability to block a response *before* it is spoken, and an audit trail. A native speech-to-speech model has no clean textual checkpoint in the middle. **Why native is wrong:** the textual intermediary native models eliminate is a *compliance feature*, not overhead. *(sourced: brain.co, 2026)*

**The medical scribe that can't afford a confident mistake.** Clinical transcription is life-safety critical; the team needs the best dedicated medical ASR, tuned and measured in isolation. Native omni models do not yet match dedicated ASR/TTS on raw accuracy, you cannot improve one component without retraining the whole model, and cross-modal reasoning remains a hallucination hotspot. **Why native is wrong:** when one modality must be near-perfect and certifiable, a swappable specialist beats a jack-of-all-trades.

**The workflow that's really one modality with tools.** An agent takes typed input, calls three APIs, hits a database, returns structured output — text-in, text-out work that *depends* on explicit text to drive symbolic actions, precisely where end-to-end multimodal models struggle at function calling. **Why native is wrong:** a strong text LLM with clean tool-calling is simpler, cheaper, more reliable.

**The consumer app that did the math.** Auto-generating alt-text for millions of images: a native omni model *can*, but long-context multimodal calls can run several dollars each, and the job (still image → one sentence) needs no fusion or real-time anything. A smaller single-purpose vision-language model, or a self-hosted open-weight model run in batch, is right. **Why native is wrong:** at high volume with simple per-item work, you pay a premium for capabilities you never use. *(sourced: wavespeed.ai, techsy.io, 2026)*

### The decision in one breath

Reach for a **native any-to-any model** when the *relationship between modalities* is the point — when tone, timing, visual-audio fusion, or conversational cross-modal context carries value a pipeline would discard, and when low latency or architectural simplicity matters. Reach for a **specialist pipeline** when you need auditability, best-in-class single-modality accuracy, reliable tool-calling, regulatory control, or low cost at scale. The trap: choosing the omni model because it is the most capable thing in the room. The most capable tool and the *right* tool coincide only when your problem actually lives in the seams between modalities.

---

## 6. Cross-industry usage & positioning (June 2026)

Separate two things vendors blur: **native input understanding** is now *mature and widespread*; **native any-to-any generation** (especially video) is the *cutting edge*, and many "any-to-any" products are actually a reasoning core that *calls* an image/video/voice tool behind the scenes. *(inference, based on architecture surveys)*

**The frontier:** **Gemini Omni** (announced 2026-05-19) is the current high-water mark — text/image/audio/video in, and **video out natively** inside the reasoning core. *(sourced: venturebeat.com, 2026-05-19)* **GPT-5.5** (2026-04-23) leads on agentic + unified *understanding*, but generation is not native any-to-any on the output side. *(sourced: teamday.ai, 2026; verifier, 2026)* Open frontier: **Emu3.5** (interleaved text+image), **Qwen3.5-Omni**, DeepSeek Janus, Show-o2, Molmo. *(sourced: arxiv.org/html/2510.26583v1, 2026)*

**Table-stakes vs cutting-edge, per industry:**

- **Coding / dev tools — table-stakes (input), cutting-edge (agentic loops).** Screenshot-to-UI-code is now a commodity (v0, Lovable, ScreenCoder); Claude Opus 4.x and Gemini 3 are the workhorses. Cutting-edge is *computer use* — the model watching a screen and acting. *(sourced: blog.brightcoding.dev, 2026; arxiv 2507.22827)*
- **Customer support — table-stakes.** Native speech-to-speech voice agents (sub-1s latency, emotion-aware) are the default for new deployments. Leaders: OpenAI Realtime, Amazon Nova Sonic, Google Gemini Live, xAI Grok Voice. *(sourced: inworld.ai, 2026)*
- **Healthcare — cutting-edge, mostly pre-clinical.** **Correction (sourced: verifier, 2026):** **Med-Gemini is the original 2024 model built on Gemini 1.0/1.5, NOT a Gemini 3 variant.** Its 91.1% MedQA score and the X-ray/pathology/genomics capabilities come from that 2024 work. The recurring finding: impressive research multimodal models "have yet to make their way to the clinic," gated by FDA regulation and validation. *(sourced: crescendo.ai, bipartisanpolicy.org, 2026; verifier, 2026)*
- **Robotics — cutting-edge, fastest-moving.** **Vision-Language-Action (VLA)** models output *physical action* as a modality. Leaders: Google (Gemini Robotics 1.5 VLA), Physical Intelligence (π0.7, 2026-04-16). The unlock is **cross-embodiment learning** — one model across many robot bodies beats body-specific models. *(sourced: hyscaler.com, 2026)*
- **Defense — table-stakes for fusion, cutting-edge for autonomy.** Multimodal *sensor fusion* (satellite + drone + ground + signals) is operational. Leaders: Palantir (Maven/AIP), Anduril (Lattice). These are integration platforms layered on multimodal models rather than single native cores. *(sourced: defensescoop.com; inference)*
- **Finance — table-stakes (document understanding).** Jointly reading text, tables, and figures in reports; multimodal RAG (MultiFinRAG, FinRAGBench-V) is the dominant pattern. *(sourced: arxiv FinMMDocR 2512.24903, 2026)*
- **Legal — table-stakes.** Per the ABA, 79% of legal professionals now use AI; tools do semantic clause understanding and review scanned filings as images. Leaders: Spellbook, Juro, Harvey-class. *(sourced: justee.ai, spellbook.com, 2026)*
- **Science — cutting-edge, domain-specialized.** Fusing heterogeneous scientific data: AlphaFold 3, ESM-3, Boltz-2, Chai-1 (biology); MultiMat (materials). Mostly domain models, not general omni. *(sourced: intuitionlabs.ai; arxiv MultiMat 2312.00111)*
- **Consumer — table-stakes.** Point the camera, talk, share a screen, get spoken answers — the default expectation. Leaders: Google (Gemini), OpenAI (ChatGPT), device-level Apple/Samsung. *(sourced: mygreatlearning.com, 2026)*

**Positioning (advisory):**

- If you are deploying: treat native multimodal *understanding* as table-stakes — assume users paste a screenshot, talk, and share a video in one turn. Treat native multimodal *generation* (especially video) as a 2026 differentiator, not a baseline.
- Buy vs. build: for understanding/RAG over mixed documents, frontier APIs are commoditized — buy. For robotics/embodied and regulated healthcare, the frontier moves monthly and regulation lags — pilot, do not bet production yet.
- Ask vendors one question: **"Is generation native to the same model, or a tool call?"** The answer predicts your latency, cost, and how gracefully the system reasons *across* modalities versus just *between* them.

---

## 7. Learning path for a technical leader (advisory)

*For someone who decides, funds, staffs, and reviews this work — not who trains the model.*

### Five core mental models

1. **Everything becomes tokens, then it's one sequence.** Every modality is converted to numbered chunks, poured into one stream, and a single transformer predicts the next chunk. This is *why* any-to-any is possible — the modalities were never really separate inside. The model is only as good as its **tokenizer**.
2. **Understanding and generating are different muscles forced into one body.** Understanding favors **autoregressive** (predict next token); image generation favors **diffusion** (denoise from noise). Three families: pure-AR, pure-diffusion, and **hybrid (AR backbone → diffusion decoder)** — the pragmatic mainstream.
3. **The "unification tax."** Sharing weights buys reasoning-in-generation and one-model-to-run, but unified models **still trail task-specialized generators on raw quality**, and joint training causes **modality interference** and forgetting. *(The single most important idea for a leader.)*
4. **Early fusion + Mixture-of-Experts is the 2026 consensus.** Apple's 457-model scaling study: early fusion matches late fusion and is more deployable at smaller sizes; internal MoE routing recovers per-modality specialization. *(sourced: arXiv 2504.07951, 2026)*
5. **These models scale like LLMs** — predictable compute→capability curves, so roadmaps are fundable and forecastable.

### Reading spine (a spine, not a library; ~6–8 hrs, skip every equation)

1. **Survey arXiv 2505.02567** (the map: taxonomy, tradeoffs, open problems) → 2. **Scaling Laws for Native Multimodal Models, arXiv 2504.07951** (the strategy doc) → 3. **A concrete shipping-example primer on native image generation** (the worked example) → 4. **Roadmap arXiv 2605.25343, May 2026** (the horizon) → 5. **One open model report — Qwen3-Omni or Emu3.5** (reality check) → 6. **One eval paper — UEval or Uni-MMMU** (what "good" is measured as).

### Understanding-checkpoints

Can you, unaided and in plain language: explain why tokenizing enables any-to-any and what caps quality (CP1); name the 3 families with a strength/weakness each (CP2); give two things unification *improves* and two it *worsens* (CP3); state the early-vs-late-fusion + MoE conclusion and why "scales like an LLM" matters to a budget (CP4); define interleaved generation and why it is still weak (CP5); and — the real test — say in two sentences when a **composite LLM-plus-image-tool** beats a native unified model for *your* product (CP6).

### How to evaluate an expert in an interview

The tell is always **specificity about tradeoffs and failures**, never fluency about capabilities.

- **Q1 "When would you NOT use a native unified model?"** — *Strong:* names cases where composite/tool-calling wins (best-in-class image quality, tight latency/cost) and raises the unification tax unprompted. *Red flag:* cannot name a scenario where the simpler approach wins.
- **Q2 "Walk me through 'a cat reading a book' → image; where does AR-vs-diffusion show up?"** — *Strong:* text tokens conditioning visual tokens/latents, then AR decode or a diffusion decoder rendering pixels; explains the hybrid. *Red flag:* confuses tokenizer with model, or thinks AR and diffusion are the same.
- **Q3 "What breaks training text+image+audio together?"** — *Strong:* modality interference, catastrophic forgetting, data-balance pain, mitigated by staged training and MoE. *Red flag:* claims joint training is free or strictly additive.
- **Q4 "Prove one is good, with money on the line."** — *Strong:* separates understanding/generation/interleaved evals, names real benchmarks (MMMU/Uni-MMMU, GenEval/ImgEdit-Bench, UEval), notes saturation at the frontier, insists on own-data evals. *Red flag:* leans on a demo or one aggregate score.
- **Q5 "June 2026 — what's SOTA and what's unsolved?"** — *Strong (current):* frontier is multimodal-by-default (Gemini Omni strongest any-to-any incl. native video out; GPT-5.5 unified *understanding* but not native any-to-any *output*; open: Qwen3.5-Omni, Emu3.5, Janus) AND honestly names open problems (weak interleaving, quality gap vs specialists, high serving cost, immature eval). *Red flag:* talks only about 2025-era models, claims generation is "solved," or claims GPT-5.5 natively emits audio/video — it does not.

**Best single signal:** strong experts **volunteer the failure modes before you ask.** Fluency about capabilities is free; fluency about limitations is earned.

### Leader's decision frame (advisory)

Native any-to-any earns its complexity only when modalities must *reason together* (conversational editing, reasoning-driven generation). If you just need "an LLM that can also make a picture," **composite (LLM + best-in-class tools)** is simpler, cheaper, higher per-modality quality, and easier to swap. And with frontier APIs and capable open models available, **almost no one should train one from scratch** — the leader's real questions are *which to adopt* and *how to evaluate on our own data*.

---

## 8. Team notes

*"Native any-to-any" means one model that takes any mix of text/image/audio/video in and emits more than one modality out, with fusion inside a single network — not separate models bolted together.*

The work splits cleanly into **"use a frontier any-to-any API"** vs. **"host/adapt an open any-to-any model."** These need very different teams.

### Roles & seniority (advisory)

**Default: for ~80% of teams, no new role is needed.** If you are calling Gemini Omni / GPT-5.x / Qwen via an API, an existing **senior application/product engineer** absorbs this. The skill is prompt-and-pipeline design plus eval, not model internals. Do not hire an "ML engineer" to call an API.

**When you genuinely need dedicated roles** (self-hosting open weights, fine-tuning on proprietary multimodal data, or latency/cost/privacy rules out the API):

| Role | Seniority | Why / when | Absorbable? |
|---|---|---|---|
| **Applied / multimodal ML engineer** | Senior (5+ yrs) | Owns fine-tuning, eval harness, modality bridging. The 2026 differentiator is the ability to *bridge modalities* — reason about where image vs. audio vs. text fail differently. *(sourced)* | No, if adapting models. A strong backend eng cannot fake this. |
| **Inference / serving engineer (GPU)** | Senior/Staff | Any-to-any models have *heterogeneous stages* (encode, prefill, decode, decode-to-image/audio) with wildly different resource profiles; concurrent cross-modal requests interfere. Disaggregated serving is the 2026 norm. *(sourced)* | Partially — a strong platform/SRE with GPU experience can grow into it. |
| **Eval / data engineer** | Mid–Senior | Multimodal eval is the actual bottleneck; datasets and graders, not the training algorithm, are where teams get stuck. *(sourced)* | Often yes — and **this is the highest-leverage hire** if you can make only one. |

**Rule of thumb (advisory):** API-only → 0 new roles. Self-host one open model → 1 senior applied ML eng + lean on platform team for serving. Fine-tune at scale / real-time voice → add a dedicated GPU serving engineer.

### Hiring signals (advisory)

**Green flags:** has shipped something where **modalities cross** (audio-in/text-out grounding, reasoning-driven image edits), not "I used a vision API once"; talks about **evaluation before training**; treats fine-tuning and RAG as baseline, not a headline; for serving roles, speaks fluently about why a 2-second multimodal request costs orders of magnitude more than a text request. *(sourced)*

**Red flags:** "I'll fine-tune a foundation model from scratch" (poor cost instinct); reaches for self-hosting before trying the API (correct ladder: managed API → managed fine-tuning → full custom training, and most should stop at rung one or two); cannot distinguish understanding hallucination from generation artifacts; quotes only single-modality benchmarks; *wants to hire ML talent to do API integration work* (a budget red flag at the **manager** level). *(sourced)*

### Build vs. buy (advisory)

**Default: rent/buy. Owning the model is rarely a moat.**

| Option | When it wins | Cost/risk reality |
|---|---|---|
| **Buy (frontier API)** — Gemini Omni, GPT-5.x | Default. Capability today, no GPU ops, edge is the *product*. | Per-token + per-image/audio pricing; lock-in; data-residency limits. |
| **Rent + fine-tune (managed)** | Proprietary multimodal data the base model handles poorly. | Managed SFT/DPO/RFT is the right *next* step. No GPU ops. |
| **Build (self-host open weights)** — Qwen3-Omni (Apache 2.0) | Only when (a) regulation forbids the API, (b) you have proprietary data no competitor can replicate, **and** (c) volume is high enough that API cost exceeds fully-loaded GPU + team cost. | You inherit disaggregated GPU serving and cross-modal interference. Most teams underestimate this cost 5–10x. *(inference)* |

**Licensing note (sourced/contested):** Qwen3-Omni shipped Apache 2.0, but reporting indicates the *3.5* generation went proprietary — verify the license of the *specific* checkpoint before building, because open-vs-closed status changes between releases.

### Common failure modes

**Technical (sourced):** **object hallucination** (reports objects not in the image, driven by language priors); **audio hallucination** (answers "piano" when there is none — easy to miss because text output *sounds* confident); **cross-modal spurious correlation** (leans on text priors, ignores what image/audio shows); **grounding trade-offs** (fixes like "zoom and re-look" introduce *new* failures — no free lunch).

**Organizational (advisory):** skipping the eval harness (you ship hallucinations you cannot see); treating it as a text problem with pictures (each modality fails differently); self-hosting too early; hiring the wrong shape of person (researchers for integration work, or generalists for genuine GPU-serving depth).

### Bottom line (advisory)

Buy the API by default; the model is not your moat. Hire zero new roles for API work, one senior applied-ML engineer + an eval-focused data engineer if you fine-tune, and a GPU serving specialist only if you self-host or run real-time voice. Screen for people who reason across modalities and build evaluation before training. The signature failure of this technique is **confident hallucination across modalities** — budget for catching it.

---

## Bottom line

Native any-to-any multimodal models work by **forcing every modality into one shared token language and predicting the next token over all of it**, then patching in **diffusion** to make generated pixels/audio/video high-fidelity. They win because **one shared internal space lets the model reason across modalities with no lossy handoffs** — the fatal flaw of the glue-specialists-together pipeline. The mid-2026 frontier is **hybrid autoregressive+diffusion**, precisely because the clean single-objective version still cannot be simultaneously best at *understanding* and *generating*. And the year's most important distinction for a buyer: native *understanding* is everywhere, but native any-to-any *generation* is a minority — Gemini Omni generates video natively, while GPT-5.5, despite unifying input, still routes generation out. Ask every vendor: *is generation native to the same model, or a tool call?*

---

## Sources

- [Toward Native Multimodal Modeling: A Roadmap (arXiv, 2026)](https://arxiv.org/html/2605.25343v1)
- [Native Multimodal Models (NMMs) — EmergentMind (2026)](https://www.emergentmind.com/topics/native-multimodal-models-nmms)
- [Emu3.5: Native Multimodal Models are World Learners (arXiv, 2026)](https://arxiv.org/html/2510.26583v1)
- [Unified Multimodal Understanding and Generation Models: Survey (arXiv, 2026)](https://arxiv.org/html/2505.02567v5)
- [Scaling Laws for Native Multimodal Models (arXiv, 2026)](https://arxiv.org/abs/2504.07951)
- [Best Multimodal AI Models in 2026 — SiliconFlow](https://www.siliconflow.com/articles/en/best-multimodal-ai-models)
- [GPT-5.5: OpenAI's Unified Multimodal Model — TeamDay (2026, promotional)](https://www.teamday.ai/blog/gpt-5-5-launch)
- [Google Unveils Gemini Omni — VentureBeat (2026-05-19)](https://venturebeat.com/technology/google-unveils-gemini-omni-any-to-any-ai-model-what-enterprises-should-know)
- [Gemini Omni — Orbilon Tech (2026)](https://orbilontech.com/gemini-omni/)
- [What Is Gemini Omni? — Great Learning (2026)](https://www.mygreatlearning.com/blog/what-is-gemini-omni-googles-unified-ai-model-for-video-image-audio-and-text/)
- [Multimodal learning with next-token prediction (Nature / PMC, 2025–26)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12893917/)
- [Kelix: Closing the Understanding Gap of Discrete Tokens (arXiv, 2026)](https://arxiv.org/html/2602.09843v1)
- [Generation Enhances Understanding in Unified Multimodal Models (arXiv, 2026)](https://arxiv.org/html/2601.21406v1)
- [UEval: Benchmark for Unified Multimodal Generation (arXiv, 2026)](https://arxiv.org/pdf/2601.22155)
- [Quantifying the Gap between Understanding and Generation (arXiv, 2026)](https://arxiv.org/pdf/2602.02140)
- [UniGRPO: Unified Policy Optimization for Visual Generation (arXiv, 2026)](https://arxiv.org/pdf/2603.23500)
- [vLLM-Omni: Disaggregated Serving for Any-to-Any Multimodal Models (arXiv, 2026)](https://arxiv.org/pdf/2602.02204)
- [Qwen3.5-Omni Technical Report (arXiv, 2026)](https://arxiv.org/abs/2604.15804)
- [Qwen3-Omni (Apache 2.0, open) — GitHub (2025)](https://github.com/QwenLM/Qwen3-Omni)
- [Chained vs Speech-to-Speech Voice Architectures — Brain.co (2026)](https://brain.co/blog/chained-voice-agent-architectures-speech-to-speech-vs-chained-pipeline-vs-hybrid-approaches)
- [Survey of Hallucinations in Multimodal Models — Galileo (2025)](https://galileo.ai/blog/survey-of-hallucinations-in-multimodal-models)
- [Adaptive Visual Grounding for Hallucination Mitigation (arXiv, 2026)](https://arxiv.org/html/2604.24396)
- [The Fine-Tuning Bottleneck Isn't the Algorithm — Fireworks (2026)](https://fireworks.ai/blog/fine-tuning-bottlenecks)
- [AI in Healthcare News (Med-Gemini context) — Crescendo (2026)](https://www.crescendo.ai/news/ai-in-healthcare-news)
- [Vision-Language-Action (VLA) Guide — HyScaler (2026)](https://hyscaler.com/insights/vision-language-action-vla-guide/)
- [Palantir-Anduril AI Consortium — DefenseScoop](https://defensescoop.com/2024/12/06/palantir-anduril-consortium-ai-new-alliance-merge-capabilities/)
- [AI Legal Document Review — Justee (2026)](https://justee.ai/blog/ai-legal-document-review)
- [Biology Foundation Models Comparison — IntuitionLabs](https://intuitionlabs.ai/articles/biology-foundation-models-comparison)
- [Screenshot-to-Code — BrightCoding (2026)](https://www.blog.brightcoding.dev/2026/06/02/stop-hand-coding-uis-from-screenshots-screenshot-to-code-does-it-instantly)
