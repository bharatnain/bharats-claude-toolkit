# Jimini Health (Sage) — Company Dossier

**One-line:** Clinician-supervised, EHR-integrated patient-facing LLM agent ("Sage") for behavioral health that supports patients between therapy sessions; differentiated by a self-published safety/evaluation architecture and an in-house multi-state clinic used as a pre-deployment QA gate. ~$25M+ raised, ~20–25 employees, no published efficacy data and no FDA clearance.

**Overall confidence: medium.** Funding, founders, dates, org shape, and B2B targeting are well-corroborated across independent outlets. Nearly all safety/architecture specifics trace to a single self-published vendor white paper (July 8, 2025) with no independent audit, dataset release, or efficacy data — accurately quoted, but design claims rather than validated capabilities.

---

## Dimension 1 — Company Journey

- Founded ~2023; NYC headquarters. [sourced — linkedin.com/company/jiminihealth]
- Launched publicly November 19, 2024 with $8M pre-seed funding. [sourced — globenewswire 2024-11-19]
- Co-founded by three people splitting the top of the org rather than a single-CEO model: **Luis Voloch** (Co-Founder & CEO), **Sahil Sud** (Co-Founder & Chief Product Officer), **Mark Jacobstein** (Co-Founder & President). [sourced — jiminihealth.com/company]
- Founding thesis: the "once-a-week therapy model leaves patients unsupported between sessions," a gap LLMs can fill; AI should "superpower clinicians, rather than replace them." [sourced — globenewswire 2024-11-19]
- Voloch openly aspires to build "a Genentech-like company in mental health, powered by AI," applying biotech-style scientific rigor. [sourced — eqvista.com interview]
- **Strategic evolution (load-bearing):** At 2024 launch Jimini was framed as a hybrid virtual-therapy provider (licensed clinicians + AI between sessions, CBT-based care). By the March 2026 raise it is repositioned as B2B "clinician-supervised AI infrastructure" sold to large multi-site behavioral health organizations and hospital systems — a shift from delivering care to selling the platform that lets health systems deliver supervised AI care. [sourced — jiminihealth.com 2026; hitconsultant 2026-03-31] [inference: this 2024→2026 shift represents a strategic pivot toward a more scalable, defensible enterprise-platform model]
- Advisors/backers spanning biotech and health policy include Robert Langer (Moderna co-founder) and Andy Slavitt (former CMS Acting Administrator). [sourced — prnewswire 2025-07-08; hitconsultant 2026-03-31]

---

## Dimension 2 — Tech Stack & Architecture

- Sage is described as an **"LLM agent" that does not improvise**: it closely follows a specific care plan authored by the human clinician, leaving all diagnostics and care decisions to the clinical team. [sourced — hitconsultant 2026-03-31]
- **Deeply integrated into the EHR** of large, multi-site behavioral health organizations. No EHR vendor, integration standard (e.g., FHIR), or stack component is publicly named. [sourced — hitconsultant 2026-03-31] [inference: integration specifics not disclosed]
- Architecture layers a constrained conversational agent over a bank of **"always-on" safety classifiers** plus an **escalation/alerting pipeline** that surfaces structured, plain-language alerts to the supervising therapist. Detection follows multi-step logic: detection → clarification step → escalation protocol. [sourced — jiminihealth.com white paper 2025-07-08]
- **In-house clinic as a staging/QA environment:** Jimini operates its own multi-state clinical practice where every model version is used and vetted by full-time licensed clinicians treating real patients before nationwide deployment — an operational architecture that is itself a differentiator. [sourced — hitconsultant 2026-03-31; Unite.AI; jiminihealth.com] [contested/caveat: specific states not disclosed; vendor self-report]
- **Foundation model provider NOT disclosed** in any reviewed public source. [sourced (verified absence) — statnews 2026-03-31]
- The white paper references **"frontier models" only for synthetic-data generation** used to train classifiers — not as the runtime conversational base model. The inference that the patient-facing agent itself rides on a third-party frontier LLM is plausible but **not directly stated**. [inference — jiminihealth.com white paper 2025-07-08] [verifier flag: slight overreach to treat the synthetic-data line as evidence about the conversational model's provenance]
- **RAG / retrieval architecture:** not described. Care-plan-following implies conditioning on clinician-authored plans and patient context, but the mechanism is not disclosed. [inference / not found]

---

## Dimension 3 — AI/ML Techniques & Models

- **Foundation model:** Builds on third-party frontier LLMs rather than training its own base model (provider unnamed). Note the "frontier models" phrase in the white paper specifically refers to synthetic therapy-conversation generation for classifier training, not the runtime agent. [sourced "frontier models" / inference on third-party — jiminihealth.com white paper 2025-07-08]
- **Classifiers:** "More than ten always-on, high-risk classifiers." Each is LLM-based and was fine-tuned on synthetic therapy conversations generated by frontier models. [sourced — verified verbatim in white paper 2025-07-08]
  - **Named classifier domains (white paper, verbatim):** suicidal ideation, psychotic symptoms, and noncompliance with prescribed medications. [sourced]
  - **Correction (verifier flag — classifier-domain conflation):** "child/vulnerable-adult endangerment" does **NOT** appear in the white paper's named classifier list; it comes only from the PR/secondary framing and should not be attributed to the white paper. [contested — PARTIALLY REFUTED]
- **Proprietary data / evals:** PhD-level clinicians manually annotated conversations, blind to model predictions, to build a "gold-standard" evaluation set. This clinician-annotated eval set plus the in-house clinic's real supervised interaction data form the proprietary-data moat. [sourced — verified verbatim] [caveat: no dataset, size, or inter-rater reliability published; "gold-standard" not externally validated]
- **Alignment:** "Deliberate Safety Alignment" — explicitly trained to align with therapist-defined safety priorities beyond generic "helpfulness," incorporating clinical judgment; explicitly engineered to avoid "overrefusal" (prematurely ending conversations at the first sign of distress). RLHF is not named verbatim. [sourced — emhicglobal / white paper 2025-07-08]
- **Interpretability:** Each safety decision carries a traceable, plain-language rationale (which classifiers fired, concern level, which policy applied) for clinical review. [sourced — white paper 2025-07-08]
- **AI judges:** "Dedicated AI judges — models trained specifically to evaluate outputs for safety, tone, and alignment with clinical standards" (an LLM-as-judge eval pipeline). [sourced — white paper 2025-07-08]
- **Red-teaming:** Adversarial testing of new capabilities before exposure to real users. [sourced — white paper 2025-07-08]
- **Staged deployment:** Internal validation → small cohort with full clinician review (24–48h) → adaptive (sampled) oversight → targeted (flag-triggered) oversight. The "24–48 hours" window is verified in the white paper. [sourced — white paper 2025-07-08]
- **Published framework:** "The New Hippocratic Code: An LLM-native Safety Framework for Patient-Facing AI in Mental Health" (July 8, 2025).
  - **Four pillars — corrected to white-paper verbatim titles (verifier flag — pillar-name conflation):** (1) Continuous Human Oversight; (2) Transparent, Interpretable Reasoning; (3) Staged, Evaluation-Driven Deployment; (4) Align AI Systems with Clinical Safety Priorities. [contested — REFUTED as previously stated] The earlier-cited titles ("Continuous Clinical Oversight & Steering," etc.) are the **PR's marketing rephrasing**, not the white paper's own names. Substance is consistent; verbatim titles differ by source. [jiminihealth.com white paper vs prnewswire 2025-07-08]
- **Marketing-as-fact caveat:** Nearly all of the above (10+ classifiers, gold-standard evals, AI judges, deliberate safety alignment, staged deployment) trace to a single self-published vendor white paper with no independent audit, dataset release, or efficacy data. Accurately quoted, but read as design claims, not validated capabilities. [verifier flag]

---

## Dimension 4 — Therapeutic Approach, Modality Encoding & Human-in-the-Loop

- **Modalities:** CBT is the only modality confirmed consistently across primary sources (launch PR Nov 19, 2024; greenhouse therapist job postings). The company describes "evidence-based practices and measurement-based care" on its own site without enumerating modalities. [sourced — globenewswire 2024-11-19; greenhouse]
- DBT, trauma-informed care, mindfulness, and "measurement-based care" appear only in secondary/aggregator sources and are **not confirmed in Jimini's own primary materials** — treat as lower-confidence. [contested — choosingtherapy.com 2025; zoonop]
- **How technique is encoded (the differentiator):** Sage does not operate as an open-ended LLM. A licensed clinician authors an individualized treatment plan, and Sage is "integrated directly into each patient's treatment plan," delivering tailored prompts and exercises aligned with therapeutic goals between sessions (reminders, skill practice, between-session reinforcement). Per March 2026 coverage, Sage "closely follows the plan of the human clinicians; it does not improvise" and "leaves all diagnostics and care decisions to the human team." Technique is therefore encoded **indirectly via the clinician-authored care plan plus constrained instruction-following**, not via a modality-specific protocol model. The white paper adds that the agent's components "must justify actions with a clear, interpretable logic" — technique application is meant to be auditable, not black-box. [sourced — globenewswire 2024-11-19; hitconsultant 2026-03-31; white paper 2025-07-08]
- **Human-in-the-loop (defining design choice, core to the product):**
  1. Every single patient–Sage interaction is visible to the supervising provider. [sourced — medcitynews 2026-03-31; hitconsultant 2026-03-31]
  2. Clinicians are "always in the driver's seat"; Sage makes no diagnostic or care decisions. [sourced]
  3. Sage both receives instruction from the clinical team and escalates situations back, sharing patient progress to inform ongoing care. [sourced]
  4. Deep EHR integration into large multi-site behavioral health organizations (vendors/mechanism undisclosed). [sourced — hitconsultant 2026-03-31]
  5. Jimini runs its own multi-state clinical practice — every model version is used by Jimini's own clinicians before partner deployment (a validation gate, not just runtime supervision). [sourced — hitconsultant 2026-03-31]
- **Provenance caveat:** Several "does-not-improvise" / EHR-integration / multi-state-clinic claims are company messaging relayed through trade press, not independently verified facts. [verifier flag]

---

## Dimension 5 — Safety, Crisis Handling, Clinical Evidence & Regulatory

- **Safety architecture (four pillars, white paper July 8, 2025 — corrected verbatim titles):** (1) Continuous Human Oversight; (2) Transparent, Interpretable Reasoning; (3) Staged, Evaluation-Driven Deployment (red-teaming + clinician-reviewed pilots before scaling any feature); (4) Align AI Systems with Clinical Safety Priorities (always-on classifiers for high-risk cues producing conservative, risk-aware responses). [contested on titles / sourced on substance — jiminihealth.com white paper; prnewswire 2025-07-08]
- **Crisis handling / escalation:** Mechanism is real but described at a high level. Always-on classifiers detect high-risk cues (suicidality, psychosis; medication noncompliance per white paper). For providers, "Sage surfaces real-time risk signals with clear escalation pathways" and escalates necessary situations to the supervising clinician. Consumer-facing material directs crises to **988**. [sourced — insider.fitt.co 2024-11-19]
- **Not publicly detailed:** specific escalation latency/SLAs, fallback-to-human handoff steps, and Sage's exact patient-facing crisis-response script. [inference / not found]
- Marketing framing positions Sage against unsupervised consumer chatbots (cites ~1M+ weekly ChatGPT users discussing suicide and wrongful-death litigation against Character.AI/Google). [sourced — jiminihealth.com 2026]
- **Clinical evidence / trials:** NO completed RCTs and no published Sage outcome data. Clinical trials are "in the process of being set up" with U.S. universities (per July 8, 2025 white paper) — no registrations, arms, or completion dates found. [sourced — prnewswire 2025-07-08]
- Voloch's claimed efficacy/retention/CSAT "far better than industry norms" is **unpublished and unverifiable**. The evidence base is founder/advisor credentials and design rigor, not validated efficacy. [verifier flag — NO EFFICACY EVIDENCE]
- **Chief Scientist's peer-reviewed work — journal-name correction (verifier flag):** Jimini's PR cites "Nature Mental Health Research." No journal by that literal title exists; the relevant Eichstaedt-affiliated work is the **2024 Stade et al. roadmap in *npj Mental Health Research*** (a Nature-portfolio open-access journal) plus a Nature "Matters Arising" response. Underlying peer-reviewed work is real; the cited title as written is inexact. [contested — prnewswire PR vs jeichstaedt.com publications]
- **FDA & regulatory status:** NO FDA clearance, approval, or device classification mentioned in any source (verified absence). Company states compliance with federal and state regulations and positions Sage as clinician-supervised (clinicians make all care/diagnostic decisions), the typical posture for managing device classification. [sourced — insider.fitt.co 2026-03-31]
- **CMS ACCESS / FDA TEMPO — correction in Jimini's favor (verifier flag):** These are **real, correctly-named federal programs**, not unverifiable as earlier flagged. FDA launched the **TEMPO** (Technology-Enabled Meaningful Patient Outcomes) digital-health pilot, announced Dec 5, 2025 (Federal Register notice Dec 8, 2025). **CMS ACCESS** (Advancing Chronic Care with Effective, Scalable Solutions) is a 10-year CMMI model beginning July 5, 2026, with qualifying conditions including depression. [sourced — FDA.gov / Federal Register 2025-22190] **Remaining caveat:** these are a general regulatory tailwind and pathway, **not a Jimini-specific authorization**; "regulatory tailwind for Jimini" remains the company's interpretive framing. [contested on Jimini-specificity — hitconsultant 2026-03-31]

---

## Dimension 6 — Engineering Difficulty

**Engineering difficulty: 4/5** (tech dimension only).

- The core conversational capability rides on **third-party frontier LLMs**, which lowers difficulty — Jimini is not training a foundation model. [inference]
- What actually constitutes the product is genuinely hard: a bank of **10+ fine-tuned always-on safety classifiers**, **clinician-annotated gold-standard eval sets**, an **LLM-as-judge** evaluation pipeline, **interpretable per-decision rationale generation**, a multi-step **detection → clarification → escalation** alerting system wired into clinician workflows, **EHR integration** into multi-site behavioral-health orgs, and a **four-stage evaluation-driven deployment** regime. [sourced — white paper 2025-07-08; hitconsultant 2026-03-31]
- The patient-facing mental-health context (reliable detection of suicidality/psychosis, avoiding both missed risk and overrefusal, full auditability) imposes a safety and reliability bar far above a generic chatbot. The **in-house multi-state clinic as a pre-deployment QA loop** is a substantial operational build. [sourced]
- **Team strength supports execution:** CEO Luis Voloch (MIT BS Math/CS + MEng EECS; ex-Palantir ML; co-founder/CTO of Immunai, valued $1B+); advisors from Google DeepMind, Yale, Harvard Medical School, Stanford, Dartmouth, plus Robert Langer (Moderna co-founder). [sourced — crunchbase; prnewswire 2025-07-08]
- **Why not 5:** the heaviest ML lifting (pretraining a frontier model, novel architectures) is outsourced; differentiation is in safety/eval/ops engineering and clinical integration rather than frontier ML research. **Caveat:** foundation-model provider, EHR specifics, and any RAG architecture are undisclosed, so part of the stack is inferred. [inference]

---

## Dimension 7 — Founders, Key Hires, Headcount & Org Shape

- **Founders (three-way split at the top):** Luis Voloch (Co-Founder & CEO; ex-co-founder Immunai; MIT), Sahil Sud (Co-Founder & Chief Product Officer; ex-Ribbon Health, Palantir), Mark Jacobstein (Co-Founder & President; ex-Chief Business Officer at Guardant Health, ex-Immunai). Founder backgrounds are AI/biotech-heavy (Immunai lineage twice over), not traditional behavioral-health operators — clinical credibility is bolted on via hires and advisors. [sourced — jiminihealth.com/company; hitconsultant 2024-11-19]
- **Key internal leadership:** Dr. Bill Hudenko (Chief Clinical Officer); Dr. Johannes Eichstaedt, PhD (Chief Scientist; Stanford Assistant Professor (Research) of Psychology); Lynn Hamilton (Chief Commercial Officer); Aviv Laufer (VP Engineering); Katie Lutz (VP Business Development); Chiara Waingarten (VP Business Operations, founding team). [sourced — jiminihealth.com/company]
- Exec team draws from Talkspace, Guardant Health, and Ribbon Health. [sourced — hitconsultant 2026-03-31]
- **Advisory board (credibility moat):** Pushmeet Kohli (Google DeepMind VP of Science), Sabine Wilhelm (Harvard), Seth Feuerstein (Yale), Robert Langer (MIT/Moderna), David Feinberg (Oracle Health, ex-Geisinger CEO), Tim Althoff (UW), Nikolaos Daskalakis (BU), Deborah Adler; Andy Slavitt (ex-CMS) as backer. [sourced — jiminihealth.com/company; prnewswire 2025-07-08] [caveat: advisor association confers credibility, not validated product efficacy]
- **Org shape:** Classic seed/early-stage healthtech, functionally split across Engineering, Product, AI/Science, Clinical, and Commercial/BD, with a heavy scientific/clinical advisory bench. The company also directly employs licensed therapists (psychologist/LCSW/LMHC/LPCC/LPC) delivering primarily CBT — so the org includes a clinician delivery layer, not just software staff. [sourced — greenhouse.io/jiminihealth]
- **Headcount:** LinkedIn lists the 11–50 band ("View all 25 employees"); Built In showed ~21. Best estimate **~20–25 employees** as of mid-2026 — small, consistent with ~$25M raised. [inference — linkedin.com/company/jiminihealth] [caveat: "View all N" and Built In figures are noisy proxies, not audited]

---

## Dimension 8 — Compensation Bands

- **Only one verifiable posted band:** Senior Software Engineer (Backend) — **$185k–$250k base + equity**, 10+ years experience, hybrid (San Francisco plus two other locations), visa sponsorship offered. [sourced — getclera.com 2026-06-24] [caveat: getclera.com is a third-party aggregator mirror, one step removed from Jimini's own ATS]
- **No data found elsewhere:** h1bdata.info returned **zero LCA records** for Jimini Health (no visa-salary anchor); Levels.fyi has no Jimini entries; no verified Jimini-specific Glassdoor salary reports (Glassdoor "Jimini" hits appear to be a different entity). [sourced — h1bdata.info 2026-06-24] [inference — levels.fyi]
- Other postings (Senior SWE Front-End, Head of AI — both NYC, removed Aug 2025; Licensed Mental Health Therapist; Director of AI Engineering) had no retrievable posted band. [sourced — builtinnyc 2025-08-07]
- **Market estimates (NOT Jimini-confirmed):** Director of AI Engineering in NYC benchmarks ~$228k–$243k base; NYC AI engineer base commonly $145k–$310k with senior ML TC $400k+ incl. equity. Jimini's verified backend band sits at-market for senior SWE in NYC/SF, implying Jimini pays roughly at-market for a funded seed-stage startup. [speculation — salary.com 2026-06-01] [inference — getclera.com]
- Therapist and exec/founder comp: **unknown — not found** (no reliable role-level estimate without speculation).

---

## Dimension 9 — Funding & AI Investment

- **Two disclosed rounds, total >$25M:**
  - **Pre-seed: $8M**, announced Nov 19, 2024. Investors: Zetta Venture Partners, LionBird, PsyMed, BoxGroup, Arkitekt Ventures, SCB and others. [sourced — globenewswire 2024-11-19]
  - **Seed: $17M**, announced ~March 31, 2026; brings total to >$25M. Named investors: M13 (Morgan Blumberg), Town Hall Ventures, Zetta Venture Partners (reported as leads), plus LionBird, OneMind; Andy Slavitt (ex-CMS Acting Administrator) as individual backer. [sourced — mobihealthnews 2026-03-31; hitconsultant 2026-03-31]
- **Valuation:** NOT disclosed in any located source (verified absent). [sourced — statnews 2026-03-31]
- **Discrepancy:** One citybiz headline cites "$13M from M13, Town Hall Ventures, Others," conflicting with the $17M figure. The $17M figure is corroborated by the strong majority of independent outlets (MobiHealthNews, HIT Consultant, STAT, TechFundingNews); $13M is most likely a headline error or partial/lead-investor subset. [contested — citybiz.co 2026; citybiz body returned HTTP 403, unverifiable]

---

## Dimension 10 — Business Model & Business Drivers

- **Customer:** large multi-site behavioral health provider organizations and hospital systems (**B2B**) — not direct-to-consumer and not primarily payers. [sourced — jiminihealth.com 2026]
- **Revenue mechanism:** exact revenue model, pricing, and contract structures with health systems are **not publicly disclosed**. [sourced (verified absence) — statnews 2026-03-31]
- **Positioning:** explicitly "reimbursement-ready" — EHR-integrated, compliance-framework-built, and aligned to emerging CMS/FDA technology-enabled-care pathways (CMS "ACCESS," FDA "TEMPO"). [sourced — jiminihealth.com 2026]
- **Core business driver behind the architecture:** every patient–AI interaction visible to and supervised by a licensed clinician is simultaneously a clinical-safety feature **and** a regulatory/liability moat — what makes the product defensible and reimbursable in a market where unsupervised consumer chatbots (ChatGPT, Character.AI) face wrongful-death litigation. The "clinician-in-the-loop" design is as much a go-to-market and legal strategy as a clinical one. [inference]
- Voloch claims efficacy, retention, and CSAT "far better than industry norms," though no figures are public. [sourced — statnews 2026-03-31; unverifiable]

---

## Dimension 11 — Stated vs. Real Motivations

**Stated vs. real motivations**

- **Stated motivation:** Fix the structural gap in therapy — the traditional once-a-week model leaves patients unsupported between sessions — using clinically-supervised LLMs to "superpower clinicians, rather than replace them," delivering safer, evidence-based, continuous support. The 2026 framing adds a safety/public-health mission: patients are already using unsupervised general-purpose AI (1M+ weekly ChatGPT users discussing suicide), so health systems need clinician-supervised AI infrastructure to bring that behavior under clinical oversight responsibly. [sourced — direct quotes, globenewswire 2024-11-19; jiminihealth.com 2026]
- **Real motivation (confidence: medium):** Capture an emerging, reimbursable B2B market by owning the "safe/compliant" layer of patient-facing behavioral-health AI. The clinician-supervision architecture is the commercial moat: it differentiates Jimini from consumer chatbots facing wrongful-death lawsuits, makes the product sellable to risk-averse health systems, and positions it to capture new CMS/FDA reimbursement pathways. The 2024→2026 pivot from "hybrid therapy provider" to "infrastructure for health systems" reflects a move toward a more scalable, defensible, investor-attractive enterprise-platform play. Backers like Andy Slavitt (ex-CMS) and the explicit reimbursement framing signal the real driver is regulatory positioning and enterprise distribution, not just clinical philosophy. [inference]
- **Alignment assessment:** Stated and real motivations are **largely aligned** — clinical safety genuinely IS the moat — but the public-health framing also functions as **market-creation messaging that manufactures urgency** for health systems to buy now. Why medium and not higher: funding/investor/founder/B2B facts are well-sourced, and stated motivations are direct quotes, but exact revenue model, pricing, contract terms, and valuation are undisclosed — so the commercial mechanics of the "real motivation" reading are inferred, not confirmed. [inference]

---

## Dimension 12 — (not assigned in raw findings)

Unknown — not found. No raw findings were provided for a distinct twelfth dimension; the investigation covered dimensions 1–11 as enumerated above (with engineering difficulty as Dimension 6). If Dimension 12 refers to a specific category not surfaced here, it was not researched in the source material.

---

## Engineering difficulty (4/5)

See Dimension 6 above for the full rationale. Summary: **4/5.** Core conversation rides on outsourced third-party frontier LLMs (lowers difficulty), but the actual product — 10+ fine-tuned always-on safety classifiers, clinician-annotated gold eval sets, an LLM-as-judge pipeline, interpretable per-decision rationale generation, a detection→clarification→escalation alerting system wired into clinician workflows, EHR integration, a four-stage deployment regime, and a wholly-owned multi-state clinic as a pre-deployment QA loop — is genuinely hard and held to a patient-safety/reliability bar far above a generic chatbot. Falls short of 5 because the heaviest ML research (pretraining, novel architectures) is outsourced; differentiation is in safety/eval/ops engineering and clinical integration. Part of the stack (foundation-model provider, EHR specifics, RAG) is undisclosed and therefore inferred.

---

## Sources

- https://hitconsultant.net/2026/03/31/jimini-health-clinician-supervised-behavioral-health-ai/
- https://jiminihealth.com/blog/the-new-hippocratic-code-an-llm-native-safety-framework-for-patient-facing-ai-in-mental-health
- https://www.statnews.com/2026/03/31/jimini-health-raises-funding-ai-chatbot-sage-mental-health/
- https://emhicglobal.com/resources/jimini-health-advances-ai-safety-framework-for-digital-mental-health/
- https://www.prnewswire.com/news-releases/jimini-health-releases-technical-blueprint-for-safe-patient-facing-ai--adds-deepmind-and-yale-leaders-to-advisory-board-302500354.html
- https://www.crunchbase.com/person/luis-voloch
- https://www.mobihealthnews.com/news/jimini-health-raises-17m-expand-ai-behavioral-health-platform
- https://www.globenewswire.com/news-release/2024/11/19/2983540/0/en/Jimini-Health-Launches-with-8M-in-Funding-to-Transform-Mental-Health-with-Responsible-AI-Supported-Therapy.html
- https://www.choosingtherapy.com/jimini-review/
- https://medcitynews.com/2026/03/jimini-ai-mental-health/
- https://insider.fitt.co/press-release/jimini-health-launches-with-8m-in-funding-to-transform-mental-health-with-responsible-ai-supported-therapy/
- https://insider.fitt.co/press-release/jimini-health-raises-17m-as-behavioral-health-systems-face-growing-pressure-to-manage-patient-ai-use-with-clinical-grade-infrastructure/
- https://eqvista.com/interview-with-luis-f-voloch-jimini-health/
- https://jiminihealth.com/blog/jimini-health-raises-usd17m-as-behavioral-health-systems-face-growing-pressure-to-manage-patient-ai-use-with-clinical-grade-infrastructure
- https://www.citybiz.co/article/826428/jimini-health-raises-13m-from-m13-town-hall-ventures-others/
- https://jiminihealth.com/company
- https://hitconsultant.net/2024/11/19/jimini-health-launches-with-8m-for-ai-therapist-assistant-sage/
- https://www.linkedin.com/company/jiminihealth
- https://boards.greenhouse.io/jiminihealth/jobs/4145318007
- https://www.getclera.com/jobs/jimini-health/senior-software-engineer-backend
- https://h1bdata.info/index.php?em=Jimini+Health
- https://www.levels.fyi/h1b/
- https://www.salary.com/research/salary/benchmark/ai-engineering-director-salary
- https://www.builtinnyc.com/job/senior-software-engineer-front-end/6213772
- https://www.federalregister.gov/documents/2025/12/08 (FDA TEMPO notice 2025-22190)
- https://www.fda.gov/ (FDA TEMPO digital-health pilot announcement, Dec 5 2025)
- https://jeichstaedt.com/ (Eichstaedt publications; npj Mental Health Research, Stade et al. 2024)
