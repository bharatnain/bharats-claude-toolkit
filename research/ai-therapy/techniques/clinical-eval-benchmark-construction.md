# Clinical eval & benchmark construction

*Labels used throughout: **sourced** (a published claim, with URL + access date in Sources); **inference** (my reasoning from sourced facts); **speculation** (a forward guess); **advisory** (my reasoned recommendation on learning design or org strategy). When a sentence carries no label, it is either definitional or sourced and traceable to the Sources list.*

---

## 1. What it is

Clinical eval and benchmark construction is the craft of building a **trustworthy measuring stick for a medical AI** — one whose score actually tells you something about how the system will behave with real patients.

The hard part is the problem itself. "Good" in medicine depends on a doctor's judgment. The questions rarely have one right answer. And a wrong answer can hurt someone. So you cannot just write an answer key and count correct letters.

The old way did exactly that. The **MedQA / USMLE** style was a pile of medical-board exam questions, each with one correct letter (A/B/C/D); you reported percent correct. By 2026 top medical models score roughly **88–91% on MedQA** (e.g., MedGemma 1.5 lands in that band depending on the variant — the 27B text variant is reported at 87.7%) (*sourced*, with the precise 91% figure treated as soft because it rests on secondary sources). That number sounds great and means little. Real patients don't arrive as clean four-option questions, and the test is **saturated**: nearly everyone scores near the top, so it can no longer separate good models from bad ones. It is also **contaminated** — the questions are on the public web and likely in training data, so a high score can be memorization rather than skill.

The new way looks nothing like an exam. The reference example is **HealthBench** (OpenAI, May 2025) and its 2026 successor **HealthBench Professional**. Instead of questions with answer keys, you have **realistic doctor–patient or doctor–AI conversations**, each paired with a **physician-written rubric**: a checklist of specific things a good answer *must do* and *must not do*, each item carrying a point weight (positive for good behaviors, negative for dangerous ones).

So the unit of a modern clinical benchmark is not "question + right answer." It is:

> **a scenario + a custom, per-scenario checklist of weighted criteria written by a doctor.**

That single shift — from *answer keys* to *rubrics* — is the whole story. Everything else is plumbing around it. The deeper reframe (*advisory*): a benchmark is a **scientific instrument**, and like any instrument it has two independent properties — **reliability** (does it give the same reading on repeat?) and **validity** (does it measure the thing you actually care about?). A benchmark can be perfectly reliable and totally invalid: it can consistently reward confident-sounding wrong answers. Holding those two ideas apart is the beginning of competence here.

---

## 2. How it works

There are two machines: the **construction** machine that builds the test, and the **grading** machine that runs it. Watch both turn.

### A. Construction — building the test

**Step 1 — Get realistic scenarios.** You need inputs that look like real clinical use, not textbook trivia. Two sources dominate in 2026:

- *Synthetic-but-curated conversations* (original HealthBench): 5,000 single- and multi-turn conversations, written and seeded to resemble real consults — patients describing symptoms, doctors asking for differential diagnoses, emergency triage, global-health contexts.
- *Real clinician chats* (HealthBench Professional, 2026): the newest move is to harvest **actual conversations clinicians had with ChatGPT while doing their jobs**, then filter hard. Professional started from **15,079 candidate real chats** and distilled to **525 final examples**, deliberately enriching for *difficult* cases by roughly 3.5× (*sourced*).

**Step 2 — Write the rubric for each scenario.** A physician reads the scenario and the space of possible responses, then writes a bespoke checklist. Example items for a chest-pain consult:

- `+8` "Recommends immediate emergency evaluation / flags a possible cardiac event"
- `+3` "Asks about radiation of pain, sweating, shortness of breath"
- `−10` "Reassures the patient it's probably nothing without referral" (a dangerous omission — large negative weight)

HealthBench contains **48,562 unique rubric criteria** across its 5,000 scenarios (about 10 per scenario), and almost every criterion was written by a physician specifically for that one example rather than reused from a template; weights run roughly **−10 to +10** (*sourced*).

**Step 3 — Adjudicate (the quality gate).** One doctor's checklist is biased and error-prone, so multiple physicians review and fix it. HealthBench Professional runs **three review stages**: (1) a clinician authors the conversation, an initial rubric, and a 1–7 difficulty rating; (2) one or more other physicians verify realism, and for "hard" cases, *two* independently confirm the AI response really has a meaningful flaw; (3) a final physician sharpens ambiguous wording. Net effect: **every example adjudicated by 3+ physicians** (*sourced*).

**Step 4 — Organize into axes and themes** so the score is diagnostic, not a single opaque number. HealthBench tags every criterion by behavioral axis — Accuracy (~33%), Completeness (~39%), Context Awareness (~16%), Communication (~8%), Instruction-Following (~4%) — and by clinical theme (global health, responding under uncertainty, emergency referrals, and so on). It also carves out a **Consensus subset** (3,671 high-agreement, safety-critical items) and a **Hard subset** (1,000 examples models fail on) (*sourced*).

### B. Grading — running the test (the "rubric-as-judge" loop)

Here is the clever, slightly circular part. You cannot pay doctors to grade every model's every answer forever — too slow, too expensive (a human takes about 10 minutes per item; an AI judge about 22 seconds, per a 2026 *npj Digital Medicine* study, *sourced*). So the grader is **another LLM acting as a judge**.

The loop, per scenario:

1. The **model under test** produces a response to the scenario.
2. For **each rubric criterion**, a **grader model** (HealthBench used GPT-4.1) is shown the conversation, the model's response, and that one criterion. It outputs a binary **met / not-met**.
3. The scenario score is the **weighted fraction of points earned**: sum the weights of met criteria, divide by the maximum achievable positive points. Negative criteria (dangerous behaviors) subtract. Professional adds a small **length penalty** (~0.0147 points per 500 characters past a 2,000-character baseline) so models can't win by padding (*sourced*).
4. Average across all scenarios to get the benchmark score.

**Why this isn't hopelessly circular.** The judge is *not* asked "is this answer good?" — that vague question would let the judge's own (possibly wrong) medical opinion leak in. It is asked "**does this answer contain *this specific, physician-pre-written fact*?**" That is closer to reading comprehension than to medical judgment. The hard reasoning was front-loaded by the doctors who wrote the rubric; the judge just pattern-matches against a fixed checklist.

### C. Validation — proving the judge can be trusted

You must show the AI judge agrees with humans before you trust any score it produces. The standard test: have physicians grade a sample by hand, then compare the judge's met/not-met calls to theirs. HealthBench reports the GPT-4.1 grader at **macro F1 ≈ 0.709** against physician labels — and, in the paper's precise framing, the grader falls **in the upper half of physicians for six of seven themes** (*sourced*). It is plain-language fair to say the judge is "about as reliable as a typical individual physician relative to consensus." It is slightly stronger than the paper to say it equals "how much two physicians agree with each other" (*inference* — the paper frames it as grader-vs-consensus standing within the physician distribution, not a direct pairwise physician-physician number).

That last idea is load-bearing: the judge is "good enough" not absolutely, but **relative to the irreducible disagreement among doctors themselves**.

That noise floor is now studied directly. A 2026 paper, *Decomposing Physician Disagreement in HealthBench*, uses variance decomposition and finds something counterintuitive (*sourced*): the things you'd expect to explain disagreement explain almost none of it — rubric identity accounts for only ~3.6–6.9% of the variance, physician identity ~2.4%, and specialty, metadata, and normative phrasing little. The **dominant ~81.8% is an unexplained case-level residual**. There is also a real **"quality-boundary" (inverted-U) effect**: doctors disagree most on borderline answers. The practical lesson actually *strengthens* the ceiling argument: most of a benchmark's "error" is not fixable noise from bad rubrics or biased reviewers — it is irreducible, case-by-case disagreement among competent doctors, and it caps how high any score can meaningfully climb.

---

## 3. Why it works

**The core principle: decompose an un-gradable global judgment into many gradable atomic facts.**

"Is this a good medical answer?" is too holistic to grade reliably — even experts disagree, and an AI judge would just impose its own opinion. But "Did the answer mention escalating to the ER?" is **atomic, checkable, and decided in advance by a human expert**. Rubrics work by moving all the expensive human judgment to *construction time* (write the checklist once) and leaving only cheap *verification* at *grading time* (tick the boxes). That is what makes the test both expert-grounded and cheaply repeatable for every new model that ships.

**Why the naive alternatives fail:**

- **Multiple-choice exams (MedQA/USMLE).** They fail on *construct validity* — they measure recall of board-exam facts, not the messy work of a real consult (asking follow-up questions, hedging under uncertainty, knowing when to escalate). A 2026 line of work calls this the **"academic-first, clinical-second"** trap. They also **saturate** (~90%+ for everyone) and are **contaminated** (public questions leak into training data).
- **Single reference answer + text-similarity scoring (BLEU/ROUGE/embedding match).** There are *many* good ways to answer a clinical question and many bad ways that look textually similar to good ones. Word overlap rewards phrasing, not correctness or safety.
- **"Just ask an LLM if the answer is good" (holistic LLM-as-judge, no rubric).** This fails on reliability and **shared blind spots**: the judge inherits the same gaps as the model it grades (both may miss the same rare-but-deadly diagnosis), and it is swayed by length, confidence, and style. The 2025 paper *Neither Valid nor Reliable?* documents these biases; a 2026 paper is titled, pointedly, *Reliability without Validity*. Rubrics constrain the judge to pre-specified facts instead of free-floating opinion.
- **Pure human grading.** It *is* the gold standard, but it doesn't scale — too slow, too costly, not reproducible run-to-run. You cannot re-grade with humans every week a new model ships.

**The honest limitations (why even the good version "isn't clinically ready").** A 2026 critique in PMC lays it out (*sourced*): these benchmarks grade **static, offline conversations** — no real-time interaction, no multimodal data, no longitudinal follow-up, and **no link to actual patient outcomes**. Roughly 95% of LLM medical studies still use no real patient data. A high HealthBench score does **not** guarantee better real-world care. The proposed next step is **"silent-mode" prospective trials**: run the model live inside an EHR, log its recommendations without acting on them, and compare against clinician decisions and real outcomes over time.

**A telling result.** On HealthBench Professional (2026), the best system (ChatGPT for Clinicians, GPT-5.4) scored **59.0**, base GPT-5.4 scored 48.1 — and **physician-written responses scored 43.7**, *below* the AI (*sourced*). Read this carefully. It does **not** mean the AI is the better doctor. It means the rubric rewards **completeness against an exhaustive checklist**, and a real busy doctor writes a terse, sufficient answer that skips "obvious" items the rubric still counts (*inference*). This is the construct-validity warning made concrete: the benchmark measures *checklist coverage*, which correlates with — but is not — *clinical quality*.

---

## 4. People & resources

Orders of magnitude. Counts are *sourced*; dollar and hour estimates are *inference* / *advisory*, reasoned from published participant and item counts.

**Team & roles (sourced counts):**
- **HealthBench**: **262 clinicians across 60 countries** authored and reviewed rubrics.
- **HealthBench Professional**: **190 physicians, 50 countries, 26 specialties** (68% staff/independent, 7% fellows, ~19% residents), plus a small **core ML/research team** (single digits to low tens) building the pipeline and grader.
- Smaller academic benchmarks run lean: a typical setup is **~10 physicians** (attendings plus residents), each double-annotating cases for inter-rater checks.

The shape: **a few hundred physicians acting as a distributed annotation crowd, behind a small engineering core.** The physicians are the cost center; the code is cheap.

**Data scale (sourced):**
- HealthBench: **5,000 scenarios → ~48,562 rubric criteria** (~10 each).
- HealthBench Professional: **15,079 raw candidate chats → 525 curated final** (a ~30:1 filter ratio — the brutal funnel is the point; most real chats aren't discriminating tests).
- DRAGON (clinical NLP): **28,824 annotated reports** across 28 tasks and 5 centers — a different, NLP-flavored scale.

**Physician time (mixed sourced / inference):**
- In one 2025 benchmark, each physician did **60 scenarios in a ~50–70 minute session** (~1 min/scenario) for *rating* tasks — but **writing** a bespoke rubric from scratch is far slower (minutes to tens of minutes per item; *inference*).
- Back-of-envelope (*inference*): ~48,000 criteria at a few minutes each, plus 3× adjudication, is on the order of **thousands of physician-hours** — a flagship like HealthBench represents roughly a **person-year-plus of clinician labor**, spread across hundreds of doctors over a few months.

**Money (inference / advisory):** Physician time dominates. At rough US specialist rates (~$100–300/hr), thousands of hours implies a **construction cost in the low hundreds of thousands to low millions** for a flagship benchmark, before engineering. Academic benchmarks (~10 doctors, hundreds of cases) land in the **tens of thousands**. Grading is cheap: an LLM judge runs each item for **cents and ~20 seconds** versus ~10 minutes of human time — that asymmetry is exactly why model-as-judge won.

**Compute:** Modest and *not* the bottleneck. No model training is required to build a benchmark. Construction is human-labor-bound; grading is **inference-only** (one judge model over items × criteria × models-tested). Even tens of thousands of criteria across dozens of models is a small batch-inference job — trivial next to the physician cost.

**Time-to-build (inference):** A flagship rubric benchmark is a **multi-month effort**; Professional's real-chat annotation ran in concentrated bursts (a documented ~12-day annotation window inside a longer pipeline). Recruiting and coordinating hundreds of physicians and running 3-stage adjudication is the long pole — not the engineering.

**The 2026 frontier — cutting the human cost (sourced).** The newest work tries to automate rubric *writing* and to beat contamination. **RubricHub** (coarse-to-fine automated rubric generation) and *Automated Rubrics for Reliable Evaluation of Medical Dialogue Systems* (2026) generate candidate rubrics with an LLM and have physicians *verify* rather than *author* — the **"Scalable Stewardship"** model (LLMs draft and flag inconsistencies; physicians keep final say). **Autorubric** is a real and related 2026 paper, but it is primarily a *unified evaluation framework* with psychometric reliability metrics and production infrastructure (caching, rate-limiting, cost tracking), not chiefly an LLM-drafts-then-physician-verifies pipeline — RubricHub and RubricRAG fit that description better (correction applied). On contamination, **LiveMedBench (2026)** is the confirmed *live* medical benchmark, continuously refreshed from new cases so models can't have seen them. The direction of travel is clear: **shift physicians from authors to auditors**, push everything else onto machines.

**Advisory takeaways for builders and buyers:**
- Don't trust a single headline number. Demand the *rubric*, the *axis breakdown* (failing on Accuracy or merely Completeness?), and the *grader-vs-physician agreement* (macro F1 near inter-physician agreement, ~0.7+). A model high overall but failing the safety/Consensus subset is dangerous.
- Treat "AI beats physician-written answers" as a **benchmark artifact, not a clinical claim**.
- Construct validity is the whole ballgame: prefer real-chat-derived and live (leakage-free) benchmarks over static exam-style ones.
- Benchmarks are necessary, not sufficient. The credible endgame is **silent-mode prospective EHR trials** tied to real outcomes; a benchmark score is a screening gate, not a clearance.
- Invest in adjudication, not volume. 525 brutally-filtered, 3×-adjudicated items discriminate better than 50,000 cheap ones. Spend physician hours on *hard, contested, safety-critical* cases.

---

## 5. Scenarios & stories

The technique in one breath: collect real clinical situations, decide in advance what a good answer must contain (a rubric), grade candidate models against that rubric, and get a number you can defend. The craft is almost entirely in the **construction** — where the cases come from, who wrote the rubric, how you stop the model from having seen the answer key, and who (or what) grades. Get construction wrong and you get a confident number that means nothing.

A cautionary tale everyone cites: a **June 2026 *Nature Medicine* study** found general-purpose models (GPT-5.2, Gemini 3.1 Pro, Claude Opus 4.6) beat two FDA-cleared specialist tools (OpenEvidence, UpToDate Expert AI) on real physician queries (*sourced* — the model lineup and the "FDA-cleared" descriptor are sourced). The popular gloss — that "clearance certifies a tool met *its own* spec, not that it beats the free chatbot a doctor already uses" — is **reasonable commentary from an opinion piece, not a finding of the Nature Medicine paper itself** (*inference*; flagged so you don't quote it as a study result).

### When it's the RIGHT tool

**1. The startup that thinks its discharge-summary model is ready.** A documentation startup has a slide reading "92% on MedQA." A new head of clinical safety kills it: MedQA tests whether the model *knows* metformin is first-line for type-2 diabetes — fact recall — and says nothing about whether a *generated discharge summary* is accurate, complete, and safe to hand a patient. She builds the right stick: 400 real de-identified admissions across the actual case mix, each with a hospitalist-written rubric (*must list active meds with doses; must flag the pending lab; must not invent a follow-up that wasn't scheduled; must read at 8th-grade level*). First run: 41% of summaries hallucinate a follow-up. That number is *useful* in a way "92% on MedQA" never was, because each failure points at a fixable behavior. **A bespoke, rubric-based, task-realistic benchmark on your own distribution — the technique working as intended.**

**2. Choosing between two vendors with impressive brochures.** A 600-bed health system weighs a cleared clinical-reference tool against a frontier general model behind its firewall. Both wave benchmark numbers. Procurement takes 300 real questions their physicians actually asked last quarter, writes rubrics with their own specialists, and grades both blind — and finds, as the Nature Medicine study did, that clearance guarantees a tool met a spec, not that it beats the alternative on *their* queries. **A head-to-head eval on real local queries is the right call; brochure numbers answer a different question.**

**3. Catching the model that's secretly memorizing.** A group keeps seeing suspiciously strong scores from a fine-tuned model. They run it against a *live* benchmark (fresh, post-cutoff cases harvested continuously). On the post-cutoff slice the score **degrades measurably — typically by a few points** (LiveMedBench reports 84% of models, 32 of 38, degrading, with the most pronounced single drop only ~3.99%; correction applied — this is a real, statistically meaningful contamination *fingerprint*, not a dramatic crash). **A contamination-aware, temporally-separated benchmark is the honest way to measure reasoning rather than recall.**

**4. Pre-deployment safety gate for a high-risk behavior.** A telehealth company adds a triage chatbot. Before launch, clinicians red-team the dangerous edge cases — the chest-pain-in-a-30-year-old that's easy to wave off, the drug interaction buried in a med list — and deliberately over-sample difficulty (HealthBench Professional enriched hard cases ~3.5×). **For a safety gate, oversampling difficulty is correct: you're not estimating average performance, you're hunting the failure that ends up in a lawsuit.**

### When it's the WRONG tool

**1. Reporting the benchmark score as the real-world success rate.** A marketing team takes a difficulty-enriched safety benchmark (60% of cases chosen *because* they're hard) and announces "our AI scores 70%, so it's right 70% of the time for patients." Category error: when you stratify toward difficulty, the score is a *relative progress meter*, not a population accuracy rate. **For population performance you want a representative prospective sample, not an adversarial one.**

**2. Trusting one LLM judge on a genuinely contested question.** A team grades a mental-health chatbot's "empathy" and "completeness" with a single LLM judge and treats the output as ground truth. But on a meaningful share of cases — roughly a fifth of HealthBench cases — *physicians themselves disagree*. The judge hits good agreement (~0.80 with clinician consensus) yet inherits biases (favoring longer answers) and hands you crisp precision on a question with no crisp answer. **Where the clinical judgment is contested, a single automated judge manufactures false precision; use multi-rater human adjudication, report disagreement, and treat the LLM judge as *one* rater.**

**3. Substituting any benchmark for a prospective trial.** A device maker wants to claim it *improves outcomes* and points to benchmark wins. Wrong instrument. A benchmark measures whether a clinician would rate the answer well in a quiet room with unlimited time; it cannot tell you whether, inside a real EHR workflow with alert fatigue and a rushed nurse at 3 a.m., the tool changes what happens to patients. **For outcome claims you need prospective study; FDA is building real-time-trial pilots precisely because static evidence isn't enough.**

**4. Heavyweight bespoke eval for a trivial, checkable task.** A team spends three months and a clinician panel to test whether a model can extract a patient's age and listed allergies from a structured form. That's deterministic fact extraction — a handful of unit tests and exact-match accuracy answers it in an afternoon. **Reserve rubric eval for open-ended, judgment-laden outputs where there's no single right string.**

**5. Validating on a public benchmark a model was likely trained on.** A group fine-tunes on web-scraped medical text, then validates on a popular *public* benchmark and reports a great score to a regulator. The benchmark is almost certainly in the training corpus; the score measures memorization. **For a model whose training data plausibly swallowed the test, use a held-out or live, contamination-controlled set.**

### The judgment call (advisory)

The rule that separates the columns: **ask what question the number will actually answer.**
- "Which model behaves better on *our* real cases?" → rubric benchmark on your distribution. Right.
- "Safe enough to ship?" → adversarial, difficulty-enriched eval. Right, but report it as a stress test, not an accuracy rate.
- "Does it help patients?" → prospective trial. Benchmarks are the wrong tool, full stop.
- "Is the answer objectively checkable?" → unit tests / exact match. Don't summon a clinician panel.
- "Could the model have seen the answers?" → if yes, no public static benchmark is trustworthy; go live/held-out.

And one governance point, bluntly: a benchmark is only as honest as its construction. Who wrote the cases, who wrote the rubric, whether the cases postdate training, who grades, and how disagreement is handled — those choices decide whether your number is evidence or theater.

---

## 6. Cross-industry usage & positioning (as of June 2026)

The technique started in medicine, and medicine is still where the methodology is most mature — but the *construction recipe* has spread to finance, law, coding, defense, and science. The recipe has five moving parts, and almost every serious 2026 benchmark in any domain uses some version of all five:

1. **Realistic tasks, not trivia** — messy, multi-turn, real-world workflows (a full consult, a 10-K analysis, a GitHub issue).
2. **Expert-authored rubrics** — decompose a good response into many independently-checkable criteria, each written and reviewed by domain experts.
3. **An automated grader (LLM-as-judge)** — a model checks each response against each criterion, so you can score thousands of open-ended answers cheaply.
4. **Validation of the grader itself** — prove the auto-grader agrees with human experts before trusting it. This is the step amateurs skip.
5. **Contamination resistance** — make sure the test wasn't in training data, increasingly by refreshing with material that postdates training cutoffs.

The big shift since ~2024: the field stopped treating benchmarks as static answer-keys and started treating them as **rubric-graded, expert-validated, living measurement instruments**. Medicine led; everyone copies the template.

**The clinical state of the art.** **HealthBench** defined the modern playbook (5,000 multi-turn conversations, 48,562 criteria, 262 physicians, axis-tagged). **HealthBench Professional** (2026) is the current frontier (525 tasks from 15,079 candidates, three-stage rubric process, ~3.5× hard-case enrichment); its headline result — **GPT-5.4 tuned for clinicians scored 59.0 vs. 43.7 for physicians** given internet access and unlimited time — captures the single most important positioning fact of 2026: **general-purpose frontier models now out-*evaluate* purpose-built clinical AI on clinical benchmarks.** **MedHELM** (Stanford-led) is the breadth complement — 121 clinical tasks (expanded to a 37-benchmark suite) in a clinician-validated taxonomy — and its key finding (models far more variable on realistic tasks than on licensing exams) is why nobody serious cites USMLE scores as readiness evidence anymore.

**Three live clinical frontiers:**
- **Agentic / EHR-grounded eval.** PhysicianBench (2026) runs agents inside a FHIR-compliant simulated EHR on 100 long-horizon, physician-authored tasks across 21 specialties; the best agent (GPT-5.5) completes only **46.3% of tasks** (pass@1) (*sourced*). Reported sibling figures (Claude Opus 4.6/4.7 ~32%/29%, best open-source ~19%) are **lower-confidence** (not independently confirmed). MedAgentBench (NEJM AI) and AgentClinic are sibling efforts. The gap between "answers questions well" and "operates a workflow safely" is enormous.
- **Contamination-free / live benchmarks.** LiveMedBench (2026) continuously harvests fresh cases so test material postdates training cutoffs, with automated rubric grading.
- **Grader validation as a first-class concern.** Smaller, cheaper models can now match individual-physician rubric grading, so the judge is no longer the bottleneck — but *contamination of the judge* (preference leakage, self-preference bias) is a recognized, actively-studied failure mode.

**Cross-industry map (who leads, how mature):**
- **Finance — cutting-edge, fast-maturing.** FinBen/FinanceBench (36 datasets, 24 tasks). **PRBench (Scale AI Labs)** is explicitly modeled on the clinical rubric playbook, with the validation step done right: independent experts agreed 93.9% on rubric validity, and the LLM judge hit ~80.2% agreement with humans, matching the ~79.6% human-human agreement (*sourced* — this triplet is well-supported). That "judge ≈ human agreement" number is borrowed straight from HealthBench.
- **Legal — table-stakes for QA, cutting-edge for reasoning/agentic.** LegalBench (162 tasks, 40 lawyers/professors), LegalBench-RAG (retrieval-focused), LegalAgentBench. Stanford, Scale, vals.ai, and vendors (Harvey, Thomson Reuters) lead.
- **Coding — most mature agentic eval outside medicine.** SWE-bench / SWE-bench-Live and LiveCodeBench continuously harvest fresh issues — *ahead* of medicine on the live-benchmark axis. Anthropic publicly recommends mixing deterministic unit tests with LLM rubrics.
- **Customer support / general assistants — table-stakes, commoditized.** Rubric-decomposed LLM-as-judge is standard tooling; the methodology is operational, not novel.
- **Safety / cross-domain — emerging.** TRIDENT benchmarks safety jointly across finance, medicine, and law.
- **Defense, robotics, consumer, science — earlier-stage.** These lean on task-success metrics and simulation; the expert-rubric tradition is least penetrated here, though science is moving toward rubric-graded research-reasoning eval.

**Table-stakes vs. cutting-edge (positioning summary):**

| Capability | Status in 2026 |
|---|---|
| Rubric decomposition + LLM-as-judge | **Table-stakes** in medicine, finance, legal, support, coding |
| Expert-authored, peer-reviewed rubrics | **Table-stakes for credible** clinical/legal/finance benchmarks |
| Validating the judge against human agreement | **Becoming table-stakes**; still a differentiator — many skip it |
| Contamination-resistant / live refresh | **Cutting-edge** in medicine; **most mature in coding** |
| Agentic / environment-grounded eval | **Cutting-edge everywhere**; coding leads, medicine close behind |
| Triangulating static eval + human arena + agentic suite | **Best-practice frontier** — agreement across all three is the strongest signal |

**Advisory for builders/buyers:** (1) Steal the medical recipe wholesale — recruit real experts and do the validation step honestly. (2) The validation-of-the-judge step is the integrity test; demand the ~80% judge-vs-human number from vendors. (3) Static exam scores are dead as readiness evidence — insist on agentic, environment-grounded evals and expect sobering pass rates (the ~46% PhysicianBench ceiling is the honest picture). (4) Budget for a live/refreshable component. (5) Generalist > specialist is now the default prior; justify any vertical model by what the *evals* show, not by branding. (6) Triangulate.

---

## 7. Learning path for a technical leader

For a smart non-implementer who must direct, fund, and judge this work. Concepts only, no coding. SOTA claims are *sourced*; learning-design and org calls are *advisory*.

**What you are learning to do:** design tests whose score *means* something about real-world behavior, that the model can't have memorized, and that an expert would defend. The medical setting removes any excuse for sloppiness, because a wrong measurement means a harmed patient.

**Core mental models:**
- **M1 — A benchmark is an instrument with validity AND reliability, independently.** A benchmark can be perfectly reliable and totally invalid (consistently rewarding confident-but-wrong answers). The reliable-invalid one is the more dangerous to ship on, because it fools you confidently.
- **M2 — The score is a proxy; the gap between proxy and reality is the real risk.** Constantly ask: *what's the gap between what we measured and what we'll deploy, and who gets hurt in it?*
- **M3 — Contamination is the default.** Public benchmark ⇒ assume the model saw it; strong scores then mean memory, not reasoning. Measured, not theoretical: **84% of models degrade on post-cutoff cases** (*sourced*) — though typically by a few points, a real fingerprint rather than a crash (correction applied).
- **M4 — Competence doesn't transfer across context; validate the *coordinate*, not "the model."** Competence lives in a grid (condition × setting × provider role × task × who the AI talks to × authority level). Proving one cell is *minimal* evidence for any other (*sourced*). Ask: *in which configurations is reliability shown, and for whom?*
- **M4b — Generic frontier models are now the baseline to beat.** A June 2026 *Nature Medicine* study found general-purpose frontier models outperformed specialized/FDA-cleared clinical tools across knowledge, alignment, and real physician queries (*sourced*). Any "medical-specialized" vendor must prove it beats a plain frontier model on *your* tasks.
- **M5 — Rubrics turn "good answer?" into many checkable facts.** Decompose quality into weighted **binary (MET/UNMET)** criteria tied to behaviors clinicians care about; binary gives the highest inter-rater reliability (*sourced*).
- **M6 — Your grader is itself a model that needs evaluating.** Judges have biases (verbosity, self-preference, position) and can share blind spots with the model judged. Non-negotiable: **meta-evaluation** — measure judge-vs-clinician agreement before trusting any score (*sourced*).
- **M7 — Ground truth is a clinician, but clinicians disagree.** "Ground truth" is constructed: multiple raters, an agreement statistic (Cohen's/Gwet's/Krippendorff), adjudication. A score reported without its raters' inter-rater agreement is hiding its noise floor.
- **M8 — Evidence hierarchy: exam → static benchmark → live/contamination-free → silent prospective trial → outcomes.** Each rung is closer to reality and costlier. The strongest pre-deployment evidence is a **silent prospective run** on live cases with output hidden from care, scored against what actually happened. Always know which rung a claim sits on.

**Sequenced concept progression:** validity vs. reliability → construct & proxy gap → evidence hierarchy → contamination & leakage → task taxonomy & realism → rubric construction → LLM-as-judge & its bias catalogue → meta-evaluation of the judge → human ground truth & inter-rater agreement → coordinate-specific validation → agentic/multi-turn eval → drift / living benchmarks → deployment & regulatory evidence (silent trials, post-market monitoring, FDA lifecycle/PCCP). *Steps 1–4 are literacy (have cold); 5–9 construction (enough to commission/critique); 10–13 judgment (enough to decide deployment).* (*advisory* sequencing)

**The reading spine (~7 anchors, in path order):**
- **A. HealthBench (OpenAI, 2025)** — the whole machine; 5,000 dialogues, 262 clinicians, 48,562 criteria, GPT-4.1 judge at macro F1 ≈ 0.71.
- **B. "HealthBench: not yet clinically ready" (PMC)** — your skepticism vaccine: synthetic-only, shared judge/model blind spots, no outcomes.
- **C. MedHELM (Stanford, Nature Medicine 2025)** — the realistic-task taxonomy anchor.
- **D. LiveMedBench (arXiv 2026)** — contamination-free / living benchmark; 84% post-cutoff degradation; the automated rubric grader reaches **0.76 macro F1**, versus a weak **~0.26 correlation (non-significant, p=0.07)** for a plain LLM-judge (correction applied — these are different metrics, *not* an F1-vs-F1 comparison).
- **E. Clinical World Model & Skill-Mix (arXiv 2026)** — the strategic anchor: competency dimensions, non-transferable validation.
- **F. "Reliability without Validity: LLM-as-a-Judge" (arXiv 2026)** — judge discipline: chance-corrected agreement, position/verbosity/self-preference bias.
- **G. "General-purpose LLMs outperform specialized clinical AI tools" (Nature Medicine, June 2026)** — current landscape plus a clean 3-stage eval template (12 blinded clinicians, ~1,800 annotations).
- *Optional:* an FDA AI/ML lifecycle/PCCP one-pager (verify on fda.gov).

> *Advisory:* stop at seven-plus-one. The field ships a benchmark weekly; chasing them is the analyst's job. Re-skim D and G quarterly — they decay fastest.

**Understanding checkpoints — you understand it when you can:** name a reliable-but-invalid benchmark and say why it's the more dangerous to ship on; take any result and instantly name the three biggest things it did *not* measure; explain why a 97% exam score can be worthless and two ways to build an unmemorizable benchmark; explain why "rate 1–10" loses to twelve weighted MET/UNMET checks; name three judge biases and the one gating question ("chance-corrected agreement with clinicians on *this* task?"); explain why "the doctors agreed" is meaningless without an agreement *statistic* and more than one rater; rewrite "the model is validated" as condition/setting/task/user/authority-specific; rank any vendor claim on the exam→static→silent-trial→outcomes ladder in seconds. **Capstone:** hand them "our AI scores 94% on medical benchmarks." Unprompted, they should ask: public or held-out? contaminated? which tasks/populations? graded by whom, agreeing how well with clinicians? versus a plain frontier model? which rung of the evidence ladder?

**How to evaluate an expert (interview kit, *advisory*).** The aim is to tell someone who has *built and defended an instrument* from someone who only *runs* other people's benchmarks. The tell: do they treat the benchmark as the object of suspicion, or as truth?
- *"Vendor scores 95% on a public medical QA benchmark — how much do you trust it?"* Strong: instantly raises contamination, asks for held-out/post-cutoff results, separates exam from real-task, asks who graded and the grader-clinician agreement, asks for the frontier-model baseline. Red flag: ranks models by leaderboard; can't articulate contamination.
- *"Build a benchmark for ambient note generation / triage."* Strong: starts from real-workflow "what good looks like," decomposes into a weighted binary rubric across axes, sources realistic de-identified post-cutoff cases, plans a grader *and* a plan to validate it against clinicians, names sample size and subgroups, picks the right evidence rung. Red flag: single overall score, no criteria, no human anchor.
- *"You're LLM-grading 40,000 responses — convince me the grades are trustworthy."* Strong: meta-evaluation on a clinician-labeled subset with *chance-corrected* agreement (not raw exact-match), names judge biases and mitigations, flags shared blind spots when judge ≈ subject. Red flag: "we spot-checked and it looked right."
- *"Validated for sepsis in our ICU; marketing wants a general-ward sale."* Strong: refuses the leap on principle (coordinate-specific validation), demands fresh prospective ward evaluation and subgroup performance. Red flag: "same model, so it's validated."
- *"Benchmark score vs. evidence it's safe to deploy?"* Strong: full evidence ladder; strongest pre-deployment = silent/prospective run against real outcomes plus drift monitoring; benchmark necessary-not-sufficient. Red flag: passing benchmark = safe.
- *Green flags overall:* reflexively suspicious of every number including their own; talks in terms of what the score *fails* to capture; treats the grader as a system to be evaluated; thinks in coordinates ("for whom, in what setting"); has opinions on drift and refresh cadence.

---

## 8. Team notes

**What this is, for staffing purposes.** Building the measuring stick before you build or buy the model. In 2026 "eval" no longer means "run it on MedQA." It means assembling realistic cases, writing fine-grained rubrics tied to each case, deciding who grades (physicians, an LLM judge, or both), and maintaining the whole thing as a living asset that resists contamination and tracks real patient-facing risk. HealthBench Professional — 190 physicians, 50 countries, 26 specialties, per-case rubrics weighted −10 to +10, three-stage review — is the bar now (*sourced*).

**Which roles you need.** The honest answer: this is **two distinct skill bundles that get conflated, and the conflation is the #1 staffing mistake.**
- **Bundle A — Clinical content & rubric authorship.** Medical judgment: what counts as a correct, safe, defensible answer; what's a "meaningful flaw." This cannot be absorbed by an ML engineer, ever. It needs **practicing or recently-practicing clinicians** — a small bench (3–8) spanning the specialties your product touches, not one token MD. Attending-level for adjudication; residents/fellows are fine and cost-effective for first-pass case generation (HealthBench used exactly this tiered mix) (*inference* from sourced methodology).
- **Bundle B — Eval engineering & psychometrics.** Building the harness, the LLM-judge pipeline, contamination checks, slicing scores by demographic and case type, measuring grader reliability (Cohen's κ), and keeping the benchmark from rotting. A **mid-to-senior ML/eval engineer with a measurement mindset** — instinct past accuracy. The blunt 2026 hiring signal: "AUROC alone gets you cut from any serious clinical AI process" (*sourced*).

**Does an existing role absorb it?** (*advisory*) A **clinical informaticist** can *own the program* (coordinate the clinician bench, translate clinical needs into rubric structure, manage regulatory framing) but usually can't build the harness. A strong **applied ML/eval engineer** absorbs Bundle B; clinical adds rubric tooling and compliance slicing, not a new hire. **You almost never need a net-new full-time "clinical eval scientist" to start.** Minimum viable team: **one eval engineer (existing or hired) + a fractional contract clinician bench + a clinical informaticist or clinical PM to run the program.** A dedicated full-time clinical eval lead is justified only once eval is your durable differentiator. Resist the expensive roles early: the 2026 market sells Chief Medical AI Officers at $320K–$720K (*sourced*); for eval construction specifically these are premature. The cited guidance — "two senior clinical AI engineers and a fractional governance advisor rather than immediately hiring a Chief Medical AI Officer" — generalizes well (*sourced* / *advisory*).

**Hiring signals & red flags.**
- *Green (engineer):* talks about **rubric decomposition** and why it matters; has measured **LLM-judge vs. human agreement with κ**, not eyeballed it, and knows "model-grader agreement ≈ physician-physician agreement" is a claim that must be **re-verified per domain**, not assumed; unprompted concern about **contamination and temporal drift** (~84% of models degrade on post-cutoff cases); **slices results by subgroup**.
- *Green (clinician):* writes self-contained, standard-grounded criteria ("must mention X contraindication") rather than vague preference; distinguishes a stylistic nitpick from a **patient-safety flaw** and defends the line.
- *Red:* leads with leaderboard numbers ("we hit 92% on MedQA"); thinks LLM-as-judge is free and unbiased; treats a single clinician as ground truth with no adjudication; conflates eval (writing the rubric, sourcing cases) with monitoring/observability (wiring a dashboard).

**Build vs. buy (default: rent/buy).** (*advisory*)
- *Buy/rent — not a moat:* the harness, observability, audit trails, compliance plumbing (HIPAA-aligned tooling now gives immutable audit logs, demographic-sliced monitoring, self-hosting, an FDA-SaMD evidence trail) (*sourced*); public/standard benchmarks (MedHELM, HealthBench, LiveMedBench) as a *floor* — they tell you "not obviously broken," not "safe for my patients"; LLM-judge infrastructure and rubric tooling.
- *Build/own — the real moat:* **your private, domain-specific, contamination-free eval set tied to your actual workflow and patient population** — the one thing no vendor has and no competitor can copy; **the clinician relationships and adjudication process** that keep it current (medical knowledge drifts; maintenance is ongoing labor, *inference*).
- *Litmus test:* if a capability appears on a vendor's product sheet, rent it. If it requires *your* clinicians' judgment about *your* use case, own it.

**Common failure modes:**
1. **Contamination / saturation** — test cases leak into training; scores inflate; the tell is performance dropping on post-cutoff cases. Mitigate with live/refreshed benchmarks and time-partitioned holdouts.
2. **Optimizing the proxy** — tuning to the benchmark; the model aces the test and is no better at care. Eval becomes theater.
3. **Trusting the LLM judge blindly** — cheap and scalable, but biased and non-reproducible on coarse criteria; failure mode is replacing physician graders without validating agreement on *your* rubric, then discovering the judge rewards confident-sounding wrong answers.
4. **One-clinician ground truth / no adjudication** — inter-rater reliability never measured. Notably, even HealthBench Professional did not publish formal κ between reviewers despite its multi-stage process, so don't assume a famous benchmark has solved this (*sourced*).
5. **MCQ tunnel vision** — measuring recall (is metformin first-line?) while the product needs reasoning under ambiguity, multi-turn dialogue, history-taking.
6. **Building the harness instead of the dataset** — effort flows to impressive, rentable infrastructure while the genuinely hard, moat-worthy work (sourcing cases, writing rubrics) gets shortchanged.
7. **Eval as a one-time gate, not a living system** — built for a launch, never maintained as model and medicine both evolve; decays silently.
8. **Compliance bolted on late** — the EU AI Act classifies AI-enabled medical devices as high-risk and FDA is tightening under QMSR/ISO 13485; evals built without demographic slicing and audit trails must be rebuilt to be defensible. Design for the evidence trail from day one (*sourced*).

**Bottom-line staffing recommendation (*advisory*):** Start with one eval engineer (likely existing) + a fractional contract clinician bench + a clinical informaticist/PM to run it. Buy the harness and compliance tooling. Own — and eventually staff full-time around — your private clinical benchmark, because that dataset is the only part competitors can't rent. Don't hire a Chief Medical AI Officer to build evals; that title is for governance scale, not benchmark construction.

---

## Sources

- HealthBench (OpenAI, May 2025): scale, 262 clinicians/60 countries, 48,562 criteria, axes/themes, Consensus/Hard subsets, weights −10..+10, grader macro F1 ≈ 0.709 — https://openai.com/index/healthbench/ ; https://arxiv.org/pdf/2505.08775 ; https://www.emergentmind.com/topics/healthbench (accessed 2026-06-25)
- HealthBench Professional (arXiv, Apr 2026): 525 from 15,079; 190 physicians/50 countries/26 specialties; 3-stage review; GPT-5.4 ChatGPT-for-Clinicians 59.0 vs physician 43.7; length penalty — https://arxiv.org/abs/2604.27470 ; https://arxiv.org/html/2604.27470v1 ; https://cdn.openai.com/dd128428-0184-4e25-b155-3a7686c7d744/HealthBench-Professional.pdf (accessed 2026-06-25)
- "Not yet clinically ready," synthetic-data limits, ~95% non-real-patient data, silent-mode trials — PMC12547120: https://pmc.ncbi.nlm.nih.gov/articles/PMC12547120/ (accessed 2026-06-25)
- Physician disagreement decomposition (rubric ~3.6–6.9%, physician ~2.4%, ~81.8% case-level residual, quality-boundary inverted-U) — https://arxiv.org/pdf/2602.22758 (accessed 2026-06-25)
- LLM-judge speed (~22s vs ~600s human), reliability — Nature *npj Digital Medicine*: https://www.nature.com/articles/s41746-025-02005-2 ; PMC12589481 (accessed 2026-06-25)
- Judge bias — "Neither Valid nor Reliable?" https://arxiv.org/pdf/2508.18076 ; "Reliability without Validity" https://arxiv.org/html/2606.19544 (accessed 2026-06-25)
- Automated rubric generation — Autorubric https://arxiv.org/abs/2603.00077 (unified eval framework); RubricHub https://arxiv.org/pdf/2601.08430 ; Automated Rubrics for Medical Dialogue https://arxiv.org/abs/2601.15161 ; Scalable Stewardship https://arxiv.org/pdf/2512.19691 (accessed 2026-06-25)
- LiveMedBench (live/contamination-free; 84% of 38 models degrade, max single drop ~3.99%; rubric grader 0.76 macro F1 vs ~0.26 non-significant correlation for plain LLM-judge) — https://arxiv.org/abs/2602.10367 ; https://arxiv.org/html/2602.10367v1 (accessed 2026-06-25)
- MedGemma 1.5 / MedQA ~88–91% depending on variant (27B text variant 87.7%); MedGemma 1.5 Technical Report reports ~5% improvement over predecessor — https://arxiv.org/abs/2604.05081 ; secondary landscape: nirmitee.io; https://www.emergentmind.com (accessed 2026-06-25)
- MedHELM — https://medhelm.org/ ; Nature Medicine 2025: https://www.nature.com/articles/s41591-025-04151-2 (accessed 2026-06-25)
- PhysicianBench (GPT-5.5 46.3% pass@1, 100 tasks/21 specialties; sibling figures lower-confidence) — https://arxiv.org/abs/2605.02240 ; https://healthrex.github.io/PhysicianBench/ (accessed 2026-06-25)
- MedAgentBench (NEJM AI) — https://ai.nejm.org/doi/full/10.1056/AIdbp2500144 (accessed 2026-06-25)
- General-purpose vs specialized/FDA-cleared clinical AI (Nature Medicine, June 2026; GPT-5.2, Gemini 3.1 Pro, Claude Opus 4.6 vs OpenEvidence/UpToDate Expert AI) — https://www.nature.com/articles/s41591-026-04431-5 ; "FDA-cleared" descriptor + clearance-vs-spec gloss (commentary): clinicaltrialvanguard.com (accessed 2026-06-25)
- PRBench Finance/Law (judge ~80.2% agreement, human-human ~79.6%, rubric validity 93.9%) — https://labs.scale.com/leaderboard/prbench-legal ; https://arxiv.org/abs/2511.11562 (accessed 2026-06-25)
- FinBen / LegalBench / domain benchmark map — https://kili-technology.com/blog/domain-specific-llm-benchmarks-guide ; LegalAgentBench review; TRIDENT https://arxiv.org/pdf/2507.21134 (accessed 2026-06-25)
- SWE-bench-Live / LiveCodeBench (contamination resistance) — https://arxiv.org/pdf/2505.23419 (accessed 2026-06-25)
- Clinical World Model / Skill-Mix (coordinate-specific validation) — https://arxiv.org/abs/2604.08226 (accessed 2026-06-25)
- DRAGON (28,824 reports, 28 tasks, 5 centers) — PMC12084576 (accessed 2026-06-25)
- Healthcare AI observability/compliance tooling, hiring bands, FDA AI/ML SaMD lifecycle/PCCP/QMSR, EU AI Act high-risk classification — https://intuitionlabs.ai/articles/fda-ai-ml-samd-guidance-compliance ; https://www.confident-ai.com/knowledge-base/compare/best-ai-observability-tools-for-healthcare-companies-2026 ; https://www.kore1.com/healthcare-ai-hiring-2026/ ; https://www.digitalapplied.com/blog/llm-benchmark-methodology-2026-contamination-leaderboard-guide (accessed 2026-06-25)
- Rubric-based eval / LLM-as-judge methodology — https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80 ; Agentic Benchmark Checklist: https://openreview.net/forum?id=E58HNCqoaA (accessed 2026-06-25)
