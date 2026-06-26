# Serving Accelerations: Speculative Decoding & Low-Precision Quantization

*State of the art as of June 2026. Factual claims are labeled [sourced] with a pointer, [inference] (my reasoning from the facts), or [speculation] (a bet beyond the evidence). Learning-design and org calls are labeled [advisory] — that is my reasoned judgment, not a citation. Plain language throughout, because the ideas are deep enough that the words shouldn't add friction.*

---

## 1. What it is

Two separate tricks that make a large language model cheaper and faster to *run* — not smarter, just cheaper to operate. They are almost always discussed together because they attack the same waste from opposite sides, and they stack.

**Speculative decoding** makes a big model write several tokens per expensive step instead of one — **without changing a single token of its output.** You attach a tiny, fast "draft" mechanism to the big "target" model. The draft cheaply guesses the next few tokens; the big model checks all the guesses at once; correct guesses are kept for free. The text that comes out is *mathematically identical* to what the big model would have written alone — just produced in fewer expensive passes [sourced — the acceptance rule is a proven exact sampler; see Sources]. This is the property that makes it low-risk: it is not an approximation of the model, it *is* the model, sped up.

**Low-precision quantization** stores and computes the model's numbers with **fewer bits**. A weight that was 16 bits (BF16) becomes 8 bits (FP8) or 4 bits (FP4) — half or a quarter the bytes. Unlike speculative decoding, this *does* change the output: fewer bits means coarser numbers, so quality can drop. The whole craft is throwing away bits without throwing away the model's intelligence.

The one-line mental model: **speculative decoding changes *how you generate*; quantization changes *how the model is stored and computed*.** One is provably lossless. The other is a deliberate quality-versus-cost trade. Keeping that distinction sharp is the single most important thing in this chapter — most expensive mistakes here come from confusing the two.

---

## 2. How it works

### The one fact underneath both

A large model is **bottlenecked by memory, not by math.** To write one token, the model must read every one of its weights — tens to hundreds of gigabytes for a frontier model — out of GPU memory and into the chips that do arithmetic. Then it does a relatively tiny amount of multiplication, produces *one* token, and starts over: read all the weights again for the next token. The expensive part is the *hauling*, not the *computing*. The industry phrase is that inference is "memory-bound" — measured arithmetic intensity sits near ~1 FLOP per byte, deep in the memory-bound region [sourced]. The math units sit mostly idle, starved, waiting for weights to arrive.

That idle time is the resource both techniques feed on:

- **Quantization** makes each weight *smaller* — fewer bytes to haul per trip.
- **Speculative decoding** makes each trip *produce more tokens* — so you haul the weights fewer times for the same output, and it spends the idle math on verification.

Both are now standard in the major open serving stacks (vLLM, SGLang, TensorRT-LLM) [sourced].

### Speculative decoding, gear by gear

The technique stands on one asymmetry: **a big model can verify N tokens in almost the same wall-clock time it takes to generate 1.** Verifying N tokens is one forward pass — you haul the weights *once* and check all N positions in parallel. Since hauling is the expensive part, checking 5 guesses costs nearly what generating 1 costs. You already paid for the memory trip; the parallel math rides along for free.

Each step of the loop:

1. **Draft.** A small model — or a lightweight "draft head" (see EAGLE below) — proposes the next ~4–8 tokens. Cheap, because the draft is tiny.
2. **Verify in one shot.** The big model does a *single* forward pass over the whole proposed sequence and, for each position, computes what *it* would have said. One memory haul, N positions checked at once.
3. **Accept the longest correct prefix.** Walk left to right. Wherever the draft's guess matches what the big model would have produced (under a precise acceptance rule), keep it. At the first mismatch, throw away the rest and substitute the big model's own correct token there.
4. **Repeat.** You've committed somewhere between 1 token (draft was useless) and N+1 (draft was perfect) for the price of roughly one big-model pass.

The acceptance rule is the clever part that guarantees identical output. It's a rejection-sampling test: accept each drafted token with a probability set by the ratio of the big model's probability to the draft's probability for that token; on rejection, sample a correction from a carefully adjusted distribution. The provable result is that **the tokens that come out follow exactly the big model's own distribution** [sourced].

**The whole speedup rides on the *acceptance rate*** — what fraction of drafted tokens survive verification. The metric to watch is "acceptance length": how many guessed tokens get accepted per verification step. ~1 is useless; 3–5+ is a big win. The current champion family is **EAGLE**. EAGLE-3 (NeurIPS 2025) reaches acceptance rates of roughly **0.80–0.88** on Llama and Qwen models, up from 0.72–0.78 for EAGLE-2 [sourced — openreview.net, NeurIPS 2025]. Its trick: instead of a separate draft model, it uses a tiny one-layer "draft head" that reads the big model's *own internal activations* — fusing low-, mid-, and high-level features through a learned gate — so the draft is essentially the big model whispering its own next move [sourced — vLLM blog]. Tighter alignment with the target is exactly what raises acceptance.

The latest iteration, **EAGLE 3.1** (May 2026; EAGLE team + vLLM + PyTorch's TorchSpec), fixed instability over long contexts by normalizing and feeding back the target's hidden states each step. Result: **up to 2× longer accepted runs in long-context workloads**, and on a Kimi-K2.6 model in NVFP4, **2.03× higher per-user throughput at concurrency 1**, still 1.66× at concurrency 16 [sourced — vLLM blog, 2026-05-26].

That concurrency detail is the most important nuance: **the win shrinks as you batch more users.** At high batch sizes the GPU is no longer idle — it's busy serving many users, so the "free" math capacity speculation exploits is already used up. So speculative decoding is most valuable for **latency-sensitive, low-concurrency** work (a single user wanting fast responses, agentic chains, reasoning models emitting long outputs) and least valuable for maxed-out throughput farms [inference, consistent with the 2.03→1.66× concurrency curve].

A 2026 shift worth flagging: **multi-token prediction (MTP)** bakes the draft heads into the model *during training* rather than bolting them on. DeepSeek-V3 pioneered this; its MTP-1 head reports an >80% acceptance rate for ~1.8× throughput with no separate draft model and near-zero extra GPU cost [sourced — DeepSeek-V3]. The rule of thumb now: if you train the model yourself, build in MTP; if you're accelerating someone else's model, use EAGLE-3 [inference].

### Quantization, gear by gear

A neural network is billions of numbers. Most cluster near zero; a few are large outliers. Naive quantization — "pick one scale for the whole tensor, round everything to the nearest of 16 levels" — is destroyed by those outliers: one huge value stretches the scale so wide that all the small, numerous values collapse into the same few buckets and lose their meaning. **This is the failure mode every modern method is a different answer to.**

The 2026 toolkit, roughly in order of aggressiveness:

**FP8 (8-bit float) — the safe default.** Quantizing both weights and activations to FP8 is now considered **effectively lossless across model scales** [sourced — "Give Me BF16 or Give Me Death", arXiv 2411.02355]; calibrated FP8 typically loses 0.5–2% on standard benchmarks, within noise for most production tasks [sourced — multiple 2026 guides]. FP8 is a floating-point format, so it keeps an exponent — meaning it can represent both tiny and large values gracefully, which is why it handles outliers far better than 8-bit *integers*. This is the "yes, just do it" lever whenever you have the VRAM.

**INT4 weight-only (AWQ / GPTQ) — the memory-saver.** Weights to 4-bit integers, activations left at 16-bit ("W4A16"). The intelligence is in *which* weights get protected:
- **AWQ** (Activation-aware Weight Quantization) notices that the weights multiplied against large *activations* matter most, and scales them to protect them before rounding.
- **GPTQ** rounds weights one at a time and, after each, nudges the remaining weights to *compensate* for the error just introduced — an error-feedback loop.

In 2026 evaluations the two are near-identical on academic benchmarks (within ~0.3 points), with GPTQ slightly ahead on real-world coding tasks [sourced — vrlatech 2026]. AWQ remains the common best-practice INT4 format for vLLM [sourced].

**FP4 (4-bit float) — the new frontier, now in production.** The big 2026 story. Two flavors:
- **MXFP4** — the open OCP standard: 4-bit E2M1 values in **blocks of 32**, each block sharing one (coarse, power-of-two) scale.
- **NVFP4** — NVIDIA's Blackwell-native version: smaller **blocks of 16** with **two-level scaling** (an FP8 scale per 16-value block, plus one FP32 scale per tensor) [sourced — edge-ai-vision]. Smaller blocks adapt to local data swings; the finer scale controls error better than MXFP4's coarser blocks. NVFP4 wins on accuracy; MXFP4 wins on portability.

FP4 only became real in 2026 because of **hardware**: Blackwell GPUs execute these 4-bit formats *natively* in the tensor cores. Before that, 4-bit was a storage trick you had to unpack before computing; now the math runs at 4-bit directly. Versus FP8, NVFP4 delivers **2–3× higher arithmetic throughput and ~1.8× memory reduction** (~3.5× vs FP16), with accuracy on MMLU/HellaSwag/PiQA differing from BF16 by only **±0.005–0.01 when done well — practically negligible** [sourced — edge-ai-vision, Llama-2 7B/70B tests]. That "when done well" is load-bearing; see Story 5 in Section 5.

**The accuracy-recovery layer (QAD).** Pushing reasoning/RL-trained models to 4-bit *can* break them — plain post-training rounding damages the delicate behaviors learned during reinforcement learning. NVIDIA's 2026 answer is **Quantization-Aware Distillation (QAD)**: instead of just rounding, you fine-tune the quantized model to *imitate the full-precision model's outputs*. Reported result: plain quantization-aware training "breaks the RL model's capabilities," while QAD **recovers near-BF16 performance** across the Nemotron family, landing NVFP4 on DeepSeek-R1 within ~1% of the FP8 baseline [sourced — NVIDIA Nemotron QAD report, 2026]. This is how 4-bit is becoming safe even for reasoning models.

**One more place bits matter: the KV cache** — the model's running memory of the conversation. FP8 KV cache is near-free and standard in 2026; it cuts the memory-bandwidth and capacity cost of long contexts and big batches, often *the* bottleneck. Below FP8, get cautious [sourced].

---

## 3. Why it works

### Speculative decoding: parallel verification beats serial generation

**The principle:** verification is parallel, generation is serial. Serial generation wastes the GPU's parallel muscle because each token depends on the one before it — token 5 truly cannot be computed until token 4 exists. Speculation breaks that dependency *speculatively*: it bets on a future, then checks the whole bet in one parallel pass. You're converting a latency problem into a throughput problem, and GPUs are throughput monsters.

**Why the naive alternatives fail.** Plain autoregression forces one full weight-haul per token, with no way around the serial chain. The fix people *want* — "just make the model smaller" — fails because a smaller model produces *different, worse* text. Speculative decoding's whole reason for existing is that it gets small-model speed on the *easy* tokens (which a tiny draft nails) while preserving big-model quality everywhere, because the big model has veto power on every single token. You give up nothing in quality; you only spend extra compute on rejected guesses — and that compute was sitting idle anyway. (Until it isn't: at high batch the idle compute is gone, which is exactly why the technique fades under load.)

### Quantization: networks are redundant, so spend your bits where they matter

**The principle:** neural networks are massively redundant and noise-tolerant. They were trained with noisy gradients and dropout; they don't need 16 bits of precision per weight to encode their knowledge. The *information* in a weight lives mostly in its rough magnitude, not its 11th decimal. So you can discard most of the bits — *if* you spend the rest intelligently, concentrating precision where the model is sensitive (outlier channels, activation-heavy weights) and economizing where it isn't. This is why **mixed precision is the real answer, not one number for everything**: sensitive parts (attention, certain layers, the KV cache) stay higher; the bulk matrix-multiply weights go to the lowest precision that survives.

**Why the naive alternative fails:** a single global scale forces every weight to share one ruler, and outliers stretch that ruler until small weights become indistinguishable — the model goes stupid. Every modern method is a structured defense against this: per-block scaling (each small group gets its own ruler), floating-point formats (an exponent gives each value its own dynamic range), activation-awareness (protect the weights that actually move the output), and error feedback or distillation (measure the damage and correct for it). "Just round everything" is the strawman each of these beats.

### Why they multiply

The gains stack because they attack different bottlenecks — one shrinks what you haul, the other reduces how often you haul it. A widely cited back-of-envelope: quantization (~4×) × continuous batching (~2×) × speculative decoding (~2×) ≈ **~16× effective cost reduction** versus naive serving [sourced — Mirantis 2026]. None of it changes what the model *says* (speculation is provably exact; quantization is near-exact with QAD) — only what it *costs* to say it.

---

## 4. People & resources

### Speculative decoding: using it is nearly free; training a good draft is the bottleneck

This asymmetry is the main practical reason adoption lagged — "speculative decoding remains underutilized... limited availability of draft models" [sourced].

- **To use it (if a draft exists):** zero training. Turn on a config flag in vLLM/SGLang/TensorRT-LLM. One engineer, an afternoon [advisory].
- **To train an EAGLE-3 draft head:** this is small. *(Verifier correction applied.)* A draft head is **not** a multi-billion-parameter model — for typical targets it's **tens to a few hundred million parameters** (roughly 1–5% of the target's size; ~0.25B for an 8B target up to ~1B for a 70B target), with checkpoints around **~277 MB** [sourced — Spheron blog, Qwen2.5-14B EAGLE-3]. (The earlier "1–3B-parameter" framing was incompatible with a 277 MB checkpoint and is corrected here: a 1–3B model would be ~2–6 GB in FP16, not 277 MB.) Training a head takes roughly **2–4 hours on 4× H100**, using the target's own activations as the training signal, on modest data like UltraChat-200K [sourced].
- **Production-scale draft for a frontier model:** larger but still tiny by frontier standards. A Kimi-K2.5 EAGLE-3 draft reportedly took **~1,500 H200 GPU-hours**, ~600k samples, ~6B tokens [sourced — Spheron blog]. At ~$3/H200-hour that's order **single-digit thousands of dollars** [inference] — a rounding error against the base model.
- **Team/roles:** 1–3 ML engineers to train and validate a draft; the serving integration is largely done for you by the open frameworks. The hard skill is raising acceptance rate on *your* traffic distribution — a data/eval problem more than a compute problem [advisory].
- **Payoff:** roughly **2–3× faster** single-stream generation in typical deployments (e.g., ~145 → ~424 tok/s reported on a Qwen-class 9B), up to ~5.8× in research systems like Apple's Mirror-SD on 14B–66B models [sourced — premai/Apple].

### Quantization: cheap for most methods, real training only for the fragile cases

- **Post-training quantization (PTQ) — AWQ, GPTQ, FP8, basic FP4:** cheap. Run the model over a small **calibration set** (a few hundred to a few thousand sample sequences) to measure activation statistics, then compute scales. **Hours on a single node**, one engineer, off-the-shelf tools (LLM Compressor, AutoAWQ, TensorRT Model-Optimizer) [sourced — llm-compressor docs; advisory on team size]. Data scale: kilobytes-to-megabytes of representative text, not training-scale.
- **Quantization-Aware Distillation (QAD) — the expensive path for fragile reasoning models:** real training. You fine-tune the quantized model against the teacher's outputs. Cost is a fraction of pretraining but far above PTQ — **order hundreds to low-thousands of GPU-hours** depending on model size, plus a meaningful slice of high-quality distillation data [inference, based on NVIDIA Nemotron QAD describing full distillation pipelines]. Team: a small ML group (2–5) who own the post-training stack, since QAD must slot into the SFT/RL pipeline.
- **Hardware dependency:** FP8 needs Hopper-class or newer; **FP4 needs Blackwell** to get the throughput win (otherwise it's storage-only) [sourced]. This is a genuine capex gate — the technique's value is coupled to owning the right silicon.
- **Payoff:** FP8 ≈ free quality, ~2× memory/throughput. INT4/FP4 ≈ 4× smaller weights, fitting a model that needed multiple GPUs onto fewer, with 2–3× more throughput on Blackwell — and, with QAD, near-BF16 accuracy.

### The open-source reality (the most important staffing fact)

Both levers are now *features inside the serving frameworks*, not research projects you build. EAGLE-3 is merged into vLLM, SGLang, and TensorRT-LLM, and all three ship quantization support out of the box [sourced — Spheron engine comparison, 2026]. For most companies this collapses to a **configuration, calibration, and evaluation** job — not a kernel-writing job [advisory].

---

## 5. Scenarios & stories

The unifying lesson, stated up front: **both techniques feed on idle resources.** Speculation eats idle compute (vanishes under load); quantization eats idle precision headroom (vanishes when the task actually needs the precision). Name the resource your workload has to spare, and the right tool — and the wrong one — falls out.

**Story 1 — Speculative decoding, exactly right: the interactive coding assistant.** A developer hits Tab, waits, reads, hits Tab again. Bursty, latency-critical, batch size effectively 1; the GPU is bored and memory-bound. This is the home-run case. Code is *extremely* predictable — after `for i in range(`, the draft nails `len(` — so acceptance is high and you cash idle compute for tokens. EAGLE-3-style drafting (and its parallel variant, P-EAGLE) is the production standard here, with pre-trained draft heads published for models like Qwen3-Coder-30B. Speedups land around 2–3×, output quality unchanged [sourced — vLLM P-EAGLE]. Every condition that makes speculation win is present at once.

**Story 2 — Speculative decoding, the wrong tool: the high-throughput batch API at peak.** Same company, 2pm on a weekday: hundreds of concurrent requests packed into batches of 64–128. Now the GPU is **compute-bound** — the math units speculation wanted to fill are already saturated by paying requests. Every drafted-then-rejected token is wasted compute stolen from real work. Measured: for an 8B model on GSM8K, EAGLE's speedup decays from ~1.73× at batch 1 to ~1.21× at batch 128, and in short-context high-batch regimes it can go *negative* [sourced — arXiv 2510.22876]. The trap: the *same model, same code* helps at 3am and hurts at 2pm. **[advisory]** Treat speculation as a *load-dependent* feature, not a global switch — enable it when batch/queue depth is low, disable as the GPU saturates. Benchmark at midnight, ship to daylight, and you ship a regression.

**Story 3 — Speculative decoding, right for a non-obvious reason: long-context reasoning agents.** Feed the model 300k tokens of retrieved documents plus a long chain-of-thought, then generate a multi-thousand-token answer. Counterintuitively a strong fit: the huge **KV cache** must be re-read on every token, which makes decoding *even more* memory-bound — more idle compute for speculation to harvest. Two asterisks. First, off-the-shelf EAGLE was tuned on short sequences (<4k) and underperforms here; you need long-context-specialized drafting like **LongSpec** [sourced — arXiv 2502.17421]. Second *(verifier correction applied)*: the often-cited "~20% longer accepted runs" figure comes from **GLM-5's shared MTP-layer design** — a general MTP improvement — *not* from a long-context method, and should not be bundled with LongSpec as if it were a long-context result [sourced — GLM-5 MTP]. Reasoning text adds its own gift: chains-of-thought are self-similar and verbose ("Let me reconsider... Actually, step 3..."), which a draft predicts well.

**Story 4 — FP8, the safe default: fitting a 70B on one card.** A mid-size company runs a 70B for internal Q&A and drafting. In FP16 it needs ~140GB — two GPUs, NVLink, the headache. Quantize to FP8 and it's ~70GB: one 96GB Blackwell-class card. Halving the box count, the power, the interconnect, and often the per-token cost. Calibrated FP8 loses 0.5–2% on benchmarks — within noise — with mature, boring tooling [sourced]. If someone serving a big model in FP16 hasn't tried FP8, that's the first question to ask.

**Story 5 — FP4 applied naively: the math tutor that started lying.** A team building an AI math-and-coding tutor reads the Blackwell marketing, post-training-quantizes to FP4 to cut cost, and watches throughput soar — then the quality dashboard caves. The failure is **task-selective and invisible in aggregate metrics**: 4 bits can't represent the fine value distinctions multi-step reasoning depends on, and tiny per-step errors **compound through the chain** — a 2% distortion per step becomes a wrong answer ten steps later. Average perplexity looks fine; the students see a tutor that botches algebra. *(Verifier correction applied.)* I'm deliberately *not* repeating the specific "-51% on MATH / -39% on HumanEval" figures that circulate for this story: those magnitudes describe an extreme/low-bit or W4A4 configuration, not the W4A16-style NVFP4/MXFP4 weight-only PTQ the scenario implies. The better-supported picture for naive W4A16: HumanEval drops "exceeding 5%," larger MATH drops appearing mainly at 3-bit or under aggressive W4A4 [sourced — "Quantization Meets Reasoning", arXiv 2501.03035]. The *mechanism* (task-selective, error-compounding, hidden in averages) is real; the eye-popping numbers were cherry-picked from a worse setup.

**Story 6 — FP4, redeemed: the same model, done with QAT/QAD.** The twist that makes Story 5 about *method*, not format. The same aggressive FP4 that craters math under naive PTQ comes back to **under ~1% loss** when you stop being lazy: **quantization-aware training/distillation** fine-tunes the model with simulated FP4 noise so it *learns* to be robust to the rounding. NVIDIA's Nemotron work lands NVFP4 on DeepSeek-R1 within ~1% of the FP8 baseline (occasionally ahead on a benchmark like AIME); Google's Gemma QAT checkpoints are a public at-scale example [sourced — NVIDIA Nemotron QAD]. The catch is cost asymmetry: QAT needs a training run; FP8 is essentially free at inference. **[advisory] Decision rule:** (1) Default to FP8. (2) Pilot FP4 in parallel, never as a swap — run task-specific evals on your *hardest* slices, not averages. (3) Adopt naive FP4 only if your task is precision-tolerant (summarization, classification, chat, retrieval). (4) For precision-sensitive tasks, FP4 is viable only via QAT/QAD — spending training budget to buy inference savings, which pays off at large, sustained volume and not much below it. The headline for a skeptic: "FP4 is fine" and "FP4 destroyed our math scores" are *both true reports* — they differ entirely by whether QAT was used and which tasks were measured. The format is not the variable; the method and the workload are.

**Story 7 — Combining them, and where the combination stops paying.** Stack an FP8 target *and* speculation on a latency-sensitive low-batch chat product — composes cleanly, common in 2026. But the two have **different load curves**: quantization is a flat, always-on win (smaller weights help at every batch size); speculation is a low-batch-only win. Push batch high and the speculation half turns into overhead (Story 2) while the quantization half keeps paying — so under heavy load the right move is often "keep FP8/FP4, drop the speculation." Treating them as one "go fast" button is the mistake. They need separate switches wired to separate conditions.

---

## 6. Cross-industry usage & positioning (as of June 2026)

**The frame:** these are infrastructure, so adoption follows the *serving stack*, not the industry. Almost everyone runs on vLLM, SGLang, or TensorRT-LLM (or buys API access from providers who do), and those stacks ship FP8 + EAGLE-3 on by default. So the *base* technique is table-stakes nearly everywhere. Industry differences show up in (a) how *aggressive* the quantization is, (b) regulatory/accuracy constraints, and (c) whether they push to the edge [inference].

| Sector | Where it sits | What's specific |
|---|---|---|
| **Coding / dev tools** | Cutting-edge, most aggressive | The natural home — long, output-heavy, latency-sensitive, and highly predictable tokens give high acceptance. Anthropic, OpenAI, GitHub, Cursor, and open coding models (Kimi K2.6, GLM-5, Qwen3-Coder) lean hard on spec-decoding + MTP. *(inference)* |
| **Customer support / conversational** | Table-stakes | High-volume, cost-dominated, FP8-tolerant; quantized models + continuous batching are standard. The economics force it. *(inference)* |
| **Consumer / on-device** | Cutting-edge, fastest-moving | The biggest 2026 story. INT4/FP4 is *mandatory* to fit models on phones. Apple (MLX), Qualcomm, MediaTek, Meta's ExecuTorch (1.0 GA Oct 2025). On-device speculation is attractive because the draft can be a quantized version of the target. *(sourced)* |
| **Robotics / automotive / edge** | Cutting-edge, hardware-led | NVIDIA's TensorRT Edge-LLM (Jetson) ships EAGLE-3 + NVFP4 for real-time robotics/automotive VLM inference; Bosch, ThunderSoft, MediaTek demoed at CES 2026. Latency is a hard real-time constraint, not just cost. *(sourced)* |
| **Healthcare** | Table-stakes cost, conservative aggression | Adopts quantization (GPTQ-style calibration), but accuracy and regulatory caution mean less aggressive FP4 in clinical paths. Speculation is "free" quality-wise, so adopted readily; quantization is where they hold back. *(inference)* |
| **Finance** | Table-stakes, latency-obsessed | Same calibration pipelines; trading/real-time-risk value latency (good for speculation), while audit/reproducibility push toward speculation's *lossless* property and away from aggressive lossy quantization in regulated outputs. *(inference)* |
| **Legal** | Table-stakes cost | Long-document, output-heavy (good for spec-decoding); low hallucination tolerance tempers aggressive quantization. Mostly consumes providers' pre-optimized stacks. *(inference)* |
| **Defense / government** | Table-stakes, edge-focused | On-prem/air-gapped deployment makes self-hosting economics dominate (quantization essential to fit local hardware); tactical edge makes the same edge stack directly relevant. *(inference)* |
| **Science / research** | Mixed | Large-batch offline inference gets *less* from speculation (batches already saturate GPUs) but full benefit from quantization. Leans quantization-heavy, spec-decoding-light. *(inference)* |

**State of the art, June 2026 (the moving parts):**

- **Quantization.** FP8 is the *default*, not the optimization (0.5–2% loss) [sourced]. FP4 has crossed into production on Blackwell, with **NVFP4** (16-element blocks, two-level scaling) beating open **MXFP4** (32-element blocks) on accuracy: ~3.5× memory vs FP16, ~1.8× vs FP8, under ~1% loss when done well [sourced — NVIDIA]. Recovery is model-dependent (Qwen3 recovers best; Llama/sub-8B worst; large MoE surprisingly robust), with **QAD** the emerging lever to claw back NVFP4 accuracy [sourced].
  - *(Verifier correction applied — FP8 training claim hedged.)* FP8 training is real and increasingly mainstream — **DeepSeek-V3 publicly trained in FP8** [sourced]. The broader "Microsoft, Meta, and Google all train frontier models in FP8 for ~30–40% throughput gains" is **[inference], not sourced fact** — the specific three-lab attribution and the precise figure aren't established publicly, and the 2026 frontier is already moving toward FP4 *training*.
- **Speculative decoding.** EAGLE-3 is the production standard, merged into all three engines; ~3–4× headline, e.g., 1.81× at batch 2 and still 1.38× at batch 64 on H100/SGLang [sourced]. **MTP** is eating bolt-on speculation's lunch for new models (DeepSeek-V3 >80% MTP-1 acceptance, ~1.8×, near-zero extra cost; now in Kimi K2.6, GLM-5) [sourced]. Research frontier: Apple's Mirror-SD (2.8–5.8×, +30% over EAGLE-3 on 14–66B), P-EAGLE parallel drafting, and specialized variants for MoE (SP-MoE), long-context (LongSpec), and state-space models (STree) [sourced].
- **Diffusion LLMs — the wild card.** *(Verifier correction applied.)* Lead with the *current* development, not the stale demo: **DiffusionGemma** (open weights, Apache 2.0, released June 10 2026) reports **1,000+ tok/s on H100 / 700+ on RTX 5090, ~4× faster than the AR Gemma baseline** [sourced]. (The widely repeated "Gemini Diffusion ~1,479 tok/s, ~5×" figure is the closed-model *Google I/O May 2025* demo number — ~13 months old, and misleading as a June-2026 headline.) Non-autoregressive serving is real but still cutting-edge, not table-stakes [inference].

**The economics that drive all of this.** *(Verifier correction applied — disentangle the two axes.)* On Blackwell + NVFP4, NVIDIA reports inference reaching ~**$0.02 per million tokens** on GPT-OSS-120B (confirmed via InferenceMAX / Baseten on B200) [sourced]. The cleaner way to read the gain is as **two distinct axes**: NVIDIA's canonical headline is a **~15× Blackwell-over-Hopper** improvement driven by native NVFP4 tensor cores, *plus* a separate **~5× cost reduction from software optimization** on gpt-oss-120b since launch. The loose "4.5–15×" range conflates these. FP8 self-hosting of 70B-class models lands near **$0.95–1.10/M tokens**, breaking even around 50–100M tokens/month [sourced]. **[advisory]** Read all per-token figures as NVIDIA marketing/InferenceMAX best-case on optimal hardware — directionally right, not a quote for your own deployment.

**Who leads, structurally:** NVIDIA, decisively, on hardware — Blackwell's native FP4 made the format real, and NVIDIA seeds the ecosystem (TensorRT-LLM, the NVFP4 format, QAD recipes, Edge-LLM); AMD (ROCm) and Huawei (CloudMatrix384) are the credible alternatives. vLLM/SGLang/TensorRT-LLM are the de-facto serving standard. DeepSeek set the MTP template; the closed labs (OpenAI, Anthropic, Google) run heavily optimized proprietary stacks with details mostly undisclosed [inference].

---

## 7. Learning path for a technical leader

*You're leading, not implementing — so this is concepts, judgment, and how to tell a real expert from a fluent talker.*

### Mental models (the load-bearing seven)

- **MM1 — Inference is memory-bound at low batch.** The GPU spends most of its time moving weights, not doing math. This one fact explains both techniques: quantization moves fewer bits; speculation spends the idle math on verification.
- **MM2 — Two regimes: latency-bound vs throughput-bound.** Small batch → memory-bound → both shine. Large batch → compute-bound → speculation's benefit *shrinks or reverses*. A leader's first instinct: *"what's our batch regime?"*
- **MM3 — Speculative decoding is guess-and-verify, and it is lossless.** Pure speed play, zero accuracy cost. The only question is whether it actually saves time.
- **MM4 — Quantization is a quality-vs-cost trade; speculation is not.** "What precision?" is never free — it's a risk decision.
- **MM5 — Acceptance length is the one number that decides speculative decoding.** ~1 useless; 3–5+ a big win. Every advance (EAGLE, MTP) is a fight to raise it, especially as contexts grow.
- **MM6 — Scale (the scaling factor) is where quantization lives or dies.** You divide a block of numbers by a shared scale before rounding. Block size + scale precision is the whole ballgame — exactly what separates NVFP4 from MXFP4.
- **MM7 — Mixed precision is the real answer.** Sensitive parts (attention, KV cache) high; bulk weights at the lowest precision that survives. "What precision?" really means "which part, at which precision?"

### Reading spine (few, high-value — read framing fully, skim papers for figures and "when it fails")

- **EAGLE-3.1 announcement** — vLLM blog, May 2026. Clearest current statement of where drafting stands. https://vllm.ai/blog/2026-05-26-eagle-3-1
- **MTP explainer** — Sebastian Raschka. Best plain-language account of models drafting for themselves. https://sebastianraschka.com/llm-architecture-gallery/mtp/
- **MagicDec (part 2)** — canonical latency-vs-throughput / batch-size / long-context treatment (read for MM2). https://infini-ai-lab.github.io/MagicDec-part2/
- **"Introducing NVFP4"** — NVIDIA. Reference on two-level scaling and why 4-bit can be accurate now. https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/
- **NVFP4 vs MXFP4 decision guide** — Spheron. The choice a leader will be asked to make. https://www.spheron.network/blog/nvfp4-vs-mxfp4-gpu-cloud-4bit-quantization-guide/
- **Quantization-Aware Distillation for NVFP4** — NVIDIA Nemotron, 2026. Current method for recovering 4-bit quality. https://research.nvidia.com/labs/nemotron/nemotron-qad/
- **vLLM vs SGLang vs TensorRT-LLM (2026)** — read for how levers compose, not benchmark numbers (those rot). https://inferenceengineering.tech/learn/vllm-vs-sglang-vs-tensorrt-llm/

### Checkpoints — you understand it when you can…

- …explain to a CFO **why FP8 is nearly free but FP4 is a risk decision**, in two sentences, without the word "quantization." (MM4)
- …say **why speculation gives zero quality loss** but quantization might — and why that makes them *different kinds of decisions*. (MM3)
- …predict, for "high-traffic batch API" vs "low-latency coding agent," **which technique helps and which might hurt**. (MM2)
- …name **acceptance length** as the deciding metric and explain why long conversations and prompt-template changes threaten it. (MM5)
- …explain in one breath **why NVFP4 beats MXFP4** (smaller blocks, precise FP8 scale) without reciting bit-widths. (MM6)
- …describe **mixed precision** and give one example of a part you'd keep higher and why. (MM7)
- …explain why **models drafting for themselves (MTP)** removed the biggest practical blocker to speculative decoding.

### How to evaluate an expert (separate "operated in production" from "read about it")

- **"When does speculative decoding stop helping — or hurt?"** *Strong:* goes straight to batch size / compute-bound regime and acceptance rate; mentions measuring acceptance length on *their* traffic. *Red flag:* thinks it degrades output quality (it's lossless by construction).
- **"Where do draft models come from, and what changed this year?"** *Strong:* the spectrum — separate small model → grafted heads (Medusa/EAGLE) → native MTP heads shipped with the model; knows EAGLE-3 is standard and 2026's shift is self-drafting. *Red flag:* picks a drafter with no idea whether its acceptance rate is good.
- **"FP8 vs FP4 — what do you deploy, and how do you decide?"** *Strong:* "FP8 safe default, ~2×; FP4 a deliberate quality risk taken only with distillation-recovery and mixed precision, validated on hard tasks; needs Blackwell to pay off." *Red flag:* believes 4-bit is free/lossless, or quotes one benchmark as proof of safety.
- **"NVFP4 vs MXFP4 — why does it matter?"** *Strong:* block size + scale precision. *Red flag:* doesn't know what a scaling factor or block is.
- **"Quantize the KV cache?"** *Strong:* "FP8 KV cache is nearly free and standard; below FP8 I get cautious," connected to context length and concurrency. *Red flag:* doesn't know what the KV cache is (disqualifying for a serving role).
- **Cross-cutting red flags:** quotes benchmark numbers as eternal truths (they rot monthly); conflates the two techniques' risk profiles; can't name a failure mode for anything they advocate; all vocabulary, no mechanism; never mentions measuring on their *own* traffic.

### The 60-second version

Two levers — cheaper tokens (quantization) + more tokens per step (speculation) — that stack. Speculation is lossless, worth it at low batch, scored by acceptance length; 2026's shift is **models drafting for themselves (MTP)**. Quantization: **FP8 is the safe default**; FP4 (**NVFP4**) is a deliberate risk taken with distillation-recovery + mixed precision on Blackwell; **MXFP4** is the coarser, more portable cousin. Quantize the KV cache to FP8 — often the cheapest big win. Leadership reflex: characterize the workload, pull safe levers first, gate every aggressive choice with a quality check on your *own hard tasks*.

---

## 8. Team notes

*Org/hiring lens for a leader deciding who owns this, build-vs-buy, and how it breaks.*

### Roles & seniority

**The single most important org fact [advisory]:** both levers are now *features inside the serving frameworks*, not research you build. vLLM, SGLang, and TensorRT-LLM all ship EAGLE-3 and quantization out of the box [sourced]. For most companies this is a *configuration, calibration, and evaluation* job — not a kernel-writing job.

**Default answer: an existing role absorbs this.** A mid-to-senior **ML Infrastructure / Inference Engineer** (or a strong platform engineer who already owns your serving stack) can own both: pick the engine, enable the flag, calibrate a quantization recipe, build an eval harness, watch the dashboards.

| Situation | Who you need | Seniority |
|---|---|---|
| Serve open-weight models on your own GPUs, inference is a top-3 cost line | Dedicated **Inference / ML Systems Engineer** | Senior |
| Need custom kernels / engine modifications / latency the framework can't hit | **GPU/CUDA performance engineer** | Senior → Staff/Principal; rare, expensive |
| Only call a managed/frontier API | **Nobody** — it's the provider's job | n/a |

**[advisory] Hiring rule:** resist hiring a CUDA specialist as your *first* move. Companies that genuinely need FlashAttention-class kernel work are few — mostly the inference providers and NVIDIA. If your draft isn't accepting tokens, the fix is almost always a better-matched draft or a config change, not a hand-tuned kernel. Hiring Staff-level GPU talent to operate a vLLM flag is a classic over-hire.

### Hiring signals (what "good" looks like)

- **Talks in the right numbers:** acceptance rate, tokens/sec, time-to-first-token vs inter-token latency, throughput at a *stated concurrency*. "Speculative decoding gives 3×" without "on what workload, batch, acceptance rate?" is a tell.
- **Treats quantization as an evaluation problem, not a download:** demands a task-specific eval set; talks about *which layers* are sensitive and mixed precision (4-bit weights, FP8/BF16 attention).
- **Has engine opinions tied to workload:** vLLM for fast iteration and model churn; TensorRT-LLM for a fixed model where peak throughput matters (compile cost, NVIDIA lock-in); SGLang when requests share long prefixes (system prompts, RAG context).
- **Knows the draft matters more than the trick:** the whole game is the draft predicting the target on *your* traffic.

### Red flags

- **"Speculative decoding changes output quality."** It doesn't, by construction — conflating it with quantization's quality hit means they don't understand the mechanism.
- **Quotes one headline speedup as universal.** The 2–4× is workload-dependent.
- **Wants to build a custom serving engine from scratch.** Almost never justified in 2026 outside companies whose product *is* inference.
- **No eval/regression harness.** If they can't say how they'd *catch* a quality drop after enabling FP4 or pushing a new draft, they'll ship the regression.
- **Treats it as one-time setup.** Both levers drift.

### Build vs. buy

**Default to rent/buy — the "build" surface is mostly already built into free open source.**
1. **Calling a frontier/managed API (Anthropic, Together, Fireworks, Baseten):** **buy.** The provider does both for you.
2. **Serving open weights, moderate volume:** **adopt** OSS (vLLM/SGLang/TensorRT-LLM) and flip the flags — configuration, not building. You contribute calibration and eval, not the engine.
3. **Self-host only when scale justifies it.** Self-hosting on rented H100s can land near ~$0.75/1M tokens [sourced], but only at predictable, high, sustained volume — and assumes you have the engineer. The reported sweet spot is a **hybrid** stack (managed for spiky/long-tail, self-host for steady high volume), with teams citing 40–70% savings vs all-API.

**When is *owning* the acceleration a real moat?** Almost never for an application company. Only if inference cost/latency *is* your core product economics — i.e., you *are* an inference provider, or serve at a scale where a 15% throughput edge is millions. For everyone else, the moat is your product; the acceleration is plumbing best rented [advisory].

### Failure modes

1. **Draft–verifier distribution mismatch (the #1 silent killer).** Draft trained on data that doesn't match live traffic → acceptance quietly drops, your "3×" becomes "1.2×" with no error thrown [sourced — Nebius; arXiv 2602.06932]. *Mitigation:* monitor acceptance rate as a first-class metric; re-tune the draft on real traffic.
2. **Over-quantizing the draft.** Squeezing the *draft* too hard tanks acceptance and eats the speedup. Tune the two techniques together, not separately.
3. **Shipping FP4 without a quality gate.** FP8 is the safe default (0.5–2%); 4-bit is newer, less forgiving, tooling still maturing. Teams that flip to full-FP4 and skip task-specific evals discover the regression in user complaints, not dashboards.
4. **"It helps everyone" — gains evaporate at high batch.** Speculation shines at low batch; under heavy batching it can go net-negative.
5. **Weight-push instability.** Frequent model/draft updates cause cache invalidation, latency jitter, transient regressions [sourced — arXiv 2602.06932].
6. **Conflating the two and assigning blame wrong.** When quality drops, teams can't tell if it was the (lossless) speculative layer or the (lossy) quantization. Without separate eval gates per lever, debugging is guesswork. Notably, public speculation around the spring-2026 Claude Opus 4.7 quality-regression reports centered on exactly these serving-side knobs — quantization, routing, speculative-decoding aggressiveness — illustrating how invisible and contested these changes are even at top labs (the vendor did not confirm any cause) [sourced — ofox.ai].

### One-paragraph recommendation [advisory]

Don't create a new role. If you call an API, it's the provider's problem — buy. If you self-serve open weights, make it an explicit responsibility of your existing senior inference/ML-infra engineer: adopt vLLM/SGLang/TensorRT-LLM, default to FP8, gate every precision change behind a task-specific eval set, and instrument *acceptance rate* and *quality* as standing dashboards. Reserve a CUDA/kernel specialist for the rare case where you are genuinely inference-cost-bound at scale — and recognize that hiring one to babysit a config flag is the most common over-hire in this area.

---

### Honest limits of this report

- Frontier *closed* labs (OpenAI, Anthropic, Google) don't publish their serving recipes; production-adoption claims lean on open frameworks, NVIDIA, and vendor reporting plus inference. Treat specific internal-deployment details as directional, not confirmed [advisory].
- GPU-hour→dollar conversions are my arithmetic on public rates [inference].
- Acceptance-rate and throughput numbers are model- and workload-specific; your mileage varies with your traffic distribution — which is precisely the variable that decides whether speculative decoding pays off for you [advisory].

---

## Sources

- EAGLE-3.1 announcement — vLLM blog, 2026-05-26. https://vllm.ai/blog/2026-05-26-eagle-3-1
- EAGLE-3 (NeurIPS 2025) — openreview.net.
- vLLM P-EAGLE blog. https://vllm.ai/blog/p-eagle
- AWS P-EAGLE. https://aws.amazon.com/blogs/machine-learning/p-eagle-faster-llm-inference-with-parallel-speculative-decoding-in-vllm/
- "Speculative Decoding: Performance or Illusion?" — arXiv 2601.11580. https://arxiv.org/pdf/2601.11580
- "Batch Speculative Decoding Done Right" — arXiv 2510.22876. https://arxiv.org/pdf/2510.22876
- LongSpec — arXiv 2502.17421. https://arxiv.org/pdf/2502.17421
- Together AI — long-context speculative decoding. https://www.together.ai/blog/speculative-decoding-for-high-throughput-long-context-inference
- "Introducing NVFP4" — NVIDIA. https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/
- NVIDIA Nemotron Quantization-Aware Distillation report, 2026. https://research.nvidia.com/labs/nemotron/nemotron-qad/
- "Quantization Meets Reasoning" — arXiv 2501.03035 (W4A16 / W4A4 reasoning-degradation magnitudes).
- "Give Me BF16 or Give Me Death" — arXiv 2411.02355 (FP8 near-lossless).
- DeepSeek quantization analysis — arXiv 2505.02390. https://arxiv.org/pdf/2505.02390
- VRLA quantization / precision guides, 2026. https://vrlatech.com/llm-quantization-explained-int4-int8-fp8-awq-and-gptq-in-2026/ ; https://vrlatech.com/fp4-vs-fp8-vs-fp16-for-llm-inference-which-precision-should-you-use/
- Spheron — FP4 on Blackwell, EAGLE-3, NVFP4-vs-MXFP4, engine comparison, 2026. https://www.spheron.network/blog/nvfp4-vs-mxfp4-gpu-cloud-4bit-quantization-guide/ ; https://www.spheron.network/blog/vllm-vs-tensorrt-llm-vs-sglang-benchmarks/
- edge-ai-vision — NVFP4 accuracy/throughput (Llama-2 7B/70B).
- Mirantis 2026 — combined cost-reduction back-of-envelope.
- DiffusionGemma (open weights, Apache 2.0, 2026-06-10) — current diffusion-LLM SOTA, superseding the May-2025 Gemini Diffusion demo figure.
- DeepSeek-V3 — public FP8 training; MTP-1 self-speculation.
- premai — speculative decoding 2–3× faster, 2026. https://blog.premai.io/speculative-decoding-2-3x-faster-llm-inference-2026/
- Nebius — MoE speculative decoding. https://nebius.com/blog/posts/moe-spec-decoding
- arXiv 2602.06932 — draft-mismatch / weight-push instability, 2026. https://arxiv.org/html/2602.06932v2
- BentoML — speculative decoding handbook. https://bentoml.com/llm/inference-optimization/speculative-decoding
- Fireworks / Baseten / Zencoder / Northflank — 2026 self-hosting cost analyses.
- ofox.ai — Claude Opus 4.7 production-reliability discussion, 2026 (vendor unconfirmed). https://ofox.ai/blog/claude-opus-4-7-production-reliability-fix-2026/
- NVIDIA InferenceMAX / Baseten — GPT-OSS-120B ~$0.02/M tokens (B200); Blackwell-vs-Hopper ~15× (hardware) and ~5× (software) as distinct axes.
