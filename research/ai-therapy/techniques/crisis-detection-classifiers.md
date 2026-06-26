# Crisis-detection classifiers

*State of the art as of June 2026. Plain language, real depth. Factual claims are labeled (sourced) with a URL and access date, (inference), or (speculation). Learning-design and org judgments are labeled (advisory) — my reasoned read, not facts pulled from a source.*

---

## 1. What it is

A crisis-detection classifier is a piece of software that reads what a person writes — a text to a crisis line, a message to a telehealth app, a post on a platform, a turn in a chatbot conversation — and decides, in roughly real time: **is this person in danger right now, and how urgently does a human need to step in?**

The output is not a diagnosis. It is a **triage signal** — a number or a label that pushes one conversation to the front of a queue ahead of thousands of others. The clearest target is what Crisis Text Line calls **imminent risk**: someone who has (1) suicidal thoughts, (2) a plan, (3) access to the means, and (4) a 0–48 hour timeline. (sourced — Crisis Text Line, https://research.crisistextline.org/what-we-learned-from-training-a-machine-learning-model-to-detect-suicidal-risk-2c65f1d4d9eb, accessed 2026-06-25)

Modern systems classify more than suicide. The reference clinical benchmark of 2026, **CRADLE**, spans **seven clinically-grounded crisis categories**: suicide (with passive and active ideation as severity levels *within* the suicide category), self-harm, domestic violence, rape, sexual harassment, and child abuse — each tagged as *ongoing* or *past*. (sourced — CRADLE, https://arxiv.org/html/2606.10380 and https://arxiv.org/abs/2510.23845, accessed 2026-06-25) *(Verifier note applied: this is seven categories, not eight. The "eight" figure that circulates comes from double-counting passive and active suicidal ideation as two separate types on top of the other six.)*

The whole point is **speed under scarcity**. A crisis line gets contacts in volumes no human team can read. The 988 Suicide & Crisis Lifeline has logged on the order of **tens of millions of contacts since it launched in July 2022** — crossing roughly 25 million by mid-2026, with a run-rate of about 8 million per year. (sourced, approximate/dated — SAMHSA, https://www.samhsa.gov/mental-health/988/faqs, accessed 2026-06-25; treat exact totals as a moving snapshot) There are never enough trained counselors. The classifier's job is to make sure the person 30 minutes from acting does not wait in line behind someone who is hurting but stable.

---

## 2. How it works

### The naive version, and why everyone started there

The obvious first idea is **a list of dangerous words**: flag any message containing "die," "cut," "suicide," "kill myself." Crisis Text Line literally did this first, with a clinically-derived keyword list. (sourced — https://research.crisistextline.org/..., accessed 2026-06-25) It is trivial to build and instantly understandable.

It fails badly in both directions:

- **False alarms.** "I'm not suicidal, just depressed" trips the "suicidal" keyword and gets escalated to imminent risk — exactly backwards. "I could kill for a coffee" trips "kill."
- **Misses.** The highest-risk messages often contain *none* of the obvious words. People say "I just want it to stop," "I won't be a burden much longer," "thank you for everything." The danger lives in the **meaning and the arc of the conversation**, not the vocabulary.

So keyword matching drowns counselors in noise *and* lets the quietest, most lethal cases slip through. That double failure motivates everything below.

### What replaced it: learned text classifiers

The mechanism in plain terms: **turn language into numbers, learn from labeled examples which number-patterns line up with real crises, then score new messages.** Three generations are all still in use depending on stakes and budget.

**(a) The deployed workhorse — two-stage NLP (cheap, fast, auditable).** A real production system at the telehealth provider Cerebral, published in *npj Digital Medicine*, is deliberately simple: **keyword filtering as a coarse first net, then logistic regression** on the survivors. It was trained on just **721 labeled chat messages** (32% of them real crises). Despite that tiny training set, on a prospective test of **102,471 messages** it reached **AUC 0.98, sensitivity 0.98, positive predictive value 0.66**. (sourced — https://www.nature.com/articles/s41746-023-00951-3, accessed 2026-06-25) The keywords cut the volume cheaply; a transparent statistical model — which weighs *combinations* of words and features rather than any single trigger word — makes the real call. Logistic regression is favored precisely because it is auditable and runs in milliseconds at volume.

**(b) The neural-net generation — context-aware embeddings.** Crisis Text Line moved to an **ensemble of deep neural networks** trained on every conversation their counselors tagged "Suicide" in post-conversation surveys. Instead of matching words, these models map each message into a high-dimensional "meaning space" (embeddings) where "I want it to stop" lands near genuine distress and "kill for a coffee" lands far away. The published discrimination figure is an **AUC of roughly 90%** for separating imminent from non-imminent risk *(verifier correction applied: the underlying number is an AUC ~90.37%, not "90.2% accuracy" — conflating the two is exactly the "accuracy is a trap" error this field warns about)*. The figure the source page actually supports is that the model surfaces **86% of severe imminent-risk people in their first conversation**. (sourced — Crisis Text Line, https://www.crisistextline.org/blog/2018/03/28/detecting-crisis-an-ai-solution/, accessed 2026-06-25) *(Verifier note: widely-repeated "52% fewer false alarms / 13% fewer misses" figures are NOT supported by that page and have been dropped here.)*

**(c) The 2026 frontier — large language models, two ways.**

- *Fine-tuned specialist models.* The **CRADLE-Dialogue** work (arXiv 2606.10380) fine-tuned a **32-billion-parameter Qwen3 model** on **3,058 synthetic multi-turn dialogues (48,557 turns)** generated by GPT-5 from Reddit posts, with the crisis revealed early, mid, or late to force the model to catch risk *as it emerges*. Four clinicians annotated a **600-dialogue (8,975-turn) evaluation set** (inter-rater agreement Cohen's κ = 0.51–0.75). The fine-tune reached **51.3 turn-level Micro-F1**, beating the base model by 7.6 points. (sourced — https://arxiv.org/html/2606.10380, accessed 2026-06-25)
- *Prompted general models.* A 2026 medRxiv study reports that **near-zero-miss detection is achievable with prompt-based sensitivity calibration alone — no fine-tuning and no large task-specific training set** — using clinician-validated data to tune the prompt. (sourced — https://www.medrxiv.org/content/10.64898/2026.01.12.26343914v1, accessed 2026-06-25)

*(Disambiguation, per verifier: "CRADLE" names two related-but-distinct papers — CRADLE-Dialogue / arXiv 2606.10380, the Qwen3-32B turn-level fine-tune and 600-dialogue eval; and CRADLE-Bench / arXiv 2510.23845, EACL 2026, the clinician-annotated benchmark. They are not interchangeable.)*

### The critical architectural lesson of 2026: don't trust the LLM to be the safety net

This is the most important finding shaping how these systems get built now. When you take frontier chatbots *as-is* and ask them to notice crises mid-conversation, **they miss most of them.** On the **InvisibleBench** caregiving-AI benchmark, composite crisis-safety scores were low: **GPT-4o-mini around 11.8%** and the best model, **Claude Sonnet 4.5, around 44.8%**. (sourced — https://arxiv.org/abs/2511.20733, accessed 2026-06-25) *(Footnote, per verifier: these are composite safety figures; the paper's finer breakdown shows performance is much better on explicit crises than on masked ones — e.g. Claude ~58% explicit vs ~31% masked — so read these as "frontier LLMs alone are unreliable here," not as a single clean miss rate.)*

The conclusion the field has converged on: **a fluent conversational LLM is not a reliable crisis detector.** Production systems therefore use **deterministic crisis routing** — a dedicated, separately-validated classifier (the simple, high-recall kind from a/b above) runs *alongside* the chatbot as a hard safety layer, not buried inside its reasoning. You see this in fielded tools: **Therabot** runs a separate crisis-classification model whose sole job is to fire an emergency module (988 / Crisis Text Line / 911 connection plus a live care-team contact) the moment high-risk content appears. (sourced — https://talk.crisisnow.com/the-generative-ai-therapy-chatbot-will-see-you-now/, accessed 2026-06-25)

So the real 2026 architecture is a **layered pipeline**: a cheap high-recall net catches everything suspicious → a more precise model (neural or fine-tuned LLM) ranks urgency → a **calibrated threshold** decides escalate / monitor / route → a **human** makes the final intervention. The LLM is a component, never the guardrail.

---

## 3. Why it works

**The principle: crisis lives in meaning and trajectory, not in tokens.** Risk is a property of *what the whole message means in context* and *how the conversation is moving* — passive ideation hardening into a plan. Keyword matching sees only surface tokens, so it is structurally blind to both the meaning ("I want it to stop") and the arc. Learned classifiers work because they map language into a representation where *meaning sits close to meaning*, and they learn the boundary from thousands of real, clinician-labeled examples rather than from a human's guess about which words matter. (inference, grounded in the sourced keyword-failure and embedding results above)

**Why you tune for recall, not accuracy.** The two errors are not equal. A **false negative** — missing someone about to die — is catastrophic. A **false positive** — escalating someone who is safe — costs a counselor a few minutes. So these systems are deliberately calibrated to **high sensitivity**, accepting more false alarms to drive misses toward zero. That is exactly why the Cerebral system targets **0.98 sensitivity** while tolerating a **0.66 PPV** — a third of its alarms are false, and that is the *intended* trade. (sourced + inference) "Accuracy" alone is a trap: if 1% of messages are crises, a model that says "no crisis" every time is 99% accurate and 100% useless.

**Why the layered, deterministic design wins.** A single end-to-end LLM optimizes for *sounding helpful*, and that objective does not reliably surface low-frequency, high-stakes danger — hence the low composite crisis scores on InvisibleBench. (sourced) A small, dedicated, separately-validated detector can be tuned purely for "never miss," held to a measurable sensitivity number, audited, and swapped out — properties you cannot get from a black-box conversational model. **Safety-critical decisions need a component you can measure and certify, not an emergent behavior you hope for.** (advisory)

**Why a human stays in the loop.** Even the best classifiers carry real false-positive rates and known demographic-bias risk; the model **prioritizes the queue**, a trained counselor **decides and acts.** The measured payoff of getting the *queue* right is enormous: Cerebral's median time-to-triage for crisis messages fell from **about 9 hours to 8–13 minutes**. (sourced — npj Digital Medicine, https://www.nature.com/articles/s41746-023-00951-3, accessed 2026-06-25) That delta — not a fancier model — is the actual life-saving mechanism.

---

## 4. People & resources

Realistic scales for building and running such a system. Figures are order-of-magnitude estimates anchored to the cited deployments unless marked (sourced). The precise dollar ranges below are **not externally validated** — treat them as reasoned estimates.

**Team & roles**
- A working production classifier is a **small team, roughly 3–8 people**: a couple of ML/NLP engineers, a data/MLOps engineer, and — non-negotiable — **embedded clinical experts**. Crisis Text Line explicitly brought clinicians in *at the start*, through the model results, and *after* deployment. (sourced) CRADLE was a joint **Computer Science + Psychiatry** effort. (sourced) (headcount: inference)
- **Annotation is the real cost center, and it must be clinician-grade.** CRADLE used **four clinician annotators** for its evaluation set. (sourced) Expert labels at scale are the dominant expense — not GPUs. (advisory)

**Data scale (note how small it can be — quality over quantity)**
- Production systems have shipped on **hundreds to low-thousands of labeled examples**: Cerebral's deployed model on **721 messages**; (sourced) CRADLE on **~3,000 synthetic dialogues / ~49k turns**. (sourced) Crisis Text Line trains at the **tens-of-thousands-of-conversations** scale.
- The 2026 shift: synthetic data (LLM-generated dialogues from real posts) and **prompt calibration without fine-tuning** sharply cut the data you need to start. (sourced)

**Compute**
- The cheap, deployed path (keyword + logistic regression, or a small neural net) trains on **a single workstation/GPU in hours** and serves at **negligible cost per message** — which is *why* it is what is actually fielded at scale. (inference)
- Fine-tuning a **32B-parameter** specialist (CRADLE) needs a **multi-GPU node for days** — roughly a **few thousand to low-tens-of-thousands of dollars** in compute. (inference, not externally validated)
- Prompting a hosted frontier model needs **zero training compute** — just per-call inference fees. (inference)

**Time**
- A first credible classifier: **a few months** end to end, with **data labeling, clinical validation, and safety/bias review consuming the bulk** of it — not the modeling. (advisory)

**Money (rough total to build + validate, not counting 24/7 human responders)**
- **Low end** (prompted or simple deployed model): tens of thousands of dollars, dominated by clinician annotation and evaluation. (inference, not externally validated)
- **High end** (fine-tuned specialist + rigorous clinical trial + bias auditing): **mid-six to low-seven figures**, again dominated by **expert clinical labor and validation**, not compute. (inference, not externally validated)
- **The dominant ongoing cost is human.** The classifier is cheap; the trained counselors it routes to are the expensive, irreplaceable resource — and the entire system exists to spend their scarce time on the right person first. (advisory)

**Bottom line.** In 2026 the state of the art is *not* "a smart chatbot that notices when you're in danger" — benchmarks show that approach misses the majority of crises. It is a **layered pipeline**: a cheap, high-recall, separately-validated classifier as a deterministic safety net, tuned to almost never miss, feeding a calibrated urgency ranking, with a human making every real intervention. The measured win is mundane and huge — turning a 9-hour wait into minutes.

---

## 5. Scenarios & stories

The technique lives or dies not on the model but on **what happens after the flag fires.** Here is where it works, and where it quietly causes harm.

### Where it's the RIGHT tool

**The triage queue at a peer-support platform.** A digital peer-support service handles tens of thousands of messages a night between strangers. No clinician can read them all. A small RoBERTa-class classifier sits in the pipeline and does exactly one useful thing: it *ranks*, surfacing the ~2% that look like active suicidal ideation to the top of a human supervisor's queue. This is the technique at its best — fast (sub-second), volume genuinely beyond human capacity, and a human still makes the decision. A false positive costs a supervisor thirty seconds; a true positive saves a life that would have scrolled past. Reported performance in this exact hybrid AI-plus-human setting was around **90%** — a number only safe to rely on *because* the human is the backstop. (sourced — https://pmc.ncbi.nlm.nih.gov/articles/PMC12986059/, accessed 2026-06-25) *(Metric-hygiene note: "90% accuracy" inherits the accuracy-as-headline problem; read it as "good enough to prioritize," not as a safety guarantee.)* The lesson: crisis classifiers shine as **attention-allocators in high-volume streams with a human decision-maker downstream.**

**The tiered alert inside a digital mental-health clinic.** A teletherapy company with licensed clinicians on staff runs a "no risk / moderate / severe" classifier on between-session messages; on "severe" it pages the on-call clinician immediately instead of waiting for the next appointment. This works because it *augments an existing clinical relationship* — there is already a treatment plan, a known patient, someone who can call. It is plumbing for an existing duty of care, not a substitute for one.

**The mandated safety layer on a general-purpose chatbot.** When someone tells a general assistant "I don't want to be here anymore," a classifier flags it and the system surfaces crisis resources. This is right not because it is elegant but because **the alternative is worse and the bar is low** — a general chatbot has no clinician, no relationship, no follow-up, so its only honest move on real danger is to hand off. Its narrow job: *recognize, refer, get out of the way.* The danger (below) is when "get out of the way" becomes the answer to everything emotionally heavy.

**Risk-surfacing to a human supervisor at a crisis line.** Inside the 988 ecosystem and Crisis Text Line, classifiers do counselor-matching and quietly highlight phrases in a live transcript so the *human counselor* sees them faster. The model never talks to the person in crisis; it whispers to the professional. This is arguably the single safest deployment pattern: maximum human scaffolding, AI strictly advisory, the cost of a false positive near zero.

### Where it's the WRONG tool

**The false-positive cascade — when the flag *is* the action.** In a study of ~10,000 real sessions from late 2025, an LLM-judge layer flagged 276 conversations for human review; reviewers found **231 of them (~84%) contained no actual risk.** (sourced — https://arxiv.org/pdf/2601.17003, accessed 2026-06-25) Where a human reads each flag, that is tolerable noise. Where the *flag itself* triggers an automated intervention — locking the conversation, dumping hotline numbers onto someone venting about a bad day, notifying a parent — that false-positive rate *is* the harm. The central failure mode: **a crisis classifier is the wrong tool the moment the flag becomes an automated action with no human in between.** Crisis language is genuinely ambiguous; trained clinicians frequently disagree on the same transcript. Automate the consequence and you make every false positive expensive.

**The crisis cliff inside therapy — over-triggering as clinical harm.** The most counterintuitive, best-documented failure. A 2026 study running AI through evidence-based protocols (prolonged-exposure therapy, CBT) found that safety training *actively sabotages treatment.* During exposure therapy the patient is *supposed* to stay with a distressing memory; the safety-trained model keeps interrupting to redirect to "present safety," reinforcing the exact avoidance the therapy exists to extinguish. One model read a trauma narrative being *processed in session* as a live emergency and told the patient to call authorities and evacuate. Between **34% and 42% of responses** contained protocol-violating reassurance like "you are safe," and fidelity hit a "crisis cliff," collapsing to zero for two models. (sourced — https://arxiv.org/html/2604.23445, accessed 2026-06-25) Same technique, opposite contexts, and it cannot tell them apart. **If sustained engagement with distress is the point, a crisis classifier is the wrong tool — it will pull the patient out of the work.**

**The school-surveillance trap — classifier as accidental informant.** Roughly 1,500 US districts run monitoring software (Gaggle, Bark, GoGuardian) scanning about 6 million students' writing for self-harm signals. The intent is benevolent; the reality, documented repeatedly, is not. A self-harm flag led to a student being **outed to an unsupportive family**; a national survey found nearly a third of LGBTQ students knew of someone outed by digital monitoring. The tools flagged students writing about being trans, and absurdly blocked the Trevor Project, an actual LGBTQ suicide-prevention line; Gaggle eventually had to *remove* words like "gay" and "lesbian" from its flag list. (sourced — https://www.the74million.org/article/gaggle-drops-lgbtq-keywords-from-student-surveillance-tool-following-bias-concerns/ and https://www.eff.org/deeplinks/2023/06/student-monitoring-tools-should-not-flag-lgbtq-keywords, accessed 2026-06-25) The technique is wrong here not because the model is inaccurate but because of **what the flag connects to**: the downstream action is disclosure, and the surveilled population cannot consent. **When the people being classified are non-consenting and a flag means exposure, the classifier stops being a safety tool and becomes a surveillance tool wearing safety's clothes.**

**The impostor — classifier-as-counselor.** As real crisis lines lose funding (one San Francisco association cut ~80% of staff in 2025), vulnerable people get funneled to chatbots by default. Some bots actively impersonate help: a Character.AI bot called "988 Prevention Hotline" told users "this is 988 Lifeline" and handed out nonexistent numbers. (sourced — https://sfstandard.com/2025/08/26/ai-crisis-hotlines-suicide-prevention/, accessed 2026-06-25) A classifier can decide *that* someone is in danger. It cannot **be the help.** A classifier that detects crisis and then *pretends to handle it itself* — rather than handing off — is the most dangerous configuration of all: the confidence to flag, none of the capacity to follow through.

### The through-line

A crisis classifier is the right tool when (1) volume genuinely exceeds human capacity, (2) a human makes the final decision and a false positive is cheap, and (3) the goal is to *route to* care, not *be* the care. It is the wrong tool when the flag auto-triggers a consequential action, when the context requires sustained engagement with distress, when the classified population can't consent and a flag means exposure, or when there's no human help on the other side of the handoff. The model is rarely the bottleneck. The make-or-break decision is *architectural and human*: what does the flag connect to, and who catches it?

---

## 6. Cross-industry usage & positioning (as of June 2026)

The important conceptual shift: the field has stopped treating this as an *offline prediction* problem ("score this transcript") and started treating it as **online, safety-oriented monitoring** — continuously watching a live conversation and balancing missed crises against over-escalation in real time. Keyword lists, refusal templates, and generic crisis scripts are now explicitly documented as failure-prone, especially against euphemism, "algospeak," and risk embedded in long or delusional conversations. (sourced, multiple — see Sources)

**The two-layer architecture almost everyone converged on:** (1) a **fast classifier layer** scanning every input/output cheaply (small fine-tuned transformers — RoBERTa-class ~125M models, or distilled LLMs); (2) a **human-in-the-loop escalation layer** for confirmed or ambiguous high-risk cases. Pure automation is now the exception, not the goal — partly clinical humility, partly legal exposure.

**Consumer AI / chatbots — the hottest battleground.** Frontier labs lead: Anthropic runs a dedicated suicide/self-harm classifier scanning active Claude.ai chats, surfacing a country-specific crisis banner, with response design informed by the crisis-support org ThroughLine; OpenAI's late-2025 Model Spec added real-time classifiers that scan *as prompts happen* plus age-prediction defaulting unknown users to an under-18 experience. Companion AI is the cautionary tale: Character.AI faced state lawsuits and wrongful-death settlements and responded by *banning under-18 back-and-forth chat entirely* — a tacit admission that reliable crisis detection in open-ended roleplay is unsolved. The open research problem: risk *embedded in delusion* or built slowly over many turns, where safety interventions can be suppressed up to ~4.5x once distress is wrapped in delusional framing. (sourced — https://arxiv.org/abs/2606.00975, accessed 2026-06-25)

**Crisis lines / digital peer support — the original adopters, most mature.** Crisis Text Line is the canonical pioneer (ML triage before counselor assignment). 988 infrastructure in 2026 is more about georouting (FCC rules) than ML triage, but ML risk-scoring of chat/text is established. Hybrid human+AI is the documented production pattern; AI is triage prioritization, never replacement.

**Healthcare / clinical — high accuracy, real friction.** Multimodal is the cutting edge: combining structured EHR data with LLM-derived text analysis reached AUROC ~0.977 in recent pediatric-ED self-harm work, notably robust across demographic subgroups (the historic weak spot). Explainable, theory-driven lexicons matter because clinicians won't act on a black box, and portability across hospitals (a model trained at one site degrades at another) is an active front. (sourced, see Sources)

**Veterans / defense — largest real-world deployment, sobering results.** The VA's **REACH VET** is the biggest operational suicide-prediction system: a logistic-regression model over EHR data, run monthly, flagging the top ~0.1% of veterans (~6,800/month) for proactive outreach — notably *not* a deep net; interpretability won. The honest scorecard: it improved process outcomes (more completed appointments, more safety plans, fewer ED visits) but a quasi-experimental evaluation found it did **not** reduce death by suicide or all-cause mortality, with tiny PPV (~0.05%) and high false-negative rate. **This is the clearest evidence that high classifier accuracy ≠ lives saved.** (sourced, see Sources)

**Social media / content moderation — ubiquitous but judged inadequate.** Meta, TikTok, Instagram, Pinterest, Snapchat, and X all run suicide/self-harm classifiers at massive scale; under the **EU Digital Services Act** their decisions are now transparency-reported and externally audited. Independent analysis (Molly Rose Foundation; Georgetown KGI, Feb 2026) finds "pronounced deficiencies" — most platforms under-respond, and detection is routinely defeated by algospeak/misspelling.

**Finance / elder-protection — adjacent but real.** Banks deploy call-center analytics detecting voice-stress markers, third-party presence on sensitive calls, and behavioral models flagging cognitive-decline patterns. The "crisis" is acute financial exploitation rather than self-harm, but it is the same classifier-plus-human-escalation pattern, and trained branch staff remain the most effective layer.

**Workplace / HR — emerging and contested.** Vendors (Spring Health, Kyan) embed distress/suicide-risk classifiers in employee mental-health tools, some claiming ~97% flagging of immediate-risk cases with human fallback. Strong ethical headwind: "your boss knows you're struggling before you do."

**State of the art, concretely.** On the **CRADLE-Bench / CRADLE-Dialogue** reference (clinician-annotated, seven crisis types, temporal labels, an Alert-vs-Confirm distinction): *dialogue-level* detection is good (70%+ F1) — *that* a crisis exists is now reasonably detectable — but *turn-level localization* is the wall (~40–60% F1). Detecting early "Alert" signals before explicit disclosure is the weakest capability across every model, and even clinician annotators disagree there (Cohen's κ ~0.51 for Alert labels). Recent turn-level Micro-F1 leaderboard: Claude-4.5-Sonnet ~56.9, Gemini-3-Flash ~53.1, GPT-5.1 ~48.9, fine-tuned Qwen3-32B ~51.3 — domain fine-tuning closes much of the gap with closed models. Frontier LLMs are now *competitive with, but not above,* expert human crisis detection; the residual gap is concentrated in early/implicit signals and ongoing-vs-past disambiguation. (sourced — https://arxiv.org/html/2606.10380, accessed 2026-06-25)

**Regulation — the real forcing function.** *(Verifier correction applied — the widely-repeated "five states require detection" claim is wrong for three of five as of June 2026.)* **In force as of June 2026:** **California SB 243** (effective Jan 1, 2026) — first state law *mandating* companion-chatbot operators maintain a protocol to detect suicidal ideation/self-harm and refer to crisis services; and **New York** (General Business Law §1700, effective Nov 5, 2025) — "reasonable efforts to detect and address" suicidal ideation with referral. **Enacted but NOT yet in effect:** Oregon SB 1546 and Washington HB 2225 were enacted March 2026 but take effect **January 1, 2027** — they do not currently require anything. **Virginia did NOT enact** such a law (SB 796 was not enacted). The **EU AI Act** published draft high-risk guidance in May 2026 (consultation through June 23, 2026), with core high-risk obligations deferred to Dec 2, 2027 / Aug 2, 2028 — so EU crisis classifiers sit in a known-but-not-yet-binding high-risk regime.

**Table-stakes vs. cutting-edge:**

| Sector | Status | Leaders |
|---|---|---|
| Crisis lines / peer support | Table-stakes, mature | Crisis Text Line, 988 ecosystem |
| Consumer / frontier LLMs | Newly mandatory; rapidly maturing | Anthropic, OpenAI |
| Companion AI | Mandatory but unsolved | Character.AI (cautionary tale) |
| Clinical / EHR | Established + multimodal cutting edge | Academic-clinical groups |
| Veterans / defense | Largest deployment; effectiveness contested | VA REACH VET |
| Social media moderation | Ubiquitous but judged inadequate | Meta, TikTok (under DSA audit) |
| Finance / elder protection | Growing, adjacent | Banks, fintech fraud teams |
| Workplace / HR | Emerging, ethically contested | Spring Health, Kyan, EAP vendors |

**Advisory reads (my reasoned synthesis, not sourced fact):** Treat turn-level early detection as *unsolved* — design the human-escalation layer for that gap, not as an afterthought. Optimize for the right error: REACH VET shows chasing offline accuracy can still fail to move the outcome that matters; define success as "right action taken in time" and measure false-negative cost and alarm fatigue explicitly. Expect the classifier to become a *regulated artifact* — build logging, versioning, and an evaluation harness from day one. Multimodal + interpretable is the defensible bet in clinical settings. The hardest adversary is your own product surface — test on multi-turn drift and delusion-embedded distress, not single-prompt benchmarks.

---

## 7. Learning path for a technical leader

*For someone who will steer, fund, staff, and govern this work — not write the model code.*

### Mental models (the load-bearing ideas)

1. **It's a detector with a deliberately lopsided cost function — not a "classifier" in the textbook sense.** A false negative and a false positive are not equally bad, and the gap is enormous and context-dependent. The whole engineering and policy conversation is really about *where you put the threshold* and *who absorbs each error*. Anyone who leads with "accuracy" has missed the point. (advisory + inference)
2. **The classifier is one layer, never the whole safety system.** 2026 best practice treats detection as an *independent* layer running alongside the product, not a feature baked into it — so you can tune, audit, and certify the safety layer on its own, and the product stays genuinely helpful instead of a nervous, over-cautious chatbot. (sourced — arXiv 2601.17003, "Beyond Simulations," Jan 2026)
3. **Crisis is a moment in a conversation, not a property of a document.** The 2025–26 shift is from static text to *turn-level detection in a live dialogue* — at which message did this become a crisis, and is it happening now or being recounted? Models that score ~70 on whether-a-dialogue-contains-risk drop to the mid-50s on pinpointing *which* turn. Fund only document-level work and you're buying yesterday's problem. (sourced — CRADLE-Dialogue, arXiv 2606.10380)
4. **Severity and temporality are clinical distinctions, not engineering ones.** "I wish I weren't here" (passive), "I've thought about how I'd do it" (active with method), and "I have a plan and the means for tonight" (active with plan and intent) are categorically different — the ladder the clinical gold standard (Columbia / C-SSRS) is built on. Likewise past vs. ongoing. A naive system collapses these and routes a recovered patient and an active emergency identically. (sourced — C-SSRS, FDA-preferred instrument since 2012)
5. **Your ground truth is the ceiling.** In multiple 2026 studies, error rates plateaued because the *labels* did, not the models — annotation quality, not algorithm choice, was the binding constraint. This is where the money and months actually go. (sourced — AEGIS/multi-agent work, arXiv 2604.22154; CRADLE-Dialogue)
6. **This is increasingly a regulated medical-device problem.** The FDA is actively shaping how generative-AI mental-health tools are regulated, with crisis-detection-and-escalation called out as a critical compliance requirement: built-in escalation, human-in-the-loop confirmation, post-market monitoring, ISO 14971 risk management. Treat it as a pure software feature and you're exposed legally and clinically. (sourced — Sidley Austin on FDA/CMS actions, Nov 2025)

### Reading spine (small, high-value, in order — the first three give ~80%)

1. **"Beyond Simulations: What 20,000 Real Conversations Reveal About Mental Health AI Safety"** (arXiv 2601.17003, Jan 2026) — the single best leader-level read: real production data, the independent-safety-layer + emergency-mode architecture, and honest numbers on classifier-catch vs. human-review-catch. https://arxiv.org/pdf/2601.17003
2. **"CRADLE-Dialogue: Expert-Level Crisis Detection in Mental Health Conversations"** (arXiv 2606.10380) — the current benchmark; read for the taxonomy (*seven* crisis types, ongoing/past, Alert/Confirm) and the hard truth that turn-level localization is where models fall down. https://arxiv.org/html/2606.10380
3. **FDA/CMS regulatory landscape** — Sidley Austin's briefing on the Nov 2025 FDA actions; short, lawyerly, tells you what "shippable" will legally require. https://www.sidley.com/en/insights/newsupdates/2025/11/us-fda-and-cms-actions-on-generative-ai-enabled-mental-health-devices-yield-insights-across-ai
4. **C-SSRS (Columbia Lighthouse Project), the instrument itself** — twenty minutes makes every clinical conversation legible. https://cssrs.columbia.edu/the-columbia-scale-c-ssrs/
5. **"Reliable Self-Harm Risk Screening via Adaptive Multi-Agent LLM Systems"** (arXiv 2604.22154) — staged-decision design and an honest section on compute cost (fewer false positives, but 20–30× the API calls) and the label-quality ceiling. https://arxiv.org/html/2604.22154
6. **"An AI-Based Behavioral Health Safety Filter and Dataset"** (arXiv 2510.12083) — a concrete production-shaped safety filter with calibration against alert fatigue and demographic auditing. https://arxiv.org/pdf/2510.12083
7. *(Optional, fairness)* any good treatment of **dialect bias in toxic-language detection** (the AAVE/AAE false-positive problem) — the same surface-marker failure mode applies directly to crisis detection. (advisory)

### Checkpoints ("you understand it when you can…")

- **…explain why a 99%-accurate crisis detector can be worthless,** reframing the goal in terms of recall, precision, base rate, and asymmetric cost — without reaching for "accuracy."
- **…draw the C-SSRS severity ladder from memory** and sort five example sentences into passive / active-with-method / active-with-plan-and-intent / past behavior / no-risk.
- **…explain why turn-level detection in live chat is harder than scoring a finished post,** and why "past or happening now?" trips even frontier models.
- **…articulate why the classifier must be a separate layer,** and what "emergency mode" buys over just making the chatbot more cautious.
- **…name the binding constraint (label quality / annotation)** and say what good ground truth looks like (validated instrument, trained annotators, measured kappa).
- **…describe three operational metrics you'd watch in production** beyond test-set F1 (flag rate, classifier-catch vs. human-review-catch, calibration, subgroup false-positive rates, drift).
- **…explain alert fatigue as an engineering failure mode** — how over-tuning for recall can *reduce* real-world safety by burning out reviewers.
- **…state at a board level what makes this a regulated medical device** and what that obligates (escalation, human-in-the-loop, post-market monitoring, ISO 14971 risk file).

### How to evaluate an expert

The throughline: *real experts lead with the cost asymmetry, the clinical grounding, and the system around the model; pretenders lead with model architectures and F1 scores.* (advisory)

- **"How would you measure whether this is good?"** Strong: rejects bare accuracy; leads with recall given asymmetric cost but *also* precision because false positives drive alert fatigue; mentions base rates, calibration, subgroup breakdowns, and live operational metrics; calls the threshold a *policy decision*. Red flag: leads with "accuracy" or can't explain why it misleads when crises are rare.
- **"What are you actually trying to detect, clinically?"** Strong: distinguishes passive vs. active ideation, ideation vs. behavior, ongoing vs. past, self-harm vs. suicidality; references C-SSRS as the labeling backbone. Red flag: dismisses clinical grounding ("the model learns it from data") or has never spoken to a clinician.
- **"Where do these systems actually fail in production?"** Strong: label quality as the ceiling, drift, the static-to-live-dialogue gap, alert fatigue degrading the human layer, fairness failures by dialect/demographic. Red flag: claims it "basically works" — overconfidence is the single biggest danger signal in this domain.
- **"Design the system around the model. What happens after it fires?"** Strong: independent safety layer, graded responses, defined human-in-the-loop pathways and SLAs, emergency mode, logging and post-market monitoring. Red flag: proposes fully autonomous action on high-risk cases with no human — a safety *and* regulatory non-starter.
- **"What are the legal/regulatory obligations?"** Strong: knows crisis-detection-and-escalation is an FDA critical requirement, human-in-the-loop expectations, post-market monitoring, ISO 14971, device classification, data privacy, duty-of-care. Red flag: "that's legal's problem."
- **(Stress test) "Tell me about a time your classifier was confidently wrong."** Strong: a concrete failure, how they *detected* it, and the systemic fix. Red flag: claims they've never had a serious failure.

---

## 8. Team notes

### The one thing to get right

The model is the easy part. As of mid-2026 a competent engineer can stand up a respectable text classifier in a sprint, and frontier LLMs already detect distress well. The hard, expensive, lawsuit-shaped part is everything *around* the model: the clinical taxonomy you classify into, the threshold policy (how sensitive, and who decided), the **emergency-mode** escalation behavior, and the **human review loop**. The predictable org failure: hire three ML engineers, zero clinicians, ship a keyword filter, and discover in a deposition that nobody owned the policy for what happens *after* a flag fires.

### Roles & seniority

You almost certainly do **not** need a dedicated "crisis ML" hire to start — this is a capability an existing Trust & Safety or Applied ML function should absorb, *paired with* clinical and ops roles that are easy to forget.

| Role | Need it? | What they own |
|---|---|---|
| **Applied ML / Trust & Safety engineer** (mid–senior) | Yes — an *existing* one can absorb it | Integrate a bought classifier or fine-tune one; build the independent safety layer; own latency, eval harness, threshold tuning. Not a research role. |
| **Clinical advisor / safety clinician** (licensed; contract to start) | **Yes — the most-skipped role** | Owns the crisis taxonomy, defines a true positive, signs off on escalation copy and thresholds, gives you defensibility. Renting it (advisory firm, ThroughLine-type partner) is fine; *no clinical sign-off at all is the red flag.* |
| **Safety operations / on-call reviewer** | Yes, if flags reach humans | Someone is on the other end of a flag. Crisis review is emotionally heavy; needs trained reviewers, rotation, and mental-health support *for the reviewers*. |
| **Policy / Legal counsel** (regulatory) | Yes — increasingly load-bearing | 2026 brought state chatbot mandates (California SB 243 in force; others coming) — now a compliance deliverable, not a nice-to-have. |
| **Dedicated crisis-ML researcher / PhD** | **No, for almost everyone** | Only if detection accuracy is your actual product (crisis-line vendor, clinical-device company). Otherwise over-hiring. |

**Seniority shape:** one senior owner who can hold the cross-functional seams (ML + clinical + legal + ops) matters more than raw ML depth. A staff-level "this is mine end to end" person beats two junior modelers. (advisory)

### Build vs. buy

Default: **rent the referral layer, rent the model, build only the policy and escalation glue.** (advisory)

- **Referral / helpline routing → BUY.** Maintaining 1,500+ verified, daily-checked, geo-localized helplines across 170+ countries is a full-time operation. Vendors (ThroughLine, Crisis Text Line partnerships) exist for this. Building it is pure cost, zero differentiation, real liability if a number is stale.
- **Detection model → RENT / BUY first.** Off-the-shelf moderation APIs cover self-harm classes; frontier LLMs detect crisis well out of the box; clinician-annotated benchmarks (CRADLE-Bench) let you evaluate vendors against a clinical standard. Start by calling an API and measuring it on your own traffic.
- **BUILD only when detection quality is a genuine moat** — you're a crisis-support product, a regulated device, or you have proprietary data where generic classifiers measurably under-perform. Even then, build the *classifier*, not the helpline database.
- **Always build in-house:** the threshold policy, emergency-mode behavior, and human-in-the-loop workflow. These encode *your* risk tolerance and are what regulators and plaintiffs scrutinize.

**Architecturally non-negotiable:** the safety classifier must be an **independent layer**, separate from the conversational model — not an inference-time guardrail bolted onto the chat model's prompt. 2026 research shows in-prompt safety gets *suppressed up to ~4.5x* once distress is wrapped in delusion or roleplay. (sourced — arXiv 2606.00975)

### Hiring signals

**Green flags:** talks about precision/recall trade-offs and the cost of each error *before* model architecture; has shipped a human-in-the-loop system and respects reviewer workload and wellbeing; asks "who's the clinician?" and "what happens *after* the flag?" unprompted; treats it as a socio-technical system, not a Kaggle problem. For clinical hires: licensed, real crisis-intervention experience, comfortable approving escalation language.

**Red flags:** pitches a pure keyword/regex/static-template approach as sufficient; wants to train a big bespoke model from scratch before measuring whether a bought API meets the bar; never mentions false positives harming users; treats clinical sign-off and regulatory review as someone else's problem; cavalier about reviewer mental health.

### Failure modes

1. **No clinician in the loop** — engineers invent the taxonomy and thresholds; no defensibility, wrong categories, found out in litigation. *(Most common and most damaging.)*
2. **Guardrail-in-the-prompt instead of an independent layer** — works in demos, collapses under roleplay/delusion/jailbreak (suppression up to ~4.5x), exactly for the highest-risk users.
3. **Keyword/template reliance** — misses indirect ideation, trivially evaded, over-fires on benign mentions (song lyrics, recovery talk, dark humor).
4. **Flag fires into the void** — detection with no funded, staffed escalation path. The classifier is the cheap 20%; the on-call human response is the expensive, neglected 80%.
5. **Tuning only for recall, ignoring precision** — over-intervention is its own harm and trains users to dismiss warnings.
6. **Reviewer burnout, unmanaged** — crisis review is traumatic; no rotation/support means attrition and degraded judgment on the most important calls.
7. **Building the helpline database** — months of work, stale within weeks, zero differentiation, direct liability.
8. **Ignoring the 2026 regulatory wave** — state detection mandates, under-18 guardrails, FDA scrutiny of GenAI mental-health "devices," active lawsuits/settlements. Legal is a core teammate, not a downstream reviewer.

### Recommended starting shape (advisory)

1. One **senior T&S/Applied-ML owner** (existing headcount if possible) — owns integration, eval, and the seams.
2. **Contract a licensed clinical advisor** before writing the taxonomy or any thresholds.
3. **Buy** the model (start as an API call) and **buy** the helpline/referral layer.
4. **Build** only: the independent safety layer, threshold policy, emergency mode, and human-review workflow.
5. Loop in **regulatory counsel** from day one.
6. Stand up a **staffed, supported reviewer rotation** before you turn flagging on.

Scale to dedicated crisis-ML researchers *only* if and when detection accuracy becomes your actual product.

---

## Sources

- Crisis Text Line — *What we learned training an ML model to detect suicidal risk*: https://research.crisistextline.org/what-we-learned-from-training-a-machine-learning-model-to-detect-suicidal-risk-2c65f1d4d9eb (accessed 2026-06-25)
- Crisis Text Line — *Detecting Crisis: An AI Solution* (supports the 86%-first-conversation figure; AUC ~90%): https://www.crisistextline.org/blog/2018/03/28/detecting-crisis-an-ai-solution/ (accessed 2026-06-25)
- *NLP system for rapid detection of mental health crisis chat messages*, npj Digital Medicine 2023 (Cerebral: keyword+logistic regression, 721 training msgs, AUC 0.98, 9h→8–13min): https://www.nature.com/articles/s41746-023-00951-3 (accessed 2026-06-25)
- *CRADLE-Dialogue: Expert-Level Crisis Detection in Mental Health Conversations* (Qwen3-32B fine-tune, 3,058 synthetic dialogues, SEVEN crisis types, 4 clinician annotators, 51.3 Micro-F1): https://arxiv.org/html/2606.10380 (accessed 2026-06-25)
- *CRADLE-Bench* (clinician-annotated benchmark, EACL 2026 — distinct from 2606.10380): https://arxiv.org/abs/2510.23845 (accessed 2026-06-25)
- *Suicide- and crisis-risk detection using LLMs in mental-health chatbots*, medRxiv 2026 (near-zero-miss via prompt calibration): https://www.medrxiv.org/content/10.64898/2026.01.12.26343914v1 (accessed 2026-06-25)
- *InvisibleBench: A Deployment Gate for Caregiving Relationship AI* (composite crisis-safety scores; deterministic routing required): https://arxiv.org/abs/2511.20733 (accessed 2026-06-25)
- *Between Help and Harm: Evaluation of Mental Health Crisis Handling by LLMs*, JMIR Mental Health 2026 (crisis taxonomy): https://mental.jmir.org/2026/1/e88435 (accessed 2026-06-25)
- Therabot crisis-classification / emergency module (separate deterministic crisis model): https://talk.crisisnow.com/the-generative-ai-therapy-chatbot-will-see-you-now/ (accessed 2026-06-25)
- SAMHSA 988 FAQ (988 contact volumes; treat exact totals as a moving, dated snapshot): https://www.samhsa.gov/mental-health/988/faqs (accessed 2026-06-25)
- *Effectiveness of Hybrid AI and Human Suicide Detection Within Digital Peer Support*, PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC12986059/ (accessed 2026-06-25)
- *Beyond Simulations: What 20,000 Real Conversations Reveal About Mental Health AI Safety*, arXiv 2601.17003 (Jan 2026): https://arxiv.org/pdf/2601.17003 (accessed 2026-06-25)
- *AI Safety Training Can be Clinically Harmful*, arXiv 2604.23445 (the "crisis cliff" / therapy-protocol study): https://arxiv.org/html/2604.23445 (accessed 2026-06-25)
- *Reliable Self-Harm Risk Screening via Adaptive Multi-Agent LLM Systems*, arXiv 2604.22154: https://arxiv.org/html/2604.22154 (accessed 2026-06-25)
- *An AI-Based Behavioral Health Safety Filter and Dataset*, arXiv 2510.12083: https://arxiv.org/pdf/2510.12083 (accessed 2026-06-25)
- *Lost in Delusion: LLM Safety Under User Delusions and Distress*, arXiv 2606.00975 (~4.5x safety suppression under delusional framing): https://arxiv.org/abs/2606.00975 (accessed 2026-06-25)
- *Crisis hotlines are getting wiped out…*, SF Standard (Aug 2025): https://sfstandard.com/2025/08/26/ai-crisis-hotlines-suicide-prevention/ (accessed 2026-06-25)
- *Gaggle Drops LGBTQ Keywords from Student Surveillance Tool*, The 74: https://www.the74million.org/article/gaggle-drops-lgbtq-keywords-from-student-surveillance-tool-following-bias-concerns/ (accessed 2026-06-25)
- *Student Monitoring Tools Should Not Flag LGBTQ+ Keywords*, EFF: https://www.eff.org/deeplinks/2023/06/student-monitoring-tools-should-not-flag-lgbtq-keywords (accessed 2026-06-25)
- C-SSRS (Columbia Lighthouse Project), FDA-preferred instrument since 2012: https://cssrs.columbia.edu/the-columbia-scale-c-ssrs/ (accessed 2026-06-25)
- Sidley Austin — *US FDA and CMS actions on generative-AI-enabled mental-health devices* (Nov 2025): https://www.sidley.com/en/insights/newsupdates/2025/11/us-fda-and-cms-actions-on-generative-ai-enabled-mental-health-devices-yield-insights-across-ai (accessed 2026-06-25)
- ThroughLine — crisis support for any platform: https://www.throughlinecare.com/ (accessed 2026-06-25)
- Sightengine — Self-harm & Suicide Moderation Guide (2026): https://sightengine.com/self-harm-mental-health-suicide-moderation-guide (accessed 2026-06-25)

*Regulatory status note (June 2026): only California SB 243 (eff. Jan 1, 2026) and New York Gen. Business Law §1700 (eff. Nov 5, 2025) impose in-force chatbot crisis-detection mandates; Oregon SB 1546 and Washington HB 2225 were enacted but take effect Jan 1, 2027; Virginia did not enact such a law.*
