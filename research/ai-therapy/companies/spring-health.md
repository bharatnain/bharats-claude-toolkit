# Spring Health — Company Dossier

**One-line:** AI-augmented enterprise (B2B2C) mental-health benefits platform — "Precision Mental Healthcare" — that uses ML to match members to human clinicians, layered with a 2025 multi-agent LLM product (Guide). ~$3.3B valuation, 10M+ lives. Mission and commercial model are tightly aligned; the evidence base is real and peer-reviewed but largely self-authored.

**Overall confidence:** High (verifier-confirmed on funding, AI-safety/VERA-MH, and crisis study; key caveats flagged below).

**Label key:** *sourced* = directly supported by a primary/credible source; *inference* = reasoned from evidence (incl. argument-from-silence); *speculation* = plausible but unconfirmed; *contested* = sources/figures conflict or are self-reported; *unsupported* = traces only to weak provenance or misidentified source; *unknown — not found* = not located.

---

## Dimension 1 — Journey / Origin Story

- Founded **May 1, 2016** by three Yale-affiliated, first-generation immigrants: **April Koh** (CEO, then a Yale undergrad), **Adam Chekroud** (Yale Psychiatry PhD; ML researcher), and **Abhishek Chandra** (engineering). *[sourced]*
- **Origin story:** Koh watched her college roommate cycle through seven antidepressants and saw the mental-health system as "broken" — long waits and trial-and-error matching. She found Chekroud's published ML papers (showing ML could outperform clinicians at predicting which antidepressant would work), emailed him, and built an MVP that put the treatment-matching algorithm online as a questionnaire. *[sourced]*
- The concept won **Yale's Thorne Prize for Social Innovation (2016)**. The founding thesis from day one: AI/ML can remove trial-and-error from mental-health care by matching the right person to the right care faster. *[sourced]*
- Became a **unicorn in 2021** (Series C, ~$2B). By 2024: **10M+ lives**, **400+/450+ employers** (see D9/contested figures), **10,000+ providers**. *[sourced]*
- Koh appeared on the **cover of TIME (2025)** and on the **TIME100 Next** list, framed around using AI to make mental-health support easier to find. *[sourced]*

---

## Dimension 2 — Tech Stack & Architecture

**Application / data stack** *(sourced from himalayas.app, undated aggregator listing — corroborated by job postings; treat consumer-app specifics as indicative, not authoritative)*:
- Backend: **Ruby on Rails + GraphQL**. Web frontend: **React/Redux**. Mobile: **Flutter**. Data/ML: **Python**. *[contested — aggregator-sourced]*
- Hosting: **AWS** (EC2, Lambda, S3, CloudFront, Route 53), **Docker**, **NGINX**, **Cloudflare/Fastly CDN**. *[contested — aggregator-sourced]*
- Data stack: **dbt + Airflow** (transformation/orchestration), **Looker** (BI), **Mixpanel** (product analytics), **Okta/OneTrust** (identity + privacy/consent). *[contested — aggregator-sourced]*

**ML/LLM platform layer** *(from AI/ML infrastructure job postings — higher confidence)*:
- **Kubernetes, Terraform (IaC), model registry, feature stores, CI/CD for models**, with stated **multi-cloud** capability (AWS/GCP/Azure). *[sourced]*
- LLM orchestration tooling: **LangGraph / LangSmith**. *[sourced]*

**Assessment:** A standard-to-sophisticated modern SaaS shape — nothing exotic at the app layer. The bar is raised above a typical SaaS app by MLOps/LLMOps tooling plus healthcare-grade data controls (data masking, training/clinical-data separation, HIPAA) and global/multi-region scale across a third-party clinician network. *[inference]*

---

## Dimension 3 — AI/ML Techniques & Models

Two distinct AI surfaces:

**(a) Classical ML provider matching — "Precision Mental Healthcare"** (the historic core differentiator):
- A clinically validated **3–5 min intake screen across 10+ conditions** feeds ML models that match members to providers using **demographics, clinical symptoms, social determinants of health (SDOH), and preferences**, with a continuous-improvement/outcomes-feedback loop. *[sourced]*
- The **exact algorithm class** (supervised / collaborative-filtering / neural net) is **not publicly disclosed** — treated as proprietary. *[sourced]*
- **CAUTION — conflated citation:** Earlier framing cited ScienceDirect S1098301525024052 as peer-reviewed validation of the *matching* ML. **The verifier found this is the wrong paper** — S1098301525024052 is the OJPHI/JMIR retrospective *outcomes* cohort study (~52,929 participants, 589 employers, 2021–2024; depression/anxiety effect sizes d=1.61 / d=1.82), **not** a matching-algorithm-validation study. **No located peer-reviewed publication specifically validates the provider-matching ML.** The "genuine data moat / validated matching ML" framing is therefore overstated. *[unsupported — for the matching-validation claim specifically]*

**(b) GenAI/LLM layer — "Guide" (2025, newer):**
- An **AI-led member experience built as a Multi-Agent System** spanning intake guidance, in-the-moment support, personalized recommendations, and clinical decision support. Early data: **5% more therapy sessions in first 7 weeks**; company-stated **95% satisfaction / 70% feel better / zero major safety concerns** in a 2025 study. *[sourced for the product description; outcome figures contested — see D5]*
- **Foundation models for Guide are not disclosed.** *[unknown — not found]*
- **VERA-MH** (their open-sourced AI-safety benchmark; GitHub SpringCare/VERA-MH; arXiv 2602.05088) is built on **LangChain + Pydantic** and supports **OpenAI (GPT-4o/5.2/5.4), Anthropic (Claude Sonnet 4.5 / Opus 4.5), Google (Gemini 3 Pro), Azure OpenAI, and Ollama**. *[sourced]*
- **Spring builds on third-party frontier foundation models rather than training/fine-tuning its own LLMs; its proprietary AI assets are longitudinal outcomes data + the eval/guardrail framework.** *[inference — argument-from-silence; VERA-MH is a benchmarking harness meant to test ANY external model, so its provider support says little definitive about what powers Guide. Plausible and likely, but not a sourced fact about the production stack.]*
- No public evidence of self-hosted/fine-tuned proprietary LLMs, nor of detailed RAG implementation specifics. *[inference]*

---

## Dimension 4 — Therapeutic Approach, Modalities & Human-in-the-Loop

**Care model:** A care-navigation + provider-network platform branded "Precision Mental Healthcare." It **does not deliver therapy via software**; **licensed human providers deliver care**. The stack spans digital self-guided resources, coaching, short-term outpatient therapy, medication management, and referrals to higher levels of care. *[sourced]*

**Modalities:** Delivered by credentialed human clinicians trained in evidence-based modalities. Provider-recruitment materials require training/experience in **CBT, DBT, EMDR, ACT, and CPT**. The approach is **generalist/eclectic** (providers combine modalities), NOT a single proprietary protocol. Nuance: the public "our approach" page markets the *matching algorithm*, not named modalities — the modality list comes from provider-recruitment pages. *[sourced]*

**How technique is encoded — the differentiator is the matching algorithm + measurement, not a coded therapy protocol:**
- Intake includes validated screeners (**PHQ-9** depression, **GAD-7** anxiety) plus socio-demographic data, family history, DSM-5 diagnostic criteria, SDOH, and engagement/utilization patterns. *[sourced]*
- "Peer-reviewed ML models" compare each person's data against "hundreds of thousands of data points" to match member-to-care-type and member-to-provider. *[sourced; note the "peer-reviewed matching" claim is the one the verifier flagged as unsupported — see D3]*
- **Measurement-based care (MBC)** is the workflow backbone: providers administer/document PHQ-9/GAD-7 on a cadence; the platform surfaces real-time provider feedback and care-plan adjustments. Technique is "encoded" mainly as data-driven routing + outcome tracking, with actual clinical technique left to humans. *[sourced]*

**Named AI products (2025):** **Guide** (member-facing AI), **Compass** (AI-enabled EHR / clinical decision support for providers, with "Continuous Care"), **Journeys** (digital self-help), **VERA-MH** (suicide-risk eval framework). Spring explicitly states AI **supports, not replaces**, clinicians. *[sourced]*

**Human-in-the-loop (strongly emphasized):** Per the **April 24, 2025 "Responsible AI"** announcement — "risk-aware design that prevents AI from making autonomous clinical decisions," "human-in-the-loop systems that ensure oversight and allow clinicians to review or override AI-generated content," an external AI Advisory Council, internal ethics reviews, and clinical validation. Master's-level licensed care navigators sit between intake and care. *[sourced]*

---

## Dimension 5 — Safety, Crisis Handling, Clinical Evidence & Regulatory

**Crisis handling (strongest, best-documented area):**
- **24/7 crisis line** (240-558-5796, option 2), available internationally, with a **24/7 team of master's-level licensed care navigators (LCSWs, LMHCs)** that proactively reaches everyone flagged for suicidal ideation — **most within 30 minutes** of flag generation, all contacted multiple times within 24 hours, documented for safety planning. *[sourced]*
- The flag is automated within the platform; the **exact instrument is not named** in the published abstract (likely PHQ-9 item 9 or a screener trigger, but unconfirmed). *[speculation]*

**Clinical evidence / trials:**
- **Crisis study:** Graupensperger, Hawrilenko, Brown, Baum, Ward, Chekroud, "Crisis Outreach, Treatment Engagement, and Outcomes After Suicide Risk Screening…," *Psychiatric Services* 77(1):5–12 (Jan 2026; online Nov 14 2025). **n=6,131** flagged for suicidal ideation with no treatment in prior 6 months. **87.3% attended ≥1 appointment within 6 months**; successful outreach → **2.37× odds of treatment initiation, 33% faster first appointment, 1.69× early retention, lower ideation recurrence (OR 0.70)**, and sustained reductions in ideation/depression/anxiety. *[sourced — verified against PubMed]*
  - **Caveat:** Observational real-world cohort, **not an RCT**, authored by **Spring-affiliated researchers on Spring's own data**. *[inference]*
  - The "**339 employers / 50 countries**" sub-detail was **not visible in the abstract** retrieved — treat as unconfirmed. *[speculation]*
- **Outcomes study:** The **92.3% "reliably improved or recovered"** headline figure traces to a real peer-reviewed publication (**OJPHI/JMIR, ~53k patients**) — so it is more than bare marketing. **However**, it is a **retrospective, single-arm cohort on Spring's own platform data, authored by Spring-affiliated researchers, with no control arm.** Peer-reviewed: yes. **Independent: no.** *[contested]*
- **"56% faster" improvement** and **"$3 saved per $1 invested" (≈$3:$1 ROI)** lack located peer-reviewed backing and remain **company-stated**. *[contested]*
- **"Endorsed by the American Psychiatric Association (APA)":** This claim appears **only in Spring's own marketing copy**, repeated by third parties quoting it. No primary APA source, press release, or endorsement program was located; the APA does not run a vendor-endorsement program of this kind. **Treat as marketing laundered as a third-party credential.** *[unsupported]*

**AI safety / VERA-MH (notable industry contribution):**
- **VERA-MH** (Validation of Ethical and Responsible AI in Mental Health) released open-source **Oct 20, 2025**, with an expert council incl. Spring CMO Dr. Mill Brown and Stanford's Dr. Nina Vasan. First open-source, clinically grounded benchmark for whether mental-health AI chatbots recognize/respond to suicidal ideation, escalate to humans, and maintain boundaries across multi-turn interactions. Public comment ran through Dec 20, 2025. *[sourced]*
- **Methodology:** persona agents + an **LLM judge** against clinical rubrics; judge aligned with clinical consensus at **IRR=0.81** (vs ~0.77 inter-clinician). *[sourced — verified against arXiv 2602.05088]*
- **VERA-MH findings (Feb 11, 2026, PR Newswire + arXiv 2602.05088 / 2605.13318):** commercial AI models show **meaningful gaps/differences** in risk evaluation, supportive response, guiding to human care, and boundaries. *[sourced]*
- **Caveat:** VERA-MH is an **arXiv preprint** (submitted 2026-02-04), **not yet confirmed as formally peer-reviewed/published**, and authorship is **entirely Spring's own team** (Bentley, Belli, Chekroud, Ward, Brown, Hawrilenko et al.). *[contested]*

**FDA / regulatory status:**
- **NOT** an FDA-cleared/authorized medical device and **NOT** a Prescription Digital Therapeutic (PDT). Operates as an **employer/health-plan mental-health benefit and modernized EAP (EAP+)**. *[sourced for product framing]*
- Governed by **HIPAA** (employers cannot see who uses the service or ideation flags), **state clinical-licensure** rules, and **EAP/benefits frameworks** — not the FDA 510(k)/De Novo device pathway. No FDA submission/clearance located. As an AI vendor it is currently under **voluntary self-regulation** (AI Advisory Council, VERA-MH). *[inference — argument-from-absence; cited PMC article is general PDT context, not Spring-specific]*

---

## Dimension 6 — Engineering Difficulty: **3/5**

The application and data stack (Rails/React/Flutter/Python on AWS; dbt/Airflow/Looker) is conventional, well-supported SaaS engineering — alone, a **2/5**. Difficulty is pushed to a **3/5** by three things:

1. A **production multi-agent clinical LLM system ("Guide")** with hard safety requirements (risk detection, human-in-the-loop override, escalation to live clinicians) in a high-liability mental-health context — plus a non-trivial open-source eval/guardrail framework (**VERA-MH**: persona + LLM-judge architecture validated against clinical consensus).
2. A **proprietary ML matching engine** tied to a **longitudinal outcomes-measurement feedback loop** — real applied ML, not a wrapper (though, per D3, its *matching-specific* peer-reviewed validation is **not** established).
3. **Healthcare-grade data governance** (HIPAA, data masking, training/clinical separation), **multi-cloud MLOps/LLMOps** (Kubernetes, Terraform, model registry, feature stores, LangGraph/LangSmith), and **global scale** + a real-time sub-30-minute suicide-risk flagging/outreach orchestration pipeline.

**Not a 4–5** because they **orchestrate third-party frontier foundation models** (OpenAI/Anthropic/Google) rather than training/fine-tuning their own; there is no evidence of novel model architecture or large-scale infra research; and the matching ML, while real, is classic feature-based modeling. The hard parts are **systems integration, clinical safety, and data governance** — demanding senior execution, but not frontier-research-level engineering.

---

## Dimension 7 — Founders, Key Hires, Headcount & Org Shape

**Founders (2016, met at/around Yale; three first-generation immigrants):**
- **April Koh** — Co-Founder & CEO. Computer-science + political-science background per profiles. TIME cover, 2025. *[sourced]*
- **Adam Chekroud** — Co-Founder & **President** (most consistently cited). BA Experimental Psychology + MS Neuroscience (Oxford), PhD Psychology/Neuroscience (Yale, 2018); Assistant Professor Adjunct in Psychiatry at Yale School of Medicine. His predictive-modeling research (JAMA Psychiatry, Lancet Psychiatry, PNAS) is the clinical/technical core of the matching engine. **Exact C-title contested** across aggregators (President vs Chief Product Officer vs Chief Scientific Officer); co-founder status and ML-research role are not in dispute. *[sourced / title contested]*
- **Abhishek Chandra** — Co-Founder, engineer. Least publicly documented; **current title/role not confirmed** in reviewed sources. *[sourced for co-founder status; current role = unknown — not found]*

**Other named executives** (Craft.co / Clay / Comparably aggregators — **NOT primary-sourced; verify before relying**): Debbie Markowitz (CFO), Eugene Ho (CPO), Riley End (COO), Marc Jacobs (CRO), Karishma Patel (Chief People Officer). *[speculation — aggregator-sourced, unverified]*

**Headcount & org shape:**
- **~3.4K–3.5K employees** as of late 2025 / 2026 (aggregator estimates), up from ~2.6K in 2024. Exact figure **not company-confirmed**. *[inference — aggregator]*
- **Department split** (Unify aggregator estimate, 2026): Healthcare/clinical **~480** (~one-third), Sales & Support ~229, **Engineering ~182**, Business Management ~153, Marketing & Product ~138. Plus **10,000+ contracted care providers** (largely not W-2 headcount). *[inference — single aggregator]*
- Scale context: **$3.3B valuation** after $100M Series E (Jul 2024); 10M+ lives, 450+ directly contracted employers. *[sourced]*

**Takeaway:** A founder-led (CEO still in seat), research-driven company where **clinical/care-delivery is the largest functional group** and engineering is a relatively lean ~180-person org — consistent with a benefits-platform + contracted-network model rather than a heavy in-house product-engineering shop. *[inference]*

---

## Dimension 8 — Compensation Bands

Primary source = **Levels.fyi** (self-reported; small samples; updated June 2026). Directionally useful, **not reliable bands** — the data is internally inconsistent across pages and several engineering equity samples show $0 (likely incomplete reporting, not a cash-only structure).

**Levels.fyi median TOTAL comp by role** *[sourced — but small-sample/contested]*:
- Software Engineer: **$208K** median (range ~$145K–$208K+)
- Software Engineering Manager: **~$200K–$246K** (inconsistent across pages: $145K–$203K on role page vs $246K on company overview — **soft**)
- Data Scientist: **$169K**
- Data Science Manager: **$211,935**
- Product Manager: **$187,200**
- Product Designer: **$178,000**
- Business Operations Manager: **$232,356**
- Financial Analyst: **$218,900** *(single point — anecdote, not a band)*
- Human Resources: **$210,000**
- Recruiter: **$130,000** (stated low-end)
- Sales: **$149,250**
- Chief of Staff: **$704,460** *(single data point, very small sample — do NOT treat as a band)*
- **Equity:** standard 4-year vest, 25% year-1 cliff then monthly. *[sourced]*

**H1B LCA data** (DOL via h1bgrader / aggregators — **BASE salary floors**, not total comp; aggregator-reported, the direct page 403'd):
- Data Scientist: **~$153,874 avg base**; up to ~$244,795 (90th pct); a Senior DS posting cited **$190K–$232.5K base**. *[sourced — aggregator; sparse/incomplete filings]*
- Roles filed: Software Engineer, Quality Engineer, Data Engineer, Data Scientist. **Thin coverage** (one source: 0 LCAs FY2023). *[contested / sparse]*

**Glassdoor:** separate SWE and Data Scientist (9 submissions) pages exist; **specific figures not extracted** this pass. *[unknown — not captured]*

**Comp takeaway:** SWE total comp clusters **~$200K median** (NYC-weighted); DS lower (~$169K total / ~$154K base); PM/Design ~$178K–$187K; managers ~$210K–$246K. Sample sizes are small across the board. *[inference]*

---

## Dimension 9 — Funding & AI Investment

**Total raised:** commonly cited **~$466M–$509M across ~13 rounds** (trackers disagree on the exact total). *[sourced — range]*

| Round | Amount | Date | Lead / Notes |
|---|---|---|---|
| Seed | ~$6M | by 2018 | Wikipedia; date/amount less firmly sourced *[speculation]* |
| Series A | ~$22M | Jan 2020 | *[sourced]* |
| Series B | $76M | Nov 2020 | **Tiger Global** lead; Northzone, Rethink Impact, William K. Warren Foundation, Work-Bench, SemperVirens, Able Partners, True Capital, Operator Partners. Total → ~$106M. *[sourced]* |
| Series C | $190M | Sep 2021 | **Kinnevik AB** lead; ~$2B valuation (**unicorn**); expand family services + health-plan partnerships. *[sourced]* |
| Series D | ~$71M | Apr 2023 | ~$2.5B valuation; **lead not clearly disclosed**. *[sourced — amount/valuation; lead unconfirmed]* |
| Series E | $100M | Jul 31 2024 | **Generation Investment Management** (Al Gore's fund) lead; Kinnevik, William K. Warren Foundation, RRE, Northzone; **$3.3B valuation**. *[sourced — confirmed across Fortune, Fierce Healthcare, Crunchbase, Built In NYC + company release]* |

- **Series E stated use:** "double down on our strengths, increase access, scale our impact, and continue to deliver even greater ROI to employers." *[sourced]*
- **AI as the capital story:** funding positioned explicitly to scale AI that empowers providers and speeds member access. Notable AI assets: **Compass** (mental-health-specific EHR with AI insights / "Continuous Care"), **ML provider matching** (demographics + SDOH + clinical data), **VERA-MH** (responsible-AI framework). *[sourced]*

---

## Dimension 10 — Business Model & Drivers Behind the Tech

- **B2B2C:** sells to large employers and health plans, **not consumers**. *[sourced]*
- **Predominantly Per-Employee-Per-Month (PEPM) subscription**, tiered by clinical integration/service level (digital access → onsite programs + executive coaching). *[sourced for model shape]*
- **~75% of revenue from PEPM** and a stated aim to **shift 10–20% of revenue to outcomes-linked payouts by 2026** — these specific percentages come from a **generic third-party business-model blog, not primary filings**; Spring is private with no public financials. **Do not rely on as fact.** *[unsupported]*
- Additional revenue: utilization-based fees for premium clinical services (psychiatry, extended therapy), health-plan/carrier management fees, and premium upsells (onsite, executive coaching, enterprise integrations). Increasingly layering **outcomes-based/value-based contracts** tied to reduced ER visits and improved PHQ-9 scores, with ROI performance guarantees. *[sourced/contested]*
- **Economic logic drives the tech:** because employers pay largely **fixed PEPM** and Spring **guarantees ROI/net savings**, Spring is financially exposed to (a) **low utilization** and (b) **poor/slow clinical outcomes**. AI provider-matching and MBC (Compass) exist to **raise utilization AND speed recovery** — simultaneously improving outcomes and protecting margins under value-based/guarantee deals. *[inference]*
- Company claims **~$3 saved per $1 invested**, **92% clinical improvement**, recovery in **~8 weeks**, and "first in its category to earn external validation of net savings (2023)." It positions against legacy EAPs (low utilization, no outcome measurement). *[contested — see D5 for the independence/validation caveats]*

---

## Dimension 11 — Stated vs. Real Motivations

**Stated motivation:** Fix a "broken," low-tech, trial-and-error mental-health system using AI/precision matching to get people the right care faster and reduce suffering — a mission-driven framing reinforced across founder interviews, the TIME cover, and the Thorne Prize origin story (Koh's roommate cycling through seven antidepressants; Chekroud's research showing ML can outperform clinicians at treatment matching). *[sourced]*

**Real (commercial) motivation:** Build a **high-growth, venture-scale enterprise SaaS business** that captures the large, under-penetrated corporate mental-health-benefits market by **out-competing legacy EAPs on measurable ROI/outcomes**. Koh has **explicitly stated** the ambition to build "one of the world's most valuable companies" by delivering mental healthcare while reducing employer healthcare spend. *[sourced]*

**Alignment (the key judgment):** The two motivations are **largely aligned rather than in conflict**. Spring's revenue model (PEPM + outcomes guarantees) **only works if care actually improves outcomes and utilization** — so "improve care" and "protect margins" are the *same lever*. AI doubles as both the clinical engine and the investor/fundraising narrative. *[inference]*

**Caveat / where the narrative is softest:** Nearly **all** outcome/ROI claims (utilization lift, $3:$1 savings, 92% improvement, "56% faster," APA "endorsement") originate from Spring's **own marketing or company-affiliated studies**. Independent third-party scrutiny in the gathered sources is thin. The verifier flagged a **systematic self-authored-evidence pattern**: the crisis study, the OJPHI outcomes study, and the VERA-MH preprint are **all authored by Spring employees/affiliates on Spring's own data** — peer-reviewed in two cases, but **not independent**. The "APA-endorsed" claim is **unsupported marketing**. The strength of the outcomes claims is therefore **not externally settled**. *[inference]* **Motivation confidence: medium–high.**

---

## Dimension 12 — Risks, Gaps & Open Questions

- **Matching-ML validation is not established.** No located peer-reviewed paper independently validates the provider-*matching* algorithm; the citation previously used (ScienceDirect S1098301525024052) is actually an *outcomes* study, not a matching-validation study. The "data moat / validated matching ML" framing is overstated. *[unsupported]*
- **Self-authored evidence base.** Flagship studies + VERA-MH are all Spring-affiliated work on Spring's own data — credible but not independent. *[inference]*
- **"APA endorsement" is unsupported** — traces only to Spring's marketing. *[unsupported]*
- **Stale/inconsistent figures.** Employer count given as both "400+" and "450+"; "10M+ lives," headcount, and department splits are ~2 years old or aggregator estimates; Levels.fyi comp is internally inconsistent. *[contested]*
- **Weak-provenance business figures.** The ~75%-PEPM and 10–20%-outcomes-by-2026 numbers come from a content-farm blog, not primary sources. *[unsupported]*
- **Aggregator dependence.** Tech stack (himalayas.app, undated), exec roster (Craft/Clay/Comparably), headcount (Unify), and H1B salaries (h1bgrader, 403'd) all rest on unverified third-party aggregators. *[contested]*
- **VERA-MH is an arXiv preprint**, not yet confirmed as formally peer-reviewed. *[contested]*

**Not found / unknown:**
- Foundation models powering **Guide** specifically — **unknown — not found.**
- Exact **provider-matching algorithm class** — **unknown — not found** (proprietary).
- Exact **suicidal-ideation auto-flag instrument** — **unknown — not found** (likely PHQ-9 item 9; unconfirmed).
- **Abhishek Chandra's current role/title** — **unknown — not found.**
- Any **FDA interaction** — **unknown — not found** (none located; inferred N/A).
- Independent (non-company) replication of the 92% / 56% efficacy figures — **unknown — not found.**

---

## Stated vs. Real Motivations (summary subsection)

- **Stated:** Mission to fix a broken, trial-and-error mental-health system with AI/precision matching, rooted in the founders' Yale experience.
- **Real:** Win the enterprise mental-health-benefits market at venture scale and high valuation by beating legacy EAPs on measurable ROI — Koh openly states the goal of building "one of the world's most valuable companies."
- **Verdict:** Mission and commerce are **tightly aligned** (the PEPM-plus-guarantee model pays off only if AI-driven matching genuinely raises utilization and speeds recovery), so improving care and protecting margins are the same lever. AI serves as both clinical engine and fundraising narrative. The main tension is **evidentiary**, not motivational: the outcome claims that justify both the mission and the model are largely self-generated. *[inference — confidence medium–high]*

## Engineering Difficulty (3/5) (summary subsection)

**3/5.** Conventional SaaS app/data stack (would be a 2) lifted to a 3 by: (1) a production multi-agent clinical LLM system with hard safety/escalation requirements in a high-liability domain + the non-trivial VERA-MH eval harness; (2) a real applied-ML matching engine on longitudinal outcomes data with an MBC feedback loop + a sub-30-min suicide-risk outreach pipeline; (3) healthcare-grade data governance and multi-cloud MLOps/LLMOps at global scale. **Not 4–5** because Spring **orchestrates** third-party frontier models rather than training/fine-tuning its own, shows no novel model architecture or infra research, and its matching ML is classic feature-based modeling. The hard parts are systems integration, clinical safety, and data governance — senior execution, not frontier research.

---

## Sources

- https://www.fiercehealthcare.com/health-tech/mental-health-benefits-company-spring-health-hits-33b-valuation-boosted-100m-series-e
- https://www.springhealth.com/news/series-e-funding-accelerate-growth-expand-global-access
- https://www.springhealth.com/news/fortune-exclusive-ai-powered-mental-health-startup-boosts-valuation
- https://himalayas.app/companies/spring-health/tech-stack
- https://job-boards.greenhouse.io/springhealth66/jobs/4611478005
- https://www.springhealth.com/our-approach
- https://www.springhealth.com/blog/how-data-driven-provider-matching-helps-members-get-better-faster
- https://www.sciencedirect.com/science/article/pii/S1098301525024052 *(misidentified — outcomes study, NOT matching validation)*
- https://ojphi.jmir.org/2025/1/e72999
- https://www.springhealth.com/blog/building-ai-native-mental-health-company-next-decade-will-need
- https://arxiv.org/abs/2602.05088
- https://github.com/SpringCare/VERA-MH
- https://www.springhealth.com/news/responsible-ai-in-mental-healthcare
- https://www.prnewswire.com/news-releases/spring-health-sets-a-new-standard-for-responsible-ai-in-mental-healthcare-302436519.html
- https://www.springhealth.com/solutions/for-providers
- https://www.springhealth.com/blog/ai-in-mental-healthcare
- https://psychiatryonline.org/doi/10.1176/appi.ps.20250319
- https://pubmed.ncbi.nlm.nih.gov/41236311/
- https://www.springhealth.com/news/spring-health-expert-council-vera-mh-first-open-source-evaluation-ai-mental-health
- https://www.prnewswire.com/news-releases/vera-mh-findings-highlight-gaps-in-how-ai-chatbots-respond-to-suicidal-ideation-302684585.html
- https://www.springhealth.com/eap
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12090883/
- https://en.wikipedia.org/wiki/Spring_Health
- https://som.yale.edu/blog/womens-innovator-breakfast-april-koh-of-spring-health
- https://som.yale.edu/story/2025/april-koh-co-founder-ceo-spring-health-featured-cover-time
- https://medicine.yale.edu/profile/adam-chekroud/
- https://theorg.com/org/spring-health/org-chart/adam-chekroud
- https://www.nbcnews.com/news/asian-america/how-three-first-generation-immigrants-are-using-machine-learning-improve-n838136
- https://craft.co/spring-health/executives
- https://www.unifygtm.com/insights-headcount/spring-health
- https://news.crunchbase.com/startups/exclusive-spring-health-provides-path-to-mental-health-benefits-with-76m-series-b/
- https://www.prnewswire.com/news-releases/spring-health-raises-76-million-in-series-b-financing-301176026.html
- https://www.fiercehealthcare.com/digital-health/spring-health-snags-190m-to-expand-family-mental-health-services-for-global
- https://news.crunchbase.com/health-wellness-biotech/mental-health-startup-funding-spring-health/
- https://tracxn.com/d/companies/springhealth/__Xu0rl5oMReMHYze74KwKhKbfOG5DD84bxEw93AIXYX0/funding-and-investors
- https://time.com/7321471/april-koh-interview-time100-next/
- https://www.springhealth.com/blog/electronic-health-record-compass-ai-continuous-care
- https://businessmodelcanvastemplate.com/blogs/how-it-works/spring-health-how-it-works *(weak provenance)*
- https://www.levels.fyi/companies/spring-health/salaries
- https://www.levels.fyi/companies/spring-health/salaries/software-engineer
- https://www.levels.fyi/companies/spring-health/salaries/software-engineering-manager
- https://h1bgrader.com/h1b-sponsors/spring-care-inc-dba-spring-health-em2m8mv5k1 *(aggregator; direct page 403'd)*
- https://www.glassdoor.com/Salary/Spring-Health-Data-Scientist-Salaries-E2612026_D_KO14,28.htm
