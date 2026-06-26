# Voice-to-voice / real-time speech loops

*State of the art as of June 2026. Factual claims are labeled sourced (with a URL and date in the Sources list), inference, or speculation. Learning-design and org recommendations are labeled advisory — these are my reasoned judgment, not established fact.*

---

## 1. What it is

A voice-to-voice loop is the machinery that lets you *talk* to a computer and have it *talk back* in something close to the rhythm of human conversation. You speak, it understands, it thinks, it answers out loud, and — this is the part that makes it feel alive — you can cut it off mid-sentence and it shuts up, the way a real person would.

The hard part is not any single piece. It is the *loop* and its *timing*.

The benchmark everyone is chasing is human turn-taking. When people talk, they answer each other with gaps of only about **200 milliseconds** — a number that holds remarkably steady across ten languages (sourced). Below roughly 300ms, a machine reply feels alive. Above 800ms, it feels like a bad phone call with a robot. Almost every technical decision in this field is downstream of that one number.

There are two fundamentally different ways to build the loop in 2026, and the industry has *not* converged on one. It has split by use case.

- **The cascade (pipeline).** Three separate models chained together: Speech-to-Text (STT) turns your voice into words, a Large Language Model (LLM) reasons over those words, and Text-to-Speech (TTS) turns the answer back into sound. Audio becomes text, text gets thought about, text becomes audio. This is still the **dominant pattern in production**, especially for phone/telephony, compliance-heavy, and cost-sensitive deployments (sourced).

- **The native / end-to-end model (speech-to-speech, or "S2S").** A *single* model that takes audio in and emits audio out, never fully converting to text in the middle. OpenAI's `gpt-realtime-2`, Google's Gemini Live native audio, and Kyutai's open-source Moshi are the flagships (sourced). Faster and more natural-sounding, harder to control and audit.

A useful third category sits between them — sometimes called **"half-cascade"** (speech goes straight in, but the answer is generated as text first and then spoken) and sometimes called **"thinker-talker"** (the model deliberately reasons in text, then speaks the result). These are overlapping but not identical ideas: half-cascade is about *where the modality boundary sits* in the I/O path; thinker-talker is a *design choice* to reason in text before speaking. Both trade a little naturalness for a lot of control.

One framing correction worth making up front, because it appears in a lot of breathless coverage: it is *not* true that the best systems have abandoned the cascade. Native S2S is the cutting edge and the fastest-feeling option, but every serious 2026 source — including the technical and org material this chapter is built from — agrees the **cascade still wins the regulated and enterprise core** (sourced/inference). The accurate statement is "native is rising and feels the most human; cascade still ships the most production traffic," not "the cascade is dead."

---

## 2. How it works

### The cascade, and why it is not as slow as it sounds

The naive mental model is: record everything you said, transcribe it, think, then speak. That would be unusably slow — you would stack three full model runs plus a silence timeout, one after another.

The trick that makes modern cascades competitive is **streaming and overlap**: every stage starts working before the previous one finishes (sourced).

- The STT emits **partial transcripts** *while you are still talking*. "I'd like to book a..." appears on the wire before you have finished the sentence.
- Those partials feed the LLM immediately.
- As the LLM produces its first few words, those words pipe into the TTS, which begins synthesizing audio *before the full answer exists*.

Done well, this gets total end-to-end latency **under about 700ms** (sourced). And the text sitting between each stage is not just plumbing — it is a feature. You can *log* exactly what was heard, what was decided, and what was said. That auditability is a large part of why regulated industries prefer the cascade (sourced).

### The turn-taking problem — the real heart of it

The deepest engineering problem is not transcription or synthesis. It is **knowing when you have finished talking** so the machine can answer without (a) talking over you or (b) leaving an awkward silence. This is called "endpointing" or "turn detection," and 2026 is the year semantic methods went mainstream. There is a clear ladder of sophistication (sourced):

1. **Silence-threshold VAD (Voice Activity Detection).** The oldest method. Wait for, say, 800ms of silence, then assume the user is done. Simple, but it *adds that full delay to every single response*, and it guesses wrong constantly — it cuts you off when you pause to think, and it waits forever when you trail off.

2. **Endpointing on the transcript.** Watch the *words* coming out of the STT for signals that the sentence is grammatically complete. Faster than waiting on raw silence.

3. **Semantic VAD / model-based turn detection.** A small classifier reads the partial transcript *and* its meaning and predicts "this person is actually done" — distinguishing "I want to fly to... [thinking] ...Boston" from a genuine stop. This pulls the gap from the 800–1500ms typical of silence-based systems back toward the human ~300ms, without chopping people off mid-thought. (LiveKit's open-weights turn-detector, fine-tuned from a small Qwen2.5-0.5B model, is a concrete public example.)

The lesson is that silence is a terrible proxy for "done," and the field's progress has been a steady move from *measuring silence* to *measuring meaning*.

### Barge-in (interruption)

A real conversation lets you cut in. So turn detection stays *active even while the agent is speaking* (sourced). The instant it detects genuine user speech, it **cancels the in-progress TTS stream and hands the floor back**. This requires **acoustic echo cancellation** so the system does not mistake *its own voice* — coming out of your speaker and back into your mic — for an interruption (sourced).

A further refinement is **barge-in confidence**: telling a real interruption apart from a *backchannel* — an "uh-huh," "yeah," "right" — which should *not* stop the agent, because humans say those to mean "keep going" (sourced). Getting this wrong in either direction is the symmetric failure: stop on a cough (false barge-in), or plow through a real interruption (missed barge-in). Either makes the agent feel broken regardless of how smart its words are.

### The native model: Moshi as the clearest worked example

Native S2S models throw out the whole "decide whose turn it is" machinery. Kyutai's Moshi is open source and fully documented, and it shows the mechanism cleanly (sourced):

- An audio **codec (Mimi)** chops the sound waveform into a stream of discrete "audio tokens" at **12.5 frames per second** — small chunks the model can predict like words. Crucially, these tokens split into **semantic tokens** (the words and meaning) and **acoustic tokens** (the voice, tone, room, emotion). That split is the deep idea under almost every native-audio model: it is what lets a system keep *what* you said while changing *how* it sounds.
- Moshi is **dual-channel and full-duplex**: at *every 80ms frame* it simultaneously listens to a stream of *your* audio tokens and predicts its *own*. There is no harness deciding "now it is the model's turn" — at each frame the model is free to speak, stay silent, backchannel, or interrupt, just like a person.
- An **RQ-Transformer** does the prediction in two directions: a big "Temporal Transformer" (built on a 7-billion-parameter text LLM) handles the flow over *time*, and a small "Depth Transformer" fills in the stacked audio tokens needed *per frame* for high-fidelity sound.
- A trick called **"inner monologue":** alongside the audio it is about to speak, the model also predicts the *text* of what it is saying, a beat ahead. Thinking in text first sharply improves the coherence of the speech — it is effectively reasoning in words and rendering in audio at the same time.

Result: Moshi hits a theoretical **160ms** latency (80ms frame + 80ms acoustic delay) and about **200ms in practice** on a modest GPU like an L4 (sourced).

### A note on the latency numbers you will see

Commercial natives land in a similar range. Public leaderboards (the Artificial Analysis speech-to-speech board, April 2026) report a spread of roughly **0.78s (xAI Grok Voice) to 2.98s (Gemini 3.1 Flash Live)**, with `gpt-realtime-1.5` around **0.82s** and Amazon Nova 2 Sonic around **1.14s** (sourced).

One correction on the metric label: for a speech-to-speech model, the relevant number is **time to first *audio* (TTFA)**, not "time to first token." The figures above are correct, but they measure when you first *hear* a reply — calling it "first token" is the wrong name for an audio-out model (sourced).

---

## 3. Why it works

**The core principle: preserve information, and overlap computation.**

The naive cascade destroys two things by routing everything through text.

- **It throws away the *how* and keeps only the *what*.** When your words become plain text, you lose pitch, pace, emphasis, hesitation, sarcasm, emotion — all the *prosody* that carries meaning. The TTS then has to *guess* the prosody back from scratch. Native audio models keep the sound nuances all the way through, which is why they sound more expressive and can do things like match the user's emotional tone (sourced). This is the same semantic-vs-acoustic split from Moshi, seen from the outside: the acoustic information survives the trip.

- **It serializes work that should overlap.** A naive "wait for the whole turn, then run three models in sequence" stacks three full latencies plus a silence timeout. Streaming partials and starting each stage early is *why* the cascade survives at all in 2026 (inference).

**Why turn-taking is the thing that actually breaks naive systems.** Silence is a bad proxy for "done." Humans pause *inside* a thought constantly. A silence-only system faces an unwinnable tradeoff: a short timeout interrupts thinkers, a long timeout feels sluggish. The escape is to stop measuring *silence* and start measuring *meaning* (semantic VAD), or to abandon discrete turns entirely (full-duplex natives) (sourced/inference).

**Why the native model is not a clean win, despite being faster and richer.** The honest tradeoffs here are narrower than the common framing suggests, so it is worth getting them exactly right:

- *The overstated version* you will hear is that native S2S is "a black box — no text in the middle to log, inspect, or correct." **That is wrong.** OpenAI's Realtime API and Google's Gemini Live API both stream input *and* output transcript deltas alongside the audio, and Moshi's inner monologue literally emits text. You *can* log and inspect a native model's transcripts (sourced).
- *The accurate version* of the gap is two narrower things. First, **you cannot swap STT, LLM, or TTS components independently** — you are locked to one vendor's whole stack, where a cascade lets you mix best-of-breed parts. Second, in a native model the text is a *derived, parallel artifact*, not the actual decision substrate. In a cascade, the text *is* what the LLM reasoned over, so a redaction or audit at the text boundary is authoritative; in a native model it is a faithful-but-secondary readout. For hard compliance (redacting PII before it reaches the model, for example) that distinction matters a great deal.

**On cost.** Natives bill per *second of audio*, so as conversation history grows, cost drifts upward in ways that are harder to forecast, while cascades bill in transparent per-minute components you can budget in advance (sourced). That said, the absolute native price has dropped sharply — the cascade-vs-native gap on cost has narrowed, not widened (see People & resources for current numbers).

**The quality argument has largely evaporated.** The best open-source TTS (Sesame CSM at about 4.7 MOS) now sits within roughly 0.1–0.3 MOS of the top commercial APIs (ElevenLabs around 4.8) (sourced). The battleground has moved from "does it sound good" to "is it fast, controllable, and cheap." That control-and-auditability gap — not quality — is exactly why cascaded pipelines still win telephony, compliance, and cost in 2026 (sourced).

---

## 4. People & resources

There are two very different cost worlds, depending on whether you are *training a native model* or *building a product on existing APIs*.

### A) Training a frontier native speech-to-speech model (the hard path almost nobody needs)

Moshi is the best-documented public data point (sourced):

- **Compute:** trained on **1,016 NVIDIA H100 GPUs** (127 DGX nodes).
- **Model:** initialized from a **7-billion-parameter** text LLM (Helium), itself trained on 2.1 trillion text tokens.
- **Data scale:** about **7 million hours** of unlabeled audio (transcribed by Whisper), plus targeted fine-tuning sets — 2,000 hours of phone conversations, ~170 hours of hand-collected multi-speaker dialogue, and ~20,000 hours of *synthetic* model-vs-user dialogue generated by their own TTS.
- **Team:** a focused research lab (Kyutai), on the order of **10–20 core researchers/engineers** for the model itself (inference, from author lists and lab size).
- **Money:** no public dollar figure, but roughly 1,000 H100s for a multi-week run is a **low-seven-figure** compute bill (order $1–5M), before salaries and data infrastructure (speculation — an order-of-magnitude estimate from GPU-hour pricing).

That is the bar to build the *engine*. Almost no one needs to. That is the point.

### B) Building a production voice agent on existing APIs (the path 99% take) — advisory

This is now an *applications* problem, not a research problem.

- **Roles:** 2–5 people is typical for a serious agent — one or two backend/voice-infra engineers (latency tuning, telephony, echo cancellation, barge-in), one prompt/conversation designer, and a domain owner. Orchestration frameworks (LiveKit, Pipecat, vendor SDKs) remove most of the plumbing.
- **Time:** a usable prototype in **days to a couple of weeks**; a production-hardened agent (interruptions, edge cases, monitoring, compliance) in **1–3 months**.
- **Compute:** effectively none of your own if you use hosted APIs; a single modern GPU if you self-host open models (Moshi runs real-time on one L4) (sourced for Moshi/L4).

**Running cost — the number that actually matters.** All-in, **$0.05–$1.00 per minute** (sourced). The spread is enormous and worth internalizing:

- **Component cascade, self-hosted/budget:** STT as low as **~$0.0015–0.012/min** (e.g. Parakeet ~$0.0015/min, Cartesia Ink-Whisper ~$0.00217/min) (sourced).
- **Managed native:** here a stale figure circulates that is worth correcting. The old "~$0.30/min" anchor reflects **GPT-4o-era** realtime pricing. Current `gpt-realtime` speech-to-speech bundles are reported around **~$0.06/min**, and Amazon Nova 2 Sonic lands around **~$0.015–0.017/min** (sourced). Native per-second billing still drifts up with conversation length, but the headline native cost is roughly **4–5x lower** than the old number suggests — which strengthens, not weakens, the point that the cascade-vs-native cost gap has narrowed.
- **All-in-one managed platforms:** **$0.25–0.50/min**; infra-layer platforms **$0.05–0.15/min** (e.g. Retell around $0.07/min) (sourced).

**Advisory takeaway.** The 2026 build decision is rarely "which model is best." It is **cascade vs. native**, and it should be driven by your *non-negotiable*. If you need auditability, telephony, regulatory logging, or tight cost control, choose **cascade with semantic turn detection**. If you need the most human-feeling, emotionally responsive consumer experience and can accept vendor lock-in and per-second billing, choose **native S2S**. The latency gap has narrowed enough (good cascades under ~700ms vs. natives ~250–800ms) that for most business voice agents it is no longer the deciding factor.

---

## 5. Scenarios & stories

Four questions sort good fits from bad ones fast, so I will lead with them and then show them in action (advisory):

1. **Are the user's hands and eyes busy, or is voice their only channel?** Driving, picking, accessibility, phone-native → voice is genuinely native. Sitting at a screen → you need a better reason than "it feels modern."
2. **Is the task structured and bounded, or open-ended and high-stakes?** Capturing and looking up data → strong. Reasoning, judgment, distress, irreversible decisions → weak; design for handoff.
3. **Does the user ever need to scan back, compare, or keep a record?** Voice is linear and ephemeral. Reference-heavy material wants a screen.
4. **What does a wrong answer cost, and how fast can it be corrected?** "No pickles" is free to fix. A dosage, a wire transfer, or a legal clause is not — and a fluent voice loop will be confidently wrong at the worst moments.

### Where it is the right tool

**The hospital scheduling line that never rings busy.** A regional hospital network has four receptionists fielding 2,000 calls a day; at peak, hold times hit eleven minutes and a third of callers hang up. A native S2S agent takes the booking line. "I need to move my Thursday cardiology thing to next week, mornings are better." The agent confirms identity, pulls the calendar, offers two morning slots, books one, reads back the confirmation — ninety seconds, no hold, no menu tree, and it handles Spanish and Vietnamese callers without a "press 2" detour. *Why it fits:* high volume, structured, the job is to capture and look up data, not to reason open-endedly. Cost is the clincher — roughly $0.30–0.50 per call versus $7–17 for a human.

**The language tutor that lets you sound stupid in private.** A Korean professional practices English on her commute. She stumbles, restarts, mangles the past tense; the AI gently recasts her error in its reply ("Oh, so you *went* to Busan last weekend?") and keeps momentum. She would never risk this in a class of ten strangers. *Why it fits:* low-stakes, infinitely patient, real-time spoken practice — and the skill being trained *is* speaking, so voice is the entire point. A small imperfection in the reply is harmless, even useful as natural conversation.

**The drive-thru and the warehouse — hands and eyes already busy.** A driver holding a wheel says "two number fours, one no pickles, swap one fries for a side salad"; a warehouse picker with full hands asks where bin 47-C is. *Why it fits:* the user's hands and eyes are committed elsewhere, the task is bounded, barge-in matters (changing your mind mid-order), and a small mistake is cheap and instantly correctable. This is voice-as-interface-of-necessity, the strongest case.

**Accessibility — the only practical channel.** A user with low vision and limited fine motor control banks entirely by voice: "What did I spend at the pharmacy this month? Move two hundred to savings... no, the *other* pharmacy." *Why it fits:* when voice is the user's *primary* viable input, the loop is not convenience, it is access.

### Where it is the wrong tool

**The cancellation call where someone is crying.** A telecom routes *all* inbound calls, including cancellations, to a voice agent. A customer calls because their spouse just died and they need to close the account; the agent plows through a retention script and offers a loyalty discount. *Why it is wrong:* open-ended, high-stakes, emotionally sensitive conversations are the textbook weak case. 2026 systems detect frustration better than before, but detecting an emotion is not the same as having the judgment to respond to a grieving human. The right design recognizes the emotional register and *hands off to a person*.

**The medical triage that hallucinated a dosage.** A telehealth startup lets a voice agent answer "quick medical questions." A parent asks how much fever medication to give a toddler; the agent — running fast, with heavy reasoning off because reasoning adds seconds and breaks the conversational feel — gives a confident, fluent, *wrong* answer. *Why it is wrong:* there is a structural tension here. To stay conversational, native loops *skip* the slow deliberate reasoning frontier text models use, and native speech models still have measurably weaker text reasoning than a top text LLM (sourced). Fluent, confident, instant, and wrong is the worst combination where a wrong answer harms someone. Medical, legal, and financial judgment belong to deliberate, auditable, text-or-human paths — ideally with a citation you can check, which a voice reply hides.

**The legal contract review done out loud.** A founder tries to review a 40-page term sheet by talking. Twenty minutes in, they are lost — which clause was the liquidation preference? What did it say three exchanges ago? *Why it is wrong:* voice is a *linear, ephemeral* medium; you cannot scan back, see structure, or compare paragraphs side by side. Dense, reference-heavy material is what text and a screen are for. It also burns money — a one-hour balanced conversation can pass $10 in audio tokens versus pennies for the text equivalent.

**The "voice-first" internal tool nobody uses.** A company replaces its text helpdesk bot with a voice loop because voice felt modern. Now employees in an open-plan office have to say "I think I got phished, can you reset my..." within earshot of forty colleagues. They quietly go back to email. *Why it is wrong:* voice fails the social and environmental test in open offices, libraries, quiet trains — anywhere privacy or silence matters — and it is a poor fit for anything async. Modernity is not a use case.

**The complex agentic workflow that needed an audit trail.** A bank wires a voice agent into a flow that can move money, change beneficiaries, and close accounts from what the caller says. A misheard accent turns "don't transfer" into "do transfer," and barge-in handling resets mid-instruction; afterward the bank cannot produce a clean record of *what was decided and why*. *Why it is wrong (mostly):* the action layer needs determinism, confirmation, and an auditable record — properties a fluid audio loop works against. The fix is not to abandon voice; it is to use the loop only for the *conversation* and route every consequential action through an explicit confirm step and a text/structured audit path.

*(One factual cleanup on this last story, since regulatory specifics get cited as leverage: an earlier draft invoked "the August 2, 2026 EU AI Act high-risk obligations now in force." That is wrong on two counts. In a June 2026 scenario, August 2 is in the future. More importantly, the EU "Digital Omnibus" provisional agreement defers the Annex III **high-risk** obligations — the audit-trail hook this story leans on — to **December 2, 2027**. August 2, 2026 remains a live date only for *other* provisions: Article 50 transparency, general-purpose-AI penalty powers, and market surveillance — not the high-risk audit obligations (sourced).)*

The pattern winning in 2026: **voice loop for the conversation, explicit confirmation plus a text/structured path for anything consequential, and a fast handoff to a human the moment the call turns emotional or open-ended.** The loop is a brilliant front door. It is a dangerous back office.

---

## 6. Cross-industry usage & positioning (as of June 2026)

### The technical state of the art

**Audio-native models are now production-grade, not demos.**

- **OpenAI** shipped **gpt-realtime-2 (May 2026)** — its first voice model with **GPT-5-class reasoning fused directly into the audio stream**, a **128K context window** (4x the prior 32K), and configurable reasoning effort (minimal through xhigh). Alongside it: gpt-realtime-translate (live translation across 70+ input languages) and gpt-realtime-whisper (streaming STT). Note that **gpt-realtime-1.5 is now the predecessor**; the 0.82s latency figure cited on leaderboards belongs to that earlier model (sourced).
- **Google** runs the **Gemini Live API** in production on **Gemini 3.1 Flash** native audio, with sub-second turn latency. Processing audio in one model instead of the STT→LLM→TTS chain trims roughly 100–200ms per turn and preserves pitch/pace/emotion (sourced).
- **Amazon** released **Nova 2 Sonic** (speech-to-speech), with telephony integrations (Amazon Connect, Twilio, Vonage), 7 languages, polyglot voices, and up to a 1M-token context window (sourced).

**Latency has crossed the "feels human" threshold.** Dedicated TTS engines now beat the 200ms human gap on synthesis alone: **Cartesia's Sonic** claims sub-100ms model latency; **ElevenLabs** advertises sub-100ms with 70+ languages. End-to-end audio-native loops land in the sub-second range (sourced for the existence of the claims; the exact millisecond figures are vendor-reported — inference on precision).

**Interruption handling is the quiet differentiator.** Cascade systems bolt on a separate turn-detection model; audio-native and especially full-duplex models (Moshi, hertz-dev) handle barge-in essentially for free because they never stop listening. This is why the new models *feel* less robotic (sourced).

**On-device is the next battleground, mostly still ahead of us.** The frontier loops are cloud-bound today. Apple's conversational "LLM Siri" (expected 2026), Mercedes' Liquid AI partnership, and Picovoice/on-device MLX demos point toward private local loops — but in June 2026 the genuinely good experiences still run in the cloud (sourced + inference).

### Sector by sector

- **Customer support / contact centers — TABLE-STAKES.** The center of gravity and a real business, not a demo. McKinsey-cited figures put AI-voice contact centers at 40–50% cost reduction. The platform layer is mature: **Vapi** (orchestration, ~62M calls/month), **Retell** (enterprise compliance, structured flows), **ElevenLabs** (voice quality, now an $11B company), **Deepgram** (unified STT/TTS, noisy environments), **Cartesia** (lowest latency), with **LiveKit** and **Pipecat** as the WebRTC/transport plumbing nearly everyone builds on. Replacing IVR menus and hold queues is now ordinary (sourced).
- **Healthcare — MOVING FROM CUTTING-EDGE TO TABLE-STAKES.** Administrative voice (scheduling, refills, insurance verification) is becoming standard. The frontier is clinical-adjacent: **Hippocratic AI** leads, launching "AI Front Door" and "Nurse Co-Pilot" (April 2026) for post-discharge follow-up and chronic-care check-ins. HIPAA-compliant voice is now a product category (Retell, Parloa) (sourced).
- **Finance — CONTESTED, defined by a security crisis.** Banks deploy voice agents for service, *and* voice authentication is collapsing — deepfake/voice-cloning fraud rose sharply, and Sam Altman publicly called voiceprint auth "crazy." The real frontier is defensive: voice biometrics combined with multi-factor and behavioral analytics, plus real-time deepfake detection. Adoption of AI-based fraud defense lags (one cited figure: ~22% of institutions) (sourced).
- **Coding / dev tools — CUTTING-EDGE, genuinely useful.** Voice as a throughput hack: speaking runs 150–200 WPM vs. 40–60 typing, a 3–4x speedup on every prompt to a coding agent. ChatGPT voice mode, a Claude Code voice mode, and dictation tools like Typeless are the visible tools. Still niche relative to typed prompting (sourced).
- **Consumer assistants — CUTTING-EDGE → TABLE-STAKES.** Apple's "LLM Siri" (expected spring 2026) aims for a conversational, on-device, private experience; Google (Gemini) and OpenAI (ChatGPT voice) already deliver strong cloud loops. The leader is whoever wins the on-device, always-available, private experience (sourced + inference).
- **Automotive — TABLE-STAKES (basic) / CUTTING-EDGE (LLM-grade).** In-car voice market ~$3.3B (2026). **Cerence** is the incumbent backbone (500M+ vehicles). **Mercedes-Benz** (MBUX, multi-LLM, Liquid AI for on-device privacy in H2 2026) and **BMW** lead the premium conversational frontier (sourced).
- **Education / language learning — TABLE-STAKES for speaking practice.** Real-time tutors give unlimited speaking practice at near-zero marginal cost: **Duolingo** (Speak/Max) plus specialists (Speak, Langua, issen) in 100+ languages. The honest limit: feedback loops still are not tight enough for advanced (B1→B2) learners, so AI+human blends win (sourced).
- **Legal — EMERGING → TABLE-STAKES (intake only).** Voice loops replace static intake forms with conversation — capturing names, issue type, deadlines, conflict-check parties, and routing to attorneys with real-time human takeover. Tools: Lawmatics, CloudTalk, CaseGen. Confidentiality is the live concern; adoption stats are vendor-reported (sourced — soft).
- **Defense / robotics — CUTTING-EDGE, procurement-stage.** The U.S. Army is building voice-controlled robots (combat vehicles, bomb disposal) using bidirectional speech for command-and-control. 2026 is described as the year defense robotics moves "prototype to procurement." Voice is the natural interface for hands-busy, eyes-busy operators (sourced).

### The quick map

- **Table-stakes (you are behind without it):** contact-center deflection, healthcare scheduling, language-speaking practice, basic in-car voice, legal intake.
- **Cutting-edge (leaders differentiate here):** audio-native full-duplex loops, sub-200ms emotionally-aware responses, on-device private loops, voice-driven coding agents, clinical-grade healthcare voice, voice-controlled robotics.
- **Contested / unstable:** voice as an *identity* mechanism in finance — actively breaking under deepfakes.

### Advisory: how to read this if you are deciding where to invest or build

1. **Default to the cascade; reach for audio-native when emotion/interruption/latency *is* the product.** For a refill-reminder bot, the STT→LLM→TTS stack is cheaper, more debuggable, and component-swappable. Audio-native earns its keep when the *feel* of the conversation is the value — de-escalating an angry caller, a tutor, a companion, a clinical check-in. Do not pay the native premium for a glorified phone tree.
2. **Buy the orchestration layer; do not build the plumbing.** LiveKit/Pipecat for transport, Vapi/Retell for orchestration, a swappable model layer. The hard, undifferentiated work is turn-taking, telephony, and failover — let the platform own it.
3. **In finance, treat voice as a convenience channel, never as proof of identity.** Anything that authenticates on voice alone is already a liability.
4. **The on-device race is the real 2026→2027 story.** Whoever delivers a frontier-quality loop that runs locally unlocks regulated and consumer markets the cloud cannot fully serve. Watch this more than incremental cloud-model benchmarks.
5. **Discount vendor-reported adoption and latency stats.** Model-vendor announcements (OpenAI, Google, Amazon) and the ElevenLabs raise are solid; the "74% of firms already use X" survey numbers are softer.

---

## 7. Learning path for a technical leader

*For someone who needs to reason about, fund, staff, and evaluate this work — not implement it.*

### The seven mental models everything hangs on

1. **The latency budget is the master constraint.** Teams target a total voice-to-voice latency around **800ms** (the outer edge of "feels attentive"; the *best* feel is nearer the ~300ms human gap). That budget is *spent*, not free — network round-trip, endpointing, model thinking, and first-audio generation all draw from it. When an engineer talks, listen for whether they think in a *budget* (good) or a single average number (naive) (sourced).
2. **Cascade vs. speech-to-speech is the central architectural fork.** Cascade = three swappable models, maximum control and grounding, more latency and more failure points. Native audio = one model, lower latency and more natural speech, but a black-boxier, vendor-locked path. There is no universal winner; the mature instinct is "cascade when you need control and grounding; native audio when you need naturalness and speed" (sourced).
3. **Speech becomes tokens, just like text — via a neural audio codec.** A codec (the reference is **Mimi**, from Kyutai) chops audio into discrete tokens that split into **semantic** (content) and **acoustic** (voice, tone, room, emotion). That split is why a model can keep *what* you said while changing *how* it sounds. If someone cannot explain semantic-vs-acoustic tokens, they do not understand how modern voice models actually work (sourced).
4. **Turn-taking and barge-in are first-class problems, not details.** *Barge-in* = stop talking the instant the user interrupts. *Turn-taking* = deciding when a pause means "your turn" vs. "I'm still thinking." The old way (a simple VAD + energy threshold) is now dated; the field has moved to learned turn-taking models. This is where most voice agents actually feel broken — in the *timing*, not the words (sourced).
5. **Half-duplex vs. full-duplex is the real frontier line.** Half-duplex = strict take-turns (almost all production systems, including most native-audio ones). Full-duplex = both streams run at once, so the system can listen while speaking, backchannel, and handle overlap (Moshi, PersonaPlex, the ICASSP 2026 HumDial challenge). Full-duplex is mostly research-grade in 2026, bottlenecked by a shortage of real two-person conversational training data. Know this is *where the field is heading but not yet where most products live* (sourced).
6. **The hard part of production is reliability and grounding, not the demo.** The expensive problems are hallucination, grounding answers in *your* data (retrieval), recovering when the STT mishears, and not degrading at peak traffic. The 2026 production pattern is hybrid: deterministic/scripted paths for transactional steps, generative responses only with confidence thresholds and human escalation. Naturalness sells; reliability ships (sourced).
7. **Tail latency, not average latency, is what users feel.** Report p50, p95, p99 separately and alert on p99 first. One in twenty calls being slow is a product that "feels laggy" even if the average looks great. This single habit separates people who have run voice in production from those who have only built prototypes (sourced).

### The reading spine (few, high-value, read top-down)

1. **OpenAI — "Introducing gpt-realtime and Realtime API updates"** and the follow-on "Advancing voice intelligence" post. The clearest articulation from a frontier lab of *why* a single S2S model beats a cascade, with real latency and benchmark numbers. Read first for the "what does good look like" anchor (sourced).
2. **A speech-to-speech architecture map** (e.g. Sopyla's "Three Architectural Bets," ai.ksopyla.com). The best conceptual map of the spectrum — audio-native full-duplex / thinker-talker / cascade — with named models and tradeoffs. Read second for mental model #2 (sourced).
3. **Moshi paper / Kyutai repo** (kyutai.org/Moshi.pdf; github.com/kyutai-labs/moshi). The canonical full-duplex + neural-codec reference. You do not need the math — read the intro and architecture overview to ground semantic/acoustic tokens and what "full-duplex" really means (sourced).
4. **A practitioner's build/staffing view** (e.g. Softcery's "Real-Time vs Turn-Based Voice Agents," a voice-stack guide). For the build-vs-buy and staffing reality (sourced).
5. **A voice-eval discipline source** (e.g. Hamming AI, Cekura). WER, latency percentiles, turn-taking gaps, task completion — what you will actually hold your team accountable to. Read last (sourced).
6. **(Optional, frontier)** Full-Duplex-Bench and the ICASSP 2026 HumDial Challenge. Skim only if you need to assess whether a team's "full-duplex" claim is real (sourced).

### Understanding checkpoints — you understand it when you can...

- ...draw the cascade and native-audio architectures on a whiteboard and say, for a given product, which you would pick and why — naming the specific tradeoff (control/grounding vs. latency/naturalness/lock-in).
- ...walk the 800ms latency budget line by line (network, endpointing, model thinking, first-audio) and point to which step a given optimization actually buys back.
- ...explain semantic vs. acoustic tokens to a smart non-expert and say why that split lets a model preserve words while changing voice or emotion.
- ...distinguish barge-in from turn-taking from full-duplex in one clean sentence each, and place a product on the half/full-duplex spectrum.
- ...say why p95/p99 latency matters more than the average, and what a "feels laggy" call looks like in the metrics.
- ...name the top three production failure modes (hallucination/grounding, mis-hearing/STT recovery, timing/turn-taking) and the standard mitigations (RAG + confidence thresholds + human escalation; learned turn-taking).
- ...state honestly what is production-ready vs. research-grade today — i.e., most shipping systems are half-duplex; true full-duplex is still mostly in the lab.

### How to evaluate an expert in an interview

The goal is to tell apart someone who has *run voice in production* from someone who read about it or built one demo.

- **"Walk me through where the 800ms reply budget goes."** *Strong:* decomposes it — network, endpointing, model time-to-first-token, time-to-first-audio — and notes which steps are fixed vs. compressible, flagging endpointing silence as the hidden cost. *Red flag:* treats latency as a single average; never mentions percentiles.
- **"Cascade or speech-to-speech — how do you choose?"** *Strong:* frames it as a tradeoff, picks cascade for a specific reasoning model / tool-use / grounding / model-swap flexibility, native for lowest latency and most natural speech, and names the cost of their choice. May mention the thinker-talker middle path. *Red flag:* cannot articulate a single concrete downside of their preferred choice.
- **"How does an audio model 'understand' speech well enough to talk back?"** *Strong:* explains neural codecs and the semantic-vs-acoustic split, and connects it to capabilities (voice preservation, emotion, cloning). *Red flag:* thinks the model literally transcribes to text internally and reads it back — that is a cascade, not native audio — and does not know the difference.
- **"A user keeps getting talked over / can't interrupt. Diagnose it."** *Strong:* separates barge-in from turn-taking; discusses VAD tuning, minimum-duration guards against false barge-in, and learned turn-taking; knows false-barge-in (cutting off on a cough or "yeah") is the symmetric failure. *Red flag:* does not know barge-in and turn-taking are different problems.
- **"How do you keep a production voice agent from making things up?"** *Strong:* hybrid design — scripted paths for transactions, retrieval-grounded generation for open questions, confidence thresholds, human escalation, continuous eval. Treats hallucination as system design, not prompt-wording. *Red flag:* "we prompt it to not hallucinate."
- **"How do you know it's actually good? What do you measure?"** *Strong:* WER (with targets), latency p50/p95/p99 (alert on p99 first), task-completion rate, turn-taking gap distribution — and stresses it must not degrade at 2–3x peak traffic; replays real call logs, not just lab tests. *Red flag:* "it sounds good in demos."
- **(Frontier probe) "What's research-grade vs. shippable today?"** *Strong:* true full-duplex is still mostly research (Moshi, PersonaPlex, HumDial), held back by scarce two-person data; most shipping systems are half-duplex. *Red flag:* conflates "interruptible" (barge-in, common) with "full-duplex" (simultaneous, rare) and oversells.

*Cross-cutting red flags:* talks only about model accuracy, never timing; has never replayed real calls; cannot name a single thing that breaks at scale (cost-per-minute, p99 spikes, STT errors in noise, accents); no view on voice-cloning consent/safety; dismisses cascades as "obsolete" or native-audio as "a toy" — both reveal they have only worked with one.

### Advisory: how a leader should use this

- **Staff for real-time systems, not just ML.** The scarce skill is people who think in latency budgets and tail percentiles.
- **Default to cascade for your first production system** unless naturalness/emotion is the core product value — you get control, grounding, model-swap freedom, and observability, and you learn where *your* problems actually are before betting on a single-vendor black box.
- **Fund evaluation from day one,** not as a launch-week afterthought.
- **Treat full-duplex as a watch-item, not a 2026 commitment.**
- **Put voice-cloning consent and safety on the roadmap explicitly** — in 2026 the bottleneck on cloning is editorial and ethical, not technical, and clean consent flows are becoming an enterprise procurement requirement.

---

## 8. Team notes

*Org and hiring lens.*

### The architectural fork drives the whole hiring plan

- **Cascaded (STT → LLM → TTS):** three swappable parts through a text layer. You can read, redact, and log every word and swap any vendor. Dominates enterprise in 2026 for debuggability, compliance, and provider flexibility. Org consequence: this is an **integration-and-tuning job**.
- **Speech-to-speech (S2S):** one model, audio in/out. ~200–300ms responses vs. ~2000ms for naive cascades, and it keeps tone/laughs/hesitation. You give up component-level swapping (vendor lock-in, mainly OpenAI and Google), and per-minute cost swings with conversation length. Org consequence: this is a **prompt-and-eval job** (sourced).

Most teams ship cascaded for the regulated core and reach for S2S only where naturalness beats auditability (advisory, grounded in sourced tradeoffs).

### Roles & seniority

**The honest headline: for most companies this is NOT a new hire.** It is a capability an existing senior backend/ML engineer absorbs — once you have decided to rent the hard parts (advisory).

| Need | Who covers it | Net-new hire? |
|---|---|---|
| Wiring the loop, latency budget, vendor integration | Senior backend / platform engineer | No — existing IC absorbs it |
| Turn-taking, barge-in, audio plumbing (WebRTC/Opus/VAD/echo cancellation/jitter) | **Real-time media engineer** | **Yes, if you self-host the transport** |
| Conversation flow, persona, repair behavior | **Conversation designer** | Yes — and people consistently under-hire this |
| Eval harness, regression, load testing | Senior IC + a QA/eval owner | Usually no |
| The reasoning prompt / agent logic | Existing LLM/applied-AI engineer | No |

Three seniority signals:

1. **The loop is a senior+ task.** "Glue three APIs together" hides latency tuning, interruption handling, and graceful degradation on garbled turns. Frontier labs are hiring *Staff+* "Voice Platform" engineers specifically for this (sourced).
2. **The audio/transport layer is a distinct specialty** — WebRTC, RTP, jitter buffering, VAD, echo cancellation, codecs. A great web backend engineer is often a beginner here. If you self-host transport (LiveKit/Pipecat) at real volume, you need someone who has done real-time media (sourced).
3. **Conversation design is a real role, not a prompt the engineer dashes off.** Systems that work pair engineers with designers who own flows, persona, and what happens when things go sideways. Most commonly skipped hire; most common reason a technically-fine agent feels awful (sourced).

**Smallest viable team that ships something good:** one senior backend/applied-AI IC (owns the loop + evals) + one part-time/contract conversation designer, riding entirely on managed vendors. Add a real-time media engineer *only* when volume forces you off managed platforms (advisory).

### Hiring signals

**Green flags:** talks in **latency budgets**, not "it's fast," and knows the streaming tricks that recover milliseconds; treats **barge-in as a first-class feature** (suppress TTS in <200ms, adapt the next turn) and measures both false-positive and false-negative interruption rates; has an **eval/observability instinct before writing agent code**; has **load-tested concurrency** (knows the first meltdown is the first busy hour); is **pragmatic about build-vs-buy** (sourced).

**Red flags:** "We'll just use the Realtime API, it's basically one call" (true for a toy); **no mention of evaluation or testing** — voice agents fail silently, a bad transcript → wrong intent → wrong tool call → silent failure, and the transcript *looks clean* afterward; **wants to train a custom speech model** for a standard use case (a moat-less time sink in 2026); demos beautifully but cannot discuss **failure modes**; **conflates a good TTS voice with a good conversation** (sourced).

### Build vs. buy — default to RENT

**Rent the models. Rent the orchestration. Own only the flow logic and the evals.** That is the 2026 default and right for >90% of teams (advisory).

The market commoditized the hard parts. Models are cheap utilities — OpenAI's gpt-realtime-2 (May 2026), GPT-Realtime-Translate ~$0.034/min, GPT-Realtime-Whisper ~$0.017/min; specialist TTS (Cartesia ~40ms time-to-first-audio, ElevenLabs) and STT (AssemblyAI/Deepgram ~150ms) all sell sub-250ms latency off the shelf; zero-shot voice cloning is now standard, not premium. Orchestration is also a buy: managed platforms (Vapi, Retell) run STT+LLM+TTS+telephony+turn-taking for you; frameworks (LiveKit, Pipecat) hand you a real-time backbone you operate, with LiveKit shipping adaptive interruption handling and dynamic endpointing — exactly the turn-taking primitives that are painful to build (sourced).

**The one published cost threshold to anchor decisions** (sourced):

- **< 10K minutes/month → stay fully managed.** Building your own loses money and time.
- **10K–50K → hybrid.**
- **> 50K minutes/month → self-host on LiveKit/Pipecat saves 60–80% per minute** — but now you own latency tuning, telephony, and uptime (i.e., now you need that real-time media engineer).

**When owning it is a real moat (narrow exceptions):** voice/conversation *is* your product and per-minute economics at huge scale dominate your P&L; hard compliance forcing deterministic redaction at a text boundary (healthcare PHI, finance) — you must own the *cascaded pipeline* so PII never reaches the model unredacted (an *architecture* moat, not a *model* moat — you still rent the models); or a genuinely proprietary voice/acoustic environment where off-the-shelf STT visibly fails. Outside those, building your own speech models is the classic trap (advisory).

### Common failure modes (org, not just technical)

1. **Under-hiring conversation design** → low-latency loop, robotic brittle persona, no repair behavior. The fix is a role, not a prompt tweak (advisory).
2. **No eval harness until it's on fire** → transcription errors cascade into silent wrong tool calls; long calls drift and hallucinate; you learn from angry users (sourced).
3. **Skipping load testing** → works in the demo, dies in the first busy hour as P95 doubles and eval pass-rate drops (sourced).
4. **Picking the architecture for the wrong reason** → choosing S2S for demo wow, then hitting a compliance wall that forces a costly rebuild onto cascaded. Decide auditability/compliance *first*, architecture *second* (advisory, grounded in sourced tradeoffs).
5. **Self-hosting transport too early** → going to LiveKit/Pipecat below ~10K min/month to "save money," then drowning in telephony and uptime work you did not budget headcount for (sourced threshold + advisory).
6. **Treating barge-in as polish** → if the agent talks over interruptions, users feel ignored and the product feels broken regardless of how smart it is. It is core, not a v2 nicety (sourced).

### Bottom line for org planning (advisory)

- **You probably don't need a "voice team."** You need one senior IC who owns the loop and the evals, plus a conversation designer (contract is fine to start). Rent everything else.
- **The single dedicated specialist to hire** *if and only if* you self-host transport at scale: a **real-time media engineer** (WebRTC/audio DSP). Below ~50K min/month, don't.
- **Hire for latency intuition, interruption handling, and eval instinct.** Be suspicious of anyone who thinks it is "just an API call" or who wants to train custom speech models.
- **The moat is your conversation logic, your evals, and (in regulated domains) your compliance-shaped architecture — never the speech models themselves.**

---

## Sources

- Inworld — Best speech-to-speech model / APIs / What is semantic VAD (2026): https://inworld.ai/resources/best-speech-to-speech-model, /best-speech-to-speech-apis, /what-is-semantic-vad
- OpenAI — Introducing gpt-realtime; Advancing voice intelligence with new models in the API (2026): https://openai.com/index/introducing-gpt-realtime/, https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/
- OpenAI — Realtime API guide & transcription docs (2026): https://developers.openai.com/api/docs/guides/realtime, /realtime-transcription
- ghacks.net — gpt-realtime-2 launch coverage (2026-05-11)
- LiveKit — Turn detection: VAD, endpointing, model-based detection (2026): https://livekit.com/blog/turn-detection-voice-agents-vad-endpointing-model-based-detection
- Gradium — Turn-taking / semantic VAD (2026): https://gradium.ai/content/turn-taking-voice-agents-vad, /blog/semantic-vad
- Callsphere — Voice agent barge-in & turn-taking (2026): https://callsphere.ai/blog/vw7d-voice-agent-barge-in-turn-taking-2026
- Kyutai Moshi — repo, paper, arXiv (2024–2026): https://github.com/kyutai-labs/moshi, https://kyutai.org/Moshi.pdf, https://arxiv.org/html/2410.00037v2
- Google — Gemini Live API native audio (2026): https://cloud.google.com/blog/topics/developers-practitioners/how-to-use-gemini-live-api-native-audio-in-vertex-ai, https://ai.google.dev/gemini-api/docs/live-api
- Softcery — Real-time vs turn-based / cascade architecture (2026): https://softcery.com/lab/ai-voice-agents-real-time-vs-turn-based-tts-stt-architecture
- Famulor — Realtime vs pipeline voice agent architecture (2026): https://www.famulor.io/blog/realtime-vs-pipeline-voice-agent-architecture-guide-2026
- Retell — AI voice agent pricing & cost breakdown (2026): https://www.retellai.com/blog/ai-voice-agent-pricing-full-cost-breakdown-platform-comparison-roi-analysis
- SiliconFlow — Best open-source TTS models (2026): https://www.siliconflow.com/articles/en/best-open-source-text-to-speech-models
- Artificial Analysis — Speech-to-speech leaderboard, TTFA metric (April 2026): https://artificialanalysis.ai/speech-to-speech
- AWS — Amazon Nova 2 Sonic pricing & docs (2026): https://aws.amazon.com (Nova 2 Sonic)
- Deepgram — Speech-to-speech vs cascade architecture (2026): https://deepgram.com/learn/speech-to-speech-vs-cascade-voice-agent-architecture
- Coval — Speech-to-speech vs cascaded voice AI (2026): https://www.coval.ai/blog/speech-to-speech-vs-cascaded-voice-ai-which-architecture-should-you-deploy/
- Particula — Vapi vs Retell vs LiveKit vs Pipecat (2026): https://particula.tech/blog/vapi-vs-retell-vs-livekit-vs-pipecat-voice-agent-platform
- AssemblyAI — Voice AI stack / orchestration tools / best S2S API (2026): https://www.assemblyai.com/blog/the-voice-ai-stack-for-building-agents, /orchestration-tools-ai-voice-agents, /best-speech-to-speech-voice-agent-api
- Hamming AI — Voice agent evaluation & stack selection (2026): https://hamming.ai/resources/best-voice-agent-stack
- Cekura — Voice AI evaluation metrics (2026): https://www.cekura.ai/blogs/voice-ai-evaluation-metrics
- FutureAGI — Barge-in & turn-taking; voice AI load testing (2026): https://futureagi.com/blog/voice-ai-barge-in-turn-taking-2026/, /voice-load-testing-simulating-10000-calls-2026/
- Anthropic — Senior/Staff+ Software Engineer, Voice Platform (accessed 2026-06): https://job-boards.greenhouse.io/anthropic/jobs/5172245008
- Sopyla — Speech-to-speech models in 2026: three architectural bets: https://ai.ksopyla.com
- Full-Duplex-Bench v1.5 (arXiv 2507.23159) & ICASSP 2026 HumDial Challenge (arXiv 2604.21406)
- EU AI Act / Digital Omnibus high-risk deferral analyses — Gibson Dunn, Latham, DLA Piper (2026)
- Stivers et al. (2009) — universals in turn-taking timing (~200ms gap, 10-language study)
