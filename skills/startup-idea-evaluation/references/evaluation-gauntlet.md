# The Evaluation Gauntlet — sequential stress-test gates

Run any candidate idea through these seven gates **in order**. Do not skip gates upward (you build on sand); do not linger after passing (that's validation theater). Run 2–3 candidates through gates 1–5 in parallel — comparison is the cheapest cure for infatuation. Expect 2–4 months per serious candidate.

Grade every piece of evidence by what it cost the person giving it: **opinions < time < reputation < money.** [Evergreen]

Verdict per gate: **PASS** (threshold met), **CONDITIONAL** (name the missing evidence and how to get it), or **KILL** (a red flag hit — fix the specific flaw or drop the idea; killing an idea rarely means killing the space: ~25% of top YC companies pivoted entirely within theirs).

---

## Gate 1: Problem & founder-market fit

**Questions to answer:**
- [ ] Who *specifically* has this problem? Name the segment tightly ("heads of RevOps at 50–500-person B2B SaaS companies"), not "businesses."
- [ ] Is it urgent, frequent, and expensive? Score against Kevin Hale's six traits: popular / growing (~20%+/yr market) / urgent / expensive / mandatory / frequent. No idea hits all six; a great one hits "growing + urgent + frequent" or "expensive + mandatory." [Evergreen]
- [ ] The hair-on-fire test: can you name **10 specific people or companies** who need this so badly they'd use a broken v1? [Evergreen]
- [ ] Founder-market fit: are you among the best-placed people alive to build this? What have you lived, built, or seen that others haven't?
- [ ] Have targets *already* tried to solve it — spreadsheets, contractors, duct-taped scripts? Existing spend of money or time is the strongest problem evidence there is.

**Evidence threshold to pass:** 10 nameable desperate users/companies, AND (once interviews are run — see Gate 6 kill criteria) at least 1 in 3 of a tight segment describes the problem as a top-3 priority they're already paying something (money or hours) to address.

**Red flags that kill:**
- You can't name the first 10 customers (Paul Graham's test: no identifiable desperate users, no idea).
- Universal politeness — everyone says "cool, I'd try that" and nobody does anything. Real validation "feels undeniable rather than ambiguous."
- You're selling efficiency to someone who wants growth ("Doctors want more patients, not an efficient office").
- Zero domain exposure and no plan to get it.

---

## Gate 2: Why now

**Questions to answer:**
- [ ] What recent, specific unlock makes this possible today when it wasn't 5 years ago? Must be one of four kinds: **technology** (capability crossed a threshold — Figma/WebGL), **economic** (a cost collapsed — cloud → SaaS), **regulatory/structural** (a law or platform shift — Checkr), **behavioral** (people changed — COVID → remote tools). [Evergreen]
- [ ] Does the unlock imply a *window*? Best answers sit 12–36 months after the unlock — capability real, market not yet consolidated.
- [ ] If you can't answer why-now: why wasn't this built 5 years ago (usually: it was, and it died), and why won't it be commoditized 5 years from now?

**Evidence threshold to pass:** a one-sentence why-now naming the specific unlock and why the window is open now — one a skeptic can check.

**Red flags that kill:**
- [2026] Your why-now is "LLMs got good." That is *everyone's* why-now and differentiates nothing. You need the second-order version: "LLMs got good **and** [specific vertical] has [specific painful workflow] with [specific data or distribution] that generalist tools can't touch."
- Your why-now was equally true 3+ years ago and nothing else changed.
- Too early (you'd educate the market and die) or too late (incumbents/swarm already consolidating).

---

## Gate 3: Market size — the worked TAM/SAM/SOM method

**The method (bottom-up only — investors distrust top-down):** [Evergreen]

1. **TAM** = (number of potential customers) × (annual revenue per customer). Count customers from a checkable source; price from your Gate-4/pricing hypothesis.
2. **SAM** = the slice of TAM you can actually serve: cut for geography, language, integrations you'll support, regulatory reach, sales model.
3. **SOM** = the slice of SAM you could realistically win in ~5 years. Convention: claiming **1–5% of SAM** is credible; below 1% signals too small, above ~10% signals naivety (unless you have monopoly dynamics in a narrow wedge — then target 50–100% of the wedge, Thiel-style).

**Worked example** (AI phone receptionist for dental offices at $500/mo = $6,000/yr):
- TAM: ~180,000 US dental practices × $6,000 = **$1.08B**
- SAM: only the top-2 practice-management integrations (~60% of practices), US only: 108,000 × $6,000 = **$648M**
- SOM: 3% of SAM in 5 years = ~3,240 practices × $6,000 = **~$19M ARR** — this is the number an investor pressure-tests, not the billion.

**The venture-scale check:** buyers × realistic price × plausible penetration — does the *best case* clear a path to ~$100M ARR (≈ a $1B company at ~10x revenue)? [Evergreen] If not, it can still be a great business — just not a venture-funded one. Killing an idea for the wrong *goal* is also a kill.

**Evidence threshold to pass:** bottom-up math with checkable inputs clearing ~$100M ARR at success, OR an honest small-wedge story ("start small, expand up the stack" — Microsoft began in Altair BASIC interpreters) with a credible expansion narrative.

**Red flags that kill:**
- The best-case math tops out at single-digit $M ARR and the wedge has no expansion path (the $30/mo tool × 500K reachable buyers × 2% penetration = $3.6M ARR trap).
- Your market slide is "capture 1% of a $50B Gartner number" — a multiplied guess, not a count.
- TAM computed from the incumbent category when your product changes behavior (the Uber-vs-taxi-market error) — recompute against the behavior you create.

---

## Gate 4: The 10x insight

**Questions to answer:**
- [ ] What's your unfair advantage? Must be at least one of Hale's five: **founder** (rare expertise), **market** (riding 20%+/yr growth), **product** (genuinely 10x better/cheaper — 2x isn't enough to beat switching inertia), **acquisition** (grows free by word of mouth), **monopoly** (network effects). [Evergreen]
- [ ] Thiel's question: what do you believe, from lived experience, that the consensus rejects — and what evidence says you're right? If everyone agrees it's a good idea, either many teams are already doing it or the market has correctly judged it bad.
- [ ] On which *one* dimension your wedge customer cares about are you 10x? (You don't need 10x on everything.)

**Evidence threshold to pass:** one exceptional, specific advantage (an A++ on one axis beats a B+ on five — Naval Ravikant's rule), plus a secret a smart outsider could NOT guess in ten minutes.

**Red flags that kill:**
- Your differentiation reduces to "we'll execute better." Every skeleton in the tarpit said that.
- Your "secret" is merely controversial-but-common ("education is broken").
- The 10x claim is really 1.5x plus enthusiasm.

---

## Gate 5: Competition & moat

**Questions to answer:**
- [ ] **Tarpit graveyard check:** search Crunchbase/Google for companies that tried exactly this. If you find many, well-funded, all dead — what *specifically* changed that makes your attempt different, and is that change real or asserted? Classic tarpits: discovery apps, plan-with-friends apps, "Yelp for X"; [2026] additions: thin AI wrappers, generic chatbots, "ChatGPT for X" where the model providers ship X natively. [Evergreen]
- [ ] [2026] **The wrapper test:** if OpenAI/Anthropic/Google shipped your product as a default feature next quarter, would your customers cancel? If yes, you're building a feature, not a company.
- [ ] Some competition is *validation* (Dropbox was ~the 20th file-sync product) — do you have the new insight the incumbents lack?
- [ ] What's the plausible *eventual* moat? Rank: network effects > embedded money/data flows > proprietary data loops > workflow depth > distribution > brand > features. Before PMF your only real moat is speed — "a moat is not a starting point, it's a result" — but evaluate for a plausible endgame moat now.
- [ ] Structural dependency check: does the whole business depend on platform access (an API, app store, data source) the owner can and would cut off?

**Evidence threshold to pass:** the graveyard is explained by a real change (not asserted); the idea survives the wrapper test; at least one plausible eventual moat named with the mechanism that builds it.

**Red flags that kill:**
- "We have no competition." (You haven't looked, or there's no market.)
- The wrapper test fails and your answer is "we'll move fast forever."
- A single uncontrolled platform dependency with incentive to cut you off.

**What is NOT a kill signal:** the work looks hard (that's the schlep — a feature, not a bug: Stripe sat in plain sight for a decade); competitors exist; smart people are skeptical; you're bored after two weeks (check for dread, not novelty wearing off).

---

## Gate 6: Kill criteria — write them before you're attached

**Write down, in advance, the specific results that would make you drop the idea.** Decided in advance, it's discipline; decided after the fact, it's rationalization. [Evergreen]

Standard kill criteria to adopt (edit numbers, then commit):
- [ ] After ~30 problem interviews (20–30 consumer, 50+ B2B) asking only about *past behavior*: no tight segment where ≥1 in 3 names this as a top-3, already-paid-for priority → **kill or reshape**.
- [ ] Minimum viable test fails its pre-registered bar — landing page with a price: <8–10% signup from ~1,000 targeted visitors and zero unsolicited "when can I get this?" follow-ups; or B2B: <5 of 20 demo calls agree to a weekly design-partner slot → **kill**.
- [ ] Zero willingness to pre-commit after direct asks: no deposits, no design-partner agreements, no scheduled second meetings. Money and calendar time are the only honest currencies; "maybe" = no → **kill**.
- [ ] After 4–8 weeks of B2B selling: fewer than 3 signed design partners and none paying anything (even $500/mo — the point is the pain of a purchase order, not the amount) → **kill**.
- [ ] The economics can't work even in the best case (Gate 3 math) → **kill as a venture bet** (may live as a lifestyle business — a legitimate, different game).

Harvest every death: the interviews from a dead idea are the idea generator for the next one.

---

## Gate 7: Premortem

Set a 45-minute timer. Write, **in past tense**, the most plausible obituary of the idea three years out — prospective hindsight improves failure identification by ~30% (Klein/HBR). Then force-rank which canonical death killed it. [Evergreen]

The canonical deaths to rank against (CB Insights: % of failure post-mortems citing each):
- [ ] **No market need (42%)** — did we ever have 10 users who'd be "very disappointed" if we vanished, or did we scale on curiosity?
- [ ] **Ran out of cash (29%; 70% in the 2023–26 shakeout)** — mechanism, not cause: *why* did it run out? What milestone did we bet the next round on, and what was Plan B? (Median death: 22 months after the last raise. [2026])
- [ ] **Team** (~65% of high-potential failures trace to founding-team conflict) — did we have the equity/roles/who-is-CEO fight before incorporating? 4-year vesting with a 1-year cliff?
- [ ] **Unit economics** — does one more customer make us richer or poorer (MoviePass test)? If growth spend went to zero, does revenue hold (Homejoy test)?
- [ ] **Premature scaling** — did we spend on growth before retention proved the core loop? (Startup Genome: ~70% of startups scale prematurely; none that did passed 100K users in their dataset.)
- [ ] **Incumbent bundling / wrapper collapse [2026]** — did OpenAI/Apple ship us as a feature (Humane test)? Would our gross margins survive an audit of how the work really gets done (Builder.ai test)?
- [ ] **Channel dependency** — one platform changed and killed us (Tutorspree test).

**The non-consensus check:** if everyone said the idea was bad — did we have *usage evidence* skeptics lacked (the Airbnb pattern: strangers really paying to sleep on air mattresses), or only a clever argument? Arguments are what the 42% had. A bad idea has neither believers nor usage; a non-consensus idea has intense usage the consensus explains away.

**Reading the result:** if the obituary writes itself and the same cause keeps topping the ranking — fix that vulnerability before starting, or pick a different idea. If you genuinely struggle to write a plausible non-generic obituary, that is what conviction with evidence feels like.

---

## Output format for a gauntlet run

Per gate: verdict (PASS / CONDITIONAL / KILL) + one-sentence reason; for CONDITIONAL, the cheapest next experiment (action, cost, time, pre-registered pass/fail bar). End with an overall verdict — **build / test further / pivot within space / kill** — plus the top-ranked premortem cause of death.

*Deeper reading: `research/startup-business-models/01-idea-evaluation-and-conviction.md` and `11-failure-patterns-and-case-studies.md`.*
