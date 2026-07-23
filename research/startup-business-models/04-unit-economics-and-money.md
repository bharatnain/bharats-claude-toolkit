# Unit Economics & Understanding Money

**Why this matters to you:** You said you want to "understand money." This is the single highest-leverage document in this library for that. Investors, co-founders, and eventually your own dashboard speak a compressed dialect — CAC, LTV, NRR, burn multiple, default alive (all defined below). Founders who can't speak it get worse terms, hire too fast, and die with money in the bank because they never did the arithmetic. Everything here is arithmetic you can do on a napkin. None of it requires an accounting degree. The payoff is concrete: Paul Graham found that [half the founders he talked to didn't know whether their company was default alive or default dead](https://paulgraham.com/aord.html). After reading this, you'll be able to answer that question for your own company in about five minutes. Read it once end-to-end, then keep it as a reference.

---

## 1. The startup P&L in plain words

A **P&L** (profit-and-loss statement, also called an income statement) is a list of money-in and money-out over a period, arranged in a specific order. **[Evergreen]** The order matters because each line tells a different story:

| Line | Plain-words meaning |
|---|---|
| **Revenue** | Money customers actually paid you (or contractually owe you) for the period. Not signed contracts, not pilots, not "commitments." |
| **COGS** (cost of goods sold) | What it costs to *deliver* the product to the customers you already have: servers, AI inference (paying OpenAI/Anthropic per token), payment processing fees, customer support. If revenue went to zero and you shut off delivery, COGS would go to ~zero too. |
| **Gross profit / Gross margin** | Revenue − COGS. Gross *margin* is that as a percentage of revenue. This is the money you have left to run the rest of the company. |
| **Opex** (operating expenses) | Everything else: salaries of engineers and salespeople, rent, laptops, legal, marketing. Costs you'd still have next month even if delivery paused. |
| **Operating profit / loss** | Gross profit − Opex. For nearly every startup you'll ever run, this is negative for years. That's normal and intentional. |
| **Burn** | How much cash leaves the bank each month. **Net burn** = expenses − revenue collected. **Gross burn** = total expenses, ignoring revenue. [a16z's "16 Startup Metrics"](https://a16z.com/16-startup-metrics/) insists you distinguish these. When investors say "burn," they mean *net burn* unless they say otherwise. |

**Worked mini-P&L** — a 6-person AI SaaS (software-as-a-service: software sold as a subscription) doing $60K MRR (monthly recurring revenue — subscription revenue per month):

- Revenue: $60,000/mo
- COGS: $21,000/mo (inference $15K, hosting $3K, support contractor $3K) → **Gross margin = ($60K − $21K)/$60K = 65%**
- Opex: $110,000/mo (6 people fully loaded ≈ $95K, tools/rent/legal ≈ $15K)
- Operating loss: $39K − $110K = **−$71K/mo** → net burn ≈ $71K/mo. With $1.4M in the bank, runway ≈ 20 months.

One accounting trap worth knowing on day one: **bookings ≠ revenue**. A signed $120K annual contract is a *booking*. Under accounting rules, you recognize it as revenue $10K per month as you deliver. a16z lists conflating these as mistake #1 founders make with investors. **[Evergreen]**

---

## 2. Unit economics from scratch

"Unit economics" means: ignore the whole company for a second — does *one customer* make you more money than it costs to acquire and serve them? If yes, growth creates value. If no, growth destroys value faster. **[Evergreen]**

### CAC — customer acquisition cost

**CAC** = total sales + marketing spend in a period ÷ new customers acquired in that period.

Two flavors, per [a16z](https://a16z.com/16-startup-metrics/):
- **Blended CAC**: all channels, including free ones (word of mouth, SEO — free traffic from search engines — and your Twitter). Makes you look good.
- **Paid CAC**: paid spend ÷ customers from paid channels only. Tells you whether pouring money into acquisition actually scales. Investors ask for paid CAC precisely because blended CAC flatters you. **[Evergreen]**

Include salespeople's salaries in CAC, not just ad spend. A common early-stage dodge is "our CAC is $200!" when the founder doing all the selling is unpaid. Investors mentally re-add your time.

### LTV — lifetime value, and why the naive version lies

**LTV** = total profit you expect from one customer over their whole life with you.

The textbook formula: **LTV = ARPA × gross margin % ÷ monthly churn rate**. Here **ARPA** is average revenue per account per month, and **churn** is the % of customers (or revenue) that cancels each month. The `÷ churn` term works because 1/churn = average customer lifetime in months (3% monthly churn → average lifetime ≈ 33 months).

Three ways naive LTV lies — sophisticated investors know all three: **[Evergreen]**

1. **Using revenue instead of profit.** [a16z](https://a16z.com/16-startup-metrics/) calls this out explicitly: LTV is the present value of *net profit* from the customer — multiply by gross margin. A $100/mo customer at 60% gross margin is worth $60/mo, not $100.
2. **Extrapolating from tiny data.** With 6 months of history and 2% measured monthly churn, the formula claims a 50-month lifetime. You have no idea whether customers who've been around 2 years behave like customers who've been around 2 months. Early cohorts are also your friends and design partners — they churn less than strangers will.
3. **Assuming churn is constant.** Real churn is usually front-loaded: lots of cancellations in months 1–3, then it flattens. A single average churn number hides this. This is why cohort analysis (Section 3) beats the formula.

Practical early-stage rule: quote LTV honestly as a *range* — or better, just show the retention curve and let investors compute it. **[Evergreen]**

### Contribution margin

**Contribution margin** = revenue from a customer − *all* variable costs of acquiring and serving them (COGS + variable **S&M** — sales & marketing spend, the standard abbreviation in every investor deck and in the examples below). It answers: "each incremental customer contributes $X toward covering fixed costs" — rent, engineers' salaries, costs that don't change with one more customer. If contribution margin is negative, you lose money on every customer, and "make it up in volume" is a joke, not a strategy. **[Evergreen]** Both worked examples below compute it as a number — watch for it.

### CAC payback period

**Payback period** = CAC ÷ (monthly revenue per customer × gross margin %). It tells you how many months until a customer's *gross profit* repays what you spent to get them. This is arguably the single most useful operational metric, because it controls how cash-hungry growth is.

Benchmarks — the principle is [Evergreen], the numbers are current consensus:
- [David Skok, "SaaS Metrics 2.0"](https://www.forentrepreneurs.com/saas-metrics-2/): **LTV:CAC > 3**, **CAC payback < 12 months**; "many of the best SaaS businesses are able to recover their CAC in 5–7 months."
- [Bessemer's benchmarks](https://www.bvp.com/atlas/cloud-computing-metrics) frame it as good/better/best: **12–18 months good, 6–12 better, under 6 best**. **[2026]**

Skok's framing of why this matters: a SaaS company spends the CAC up front and collects revenue over years. That creates a "cash flow trough" — the faster you grow, the deeper the trough. This is *why* SaaS companies raise venture money at all (see `02-business-models.md`).

### Worked example 1 — classic SaaS

You sell a $150/mo dev-tool subscription. Gross margin 85% (pure software). Last quarter you spent $12,000 on ads plus a part-time SDR (sales development representative — a junior salesperson who cold-emails and books meetings with prospects) and closed 20 customers.

- CAC = $12,000 ÷ 20 = **$600**
- Monthly gross profit per customer = $150 × 0.85 = $127.50 (COGS = $22.50/mo per customer)
- **Payback = $600 ÷ $127.50 ≈ 4.7 months** — excellent (Skok's "best SaaS" range)
- **First-year contribution margin per customer** = revenue − COGS − variable S&M = ($150 × 12) − ($22.50 × 12) − $600 CAC = $1,800 − $270 − $600 = **+$930**. Each new customer contributes $930 toward payroll and rent in year one — and $1,530/year after that, since the CAC was already spent. Positive and growing: acquisition is worth funding.
- Measured monthly revenue churn = 2.5% → implied lifetime = 40 months → naive LTV = $127.50 × 40 = **$5,100** → LTV:CAC = 8.5×. Report it as "well above 3×, but from only 2 quarters of data." That honesty reads as sophistication, not weakness. (Lifetime contribution per customer = LTV − CAC = $5,100 − $600 = $4,500.)

### Worked example 2 — usage-based AI product

You sell an AI document-processing API at $0.08/page. A typical customer processes 50,000 pages/mo → $4,000/mo revenue. Inference + compute costs you $0.035/page → COGS $1,750/mo → **gross margin 56%** (typical for inference-heavy products — see Section 7). CAC via outbound sales ≈ $9,000 per customer.

- Monthly gross profit per customer = $4,000 − $1,750 = $2,250
- **Payback = $9,000 ÷ $2,250 = 4 months** — great
- **First-year contribution margin per customer** = revenue − COGS − variable S&M = ($4,000 × 12) − ($1,750 × 12) − $9,000 CAC = $48,000 − $21,000 − $9,000 = **+$18,000**. Looks fantastic — *but* note how sensitive it is. If usage halves, contribution drops to ($24,000 − $10,500 − $9,000) = $4,500. That's a 75% collapse from a 50% usage drop, because the CAC was fixed. That leverage cuts both ways — it shapes both the LTV range below and the ARR caveat after it:
- **LTV — computed as a range, on purpose.** For a subscription product, you'd divide by one churn number and move on. For usage-based revenue, the honest move is to bracket it, because revenue can shrink *without anyone canceling* (usage contraction). So you must use *revenue* churn (cancellations + shrinking usage), not just logo churn (the % of customer accounts that cancel). Suppose 8 months of data show ~3%/mo logo churn, but usage contraction pushes net monthly *revenue* churn to somewhere between 3% and 8% depending on the cohort:
  - Optimistic (3%/mo revenue churn → ~33-month lifetime): LTV = $2,250 × 33 ≈ **$75K** → LTV:CAC = $75K ÷ $9K ≈ **8.3×**
  - Base (6%/mo → ~17-month lifetime): LTV ≈ **$37.5K** → LTV:CAC ≈ **4.2×**
  - Pessimistic (8%/mo → ~12.5-month lifetime): LTV ≈ **$28K** → LTV:CAC ≈ **3.1×**

  Even the pessimistic case clears Skok's 3× bar — that's the actual finding. And presenting it as "3–8× depending on how usage-contraction-adjusted churn settles, here's the cohort data" is *more* credible to investors than a single confident 8.3×. They know single-number LTV on 8 months of usage-based data is fiction (see the three ways naive LTV lies, above). **[Evergreen]** method; the practice of probing usage-based LTV with revenue churn is standard per [a16z's 16 Startup Metrics](https://a16z.com/16-startup-metrics/) (LTV must be margin- and churn-honest) and Skok's [SaaS Metrics 2.0](https://www.forentrepreneurs.com/saas-metrics-2/).
- Usage-based revenue isn't contractually recurring. If usage drops 40% in a downturn, payback stretches to 6.7 months, and your "ARR" (annualized run rate — last month's revenue × 12) was never guaranteed. Investors discount usage-based ARR vs. contracted ARR for exactly this reason. **[2026]** (More on this in Section 8 and in `03-pricing.md`.)
- Watch the *dispersion*: one power user processing 500K pages on a discounted plan can single-handedly wreck your blended margin. [Tanay Jaipuria notes](https://www.tanayj.com/p/the-gross-margin-debate-in-ai) that Anthropic initially lost tens of thousands of dollars per month on some $200/mo power users. Track margin per customer, not just the average. **[2026]**

---

## 3. Cohorts and retention curves — the best product-market fit (PMF) signal there is

A **cohort** is the group of customers who started in the same month. Instead of one blended churn number, you track: of the customers who signed up in January, what % were still active (or still paying) 1, 3, 6, 12 months later? Plot that and you get a **retention curve**.

**The one thing to look for: does the curve flatten?** A curve that decays toward zero means you have a leaky bucket and no durable business, regardless of top-line growth. A curve that drops and then goes *flat* means some set of users has made you a habit. That flat floor is your real business. **[Evergreen]**

Casey Winters (growth lead at Pinterest, ex-Grubhub), from the benchmark study he ran with Lenny Rachitsky: "Great retention is the scalable way to grow a product. It's the best indicator of product-market fit, it is the most important factor in a user's lifetime value, and high retention drives all of the best acquisition strategies." ([Lenny's Newsletter, "What Is Good Retention"](https://www.lennysnewsletter.com/p/what-is-good-retention-issue-29) — the surviving canonical writeup; Casey's original post on caseyaccidental.com has since gone offline). Why retention beats other PMF signals: growth can be bought and signups can be spiked, but nobody keeps using a product month after month unless it's actually working for them. (See `08-talking-to-users.md` for the qualitative side of the same question.)

Their benchmarks come from surveying ~20 senior growth practitioners (Pinterest, Slack, Dropbox, Grubhub, Twitter). The principle is **[Evergreen]**; the specific numbers are from the 2020 study but remain the standard reference cited in 2026:

**Six-month *user* retention** (% of new users still active at month 6):

| Category | Good | Great |
|---|---|---|
| Consumer social | ~25% | ~45% |
| Consumer transactional (e.g., e-commerce, delivery) | ~30% | ~50% |
| Consumer SaaS (e.g., a Spotify-like subscription) | ~40% | ~70% |
| SMB (small and mid-size business) / mid-market SaaS | ~60% | ~80% |
| Enterprise SaaS | ~70% | ~90% |

**Twelve-month *net revenue* retention** (revenue kept + expansion from a cohort after a year — defined precisely in Section 8):

| Category | Good | Great |
|---|---|---|
| Consumer SaaS | ~55% | ~80% |
| Land-and-expand SMB/mid-market SaaS (sell small to one team, then grow the account) | ~90% | ~110% |
| Bottom-up SaaS (individual users adopt, then teams pay) | ~100% | ~120% |
| Enterprise SaaS | ~110% | ~130% |

Note that enterprise's numbers exceed 100%: existing customers *grow*. This is the "negative churn" Skok describes, where expansion from remaining customers outweighs losses from churned ones. One 2026-specific caveat: AI products have shown unusually fast early churn, because buyers trial many tools at once. Kyle Poyar calls this [the "AI churn wave"](https://www.growthunhinged.com/p/the-ai-churn-wave). Investors now probe *month-2 and month-3* cohort retention on AI products especially hard. **[2026]**

Skok's floor, worth memorizing: monthly revenue churn above ~2% is danger territory. It compounds to losing roughly a quarter of your revenue every year, and "if this isn't right, the business isn't viable." **[Evergreen]**

---

## 4. Burn, runway, and default alive vs. default dead

- **Burn rate**: net cash out per month (Section 1).
- **Runway**: cash in bank ÷ net burn = months until zero. But this static version is misleading if revenue is growing — which is the entire point of Paul Graham's essay [Default Alive or Default Dead](https://paulgraham.com/aord.html) **[Evergreen]**:

> Assuming expenses stay constant and revenue growth continues at its current rate, do you reach profitability before the money runs out? If yes, you're **default alive**. If no, you're **default dead**.

Graham's alarming observation: "half the founders I talk to don't know whether they're default alive or default dead" — and the ones who don't know are almost always the ones in trouble. He points to Trevor Blackwell's calculator at [growth.tlb.org](http://growth.tlb.org) for the exact computation.

**Worked example.** Cash: $900K. Net burn: $60K/mo (expenses $90K, revenue $30K). Revenue growing 10%/mo.

- Static runway: $900K ÷ $60K = 15 months.
- Default alive check: with expenses flat at $90K, you need revenue ≥ $90K, i.e., 3× growth. At 10%/mo, that takes ln(3)/ln(1.1) ≈ 11.5 months. Cumulative cash burned before break-even ≈ $440K (the monthly gaps shrink: $60K, $57K, $53.7K, … summed over ~12 months: 12 × $90K − $30K × (1.1¹² − 1)/0.1 ≈ $1,080K − $641K ≈ $439K), well under the $900K in the bank. **Default alive.**
- Same company at 4%/mo growth: 3× takes ~28 months, and cumulative burn far exceeds $900K. **Default dead** — and the time to know that is *now*, not month 12. Graham calls the late discovery "the fatal pinch": default dead + slow growth + not enough time left to fix either.

Two of Graham's points that will save you real money **[Evergreen]**:
1. **Spending doesn't buy growth.** "There is surprisingly little connection between how much a startup spends and how fast it grows." Growth comes from product-market fit. Heavy spend usually reflects an expensive product to build, or plain waste.
2. **Over-hiring is "by far the biggest killer of startups that raise money."** Founders hire because it feels like what funded startups do. Airbnb — one of the fastest-growing companies Y Combinator (YC, the startup accelerator Graham co-founded) had seen — waited 4 months after raising money before hiring anyone. Your product needs to *evolve*, and small teams evolve products faster.

A related metric investors quote constantly in 2026: the **burn multiple** = net burn ÷ net new ARR added in the same period (David Sacks' formulation). Burning $200K/mo to add $100K/mo of new ARR annualized = burn multiple of 2. Under ~1.5 is considered good and under 1 exceptional at early stage; over 3 signals trouble. Bessemer's version, [efficiency score = net new ARR ÷ net burn](https://www.bvp.com/atlas/cloud-computing-metrics), is the same ratio inverted (>1.5× best). **[2026]**

---

## 5. How much to pay yourself

**[Evergreen]** principle: pay yourself enough that personal financial stress doesn't distort company decisions, and little enough that it visibly signals the money goes into the company. Investors read founder salary as an alignment signal. A market-rate salary pre-revenue is a red flag — but so is a $0 salary that forces you to quit in month 14.

**[2026]** numbers, from [Kruze Consulting's payroll data across 450+ VC-backed startups](https://kruzeconsulting.com/blog/startup-ceo-salary-report/) (VC = venture capital): average seed-stage CEO salary rose from ~$132K (2024) to ~$147K (2025) to ~$153K (2026); Series A averages ~$203K. A common rule of thumb: a $2M+ seed round supports roughly **$130K–$170K** for a founder-CEO — in NYC or SF, that's "comfortable, not accumulating." Pre-seed/bootstrapped founders typically take much less ($0–$80K). Set it with your co-founder explicitly, and revisit at each raise; see `05-fundraising.md` for how this interacts with the board.

---

## 6. What seed money is actually spent on: headcount math

Seed money is overwhelmingly spent on **people** — typically 70–80% of burn. The number that matters is **fully-loaded cost**: what an employee actually costs you, not their salary. **[Evergreen]** principle; **[2026]** numbers:

Fully loaded = base salary × roughly **1.25–1.4×**. That covers employer payroll taxes (~10%), health insurance (per [KFF's 2025 Employer Health Benefits Survey](https://www.kff.org/health-costs/report/2025-employer-health-benefits-survey/), the employer's share of the premium averages **~$7.9K/year for single coverage and ~$20.1K for family coverage** — so budget roughly $8K–$20K per employee depending on who's covering a family), 401(k) match, equipment, software seats, and workspace ([Kruze](https://kruzeconsulting.com/blog/startup-payroll-costs/), [data derived from the BLS](https://www.glencoyne.com/guides/fully-loaded-cost-us-employee) — the Bureau of Labor Statistics). Concretely: a **$140K engineer costs ~$187K/year ≈ $15.6K/month**; a senior NYC/SF engineer at $180–200K base costs **$230–270K/year** fully loaded.

**Worked seed budget.** You raise $3M. Team: 2 founders at $150K ($200K loaded each) + 3 engineers at $170K (~$225K loaded each) = $1.075M/year ≈ **$90K/mo in payroll**. Add ~$25K/mo for infra/inference, tools, legal, accounting, insurance, and space → **$115K/mo gross burn** → 26 months of runway at zero revenue. That's the standard shape: a seed round buys a team of ~5–7 people about two years to find product-market fit. Every additional hire at ~$19K/mo costs ~$228K/year. At this company's $115K/mo burn, that's roughly *two months of total company runway per year they're employed* — which is why Graham's over-hiring warning is arithmetic, not ideology.

---

## 7. Margin structure: pure software vs. AI-inference-heavy — and what it does to valuation

**[Evergreen]** principle: gross margin determines how much of each revenue dollar can fund growth, and therefore what a revenue dollar is *worth*. Public-market investors pay a multiple of revenue that depends heavily on gross margin, and that logic flows all the way down to your seed valuation.

**[2026]** landscape:
- **Pure software**: 80–90% gross margins — the historical SaaS norm.
- **AI-native applications**: wildly dispersed. Per [Bessemer's State of AI 2025](https://www.bvp.com/atlas/the-state-of-ai-2025) data (analyzed in [Tanay Jaipuria's gross-margin post](https://www.tanayj.com/p/the-gross-margin-debate-in-ai)): fast-growing AI "Supernovas" average **~25%** gross margin early (some negative); steadier "Shooting Stars" trend toward **~60%**. Model providers themselves run ~50% (OpenAI) to ~60% (Anthropic), excluding training costs. Bessemer pegs AI-native margins broadly at **50–60%**. ICONIQ's survey of ~300 software executives found AI products averaging **~45% in 2025, projected ~52% in 2026** (via [Growth Unhinged's coverage](https://www.growthunhinged.com/)).
- Consequence: [The SaaS CFO estimates](https://www.thesaascfo.com/how-to-calculate-the-inference-efficiency-ratio/) an AI company needs roughly **6× the revenue** of a traditional SaaS company to produce the same EBITDA (earnings before interest, taxes, depreciation, and amortization — roughly, operating cash profit). All else equal, low-margin revenue gets a lower multiple — though in 2026's AI funding frenzy, growth rate is often overriding margin at seed (see `10-ai-era.md` for whether that lasts).

Why smart people are still optimistic about AI margins, per Jaipuria: inference costs for a fixed capability level have been falling 80–90% per year; products can route easy tasks to cheap models; and AI apps are layering on non-inference revenue (Replit and Bolt monetize hosting, storage, deployments). Replit is the cautionary tale about how *volatile* this all is. Per The Information's reporting (cited in Jaipuria's post), its gross margin went from **9.8%** (Aug 2024, $2M ARR) to **36.1%** (Dec 2024, $16.1M ARR) via pricing changes — then fell back to **~23%** by July 2025 at $144M ARR. And Replit never even had it worst: Jaipuria notes from the same Bessemer dataset that "many of the AI Supernovas have *negative* gross margins, something we don't tend to see often in software" — i.e., some of the fastest-growing AI companies lose money on every marginal dollar of usage. The lesson isn't "margins improve on a clean arc." It's that inference-heavy margins whipsaw with pricing and model choices, and one snapshot tells you little. The counterweights: users keep demanding the newest frontier model (whose price stays high), and power users blow up fixed-price plans. Jaipuria's advice to founders: "The goal is not a perfect gross margin in isolation. The target is a healthy net margin profile as cohorts mature." Design pricing so margin *improves* with scale — that's a `03-pricing.md` problem as much as a cost problem.

---

## 8. Revenue quality: recurring vs. one-time, GRR and NRR

Not all revenue dollars are equal. **[Evergreen]** hierarchy, best to worst: contracted recurring (subscriptions) > usage-based with strong retention > repeat-transactional > one-time (services, implementation fees). The reason is evergreen: recurring revenue is a machine that runs next year without being resold, so a dollar of it is worth a multiple of a dollar that must be re-earned. The canonical explanation is Bill Gurley's [All Revenue Is Not Created Equal: The Keys to the 10X Revenue Club](https://abovethecrowd.com/2011/05/24/all-revenue-is-not-created-equal-the-keys-to-the-10x-revenue-club/), which showed public internet companies trading anywhere from ~0.2× to ~21.7× revenue based on exactly these quality factors (recurring/predictable revenue, high margins, low churn, network effects). The *specific* spread is market-dependent: **[2026]** the [SaaS Capital Index](https://www.saas-capital.com/the-saas-capital-index/) tracks the live median run-rate-revenue multiple for public SaaS. In recent years it has sat in the mid-to-high single digits (down from a ~16× peak in the 2021 bubble), with the best names well above 10×, while services-like one-time revenue fetches on the order of ~1×. The gap widens in bull markets and compresses in downturns, so check the current index before quoting a multiple to anyone. Strip one-time fees out of your ARR — a16z flags padding MRR with non-recurring fees as a classic credibility-killer.

The two retention metrics every investor will ask for, with math. Take the customers who were paying you a year ago — say $100K/mo combined:

- **GRR (gross revenue retention)** = (starting revenue − churn − downgrades) ÷ starting revenue. *Expansion doesn't count.* If you lost $8K to cancellations and $2K to downgrades: GRR = ($100K − $10K)/$100K = **90%**. GRR ≤ 100% by definition; it measures how leaky the bucket is.
- **NRR (net revenue retention)** = (starting revenue − churn − downgrades + expansion) ÷ starting revenue. Same cohort also expanded by $18K: NRR = ($100K − $10K + $18K)/$100K = **108%**. NRR > 100% means you'd grow without signing a single new customer.

Benchmarks **[2026]**: good B2B (business-to-business — selling to companies) SaaS shows GRR ≥ 90% (enterprise ≥ 95%) and NRR 100–120%+ (see the Lenny/Casey table in Section 3; Series A AI investors commonly cite [NRR > 120% as the bar](https://valueaddvc.com/blog/what-series-a-investors-are-looking-for-in-ai-startups-in-2026)). NRR can mask disaster: 115% NRR with 75% GRR means one **whale** (investor slang for a single outsized customer who dwarfs the rest — the term comes from casinos' biggest gamblers) is expanding while everyone else flees. Report both.

---

## 9. What investors actually ask for at seed and Series A in 2026

**[2026]** — this section will age fastest. Treat it as a snapshot and re-verify before you raise (process in `05-fundraising.md`, investor landscape in `06-investors-and-accelerators.md`).

**At seed** (your first substantial funding round), the honest answer is that metrics are secondary to team, market, and early evidence of pull — many 2026 AI seeds close pre-revenue. But you should still know what "good" looks like where numbers exist, per the [pitchwise 2026 guide](https://www.pitchwise.se/blog/the-complete-guide-to-seed-and-series-funding-rounds-for-founders-in-2026) and the sources below:

| Metric | 2026 seed expectation |
|---|---|
| ARR | Often $0 (pre-revenue is common, especially AI); where revenue exists, **$300K–$500K ARR** is the commonly cited band |
| Growth | No hard bar — investors want *evidence of pull*: a waitlist, usage growing week over week, unsolicited inbound |
| Retention | A *signal*, not a benchmark: early cohort curves that flatten rather than decay; for AI products, month-2/3 retention (Section 3) |
| Gross margin | Know it cold, especially if AI-inference-heavy — you'll be asked how it improves with scale |
| Unit economics | A credible *story* (CAC channel, rough payback logic), not proven numbers |
| Burn / runway | Know your net burn and months of runway to the dollar; hesitation here is the red flag |

What you *will* be asked regardless of revenue: burn, runway, gross margin (especially if AI-heavy), and early cohort behavior of whatever usage you have.

**At Series A** (the next round after seed), metrics become the conversation. [Tomasz Tunguz notes](https://tomtunguz.com/categories/fundraising) that the old "$1M ARR = Series A" rule has dissolved into enormous variance — some companies raise at $0.5–1M ARR with 100–150% year-over-year (YoY) growth, others at $3M+ with 500% YoY growth. The 2026 consensus band, synthesized from [CRV](https://www.crv.com/content/series-a-metrics-vcs-expect), [Value Add VC](https://valueaddvc.com/blog/what-series-a-investors-are-looking-for-in-ai-startups-in-2026), and market surveys:

| Metric | 2026 Series A expectation (AI/SaaS) |
|---|---|
| ARR | $1–3M typical; $3–5M median for hot AI deals |
| Growth | 10–15%+ month-over-month (strong candidates >15%) |
| NRR | >110%, AI deals often >120% |
| GRR | ≥85–90% |
| Gross margin | Trending above 60% for AI-native (pure SaaS: 75%+) |
| CAC payback | <12–18 months |
| Burn multiple | <2, ideally <1.5 |
| Runway at raise | 12+ months remaining (raise *before* you're desperate) |

Context: the funnel is brutal. Seed rounds fell 28% YoY in Q1 2025, and a large majority of seeded startups never raise an A ([scaleup.finance](https://www.scaleup.finance/article/the-series-a-crunch-is-back-why-85-of-seed-stage-startups-now-fail-to-raise-series-a-and-how-to-beat-the-odds) claims ~85%; the exact figure varies by source and cohort, but "most" is directionally right). Meanwhile, AI Series A rounds that *do* happen are large — median ~$13–15M at $75M+ post-money (the company's valuation immediately *after* the new money is added; defined fully in `05-fundraising.md`) per 2026 market surveys. It's a barbell market: winners overfunded, everyone else squeezed.

**[Evergreen]** meta-rule from Bessemer's good/better/best framing and a16z's "order of operations": investors read metrics in sequence — size (ARR), then growth, then quality (retention/margin), then efficiency (payback/burn multiple). Prepare your numbers in that order and know each one cold. Hesitating on your own churn number is worse than the churn number itself.

---

## 10. A financial model skeleton you can build in a spreadsheet

You don't need a banker's model. One tab, months as columns (18–24 of them), these rows. **[Evergreen]**

**Revenue block**
1. `New customers` — your assumption; tie it to a driver (e.g., signups × conversion %)
2. `Churned customers` = prior-month customers × monthly churn %
3. `Total customers` = prior month + row 1 − row 2
4. `ARPA` ($/customer/mo; grow it slowly if you expect expansion)
5. `MRR` = row 3 × row 4  (for usage-based: `usage units × price/unit` instead)
6. `ARR` = MRR × 12

**Cost block**
7. `COGS` = MRR × COGS % (model 15% for pure SaaS; 40–50% if inference-heavy — and add a row for `inference cost/unit` so you can test what a 50% price cut from your model provider does)
8. `Gross profit` = 5 − 7; `Gross margin %` = 8 ÷ 5
9. `Headcount` (integer per month — your hiring plan lives here)
10. `Payroll` = row 9 × fully-loaded cost (~$16–19K/mo per head, Section 6)
11. `Other opex` = fixed $ (tools, rent, legal) + `S&M spend` (S&M = sales & marketing; it drives row 1 — link them: new customers = S&M ÷ CAC)

**Cash block**
12. `Net burn` = 8 − 10 − 11 (negative = burning)
13. `Cash` = prior-month cash + row 12
14. `Runway (months)` = row 13 ÷ current burn — **and** a `default alive?` flag: does row 12 turn positive before row 13 hits zero?

**Output block (the metrics from this doc, computed live)**
15. `CAC` = S&M ÷ new customers; `Payback` = CAC ÷ (ARPA × gross margin %); `Burn multiple` = net burn ÷ net new ARR; `NRR/GRR` once you have 12 months of cohorts.

Then make three copies of the assumptions: conservative / base / optimistic. The model's job is not prediction. Its job is to show you, before reality does, which assumption kills you first. Revisit it monthly against actuals — the *variance* between model and reality is where you learn.

---

## The five-line summary

1. **Gross margin is destiny**: it sets what a revenue dollar is worth, and AI inference costs have made it a live issue again. [Evergreen principle, 2026 numbers]
2. **Retention is the truest PMF signal** — a flattening cohort curve beats any growth chart. [Evergreen]
3. **Know if you're default alive** — most founders don't, and the calculation takes five minutes. [Evergreen]
4. **People are the burn** — every hire at ~$19K/mo fully loaded is runway you're spending; over-hiring is the top killer of funded startups. [Evergreen]
5. **Investors read: size → growth → quality → efficiency.** Know your ARR, growth rate, NRR/GRR, margin, CAC payback, and burn multiple cold. [Evergreen framework, 2026 benchmarks]

---

## Sources

- Paul Graham, [Default Alive or Default Dead?](https://paulgraham.com/aord.html)
- David Skok, [SaaS Metrics 2.0](https://www.forentrepreneurs.com/saas-metrics-2/) (For Entrepreneurs)
- Jeff Jordan et al., [16 Startup Metrics](https://a16z.com/16-startup-metrics/) (a16z)
- Casey Winters & Lenny Rachitsky, [What Is Good Retention: An Exhaustive Benchmark Study](https://www.lennysnewsletter.com/p/what-is-good-retention-issue-29) (Lenny's Newsletter; Casey's original caseyaccidental.com post is no longer online)
- Bill Gurley, [All Revenue Is Not Created Equal: The Keys to the 10X Revenue Club](https://abovethecrowd.com/2011/05/24/all-revenue-is-not-created-equal-the-keys-to-the-10x-revenue-club/) (Above the Crowd)
- SaaS Capital, [The SaaS Capital Index](https://www.saas-capital.com/the-saas-capital-index/) (live median public-SaaS revenue multiples)
- Bessemer Venture Partners, [The five accounting metrics for cloud companies / Good-Better-Best benchmarks](https://www.bvp.com/atlas/cloud-computing-metrics), [Cloud 100 Benchmarks Report](https://www.bvp.com/atlas/the-cloud-100-benchmarks-report), and [The State of AI 2025](https://www.bvp.com/atlas/the-state-of-ai-2025) (source of the Supernovas/Shooting Stars margin data)
- Tanay Jaipuria, [The Gross Margin Debate in AI](https://www.tanayj.com/p/the-gross-margin-debate-in-ai) (discusses Bessemer's State of AI 2025 data and The Information's Replit margin reporting)
- Kyle Poyar, [Growth Unhinged](https://www.growthunhinged.com/) — incl. [The AI Churn Wave](https://www.growthunhinged.com/p/the-ai-churn-wave) and AI pricing/margin benchmarks
- The SaaS CFO, [How to Calculate the Inference Efficiency Ratio](https://www.thesaascfo.com/how-to-calculate-the-inference-efficiency-ratio/)
- Tomasz Tunguz, [Fundraising posts](https://tomtunguz.com/categories/fundraising) incl. [Benchmarking Exceptional Series A SaaS Companies](https://tomtunguz.com/benchmarking-exceptional-series-a-companies/)
- Kruze Consulting, [Startup CEO Salary Report 2026](https://kruzeconsulting.com/blog/startup-ceo-salary-report/) and [Startup Payroll Costs](https://kruzeconsulting.com/blog/startup-payroll-costs/)
- Glencoyne, [Fully Loaded Cost of a US Employee](https://www.glencoyne.com/guides/fully-loaded-cost-us-employee)
- KFF, [2025 Employer Health Benefits Survey](https://www.kff.org/health-costs/report/2025-employer-health-benefits-survey/) (employer share of health-insurance premiums)
- CRV, [Series A Metrics VCs Expect in 2026](https://www.crv.com/content/series-a-metrics-vcs-expect); Value Add VC, [Series A AI Startup Requirements 2026](https://valueaddvc.com/blog/what-series-a-investors-are-looking-for-in-ai-startups-in-2026); Pitchwise, [Guide to Funding Rounds 2026](https://www.pitchwise.se/blog/the-complete-guide-to-seed-and-series-funding-rounds-for-founders-in-2026); ScaleUp Finance, [The Series A Crunch](https://www.scaleup.finance/article/the-series-a-crunch-is-back-why-85-of-seed-stage-startups-now-fail-to-raise-series-a-and-how-to-beat-the-odds)
