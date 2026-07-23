# The Playbook — from pre-idea to funded startup

**Read this first.** This is the master synthesis of a 12-document research library built for one reader: Bharat — technical, in NYC, pre-idea with a few candidate directions, new to the startup world, wanting to build something big. Every section below answers one of your literal questions, states the timeless rule (**Evergreen**), then what's different right now (**[2026]**), and links to the library doc that goes deep. Every jargon term is defined the first time it appears. Nothing here requires prior startup knowledge.

The one-sentence version of the whole library: **your successful friends were not smarter — they knew a set of legible, learnable rules that nobody writes down in one place, and they manufactured their "certainty" out of cheap evidence before betting years on it.** This document is those rules, in order of when you'll need them.

---

## 1. What do successful founders know that you don't?

Five things. None of them are secrets; all of them are unwritten.

### 1.1 They know it's a game with published rules — and they learned the scoring system

**Evergreen.** When your friends sat in pitch meetings, both sides were running shared mental shortcuts: what a "big enough" market is, what "good" growth looks like, how much of the company you're supposed to sell per round, what number unlocks the next round. Founders who don't know these heuristics get filtered out early or sign bad deals without realizing it. The full decoder ring is [rules of thumb](00-rules-of-thumb.md); the ones you must internalize now:

- **Startup = growth.** Paul Graham's definition: a startup is a company designed to grow fast — 5–7% *per week* is good at the earliest stage, because 5%/week compounds to ~12.6x per year. Growth rate, not size, is what investors ask about.
- **VC money is power-law money.** A venture fund's returns come almost entirely from one or two outlier companies; the rest are "a cost of doing business." So when an investor asks "how big can this get?", they're checking whether your ceiling, times their ownership, can return their entire fund. A business *certain* to be worth $50M is a *worse* VC bet than a 5% shot at $5B. This single fact explains most otherwise-mysterious investor behavior — the obsession with $1B+ markets, the fast passes, the "come back when you're bigger."
- **Dilution compounds.** You'll sell roughly 12–20% of the company per early round (the current medians, from Carta's cap-table data), and each round multiplies against what's left — the median founding team owns ~56% after seed and ~36% after Series A. Details and the SAFE mechanics that trip up first-timers: [fundraising mechanics](05-fundraising-mechanics-2026.md).
- **Retention is the truth serum.** Growth can be bought; signups can be spiked; the only unfakeable signal that people want your product is that they keep using and paying for it, cohort after cohort. ("Cohort" = the group of customers who started in the same month, tracked over time.)

**[2026].** The numbers moved, hard. AI companies take roughly half of all venture dollars. The best AI-native startups grow so fast (Lovable: $0 to $100M ARR in eight months with 45 people) that the perceived bar rose for everyone — "seed is the new Series A," with many seed funds wanting $300–500K ARR ("ARR" = annual recurring revenue, the yearly run-rate of subscription income) before leading. Meanwhile the *scrutiny* rose too: median revenue retention for AI-native products is catastrophically low (the "AI churn wave"), so investors now probe whether fast AI revenue is real, retained, and profitable after compute costs. Full sorting of what changed vs. what didn't: [the 2026 AI era](10-ai-era-2026-what-changed.md).

### 1.2 They know most startups die of one specific disease — and they check for it first

**Evergreen.** The number-one killer, across every failure study ever run, is **no market need**: building a solution nobody urgently wants (42% of failure post-mortems). "Ran out of cash" is the mechanism of death, not the cause — the cash ran out because nobody wanted the thing. Your friends internalized this, which is why they spent their first months talking to customers instead of building. The graveyard, with names and dollar amounts, is [failure patterns](11-failure-patterns-and-case-studies.md) — read it to understand that every diligence question an investor asks you is the ghost of a specific dead company.

### 1.3 They know conviction is an output, not an input

**Evergreen.** From the outside, your successful friends looked certain from day one. They weren't. Almost all of them ran an unglamorous, repeatable evaluation process — interviews, cheap tests, pre-sales — and their certainty was *manufactured out of evidence, piece by piece*. A founder with earned conviction and a deluded founder look identical in confidence; they differ only in evidence. The full process is Section 2 below and [idea evaluation](01-idea-evaluation-and-conviction.md).

### 1.4 They know the startup world allocates everything through networks

**Evergreen.** Funding, first hires, first customers, and real market information all flow through warm introductions and vouching, not applications and forms. A "warm intro" — an introduction from someone the investor already trusts — converts roughly 10x better than cold email. Nobody tells newcomers this explicitly. The good news: access is buildable from a standing start, and Section 3 covers how. Deep dive: [networks](09-networks-and-who-can-help.md).

### 1.5 They know which advice is timeless and which is dated

**Evergreen.** Most bad startup advice is evergreen advice and current-era advice mislabeled as each other. "Talk to users" is permanent physics. "Raise $2M at a $12M cap" is weather. Your friends could tell the difference; this library tags every claim so you can too.

---

## 2. How did they reach certainty — what did they evaluate, in what order?

This is the most learnable thing in the whole library. The order matters: analysis picks the *space*, empiricism picks the *idea*, and conviction arrives at the end, not the beginning.

### Step 1: Pick the space by living in the future

**Evergreen.** Graham's rule: "The way to get startup ideas is not to try to think of startup ideas." The best ideas are *noticed*, not invented — by people at the leading edge of a fast-changing field, using the newest tools as real users and writing down every gap. Two biases hide the good ideas from you: **schlep blindness** (your unconscious filters out ideas involving painful work — sales grind, regulation, banks — which is exactly why they're uncontested; Stripe sat in plain sight for a decade) and **tarpit ideas** (ideas that look appealing and easy, and have killed waves of founders — social discovery apps, plan-with-friends apps, and in 2026, thin "AI wrapper" chatbots). **[2026]:** for you, living in the future means using frontier AI models and agent tools daily in your candidate domains and cataloguing what breaks.

One de-stressing data point: roughly a quarter of YC's top companies pivoted to a completely different idea. The space matters more than the first idea. Choose a rich problem space; hold the specific idea loosely.

### Step 2: Score the idea before touching it

**Evergreen.** The canonical checklists converge on the same questions (Kevin Hale and Jared Friedman of YC, plus angels Naval Ravikant and Elad Gil — all detailed in [idea evaluation](01-idea-evaluation-and-conviction.md)):

1. **Is the problem urgent, frequent, and expensive** for a specific, nameable group? Hale's "hair on fire" test: can you name 10 people who need this so badly they'd use a broken v1?
2. **Founder-market fit:** are *you* among the best-placed people alive to build this? (Your technical skill is real leverage — but the strongest version pairs it with domain exposure.)
3. **Why now:** what recent, specific unlock — a technology crossing a threshold, a cost collapsing, a law changing, behavior shifting — makes this possible today when it wasn't five years ago? **[2026]:** "LLMs got good" is now *everyone's* why-now and differentiates nothing. You need the second-order version: "LLMs got good **and** [specific industry] has [specific painful workflow] with [specific data or distribution] that generalist tools can't touch."
4. **Your secret** (Thiel): what do you believe, from lived experience, that the consensus rejects — and what evidence says you're right?
5. **The venture-scale arithmetic:** buyers × realistic price × plausible penetration — does the best case clear a path to ~$100M ARR? If not, it can still be a great business, just not a venture-funded one (a legitimate choice — see [business models](02-business-model-taxonomy.md)).
6. **[2026] The wrapper test:** if OpenAI/Anthropic/Google shipped your product as a feature next quarter, would your customers cancel? If yes, you're building a feature. The sanctioned counterweight: before product-market fit your only real moat *is* speed — "a moat is not a starting point, it's a result." Evaluate for a plausible *eventual* moat (proprietary data loops, workflow depth, distribution), then win by moving fast. Full moat treatment: [the 2026 AI era](10-ai-era-2026-what-changed.md).

Also run the **premortem**: write, in past tense, the most plausible obituary of the idea three years out, and force-rank which canonical death killed it. The checklist is at the end of [failure patterns](11-failure-patterns-and-case-studies.md).

### Step 3: Climb the evidence ladder

**Evergreen.** This is where certainty is actually built — each rung costs more and proves more. Grade every signal by what it cost the person giving it: **opinions < time < reputation < money.**

1. **~30 problem interviews** in a tight segment, asking only about *past behavior* ("walk me through the last time this happened; what have you already tried?") — never "would you use this?", because people lie politely. The full technique, scripts, and the Mom Test rules: [talking to users](08-talking-to-users-and-people.md).
2. **A minimum viable test** of the single riskiest assumption — a landing page with a price on it, a manual "concierge" version of the service, a demo shown to skeptical professionals. Not a full product.
3. **Commitments:** design partners (early customers who commit weekly time to shape the product), signed letters of intent with numbers on them, and best of all **pre-payment** — even $500/month. Money and calendar time are the only honest currencies.
4. **Retention and pull:** people keep using the ugly v1, complain when it breaks, and strangers arrive unbidden. This is what product-market fit feels like — "if you have to ask whether you have it, you don't."

Write your **kill criteria in advance** — the specific results that would make you drop the idea — because decided in advance it's discipline, decided after the fact it's rationalization. Run 2–3 candidates through the early rungs *in parallel*; comparison is the cheapest cure for infatuation. Expect 2–4 months per serious candidate. The complete ladder with pass/fail conditions is in [idea evaluation](01-idea-evaluation-and-conviction.md); the week-by-week execution plan is in [talking to users](08-talking-to-users-and-people.md).

---

## 3. Who did they have access to — and how do you get it from NYC?

### What they had

**Evergreen.** Nearly every hard early step — co-founder, first hire, first customer, first check — was unlocked by a *person*, usually one or two hops away: an ex-boss who became their angel investor, a classmate who became their co-founder, an ex-colleague who became customer #1. Vouching is transitive and compounds: one respected person who rates you introduces you to five more who now start from trust. The categories that matter, in order of value: founder-mentors 2–10 years ahead of you, operator angels (individuals from successful startups investing their own $5–100K checks), accelerator networks, and ex-colleague "mafias." Full map: [networks](09-networks-and-who-can-help.md).

### How you build it, starting from zero

**Evergreen.** The norm is inverted from what newcomers expect: **you don't get access by asking for things; you get it by being interesting and useful, after which people offer things.** The mechanics:

- **Do impressive work in public.** Ship small demos in your candidate directions and post 60-second videos with short writeups. This lets busy people evaluate you asynchronously at zero cost — the opposite of "can I pick your brain?"
- **Give before you ask.** Send useful things (leads, candidates, sharp feedback). Reliably doing what you said you'd do puts you in the top quartile by itself.
- **Cold outreach done right:** 5–8 sentences, why *them specifically*, one low-lift ask (advice or a reaction — never money or intros first), demo link attached, an explicit out ("no need to reply if not relevant").
- **Monthly update emails** to everyone who has helped — what you shipped, learned, one ask. This is how mentors and investors decide who to keep helping; after months of updates, intros start arriving unprompted.
- **Close every loop.** Report back to whoever made an intro. The community is small and memory is long.

**[2026].** This is the easiest era ever for a technical person to build access from scratch, because demonstrating skill in public has never been cheaper — investors and senior operators actively scout people who ship impressive demos.

### The NYC map

**[2026].** NYC is the firm #2 US ecosystem, and for *applied* AI arguably the best place to build: 71% of NYC's venture-backed AI startups are vertical applications (software for one industry — finance, law, health, real estate), and the Fortune 500 customers are in the same subway system. The specific rooms and names, all detailed in [networks](09-networks-and-who-can-help.md) and [the investor landscape](06-investor-landscape-and-accelerators.md):

- **Communities:** AI Tinkerers NYC (the highest-density technical AI meetup — attend twice, then apply to *demo*, which flips you from audience to participant), South Park Commons NYC (a selective community *specifically* for the pre-idea phase — your exact stage; its Founder Fellowship offers $400K for 7% and can be done from NYC), Betaworks Camps, NY Tech Week in June, Antler NYC for co-founder matching.
- **NYC seed funds to know:** USV, First Round, Primary, BoxGroup, Lerer Hippeau, FirstMark, Work-Bench (enterprise software — they hand portfolio companies Fortune 500 customers), Company Ventures. NYC angels: Fabrice Grinda/FJ Labs, Kevin Ryan/AlleyCorp, Joanne Wilson.
- **The SF question:** you don't have to choose today. The trodden path is build and sell from NYC, and if accepted, do a 3-month SF program (YC's $500K standard deal for ~7% remains the strongest expected-value trade for a first-time founder without a network; a16z speedrun and Neo are alternatives). Fly to SF for fundraising sprints — the biggest AI checks cluster there — but NYC is fully sufficient for pre-seed and seed. If you end up building *the model* rather than *an application*, revisit.

### Co-founder

**Evergreen.** The highest-stakes network decision. Investors read a strong co-founder as proof you can convince one talented person to bet their career on you — and ~65% of high-potential startup failures trace to founding-team conflict. Norms: trial-work together for 2–8 weeks before committing; split equity equally or near-equally (execution over a decade dwarfs whose idea it was); **4-year vesting with a 1-year cliff is non-negotiable** (vesting = equity earned over time, so a departing co-founder doesn't leave with half the company). As the technical half, you're the scarce side of the pairing — don't add a "business co-founder" who only brings slides. Sources: ex-colleagues first, then YC's free co-founder matching platform, SPC, and hackathons. Details: [networks](09-networks-and-who-can-help.md).

---

## 4. How do business models, pricing, and money actually work — the 20% that matters

### Business model: it's half the idea

**Evergreen.** Two startups attacking the same problem with different models have wildly different margins, funding needs, and endgames. The full taxonomy — SaaS, usage-based, marketplaces, enterprise, hardware, open source, and the 2026 AI-native models — with tradeoffs and famous corpses for each, is [business models](02-business-model-taxonomy.md). The compressed decision logic:

- **Who feels the pain, and who controls the budget?** Individuals → self-serve/product-led. Teams → seat-based SaaS. Executives with a P&L problem → enterprise sales or outcome pricing.
- **Gross margin is destiny.** Gross margin = the share of each revenue dollar left after the direct cost of serving the customer (servers, AI compute, support). Software is prized because it runs 75–90%; every efficiency rule investors apply silently assumes ~80%. A 40%-margin business needs double the revenue for the same profit engine.
- **Recurring revenue is worth a multiple of one-time revenue,** because it runs next year without being resold.

**[2026].** Three big shifts. (1) **Per-seat pricing is breaking for AI products** — if the AI does the work, headcount shrinks and your revenue shrinks as your product improves. (2) **AI products can price against labor budgets, not software budgets** — labor budgets are ~10x bigger, which is why AI startups can sign contracts SaaS never could ("service-as-a-software": selling completed work, like Sierra's pay-per-resolved-ticket). (3) **The modal winning structure is hybrid**: a predictable platform/subscription fee plus a usage or outcome component. Default advice for you: B2B, hybrid-priced, sold to a budget you can name, gross margin ≥60%, first revenue within 6 months. Deviate knowingly.

### Pricing: the highest-leverage decision founders neglect

**Evergreen.** Three rules cover most of it (full frameworks and worked examples: [pricing](03-pricing.md)):

1. **Price on value, not cost.** Quantify what the product is worth to one specific segment (hours saved × loaded labor cost + revenue gained) and charge ~10–20% of it. The technical founder's instinct — charge little because the code cost "nothing" — is exactly backwards and structurally fatal: your price determines whether you can ever afford salespeople, and cheapness signals toy.
2. **Charge more.** The single most-repeated pricing advice in startup history (Marc Andreessen's billboard: "Raise Prices"). Practical rule: quote a price with a straight face; if nobody flinches, double it for the next prospect; you're correctly priced when ~20–30% of qualified prospects push back.
3. **The pricing *metric* matters more than the number.** Choose the unit you charge by (per seat, per usage, per outcome) so the customer's bill grows as their value grows — that's what makes existing customers expand without a re-sale. Ask prospects the willingness-to-pay questions *before* building ("what would be an acceptable / expensive / prohibitive price?"), never "would you pay?"

**[2026].** Know your inference cost per unit of value ("one resolved ticket costs us $0.11 of compute") and price with a floor above it — flat-rate unlimited plans are how AI startups die, because 10% of power users burn 70–80% of the compute. Outcome pricing (Intercom's $0.99 per resolved conversation) is powerful but only where outcomes are countable and attributable.

### Unit economics: the arithmetic that keeps you alive

**Evergreen.** Everything an investor will ever probe reduces to napkin math you can learn in an afternoon — [unit economics](04-unit-economics-and-money.md) teaches all of it with worked examples. The five that matter most:

- **CAC and payback:** CAC = what you spend on sales/marketing to win one customer. Payback = months until that customer's *gross-profit* dollars repay their CAC. Under 12 months is excellent; over 24 is alarming.
- **LTV:CAC ≥ 3** is the folk convention — but early on both numbers are fiction; show the retention curve instead.
- **Retention curves that flatten** are the best product-market-fit signal in existence. A curve decaying to zero means a leaky bucket no growth can fix.
- **Default alive or default dead** (Graham's question): at current growth and spending, do you reach profitability before the cash runs out? Half of founders can't answer; the calculation takes five minutes and the ones who don't know are almost always the ones in trouble. Corollary: **over-hiring is the #1 killer of funded startups** — every hire is ~$19K/month of runway.
- **Investors read metrics in a fixed order:** size (ARR) → growth → quality (retention, margin) → efficiency (payback, burn multiple). Know yours cold; hesitating on your own churn number is worse than the number.

### Fundraising: the machine, compressed

**Evergreen mechanics, [2026] numbers** — full detail in [fundraising mechanics](05-fundraising-mechanics-2026.md) and [the investor landscape](06-investor-landscape-and-accelerators.md):

- **The ladder:** angels → pre-seed (~$500K–$2.5M on SAFEs) → seed (~$3–4M, ~$20M valuations, heavily AI-skewed) → Series A (~$1M+ ARR floor, realistically $2M+ for non-AI; only ~20–25% of recent seed cohorts graduate, so plan your seed to last).
- **The SAFE** (Simple Agreement for Future Equity — YC's standard 5-page contract: money now, shares later at your next priced round, subject to a valuation cap) is the default instrument. The gotcha: post-money SAFEs don't dilute each other — every SAFE you stack comes entirely out of *you*. Track your fully-diluted ownership from day one.
- **A raise is a designed, parallel, compressed process** — 40–80 researched investors, warm intros, all first meetings inside a 2–3 week window to manufacture urgency — not a series of ambient coffee chats. The first committed check is half the battle; investors herd.
- **The pitch** is a compression test of your thinking, not a slide performance: what you do in your mom's vocabulary → who has the problem and how badly → why now → what you understand that others don't → traction → team → ask. Bottom-up market math only; never "no competition." **[2026]:** lead with a live demo, bring reliability numbers (not cherry-picked outputs), and have a worked answer to "what's your gross margin and what happens when OpenAI ships this?" Full grammar: [pitching](07-pitching-and-storytelling.md).
- **The strongest negotiating position is not needing the money.** Ramen profitability — revenue covering founders' living costs — transforms every conversation, and **[2026]** AI tooling makes "two people, real revenue, tiny burn" more achievable than it's been in a decade. Get to revenue before you raise seriously, so you're choosing investors rather than begging.

---

## 5. Your path: pre-idea with candidates → funded startup

The sequence, with the library doc for each phase:

1. **Weeks 0–8 — Evaluate in parallel.** Run your 2–3 candidate directions through the scoring checklist and desk research ([idea evaluation](01-idea-evaluation-and-conviction.md)), premortem each ([failure patterns](11-failure-patterns-and-case-studies.md)), and start problem interviews ([talking to users](08-talking-to-users-and-people.md)). Build your public surface and network in parallel ([networks](09-networks-and-who-can-help.md)).
2. **Weeks 8–16 — Converge and validate.** Pick the winner. Climb the evidence ladder: minimum viable test → design partners → first money. Choose model and pricing hypothesis ([business models](02-business-model-taxonomy.md), [pricing](03-pricing.md)).
3. **Weeks 16–24 — Build with commitments in hand.** Ship the embarrassing v1 to committed users. Watch retention, not signups. Solidify the co-founder relationship on standard terms.
4. **Then — raise from strength.** With real usage or revenue: apply to YC (and SPC/Neo/speedrun), and/or run a designed pre-seed/seed process ([fundraising](05-fundraising-mechanics-2026.md), [investors](06-investor-landscape-and-accelerators.md), [pitching](07-pitching-and-storytelling.md)). Rejection is weak signal; reapplying with visible progress is a positive pattern.

### The 90-day action plan (NYC, technical, starting now)

**Days 1–30 — Surface and shortlist.**
- Write a one-page hypothesis for each candidate direction: problem, who has it, why now, your secret, and *written kill criteria*. One day each.
- Desk-check each: tarpit search (who tried this and died?), venture-scale arithmetic, the wrapper test. Kill or keep. (2–3 days each.)
- Write your public one-liner: "Technical founder exploring X and Y, currently building Z to learn." Ship one small, impressive demo in your strongest direction; post a 60-second video and short writeup. Repeat every ~2 weeks.
- Reactivate 20 people you already know who are 1–2 degrees from startups — the single highest-ROI action available to you. Tell them what you're exploring; ask each one specific question.
- Attend one AI Tinkerers NYC event and one other meetup. Three real conversations each, same-day follow-ups. Sign up for YC's free Startup School; browse co-founder matching to calibrate.
- Start the interview pipeline: list 50 target interviewees across your top two candidates; send the first 40 outreach messages ("researching how [role] handles [task] — not selling anything").

**Days 31–60 — Interview and demo.**
- Run 10–15 problem-discovery interviews per surviving candidate (past behavior only; record; end each with "who else should I talk to?"). Mid-point synthesis: is one pain named unprompted by >50%? Have most people already tried to solve it? If no — kill or reshape, and count it as a win.
- Apply to demo at AI Tinkerers. Apply to South Park Commons NYC — it is built for exactly your stage.
- Cold-outreach sprint: 15 carefully researched advice-asks (never money-asks) to NYC founders and operator angels in your candidate spaces, demo attached. 3–5 real conversations = success.
- Start a monthly update email to everyone who has helped so far.
- Build the cheapest possible validation artifact for your leading candidate: a working demo (B2B) or a landing page with a price on it plus ~$500 of ads (consumer).

**Days 61–90 — Commit and convert.**
- Run 8–10 solution-validation interviews with your artifact, including at least 3 with economic buyers (the people who control budget, not just the people who feel the pain). End every one with a real ask: design-partner slot, LOI with a number on it, or a paid pilot. "Maybe" = no.
- Write the one-page verdict against your Week-0 kill criteria: build / pivot / kill, with evidence. Show it to the smartest skeptic you know.
- If building: go back to the 2–3 most useful people from your conversations with results ("you suggested X; here's what happened") — this is how mentors form. Put your YC co-founder-matching profile live and invite the best 1–2 builders you've met to a trial project on standard terms.
- Host one small themed dinner or build-night for the best 6–8 people you've met. You're now a node, not an edge.
- Checkpoint: ~5 people who'd take your call within a day, ≥2 proto-mentors, ≥1 trial co-founder conversation, 1 public demo with real engagement, 25–30 interviews on your lead idea, and at least one commitment of time, reputation, or money. At half of this, you're on track — compounding is slow for 90 days, then startlingly fast.

Total cash cost of all of the above: roughly $1,000–2,000. Compare that to the cost of spending a year building the wrong thing — which is the mistake this entire library exists to prevent.

---

## The compressed rulebook

1. Make something people want; "no market need" is the #1 killer. **Evergreen**
2. Conviction is manufactured from evidence — opinions < time < reputation < money. **Evergreen**
3. Growth rate defines a startup; retention defines product-market fit. **Evergreen**
4. Price on value, charge more, and pick the metric before the number. **Evergreen**
5. Gross margin is destiny — and AI inference made it a live question again. **Evergreen rule, [2026] numbers**
6. Know if you're default alive; over-hiring is the top killer of funded startups. **Evergreen**
7. Access comes from public work + usefulness + closed loops, not from asking. **Evergreen**
8. Dilution compounds; track fully-diluted ownership; a raise is a designed sprint. **Evergreen**
9. In 2026: tiny teams, labor-budget pricing, speed-as-moat, and forensic churn scrutiny are all real. Build with 2026 leverage on evergreen foundations. **[2026]**
10. When 2026 advice and evergreen advice conflict on a decade timescale, evergreen wins. **Evergreen**
