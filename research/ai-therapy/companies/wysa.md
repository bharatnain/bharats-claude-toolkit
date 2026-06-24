# DOSSIER — Wysa (Touchkin eServices Private Limited)

**One-line:** India-founded B2B2C AI mental-health platform built on clinician-scripted CBT (rule engine + 120+ NLU routing models), using a free anonymous chatbot as a top-of-funnel and evidence engine for enterprise/payor/NHS clinical contracts — strong safety governance, but an uneven evidence base whose headline efficacy claims are vendor framing rather than study findings.

**Overall confidence:** medium-high. Entity, founders, funding rounds, regulatory status, org shape, and therapeutic architecture are well-corroborated. The chronic-pain efficacy framing is the weakest link (see Dimension 5).

> Label key: **[sourced]** = corroborated in cited source(s); **[inference]** = reasoned from disclosed facts, not directly stated; **[speculation]** = plausible but unverified; **[contested]** = sources disagree or claim overstates underlying evidence; **[unsupported]** = no support found / placeholder. "unknown — not found" = searched, not located.

---

## Dimension 1 — Company journey / history

- Operated by **Touchkin eServices Private Limited** (Karnataka, India; CIN U72200KA2015PTC078356), **founded 2015** by husband-and-wife team **Jo (Jyotsana) Aggarwal** (CEO) and **Ramakant Vempati** (President). **[sourced]**
- Started as "Touchkin," a passive-sensing app that built ML models to **detect depression from phone sensor data (founder-claimed ~90% accuracy)**. Trials revealed users did not want loved ones/doctors to know and were not ready for therapists, prompting a **pivot to an anonymous conversational chatbot**. The 90% figure is the founder's own statement, not independently validated. **[sourced]**
- Wysa app **launched on Google Play in October 2016**; chatbot rolled out broadly ~2017. **[sourced]**
- Evolved into a **B2B2C clinical-infrastructure player**: NHS Talking Therapies (formerly IAPT) deployments, FDA Breakthrough Device Designation (May 2022), Singapore Ministry of Health, and enterprise clients (Accenture, Colgate-Palmolive, Aetna International, Swiss Re). **[sourced]**
- At Series B (Jul 2022): **4.5M users across 65 countries, 400M+ conversations.** **[sourced]**
- HQ now effectively **Boston**, with operations in **Bengaluru** and **London**. **[sourced]**
- **March 2025: merged with US-based April Health** (primary-care-embedded virtual behavioral health), dba Wysa, to pursue the **Collaborative Care Management (CoCM)** reimbursement model in US primary care; terms undisclosed. **[sourced]**

## Dimension 2 — Product surface / what it actually does

- Free, anonymous AI **self-help chatbot** delivering CBT and adjacent techniques via text. **[sourced]**
- Optional **paid human coaching** (text; audio/video in US & India). **[sourced]**
- **Clinical/enterprise programs** sold to employers, payors, and health systems, including NHS waitlist support and triage. **[sourced]**
- **Wysa Copilot** (launched Nov 5, 2024): therapist-facing platform with async/real-time messaging, tool assignment, and between-session patient tracking. **[sourced]**
- NHS **Digital Referral Assistant (DRA)**: gathers patient info, produces a clinician-reviewed report transferred to the EHR (integrates with Mayden's iaptus). **[sourced]**
- Granular consumer feature inventory (exact module list, premium-tier pricing) — *unknown — not found.*

## Dimension 3 — Technology stack / architecture

- Core conversational engine is a **clinician-approved rule engine** delivering pre-scripted flows; **120+ NLU (natural-language-understanding) AI models** classify intent/emotion and route users into the appropriate scripted conversation. **[sourced]**
- Newer implementations described as a **"combination of rule-based and LLM-powered chats"** — selective, guard-railed LLM use layered on the rule engine, not open generation. **[sourced]**
- Exact boundary of where LLMs are now used and what guardrails govern them is **not disclosed publicly.** **[inference]**
- Specific infra/cloud/data-pipeline stack (languages, hosting, model-serving) — *unknown — not found.*

## Dimension 4 — Therapeutic approach, modalities, technique encoding, human-in-the-loop

- **Primary modality CBT**, supplemented by **DBT, mindfulness/meditation, breathing, guided relaxation/yoga, motivational interviewing, behavioral activation, and "micro-actions."** **[sourced]**
- **Two-stage conversational flow:** an open-ended free-text **"listening" stage**, followed by a **"therapeutic" stage** delivering a CBT (or other) technique the bot judges relevant. **[sourced]**
- **Technique encoding (the load-bearing design choice):** the core chatbot is **NOT free-form generative.** Therapeutic content is **clinician-authored and fixed**; Wysa explicitly contrasts this with ChatGPT — *"the responses Wysa provides are not AI generated."* The AI does interpretation/routing; humans write the content. **[sourced]** *(FAQ page returned 403 on re-fetch this session; rule-engine/NLU-routing description corroborated by secondary sources — EMHIC.)*
- **Human-in-the-loop — three layers:**
  1. **1:1 human coaching** with licensed professionals (text; audio/video in US & India), built on a self-reported **125,000+ hours of human coaching.** **[sourced]** *(vendor-provided metric)*
  2. **Wysa Copilot** (Nov 5, 2024): hybrid therapist-facing tooling extending clinician reach. **[sourced]**
  3. **NHS DRA**: clinician-reviewed referral reports; clinician oversight required, consistent with NICE's stance. **[sourced]**
- Wysa also **merged with April Health** to add in-person care. **[sourced]**

## Dimension 5 — Safety, crisis handling, clinical evidence, FDA & regulatory status

**Crisis handling**
- Built-in **real-time risk detection** scans free text for suicidal ideation, self-harm, trauma, abuse; on detection it **seeks user confirmation**, then surfaces an always-visible **SOS path**: local crisis helplines, co-created safety planning, guided grounding. High-risk users urged to call emergency services. **[sourced]**
- Wysa's **April 15, 2024 vendor study** (~19,000 anonymized users, 99 countries): **5.2%** reported a crisis instance in a year; **AI detected 82%** of these (user-confirmed); **46.6%** of crisis users used grounding exercises; **only 2.4%** called a helpline when prompted. **[sourced]** *(vendor-conducted; no independent replication found — **[inference]**)*
- The framing that **"18% self-selected via SOS"** is the findings' arithmetic (100% − 82%), **not a stated figure** in the press release. **[inference]**

**Clinical safety governance**
- **First AI mental-health app certified to NHS DCB0129** (Clinical Risk Management) — required a **Clinical Safety Officer, defined self-harm escalation paths, an ethics board, internal clinical audit loops.** The "first" superlative is vendor-originated but uncontradicted. **[sourced]**
- **ORCHA-approved**; won Mozilla **"Best in Privacy" (2022, 2023).** **[sourced]**

**Clinical evidence (design quality varies widely)**
- **Foundational study** (JMIR mHealth uHealth, Nov 23, 2018): **non-RCT quasi-experimental pre-post, n=129** (108 high / 21 low engagement). High-engagement users improved more on PHQ-9 (**5.84 vs 3.52 points; Mann-Whitney P=.03; common-language effect 0.63, ~Cohen d 0.47**). Authors **explicitly call for larger validation**; not an RCT. Every figure primary-source verified. **[sourced]**
- **Chronic pain — the headline efficacy claim is CONTESTED.** Wysa's press release states an "independent peer-reviewed JMIR RCT" found Wysa **"more effective than standard orthopedic care and comparable to in-person counseling,"** said to underpin the FDA designation. **The contemporaneous peer-reviewed study (JMIR Formative Research 2022, e34889) is a SINGLE-ARM prospective cohort PILOT FEASIBILITY study with NO control arm** — it explicitly states *"there was no true control arm,"* and compares high vs low users, **NOT** Wysa vs orthopedic care or vs counseling. **It does not make the comparative-effectiveness claim; that phrasing originates in Wysa's own press release.** A *"Protocol for a Series of Randomized Trials"* was still being published in **2025**, indicating the pivotal RCT was **not complete** at the time of designation. **[contested]** — *Marketing laundered as fact; treat the "RCT more effective than orthopedic care" claim as vendor framing, not a study finding.*
- **Chronic diseases RCT (2024, JMIR/ScienceDirect-hosted):** exists, but full text was inaccessible for sample size/statistics. **[sourced — for existence only]**
- **NHS Talking Therapies RCT** (sponsor University of Plymouth; IRAS 310377; REC 22/PR/0467; favourable opinion 25 May 2022): real-world trial in patients awaiting IAPT. **Effectively null** — mean depression change **similar between arms** (Wysa M=2.62; control M=2.59), **large SDs**, small randomized **n=76 of 2,161 screened** (625 invited, 99 consented, 2:1). **[sourced]** — *Sourcing caveat: the HRA application-summary URL cited in raw findings contains only the protocol/approval, NO results. The actual numbers live in the published paper (Int J Soc Psychiatry / Sage, DOI 10.1177/00207640251415507). Numbers correct, citation corrected here.* This is an important negative signal against vendor efficacy framing.
- Academic/critical literature (JMIR 2025, e67114) notes **heterogeneous evidence, risk of "therapeutic misconception"** (users bonding with a system lacking genuine therapeutic capacity), and that consumer chatbots largely **fall outside medical-device regulation.** **[sourced]**

**Regulatory / FDA status**
- **FDA Breakthrough Device Designation granted May 12, 2022** — **narrow indication**: AI-led conversational CBT tool for **adults 18+ with chronic musculoskeletal pain AND associated depression/anxiety.** This is an **expedited-review status, NOT marketing clearance/approval, and NOT a blanket clearance** of all Wysa products. Date and narrow indication confirmed across multiple independent outlets. **[sourced]**
- **No public evidence** that Wysa has converted this into a **510(k)/De Novo clearance** as of mid-2026 (FDA database searches found no Wysa clearance) — appears to remain a designation only. **[inference; absence of evidence]**
- **UK/NHS:** deployed across more than a dozen trusts; DCB0129 certified; ORCHA-approved; operates within NICE's evolving **Early Value Assessment** framework (which mandates clinician oversight). A specific positive NICE EVA recommendation naming Wysa was **not confirmed.** **[inference]**

**Overall read:** Therapeutically conservative-by-design (scripted clinician content + NLU routing, not open generative therapy), with serious safety governance and a real crisis pipeline. Evidence base is broad but uneven — the strongest headline claim (chronic-pain comparative effectiveness) is overstated vendor framing, the foundational 2018 study is a non-RCT, and the independent NHS RCT was effectively null. FDA status is a 2022 Breakthrough Designation (narrow indication), not approval.

## Dimension 6 — Market position / competition

- Positioned as **"one of the biggest suppliers of AI to the NHS,"** with contracts across more than a dozen trusts. **[sourced]**
- Targets the structural pain point of **long therapy waitlists** ("fill the gap while you wait" rather than replacing clinicians), which de-risks procurement. **[sourced]**
- Named enterprise/payor clients: Accenture, Colgate-Palmolive, Aetna International, Swiss Re; Singapore Ministry of Health. **[sourced]**
- Named competitive set, market-share figures, head-to-head positioning vs Woebot / Limbic / others — *unknown — not found.*

## Dimension 7 — Founders, key hires, headcount & org shape

**Founders**
- **Jo (Jyotsana) Aggarwal** — Co-Founder & CEO. Prior: built mobile-livelihoods tech across MENA (Silatech); MD at Pearson Learning Solutions. **[sourced]**
- **Ramakant Vempati** — Co-Founder & President. Prior: Executive Director, Goldman Sachs Investment Partners. Married to Aggarwal. **[sourced]**
- **Shubhankar Sarda** — CTO and early technical contributor; described in a single 2019 founder interview as **Aggarwal's nephew** (verbatim: *"Shubhankar, who's our tech genius, is my nephew."*) — relationship claim rests on a single source. **[inference]**

**Key execs / hires**
- **Shubhankar Sarda** — CTO (heads ~33-person engineering org per TheOrg). **[sourced]**
- **Harsh Gupta** — COO (~20 reports). **[sourced]**
- **Chaitali Sinha** — Chief Clinical R&D Officer (~5 reports). **[sourced]**
- **Sarah Baldry** — CMO (~12 reports). **[sourced]**
- **Zereana Jess-Huff, Ph.D.** — Chief Clinical Officer; licensed clinician, 15+ yrs digital health, prior won a $77M Maryland behavioral-health contract; appointed Oct 2021. **[sourced]**
- **Chad Cruse** — Head of Sales (US); appointed Oct 2021. **[sourced]**
- **Ross O'Brien** — Managing Director, UK & Europe; ex-NHS Associate Director of Innovation; appointed Oct 2021. **[sourced]**
- **John Tench** — Managing Director (UK). **[sourced]**
- **Emma Taylor** — Young-Adult Clinical Lead & Senior Clinical Safety Officer (tied to DCB0129 compliance). **[sourced]**
- Board/advisors: Becky Inkster, John Pestian, Kamal Jethwani, Amit Gupta, Anuj Srivastava, James Abraham. **[sourced]**

**Headcount & org shape**
- **~170–175 employees** as of early-mid 2026 (Tracxn 175 Apr 2026; LeadIQ ~172 Mar 2026; PitchBook 170). India legal entity ~113 (Feb 2025), consistent with ~175 global once US/UK GTM/clinical staff added. **[sourced]**
- Self-describes "over 150 people across five countries / three continents." **[sourced]**
- **Engineering is the largest function (~33 under the CTO)**; engineering/data-science core in **Bangalore**, with clinical/sales/GTM leadership split US (Boston-registered) / UK. Series B stage. **[inference]** *(org-shape detail from TheOrg, single aggregator)*
- Exact engineer level ladder, clinical "human coach" headcount split, diversity breakdown — *unknown — not found.*

## Dimension 8 — Compensation bands

> Nearly all data is India/INR; engineering core is India-based. **Zero H-1B/LCA records** for Touchkin eServices (h1bdata.info) — confirms no meaningful US-petitioned technical workforce; US/UK roles are senior GTM/clinical hires not captured in salary aggregators. **[sourced]**

**Levels.fyi (India, total comp/yr, ~June 2026)** — **[sourced]**
- Software Engineer: **median ₹1.81M; range ~₹1.36M–₹2.94M.**
- Data Scientist: low end **~₹1.21M** total comp.
- Software Engineering Manager: high-end **~₹6.12M.**
- Company-wide median: **~$20,978 USD-equiv (~₹1.75M).**

**Glassdoor (India)** — 88 salary submissions (2026; was 7 in 2025); comp & benefits rating **3.4/5**. Per-role figures (e.g., Data Scientist (NLP), Bangalore: **₹556K–₹601K**) are **Glassdoor model ESTIMATES, not reported data.** **[sourced / estimate]**

**US/UK leadership comp** — **No disclosed data** (no LCA filings, no posted ranges, no Glassdoor entries). Any US C-suite / UK MD figure would be pure speculation. **[inference — explicit gap]**

**Gaps (unknown — not found):** exact current headcount (only third-party estimates); engineer level ladder naming; UK/US base bands; equity terms.

## Dimension 9 — Funding & AI investment

**Confirmed equity rounds** — **[sourced]**
- **Seed ~$1.3M** (2017, Kae Capital + angels).
- **~$2M** round led by **pi Ventures** (with Kae Capital), reported ~2019.
- **Series A $5.5M** (announced May 2021; "missing middle of mental health").
- **Series B $20M** (announced **14 Jul 2022**, all-equity, led by **HealthQuad** with **British International Investment / BII**, plus existing investors W Health Ventures, Kae Capital, pi Ventures, Google Assistant Investments). No disclosed post-money valuation.

**Grants & later investors** — Wellcome Trust (grant); **Zurich Insurance Group** cited as a recent investor; Tracxn lists a **Grant-IV of $7.24M dated Feb 2026** (single-aggregator, low confidence). **[sourced / cautious]**

**Total raised — CONTESTED / aggregator-dependent:**
- Tracxn: **~$40.1M over 23 rounds** (grants bundled in).
- Older Crunchbase: **~$30.5M over 11 rounds.**
- Series B press: **~$29.4M cumulative.**
**[contested]** — totals mutually inconsistent and bundle grants; treat aggregate raise and the Feb 2026 grant as low-confidence.

**Valuation / revenue:** ~**Rs 682Cr (~$82M)** as of Aug 2023 (Tracxn); annual revenue **~Rs 47.3Cr (~$5.5M)** for FY ending Mar 2025 (aggregator; revenue echoed via legal-entity profile). **[sourced / cautious]**

## Dimension 10 — Business model & technical drivers

- **Three-tier / B2B2C model:** (1) free anonymous AI CBT chatbot (freemium funnel), (2) paid human coaches/counsellors/therapists, (3) clinical programs sold to enterprises, payors, health systems. **[sourced]**
- **~80% of revenue is enterprise (B2B)** (founder-stated at Series B); the free consumer app is largely top-of-funnel and a clinical-validation engine, not the revenue driver. **[sourced]** *(self-reported but consistently cited)*
- **Business drivers behind tech decisions:**
  - **Anonymity-first design** was driven directly by the discovery that stigma blocked sensor-based detection — privacy is the product wedge, not just a feature. **[sourced]**
  - **NHS DCB0129** (first AI mental-health app to meet it) and **FDA Breakthrough Designation** are **regulatory moats** enabling B2B/clinical sales and differentiating from unregulated consumer chatbots. **[sourced]**
  - **NHS waitlist-support / e-triage** (Mayden/iaptus integration) targets long therapy waitlists — "fill the gap" rather than replace clinicians, de-risking procurement. **[sourced]**
  - **April Health merger** explicitly aimed at unlocking **US CoCM reimbursement**, pairing AI with human specialists/psychiatrists so primary-care clinics can bill for behavioral health. **[sourced]**
  - Historical preference for **rules-based/curated CBT over open-ended generative LLMs** is a safety-and-liability-driven choice supporting clinical-credibility positioning. **[inference]**

## Dimension 11 — Stated vs. real motivations

**Stated motivation:** Democratize and de-stigmatize mental-health access — "meet people where they are," from everyday workplace stress to debilitating depression/anxiety; close the global treatment gap (underserved, low-income, rural, the "missing middle of mental health"); provide safe, evidence-based, anonymous support and reduce NHS/therapy waitlist suffering. Founders frame it as a mission born from Aggarwal's own depression and a desire to "scale impact." **[sourced]**

**Real (operative) motivation — confidence medium-high:** Build a **defensible, reimbursable clinical-infrastructure business** by using a free/anonymous consumer chatbot as a low-cost **acquisition and evidence-generation funnel**, then monetizing primarily through **enterprise, payor, and health-system contracts (~80% B2B)**. The heavy investment in regulatory credentials (NHS DCB0129, FDA Breakthrough Designation), peer-reviewed evidence, and waitlist/triage integrations is a **moat-building, procurement-enabling strategy** distinguishing Wysa from unregulated consumer chatbots and justifying institutional pricing. The **April Health / CoCM** focus reveals a clear pull toward **US reimbursement dollars**. The mission/impact framing is genuine and investor-attractive, but the operative driver is **converting clinical legitimacy + scale into recurring institutional revenue**. Stigma/anonymity, originally a mission discovery, doubles as the competitive wedge. **[inference]** — *This "real motivation" reading is inferred from disclosed revenue mix, regulatory strategy, and the April Health/CoCM pivot, not a stated admission.*

**Tension to note:** Press materials describe Wysa's AI as *"clinically proven therapeutic AI"* — promotional language given the uneven and partly null evidence base (see Dimension 5). The gap between marketing ("clinically proven," "RCT more effective than orthopedic care") and the actual evidentiary record (single-arm feasibility study, null NHS RCT, designation-not-approval) is the clearest signal that clinical-legitimacy positioning is doing commercial work beyond what the studies support. **[contested]**

## Dimension 12 — Engineering difficulty (3/5)

**Rating: 3/5.** **[inference]**

- **What lowers difficulty:** the core therapeutic engine is **deliberately NOT open generative** — it is a clinician-authored, pre-scripted **rule engine**. The genuinely hard, novel ML is concentrated in the **120+ NLU intent/emotion classifiers** that route free text to the right scripted flow, plus **real-time crisis/risk detection** on free text. NLU intent classification and routing are well-trodden engineering, not frontier research. Curated-content delivery is comparatively low-risk to build. **[inference]**
- **What raises difficulty:** **clinical-safety engineering at regulated scale** — DCB0129 compliance (CSO, escalation paths, audit loops), reliable **crisis detection** with low false-negative tolerance (a missed suicidal-ideation signal is catastrophic), **multi-region deployment** (NHS EHR/iaptus integration, US CoCM billing workflows), and **selective, guard-railed LLM layering** atop a rule engine without breaking safety guarantees. The integration and compliance surface — not the core ML — is where the real engineering weight sits. **[inference]**
- Net: a competent team could rebuild the conversational core; the moat and the difficulty are in **safety-critical reliability, regulatory integration, and clinical-governance tooling**, which is meaningful but not at the 4–5 (novel research / frontier-systems) tier. **[inference]**

---

## Sources

- https://tracxn.com/d/companies/wysa/__YEHv0JLExoPTeMeL2OhbNwdldK37lOPp7sWaWQecea8
- https://www.crunchbase.com/organization/touchkin-eservices
- https://techcrunch.com/2022/07/14/wysa-20-million-series-b-funding-expand-therapist-chatbot-wider-mental-health-services/
- https://techcrunch.com/2021/05/21/mental-health-app-wysa-raises-5-5m-for-emotionally-intelligent-ai/
- https://www.bwdisrupt.com/article/touchkin-raises-13m-in-seed-funding-from-kae-capital-others-for-its-mental-health-chatbot-wysa-123271
- https://inc42.com/buzz/pi-ventures-leads-2-mn-funding-round-in-mental-health-startup-wysa/
- https://www.businesswire.com/news/home/20250313775451/en/Wysa-and-April-Health-Merge-to-Revolutionize-Access-to-Behavioral-Health-Care-Through-Primary-Care-Providers
- https://www.mobihealthnews.com/news/wysa-merges-april-health-combine-ai-and-person-mental-healthcare
- https://emhicglobal.com/hall-of-fame/ramakant-vempati-jo-aggarwal/
- https://thepolitic.org/an-interview-with-jo-aggarwal-co-inventor-of-wysa/
- https://play.google.com/store/apps/details?id=bot.touchkin
- https://www.wysa.com/faq
- https://www.wysa.com/nhs-talking-therapies
- https://emhicglobal.com/artificial-intelligence-2/wysa-transforming-mental-health-through-ai-driven-support/
- https://www.meegle.com/en_us/topics/ai-app/wysa
- https://www.businesswire.com/news/home/20241105716965/en/Wysa-Unveils-Wysa-Copilot-to-Elevate-Mental-Health-Therapy-With-AI
- https://blogs.wysa.io/blog/company-news/wysa-unveils-wysa-copilot-to-elevate-mental-health-therapy-with-ai
- https://www.businesswire.com/news/home/20240415230248/en/AI-Detects-82-of-Mental-Health-App-Users-in-Crisis-Finds-Wysa
- https://blogs.wysa.io/blog/company-news/ai-detects-82-of-mental-health-app-users-in-crisis-finds-wysas-global-study-released-on-the-role-of-ai-to-detect-and-manage-distress
- https://mhealth.jmir.org/2018/11/e12106/
- https://formative.jmir.org/2022/2/e34889/
- https://www.businesswire.com/news/home/20220512005084/en/Wysa-Receives-FDA-Breakthrough-Device-Designation-for-AI-led-Mental-Health-Conversational-Agent
- https://blogs.wysa.io/blog/research/wysa-receives-fda-breakthrough-device-designation-for-ai-led-mental-health-conversational-agent
- https://www.sciencedirect.com/org/science/article/pii/S2561326X24003160
- https://www.hra.nhs.uk/planning-and-improving-research/application-summaries/research-summaries/clinical-investigation-of-wysa-v10/
- https://doi.org/10.1177/00207640251415507
- https://www.nice.org.uk/guidance/htg756/resources/digital-front-door-technologies-to-gather-service-user-information-for-nhs-talking-therapies-for-anxiety-and-depression-assessments-early-value-assessment-pdf-1809600827144389
- https://www.jmir.org/2025/1/e67114
- https://www.prnewswire.com/news-releases/wysa-the-leading-ai-powered-mental-health-platform-welcomes-new-senior-executive-members-301399313.html
- https://theorg.com/org/wysa
- https://www.craft.co/wysa/executives
- https://h1bdata.info/index.php?em=touchkin+eservices
- https://www.levels.fyi/companies/wysa/salaries
- https://www.glassdoor.co.in/Salary/Wysa-Salaries-E2924104.htm
- https://rorycellanjones.substack.com/p/ai-in-the-nhs-therapy-from-a-chatbot
- https://nhsaccelerator.com/innovations/wysa/
