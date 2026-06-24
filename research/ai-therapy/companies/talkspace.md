# Talkspace — Company Dossier

**One-line:** A profitable, payer-pivoted virtual behavioral-health platform (Nasdaq: TALK; pending UHS acquisition for ~$835M) layering a fine-tuned, clinically-supervised LLM ("Tee") on a human-therapist core. The differentiation is proprietary clinical data plus safety/clinical-integration engineering — not novel ML.

**Verifier overall confidence: high.** Labels below: **[sourced]** = directly evidenced; **[inference]** = reasoned from evidence; **[speculation]** = plausible, weak/no direct evidence; **[contested]** = sources disagree; **[unsupported]** = claim does not trace to its cited source. Where a fact was not found, it is marked "unknown — not found."

---

## Dimension 1 — Company journey / history

- **[sourced]** Founded **2012** in NYC by married couple **Oren Frank** (ex-advertising, McCann Worldgroup/MRM) and **Roni Frank** (CS degree, ex-Amdocs software developer, later a psychotherapy/psychoanalysis master's), inspired by their own couples therapy.
- **[sourced]** Pioneered text-based subscription teletherapy; added **live video/audio (2015)** and **psychiatry (2016)**; expanded into employer/health-plan partnerships (~2018).
- **[sourced]** Went public via **SPAC merger with Hudson Executive Investment Corp**; merger completed **June 22, 2021**, trading on Nasdaq as **TALK** from June 23, 2021, at ~$1.4B initial enterprise value and ~$250M cash.
- **[sourced]** Both founders departed in **2022** after worse-than-expected post-IPO results. Douglas Braunstein served as interim CEO; **Dr. Jon R. Cohen** (ex-BioReference Laboratories / OPKO Health) was named permanent CEO **Nov 8, 2022**, leading a turnaround that pivoted from consumer-first to a B2B/payer model (with layoffs).
- **[sourced]** Reached profitability and growth by 2024–2025.
- **[sourced]** **March 9, 2026:** Universal Health Services (UHS) agreed to acquire Talkspace for **~$835M ($5.25/share)**; expected to close Q3 2026.
- **[sourced / date-corrected]** Launched consumer AI agent **"Tee" on June 9, 2026** — fulfilling the H1-2026 conversational-AI roadmap. *Verifier correction: an earlier finding's "June 22, 2026" date is wrong/stale (it conflated the IR-page access date / SPAC anniversary). Every independent source — BusinessWire slug 20260609, Yahoo, StockTitan, Inc. — dates the announcement June 9, 2026.*

---

## Dimension 2 — Tech stack & architecture

- **[sourced]** Conventional teletherapy SaaS: web + iOS/Android apps for text/audio/video sessions, scheduling, insurance/EAP billing. Public detail on the core stack is thin.
- **[sourced]** Job postings call for **React + Node.js + TypeScript + AWS** full-stack engineers, indicating a JS/TS web stack (and independently confirming AWS in the stack).
- **[inference / weak — effectively unsupported]** Mobile apps use **React Native**. *No source confirms this; it is a plausible inference from a JS/TS web stack but evidence is nil. Treat as weak/unsupported.*
- **[sourced]** Strategic cloud/AI partner is **AWS**: Talkspace is co-developing a "foundational safety and quality AI model" with the **AWS Generative AI Innovation Center** to score therapy sessions for clinical quality and risk.
- **[speculation]** Talkspace uses **AWS Bedrock** for production LLM inference. *AWS partnership is confirmed; "Bedrock for inference" specifically is searched-and-not-found. Speculation.*
- **[inference]** Architecturally, the AI layer sits **on top of**, not replacing, the human-therapist platform. Provider-facing AI (Smart Notes, Insights, Talkcast, risk alerts) feeds clinicians; the direct-to-consumer **Tee** agent is a separate conversational product with human-in-the-loop escalation.
- Specific inference infrastructure (e.g., Bedrock confirmation): **unknown — not found.**

---

## Dimension 3 — AI/ML techniques & models

- **[sourced]** The central, well-corroborated fact: Talkspace is **fine-tuning / domain-adapting LLMs on proprietary data, NOT pretraining a foundation model from scratch.** The official Tee announcement describes it verbatim as "a safe, fine-tuned large language model developed by mental health experts."
- **[sourced — company claim]** **Proprietary training data:** de-identified clinical data from "millions of therapeutic interactions" over ~12 years, claimed the "largest behavioral health datasets in the industry" (more specific figures surfaced in search: ~140M anonymized messages, 6.2M assessments, 1.2M diagnoses, 4.3M notes). *The "largest in industry" superlative is an unverified marketing claim.*
- **[sourced — company-run internal test, not independently verified]** Reported fine-tuning gains vs the base model: **50%** better at identifying/responding to high-risk behaviors, **47%** higher therapeutic-quality score (Cognitive Therapy Rating Scale), **3x** higher user satisfaction. *No methodology, sample size, or base-model identity disclosed; should not be cited as established performance facts.*
- **[sourced — sourced negative]** The **base model identity** (Llama / Claude / other) is **not publicly disclosed** — unknown — not found.
- **[sourced]** **Risk/safety model:** an NLP suicide-detection classifier reporting **AUC 82.78 at the individual sentence level**. Tee detects suicide, homicide/violence, abuse, and seven other risk entities — **10 total**.
  - **[unsupported]** The claim that the algorithm is now **"92% accurate, up from 83%"** does **not** appear on the cited talkspace.com/ai-at-talkspace page (which cites only AUC 82.78) nor in the 2023 source (which framed 83% accuracy vs a human expert). The "92%" appears conflated with unrelated third-party academic studies. **Dropped / downgraded.**
  - **Metric note:** AUC 82.78 (a ranking metric, sentence-level) and "83% accuracy vs human expert" are **distinct measurements** repeatedly blended in source material — do not treat as interchangeable.
- **[speculation]** The risk-detection classifier is a **transformer / BERT-RoBERTa-class** model. *Pure domain inference; the original 2020 model predates the BERT-dominant era and may use simpler NLP. Architecture undisclosed → speculation.*
- **[sourced]** **Guardrails/oversight:** real-time licensed-clinician oversight with immediate human handoff, "algorithmic blockades" that trigger clinician step-in, under-18 exclusion, and a pre-access clinical self-harm/suicidal-ideation screen.
- **[inference]** **Evals** function as domain-specific clinical scoring (CTRS therapeutic-quality, risk-detection accuracy) plus the AWS-built safety/quality model — effectively LLM-as-judge-style session scoring.
- **[sourced — sourced negative]** Whether Talkspace uses **RLHF and/or RAG** is **not stated** in public sources — unknown — not found.
- **[sourced]** **Timeline:** Tee/LLM in beta through early 2026; full DTC launch targeted H1 2026 / "this summer" (Q2 2026), realized as the **June 9, 2026** launch. CEO Cohen floated **licensing the LLM to third parties** (8–10 use cases discussed on the Q2 2025 call) as possible but TBD.

---

## Dimension 4 — Therapeutic approach, modalities, technique encoding, human-in-the-loop

- **[sourced]** Fundamentally a **human-therapist teletherapy platform**: all therapeutic communication comes from licensed providers. Offers text/messaging, live video/audio, and psychiatry. **Modality-agnostic** — spans CBT, ACT, psychodynamic, grief counseling, and general talk therapy; matches members to licensed clinicians rather than encoding one technique into software.
- **Is technique "encoded"?** Largely **NO** for the core product — technique lives in the human therapist. Talkspace explicitly positions AI as supporting, not replacing: "AI doesn't replace human therapists… AI is used to strengthen the human-centered therapeutic relationship," and "All therapeutic communication comes directly from a trained, licensed provider."
- **[sourced]** Where AI touches clinical technique, it is **provider-facing tooling**, described as optional, editable, and under the therapist's control:
  - **Smart Notes** — automated session-documentation summaries.
  - **Insights / Smart Insights** — pre-session primer and post-session update synthesizing the client's care journey.
  - **Talkcast** — AI generates a personalized "podcast" episode from a **therapist-reviewed script** tied to therapy objectives.
- **[sourced]** **The exception — Tee:** a consumer-facing fine-tuned LLM built from "proprietary clinical algorithms, rigorously tested safety features, and proven therapy techniques." This is where technique is most directly encoded in software — but Talkspace explicitly frames Tee as a **wellness "companion/guide," NOT therapy and NOT a clinician.**
- **[sourced]** **Human-in-the-loop** is retained throughout: humans do all core therapy; the suicide-risk AI flags and a human responds; even autonomous Tee has "real-time oversight by licensed clinicians and immediate human intervention by a therapist as needed."
- **[sourced]** Underlying base model/architecture & training methodology for Tee: **not disclosed** — unknown — not found.

---

## Dimension 5 — Safety, crisis handling, clinical evidence, FDA & regulatory status

**Crisis handling (core platform):**
- **[sourced]** A proprietary NLP suicide-risk algorithm scans member messages in real time and triggers an urgent therapist alert on self-harm risk. Tee extends this to 10 risk categories (suicide, homicide/violence, abuse + 7 others — *the other seven are not named in the release*).
- **[sourced]** Talkspace is explicit it is **NOT a crisis/suicide-prevention line**; on detection, therapists have referred members to child protective services, more intensive therapy, or hospitalization (per NYC Teenspace).
- **[sourced — company-stated, unaudited]** **NYC Teenspace** figures (CEO Cohen, Oct 2025): ~40,000 teens served, **over 40,000 suicide alerts**, **500 interventions** to prevent suicide over two years. *Not independently audited; the 40K-alerts-from-40K-teens ratio warrants caution.*

**Tee-specific guardrails (announced June 9, 2026):**
- **[sourced]** **18+ age gate** (under-18s not permitted); **HIPAA** protections; real-time clinician oversight + immediate human intervention.
- **[sourced — partially disclosed]** An **onboarding clinical self-harm/SI screen** that prohibits use on positive history. *This was sourced to Inc. / talkspace.com but was NOT restated in the primary June 9 press release; real but less uniformly disclosed than presented.*
- **[sourced]** Hard disclaimers: Tee "is an AI, not a licensed professional," is not a substitute for clinical care, and "cannot diagnose a mental health condition, provide specialized treatment, or safely handle a crisis or mental health emergency."
- **[contested]** Sources reference "three main guardrails," but the canonical three-item wording sits in a **paywalled trade source** that could not be retrieved. The verifiable trio: 18+ age gate, onboarding self-harm/SI screen, HIPAA monitoring with human escalation.
- **[sourced]** Availability/pricing: 24/7; **7-day free trial then $19.99/month.**

**Clinical evidence / trials:**
- **[sourced]** Suicide-alert algorithm developed with **NYU Grossman School of Medicine**; peer-reviewed work is **Bantilan, Malgaroli, Ray & Hull (2020), "Just in time crisis response," *Psychotherapy Research.*** Reported **~83% accuracy vs human expert** (and AUC 82.78 at sentence level — distinct metrics). Deployed since **2019**.
- **[sourced — company-stated, possibly stale]** Algorithm has flagged **~32,000 members**, with **>50% of those who continued care** showing improved outcomes. *Figures date to 2023; not an RCT of the alert's downstream effect; potentially stale by 2026.*
- **[sourced — sourced absence]** **Tee:** no clinical trials, peer-reviewed efficacy studies, or RCTs disclosed in launch materials. Formal clinical validation is **not published.**

**FDA & regulatory status:**
- **[inference]** Core teletherapy is regulated as a **healthcare service** (state licensure, HIPAA), **not as an FDA-cleared medical device**; no 510(k)/De Novo clearance is claimed for the platform or its AI features. *The wellness-tool framing is sourced; the FDA-clearance absence is an inferred negative, not an affirmative source statement.*
- **[sourced]** Tee is positioned as a **wellness/support tool** that explicitly does not diagnose or treat disease — the framing that keeps it outside FDA SaMD regulation.
- **[sourced]** Talkspace has **engaged with the FDA** on mental-health AI policy (AI should support, not replace, clinicians) and the CEO has commented on **state-level teen-AI-chatbot regulation** (e.g., NY Gov. Hochul's push), to which Tee's age-gating/oversight design partly responds.

---

## Dimension 6 — Engineering difficulty

**Engineering difficulty (3/5).** Above commodity LLM-wrapper work, below frontier research.

- **What makes it non-trivial:** (1) fine-tuning/aligning an LLM on **regulated, de-identified clinical PHI under HIPAA**; (2) a **production real-time multi-entity (10-class) clinical-risk classifier** wired to live human-clinician escalation in a **life-safety domain**, with low-latency intervention — the safety/orchestration layer is harder than the model; (3) the **safety, guardrail, and clinical-validation engineering** that high-stakes mental-health use demands.
- **What caps it:** they are **fine-tuning existing base models, not pretraining**; the surrounding teletherapy platform is **conventional SaaS**; **AWS provides much of the ML infra and a co-built safety model**; the moat is **proprietary data + clinical/safety integration, not algorithmic novelty**. They have run an NLP suicide-risk classifier in production since 2019 (NYU-validated), so the harder parts are crisis-detection reliability at scale and the human-escalation ops layer — substantial systems/safety engineering, **modest research novelty.**
- Integration with the existing payer/EAP platform and ~200M-covered-lives eligibility plumbing adds operational (not research) complexity.

---

## Dimension 7 — Founders, key technical/clinical hires, headcount & org shape

**Founders [sourced]:** Oren Frank (ex-advertising; long-time CEO) and Roni Frank (CS/ex-Amdocs developer, trained in psychoanalysis; led the clinical/provider-network side). **Neither runs the company today.**

**Current top leadership [sourced]:**
- **Jon R. Cohen, M.D.** — CEO (since 2023; board director since Sept 2022); ex-CEO BioReference Laboratories / OPKO Health.
- **Ian Harris** — CFO
- **Gil Margolin** — **CTO** and very-early employee (joined 2014); oversees Software Engineering, Product, Operations — the senior-most surviving technical leader from the original build.
- **John Mooney** — Chief Product Officer; **Natalie Cummins** — Chief Business Officer; **Mary Potter** — Chief Compliance/Privacy/Information Security Officer; **Andrea Cooper** — Chief People Officer; **John Reilly** — Chief Legal Officer.

**Key clinical hire [sourced]:** **Nikole Benders-Hadi, M.D.** — Chief Medical Officer (Oct 2023), board-certified psychiatrist (ex-Included Health); sits on the **AI innovation governance committee** — clinical leadership is wired into AI product governance.

**AI / data org [inference, lower confidence]:** Talkspace stood up a dedicated **AI Innovation Group** [sourced]. Reported leads — **Michael Rodio (GM of AI), Nir Tal (SVP Data Science & Analytics), Katie McCrudden (AI PM), Emily Williams (VP Engineering)** — come from aggregators, not the IR page → treat as inference. **[sourced]** It posted a **Senior AI Engineer** role (Dec 17, 2025) to build autonomous multi-agent LLM systems.

**Headcount & shape [sourced]:** ~**635 FTE (Dec 2025)**, ~642 (2024) — flat-to-slightly-declining corporate headcount — atop a **~6,000-person network of contracted (1099) licensed therapists** across all 50 states + DC + Puerto Rico. **[contested]** Aggregators citing ~1,100–1,180 (LeadIQ, PitchBook) appear to conflate the provider network/LinkedIn profiles and conflict with the company's ~635 FTE figure.

**Major org event [sourced]:** UHS acquisition (~$835M, $5.25/share, announced 2026-03-09, expected close Q3 2026) is a control change; Talkspace becomes the virtual-behavioral-health arm of a ~340-facility hospital operator. **All forward-looking org/headcount/comp conclusions must be caveated by this pending integration.**

---

## Dimension 8 — Compensation bands

Three sources triangulate but disagree materially: **Levels.fyi** runs high (self-selected tech submissions, total comp), **Glassdoor** runs low (broader sample, average), **H1B LCA** is the hard legal floor (base only, dated).

| Role | Levels.fyi (est., total comp) | Glassdoor (est.) | H1B LCA (data, base only) |
|---|---|---|---|
| **Software Engineer** | ~$219K–$225K (high ~$237K) | ~$97K–$140K (avg base ~$116K) | Full Stack $154,900 (2022, Charlotte/Philadelphia); $100K (2021, NY) |
| **Product Manager** | ~$179K (band $146K–$212K+) | ~$100.8K–$197K (avg ~$140.9K) | Senior PM $159,245 (NY 2022); $189,999 (LA 2022) |
| **Data Scientist** | ~$139.3K (band $119K–$167K+) | unknown — not found | $149,000 (Brooklyn NY, 2023) |
| **Marketing** | ~$250K (band $250K–$294K+; small/senior sample) | unknown — not found | unknown — not found |

- **[inference]** The ~$219K vs ~$116K SWE gap reflects total-comp vs average: a mid/senior SWE is likely **mid-$100Ks base** (consistent with H1B $155K in 2022) plus equity/bonus.
- **[sourced]** Therapists/clinical: mostly **1099 contractors paid per-session/per-message**, not salaried bands (Glassdoor NYC ~$70,884 estimate — low confidence, small sample).
- **[inference / not found]** No public role-level comp for AI/LLM leadership (GM of AI, SVP Data Science), CTO, CMO, or other named execs — NEO pay would be in the **DEF 14A proxy** (not retrieved). **[sourced]** Talkspace filed **0 H1B LCAs in FY2025**, so the freshest legal-wage data points are 2021–2023.

---

## Dimension 9 — Funding & AI investment

- **[sourced]** Pre-IPO venture: **~$109M across ~7 rounds / ~22 investors** (Tracxn): Series A (~2014–15, Spark Capital + SoftBank), **Series B $15M** (Norwest, 2016), **Series C $31M** (Qumra, 2017–18), **Series D $50M** (Revolution Growth, May 2019).
- **[contested]** **Series A** is reported inconsistently — both **$3.5M (2014)** and **$9.5M** appear; exact figure/date ambiguous.
- **[sourced]** The **2021 SPAC merger** provided **~$250M** growth cash at ~$1.4B enterprise value.
- **[inference]** **AI is self-funded** from operating cash/balance sheet — no dedicated AI raise disclosed. Talkspace self-funds the Tee LLM and 2026 AI roadmap, guiding to **2026 revenue $275–290M** and **adjusted EBITDA $30–35M**.
- **[sourced]** The pending **UHS acquisition (~$835M)** is the effective exit / capitalization event for scaling AI. *Valuation note: ~$835M is **aggregate equity/purchase value** ($5.25/share), **NOT enterprise value** — earlier "~$835M EV" labeling is imprecise.*

---

## Dimension 10 — Business model & business drivers behind the tech

- **[sourced]** Three channels: (1) **Payor/B2B insurance — ~75% of revenue (Q2 2025**, up from ~65% in Q2 2024), grown by signing health plans covering **~200M lives** (~two-thirds of the US commercial population); (2) **Direct-to-Enterprise (DTE/EAP)** ~$9M/qtr; (3) **Direct-to-Consumer (DTC), shrinking** (~$4–6M/qtr).
- **[sourced]** **Financials:** FY2024 revenue **$187.6M (+25%)**; FY2025 **$228.9M (+22%)**; Q4 2025 **~$63M (+29%)**. Gross margin **compressed from ~49.6% (2023) → 45.8% (2024) → low-40s% (Q2 2025)** — precisely because of the payer-mix shift (lower per-unit margin but far more predictable, scalable, covered-lives volume).
- **[inference]** This business reality **directly drives the AI roadmap.** The payer model rewards scale/reach; AI (Tee at $19.99/mo standalone, plus the broader agent) lets Talkspace **extend a supply-constrained therapist workforce**, **defend against general-purpose chatbots** (ChatGPT/Character.ai), **re-monetize the declining DTC channel**, and build a **funnel** upselling AI users into paid human therapy and payer-covered care.
- **[sourced]** **UHS rationale:** accelerating outpatient/behavioral-health growth, bypassing provider shortages, diversifying payer mix.

---

## Dimension 11 — Stated vs. real motivations

**Confidence on this read: medium / medium-high.**

**Stated motivation [sourced]:** A clinical-safety and access mission. CEO Jon Cohen: Talkspace is "positioned to be a leader in the application of AI to mental health services" and "AI does not replace clinicians but rather extends their reach." Tee is marketed as the **first "SAFE" AI agent** — real-time clinician oversight, multi-entity risk detection, algorithmic blockades, age gating, self-harm screening — the clinically responsible, human-first alternative to unsafe general-purpose chatbots, expanding access amid a provider shortage.

**Real motivation [inference, medium-high]:** Predominantly **commercial and defensive.**
1. **Margin/scale economics** — the payer pivot (~75% of revenue) compressed gross margins, so AI lets Talkspace serve far more covered lives without proportional therapist labor cost; clinician supply is the binding growth constraint.
2. **Competitive defense + TAM expansion** — consumers increasingly use free general-purpose chatbots for emotional support, eroding the shrinking DTC business; **[sourced]** mental-health brands are adding AI companions specifically to compete with ChatGPT/Character.ai. Tee at $19.99/mo recaptures that demand and feeds a paid-therapy funnel.
3. **[inference]** The "safe/clinically supervised" framing functions as a **regulatory and competitive moat** as general-purpose chatbots draw legal/FTC scrutiny over self-harm incidents.
4. **Strategic exit value** — AI scalability plus ~200M covered lives made Talkspace attractive to UHS (~$835M, March 2026); the AI roadmap doubles as **acquisition value-maximization.**

**[speculation]** The precise internal weighting between mission-driven and commercial/defensive motivations is **not disclosed** and is inferred from financials and timing.

---

## Dimension 12 — Overall confidence & key uncertainties

**Overall verifier confidence: high** on the core, sourced facts (founding, financials, payer mix, UHS deal, Tee launch/pricing/guardrails, fine-tuning-not-pretraining, NYU-validated suicide classifier).

**Key uncertainties / not found:**
- **Base model identity** for Tee (Llama/Claude/other) — unknown — not found (sourced negative).
- **RLHF / RAG** usage — unknown — not found.
- **Production inference infra** (e.g., Bedrock) — speculation only.
- **React Native** for mobile — weak/unsupported.
- **Risk-classifier architecture** (BERT/RoBERTa-class) — speculation; 2020 model predates BERT dominance.
- **Independent validation** of NYC Teenspace/alert statistics — none; company-stated, some figures stale (2023).
- **RCT-grade efficacy evidence for Tee** — none disclosed.
- **Canonical "three guardrails" wording** — in a paywalled source, unretrieved (contested).
- **Series A amount** — contested ($3.5M vs $9.5M).
- **AI-leadership/exec role-level comp** — not found (would be in DEF 14A).

**Watch-outs carried forward from verification:**
- **Date correction:** Tee launched **June 9, 2026** (not June 22).
- **Unsupported figure dropped:** the "**92% accurate, up from 83%**" suicide-detection claim does not trace to its cited source; only **AUC 82.78** is supported.
- **Metric conflation:** AUC 82.78 ≠ "83% accuracy vs human expert."
- **Valuation mislabel:** ~$835M is **aggregate equity/purchase value**, not enterprise value.
- **Marketing-as-fact:** the 50%/47%/3x gains, "largest dataset in industry," and "first safe AI agent" are unverified company claims/superlatives.

---

## Sources

- https://bhbusiness.com/2026/02/19/talkspaces-mental-health-ai-agent-will-jump-into-chatbot-fray-this-summer/
- https://www.fiercehealthcare.com/health-tech/talkspace-boosts-ai-investments-plans-build-out-behavioral-health-llms
- https://www.talkspace.com/ai-at-talkspace
- https://investors.talkspace.com/news-releases/news-release-details/talkspace-announces-tee-first-safe-ai-agent-specifically
- https://www.inc.com/moses-jeanfrancois/talkspace-just-launched-an-ai-therapist-with-one-major-catch/91358983
- https://bhbusiness.com/2025/08/05/talkspace-has-big-plans-for-its-llms-potentially-including-licensing-to-other-organizations/
- https://startup.jobs/senior-full-stack-engineer-react-nodejs-talkspace-1622879
- https://arxiv.org/html/2410.08375
- https://www.talkspace.com/online-therapy/cognitive-behavioral-therapy/
- https://www.talkspace.com/blog/how-is-talkspace-therapy-different-from-ai-mental-health-tools/
- https://finance.yahoo.com/sectors/healthcare/articles/talkspace-announces-tee-first-safe-123000202.html
- https://www.talkspace.com/tee
- https://seekingalpha.com/news/4554235-talkspace-targets-275m-290m-revenue-in-2026-while-advancing-ai-driven-mental-health-solutions
- https://hitconsultant.net/2023/09/13/ai-algorithm-alerts-therapists-to-suicide-risk-in-patients/
- https://www.cnbc.com/2025/10/10/talkspace-online-therapy-therapists-mental-health.html
- https://reason.com/2025/12/03/chatbots-are-not-medical-devices/
- https://hoodline.com/2026/02/talkspace-boss-weighs-in-on-hochul-s-teen-ai-chatbot-crackdown/
- https://en.wikipedia.org/wiki/Talkspace
- https://canvasbusinessmodel.com/blogs/brief-history/talkspace-brief-history
- https://www.sec.gov/Archives/edgar/data/0001803901/000119312521193378/d115266dex991.htm
- https://bhbusiness.com/2022/11/08/talkspace-names-new-ceo-reveals-layoffs-as-part-of-turnaround-effort/
- https://tracxn.com/d/companies/talkspace/__SK61CePKo3n75FdfUEw-5Ct26oRJPkMU3A6wBsrG4F0/funding-and-investors
- https://techcrunch.com/2019/05/29/talkspace-picks-up-50-million-series-d/
- https://www.vcnewsdaily.com/Talkspace/venture-capital-funding/htvqzqdgyd
- https://www.investing.com/news/company-news/talkspace-q3-2025-slides-payor-segment-drives-25-revenue-growth-ebitda-doubles-93CH-4320479
- https://www.fiercehealthcare.com/digital-health/talkspace-logs-19m-q3-profit-driven-strong-growth-payer-enterprise-business
- https://www.investing.com/news/company-news/talkspace-q2-2025-slides-revenue-jumps-18-ebitda-nearly-doubles-93CH-4170170
- https://www.globenewswire.com/news-release/2026/02/19/3241014/0/en/Talkspace-Announces-Fourth-Quarter-and-Full-Year-2025-Results.html
- https://www.statnews.com/2025/12/01/ai-chatbot-headspace-talkspace-lyra-sondermind-digital-mental-health/
- https://www.healthcaredive.com/news/uhs-talkspace-acquisition-behavioral-health/814155/
- https://www.fiercehealthcare.com/health-tech/talkspace-sees-big-opportunities-lead-ai-mental-health-generic-ai-chatbots-draw
- https://marketrealist.com/p/talkspace-ceo-oren-frank/
- https://www.linkedin.com/in/oren-frank-08619322
- https://investors.talkspace.com/governance/management/
- https://craft.co/talkspace/executives
- https://theorg.com/org/talkspace/teams/leadership-team-1
- https://investors.talkspace.com/news-releases/news-release-details/talkspace-appoints-nikole-benders-hadi-md-chief-medical-officer
- https://investors.talkspace.com/news-releases/news-release-details/talkspace-launches-dedicated-ai-innovation-group-advance
- https://www.clay.com/dossier/talkspace-executives
- https://www.macrotrends.net/stocks/charts/TALK/talkspace/number-of-employees
- https://www.statnews.com/2026/03/09/talkspace-to-be-acquired-for-835-million-by-mental-health-services-giant/
- https://leadiq.com/c/talkspace/5a1d9736230000520085c4cf/employee-directory
- https://www.prnewswire.com/news-releases/universal-health-services-inc-to-acquire-talkspace-inc-302708096.html
- https://www.levels.fyi/companies/talkspace/salaries
- https://www.glassdoor.com/Salary/Talkspace-Salaries-E1284778.htm
- https://h1bdata.info/index.php?em=talkspace+inc
- https://h1bgrader.com/h1b-sponsors/talkspace-inc-82wrjv1jk1
