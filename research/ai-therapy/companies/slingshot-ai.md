# Slingshot AI — Ash

**One-line:** A free consumer AI-therapy app built as a domain-specialized post-training stack (SFT + DPO/RL on the open-weight Qwen3-235B), marketed as "the world's first foundation model for psychology," funded with $93M and deliberately positioned as a non-regulated "wellbeing product" — a posture that forced a January 2026 UK withdrawal and sits behind a thin, company-authored evidence base.

**Verifier overall confidence: medium.** Many of the strongest technical claims trace to vendor marketing (Nebius, Together AI) or company-produced studies; independence and verification are weak in exactly the places (efficacy, safety accuracy) where it matters most. Evidence labels below: **sourced / inference / speculation / contested / unsupported**. Where a fact was not found: "unknown — not found."

---

## Dimension 1 — Company Journey / Origin Story

- **[sourced]** Slingshot AI was founded in **2022** by **Daniel Reid Cahn** and **Neil Parikh**, with **Lucy Hong** a founding member; the stated mission is to "exponentially increase global access to mental healthcare." (slingshotai.com/blogs/introducing-slingshot)
- **[sourced]** Origin: Parikh spent ~18 months seeking a co-founder for an AI mental-health lab; he met **David Cahn** (a Sequoia AI investor) at a coffee bar, who introduced his brother **Daniel**; the two found they'd lived "parallel lives" and mapped out the "Slingshot Master Plan on a whiteboard." (slingshotai.com/blogs/introducing-slingshot)
- **[sourced]** Both founders are school dropouts who bonded over parallel lives and personal mental-health struggles. (slingshotai.com/blogs/introducing-slingshot)
- **[sourced]** Timeline: founded 2022 → **Aug 2024 $30M seed** → **Jan 2025 $40M Series A** → **Jul 22 2025** launched Ash publicly + extended Series A to **$93M total** (after ~18 months of development and ~50,000 beta users) → **Nov 2025** published first safety/clinical study (met with expert skepticism); reported 150,000+ users → **Jan 21 2026** announced withdrawal of Ash from the UK over regulatory uncertainty (effective Jan 23, 2026). (a16z.com/announcement/investing-in-slingshot-ai; businesswire.com 2025-07-22; statnews.com 2025-11-24; statnews.com 2026-01-21)
- **[contested]** Founding year: Built In lists 2022; Crunchbase / some aggregators show 2018 — likely an entity/registration artifact. Product (Ash) launched July 2025. (builtinnyc.com; crunchbase.com)

---

## Dimension 2 — Technology Stack & Architecture

- **[sourced]** Ash is not a single LLM but a **multi-model serving system**. The backbone is the **open-weight Qwen3-235B** (Mixture-of-Experts: 235B total / ~22B active params), and the system **mixes models from 32B to 235B dynamically within a single dialogue** (presumably routing cheaper models for simple turns, the large model for clinically delicate moments). (nebius.com/customer-stories/slingshot-ai)
  - *Verifier caveat: the base-model identification rests on a single vendor (Nebius) marketing page; the Together AI source does NOT name the base model.*
- **[sourced]** Qwen3-235B-A22B is a sparse MoE transformer: 235B total params, 128 experts, 8 activated per token, ~22B active. (arxiv.org/html/2505.09388v1)
- **[sourced]** Training infrastructure runs on **Nebius GPU clusters** using **DeepSpeed + ZeRO-3** (memory-efficient distributed training) and **SkyPilot** (orchestration). Inference is **planned on managed Kubernetes with autoscaling**. (nebius.com/customer-stories/slingshot-ai)
- **[sourced]** **Together AI's fine-tuning platform** is used for SFT and DPO (long-context SFT+DPO, parallel experiment configs); retraining frequency rose to **3–7×/week** (vs. weekly previously). (together.ai/customers/slingshot-ai)
- **[sourced]** The **Nebius infrastructure** carries **SOC 2 Type II, HIPAA, and ISO 27001** certifications.
  - *Verifier caveat: these are certifications of the Nebius infra **vendor**, not of Slingshot/Ash as a product.* (nebius.com/customer-stories/slingshot-ai)
- **[sourced]** Delivery is a **free consumer iOS/Android app**. (bhbusiness.com 2025-07-22)
- **[sourced]** The safety layer is a distinct **two-pass guardrail architecture**: a fast classifier first pass, then an LLM-based safety check that decides block/replace/allow, with every flagged session reviewed by a clinician. (nebius.com/customer-stories/slingshot-ai)
- **[inference]** No public evidence indicates Ash uses **retrieval-augmented generation (RAG)**; personalization appears to derive from RL on conversation signals rather than a documented retrieval system. (negative finding across Nebius/Together case studies)
- **Not disclosed:** exact routing logic, param counts of distilled/smaller variants, whether RAG is used for memory/personalization. **Unknown — not found.**

> **Source-quality note:** Nearly all Dimension 2 facts come from **self-interested vendor case studies** (Nebius, Together AI). Accurate but **not independently verified**.

---

## Dimension 3 — AI/ML Techniques & Models

- **[contested → marketing framing]** Slingshot markets Ash as **"the world's first foundation model for psychology,"** but technically it is a **specialized post-training stack on top of an open-weight base (Qwen3-235B), NOT a from-scratch foundation model.** (see inference below)
- **[sourced]** Three-phase pipeline (per company messaging): (1) **"pre-training"/continued training** on what they call the largest behavioral-health dataset assembled, teaching dozens of therapeutic modalities (CBT, DBT, ACT, psychodynamic, Gestalt, motivational interviewing); (2) **supervised fine-tuning** on clinical conversations authored/curated by their clinical team to encode therapeutic micro-decisions (when to challenge, stay silent, end a session); (3) **reinforcement learning** — DPO for behavioral policies plus an RL loop. (businesswire.com 2025-07-22; nebius.com/customer-stories/slingshot-ai)
- **[sourced]** The RL stage uses a **hybrid weighted reward**: (a) a reward model trained on **thousands of clinician-written comparisons** (weighted most heavily); (b) **user-behavior signals** (ratings, app returns, linguistic cues); (c) **LLM-as-a-judge** comparative scoring. Retraining cadence reached **3–7×/week**. (nebius.com/customer-stories/slingshot-ai; together.ai/customers/slingshot-ai)
- **[sourced — but central, unquantified claim]** **Proprietary data** is the core moat: clinically labeled therapeutic conversations and expert preference comparisons. **Dataset size/provenance are not publicly quantified.** (businesswire.com 2025-07-22)
- **[inference]** Despite the "first foundation model for psychology" marketing, Ash is technically a **domain-specialized post-training stack (continued training + SFT + DPO/RL) on an open-weight base**, not a from-scratch foundation model. Well-supported: the base is the open-weight Qwen3-235B (Nebius); Together AI describes the work as fine-tuning open-source models; no source claims from-scratch pretraining of a frontier base. (nebius.com/customer-stories/slingshot-ai; together.ai/customers/slingshot-ai)
- **[inference]** No public evidence Ash uses RAG; absence of evidence, not evidence of absence.

**Capability summary:** foundation model from scratch = **NO** (open-weight base); fine-tuning (SFT) = **YES**; RLHF (reward model + RL + DPO) = **YES**; RAG = **not evidenced**; guardrails = **YES** (two-pass); evals = **partial/contested**; proprietary data = **YES** (central claim, unquantified).

---

## Dimension 4 — Therapeutic Approach, Technique Encoding & Human-in-the-Loop

- **[sourced]** Ash is positioned as "the first foundation model for psychology," trained on what Slingshot calls the world's largest and most diverse behavioral-health dataset. It is **not built around a single protocol** but integrates multiple evidence-based modalities: **CBT, ACT, psychodynamic methods, Gestalt, and motivational interviewing** (other press also cites **DBT**). (nebius.com/customer-stories/slingshot-ai)
- **[sourced]** Design philosophy emphasizes **"appropriate challenge"** rather than sycophantic agreement — knowing when to challenge a user, stay silent, or end a conversation. (nebius.com/customer-stories/slingshot-ai)
- **[sourced]** Technique is encoded via the 3-phase training described in Dimension 3: continued pre-training on therapeutic data → clinical fine-tuning by Slingshot's clinical team → RL with a 3-component weighted reward (clinician comparisons weighted most heavily). Backbone Qwen3-235B mixed with smaller (~32B) models for latency. Developed over ~18 months with ~50,000 beta users before launch. (nebius.com/customer-stories/slingshot-ai; businesswire.com 2025-07-22)
- **Human-in-the-loop has two distinct roles:**
  - **[sourced]** **Build-time:** clinicians shape fine-tuning and author the comparison data that drives the reward model.
  - **[inference]** **Run-time:** the product is **autonomous (no live therapist in the conversation)**, EXCEPT for safety — **every session flagged by the guardrails is reviewed by a clinician after the fact** to confirm appropriate information was given (e.g., emergency contacts). So human-in-the-loop = **build-time + post-hoc safety review, not real-time co-piloting of therapy.** (nebius.com/customer-stories/slingshot-ai)

---

## Dimension 5 — Safety, Crisis Handling, Clinical Evidence & FDA/Regulatory

### Crisis / safety architecture (defense-in-depth)
- **[sourced]** **Pass 1:** a fast classifier scans user input for unsafe content before the model responds. **Pass 2:** a separate safety-tuned LLM decides to **block, replace, or allow**. A redundant **embeddings-based safeguard** trained on real-world usage supplements model-level handling. (nebius.com/customer-stories/slingshot-ai)
- **[sourced]** On confirmed suicidal ideation or non-suicidal self-injury, Ash delivers an escalation message with **988 (US)** and sometimes additional crisis resources; **every flagged session is clinician-reviewed.** (statnews.com 2025-11-24)
- **[sourced]** Ash explicitly disclaims it is **NOT for people facing a mental-health crisis** and redirects such users to human professionals. (statnews.com 2025-11-24)

### Clinical evidence — the sole study
- **[sourced]** **arXiv 2511.11689** ("Generative AI Purpose-built for Social and Mental Health: A Real-World Pilot"), submitted Nov 12 2025 (v3 Jan 20 2026). A **single-arm naturalistic observational pilot — NOT an RCT.** Conducted **May 15 – Sep 15 2025**, assessments every 2–6 weeks plus a 10-week follow-up. (arxiv.org/abs/2511.11689)
- **[sourced]** **305 completers** in three trajectories: **Improving 42.3% (n=129), Non-responders 48.2% (n=147), Rapid Improving 9.5% (n=29).** Reported sustained PHQ-9/GAD-7 reductions plus gains in hope, behavioral activation, social interaction, loneliness, perceived social support; working alliance comparable to traditional care. (arxiv.org/pdf/2511.11689; thehemingwayreport.beehiiv.com)
- **[sourced]** In the pilot, automated guardrails flagged **76 sessions (1.02%)** for risk, all handled per escalation policy. (arxiv.org/pdf/2511.11689)

### ⚠️ Conflict-of-interest flag (verifier)
- **[contested — COI]** The study is presented as academic/independent, but **Thomas D. (Derrick) Hull, the corresponding author, is Slingshot's own R&D / founding Clinical Lead** — NOT an independent University of Washington academic, as a conflated entity in the raw findings implied. **Patricia Arean holds advisor shares in Slingshot**, and Malgaroli's (NYU) work was Slingshot-supported. **The study is effectively company-authored** — a material conflict the original findings understated. (arxiv.org/pdf/2511.11689; talktoash.com/about)

### Evidence caveats
- **[sourced]** Cannot establish causation (no control group); **~47% dropout requiring imputation**; **82% female sample** (12.5% men — generalizability concern, esp. for higher-suicide-risk groups); concurrent-care confound (**36.4% on psychiatric meds, 23.9% in psychotherapy**, controlled only as binary yes/no); nearly half (48.2%) showed minimal improvement. **STAT** framed the study as raising **"more questions than answers."** (thehemingwayreport.beehiiv.com; statnews.com 2025-11-24)

### The "100% accuracy" risk-detection claim
- **[contested]** A NYU/Slingshot evaluation claims Ash identified moments of risk with **"100% accuracy"** across tests and human reviews. The figure traces to the **Nebius vendor marketing page** and Slingshot's own messaging — **not an independent NYU publication.** STAT covered it as a **company claim met with expert skepticism** that the small, uncontrolled study "offers little clinical proof." A self-evaluated, small, company-run 100% metric is a marketing claim, not an independently verified result. (nebius.com/customer-stories/slingshot-ai; statnews.com 2025-11-24)

### The "76% / 77%" improvement figures
- **[contested]** A "10-week real-world study" reportedly found **76% of users with decreased depression and 77% with lower anxiety.** The numbers are real but trace to **Slingshot's own marketing/study** (single-arm, no causation). The originally-cited source (techbrew.com 2025-07-31) does **NOT** contain these figures — that article only discusses Stanford and Dartmouth studies. **Misattributed source + company-produced figures = contested, not sourced.**

### Regulatory / FDA status
- **[sourced]** Ash launched ~Jul 22 2025 as a **free consumer iOS/Android app.** Slingshot classifies it as a **"general wellness" / "wellbeing" product, NOT a regulated medical device**, and **has not obtained FDA clearance or approval** (no 510(k)/De Novo/clinical trial found). (statnews.com 2026-01-21)
- **[sourced]** Slingshot complained to the FDA that AI-tragedy coverage (e.g., ChatGPT) "skewed the public's perception of risk" for general wellness apps like Ash, arguing it provides "enormous benefit at low risk." (statnews.com 2025-11-24)
- **[sourced]** **UK withdrawal:** On **Jan 21 2026** Slingshot announced Ash would be unavailable in the UK after **Jan 23 2026** over UK medical-device regulatory concerns; CEO Daniel Cahn cited the lack of a clear regulatory pathway for "wellbeing products like ours." (statnews.com 2026-01-21)
  - *Verifier correction: the withdrawal was a **voluntary business decision over regulatory uncertainty**, with the company "in conversations with the government on a remedy." Framing it as the **MHRA forcing/challenging** the classification is **[unsupported]** — STAT does not support a "forced by regulator" reading.*
- **[inference]** No FDA clinical trial, De Novo, or 510(k) for Ash; no peer-reviewed (vs. preprint) publication and no efficacy RCT exists as of the current date.

### Gaps
- Exact in-app crisis disclaimer wording and minimum-age requirement (likely 18+) **[speculation]** — **unknown — not found** from a primary source. No peer-reviewed publication; no published numeric PHQ-9/GAD-7 effect sizes beyond "significant reductions" + the trajectory breakdown.

---

## Dimension 6 — Engineering Difficulty (4/5)

**Genuinely difficult:**
- **(a)** A multi-stage **SFT + DPO + RL post-training pipeline** with a clinician-grounded reward model, retraining **3–7×/week**.
- **(b)** **Dynamic in-dialogue routing across 32B–235B models** for cost/quality tradeoffs.
- **(c)** A **two-pass safety guardrail** that must approach **near-100% recall** on crisis detection with **clinician-in-the-loop** review — a high-stakes, very-low-error-tolerance subsystem (the riskiest part).
- **(d)** Sourcing/curating a **large proprietary clinically-labeled dataset** — the genuine moat and arguably the hardest, slowest non-software part.
- **(e)** **HIPAA/SOC2/ISO-compliant inference at consumer-app scale.**

**Why not 5/5:** they did **not** pretrain a frontier base model from scratch — they leverage the open-weight **Qwen3-235B** and standard open-source tooling (**DeepSpeed/ZeRO-3, SkyPilot, Together AI, Nebius, Kubernetes**). The novelty is **domain specialization, proprietary data, and safety/serving engineering** — applied ML systems engineering — **not novel foundational ML research.**

**[inference]** Rating = **4/5.** This is an analytical judgment grounded in verified facts; it depends partly on the contested independence of the safety/eval evidence.

---

## Dimension 7 — Founders, Key Hires, Headcount & Org Shape

**Founders / top of house**
- **[sourced]** **Daniel Reid Cahn** — Co-Founder & CEO. AI research at Imperial College London (post-graduate research on ML for mental-health crises, named "distinguished"); child of a psychologist/social worker; high-school dropout. (talktoash.com/about; slingshotai.com/blogs/introducing-slingshot)
- **[sourced]** **Neil Parikh** — Co-Founder & President. Previously co-founded **Casper** (dropped out of medical school; scaled to $500M+ revenue, 2020 IPO; holds 7 patents in sleep and robotics). (talktoash.com/about; a16z.com)
- **[contested]** **Lucy Hong** — Crunchbase lists her as "Founding member and advisor" (Wharton MBA); some aggregators (Tracxn, search) call her a third co-founder. **Status genuinely ambiguous across sources.** (crunchbase.com/person/lucy-hong)

**Key clinical / technical hires (publicly named)**
- **[sourced]** **Dr. Derrick Hull** — R&D Lead / founding Clinical Lead. PhD Clinical Psychology (Columbia); ex-Clinical R&D at Talkspace, plus Noom and Hero Journey Club. (Also the corresponding author on the clinical pilot — see COI flag, Dim 5.) (talktoash.com/about)
- **[sourced]** **Dr. Caitlin Stamatis** — Head of Clinical Research. (talktoash.com/about)
- **[sourced]** **Dr. Mark Ungless** — Head of Safety (former Director of Data Science, AI & Research at Mental Health Innovations; ex-faculty Imperial / Oxford). Role evolved from advisor to Head of Safety. (talktoash.com/about)
- **[sourced]** **Josh Hsu** — General Counsel. (talktoash.com/posts)

**[inference]** **No publicly named CTO, VP/Head of Engineering, or CFO** was found; CEO **Cahn appears to be the technical lead.** No named ML research lead beyond Cahn/Hull surfaced.

**Advisory board (clinical credibility layer, ~9 advisors)**
- **[sourced]** Dr. Tom Insel (ex-NIMH Director 2002–2015), Lori Gottlieb (psychotherapist/author), former Rep. Patrick J. Kennedy, Dr. Patricia Arean (ex-NIMH research director — also financially entangled via advisor shares, see Dim 5), Mahmoud Khedr, Nina Vasan. (talktoash.com/about; statnews.com 2025-07-22)

**Headcount (small, inconsistent across third-party trackers — all ESTIMATE)**
- **[sourced]** Built In NYC: **16**; RocketReach: **36**; Crunchbase band: **11–50**; one aggregator: 32 **[contested]**. **Best read: ~15–40 FTEs**, a small Series A team. (builtinnyc.com; rocketreach.co)

**Org shape**
- **[sourced]** **Two-hub company:** **NYC HQ** (exec/clinical/marketing/ops) and **London** (engineering concentration). Of 9 current Ashby openings, **6 are engineering, 5 of those London-based**; NY roles are marketing + clinical. (api.ashbyhq.com/posting-api/job-board/slingshotai)
- **[sourced]** Org spans ML, product, engineering, conversational design, clinical, growth, and operations. (slingshotai.com/careers)

---

## Dimension 8 — Compensation Bands

**Hard DATA points (only two genuine Slingshot-specific figures exist publicly)**
- **[sourced — DATA]** **Software Engineer, New York, NY — base $250,000** (H1B LCA filed 2024-12-18, start 2025-01-01). Well above NY market median for the title; suggests senior/staff-level pay. (h1bdata.info)
- **[sourced — DATA]** **Licensed Therapist (NY) — $50–$75 per session, 4 sessions per engagement** (per-session contractor pay, not salaried). (api.ashbyhq.com/posting-api/job-board/slingshotai)
- **[sourced — qualitative]** Stated philosophy: "competitive compensation (top of personal market)"; one aggregator notes ~90th-percentile targeting. **No numeric salaried bands posted on the job board** (NY/London listings show "Not specified"). (api.ashbyhq.com)

**ESTIMATEs (third-party, low confidence — market context, not company actuals)**
- **[speculation — ESTIMATE]** Senior Mobile Engineer (NY) ~**$130K–$180K** (Ladders/ZipRecruiter) — employer-not-posted, and conflicts downward with the $250K LCA. Weight the $250K DATA over this for senior technical staff. (theladders.com)
- **[speculation — ESTIMATE]** NY AI Engineer market context: avg ~$178K; 25th–75th pct ~$139K–$232K (Glassdoor/Built In, market-wide).
- **No data found:** levels.fyi has no Slingshot page (returns unrelated "Slingshot Aerospace"); Glassdoor has ~1 self-reported salary (too thin). **London engineering comp: unknown — not found.** (levels.fyi)

**NET:** Only **two** genuine Slingshot-specific comp data points exist publicly (the $250K NY SWE LCA; the $50–$75/session therapist contract). Everything else is market extrapolation.

---

## Dimension 9 — Funding & AI Investment

- **[sourced]** **Total raised: $93M**, across three disclosed rounds, all involving a16z:
  - **Seed — $30M, Aug 2024**, led by **a16z**, with Felicis, BoxGroup, and angels (Gokul Rajaram, Arjun Sethi, David Cahn, Cory Levy). Valuation undisclosed. (thesaasnews.com)
  - **Series A — $40M, Jan 14 2025**, led by **a16z**. (a16z.com)
  - **Series A extension — $50M+, Jul 22 2025**, co-led by **Radical Ventures and Forerunner Ventures** (joining a16z, Felicis, Menlo), bringing total to $93M; Ash launched publicly the same day. (statnews.com 2025-07-22)
- **[sourced]** Co-investors/angels include **NBA players Aaron Gordon & Scottie Barnes, Replit's Amjad Masad, Hugging Face's Clement Delangue & Thomas Wolf, ElevenLabs' Mati Staniszewski, Oura's Harpreet Rai**; also Menlo, TMV, SV Angel. (statnews.com 2025-07-22)
- **[inference]** **No company-wide post-money valuation** has been publicly disclosed for any round. **Unknown — not found.** (pitchbook.com)
- **[contested]** Funding-total aggregators disagree: **Tracxn $93M, PitchBook ~$99M**, one finding cites **$123M**. The **$93M** company/press-confirmed total is sound; the "$123M" figure is just one of several conflicting, unstable aggregator numbers and should not be presented as a fixed competing total. (tracxn.com; pitchbook.com)

---

## Dimension 10 — Business Model & Business Drivers Behind the Tech

- **[sourced]** Ash is **free on iOS/Android**, deliberately **un-monetized at launch**. The company plans to monetize eventually but has not disclosed how, stating it wants to "hear from people about what's valuable." (techbrew.com 2025-07-31)
- **[sourced]** Because the app is free, **user conversations are used to keep tuning the model** (unless the user opts out); **the data is part of the value exchange.** (choosingtherapy.com)
- **Business driver behind "free":** maximize user volume to gather conversational data to train/improve the model and learn what users value before choosing a monetization path. **[inference + sourced]**
- **[sourced]** The core tech decision — building a **domain-specific model rather than wrapping GPT** — is driven by the thesis (echoed by a16z) that general-purpose models fail at therapy because they give answers, whereas good therapy builds the user's own **agency**. a16z's broader thesis: "the biggest global company will be a consumer health company." (a16z.com)
- **[sourced]** Major business-driven regulatory decision: Ash is marketed as a **"wellbeing product," NOT a regulated medical device**, to stay under FDA enforcement discretion for low-risk wellness apps and enable fast, broad consumer deployment. (statnews.com 2025-11-24)
- **[contested — source correction]** This positioning is in tension with the **"first AI designed for therapy"** branding. *Note: that exact phrase comes from the **BusinessWire press release title (Jul 22 2025)**, not the talktoash.com/about page — the About page reads "the first AI designed for **mental health**" and states Ash is "not designed to be used in crisis."* The therapy-vs-wellbeing tension is real; the specific source attribution in the raw findings was wrong. (businesswire.com 2025-07-22; talktoash.com/about)
- **[inference]** The "wellbeing product, not medical device" classification appears designed to avoid stricter medical-device regulation and enable faster, broader consumer deployment — challenged by UK regulatory uncertainty (voluntary withdrawal, not a regulator-forced action; see Dim 5). (statnews.com 2026-01-21)
- **[speculation]** Future monetization will likely be a subscription/premium model similar to other health-tech apps — **not announced.**

---

## Dimension 11 — Stated vs. Real Motivations

**Confidence: medium.**

### Stated motivation
**[sourced]** Democratize mental healthcare and "exponentially increase global access to mental health" by building the first foundation model for psychology — addressing the provider shortage (cited as ~1 provider per 1,000–10,000 people in need) and the claim that "half the world's population will develop a mental health disorder." Founders frame it as personally mission-driven (both cite their own mental-health struggles and family backgrounds) and emphasize AI that "increases — not decreases — people's sense of autonomy, competence and connection." (slingshotai.com/blogs/introducing-slingshot)

### Real motivation (medium confidence)
**[inference]** Build a large, defensible **consumer health company** on a proprietary domain-specific model, using a **free app to amass conversational training data and a user base** ahead of later monetization (subscription/premium inferred). The mission framing reads as genuine but commercially convenient:
- Backed by a16z's explicit thesis that "the biggest global company will be a consumer health company," the strategy is **mass consumer deployment**.
- A deliberate **"wellbeing product, not medical device" regulatory posture** chosen for **speed-to-market and growth** (avoiding FDA/medical-device oversight) — the posture behind the UK withdrawal.
- The clearest signal: the **therapy-vs-wellbeing ambiguity** — marketed around therapy/"designed for mental health" while legally disclaiming therapy/medical-device status. Growth and regulatory avoidance sit **alongside** (not necessarily against) the stated access mission.

**[contested]** Critics (e.g., Scott Wallace on Medium; STAT; The Hemingway Report) flag a **marketing-surge-vs-evidence-shortfall** gap: aggressive efficacy/safety messaging ("100% accuracy," "76%/77% improvement," "enormous benefit at low risk") rests on a single company-authored, single-arm study. (medium.com/ai-in-mental-health; statnews.com 2025-11-24)

---

## Dimension 12 — Risks, Controversies & Open Questions

- **[contested — COI]** The sole clinical study is effectively **company-authored** (corresponding author is Slingshot's R&D Lead; an advisor holds shares) yet presented as independent academic evidence. Material undisclosed conflict.
- **[contested]** Marquee metrics ("100% risk-detection accuracy," "76%/77% symptom improvement") are **company-produced and not independently verified**; one was **misattributed** to a source (techbrew) that doesn't contain it.
- **[sourced]** **Regulatory fragility:** the "wellbeing, not medical device" posture already forced a **UK exit** (Jan 2026); a clear US/UK regulatory pathway for AI "wellbeing" therapy products does not exist.
- **[sourced]** **Safety stakes:** an autonomous, free, consumer-scale mental-health chatbot disclaiming crisis use, in a climate of high-profile AI-harm cases — the two-pass guardrail must achieve near-100% crisis recall, and its accuracy is self-reported.
- **[inference]** **Single-vendor / single-source dependency:** the core architecture (Qwen3-235B backbone, infra) is documented almost entirely via **paid vendor marketing**, with no independent technical audit.
- **Open questions (unknown — not found):** company valuation; dataset size/provenance; whether RAG/memory is used; exact safety-classifier performance under independent test; minimum-age and disclaimer wording; London comp; identity of any engineering/finance leadership beyond the CEO; monetization model.

---

## Sources

- https://nebius.com/customer-stories/slingshot-ai
- https://arxiv.org/html/2505.09388v1
- https://www.together.ai/customers/slingshot-ai
- https://www.businesswire.com/news/home/20250722566346/en/Slingshot-Launches-Ash-the-First-AI-Designed-for-Therapy
- https://www.techbrew.com/stories/2025/07/31/slingshot-ai-therapy-chatbot-a16z
- https://medium.com/ai-in-mental-health/slingshots-93-million-gamble-marketing-surge-evidence-shortfall-d958e0cfd8e4
- https://bhbusiness.com/2025/07/22/with-93m-raised-slingshot-slingshot-ai-debuts-ai-powered-therapy-service/
- https://arxiv.org/abs/2511.11689
- https://arxiv.org/pdf/2511.11689
- https://www.statnews.com/2025/11/24/slingshot-ai-mental-health-chatbot-safety-study-results/
- https://www.statnews.com/2025/07/22/slingshot-new-investors-generative-ai-mental-health-therapy-chatbot-called-ash/
- https://www.statnews.com/2026/01/21/slingshot-therapy-chatbot-ash-uk-regulatory-concerns/
- https://thehemingwayreport.beehiiv.com/p/78-reflections-on-slingshot-s-real-world-study
- https://slingshotai.com/blogs/introducing-slingshot
- https://a16z.com/announcement/investing-in-slingshot-ai/
- https://www.thesaasnews.com/news/slingshot-ai-raises-30-million-in-seed-round
- https://pitchbook.com/profiles/company/501337-54
- https://tracxn.com/d/companies/slingshot-ai/__A9mVT41EmVcWVNH4TFhXGvym49VlT2u-_HduJtEob40/funding-and-investors
- https://www.choosingtherapy.com/ash-ai-therapy-app-review/
- https://www.talktoash.com/about
- https://www.talktoash.com/posts/ash-by-slingshot-ai-welcomes-new-head-of-research-general-counsel-and-advisors-lori-gottlieb-nina-vasan
- https://www.crunchbase.com/person/lucy-hong
- https://www.builtinnyc.com/company/slingshot-ai
- https://rocketreach.co/slingshot-ai-management_b7846139c2500a5c
- https://api.ashbyhq.com/posting-api/job-board/slingshotai
- https://slingshotai.com/careers
- https://h1bdata.info/index.php?em=Slingshot+AI
- https://www.theladders.com/job/senior-mobile-engineer-slingshot-ai-new-york-ny_82476118
- https://www.levels.fyi/companies/slingshot/salaries/software-engineer
