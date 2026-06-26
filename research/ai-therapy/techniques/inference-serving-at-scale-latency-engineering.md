# Inference & serving at scale + latency engineering

*A note on labels.* Throughout, factual claims carry a tag: **(sourced)** with a URL and date means a published source backs it; **(inference)** means it's my reasoning from those sources; **(speculation)** means a forward guess; **(advisory)** marks my learning-design and org judgment — reasoned, not sourced. Verifier corrections have been folded in silently where they sharpen a claim, and called out where a popular framing is wrong.

---

## 1. What it is

Training a model is a one-time cost. **Serving** it is the forever-cost. Once you have a good model, the question that decides your margins, your latency, and whether the product feels alive is mundane and brutal: how do you run this thing for millions of people at once, fast enough that nobody notices the wait, cheap enough that you don't go broke?

"Inference and serving at scale + latency engineering" is the discipline of answering that question. It is mostly *not* about the model. It is about the machinery around the model — how requests get batched onto GPUs, how the GPU's memory is rationed, where the cache lives, how the work is split across machines, and how you keep the slowest 1% of requests from ruining the experience for everyone. By 2026 this has become arguably *the* dominant engineering and cost problem in AI, larger in aggregate spend than training itself. (inference, grounded in the cost-share material below)

To understand any of it, you need one mental model. When you send a prompt to a large language model, two very different things happen:

- **Prefill** — the model reads your *entire* prompt at once and builds up its understanding of it. This is one big parallel computation. It is **compute-bound**: the bottleneck is the GPU's math units. (sourced — [Spheron, 2026](https://www.spheron.network/blog/llm-serving-optimization-continuous-batching-paged-attention/))
- **Decode** — the model writes its answer **one token at a time**. To produce token #50 it must look back at tokens #1–49. This is an inherently sequential grind, and it is **memory-bound**: the bottleneck is how fast the chip can shuttle data in and out of memory. (sourced — same)

Almost every technique in this field is a consequence of these two phases having *opposite personalities* and fighting over the same hardware.

A serving system takes thousands of these requests arriving every second, packs them onto a fleet of GPUs, and returns answers under two latency promises (called SLOs, service-level objectives):

- **TTFT — Time To First Token** — how long until the answer *starts* appearing. Dominated by prefill. (sourced — [TianPan, 2026-03-10](https://tianpan.co/blog/2026-03-10-llm-latency-decomposition-ttft-vs-throughput))
- **TPOT / ITL — Time Per Output Token (inter-token latency)** — how fast the words then stream out. Dominated by decode. (sourced — same)

Latency engineering is the craft of hitting both targets at once while keeping the GPUs busy — because an idle GPU at \$2–4 an hour is money on fire.

> Two metrics, two enemies. TTFT and throughput are *different problems that often fight each other* — the central tension of the whole field. (sourced — [TianPan, 2026-03-10](https://tianpan.co/blog/2026-03-10-llm-latency-decomposition-ttft-vs-throughput))

---

## 2. How it works

There are about seven big gears. Each solves a specific bottleneck, and the modern engines — **vLLM**, **SGLang**, **NVIDIA Dynamo**, **TensorRT-LLM** — run all of them together.

### Gear 1: Continuous batching — never let the GPU idle

GPUs are fast only when doing a *lot* of math at once. Serving one user at a time wastes ~99% of the chip. So you batch many users together. The naive way ("static batching") waits for a full group, runs them in lockstep, and waits for *all* to finish — so one user writing a long essay stalls everyone else.

**Continuous batching** fixes this: at *every single token step*, the scheduler kicks out finished requests and slots in new ones. The batch is a revolving door, not a bus that waits for a full load. This alone is the difference between a GPU at 20% utilization and one above 80% — a 10–24x win over naive serving, and now table stakes. (sourced — [Spheron, 2026](https://www.spheron.network/blog/llm-serving-optimization-continuous-batching-paged-attention/))

### Gear 2: PagedAttention — stop wasting memory on the KV cache

As the model decodes, it stores the "meaning" of every token so far in a structure called the **KV cache** (key-value cache). This cache is large and grows with every token. Naively you'd reserve one big contiguous slab of memory per request, sized for the worst case — wasting 60–80% of memory on requests that turn out short.

**PagedAttention** borrows the trick operating systems use for RAM: chop the KV cache into small fixed **pages** and hand them out on demand, like virtual memory. Now you fit far more concurrent users in the same GPU memory. (sourced — [Spheron, 2026](https://www.spheron.network/blog/llm-serving-optimization-continuous-batching-paged-attention/)) SGLang's variant, **RadixAttention**, goes further by sharing pages between requests with common prefixes — a tree of cached tokens. (sourced — [Particula, 2026](https://particula.tech/blog/sglang-vs-vllm-inference-engine-comparison))

The KV cache is the single most important object in this whole field. It is the model's working memory, it lives in scarce GPU memory, and *most* of the cleverness in 2026 serving is really KV-cache management — paging it, reusing it, offloading it, routing requests to wherever it already lives.

### Gear 3: Prefix caching — don't recompute what you already computed

Most real traffic shares huge prefixes: the same system prompt, the same document, the same conversation history on every follow-up turn. **Prefix caching** keeps the KV cache for those shared tokens and reuses it, so a returning request skips straight past the prefill it already paid for.

> "KV cache prefix reuse is the single highest-leverage TTFT optimization for most production workloads." (sourced — [BentoML LLM Handbook, 2026](https://bentoml.com/llm/inference-optimization/kv-cache-offloading))

In 2026 this scaled into a *distributed* cache layer. **Mooncake** (a KV-cache-centric architecture) and **LMCache** offload and share KV cache across an entire cluster — even down to CPU RAM and SSD. Integrating Mooncake into vLLM reported **3.8× higher throughput, 46× lower TTFT, and 8.6× lower end-to-end latency on agentic traces** (on roughly 60 GB200 GPUs). (sourced — [vLLM Blog, 2026-05-06](https://vllm.ai/blog/2026-05-06-mooncake-store)) The mental model that has hardened: the KV cache is now a **memory hierarchy** — GPU HBM → CPU DRAM → local SSD → distributed store — exactly like a CPU cache hierarchy. (sourced — [Touchdown Labs, 2026](https://touchdown-labs.com/blog/kv-cache-memory-hierarchy-inference.html))

### Gear 4: Disaggregated prefill/decode — stop the two phases from fighting

This is the headline architectural shift of 2024→2026. Prefill (compute-heavy, bursty) and decode (memory-heavy, steady) have opposite appetites. Run them on the same GPU and a fat prompt's prefill freezes everyone's token streaming — "prefill-decode interference." (sourced — [arXiv 2512.22066, 2026](https://arxiv.org/html/2512.22066v1))

**The fix:** physically split them. A pool of **prefill workers** does nothing but ingest prompts; a pool of **decode workers** does nothing but stream tokens. When prefill finishes, it ships the KV cache over a fast link to a decode worker. The plumbing that moves that cache is its own engineering feat: **NIXL**, NVIDIA's KV-transport layer, picks the fastest available path — NVLink inside a box, InfiniBand across boxes — to move gigabytes of tensors in milliseconds. (sourced — [Spheron, 2026](https://www.spheron.network/blog/nvidia-dynamo-disaggregated-inference-guide/))

- **NVIDIA Dynamo 1.0** — the orchestration layer that sits *above* vLLM/TensorRT-LLM and routes work to the two pools — went **GA at GTC on 16 March 2026**, reporting up to **7× throughput gains** on DeepSeek-R1 on Blackwell. (sourced — [NVIDIA, 2026](https://developer.nvidia.com/blog/nvidia-dynamo-1-production-ready/))
- SGLang reported **2.7× higher decode throughput on GB200 NVL72** with disaggregation. (sourced — [LMSYS, 2025](https://www.lmsys.org/blog/2025-05-05-large-scale-ep/))
- The open-source, Kubernetes-native equivalent is **llm-d** (now a CNCF Sandbox project, backing the GKE Inference Gateway). One real-world caveat to keep: cross-node disaggregation needs a fast fabric (RDMA / InfiniBand). Without it, shipping the KV cache over plain TCP can *dominate* TTFT and erase the entire gain. (sourced — [llm-d, 2026](https://llm-d.ai/blog/production-grade-llm-inference-at-scale-kserve-llm-d-vllm))

### Gear 5: Speculative decoding — beat the sequential bottleneck

Decode is slow because it's one-token-at-a-time. **Speculative decoding** uses a tiny, cheap "draft" model to *guess* the next several tokens, then the big model checks all the guesses **in one parallel pass**. Correct guesses are accepted for free; wrong ones are thrown out.

Be precise about what "free" means here. Speculative decoding is **lossless in distribution, not token-for-token identical**. With proper verification (rejection sampling), it provably preserves the model's output *distribution*. Under greedy decoding (temperature 0) that means the exact same tokens; at temperature > 0 an individual run will differ from a baseline run while the statistics are provably unchanged. So: a true speedup that never degrades quality — but "distributionally identical," not "the same sentence every time." (inference, correcting a common overstatement)

In 2026 the production standard is **EAGLE-3**, merged into vLLM, SGLang, and TensorRT-LLM in early 2026. (sourced — [Spheron, 2026](https://www.spheron.network/blog/eagle-3-speculative-decoding-gpu-cloud/)) It hits acceptance rates of **0.80–0.88** on coding/instruction tasks, for **3–4× throughput** at low batch sizes on H100/H200.

**The catch — and this is the most commonly mangled point in the field.** It is tempting to state a clean acceptance-rate cutoff ("pays off above 0.7, slower below 0.5"). That is only roughly true *at small batch sizes*. The dominant variable is actually **batch size / system load, not a fixed acceptance threshold**. Speculative decoding spends spare compute to verify guesses. At low-to-medium batch that compute is sitting idle, so verification is nearly free and you win. As batch size grows (or utilization climbs), decode becomes compute-bound — the spare compute disappears — and even with good acceptance (0.8+) speculative decoding can *lose*, because now you're paying real compute to verify tokens you could have just generated. (sourced — [TianPan, 2026-04](https://tianpan.co/blog/2026-03-10-llm-latency-decomposition-ttft-vs-throughput); BentoML 2026) So the honest rule: **it pays off at low-to-medium batch with a good draft model, and gives the win back as batch size grows or acceptance falls.** This is exactly why it's the default layer for *interactive* (low-batch, latency-sensitive) serving and less so for high-throughput batch jobs.

### Gear 6: Quantization — shrink the numbers, move less memory

The model's weights are stored as numbers. Storing them in lower precision (fewer bits) means less memory to move — and since decode is bottlenecked by memory movement (see Section 3), this directly buys speed. The 2026 frontier is **NVFP4**, a 4-bit float with dedicated tensor-core hardware on NVIDIA Blackwell:

- **3.5× smaller** than FP16, **1.8× smaller** than FP8, with **<1% accuracy loss** (DeepSeek-R1 showed ~0.1% MMLU degradation). (sourced — [NVIDIA, 2026](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/))
- Production practice is **mixed precision**: NVFP4 weights + FP8/BF16 attention, which beats full-FP4 on quality-sensitive tasks. (sourced — [Spheron, 2026](https://www.spheron.network/blog/fp4-quantization-blackwell-gpu-cost/))

FP8 is now the *conservative default*; FP4 is moving from cutting-edge to mainstream.

### Gear 7 (for the biggest models): Wide Expert Parallelism

Virtually every frontier open model in 2026 is **Mixture-of-Experts** (MoE): a huge total parameter count, but only a fraction of "experts" fire per token. The examples shift fast — DeepSeek's V3-family (671B total / 37B active) defined the pattern; by mid-2026 a newer generation (DeepSeek V4-class at ~1.6T parameters, Kimi K2.6) has shipped, and the various models differ in size (Kimi K2 ~1T total; Llama 4 Maverick ~400B/17B active). The point is structural, not about any one model: you can't fit these on one GPU, so the experts are spread across dozens — **Expert Parallelism (EP)**. (sourced — [LMSYS, 2025](https://www.lmsys.org/blog/2025-05-05-large-scale-ep/); model generation per deeplearning.ai / spectrumailab, May–June 2026)

The hard part is the all-to-all network shuffle that routes each token to its experts. **DeepEP** (DeepSeek's communication library, with its EPLB load balancer now in SGLang) and NVIDIA's **Wide-EP** on GB200 NVL72 make this efficient — **1.8× higher per-GPU throughput**, with a reference deployment hitting **52.3k input + 22.3k output tokens/sec per node**. (sourced — [NVIDIA, 2026](https://developer.nvidia.com/blog/scaling-large-moe-models-with-wide-expert-parallelism-on-nvl72-rack-scale-systems/))

---

## 3. Why it works

Everything above descends from **one physical fact**, captured by the **Roofline model**: a chip is limited *either* by how fast it can do math (compute) *or* by how fast it can fetch data from memory (bandwidth) — whichever ceiling is tighter for the work at hand. The deciding ratio is **arithmetic intensity** (math operations per byte fetched). (sourced — [arXiv 2503.08311, 2026](https://arxiv.org/html/2503.08311v2))

- **Prefill** processes all prompt tokens together, reusing each loaded weight across many tokens → **high arithmetic intensity → compute-bound.**
- **Decode at batch size 1** loads the *entire multi-gigabyte model from memory to produce a single token*, then does it again for the next. Almost no math per byte → **memory-bandwidth-bound.**

This single asymmetry explains the whole field:

| The naive approach | Why it fails | The fix it forces |
|---|---|---|
| Serve one request at a time | Decode wastes ~99% of compute waiting on memory | **Batching** (amortizes the weight load over many requests) |
| Static batches | One slow request stalls all | **Continuous batching** |
| Co-locate prefill + decode | Compute-bound and memory-bound work sabotage each other's SLOs | **Disaggregation** |
| Reserve worst-case memory per request | 60–80% of memory wasted | **PagedAttention** |
| Recompute every prompt fresh | Pay for the same system prompt a million times | **Prefix / KV caching** |
| Generate strictly one token at a time | Sequential dependency caps speed | **Speculative decoding** |
| Store weights in 16 bits | More bytes to move = slower decode | **Quantization (NVFP4)** |

**The deep "why batching works":** batching is the lever that *moves you along the roofline*. A single decode request sits far left in the bandwidth-bound regime; pile 32+ requests onto the same weight-load and you climb toward the compute ceiling, getting near-free extra throughput — until you hit the bandwidth wall again. (sourced — [arXiv 2503.08311, 2026](https://arxiv.org/html/2503.08311v2))

**The deep "why it's hard":** every optimization trades against another.
- Batching helps throughput but *hurts* per-user latency (your request waits for the batch).
- Caching helps TTFT but *consumes* the memory PagedAttention is trying to conserve.
- Speculative decoding helps single-stream latency but *burns* the spare compute you'd rather give to batching — which is exactly why it stops paying off as batch size grows.

This is why the field's real metric isn't throughput but **goodput** — throughput that actually *meets its SLO*. Push load too low and you waste GPUs; too high and you miss your latency promise; goodput peaks in the middle. (sourced — [arXiv 2410.14257, 2026](https://arxiv.org/abs/2410.14257)) Goodput exists *because* of the trilemma. Optimizing it is engineering, not a checklist.

One more piece of physics worth internalizing, because it governs every interactive product: **tail latency explodes with utilization.** P99 latency grows roughly as 1/(1−ρ), where ρ is utilization. At 80% utilization, the tail is about 5× worse than at 20%. (sourced — queueing-theory M/M/1 result, confirmed) This is why latency-sensitive products *deliberately* run their GPUs at 60–70% and "waste" the headroom — the alternative is a fraction of users hitting brutal pauses.

---

## 4. People & resources

*All figures are orders of magnitude with stated basis — planning estimates, not quotes.*

### Compute and money (the dominant cost)

*Pricing basis: GMI Cloud, Spheron, Inworld, 2026.* (sourced)

- **Hourly GPU rents (2026):** H100 SXM ~\$2/hr on-demand (spot ~\$1); H200 ~\$2.60/hr; B200 ~\$4/hr; GB200 NVL72 ~\$8/GPU-hr effective.
- **Cost per million tokens** is the number that actually matters, and it's where the engineering pays off: roughly **\$0.14/M on H100 vs ~\$0.02/M on B200** for the same work — a ~**7× cost collapse**, driven by Blackwell's FP4 throughput. (sourced — [Inworld, 2026](https://inworld.ai/resources/nvidia-b200-gpu-cloud))
- B200: **192 GB HBM3e, 8 TB/s bandwidth, ~9,000 FP4 TFLOPS — ~4× H100 inference throughput.**

**How much of the AI compute bill is inference?** The direction is unambiguous: inference now dominates spend, and low utilization is treated as a *systems-engineering failure, not a hardware-scarcity excuse*. On the exact share, be careful — the widely-quoted ">80%" traces to a forward-looking executive remark (Lenovo's CEO at CES 2026 predicting the ratio would flip), not a measured 2026 number. Deloitte's actual 2026 estimate is **roughly two-thirds (~66%) of AI compute on inference, up from about half in 2025**. So: **roughly two-thirds and rising** is the defensible figure; treat ">80%" as a directional/quoted forecast. (sourced — Deloitte 2026 estimate; Lenovo CES 2026 quote — directional)

> **The takeaway for a non-implementer:** the hourly rate is the *least* important of three numbers. **Utilization, batching efficiency, and cache hit rate** swing your real bill by 5–50×. A team that masters the gears above pays a fraction of one that rents the same hardware naively. (advisory, grounded in [GMI Cloud, 2026](https://www.gmicloud.ai/en/blog/gpu-cloud-pricing-llm-inference-2026))

### Time

- The hard mechanisms (PagedAttention, continuous batching, EAGLE-3, NVFP4, disaggregation) are now **off-the-shelf** in vLLM/SGLang/Dynamo/TensorRT-LLM. Standing up a *competent* serving stack on rented GPUs is **days to weeks**, not months. (advisory)
- Building a *frontier* stack from scratch — custom kernels, distributed KV transport, multi-datacenter scheduling — is a **multi-year, continuous** effort (vLLM and SGLang have each run for years with dozens of contributors). (inference, from project histories)

### Team size and roles *(advisory — reasoned estimate)*

- **Use existing open-source serving (most companies):** a **2–6 person** platform/MLOps team — an inference-platform engineer (owns vLLM/SGLang config), an SRE (autoscaling, SLOs, on-call), a performance engineer (profiling, batching/cache tuning), plus part-time GPU-capacity planning.
- **Build/customize a serving engine (frontier labs, large clouds, NVIDIA):** **20–60+** engineers — CUDA/kernel specialists, distributed-systems engineers (the KV-cache transport and scheduler are genuinely hard distributed systems), compiler/quantization experts, and a research-adjacent group tracking the EAGLE/Mooncake/MoE literature. (inference, from the scale of the Dynamo, vLLM, SGLang, DeepSeek teams)

### Data scale

- **Inference itself needs no training data** — it consumes prompts and emits tokens. The relevant "data" is *operational*: production **traffic traces** (request rates, prompt/response length distributions, prefix-sharing patterns) used to size fleets and tune caches. (sourced — [arXiv 2603.16054, 2026](https://arxiv.org/pdf/2603.16054))
- **Speculative decoding *does* need data:** the EAGLE-3 draft head is *trained*, typically on the target model's own outputs — modest by LLM standards (hours-to-days on a handful of GPUs), not a frontier-scale run. (inference from [EAGLE-3 paper, 2025](https://arxiv.org/html/2503.01840v1))
- **Volume that justifies all this:** the techniques only pay off at scale — think **billions of tokens/day** across **thousands to tens-of-thousands of concurrent requests**. Below that, you rent an API and skip the entire problem. (advisory)

---

## 5. Scenarios & stories

The one judgment that separates real inference engineering from cargo-culting: **name your binding constraint before you touch the stack.** Latency-bound or cost-bound? Prefill-heavy or decode-heavy? High-reuse or one-shot? At a scale that pays for a serving team, or below it? Every technique is the right answer to *one* constraint and dead weight against the others.

### Where it's the right tool

**The chat product that got popular.** A startup ships a coding assistant on a managed API. Usage explodes — say 200M tokens a day, steady around the clock, on an open-weight model that's good enough. This is the textbook case for self-hosting. The key word is *steady*: a constant firehose lets you keep a GPU above 70% utilization, and a GPU at 70% costs roughly 1/7th per token of one idling at 10%. (sourced) You'd run vLLM or SGLang with continuous batching, paged KV cache, and — crucially for a coding assistant — **prefix caching**, because the giant "here are the rules and the open files" preamble is identical across thousands of requests. RadixAttention-style caching reuses it automatically. (sourced — [Spheron, 2026](https://www.spheron.network/blog/llm-serving-optimization-continuous-batching-paged-attention/))

**The voice agent where 300 milliseconds is the whole product.** A real-time voice assistant: the user speaks, the answer must start before the silence feels awkward. Here latency *is* the product, and the relevant number is TTFT. This justifies the heavy artillery — **speculative decoding (EAGLE-3)** for 2–6× faster decode at low batch, and **provisioning for the tail, not the average.** Because P99 grows as 1/(1−ρ), a voice product deliberately runs its GPUs at 60–70% peak, "wasting" headroom on purpose, because the alternative is one caller per second hearing a two-second pause. (sourced) The lesson: in interactive systems, *the average is a lie*; P99 catches the batch-interference spikes and cache evictions that averaging hides — and those are exactly the users who churn.

**The long-context, high-reuse workload.** A document-analysis platform where every query drags 50,000 tokens of context and many queries share the same documents. This is the poster child for **prefill/decode disaggregation** plus **cache-aware routing** (send a request to whichever node already holds the relevant cached documents). With 50K-token prompts, prefill is a monster; splitting it from decode removes the interference, and routing turns the repeated-document pattern into a big win — up to ~40% faster on long-context serving. (sourced — [Together AI, 2026](https://www.together.ai/blog/cache-aware-disaggregated-inference))

**Ten million contracts to summarize by morning.** A legal-tech firm needs to classify and summarize an archive overnight. Nobody's waiting at a screen. This is the right tool *in its batch form* — and recognizing that is the skill. No streaming, no TTFT, no P99. You do the *opposite* of the voice case: crank batch sizes to fill the GPU, run on cheap spot instances (60–70% cheaper, fine because restartable), and shut down when the queue drains. An offline batch job costs 5–10× less per token than the same work pushed through a latency-optimized endpoint at 20–30% utilization. (sourced — [Spheron, 2026](https://www.spheron.network/blog/batch-llm-inference-gpu-cloud/)) Same models, same hardware, opposite engineering — because the constraint flipped from latency to cost.

### Where it's the wrong tool

**The prototype that serves 40 people.** An internal tool, a few hundred requests a day, three engineers. Building a disaggregated, speculatively-decoded, KV-offloading stack here is malpractice. Self-hosting carries a hidden tax of ~10–20 engineering hours/month even when nothing breaks. (sourced) Right answer: call a managed API and move on.

**Racing an ultra-cheap commodity model to the bottom.** To beat a budget API tier (Gemini-Flash-class pricing) by self-hosting, you'd need your GPU pinned near 100% utilization 24/7 just to break even — and real traffic is bursty, so you never do. The wrongness isn't technical, it's strategic: solving a cost problem the market already solved. (advisory)

**Reaching for serving tricks when the model is the problem.** Latency is bad, so the team bolts on speculative decoding, disaggregation, a tiered cache — and it barely helps. If TTFT is dominated by a 50K-token prompt that's mostly junk, the fix is *prompt and context engineering*, not a serving rewrite. Speculative decoding speeds *decode*; it does nothing for a prefill-bound TTFT problem. Disaggregation helps *interference and scaling*; on a single under-loaded GPU it just adds network hops. The discipline is **diagnosis first**: measure whether you're prefill- or decode-bound, compute- or memory-bound, queue- or model-bound — *then* pick the matching tool. Applying decode tricks to a prefill problem is a tune-up on a car that's out of gas. (advisory, grounded in the sourced prefill/decode split)

**Latency obsession on a batch workload.** An overnight embeddings pipeline given the full real-time treatment — small batches, tail-latency autoscaling, speculative decoding — is pure waste. It throws away the single biggest lever (large batches) to protect a metric no human is waiting on. A team that can't tell whether its workload is latency- or throughput-sensitive will mis-engineer it in one of these two directions every time. (advisory)

---

## 6. Cross-industry usage & positioning (as of June 2026)

By 2026 the stack has crystallized into a recognizable shape, and different sectors assemble different subsets of the same parts bin. The **inference engines** — vLLM (broadest, fastest to production, the open ecosystem hub), SGLang (shared-prefix workloads via RadixAttention), TensorRT-LLM (peak NVIDIA throughput, but a long compile cold-start) — are roughly at feature parity on the fundamentals. Above them sits an **orchestration layer** (NVIDIA Dynamo, or the open Kubernetes-native llm-d) doing disaggregation and KV-aware routing, a **KV memory hierarchy** (LMCache, Mooncake), and a **gateway** doing semantic and cache-aware routing with SLO-aware autoscaling (the Kubernetes Gateway API Inference Extension is the emerging standard). (sourced — [LeetLLM, 2026](https://leetllm.com/blog/llm-inference-engine-comparison-2026))

**Coding / developer tools — most demanding, sets the pace.** Coding agents (Claude Code, Cursor, Copilot) drive the state of the art because they're *agentic* and *prefix-heavy*: huge, mostly-stable system prompts, then long multi-step tool loops. The defining technique is **prefix caching**, with reported 41–80% cost reduction and 13–31% TTFT improvement. The hard-won 2026 lesson: cache *boundaries* matter — cache the stable system prompt, exclude volatile tool results, or naive full-context caching can *raise* latency. Agent latency compounds (a 10-step chain at 500ms/step = 5s of pure wait), so prefix caching and speculative decoding here are load-bearing, not optional. (sourced — [AI Checker Hub, 2026](https://aicheckerhub.com/anthropic-prompt-caching-2026-cost-latency-guide); [arXiv 2601.06007](https://arxiv.org/html/2601.06007v2))

**Customer support / voice — latency is the entire product.** Target is sub-800ms end-to-end, with LLM inference ~70% of the budget. Real-world medians sit around 1.4–1.7s with P99 of 3–5s — so the gap between "demo" and "feels human" is exactly latency engineering. Platforms: LiveKit, Pipecat, Vapi. Techniques like preemptive generation (start the LLM before the user finishes) and speech-native end-to-end models are displacing the slower STT→LLM→TTS pipeline. Sub-second is now a baseline, not a differentiator. (sourced — [Forasoft, 2026](https://www.forasoft.com/blog/article/livekit-ai-agents-guide))

**Finance / trading — latency king, pays any premium.** Finance routes the latency-critical slice of traffic to **specialized non-GPU silicon**: Groq (LPU, <100ms TTFT) and Cerebras (wafer-scale, throughput champion, ~80–150ms TTFT). A common contrast cites GPU inference at 400–600ms TTFT vs Groq <100ms — but read that carefully: the 400–600ms is a *particular GPU baseline*, not a property of GPUs in general. Well-optimized GPU serving (small prompt, prefix-cache hit, disaggregated prefill) routinely lands well under 200ms. The honest framing is *tiered routing*: a cheap GPU pool for bulk/async, a premium LPU/wafer pool for the latency-critical slice. (sourced — [GMI Cloud, 2026](https://www.gmicloud.ai/en/blog/fastest-llm-platform-compare); hedge per verifier)

**Healthcare / clinical — privacy forces the architecture.** Regulation (HIPAA/GDPR) and PHI push inference **on-premise or on-device** rather than to frontier APIs. The 2026 answer is twofold: small/edge models quantized to run on-prem or even on a clinician's device, and on-prem open models on Blackwell with TensorRT-LLM for ambient-scribe workloads. This sector lags coding/voice on cutting-edge serving tricks but leads on edge/small-model deployment. (sourced — [MD+DI, 2026](https://www.mddionline.com/artificial-intelligence/how-large-language-models-are-reshaping-health-prediction-clinical-decision-making))

**Robotics / physical AI / defense — hard real-time, edge-constrained.** The hardest latency regime: a closed control loop with physics. Vision-Language-Action (VLA) models must run at bounded latency on hardware beside the robot. The dominant 2026 architecture is **hierarchical / dual-rate** — a heavy VLM plans at 5–10Hz, a lightweight action expert runs at 50–100Hz — with **action chunking** (emit many future actions at once, execute open-loop) decoupling control rate from inference rate. Genuinely frontier; nothing here is yet table-stakes. (sourced — [NeuralCoreTech, 2026](https://neuralcoretech.com/physical-ai-architecture-vla-robotics/))

**Enterprise / legal / RAG — throughput + prefix-reuse economics.** Shared-prefix, long-context workloads — the natural home of RadixAttention and cross-request KV reuse. The wins are economic (reuse the KV of a 50-page contract across many queries) rather than hard-real-time. This is where most large enterprises are now: cost optimization is table-stakes, disaggregation is the upgrade in flight.

**Consumer / science — cost floor and batch throughput.** Consumer chat is dominated by the cost-per-token race (Blackwell drove the floor to ~\$0.02/M tokens on open models, making free tiers viable); science leans on wafer-scale throughput for non-interactive screening and simulation.

**The 2026 inflection — agentic workloads.** Test-time compute (extended "thinking," long tool loops) means a single task can burn enormous token counts. A 128k-token context alone needs ~16GB of KV cache for an 8B model. This is *why* KV tiering, prefix caching, and disaggregation went from nice-to-have to mandatory. There's also a sobering finding (CMU 2026) that more agent turns can *hurt* — so serving efficiency now interacts with agent design, not just raw speed. (sourced — [Effloow, 2026](https://effloow.com/articles/agent-test-time-compute-scaling-context-ceiling-2026))

**Table-stakes vs cutting-edge (June 2026):** Continuous batching, paged KV, prefix caching, and FP8 are table-stakes everywhere. Speculative decoding (EAGLE-3) is mainstream for interactive serving. Disaggregation (Dynamo, llm-d), NVFP4, and tiered/distributed KV are cutting-edge but rapidly mainstreaming for long-context. SLO-aware independent prefill/decode autoscaling, wafer-scale/LPU silicon, and hierarchical VLA edge serving remain frontier or niche-but-leading.

---

## 7. Learning path for a technical leader

*For a leader, not an implementer. No coding labs. You don't need to write CUDA — you need the mental models to ask the right questions, read a serving architecture and smell what's wrong, set the right SLOs, and tell a real expert from a confident talker.*

### Mental models (the load-bearing ideas)

1. **Two phases, two physics.** Prefill is compute-bound and sets TTFT; decode is memory-bandwidth-bound and sets TPOT. Nearly every decision treats them as different beasts.
2. **The KV cache is the working set, and the real bottleneck.** It grows with context × batch, lives in scarce GPU memory, and most 2026 cleverness is KV-cache management.
3. **Throughput vs latency vs cost is a trilemma; the dial is batch size.** Bigger batches = cheaper per token but each user waits longer. You choose a point *per workload*.
4. **Goodput, not throughput, is the real metric.** Requests/sec that *met their SLO*. It peaks in the middle, not at max load.
5. **Continuous batching is the floor, not the ceiling.** A 10–24× win, now table stakes.
6. **Reuse beats recompute.** Prefix/KV caching is the highest-leverage *application* lever; agentic workloads benefit most.
7. **Disaggregation: stop making prefill and decode fight** — but you now pay to move the KV cache, and that needs a fast fabric.
8. **Speculative decoding: predict ahead, verify cheaply** — distributionally lossless, batch-size-sensitive (wins at low batch, gives back at high).
9. **The serving stack is a memory hierarchy + a routing problem.** KV spills GPU → CPU → SSD → remote, and a smart router sends each request to the GPU already holding its cache.

> **One-sentence model:** Inference is two phases with opposite physics; the KV cache is the scarce resource; everything else — batching, caching, disaggregation, speculation, routing — is a different way to spend less GPU memory and time per token while still hitting your latency SLO. (inference)

### Reading spine (few, high-value)

**Tier 1 — build the intuition:** Morph's *"LLM Inference: Prefill, Decode, KV Cache & Cost Guide (2026)"* (best plain-language on-ramp); DigitalOcean's *"The LLM Inference Trilemma"* (locks in the central tradeoff); Spheron's *"LLM Serving Optimization"* and *"LLM Inference SLO Engineering: TTFT, ITL, P99"* (the mechanics and the latency vocabulary). (sourced, 2026)

**Tier 2 — the 2026 architecture shift:** NVIDIA's *"Introducing Dynamo"* (canonical disaggregation — vendor, read critically) paired with the arXiv counterweight *"Beyond the Buzz: A Pragmatic Take on Inference Disaggregation"* (when it does *not* pay — [arXiv 2506.05508](https://arxiv.org/pdf/2506.05508)); LeetLLM's engine comparison (the live tool landscape). (sourced, 2026)

**Tier 3 — depth, skim and return:** the EAGLE-3 paper ([arXiv 2503.01840](https://arxiv.org/pdf/2503.01840)); the LMCache report ([arXiv 2510.09665](https://arxiv.org/abs/2510.09665)); *"Revisiting SLO and Goodput Metrics"* ([arXiv 2410.14257](https://arxiv.org/abs/2410.14257)); NVIDIA InferenceMAX for hardware economics (directional). (sourced, 2026)

*Source caveat: vendor and vendor-adjacent benchmarks (NVIDIA, Spheron) are best-case — treat as directional. The arXiv pieces are the neutral anchors.* (advisory)

### Checkpoints — you understand it when you can…

- Explain why a chatbot gives a fast first word but a slow full answer, and which phase fixes each complaint — without saying "the model is slow." *(literate)*
- Explain why more compute often *doesn't* speed decode, and why you ran out of memory before FLOPs. *(literate)*
- Say where you'd set the batch-size dial for a given product, and why P99 can worsen as average throughput improves. *(literate)*
- Estimate the cost win from prefix-caching a 10K-token system prompt across 50 agent calls — and say when caching *won't* help. *(competent)*
- Articulate disaggregation's trade (less interference vs paying to move the KV cache) and name two workloads where it isn't worth it. *(competent)*
- Explain why speculative decoding is distributionally lossless yet faster, and why the speedup hinges on *both* acceptance rate *and* batch size. *(competent)*
- Sketch the request path — router → cache-aware placement → prefill pool → KV transfer → decode pool → tiered offload — and locate the tail latency. *(competent)*
- Reason about cost-per-million-tokens vs batch size, quantization, hardware gen, and cache hit rate — and challenge a vendor number. *(can run the org)*
- Propose a serving shape for a *new* workload (e.g., a long-context legal-RAG agent) and defend the trade-offs. *(can run the org)*

### How to evaluate an expert

The goal is to separate someone who *operated* serving at scale from someone who *read* about it. The tell is **tradeoff reasoning under specifics**, not vocabulary. (advisory throughout)

- **Opening calibration:** *"Walk me through what happens, physically, from prompt arrival to first word, then full answer."* **Strong:** splits prefill/decode, names the KV cache, ties first-word→TTFT and streaming→TPOT. **Red flag:** conflates the two phases, or thinks decode is compute-bound.
- **Latency diagnosis:** *"Users say it feels sluggish but average latency looks fine."* **Strong:** goes to **P99 not mean**, suspects batch size/queuing/a long prompt starving others, asks traffic shape and SLOs first. **Red flag:** treats average as sufficient.
- **Caching:** *"Agent with a 12K-token system prompt, called many times per session — make it cheap and fast, and where does it break?"* **Strong:** prefix/KV caching, cache-aware routing, eviction and tiered offload; failure mode = low hit rate / many distinct prefixes. **Red flag:** thinks caching means storing past *responses*.
- **Disaggregation (best 2026 signal):** *"Vendor pushes disaggregated prefill/decode. When adopt, when refuse?"* **Strong:** removes interference and sizes pools independently *but* costs KV-transfer bandwidth and ops complexity, needs RDMA, often *not* worth it at small/bursty scale. **Red flag:** "it's faster, so yes."
- **Speculative decoding:** *"3× with lossless output — what's the catch?"* **Strong:** single-stream/low-batch win that gives back at high batch; hinges on acceptance rate *and* draft quality; preserves the output distribution. **Red flag:** thinks it degrades quality, or that 3× is unconditional.
- **Economics:** *"Vendor claims two cents per million tokens — sanity-check it."* **Strong:** asks which model, hardware, batch/concurrency, input:output ratio, quantization, SLO, cache hit rate; knows the headline assumes huge batches and a favorable workload, and your interactive SLO may force 10–100× higher real cost. **Red flag:** doesn't know cost and latency are in tension.

**Green flags overall:** reaches for "it depends on the workload" then *specifies* it; reasons from physics before tools; has opinions on goodput/P99; states the frontier honestly (disaggregation situational, spec-decoding batch-sensitive, vendor benchmarks best-case); can scope a *new* workload end-to-end and name what would change their mind. **Cross-cutting red flag:** never mentions the KV cache in a 45-minute serving conversation — disqualifying for a senior hire.

---

## 8. Team notes

### What you're actually hiring for

This splits into two tightly-coupled jobs. **Serving at scale** — keeping a fleet of GPUs busy across spiky, mixed traffic without overpaying — is mostly a *systems and FinOps* problem (scheduling, batching, autoscaling, routing, utilization). **Latency engineering** — making a single request return fast — is mostly a *performance* problem (KV-cache management, quantization, speculative decoding, prefill/decode separation). The person you hire is, in large part, a cost engineer who happens to speak GPU. (advisory)

### Roles & seniority — the decision ladder

- **Tier 0 — you call an API (most companies).** No new role, no new hire. Latency and serving are the vendor's problem; your existing backend engineer owns caching, batching at the app layer, retries, streaming, and model-tier choice. **Hiring an "inference engineer" here is the most common over-hire in the space.** (advisory)
- **Tier 1 — self-host open models, modest scale.** Absorbed by a senior platform / ML-platform engineer who stands up vLLM or SGLang, configures parallelism and KV cache, wires autoscaling and metrics. One strong generalist comfortable with GPUs and Kubernetes — *not* a kernel specialist. Budget ~10–20 engineering hours/month just on maintenance. (sourced — [Spheron, 2026](https://www.spheron.network/blog/inference-engineering-guide-2026/))
- **Tier 2 — high volume, latency is a product feature, or cost is a board-level line.** Now hire a dedicated **Inference / Performance Engineer** (senior, 5+ yrs): chooses hardware, optimizes serving frameworks, manages KV cache, controls cost per token. Searches like this typically run ~9 weeks; budget for a slow fill. (sourced — [NVIDIA Careers, 2026](https://jobs.nvidia.com/careers/job/893393953033); [KORE1, 2026](https://www.kore1.com/how-to-hire-ml-engineer-2026/))
- **Tier 3 — model lab, inference provider, or very large fleet.** A small *team*: performance engineers + an inference-platform/SRE function. Only here does the deep specialist — custom CUDA kernels, bespoke scheduler, novel quantization — earn their cost.

> **Rule of thumb:** if you can't name your monthly token volume and your TTFT/TPOT targets, you're Tier 0 or 1 and should not be hiring a specialist yet. (advisory)

### Hiring signals (what "good" looks like)

- **Thinks in TTFT / TPOT / throughput as a triangle**, and asks *which one matters for your product* before proposing anything.
- **Profiles before optimizing.** The field's headline 2026 lesson: the GPU often sits idle while the *system around it* (CPU, PCIe, memory bandwidth, KV cache, routing) is the bottleneck. Good candidates know the GPU is frequently *not* the problem. (sourced — [Yotta Labs, 2026](https://www.yottalabs.ai/post/why-llm-inference-has-low-gpu-utilization-cpu-pcie-memory-bandwidth-and-kv-cache-bottlenecks))
- **Has a defensible default among vLLM / SGLang / TensorRT-LLM**, and treats the choice as workload-dependent, not religious. (vLLM = broad default; SGLang = prefix-heavy; TensorRT-LLM = peak NVIDIA throughput, ~15–30% over vLLM on H100 but NVIDIA-only with real setup cost.) (sourced — [Yotta Labs, 2026](https://www.yottalabs.ai/post/best-llm-inference-engines-in-2026-vllm-tensorrt-llm-tgi-and-sglang-compared))
- **Connects every technique to a dollar or a millisecond**, and knows the toolbox by what it *buys you*, not by name-dropping.

### Red flags

- Optimizes tokens/sec while ignoring utilization (named the top recurring 2026 team mistake — low-utilization clusters burn money even at high per-request throughput).
- Wants to write custom CUDA kernels on day one for a Tier 1/2 workload.
- Mixes interactive and batch traffic under one scheduling policy without measuring.
- Reaches for disaggregation reflexively without asking about your network (cross-node needs RDMA; over TCP the KV transfer can *dominate* TTFT).
- Can't articulate the break-even for self-hosting. (sourced — [Spheron FinOps, 2026](https://www.spheron.network/blog/ai-inference-cost-economics-2026/))

### Build vs buy

**Default: rent/buy. Own it only past a clear volume-and-latency threshold.** (advisory, grounded in current economics)

- **Below ~20M tokens/month**, managed APIs win on *total* cost including ops. **Above ~100M tokens/month**, self-hosting almost always wins on unit economics. Thresholds shift by tier: premium-tier APIs break even sooner (~5–10M/mo), cheap APIs not until ~50–100M/mo. (sourced — [AI Pricing Master, 2026](https://www.aipricingmaster.com/blog/self-hosting-ai-models-cost-vs-api))
- *Note the units: break-even is in tokens per **month**, not per day. A widely-seen "100M tokens/day" figure is ~30× higher than the rest of the evidence and is best read as a per-month threshold.* (inference, reconciling a likely typo)
- **The trap:** the spreadsheet that says "self-hosting is cheaper" is usually wrong by 3–5×, because it counts GPU rental and forgets engineering labor, model updates, utilization waste, and depreciation. (sourced)

**What to buy vs build:**
1. **Buy the model API** until volume or data-residency/latency forces otherwise. Right default for nearly everyone.
2. **Rent the serving layer:** self-host the *model* on vLLM/SGLang — **never write your own inference engine.** Use a managed GPU/serverless layer (Modal, Baseten) before running your own Kubernetes fleet.
3. **Adopt orchestration incrementally, don't build it.** NVIDIA Dynamo is modular — you can adopt just the KV-aware router on your existing engine. A strong argument *against* building your own scheduler. (sourced — [Spheron, 2026](https://www.spheron.network/blog/nvidia-dynamo-disaggregated-inference-guide/))
4. **Build only the genuinely proprietary moat** (custom kernels, bespoke scheduler, novel quantization) — and only if inference *is* your product or your scale makes single-digit-percent efficiency worth a whole team.

### Common failure modes

1. **Hiring the specialist too early** — a Tier-0/1 company hires a CUDA expert with no kernels to write.
2. **Paying for idle GPUs** — dedicated GPUs sit idle on uneven traffic, and decode itself is memory-bandwidth-bound so the GPU's *compute* is largely idle even mid-generation.
3. **Optimizing the wrong metric** — chasing throughput when the product needs low TTFT, shipping a system that's technically faster but *feels* worse.
4. **Premature complexity** — disaggregation/multi-node before exhausting framework defaults, especially cross-node without the required RDMA fabric.
5. **The "inference is one step" mental model** — ignoring everything around the GPU, so CPU/PCIe/scheduling stalls leave expensive hardware idle.
6. **One traffic policy for everything** — latency-sensitive user traffic and interruptible batch jobs under the same policy, wasting both.
7. **Buying the self-hosting spreadsheet at face value** — then being shocked when true cost lands 3–5× higher. (all sourced — [Spheron FinOps, 2026](https://www.spheron.network/blog/ai-inference-cost-economics-2026/); [regolo.ai, 2026](https://regolo.ai/inference-efficiency-and-gpu-cost-optimization-in-2026-how-to-cut-llm-serving-waste/))

> **One-paragraph summary for a hiring manager.** Don't hire for this until you can state your token volume and TTFT/TPOT targets. Below that, it's a *skill* your platform engineer already has — buy the API, cache aggressively, move on. When self-hosting pays off (~20–100M+ tokens/month depending on tier), hire **one senior inference/performance engineer** and have them stand up **vLLM or SGLang** on a **rented** GPU layer — never a homegrown engine. Reserve deep CUDA specialists, custom schedulers, and multi-node disaggregation for when inference *is* your product. The recurring way teams lose money here isn't slow models — it's idle GPUs, the wrong optimized metric, and complexity bought before it was needed. (advisory)

---

## Sources

- [Spheron — LLM Serving Optimization: Continuous Batching, PagedAttention, Chunked Prefill (2026)](https://www.spheron.network/blog/llm-serving-optimization-continuous-batching-paged-attention/)
- [TianPan — LLM Latency Decomposition: TTFT vs Throughput (2026-03-10)](https://tianpan.co/blog/2026-03-10-llm-latency-decomposition-ttft-vs-throughput)
- [BentoML — KV Cache Offloading, LLM Handbook (2026)](https://bentoml.com/llm/inference-optimization/kv-cache-offloading)
- [vLLM Blog — vLLM × Mooncake (2026-05-06)](https://vllm.ai/blog/2026-05-06-mooncake-store)
- [Touchdown Labs — KV Cache as the Memory Hierarchy of Inference (2026)](https://touchdown-labs.com/blog/kv-cache-memory-hierarchy-inference.html)
- [NVIDIA — Dynamo 1.0 Production-Ready (2026)](https://developer.nvidia.com/blog/nvidia-dynamo-1-production-ready/)
- [Spheron — NVIDIA Dynamo Disaggregated Inference Guide (2026)](https://www.spheron.network/blog/nvidia-dynamo-disaggregated-inference-guide/)
- [llm-d — Production-Grade Inference at Scale: KServe + llm-d + vLLM (2026)](https://llm-d.ai/blog/production-grade-llm-inference-at-scale-kserve-llm-d-vllm)
- [LMSYS — DeepSeek with PD Disaggregation + Large-Scale EP on 96 H100s (2025-05-05)](https://www.lmsys.org/blog/2025-05-05-large-scale-ep/)
- [Spheron — EAGLE-3 Speculative Decoding on GPU Cloud (2026)](https://www.spheron.network/blog/eagle-3-speculative-decoding-gpu-cloud/)
- [EAGLE-3 paper — arXiv 2503.01840 (2025)](https://arxiv.org/html/2503.01840v1)
- [NVIDIA — Introducing NVFP4 for Efficient, Accurate Low-Precision Inference (2026)](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/)
- [Spheron — FP4 Quantization on Blackwell (2026)](https://www.spheron.network/blog/fp4-quantization-blackwell-gpu-cost/)
- [NVIDIA — Scaling Large MoE with Wide Expert Parallelism on NVL72 (2026)](https://developer.nvidia.com/blog/scaling-large-moe-models-with-wide-expert-parallelism-on-nvl72-rack-scale-systems/)
- [arXiv 2503.08311 — Memory-gap / large-batch bottlenecks (2026)](https://arxiv.org/html/2503.08311v2)
- [arXiv 2512.22066 — Prefill vs Decode bottlenecks (2026)](https://arxiv.org/html/2512.22066v1)
- [arXiv 2410.14257 — Revisiting SLO and Goodput Metrics in LLM Serving (2026)](https://arxiv.org/abs/2410.14257)
- [arXiv 2506.05508 — Beyond the Buzz: A Pragmatic Take on Inference Disaggregation (2026)](https://arxiv.org/pdf/2506.05508)
- [arXiv 2603.16054 — Fleet Capacity Planner (2026)](https://arxiv.org/pdf/2603.16054)
- [arXiv 2601.06007 — Don't Break the Cache: Agentic Prompt Caching (2026)](https://arxiv.org/html/2601.06007v2)
- [Together AI — Cache-Aware Prefill–Decode Disaggregation (CPD) (2026)](https://www.together.ai/blog/cache-aware-disaggregated-inference)
- [Spheron — Batch LLM Inference on GPU Cloud (2026)](https://www.spheron.network/blog/batch-llm-inference-gpu-cloud/)
- [Inworld — NVIDIA B200 GPU Cloud Specs/Pricing (2026)](https://inworld.ai/resources/nvidia-b200-gpu-cloud)
- [GMI Cloud — GPU Cloud Pricing for LLM Inference (2026)](https://www.gmicloud.ai/en/blog/gpu-cloud-pricing-llm-inference-2026)
- [GMI Cloud — Fastest LLM Inference Platform Comparison: Groq/Cerebras/SambaNova (2026)](https://www.gmicloud.ai/en/blog/fastest-llm-platform-compare)
- [LeetLLM — vLLM vs SGLang vs TensorRT-LLM vs Ollama (2026)](https://leetllm.com/blog/llm-inference-engine-comparison-2026)
- [Yotta Labs — Best LLM Inference Engines (2026)](https://www.yottalabs.ai/post/best-llm-inference-engines-in-2026-vllm-tensorrt-llm-tgi-and-sglang-compared)
- [Yotta Labs — Why LLM Inference Has Low GPU Utilization (2026)](https://www.yottalabs.ai/post/why-llm-inference-has-low-gpu-utilization-cpu-pcie-memory-bandwidth-and-kv-cache-bottlenecks)
- [Spheron — AI Inference Cost Economics 2026: GPU FinOps Playbook (2026)](https://www.spheron.network/blog/ai-inference-cost-economics-2026/)
- [regolo.ai — Inference Efficiency & GPU Cost Optimization in 2026 (2026)](https://regolo.ai/inference-efficiency-and-gpu-cost-optimization-in-2026-how-to-cut-llm-serving-waste/)
- [AI Pricing Master — Self-Hosting AI Models vs API: Cost Analysis (2026)](https://www.aipricingmaster.com/blog/self-hosting-ai-models-cost-vs-api)
- [KORE1 — How to Hire an ML Engineer: 2026 Guide (2026)](https://www.kore1.com/how-to-hire-ml-engineer-2026/)
- [NVIDIA Careers — AI Inference Performance Engineer (2026)](https://jobs.nvidia.com/careers/job/893393953033)
- [AI Checker Hub — Anthropic Prompt Caching: Cost & Latency Guide (2026)](https://aicheckerhub.com/anthropic-prompt-caching-2026-cost-latency-guide)
- [Forasoft — LiveKit AI Voice Agents 2026 Playbook (2026)](https://www.forasoft.com/blog/article/livekit-ai-agents-guide)
- [NeuralCoreTech — Physical AI Architecture: VLA & Robotics Inference (2026)](https://neuralcoretech.com/physical-ai-architecture-vla-robotics/)
- [Effloow — Agent Test-Time Scaling Has a Ceiling, CMU 2026 (2026)](https://effloow.com/articles/agent-test-time-compute-scaling-context-ceiling-2026)
- [MD+DI — How LLMs Are Reshaping Health Prediction & Clinical Decision-Making (2026)](https://www.mddionline.com/artificial-intelligence/how-large-language-models-are-reshaping-health-prediction-clinical-decision-making)
- [LMCache report — arXiv 2510.09665 (2026)](https://arxiv.org/abs/2510.09665)
- Deloitte 2026 estimate (~two-thirds of AI compute on inference) and Lenovo CEO CES 2026 remark (directional, on the inference/training spend split)
