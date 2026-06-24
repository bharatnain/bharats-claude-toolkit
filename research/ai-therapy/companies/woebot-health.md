# Woebot Health — Company Dossier

**One-line summary:** A Stanford-spun, CBT-based mental-health chatbot built on a rules-based decision-tree engine (explicitly *not* generative AI in production) with clinical-grade safety scaffolding and an FDA Breakthrough-Device digital-therapeutic ambition, which retired its consumer app in mid-2025 and pivoted entirely to enterprise as its regulated, scripted approach was outpaced by generative AI it could not yet ship under regulation.

**Overall verifier confidence:** high

> **Label key:** `[sourced]` = directly supported by cited source(s); `[inference]` = analytical judgment grounded in sourced facts; `[speculation]` = plausible but uncorroborated; `[contested]` = sources disagree / verifier reversed the raw-findings lean; `[unsupported]` = asserted without support. "unknown — not found" = no evidence located.

---

## D1 — Company Journey / Timeline

- **2017** — Woebot founded by Dr. Alison Darcy, who created Woebot while an intervention scientist in child & adolescent psychiatry at Stanford and while running Andrew Ng's Health Innovation Lab in CS. `[sourced]`
- **2017** — Foundational JMIR Mental Health RCT published (Woebot vs. NIMH ebook control). `[sourced]`
- **~March 2018** — $8M seed (Woebot Labs), led by NEA with Andrew Ng's AI Fund. `[sourced]`
- **January 2019** — BERT-based intent-classification models deployed (NLP evolution milestone). `[sourced]`
- **26 May 2021** — FDA Breakthrough Device Designation granted for WB001 (postpartum-depression DTx). `[sourced]`
- **21 July 2021** — $90M Series B closed, co-led by JAZZ Venture Partners and Temasek. `[sourced]`
- **March 2022** — ~$9.5M Leaps by Bayer tranche, bringing reported total to ~$123M. `[sourced]`
- **November 2022 onward (post-ChatGPT)** — Built a custom multi-model LLM prompt-execution engine for IRB-regulated study use. `[sourced]`
- **January 2023** — First patient enrolled in pivotal trial NCT05551195 (WB001). `[sourced]`
- **July 2023** — IRB-approved hybrid LLM-augmented "Build study" reported equivalent outcomes vs. standard Woebot, no adverse events. `[sourced]`
- **~May 2023 / Feb 2025** — Pivotal trial NCT05551195 reached primary completion ~May 2023, then status **TERMINATED** (internal company decision), last updated Feb 2025; no efficacy results published. `[sourced]`
- **30 June 2025** — Direct-to-consumer app retired; account data anonymized after 31 July 2025; full pivot to enterprise (payers/providers/employers). `[sourced]`
- **Lifetime** — ~1.5 million users served over the consumer app's life. `[sourced]`

---

## D2 — Technology Stack & Architecture

- The commercial product is a **rules-based engine resembling a decision tree of conversational paths** — explicitly *not* a generative LLM product in production. `[sourced]`
- Content authoring/routing runs on a **proprietary React-based (web) conversational management system** where designers build content modules, define routing, and mark free-text entry points. `[sourced]`
- NLP is used **only to understand and classify user text and route to pre-authored content**; users "never interact directly with LLMs." `[sourced]`
- **NLP evolution:** regular expressions → supervised classifiers → fastText → **BERT (deployed January 2019)**. `[sourced]`
- A custom **multi-model LLM prompt-execution engine** was later built for experimental use only. `[sourced]`
- **Caveat (verifier flag):** Architecture/safety self-descriptions originate from Woebot's own AI-core-principles/marketing page; the *architecture* is independently corroborated by IEEE Spectrum, but safety-stack efficacy is self-reported and not independently audited. `[contested]`

---

## D3 — AI / ML Approach

- **Production LLM use is deliberately constrained:** LLMs are used only (a) to *classify* user input into categories routing to human-written content, and (b) for *response generation strictly within IRB-regulated study settings*. Commercial products do not use LLMs for response generation. `[sourced]`
- Generative response capability was confined to IRB-regulated studies, wrapped in proprietary guardrails: **Concerning Language Detection run before any LLM call, prompt-injection-resistant prompt architecture, off-topic detection, maximum-turn enforcement, and input/output validation.** `[sourced]` (vendor-self-reported, IEEE-corroborated on the experiment's existence)
- The AI-principles page **does not name specific foundation models, fine-tuning approaches, or RAG**; it emphasizes well-validated NLP plus conversational-design principles. `[sourced]`
- The July 2023 hybrid LLM "Build study" reported equivalent satisfaction/symptom improvement vs. standard Woebot with no adverse events. `[sourced]`
- The company acknowledged that "without generative AI, it's impossible to respond in a novel way to every different situation," and that LLM responses "made people feel understood." `[sourced]`
- **Specific production model providers / fine-tuning details:** unknown — not found.

---

## D4 — Therapeutic Approach, Modalities & Technique Encoding

- **Core modality: Cognitive Behavioral Therapy (CBT)**, with elements of Interpersonal Psychotherapy (IPT) and Dialectical Behavior Therapy (DBT). `[sourced]`
- Positioned as a **relational agent / digital companion and adjunct to clinical care — not a replacement** — delivering psychoeducation, mood tracking, goal planning, social-skills training, and cognitive restructuring ("challenging thoughts"). `[sourced]`
- **Technique encoding:** Therapy is encoded as **human-authored, clinician-reviewed content modules** in a decision-tree structure; conversational designers trained in evidence-based approaches collaborate with clinical experts. NLP classifiers route users to the appropriate CBT content module. `[sourced]`
- **WB001** specifically is an 8-week prescription CBT+IPT course (SaMD). `[sourced]`

### Human-in-the-loop
- Designed as a **"fully automated conversational agent"** (2017 RCT framing); human involvement sits at the **authoring/clinical-design layer**, not live in-conversation. `[sourced]`
- WB001 was intended for use "under the supervision of a clinician" — i.e., clinician-prescribed, but the chatbot interaction itself is automated. `[sourced]`

---

## D5 — Safety, Crisis Handling, Clinical Evidence & Regulatory

### Safety / crisis
- A **Language Detection Protocol (LDP) / Concerning Language Detection** algorithm detects concerning free-text (e.g., suicidal ideation, domestic violence). On detection it reminds users of the app's limitations and surfaces a resource list with emergency numbers and suicide/domestic-violence hotlines. `[sourced]`
- The generative experiment added further safeguards (refuses medical advice, blocks off-topic, avoids suicidal-ideation discussion). `[sourced]`

### Clinical evidence
- **Foundational 2017 JMIR Mental Health RCT:** n=70, ages 18–28, Woebot (n=34) vs. NIMH ebook control (n=36); statistically significant PHQ-9 depression reduction over 2 weeks (F=6.47, P=.01). `[sourced]`
- Additional RCTs cover **postpartum depression/anxiety** (significant reductions vs. waitlist, large effect sizes at 2 and 6 weeks) and **subclinical young-adult anxiety/depression** (JMIR 2024). WB001 design published in *Expert Review of Medical Devices* ("Anatomy of a Woebot (WB001)," 2023). `[sourced]`
- **Verifier caveat:** The foundational RCT is small (n=70), unblinded, 2-week feasibility against an information-only control; "multiple RCTs / clinically validated" framing should be read with small-n, short-duration, often-waitlist-control limitations in mind. `[contested]`

### Regulatory (with dates)
- **FDA Breakthrough Device Designation** for WB001 (postpartum depression) granted **26 May 2021**. This is a development-pathway status, **NOT FDA clearance or approval.** `[sourced]`
- **WB001 was never FDA-cleared or approved — it remained investigational throughout.** `[sourced]`
- **Pivotal trial NCT05551195** (WB001 vs. ED001 vs. TAU; randomized, double-blind): start ~16 Nov 2022, first patient announced Jan 2023, primary completion ~10 May 2023, status **TERMINATED** (internal company decision), last updated Feb 2025. `[sourced]`
- **WB001 pivotal-trial efficacy outcome (endpoint met/missed): unknown — not found.** No results publication located. `[sourced]` (that the outcome is undisclosed)
- Consumer app retired 30 June 2025; CEO/founder cited FDA marketing-authorization cost/difficulty plus the FDA's lack of a framework to regulate the LLMs Woebot wanted to adopt. `[sourced]`

---

## D6 — Engineering Difficulty

### Engineering difficulty (3/5)
The original system is a **moderately complex rules-based conversational platform**: a bespoke content-authoring/routing engine plus a progression of NLP intent classifiers (regex → supervised → fastText → BERT) and a free-text safety-detection layer (LDP). The later LLM prompt-execution engine with multi-layer guardrails raises complexity modestly.

- The **raw software stack is engineeringly modest** — classification + routing + scripted dialog — not a research-frontier or hard distributed-systems problem by 2020s standards, and explicitly *not* a generative system in commercial deployment. `[inference]`
- The **genuinely hard parts are wrap-around rather than novel ML:** (a) a Concerning Language Detection / crisis-safety layer reliable enough for clinical mental-health use; (b) prompt-injection-resistant architecture and multi-layer guardrails for the experimental LLM path; (c) the surrounding RCT, clinical-evidence, and FDA Breakthrough-Device regulatory machinery. `[inference]`
- **Rating reconciliation:** Raw findings split between 2/5 (pure software) and 3/5 (including clinical-content tooling, robust intent classification, safety guardrails, and regulated-SaMD rigor). The verifier endorsed a low-to-moderate **2–3/5** band, with the difficulty dominated by safety-engineering rigor and regulatory/clinical validation rather than novel ML or distributed-systems complexity. **Dossier rating: 3/5**, reflecting that clinical-grade safety classification and the hybrid-LLM-with-guardrails work require real care beyond a CRUD chatbot, while remaining within standard applied-ML/product engineering. `[inference]`

---

## D7 — Founders, Key Hires & Org Shape

- **Founder:** Dr. Alison Darcy (clinical research psychologist), founded the company in 2017; named to the **TIME100 AI list (2023)**. `[sourced]`
- **CEO title — CONTESTED (verifier reversal):** The raw findings leaned toward Darcy as CEO, but the weight of evidence — Woebot's own About-Us/leadership pages, AI Fund, Behavioral Health Tech, the TIME100 release, and Business of Business — supports **Darcy as "Founder & President" and Michael Evers as CEO.** The STAT (2025) "founder and CEO" phrasing is treated as a press simplification, not authoritative. `[contested]`
- **Leadership team (company About-Us page):**
  - Casey Sackett, PhD — Chief Technology Officer `[sourced]`
  - Athena Robinson, PhD — Chief Clinical Officer `[sourced]`
  - Joe Gallagher, PhD — Chief Product Officer `[sourced]`
  - Monique Levy — Chief Business Officer (historically titled "Chief Commercial and Strategy Officer," 2020) `[sourced]`
  - Trina Histon, PhD — VP Clinical Product Strategy `[sourced]`
  - Sheetal Shah — SVP Commercial `[sourced]`
  - Robbert Zusterzeel, MD/PhD/MPH — VP Regulatory Science & Strategy `[sourced]`
- **Board:** includes Andrew Ng (AI Fund); leadership is heavily PhD/clinically credentialed. `[sourced]`
- **Headcount / org shape:** ~90 employees (TrueUp, mid-2024); a separate source cited ~40. Discrepancy unresolved; **current post-pivot headcount: unknown — not found.** The 2025 consumer-app shutdown + enterprise pivot implies organizational contraction, though **no documented mass-layoff event was found.** `[sourced]` (headcount estimates) / `[inference]` (contraction)

---

## D8 — Compensation (role-level)

**Most reliable (H1B LCA filings, Woebot Labs Inc, San Francisco — base salary only / prevailing-wage floors):** `[sourced]`
- Senior Platform Engineer: $150,000 (2021)
- Director of Content: $100,000 (2021)
- VP, Content: $155,480 (2024)
- H1B median across filings: $150,000

**Estimate (Glassdoor, self-reported, small n ~34, base/approx — directional only):** `[sourced]` figures, `[inference]` on reliability
- Software Engineer: ~$90K–$125K (avg ~$101K)
- DevOps Engineer: ~$125K (single data point)
- Full Stack Engineer: ~$90K (single data point)

**Benefits:** Equity/stock options offered to all employees, plus health/dental/vision, parental leave, and a professional-development stipend. `[sourced]`

**Notes:** Glassdoor figures skew low versus H1B filings and SF venture-backed health-tech norms; treat as directional. `[inference]` No levels.fyi data surfaced. `[unknown — not found]` Post-pivot (2025–26) compensation: unknown — not found.

---

## D9 — Funding

- **Seed:** $8M, ~March 2018, led by NEA with Andrew Ng's AI Fund (Woebot Labs). `[sourced]`
- **Series B:** $90M, closed 21 July 2021, co-led by **JAZZ Venture Partners and Temasek**, with BlackRock Private Equity Partners, Owl Ventures, Mirae Asset Capital, Kicker Ventures, Alumni Ventures, Gaingels, and existing investors NEA and AI Fund. Cumulative total stated as **$114M** at that time. `[sourced]`
- **Leaps by Bayer tranche:** ~$9.5M, March 2022, bringing the reported total to **~$123M** (per BHBusiness). `[sourced]`

### Funding-total reconciliation (verifier flag — CONTESTED)
The raw "$114M-to-$129M" range was **muddled and partly misattributed.** Corrected picture: `[contested]`
- **$114M** = pre-Bayer cumulative total (July 2021).
- **~$123M** = total after the March 2022 ~$9.5M Leaps by Bayer tranche (the intermediate figure the raw findings omitted).
- **~$124M / 17 investors** = Tracxn's current profile.
- **~$129M / 23 investors** = traces to **PitchBook**, not Tracxn (the raw findings misattributed this to Tracxn).

**Best statement of total raised: ~$123M**, with aggregator-dependent figures ranging $114M–$129M.

- **Post-money valuation:** unknown — not found (no public valuation located). `[sourced]` (that none was found)

---

## D10 — Business Model

- **Original model:** direct-to-consumer (D2C) free app plus a prescription digital-therapeutic ambition (WB001 for postpartum depression), targeting FDA marketing authorization and reimbursement. `[sourced]`
- **Post-pivot model:** **entirely enterprise / B2B** — distribution to payers, providers, and employers (health systems/employers/payers via access codes), trading the D2C + prescription-DTx vision for a "clinically validated, safety-scaffolded" enterprise positioning against unregulated generative-AI companion apps. `[sourced]`
- The D2C app was retired 30 June 2025 (data anonymized after 31 July 2025). `[sourced]`
- **Enterprise revenue / contract figures, pricing, customer counts:** unknown — not found.

---

## D11 — Motivations

### Stated vs. real motivations

**Stated motivation** `[sourced]`
"Make mental health radically accessible" — democratize evidence-based CBT to the many who can never reach a human therapist (Darcy's stated mission, rooted in her Stanford intervention-science work), delivered 24/7 via an automated, clinically grounded conversational agent as an adjunct to traditional care, and pursue an FDA-authorized prescription DTx (WB001). Publicly, the consumer-app shutdown was framed as a **principled/regulatory decision**: the cost and challenge of meeting FDA marketing-authorization requirements, plus the FDA's lack of a framework to regulate the LLMs Woebot wanted to adopt — "AI is moving faster than regulators."

**Real motivation — *triangulated inference (confidence: medium)*** `[inference]`
A scripted, rules-based CBT chatbot — Woebot's whole safety-and-regulatory moat — became commercially squeezed from both sides: free, fluent general-purpose LLMs (ChatGPT, character chatbots) made the predictable scripted experience feel obsolete to consumers, while the FDA path Woebot bet on (Breakthrough Device, RCTs, ~$114M+ raised since 2017) was slow, expensive, and had **not** produced a marketed, reimbursed prescription product after ~8 years — and the pivotal WB001 trial was terminated with no published results. The enterprise pivot reads as a **commercial-survival / revenue-durability move**: B2B contracts offer durable revenue, regulatory cover via existing care ecosystems, and a way to monetize the clinical IP without funding a costly D2C business that couldn't safely adopt the generative AI users now expect.

Supporting (sourced) signals behind the inference: the D2C app was retired exactly as consumer LLM chatbots peaked `[sourced]`; the company's own admission that the experience felt limited "without generative AI" `[sourced]`; a long capital-intensive FDA path with no marketed product `[sourced]`; a terminated pivotal trial `[sourced]`.

**The "face-saving narrative" characterization — *speculation; do not elevate*** `[speculation]`
The stronger claim that the FDA framing is *partly a cover for commercial distress* directly contradicts the only on-record source (the founder) and has **no internal-financial, board-minute, or burn-rate corroboration.** No internal financials were found to confirm commercial distress directly. Retained strictly as speculation. `[speculation]`

---

## D12 — Outcome / Current Status

- **Consumer business wound down:** D2C app retired 30 June 2025; account data anonymized after 31 July 2025. `[sourced]`
- **Strategic state:** fully pivoted to enterprise (payers/providers/employers). `[sourced]`
- **Regulatory endgame:** WB001 never cleared/approved; pivotal trial terminated; no efficacy results published. `[sourced]`
- **Reach achieved:** ~1.5M lifetime consumer users. `[sourced]`
- **Company viability / current financial health post-pivot:** unknown — not found.
- **Current headcount:** unknown — not found (last estimates ~40–90, mid-2024). `[sourced]` (the estimates) / unknown (current)

---

## Sources

- https://en.wikipedia.org/wiki/Alison_Darcy
- https://woebothealth.com/ai-core-principles/
- https://aifund.ai/insights/insights-making-mental-health-radically-accessible-a-conversation-with-allison-darcy-founder-and-president-of-woebot-health/
- https://woebothealth.com/woebot-health-closes-90-million-series-b-funding/
- https://tracxn.com/d/companies/woebot-health/__cuCfb1dFxeFNB_5RcIpxsTJDcypnMKXlAS0PbwYAWVI/funding-and-investors
- https://www.businesswire.com/news/home/20210526005054/en/Woebot-Health-Receives-FDA-Breakthrough-Device-Designation-for-Postpartum-Depression-Treatment
- https://bhbusiness.com/2025/04/23/woe-is-me-woebot-says-farewell-to-signature-app/
- https://www.statnews.com/2025/07/02/woebot-therapy-chatbot-shuts-down-founder-says-ai-moving-faster-than-regulators/
- https://spectrum.ieee.org/woebot
- https://mental.jmir.org/2017/2/e19/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC5478797/
- https://cdn.clinicaltrials.gov/large-docs/95/NCT05551195/Prot_SAP_000.pdf
- https://clinicaltrials.gov/study/NCT05551195
- https://woebothealth.com/woebot-health-enrolls-first-patient-in-pivotal-clinical-trial-of-wb001-for-postpartum-depression/
- https://woebothealth.com/woebot-health-founder-alison-darcy-named-to-2023-time100-ai-list/
- https://woebothealth.com/about-us/
- https://craft.co/woebot/executives
- https://www.trueup.io/co/woebot-health
- https://h1bdata.info/index.php?em=WOEBOT+LABS+INC
- https://www.glassdoor.com/Salary/Woebot-Health-Engineering-Salaries-EI_IE2464640.0,13_DEPT1007.htm
