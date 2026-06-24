# AI Therapy: Technology & Mental-Health Deep-Dive Research Report

> **Scope:** Slingshot AI / Ash and Spring Health (anchors) plus the broader AI-therapy field — 16 companies/subjects.
> **Produced by:** an autonomous multi-agent research run (research lead → discovery → tech / clinical / business / people analysts → adversarial verifier → synthesizer). 111 agents, ~3.9M tokens.
> **Trust model:** every material claim is labeled `sourced` (with source), `inference`, or `speculation`; salaries are labeled data vs. estimate; an adversarial verifier pass ran before synthesis. Treat this as a high-quality research draft to act on *with* the labels, not as audited fact.
> **Per-company dossiers:** see `companies/` · **Sources:** see `sources.md`
> ⚠️ **Known glitch:** the charter-setting agent returned placeholder text ("test"); the detailed per-dimension briefs were hard-coded in the workflow so research depth was unaffected, but the lead's stated success criteria in Appendix B are not meaningful for this run.

---

# AI Mental-Health Landscape — Master Synthesis Report

*As of 2026-06-24. Synthesized from 17 company dossiers spanning consumer AI-therapy apps, enterprise benefits platforms, regulated clinical-AI vendors, and one academic research project. Evidence labels (`[sourced]`, `[inference]`, `[contested]`, etc.) are preserved from the underlying dossiers; this report flags where headline claims are vendor marketing rather than independent fact.*

---

## 1. Executive Summary

Seventeen entities, one structural truth: **almost no one in AI mental health is doing frontier ML, and almost everyone's real moat is somewhere other than the model.** Across the cohort, the genuinely hard and defensible work is concentrated in (a) proprietary clinical/outcomes data, (b) safety/crisis-detection and evaluation engineering, and (c) regulatory positioning — not in novel model research. The dominant architectural pattern is a third-party foundation LLM (vendor almost universally undisclosed) wrapped in clinical scaffolding, guardrails, and human-in-the-loop escalation. Only Slingshot (continued pre-training of Qwen3-235B) and Wysa/Woebot (deliberately non-generative rule engines) deviate, and even Slingshot's "foundation model for psychology" label is contested as a heavy fine-tune.

**The field is bifurcating along a regulation/positioning axis.** One camp pursues clinical legitimacy and reimbursement (Spring Health, Lyra, Limbic, Jimini, Talkspace, ieso, SonderMind, Wysa) — selling B2B/payer infrastructure where clinician supervision is simultaneously a safety feature, a commercial moat, and a liability shield. The other camp deliberately self-classifies as "wellbeing"/"non-device" to stay outside FDA jurisdiction (Slingshot/Ash, Youper, Sonia, Earkick, Headspace/Ebb, BetterHelp) — a posture that delivered speed but is now actively collapsing under regulatory pressure (Slingshot's UK withdrawal and Illinois blocking; the May 2026 Common Sense Media / Stanford report that flagged Earkick and Youper).

**2025–2026 was an inflection year.** Generative AI moved from experiment to product (Spring's Guide, Talkspace's Tee, SonderMind's Sonder, Lyra AI, Headspace's Ebb, ieso's Velora). Simultaneously the regulatory environment hardened: the FDA Digital Health Advisory Committee met (Nov 6, 2025) and has cleared **zero** generative-AI mental-health tools; Illinois passed the WOPR Act (Aug 4, 2025, $10K/violation); California passed AB 489 / SB 243. Several players retreated or repositioned defensively — Woebot retired its consumer app (June 30, 2025) and pivoted to enterprise; Youper retreated to "not a medical device" wellness; ieso sold its human-services arm to Mindler; BetterHelp is in revenue decline and pivoting to insurance.

**The single most pervasive integrity issue is marketing laundered as fact.** Nearly every dossier flags self-reported efficacy or safety numbers presented as established findings — Slingshot's "100% accuracy," Talkspace's "92% accurate," Spring's "92.3% improvement," Headspace's "34% more engagement," ieso's "zero safety incidents," Earkick's stale 34%/32% survey, and the recurring "validated"/"clinical-grade"/"first" superlatives. Independent, peer-reviewed RCT evidence for the *actual generative product being sold* is rare-to-absent across the entire cohort; the strongest peer-reviewed evidence (Limbic's two Nature Medicine studies, Therabot's NEJM AI RCT) carries its own caveats (process-quality rubrics vs. outcomes; waitlist controls).

---

## 2. Landscape Overview

### Four archetypes

**A. Enterprise/payer benefits platforms (human-core, AI-layer).** Spring Health ($3.3B), Lyra Health (~$5.6B), Talkspace (Nasdaq: TALK, pending UHS acquisition ~$835M), SonderMind (~$1.1B), BetterHelp (Teladoc segment, ~$1B declining). These are clinically-weighted services businesses where AI is retention/margin/utilization infrastructure layered onto a human-therapist network. Moats: proprietary outcomes data, payer relationships, provider supply.

**B. Regulated clinical-AI vendors (B2B infrastructure).** Limbic (UKCA Class IIa), Jimini/Sage, Wysa (FDA Breakthrough Designation), ieso/Velora. These sell *the platform that lets health systems deliver supervised AI care*. Moats: regulatory credentials, clinical-safety engineering, proprietary clinical datasets.

**C. Consumer AI-therapy apps (D2C, "wellbeing" positioning).** Slingshot/Ash ($93M), Youper (~$4M, contracted), Sonia ($3.35M), Earkick ($1.56M), Headspace/Ebb. These chase scale/engagement, mostly avoid the "therapy"/device label, and run with little-to-no human-in-the-loop. Highest regulatory exposure.

**D. Academic research.** Therabot (Dartmouth) — not a company; first generative-AI-therapy RCT (NEJM AI, 2025); mission/priority-driven, no commercialization disclosed.

### Cross-cutting structural facts
- **Foundation-model vendor disclosure is near-universally absent.** Only Youper (OpenAI GPT, partially) and Slingshot (Qwen3-235B, open-weight) name their base. Spring, Lyra, Talkspace, Jimini, SonderMind, Headspace, ieso, Sonia, Earkick, Therabot, Woebot — all undisclosed.
- **"Foundation model from scratch" is a myth in this space.** Every player either fine-tunes/wraps a third-party model or (Slingshot) continued-pre-trains an off-the-shelf open-weight model. No one pretrains.
- **The hardest problems are clinical/regulatory, not ML** — a verdict repeated in 16 of 17 engineering-difficulty assessments.

---

## 3. Engineering Difficulty Ranking

Ratings are the dossiers' own (tech dimension; consistent rubric: 1=thin wrapper, 5=frontier research). The notable finding: the ratings cluster tightly at 2–4, and **difficulty correlates with safety/eval/regulatory burden, not ML novelty.**

| Rating | Company | What drives the score |
|---|---|---|
| **4/5** | **Limbic** | Class IIa regulated device + blinded RCT-grade eval across 4 LLMs + crisis detection + NHS-scale deployment. Hardest parts regulatory/clinical, not ML. |
| **4/5** | **Jimini (Sage)** | 10+ fine-tuned safety classifiers, LLM-as-judge pipeline, interpretable rationale, EHR integration, in-house multi-state clinic as QA gate. Heaviest ML outsourced. |
| **4/5** | **ieso (Velora)** | 25-yr outcomes-indexed dataset, in-silico patient-agent adversarial testing, clinical-safety generative agent. Capped below 5 by model-layer opacity / no frontier ML. |
| **4/5** | **Therabot** | Fully-generative therapist that cleared an IRB RCT; 6 yrs + 100k+ hrs building a curated CBT dataset. Novelty in data, not architecture. |
| **3/5** | **Slingshot (Ash)** | Continued pre-training + SFT + RLHF/DPO on Qwen3-235B MoE; ensemble serving; two-pass guardrails. ~1% post-training corpus, off-the-shelf weights cap it. (Alt read of 4/5 down-weighted.) |
| **3/5** | **Spring Health** | Proprietary matching ML + VERA-MH eval harness + HIPAA at 10M lives. Human-in-the-loop safety net lowers raw risk. |
| **3/5** | **Lyra Health** | RAG + scope-limit + risk classifier + human escalation; multilingual/voice. Could be 4 if meaningful fine-tuning confirmed. |
| **3/5** | **Talkspace** | Fine-tuning on regulated PHI + production 10-class risk classifier wired to live human escalation since 2019. Fine-tunes, doesn't pretrain. |
| **3/5** | **Wysa** | Rule engine + 120+ NLU routing models + crisis detection at DCB0129-regulated scale. Conservative-by-design lowers ML difficulty. |
| **3/5** | **Sonia** | Therapy-as-FSM, custom voice-to-voice loop, ~7 background calls/turn, async crisis classification. Commodity primitives cap it. |
| **3/5** | **SonderMind** | RAG + orchestration on commercial LLMs across acquired EHR/billing systems under HIPAA+ISO 27001. Consumer chatbot alone = 2/5. |
| **3/5** | **Headspace (Ebb)** | App-layer LLM + fine-tuned 7-category safety classifier on 100% of messages + LLM-as-judge + red-teaming. No validated MI-fidelity/crisis benchmark. |
| **3/5** | **Woebot** | Rules-based decision tree + NLP classifier progression (→BERT) + LDP crisis layer + hybrid-LLM guardrail experiment. (2–3 band; 3 for clinical-grade rigor.) |
| **2/5** | **Youper** | Decision-tree → OpenAI GPT hybrid with guardrails; conventional stack; lean team. Hard work is clinical/regulatory. |
| **2/5** | **BetterHelp** | App-layer matching/summaries/triage on commercial models. Hardest engineering (marketplace + insurance/claims integration) is non-AI. |
| **2/5** | **Earkick** | Consumer LLM wrapper + multimodal input + on-device privacy. Deliberately skips the hard safety/crisis/device work. |

**Pattern:** The 4/5 cluster (Limbic, Jimini, ieso, Therabot) earns its rating through *safety-eval rigor + regulatory validation + proprietary data*, explicitly NOT through model R&D. The 2/5 floor (Youper, BetterHelp, Earkick) is occupied by consumer wrappers that sidestep the hard clinical-safety problems. No entity rates 5/5 — the field has no frontier-ML players.

---

## 4. Funding & Compensation Table

### Funding / valuation

| Company | Total raised | Valuation | Latest event |
|---|---|---|---|
| Lyra Health | ~$910–915M | ~$5.58–5.85B (Series F, Jan 2022) | No new priced round since 2022; AI self-funded |
| Spring Health | >$470M | $3.3B (Series E, Jul 2024) | Generation IM-led Series E |
| Talkspace | ~$109M pre-IPO + ~$250M SPAC | Pending UHS acq. ~$835M equity value | UHS acquisition announced Mar 9, 2026 |
| BetterHelp | N/A (Teladoc segment) | Embedded in TDOC | UpLift acq. ~$45M (Apr 2025); revenue declining |
| Woebot | ~$123M ($114M–$129M agg-dependent) | Undisclosed | Consumer app retired; enterprise pivot |
| SonderMind | ~$183M ($150M Series C, 2021) | ~$1.1B (2021, likely stale) | AI Suite launched Oct 2025 |
| Slingshot (Ash) | ~$93M cumulative | Undisclosed | UK withdrawal Jan 2026 |
| ieso (Velora) | ~$70M stated / ~$89–91M tracked | £97.5M (~Nov 2021, stale) | Sold UK services to Mindler, Aug 2025 |
| Headspace (Ebb) | ~$216M + Ginger ~$220M | ~$3B (2021 merger, STALE; possible markdown to ~$1B) | Stratified care model 2025 |
| Jimini (Sage) | >$25M ($8M pre-seed + $17M seed) | Undisclosed | $17M seed ~Mar 2026 |
| Limbic | ~$14.7M–$21.8M (contested) | Undisclosed | $14M Series A, Mar 2024 |
| Youper | ~$3.5–5.2M | Undisclosed | Nothing raised since 2019 seed |
| Sonia | ~$3.35M | Undisclosed | YC W2024 seed |
| Wysa | ~$29–40M (contested, grants bundled) | ~$82M (Aug 2023) | April Health merger Mar 2025 |
| Earkick | ~$1.56M | Undisclosed | Wefunder note Apr 2024 |
| Therabot | None (academic) | N/A | NEJM AI RCT Mar 2025 |

### Engineering compensation (representative; bases/total comp as labeled in dossiers)

| Company | Senior SWE / ML benchmark | Notes |
|---|---|---|
| Slingshot | London MTS £100K–£250K + equity; NY SWE $250K (H1B) | Research-lab "MTS" titles |
| Spring Health | SWE ~$208K TC (levels.fyi); Sr SWE $212K base (H1B) | |
| Lyra Health | SWE ~$222–225K TC; VP Data & AI $251K–$346K base | Below FAANG |
| Talkspace | SWE ~$219–225K TC; Full-Stack $154.9K base (H1B 2022) | Levels high vs Glassdoor low |
| Headspace | Sr SWE ~$165K median base (H1B); SWE ~$180–190K TC | |
| Jimini | Sr SWE (Backend) $185K–$250K base + equity | One verifiable band |
| SonderMind | Principal AI Eng $160K–$190K; SWE ~$110–117K TC | |
| Woebot | Sr Platform Eng $150K; VP Content $155K (H1B) | |
| BetterHelp | Embedded in Teladoc — not found | |
| Wysa | SWE median ₹1.81M (India); zero US H1B | India-based core |
| ieso | SWE ~£42–66K (Cambridge UK; tiny n) | Zero US H1B |
| Youper / Sonia / Earkick / Therabot | No reliable company data (modeled estimates only) | Therabot = academic bands ~$53–111K |

**Comp pattern:** US enterprise players cluster at ~$200–225K TC for senior engineers (market-but-not-FAANG, private illiquid equity). UK/India players (Limbic, ieso, Wysa) run materially lower on local scales. The smallest consumer apps (Youper, Sonia, Earkick) have zero authoritative comp data — only modeled aggregator estimates that conflict with each other.

---

## 5. Stated vs. Real Motivations Matrix

A near-universal structure: a *genuine and well-documented* access/mission narrative sitting atop *inferred* commercial/defensive drivers. In almost every case the two are **aligned in direction but differ in emphasis** — the dossiers stress these are reasoned inferences from investor theses, financials, and timing, not founder admissions of hidden goals.

| Company | Stated | Real (inferred) | Alignment |
|---|---|---|---|
| Slingshot (Ash) | Democratize access; "best therapist for everyone"; not a companion | Venture-scale consumer-health land-grab; free-now data moat → subscription + B2B; "wellbeing" = regulatory positioning | Genuinely intertwined; split on retention-vs-reduce-dependence incentives |
| Spring Health | Eliminate barriers; precision care | ROI-positive EAP replacement; utilization + cost savings monetized via guarantees; AI defends margin/valuation | High alignment; gap is emphasis |
| Lyra Health | Clinical access/quality; supplement not replace | Defensive margin/engagement move; keep ChatGPT demand in-platform; defend $5.6B post-Series-F | Aligned; real motive most heavily caveated/unfalsifiable |
| Wysa | De-stigmatize, close treatment gap | Reimbursable clinical-infra business; free chatbot as evidence/acquisition funnel → ~80% B2B | Mission genuine; operative driver is institutional revenue |
| Limbic | Equity/access; augment clinicians | Venture-scale defensible clinical-AI; NHS data moat → monetize "more privatised" US | Aligned — access IS the GTM/data strategy |
| Youper | Simple, accessible, affordable care | Venture-scalable D2C subscription; clinical study as sales/fundraising asset | Diverged in practice — narrowed to lean consumer app after no capital post-2019 |
| Sonia | Democratize "validated" support; "arbitrage of happiness" | Capture Goldilocks-zone market ahead of B2B2C reimbursement land-grab | Aligned in direction; "validated" outruns evidence |
| Jimini (Sage) | Fix between-session gap; superpower clinicians | Own the "safe/compliant" reimbursable B2B layer; clinician-supervision = moat + liability shield | Largely aligned; public-health framing manufactures urgency |
| Talkspace | Clinical-safety/access; "first SAFE AI agent" | Margin/scale economics; competitive defense vs ChatGPT; acquisition value-max for UHS | Broadly aligned, emphasis differs |
| SonderMind | AI complements, never replaces; "there at 3 a.m." | Competitive defense + outcomes/cost economics; monetize 167 empty between-session hours | Medium-high confidence on commercial drivers |
| ieso (Velora) | "Sharpen focus" on AI mental health | Convert labor-bound services into scalable software/IP; data moat is the product; pivot is also a *retreat* from un-scalable services | Largely congruent; "sharpen focus" masks divestiture of margin-capped unit |
| Headspace (Ebb) | Blend AI + humans for better outcomes | Margin and scale; cheap bottom tier of stratified funnel; therapist headcount variabilized | Medium-high; cost-substitution is dominant driver |
| BetterHelp | AI assists, not replaces clinicians | Financial defense of declining ~$1B segment; retention/margin + FTC reputational risk mgmt | Aligned but emphasis differs |
| Woebot | Make mental health radically accessible | Commercial-survival pivot; scripted moat squeezed by free LLMs + failed FDA path (terminated pivotal trial) | "Face-saving" read is speculation, not elevated |
| Earkick | Accessible, anonymous, safety-minded | Regulatory-avoidance + speed/low-cost; credibility-signaling exceeds operational reality | Founder sincerity plausible; structural choices optimize for distance from regulation |
| Therabot | Close supply-demand gap; test before deploying | Establish scientific priority/credibility; attract grants, shape regulatory norms | Genuinely mission/research-driven; no commercial intent found |

---

## 6. Common Patterns

1. **The undisclosed-foundation-model norm.** 15 of 17 refuse to name their base LLM. This is now an industry convention, not an oversight — it preserves swap-ability and obscures dependence on OpenAI/Anthropic/Google. Limbic's transparency (model-agnostic across GPT-4/Claude/Gemini/Llama 3) is the exception that proves the rule.

2. **The moat is data + safety-eval + regulation, never the model.** Stated verbatim in nearly every engineering-difficulty section. The hardest-to-replicate assets are longitudinal outcomes datasets (Spring, ieso, Slingshot, Talkspace) and safety/eval apparatus (Spring's VERA-MH, Jimini's classifier bank, Headspace's 7-category classifier, Limbic's CTRS-scored layer).

3. **Human-in-the-loop as a spectrum that maps to positioning.** Strong/runtime HITL = the B2B/regulated camp (Spring, Limbic, Jimini, Talkspace, Wysa). Weak/async or none = the consumer camp (Slingshot, Youper, Sonia, Earkick, Headspace-Ebb consumer side). The HITL choice is simultaneously a safety control, a moat, and a liability/regulatory strategy.

4. **"Wellbeing/not-a-device" as deliberate regulatory arbitrage — now collapsing.** Slingshot, Youper, Sonia, Earkick, Headspace, BetterHelp all self-classify to stay outside FDA. This worked until 2025–2026: Slingshot withdrew from the UK and blocks Illinois; the FDA DHAC convened; Illinois WOPR and California AB 489/SB 243 passed; the May 2026 Common Sense Media/Stanford report flagged consumer apps.

5. **Marketing laundered as fact — the cohort-wide integrity failure.** Self-reported, uncontrolled, or single-vendor-page numbers presented as efficacy: Slingshot "100% accuracy" / 76-77% improvement; Talkspace "92% accurate" (unsupported) and 50%/47%/3x gains; Spring "92.3% improvement" (observational); Headspace "34% more engagement" (secondary); ieso "zero safety incidents"; Earkick stale 34%/32%; pervasive "first"/"clinical-grade"/"validated"/"largest" superlatives.

6. **The efficacy-evidence gap for the actual generative product.** No company in the cohort has a published RCT of its *current generative chatbot*. The strongest peer-reviewed evidence attaches to *predecessor* systems (ieso's tree-based IDH-DP2-001; Slingshot's single-arm preprint; Spring's observational OJPHI cohort; Wysa's null NHS RCT). Limbic's two Nature Medicine studies are real but measure CTRS process-quality (not outcomes), and Therabot's NEJM AI RCT used a waitlist control. Lyra's, SonderMind's, Talkspace-Tee's, and Headspace-Ebb's chatbots have engagement data only.

7. **CBT is the lingua franca; integrative is the trend.** Every clinically-grounded product centers CBT, usually with DBT/ACT. Slingshot and Spring push "dozens of modalities"; Wysa/Woebot/Limbic stay CBT-anchored.

8. **Crisis handling is structurally similar and structurally opaque.** Nearly all escalate to 988/local hotlines via a risk classifier; nearly none publish false-negative rates or recall. Slingshot's own data (3-of-45 escalation misses) contradicts its "100% accuracy" marketing — emblematic of the gap.

9. **Founder/entity-fact contestation is rampant.** Founding dates (Slingshot 2018 vs 2022; SonderMind 2014 vs 2015; Limbic 2017/2018/2020), founder counts (Spring's omitted 3rd co-founder Chandra; Slingshot's Lucy Hong; Sonia's YC profile), titles (Lyra's Gonsalves = CPTO not CEO; Woebot's Darcy = President not CEO), and headcounts (aggregator conflation of contractor networks) are inconsistent across sources throughout.

10. **2025–2026 strategic retreats and pivots.** Woebot (consumer→enterprise, app retired), Youper (clinical→wellness), ieso (services→software, divested), Slingshot (UK exit), BetterHelp (D2C→insurance), Headspace/Talkspace/SonderMind (therapist headcount variabilized). The labor-to-software substitution thesis is now explicit and resourced across the enterprise camp.

---

## 7. Key Risks (Cohort-Level)

- **Regulatory tightening with zero cleared products.** FDA has cleared no generative-AI mental-health tool; state laws (IL WOPR, CA AB 489/SB 243) and the FDA DHAC create live exposure for the "wellbeing" camp. Wysa's and Woebot's FDA Breakthrough *Designations* are not clearances; Woebot's pivotal trial was terminated with no published results.

- **Safety-claim verification deficit.** Crisis-classifier performance is near-universally unpublished; safety architectures are self-reported with no independent audit (Jimini, ieso, Headspace, Slingshot, SonderMind governance councils). The May 2026 Common Sense Media report (Earkick/Youper disappearing mid-test; Wysa rated "unacceptable") is the first major third-party safety reckoning.

- **Incentive conflict.** Subscription/engagement revenue rewards retention; good therapy should reduce dependence — flagged for Slingshot, Lyra, SonderMind, Headspace, Talkspace.

- **Financial fragility at the edges.** BetterHelp (~$1B segment in decline, drove Teladoc's ~$1B FY24 loss), Youper/Earkick (no capital since 2019/lean), Headspace (stale $3B valuation, repeated layoffs, venture debt) face down-round/sustainability risk. Talkspace's exit (UHS) and Slingshot's UK retreat show the model is being stress-tested.

- **Evidence/marketing gap as legal and reputational liability.** As general-purpose chatbots face wrongful-death litigation (Character.AI), the "clinically validated"/"safe" superlatives that outrun the evidence base become the cohort's clearest shared vulnerability.


---

## Appendix A — Senior Research Lead: Decisions Log

_Every judgment call the autonomous research lead made on your behalf, so you can audit where it spent your judgment._

### Roster ratification decisions

- **Ratified the roster's three core verified anchors and structure; trimmed from 20 to 16 subjects to protect depth on anchors.**
  - Fork: Keep all 20 as proposed vs. trim the weakest tier-3 long tail.
  - Rationale: Brief explicitly says 'keep it focused enough to go deep on the anchors.' Tier 3 had 8 entries, several of them thin adjacencies that dilute research budget. Cutting the 4 weakest preserves segment coverage while concentrating effort.
  - Confidence: high
- **DOWNGRADED Woebot Health from tier 2 to tier 3.** ⚠️ **flagged for your review**
  - Fork: Keep at tier 2 as 'category pioneer / substantial profile' vs. drop to field-scan.
  - Rationale: Verified the consumer app was retired 30 Jun 2025 and the company pivoted entirely to enterprise. Its value is now historical/benchmark, not active competitor. A full tier-2 substance profile overstates its present relevance; tier-3 captures the legacy reference correctly.
  - Confidence: high
- **CUT Noah AI (tier 3).** ⚠️ **flagged for your review**
  - Fork: Retain as consumer-companion field-scan vs. cut.
  - Rationale: Redundant with Sonia/Youper/Earkick which already cover the consumer-companion cohort more notably. Its 'therapist-export PDF' differentiator is thin and the cohort is already well-represented. Lowest marginal value.
  - Confidence: medium
- **CUT Rosebud (tier 3).** ⚠️ **flagged for your review**
  - Fork: Retain as AI-journaling adjacency vs. cut.
  - Rationale: AI-journaling is an adjacency, not core AI-therapy. With budget concentrated on anchors, a single representative of a non-therapy adjacency is expendable. Earkick already flags the consumer breadth.
  - Confidence: medium
- **CUT Big Health (Sleepio/Daylight) (tier 3).** ⚠️ **flagged for your review**
  - Fork: Retain as evidence-based DTx reference vs. cut.
  - Rationale: Explicitly 'CBT-driven, not generative-AI-native.' It is a digital-therapeutics incumbent, not an AI-therapy competitor. Therabot and ieso already supply the clinical-evidence/validation framing. Off the core thesis.
  - Confidence: medium
- **Confirmed the four 'NEW (seed missed)' tier-2 promotions kept (Jimini, ieso, SonderMind) and Talkspace's tier-3 to tier-2 bump.**
  - Fork: Trust scout claims vs. verify before ratifying tier-2 spend.
  - Rationale: Verified Jimini ($17M seed, 31 Mar 2026, ~$25M+ total, M13/Town Hall/Zetta) and ieso (telecare divested to Mindler Aug 2025, API-first, US expansion). Both warrant tier-2. Talkspace's public-incumbent AI push and SonderMind's scale justify their tiers without further checks.
  - Confidence: high
- **Confirmed Slingshot/Ash disambiguation (Ash = Slingshot's product, same entity) and tier-1 status.**
  - Fork: Risk treating Ash as a separate subject vs. lock the disambiguation.
  - Rationale: Verified $93M total and 22 Jul 2025 public launch after 50k beta users. Locking the 'same entity' note prevents a duplicate profile downstream.
  - Confidence: high

### Final sign-off decisions

- **Frame the entire cohort around the structural thesis that the moat in AI mental health lies in proprietary clinical/outcomes data, safety/eval engineering, and regulatory positioning — NOT in novel model R&D.**
  - Fork: Lead with 'everyone is doing frontier ML' vs. 'almost no one is doing frontier ML; the moat is elsewhere'.
  - Rationale: 16 of 17 engineering-difficulty assessments independently reach this verdict; only Slingshot (continued pre-training of Qwen3-235B) and the rule-engine outliers (Wysa/Woebot) deviate, and even Slingshot is a heavy fine-tune. The convergence is strong enough to anchor the report.
  - Confidence: high
- **Adopt a four-archetype roster taxonomy: (A) enterprise/payer benefits platforms, (B) regulated clinical-AI vendors, (C) consumer 'wellbeing' apps, (D) academic research.**
  - Fork: Organize by funding stage / valuation vs. by regulatory-positioning archetype.
  - Rationale: The regulation/positioning axis is the field's true cleavage and predicts HITL depth, evidence posture, and regulatory exposure better than size or stage. Archetypes map cleanly onto the bifurcation thesis.
  - Confidence: high
- **Classify Therabot (Dartmouth) as an in-scope entity but explicitly non-commercial academic research, kept separate from the three commercial archetypes.**
  - Fork: Include Therabot as a 'company' vs. exclude it vs. include-but-segregate.
  - Rationale: It is the only published generative-AI-therapy RCT (NEJM AI 2025) and a critical evidence reference point, but has no commercialization; segregating it preserves the evidence value without distorting commercial comparisons.
  - Confidence: high
- **Treat self-reported efficacy/safety statistics as marketing-laundered-as-fact and flag them cohort-wide rather than reporting them as findings.** ⚠️ **flagged for your review**
  - Fork: Report vendor numbers (Slingshot 100%/76-77%, Talkspace 92%, Spring 92.3%, Headspace 34%, ieso zero-incidents, Earkick 34/32%) at face value vs. quarantine them as contested vendor claims.
  - Rationale: None are independently audited or from RCTs of the actual generative product; presenting them as fact would propagate the cohort's central integrity failure. Slingshot's own 3-of-45 escalation misses directly contradict its '100% accuracy' claim.
  - Confidence: high
- **Down-weight the alternate 4/5 engineering-difficulty read for Slingshot and settle on 3/5.**
  - Fork: Rate Slingshot 4/5 (continued pre-training is genuinely hard) vs. 3/5 (off-the-shelf open weights + ~1% post-training corpus cap it).
  - Rationale: Continued pre-training on an off-the-shelf open-weight MoE with a ~1% post-training corpus is meaningfully below the proprietary-data + regulated-eval rigor of the 4/5 cluster (Limbic, Jimini, ieso, Therabot). Consistency with the rubric favors 3/5.
  - Confidence: medium
- **Place the 4/5 ceiling on Limbic, Jimini, ieso, and Therabot, with NO entity rated 5/5.**
  - Fork: Award a 5/5 to the most technically sophisticated player vs. cap the field at 4/5.
  - Rationale: 5/5 denotes frontier ML research; the rubric's own evidence shows the 4/5 cluster earns its rating through safety-eval rigor, regulatory validation, and proprietary data — explicitly not model R&D. No cohort member pretrains or does frontier research.
  - Confidence: high
- **Report contested funding/valuation figures as ranges with staleness flags rather than single point estimates.**
  - Fork: Pick a single headline number per company vs. present contested ranges (Limbic $14.7M-$21.8M, Wysa $29-40M, ieso $70M/$89-91M) with explicit 'stale'/'contested' labels.
  - Rationale: Sources genuinely conflict and several valuations predate 2022 (Headspace $3B, SonderMind $1.1B, ieso £97.5M); ranges with staleness flags are more honest than false precision.
  - Confidence: high
- **Characterize stated-vs-real motivations as 'aligned in direction, differ in emphasis' inferences rather than claims of hidden agendas.**
  - Fork: Assert concealed commercial motives vs. frame as reasoned inferences from investor theses/financials/timing that mostly align with the stated mission.
  - Rationale: The dossiers stress these are inferences, not founder admissions; in nearly every case access/mission and commercial drivers are genuinely intertwined (access often IS the GTM/data strategy, e.g., Limbic, Wysa). Overclaiming concealment would not be defensible.
  - Confidence: medium
- **Treat the 'wellbeing / not-a-device' positioning as deliberate regulatory arbitrage that is now actively collapsing, not a stable strategy.** ⚠️ **flagged for your review**
  - Fork: Present 'wellbeing' self-classification as durable vs. as eroding under 2025-2026 regulatory pressure.
  - Rationale: Concrete 2025-2026 events (Slingshot UK withdrawal + Illinois block, FDA DHAC Nov 2025 with zero clearances, IL WOPR Act, CA AB 489/SB 243, May 2026 Common Sense Media/Stanford report flagging Earkick/Youper) show the posture failing in real time.
  - Confidence: high
- **State that no cohort member has a published RCT of its current generative product, attaching the strongest peer-reviewed evidence to predecessor or process-quality systems with caveats.** ⚠️ **flagged for your review**
  - Fork: Credit Limbic's Nature Medicine studies and Therabot's NEJM AI RCT as validating the marketed generative products vs. caveat them (CTRS process-quality not outcomes; waitlist control; predecessor tree-based systems).
  - Rationale: The evidence-to-product gap is the cohort's defining scientific weakness; conflating predecessor/process evidence with current-product efficacy would repeat the marketing-as-fact error.
  - Confidence: high
- **Record the undisclosed-foundation-model norm (15 of 17) as an industry convention preserving swap-ability, with Limbic's model-agnostic transparency as the lone exception.**
  - Fork: Treat non-disclosure as incidental omission vs. as a deliberate, near-universal convention.
  - Rationale: Only Youper (OpenAI, partial) and Slingshot (Qwen3-235B) name a base model; the uniformity across 15 others indicates intent to obscure dependence on OpenAI/Anthropic/Google and preserve vendor flexibility.
  - Confidence: high
- **Flag founder/entity-fact contestation (founding dates, founder counts, titles, headcounts) as a data-integrity caveat rather than silently picking one value.**
  - Fork: Resolve each disputed fact to a single value vs. surface the contestation explicitly.
  - Rationale: Conflicts are rampant and partly driven by aggregator conflation of contractor networks (e.g., Slingshot 2018 vs 2022, Lyra Gonsalves CPTO-not-CEO, Spring's omitted co-founder); surfacing the disputes is more accurate than false resolution.
  - Confidence: high

### Knowingly accepted gaps (shipped as-is)

- Foundation-model vendor remains unknown for 15 of 17 entities (all except Youper/OpenAI partial and Slingshot/Qwen3-235B); base-LLM dependence on OpenAI/Anthropic/Google cannot be confirmed.
- No published RCT exists for any cohort member's current generative product; efficacy for the actual marketed chatbots is unverified across the board.
- Crisis-classifier performance (false-negative rates, recall) is unpublished for nearly every entity; safety architectures are self-reported with no independent audit.
- Compensation data is absent or modeled-estimate-only for the smallest consumer apps (Youper, Sonia, Earkick) and academic Therabot; aggregator estimates conflict with each other.
- Several valuations are stale and unverifiable (Headspace ~$3B 2021 merger with possible markdown to ~$1B, SonderMind ~$1.1B 2021, ieso £97.5M 2021); current marks unknown.
- Contested funding totals remain unresolved where sources conflict (Limbic ~$14.7M-$21.8M, Wysa ~$29-40M with grants bundled, ieso ~$70M stated vs ~$89-91M tracked).
- Stated-vs-real motivation gaps are reasoned inferences from financials/timing/investor theses, not founder admissions, and are inherently unfalsifiable.
- Whether Lyra and SonderMind perform meaningful fine-tuning (vs. RAG/prompt-orchestration on commercial models) is unconfirmed, leaving their 3/5-vs-4/5 difficulty rating uncertain.
- BetterHelp engineering comp is embedded in Teladoc and could not be isolated.
- The actual outcome of Woebot's terminated FDA pivotal trial is unpublished, so the reason for termination and any efficacy signal are unknown.

**Signed off:** True


---

## Appendix B — Charter (as set by the lead)

- **successCriteria:** test
- **dimensionBar:** test
- **tierPolicy:** test
- **escalationRule:** test
