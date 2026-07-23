# Fundraising Mechanics — how seed money actually works in 2026

**Why this matters to you:** Your friends who raised money successfully weren't smarter than you. They knew the machinery: what a SAFE actually does to your ownership, what numbers are "normal" this year, and that a raise is a designed process, not a series of coffee chats. Investors talk to founders all day and know every convention. A first-time founder who doesn't know them negotiates blind and gets worse terms — or worse, structures an early round in a way that quietly kills the company two years later. This document gives you the full mechanical picture — instruments, math, dilution, process — with 2026 numbers attached. When you start raising, you'll be playing the same game as everyone across the table. Read it before you take a single check.

Related docs: who the investors actually *are* and how accelerators like Y Combinator work is in `06-investors-and-accelerators.md`; how to build the pitch itself is in `07-pitching.md`; the burn-rate and margin math investors will probe is in `04-unit-economics.md`.

---

## 1. The funding ladder

Startups raise money in rungs. Each rung has a conventional size, a conventional valuation range, and a conventional amount of the company you give up. The rungs and their logic are **[Evergreen]**; the specific dollar figures below are **[2026]** and drift every year.

**Quick definitions first:** *Valuation* is the price of the whole company. *Pre-money valuation* is the price before the new cash goes in; *post-money* is after (post-money = pre-money + amount raised). *Dilution* is the percentage of the company you hand over: raise $4M at a $20M post-money valuation and the investors own $4M / $20M = 20%.

### Rung 0: Bootstrapped
You fund the company yourself from savings or early revenue. **[Evergreen]** You keep 100% and all control; the tradeoff is speed. Paul Graham's advice in [The Fundraising Survival Guide](https://paulgraham.com/fundraising.html) is that reaching "ramen profitable" — revenue covering the founders' basic living costs — transforms everything: "Once you cross into ramen profitable, everything changes. You may still need investment to make it big, but you don't need it this month." **[2026]** This rung matters more than it has in a decade, because AI tooling lets tiny teams ship products and get to revenue before raising at all — see `10-ai-era.md`.

### Rung 1: Angels
*Angels* are individuals (often ex-founders) who invest their own money. **[2026]** Typical checks: $10k–$100k, occasionally $250k+. Angels usually invest on SAFEs — a *SAFE* ("Simple Agreement for Future Equity") is a standard contract where the investor gives you money now in exchange for shares later; section 2 explains it in full. Angels take whatever valuation cap the round sets; they rarely negotiate terms and almost never take board seats. **[Evergreen]** Their real value is often intros and credibility, not the money.

### Rung 2: Pre-seed
The first organized round. Typically raised on SAFEs from angels and small pre-seed funds, usually before you have a product or revenue. **[2026]** The numbers below come from Carta. (Carta runs *cap-table* software — a cap table is the ledger of who owns what percentage of the company — for most US startups, so their data is the closest thing to ground truth. Their [State of Pre-Seed reports](https://carta.com/data/state-of-pre-seed-q1-2026/) are the standard reference. Note: the Q1 2026 report itself blocks scrapers, so the figures here come via [summaries of Carta's data](https://vclens.substack.com/p/carta-state-of-preseed-2025-explained) and [SaaStr's digest](https://www.saastr.com/the-state-of-seed-today-10-key-learnings-from-cartas-latest-data).)

- Round size: roughly $500k–$2.5M.
- Median post-money SAFE valuation caps step up with round size: **~$8M** for tiny sub-$250k rounds, **~$10M** for $250–499k rounds, **~$12M** for $500–999k rounds, and **~$15M** for $1M–$2.4M rounds.
- **92% of pre-seed rounds now use SAFEs**, up from 54% in 2019. Convertible notes have fallen to ~9%.
- The volume is huge: **330,000+ SAFEs and convertible notes** have been signed on Carta since 2021. This is a standardized, mass-market instrument, not an exotic one.

**[2026]** If you go through Y Combinator (YC — the best-known startup accelerator; see `06-investors-and-accelerators.md`), [the current standard deal](https://www.ycombinator.com/blog/ycs-500-000-standard-deal) is $500k total: $125k for 7% on a post-money SAFE, plus $375k on an uncapped "MFN" SAFE that takes the terms of your next round (all terms defined in section 2). This deal has been standard since [it was announced in January 2022](https://www.ycombinator.com/blog/ycs-500-000-standard-deal), and [YC's live deal page](https://www.ycombinator.com/deal) lists the same terms as of July 2026.

### Rung 3: Seed
The round where you prove the core product works and — increasingly — that people pay for it. It can be a stack of SAFEs or a *priced round* (an actual sale of shares at a negotiated valuation; section 3 explains the difference). **[2026]** numbers, per Carta/[SaaStr](https://www.saastr.com/the-state-of-seed-today-10-key-learnings-from-cartas-latest-data) and the [H1 2026 seed market summaries](https://hub.causo.ai/guides/h1-2026-state-of-seed-report):

- Median round size: **~$3–4M** (95th percentile: $16.6M).
- Median post-money valuation: **~$20M** as of mid-2025 data, drifting to ~$24M by Q4 2025 — but heavily skewed by AI. Non-AI seed rounds track closer to ~$18M *pre*-money on ~$3M raised. The 95th percentile seed valuation is $80.5M — a 4x spread over the median. In other words, "the market rate" barely exists; hot AI deals live in a different market.
- Typical dilution: **15–20%** to investors, plus the option pool (section 5). Total founder dilution in a seed round commonly lands at 20–28%.
- Geography: 66% of top-decile (top 10%) seed valuations go to startups in SF (44%) or NYC (22%), per [SaaStr's digest of Carta's data](https://www.saastr.com/the-state-of-seed-today-10-key-learnings-from-cartas-latest-data). Relevant to you: NYC is a legitimate place to raise, but the very top of the market clears in SF.

### Rung 4: Series A
The first big institutional round — "institutional" meaning it's led by a venture capital (VC) firm, a professional fund that invests other people's money. A Series A is almost always priced, and the lead firm takes a board seat.

**[2026]** Typical numbers:

- A normal (non-AI) software Series A raises roughly **$8–15M**, selling ~15–25% of the company. Series A lead funds like Chemistry describe writing "$3–30M checks with an average of $10–12M" ([via SaaStr](https://www.saastr.com/the-series-a-landscape-in-2025-insights-from-chemistry-vcs-ethan-kurzweil/)).
- Market-wide medians run higher because AI deals dominate the stage: median Series A deal size hit **~$19.6M** on a **~$62M median pre-money** valuation (≈$80M post) in Q1 2026, up from ~$48M pre-money a year earlier, per PitchBook-NVCA and Carta figures ([collected here](https://hub.causo.ai/guides/seed-to-series-a-graduation-rate-benchmarks-2026)).
- AI companies carry roughly a **40% valuation premium** at the A (Chemistry VC, same source). So a solid non-AI company should expect more like **$40–55M pre-money**. The *step-up* math agrees. (A step-up is the multiple by which your valuation grows from one round to the next: a $20M seed valuation × 2.6 ≈ a $52M Series A.) The median seed-to-A step-up is ~2.6x ([Carta data via SaaStr](https://www.saastr.com/the-state-of-seed-today-10-key-learnings-from-cartas-latest-data)), up from 2.4x in 2024 but far below the 4.2x peak of 2021 — and 2.6x on top of a ~$18–20M non-AI seed lands right in that $40–55M range.
- AI-outlier Series A rounds reportedly average ~$50M+ *raised*, per [industry surveys](https://www.crv.com/content/ai-startup-funding). Treat that figure as directional; it's dominated by outliers.

**[2026]** Timing and odds: median time from seed to A is now **2.1–2.2 years**, up from 1.5 in 2019 — and the odds of getting there at all have fallen hard. "About half" was true for older cohorts: roughly 50% of 2017–2019 seed companies reached an A within four years (the Q1 2019 cohort hit 49.1%, per [Carta's cohort data via SaaStr](https://www.saastr.com/the-state-of-seed-today-10-key-learnings-from-cartas-latest-data)). But per Carta's cohort tracking, only **15.4%** of Q1 2022 seed companies raised an A within two years, versus 30.6% for Q1 2018. The post-2021 cohorts are tracking toward an eventual graduation rate closer to **20–25%** — roughly half the historical rate ([Carta data via Incisive Ventures](https://incisive.vc/2025/06/10/update-on-venture-graduation-rates/); [SaaStr's Carta digest](https://www.saastr.com/the-state-of-seed-today-10-key-learnings-from-cartas-latest-data)). Plan your seed as if the A is a ~1-in-4 event on today's odds, not a coin flip.

The traction bar rose accordingly. $1M+ **ARR** growing fast is the floor (*ARR* = annual recurring revenue — the yearly run-rate of your subscription income, and the standard traction yardstick for software startups). For ordinary (non-AI) software, many A investors now want **$2M+ ARR** ([SaaStr, on Carta's timeline data](https://www.saastr.com/your-seed-round-now-needs-to-last-3-years-what-3365-startups-tell-us-about-the-new-series-a-timeline/)).

### What the ladder does to your ownership
**[2026]** Carta's cap-table data shows median founder-team ownership of **56.2% after seed, 36.1% after Series A, 23.0% after Series B** — roughly 20 points of dilution per early round. **[Evergreen]** The lesson: dilution compounds, so every point you save early is worth multiples later. YC's [Guide to Seed Fundraising](https://www.ycombinator.com/library/4A-a-guide-to-seed-fundraising) puts the norm bluntly: most seed rounds cost ~20% of the company, and "if you can manage to give up as little as 10% of your company in your seed round, that is wonderful."

---

## 2. SAFEs, in full detail

The **SAFE** ("Simple Agreement for Future Equity") is the default early-stage instrument. Y Combinator invented it in 2013 and publishes the standard documents free ([YC's SAFE documents and user guide](https://www.ycombinator.com/documents), with the mechanics spelled out in the [Primer for the post-money SAFE](https://www.ycombinator.com/assets/ycdc/Primer%20for%20post-money%20safe%20v1.1-2af8129e12effd9638eeab383b7309142c8f415e5cdb0bc210d573f779177a1c.pdf)). Nearly every US pre-seed round and many seed rounds use the standard YC forms, unmodified. The structure is **[Evergreen]**; its dominance (92% of pre-seed) is **[2026]**.

**What it is:** the investor gives you money *now* in exchange for the right to receive shares *later*, when you raise a priced round. It is not debt — no interest, no maturity date, no repayment obligation. You sign a 5-page standard document, the money wires, done. No lawyers negotiating for weeks — which is the entire point.

**The key terms:**

- **Valuation cap** — the maximum company valuation at which the SAFE converts into shares. A $500k SAFE with a $10M post-money cap converts as if the company were worth at most $10M, even if the priced round later values it at $50M. The cap is effectively the price of the deal, and it's the number founders and investors actually negotiate.
- **Post-money vs pre-money SAFE** — since 2018 the standard is the **post-money SAFE**: the cap is measured *after* including all the SAFE money and other converting instruments. The huge practical consequence: **a post-money SAFE locks in the investor's exact ownership percentage.** $500k on a $10M post-money cap = exactly 5% of the company immediately before the priced round, no matter what else you do. The old pre-money SAFE left everyone guessing until conversion.
- **The founder-side gotcha:** because each post-money SAFE's percentage is fixed, SAFEs do not dilute *each other*. Every additional SAFE you stack dilutes **only the founders and other common stockholders**, dollar for dollar. ([YC's own primer](https://www.ycombinator.com/assets/ycdc/Primer%20for%20post-money%20safe%20v1.1-2af8129e12effd9638eeab383b7309142c8f415e5cdb0bc210d573f779177a1c.pdf) states this explicitly, and [term-by-term guides](https://www.elego.law/insights/decoding-the-yc-safe-a-term-by-term-guide) unpack it.) Founders who casually stack SAFEs over two years frequently discover at their priced round that they've sold 25–30% of the company without ever "doing a round." Track your SAFE stack in a cap-table tool from day one.
- **Discount** — instead of (or alongside) a cap, a SAFE can convert at a discount to the priced-round price, typically 10–20%. For example, a 20% discount SAFE converts at 80% of what the Series A investors pay. Cap-only is the most common structure (~61% of post-money SAFEs use cap only, per Carta).
- **MFN ("Most Favored Nation")** — a SAFE with no cap and no discount, but a promise: if you later issue a SAFE on better terms (e.g. with a cap), the MFN holder can adopt those terms. This is how YC's $375k tranche works: it simply takes the terms of the best (lowest-cap) SAFE you sign before your next equity round.
- **Pro-rata side letter** — SAFEs from funds (as opposed to angels) often come with a side letter granting **pro-rata rights**: the right to invest again in the next round to keep their ownership percentage. Per [Carta's SAFE data](https://carta.com/learn/startups/fundraising/pre-seed-funding/), the most common side-letter terms are MFN, pro-rata, and **information rights** (the right to receive regular financials). These sound harmless, but pro-rata rights consume space in your next round that you might want for a new lead. Grant them to investors you'd happily have double down — not to everyone.

### Worked dilution example — what actually happens when SAFEs convert

**[Evergreen math, 2026-typical numbers.]** You and a co-founder own 100% (50/50).

1. **Pre-seed SAFE #1:** $500k at a $5M post-money cap → this investor is locked at **10%**.
2. **Pre-seed SAFE #2 (a year later):** $1M at a $10M post-money cap → locked at **10%**.
3. Immediately before your priced seed round: SAFE holders 20%, founders **80%** (40% each). Note both SAFEs' dilution came entirely out of you.
4. **Priced seed round:** $4M at $16M pre-money = $20M post-money. New investors get $4M / $20M = **20%**. The term sheet also requires a **10% post-round option pool** (section 5).
5. New investors (20%) + pool (10%) = 30% of the post-round company is new. Everyone who existed before — founders *and* converting SAFE holders — is squeezed into the remaining 70%:
   - Founders: 80% × 0.70 = **56%** (28% each)
   - SAFE #1: 10% × 0.70 = 7%; SAFE #2: 7%
   - New seed investors: 20%; option pool: 10%. Total: 100%.

Notice the founders landed at 56% — almost exactly Carta's real-world median of 56.2% post-seed. This is the normal path, not a horror story. The horror-story version is stacking $3M of SAFEs at a $6M cap because you were desperate: that's 50% gone before the seed round even starts, and a cap table that makes Series A investors walk away. **[Evergreen]** Rule of thumb: know your **fully-diluted ownership** at all times. "Fully diluted" means your percentage counted as if every share that *could* exist already did — all issued shares, plus every SAFE converted at its cap, plus the entire option pool (granted or not), plus any warrants. That number, not your share of stock issued today, is your real ownership. The worked example above is fully-diluted math.

---

## 3. Priced rounds vs SAFEs

A **priced round** (also called an "equity round") is the traditional structure: investors buy newly issued **preferred stock** at a negotiated price per share, with a full set of legal documents. "Preferred" means it carries rights your common stock doesn't — most importantly a **liquidation preference** (defined in the glossary).

**[Evergreen]** The tradeoff:

| | SAFEs | Priced round |
|---|---|---|
| Speed / cost | Days; ~$0–5k legal | 4–8 weeks; $15k–$50k+ legal |
| Rolling close | Yes — take checks one at a time | Mostly one close |
| Board seat | Never | Often (see section 6) |
| Dilution clarity | Deferred (dangerous if untracked) | Exact, on day one |
| Investor rights | Minimal (side letters only) | Full: preference, pro-rata, information rights, protective provisions |

**[2026]** convention: pre-seed = SAFEs, almost always. Seed = either. Roughly speaking, party rounds (many small checks, no lead — see section 7) and smaller seeds run on SAFEs, while a $3–5M seed with a strong lead fund is often priced — the lead wants a board seat and defined rights. Series A = priced, essentially always. If a good lead offers you a clean priced seed at a fair valuation, that's not a worse deal than SAFEs. It's often better, because your cap table becomes exact and the ambiguity is gone.

---

## 4. How much to raise: milestones, not vibes

**[Evergreen]** The right question is not "what's a normal amount" but **"what does it cost to reach the milestone that unlocks the next round?"** Work backwards: define what a Series A investor will need to see (in 2026, usually $1M+ ARR growing fast, or extraordinary usage), price the team and time required to get there, add buffer. YC's guide frames it as raising "as much money as you need to get to profitability or your next fundable milestone" — raise for a plan, not for a number that sounds impressive.

**[Evergreen]** The **18–24 month runway convention**. (*Runway* = the number of months of cash you have left at your current spending rate.) Rounds are sized so the money lasts 18–24 months, because you'll spend the last ~6 months of it fundraising again — so 18 months of money is really ~12 months of building. (Lenny's Newsletter's [seed guide](https://www.lennysnewsletter.com/p/raising-a-seed-round-101) pushes toward 24–36 months with a 25% buffer in the current market. With rounds taking longer to raise, thin runway is how companies die.) Paul Graham's back-of-envelope in [How to Raise Money](https://paulgraham.com/fr.html): estimate each person as costing ~$15k/month *fully loaded* — the all-in cost of an employee, meaning salary plus payroll taxes, benefits, equipment, and overhead, not just the paycheck. So a 5-person, 18-month plan ≈ $1.35M. **[2026]** Real fully-loaded costs for senior engineers in NYC/SF are more like $20–30k/month; the *method* is what's evergreen.

**[Evergreen]** Announce the *low* end of your range publicly. Per Lenny's guide: "it's better to say you are raising $2M than to say you are raising $3M." An oversubscribed $2M (*oversubscribed* = more investor demand than the amount you said you were raising) becomes $3M gracefully; an undersubscribed $3M (less demand than the announced target) looks like failure. Paul Graham says the same: give a low number and let demand raise it.

**[Evergreen]** Raising *more* than you need is not free. It costs dilution. It drags your next-round expectations up — a $30M post-money seed means the A needs to clear ~$60M+, which means you need the traction to justify it. And cash-rich companies get sloppy. See `00-rules-of-thumb.md`.

---

## 5. Option pools — the stealth dilution

An **option pool** (or "employee stock option pool") is a block of shares reserved for future employees. **[Evergreen]** The mechanic to understand: in a priced round, investors almost always require the pool to be created or topped up **pre-money** — meaning it comes out of the existing holders (mostly you), not out of the investors. A "$16M pre-money" offer with a 15% pool demand is a meaningfully lower price than the same headline with a 10% pool demand. This is the classic first-time-founder blind spot. As one [analysis of Carta's data](https://hub.causo.ai/guides/seed-valuation-2026) put it, the pool top-up "is where 8–12% of founder equity quietly vanishes" while founders fixate on the headline valuation.

**[2026]** Norms: seed-stage pools are typically set to 10% post-round (you saw its effect in the worked example — it was 1/3 of your round's dilution). Negotiate the pool size against your *actual 18-month hiring plan*, not the investor's default. Carta's hire-by-hire data: median first hire gets 1.5%, second 0.85%, third 0.50% — so a 10% pool covers a lot of hiring. A demanded 15% pool is often just price negotiation wearing a costume. Say so, politely, with your hiring plan as evidence.

---

## 6. Board seats and control at seed

**[Evergreen]** A **board of directors** legally controls the company: it can approve financings, set option grants, and fire the CEO (you). Control at each stage:

- **SAFE rounds:** no board seats, ever. SAFE holders aren't even shareholders yet. You retain complete control.
- **Priced seed:** commonly either founders-only (2 founders) or a 2–1 board: two founders plus one seat for the lead investor. A 2–1 board is normal and fine; you still control it.
- **Series A:** the lead takes a seat, and boards often become 2 founders / 2 investors / 1 independent over time.

**[Evergreen]** What matters more than the seat count at seed: **protective provisions** in a priced round — a list of actions that require investor approval, such as selling the company, raising money, or taking debt. These are standard and mostly reasonable. Have a startup lawyer (not your cousin) confirm yours match the market standard: the model documents from the NVCA (National Venture Capital Association, the US venture industry's trade body). Red flags at seed that should make you walk: investor board *control*, participation rights beyond a 1x liquidation preference (glossary), or anyone asking for >25% at seed.

---

## 7. How a raise is actually run

The single biggest insight for a newcomer: **a raise is a compressed, parallel, deliberately engineered process — not an ambient activity.** Everything below is from [Paul Graham's How to Raise Money](https://paulgraham.com/fr.html), [Lenny's seed guide](https://www.lennysnewsletter.com/p/raising-a-seed-round-101), and [First Round Review's fundraising pieces](https://review.firstround.com/the-fundraising-wisdom-that-helped-our-founders-raise-18b-in-follow-on-capital/), and it's all **[Evergreen]**.

1. **Prep (4–8 weeks before, while NOT talking to investors).** Build the deck and/or memo, a simple financial model, and a data room (a shared folder with your incorporation docs, cap table, and metrics). Rehearse the pitch (see `07-pitching.md`). First Round's warning: starting before you're ready "burns through warm introductions with an underprepared pitch" — you usually get one shot per investor per year.
2. **List building.** Build a tracked list of **40–80 investors** who actually invest at your stage, in your sector, at your check size (First Round's range; sources: Crunchbase, portfolio pages, and — most importantly — founder friends' direct knowledge; see `09-networks.md`). Rank by fit. Paul Graham's rule: do **"breadth-first search weighted by expected value"** — expected value = probability they say yes × how good it is if they do. Talk to everyone in parallel, but spend your energy in rank order.
3. **Warm intros.** A *warm intro* is an introduction from someone the investor already trusts. Cold email works occasionally; intros from founders the investor has backed convert at dramatically higher rates. Per Lenny's guide: "Who introduces you to prospective investors matters a lot more than you might think."
4. **Sprint, in parallel.** Compress first meetings into a **2–3 week window**. Paul Graham: "You should always talk to investors in parallel rather than serially." Serial conversations let each investor stall you while keeping the option open; parallel ones force decisions. One founder runs the raise full-time while the other(s) keep building — per Graham's [Fundraising Survival Guide](https://paulgraham.com/fundraising.html), companies that halt product progress during a raise visibly wilt, and investors notice.
5. **Momentum and FOMO** (fear of missing out). Getting the first real commitment "can be half the total difficulty of fundraising" (Graham). Investors herd, and one credible yes reprices you for everyone else. A common tactic from Lenny's guide: open a SAFE and collect smaller angel checks first, then use that social proof to land the lead. Real urgency comes from an actually-closing round; faked urgency is transparent and backfires.
6. **Term sheet to close.** A **term sheet** (glossary) arrives. You negotiate for days, not weeks, then sign, and lawyers document it. SAFE money can wire within days; a priced round takes ~4–8 weeks from signed term sheet to money in the bank. Until then, Graham's mantra: **"Deals fall through"** and "it's not a deal till the money's in the bank." Keep other conversations warm until you've closed. **[2026]** total elapsed time, first meeting to wired funds: typically **3–6 months** ([H1 2026 data](https://hub.causo.ai/guides/h1-2026-state-of-seed-report)); hot AI deals with warm intros have closed in ~4 weeks.
7. **Expect rejection at volume.** VCs structurally say no to almost everything — a partner does 1–2 deals a year out of hundreds of pitches. Graham: don't internalize it; extract any specific feedback and keep moving. Then, per his final rule, stop: once you've raised, "don't leave the path" — go back to building.

### Lead investors and party rounds

**[Evergreen]** The **lead investor** is the fund that sets the terms (price, structure), writes the biggest check (usually 40–60% of the round), does the real *due diligence* (the investigation of your company — finances, legal, references — before wiring money), and often takes the board seat in a priced round. Everyone else "follows" on the lead's terms. As Lenny's guide notes, "Most rounds are put together with at least one big check and any number of angels and smaller funds."

A **party round** is a round with *no* lead — many small checks from angels and micro-funds (very small VC funds), usually on SAFEs. **[Evergreen]** Pros: fast, founder-friendly terms, no board seat, lots of helpful names. Cons: nobody owns enough to care when things get hard — no one to lead your bridge round (a small in-between round that extends your runway to a milestone), make the crucial intro, or vouch for you at Series A. Conventional wisdom (and mine): party rounds are fine at pre-seed; by seed, a committed lead is worth a couple points of extra dilution.

### Signaling risk

**[Evergreen]** — and worth its own heading, because it's invisible to newcomers. Big **multi-stage funds** — the Series A/B firms such as Sequoia, a16z (Andreessen Horowitz), and dozens more — also write small seed checks. Sounds great: a famous name on your cap table! The trap is laid out in [Elad Gil's "VC Signaling Coming Home To Roost"](https://blog.eladgil.com/p/vc-signaling-coming-home-to-roost). When you raise your Series A, every other investor will ask why the famous fund that knows you best isn't leading it. "If your seed round VC is passing on your company, then other VCs think it is probably a bad investment." And the math guarantees most seed portfolio companies get passed on — a fund making 30 seed bets but 10 Series A investments per year can follow on for *at most* 1 in 3. The signal is worse the more famous the fund, the bigger their check, and the more such funds are in your round. Mitigations (per Gil): keep multi-stage checks small relative to the round, prefer dedicated seed funds and angels as your core, and if you do take multi-stage money and they pass later, have the explanation ready (competitive conflict, minimal engagement). **[2026]** This matters *more* now, because multi-stage funds are doing more seed deals than ever — especially in AI — to keep a foot in the door on the category.

---

## 8. Venture debt, briefly

**Venture debt** is a loan (from specialist banks and funds) made to VC-backed startups. It's typically sized at 20–35% of your last equity round and repaid over ~3–4 years, with **warrants** — rights for the lender to buy a small amount of stock, usually well under 1% — as an equity sweetener. **[Evergreen]** What it's for: extending runway *after* an equity round without extra dilution. For example: raise a $4M seed, add $1M of debt, buy an extra quarter or two to hit Series A metrics. What it's not for: replacing equity you can't raise. Debt must be repaid on a schedule regardless of how the company is doing, and **covenants** — promises written into the loan agreement, e.g. maintaining a minimum cash balance or hitting revenue floors — can let the lender pull the loan exactly when you're weakest. Breach a covenant and the lender gets the right to demand immediate repayment ("call the loan"). **[Evergreen]** Rule of thumb: venture debt is a tool for companies that *could* raise equity choosing not to, never a lifeline for companies that can't. It's rarely relevant before seed; revisit at Series A. (The venture-debt market was reshaped by Silicon Valley Bank's 2023 collapse; the product survived at successor banks and dedicated funds. I have not verified current 2026 pricing, and terms vary widely, so get current quotes when the time comes.)

---

## 9. The 2026 market reality

Everything above is the machine; here is the weather. All **[2026]**.

**Capital is radically concentrated in AI.** AI companies take roughly **42% of all seed capital** (vs. ~23% pre-ChatGPT) per Carta, and by some counts [60%+ of all VC dollars in early 2026](https://hub.causo.ai/guides/h1-2026-state-of-seed-report). The market is genuinely split in two. AI-application seeds clear at $4–5M on $20–22M post-money. Hot AI *infrastructure* seeds have priced at $160–200M post (per Peter Walker, Carta's Head of Insights). Non-AI software seeds track ~$18M pre on ~$3M raised and take longer to close. Fewer rounds, larger checks: pre-seed round *count* fell 13% in 2025 while dollars fell only 1%.

**"Seed is the new Series A."** The traction bar at seed has migrated to where Series A used to be. Many seed funds now [want to see $300k–$500k ARR](https://www.pitchwise.se/blog/the-complete-guide-to-seed-and-series-funding-rounds-for-founders-in-2026) ("ARR" = annual recurring revenue) or steep usage growth before leading. AI-native companies showing $20–50k MRR (monthly recurring revenue) within months of founding are clearing the bar easily, which resets expectations for everyone else. Correspondingly, Series A got harder and slower: median seed-to-A time is 2.1–2.2 years, and while ~half of the 2017–2019 seed cohorts reached an A within four years, the post-2021 cohorts are graduating at roughly half that rate — ~15% of the Q1 2022 cohort raised an A within two years vs. ~31% for Q1 2018 (Carta cohort data; see Rung 4). First Round called this dynamic early in [What the Seed Funding Boom Means for Raising a Series A](https://review.firstround.com/what-the-seed-funding-boom-means-for-raising-a-series-a/).

**Small teams changed the sizing math.** Median seed-stage headcount is now ~6 employees (down from ~10 in 2021), because AI-leveraged teams ship more with fewer people. This cuts both ways for you: your $3M can genuinely last 24 months with 5 people — and investors know it, so "we need $6M for headcount" gets scrutinized. The credible 2026 pitch is a small team with fast revenue, not a hiring plan. (See `10-ai-era.md`.)

**What this means tactically for you, Bharat:** (1) if your idea has a genuine AI wedge — a narrow entry point where AI gives you a real edge — the market will pay a 40%+ valuation premium and move in weeks, but the bar for *what counts* as genuine is rising monthly; (2) if it doesn't, budget a longer raise (4–6 months), a ~$15–18M-ish cap, and more emphasis on revenue; (3) either way, the winning strategy in 2026 is the old one with the volume turned up: get to real revenue with a tiny team *before* raising seriously, so you're choosing investors rather than begging. NYC is fully viable for this; if you end up in the top 10% of market heat, expect the highest bids to come from SF funds regardless of where you sit.

---

## Glossary — plain words

- **ARR / MRR** — annual / monthly recurring revenue; the standard traction metrics for subscription software.
- **Angel** — an individual investing their own money in startups.
- **Bridge round** — a small round (usually SAFEs) between official rounds to extend runway to a milestone.
- **Burn rate** — cash spent per month, net of revenue.
- **Cap table (capitalization table)** — the ledger of who owns what percentage of the company: founders, investors, option pool, SAFEs. Kept in software (Carta et al.), not spreadsheets.
- **Convertible note** — the SAFE's predecessor: a loan that converts to equity later, with interest and a maturity date. Now rare (~9% of pre-seed deals).
- **Covenant** — a promise written into a loan agreement (e.g. keep a minimum cash balance); breaking one lets the lender demand immediate repayment.
- **Dilution** — the reduction in your ownership percentage when new shares are issued to investors or employees.
- **Discount** — a SAFE term converting the investment at a percentage off the next round's share price.
- **Due diligence** — the investigation an investor does before wiring money: finances, legal docs, references, metrics.
- **Fully-diluted ownership** — your percentage counted as if every share that could exist already did: issued shares plus converted SAFEs, the whole option pool, and warrants. The ownership number that actually matters.
- **Fully loaded (cost)** — the true all-in monthly cost of an employee: salary plus payroll taxes, benefits, equipment, and overhead.
- **Information rights** — an investor's contractual right to receive regular financial statements from the company.
- **Lead investor** — the fund that sets the round's terms, writes the largest check, does real diligence, and often takes the board seat.
- **Liquidation preference** — a preferred-stock right: when the company is sold or wound down, investors get their money back *first*, before common stockholders see anything. Standard is "1x non-participating": they choose either their money back or their ownership percentage of the proceeds, whichever is larger. Anything above 1x, or "participating" (money back *and* their percentage), is off-market at early stages — refuse it.
- **MFN (Most Favored Nation)** — a SAFE clause letting the holder adopt the terms of any better SAFE you issue later.
- **Multi-stage fund** — a large VC firm that invests from seed through late stages (source of signaling risk at seed).
- **Option pool** — shares reserved for future employee stock options; usually created pre-money, i.e., out of the founders' share.
- **Party round** — a round of many small checks with no lead investor.
- **Post-money / pre-money valuation** — company value after / before adding the new investment. Post = pre + raise.
- **Preferred stock** — the share class investors buy in priced rounds, carrying extra rights (liquidation preference, protective provisions) over founders' common stock.
- **Priced round (equity round)** — a financing where investors buy shares at a negotiated price per share, fixing the valuation exactly.
- **Pro-rata rights** — an investor's right to invest in future rounds to maintain their ownership percentage.
- **Protective provisions** — a list of company actions (sale, new financing, debt) requiring investor approval in a priced round.
- **Runway** — months of cash remaining at current burn: cash ÷ monthly net burn.
- **SAFE (Simple Agreement for Future Equity)** — YC's standard instrument: money now, shares later at the next priced round, converting at a valuation cap and/or discount.
- **Signaling risk** — the negative inference future investors draw when an existing (especially multi-stage) investor declines to follow on.
- **Step-up** — the multiple by which a company's valuation grows from one round to the next (a $20M seed valuation followed by a $52M Series A is a 2.6x step-up). Median seed-to-A step-up in 2025: ~2.6x.
- **Term sheet** — the short non-binding document stating a proposed investment's key terms (amount, valuation, board, pool, preferences); signing it starts legal documentation and, by strong convention, ends your talks with other leads.
- **VC (venture capital / venture capitalist)** — professional investing of other people's money into startups, or a person/firm that does it.
- **Valuation cap** — the maximum valuation at which a SAFE converts into shares; effectively the SAFE's price.
- **Venture debt** — loans to VC-backed startups, sized off the last equity round, repaid on a schedule, with small equity warrants for the lender.
- **Warrant** — a right to buy shares at a fixed price later; the equity sweetener in venture debt deals.

---

## Sources

- Y Combinator — [A Guide to Seed Fundraising](https://www.ycombinator.com/library/4A-a-guide-to-seed-fundraising) (Geoff Ralston) *(page is script-rendered; content verified via search excerpts)*
- Y Combinator — [SAFE documents and user guide](https://www.ycombinator.com/documents) and [Primer for post-money SAFE v1.1](https://www.ycombinator.com/assets/ycdc/Primer%20for%20post-money%20safe%20v1.1-2af8129e12effd9638eeab383b7309142c8f415e5cdb0bc210d573f779177a1c.pdf)
- Y Combinator — [YC's $500,000 Standard Deal](https://www.ycombinator.com/blog/ycs-500-000-standard-deal) (Jan 2022 announcement) and [The YC Deal](https://www.ycombinator.com/deal) (live page; terms verified unchanged July 2026)
- Paul Graham — [How to Raise Money](https://paulgraham.com/fr.html)
- Paul Graham — [The Fundraising Survival Guide](https://paulgraham.com/fundraising.html)
- Elad Gil — [VC Signaling Coming Home To Roost](https://blog.eladgil.com/p/vc-signaling-coming-home-to-roost) and [High Growth Handbook, Ch. 8: Financing and Valuation](https://growth.eladgil.com/book/chapter-8-financing-and-valuation/types-of-late-stage-investors/)
- Carta — [State of Pre-Seed: Q1 2026](https://carta.com/data/state-of-pre-seed-q1-2026/) *(direct page blocks fetching; data obtained via the summaries below)* and [Pre-Seed Funding guide](https://carta.com/learn/startups/fundraising/pre-seed-funding/)
- SaaStr — [The State of Seed Today: 10 Key Learnings from Carta's Latest Data](https://www.saastr.com/the-state-of-seed-today-10-key-learnings-from-cartas-latest-data), [The Series A Landscape in 2025 (Chemistry VC's Ethan Kurzweil)](https://www.saastr.com/the-series-a-landscape-in-2025-insights-from-chemistry-vcs-ethan-kurzweil/), and [Your Seed Round Now Needs to Last 3+ Years](https://www.saastr.com/your-seed-round-now-needs-to-last-3-years-what-3365-startups-tell-us-about-the-new-series-a-timeline/)
- Incisive Ventures — [Update on Venture Graduation Rates](https://incisive.vc/2025/06/10/update-on-venture-graduation-rates/) *(compiles Carta cohort graduation data: 15.4% of Q1 2022 seed cohort raised an A within two years vs. 30.6% for Q1 2018)*
- VC Lens (formerly My Unicorn Club) — [Carta State of Pre-Seed 2025 Explained](https://vclens.substack.com/p/carta-state-of-preseed-2025-explained) *(source for the pre-seed cap medians by round size and the 330k+ SAFE/note volume figure)*
- Causo Hub — [State of Seed Fundraising 2026: H1 Report](https://hub.causo.ai/guides/h1-2026-state-of-seed-report), [Seed valuation 2026: ranges, SAFE caps, and dilution math](https://hub.causo.ai/guides/seed-valuation-2026), and [Seed-to-Series A Graduation Rate Benchmarks 2026](https://hub.causo.ai/guides/seed-to-series-a-graduation-rate-benchmarks-2026) *(source for the PitchBook-NVCA Q1 2026 Series A medians: $19.6M deal size, $62.0M pre-money)*
- Lenny's Newsletter — [Raising a Seed Round 101](https://www.lennysnewsletter.com/p/raising-a-seed-round-101)
- First Round Review — [The Fundraising Wisdom That Helped Our Founders Raise $18B in Follow-On Capital](https://review.firstround.com/the-fundraising-wisdom-that-helped-our-founders-raise-18b-in-follow-on-capital/) and [What the Seed Funding Boom Means for Raising a Series A](https://review.firstround.com/what-the-seed-funding-boom-means-for-raising-a-series-a/)
- Elego Law — [Decoding the YC SAFE: A Term-by-Term Guide](https://www.elego.law/insights/decoding-the-yc-safe-a-term-by-term-guide)
- CRV — [How to Raise Seed Funding](https://www.crv.com/content/seed-funding) and [AI Startup Funding: What Investors Look for in 2026](https://www.crv.com/content/ai-startup-funding)
- Pitchwise — [The Complete Guide to Startup Funding Rounds in 2026](https://www.pitchwise.se/blog/the-complete-guide-to-seed-and-series-funding-rounds-for-founders-in-2026)
