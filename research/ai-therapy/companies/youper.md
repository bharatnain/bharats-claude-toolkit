# DOSSIER: Youper

**One-line:** A lean, founder-led consumer mental-health chatbot whose real moat is clinical validation and psychiatrist-authored content rather than novel AI; it evolved from a 2021 decision-tree engine to a 2023 OpenAI-GPT generative hybrid, never raised after 2019, and has retreated to a "not a medical device" wellness positioning.

**Evidence labels:** `[sourced]` = verified against a primary/credible source · `[inference]` = reasoned from sourced facts · `[speculation]` = plausible but unverified · `[contested]` = sources disagree / internal contradiction · `[unsupported]` = asserted in raw findings but refuted or unverifiable.

---

## Dimension 1 — Company Journey & Origin Story

- Founded **January 2016** in **San Francisco** by Brazilian co-founders **Jose Hamilton Vargas (CEO)**, **Thiago Marafon (CTO)**, **Diego Dotta (CPO)**, with **Andrea Niles, PhD** also publicly listed as a co-founder (Chief Science Officer). `[sourced]`
- **Origin:** Hamilton, a clinical psychiatrist (~12 years / reportedly 3,000+ patients), saw that cost and long wait times kept people from care — "people need support now, not three months from now." After a 2015-16 data-science specialization at Johns Hopkins, he co-founded Youper. `[sourced]`
- **The pivot:** The first product delivered structured CBT techniques and produced symptom reduction but had **low engagement**; user interviews revealed people wanted "a confidant or friend," which drove the pivot to a **conversational AI emotional-health assistant**. `[sourced]`
- **Trajectory & retreat:** Youper built a clinical-validation narrative (Stanford/JMIR 2021) and pursued digital-therapeutics credibility, but by 2026 had **contracted sharply** (aggregators list ~4 employees) and its live site repositions Youper as a consumer "wellbeing AI chatbot" that explicitly states it is **"not a medical device"** and "not a substitute for professional mental health care." `[sourced]` This is a notable retreat from earlier prescription-digital-therapeutic / B2B-clinical ambitions. `[inference]`
- **The name** "Youper" = "You" + "Super" (founder framing: "help everyone on the planet become the best version of themselves"). `[sourced]`

> **Corrected claim:** The raw findings flagged a `[contested]` claim that "Youper received an FDA Breakthrough Device designation for anxiety in 2021." This is **`[unsupported]` — refuted**. No such designation exists for Youper; it belongs to **Wysa** (granted **May 2022**, for chronic pain with depression/anxiety). The claim is false on company, year, and indication — a clear entity conflation. See Dimension 5.

---

## Dimension 2 — Technology Stack & Architecture

- Youper is a **consumer mobile app** (iOS/Android), **text-only**, mobile-first, with **limited or no cross-session conversational memory** reported. `[sourced]`
- Third-party technographics list the stack as **Amazon EC2, MySQL, Nginx, Google Data Studio/Analytics, Airtable**, with **reCAPTCHA / HSTS / X-XSS-Protection** security headers — a conventional consumer-app cloud backend. `[inference]` **Caveat:** This is scraped third-party data (LeadIQ), possibly stale, and **not confirmed as current architecture** — treat as low-confidence. `[contested]`
- There is **no public disclosure of a sophisticated distributed/ML-serving architecture**. The architecture is best described as a standard consumer-app backend plus a conversational engine constrained by an expert-system decision tree. `[inference]`
- **Generated-content disclosure:** the safety page confirms all responses are AI-generated, but reveals **no model internals, no serving infrastructure, no scaling details**. `[sourced]`

---

## Dimension 3 — AI/ML Techniques & Models

This is the **most important and most nuanced** dimension, and the raw findings contained an internal contradiction the verifier corrected.

- **2021 (validated version):** The peer-reviewed JMIR study states verbatim: *"Youper primarily uses a decision tree to select its responses."* Conversation followed a structured flow (emotion rating → preset contributing factors → limited open-text → **randomly selected** intervention from a **predefined skill library**). The validated product was **rule-based / decision-tree NLP over a curated clinical content library — NOT a generative LLM.** `[sourced]`
- **2023 onward (current architecture):** Per CEO Dr. Jose Hamilton (LinkedIn, Mar 6 2023), the architecture is a **HYBRID**: a *"structured expert system (a complex decision tree) plus NLP plus generative AI built on OpenAI's GPT."* Verbatim: *"The expert system is a complex decision tree that guides how and when the generative AI interacts with the user to ensure the application of evidence-based interventions."* The CEO also references **"automatic input and output flagging"** and an intent to **"fine-tune GPT on relevant proprietary data."** `[sourced]`

> **`[contested]` → resolved:** The raw findings (Dims 3 & 6) leaned on the outdated "NOT an LLM / decision-tree" framing. The verifier corrects this: that description is accurate **only for the 2021 product**. **The current product is a generative-AI hybrid built on OpenAI's GPT, not a non-LLM system.** Older "non-generative" citations are outdated.

- **Vendor & disclosure:** The safety page discloses **no model internals**, but the CEO's 2023 article **partly discloses the vendor (OpenAI GPT)** and a fine-tuning intent. So the "wrapper over a vendor LLM with a guardrail layer" characterization is **closer to confirmed/`[inference]` than `[speculation]`**. `[inference]` What remains undisclosed: exact current model, whether fine-tuning was actually executed, RLHF, or RAG details. `[inference]`
- **Safety/guardrail layer:** A **suicidal-ideation/self-harm detection system** with escalation protocol and disclaimers (responses AI-generated, not clinician-reviewed). `[sourced]`
- **Genuine differentiated AI/ML assets** are NOT novel model R&D. They are: (a) **proprietary, psychiatrist-authored, clinically-structured intervention content**; (b) a **published clinical evidence base**; (c) **embedded validated clinical scales (PHQ-9, GAD-7)**. Defensibility lies in clinical validation and content. `[inference]`

---

## Dimension 4 — Therapeutic Approach, Modalities & Technique Encoding

- **Modalities:** CBT, ACT, DBT, IPT (Interpersonal Therapy), Problem-Solving Therapy, and Mindfulness-based CBT. `[sourced]`
- **Mechanisms (per JMIR):** interventions target **attention change, cognitive change, and context engagement**, operationalized as concrete skills: behavioral activation, goal setting, problem-solving, mindfulness, sleep relaxation, acceptance, cognitive restructuring, gratitude journaling, self-compassion. `[sourced]`
- **Delivery:** Fully automated **text-chat**, using **"just-in-time" interventions** (delivered at the moment of need). `[sourced]`
- **Fixed session loop:** identify emotion + rate intensity → select contributing factors → open-text entry → complete an emotion-regulation skill → **re-rate** emotion/intensity. `[sourced]`
- **How technique is encoded (load-bearing nuance):** The **decision tree / expert system encodes and constrains the clinical technique** (which intervention, and when), ensuring evidence-based delivery; in the current hybrid, **GPT handles conversational language generation within those guardrails.** This is the key 2021→2023 evolution. `[sourced]`
- **Human-in-the-loop: essentially NONE.** The clinical study defines the intervention as *"fully automated"* with *"no trained clinician."* The current safety page states: *"All responses are generated by AI and have not been reviewed by a licensed mental health professional."* It is a consumer-first self-help product, **not** coach- or therapist-augmented; there is **no live human escalation inside the app** (crisis is referred out — see Dim 5). `[sourced]`

---

## Dimension 5 — Safety, Crisis Handling, Clinical Evidence & Regulatory Status

### Safety / crisis handling
- The AI *"is designed to identify expressions of suicidal ideation, suicide, or self-harm"* and includes *"safeguards designed to prevent the AI from producing responses that contain instructions, encouragement, or detailed content related to methods of self-harm or suicide."* `[sourced]`
- CEO (2023) describes **automatic input and output flagging** as moderation on top of GPT. `[sourced]`
- On detecting distress, Youper **refers out** (does not intervene): **988 Suicide & Crisis Lifeline**, **Crisis Text Line (text HOME to 741741)**, and **911**. It states it *"is not an emergency service and cannot provide crisis intervention"* and admits its *"detection systems are not infallible."* **No live human crisis responder.** `[sourced]`
- **Note:** the 2021 study used a **modified PHQ-9 with the suicide item (item 9) removed.** `[sourced]`

### Clinical evidence
- **Primary study — JMIR, June 22 2021** (Mehta, Niles, Vargas, Marafon, Couto, Gross; Stanford + Youper): longitudinal **observational** study, **no control group**, **N=4,517 paying users** (81.62% female, mean age 28.73). Within 2 weeks: anxiety **GAD-7 d=0.57** (d=0.60 at 4 wk); depression (modified PHQ-9) **d=0.46** (d=0.42 at 4 wk). 42.66% retained at week 4; mean **4.36 stars**. Greater "successful emotion regulation" predicted greater symptom reduction. `[sourced]`

> **`[unsupported]` — corrected figure:** Raw findings claimed a **"~3.6-point PHQ-9 reduction"** in 2 weeks. **This is wrong.** JMIR reports PHQ-9 falling **14.41 → 11.61 = a ~2.8-point reduction**, not 3.6. Use **~2.8 points.**

- **Earlier study — 2019 feasibility trial** (~1,012 adults, 8 weeks, nonrandomized): ~**48% depression** and ~**43% anxiety** symptom reductions (77% female, mean age 24.79). `[sourced]`
- **Caveats (author-acknowledged):** no control group, self-report only, **~48% of users on concurrent medication/therapy** (47.84%), no clinician-administered assessments; authors explicitly call for a **future RCT**. `[sourced]`
- **No published RCT for Youper was found** as of the current date. `[inference]`

### FDA / regulatory status
- Youper's safety page states plainly: *"Youper is not a medical device and has not been cleared or approved by the U.S. Food and Drug Administration."* No clearance, no De Novo. Positioned as a **general-wellness / non-device consumer product.** `[sourced]`
- **No FDA Breakthrough Device Designation exists for Youper.** That designation is **Wysa's** (May 2022, chronic pain with depression/anxiety), frequently conflated with Youper in secondary sources. `[sourced]` (Refutes the `[contested]` Dim-1 claim.)
- **Category context (not Youper-specific):** The **FDA Digital Health Advisory Committee (Nov 6, 2025)** examined generative-AI mental-health devices and flagged **hallucination, sycophancy, and bias** as key unsolved risks; *"the agency has yet to clear mental health tools using generative AI."* `[sourced]`

---

## Dimension 6 — Engineering Difficulty

**Engineering difficulty: 2/5 (moderate-to-low).**

- The clinically validated core is a **decision-tree/rules-based conversational engine over a hand-authored clinical content library** — well-understood engineering, not frontier ML. `[sourced]`
- The current hybrid most plausibly **wraps a vendor LLM (OpenAI GPT) with a safety/guardrail layer** rather than training a proprietary foundation model — and the CEO has publicly stated as much. There is **no public evidence of in-house model training, executed fine-tuning, RLHF, or RAG infrastructure.** `[inference]`
- The **stack is conventional** (EC2/MySQL/Nginx + mobile apps), and **team (~5-15)** and **funding (~$3.5-5.2M)** are too lean for a deep-tech ML operation. `[inference]`
- **The genuinely hard work is clinical/regulatory, not software:** running trials, building reliable **crisis-detection guardrails**, and producing FDA-grade evidence — the exact risks (hallucination, sycophancy, bias) the FDA's Nov 2025 committee flagged as unsolved for this category. `[sourced]`
- **Why above the floor:** building reliable crisis-detection guardrails and a clinically faithful conversational system at consumer scale is non-trivial. **Why not higher:** absence of novel model R&D. Confidence is limited by Youper's non-disclosure of current model internals. `[inference]`

---

## Dimension 7 — Founders, Key Hires, Headcount & Org Shape

### Founders (founded Jan 2016, HQ San Francisco)
- **Jose Hamilton Vargas, MD — Co-founder & CEO.** Clinical psychiatrist (MD, Universidade de Brasilia; data-science specialization, Johns Hopkins 2015-16; reportedly 3,000+ patients over a decade). Provides clinical/CBT domain expertise. `[sourced]`
- **Thiago Marafon — Co-founder & CTO.** Software engineer (security, web, chatbots, AI). Technical lead. `[sourced]`
- **Diego Dotta (Diego Dotta Couto) — Co-founder & Chief Product** (also "Chief Product & Growth"). Design/product lead. `[sourced]`
- **Andrea Niles, PhD — Co-founder & Chief Science Officer.** UCLA clinical psychology; co-author on the JMIR study. `[sourced]`

> **`[unsupported]` — corrected internal contradiction:** Raw Dim-7 claimed "no specific named non-founder key clinical hire / confirmed CSO was identified." **This is refuted.** **Andrea Niles, PhD is publicly Youper's Co-founder & Chief Science Officer** (and named as a co-founder in Dim 1). The "psychiatrist + developer + designer + scientist" framing maps to the four founders.

### Org shape
- **Tiny, founder-led, flat.** Founders hold CEO/CTO/CPO/CSO. The Org also lists a Community Manager (Tabea L.) and **board/advisors Edward Suh, Alex Bargar, Chia-Hua Chien** (Edward Suh = Goodwater Capital, lead seed investor `[inference]`). No publicly confirmed VP/Head-of layer below the founders. `[sourced]`
- Clinical/AI work is concentrated in the founders (CEO = clinical, CTO = eng/AI, CSO = science) rather than a large specialized staff. `[inference]`

### Headcount (disputed across aggregators)
- LinkedIn band **11-50**; PitchBook **8**; Craft.co **5**; LeadIQ **~11** (Jun 2025); Tracxn **6** (Dec 2021); one aggregator **~4** (Jun 2026). `[sourced]`
- **Best estimate: ~5-15 people, well under 20** — consistent with ~$5M total funding. The 2026 low end (~4) suggests **contraction**. `[inference]`

---

## Dimension 8 — Compensation Bands

**Bottom line: NO authoritative company-reported or government compensation data exists for Youper.** All figures are third-party **MODELED ESTIMATES** — low confidence.

- **Zero H1B/LCA records** (h1bdata.info returns 0 across all years). `[sourced]`
- **No levels.fyi entries; no retrievable posted salary ranges** from the careers page (jobs.youper.ai) or job boards. `[sourced]`
- **Salary.com (modeled, ~Jun 2026):** Chief Science Officer ~$356,673 ($290K-$433K); Full-Stack Developer ~$92,466 ($85K-$100K); a separate Full Stack Developer listing ~$72,874 ($65K-$81K); company average ~$115,142. `[speculation]`
- **Glassdoor (modeled estimates):** Head of User Acquisition ~$190,822; Chief Science Officer ~$276,994. `[speculation]`
- **Interpretation:** The Salary.com vs. Glassdoor CSO figures (~$357K vs. ~$277K) **conflict**, confirming these are model outputs, not real pay. The full-stack figures (~$73-92K) read **below SF AI-startup market** and are likely thin-data model artifacts. `[speculation]`
- **Actual compensation bands: unknown — not found.**

---

## Dimension 9 — Funding & AI Investment

- **Modest and old.** Tracxn/CB Insights report a **$3.0M Seed on June 18, 2019, led by Goodwater Capital** (covered by TechCrunch). `[sourced]`
- **Total raised:** aggregators range **~$3.5M-$5.2M** (Tracxn $5.18M; PitchBook $3.53M). Founder bios cite "~$4M in venture funding." `[sourced]`

> **`[contested]` — corrected:** Raw findings stated "$5-6M total incl. a Series A in 2019." The **"Series A" is weakly supported** — primary and most sources document only the **Seed round**; the Series A label appears in only some aggregators and is not cleanly corroborated. Total is better stated as **~$3.5-5.2M**, not $5-6M.

- **No valuation publicly disclosed** in any source (PitchBook, Crunchbase, Tracxn, CB Insights). `[sourced]`
- **No funding round after 2019** was found across multiple aggregators, **despite the 2020-2024 AI/mental-health funding boom** — a strong signal of capital constraint. `[inference]`
- **AI-specific investment:** cannot confirm any large dedicated AI investment; the lean funding profile is inconsistent with a deep-tech ML build. `[inference]`

---

## Dimension 10 — Business Model & Drivers Behind Tech Choices

- **Consumer-first freemium.** Free tier (mood tracking, AI chat, limited content) funnels to **"Youper Plus"** paid subscription (monthly/annual) for personalized insights, unlimited history, premium content. `[sourced]`
- **Stated dual model:** marketing/aggregators describe a B2C **+ B2B** ambition (employers, payers, providers). But the live consumer site shows **no enterprise, pricing, or partnership detail** and disclaims medical-device status — suggesting **the B2B/clinical channel never became the core revenue engine.** `[sourced]` / `[inference]`
- **Driver behind tech choices:** the AI chatbot was chosen specifically to **drive down cost-of-delivery and scale "just-in-time" CBT to millions cheaply** (an explicit goal in the Stanford study). `[sourced]`
- **The 2021 clinical study functioned substantially as a go-to-market / credibility / enterprise-sales asset**, not purely a scientific output. `[inference]`

> **Marketing-as-fact caveat:** The PRNewswire headline figures (**"-24% anxiety / -19% depression in 2 weeks"**) originate from a **company press release about an observational, uncontrolled study** and should **not** be read as RCT-grade efficacy. `[contested]`

- The **2026 disclaimer-heavy, consumer-only positioning** likely reflects both **regulatory caution** (FDA scrutiny of generative-AI mental-health tools) and a **capital-constrained, lean operating reality.** `[inference]`

---

## Dimension 11 — Stated vs. Real Motivations

### Stated vs. real motivations

**Stated motivation:** *"Make mental health care simple, accessible, and affordable"* — give immediate AI-driven support to the hundreds of millions who can't afford or quickly reach a psychiatrist. Framed as **supplementing, not replacing**, clinicians by lowering cost, stigma, and access barriers ("people need support now, not three months from now"), reinforced with a Stanford/JMIR clinical-validation story to claim real health outcomes, not just wellness. `[sourced]`

**Real motivation:** Build a **venture-scalable digital mental-health business** by using AI to **collapse the cost of delivering CBT**, then monetize via consumer subscriptions (Youper Plus) and — aspirationally — higher-value **B2B/clinical contracts** and a prescription-digital-therapeutic path. The founder's psychiatrist credibility plus the published study functioned substantially as **differentiation, enterprise-sales, and fundraising assets**. `[inference]`

**Where stated and real diverge:** With **no capital raised after 2019** and a team that **shrank to a handful**, the realized motivation narrowed to **sustaining a lean, subscription-funded consumer app**. The company **explicitly stepped back from medical-device/clinical claims**, indicating the loftier B2B-therapeutic / prescription-digital-therapeutic vision was **not achieved at scale.** `[inference]`

---

## Dimension 12 — Summary Assessment & Confidence

- **What Youper actually is:** a small, founder-led, clinically-credentialed consumer chatbot whose differentiation is **clinical validation + psychiatrist-authored CBT/ACT/DBT content + embedded validated scales (PHQ-9/GAD-7)** — *not* frontier AI. `[inference]`
- **Architecture truth:** evolved from a **2021 non-generative decision tree** to a **2023 OpenAI-GPT generative hybrid** with an expert-system controller and input/output safety flagging. The "NOT an LLM" framing is outdated. `[sourced]`
- **Evidence truth:** real but **uncontrolled, observational, self-report** data (anxiety d=0.57, depression d=0.46; **~2.8-point** PHQ-9 drop, *not* 3.6); **no RCT; not FDA-cleared; not a medical device.** `[sourced]`
- **Engineering difficulty: 2/5** — conventional stack and vendor-LLM-plus-guardrails; the hard problems are clinical/regulatory, not software. `[inference]`
- **Trajectory:** capital-constrained (nothing after 2019), contracted headcount, and a strategic retreat to wellness positioning. `[inference]`

**Overall confidence: HIGH** — the core facts (clinical study, architecture evolution, funding, founders, regulatory status) are well-sourced and cross-verified. Lower-confidence items: current model internals (non-disclosed), exact headcount (aggregator disagreement), and all compensation figures (modeled estimates only).

**Key items marked "unknown — not found":** current foundation-model specifics / whether fine-tuning was executed; RLHF/RAG details; precision/recall of the crisis-detection classifier; whether any human reviews flagged conversations; valuation; actual compensation bands; exact current user count; post-2023 architecture changes; any funding after 2019.

---

## Sources

- https://www.jmir.org/2021/6/e26771/ (JMIR longitudinal study, 2021-06-22)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8423345/ (PMC mirror / 2019 feasibility trial context)
- https://www.youper.ai/safety (safety page, 2026-06)
- https://www.youper.ai/emergency (emergency/crisis-referral page, 2026-06)
- https://www.youper.ai/about-us (current positioning, 2026)
- https://blog.youper.ai/about-us (mission statement, 2026)
- https://www.linkedin.com/pulse/why-generative-ai-chatgpt-ready-mental-healthcare-jose-hamilton-md (CEO on hybrid architecture / GPT, 2023-03-06)
- https://www.odbms.org/2018/08/ai-mental-health-youper-qa-with-jose-hamilton-vargas/ (origin story / pivot, 2018-08)
- https://www.prnewswire.com/news-releases/major-study-from-stanford-university-and-youper-finds-artificial-intelligence-therapy-effective-at-reducing-anxiety-and-depression-301334656.html (press release, 2021)
- https://techcrunch.com/2019/06/18/youper-a-chatbot-that-helps-users-navigate-their-emotions-raises-3-million-in-seed-funding/ ($3M seed, 2019-06-18)
- https://tracxn.com/d/companies/youper/__sajx6skkqp9P5sNeO71t00hwxOI4enFyn3PkuTtmWCE (funding/founders aggregator, 2026)
- https://pitchbook.com/profiles/company/117382-78 (funding/headcount aggregator, 2026)
- https://www.crunchbase.com/organization/youper (funding aggregator, 2026)
- https://www.cbinsights.com/company/youper (headcount ~4, 2026)
- https://theorg.com/org/youper (org chart / founders / advisors, 2026)
- https://www.linkedin.com/in/josehamiltonvargas/ (CEO bio, 2026)
- https://www.crunchbase.com/person/thiago-marafon (CTO profile, 2026)
- https://theorg.com/org/youper/org-chart/diego-dotta-couto (CPO profile, 2026)
- https://intuitionlabs.ai/software/telepsychiatry-digital-mental-health/chatbots-and-ai-therapy-assistants/youper (modalities / dual model, 2026)
- https://mymeditatemate.com/blogs/wellness-tech/best-ai-mental-health-apps (current hybrid/text-only description, 2026)
- https://leadiq.com/c/youper/5a1dda212300005c00e71b9a (technographics — non-authoritative, 2026)
- https://vizologi.com/business-strategy-canvas/youper-business-model-canvas/ (freemium model, 2026)
- https://www.salary.com/research/company/youper-inc-salary (modeled comp estimates, 2026)
- https://www.glassdoor.com/Salary/Youper-Salaries-E2457736.htm (modeled comp estimates, 2026)
- https://www.glassdoor.com/job-listing/clinical-product-psychologist-youper-JV_IC1147401_KO0,29_KE30,36.htm (clinical job listing, 2026)
- https://h1bdata.info/index.php?em=Youper (zero H1B records, 2026)
- https://www.levels.fyi/companies/youper/jobs (no salary entries, 2026)
- https://www.orrick.com/en/Insights/2025/11/FDAs-Digital-Health-Advisory-Committee-Considers-Generative-AI-Therapy-Chatbots-for-Depression (FDA DHAC, 2025-11)
- https://www.nature.com/articles/s44184-025-00174-2 (Wysa FDA designation context / conflation correction, 2025)
