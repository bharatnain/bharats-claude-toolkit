# Lyra Health — Company Dossier

**One-line:** Lyra Health, a ~$5.6B B2B mental-health benefits platform, launched "Lyra AI" — a deliberately scope-limited generative-AI coaching guide for mild-to-moderate issues, wrapped in human-escalation guardrails — atop a mainstream AWS/Snowflake stack. The hard engineering lives in safety/crisis-triage, compliance, and clinical validation, not model R&D.

**Overall verifier confidence:** high

**Note on labels:** Each claim below carries the verifier's label — `[sourced]`, `[inference]`, `[speculation]`, `[contested]`, or `[unsupported]`. Where a fact was not found, it is written "unknown — not found." Several verifier flags (misattribution, date errors, marketing-as-fact, entity conflation) are surfaced inline.

---

## Dimension 1 — Company Journey & Milestones

- `[sourced]` Founded **2015** in Burlingame, CA by **David Ebersman** (ex-CFO of Facebook/Meta and Genentech) and **Dr. Dena Bravata** (ex-CMO of Castlight Health; Lyra's first CMO, 2015–2016). The exact "Oct 14, 2015" day rests on a secondary brand blog and is weakly sourced; the **2015 year is solid**.
- `[sourced]` Ebersman founded Lyra after a roughly year-long personal struggle to find quality mental-health care for a close family member.
- `[sourced]` **Aug 25, 2020** — became a unicorn ($1.1B) via Series D.
- `[sourced]` **2022** — Series F at ~$5.58–5.85B valuation, paired with the **ICAS World** acquisition for international expansion; reached **20M+ members** globally.
- `[sourced]` **Jan 13, 2025** — leadership transition: **Jennifer Schulz** (ex-CEO of Experian North America) became CEO; Ebersman moved to **Chairman**, citing his family grieving the death of one of his sons (self-reported, sensitive).
- `[sourced]` **Oct 14, 2025** — launched **"Lyra AI"** as a pilot for select US Lyra Coaching customers.
- `[sourced]` **May 5, 2026** — scaling the AI Guide to general availability (US + additional countries, text and voice modes) through end of 2026.
- `[unsupported]` Lyra's positioning that it is the **"largest company to embed generative AI into ongoing therapy treatment"** is a marketing superlative repeated by STAT with no cited methodology or comparative basis.

---

## Dimension 2 — Tech Stack & Architecture

- `[sourced]` Core data architecture: **Snowflake** data lake/warehouse, **Fivetran** Managed Data Lake for ingestion, with **PHI isolated in a VPC** for HIPAA compliance (Iceberg/Delta table formats confirmed). **Caveat:** this rests on a Fivetran customer case-study blog — vendor marketing co-produced with the customer — so the self-congratulatory framing should be treated skeptically; the core tech names are nonetheless confirmed in that source.
- `[inference]` Broader analytics/MLOps stack — **dbt, Airflow, Tableau/Sigma, MLflow, Kubeflow, AWS SageMaker; ML frameworks PyTorch / scikit-learn / XGBoost; Python and Java** — appears in **job-posting requirements**. These signal desired skills, not verified production architecture. (Findings originally labeled this "sourced"; verifier **downgraded to inference**.)
- `[sourced]` Production ML runs on **AWS via Kubernetes**.
- `[sourced/inference]` Product surface organized under one platform, **"Lyra Empower,"** with sub-products: **Lyra AI** (member-facing AI Guide chatbot, text + voice), **Lyra Engage** (provider session/episode summarization), **Lyra Connect** (HR org-level analytics). Architecture is a **hybrid** of classic ML (provider-matching engine over "millions of data points"; outcome-prediction models) and newer generative/LLM components (conversational guide, clinical documentation).

---

## Dimension 3 — AI/ML Techniques & Models

- `[sourced]` **The specific foundation model behind Lyra AI is NOT publicly disclosed** in any located source. Lyra never names OpenAI, Anthropic, or a proprietary in-house LLM. STAT explicitly does not name it. This is a genuine disclosure **gap**, correctly flagged.
- `[contested]` Lyra **"began developing its own offering last year"** in response to members using ChatGPT for mental health. **Entity-conflation flag:** the raw findings (D3) attributed this to "CEO Jenny Gonsalves." Gonsalves is **Chief Product & Technology Officer (CPTO)**, not CEO — the CEO is Jennifer Schulz. The substance (the quote on developing its own offering) is sourced to STAT; the title is wrong and contradicts D1/D7 of the same findings.
- `[inference/speculation]` Lyra **most likely wraps one or more third-party frontier LLMs with a RAG/orchestration + guardrail + risk-classification layer** rather than pretraining its own base model — consistent with its job-posting stack ("experience with LLMs and building infrastructure to support LLM applications") and company stage. Plausible but **unconfirmed**; Lyra discloses nothing about its model approach.
- `[sourced]` Disclosed techniques: (1) conversational **"Guide"** deliberately scoped to mild-to-moderate issues (burnout, sleep, stress) as a safety guardrail; (2) a **"sophisticated risk-flagging system"** / safety classifier that triggers escalation to a live 24/7 human care team with provider monitoring; (3) training/grounding on Lyra's proprietary clinical data "tied to proven clinical outcomes" (the Lyra Care model); (4) "clinical guardrails, rigorous testing, active monitoring" + the published **Polaris Principles**; (5) NLP-based provider matching and LLM-generated session/episode summaries; (6) multilingual/global rollout and "Culturally Responsive Care."
- `[speculation]` The claim that the **"20M+ members, decade of data" is the core moat as a training corpus** is an analyst inference that conflates total member reach with a clean, labeled, usable clinical-outcomes training set. **No source establishes** that 20M members' data is used (or usable) as AI training data. Lyra's own statement is only the marketing line "trained on high-quality data linked to proven clinical outcomes," with no disclosed methodology.
- `[sourced]` **Not disclosed:** fine-tuning vs. RAG split, RLHF, eval benchmarks/metrics, vector DB, or named guardrail models — all genuine gaps.
- `[sourced]` Scale (mid-2026): **20M+ direct members, 100M+ via health-plan partnerships** (Lyra's own self-reported, not independently audited figures).

---

## Dimension 4 — Therapeutic Approach, Modalities, Technique Encoding & Human-in-the-Loop

- `[sourced]` **Modalities are a notable disclosure gap.** Lyra does **not** publicly name specific therapeutic modalities (no CBT, ACT, behavioral activation, etc.) for the AI guide. Technique is described abstractly: the guide helps members "apply mental health skills" between sessions, trained on "high-quality data linked to proven clinical outcomes," with "decades of evidence-based training [that] shape how Lyra AI responds, guiding members towards more helpful choices… and not validating harmful ones."
- `[inference]` It **appears to be a generative LLM with clinical guardrails/training** rather than a scripted decision-tree (à la first-gen Woebot), but Lyra does not confirm the mechanism (rules vs. generative, protocol structure, curated-vs-free generation). **How technique is encoded is largely a black box.** Confidence: LOW.
- `[sourced]` **Scope** is deliberately limited to "mild and moderate challenges like burnout, sleep, and stress"; higher-risk conditions are meant to be screened out and routed to humans.
- `[sourced]` **Human-in-the-loop is strongly emphasized** (confidence: HIGH): positioned to "supplement human-led care between coaching sessions" and "enhance, not replace" clinicians; human providers remain "the foundation of care." Features: live human provider monitoring; provider insights generated "in coordination with care supervisors"; member transparency (AI "clearly identified"); easy opt-out.

---

## Dimension 5 — Safety, Crisis Handling, Clinical Evidence & FDA/Regulatory Status

**Safety & crisis handling**
- `[sourced]` Core marketed feature: a **"sophisticated risk-flagging system that identifies situations requiring immediate escalation,"** with "clear pathways to quickly connect a member with a live representative from Lyra's 24/7 care team." "AI interactions are monitored, with clear protocols for looping in a human provider if risks or other concerns arise." **This describes a MARKETED feature; the technical crisis/suicide-risk protocols are not disclosed and not independently verified.** Confidence: MEDIUM.
- `[sourced]` Governance framework = the **Polaris Principles** (published Oct 2025): (I) Safety is paramount; (II) Human providers are critical; (III) Culturally responsive care is key to global reach; (IV) Innovation driven by science. This is Lyra's **self-authored** framework, not an external standard.
- `[sourced]` Security/compliance: **HIPAA-compliant, HITRUST certified, ISO 27001 certified.**

**Clinical evidence / trials**
- `[sourced]` **No published clinical trial, RCT, or peer-reviewed study of the Lyra AI guide itself was found.** The Oct 2025 pilot is called "successful" with no published results. Confidence: LOW/absent.
- `[contested]` Cited clinical evidence — "23 peer-reviewed studies," "recover twice as fast," "26% annual reduction in health-care claims costs," "9 in 10 members improve," "95% stay with first AI-recommended provider" — pertains to **Lyra's broader human-care model, not the AI guide.** **Misattribution flag:** "23 studies," "recover twice as fast," and "26% reduction" are verified in the Oct 14 2025 announcement, but **"9 in 10 improve" and "95% stay with first provider" do NOT appear there** — they come from Lyra careers/FAQ/ROI pages (and "95%" appears elsewhere as "96%").
- `[contested]` Lyra's peer-reviewed **Value in Health study (Aug 12, 2025)** — ~20% per-episode cost cut, ~$340/member — is real, but it evaluates Lyra's **AI provider-matching algorithm, NOT the generative Lyra AI Guide chatbot.** **Conflation risk:** presenting it near AI-Guide claims wrongly implies the chatbot has published cost/outcome evidence, which it does not.

**FDA / regulatory (key finding)**
- `[sourced]` **Lyra AI is NOT FDA-cleared or FDA-approved, and Lyra makes no FDA claim.** It operates outside FDA device regulation. FDA has authorized 1,200+ AI devices but **none for mental health**, and no GenAI device for any clinical purpose. Confidence: HIGH.
- `[inference]` Generative-AI products that **treat/diagnose** a psychiatric condition or substitute for a provider would fall under FDA purview; Lyra's narrow "mild/moderate, supplement-not-treat, human-in-loop" framing appears designed to **stay below that threshold** — an analyst reading of Lyra's motive, not an FDA finding about Lyra.
- `[contested]` The **FDA Digital Health Advisory Committee** met to weigh regulating generative-AI therapy chatbots; **no rule issued**, framework still developing as of mid-2026. **Date-error flag:** the meeting was **Nov 6, 2025** (Thursday), not Nov 5 — the STAT article is dated Nov 5 and describes the meeting happening the next day. The raw findings repeat "Nov 5" twice.
- `[contested]` External skepticism is significant but context-only, not findings against Lyra: the **APA** warns against general-purpose chatbots; lawsuits allege harm from other AI tools; **Illinois's WOPR Act** (signed Aug 4, 2025). **Regulatory-overstatement flag:** "Illinois banned AI therapy" overstates the WOPR Act, which bars AI from making **independent** therapeutic decisions or posing as a licensed therapist while **permitting** administrative/supplementary uses — not a blanket ban.

---

## Dimension 6 — Engineering Difficulty

### Engineering difficulty (3/5)

- `[sourced/inference]` The **core LLM application pattern** — wrap a frontier model with RAG, scope-limiting, a risk classifier, and human-escalation routing — is **well-trodden 2025/2026 engineering, not novel research**; the underlying data stack (AWS, Snowflake, Fivetran, Kubernetes, standard MLOps) is mainstream. This **caps it below 4**.
- It rises **above a 2** because: (a) the safety-critical **real-time risk-detection/escalation classifier** for mental-health crises has very low tolerance for false negatives and must integrate with a live 24/7 human care team — hard to get right and validate; (b) **HIPAA/PHI handling, VPC isolation, and multi-country data-residency** add substantial compliance-engineering burden; (c) **multilingual + voice mode + culturally-responsive behavior** across additional countries multiplies eval/guardrail surface area; (d) **clinical validation, active monitoring, and the proprietary-outcomes data pipeline** are nontrivial.
- **The difficulty is concentrated in safety, evaluation, and compliance integration rather than core model R&D.** Lyra deliberately narrowed scope to avoid the hardest problem (autonomous treatment of high-acuity/diagnosable conditions).
- **Confidence is limited** by non-disclosure of the model and eval specifics, **which could move this to a 4** if Lyra is doing meaningful fine-tuning or custom safety modeling.

---

## Dimension 7 — Founders, Key Hires, Headcount & Org Shape

- `[sourced]` **Founders:** David Ebersman (ex-CFO Facebook/Genentech) and Dena Bravata, MD (ex-CMO Castlight; Lyra CMO 2015–2016). **Bob Kocher, MD** (Venrock) is credited as a co-founder and remains a Board Member; Venrock's Bryan Roberts was an early co-investor/board figure.
- `[sourced]` **CEO transition:** Ebersman → Chairman effective **Jan 13, 2025**; **Jennifer Schulz** (ex-CEO Experian North America, ~$4.5B / ~8,000-employee unit) became CEO and joined the board — a classic founder-to-professional-operator handoff toward an eventual IPO.
- `[sourced]` **Current C-suite (lyrahealth.com/about, June 2026):** Jennifer Schulz (CEO); **Sandra Beaver** (CFO, joined June 2025 from Evolus, ex-SVP Finance at Experian — a Schulz hire); Lisa Caccavo (GC); **Jenny Gonsalves** (Chief Product & Technology Officer — top tech exec; AI/data leadership reports to her); Andrew Davies (President, Lyra International); Sean McBride (President, Employer Solutions); Monika Roots, MD (President, Health Plans & Systems); Suzanne Fauvre-Willis (Chief Clinical Operations Officer).
- `[sourced]` **Clinical leadership is MD/PhD-heavy** (reflects clinical-grade positioning): Alethea Varra, PhD (Chief Clinical Officer); Bob Kocher, MD (co-founder/board); **Anita Lungu, PhD (VP, Clinical Product & Research — key bridge between clinical science and the AI product)**; plus VPs/directors for pediatric, clinical quality, adult outpatient, neurobehavioral, and high-acuity care.
- `[inference]` **Connie Chen, MD** (formerly COO & CMO) is **absent from the current leadership page**, suggesting a departure or role change.
- `[sourced]` **AI/technical hiring:** As of mid-2026 there is an **OPEN req for "VP of Data and AI"** (reports to CPTO; posted base **$251K–$346K**) to build Data Engineering, Data Science, AI Platform and AI/ML Engineering teams — i.e., the senior AI org is **still being assembled**. Also hiring Senior ML Engineers. **No dedicated Chief AI Officer title.**
- `[sourced]` **Headcount:** ~**2,859** as of May 31, 2026 (Revelio Labs); ~2,973 Dec 2025; 2,761 in 2025 (+3.8% YoY) — growth flattened to low single digits, consistent with a late-stage company optimizing rather than blitz-scaling. **Caveat:** third-party estimators vary materially (PitchBook ~2,658; LeadIQ ~2.8K).
- `[inference]` A **large share of headcount is the clinical provider network** (therapists/coaches), not corporate/engineering staff — typical for this model.

---

## Dimension 8 — Compensation Bands

*Caveat: Lyra is private (no public equity value); levels.fyi/Glassdoor totals include estimated illiquid stock/bonus and small sample sizes; H1B/LCA = base only.*

**Software Engineer (US)**
- `[sourced — levels.fyi, June 23 2026]` Median total comp **~$222K–$225K**; range ~$150K–$270K+ (base+stock+bonus). Senior SWE ~$220K TC. Software Engineering Manager ~$235K TC median.
- `[sourced — H1B/LCA, base only]` Senior Software Engineer – Backend **$179,000** (2023, 1 record).
- `[sourced — Glassdoor estimate]` Senior SWE avg base ~$141K; total ~$130K–$176K (lower than levels.fyi; model estimate, not verified pay).

**Data**
- `[sourced — H1B/LCA]` Senior Data Scientist **$160,000** base (2024). `[sourced — levels.fyi]` Data Analyst ~$132K TC.

**Product / Design**
- `[sourced — levels.fyi]` Product Designer ~$159K TC. `[sourced — Glassdoor estimate]` Senior PM up to ~$164K. `[sourced — Lyra posting/LCA-grade]` VP Data & AI base **$251K–$346K**.

**Business/Ops**
- `[sourced — levels.fyi]` Business Operations ~$251K TC (high end), Business Ops Manager ~$151K, Business Analyst ~$173K.
- `[sourced — H1B/LCA]` Growth Strategy & Ops Senior Manager $159,328 (2025); Staff Salesforce Developer $153,317 (2025).

**Overall H1B/LCA**
- `[sourced]` ~29 records, median ~$167,731; FY2025 median ~$195,700; ~7% >$200K, 66% $150–200K, 28% $100–150K. FY2025 had only ~2–3 filings — **Lyra is a light H1B sponsor** with thin visa data.
- `[inference]` Engineering pay (~$220K+ median TC) is **competitive but below FAANG** — market-but-not-top-of-market with private/illiquid equity. Glassdoor comp/benefits rating 3.2/5.

---

## Dimension 9 — Funding & AI Investment

- `[sourced]` **Total raised ~$910–915M across ~9 rounds.** Investors: Addition, Greylock, IVP, Coatue, Dragoneer, Salesforce Ventures, Durable, Fidelity, Baillie Gifford, plus angels incl. Howard Schultz.
  - Series C: **$75M**, early 2020, led by IVP.
  - Series D: **$110M**, Aug 25 2020, led by Addition — **$1.1B** post-money (unicorn).
  - Series E: **$187M**, Jan 28 2021, led by Addition — **$2.3B** post-money.
  - Series F: **$235M**, Jan 19 2022, led by Dragoneer (with Salesforce Ventures + Coatue) — **~$5.58–5.85B** valuation, paired with the **ICAS World** acquisition. ($5.58B in the body/PR; $5.85B in a Fierce headline variant.)
- `[inference]` **No new priced round publicly reported since the Jan 2022 Series F**; the AI buildout is funded **internally from existing capital, not a dedicated raise.** This is an argument from silence — a private round could exist unreported.
- `[sourced]` **AI investment:** Lyra AI launched Oct 14, 2025 as a pilot, scaling to general availability (US + more countries, text + voice) through end of 2026. The AI launch is **not itself a separately-funded round** — it is product investment.

---

## Dimension 10 — Business Model & Business Drivers

- `[sourced]` **Model:** B2B (enterprise) mental-health benefits. Employers buy benefits (therapy, coaching, EAP); employees get a set number of free sessions/year (commonly ~16). Lyra runs a curated, outcomes-tracked provider network plus in-house clinicians and digital tools. **Clients:** Meta, Starbucks, Morgan Stanley, Uber, Lululemon, Zoom, eBay, Pinterest, Genentech — **300+ employers, 20M+ members.**
- `[sourced]` **Sector-wide AI drivers:** therapist demand outstrips supply; chatbots are cheaper and always-available ("fast, private, there at 3 a.m."); competitors (Talkspace, Headspace, SonderMind) view AI as too advantageous to ignore.
- **Business drivers (analyst synthesis):** (1) **Supply/demand** — AI extends capacity without adding clinicians; (2) **consumer behavior** — people already use ChatGPT-style bots as de-facto therapists, and Lyra wants to capture/retain that demand inside its walled platform; (3) **unit economics** — AI is far cheaper per interaction, improving margins; (4) **competitive necessity**; (5) **engagement/retention** — keeps members in-platform between sessions, deepening employer-contract stickiness.

---

## Dimension 11 — Stated vs. Real Motivations

### Stated vs. real motivations

**Stated motivation** `[sourced]`
Lyra frames the AI as a **clinical access/quality play**: it "opens up a new path to care" for people held back by shame or stigma, provides 24/7 support between human sessions, and meets members "where they are" — built with clinical training and guardrails so it **supplements (never replaces)** human providers. Executives (CEO Jennifer Schulz, Chief Clinical Officer Alethea Varra) emphasize care innovation, safety, and outcomes.

**Real motivation** `[speculation — most heavily caveated; unfalsifiable, unsourced to any Lyra statement]`
A **defensive, margin- and engagement-driven competitive move**. Members already use free consumer chatbots (ChatGPT) as therapists; Lyra is building its own to keep that demand inside its platform. AI's far-lower per-interaction cost lets Lyra absorb the therapist supply/demand imbalance, serve more members between (or instead of) expensive human sessions (**margin expansion**), and stay competitive with Talkspace/Headspace/SonderMind. As a post-Series-F company at a **$5.6B+ valuation with no new raise reported**, AI is also a **growth/efficiency lever to defend that valuation** and improve the path to durable profitability.

**Regulatory-cover angle** `[speculation]`
The "clinical-grade"/safety framing is **partly genuine and partly differentiation/regulatory cover**, given **California AB 489** (signed Oct 13, 2025; effective Jan 1, 2026) barring AI from implying it is a licensed provider (with SB 243 for companion bots). The raw findings loosely say "California's ban"; the precise vehicle is **AB 489**. The "regulatory cover" motive is speculation about intent.

**Marketing-laundered-as-fact (verifier flags):**
- `[unsupported]` **"First clinical-grade AI for mental health"** is Lyra's own press-release headline. "Clinical-grade" has no regulatory or industry-standard definition; no independent body validated the "first" claim. Pure marketing positioning.
- `[unsupported]` **"Largest company to embed generative AI into ongoing therapy treatment"** originates from Lyra's positioning, repeated by STAT, with no cited methodology.

---

## Dimension 12 — Notes, Gaps & Open Questions

**Genuine disclosure gaps (facts not found):**
- **Underlying foundation model / LLM vendor** — unknown — not found (Lyra discloses nothing).
- **Fine-tuning vs. RAG split, RLHF, eval benchmarks/metrics, vector DB, named guardrail/safety models** — unknown — not found.
- **Technical crisis/suicide-risk escalation protocols** (how flagging works) — unknown — not found; described only at a high level.
- **Therapeutic modalities encoded in the AI** (CBT/ACT/etc.) — unknown — not found; described abstractly.
- **Published clinical trial/RCT of the Lyra AI Guide chatbot** — unknown — not found (none exists; the Aug 2025 Value-in-Health study covers the **provider-matching algorithm**, not the chatbot).

**Cross-cutting verifier flags to carry forward:**
- **Entity conflation:** "Jenny Gonsalves" is **CPTO**, not CEO (CEO = Jennifer Schulz). Internal contradiction within the raw findings.
- **Misattribution:** "9 in 10 improve" / "95% stay with first AI-recommended provider" are broader-care-model stats from careers/FAQ/ROI pages, **not** the Oct 14 2025 AI announcement; "95%" also appears as "96%."
- **Conflation risk:** the cost-reduction study evaluates the matching algorithm, **not** the chatbot.
- **Date error:** FDA Digital Health Advisory Committee met **Nov 6, 2025**, not Nov 5.
- **Regulatory overstatement:** "Illinois banned AI therapy" overstates the WOPR Act.
- **Vendor-marketing source:** the D2 data-stack confirmation rests on a Fivetran co-produced case study; analytics-stack specifics beyond Snowflake/Fivetran/VPC are inferred from job postings, not confirmed production architecture.
- **Date labeling:** several "2026-06-24" source dates are **access dates**, not publication dates.
- **Unverified moat:** "20M+ members, decade of data = training corpus" conflates total reach with a usable labeled training set; unverified.

---

## Sources

- https://www.lyrahealth.com/announcement/lyra-health-introduces-first-clinical-grade-ai-for-mental-health/
- https://www.lyrahealth.com/blog/introducing-lyra-ai/
- https://www.lyrahealth.com/blog/the-polaris-principles/
- https://www.lyrahealth.com/our-approach/ai/
- https://www.lyrahealth.com/platform/empower/
- https://www.lyrahealth.com/announcement/lyra-health-scales-clinically-vetted-ai-guide-to-members-globally/
- https://www.lyrahealth.com/announcement/lyra-health-study-finds-ai-can-reduce-mental-health-care-costs-without-sacrificing-outcomes/
- https://www.lyrahealth.com/announcement/lyra-health-dec-5-2024/
- https://www.lyrahealth.com/about/
- https://www.businesswire.com/news/home/20251014882130/en/Lyra-Health-Introduces-First-Clinical-Grade-AI-for-Mental-Health
- https://www.businesswire.com/news/home/20260505129157/en/Lyra-Health-Scales-Clinically-Vetted-AI-Guide-to-Members-Globally
- https://www.businesswire.com/news/home/20241205930293/en/Lyra-Health-Welcomes-Jennifer-Schulz-as-Chief-Executive-Officer
- https://www.statnews.com/2025/10/14/lyra-health-ai-chatbot-mental-health/
- https://www.statnews.com/2025/11/05/fda-digital-advisers-therapy-chatbots-regulating-generative-ai/
- https://www.statnews.com/2025/12/01/ai-chatbot-headspace-talkspace-lyra-sondermind-digital-mental-health/
- https://www.emarketer.com/content/lyra-debuts-ai-therapy-chatbot-lower-risk-mental-health-conditions
- https://www.fivetran.com/blog/lyra-health-leads-mental-health-innovation-with-data-lakes-ai
- https://careers.lyrahealth.com/category/data-science-and-machine-learning-jobs/43250/8603904/1
- https://jobs.lever.co/lyrahealth/09c26902-b358-4a8c-8ea1-6cf6d7867b37
- https://www.fda.gov/media/189391/download
- https://thebrandhopper.com/featured-startups/lyra-health-history-founders-business-model-funding/
- https://research.contrary.com/company/lyra
- https://news.crunchbase.com/startups/lyra-health-gains-unicorn-status-after-110m-series-d/
- https://news.crunchbase.com/health-wellness-biotech/lyra-health-funding-valuation-series-e/
- https://www.fiercehealthcare.com/digital-health/lyra-health-gets-235m-soars-to-5-85b-valuation-new-acquisition-for-global-expansion
- https://tracxn.com/d/companies/lyra-health/__qLc5Ab2l9Bwe93bvCdLQSqy1XP210Bg1OWHCM9m512s/funding-and-investors
- https://en.wikipedia.org/wiki/David_Ebersman
- https://www.reveliolabs.com/companies/lyra-health/employees/
- https://www.levels.fyi/companies/lyra-health/salaries
- https://h1bdata.info/index.php?em=lyra+health+inc
- https://h1bgrader.com/h1b-sponsors/lyra-health-inc-nokpzn7n04
- https://www.glassdoor.com/Salary/Lyra-Health-Salaries-E1483303.htm
- https://www.medscape.com/viewarticle/california-bans-ai-chatbots-posing-licensed-health-providers-2025a1000tpj
