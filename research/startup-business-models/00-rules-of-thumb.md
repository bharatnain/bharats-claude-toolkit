# The Rules of Thumb — the insider heuristics glossary

**Why this matters to you:** When your friends who "made it" sat in pitch meetings, both sides of the table were running a shared set of mental shortcuts — about market size, growth rate, spending, ownership — that nobody ever wrote down in one place for outsiders. Investors will judge your idea against these heuristics whether or not you know they exist. Founders who don't know them either get filtered out early or sign bad deals without realizing it. This document is the decoder ring. It covers every rule of thumb the ecosystem actually uses: what the math really is, who coined it, and — just as important — when the smartest people in the industry say to ignore it. Read it once now, then come back to individual rules as they become relevant. Everything here is tagged **[Evergreen]** (has been true for decades and will stay true) or **[2026]** (current-era numbers or AI-driven norms that may shift).

A note on scope: this doc defines the rules and their math. Deep dives on applying them live elsewhere in this library — unit economics in `04-unit-economics.md`, pricing in `03-pricing.md`, the fundraising process in `05-fundraising.md`, and the AI-era rewrites of these rules in `10-ai-era.md`.

---

## Part 1: Market size — TAM, SAM, SOM

### 1. TAM / SAM / SOM **[Evergreen]**

**Plain words.** Three nested estimates of how big your market is:

- **TAM (Total Addressable Market):** total annual revenue if literally every possible customer in the world bought your product. The theoretical ceiling.
- **SAM (Serviceable Addressable Market):** the slice of TAM you could actually serve, given your product, geography, language, regulatory reach, and sales model.
- **SOM (Serviceable Obtainable Market):** the slice of SAM you could realistically win in the next few years, given competition and your resources. This is the only one of the three that resembles a revenue forecast.

**The two ways it's actually calculated.**

- **Top-down:** start from an analyst's market number and slice it. "Gartner says practice-management software is a $5B market; dental is 20% of that, so our TAM is $1B." Fast — and investors distrust it, because you're multiplying someone else's guess by your own guesses.
- **Bottom-up:** count customers and multiply by what each will pay: `TAM = (number of potential customers) × (annual revenue per customer)`. Paul Graham states it exactly this way in [How to Convince Investors](https://paulgraham.com/convince.html): the TAM "of your company is $xy," where x is customer count and y is average annual revenue per customer. Investors strongly prefer bottom-up because every input is checkable.

**Worked example.** Say you build an AI phone receptionist for dental offices at $500/month, or $6,000/year. (This is a hypothetical product with hypothetical numbers, for arithmetic only.)

- **TAM (bottom-up):** roughly 180,000 dental practices in the US × $6,000/yr = **$1.08B** US TAM. Add Canada/UK/Australia and you might claim ~$1.5B.
- **SAM:** you only integrate with the two biggest practice-management systems, covering ~60% of practices, and only sell in the US: 108,000 practices × $6,000 = **$648M**.
- **SOM:** you believe you can win 3% of your SAM in 5 years: ~3,240 practices × $6,000 = **~$19M ARR**. (ARR = Annual Recurring Revenue: the annualized value of your subscription revenue. It is the standard yardstick for software startups.)

That last number — not the billion — is what a serious investor will pressure-test.

**Where it comes from.** TAM/SAM/SOM is decades-old market-research vocabulary with no single coiner. It was imported into startup pitching in the 2000s and is now a mandatory slide in nearly every deck.

**When legends say to ignore it.** This is the rule with the loudest "ignore it" chorus. Know the arguments verbatim — they're the escape hatch when your honest TAM is small:

- Paul Graham, in [How to Convince Investors](https://paulgraham.com/convince.html): "the market doesn't have to be big yet... it's often better to start in a small market that will either turn into a big one or from which you can move into a big one." His example: Microsoft started in the microscopic market of Altair BASIC interpreters but was "perfectly poised to expand up the stack of microcomputer software as microcomputers grew powerful enough."
- A line widely repeated in the ecosystem holds that the most interesting companies start with a TAM of nearly zero. It is usually attributed to Sam Altman, former president of Y Combinator (YC — the best-known startup accelerator, a program that funds and coaches early-stage startups in batches). Honesty note: I could not find a primary source for that exact sentence, so treat it as folklore with a famous name attached, not a citation. The example underneath it is real and documented, though: Airbnb launched in 2008 as "AirBed & Breakfast," literally renting air mattresses on the founders' San Francisco apartment floor — a market whose honest TAM at the time rounded to zero, attached to a company now worth tens of billions.
- Peter Thiel, *Zero to One*: deliberately pick a market small enough to monopolize, then expand in concentric circles — "always err on the side of starting too small." His example: PayPal ignored the millions of general internet users and targeted eBay's high-volume "PowerSellers" — about 20,000 people. (Note: Thiel never uses the term "TAM" in the book. The monopoly-first framing is his; the TAM vocabulary is the ecosystem's.)

The synthesis every insider knows: **the TAM slide is a story about where the market is going, not a spreadsheet about where it is.** Investors know the numbers are soft. What they're really testing is whether you have a credible narrative from a small wedge (the narrow first market you enter) to a huge market, plus a "why now" (see `01-idea-evaluation.md`).

### 2. The venture-scale threshold: "$1B+ TAM" **[Evergreen]** (principle) / current thresholds **[2026]**

**Plain words.** VCs (venture capitalists — investors who buy minority stakes in startups using pooled funds) will generally only invest if your market could plausibly support a company worth $1B+. In practice that means claiming a TAM of $1B minimum. Top firms increasingly want $5–10B claimed at seed or Series A — the early funding stages; Rule 4 decodes the full ladder ([SheetVenture](https://sheetventure.com/fundraising-knowledge/how-do-investors-think-about-market-size), [Practical Founders](https://practicalfounders.com/articles/venture-scale-means-big-vcs-require-billion-dollar-exit-potential/)).

**Where the number comes from — the actual math.** It's not arbitrary; it falls straight out of fund economics. A rough rule embedded in the folklore: a software company is typically valued at some multiple of revenue — historically ~10x ARR for fast growers. (This multiple swings with markets — **[2026]** it's lower for ordinary SaaS, higher for hot AI companies.) So a $1B company ≈ $100M ARR. Now ask what makes $100M ARR believable: capturing 10% of a $1B market is heroic; capturing 1% of a $10B market is merely hard. That's why founders inflate TAM claims to $10B: **the bigger the claimed TAM, the smaller and more believable the required market share.** The deeper "why" is power-law fund math — Rule 3, next. If venture scale isn't for you, that's a legitimate choice (see [Lenny Rachitsky's "Your startup idea probably isn't venture-scale"](https://www.lennysnewsletter.com/p/your-startup-idea-probably-isnt-venture)) — but then don't pitch VCs; see `02-business-models.md`.

### 3. Power-law fund math — why your investor needs you to be huge **[Evergreen]**

**Plain words.** Startup outcomes follow a power law: a tiny number of companies produce nearly all the returns. Paul Graham documented this from inside YC in [Black Swan Farming](https://paulgraham.com/swan.html) (2012). Just two companies — Dropbox and Airbnb — accounted for about **75% of YC's ~$10B portfolio value** at the time. "Only one company per batch" moved YC's returns at all; the rest were "just a cost of doing business." He calls it "1000x variation in outcomes."

**The worked fund example.** A VC raises a **$100M fund** from LPs (limited partners — the pensions, endowments, and rich families whose money the VC invests). VC money is locked up ~10 years and most startups die, so LPs expect roughly **3x gross** back: $300M.

- The fund backs ~30 companies.
- Historical base rates: 50–70% return roughly nothing; a handful return 1–5x; maybe one or two go huge.
- Suppose the VC owns ~10% of each company at exit — the moment investors can finally sell, via acquisition or IPO — after dilution (dilution = your stake shrinking as later investors buy in; Rule 17). If one company must effectively return the whole fund (a "fund-returner" — real insider vocabulary), that one stake must be worth $100M+. So that company must exit at **$1B+**. To hit $300M total, the portfolio needs one $1B+ outcome plus several meaningful smaller wins — or, ideally, one $3B+ monster.

**What this means for you.** When a partner asks "how big can this get?", they are not making conversation. They are checking whether your ceiling, times their ownership, can return their fund. A business that will *certainly* be worth $50M is a *worse* VC investment than one with a 5% chance of being worth $5B. Graham's corollary in Black Swan Farming: the best ideas look bad at first ("Facebook... seemed like a site for college students to waste time"), so investors who only fund safe-looking ideas systematically miss the winners — and even YC, knowing this, admits it's "too conservative." Understand this math, and half of investor behavior — fast passes, "come back when you're bigger," obsession with ambition — stops being mysterious. More in `05-fundraising.md` and `06-investors-accelerators.md`.

### 4. The obtainable-market convention: ~1–5% of SAM **[Evergreen]**

**Plain words.** When projecting your SOM or your 5-year revenue, claiming you'll capture **1–5% of your SAM** is the conventional "credible" range. Below 1% signals a business too small to matter; above ~10% signals naivety about competition (unless you have monopoly dynamics). In the dental example above: 3% of a $648M SAM ≈ $19M ARR — a fundable Series B trajectory story, told without claiming you'll conquer dentistry.

(First use of the round ladder, so a quick decoder: startups raise money in named stages. **Pre-seed** and **seed** are the first small rounds, raised on team and early evidence. **Series A, B, C…** are the successively larger "priced" rounds that follow, each requiring more proof — the letters are literally just the sequence of share classes sold. So "a Series B trajectory" means "growth that would justify the third or fourth major round." Rule 18 gives the traction bar for each stage; mechanics live in `05-fundraising.md`.)

**When to ignore it.** Thiel argues the opposite for wedge markets: in a market you've defined narrowly enough, target **monopoly** (50–100% share), not 3%. "1% of a huge market" is precisely the framing he mocks in *Zero to One*. Use 1–5% for the big-TAM slide; use monopoly logic for your actual first market.

---

## Part 2: Growth — the defining metric

### 5. Startup = Growth: 5–7% per week **[Evergreen]**

**Plain words.** Paul Graham's [Startup = Growth](https://paulgraham.com/growth.html) (2012) is the closest thing to a founding document for the modern definition: "a startup is a company designed to grow fast." Not tech, not funding — growth. His YC-era benchmarks for weekly growth in revenue (or active users, if pre-revenue): **1%/week = something's wrong; 5–7%/week = good; 10%/week = exceptional.**

**The math.** Growth compounds: 5%/week = 1.05^52 ≈ **12.6x per year**; 1%/week ≈ 1.7x per year. That gap — 12.6x vs 1.7x — is the entire difference between a startup and a small business. It's why YC partners ask about growth rate (a ratio), not absolute numbers, every week. Graham's operating advice: pick a growth target and treat it as a compass — "anything that gets you the growth you need is ipso facto right."

**When to ignore it.** These rates apply to tiny early-stage companies. Growing 7% weekly from $400/week is achievable; from $10M ARR it is not. Also, growth-at-all-costs got repriced after 2021 — the modern investor question is growth *at what burn*, meaning how much cash you lose per month to get it (Rules 8–9). **[2026]**

### 6. T2D3 — triple, triple, double, double, double **[Evergreen]** (path) / exact bar **[2026]**

**Plain words.** First, the most load-bearing piece of jargon in the whole ecosystem: **product-market fit (PMF)**. PMF is the point where a product demonstrably satisfies a real market demand: customers pull it out of your hands, retention holds, and the constraint flips from "does anyone want this?" to "can we build and sell it fast enough?" The term comes from Marc Andreessen's 2007 essay [The Only Thing That Matters](https://pmarchive.com/guide_to_startups_part4.html): "Product/market fit means being in a good market with a product that can satisfy that market." You'll see it abbreviated PMF everywhere, including below.

T2D3 is the canonical *post*-PMF growth curve for B2B SaaS — business-to-business software sold as a subscription (SaaS = Software as a Service). **Neeraj Agrawal of Battery Ventures** coined it in a 2015 essay ([The SaaS Adventure](https://www.battery.com/blog/helping-entrepreneurs-triple-triple-double-double-double-to-a-billion-dollar-company/), originally on TechCrunch): once you reach ~$2M ARR, triple annual revenue twice, then double it three times.

**Worked example.** $2M → **$6M** (T) → **$18M** (T) → **$36M** (D) → **$72M** (D) → **$144M** (D). Five years from $2M to ~$100M+ ARR, which at ~10x revenue ≈ a $1B+ company — the unicorn track. (**Unicorn** = a private startup valued at $1B or more. Venture investor Aileen Lee coined the term in her 2013 TechCrunch essay [Welcome to the Unicorn Club](https://techcrunch.com/2013/11/02/welcome-to-the-unicorn-club/) because billion-dollar startups were then rare enough to feel mythical. The word stuck even as the club grew crowded.) Salesforce, NetSuite, and Zendesk roughly traced it.

**When to ignore it.** T2D3 was always describing the ~top-1% outcome, not the median. **[2026]** twist: the best AI-native companies have blown past T2D3 (some going $0→$100M ARR in 2–3 years), which has *raised* the perceived bar in AI — while the median SaaS company grows far slower than T2D3. Know which comparison set you're in. Fast AI revenue also gets discounted for **churn** risk. Churn simply means customers canceling; it's the leak in every recurring-revenue bucket, and it drives Rules 10, 11, and 15 below (see also Rule 13 and `10-ai-era.md`).

---

## Part 3: Efficiency — the burn-and-return rules

### 7. Rule of 40 **[Evergreen]**

**Plain words.** A healthy software company's **revenue growth rate (%) + profit margin (%) should sum to ≥ 40**. This lets a fast grower lose money and a slow grower be judged fairly: growing 100% and burning 40% of revenue (sum 60) is healthy; growing 10% at breakeven (sum 10) is not.

**Worked example.** Growing 60% YoY (year-over-year — this year's revenue vs. the same period a year ago) with a −15% free-cash-flow margin: 60 + (−15) = **45**. Passes. (**Free cash flow** = the actual cash a business generates or burns after paying all its operating costs and investments — the plainest measure of "is money piling up or draining away." An FCF margin of −15% means the company burns cash equal to 15% of its revenue. The "profit margin" leg of the rule is computed several ways — operating margin, EBITDA margin (EBITDA = earnings before interest, taxes, depreciation, and amortization, a rough measure of operating profit), or FCF margin — so always ask which one someone is using.)

**Where it comes from.** Popularized by **Brad Feld** in 2015 ([The Rule of 40% For a Healthy SaaS Company](https://feld.com/archives/2015/02/rule-40-healthy-saas-company/)). He heard it from a late-stage investor at a board meeting and called 40% "the minimum point of happiness." Top-quartile public SaaS scores 50+ ([Wall Street Prep](https://www.wallstreetprep.com/knowledge/rule-of-40/)).

**When to ignore it.** Feld himself: it's for companies **at scale — "assume at least $50 million in revenue."** Applying Rule of 40 to your seed-stage startup is a category error; his own advice was T2D3 first, Rule of 40 later. It reappears at Series C+ and in acquisition talks.

### 8. Burn multiple **[Evergreen]** (metric) / current bar **[2026]**

**Plain words.** How many dollars you burn to buy each dollar of new ARR. Coined by **David Sacks** (founder of Yammer, later Craft Ventures) in [The Burn Multiple](https://sacks.substack.com/p/the-burn-multiple-51a7e43cb200) (2020). It is now arguably *the* headline efficiency metric.

**The math.** `Burn Multiple = Net Burn ÷ Net New ARR`. **Net burn** = cash going out minus cash coming in over the period — spending after subtracting revenue collected. ("Gross burn" is total spending ignoring revenue; investors care about net.) Worked example: you burned $6M last year and grew ARR from $2M to $5M (net new ARR = $3M). Burn multiple = 6/3 = **2.0x** — you paid $2 for every $1 of new recurring revenue.

**Sacks' benchmarks.** The table everyone quotes as "the Sacks table" — under 1x amazing; 1–1.5x great; 1.5–2x good; 2–3x suspect; 3x+ bad — comes from a graphic in the essay and is reproduced all over the ecosystem. But the essay's retrievable *prose* anchors are softer and stage-aware: it calls a 2x burn multiple "reasonable for an early-stage startup," calls 5x "terrible," and expects the multiple to improve with stage (roughly: ~3x tolerable at seed, ~2x at Series A, trending toward efficient by Series B+). So read the famous table as the *at-scale* grading curve, not a seed-stage one. Why Sacks likes the metric: "The beauty of the Burn Multiple is that it's a catch-all metric. Any serious problem will eventually impact the Burn Multiple by either increasing burn, decreasing net new ARR, or (most tricky) increasing both but at disproportionate rates." His best line, worth memorizing: "A startup that over-burns is effectively claiming that its sales will be spring-loaded" — wasteful spending is an implicit promise of future efficiency that rarely arrives. Bessemer's Cloud 100 data backs the market's verdict: efficient companies (burn multiple <1x, Rule of 40 ≥40) traded at ~2.3x the revenue multiples of inefficient peers ([Bessemer Cloud 100 Benchmarks Report](https://www.bvp.com/atlas/the-cloud-100-benchmarks-report)). **[2026]** stage-specific bars circulating in the ecosystem: ≤1.2x by Series A, ≤1.4x at growth stage ([Scale VP](https://www.scalevp.com/blog/benchmarking-saas-growth-and-burn)).

**When to ignore it.** Pre-PMF (Rule 6), when net new ARR ≈ 0, the ratio is meaningless — Sacks aimed it at venture-stage companies. And a company briefly over-burning to seize a genuine land grab (the 2023–24 AI application window, arguably) can rationally accept an ugly burn multiple for a few quarters — if it says so out loud and has a date when it stops.

### 9. Magic number **[Evergreen]**

**Plain words.** Sales efficiency: annualized new revenue per dollar of prior-quarter sales & marketing (S&M) spend. Coined ~2008 by **Lars Leckie** (Hummer Winblad), building on an observation by Rory O'Driscoll of Scale ([The SaaS CFO](https://www.thesaascfo.com/calculate-saas-magic-number/)).

**The math.** `Magic Number = (this quarter's revenue − last quarter's revenue) × 4 ÷ last quarter's S&M spend`. Worked example: quarterly revenue rose $250K (×4 = $1M annualized) on $1.2M of prior-quarter S&M → magic number **0.83**. Leckie's threshold, in his words: "if you are below 0.75 then step back and look at your business, if you are above 0.75 then start pouring on the gas." Above 0.75, your sales machine converts money into growth well enough to justify scaling spend.

**When legends say to ignore it.** Four standard caveats, all of which practitioners (including [The SaaS CFO's treatment](https://www.thesaascfo.com/calculate-saas-magic-number/) of the metric's variants) flag:

- **It's margin-blind.** The formula uses revenue, not gross profit (revenue minus the direct costs of serving customers). A 0.9 magic number at a 55% AI gross margin buys far less actual profit than the same 0.9 at 80% (Rule 16); sophisticated operators compute a gross-margin-adjusted version.
- **The one-quarter lag is a guess.** The formula assumes last quarter's S&M spend caused this quarter's revenue. For enterprise products with 6–12-month sales cycles, that attribution is simply wrong — lengthen the lag or the number is fiction.
- **It's retention-blind.** It counts new revenue landing, not whether it stays. A great magic number selling to customers who churn out in a year is a treadmill, not a machine. Read it alongside NRR (Rule 15).
- **It's noise before repeatable sales.** With a handful of lumpy deals per quarter, the ratio swings wildly. Like the burn multiple, it's a venture-stage metric, not a seed-stage one.

### 10. CAC payback period **[Evergreen]** (metric) / norms **[2026]**

**Plain words.** CAC (Customer Acquisition Cost) = total sales + marketing cost to land one customer. CAC payback = months until that customer's **gross-margin** dollars — not revenue — repay their CAC. (**Gross margin** = the share of each revenue dollar left after the direct costs of serving that customer: servers, support, model compute. Rule 16 covers the norms.)

**The math.** `Payback = CAC ÷ (monthly revenue per customer × gross margin %)`. Worked example: CAC $12,000; customer pays $1,000/month; 80% gross margin → contributes $800/month → payback = 12,000/800 = **15 months**. Conventional norms: **under 12 months excellent, 12–18 good, 18–24 acceptable for enterprise, 24+ alarming.** The smaller the customer, the faster payback must be, because small customers churn faster. **[2026]** watch-out: AI products with ~60% gross margins mechanically lengthen payback ~33% at identical CAC and pricing — a major reason investors now recompute everything at *your* margin, not the assumed 80% (see Rule 17).

**Where the norms come from.** These bands have a real address, in two layers. The stage-and-segment version is Bessemer's benchmark report [Scaling to $100 Million](https://www.bvp.com/atlas/scaling-to-100-million): target CAC payback **<12 months for SMB** customers (SMB = small and mid-sized businesses), **<18 months for mid-market**, **<24 months for enterprise**. Their rationale: enterprise customers live longer, so a slower payback is affordable; SMBs churn fast, so it isn't. Bessemer puts ~15 months as the average for $1–10M-ARR cloud companies — and Bessemer, like this rule, insists payback be computed on gross-margin-adjusted dollars, not revenue. The older single-number version comes from David Skok's [SaaS Metrics 2.0](https://www.forentrepreneurs.com/saas-metrics-2/) (forEntrepreneurs — the closest thing SaaS metrics has to a standard textbook): recover CAC within ~12 months; the best SaaS businesses recover in 5–7; and "profitability is anemic if the time to recover CAC extends beyond 12 months."

**When legends say to ignore it.** Payback measures how fast you *recycle cash*, not whether a customer is ultimately profitable — and the rule's own sources supply the exceptions. First, Bessemer's segmentation is itself the caveat: a 22-month payback fails the SMB bar and passes the enterprise one, so the single-number version of this rule is always wrong for somebody — know your segment before you grade yourself. Second, with very high retention (NRR 120%+, Rule 15), each customer is an annuity that keeps expanding. A long payback then becomes a *financing* problem rather than a business-quality problem — fronting cash for provably durable customers is exactly what venture money is for, the same speed-over-efficiency logic as Rule 12's counter-tradition. Third, pre-PMF the number is noise: with a handful of customers and founder-led sales, computed CAC is mostly your own salaries divided by luck.

### 11. LTV:CAC ≥ 3 **[Evergreen]**

**Plain words.** LTV (Lifetime Value) = total gross-margin dollars a customer generates before churning. The convention: **LTV should be at least 3× CAC.** Below 3, you're buying growth too expensively; a very high ratio (8+) suggests you're under-investing in growth.

**The math.** Standard simple formula: `LTV = ARPA × gross margin % ÷ monthly churn rate`. (ARPA = average revenue per account; monthly churn rate = the fraction of customers who cancel each month — see Rule 6 for churn.) Worked example: $500/month × 80% margin = $400/month contribution; 2% monthly churn → average lifetime 1/0.02 = 50 months → LTV = **$20,000**. If CAC = $5,000, LTV:CAC = **4:1**. Healthy.

**Where it comes from — honesty note.** Unlike Rule of 40 or burn multiple, nobody can point to a coiner. The 3:1 ratio is genuine folk wisdom from 2000s-era SaaS investing, popularized by benchmark shops like [ProfitWell/Paddle](https://www.paddle.com/resources) and David Skok's [forEntrepreneurs](https://www.forentrepreneurs.com/saas-metrics-2/) (which states the best SaaS businesses run 3x+, sometimes 7–8x). I could not verify a single original source — treat 3:1 as a convention, not a law. **When to ignore:** early on, both numbers are fiction. LTV extrapolates churn you haven't observed from a handful of customers. Insiders roll their eyes at seed decks with precise LTV:CAC claims. It becomes meaningful with ~2 years of cohort data — a cohort being a group of customers who signed up in the same period, tracked over time. Full treatment in `04-unit-economics.md`.

---

## Part 4: Survival rules

### 12. Default alive vs. default dead **[Evergreen]**

**Plain words.** From Paul Graham's [Default Alive or Default Dead?](https://paulgraham.com/aord.html) (2015) — the first question he asks any startup: *at your current growth rate and burn, do you reach profitability before the money runs out?* If yes, you're **default alive**: everything else is optimization. If no, you're **default dead**: your survival depends on raising money from people you don't control. PG's alarming observation: most founders can't answer, even 8–9 months in. (Trevor Blackwell built a calculator: [growth.tlb.org](https://growth.tlb.org/).)

**Worked example.** $600K in the bank, costs flat at $70K/month, revenue $20K/month today. The naive "runway" calculation (runway = months of cash left at your current burn) says $600K ÷ $50K net burn = 12 months. But that's the static mistake PG's essay exists to correct: your burn *shrinks every month* as revenue compounds against flat costs, so you last longer than static runway says. The real question is whether revenue reaches $70K/month (breakeven) before the cash is gone. Run the actual arithmetic. At **6% monthly growth**, cumulative burn eats the $600K in month ~16, with revenue still only ~$48K/month — about $22K short of breakeven. **Default dead.** At **7% monthly growth**, you cross breakeven around month 20 with roughly $18K of cash to spare. **Default alive.** One percentage point of monthly growth flips the answer — which is exactly why PG insists you do the compounding math (Blackwell's calculator does it for you) instead of eyeballing a runway number.

**The corollary insiders quote constantly:** "overhiring is by far the biggest killer of startups that raise money." Founders hire to *cause* growth; PG says slow growth usually means "the product is not appealing enough," and payroll just shortens the time you have to fix it. The **fatal pinch** (his term): default dead + slowing growth + not enough runway left to fix either — the state from which startups rarely recover. Related failure patterns: `11-failures.md`.

**When legends say to ignore it.** The canonical counter-tradition is **blitzscaling** — the doctrine of Reid Hoffman (co-founder of LinkedIn, partner at Greylock), laid out in *Blitzscaling* (2018, with Chris Yeh): deliberately "prioritiz[ing] speed over efficiency in an environment of uncertainty" ([blitzscaling.com](https://www.blitzscaling.com/)). Translated into PG's vocabulary: in a winner-take-most market — strong network effects (the product gets more valuable as more people use it), a closing land-grab window — you *choose* to run default dead. The first company to reach scale captures the market and can fix its economics afterward, while the competitor who grew "responsibly" captures nothing. Hoffman's own PayPal and LinkedIn, and later Uber and Airbnb, all ran years of deliberate, investor-financed default-dead. The synthesis: blitzscaling doesn't refute PG's question — it answers it differently. "Default dead, on purpose, in a market structure that rewards it, with investors who have explicitly signed up to keep funding it." All three conditions are load-bearing. If you're default dead by *accident* — no land grab, no committed capital, just burn — PG's rule, not Hoffman's, is the one that applies to you.

### 13. Ramen profitable **[Evergreen]**

**Plain words.** Also PG ([Ramen Profitable](https://paulgraham.com/ramenprofitable.html), 2009): profitable *only* in the sense that revenue covers the founders' bare living expenses (rent + instant noodles). Not a destination — "a trick for not dying en route." It buys unlimited runway, which transforms every negotiation: you can't be forced into a bad funding round, because you don't need one. Paradoxically, it makes fundraising easier — it proves customers pay and founders are disciplined. **[2026]** revival: with AI tooling collapsing headcount needs, "ramen profitable with 2 people and real revenue" has become a high-status position again, and some founders use it to skip priced rounds entirely.

(Two terms there. A **priced round** is a fundraise that sets an explicit valuation on the company and sells shares at that price. The alternative is a **SAFE** — Simple Agreement for Future Equity: a short standard contract, introduced by Y Combinator in 2013 and drafted by YC partner Carolynn Levy, in which an investor hands you money *now* in exchange for the right to receive shares *later*, at whatever price your next priced round sets, usually subject to a valuation cap. SAFEs and their older loan-shaped cousin, convertible notes, exist precisely to defer the valuation question. Mechanics in `05-fundraising.md`.)

**When legends say to ignore it.** PG's own essay contains the counterargument, and it's worth reading past the headline: "ramen profitability is not the destination. A startup's destination is to grow really big; ramen profitability is a trick for not dying en route." His named dangers: "the biggest danger is that it might turn you into a consulting firm" — grinding out service revenue to cover rent instead of building one product everyone uses — plus the self-deception of "telling yourselves you're a ramen profitable startup, when in fact you're not a startup at all." He also concedes it's simply infeasible for whole categories ("it would not be for most biotech startups, for example," or anything with long R&D before first revenue). The venture-scale critique sharpens this: optimizing for survival can optimize *against* the outlier outcome. The power-law math of Rule 3 pays for growth, not persistence, and a team that spends a year contorting the product toward early revenue may burn its "why now" window doing it. The synthesis: ramen profitability is leverage, not a goal. Take it if it lies on the path your product is already on; don't detour a venture-scale idea to reach it.

### 14. The 10x-better rule **[Evergreen]**

**Plain words.** From Peter Thiel, *Zero to One* (2014): "proprietary technology must be at least 10 times better than its closest substitute" to escape the gravity of switching costs and incumbency. 2x better isn't enough — customers discount your claims, and switching is painful, so marginal improvements lose to inertia. The 10x can come from being dramatically faster, cheaper, or making something possible that simply wasn't (Google search vs. 1999 alternatives; Stripe's 7 lines of code vs. merchant-account paperwork).

**When to ignore it.** Plenty of huge companies won on **distribution, timing, or bundling** with a ~2x product (Teams vs. Slack is the canonical cautionary tale — for the incumbent's side). The honest version of the rule: *you* need 10x on at least one dimension that your specific wedge customer cares about; you don't need 10x on everything. See `01-idea-evaluation.md`.

---

## Part 5: Retention and margin — the quality-of-revenue rules

### 15. Net revenue retention (NRR): 100% / 110% / 120%+ **[Evergreen]** (metric) / benchmarks **[2026]**

**Plain words.** NRR asks: of the customers you had 12 months ago, what is their revenue worth today, counting expansion, downgrades, and churn — but **no new customers**? Over 100% means your existing base grows by itself ("negative churn"): the single strongest signal of product quality in B2B software.

**The math.** `NRR = (starting cohort ARR + expansion − downgrades − churn) ÷ starting cohort ARR`. Worked example: cohort starts at $100K ARR; loses $10K to churn, $5K to downgrades, gains $25K expansion → (100−10−5+25)/100 = **110%**.

**Benchmarks.** Rough current consensus, compiled across [SaaS Capital's retention benchmarks](https://www.saas-capital.com/wp-content/uploads/2023/05/RB28WS1-2023-B2B-SaaS-Retention-Benchmarks.pdf) and [Lenny Rachitsky's expert-survey benchmarks](https://www.lennysnewsletter.com/): **<100% concerning, 100–110% solid, 110–120% good, 120%+ elite.** Crucially, NRR scales with contract size. SaaS Capital's survey of 1,500+ private B2B SaaS companies (the largest of its kind) found median NRR *rises* as annual contract value (ACV) rises. Companies with ACVs above $25K show median NRR of at least ~103%, while the numbers venture folklore calls "enterprise-grade" — ~118–120% — are what *top-quartile* companies with $100K+ ACVs report, not the median. So judge yourself against your segment, and be suspicious of anyone quoting 115%+ as a typical bar; across all private SaaS the median sits near 100%. **When to ignore:** NRR needs 12+ months of cohorts; it's noise at seed. And **[2026]**: usage-based AI products can show spectacular NRR that's really just usage volatility. Sophisticated investors now ask for **logo retention** alongside it — the % of *customers* who stay, regardless of dollars. (In sales-speak, each customer company is a "logo.") A 130% NRR from one whale (one very large customer) expanding while half your logos quietly leave is a sick business wearing a healthy metric.

### 16. Gross margin norms: software ~80% **[Evergreen]**, AI ~50–65% **[2026]**

**Plain words.** Gross margin = (revenue − direct cost of serving customers) ÷ revenue. Classic SaaS runs **75–85%** because serving one more customer costs pennies of server time. This is *why* software commands premium valuation multiples; high gross margin is the engine behind every efficiency rule above. **[2026]**: AI-native products pay for GPU inference — running the model on specialized graphics chips — on every single use. [a16z's "The New Business of AI"](https://a16z.com/the-new-business-of-ai-and-how-its-different-from-traditional-software/) flagged this early: AI companies run gross margins **25–30 points below classic SaaS, often 50–60%**, and current-era estimates put compute at 30–60% of revenue for many AI startups vs. 5–15% hosting costs for traditional SaaS. The open debate (detailed in `10-ai-era.md`): bulls say falling inference prices fix this over time; bears note that competitive products keep absorbing the savings with bigger models and more tokens per task. What you must internalize: **an "AI SaaS" company at 55% margin needs roughly 1.5x the revenue of an 80%-margin SaaS company to generate the same gross profit — and every payback/LTV rule above silently assumed 80%.**

**When legends say to ignore it.** Three sanctioned exceptions:

- **The 80% bar is a *software* norm, not a universal one.** Marketplaces, fintechs earning interchange, and hardware companies are judged on entirely different yardsticks. (**Interchange** = the small fee, typically ~1–2% of each card transaction, that merchants pay and the card-issuing side collects on every swipe — the core revenue engine of many consumer fintechs, which is why their "gross margin" looks nothing like SaaS.) Marketplaces are graded on take rate (the percentage of each transaction the marketplace keeps); hardware on unit margins of ~30–50%. Amazon built one of history's great companies on famously thin margins. Applying the SaaS bar outside SaaS is a category error — know which comparison set your business is in (`02-business-models.md`).
- **Early margins are a snapshot, not a destiny.** At seed, investors underwrite the *trajectory*: an AI product at 40% margin with a credible path — falling inference prices, model distillation, caching, routing easy queries to cheaper models — can be a fine bet. Even [a16z's original piece](https://a16z.com/the-new-business-of-ai-and-how-its-different-from-traditional-software/) frames low AI margins as a structural difference to manage, not a disqualifier. What's *not* sanctioned is pretending: claiming 80% "at scale" with no mechanism.
- **Margin math on ten customers is noise.** With a handful of pilot deals, discounts, and un-optimized infrastructure, computed gross margin is meaningless. Like most rules here, it becomes a real gate at scale — Series B+ diligence (the investor's formal vetting of your books before writing a check) recomputes everything at your actual margin.

---

## Part 6: Fundraising norms

### 17. Dilution per round: ~10–25% **[Evergreen]** (range) / current medians **[2026]**

**Plain words.** Dilution = the percentage of the company you sell in each funding round. The evergreen band is 10–25% per round. Selling more signals weakness and wrecks founder math over multiple rounds.

**Current medians.** These come from Carta, drawn from actual cap tables. (A **capitalization table**, or cap table, is the official ledger of exactly who owns what percentage of a company. Carta is the software most startups use to manage theirs, which is why its data is the gold standard.) The medians: **~12.5% at pre-seed, ~19.5% at seed, ~18–20% at Series A, ~14% at Series B** ([Carta Founder Ownership Report 2026](https://carta.com/data/founder-ownership-2026/), [Carta State of Private Markets](https://carta.com/data/state-of-private-markets-q4-2025/)). Median founding *team* ownership: ~56% after seed, ~36% after Series A. *Verification caveat:* Carta's site blocks automated fetching, so these exact 2026 figures could not be re-verified at review time. They are consistent with Carta's 2025 reporting but should be treated as approximate-and-unconfirmed — pull the current report yourself before negotiating a round. The *shape* of the data (roughly 10–13% pre-seed, ~20% seed, slightly less at A, declining thereafter) has been stable across Carta's editions.

**Worked example (simplified).** Two founders, 50/50. Pre-seed: sell 12.5% and create a ~10% employee option pool (shares set aside to grant future employees) → founding team: 100% × (1 − 0.125 − 0.10) = **77.5%**. Seed: sell 19.5%, top the pool back up (~5%) → 77.5% × 0.755 ≈ **58.5%**. Series A: sell 19%, pool top-up ~5% → 58.5% × 0.76 ≈ **44.5%**. Note the example lands *above* Carta's medians (~56% post-seed, ~36% post-A): real cap tables give up more than this clean arithmetic, via larger pool top-ups, advisor grants, and stacked SAFEs converting at once. (SAFEs are defined in Rule 13. The trap here: founders often raise *several* SAFEs over a year or two, each one a promise of future shares, and they all convert to actual shares simultaneously at the next priced round. The combined dilution lands at once and routinely surprises founders who never added it up.) Two lessons: dilution *compounds* — each round multiplies against what's left, so 5 extra points sold at pre-seed costs far more than 5 points at Series B — and the tidy version of the math is the *floor*, not the median. Mechanics of SAFEs, priced rounds, and option pools: `05-fundraising.md`.

**When legends say to ignore it.** The counter-tradition says founders over-optimize dilution and under-optimize company quality. Paul Graham formalized it in [The Equity Equation](https://paulgraham.com/equity.html) (2007): selling n% of your company is worth it whenever the trade improves your outcome by more than 1/(1 − n) — e.g., giving an investor 20% is a win if the money and help make the company more than 1.25x more valuable ("In the general case, if n is the fraction of the company you're giving up, the deal is a good one if it makes the company worth more than 1/(1 - n)"). Owning 30% of a $1B company beats owning 60% of a $50M one by an order of magnitude. The rule of thumb protects you from *pointless* dilution — selling 35% at seed because you didn't know the norms — not from *productive* dilution. Run the equity equation, not just the percentage.

### 18. Traction milestones that unlock each round **[2026]** (numbers) / **[Evergreen]** (existence of a laddered bar)

These are conventions, not laws — hot AI teams routinely skip rungs, and the bar shifts yearly. As of 2025–2026 data ([Carta](https://carta.com/data/state-of-private-markets-q4-2025/) and ecosystem surveys; treat non-Carta specifics as approximate):

- **Pre-seed** (~$500K–$1M raised): no revenue required. You're selling team + insight + a prototype. In AI, strong technical founders raise on reputation alone.
- **Seed** (~$2–4M raised, low-teens $M valuations for the median, dramatically higher for AI-anointed teams): a live product and *evidence of pull* — often $100–500K ARR, or design partners plus explosive usage. (**Design partners**, a term of art: early customers who use the product free or at a steep discount in exchange for shaping it with feedback. They count as demand evidence before they count as revenue.) Pre-revenue seeds still happen, mostly for repeat founders and hot AI theses.
- **Series A**: the real gate. Convention: **~$1–2M ARR floor, with 2–3x year-over-year growth**. The median Series A company recently sat around ~$1.5M ARR, and competitive deals cluster at $2–3M+ with strong retention and a sane burn multiple (≤~1.5x). The median seed→A gap has stretched to ~24 months, and a large fraction of seeded companies never raise an A at all — plan runway accordingly (see Rule 12).

I could not verify one single authoritative 2026 number for "ARR required at Series A" — no such number exists. It's a distribution, and the right mental model is: the A rewards *evidence the machine works*, at whatever metric your category uses.

### 19. 2026-era additions: what's newly true this cycle **[2026]**

Three current-era norms that didn't exist in the pre-2023 canon, covered in depth in `10-ai-era.md` and `03-pricing.md`:

- **Burn-multiple scrutiny on AI startups.** Fast AI revenue is now routinely discounted as "experimental budget" revenue: investors probe whether spectacular ARR is retained, contracted, and gross-margin-positive after inference costs. A 1.5x burn multiple *at 55% gross margin* is worse than it looks — some investors now compute burn against new *gross profit* instead of new ARR to normalize this.
- **The inference-cost gross-margin debate** (Rule 16): whether AI margins converge to SaaS's 80% or settle at a structural 60–65% ceiling is the single most-argued benchmark question of this cycle. Underwrite your model at your *actual* margin.
- **The "seat-based collapse."** Per-seat pricing — charging per user with a login — is being abandoned for AI products, because a good agent *reduces* the seats a customer needs: the vendor gets paid to under-deliver. Industry pricing surveys in 2025–26 show pure seat-based pricing dropping sharply (one widely cited survey: from ~21% to ~15% of software companies in a year), while hybrid platform-fee-plus-usage models surged to become the default, and outcome-based pricing (pay per resolved ticket, per completed task) emerged at the vendors with the most measurable outcomes ([Growth Unhinged](https://www.growthunhinged.com/) tracks this benchmark data continuously; specific survey percentages are approximate and moving fast).

---

## The one-page cheat sheet

| Rule | The number | Tag | Coined by |
|---|---|---|---|
| TAM math | customers × $/customer (bottom-up) | Evergreen | folk / PG formulation |
| Venture-scale TAM | $1B min, $5–10B preferred | Evergreen / 2026 | VC fund math |
| Obtainable share | 1–5% of SAM | Evergreen | convention |
| Good early growth | 5–7%/week | Evergreen | Paul Graham |
| Post-PMF path | T2D3: 3,3,2,2,2 from $2M ARR | Evergreen | Neeraj Agrawal |
| Rule of 40 | growth% + margin% ≥ 40 (at scale) | Evergreen | Brad Feld (popularized) |
| Burn multiple | <1x amazing, >3x bad | Evergreen / 2026 | David Sacks |
| Magic number | >0.75 → scale sales | Evergreen | Lars Leckie |
| CAC payback | <12 mo great, >24 alarming | 2026 numbers | Bessemer benchmarks / David Skok |
| LTV:CAC | ≥3:1 | Evergreen | folk wisdom |
| Default alive | reach profit before $0? | Evergreen | Paul Graham |
| 10x rule | 10x better on one axis | Evergreen | Peter Thiel |
| NRR | 100 solid / 110 good / 120+ elite (scales with ACV) | 2026 numbers | convention |
| Gross margin | SaaS ~80%, AI ~50–65% | Evergreen / 2026 | a16z flagged AI gap |
| Dilution/round | ~12% pre-seed, ~20% seed, ~18% A | 2026 medians | Carta data |
| Series A bar | ~$1.5–3M ARR, 2–3x growth | 2026 | convention |

---

## Sources

- Paul Graham, [Default Alive or Default Dead?](https://paulgraham.com/aord.html) (2015)
- Paul Graham, [Startup = Growth](https://paulgraham.com/growth.html) (2012)
- Paul Graham, [Black Swan Farming](https://paulgraham.com/swan.html) (2012)
- Paul Graham, [How to Convince Investors](https://paulgraham.com/convince.html) (2013)
- Paul Graham, [Ramen Profitable](https://paulgraham.com/ramenprofitable.html) (2009)
- Paul Graham, [The Equity Equation](https://paulgraham.com/equity.html) (2007)
- Marc Andreessen, [The Only Thing That Matters (product-market fit)](https://pmarchive.com/guide_to_startups_part4.html) (2007)
- David Sacks, [The Burn Multiple](https://sacks.substack.com/p/the-burn-multiple-51a7e43cb200) (2020)
- Brad Feld, [The Rule of 40% For a Healthy SaaS Company](https://feld.com/archives/2015/02/rule-40-healthy-saas-company/) (2015)
- Neeraj Agrawal / Battery Ventures, [The SaaS Adventure (T2D3)](https://www.battery.com/blog/helping-entrepreneurs-triple-triple-double-double-double-to-a-billion-dollar-company/) (2015)
- Bessemer Venture Partners, [The Cloud 100 Benchmarks Report](https://www.bvp.com/atlas/the-cloud-100-benchmarks-report) and [Scaling to $100 Million](https://www.bvp.com/atlas/scaling-to-100-million)
- Scale Venture Partners, [Benchmarking SaaS growth and burn](https://www.scalevp.com/blog/benchmarking-saas-growth-and-burn)
- Carta, [Founder Ownership Report 2026](https://carta.com/data/founder-ownership-2026/) and [State of Private Markets: 2025 in Review](https://carta.com/data/state-of-private-markets-q4-2025/)
- Lenny Rachitsky, [Your startup idea probably isn't venture-scale](https://www.lennysnewsletter.com/p/your-startup-idea-probably-isnt-venture) and [Lenny's Newsletter benchmark surveys](https://www.lennysnewsletter.com/)
- a16z, [The New Business of AI (and How It's Different From Traditional Software)](https://a16z.com/the-new-business-of-ai-and-how-its-different-from-traditional-software/)
- Kyle Poyar, [Growth Unhinged](https://www.growthunhinged.com/) — SaaS/AI benchmark reports incl. the [2026 State of AI for B2B GTM report](https://www.growthunhinged.com/p/2026-state-of-ai-gtm-report)
- SaaS Capital, [2023 B2B SaaS Retention Benchmarks (Research Brief 28)](https://www.saas-capital.com/wp-content/uploads/2023/05/RB28WS1-2023-B2B-SaaS-Retention-Benchmarks.pdf) — survey of 1,500+ private B2B SaaS companies; source of the NRR-by-ACV figures in Rule 15
- The SaaS CFO, [How to Calculate the SaaS Magic Number](https://www.thesaascfo.com/calculate-saas-magic-number/) (Lars Leckie origin and quote)
- Practical Founders, ["Venture Scale" Means Big VCs Require Billion Dollar Exit Potential](https://practicalfounders.com/articles/venture-scale-means-big-vcs-require-billion-dollar-exit-potential/)
- Wall Street Prep, [The Rule of 40](https://www.wallstreetprep.com/knowledge/rule-of-40/) and [Bessemer Efficiency Score](https://www.wallstreetprep.com/knowledge/bessemer-efficiency-score/)
- Peter Thiel, *Zero to One* (2014) — 10x rule, small-market monopoly strategy (book; not linkable)
- Reid Hoffman & Chris Yeh, *Blitzscaling* (2018) and [blitzscaling.com](https://www.blitzscaling.com/) — "prioritizes speed over efficiency in an environment of uncertainty"; the deliberate-default-dead counter-tradition in Rule 12
- David Skok, [SaaS Metrics 2.0](https://www.forentrepreneurs.com/saas-metrics-2/) (forEntrepreneurs) — CAC payback ~12-month guideline ("profitability is anemic if the time to recover CAC extends beyond 12 months"; best businesses 5–7 months) and LTV:CAC 3x+ guideline
- Aileen Lee, [Welcome to the Unicorn Club: Learning From Billion-Dollar Startups](https://techcrunch.com/2013/11/02/welcome-to-the-unicorn-club/) (TechCrunch, 2013) — coined "unicorn"
- Trevor Blackwell, [Startup Growth Calculator](https://growth.tlb.org/)

*Verification notes: written 2026-07-23, revised same day after two rounds of review. Carta dilution/ownership medians and Series A ARR figures reflect 2025–early-2026 reporting and drift quarterly; Carta's site blocks automated fetching, so the specific 2026-report figures in Rule 17 are flagged unverified in the text — consistent with prior Carta editions but unconfirmed against the cited report. The seat-based-pricing survey percentages and stage-specific burn-multiple bars circulate widely in 2026 ecosystem writing but come from vendor/VC surveys of varying rigor — treat them as directional. The LTV:CAC 3:1 ratio has no verifiable original source. The "TAM of nearly zero" line often attributed to Sam Altman could not be traced to a primary source and is now presented as unattributed folklore, not a quotation. Rule 8's Sacks quotes were verified verbatim against sacks.substack.com; the amazing/great/good/suspect/bad table comes from a graphic in the essay and could not be confirmed in retrievable text, so it is presented alongside the essay's prose anchors (2x "reasonable for an early-stage startup," 5x "terrible"). Rule 10's payback bands were verified against Bessemer's Scaling to $100 Million (<12/<18/<24 by segment) and Skok's SaaS Metrics 2.0. Rule 12's worked example was recomputed after the original was found arithmetically wrong (at the original numbers the company was default alive, not dead); the current 6%-vs-7% version has been checked by compounding month by month. Rule 15's NRR-by-ACV figures were checked directly against SaaS Capital's Research Brief 28 (median NRR ≥ ~103% for ACVs above $25K; 118–120% is the top-quartile figure for $100K+ ACVs, not a segment median). The PayPal PowerSeller count (~20,000) and the "err on the side of starting too small" line follow Zero to One; Thiel's small-market argument is his, but he does not use "TAM" vocabulary in the book. The Rule 17 worked example is deliberately simplified and lands above Carta's medians; the text now says so rather than claiming an exact match.*
