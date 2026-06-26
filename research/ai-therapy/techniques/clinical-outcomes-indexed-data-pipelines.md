# Clinical & outcomes-indexed data pipelines

*State of the art, June 2026. Written for a sharp reader who will fund, steer, hire, and judge this work — but won't write the code.*

How to read the labels in this chapter:
- **(sourced)** — a factual claim backed by a cited source (see Sources), current as of the date noted.
- **(inference)** — my reasoning from the sourced facts, not itself directly stated by a source.
- **(speculation)** — a forward guess, lower confidence.
- **(advisory)** — a learning-design, hiring, or org recommendation. This is reasoned editorial judgment, not a sourced fact.

---

## 1. What it is

Healthcare data is **born messy and born for billing, not for science.** A hospital's electronic health record (EHR) notes that a patient got billing code 99214 (an office visit) on a Tuesday — not "this patient's diabetes is getting worse." The diagnosis lives as a code attached to a claim; the actual clinical reality often lives in a paragraph a nurse typed at 2 a.m.

Three problems make this raw exhaust unusable as-is:

1. **Different dialects.** Hospital A encodes a sodium lab one way; Hospital B another; a claims database a third. Same biology, three encodings. (inference, illustrative)
2. **No native concept of "outcome."** The data records *events* — a code fired on a date. It does not record that those events *mean* "the patient had a stroke." Someone has to define that. (inference)
3. **No native concept of "the patient."** A person is #4471 at one health system and #88210 at another, with no shared key. Their journey is shattered across sources. (inference)

A **clinical and outcomes-indexed data pipeline** is the industrial machine that solves all three. It **harmonizes** the dialects into one standard schema, **defines and computes outcomes** as reproducible logic, and **links** the shattered patient back together across sources — all while keeping a paper trail good enough for a regulator.

"Outcomes-indexed" is the load-bearing phrase. The whole apparatus exists so you can ask *"of the people who took drug X, how many had outcome Y, and when?"* — and trust the answer enough to put it in front of the FDA.

The dominant standard schema is **OMOP CDM** (the Observational Medical Outcomes Partnership Common Data Model), stewarded by the open OHDSI community. As of 2026 the OHDSI network connects 500+ databases representing on the order of **~1 billion patient records** across dozens of countries (sourced, Book of OHDSI). The de-facto production standard is **OMOP CDM v5.x** (most deployments run v5.3/v5.4); note that a v6.0 was released back in 2023 but saw very low adoption, so the community continues to iterate on the v5.x line rather than v5.4 being the newest version that exists (sourced/clarified per verifier, Lifebit 2026). The other standard you'll hear is **FHIR** — the format hospitals use to *move* data in real time. A common modern pattern: data arrives as FHIR, then gets transformed into OMOP for analysis (sourced, Frontiers/TermX 2026).

---

## 2. How it works

Think of it as five stages, each one solving one of the messes above.

**Stage 1 — Ingest and land (the "bronze" layer).** Raw extracts land untouched: claims files, EHR dumps, lab feeds, flat CSVs. The discipline here is *don't transform yet* — keep a pristine copy so any later mistake can be traced back. Modern stacks (2025–26) increasingly use the same tooling as the rest of the data world: a cloud warehouse (Snowflake/Databricks/BigQuery) plus **dbt** to manage transformations as version-controlled SQL (sourced, Tuva/dbt-for-healthcare).

**Stage 2 — Map the vocabularies (the hardest, least glamorous part).** This is the "different dialects" problem. Every source code — ICD-10, CPT, NDC drug codes, LOINC lab codes, local codes — must be mapped to one canonical concept. OHDSI maintains a giant **standardized vocabulary** that says, e.g., "this local lab code and that LOINC code both mean *serum sodium*." The mechanism is a lookup-and-translate step: each source code is joined against the vocabulary's mapping tables, which collapse synonyms into a single "standard concept ID." This is where most human labor goes, because mappings are never fully clean — a 2026 study formalizing FHIR→OMOP rules for just vital signs hit only ~74% automatic mapping coverage, with the rest needing human judgment (sourced, Frontiers/TermX 2026).

**Stage 3 — Transform into the model (the OMOP "ETL").** Now reshape the data so the *person* is the spine. OMOP has a fixed set of tables — `PERSON`, `CONDITION_OCCURRENCE`, `DRUG_EXPOSURE`, `MEASUREMENT`, `VISIT_OCCURRENCE`, and so on. The ETL ("extract-transform-load") fans the source rows into these tables, each row now carrying a standard concept ID (from Stage 2), a patient ID, and a date. After this stage, **any** OMOP database in the world can be queried with the same code — which is the entire point of a common model.

**Stage 4 — Define and compute the outcome (this is "outcomes-indexed").** Here's the crux. An outcome like "acute myocardial infarction" is not a field in the data — it's a **definition you author**, called a **computable phenotype**: a precise, executable rule like *"≥1 inpatient diagnosis of MI **OR** (1 outpatient MI diagnosis **AND** a troponin lab above threshold within 7 days), excluding history-of codes."* The mechanism: the phenotype is logic that scans the harmonized tables and stamps each qualifying patient with an outcome **and the date it occurred.** That date is the "index" — it lets you place the outcome on the patient's timeline relative to a drug exposure, which is what makes causal-style questions ("did the drug precede the event?") answerable. The 2026 frontier treats these phenotypes as first-class, validated, reusable artifacts; a 2026 *Pharmacoepidemiology & Drug Safety* paper lays out a formal "fitness-for-purpose" process for judging whether a phenotype is good enough for a given study (sourced). The FDA's **Sentinel RWE Data Enterprise** (linked EHR + claims for 25M+ patients — a scoped subset of the larger ~129M-patient Sentinel system) explicitly runs on *validated computable phenotyping algorithms* (sourced).

**Stage 5 — Link patients and check quality.** **Linkage** solves the "shattered patient" problem via **tokenization.** Take identifying fields (name, date of birth, etc.), run them through a one-way cryptographic hash with a secret salt, and produce a **token** — an opaque string that reveals nothing about the person but is *identical* whenever the same person appears. Two datasets tokenized the same way can be joined on the token without either side ever exposing protected health information. Datavant is the dominant vendor; its network moves 60M+ records across 300+ partners, and tokenized clinical trials grew ~300% from 2022 to ~270 trials by end of 2024 (sourced, Datavant 2025). A 2026 market note observes that **linkage now often costs more than the data itself** — matching identity correctly is the thing regulators care most about (sourced).

**Quality gating** is the OHDSI **Data Quality Dashboard (DQD)** plus **Achilles.** Achilles characterizes the database ("here's what's in it"); DQD runs automated conformance/completeness/plausibility checks table-by-table, field-by-field, organized by the Kahn framework. (One housekeeping note, since published figures disagree: the DQD's check count is reported variously as ~1,500+, 3,000+, and 4,000+ depending on version and on whether you count *parameterized check instances* or *check types*. Throughout this chapter, treat "thousands of checks" as referring to **parameterized instances** — that's the larger, instance-level count.) The 2025 trend is **continuous** quality testing — e.g., `dqdbt`, shown at the OHDSI 2025 showcase, wires these checks into the dbt build so every pipeline run is re-validated, the way software gets unit-tested on every commit (sourced).

**The new ingredient (2025–2026): LLMs eating the unstructured layer.** Roughly half of clinical truth lives in free text that structured codes never capture (cancer stage, why a drug was stopped, response to therapy). The shift is using **frontier LLMs to abstract that text into structured fields.** Microsoft's "Universal Abstraction" work (2025) and a Jan-2026 JMIR technical study both show LLMs extracting structured variables (e.g., cancer staging) from notes at near-human accuracy, validated against expert gold-standard abstraction (sourced). This replaces the older, narrow, train-a-model-per-variable NLP approach (the lineage Flatiron pioneered in oncology) with general-purpose models you *prompt* rather than *train.* In **early 2026** (sources say "early 2026," not a specific month) TriNetX launched a conversational AI front-end for natural-language queries over its federated network — a sign the LLM layer is moving from extraction into the query interface itself (sourced, corrected per verifier).

---

## 3. Why it works

**The underlying principle: separate "what the data says" from "what it means," and make every layer reproducible and explicit.** (inference)

The naive alternative is to write one bespoke analysis script per dataset that reads raw codes directly. It fails for three structural reasons.

- **It doesn't compose.** Hard-coding "ICD-10 I21.* = heart attack" into your script means your study runs on exactly one database and nowhere else. The common-model approach pays a large upfront harmonization tax precisely so the analysis becomes **portable** — write the phenotype once, run it across 500 databases. Network-scale evidence (a billion records) is only possible because the model is shared. (inference, grounded in sourced network figures)

- **It can't be audited.** The regulatory bar in 2026 has moved toward **fact-level provenance**: following the July 2024 RWD guidance and the Oct 2, 2024 finalization of 21 CFR Part 11 for electronic records in clinical investigations, the FDA *increasingly* expects that every value in a submission can be traced to its source and reproduced (sourced for the guidance dates; note this "every value" expectation is a reasonable reading of the 2024–2026 regulatory *direction*, not a single hard codified rule — directional, not literal). A monolithic script that reads raw data and emits a number cannot tell you *why* a given patient was counted. A layered pipeline (raw → mapped → modeled → phenotyped) with logged transformations can replay the exact lineage of any single fact.

- **It silently encodes bias as truth.** Because phenotypes are *definitions*, two analysts can get different "heart attack rates" from identical data by defining the outcome differently. The naive script hides that choice inside undocumented `WHERE` clauses. The discipline of computable phenotypes drags the definition into the open, where it can be validated (sensitivity / positive predictive value against chart review) and reused. **The data doesn't contain outcomes; people define them — so the definition must be a first-class, testable object, not buried logic.** (inference)

There's a subtler reason the LLM layer works *now* when it didn't before: clinical abstraction is a *reading-comprehension* task ("what stage is this cancer, per this note?"), and frontier models generalize across the long tail of how clinicians phrase things — whereas the old approach needed a separately trained model per variable and broke on phrasing it hadn't seen. (inference) The catch, and why humans stay in the loop: LLMs can be confidently wrong, so the 2026 pattern is **LLM-extracts → human-or-second-model-verifies → provenance-logged**, never LLM-extracts → trust. (advisory)

---

## 4. People & resources

*Orders of magnitude, with basis. Team and cost figures are **advisory** — reasoned estimates from how these orgs staff, not quoted line-items.*

**Data scale (sourced).** A single national database lands in the tens of millions of patients (FDA Sentinel RWE-DE: 25M+ linked; N3C: ~22.8M from 84 sites). A *network* reaches ~1 billion records (OHDSI: 500+ sources). A vendor linkage network like Datavant moves 60M+ records across 300+ partners. So: **one institution ≈ 10⁵–10⁶ patients; one national asset ≈ 10⁷; the global network ≈ 10⁹.**

**Compute.** Modest by AI standards — until the LLM layer. The harmonization/ETL/phenotyping work is warehouse SQL: a Snowflake/Databricks/BigQuery cluster, with costs dominated by storage and query volume, not GPUs. The DQD's thousands of checks are heavy SQL passes, not training runs. The expensive new line item is **LLM inference at scale** — abstracting free text across millions of notes means millions of model calls, a cost driver that didn't exist two years ago. (inference)

**Money.** The market frames it: RWE *linkage services* alone were ~$0.7B in 2025, projected to $3.6B by 2036 (sourced, FMI) — and notably, **linkage now frequently costs more than the underlying data licenses,** because correct identity matching is what makes a study regulatory-grade (sourced). For a single pharma RWE study, the all-in (data license + tokenized linkage + analytics + curation) commonly runs into the high six to seven figures. (advisory)

**Time.** Standing up a new source into OMOP (the Stage 2/3 mapping + ETL) is typically a **multi-month** effort, with vocabulary mapping as the long pole; a 2025 OHDSI showcase explicitly pushed tools (`dbt-synthea`, `dqdbt`) to *shorten* this. An individual outcomes study, once the infrastructure exists, runs in **weeks to a few months**, gated by phenotype validation. (advisory, consistent with OHDSI literature)

**Team and roles (advisory).** The repeated industry truth is *"80% data engineering, 20% model training."* A realistic build team:
- **Data engineers (2–6)** — the bulk; own ingest, ETL, the warehouse/dbt pipeline.
- **Clinical informaticist / vocabulary specialist (1–2)** — own the code→concept mappings; domain knowledge is non-negotiable here.
- **Epidemiologist / phenotype author (1–2)** — author and *validate* computable phenotypes against chart review.
- **ML/NLP engineer (1–2, growing)** — own the LLM abstraction + verification loop; the fastest-growing seat in 2026.
- **Data-quality / regulatory lead (1)** — owns DQD, lineage, and the 21 CFR Part 11 / provenance audit trail.
- **Privacy/governance (shared)** — owns tokenization and the de-identification framework.

A credible regulatory-grade pipeline team is **~6–12 people**, weighted heavily toward engineering, with a small irreplaceable core of clinical-domain experts and a dedicated quality/provenance owner. The clinical experts are the bottleneck resource — not the compute. (advisory)

**The mental model to keep.** Three jobs, in order of difficulty: **(1) translate the dialects** (vocabulary mapping — most human labor), **(2) define the outcomes as testable logic** (computable phenotypes — most scientific judgment), **(3) link the patient and prove the lineage** (tokenization + provenance — most regulatory weight). Everything else — the warehouse, dbt, the DQD, the LLMs — is tooling in service of doing those three things *reproducibly enough that a regulator can trace any single number back to the chart it came from.*

---

## 5. Scenarios & stories

The technique earns its keep under specific conditions — and quietly ruins your study when those conditions break.

### Where it's the right tool

**Story 1 — The oncology label expansion no one could ethically randomize.** A mid-size pharma has a drug approved for second-line lung cancer and wants to show it works in a rarer first-line subgroup. A fresh randomized trial means recruiting dying patients into a control arm getting the *old* standard of care — slow, expensive, ethically fraught for so small a population. Instead, the team builds an outcomes-indexed oncology pipeline over hundreds of thousands of real charts. The hard part isn't the structured data — it's that the outcome that matters, *real-world progression*, lives in radiology reports and oncologist notes, not a tidy column. This is exactly the job LLM-based extraction now does well. Flatiron has published two related-but-distinct results here, and it's worth keeping them straight (corrected per verifier): a **2025 progression-extraction study** found LLM-extracted oncology variables landing within ~two percentage points of expert human abstractors, with real-world survival estimates the company describes as clinically indistinguishable from traditionally abstracted data — while the separate **VALID framework** (*JCO Clinical Cancer Informatics*, April 2026) is the validation *methodology* for AI-extracted oncology data, not the source of those specific accuracy figures (sourced). The pipeline indexes every patient by progression and death dates, emulates a target trial against a matched real-world control arm, and produces an audit trail a regulator can follow. **Why it fits:** the outcome is well-defined, the population is too small or too sick to randomize cleanly, and the evidence consumer explicitly accepts validated real-world evidence.

**Story 2 — Post-market safety surveillance across hospitals you don't control.** A device maker must watch for a rare complication after an implant ships. The signal is spread across dozens of hospitals on different EHRs, and nobody will hand over raw records. The pipeline shines in its **federated** form: each site maps its data to OMOP *locally*, runs the *same* cohort and outcome definitions (shipped as a portable JSON cohort definition plus an analysis package — the OHDSI pattern), and returns only aggregate counts. The December 2025 FDA guidance that relaxed the need for individually identifiable data — letting registries pseudonymize while keeping investigator-level audit trails — makes this newly practical for regulatory-grade work (sourced). No raw data leaves any hospital, and the same code runs everywhere, so you're comparing apples to apples. **Why it fits:** standardized outcome + standardized model + privacy-preserving distribution is the precise problem this architecture was built for.

**Story 3 — Trial feasibility before the protocol is locked.** A sponsor is about to freeze eligibility criteria for a Phase III trial. Historically they'd do a one-off feasibility check, finalize the protocol, and then discover mid-enrollment that almost nobody real meets criterion #7. With a queryable, outcomes-indexed network (Datavant frames this as "continuous, enterprise-scale data discovery" replacing static feasibility; TriNetX shipped a natural-language query interface over its federated network in early 2026), they stress-test each criterion against real populations *before* signing — checking not just who exists but who has the right outcome trajectory and follow-up (sourced/advisory). Fewer amendments, fewer enrollment surprises. **Why it fits:** it's a counting-and-coverage question against well-structured population data, where being wrong is expensive.

### Where it's the wrong tool

**Story 4 — Trying to prove a brand-new drug beats the standard.** A startup with a genuinely novel mechanism wants to skip the randomized trial by emulating one from real-world data. This is where the technique becomes *dangerous*, not just imperfect. A target trial emulation **cannot study an intervention that isn't in the data** — if the drug hasn't been used in routine care, there are no records, full stop (sourced). And even for existing drugs, the core threat is *confounding by indication*: sicker patients get treated differently, and the pipeline can't randomize that away. As the 2026 methods literature puts it, emulation "is irremediably compromised by confounding by severity of indication and by inadequately measured, unmeasured, and unknown confounds" — these are pragmatic emulations, but "they cannot drive causal inference" on their own (sourced). A flawless OMOP pipeline will produce a confident, precise, *wrong* effect estimate. The polish hides the bias. **Why it's wrong:** when the central threat is unmeasured confounding and the question is "does A cause better outcomes than B," a clean pipeline is no substitute for randomization.

**Story 5 — A "soft" outcome buried in inconsistent language.** A team wants to study fatigue, or pain, or "patient was doing well" — subjective outcomes recorded inconsistently and meaning different things in different clinics. They reach for the same LLM extraction that nailed cancer progression, and it falls apart. A leading reason RWE studies get rejected is variability in physician practice and differing standards of care producing *unclear outcome measures* (sourced). When the outcome has no stable definition in the source data, no pipeline engineering rescues it — you get outcome misclassification, which biases results in ways that are hard to detect and harder to correct (sourced). The pipeline will happily produce a number; the number won't mean anything. **Why it's wrong:** outcomes-indexing requires a *computable* outcome. If clinicians can't agree what the event is, neither can your phenotype.

**Story 6 — A single small dataset and a one-time question.** A health-system researcher has 4,000 patients in one hospital's EHR and one question for a quality-improvement project. Standing up a full OMOP mapping, an LLM stage, vocabulary harmonization, and a regulatory-grade audit trail is wildly disproportionate — the "minimum that solves the problem" instinct applies to data architecture too. The pipeline's whole value is *reuse and scale*. For one dataset and one question, a careful analyst with SQL and a chart review is faster, cheaper, and just as valid. **Why it's wrong:** the heavy machinery pays off across many studies and sites; for a single-use analysis it's all cost, no leverage. (advisory)

**Story 7 — Real-time care at the bedside.** Someone proposes using the OMOP analytics pipeline to drive live EHR alerts. Wrong layer. OMOP and outcomes-indexed marts are optimized for *population analytics after the fact* — looking back across many patients. Real-time, point-to-point exchange for one patient in front of a clinician is FHIR's job, not the analytics warehouse's (sourced). The community builds FHIR-to-OMOP bridges precisely because these are two different jobs. **Why it's wrong:** the technique is built for retrospective, aggregated questions.

**The through-line (advisory).** The technique is right when **three things are simultaneously true**: the outcome is crisply computable, the question is retrospective and population-scale, and you'll reuse the machinery across sites or studies. It becomes wrong the moment any one breaks. The most expensive failure mode in 2026 isn't a pipeline that crashes — it's one that runs flawlessly and produces a precise, audit-trailed, confidently *wrong* answer because the study design never belonged in observational data. A senior reviewer's first question should not be "is the pipeline clean?" but "should this question be answered this way at all?"

---

## 6. Cross-industry usage & positioning (as of June 2026)

A clinical and outcomes-indexed pipeline's organizing principle is the **outcome, not the event**. Every record is structured so it can be traced forward to *what it led to* — did the patient survive, did the ticket get resolved, did the code pass tests, did the trade make money. The phrase now lives in two worlds that have quietly converged: the literal healthcare meaning, and a machine-learning meaning where data is labeled by *downstream verified reward.* Both share the same hard problem: **the outcome arrives later, somewhere else, in a different system, and linking it back — privately, accurately, at scale — is where most of the engineering goes.** (inference)

**Healthcare and life sciences — the home turf, now table-stakes.** FHIR is the lingua franca for live clinical exchange; OMOP CDM for research and outcomes analysis. The 2026 frontier is *bidirectional FHIR↔OMOP transformation*, and coverage is still imperfect — OMOP→FHIR mapping reaches only ~23% in published work, reflecting structural mismatches (sourced, Frontiers/TermX 2026). The defining enabling technology is **privacy-preserving record linkage (PPRL) / tokenization** (described mechanically in Section 2); Datavant is the dominant infrastructure player, and a published psoriasis trial demonstrated >99% linkage precision linking EHR to claims (sourced).

Who leads, by use case (sourced, as of 2026):
- **IQVIA** — global scale and regulatory authority; 1.2B+ anonymized records across 60+ countries; the default for FDA/EMA submissions and post-market surveillance.
- **Truveta** — real-time EHR with full clinical notes from a 30+ health-system consortium, covering roughly **120–130M de-identified US patients (~18% of US daily clinical care, US-only)** — scale added here per verifier so it reads alongside the precisely-numbered competitors; its Truveta Language Model abstracts notes automatically, and it launched "Truveta Intelligence" in April 2026 for continuously refreshed insight.
- **Tempus / Flatiron / ConcertAI** — oncology and clinico-genomic depth (molecular + imaging + clinical); the standard stack for cancer launches.
- **Komodo Health** — all-payer patient-journey mapping, 330M+ patients, strong in rare disease; its "Marmot" agentic AI runs complex cohort studies.
- **HealthVerity** — flexible tokenized data marketplace; **Veeva Crossix** — outcomes linked to marketing exposure, used by 17 of the top 20 biopharmas.

A telling structural fact: sophisticated buyers run **2–4 RWE platforms in parallel** rather than consolidating — roughly $5M/year on a core analytics platform plus $1–2M each on specialty tools (sourced). No single pipeline captures all outcomes.

**Regulatory state of the art.** The big 2026 shift is acceptance. In December 2025 the FDA finalized *Use of Real-World Evidence to Support Regulatory Decision-Making for Medical Devices* (Federal Register, Dec 18, 2025), superseding the 2017 guidance, and crucially said it will **accept RWE without always requiring individual participant-level data** — opening the door to large de-identified registries and claims databases (devices-only; operationalization from Feb 16, 2026). The FDA also adopted **ICH M14** (non-interventional RWD safety studies) via Federal Register on Mar 4, 2026 (sourced). This moves outcomes-indexed pipelines from "nice to have" to a recognized evidentiary pathway.

**Pharmacovigilance** is the fastest-moving sub-area: ~73% of global pharma organizations are planning, piloting, or deploying agentic AI for drug safety, with LLM-agent solutions reporting ~40% faster turnaround and ~30% accuracy gains (sourced).

**The machine-learning sense.** Outside healthcare, the same idea is the backbone of how frontier AI is trained and judged — "clinical" maps to "instrumented production telemetry," "outcome" to a verifiable reward.
- **Coding / dev tools** — the most advanced verifiable-outcome domain. Reinforcement Learning from Verifiable Rewards (RLVR) indexes each agent trajectory by whether the code passed tests. Agent-RLVR lifted pass@1 on SWE-Bench Verified from 9.4% to 22.4% on a 72B model; SWE-RM is a 30B execution-free verifier that grades trajectories *without running them*, beating execution-based feedback by +3 pass@1 (sourced). The frontier is moving from "run the tests" to "predict the outcome cheaply" — the direct analog of healthcare's delayed, sparse clinical endpoints. (inference)
- **Customer support** — outcomes-indexed eval is table-stakes; production telemetry follows OpenTelemetry GenAI conventions, with **resolution rate / task completion** as the executive metric, in an explicit closed loop: monitoring → auto-curated eval sets → experimentation → redeployment (sourced).
- **Robotics** — closed-loop data-generation pipelines (e.g., RADAR) now include **automated success-evaluation modules** that judge whether a policy met its goal without a human in the loop (sourced) — the robotics version of outcomes-indexing.
- **Defense** — outcomes-indexing maps to mission-success-labeled autonomy data; open detail is sparse (much is classified), so treat the parallel as **inference**.

**The cross-cutting truth (inference).** Every domain solves the same three problems: (1) **normalize** heterogeneous upstream data into a common model; (2) **link** each record to a downstream outcome that arrives late and elsewhere — via tokens in healthcare, trace IDs in software, episode IDs in robotics; (3) **index** by outcome so you can train, evaluate, and audit on what actually happened. Healthcare is the most mature because it had to solve privacy-preserving linkage first, and tokenization is the reusable crown jewel. The AI-training world is the fastest-moving because its outcomes are cheaper to verify — and its 2026 frontier (execution-free verifiers, process reward models) is precisely an attempt to make outcomes cheaper and denser, the same wall healthcare hits with delayed, sparse clinical endpoints.

---

## 7. Learning path for a technical leader

*For a leader who must steer, fund, hire, and judge — not build. Concepts only. (advisory throughout)*

### Mental models to install

- **MM1 — The pipeline IS the evidence.** Every transformation choice (how you defined "diabetic," which records you dropped, how you handled a missing lab) is a scientific claim that can flip a result. There is no "just move the data."
- **MM2 — Standardize the meaning, not just the shape.** The hard, valuable, risky part is *semantic interoperability* — making "MI," "myocardial infarction," ICD-10 I21, and a SNOMED code all mean the same thing. OMOP does this via standardized concept IDs.
- **MM3 — Common data model = write once, run everywhere.** ~1B records in one schema lets a study package run at every site *without moving patient data*. This is why OMOP won.
- **MM4 — Observational ≠ randomized; design is your only defense against confounding.** The modern discipline is **target trial emulation**: design the observational analysis to mimic the trial you wish you could run, with a clean time-zero and no leaking the future into the past.
- **MM5 — A phenotype is a validated definition, not a WHERE clause.** A computable phenotype is precise, versioned, and validated with known sensitivity/specificity (e.g., via PheValuator). Throwaway cohort queries are the #1 amateur tell.
- **MM6 — Relevance and reliability are the regulator's two questions.** FDA + ICH M14 (2026) evaluate RWD on relevance (detailed, representative, appropriate?) and reliability (provenance, completeness, accuracy, traceability). "Fit-for-purpose" is now a documented determination.
- **MM7 — Pre-specification is the credibility unlock.** Design, variable definitions, and analysis plan locked *before* looking at outcomes. Reproducibility from a frozen spec is the product.
- **MM8 — Two clocks.** Clinical-time (FHIR, real-time, one patient) vs. analysis-time (OMOP, retrospective, populations) — complementary ends of one pipeline, with 2026 direction toward bidirectional FHIR↔OMOP.

### Reading spine (few, high-value)

1. **The Book of OHDSI** — canonical; the CDM, Vocabularies, Data Quality, Cohorts, Estimation, Prediction chapters.
2. **OMOP CDM spec + a medallion (bronze/silver/gold) primer** — for shared layering vocabulary.
3. **Hernán & Robins on target trial emulation** — a recent overview, with *Causal Inference: What If* for depth.
4. **FDA RWE guidance + ICH M14** — to internalize relevance/reliability and pre-specification.
5. **The OHDSI Software Tools page** — map names (ATLAS, HADES, Strategus, DQD, Achilles, PheValuator) to functions; skim.
6. **One LLM-vs-rule-based phenotype-extraction paper (JAMIA 2025)** — to calibrate the hype.

### Checkpoints ("you understand it when you can…")

- Explain to a board why **vocabulary mapping** is the expensive, value-creating step — not data movement.
- Take a "drug X cuts readmissions" claim and **name the bias most likely faking the result** plus the design defense.
- Distinguish **"the pipeline ran" from "the data is fit for this question"** and name the proving artifacts.
- Describe a **30-site study sharing no patient records**, and why that's both privacy and reproducibility.
- State **regulatory-grade in two words** (relevance, reliability) and the documentation it forces.
- Say **where you'd let an LLM in and where you'd forbid it**, grounded in validation.
- Articulate **FHIR↔OMOP as complementary clocks**, not a competition.

### How to evaluate an expert (interview questions, with tells)

Use open questions; listen for whether they reach for **bias, validation, and reproducibility unprompted.**

- **"How does a wrong result get into an RWE study, and where does your pipeline stop it?"** *Strong:* names confounding-by-indication, immortal-time, selection, measurement error, each tied to a defense (target trial emulation, time-zero, phenotype validation, negative controls). *Red flag:* thinks big *n* gives randomization for free.
- **"How do you define and trust a phenotype like type 2 diabetes?"** *Strong:* conceptual vs operational definition, validation against a gold standard, sensitivity/specificity, versioning, libraries. *Red flag:* surprised a cohort definition needs validating.
- **"What does regulatory-grade mean, concretely, in 2026?"** *Strong:* relevance + reliability, fit-for-purpose, pre-specification, provenance; names FDA RWE guidance and **ICH M14**. *Red flag:* thinks it's purely security and de-identification.
- **"OMOP vs FHIR — when and why?"** *Strong:* FHIR = real-time per-patient; OMOP = population analytics; two ends of one pipeline; OMOP's killer feature is the network study. *Red flag:* conflates the two.
- **"Where would you use an LLM here, and where refuse?"** *Strong:* LLM/NLP to surface candidate facts from notes, every fact validated; LLM output = hypothesis. *Red flag:* feeds unvalidated LLM extractions straight into an outcomes analysis.

**Green flags:** reaches for bias and validation before asked; treats reproducibility and pre-specification as non-negotiable; comfortable saying "the data can't answer that"; rare four-way fluency across clinical + data engineering + biostatistics + regulatory.

---

## 8. Team notes

*Org/hiring strategist view. (advisory unless a claim is tagged sourced.)*

**The shape of the discipline.** Treat this as *governed analytics-engineering* sitting on a *clinical-terminology* discipline, with a *regulatory/quality* overlay. That three-part shape is the whole org story. Two things make it different from ordinary data engineering, and they drive every hire: **vocabulary/semantics are the hard part, not the plumbing** (sourced — OMOP for analytics, FHIR for exchange), and **provenance is now a regulatory requirement** — sponsors must document lineage and re-run the pipeline a year later to an identical result (sourced — FDA finalized revised RWE-for-devices guidance Dec 2025).

**Roles and seniority.** The instinct to spin up a big new "clinical data platform team" is usually wrong for anyone who isn't a top-20 pharma or a research-mission health system. Most orgs need 1–3 specialized people plus rented infrastructure.

- **Healthcare Analytics Engineer (the anchor hire, mid–senior).** Knows modern data tooling (SQL + Python/R, dbt, a cloud warehouse) *and* clinical terminologies and the OMOP/OHDSI toolchain. Often *absorbed* from an existing data engineer given 3–6 months of ramp. These people are actively recruited under titles like "Senior Clinical Data Engineer / OMOP Specialist" (sourced — OHDSI job board, John Snow Labs, Syneos/IQVIA postings).
- **Terminology/vocabulary specialist (senior)** — dedicated only at scale.
- **Clinical informaticist or epidemiologist, paired with a clinician (senior)** — owns outcome/phenotype definitions; usually a *part-time clinical SME*, not a full FTE.
- **RWE biostatistician / data scientist (senior)** — runs causal/statistical analysis on the output. **Do not fuse this with the engineer.** Building the pipeline and running causal inference are different jobs; conflating them gives you mediocre versions of both.
- **Data quality / validation lead (mid–senior)** — absorb into engineering at small scale, dedicate at regulated scale.

**Comp reality check:** "OMOP Data Analyst" averages ~$83k US (range ~$62k–$97k) — but that's the *analyst* tier (sourced — ZipRecruiter, 2026-06-24). The senior *engineer* who owns mapping + pipeline + provenance is materially scarcer and more expensive, typically 5+ years. **Budget for one strong senior, not three juniors** — the junior-heavy version produces plausible-looking tables that are subtly wrong, which is the worst outcome in this field. (advisory)

**Hiring signals.** *Green flags:* talks fluently about terminology mapping as the real work (names SNOMED, ICD-9/10, CPT/HCPCS, RxNorm, LOINC and where they disagree); uses OHDSI tooling by name unprompted (ATLAS, ATHENA, ACHILLES, DQD); brings software discipline to data (version control, tests, dbt, reproducible builds); asks *what the output is used for* (internal dashboard vs. FDA submission) before designing anything. *Red flags:* treats it as generic ETL and waves off vocabularies as "just a lookup table"; wants to build a *custom* common data model instead of adopting OMOP; can't distinguish "the pipeline ran" from "the numbers are right"; no instinct for audit/lineage; over-indexes on LLMs as a silver bullet.

**Build vs. buy.** Default: **rent/buy the data and most of the platform; own only the outcome definitions and the governance.**
- **Buy the data — always.** Nobody recreates a 318M-patient longitudinal network; TriNetX alone covers 318M+ patients across 9,200+ sites, pre-mapped (sourced). The market consolidated hard — **Datavant acquired Aetion (closed July 2025)**, creating an end-to-end linkage-plus-causal platform accepted by FDA and EMA (sourced).
- **Buy/rent the transformation layer too.** You don't need to write OMOP ETL from scratch: **Tuva Project** (open-source dbt package into analytics-ready marts with built-in DQ tests and pre-built outcome measures), **InterSystems OMOP** (managed FHIR-to-OMOP SaaS), or full vendor platforms (IQVIA, Merative, TriNetX, Datavant/Aetion) (sourced).
- **Own only two things:** your **outcome/phenotype definitions** — the clinically-validated logic for what counts as response, progression, or adverse event *in your therapeutic area*, where domain advantage compounds (sourced — the 2026 frontier is exactly this) — and your **governance/provenance harness**, because the *discipline* is organizational and must be yours.

Rule of thumb: pharma/medtech filing with FDA → buy data + a regulatory-grade platform (Aetion-class), own definitions + governance, and expect to run **2+ vendors in parallel** because data types are complementary, not substitutable. Provider/payer/internal analytics → adopt OMOP + Tuva on your existing warehouse and hire one strong analytics engineer. Build-from-scratch → justify only if your data itself is a genuinely unique product.

**Failure modes** (mostly sourced):
1. **The pipeline is green but the outcomes are wrong** — ETL errors, EHR data-entry errors, source incompleteness, coding errors all yield clean-looking-but-false results (sourced). *Mitigation: validation is a named role/deliverable, not a side effect.*
2. **Mapping invents detail that isn't there** — converting local codes to a model demanding more specificity than the source has → fabricated precision (sourced). The most insidious technical failure.
3. **Outcome definitions left to engineers** — when the SQL author, not a clinician/epidemiologist, decides what counts as the outcome, the study is built on sand. (advisory)
4. **Two sources merged as if equivalent** — routine-care and research data are collected under different practices; naive joins corrupt the result (sourced).
5. **No reproducibility, discovered at submission time** — teams that didn't version their rules/models can't re-run to the same answer, and the filing stalls (sourced). *Retrofitting lineage is far more expensive than building it in.*
6. **Building a bespoke data model** — orphans you from the entire OHDSI/Tuva ecosystem and every purchasable dataset. (advisory)
7. **AI abstraction without governance** — pointing an LLM at notes is genuinely useful but, ungoverned, silently injects unauditable errors into a pipeline that's supposed to be reproducible (sourced).
8. **Under-hiring with juniors** — three analysts producing confident, wrong tables is worse than one senior who knows what they don't know. (advisory)

**Bottom line (advisory).** Hire **one strong Healthcare Analytics Engineer** as the anchor. **Rent the data, rent the transformation layer, rent the analytics platform** if you're filing with regulators. **Own only your outcome definitions and your provenance discipline** — that's the moat. Pair the engineer with a part-time clinical SME for definitions and a separate biostatistician for causal analysis; don't fuse those roles. Treat reproducibility and lineage as day-one requirements, because as of 2026 the FDA does.

---

## Sources

- The Book of OHDSI — Network Research: https://ohdsi.github.io/TheBookOfOhdsi/NetworkResearch.html
- Lifebit — OMOP CDM: The Complete Guide for Healthcare Researchers (2026): https://lifebit.ai/blog/omop-complete-guide/
- Frontiers in Medicine — Bidirectional FHIR–OMOP CDM transformations using TermX (2026): https://www.frontiersin.org/journals/medicine/articles/10.3389/fmed.2026.1736785/full
- Communications Medicine — Automating clinical phenotyping using NLP (2025/2026): https://www.nature.com/articles/s43856-025-01337-0
- Flatiron Health — VALID validation framework, JCO Clinical Cancer Informatics (April 2026): https://resources.flatiron.com/press/flatiron-health-publishes-first-peer-reviewed-validation-framework-for-ai-extracted-real-world-oncology-data-in-journal-of-clinical-oncology
- Datavant — 3 Data Trends Shaping Clinical Research and RWE in 2026: https://www.datavant.com/blog/3-data-trends-shaping-clinical-research-and-rwe-in-2026-and-beyond
- Datavant — 2025 Trends in Clinical Trial Tokenization and RWD Linkage: https://www.datavant.com/blog/datavant-analysis-2025-trends-in-clinical-trial-tokenization-and-real-world-data-linkage
- Datavant — Privacy-Preserving Record Linkage (PPRL): https://www.datavant.com/blog/privacy-preserving-record-linkage
- Castor — FDA Real-World Evidence standards 2026: https://www.castoredc.com/blog/fda-real-world-evidence-standards-2026/
- Federal Register — Use of RWE for Medical Devices (Dec 18, 2025): https://www.federalregister.gov/documents/2025/12/18/2025-23252/use-of-real-world-evidence-to-support-regulatory-decision-making-for-medical-devices-guidance-for
- FDA — Use of RWE to Support Regulatory Decision-Making for Medical Devices: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-real-world-evidence-support-regulatory-decision-making-medical-devices
- IQVIA — FDA Updates Guidance on RWE for Medical Devices (Jan 2026): https://www.iqvia.com/blogs/2026/01/fda-updates-guidance-on-real-world-evidence-for-medical-devices
- Applied Clinical Trials — Overcoming the Pitfalls of Using RWE in Regulatory Submissions: https://www.appliedclinicaltrialsonline.com/view/overcoming-the-pitfalls-of-using-real-world-evidence-in-regulatory-submissions
- Zoccali et al., European Journal of Clinical Investigation (2026) — Methodological challenges in RWE: https://onlinelibrary.wiley.com/doi/10.1111/eci.70153
- ScienceDirect (2026) — Target Trial Emulation for causal inference using observational data in neurology: https://www.sciencedirect.com/science/article/pii/S0035378726004790
- IntuitionLabs — Pharma Real-World Data Platforms: 2026 Vendor Comparison: https://intuitionlabs.ai/articles/pharma-real-world-data-platforms-comparison
- GlobeNewswire — Truveta Intelligence launch (April 2026): https://www.globenewswire.com/news-release/2026/04/28/3283008/0/en/truveta-unveils-truveta-intelligence-delivering-real-time-insights-from-real-world-data.html
- John Snow Labs — Agentic AI in Healthcare Data / RWE: https://www.johnsnowlabs.com/the-age-of-agentic-ai-in-healthcare-data-automating-clinical-research-and-real-world-evidence-workflows/
- IntuitionLabs — AI in Pharmacovigilance / Adverse-Event Detection: https://intuitionlabs.ai/articles/ai-pharmacovigilance-adverse-event-detection-gvp
- arXiv — Agent-RLVR (SWE agents): https://arxiv.org/abs/2506.11425
- arXiv — SWE-RM execution-free verifier: https://arxiv.org/pdf/2512.21919
- arXiv — RADAR closed-loop robotic data generation: https://arxiv.org/pdf/2603.11811
- MLflow — Setting Up LLM Observability Pipelines in 2026: https://mlflow.org/articles/setting-up-llm-observability-pipelines-in-2026/
- The Tuva Project: https://thetuvaproject.com/ and https://github.com/tuva-health/tuva
- InterSystems OMOP: https://www.intersystems.com/resources/intersystems-omop/
- Fierce Healthcare — Datavant acquires Aetion: https://www.fiercehealthcare.com/health-tech/datavant-acquires-real-world-evidence-company-aetion-boost-its-life-sciences-business
- TriNetX: https://trinetx.com/
- ZipRecruiter — OMOP Data Analyst salary (2026-06-24): https://www.ziprecruiter.com/Jobs/Omop-Data-Analyst
- OHDSI Forums — Senior Clinical Data Engineer / OMOP Specialist job post: https://forums.ohdsi.org/t/job-post-senior-clinical-data-engineer-omop-specialist-anywhere-us-or-mexico-city-mx/20213
- Merative — Real-World Data Trends 2026: https://www.merative.com/blog/real-world-data-trends-2026-the-shift-to-quality-and-ai-precision
