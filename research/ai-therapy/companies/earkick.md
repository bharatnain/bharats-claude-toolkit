# Earkick — Company Dossier

**One-line:** A tiny (~8-person), founder-led, seed-stage US/Swiss AI mental-health startup whose anonymous "Panda" companion deliberately avoids the therapy/medical-device label, rests on internal-survey-grade efficacy evidence, runs with no human-in-the-loop, and was flagged in a May 2026 Common Sense Media / Stanford safety report after vanishing from app stores mid-testing.

**Overall confidence:** Medium. The most material, most current finding (the May 2026 safety report and the app-store disappearance) is primary-sourced. Several supporting details — Swiss office, advisor identity, persona names, the report's user count — are weak, contested, or unverified, and are flagged inline below.

---

## Dimension 1 — Company overview & positioning
- **Founded 2021**, US (San Francisco HQ) with a probable Switzerland presence. *[sourced — SF confirmed by PitchBook; the Swiss office is weakly sourced and is plausible only via the founders' Swiss/Innosuisse ties]*
- Positions itself in the **general-wellness / self-care** category, not clinical care. The product is consumer-facing, anonymous, and no-registration. *[sourced]*
- Deliberately positions **away from "therapy"** as both a product and regulatory stance (see Dimensions 5 and 12). *[sourced]*

## Dimension 2 — Product
- Core product is **"Panda," a multimodal AI companion** that processes text, voice, and biometric/contextual input. *[sourced]*
- Delivers therapist-style interactions: mood check-ins, cognitive reframing, emotion labeling, distress tolerance, and paced-breathing/meditation exercises. *[sourced]*
- Built on a **multimodal LLM**; the underlying foundation model and any fine-tuning are **not publicly disclosed**. *[inference]*
- Privacy/UX features: **anonymous, no-registration, AES-256 encrypted**. *[sourced]*
- Users reportedly select a Panda **persona/tone** — examples cited as "Calm Listener" and "Motivational Coach." *[inference — persona feature plausible, but these specific names trace to marketing and were not independently corroborated; treat as marketing-sourced]*

## Dimension 3 — Market, traction & scale
- **User counts are inconsistent across sources** and should not be stated as a single fact:
  - Earkick's own current App Store listing: **250,000+ users**. *[sourced]*
  - Earlier company figure (Nov 2023): **~40,000 downloads**. *[sourced]*
  - The May 2026 Common Sense Media report asserts **"more than 3 million users"** were affected by the disappearance. *[contested — the 3M figure is unverified and conflicts with Earkick's own 250k listing; treat as the report's assertion, not established fact]*
- App is **active/available in 2026** (App Store listing shows hands-free Panda and Apple Watch features), notwithstanding the reported mid-2026 disappearance. *[sourced]*

## Dimension 4 — Therapeutic approach, modalities & human-in-the-loop
- Technique is described by Earkick's own marketing as **"rooted in" / "blending" CBT and DBT** — mood check-ins, cognitive reframing, emotion labeling, distress tolerance, breathing/meditation. *[sourced — but this is the company's marketing language; see flag below]*
- **No published protocol exists.** The exact encoding of technique (prompt engineering vs. fine-tuned model vs. scripted exercises) is not disclosed, and there is no independent validation of clinical fidelity. *[inference]*
  - **FLAG — marketing-as-fact:** "Rooted in CBT and DBT" is Earkick's own framing with no published protocol or independent fidelity validation. Treat the CBT/DBT "rooting" as a company claim, not verified clinical method.
- **Human-in-the-loop: essentially NONE.** The product is fully automated self-care; no licensed clinician reviews conversations or intervenes. *[sourced for the no-oversight design; "no in-house clinical/safety team" is an inference from headcount]*
- This no-oversight design is the central concern flagged by the May 2026 Common Sense Media / Stanford Brainstorm Lab assessment, which contrasted no-oversight AI apps against school-based apps (Alongside, Sonar) that put a trained human on the line during simulated crises. *[sourced]*

## Dimension 5 — Safety, crisis handling, clinical evidence & regulatory
- **Regulatory:** NOT an FDA-cleared/approved medical device; **no FDA submission**. By design the app disclaims "any form of medical care, opinion, diagnosis, or treatment" and avoids the "therapy" label, keeping it outside FDA device regulation (general-wellness positioning). *[sourced]*
- **Crisis handling:** Self-describes as "not a crisis service, diagnostic tool, replacement for therapy, or clinician-led pathway." A specific crisis protocol (e.g., 988 referral, self-harm detection thresholds) is **not publicly documented and could not be confirmed**. *[unknown — not found]*
- **Clinical evidence:** Headline figures of **34% mood improvement / 32% anxiety reduction over ~5–6 months** come from **internal user surveys + app analytics** (Nov 1, 2023 BusinessWire + company blog), **not a peer-reviewed RCT**. The data is correlational/observational with survivorship bias among self-selected continuing users; no causal claim is supportable. *[sourced]*
  - **FLAG — stale figure:** These 34%/32% stats are from a Nov 2023 internal survey (~2.5 years old as of this dossier) and remain the only efficacy data cited.
- **No peer-reviewed publication and no ClinicalTrials.gov (NCT) registration** for Earkick were found. *[inference — absence of evidence, not evidence of absence]*
- **Major safety event (May 2026):** The Common Sense Media Youth AI Safety Institute + Stanford Medicine Brainstorm Lab ran 3,100+ exchanges across 5 AI therapy apps spanning 13 conditions (including suicidal ideation, self-harm, psychosis). The report states Earkick (and Youper) **"vanished from app stores during the testing period, without warning to users and without referrals to alternative care."** Earkick received **no formal risk rating** because it was unavailable, but the report said it had "serious shortcomings." *[sourced — primary source confirms verbatim that Earkick "did not receive ratings because it is currently not available for download"]*
  - **FLAG — mis-attribution risk:** The "**unacceptable**" rating in the CNBC headline belongs to **Wysa, NOT Earkick**. Earkick received no rating at all because it was unavailable. Do not attribute "unacceptable" to Earkick.
- **Contested:** Other 2026 sources (App Store listings, review sites) show Earkick active in 2026, conflicting with the reported disappearance; the cause and duration of the removal are not stated, so it may have been temporary or region-specific. *[contested]*
- **CNBC** (2026-05-28) corroborated the report's findings on AI mental-health apps and teen safety, including Earkick's disappearance. *[sourced — article confirmed to exist; the Earkick-specific line could not be read directly due to a 403/paywall, but the underlying facts are primary-sourced via Common Sense Media]*

## Dimension 6 — Business model & pricing
- Consumer freemium app (anonymous, no-registration). Specific pricing tiers and subscription economics were **not found** in the research. *[unknown — not found]*

## Dimension 7 — Founders, hires & org shape
- **Founded 2021** by **Herbert Bay (CEO)** — computer-vision/AI serial entrepreneur, prior CV startups built/sold — and **Karin Andrea Stephan (COO)** — mental-health-x-tech background, ex-Impact Hub Zurich MD, Innosuisse startup trainer. *[sourced — fully corroborated across multiple independent sources, including the lead investor's own announcement]*
- **Advisors (clinical credibility, not employees):**
  - **Jasper Smits, PhD** — UT Austin Professor; exposure-therapy/CBT researcher; confirmed Earkick advisor (holds equity per ADAA disclosure). *[sourced]*
    - **FLAG — stale title:** The "Director, Anxiety & Stress Clinic" title is not on his current UT Austin page (now "Professor and Department Liaison for Medical Affairs"). Affiliation is correct; that specific title is dated.
  - **Robert Levitan, MD** — listed as an Earkick senior advisor; commonly described as a University of Toronto / CAMH psychiatrist and mood-disorders/SAD researcher. *[contested]*
    - **FLAG — possible entity conflation:** theorg.com lists "Robert Levitan" as Earkick senior advisor but gives **no** U Toronto/CAMH affiliation. The CAMH psychiatrist of the same name is real, but no primary source links him to Earkick, and a separate search associated an Earkick-linked "Robert Levitan" with the AEGIS Response Team (Bethesda, MD) — likely a different person. The CAMH identification is unverified.
- These advisory clinicians are the **de facto clinical bench**; Earkick has **no evident in-house staff clinicians**. *[inference]*
- **Headcount / org shape:** very small — **~8 employees** (PitchBook 2026); Tracxn/Glassdoor list 1–10. SF base confirmed; a Switzerland office is plausible but weakly sourced. Founder-led with mobile-dev + advisory; **no separate clinical-ops or safety team evident**. *[sourced for headcount/SF; "no safety team" is an inference from size; Swiss office weakly sourced]*

## Dimension 8 — Compensation
- **No company-specific compensation data exists.** levels.fyi has no Earkick entries; H1Bdata.info returns 0 LCA/H1B records (consistent with ~8 people split US/Switzerland and likely no H1B sponsorship); Glassdoor has a profile but no posted salary figures (only a tiny, unusable comp-sentiment rating). *[sourced — absence confirmed]*
- **Benchmark estimate only** (SF market, levels.fyi June 2026): Software Engineer SF Bay total comp avg ~$274k (range ~$201k–$378k); entry-level ~$162k–$230k. *[sourced as a benchmark]*
- **Caveat:** An ~8-person seed-stage Swiss/US startup with ~$1.56M raised almost certainly pays **below** these big-tech-weighted medians and substitutes equity; Swiss-side staff are on Swiss scales, not SF. Treat the benchmark as a ceiling, not actual bands. *[speculation — correctly self-labeled as estimate, not data]*

## Dimension 9 — Funding & investors
- **Total funding ~$1.56M.** *[sourced]*
- **$1M seed on 2021-11-25**, led by **LDV Capital** (also Tarifa Holding, WestTech Ventures, Swiss-Israel Lean Launchpad). *[sourced]*
  - **FLAG — funding timeline:** The ~$1.56M total spans multiple events. Sources indicate Earkick "was last funded April 2024" via a **Wefunder convertible note** from ~23 investors. The single "$1M seed Nov 2021" is one tranche, not the whole; the "Nov 2021 seed" framing understates the timeline.
- Lean, pre-scale capitalization — consistent with the absence of dedicated safety/clinical staff.

## Dimension 10 — Stated vs. real motivations
- **Stated motivation:** Provide accessible, low-friction, anonymous mental-health support; co-founder Karin Stephan publicly frames the company as cautious and safety-minded, arguing regulation is essential but that current approaches often "prioritize liability over user safety." *[sourced]*
- **Apparent real / structural incentives:**
  - The refusal to call the product "therapy" and the explicit disclaimers of medical care are **as much a regulatory-avoidance strategy as a safety posture** — they keep Earkick outside FDA device jurisdiction while still marketing therapist-style CBT/DBT techniques. The "we won't call it therapy" stance is consistent with both genuine caution and with avoiding the cost/liability of clearance. *[inference]*
  - Marketing leans on **clinical-sounding language ("rooted in CBT and DBT") and named academic advisors** to borrow credibility, while the actual evidence base is internal-survey-grade and there is no in-house clinical oversight or human-in-the-loop. The gap between the credibility signaling and the operational reality is the core tension. *[inference]*
  - The reported **unannounced app-store disappearance** — leaving users without referrals and their mental-health data in an uncertain state — sits awkwardly against the stated user-safety-first narrative, though cause and duration are unknown. *[contested]*
- **Net read:** Stated motivation (accessible, careful mental-health support) is plausibly sincere at the founder level, but the structural choices — general-wellness positioning, no HITL, lean clinical staffing, marketing-as-method — are also exactly what a small startup optimizing for speed, low cost, and regulatory distance would do. *[speculation]*

## Dimension 11 — Risks & red flags (summary)
- **Credibility/risk event:** May 2026 Common Sense Media / Stanford report + unannounced app-store disappearance. *[sourced]*
- **Evidence quality:** Internal-survey-grade only; no RCT, no peer review, ~2.5-year-stale stats. *[sourced/inference]*
- **No human-in-the-loop and no in-house clinical/safety team.** *[sourced/inference]*
- **No documented crisis protocol.** *[unknown — not found]*
- **Data/continuity risk:** Sensitive mental-health data left "in an uncertain state" per the report. *[sourced, with contested user-count]*
- **Advisor identity uncertainty** (Robert Levitan conflation). *[contested]*

## Dimension 12 — Engineering difficulty (2/5)
- **Rating: 2 out of 5 — low-to-moderate.**
- **Why low:** The product is, at its core, a **consumer LLM wrapper** — a multimodal companion built on an undisclosed foundation model, delivering scripted/prompted CBT/DBT-style exercises, mood tracking, and breathing/meditation content. There is **no FDA-cleared device pipeline, no RCT machinery, no human-in-the-loop infrastructure, and no clinician-ops tooling** to build or maintain. A ~8-person founder-led team ships and runs it. *[inference]*
- **What adds modest difficulty (keeps it at 2, not 1):** genuine **multimodal input** (text + voice + biometric/contextual signals), on-device/privacy-preserving design (anonymous, no-registration, AES-256 encryption), and mobile + Apple Watch / hands-free Panda integrations. These are real but well-trodden engineering problems. *[inference]*
- **What would push difficulty higher but is absent here:** clinically validated safety/crisis-detection systems, real-time risk classification with human escalation, regulated-device controls, and reproducible efficacy infrastructure — none of which Earkick appears to operate. The hard parts of *safe* AI mental health are precisely the parts Earkick has chosen not to build. *[inference]*

---

## Sources
- https://earkick.com/
- https://ideausher.com/blog/developing-ai-mental-health-companion-app-earkick/
- https://www.tech360.tv/ai-chatbots-mental-health-earkick-unique-approach-regulatory-challenges
- https://americanbazaaronline.com/2026/01/28/earkick-karin-stephan-on-leveraging-ai-to-better-mental-health-474079/
- https://earkick.com/research/how-teens-use-earkick/
- https://www.businesswire.com/news/home/20231101899856/en/Earkick-Unveils-Evidence-Supporting-AIs-Real-Time-Impact-on-Mental-Health-Improvement
- https://www.commonsensemedia.org/press-releases/some-ai-mental-health-apps-are-actively-harmful-for-teens-but-a-safer-approach-exists
- https://www.cnbc.com/2026/05/28/some-ai-mental-health-apps-have-an-unacceptable-rating-for-teens-says-report.html
- https://apps.apple.com/de/developer/earkick/id1584854533
- https://blog.earkick.com/from-vision-to-company-earkicks-1-year-on-the-way-to-becoming-the-leading-mood-anxiety-tracker/
- https://theorg.com/org/earkick
- https://liberalarts.utexas.edu/psychology/faculty/smitsja1
- https://psychiatry.utoronto.ca/faculty/robert-levitan
- https://pitchbook.com/profiles/company/482773-87
- https://www.crunchbase.com/organization/earkick
- https://h1bdata.info/index.php?em=Earkick
- https://www.levels.fyi/t/software-engineer/locations/san-francisco-bay-area
