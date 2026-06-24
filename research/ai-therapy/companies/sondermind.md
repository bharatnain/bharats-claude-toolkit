# SonderMind — Company Dossier

**One-line:** Denver-based, insurance-native two-sided therapy marketplace (founded ~2014) that in October 2025 launched a generative-AI suite — provider documentation tools plus a deliberately non-clinical consumer companion called "Sonder" — layered onto an EHR/billing platform assembled largely through three acquisitions. The AI work is applied integration of commercial foundation LLMs wrapped in heavy compliance and self-asserted governance, not frontier ML research.

**Overall verifier confidence: high.** Note that several headline metrics are first-party/marketing claims (flagged inline), and several "current" figures are 2021–2024 vintage repeated as present-day standing.

---

## Dimension 1 — Company Journey / Timeline

- **Founding:** Founded by Mark Frank (CEO) and Sean Boyd (clinician co-founder). Frank was motivated by his own difficulty finding mental health care and his counselor sister's struggles with patient acquisition and insurance billing. *[sourced — Contrary Research]*
- **Founding year — contested:** Contrary Research, Fierce, and the company indicate **early 2014**; Crunchbase/Clay say **January 2015**. *[contested]* Carry both; 2014 is the more widely repeated figure.
- **Funding arc:** Seed/early → **Series B $27M** (led by General Catalyst, ~2020) → **Series C $150M** (co-led by Drive Capital and Premji Invest), reaching unicorn status (~$1.1B valuation). *[sourced — SonderMind announcement; Fierce; Bloomberg]*
  - **Series C date conflation — flag:** The round was **raised ~March 2021 and announced July 28, 2021**. Treat July 28 as the announcement date, not the raise date. *[sourced/flagged]*
- **Inorganic tech/clinical build-out:** Qntfy (ML/predictive analytics, Oct 2021), Total Brain (wellness/cognitive-screening app, Nov 2022), Mindstrong tech assets + ~20 staff (March 2023, acquired cheaply in Mindstrong's wind-down). *[sourced — Crunchbase; MobiHealthNews; Contrary]*
- **Geographic expansion:** From ~15 to 25 states in mid-2024, reaching **all 50 states + DC by April 1, 2025**. *[sourced — growjo / company]*
- **AI productization:** **"AI Suite" launched October 15, 2025** — provider tools (AI Notes, Session Prep, Treatment Plans, Session Takeaways) and a client-facing 24/7 between-session companion (recaps, journaling, goal-setting), governed by an internal "AI Constitution." *[sourced — SonderMind announcement; Yahoo Finance]*
  - **Chatbot-name timing — flag:** The brand name "Sonder" for the consumer chatbot does **not appear** in the Oct 15, 2025 launch announcement (which lists generic features); the name surfaces in the company FAQ. Minor. *[sourced/flagged]*

---

## Dimension 2 — Technology Stack & Architecture

- **Core platform:** A two-sided marketplace — patient matching/intake, a provider EHR suite (scheduling, messaging, claims filing, assessments, telehealth), and insurance billing automation. *[sourced — Contrary Research]*
- **AI built by acquisition, not ground-up:** ML/analytics capability assembled via **Qntfy (2021), Total Brain (2022), and Mindstrong tech assets (2023, EHR + clinical notes + care planning + ML)**. *[sourced — Contrary; Fierce; MobiHealthNews; SonderMind]*
  - **Total Brain price refinement:** "~$10M" is the base; MarketScreener indicates up to a **+$3M earnout**, so all-in may be ~$13M. *[sourced/flagged]*
- **AI engineering stack (per Principal AI Engineer posting):** Python with TensorFlow/PyTorch/Keras, optional C++/Rust for performance, LLM workflows, agentic patterns, in-context/many-shot learning + fine-tuning, prompt engineering, and AI/ML Ops with eval frameworks. Role pays **$160K–$190K** and reports to **Miguel Alvarado** (AI engineering lead). *[sourced — Built In Colorado posting]*
  - **Caveat:** A single job posting describes *desired* skills, not the deployed production architecture — it is an aspirational requirements list, reasonable as evidence but not an architecture disclosure. *[inference]*
- **Cloud / vector DB / foundation-model provider:** No specific cloud platform, vector database, or foundation-model vendor is publicly named. *[inference / absence confirmed across searches]*
- **Compliance posture:** HIPAA + ISO 27001, dual encryption, encrypted audio deleted after 30 days, feature-specific deletion protocols, explicit opt-in. *[sourced — company-stated; ISO 27001 certification not independently verified via a registrar lookup]*

---

## Dimension 3 — AI/ML Techniques & Models

- **Build vs. train:** Almost certainly built **on top of third-party foundation LLMs** rather than pretraining its own — the posting emphasizes "evaluate and select appropriate LLMs," LLM workflows, in-context/many-shot learning, fine-tuning, agentic patterns, and prompt engineering (integration/orchestration skills, not pretraining). *[inference — well-grounded]*
- **Foundation-model provider undisclosed:** Specific provider (OpenAI / Anthropic / etc.) is **not publicly disclosed** anywhere located. *[sourced — absence confirmed across searches]*
- **Product surface:**
  - **"Sonder"** — 24/7 consumer AI companion for between-session reflection/coping; explicitly **not therapy**.
  - Provider tools: AI-generated clinical notes via an **ambient scribe**, Session Prep, AI-generated treatment plans, Session Takeaways; AI journaling (2024). *[sourced — SonderMind announcement; FAQ]*
- **Productivity / adoption metrics — DOWNGRADE TO COMPANY-CLAIMED:** "~40% of treatment plans AI-generated (provider-in-loop)" and "saves clinicians ~7–8 hours/week" come from a behavioralhealthtech.com blog **authored by Miguel Alvarado, SonderMind's own AI engineering lead** — first-party marketing, not independent reporting. The same blog cites "3–4× better symptom reduction," "67% higher engagement," "55 hours faster" — none independently validated. *[company-claimed, not verified]*
- **Governance (the headline differentiator) — asserted, not demonstrated:** An **"AI Constitution"** approved by an **"AI Governance Council"** (clinicians, compliance experts, data scientists, product leaders); every AI feature reviewed pre-launch; mandatory provider sign-off on AI notes; annual bias & safety audits; audit logs; explicit opt-in. **No published audit results, council roster, or third-party verification exists** — these are governance/process claims the company makes about itself. *[sourced as claims / verification absent]*
- **Proprietary data assets:** 8K+ providers, 3M+ in-person/virtual sessions, Mindstrong EHR clinician-sourced data, enterprise/workplace mental-health data (Southern Company, Boeing, IBM, Cerner, Kaiser Permanente). Usable for fine-tuning/RAG/evals subject to regulatory constraints. *[sourced — Contrary, mid-2024]* **Stale flag:** the 8K provider figure is mid-2024; later figures cite 12K–13K (see Dimension 7 inconsistency note).
- **No bespoke ML for crisis:** No public evidence of RLHF or a custom-trained crisis-detection model; crisis safety appears **guardrail/policy-driven**, not a bespoke ML system. *[inference — appropriately hedged]*

---

## Dimension 4 — Therapeutic Approach, Technique Encoding & Human-in-the-Loop

- **Modalities (consumer Sonder):** Positioned as a guided space to "reflect, practice coping skills, and organize your thoughts," explicitly associated with SonderMind's evidence-based framework (**CBT / DBT / ACT**) for emotional regulation and coping. *[sourced — FAQ]*
- **How technique is encoded — effectively unanswered:** SonderMind publishes **no technical detail** on how clinical technique is encoded — no disclosed protocol library, manualized CBT modules, or model/architecture detail. It reads as a general-purpose LLM constrained by guardrails and a "supportive, non-clinical role," not a structured protocol-driven CBT engine. *[inference]*
- **Scope limits as the primary safety mechanism:** Sonder "is not therapy or a therapist," "cannot diagnose, interpret symptoms, or provide treatment recommendations," and "stays strictly in a supportive, non-clinical role." This deliberate bounding is itself the chief technique-encoding/safety control. *[sourced — FAQ]*
- **Human-in-the-loop — consumer chatbot: WEAK.** The therapist is **not automatically in the loop** — "Provider visibility depends on the feature and your settings. You choose what to bring into the session." Sonder conversations are **user-gated, not clinician-supervised by default**. *[sourced — FAQ]*
- **Human-in-the-loop — provider tools: STRONG.** AI Notes/scribe, Session Prep, Treatment Plans, Session Takeaways are "co-developed with licensed therapists; released only after clinical review and workflow testing," "always co-developed with clinicians, never autonomous," producing **editable drafts** where "the clinician's role requires maintaining full control over any AI-generated content. This is non-negotiable." *[sourced — announcement; safety article]*
- **The gap:** Oversight is robust for provider-facing tools but minimal for the consumer-facing Sonder chatbot — which is precisely where the "there at 3 a.m." use case lives. *[inference]*

---

## Dimension 5 — Safety, Crisis Handling, Clinical Evidence & Regulatory Status

- **Crisis handling — passive (detect + deflect):** Sonder "will show emergency resources if you express you are unsafe or in danger" but "cannot assess risk or provide crisis support itself," directing users to **988** or local emergency. No published one-tap-to-clinician escalation for the consumer chatbot. *[sourced — FAQ; inference on "passive" characterization]*
  - **Partially unverified quotes:** The specific "988 / cannot assess risk" wording and the "may miss signs of suicidal ideation or psychosis / automatic evaluations and safeguards" phrasing attributed to StatNews **could not be confirmed** in the visible (paywalled) StatNews text. *[partially unverified]*
- **Safety/governance ≠ clinical-safety evidence:** HIPAA + ISO 27001, dual encryption, privacy-by-design, AI Constitution, annual bias/safety reviews, audit logs are governance/privacy controls, **not clinical-safety trial evidence**. *[sourced as claims]*
- **Clinical evidence — program metrics, not trials:**
  - SonderMind cites "**85% reduction in symptoms across the therapy journey**" for AI-tool engagers and "**77% sustain therapy improvements for two years or longer**." **SOURCE MISATTRIBUTION FLAG:** these originate in the **Fierce Healthcare article (Oct 2025), self-reported by SonderMind** — they are **not** in the Oct 15 announcement (no metrics) and **not** in the BHT blog (which uses different figures). Downgrade to **company-claimed** with no published methodology. *[company-claimed]*
  - Measurement-based care: PHQ-9 / GAD-7 used in ~80% of sessions. *[sourced — clinical-results page]*
  - **No published RCT, peer-reviewed study, or registered clinical trial of the Sonder chatbot itself.** Cited validation (an 18-RCT CBT-chatbot meta-analysis; Dartmouth's Therabot trial) is **third-party and category-level**, not SonderMind's own. *[inference — strongly supported by absence]*
- **FDA / regulatory:**
  - As of the **FDA Digital Health Advisory Committee meeting on Nov 6, 2025**, the FDA had cleared **zero** generative-AI mental-health tools. *[sourced — Orrick]*
  - SonderMind filed a **public comment to FDA docket FDA-2025-N-2338**; the PDF is CID-font-encoded and **its specific text could not be extracted**. *[sourced; comment content not quotable]*
  - Sonder has **no FDA clearance** and none appears to be sought; the non-clinical framing ("not therapy," "cannot diagnose/treat") keeps it **outside FDA medical-device regulation** — in part a regulatory-avoidance posture. *[inference — well-supported]*
  - SonderMind publicly tracked **California SB 243** on companion chatbots. *[sourced]* **Framing caveat:** SB 243 governs "companion chatbots," a category SonderMind explicitly says Sonder is **not** — so using this to imply Sonder is an "active regulatory target" mildly overstates exposure. *[flagged]*

---

## Dimension 6 — Engineering Difficulty

### Engineering difficulty (3/5)
**Tech dimension: 3/5. Consumer chatbot in isolation: 2/5.**

- The generative-AI components (chatbot, ambient scribe, note/plan generation, journaling) are **well-trodden patterns** — RAG + prompt orchestration + fine-tuning on top of commercial foundation LLMs, exactly what the named stack (Python/PyTorch/LLM workflows/agentic patterns) handles. Not proprietary model training, which **caps difficulty below 4**. *[inference]*
- **What raises it above a generic chatbot:** (1) a **HIPAA + ISO 27001** regulated environment with deletion/encryption requirements; (2) **high-stakes mental-health crisis/self-harm safety** in an area of active regulation and documented LLM failure modes; (3) integration into **legacy EHR/billing/marketplace systems stitched together from three acquisitions** (Qntfy, Total Brain, Mindstrong); (4) **human-in-the-loop clinical workflows** requiring provider review. *[inference]*
- **Why the consumer chatbot alone is only 2/5:** the hard clinical-safety and autonomy problems are **sidestepped by scope-limiting** the bot (no diagnosis, no treatment logic, keyword/intent crisis detection that surfaces 988) rather than solved. *[inference]*
- **Net:** Disciplined applied-AI + safety + compliance engineering using known techniques — **not frontier model development**. A rating of 4–5 would require an FDA-cleared autonomous therapeutic chatbot with validated endpoints and reliable suicide-risk assessment, which is explicitly **not** what SonderMind built. *[inference]*

---

## Dimension 7 — Founders, Key Hires, Headcount & Org Shape

**Founders**
- **Mark Frank** — Co-Founder & CEO since inception. B.S. Computer Science from West Point, ~5 years as a U.S. Army officer (Bronze Star, Iraq); prior founder of Next Oncology / Denver CyberKnife and SafeImageMD (sold 2016); investment-banking background. *[sourced — Crunchbase]*
- **Sean Boyd** — Clinician co-founder (Regis University counseling background). Described as "Former Co-CEO" who stepped back ~2016; elsewhere listed as CSO & Co-Founder. **Current role is contested/ambiguous.** *[sourced; current role contested]*

**Key technical / clinical / data hires**
- **Glen Coppersmith** — Chief Data Officer; joined Oct 2021 via the **Qntfy acquisition** (Qntfy became the Data Science division). The most material AI/ML leadership hire. *[sourced — fully confirmed]*
- **Nabeel Meghji** — Chief Product Officer (Jan 2021 release; ex-DispatchHealth CPO, ex-Healthgrades). *[sourced]*
- **Miguel Alvarado** — AI engineering lead (the Principal AI Engineer reports to him; author of the BHT marketing blog). *[sourced — Built In posting + BHT blog]*
- **Mindstrong assets (2023)** cited as adding clinical-data/EHR-modeling capability. *[sourced, lower confidence on integration detail]*
- **Single-aggregator, treat as inference-grade:** Kevin Howard (CTO), Karan Singh (COO), a CMO (Dr. Smitha "Upa" Upadhyaya per one aggregator), Wesley Knepper (VP Clinical Excellence) — appear only in aggregator listings, **not cross-confirmed** on a primary source. *[inference]*

**CFO churn**
- **Corley Hughes** — named CFO (Jan 2021; ex-Microsoft, Glossier); since transitioned **off** CFO to independent board member. **Kevin Delaney** reported as later CFO (~Nov 2024, single aggregator). *[sourced]*

**Headcount & org shape**
- ~**577 employees** (UnifyGTM, ~April 2026); Contrary cited **785** as of July 2024. *[sourced]*
  - **"Decline" framing REFUTED:** UnifyGTM reports 577 as a **7.2% year-over-year *increase*** (prior year ~538), contradicting any "785→577 material contraction" narrative. The 785 and 577 figures almost certainly **count different populations** (e.g., including vs. excluding 1099 contract therapists) and are **non-comparable**. Do not read as a clean decline. *[contested]*
- **Org skews clinical:** ~329 Healthcare; Engineering ~55; Business Mgmt ~50; Marketing & Product ~41; Sales & Support ~24; Finance & Admin ~23 (aggregator estimate). *[sourced — estimate-grade]*
- **Layoffs:** ~50 people (~15%) Dec 2022; ~49 people (~17%) Jan 2024. *[sourced — events confirmed]*
  - **Math conflict flag:** 49 = 17% implies a ~288-person base (Jan 2024), irreconcilable with the 785 mid-2024 figure. The percentages, absolute counts, and 785 figure **cannot all be true under one definition of "employee."** *[contested]*
- **Provider count internally inconsistent:** 8K (Contrary, 2024) vs. "more than 12,000" (Dec 2025 review) vs. 13,000 (business-dimension findings). The **13,000 figure is not cleanly sourced; 8K is stale.** Treat provider count as growing and approximate. *[contested]*

---

## Dimension 8 — Compensation Bands

**Data quality:** H1B/LCA data is thin — only 3 SonderMind LCA records total; 0 LCAs filed in FY2024. H1B gives spot DATA points, not bands. Levels.fyi (self-reported, verified) and Glassdoor (mixed reported + modeled) are the main band sources.

**Engineering (AI/platform-relevant)**
- **Software Engineer** (Levels.fyi, 6/2026): median total comp ~$111K–$117K; base band ~$89.5K–$111K; top package ~$203,575. *[DATA — Levels.fyi]*
- **Backend Software Engineer** (Levels.fyi): median TC ~$110K; top ~$203,575. *[DATA — Levels.fyi]*
- **Principal Engineer** (DOL LCA): **$172,744 base** (Andover MA, 05/2025); **$200,000 base** (Andover MA, 03/2023). *[DATA — DOL LCA]*
- **Principal AI Engineer** (live posting): **$160K–$190K** — consistent with the Principal H1B band. *[sourced — Built In posting]*
- **Engineering Manager** (DOL LCA): **$145,000 base** (Fremont CA, 03/2023). *[DATA — DOL LCA]*
- **Software Engineer** (Glassdoor): up to ~$118,396. *[ESTIMATE — Glassdoor modeled]*

**Product / corporate**
- **Product Manager** (Levels.fyi): up to **~$208,950 TC** — company high-end. *[DATA]*
- **Recruiter** (Levels.fyi): ~$76.5K–$104K; ~$90,450 TC cited as company low-end. *[DATA]*

**Clinical (workforce core)**
- **Therapist** (Glassdoor): avg ~$96,001/yr (~$46/hr); typical $76,284–$122,310 (25th–75th pct). Note: SonderMind therapists are largely contracted/per-session, so "salary" is a loose construct. *[ESTIMATE — Glassdoor modeled]*
- **Therapist comp satisfaction: 2.3/5, ~25% below peer average** — relevant to retention risk. *[sourced, single-source]*
- **Wellness Coordinator** (Glassdoor): ~$53,910 (org low-end). *[ESTIMATE]*

**Overall band:** Glassdoor frames ~$53,910 (Wellness Coordinator) to ~$118,396 (Software Engineer); Levels frames ~$90,450 (Recruiter) to ~$208,950 (Product Manager). Engineering/Product top out around $200K TC; clinical core ~$50K–$120K.

**Not found:** No executive comp (CEO/CTO/CDO/CFO — private company). No Data Scientist / ML Engineer-specific band despite the Qntfy data-science division — a gap given the AI-chatbot thesis. *[unknown — not found]*

---

## Dimension 9 — Funding & AI Investment

- **Series C = $150M**, announced July 28, 2021 (raised ~March 2021), co-led by **Drive Capital** and **Premji Invest**; participants: General Catalyst, Partners Group, Smash Ventures, Kickstart Fund, F-Prime Capital, Founders Circle Capital, Zoma Foundation, FCA Venture Partners. **~$1.1B valuation; ~$183M cumulative.** *[sourced — company; Fierce; Bloomberg]*
- **Series B = $27M** (General Catalyst, ~2020). *[sourced]*
- **Contested totals:** Tracxn reports **$242M Series C / $276M total over 8 rounds** — contradicts the company announcement and multiple primary outlets ($150M / $183M) and appears **inflated**. *[contested]*
- **No dedicated AI funding round:** AI capability was **acquired** (Qntfy, Total Brain, Mindstrong) and built internally, not separately financed. *[inference]*
- **No new priced round 2022–2026** publicly reported; still presented as Series C-stage private (EquityZen lists pre-IPO secondary shares). *[inference]*
- **Stale-as-current risk:** Valuation, funding total, and provider count are 2021–2024 vintage repeatedly presented as current standing. *[flagged]*
- Secondary/aggregator/podcast estimates (treat as approximate): **$300M–$500M gross bookings**, **~12% no-show reduction** in AI pilots, **~400% revenue growth** between the 2020 Series B and 2021 Series C. *[inference — not audited]*

---

## Dimension 10 — Business Model & Business Drivers Behind the Tech

- **Model:** Insurance-native, two-sided marketplace matching patients to in-network therapists (virtual + in-person), handling credentialing, billing, claims. **Primary revenue: insurance reimbursement + per-completed-appointment commission**, supplemented by out-of-pocket pay, employer/enterprise benefits, minor fees. In-network with **UnitedHealthcare, Cigna, Aetna, Medicare Advantage**. *[sourced — Contrary]*
- **Differentiators:** Insurance acceptance (vs. cash-pay BetterHelp), in-person + virtual, both therapy and psychiatry. *[sourced]*
- **Tech decisions trace to concrete business drivers:** *[inference — well-evidenced linkages]*
  - **(a) Value-based / outcomes payer contracts** reward measurable improvement and lower total cost → AI pitched to drive engagement and outcomes.
  - **(b) Provider economics** — AI documentation tools reduce clinician admin burden, improving retention of the scarce provider supply that is the marketplace's input.
  - **(c) No-show reduction** (~12% in pilots, per one source) directly protects reimbursement revenue.
  - **(d) Structural therapist supply–demand gap and the "~167 hours between sessions"** justify the between-session companion as **capacity extension without adding clinician hours**.

---

## Dimension 11 — Stated vs. Real Motivations

### Stated vs. real motivations

- **Stated (Mark Frank):** AI exists to support patients in vulnerable moments and to **complement, never replace,** human therapeutic connection — *"It's fast, it's private, and it's there at 3 a.m."* and *"AI cannot replace the human connection that is absolutely necessary to move the needle."*
  - The "fast, private, 3 a.m." quote is **confirmed** in StatNews. *[sourced]*
  - The "AI cannot replace the human connection…" quote **could not be located** in the visible (paywalled) StatNews text and may come from a different source or the paywalled portion — **unverified here.** *[partially unverified]*
- **Real drivers (confidence: medium-high):** STAT (Dec 2025) explicitly attributes the move to generative AI having become *"too popular and offers too many advantages to ignore"* — i.e., **competitive/defensive pressure** against ChatGPT (~800M weekly users, many for emotional support) and AI-native rivals (Spring Health, Slingshot, etc.), **the need to monetize the ~167 empty between-session hours**, **payer outcome/cost incentives**, **clinician retention** via reduced admin burden, **no-show reduction** protecting reimbursement, and **stretching scarce therapist supply** — all wrapped in a "human-connection-first" narrative that also defuses safety/trust concerns. *[sourced framing + inference on internal weighting]*
- **Assessment:** Medium-high confidence the real motivation is **competitive defense + outcomes/cost economics** layered onto the stated human-connection narrative. The business-driver linkages are well-evidenced; the precise internal weighting of motives is inferred. *[inference]*

---

## Dimension 12 — Notable Risks, Inconsistencies & Open Questions

- **Marketing laundered as fact:** Headline AI metrics ("40% of treatment plans AI-generated," "7–8 hrs/week saved," "85% symptom reduction," "77% sustain 2+ years," "3–4× symptom reduction") are **first-party, unaudited** — sourced to a blog by SonderMind's own AI lead or to self-reported figures in a Fierce article. **Treat as company claims, not verified outcomes.** *[contested / company-claimed]*
- **Source misattribution:** The 85%/77% figures originate in the **Fierce article**, not the Oct 15 announcement or BHT blog. *[flagged]*
- **Headcount narrative refuted:** No clean 785→577 decline; figures count different populations and one source shows a YoY *increase*. *[contested]*
- **Internal math conflicts:** Layoff percentages vs. counts vs. the 785 figure cannot all be reconciled under one definition of "employee." Provider count reported as 8K / 12K / 13K. *[contested]*
- **Governance unverified:** AI Constitution, AI Governance Council, annual audits are **asserted with no published roster, audit results, or third-party verification.** *[verification absent]*
- **Foundation-model provider, deployed architecture, cloud, vector DB:** **unknown — not found.** *[absence]*
- **FDA comment text:** **unknown — not extractable** (CID-font-encoded PDF). *[absence]*
- **Series C date:** raised ~March 2021, announced July 28, 2021 — often conflated. *[flagged]*

---

### Sources
- https://research.contrary.com/company/sondermind
- https://www.sondermind.com/resources/announcement/sonder-mind-launches-suite-of-clinically-backed-ai-tools-for-mental-health-care-delivery-to-help-people-feel-better-faster/
- https://www.sondermind.com/faqs/
- https://www.sondermind.com/resources/articles-and-content/is-artificial-intelligence-for-mental-health-safe/
- https://www.sondermind.com/resources/articles-and-content/california-sb-243-sets-a-new-regulatory-baseline-for-ai-companion-chatbots/
- https://www.sondermind.com/resources/clinical-resources/sondermind-clinical-results-delivering-effective-care-with-evidence-based-practices/
- https://www.sondermind.com/resources/announcement/technology-driven-behavioral-health-company-sondermind-raises-150-million-to-expand-mission-of-improving-clinical-outcomes/
- https://www.builtincolorado.com/job/principal-ai-engineer/3193831
- https://www.behavioralhealthtech.com/insights/engineering-empathy-how-were-building-ai-that-strengthens-not-replaces-human-care
- https://www.statnews.com/2025/12/01/ai-chatbot-headspace-talkspace-lyra-sondermind-digital-mental-health/
- https://www.fiercehealthcare.com/digital-health/behavioral-health-matchmaker-sondermind-hits-unicorn-status-150m-series-c
- https://bhbusiness.com/2023/03/22/sondermind-acquires-mindstrongs-tech-as-part-of-final-wind-down/
- https://www.mobihealthnews.com/news/mindstrong-sells-tech-assets-sondermind-shuts-down-operations
- https://news.crunchbase.com/startups/exclusive-mental-health-startup-sondermind-acquires-machine-learning-company-qntfy/
- https://www.businesswire.com/news/home/20210128005851/en/SonderMind-Adds-Chief-Financial-and-Chief-Product-Officer-to-Senior-Management-Team
- https://www.orrick.com/en/insights/2025/11/fdas-digital-health-advisory-committee-considers-generative-ai-therapy-chatbots-for-depression
- https://www.federalregister.gov/documents/2025/09/12/2025-17651/digital-health-advisory-committee-notice-of-meeting-establishment-of-a-public-docket-request-for
- https://files.lbr.cloud/public/2025-11/sonder%20mind.pdf
- https://www.beckersbehavioralhealth.com/behavioral-health-news/sondermind-lays-off-15-of-staff/
- https://www.unifygtm.com/insights-headcount/sondermind
- https://www.levels.fyi/companies/sondermind/salaries
- https://h1bdata.info/index.php?em=sondermind
- https://h1bgrader.com/h1b-sponsors/sondermind-inc-9k5n4596k1
- https://www.glassdoor.com/Salary/SonderMind-Salaries-E2895660.htm
- https://tracxn.com/d/companies/sondermind
- https://growjo.com/company/SonderMind
- https://finance.yahoo.com/news/sondermind-launches-suite-clinically-backed-130000392.html
- https://www.crunchbase.com/person/mark-frank
- https://www.zippia.com/sondermind-careers-1400273/executives/
