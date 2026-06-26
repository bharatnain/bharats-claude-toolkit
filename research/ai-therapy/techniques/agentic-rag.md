# Agentic RAG (planning, multi-hop, self-correcting retrieval)

*A chapter for a technical leader who will fund, staff, and evaluate this work — not write the code. Claims are labeled **sourced** (with a URL and access date), **inference** (my reasoning from those sources), or **speculation** (forward-looking judgment). Learning-design and org recommendations are labeled **advisory** — my reasoned read, not a citation. Current as of June 2026.*

---

## 1. What it is

Ordinary RAG — retrieval-augmented generation — is a straight line. Take the user's question, fetch the few text chunks that look most similar to it from a database, paste them into the prompt, generate an answer. One lookup, one shot. It works beautifully when the answer sits in one obvious place.

It breaks the instant a question needs **chaining**. *"Which university did the director of the highest-grossing 1997 film attend?"* No single document holds that answer. You have to learn the film first (Titanic), then its director (James Cameron), then his school (Fullerton College). Each answer is the input to the next search. That is a **multi-hop** question, and one similarity lookup cannot solve it — because the document naming Cameron's university looks nothing like the words in the original question. *(sourced — [jobsbyculture, 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026); the Titanic/Cameron/Fullerton chain is factually correct.)*

**Agentic RAG wraps the retrieval step inside a loop the model runs itself.** Instead of fetching once, the model is given search (and often web lookup, SQL, a calculator) as **tools it can call repeatedly**, and it controls the sequence: decide what to fetch, fetch it, judge whether it was any good, fetch again if not, throw away weak evidence, and verify before answering. It keeps looping until satisfied — or until it hits a hard cap. *(sourced — [jobsbyculture, 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026); [freeacademy.ai, 2026](https://freeacademy.ai/blog/agentic-rag-ai-agents-supercharge-retrieval-2026))*

Three capabilities define it:

- **Planning / decomposition** — break a compound question into ordered sub-questions before retrieving anything.
- **Multi-hop retrieval** — iterate retrieve → reason → retrieve, feeding each hop's finding into the next search.
- **Self-correction** — grade the evidence; if it's weak or off-target, rewrite the query, switch sources, or abstain — rather than confidently answering from garbage.

By mid-2026, practitioner guides call this "the default pattern" for hard question-answering and the engine inside "deep research" products. *(sourced — [freeacademy.ai, 2026](https://freeacademy.ai/blog/agentic-rag-ai-agents-supercharge-retrieval-2026))* But the single most important caveat in this whole chapter comes right here, and it is the mark of a mature team: **the production answer is not "use it everywhere." It is "route to it only when it's needed."** More on that in section 2.

---

## 2. How it works — the gears turning

### The core loop (ReAct is the ancestor, not the current workhorse)

The conceptual backbone is **ReAct** — "Reason + Act" (Yao et al., 2022). The model writes an interleaved trace:

```
Thought:  I need the director of the 1997 highest-grossing film.
Action:   search("highest-grossing 1997 film")
Observation: "Titanic, directed by James Cameron..."
Thought:  Now I need where James Cameron studied.
Action:   search("James Cameron university")
Observation: "...attended Fullerton College..."
Thought:  I have the chain. Answer.
Answer:   Fullerton College.
```

Each loop iteration is at least one model call (the Thought/plan) plus one tool call (the Action). The model literally writes its next search as text, a tool runs it, the result is pasted back as an "Observation," and the model reads it and decides the next move. *(sourced — [jobsbyculture, 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026))*

A precision note worth carrying into vendor conversations: **ReAct is the idea everyone descends from, but it is increasingly not the literal mechanism running in production.** By mid-2026 the dominant patterns are reasoning-model-native tool-calling loops (the o-series / R1 style, where the model calls tools as a trained reflex rather than emitting a hand-formatted text trace) and graph-structured plan-execute orchestration (LangGraph-style state machines). *(inference, from the body of 2026 sources)* If an expert describes their system as "a literal ReAct text loop," that is a slightly dated framing — the substance is right, the vintage is 2023.

That cap matters: practitioners typically **cap at ~3 iterations**, because cost and latency multiply with every round. *(sourced — [jobsbyculture, 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026))*

### The self-correction gear (Corrective RAG / Self-RAG)

A naive loop will happily reason over irrelevant junk. Two named mechanisms stop it:

- **Corrective RAG (CRAG)** inserts a **retrieval evaluator** that grades each retrieved document *before* it's used. In the original design the grader is a fine-tuned **T5-large model (~0.77B parameters)** that scores documents on a confidence scale (roughly −1 to 1) and picks one of three actions — **Correct** (refine the good evidence into "knowledge strips"), **Incorrect** (discard it and fall back, classically to a web search), or **Ambiguous** (combine both). The common one-line summary — "score below a threshold triggers a web-search fallback" — is directionally right but flattens a three-way decision into a binary. *(sourced — [Analytics Vidhya, 2024](https://www.analyticsvidhya.com/blog/2024/12/corrective-rag/))*

- **Self-RAG** fine-tunes the model to emit special **reflection tokens** that gate the flow. It decides on demand *whether to retrieve at all*, tags retrieved passages `IsRELevant?`, and tags its own draft `IsSUPported by evidence?` and `IsUSEful?`. Retrieval becomes on-demand rather than always-on, and the model is trained to notice when its own answer isn't grounded. *(sourced — [LangChain blog](https://www.langchain.com/blog/agentic-rag-with-langgraph))*

In production with off-the-shelf models, teams **approximate** Self-RAG without fine-tuning: wrap each step in an evaluation prompt — "is this relevant? is the answer grounded?" — and force a **structured JSON output** (`{"is_relevant": false}`) that programmatically gates the next step. *(sourced — [freeacademy.ai, 2026](https://freeacademy.ai/blog/agentic-rag-ai-agents-supercharge-retrieval-2026))*

### The router gear (Adaptive RAG) — the 2026 production reality

The single most important *current* shift: don't run the expensive loop on every query. **Adaptive RAG** puts a cheap **classifier in front** that routes:

- trivial / already-known → answer directly, skip retrieval;
- single-hop fact → plain one-shot RAG;
- genuine multi-hop → the full agentic loop.

This is described as the de facto production best practice for mixed-complexity workloads, precisely because **~60–70% of real enterprise queries are simple enough for single-hop or direct answers** — paying the agentic tax on all of them wastes money and adds latency for zero accuracy gain. *(sourced — [jobsbyculture, 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026); [datanucleus, 2026](https://datanucleus.dev/rag-and-agentic-ai/agentic-rag-enterprise-guide-2026))*

A counter-intuitive finding from 2026 routing research: cheap **keyword (TF-IDF) features predict query complexity better than fancy semantic embeddings** — surface patterns are surprisingly strong signal. And routing difficulty varies by domain: **medical queries are the hardest to classify correctly, legal the most tractable.** *(sourced — routing research summarized in [jobsbyculture, 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026) and the adaptive-routing literature)*

### The frontier gear (RL-trained search agents)

The biggest research-to-product movement since 2025 is **teaching the model itself to search well via reinforcement learning**, instead of hand-wiring the loop with prompts.

- **Search-R1** and **R1-Searcher** were the first open search agents trained with RL where the *only* reward is "did you get the final answer right." The model learns on its own when to fire a search and how to weave results into step-by-step reasoning. A key trick is **retrieved-token masking** — you don't let the gradient train the model to *generate* the retrieved text, only to *use* it, which keeps training stable. Search-R1 reported a **~41% improvement** over RAG baselines on a 7B Qwen2.5 model across seven QA datasets. *(sourced — [Search-R1, arXiv 2503.09516](https://arxiv.org/abs/2503.09516); [R1-Searcher, arXiv 2503.05592](https://arxiv.org/pdf/2503.05592))*

- The intuition: a prompted ReAct agent uses a model that was never *trained* to be a good searcher — it's improvising. RL search agents are *optimized* end-to-end so that good search behavior (when to query, how to phrase it, when to stop) emerges from rewarding correct final answers. *(inference)* Successors through 2026 push on efficiency — **FrugalRAG** matches strong multi-hop accuracy while training on only **~1,000 examples** and roughly **halving the number of retrievals**. *(sourced — [FrugalRAG, arXiv 2507.07634](https://arxiv.org/pdf/2507.07634))*

---

## 3. Why it works — and why the naive alternative fails

**The principle: a single retrieval can only match against words the user already gave you.** Vector search finds documents similar to the *question*. In a multi-hop question, the bridge facts (Titanic, Cameron) **aren't in the question** — so the document holding the final answer (Cameron's university) isn't "similar" to the original query and won't be retrieved. One-shot RAG fails not because the database lacks the answer, but because it can't form the *intermediate query* that would surface it. *(inference, grounded in the multi-hop definitions in [jobsbyculture, 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026))*

The loop fixes this structurally: **each hop converts a retrieved fact into the search terms for the next hop.** The agent generates the query the user couldn't. That is the whole game.

**Why self-correction is non-negotiable.** The failure mode of plain RAG isn't "no answer" — it's a *confident wrong answer* built on irrelevant retrieved text. A grading/abstention step (CRAG's evaluator, Self-RAG's `IsSUP` token) is what stops the model reasoning over garbage. That is why the technique concentrates in legal, medical, and financial QA, where a grounded-or-abstain guarantee is worth the cost. *(sourced — [jobsbyculture, 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026))*

**Why it earns its keep — the numbers (carefully stated).** A DSPy-style ReAct agent has been reported to move a complex task from roughly 24% to 51% accuracy. *(sourced — [freeacademy.ai, 2026](https://freeacademy.ai/blog/agentic-rag-ai-agents-supercharge-retrieval-2026))* And in deep-search research, an iterative-evidence framework (EvidenceLoop) improved Pass@1 from **20.0% to 25.0% (+25% relative)** on the WebDetective benchmark, with even frontier models capping near ~50% Pass@1 — a reminder that iteration helps but does not "solve" hard retrieval. *(sourced — [Demystifying deep search, arXiv 2510.05137](https://arxiv.org/pdf/2510.05137))* (An earlier draft of this material cited a "25.5/50 vs 19/50, ~34% gain" figure for this paper; those numbers do not appear in the source and have been removed — the correct figure is 20.0%→25.0%.)

**Why "just use a bigger context window" fails.** Even with a huge context, you still have to *find* the right documents to dump in, and the bridge-fact problem means one search won't find them. Reasoning quality also degrades when you bury a model in mostly-irrelevant text. The agentic loop is a *search strategy*, not a bigger bucket — it targets evidence rather than hoarding it. The current bottleneck is **retrieval, not generation**: models are fast; finding the right evidence is the hard part. *(sourced — [jobsbyculture, 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026))*

**The cost of why-it-works.** Every loop is more model calls and more tool calls, so cost and latency compound:

| Pattern | Cost/query | Latency |
|---|---|---|
| Naive RAG | ~$0.001 | <1 s |
| Advanced RAG | ~$0.005 | 2–3 s |
| **Agentic RAG** | **$0.01–0.05** | **5–15 s** |

Agentic workflows burn roughly **3–10× the tokens** of one-pass RAG (Gartner's March 2026 figure cites **5–30×** tokens vs. a standard chatbot turn). *(sourced — [jobsbyculture, 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026); [datanucleus, 2026](https://datanucleus.dev/rag-and-agentic-ai/agentic-rag-enterprise-guide-2026))* This multiplier is the entire reason Adaptive routing exists.

---

## 4. People & resources

There are **two very different cost worlds** here. Don't conflate them.

### A) Building an agentic RAG *application* (the common case — you orchestrate existing models)

- **Team & time:** small. Practitioner guides put a production RAG build at roughly **$8K–$50K over 3–16 weeks**. A capable team is **~2–5 engineers** (retrieval/infra, orchestration, evaluation, plus a domain expert) — the dollar/week figures are sourced; the headcount is **inference** from the listed skill stack, not a published number. *(sourced for $/weeks — [MarsDevs, 2026](https://www.marsdevs.com/guides/agentic-rag-2026-guide); team size — advisory/inference)*
- **Skill stack (real, named):** Python; **LlamaIndex** (retrieval infra — chunking, hybrid search, re-ranking); **LangGraph** (the agent state machine, checkpointing, human-in-the-loop); a vector database; an eval framework (**Ragas**, with production targets like faithfulness ≥0.9, context precision ≥0.8); and trajectory tracing (**Arize Phoenix / Langfuse / LangSmith**) so you can debug *what the planner did wrong*, step by step. *(sourced — [jobsbyculture, 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026))*
- **The hidden cost everyone underestimates:** maintaining orchestration logic + embedding pipeline + vector store + eval + monitoring. Teams **underestimate this by 2–3×.** Running costs sting too: at Uber, monthly LLM API spend ran **$500–$2,000 per engineer.** *(sourced — search synthesis of [MarsDevs, 2026] and [Cockroach Labs, 2026](https://www.cockroachlabs.com/blog/agentic-ai-costs-at-scale/))*
- **Data scale:** no training data needed — a **clean document corpus plus a labeled eval set** (a few hundred question→expected-answer pairs is enough to gate quality). *(advisory)*

### B) *Training* a custom RL search agent (the frontier case — Search-R1 / FrugalRAG style)

Dramatically cheaper than people assume, because it's post-training a small open model, not pre-training one:

- **Data:** Search-R1 trained on **~90K samples**; FrugalRAG hit competitive multi-hop accuracy with **~1,000 examples** — orders of magnitude below pretraining corpora. *(sourced — [Search-R1](https://github.com/PeterGriffinJin/Search-R1); [FrugalRAG, arXiv 2507.07634](https://arxiv.org/pdf/2507.07634))*
- **Compute:** related RL-search projects report a few hundred GPU-hours; small agents trained on 16–32 H100s. At ~$2/H100-hour on-demand, a comparable post-train lands in the **low-thousands to low-tens-of-thousands of dollars**. *(inference, from the GPU-hour figures in the RL-search literature; the exact dollar mapping is my arithmetic, not a published number)*
- **Team:** a small research/ML group using open frameworks (veRL, GRPO/PPO). *(inference)*

**Bottom line.** Building the *app* is a small-team, weeks-long, low-five-figures effort dominated by retrieval quality and eval discipline. Training a *custom* search agent is a low-five-figures GPU run on ~1K–90K examples. Neither is a frontier-lab-scale undertaking — the expensive part is the base model you build on, which you rent rather than train. *(advisory)*

---

## 5. Scenarios & stories

The whole art is spending the agentic premium only where it buys you something.

### Where it's the RIGHT tool

**Story 1 — the acquisition that lives in twelve documents.** A lawyer asks: *"In the Meridian deal, does the indemnification cap survive the change-of-control provision, and does that interact with the earn-out schedule?"* No single section answers this. The cap is in the purchase agreement; the change-of-control language is in a side letter; the earn-out is in a third schedule cross-referencing a definition buried in the master agreement. One-shot retrieval grabs the indemnification clause and stops — it misses the side letter entirely, because the side letter never uses the word "indemnification." Agentic RAG retrieves the cap, *notices* it references a defined term, fetches that definition, sees it points to change-of-control, retrieves the side letter, and only then synthesizes. The model can only know it needs hop #3 *after* reading hop #2. *(inference, from the multi-hop framing in the sources)*

**Story 2 — the support question that depends on the customer's own state.** *"Why did my export fail this morning?"* A naive bot recites the generic troubleshooting article. The real answer: this customer is on the legacy plan, exports over 2GB are throttled there, and that limit lives in a different doc section. Agentic RAG plans — find the plan tier, look up the export limit for that tier, check whether this export hit it — and returns "your 2.3GB export exceeded the 2GB cap on the Starter plan." The right documents only become identifiable *after* the system gathers context. *(inference)*

**Story 3 — the analyst who needs an answer that's actually true.** Summarizing a company's debt covenants across three years of filings. Here self-correction matters most: require that **every claim cite a specific source chunk by ID**, and flag any uncited claim for review. This single discipline is reported to eliminate most "synthesis hallucinations" — where a model glues a real party name from one document to a fabricated figure from another and produces something that *sounds* sourced but isn't. (A real 2026 incident: a legal assistant cited "Johnson v. Meridian Holdings, 2023 WL 456789" — a case that didn't exist, stitched from a real name and a fake docket number.) *(sourced — [Towards Data Science failure-modes piece, 2026](https://towardsdatascience.com/agentic-rag-failure-modes-retrieval-thrash-tool-storms-and-context-bloat-and-how-to-spot-them-early/))*

### Where it's the WRONG tool

**Story 4 — the FAQ bot that took five seconds to say "9am to 5pm."** A company wired agentic RAG into its store-hours/return-policy chatbot because it was the impressive new thing. These questions have one answer in one place — no second hop, nothing to self-correct. Every "what time do you open?" now triggers a planning call, a retrieval, an evaluation call, and sometimes a needless re-retrieval: **~10× the cost and several extra seconds** for a question a single fetch (or a hardcoded string) answered perfectly. Since **60–70% of enterprise queries are this simple**, paying agentic prices on all of them is the most common waste in the field. *(sourced — [jobsbyculture, 2026](https://jobsbyculture.com/blog/agentic-rag-guide-2026))*

**Story 5 — the autocomplete that can't afford to think.** A dev-tools team wanted retrieval-grounded code suggestions inline as you type. Inline completion has a latency budget of tens of milliseconds; the agentic planning loop measures in *seconds*. By the time the agent "planned its retrieval," the developer had typed three more lines. The technique's defining feature — taking more steps — is exactly what a hard real-time ceiling forbids. *(inference, grounded in the latency table in section 3)*

**Story 6 — the retrieval that thrashed itself into a loop.** A team pointed agentic RAG at a knowledge base that simply didn't contain the answers to a class of questions. The agent searched, found nothing good, rewrote the query, searched again, rewrote again. In 2026 this has a name — **retrieval thrash** — alongside its cousins *tool storms* and *context bloat* (stuffing every mediocre chunk into the window until quality collapses). One user query spun fourteen retrievals and a multi-dollar bill before timing out. The fix the field settled on is blunt: **cap retries at two or three, then refuse or escalate to a human.** When the answer isn't in the corpus, self-correction has nothing to correct toward — it just burns money. *(sourced — [Towards Data Science failure-modes piece, 2026](https://towardsdatascience.com/agentic-rag-failure-modes-retrieval-thrash-tool-storms-and-context-bloat-and-how-to-spot-them-early/))*

### The decision rule (advisory)

Reach for agentic RAG when **all three** hold: the answer is spread across multiple sources; the next thing to look up is only knowable after reading the last thing; and a wrong answer is expensive enough to justify seconds of latency and 5–10× the cost. If your queries are single-fact, latency-critical, or your corpus might not contain the answer — don't. And if your traffic is a *mix* (it almost always is), **don't pick one — route.** Whatever you build, cap the retry loop at 2–3 and force a citation per claim, because in 2026 hallucination in RAG is not solved — it's *managed*, and those two guardrails are what manage it.

---

## 6. Cross-industry usage & positioning (as of June 2026)

**The one-line framing:** agentic RAG is **table-stakes as a capability your stack must support, but cutting-edge in how cheaply and selectively you deploy it.** *(inference)*

### On the maturity curve

**Commodity / table-stakes in 2026:** hybrid retrieval (vector + keyword + rerank) as the substrate; a "is this grounded?" self-correction check before answering; query routing by complexity (Adaptive RAG); citations with source-grounding in any regulated deployment.

**Still differentiating:** RL-trained retrieval agents (Search-R1 and descendants); graph + agentic hybrids doing real multi-hop relationship traversal at scale; deep-research agents running dozens-to-hundreds of retrieval steps; robust evaluation of multi-step pipelines (every intermediate step can fail independently); and **security hardening against retrieval-targeted attacks** (poisoning, injection via retrieved content). *(sourced/inference)*

### Sector by sector

- **Legal — leading edge, high adoption.** Legal questions are inherently multi-hop (cross-referencing statutes, cases, filings, clauses). **Harvey** — which, per its own materials and the Sacra report, serves **~50% of the Am Law 100** (1,000–1,300+ customers across 60 countries; some sources note 70%+ of the Am Law *10* specifically, which is likely the origin of inflated "97%" figures elsewhere) — runs the agentic pattern: structured document retrieval, live court-filing APIs, knowledge-graph cross-referencing. A hallucinated citation here is a malpractice risk, so self-correction is non-negotiable. *(sourced — Harvey/Sacra 2026 materials; this corrects an earlier "97% of the Am Law 100" claim, which was roughly 2× too high)*
- **Finance — leading edge, high adoption.** **Hebbia** built a distributed orchestration engine specifically because the hard problem is retrieval over *private, offline* documents where the answer is often inferred across many sources — the canonical multi-hop case. Finance and legal are repeatedly named together as where the extra cost is justified "because accuracy is non-negotiable." *(sourced)*
- **Coding / dev tools — table-stakes and invisible.** Arguably the most mature everyday use, though rarely branded "RAG." Coding agents (the Claude Code / Cursor / Augment generation) increasingly do **agentic codebase search** — iteratively grep/read/trace dependency graphs rather than pre-embedding everything. The agent decides what to read next based on what it just found: that *is* planning + multi-hop retrieval, applied to source code. *(sourced/inference)*
- **Customer support — table-stakes, high commercial stakes.** Contact-center vendors made agentic RAG mainstream. **Decagon** (~$4.5B valuation, Jan 2026; claims ~80% average deflection) frames it as end-to-end resolution; **Sierra** ($15.8B valuation, May 2026 Series C) positions around enterprise trust and governance. It earns its keep on genuinely multi-hop questions ("my order shipped but tracking is wrong and I was double-charged"). *(sourced — vendor valuations and figures; deflection % is a vendor claim, treat as indicative)*
- **Healthcare — pivotal but still mostly pilot.** Frontier models now **match or exceed human experts on medical licensing and clinical-reasoning *benchmark tasks***, and agentic systems retrieve real-time guidelines + literature + EHR history to support diagnosis. (I've deliberately scoped this to *benchmark* performance — the same literature is candid that most deployment is still proof-of-concept, and benchmark parity is not clinical equivalence.) The gap is prospective clinical trials and trustworthy data substrates. *(sourced/inference, softened per verifier)*
- **Science / R&D — fast-rising.** Microsoft's **GraphRAG now ships inside Microsoft Discovery**, an agentic platform for scientific research on Azure — a signal that graph+agentic retrieval is going from paper to product. *(sourced)*
- **Defense / security — dual character.** Both a tool for multi-source intelligence synthesis *and* a security problem: because these agents call tools, execute code, and can modify databases, the field is shifting from "content security" to **"behavioral security,"** with 2026 surveys cataloguing retrieval-poisoning and injection attacks. *(sourced/inference)*
- **Consumer — table-stakes via deep research.** For ordinary users, agentic RAG arrives packaged as **Deep Research** in ChatGPT, Claude, and Gemini; most users don't know the term.

### State of the art

- **Commercial deep-research agents** are the flagship consumer/prosumer form — all three frontier labs ship GA products that plan a research strategy, issue dozens of searches, read full pages, track gaps, iterate, and produce a cited report. The vendor product names referenced in the source material (e.g. "Claude Deep Research," "Claude Cowork," OpenAI/Gemini "Deep Research") are consumer-surface marketing names rather than API surfaces; I verified the **underlying API/standards layer** ([MCP](#)) but treat the specific product-name-plus-date claims as **sourced to the vendor announcements, not independently re-verified here.** *(sourced/advisory caveat)*
- **MCP (Model Context Protocol)** is the standard plumbing connecting agents to retrieval sources. It was **donated to the Linux Foundation's Agentic AI Foundation on Dec 9, 2025** (co-founded by Anthropic, Block, and OpenAI, with Google support) — confirmed against current Anthropic reference material. *(sourced — confirmed via the Anthropic claude-api skill reference, June 2026)*
- **The research frontier is RL-trained retrieval** (Search-R1 lineage, FrugalRAG), and **Graph RAG got cheap** — indexing that cost ~$33K on large corpora in 2024 has been cut 50–6,000× by LazyGraphRAG / LightRAG / Fast GraphRAG, making hybrid (vector for precision + graph for relationship expansion) the production consensus. *(sourced)*
- **Evaluation is the acknowledged hard problem.** Because a pipeline has many independently-failing steps, answer quality is the product of every step's reliability. The default stack pairs Ragas-style faithfulness/recall metrics with tracing (Phoenix, Langfuse), benchmarked on multi-hop suites (HotpotQA, 2WikiMultiHopQA, MuSiQue) and deep-research benchmarks like **BrowseComp-Plus** (a fixed ~100K-doc corpus, ACL 2026, that isolates retriever quality from agent quality). *(sourced)*

> **A note on low-confidence material.** The source package included provisional agentic-leaderboard standings naming specific models ("Claude Mythos 5 / Opus 4.8 / Gemini 3.5 Flash"). Those model IDs are real strings, but the standings come from a single benchmark aggregator and are self-flagged as provisional. I've kept them out of the body and flag them here as **speculation / low-confidence** — the right call.

---

## 7. Learning path for a technical leader

*Concepts, not code. For a leader who will direct, evaluate, and fund this — not write it.*

### Core mental models (the eight that matter)

1. **Retrieval is a decision, not a step.** The model *chooses* when and what to retrieve. That choice is what makes it "agentic."
2. **The loop is plan → retrieve → judge → correct.** After each retrieval it asks "relevant? complete?" and re-queries if not (CRAG, Self-RAG; in production, gated on structured output like `is_relevant: true/false`).
3. **Multi-hop = reasoning over a chain of lookups.** Hard questions need evidence no single search returns. This is the main reason to pay for agentic RAG.
4. **The accuracy ceiling splits roughly 60/40.** Retrieval quality explains ~60% of answer quality; how well the model *uses* what it retrieved is the other ~40%. A better vector DB cannot fix a *utilization* problem. *(sourced framing)*
5. **Adaptive routing beats one-size-fits-all.** A query classifier sends easy questions to cheap retrieval and reserves the agentic budget for genuinely hard ones. This is where the 2026 cost-accuracy win lives.
6. **Cost and latency scale with intelligence.** Naive ≈ $0.001/query; hybrid+rerank ≈ $0.005; agentic ≈ $0.01–0.05 and seconds of latency. The leader's job is deciding *which questions deserve it*.
7. **"Context engineering" is the new framing.** With million-token windows the constraint is no longer "can it fit" but "what *should* be in there." "Is RAG dead?" is the wrong question — RAG was absorbed into context engineering, not replaced. *(inference / 2026 framing)*
8. **Failures are finite and nameable.** ~Six recurring modes — bad retrieval, poor ranking, context overload, retrieval thrash, latency spirals, and the agentic-specific **bad synthesis** (stitching two unrelated chunks into a claim neither supports).

### Reading spine (six items, deliberately short)

1. **"Agentic RAG: A Survey"** (arXiv 2501.09136) — the canonical map and vocabulary.
2. **A 2026 "Is RAG Dead? / Context Engineering" piece** (Towards Data Science) — the best current framing. *(Source-hygiene note: the original curriculum cited a VentureBeat "retrieval-optimization spend rose 19%→28.9%" stat; the actual VB Pulse Q1'26 tracker reports buyer intent for **hybrid retrieval tripling from 10.3% to 33.3%** and retrieval optimization overtaking evaluation as the top investment priority. The directional claim is right; use the corrected numbers.)*
3. **Self-RAG (arXiv 2310.11511) + CRAG (arXiv 2401.15884)** — abstracts and figures only; the two patterns every vendor claims to implement.
4. **Search-R1** ([arXiv 2503.09516](https://arxiv.org/abs/2503.09516)) — what "trained to retrieve" actually means.
5. **A "How OpenAI/Gemini/Claude power Deep Research" explainer** — how the productized systems work end to end.
6. **A 2026 RAG-evaluation-metrics piece** — the failure taxonomy and production thresholds (faithfulness ≥0.9, answer relevancy ≥0.85, context precision ≥0.8).

### Understanding checkpoints — you understand it when you can:

- Explain to a CFO why a query costs $0.05 not $0.001, and which queries justify it.
- Whiteboard the plan→retrieve→judge→correct loop and point to where self-correction lives.
- Take a multi-hop question and explain why one vector lookup can't answer it.
- Say in one sentence what changes from advanced to agentic RAG: *the model gets control of the loop.*
- Explain why a better vector DB won't fix a context-utilization problem.
- Name three of the six failure modes and identify the one unique to agentic systems (bad synthesis across unrelated chunks).
- Decide GraphRAG vs. vectors vs. both for a use case — and give the *cost* reason GraphRAG isn't an automatic default.

### How to evaluate an expert in an interview

The goal is to separate someone who has *operated* this in production from someone who read the same blog posts. Probe for tradeoffs and scar tissue.

- **"When would you *not* use agentic RAG?"** Strong: reaches for cost/latency immediately, routes with a classifier, reserves agentic for hard multi-hop or high-stakes, names Adaptive RAG. Red flag: "it's just better, use it everywhere."
- **"Faithfulness is 0.6 — what does it mean, what do you do?"** Strong: "~40% of statements aren't grounded"; diagnoses retrieval vs. utilization (the 60/40 split); distinguishes faithfulness from relevancy and context precision. Red flag: thinks citing a source *guarantees* grounding (a system can cite real sources and still be misleading by decontextualizing facts).
- **"Walk me through a multi-hop question."** Strong: decompose → retrieve per hop → reason across → re-retrieve; names a benchmark unprompted; flags the bad-synthesis failure. Red flag: can't distinguish multi-hop from "retrieve more chunks."
- **"How do you catch a silent quality regression?"** Strong: named harness (Ragas/Phoenix/Langfuse); an offline golden set with *component-level* metrics (retrieval vs. generation separately); gating thresholds; **P95 latency as the real UX metric.** Red flag: "we vibe-check a few queries."
- **"What changed this past year?"** Strong: context engineering as the new framing; MCP as the standard tool surface; RL-trained retrieval as the frontier; hybrid graph+vector as production reality — with a *defended opinion*. Red flag: still calls 2023 naive RAG state of the art.

**Cross-cutting tell:** strong candidates speak in tradeoffs and have specific failure war stories. The hardest red flag is anyone who claims agentic RAG *eliminates* hallucination. It reduces it; it never eliminates it.

---

## 8. Team notes

*What this technique is, so the org reads it right: not "retrieve once, then generate," but **retrieval plus a control loop plus an evaluation harness.** The third part is where teams underinvest — and where the role question actually lives.* *(advisory throughout this section unless a [sourced] tag appears)*

### Roles & seniority — does an existing role absorb it?

**Short answer: yes.** A strong **AI/Applied-LLM Engineer who owns retrieval end-to-end** absorbs most of this. You do *not* need a new "Agentic RAG team," and you usually do *not* need an ML Engineer (someone who trains/fine-tunes models) until retrieval quality is already solved. The clean 2026 split: an **AI Engineer** builds products on top of foundation models; an **ML Engineer** builds/trains the models themselves. For agentic RAG the bottleneck is retrieval quality and the control loop — AI-engineer territory. *[sourced split]*

Who you actually need, in priority order:

1. **One senior "retrieval owner" (Senior AI/RAG Engineer).** The load-bearing hire. Owns ingestion, chunking, embedding choice, hybrid search, reranking, the agent's stopping rules, and — critically — the eval harness. Seniority matters because the hard part isn't writing the loop, it's *bounding* it (budgets, stop signals) and *measuring* it. A junior will ship a loop that hallucinates *more* than plain RAG. Comp reference: seniors with shipped production RAG pull ~$195K–$290K base, total comp past $400K at frontier labs; searches close in ~5–9 weeks. *[sourced comp/timeline]*
2. **A data engineer (often part-time/shared).** Day-to-day RAG is "more data-engineering than people expect" — ingestion, freshness, dedup, document parsing. If your corpus is messy (most are), this is half the battle. *[sourced]*
3. **Eval ownership — assign it, don't assume it.** Someone must own the labeled eval set and the faithfulness/precision dashboards. It's the thing that silently gets dropped. Make it an explicit line in a named person's job with a metric they're accountable for.

**The disqualifying tell:** a candidate who frames agentic RAG as primarily a *prompt-engineering* problem doesn't understand the work. There's less prompting than people expect; the job is retrieval quality, evaluation, and loop control. *[sourced]*

### Hiring signals

**Green:** has **shipped a RAG system to production and watched retrieval quality degrade**, then diagnosed it (the war story is the signal); talks fluently about retrieval metrics (recall@k, MRR, nDCG) *and* output metrics (faithfulness, answer relevancy, context precision/recall) and the difference between them; reaches for **hybrid search (dense + BM25) + a cross-encoder reranker** as table stakes and adds agentic complexity *only after* eval is instrumented; brings up **step budgets, explicit stop signals, and a faithfulness judge with re-retrieve-on-failure** unprompted. *[sourced signals]*

**Red flags:** "we'll add evals later" (evals come *first*); wants to build a vector DB from scratch with no thesis on why managed won't do; treats the agent loop as free (real costs run ~$0.02 simple to ~$0.31 complex multi-source per query); believes "more retrieves = better" (a naive 4-retrieve agent *hallucinates more* than classic RAG — more chances to drift). *[sourced]*

### Build vs. buy (default: rent/buy)

**Buy/rent the retrieval substrate; own only the agent loop and evals — and only if retrieval quality is your product differentiator.** The 2026 market splits three ways: turnkey RAG platforms (Glean, Onyx, Vectara, Cohere North); hyperscaler services (AWS Bedrock Knowledge Bases, Azure AI Search, Google Gemini Enterprise — buy this if you're already cloud-locked); and assemble-it-yourself (Pinecone, LlamaIndex, LangChain/LangGraph, Elastic). *[sourced]*

**Decision rule:** the rough build-vs-buy breakpoint is **~3 dedicated ML engineers** — below that, managed RAG wins on time-to-value. Sharper: MIT's 2025 GenAI Divide report found **vendor-partner deployments succeed ~67% of the time vs. ~33% for in-house builds**, and 95% of enterprise GenAI pilots never reach measurable P&L. **Default to renting.** *[sourced]* Own the layer where your *hallucination risk lives*: if your private corpus is the product (legal, medical, financial), own the agent loop, the eval set, and possibly a fine-tuned reranker — but still rent the boring substrate.

**Standards note:** **MCP** became the de-facto retrieval-tool interface after Anthropic donated it to the Linux Foundation's Agentic AI Foundation in Dec 2025, with OpenAI and Google adopting it. Build against MCP-compatible tools to avoid lock-in. *[sourced]*

**The single biggest cost lever:** **Adaptive routing** — classify the query, send easy ones through cheap Advanced RAG and only hard ones through the full agentic loop. Hire someone who reaches for this instinctively.

### Failure modes (interview for them, staff against them)

Four kill most first deployments *[sourced]*: **(1) retrieval thrash / infinite loops** (no step budget, weak stopping rules — fix: hard cap, explicit stop signal, a *retrieves-per-correct-answer* dashboard metric); **(2) graders that never reject** (a lenient faithfulness judge passes hallucinations through — a weak judge makes agentic RAG *worse* than classic RAG); **(3) context overflow / bloat** (the loop stuffs the window until the generator drifts); **(4) latency spirals** (extra retrieves and judge calls compound). Plus two synthesis-specific traps: **synthesis hallucination** (stitching two chunks about different things into a claim neither supports — fix: **per-claim citation grounding**, which kills most of them) and **early stopping** (the agent quits at 1 retrieve when 3 were needed — the faithfulness judge is what tells it to keep going).

**The org-level lesson:** the difference between agentic RAG that *beats* classic RAG and one that's *worse* than it is *entirely* the eval/judge/citation layer — not the cleverness of the loop. Staff and interview for that layer first. Production targets to hold people to: **faithfulness >0.9, answer relevancy >0.85, context precision >0.8.** *[sourced thresholds]*

### TL;DR for the hiring plan

- **First hire:** one senior AI/RAG Engineer who owns retrieval *and* evals end-to-end. This is the whole ballgame.
- **Support:** part-time/shared data engineer; a named owner for the labeled eval set.
- **Don't hire yet:** ML Engineer (model training) or GraphRAG specialist — only after retrieval is solved, or the corpus genuinely demands graph traversal.
- **Build vs. buy:** rent the substrate (MCP-compatible). Own only the agent loop + eval set + domain retrieval if correctness *is* your product.
- **Interview filter:** they bring up step budgets, faithfulness judges, citation grounding, and adaptive routing unprompted — and they put evals *before* the loop.

---

## Sources

- Agentic RAG in 2026: Architecture Patterns, Frameworks & When to Use It — jobsbyculture.com (accessed 2026-06-25): https://jobsbyculture.com/blog/agentic-rag-guide-2026
- Agentic RAG Explained — freeacademy.ai (2026): https://freeacademy.ai/blog/agentic-rag-ai-agents-supercharge-retrieval-2026
- Agentic RAG enterprise guide — Data Nucleus (2026): https://datanucleus.dev/rag-and-agentic-ai/agentic-rag-enterprise-guide-2026
- Search-R1 — arXiv 2503.09516 / GitHub: https://arxiv.org/abs/2503.09516 · https://github.com/PeterGriffinJin/Search-R1
- R1-Searcher — arXiv 2503.05592: https://arxiv.org/pdf/2503.05592
- FrugalRAG — arXiv 2507.07634: https://arxiv.org/pdf/2507.07634
- Demystifying deep search (EvidenceLoop; 20.0%→25.0% Pass@1) — arXiv 2510.05137: https://arxiv.org/pdf/2510.05137
- Corrective RAG (CRAG; T5-large evaluator, three-action design) — Analytics Vidhya (2024): https://www.analyticsvidhya.com/blog/2024/12/corrective-rag/
- Self-Reflective RAG with LangGraph (Self-RAG reflection tokens) — LangChain: https://www.langchain.com/blog/agentic-rag-with-langgraph
- Agentic RAG Failure Modes: Retrieval Thrash, Tool Storms, Context Bloat — Towards Data Science (accessed 2026-06-25): https://towardsdatascience.com/agentic-rag-failure-modes-retrieval-thrash-tool-storms-and-context-bloat-and-how-to-spot-them-early/
- Query-Adaptive RAG routing — ragaboutit.com (accessed 2026-06-25): https://ragaboutit.com/query-adaptive-rag-routing-complex-questions-to-multi-hop-retrieval-while-keeping-simple-queries-fast/
- Agentic RAG: A Survey — arXiv 2501.09136
- Self-RAG (arXiv 2310.11511) · CRAG (arXiv 2401.15884)
- Harvey customer figures (~50% of the Am Law 100) — Harvey materials / Sacra (2026)
- Decagon (~$4.5B, Jan 2026) and Sierra ($15.8B, May 2026) — vendor announcements
- MCP donated to the Linux Foundation's Agentic AI Foundation, Dec 9 2025 — confirmed via Anthropic claude-api reference (June 2026)
- Agentic RAG: The 2026 Production Guide — MarsDevs: https://www.marsdevs.com/guides/agentic-rag-2026-guide
- Managing Agentic AI Costs at Scale — Cockroach Labs: https://www.cockroachlabs.com/blog/agentic-ai-costs-at-scale/

*Sourcing caveat: vendor figures (deflection rates, valuations, the 60–70% simple-query share, 30–50% routing savings, build-cost ranges, GraphRAG cost reductions) are indicative industry claims, not independently audited numbers. RL-retrieval results are from arXiv papers. Model-name leaderboard standings in the source material are flagged provisional and excluded from the body.*
