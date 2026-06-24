# Therabot (Dartmouth) — Company Dossier

**Verifier overall confidence: HIGH**
**Entity type:** Academic research project (Dartmouth AIM HIGH Lab), not a company. No spinout, no revenue, no FDA clearance.

> **Label legend:** `[sourced]` = directly supported by a cited source · `[inference]` = reasoned from evidence/absence of evidence · `[speculation]` = plausible but unverified · `[contested]` = reported but disputed by other sources · `[unsupported]` = claim circulated but not confirmable in any verified source.

> **Scope note:** Of the 12 dimensions below, the raw research substantively covered Dimensions 4, 5, 7, and 8. The remaining dimensions were not researched and are marked "unknown — not found" with whatever can be reasonably inferred labeled as inference. **Conflated-entity warning:** Dartmouth launched a *separate* AI well-being tool called "Evergreen" (Oct 2025) — it is NOT Therabot and must not be treated as Therabot deployment or commercialization. `[sourced]`

---

## Dimension 1 — Company overview / what they do
- `[sourced]` Therabot is an academic research project from Dartmouth's AIM HIGH Lab (AI and Mental Health: Innovation in Technology Guided Healthcare), led by Nicholas C. Jacobson, PhD. It is a fully-generative AI therapy chatbot. (Dartmouth News, 2025-03-27; Geisel BMDS, 2025-04-08)
- `[sourced]` It is not a company — no spinout, no revenue, no commercial availability. (Dartmouth News, 2025-03-27)
- `[sourced]` Development began in 2019; ~6 years in development as of the 2025 trial publication. (Geisel BMDS, 2025-04-08)
- **Stated vs. real motivations:** see dedicated subsection at the end of this dossier.

## Dimension 2 — Market / problem space
- `[sourced]` Stated target problem: the supply-demand gap in mental health care — far more people need therapy than there are available clinicians; a scalable generative-AI tool grounded in evidence-based CBT is positioned to deliver on-demand support. (Dartmouth News, 2025-03-27)
- `[inference]` Addressable conditions demonstrated in trials: Major Depressive Disorder (MDD), Generalized Anxiety Disorder (GAD), clinically-high-risk feeding/eating disorders, and (follow-on) anxiety/depression in Cannabis Use Disorder. (derived from trial registrations NCT06013137, NCT06920238)
- Market sizing, competitive positioning vs. Woebot/Wysa/Slingshot/Ash, and go-to-market: **unknown — not found.** `[inference]` MIT Technology Review noted competitors are "slight variations of Llama," implicitly contrasting Therabot's custom approach, but no formal competitive analysis was researched.

## Dimension 3 — Product / technology stack
- `[sourced]` Therabot is a generative large language model fine-tuned on expert-curated mental health dialogues. (National Elf Service, 2025-04)
- `[sourced]` The specific base LLM is **not publicly disclosed** in any reviewed source. MIT TR contrasts Therabot with competitors that are "slight variations of Llama," implying but not confirming Therabot is non-Llama. (MIT Technology Review, 2025-03-28; National Elf Service, 2025-04)
- `[inference]` Delivered as a mobile app with an integrated crisis-routing/guardrail layer (see Dimension 5).
- Infrastructure, hosting, model-serving stack, and data pipeline details: **unknown — not found.**

## Dimension 4 — Therapeutic approach, modalities, technique encoding, human-in-the-loop
- `[sourced]` Modality: grounded in evidence-based Cognitive Behavioral Therapy (CBT) and broader psychotherapy best practices. A secondary source (MIT Media Lab event) specifies "third-wave CBT approaches" — slightly more specific but not contradictory. (Dartmouth News, 2025-03-27; NEJM AI, 2025-03-27)
- `[sourced]` Fully generative (not rules/decision-tree). (Dartmouth News, 2025-03-27; NEJM AI title "Generative AI Chatbot")
- `[sourced]` **How technique is encoded (load-bearing):** the team first trained on general mental-health conversations scraped from internet forums (poor results), then on transcripts of real psychotherapy sessions (also unsatisfactory — Jacobson dissatisfied with therapist "hmm-hmms / go ons"), and finally hand-built a custom evidence-based dataset, which is what went into the trial model. (MIT Technology Review, 2025-03-28)
- `[inference]` The hardest, least-reproducible asset is this proprietary expert-curated CBT dialogue dataset — the technique lives in the data, not in a novel architecture. (derived from training history)
- `[unsupported]` "During development, >90% of earlier-version responses aligned with therapeutic best practices." **This figure could NOT be confirmed in any verified source (Dartmouth, NEJM, healio, MIT TR).** Likely from an unverified preprint/abstract. Do not treat as sourced.
- `[sourced]` **Human-in-the-loop:** During the RCT, study staff monitored conversations and intervened on 28 occasions — 15 for safety concerns (e.g., suicidal ideation) and 13 to correct inappropriate Therabot responses. (healio, 2025-04-10)
- `[sourced]` Investigators stress no generative AI agent is ready for autonomous deployment; clinician oversight remains essential. (Dartmouth News, 2025-03-27)

## Dimension 5 — Safety, crisis handling, clinical evidence/trials, FDA/regulatory
**Crisis handling**
- `[sourced]` On detecting high-risk content (e.g., suicidal ideation), Therabot triggers an automated onscreen prompt/button to call 911 or contact a suicide-prevention/crisis hotline. The human study team was equipped to intervene immediately. (Dartmouth News, 2025-03-27)

**Clinical evidence — primary RCT**
- `[sourced]` First-ever RCT of a generative-AI therapy chatbot, published in NEJM AI on 2025-03-27 (Heinz et al., DOI 10.1056/AIoa2400802). The "first-ever" superlative is self-asserted but broadly accepted in coverage; treat date/DOI as solid. (NEJM AI; Dartmouth News, 2025-03-27)
- `[sourced]` Trial NCT06013137, sponsor **Dartmouth-Hitchcock Medical Center**, N=210 (~106 Therabot / ~104 waitlist control); conditions MDD, GAD, clinically-high-risk feeding/eating disorders (CHR-FED). Registry lists conditions generically as "Depression, Anxiety, Eating Disorders." (clinicaltrials.gov NCT06013137; NEJM coverage)
- `[sourced]` Trial dates: start 2024-03-11, overall completion 2024-08-30. **Date precision caution:** primary completion is 2024-05-18 (the 4-week endpoint), distinct from overall completion 2024-08-30. Design = 8 weeks (4 weeks unlimited access + 4 weeks user-initiated). (clinicaltrials.gov NCT06013137; Dartmouth)
- `[sourced]` Results (press-release figures, vs. waitlist control): depression −51%, anxiety −31%, eating-disorder body-image/weight concerns −19%; therapeutic alliance rated comparable to human providers; ~6 hours average engagement (~8 therapy sessions equivalent). (Dartmouth News, 2025-03-27)
- `[contested]` Claim that effect sizes "exceed typical SSRI trials and approach first-line psychotherapy." This is a cross-trial comparison against a **waitlist** control (not head-to-head), which inflates apparent effects. Published NEJM AI letters (DOIs 10.1056/AIp2500390, 10.1056/AIp2500453) and a Lancet commentary flag methodological limits (waitlist control, no independent evaluation, alliance measure misapplied). **Marketing laundered as fact.** (secondary press: Psychology Today, eWeek; NEJM letters; Lancet commentary)

**Follow-on trial**
- `[sourced]` Therabot-CALM (NCT06920238): Phase 1 single-arm trial for anxiety/depression among persons with Cannabis Use Disorder; sponsor **Trustees of Dartmouth College** (note: a different sponsor entity than the RCT); N=15 (estimated); started 2025-04-13; estimated completion Dec 2025; record last updated 2025-09-08. (clinicaltrials.gov NCT06920238)

**FDA / regulatory**
- `[sourced]` No FDA clearance or approval. No regulatory submission found in any source. Investigators explicitly state the tool is not ready for autonomous/unsupervised use; no FDA pathway is implied. (Dartmouth News, 2025-03-27)

## Dimension 6 — Business model / revenue / pricing
- `[sourced]` No revenue, no pricing, no commercial availability — Therabot is a research instrument, not a product. (Dartmouth News, 2025-03-27)
- `[inference]` No spinout company, licensing deal, or commercialization plan was found in any reviewed source as of June 2026 (absence of evidence). Note: absence of a disclosed plan does not rule out future licensing. (absence across reviewed sources)
- Funding model / grant sources (e.g., NIH grants to CTBH): **unknown — not found.**

## Dimension 7 — Founders, key hires, headcount, org shape
- `[sourced]` This is an academic lab, not a startup. **Senior author / PI / lab director:** Nicholas C. Jacobson, PhD — Associate Professor of Biomedical Data Science, Psychiatry, and Computer Science at Dartmouth (Geisel School of Medicine); Director of the AIM HIGH Lab; Director of the Treatment Development and Evaluation Core at the Center for Technology and Behavioral Health (CTBH). (Geisel BMDS, 2025-04-08)
- `[sourced]` **First author / co-creator:** Michael V. Heinz, MD — Assistant Professor of Psychiatry at Geisel/CTBH and attending psychiatrist at Dartmouth Hitchcock Medical Center. (Dartmouth News, 2025-03-27)
- `[sourced]` **Named RCT co-authors:** Daniel M. Mackin, Brianna M. Trudeau, Sukanya Bhattacharya, Yinzhou Wang, Haley A. Banta, Abi D. Jewett, Abigail J. Salzhauer, Tess Z. Griffin. (Health AI Partnership, 2025)
- `[sourced]` Developed over six years by a team described as **100+ people contributing 100,000+ human hours.** **Lightly sourced caution:** this figure traces to secondary press / an MIT Media Lab event blurb, NOT the primary Dartmouth release; treat as marketing-origin and cumulative (including dialogue-writing experts), not a current standing org chart. (MIT Media Lab event description; secondary aggregation, 2025)
- `[inference]` The active core team is small — the ~10 named authors plus consulting Dartmouth/Dartmouth Health clinicians — not a 100-person standing org. (derived from author list + cumulative nature of the 100+ figure)

## Dimension 8 — Compensation bands
- `[sourced]` Faculty PI compensation (Jacobson, Heinz) is **not available** in public sources; US tenure-track faculty are generally not on H1B visas, so LCA data does not capture them. (h1bdata.info, DARTMOUTH COLLEGE)
- `[inference]` **H1B LCA bands for Dartmouth College (Hanover/Lebanon NH, 2018–2022) — institution-wide role data, NOT Therabot-team pay:** Research Scientist ~$53K–$77K (cluster ~$55K–$65K); Senior Research Scientist ~$66K; Software Engineer (Hanover) ~$96K–$111K; Senior Research Software Engineer ~$98K; Research Engineer ~$58K; Postdoctoral Fellow ~$54K–$58K; Research Assistant Professor ~$77K; Research Associate B ~$46K–$79K. Dartmouth-wide H1B median ~$64K. (h1bdata.info, 2018–2022 filings)
- `[inference]` These academic bands run far below industry AI/ML compensation — a sound directional inference consistent with a university research lab, but it is a **proxy**, not a measurement of actual Therabot-team pay. (h1bdata.info)

## Dimension 9 — Funding history / investors / valuation
- **unknown — not found.** `[inference]` As an academic project, Therabot has no venture funding, investors, or valuation; any support is institutional/grant-based (CTBH/Dartmouth/NIH likely, but no specific grant numbers or amounts were researched). No disclosed raise.

## Dimension 10 — Traction / users / growth
- `[sourced]` The only quantified usage is trial engagement: ~106 participants in the Therabot arm of the RCT, ~6 hours average engagement each (~8 therapy-session equivalents). (Dartmouth News, 2025-03-27)
- Production user counts, retention, DAU/MAU, or waitlists: **unknown — not found** (no commercial deployment exists). `[inference]`

## Dimension 11 — Risks / controversies / red flags
- `[contested]` **Methodology critique:** The headline efficacy figures rest on a waitlist control with no head-to-head comparison and no independent evaluation; NEJM AI letters and a Lancet commentary contest the alliance-measure application and the SSRI/psychotherapy comparisons. (NEJM letters; Lancet commentary)
- `[unsupported]` The widely-quoted ">90% best-practice alignment" development figure is unverifiable in primary sources — a citation red flag.
- `[sourced]` Safety incidents during the trial: 28 staff interventions (15 safety, 13 to correct inappropriate bot responses), underscoring that autonomous deployment is not yet safe per the investigators. (healio, 2025-04-10; Dartmouth News, 2025-03-27)
- `[inference]` **Conflated-entity risk:** Dartmouth's separate "Evergreen" AI well-being tool (Oct 2025) is frequently at risk of being mistaken for Therabot; it is distinct.
- `[inference]` Reproducibility risk: the proprietary, undisclosed curated dataset and undisclosed base model limit external replication.

## Dimension 12 — Strategic outlook / what to watch
- `[sourced]` Near-term watch item: Therabot-CALM (NCT06920238) Phase 1 results, estimated completion Dec 2025. (clinicaltrials.gov NCT06920238)
- `[inference]` Key open questions: whether Dartmouth pursues a spinout/licensing path or an FDA SaMD pathway (none disclosed as of June 2026); whether a head-to-head (vs. active control) trial addresses the contested efficacy critiques.
- `[speculation]` Given the lab's first-mover RCT and academic positioning, the more likely trajectory is continued grant-funded research and norm-setting influence on regulators rather than near-term commercialization — but this is speculative absent any disclosed plan.

---

## Stated vs. real motivations
- **Stated motivation** `[sourced]`: Close the mental-health supply-demand gap with a scalable, on-demand, evidence-based (CBT-grounded) generative-AI tool — framed as a research mission to rigorously test safety and efficacy *before* anyone deploys generative-AI therapy. (Dartmouth News, 2025-03-27)
- **Real motivation (confidence: medium)** `[inference]`: Genuinely research/mission-driven rather than commercial — a university lab with academic-band pay, no spinout, no FDA filing, and no product. The deeper driver appears to be **establishing scientific priority and credibility**: being first to run an RCT of generative-AI therapy (a field-defining NEJM AI result) positions Jacobson's lab as the authoritative voice on safe clinical deployment, which attracts grant funding and shapes regulatory/clinical norms. Confidence moderate — no evidence of commercial intent was found, but absence of a disclosed commercialization plan does not rule out future licensing. `[inference]`

## Engineering difficulty (4/5)
`[inference]` Building a **fully-generative** (not scripted) LLM therapist that performed safely enough to clear an IRB-approved RCT is genuinely hard. The team abandoned two training-data strategies (forum scraping, real session transcripts) and hand-built an expert-curated CBT dialogue dataset over six years and a reported 100,000+ human hours. Encoding therapeutic technique into a generative model while constraining harmful outputs (suicidal-ideation detection, crisis routing, clinician oversight) is a substantial alignment/data-engineering effort.

**Not a 5** because the underlying tech is fine-tuning an existing foundation model + a guardrail/crisis-routing layer + a standard mobile app — the novelty is in the curated data and clinical validation, not novel ML architecture. **The hardest, least-reproducible asset is the proprietary expert-curated dataset.**

---

## Sources
- https://home.dartmouth.edu/news/2025/03/first-therapy-chatbot-trial-yields-mental-health-benefits
- https://www.technologyreview.com/2025/03/28/1114001/the-first-trial-of-generative-ai-therapy-shows-it-might-help-with-depression/
- https://www.nationalelfservice.net/treatment/digital-health/genai-chatbots-can-treat-clinical-level-mental-health-symptoms/
- https://www.healio.com/news/psychiatry/20250410/generative-ai-chatbot-promising-for-mental-health-treatment-but-supervision-needed
- https://ai.nejm.org/doi/full/10.1056/AIoa2400802
- https://clinicaltrials.gov/study/NCT06013137
- https://clinicaltrials.gov/study/NCT06920238
- https://geiselmed.dartmouth.edu/bmds/2025/04/08/dr-nicholas-jacobson-leads-team-to-develop-dartmouths-therabot/
- https://healthaipartnership.org/insight/therabot-the-first-randomized-controlled-trial-of-a-generative-ai-for-psychotherapy
- https://h1bdata.info/index.php?em=DARTMOUTH+COLLEGE
