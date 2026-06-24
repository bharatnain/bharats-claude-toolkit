# DOSSIER — ieso (product: Velora)

**Legal entity:** ieso Digital Health Limited (Cambridge, UK). **Brand/product:** Velora. **HQs:** Cambridge, England (R&D/clinical heritage) + Boston, MA (101 Federal St, Suite 1900, Boston MA 02110) for US commercial. *[sourced]*

**Critical framing (load-bearing throughout):** "ieso" today is NOT the same operating business as legacy "ieso Digital Health." On 20 Aug 2025 ieso sold its UK NHS-facing care operations (typed/video therapy, ~600 contracted therapists) to Mindler and now operates as an API-first/white-label clinical-AI company built around Velora. Two product *generations* must also be kept apart: (1) the earlier **tree-based/NLP** blended product tested in the peer-reviewed JMIR study, and (2) the **generative-AI Velora**. Conflating them is the single most common error in the source material. *[sourced + inference]*

---

## Dimension 1 — Company journey / origin story

- Founded ~2000 (one source range 2000-2002) by **Barnaby (Barney) Perks** as **"PsychologyOnline,"** providing typed/text-based therapy in Cambridge UK. Primary sources consistently say 2000; the "2000-2002" hedge is unnecessary but not wrong. *[sourced]*
- **2009:** A study in *The Lancet* validated online CBT; **Imperial Innovations** became the first institutional investor. *[sourced]*
- **~2013:** Rebranded to **ieso Digital Health**; signed first major NHS Trust contract, beginning a decade-plus relationship with NHS Talking Therapies; eventually held contracts with ~1/3 of England's integrated care systems plus a national Scotland contract. *[sourced]*
- **2017:** Raised £18m led by Draper Esprit and Touchstone Innovations. *[sourced]*
- **Through the 2010s:** Accumulated a large outcomes-indexed clinical dataset (cited ~220k hours ~2018, ~460k hours by 2021, now 750k-815k hours / ~1B words). At the 2021 Series B, ieso had delivered ~460,000 hours of therapy to ~80,000 patients. *[sourced]*
- **23 Nov 2021:** $53M (~£39M) Series B led by Morningside to build autonomous AI therapy and enter the US. *[sourced]*
- **July 2024:** Published a study it characterized as "proving" its AI program is as effective as human care. *(See Dim 5 — this is marketing overstatement of the JMIR e69351 single-arm study, which tested the tree-based product, not generative Velora.) [sourced for the press claim; contested as to its accuracy]*
- **Nov 2024:** Kent Tangen appointed CEO to drive US expansion. *[sourced]*
- **20 Aug 2025:** Sold UK telecare/NHS-facing typed-and-video therapy services business to Mindler (pan-European digital therapy provider) to become a pure AI company; ieso Digital Health Ltd remains independent and retains Velora; advisors Cooley LLP and Artis Finance; terms officially undisclosed (one secondary source ~£20m). *[sourced; deal value contested]*
- **Oct 2025 onward:** Going API-first/white-label with Velora, focused on the US. *[sourced]*

---

## Dimension 2 — Tech stack & architecture

- Velora is publicly described as a **"proprietary three-layer architecture"** combining clinical rigor, personalization, and safety, delivered as a **modular, time-limited** CBT/ACT program (not an open-ended chatbot). *[sourced — but this is marketing language verbatim from the product page, not an independently verified engineering description]*
- Ships as a **white-label web app and as an API** that plugs into partner care pathways (the Oct 2025 "API-first" pivot). Velora described as "intentionally modular and time-limited by design." *[sourced]*
- **Concrete infra/stack details — unknown — not found.** Cloud provider, languages, model-serving, vector store: not publicly disclosed. The company's Himalayas tech-stack profile is empty; press/product materials and the safety preprint describe architecture only conceptually ("three-layer," "multi-agent safety"). The absence is genuine. *[sourced as a negative claim]*
- **Heritage implying mature pipelines:** ieso ran a real-world online CBT service at scale for years and built the Therapy Insights Model (TIM) therapist-augmentation tool (2019), implying mature data pipelines, transcript processing, and outcomes linkage. *[sourced]*

**The decisive, hard-to-replicate asset is the DATA and the clinical/eval apparatus around it, not a novel model architecture.** *[inference]*

---

## Dimension 3 — AI/ML techniques & models

- **Peer-reviewed NLP/deep-learning lineage (real, but cited figures must be corrected):** ieso has a genuine deep-learning lineage auto-coding therapy-session utterances and linking content to clinical outcomes. **CORRECTION (verifier):** the often-quoted figures "~90,000 hours / 17,572 patients / 90,934 transcripts, therapist+patient utterances" are a **conflation of two distinct papers**. Those numbers belong to the **2019 JAMA Psychiatry** paper ("Quantifying the Association…"), which coded **therapist utterances only**. The separately cited 2020 Tandfonline paper ("Understanding the relationship between patient language…") coded **patient** utterances over ~34,000 patients / ~188,000 hours with 340 annotated transcripts. The underlying lineage is real; the source-to-figure mapping in earlier findings was wrong. *[contested → corrected per verifier]*
- **AI leadership — entity/staleness caveat:** **Valentin Tablan** (Chief AI Officer/SVP AI on the *legacy* iesogroup.com page; 20+ yrs NLP, Sheffield PhD, ex-Amazon lead scientist on Alexa general-knowledge Q&A, 70+ publications, oversaw TIM 2019). **However**, the *current* ieso.ai/about-us roster lists **Ronan Cummins, PhD as "VP of AI"** and does **not** list Tablan — suggesting Tablan is tied to the legacy/group entity while Cummins leads AI at the post-divestiture ieso.ai company. Treating Tablan as the *current* Velora AI lead may conflate legacy and current org. *[sourced for both, with verifier-flagged staleness/entity caveat]*
- **Base model / from-scratch vs. fine-tuned — unknown — not found.** Public materials do NOT name a base foundation model and do NOT confirm whether Velora is from-scratch or a foundation LLM grounded on ieso data. Marketing says "trained on 750k+ hours… not a generic LLM" / "purpose-built for mental health." *[sourced for the marketing claim; base model not disclosed]*
- **INFERENCE (correctly labeled, endorsed by verifier):** Velora is almost certainly a **foundation LLM conditioned via proprietary fine-tuning and/or RAG** over the outcomes-indexed corpus, plus structured CBT/ACT module scaffolding and a multi-layer safety stack — **not** a frontier-grade model trained from scratch on 1B words (which would be infeasible). Consistent with the preprint's "constrained generative AI architecture governed by a multi-agent safety system," though that phrasing does not confirm the design. Remains unconfirmed by ieso. *[inference]*
- **Disclosed safety/eval apparatus:** "safety by design," risk detectors, human-in-the-loop clinical review ("no black boxes"), de-identification/PII masking, post-deployment audits, continuous evaluation. *[sourced]*
- **Moat:** The outcomes-indexed dataset is the genuine proprietary moat and the basis for evals; the guardrails + crisis-detection + clinical-governance architecture is industry-standard for regulated mental-health genAI. *[inference]*
- **De-conflation flag (upheld):** The JMIR/PMC "Safety and User Experience of a Generative AI Digital Mental Health Intervention" RCT (text-davinci-003, ~2,207 reviewed responses, Azure) is a **Woebot Health** study (all 15 authors Woebot, San Francisco; corresponding author Timothy R. Campellone) — **NOT ieso**, and must not be attributed to ieso despite surfacing in ieso searches. *[sourced; conflation correctly excluded]*

---

## Dimension 4 — Therapeutic approach, modality encoding, human-in-the-loop

- **Modality:** Grounded in **cognitive behavioral therapy (CBT)** — "every interaction and exercise is grounded in CBT-based principles"; delivers "clinically validated CBT-based skills." Delivered as time-limited, modular skills-training ("a guided program that teaches people the skills they need"), text-based, targeting anxiety and depression symptoms — not open-ended chat. *[sourced]*
- **Third-wave / ACT elements:** An ACT-inclusive structured program appeared in a Roche Type-2-diabetes collaboration, and the May-2025 JMIR GAD study describes "principles from traditional CBT… including third-wave approaches, that is, acceptance and commitment therapy (ACT)." Extent of ACT in *current* Velora is not precisely quantified. *[inference — extent unknown]*
- **How technique is encoded — two distinct generations (must be separated):**
  1. **Earlier product** (basis of the peer-reviewed JMIR e69351 study): **NOT generative.** A "tree-based dialogue system where natural language processing was used to deliver appropriate clinician-prewritten responses with controlled use of natural language generation" — i.e., scripted/branching with tightly bounded NLG. *[sourced]*
  2. **Velora (generative-AI product):** a "constrained generative AI architecture governed by a multi-agent safety system." Technique encoded via clinician curation of the program/skills plus constraints/guardrails on the generative model, rather than free-form LLM output. *[sourced]*
- **Human-in-the-loop:**
  - *Earlier blended model (JMIR study):* substantial human involvement — average clinician time **1.6 hours/participant** (range 31-200 min: ~66-min assessment, review and discharge appointments), plus fortnightly research-coordinator check-in calls; clinicians monitored GAD-7/PHQ-9 and escalated risk. *[sourced]*
  - *Velora (generative):* oversight is **supervisory/monitoring**, not per-session delivery — "human clinicians continuously monitor and review Velora for safety" via "clinician-trained supervision agents" monitoring user input and AI output, plus continuous post-deployment audits. Automated delivery with clinicians in an oversight/audit loop. *[sourced]*

---

## Dimension 5 — Safety, crisis handling, clinical evidence/trials, FDA/regulatory

- **Safety architecture:** "multi-agent safety system combining synthetic high-risk scenario testing, automated harm detection, and clinician oversight"; "safeguards, risk detectors, and human oversight"; in-program guardrails to prevent misuse; PII masking; explicit consent; continuous post-deployment monitoring. *[sourced]*
- **Crisis-escalation pathway — unknown — not found.** The specific protocol on active suicidal ideation (human handoff, hotline routing, human contact) is NOT publicly detailed. The preprint only states flagged sessions were "handled according to escalation policies." *[sourced as a negative claim]*

**Clinical evidence — two main studies:**

**A) Peer-reviewed — JMIR e69351** (published 13 May 2025). Actual title: "*Combining Artificial Intelligence and Human Support in Mental Health: Digital Intervention With Comparable Effectiveness to Human-Delivered Care*." Conducted Oct 2023-May 2024. Mild-severe GAD. **N=299 enrolled (169 per-protocol).** Single-arm pragmatic design with propensity-matched external NHS controls (waitlist, face-to-face CBT, typed CBT). Per-protocol GAD-7 change **-7.4 (d=1.6)** vs face-to-face CBT -6.4 (d=1.3); noninferiority met (upper CI below 1.8 margin). No serious adverse events. **CRITICAL: this tested the tree-based/NLP product, NOT generative Velora.** *[sourced; the de-conflation is load-bearing and verified]*

**B) Preprint (NOT peer-reviewed) — PsyArXiv/OSF DOI 10.31234/osf.io/8kvm6.** **CORRECTED title (verifier, v2):** "*Safety Evaluation of a Generative AI Agent for Anxiety and Depression Symptoms*" — **WITHOUT "Clinical-Grade."** "Clinical-grade" is ieso marketing language that had been laundered into the cited title; the verified v2 title omits it. v1 posted 27 Sept 2025; v2 posted 30 Apr 2026. **This IS the generative Velora.**
- *Authorship:* Lead author is **Pearla Papiernik**; v2 runs 16 authors "from Papiernik through Clare Palmer." Earlier findings implied Ewbank lead authorship — **not confirmed**; Ewbank/Catarino/Tablan/Cummins could not all be confirmed on v2 from the available record. ieso affiliation is clear; the specific roster as previously stated is only partially verified. *[contested → partially supported per verifier]*
- *Study 1 (simulation):* **43,325** generated responses; potentially-harmful outputs at **0.01% (95% CI 0.01-0.03%)** — i.e., small but **non-zero** — with none encouraging self/other harm, invalidating users, or using offensive language. *[sourced]*
- *Study 2 (real-world):* 2-week prospective study of US adults with moderate-to-severe anxiety/depression. **N=111** (RESOLVED — the earlier "85 vs 111" contest is settled at **111** in v2; the 85 was a v1/abstract artifact). **12,040** responses; no AI content-safety risks detected (95% CI 0.00-0.04%); zero serious adverse events; **>50% met responder criteria after ~90 min median use.** *[sourced; N upgraded from contested to sourced per verifier]*
- *Deterioration rates of 5% (anxiety) / 3% (depression):* **unsupported — not found** in the verified v2 record (deterioration "not reported" in the fetched summary). Likely from a secondary/marketing source; treat as unsupported pending direct preprint reading. *[unsupported]*
- *Authors stress this is early signal requiring controlled-trial validation.* *[sourced]*

**Marketing claim — "zero AI-induced safety incidents across 55,000+ evaluated responses":** verified verbatim on the product page, but it is a **marketing-as-fact overstatement.** The 55,000+ ≈ 43,325 (simulated) + 12,040 (real-world) = 55,365 from the **non-peer-reviewed** preprint. "Zero" is only literally true for the smaller Study 2; Study 1 found a non-zero 0.01% harmful-output rate. Self-reported, not independently audited. *[sourced for the claim's existence; contested as to accuracy]*

**FDA / regulatory status:** Velora is **explicitly NOT FDA-cleared** — product-page disclaimer: "The Velora program is not FDA-cleared. Not for diagnosis or treatment of medical conditions." No 510(k), De Novo, or breakthrough-device designation, and **no CE mark / UKCA / MHRA clearance**, found in available sources. As of the current date the FDA has authorized 1,200+ AI devices but cleared **zero** generative-AI mental-health tools; its Digital Health Advisory Committee met **6 Nov 2025** to weigh guardrails for generative-AI mental-health devices. ieso's stated posture (Oct 2025 Hemingway interview; Jun 2025 BHT article by Clare Palmer) is to plan for the most-constraining regulatory path and treat safety as a continuous discipline, citing FDA's Predetermined Change Control Plan for systems that "learn as they go." **Net: Velora currently operates outside formal medical-device clearance in both US and UK.** No regulatory overstatement in the findings here. *[sourced]*

---

## Dimension 6 — Engineering difficulty

The core generative loop sits on commodity foundation-model + RAG/fine-tuning + guardrails patterns many teams can now assemble. What raises difficulty into the upper-middle range: (a) a uniquely large, longitudinal, outcomes-**linked** clinical corpus that took ~25 years to accumulate and is effectively non-replicable; (b) safety-critical engineering for a regulated, high-risk domain (suicide/self-harm crisis detection, clinical governance, auditability, de-id/PII, human review at scale); (c) rigorous clinical evaluation (RCTs/simulated + real-user safety testing, peer review) as a first-class engineering deliverable; (d) productionizing this as a multi-tenant white-label API. The novelty is in **data + evidence + safety regime**, not model research. *[inference]*

### Engineering difficulty (3.5/5)
The generative core is buildable on now-standard primitives (foundation LLM + fine-tuning/RAG + layered guardrails + crisis detection), which **caps** raw model-engineering difficulty. It is pushed **above a 3** by the safety-critical requirements of a regulated mental-health setting (reliable risk/crisis detection, human-in-the-loop review at scale, auditability, de-identification, clinical governance across the AI lifecycle) and by treating rigorous clinical evaluation as core engineering. The single biggest moat — the 750k-815k-hour outcomes-indexed corpus — is a **data-acquisition and longitudinal-curation feat (25 years)** more than a pure-engineering one, and the lack of any disclosed novel model architecture keeps it **below a 4**. INFERENCE-heavy because ieso does not publish its model stack, base model, or infra; the rating reflects the plausible architecture, not confirmed internals. *[inference]*

---

## Dimension 7 — Founders, key hires, headcount, org shape

- **Founder:** Barnaby (Barney) Perks — founder & founding CEO, company founded 2000 (Cambridge UK); has since left ieso to lead St John's Innovation Centre. *[sourced]*
- **Current leadership (ieso.ai/about-us, 8-person team):**
  - **Kent Tangen** — CEO (appointed Nov 2024; ~25 yrs scaling businesses; hired to drive US expansion). *[sourced]*
  - **Dr. Andy Blackwell** — Chief Science & Strategy Officer; credited as inventor of the concept behind Velora; long-tenured (formerly Chief Scientist). *[sourced]*
  - **Ronan Cummins, PhD** — VP of AI (current technical AI lead at the post-divestiture company). *[sourced]*
  - **Alyssa Dietz, PhD** — Head of Clinical Strategy. *[sourced]*
  - **Clare Palmer, PhD** — Director of Evidence Generation. *[sourced]*
  - **Joanna Beasley** — Head of Product & Design. *[sourced]*
  - **James Dold** — Head of Sales. *[sourced]*
  - **Molly Fuller** — Head of Strategic Partnerships. *[sourced]*
  - *(Valentin Tablan — CAIO per legacy iesogroup.com — appears tied to the legacy/group entity and is NOT on the current ieso.ai roster; see Dim 3.) [sourced, with staleness caveat]*
- **Board (legacy entity, ~7 active members per Tracxn):** Chairman **Andy Richards CBE**; members incl. Nigel Pitchford, Vishal Gulati, Michael Black, Joanne Parfrey, Stephen Bruso (also John Richard Marsh / Andrew Richards cited). *[sourced]*
- **Org shape (inference):** Flat functional structure under the CEO — Science/Strategy (Blackwell) + AI (Cummins) as the technical/clinical core; dedicated Clinical Strategy + Evidence Generation functions reflect the regulated-medical-device posture (**4 of 8 leaders hold PhDs**); commercial arm = Sales + Partnerships + Product, consistent with API-first/white-label GTM. Dual HQ Cambridge + Boston. *[inference from roster + office data]*
- **Headcount (best estimate ~30-80 FTEs — INFERENCE):** "The Org" lists ieso US at **11-50** (US entity, ~17 open roles); LinkedIn shows **51-200** / PitchBook **~192** — but those are **stale**, pre-Mindler, and include the ~600 therapists now divested. The ~30-80 consolidated AI-company figure is a labeled inference between those bounds. *[ranges = sourced/data; point estimate = inference]*

---

## Dimension 8 — Compensation bands

**CRITICAL CAVEAT:** There is **NO ieso-specific compensation data — unknown — not found.** Verified absences: zero H1B LCA records for "ieso" on h1bdata.info (does not sponsor H1B); no levels.fyi company page; Glassdoor pages 403-blocked or conflated with the unrelated Ontario electricity operator "IESO"; no posted ieso salary ranges surfaced. **All figures below are ESTIMATEs anchored to Boston-market / Series-B-stage comparables (June 2026), NOT ieso data.** Expressed as base; early-stage equity additive but unknown. *[inference/estimate; negative claims sourced]*

**Boston market anchors [data, benchmark only]:** ML Engineer median ~$194K (levels.fyi); startup avg ~$139K base, range $85K-$310K (Wellfound); senior ML at top-tier Boston cos ~$255K median total comp.

**Role-level ESTIMATEs (Boston/remote-US, Series-B health-AI; equity extra) [all estimate]:**
- AI/ML Engineer (mid): base ~$130K-$170K
- Senior/Staff ML/AI Engineer: base ~$170K-$215K (total w/ equity ~$230K-$280K)
- VP of AI (Cummins-level): base ~$220K-$300K + meaningful equity
- Software Engineer (backend/full-stack, mid-senior): base ~$120K-$175K
- Product Manager / Head of Product: IC ~$140K-$180K; Head-of ~$190K-$250K
- Clinical Strategy / Evidence (PhD scientist): base ~$120K-$170K; Director/Head-of ~$170K-$230K
- Head of Sales / Partnerships: base ~$150K-$200K + variable/OTE potentially doubling cash
- C-suite (CEO/CSO): UK director pay historically modest (typical Cambridge scale-up CEO base ~£200K-£350K); US CEO comp higher but **unknown — not found**.

**Open hard-data gap:** ieso Digital Health Ltd files at Companies House; aggregate director remuneration and highest-paid-director figures are disclosed there but were **NOT retrieved** in this pass — the only hard UK comp data available. *[flagged open item]*

**Confidence:** Dim 7 HIGH on named leaders/founder, MEDIUM on exact headcount. **Dim 8 LOW** — no company-specific comp data; figures are market-benchmark estimates only.

---

## Dimension 9 — Funding & AI investment

- **2009:** First institutional investment (Imperial Innovations). *[sourced]*
- **2017:** £18m led by Draper Esprit + Touchstone Innovations. *[sourced]*
- **23 Nov 2021:** **$53M / ~£39M Series B** led by **Morningside**, with **Sony Innovation Fund** (new) and existing holders IP Group, Molten Ventures (formerly Draper Esprit) and Ananda Impact Ventures. This is the **only round corroborated by multiple primary sources.** Morningside (NY-based, est. ~£430m) described as a backer "from Day One"; Dr Andy Richards a named champion. *[sourced]*
- **Total raised — INTERNALLY INCONSISTENT across sources:**
  - **"$70M+"** — ieso's own 2025 messaging; **the most defensible self-reported figure.** *[sourced]*
  - **"~$91M"** — appears in findings (Dim 7) with **no clear primary source**; treat as unsupported. *[unsupported]*
  - **"~$126M over 11 rounds" incl. a ~$35.9M Nov-2024 Series C** — Tracxn aggregator only; the Series C is **not corroborated by any located press release** and conflicts with ieso's own "$70M+." Treat as **unverified aggregator data.** *[contested]*
- **Valuation:** No public valuation figures for any ieso equity round — **unknown — explicitly not disclosed.** *[sourced]*
- **Mindler divestiture (Aug 2025):** reportedly ~£20m (single secondary source) but terms officially undisclosed. *[contested]*

---

## Dimension 10 — Business model & business drivers behind tech decisions

- **Old model:** B2G/B2B service revenue — human therapists delivering typed CBT, paid by the NHS per contract (~£7.5m turnover circa 2018). *[sourced]*
- **New model:** SaaS/licensing — Velora as a generative-AI therapy program embedded via **white-labeled APIs** into partners' platforms (virtual-care companies, chronic-condition management platforms, health systems). *[sourced]*
- **Tech decisions driven by business realities:**
  - (a) CEO Kent Tangen: "people really did not want a single solution anymore. One-off mental health apps weren't gaining traction" → API/embed beats a standalone app on go-to-market ("integration over isolation"). *[sourced]*
  - (b) The outcomes-indexed dataset (750k+ hrs) is positioned as the defensible moat enabling claims of "outcomes on par with human-delivered care" and "zero AI-induced safety incidents" — the wedge for regulated buyers. *[sourced; note the "zero incidents" claim is overstated, see Dim 5]*
  - (c) Divesting the labour-intensive NHS services business removes a low-margin, capacity-constrained operation so capital/focus concentrate on the scalable software product and the larger US market. *[sourced]*
- **Economics** described by Tangen as "very similar" to the prior model with the "same value proposition." *[sourced]*

---

## Dimension 11 — Stated vs. real motivations

### Stated vs. real motivations

**Stated motivation:** "ieso is committed to building the future we've long envisioned: delivering safe, effective AI-powered mental healthcare at scale," with mental health framed as one of AI's "most urgent and natural use cases" (CEO Kent Tangen). The stated rationale for the API-first/white-label pivot is **patient access and product-market fit**: standalone mental-health apps "weren't gaining traction," so embedding clinically-validated AI into existing care workflows ("integration over isolation") best reaches people who can't access human therapists. The data moat (750k+ outcomes-indexed hours) is presented as enabling care "on par with human-delivered care." The Mindler divestiture is framed as "sharpening focus" on Velora. *[sourced]*

**Real motivation (medium-high confidence — INFERENCE):** A **scaling-and-margins play dressed as a mission narrative.** The human-delivered NHS service was a low-margin, capacity-bound, single-payer (UK government) business with modest turnover; software licensing of an AI model against a hard-to-replicate proprietary dataset is far more scalable and higher-margin, and the US is a much larger, better-paying market than the NHS. Selling the services arm to Mindler (and earlier divesting telecare) converts a costly operating business into focus + likely cash while keeping the crown jewel — the outcomes-linked data and the AI built on it. API-first/white-label is also pragmatic GTM: ieso lacks a consumer distribution engine, so riding partners' existing platforms (and partners' demand for a conversational-AI feature) is cheaper customer acquisition than building a branded app. The "outcomes/safety" emphasis is as much a **regulatory and enterprise-sales unlock** as a clinical ethic. Investor framing in 2025 shifting toward "regulatory strategy" and "go-to-market" corroborates a commercialization-pressure read. *[inference]*

---

## Dimension 12 — Notable claims, red flags & evidence integrity

- **Marketing-as-fact — "zero AI-induced safety incidents across 55,000+ responses":** Overstates the preprint. Study 1 found a non-zero 0.01% harmful-output rate (95% CI 0.01-0.03%) across 43,325 responses; only Study 2 (12,040) found zero detected. Self-reported, non-peer-reviewed, not independently audited. *[contested]*
- **Marketing-as-fact — "Clinical-grade":** Laundered into the cited preprint *title*; the verified v2 title omits "Clinical-Grade." *[contested]*
- **Marketing overstatement — July 2024 "Proves AI as effective as human care":** The press headline says "Proves," but the underlying JMIR e69351 study is a single-arm pragmatic design with external propensity-matched controls (not an RCT) and supports "comparable/noninferior effectiveness," not "proof." It also tested the **tree-based** product, not generative Velora. *[contested]*
- **Citation conflation (Ewbank lineage):** "90,934 transcripts / 17,572 patients / therapist+patient utterances" merges a 2019 JAMA Psychiatry paper (therapist utterances) with a separate 2020 Tandfonline paper (patient utterances, different N). Lineage real; source-to-figure mapping was wrong. *[contested → corrected]*
- **Entity/staleness conflation (Tablan vs Cummins):** Legacy iesogroup.com lists Tablan as CAIO; current ieso.ai lists Cummins as VP of AI. Mixing them conflates legacy-group and current-company org. *[contested]*
- **Dataset figure drift:** Product page "750,000+ hours / 1B words" vs Oct-2025 interview "815,000 hours / 145,000+ patients / 25 yrs." Both company self-reported, never independently audited; the live product page carries the lower/rounded (staler) number. *[contested — both figures verified at their sources]*
- **Funding inconsistency:** Total raised stated three ways ($70M+, ~$91M, ~$126M); only the $53M Series B is multi-source-corroborated; "$91M" has no clear source; Tracxn $126M + Nov-2024 Series C are uncorroborated. *[contested]*
- **De-conflation upheld:** The Woebot Health "Safety and User Experience…" RCT (text-davinci-003) is **not** ieso and is correctly excluded. *[sourced]*
- **Regulatory:** No overstatement — "Not FDA-cleared" and "FDA has cleared zero generative-AI mental-health tools (DHAC met 6 Nov 2025)" are both verified accurate. *[sourced]*
- **Unsupported:** Study 2 deterioration rates (5% anxiety / 3% depression) not found in verified preprint v2 — treat as unsupported. *[unsupported]*

---

## Sources

- https://www.ieso.ai/velora
- https://www.ieso.ai/
- https://www.ieso.ai/about-us
- https://www.thehemingwayreport.com/articles/73-why-ieso-is-going-api-first
- https://thehemingwayreport.beehiiv.com/p/73-why-ieso-is-going-api-first
- https://www.jmir.org/2025/1/e69351
- https://sciety.org/articles/activity/10.31234/osf.io/8kvm6_v1 (PsyArXiv/OSF DOI 10.31234/osf.io/8kvm6, v1 27 Sep 2025; v2 30 Apr 2026)
- https://www.tandfonline.com/doi/full/10.1080/10503307.2020.1788740 (2020 patient-language paper)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6707006/ (2019 JAMA Psychiatry therapist-utterance paper)
- https://www.iesogroup.com/team/dr-valentin-tablan
- https://www.behavioralhealthtech.com/insights/proving-value-in-motion
- https://himalayas.app/companies/ieso-digital-health/tech-stack
- https://www.psychiatrictimes.com/view/fda-committee-meets-on-generative-ai-digital-mental-health-devices
- https://www.crunchbase.com/organization/ieso-digital-health
- https://www.scaleupinstitute.org.uk/stories/ieso-digital-health/
- https://www.digitalhealth.net/2025/08/mindler-acquires-nhs-online-mental-health-service-supplier/
- https://www.businesswire.com/news/home/20211123005738/en/ieso-Raises-%2453m-to-Address-Global-Mental-Health-Crisis-With-Digital-Therapeutics
- https://techcrunch.com/2021/11/23/uk-based-mental-health-provider-ieso-raises-53m-armed-with-an-unprecedented-dataset/
- https://www.businessweekly.co.uk/posts/ieso-ai-set-to-revolutionise-global-treatment-of-mental-disorders
- https://tracxn.com/d/companies/ieso/__75AiZFMDlputVo3kEe4GCqjkmNxDKVQsYDduiYNQDJk
- https://www.businesswire.com/news/home/20240718180916/en/Landmark-Study-Proves-AI-Driven-Mental-Health-Program-is-as-Effective-as-Human-Care
- https://www.ipgroupplc.com/news-and-events/portfolio-news/2025/2025-08-20
- https://www.business-sale.com/news/division-sale/mindler-acquires-uk-telecare-services-division-of-ieso-digital-health-228037
- https://www.businesswire.com/news/home/20250820050198/en/ieso-Sharpens-Focus-on-AI-Powered-Mental-Healthcare-with-Sale-of-UK-Telecare-Services-Business
- https://www.businessweekly.co.uk/posts/ieso-founding-ceo-perks-succeeds-david-gill-as-st-johns-innovation-centre-boss
- https://www.ipgroupplc.com/news-and-events/portfolio-news/2024/2024-11-04
- https://theorg.com/org/ieso-us
- https://www.linkedin.com/company/iesohealth
- https://www.mobihealthnews.com/news/emea/digital-mental-health-firm-ieso-lands-53m-series-b-round
- https://h1bdata.info/index.php?em=ieso
- https://www.levels.fyi/t/software-engineer/title/machine-learning-engineer/locations/boston-usa
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12144468/ (Woebot Health study — cited to document the de-conflation; NOT ieso)
