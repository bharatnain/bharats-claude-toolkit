# On-Device / Edge LLM Inference

*A chapter for a technical leader. State of the art as of June 2026. Plain language, real depth.*

Factual claims are labeled **sourced** (with a URL + access date in the Sources list), **inference** (a reasonable conclusion drawn from sourced facts), or **speculation** (informed guess, thin sourcing). Learning-design and organizational recommendations are labeled **advisory**.

---

## 1. What it is

**On-device (or "edge") LLM inference means running a large language model directly on the hardware in your hand or in front of you — phone, laptop, car, smart speaker, robot, factory sensor — instead of sending your words over the internet to a data center.**

When you use a cloud chatbot, your text travels to a warehouse of GPUs, gets processed there, and the answer travels back. On-device inference does the whole thing locally: the model's weights live in the device's own memory, the device's own chips do the thinking, and nothing leaves the device.

By mid-2026 this is no longer a research curiosity. It ships as a built-in system service in mainstream products: **Apple Intelligence on iOS, Gemini Nano on Android, and Phi models inside Windows Copilot** all run language models locally [sourced]. A modern flagship phone runs a 3-billion-parameter model at roughly **30 tokens per second** — about as fast as you read [sourced; Apple's own 2025 tech report puts its 3B on-device model near ~30 tok/s].

There are exactly four reasons to want this, and each one implies a different definition of success [sourced]:

- **Latency** — no network round trip. Local first-token response is on the order of tens of milliseconds, versus the cloud's added ~20–80 ms of network overhead before generation even begins.
- **Privacy** — your data never leaves the device. This is a *capability*, not a mere feature: it lets you process data you may be legally forbidden to send to a server.
- **Cost** — the compute is paid for by the user's own hardware and battery, not the provider's cloud bill. The cost no longer grows with your user count.
- **Availability** — it works on a plane, in a tunnel, on a factory floor with no signal.

The price you pay for all four is a single currency: **capability**. The model has to fit in a few gigabytes of memory inside a tiny power-and-heat budget, so it is smaller — and therefore, on the hardest problems, less capable — than the frontier model in the cloud. Every good decision about this technique is ultimately a judgment about whether the smaller, private, instant model is *good enough* for the specific job [inference].

---

## 2. How it works — mechanism and intuition

To understand the engineering, you need one core fact that drives *everything* else.

### The binding constraint: memory bandwidth, not compute

A language model generates text one word-piece ("token") at a time. **To produce each single token, the chip must read the entire set of model weights out of memory.** A 3-billion-parameter model stored at 4 bits each is about 1.5 GB of numbers — and all 1.5 GB must be streamed through the processor for *every token*.

Here is the surprise: the arithmetic itself is cheap. The bottleneck is **moving the weights from memory into the compute units.** A phone's memory delivers data at roughly **50–90 GB/s** (the Snapdragon 8 Elite Gen 5 measures 84.8 GB/s); a data-center GPU moves **2–3 TB/s** — a **30–50× gap** [sourced]. So during generation, the phone's powerful neural processor mostly sits idle, *waiting for memory*. The field's term for this is **memory-bandwidth bound**.

> **Intuition:** Picture a chef who can chop instantly but must walk to a distant pantry to fetch each ingredient. Buying a faster knife (more compute, more "TOPS") doesn't help — the chef is already waiting. You win two ways: (a) shrink each ingredient so every trip carries less weight, and (b) cook several dishes per pantry trip. Every major edge technique is one of those two moves.

There's a twist worth holding onto: the *first* phase — reading in the user's prompt, called **prefill** — is compute-bound and parallel, so it's fast. The *generation* phase — writing the answer, called **decode** — is memory-bound and sequential, so it's slow. A 2-second reply might be 0.3 s reading your question and 1.7 s writing the answer [inference]. This split explains nearly every optimization below.

The headline insight of 2026, in one line: *the field didn't turn phones into GPUs; it learned to treat memory bandwidth, not compute, as the binding constraint* [sourced].

### Move 1 — Shrink the weights (quantization)

Models are trained using 16-bit numbers but **deployed at 4 bits**, cutting memory traffic roughly 4× with little quality loss. This is the universal baseline; 4-bit is the production standard, shrinking a model to ~27% of its full size while losing only ~1–3 points of accuracy [sourced]. Methods like **GPTQ** and **AWQ** do this "post-training" — they compress an already-trained model intelligently, protecting the few numbers that matter most. **SpinQuant** rotates the data so it compresses more cleanly, losing under 3% accuracy at 4 bits [sourced].

The frontier goes much lower. **BitNet** models use **ternary weights** — every weight is just −1, 0, or +1 (~1.58 bits) [sourced]. At that point a "multiply" becomes a "keep / drop / flip sign," which barely touches the chip. Microsoft's open **BitNet b1.58 2B** fits in about **400 MB** [sourced]. The catch: below ~2 bits a model has to be *trained that way from scratch* — you cannot squeeze a normal model down that far afterward, because below 2 bits models learn fundamentally different internal representations [sourced].

### Move 2 — Generate more than one token per memory trip (speculative decoding)

Since reading the weights is the expensive part, doing extra work *per read* is nearly free. **Speculative decoding** exploits this: a tiny, fast "draft" model guesses the next several tokens, then the real model verifies all of them **in a single pass**. Correct guesses are kept; wrong ones are discarded. Output quality is identical to running the big model alone — verification preserves correctness — and the result is **2–3.6× faster** [sourced]. (Named variants: Medusa, EAGLE.) Deep version: this attacks the *sequential* nature of decode, the one thing quantization can't touch.

### Make the multiplications disappear (table lookup)

A clever trick for very-low-bit models: **T-MAC** replaces multiplication with **bit-wise table lookups** [sourced]. When weights take only a few possible values, you can pre-compute every possible result and simply *look it up* instead of calculating. On a Snapdragon X Elite laptop this hit **48 tokens/sec on a 3B BitNet model — 4–5× faster than llama.cpp, using only a quarter to a sixth of the CPU cores** [sourced]. The 2026 successors (T-MAN, Vec-LUT) push this onto phone **NPUs** (neural processing units) [sourced].

### Tame the KV cache (the hidden memory hog)

As a conversation grows, the model keeps a running memory of everything said so far — the **KV cache** (key-value cache). It grows *linearly with length*, and for long documents it **can become larger than the model's own weights** [sourced]. So edge systems compress it (down to ~3 bits) or keep only the important parts. **StreamingLLM** keeps "attention sinks" — the first few tokens — to allow effectively unbounded conversation length [sourced]. The leadership trap here: approving "give it a 128K context window" without realizing you just blew the device's memory budget.

### Put it together: the assembly line

1. **Pick a small, smart model** (sub-1B to ~8B parameters) — below ~1B, deep-and-thin networks beat wide-and-shallow ones [sourced].
2. **Quantize** to 4-bit (or ternary, if trained for it).
3. **Run it** through a runtime tuned to the device: **ExecuTorch** (Meta — reached 1.0 GA on 22 October 2025, ~50 KB footprint, 12+ hardware backends, runs the majority of popular HuggingFace edge LLMs out of the box [sourced]), **llama.cpp** (CPU, GGUF format), or **MLX** (Apple Silicon).
4. **Accelerate generation** with speculative decoding plus KV-cache compression, dispatching the heavy parts to the NPU.

### One catch the spec sheets hide: heat

A phone cannot sustain peak speed. **Thermal limits, not peak compute, are often the real ceiling.** Under sustained load an **iPhone 16 Pro was measured losing nearly half its throughput within two generation iterations** as it heated up; a **Galaxy S24 Ultra hit an OS-enforced GPU frequency floor that terminated inference outright** [sourced]. Dedicated low-power NPUs trade peak speed for stability — a Hailo-10H holds ~6.9 tok/s at ~2.1 W with near-zero variance [sourced]. Edge models are tuned for *sustained* performance, not benchmark sprints.

---

## 3. Why it works — the principle, and why the naive approach fails

**The principle:** Edge inference works because the workload is bottlenecked on **memory movement**, and the two cheap levers — *smaller weights* and *more output per memory read* — attack exactly that bottleneck without exotic hardware. A weak processor is fine as long as you stop making it wait.

**Why the naive alternatives fail:**

- **"Just shrink the cloud model and run it as-is."** Fails on two fronts. A full-precision frontier model is tens of gigabytes — it won't fit in the **under ~4 GB of RAM** actually free on a flagship phone after the OS takes its share [sourced]. And even if it fit, streaming all those 16-bit weights per token at 50–90 GB/s would be painfully slow.
- **"Just wait for faster chips."** Misdiagnoses the problem. More TOPS buys you compute you can't use, because the chip is starved for *data*, not cycles. This is why the 2026 breakthroughs came not from faster silicon but from rethinking how models are built, trained, compressed, and deployed [sourced].
- **"Just quantize harder, all the way to 1-bit, after training."** Fails because aggressive low-bit compression of an already-trained model wrecks it — below ~2 bits the network needs a fundamentally different internal representation, achievable only by **training in that regime from the start** [sourced].
- **"Just send it to the cloud."** That *is* the alternative on-device aims to escape — and it loses on privacy, offline use, per-query cost, and the unavoidable network round trip [sourced].

The deep reason edge LLMs took off in 2026 is that **small models got dramatically smarter.** Reasoning distilled from frontier models (e.g. DeepSeek-R1) means **Qwen3-4B now rivals the older Qwen2.5-72B**, and a Mixture-of-Experts model like **Qwen3-30B-A3B beats QwQ-32B while activating roughly 10× fewer parameters per token** [sourced]. Mixture-of-Experts (MoE) is itself a bandwidth trick: a big model where only a small slice runs per token, giving a big model's knowledge at a small model's *compute* cost.

A non-obvious result worth knowing because it signals real depth: for a *fixed memory budget*, a **bigger model squeezed to 2 bits often beats a smaller model at 4 bits** (the ParetoQ finding) [sourced] — provided that sub-2-bit model was natively trained low-bit, and provided you remember to budget for the KV cache too.

---

## 4. People & resources

Two very different activities live under this banner. Don't conflate them.

### A) Deploying an existing open model to a device (most teams)

This is an **engineering-integration job, not an AI-training job.**

- **Team:** a handful of engineers — **~1–5 people** [inference]. A mobile/embedded engineer, an ML-systems/optimization engineer (quantization + runtime), and a product/QA owner. The hard skill is the runtime and hardware backend (ExecuTorch / llama.cpp / Core ML), not model science.
- **Compute:** a workstation or a few cloud GPU-hours for quantizing and benchmarking — **hundreds to low thousands of dollars** [inference].
- **Time:** weeks to a few months to ship a polished feature [inference].
- **Hardware target (2026 reality):** mobile NPUs of **~35–60 TOPS** — Apple A19 Pro ~35, Snapdragon 8 Elite Gen 5 ~60, MediaTek Dimensity 9400+ ~50 — paired with **12 GB+ LPDDR5X** and that crucial **50–90 GB/s** bandwidth ceiling [sourced].
- **Data scale:** roughly **zero**. You're reusing someone else's trained weights.

### B) Training a custom small / edge model from scratch (few teams)

- **Team:** a small research-plus-infra group, **~5–20 people** [inference]: data engineers, pre-training researchers, an evaluation lead, infra/MLOps.
- **Compute and money (orders of magnitude, 2026 prices):**
  - A **~7B model** from scratch: **~$50K–$200K** [sourced].
  - A **~20B model:** **~$500K–$2M** [sourced].
  - GPU rental runs **~$2–4/hr**; training costs fell roughly 45% in the past year as H200/B200 chips and better algorithms landed [sourced].
  - **Fine-tuning** (adapting an existing model rather than training fresh) is radically cheaper — a LoRA run finished in **~7 hours on a single 16 GB T4 GPU** (Colab-tier hardware) [sourced].
  - Memory-efficient pre-training has come a long way, but the exact figure matters: **APOLLO, combined with quantization, can pre-train a LLaMA-7B-class model in under 12 GB of GPU memory; plain GaLore does it in ~24 GB (a single RTX 4090), and Q-GaLore (quantized GaLore) in ~16 GB** [sourced]. *(Corrected from an earlier draft that wrongly attributed the sub-12 GB figure to GaLore.)*
- **Time:** weeks to a few months of training plus iteration [inference].
- **Data scale:** pre-training a strong small model consumes on the order of **trillions of tokens** of text — terabytes of curated data [inference, based on published recipes like SmolLM/Qwen]. Fine-tuning needs only thousands to millions of examples [inference].

### Bottom line on resources [advisory]

If your goal is to *ship* an on-device LLM feature, treat it as a **hardware-integration and optimization problem for a small engineering team**, not a multimillion-dollar training program. The expensive path (B) is warranted only when no open model fits your size, language, or domain — and even then, **fine-tuning an existing small model is almost always the right first move** before training from scratch. Budget your real effort for the runtime, the quantization, and the **thermal / sustained-performance testing on actual target devices**, which is where on-device projects most often stumble.

---

## 5. Scenarios and stories

### The one tradeoff behind everything

Running the model locally buys privacy, latency, offline operation, and zero per-query cost — and you pay for all of it in **capability**. As of mid-2026 the "good enough" line has moved a long way: a 3–4B model now does things that needed a 70B model two years ago. But the line is still real, and the mature move is to stop asking "edge *or* cloud?" and start asking "*which queries* go where?"

### Where the field actually stands (June 2026) — an honest snapshot

- **The small models got genuinely good.** Microsoft's **Phi-4-reasoning (14B)** is *comparable to the full 671B DeepSeek-R1 on AIME 2025 math and beats the R1-Distill-70B models*; the "beats models ~50× its size" framing is true specifically on olympiad-math benchmarks, not on broad capability — a 14B model does not out-think a 671B model in general [sourced, with that scope correction]. **Qwen3-4B** rivals the older Qwen2.5-72B; Google's **Gemma 4 E4B** (shipped 2 April 2026) hits ~69.4% on MMLU-Pro and runs in about 5 GB of RAM at 4-bit, with a 128K context window and native audio input [sourced].
- **The phones can run small models at usable speed — but read the model size.** Benchmarks of ~136 tok/s on an iPhone 17 Pro and ~91 tok/s on a Galaxy S25 Ultra are for a **~450M-parameter model (LFM2-VL-450m) at INT8** — *not* the 3–4B models the narrative is usually about. A 3B-class model runs closer to **~30 tok/s** on the same phones [sourced, with that size correction]. Both numbers are "faster than you read"; only one of them is the good small model.
- **Apple ships a 3B on-device model** to recent devices and lets any app call it in a few lines of Swift via the Foundation Models framework; it uses 2-bit quantization-aware training and KV-cache sharing to fit [sourced].
- **The laptop/PC tier got big.** Qualcomm's Snapdragon X2 Elite Extreme ships with up to **128 GB of on-package memory** — enough to hold a 70B-class model locally on a Windows-on-Arm laptop [sourced].
- **Heat, not raw compute, is the real ceiling on phones** (see Section 2's throttling findings) [sourced].
- **The winning architecture is hybrid.** In production, teams keep the easy majority of queries on-device and escalate the hard minority to the cloud. The commonly cited fraction is **~60–80% local** for general assistant traffic, though some narrow consumer workloads run as high as ~95% local — the exact number depends entirely on the task mix, so treat it as a directional pattern, not a measured universal constant [inference; the underlying routing pattern is sourced].

### Part 1 — Where it's the RIGHT tool

**Story 1 — The hospital scribe that never phones home.** A regional hospital auto-drafts clinical notes from the exam-room conversation. The data is protected health information; a cloud API means business-associate agreements, audit trails, and a permanent worry about where transcripts live. They run a small speech model plus a 3–4B summarizer *entirely on the exam-room tablet*. Compliance isn't bolted on — it's a property of the architecture, because there is no data to leak. **Why it fits:** the task is narrow, privacy stakes are high, and clinician-edited drafting is acceptable. [sourced for viability; advisory for the design recommendation]

**Story 2 — The car that must think with no signal.** A driver-assistance assistant has to answer "roll down the rear window and set the cabin to 20 degrees" inside a tunnel or a parking garage. A cloud round trip is not just slow — sometimes it is *impossible*. A small model on the car's compute handles the bounded vocabulary instantly and offline. **Why it fits:** offline is non-negotiable and the command space is small. **Subtlety:** automotive teams favor dedicated NPUs over phone-style GPUs precisely because they hold throughput steady instead of throttling. [inference, grounded in the thermal findings]

**Story 3 — The "instant" features inside an app.** Tap-to-summarize, smart replies, "rewrite this more formally" — on a phone via Apple's Foundation Models framework (or an Android equivalent) these run on the built-in 3B model: no API key, no per-call cost, no spinner, and they keep working in airplane mode. **Why it fits:** high-volume, low-stakes, latency-sensitive features where a local response feels magical and the cost never grows with your user count. [sourced for capability; advisory for the product framing]

**Story 4 — The cheap front-door of a hybrid system.** A support product gets millions of queries. Most are routine ("where's my order," "reset my password"). A small model handles those directly and escalates only the genuinely hard ones to a frontier cloud model. **Why it fits:** this is the dominant 2026 architecture — edge for what it's good at (volume, speed, cost), cloud for what it's needed for (the long tail). The key engineering piece is the router: a confidence/complexity classifier that decides what stays local. [sourced]

**Story 5 — The field technician with no connectivity.** A wind-turbine or oil-rig technician queries dense equipment manuals on-site, in places with no reliable internet. A small model with the manuals loaded locally answers offline. The broader point: on-device AI is the *only* AI for the roughly **2.2 billion people** still offline as of 2025 (ITU Facts & Figures 2025; the older 2.6 billion figure was the 2023 number) [sourced, corrected]. **Why it fits:** offline is the whole game, and document-grounded Q&A suits a small model well.

**Story 6 — Privacy-sensitive personal memory.** A personal assistant that remembers "my daughter's allergy is peanuts" and "I prefer aisle seats" is most useful when it holds an intimate, long-running profile. Keeping that memory and the reasoning over it on-device means the most sensitive picture of a person's life never becomes someone else's database. **Why it fits:** the value scales with how personal the data is — and personal data is exactly what you don't want to ship. [sourced for the ecosystem direction; advisory for the design choice]

### Part 2 — Where it's the WRONG tool

**Story 7 — A frontier-reasoning task dressed up as a small one.** A legal-tech startup wants on-device contract analysis "for privacy." But the task is multi-step reasoning over 80-page documents with cross-references and high cost of error. A 3–4B model will produce fluent, confident, *wrong* analysis on the hard clauses. The honest move is a covered cloud endpoint (under a business-associate or equivalent agreement) or on-prem large-model hardware. **Why it's wrong:** the capability gap is exactly where the liability lives. There's no such thing as a "HIPAA-compliant model," only compliant *deployments* — so you can get privacy from a properly-wrapped server too, and you should, when the task needs a bigger brain. [sourced]

**Story 8 — Long, multi-turn conversations with deep world knowledge.** An open-ended research companion that holds an hour-long conversation drawing on broad knowledge. Small models have shallower world knowledge and degrade as turns accumulate. **Why it's wrong:** broad knowledge and long-horizon coherence are precisely where parameter count still buys real capability that quantization can't conjure back. The 2026 consensus is explicit: for frontier reasoning, broad knowledge, or long multi-turn depth, cloud still wins. [sourced]

**Story 9 — The "always-on, full-tilt" misjudgment.** A real-time video-understanding feature runs a model continuously on a phone GPU. It demos beautifully for 30 seconds — then the phone heats up and throughput collapses by half, or the OS kills the GPU job. **Why it's wrong:** they budgeted for *peak* compute; the real constraint is *sustained thermal* headroom. Rethink the duty cycle (short bursts), move to a dedicated low-power NPU, or offload. **The trap:** benchmarks quote peak tokens/sec; production lives on the throttled floor. [sourced]

**Story 10 — Using "private" to justify a model that's just worse.** A bank wants on-device fraud-explanation text "because it's private." But the bank's data already lives in its own controlled cloud, and the task needs accuracy the small model can't hit. Edge bought nothing and cost capability. **The discipline:** name the *specific* benefit you're buying from edge, and check you don't already have it more cheaply elsewhere. [advisory]

**Story 11 — Ignoring the fleet-management tax.** A team ships on a 4-bit model and treats it as "set and forget." Then the model needs updating, different phones have wildly different NPUs, and the same feature is fast on one device and unusable on another. **Why it's underestimated:** on-device means you inherit the *entire* heterogeneity and update-distribution problem of the world's hardware. For a small team without the appetite to test across a device matrix, a single cloud endpoint is operationally simpler — and that simplicity is a legitimate reason *not* to go edge. [advisory]

### How to decide [advisory]

Walk these in order; the first "no" usually settles it:

1. **Must it work offline, or must the data never leave?** If yes, edge is strongly indicated — now justify the capability.
2. **Is the task narrow and well-bounded?** (Summarize a known genre, classify, fixed command set, document-grounded Q&A.) Small models shine on narrow tasks and fail on open-ended ones.
3. **What's the cost of a confident wrong answer?** High stakes + hard reasoning → cloud or large on-prem, even if you'd love edge.
4. **Is the load bursty or continuous?** Bursty fits phones; continuous heavy load needs a real NPU or the cloud, because of heat.
5. **Default to hybrid.** Build the router; let it move the line for you as models improve.

The recurring failure across every wrong-tool story is identical: someone picked edge for *one* real benefit (privacy, latency, cost) and quietly assumed the capability would be there. It often is now — which is exactly why it's so easy to assume it when it isn't.

---

## 6. Cross-industry usage and positioning (June 2026)

**Quick read of the whole landscape:** on-device LLM is **table-stakes** in consumer phones/PCs and developer tooling; **production-but-differentiating** in healthcare, customer support, and robotics; and **cutting-edge / partly aspirational** in finance, legal, defense, and science, where the model must be genuinely good and the cost of being wrong is high.

### The reference models (4-bit quantized, the de-facto standard)

| Model | Size | On a phone (3–4B class) | What it's for |
|---|---|---|---|
| **Gemma 4 E4B** (Google, shipped Apr 2 2026) | ~4B effective | ~5 GB RAM at 4-bit, 128K context, native audio | Current SOTA all-around edge model |
| **Phi-4-Mini / Phi-4-reasoning** (Microsoft) | 3.8B / 14B | reasoning-heavy tasks | Best per-parameter reasoning |
| **Qwen3-4B** (Alibaba) | 3–4B | best knowledge-per-parameter; rivals Qwen2.5-72B | Knowledge & reasoning |
| **Gemma 4 small tier** | ~1B | fast, lightweight phone tasks | Speed-first features |

*(sourced; the table is corrected to Gemma 4 — the prior Gemma 3 listing was one generation stale and inconsistent with the rest of this chapter. Note that a 3B-class model runs ~30 tok/s on current flagships, not the ~136 tok/s sometimes quoted for sub-500M models.)*

**The hardware floor has risen sharply.** Mobile NPUs now hit ~35 TOPS (Apple A19 Pro), ~50 TOPS (MediaTek Dimensity 9400+), ~60 TOPS (Snapdragon 8 Elite Gen 5). On Windows, Microsoft's "Copilot+" label *requires* a 40+ TOPS NPU plus 16 GB RAM. For robotics, NVIDIA's Jetson Thor delivers a data-center-class brain inside a robot [sourced].

**The techniques that make it work** are the ones from Section 2: 4-bit quantization as the standard; native ternary (BitNet) as the radical frontier (a 2B model in ~400 MB); speculative decoding for 2–3.6× speedups; KV-cache tricks (paged cache, attention sinks, 3-bit cache) for 64K–128K contexts; and on-device MoE (Apple's AFM-class models activate only a slice of parameters per prompt) [sourced]. **The dominant deployment pattern is hybrid, not pure-local** — most queries run on-device, the rare hard ones escalate to the cloud; "on-device vs. cloud" is a routing decision, not a religion [sourced].

### Who leads

- **Meta** leads *deployment scale* — ExecuTorch (1.0 in Oct 2025, ~50 KB footprint, 12+ backends) puts on-device models in front of billions across WhatsApp/Instagram/Messenger [sourced].
- **Google** leads *model efficiency* (Gemma 4 family) and the Android stack (Gemini Nano, AI Edge SDK) [sourced].
- **Microsoft** leads *per-parameter quality* (Phi-4 on filtered synthetic data) and *the AI-PC platform* (Copilot+) [sourced].
- **Apple** leads *silicon-specific optimization* — MLX runs 30–50% faster than llama.cpp on Apple Silicon — and the most polished consumer on-device/cloud hybrid [sourced].
- **Alibaba (Qwen)** and **Hugging Face (SmolLM)** drive the *open-source* frontier everyone else builds on [sourced].
- **NVIDIA** owns *edge robotics* (Jetson Thor + TensorRT Edge-LLM + Isaac) [sourced].

### Sector by sector

- **Consumer (phones, PCs, wearables) — TABLE-STAKES.** Galaxy AI on 400M+ devices; Copilot+ NPUs a baseline Windows requirement; Apple ships on-device models to every recent iPhone. Summarize, rewrite, translate, transcribe, smart-reply all run locally and are expected, not impressive. The frontier has moved to *speed* and *personal context*. [sourced]
- **Coding / dev tools — TABLE-STAKES (for the privacy-conscious).** Running a capable coding model locally is routine. **Qwen2.5-Coder-32B scores ~92.7% on HumanEval and is competitive with GPT-4o** (it does not clearly edge GPT-4o overall; GPT-4o still leads on reasoning-heavy code tasks) [sourced, corrected]. Tooling (Ollama, llama.cpp, Continue.dev) is mature and offline. The driver is data privacy plus cost. **Leaders: Alibaba (Qwen), the open-source/Ollama ecosystem.**
- **Healthcare — PRODUCTION, AND THE STRONGEST "WHY".** On-device's core advantage — data never traverses a network — becomes a *compliance superpower*: HIPAA's Security Rule is satisfied almost by construction when PHI never leaves the device. Browser-based stacks (WebLLM, WebGPU) now run quantized models *inside a hospital's Chrome tab*, and edge-enabled scanners flag findings at the point of care. The dividing line is regulatory: general AI software vs. certified Software-as-a-Medical-Device. [sourced; the regulatory framing is advisory]
- **Customer support — PRODUCTION, HYBRID-DOMINANT.** A 7B model serves the routine bulk locally at ~10–30× lower cost than a 70B+ cloud model, escalating the hard tail; enterprises report large AI cost cuts this way. Table-stakes is the routing architecture; differentiation is how cleanly you hand off without the user noticing. [sourced]
- **Finance — CUTTING-EDGE / EMERGING.** Strong *pull* (confidential positions, low latency) but a *high bar* — accuracy leaders are still frontier cloud models (**Claude Fable 5** was first past 90% on the AIMultiple finance benchmark, at 90.34% — a real model) [sourced]. The 2026 reality is hybrid: on-device/on-prem SLMs for routine document and compliance work, cloud for analysis that must be right. The "high bar" judgment is [inference].
- **Legal — CUTTING-EDGE / EMERGING.** Same shape as finance. Privilege and confidentiality make "the document never leaves our network" attractive, but legal work punishes hallucination harshly, so adoption skews toward local models for triage, search, and redaction with cloud (or governed on-prem large models) for drafting. [inference, grounded in the sensitive-data sourcing]
- **Robotics — PRODUCTION & ADVANCING FAST.** Here on-device is *physically mandatory*: a robot reaching for an object cannot tolerate a 200–500 ms cloud round trip. 2026's enabler is NVIDIA Jetson Thor running Vision-Language-Action models (e.g. Isaac GR00T) directly on the machine. **Leader: NVIDIA.** [sourced]
- **Defense — CUTTING-EDGE, OVERLAPPING ROBOTICS.** The requirements line up almost perfectly with edge inference: no connectivity in contested environments, latency independent of any network, data that must not leave the platform. The technology base is shared with robotics. Open sources are sparse — treat concrete capability claims as [speculation], but the *fit* is real and the dual-use platforms ship. [inference from adjacent sourced material]
- **Science — CUTTING-EDGE / NICHE.** Edge inference appears where instruments generate too much data to ship, or sit somewhere disconnected (field sensors, remote monitoring) — e.g. a Raspberry Pi interpreting sensor streams locally. Real but specialized. [inference; the $35-Pi capability is sourced]

### The honest bottom line [advisory]

1. **Default to hybrid, route by difficulty.** Pure-local is right only when privacy/latency/offline is non-negotiable; pure-cloud only when the task genuinely needs frontier accuracy.
2. **The constraint is memory bandwidth — design around it.** Smaller models, aggressive 4-bit (eventually ternary) quantization, and KV-cache discipline matter more than raw NPU TOPS. Don't buy the TOPS headline.
3. **In regulated fields, "the data never leaves the device" is the product, not a feature** — but only if your model is actually good enough, which is exactly where finance/legal/healthcare still split between local triage and cloud-grade reasoning.
4. **Watch BitNet/ternary and on-device MoE** — the two developments most likely to expand what runs locally in the next 12 months.

---

## 7. Learning path for a technical leader

For someone who **decides, funds, staffs, and evaluates** — not someone who writes the kernels. No coding labs. The job is to hold the right mental models, ask the questions that separate real expertise from confident hand-waving, and know which tradeoffs are real versus marketing.

### Part A — The five core mental models

**1. Decode is memory-bound, not compute-bound. This is the master key.** Generation speed is governed by **memory bandwidth** (GB/s), not by raw TOPS, because each token requires streaming essentially the whole model out of memory. A phone advertising a 45–60 TOPS NPU still has only ~50–90 GB/s of bandwidth versus a data-center GPU's 2–3 TB/s — a 30–50× gap [sourced]. When a vendor dazzles you with TOPS, your instinct should be: *"TOPS is the wrong metric for decode. What's the memory bandwidth, and what tokens/sec do I actually measure?"* The twist: prefill (reading the prompt) is compute-bound and fast; decode (writing the answer) is memory-bound and slow [inference].

**2. A model is a "memory budget," and quantization is how you spend it.** Size on device ≈ (parameters × bits) / 8 bytes. 4-bit is the production standard [sourced]. The depth signal: at 3–4 bits quantization behaves like *compression*; below 2 bits the model needs *fundamentally different internal representations*, so you must **train it that way from the start** (BitNet). And for a *fixed* budget, a bigger model at 2 bits often beats a smaller one at 4 bits (ParetoQ) [sourced] — a great litmus test.

**3. The KV cache is a hidden second model that grows as you talk.** It grows linearly with conversation length and, in long-context use, **can exceed the model weights themselves** [sourced]. Your memory budget is "the model *plus* a ballooning cache." Leaders who miss this approve "128K context" features that silently blow the budget.

**4. Edge vs. cloud is a routing decision, not a religion.** The mature architecture is a tiny router that decides per request, on three axes: **privacy** (a hard constraint — sensitive data stays local), **complexity** (extraction/classification/short Q&A → edge; multi-step reasoning/code/long synthesis → cloud), and **length/cost**. Escalate when on-device confidence is low. The right question is never "edge or cloud?" but *"what's our routing policy, and what fraction can we keep local?"* — directionally ~60–80% for general assistant traffic, higher for narrow consumer tasks [sourced for the pattern; the exact fraction is inference].

**5. The four reasons to go on-device — and they're not all about speed.** Latency, privacy (a capability, not a feature), cost (moved to the user's battery), availability (offline). Each implies different success metrics. Naming the *primary* driver up front prevents months of optimizing the wrong thing [sourced + advisory].

### Part B — A concepts-only progression [advisory]

Climb in order; each rung assumes the one below. (1) Why on-device at all — the four drivers. (2) The decode bottleneck — why TOPS misleads; prefill vs. decode. (3) Quantization basics — the 16→4-bit path. (4) The quantization frontier — sub-4-bit, native low-bit training (BitNet), "bigger-but-lower-bit wins." (5) The KV cache — why it grows, how to tame it. (6) Small Language Models — why sub-4B got shockingly good (distillation, data quality over raw parameter count). (7) Speculative decoding — attacking the sequential nature of decode. (8) The hardware reality — NPU vs. CPU vs. GPU, why NPUs hit limits in practice (weak support for attention and dynamic shapes), unified memory. (9) The runtime stack — llama.cpp/GGUF for prototyping & CPU, ExecuTorch for production mobile, MLX for Apple, MLC for cross-platform. (10) Hybrid routing — router-as-classifier, escalation on low confidence. (11) On-device agents & tool use — the frontier and its limits (tiny working memory; tool descriptions eat the context budget). (12) The open frontier — MoE on edge (you must *store* all experts even though you *use* few), test-time compute, on-device personalization.

### Part C — The curated reading spine [advisory]

Read big-picture to sharp-edge: (1) **"On-Device LLMs: State of the Union, 2026"** — the single best leader-level overview, with numbers; start here [sourced]. (2) **"On-Device LLMs in 2026: What Changed"** (Edge AI and Vision Alliance) — a tighter executive companion [sourced]. (3) **The hybrid-routing pieces** (TianPan.co, April 2026) — read at least the routing-layer article, the architecture you'll actually fund [sourced]. (4) **Vendor architecture docs as primary sources** — Apple Intelligence + Private Cloud Compute, and Google's Gemini Nano / AICore — to see how the biggest players drew the edge/cloud line [sourced]. (5) **One quantization deep-read for vocabulary, not math** — a BitNet b1.58 write-up plus a short ParetoQ summary [sourced]. (6) **One survey for breadth** — "A Survey of Small Language Models" (arXiv 2410.20011); skim the taxonomy [sourced]. For each, extract (a) the bottleneck it cares about, (b) the named techniques, and (c) the one number it hangs its argument on.

### Part D — Understanding checkpoints [advisory]

You can lead if you can answer these out loud, plainly:
- **A (master key):** Why is generation on a phone slow even with tons of TOPS? → memory bandwidth + the prefill/decode split.
- **B (quantization):** What's the difference between 4-bit and 2-bit, and why can't I crush any model to 1.58 bits? → compression vs. native low-bit training.
- **C (memory):** We want 128K context on-device — what just happened to our budget? → the KV cache growing linearly, possibly exceeding the weights.
- **D (architecture):** On-device or cloud for this feature? → reframe to a routing policy with privacy as a hard constraint and a target local fraction.
- **E (calling BS):** Given "our NPU does 60 TOPS, runs any 8B model instantly," name two reasons to doubt it (real bandwidth; real NPU utilization on attention) and the one number you'd demand (measured tokens/sec at a stated quantization, plus memory headroom including the KV cache).
- **F (frontier):** Why is MoE attractive in the cloud but hard on the edge? → it saves *compute* per token but you must still *store every expert in memory*, and memory is what the edge lacks.

### Part E — How to evaluate an expert in an interview [advisory] (the technical facts the answers reference are sourced)

You don't need to out-code them — you need to tell deep understanding from pattern-matched buzzwords.

- **"Why is on-device generation slow, and what would you optimize?"** *Strong:* leads with **memory bandwidth**, distinguishes prefill from decode, names concrete levers (quantization, speculative decoding, KV-cache compression), quotes a rough number. *Red flag:* "we need more TOPS / a faster NPU."
- **"Fixed 2 GB budget — bigger model at 2-bit or smaller at 4-bit?"** *Strong:* knows the bigger-at-lower-bit result (ParetoQ) often wins, *and* adds the caveats (sub-2-bit needs native training; budget for the KV cache). *Red flag:* thinks you can quantize anything to any bit-width with no quality cliff.
- **"What runs on-device vs. cloud?"** *Strong:* a router making per-request decisions, privacy as a hard constraint, escalate on low confidence, a realistic local-traffic target. *Red flag:* dogmatic single-side answer; treats privacy as negotiable.
- **"What breaks when we ship 128K context on a phone?"** *Strong:* immediately names the **KV cache** ballooning past the weights; reaches for attention sinks / cache compression / low-bit KV. *Red flag:* never mentions the KV cache.
- **"Make generation 2–3× faster without changing the model."** *Strong:* **speculative decoding**, and knows it preserves output quality. *Red flag:* "quantize more" (that changes the model) or "wait for better hardware."
- **"Why is MoE hard on the edge?"** *Strong:* saves *compute*, not *memory* — you must store all experts. *Red flag:* conflates compute savings with memory savings.
- **"When was on-device the wrong call?"** *Strong:* a real story where the small model's quality wasn't acceptable and hybrid/cloud was correct. *Red flag:* edge zealotry; never reconsidered.

**Cross-cutting red flags:** leads with TOPS as the speed metric; never spontaneously mentions memory bandwidth or the KV cache; quotes only peak/theoretical numbers, never measured tokens/sec on a real device at a stated quantization; believes you can post-hoc quantize anything to ~1-bit; treats privacy as negotiable; talks frameworks as fashion rather than mapping runtime to target; confuses MoE compute savings with memory savings; treats post-training quantization and quantization-aware training as interchangeable (QAT typically costs far less accuracy — single-digit-percent loss can drop toward ~1% — but more to produce) [sourced].

**Green flags:** defaults to measured numbers on real hardware, stated alongside the quantization and KV-cache headroom; frames everything as tradeoffs against a named primary driver; treats edge-vs-cloud as a routing policy with fallback; knows the frontier honestly (solved: 4-bit, SLMs, speculative decoding; open: MoE on edge, long-context memory, on-device agent/tool-use limits).

**A note on currency [advisory]:** the *mental models* above are durable — memory-bandwidth dominance, the quantization budget, the KV cache, hybrid routing, the four drivers will still frame the problem next year. The *specific numbers* (TOPS, GB/s, which model leads) drift; re-check the "State of the Union" overview and the major vendors' architecture docs every few months.

---

## 8. Team notes

### What this means for staffing

The whole engineering problem is squeezing a model into a device with ~50–90 GB/s of bandwidth versus a data-center GPU's 2–3 TB/s [sourced]. The thing to internalize: during generation the chip is **waiting on memory, not on math**. You need people who think in *bytes moved*, not in FLOPs.

### Roles and seniority [advisory]

This is **not** a "hire an LLM/prompt person" problem. It's a **systems + numerics** discipline, closer to embedded/performance engineering than to data science.

| Need | Seniority | Can an existing role absorb it? |
|---|---|---|
| **On-device inference / model-optimization engineer** (the real hire) | Senior (staff-level for the first one) | No. Owns quantization, runtime selection, hardware profiling, memory-bandwidth thinking. |
| **Mobile/embedded platform engineer** | Mid–Senior | Often yes — a strong mobile engineer can absorb the *integration* layer once the inference engineer hands off a working model. |
| **ML / quantization specialist** | Senior, often fractional at first | Partially. Only needed dedicated if you push sub-4-bit or train your own model. |
| **Eval / quality owner** | Mid | Yes — fold into QA, but they need device-specific eval (latency, thermal, battery, not just accuracy). |
| **Product owner for the cloud↔device routing decision** | — | Yes, existing PM/eng lead. This is a product decision, not a new hire. |

**Bottom line [advisory]:** for most teams the honest answer is **one senior inference engineer + your existing mobile engineer**. If you're shipping a generic feature (summarize, rewrite, classify) on iPhone/Android, you may need **zero** net-new ML hires — the platform SDKs absorb the hard part. A dedicated team becomes necessary only when you run a *custom* model or target hardware the SDKs don't cover.

### Hiring signals and red flags

**Strong signals** (sourced where noted, otherwise inference from the technical literature): says **"profile on real hardware early; emulators aren't accurate"** unprompted [sourced]; talks about **memory bandwidth as the bottleneck**, not TOPS (the single best filter) [inference]; hands-on with the real runtimes (ExecuTorch, llama.cpp/GGUF, MLX, LiteRT-LM/ML Kit) [sourced]; understands quantization by name (AWQ/GPTQ for 4-bit, SmoothQuant for 8-bit, SpinQuant for sub-4-bit, and what an "outlier activation" is) [sourced]; knows **KV-cache memory can exceed the weights** and names mitigations [sourced]; has war stories about **thermal throttling** [sourced].

**Red flags:** only ever ran models behind a cloud API (the binding constraints don't transfer) [inference]; quotes throughput from a single cold run (sustained/thermal behavior is where edge breaks) [inference]; reaches for "just fine-tune it" for every quality gap (the edge lever is usually quantization/distillation/routing); wants to roll a custom runtime by default; can't explain why a 60-TOPS NPU still runs an LLM slowly.

**Comp anchor [sourced]:** US LLM-engineer base ~$155–225K mid, ~$245–355K senior; frontier-lab total comp $480–750K. On-device specialists who genuinely combine ML + embedded systems are *rarer* than generic LLM engineers — expect to pay at the senior end and search longer [inference].

### Build vs. buy [advisory] — default: buy/rent unless owning is a real moat

The platform vendors did the hard part and gave it away:

| Layer | Default | Why |
|---|---|---|
| **The model** | **Buy/rent** — use the OS model (Apple Foundation Models; Gemini Nano via Android AICore/ML Kit) | Zero inference cost, OS handles distribution and updates, privacy by default [sourced]. |
| **The inference runtime** | **Adopt OSS** — ExecuTorch, llama.cpp, MLX, LiteRT-LM | Production-grade, hardware-portable, maintained by Meta/Google/Apple. Writing your own is a multi-year tarpit. |
| **Cloud↔device routing** | **Build (thin)** | This is your product logic and genuinely worth owning. As of iOS 27 you can put on-device and cloud models behind one protocol and switch per call [sourced]. |
| **A custom small model** | **Build only if it's a moat** | Justified when the OS model can't run on your target hardware (embedded/automotive/older devices), or when proprietary on-device data makes a small custom model meaningfully better, or when regulation forbids any vendor dependency. |

**When owning IS a moat [inference + advisory]:** you ship to hardware the SDKs don't cover (embedded boards, cars, kiosks, Pi + NPU); the on-device model *is* the product (a privacy-first or offline-first app); or you have proprietary on-device data. Otherwise, every month spent hand-rolling quantization for a generic summarize/rewrite feature is a month the OS vendors will obsolete with a free SDK update.

### Common failure modes

**Technical** (sourced — primarily the State-of-the-Union overview and the sustained-load paper): (1) **thermal throttling kills sustained performance** — a phone can lose ~half its throughput within a couple of iterations, and some OSes enforce a GPU floor that terminates inference; the demo looks great, the 30th request doesn't. (2) **KV-cache memory explosion at long context** — the cache can exceed the weights, blowing a sub-4 GB usable budget. (3) **outlier activations break naive quantization** — quality silently degrades without outlier-aware methods. (4) **NPU operator gaps** force CPU/NPU fallback that erases the expected speedup. (5) **small-model quality cliff** on long reasoning, novel problems, and broad knowledge — without cloud routing, users hit a wall. (6) **hardware fragmentation** — "works on my Pixel" is not "ships."

**Organizational [advisory]:** (7) hiring a cloud-LLM person for an embedded-systems job (the most common and most expensive miss). (8) building a custom runtime when an SDK existed. (9) benchmarking on a cold flagship when ship targets are mid-tier and thermally constrained. (10) treating accuracy as the only metric — latency, battery, binary size, and thermals are first-class. (11) no fallback plan — shipping on-device-only means the small model's weak spots become your support tickets.

### TL;DR for the hiring manager [advisory]

- **First hire:** one senior **on-device inference engineer** who thinks in memory bandwidth and has shipped on real hardware. This role rarely already exists on your team.
- **Often sufficient with that:** your existing mobile engineer for integration. You may need **zero** net-new ML scientists.
- **Buy the model and runtime** (OS SDKs + OSS runtimes); **build only** the cloud↔device routing and a custom model *if* it's a genuine moat.
- **Top red flag:** cloud-API-only experience presented as edge experience.
- **Top failure mode:** great demo, dies under sustained thermal load.

---

## Sources

- On-Device LLMs: State of the Union, 2026 — V. Chandra — https://v-chandra.github.io/on-device-llms/ (accessed 2026-06-25)
- On-Device LLMs in 2026: What Changed, What Matters, What's Next — Edge AI and Vision Alliance (Jan 2026) — https://www.edge-ai-vision.com/2026/01/on-device-llms-in-2026-what-changed-what-matters-whats-next/ (accessed 2026-06-25)
- Advances to low-bit quantization enable LLMs on edge devices — Microsoft Research — https://www.microsoft.com/en-us/research/blog/advances-to-low-bit-quantization-enable-llms-on-edge-devices/ (accessed 2026-06-25)
- Best LLMs for Real-Time Inference on Edge in 2026 — SiliconFlow — https://www.siliconflow.com/articles/en/best-LLMs-for-real-time-inference-on-edge (accessed 2026-06-25)
- LLM Inference at the Edge: Mobile/NPU/GPU Trade-offs Under Sustained Load — arXiv 2603.23640 — https://arxiv.org/abs/2603.23640 (accessed 2026-06-25)
- T-MAN: End-to-End Low-Bit LLM Inference on NPUs via Unified Table Lookup — arXiv 2511.11248 — https://arxiv.org/pdf/2511.11248 (accessed 2026-06-25)
- Vec-LUT: Vector Table Lookup for Ultra-Low-Bit LLM Inference on Edge — arXiv 2512.06443 — https://arxiv.org/pdf/2512.06443 (accessed 2026-06-25)
- Small Language Models on Edge Devices (2026) — Renard Digital — https://renard-digital.fr/blog/en/small-language-models-edge-devices-2026/ (accessed 2026-06-25)
- Cost of Training LLM From Scratch in 2026 — AI Superior — https://aisuperior.com/cost-of-training-llm-from-scratch/ (accessed 2026-06-25)
- LLM Training Cost: What $100M+ Really Buys in 2026 — AI Superior — https://aisuperior.com/llm-training-cost/ (accessed 2026-06-25)
- GaLore: Memory-Efficient LLM Training by Gradient Low-Rank Projection — arXiv 2403.03507 (accessed 2026-06-25)
- APOLLO: SGD-like Memory, AdamW-level Performance — arXiv 2412.05270 (accessed 2026-06-25)
- ITU Facts and Figures 2025 (offline population ~2.2 billion) — https://www.itu.int/itu-d/reports/statistics/facts-figures-2025/ (accessed 2026-06-25)
- Apple ML Research — On-Device & Server Foundation Models updates — https://machinelearning.apple.com/research/apple-foundation-models-2025-updates (accessed 2026-06-25)
- Introducing Apple's On-Device and Server Foundation Models — Apple ML Research — https://machinelearning.apple.com/research/introducing-apple-foundation-models (accessed 2026-06-25)
- Apple Foundation Models framework (Swift) — https://dev.to/arshtechpro/apples-foundation-models-framework-run-ai-on-device-with-just-a-few-lines-of-swift-lbp (accessed 2026-06-25)
- Apple Foundation Models 3 (WWDC 2026) read — ofox.ai — https://ofox.ai/blog/apple-foundation-models-3-wwdc-2026-developer-read/ (accessed 2026-06-25)
- NPU Comparison 2026 (Intel/Qualcomm/AMD/Apple) — https://localaimaster.com/blog/npu-comparison-2026 (accessed 2026-06-25)
- Running LLMs on Snapdragon 8 Elite — GrapeUp — https://grapeup.com/blog/running-llms-on-device-with-qualcomm-snapdragon-8-elite (accessed 2026-06-25)
- Comparative study: MLX, MLC-LLM, Ollama, llama.cpp — arXiv 2511.05502 — https://arxiv.org/pdf/2511.05502 (accessed 2026-06-25)
- SLM comparison: Phi-4 / Gemma / Llama for enterprise edge — https://www.meta-intelligence.tech/en/insight-slm-enterprise (accessed 2026-06-25)
- Edge/Mobile LLM Leaderboard 2026 — Awesome Agents — https://awesomeagents.ai/leaderboards/edge-mobile-llm-leaderboard/ (accessed 2026-06-25)
- On-Device LLM Inference 2025–2026 Guide — Octomil — https://docs.octomil.com/blog/on-device-llm-inference-2025-2026/ (accessed 2026-06-25)
- Hybrid Cloud-Edge LLM Inference: The Routing Layer — TianPan.co (2026-04-10) — https://tianpan.co/blog/2026-04-10-hybrid-cloud-edge-llm-inference-routing (accessed 2026-06-25)
- Hybrid Cloud-Edge LLM Inference: When On-Device Models Beat the Cloud — TianPan.co (2026-04-10) — https://tianpan.co/blog/2026-04-10-hybrid-cloud-edge-llm-inference-when-to-run-on-device (accessed 2026-06-25)
- Hybrid Cloud-Local LLM Architecture Guide 2026 — SitePoint — https://www.sitepoint.com/hybrid-cloudlocal-llm-the-complete-architecture-guide-2026/ (accessed 2026-06-25)
- Collaborative Inference between Edge SLMs and Cloud LLMs (survey) — arXiv 2507.16731 — https://arxiv.org/html/2507.16731v1 (accessed 2026-06-25)
- LLM Deployment in Regulated Industries: HIPAA/SOC2/GDPR Playbook 2026 — TrueFoundry — https://www.truefoundry.com/blog/llm-deployment-in-regulated-industries-hipaa-soc2-and-gdpr-playbook-for-2026 (accessed 2026-06-25)
- On-Device AI for Medical Transcription and Note Generation — arXiv 2507.03033 — https://arxiv.org/pdf/2507.03033 (accessed 2026-06-25)
- Hospital of 2026: Local LLMs in Healthcare — Drug & Device World (Jan 2026) — https://druganddeviceworld.com/2026/01/26/hospital-of-2026-local-llms-and-ai-are-redefining-healthcare/ (accessed 2026-06-25)
- Browser-Based LLMs in Healthcare — DEV — https://dev.to/shieldstring/browser-based-llms-in-healthcare-2e72 (accessed 2026-06-25)
- Edge-AI secure healthcare architecture — Nature Scientific Reports — https://www.nature.com/articles/s41598-025-30150-x (accessed 2026-06-25)
- NVIDIA Jetson Thor — Physical AI platform — https://developer.nvidia.com/blog/introducing-nvidia-jetson-thor-the-ultimate-platform-for-physical-ai/ (accessed 2026-06-25)
- Jetson T4000 / JetPack 7.1 + TensorRT Edge-LLM — NVIDIA — https://developer.nvidia.com/blog/accelerate-ai-inference-for-edge-and-robotics-with-nvidia-jetson-t4000-and-nvidia-jetpack-7-1/ (accessed 2026-06-25)
- 2026 Guide to Copilot AI Laptops / NPUs — Skywork — https://skywork.ai/skypage/en/copilot-ai-laptops-guide/2033470596177543168 (accessed 2026-06-25)
- On-Device LLM or Cloud API checklist — Data Science Collective (Medium) — https://medium.com/data-science-collective/on-device-llm-or-cloud-api-a-practical-checklist-for-product-owners-and-architects-30386f00f148 (accessed 2026-06-25)
- Finance LLM benchmark (Claude Fable 5, 90.34%) — AIMultiple — https://aimultiple.com/finance-llm (accessed 2026-06-25)
- Best local coding LLMs 2026 (Qwen2.5-Coder-32B, HumanEval) — Local AI Master — https://localaimaster.com/models/best-local-ai-coding-models (accessed 2026-06-25)
- Running LLMs Locally in 2026: Ollama, llama.cpp — daily.dev — https://daily.dev/blog/running-llms-locally-ollama-llama-cpp-self-hosted-ai-developers/ (accessed 2026-06-25)
- 1.58-bit LLM (BitNet) — Wikipedia — https://en.wikipedia.org/wiki/1.58-bit_large_language_model (accessed 2026-06-25)
- BitNet a4.8: 4-bit Activations for 1-bit LLMs — Microsoft Research — https://www.microsoft.com/en-us/research/publication/bitnet-a4-8-4-bit-activations-for-1-bit-llms/ (accessed 2026-06-25)
- BitNet b1.58 / native 1-bit LLMs overviews — https://medium.com/@akhshyganesh/the-dawn-of-native-1-bit-llms-how-bitnet-b1-58-2b-4t-is-changing-the-game-5db3b659a0a9 and https://emelia.io/hub/bitnet-1bit-llm-cpu-inference (accessed 2026-06-25)
- Apple AI architecture around Google Gemini — https://news.ycombinator.com/item?id=48450142 and https://medium.com/macoclock/apples-quiet-bet-on-llm-routers-using-gemini-d0a04cc1c4b6 (accessed 2026-06-25)
- A Survey of Small Language Models — arXiv 2410.20011 — https://arxiv.org/pdf/2410.20011 (accessed 2026-06-25)
- ParetoQ / 2-bit instruction-tuned LLMs — arXiv 2506.09104 — https://arxiv.org/pdf/2506.09104 (accessed 2026-06-25)
- Embodied Foundation Models at the Edge: A Survey — arXiv 2603.16952 — https://arxiv.org/pdf/2603.16952 (accessed 2026-06-25)
- Cactus on-device benchmark (LFM2-VL-450m tokens/sec, INT8) — referenced in edge leaderboard 2026 (accessed 2026-06-25)
- US LLM-engineer compensation 2026 — Kore1 — https://kore1.com (accessed 2026-06-25)
