# Business Model Taxonomy — every model, its tradeoffs, what works and what fails

**Why this matters to you:** Your business model is not a detail you figure out after the idea — it *is* half the idea. Two startups attacking the same problem with different models can have wildly different margins, fundraising prospects, and endgames. Investors pattern-match your model within the first two minutes of a pitch. Your friends who succeeded knew this vocabulary cold: they could say "we're PLG with a usage-based expansion motion" and instantly communicate their margins, sales strategy, and hiring plan. This document gives you that vocabulary, the honest tradeoffs behind each model, and a framework for choosing. For how to *price* within a model see `03-pricing.md`; for the underlying math (CAC, LTV, payback) see `04-unit-economics.md`.

---

## Part 1: The core vocabulary (read this first)

A few terms you'll see throughout, defined once:

- **Gross margin** — revenue minus the direct cost of delivering the product (servers, support, hardware parts), as a percentage of revenue. Software is prized because gross margins run 80–90%; every extra dollar of revenue costs almost nothing to serve. **[Evergreen]**
- **COGS** — Cost of Goods Sold: the accounting name for that direct cost of serving the product (servers, AI inference, support, hardware parts). Gross margin is simply revenue minus COGS, as a percentage. When someone says "inference is the dominant COGS line," they mean GPU compute is the biggest cost of serving each customer. **[Evergreen]**
- **Inference** — running a trained AI model to produce an answer. Every AI query burns real compute money on GPUs (the specialized chips that run AI models). This is why AI products have real per-use costs where classic software has almost none. **[Evergreen]**
- **ARR / MRR** — Annual / Monthly Recurring Revenue. The annualized value of subscription contracts. Recurring revenue is valued far above one-time revenue because it compounds and is predictable. **[Evergreen]**
- **CAC** — Customer Acquisition Cost: total sales and marketing spend divided by new customers won.
- **LTV** — Lifetime Value: the gross profit a customer generates before they leave (churn).
- **Churn** — the rate at which customers or revenue leave you per month or year.
- **Runway** — how many months of cash the company has left at its current spending rate before it dies. "18 months of runway" means 18 months to reach profitability or raise more money. **[Evergreen]**
- **GMV** — Gross Merchandise Value: the total dollar value of goods/services sold *through* a marketplace. Not your revenue — your revenue is the slice you keep.
- **Take rate / rake** — the percentage of each transaction a platform keeps.
- **Series A, B, C…** — the named rounds of venture funding, in order. Seed is the first small round; Series A is the first major round; each later letter is a bigger round at (hopefully) a higher valuation.
- **Defensibility / moat** — whatever stops a competitor from copying you and stealing your customers (network effects, switching costs, data, brand, scale economies). See `01-idea-evaluation.md`.

YC (Y Combinator, the startup accelerator) teaches that essentially every startup falls into roughly nine model families — enterprise, SaaS, usage-based, subscription, transactional, marketplace, e-commerce, advertising, hardware — each with its own metrics that investors expect you to know ([Anu Hariharan, "Nine Business Models and the Metrics Investors Want," YC Startup Library](https://www.ycombinator.com/library/8E-nine-business-models-and-the-metrics-investors-want)). **[Evergreen]** The taxonomy below expands those into today's full menu, including the AI-native models that emerged 2023–2026.

---

## Part 2: The taxonomy

### 2.1 B2B SaaS, seat-based subscription

**How it works:** You sell software to businesses ("B2B" = business-to-business; "SaaS" = Software as a Service, i.e., software delivered over the internet for a recurring fee). Price is per user ("seat") per month, e.g., $30/seat/month. Salesforce popularized this in the 2000s.

**Revenue mechanics:** ARR = seats × price × 12. Growth comes from (a) new customers, (b) existing customers adding seats ("expansion"), minus (c) churn. Best-in-class SaaS shows **net revenue retention (NRR)** — revenue this year from last year's customers — above 110–120%: the base grows even with zero new sales. **[Evergreen]** principle; the specific 110–120% benchmark is a **[2026]**-era number.

**Worked example:** 100 customers × 20 seats × $30/month = $60,000 MRR = $720K ARR. If customers add seats at 15%/year and 8% of revenue churns, you grow 7%/year before selling to anyone new.

**Gross margin:** 75–90%. **Capital needs:** low-to-moderate; the main cost is people. **Defensibility:** workflow lock-in and integration depth — switching CRMs (Customer Relationship Management software) is painful, so churn is low.

**Failure modes:** building a "vitamin not painkiller" (a nice-to-have that churns in a downturn); competing in a crowded category on features; SMB (small/medium business) churn so high that CAC never pays back.

**Winners:** Salesforce, Slack, Figma. **Failures:** the long tail of thousands of undifferentiated SaaS tools that plateaued at $1–5M ARR — common enough that "SaaS graveyard" is a genre (see `11-failures.md`).

**Fit criteria:** choose when value scales with the *number of humans using it* and usage is continuous. **[2026] caveat:** the AI era is directly attacking this assumption — see §2.13.

---

### 2.2 Usage-/consumption-based

**How it works:** Customers pay for what they consume — gigabytes, API calls, compute-minutes, messages. AWS, Snowflake, Twilio, Datadog.

**Revenue mechanics:** revenue tracks customer activity, so it grows automatically as customers grow ("land small, expand with usage"). Snowflake-style NRR ran 130–170% in peak years because customers' data grew. The flip side: revenue also *shrinks* automatically. Customers optimize their bills in downturns, and there is no contractual floor unless you sell committed-use contracts (deals where the customer promises a minimum spend). Tomasz Tunguz (VC at Theory Ventures, prolific SaaS-metrics blogger) found usage-based companies suffered worse sales-cycle elongation than seat-based ones in the 2022–23 downturn (29% vs 21%), because buyers crave predictability when budgets tighten ([Tunguz on seat vs. usage pricing](https://tomtunguz.com/seat-vs-usage-based-pricing/)). **[Evergreen]** principle (usage aligns price to value but transfers volatility to you); numbers **[2026]**.

**Gross margin:** 60–80% — lower than seat SaaS because you're reselling real infrastructure. **Capital needs:** moderate. **Defensibility:** data gravity (moving stored data is expensive) and integration depth.

**Failure modes:** revenue whiplash; misaligned incentives (customers fear surprise bills and cap usage); pricing on a metric customers can't predict or control.

**Winners:** AWS, Twilio, Snowflake. **Failures/warnings:** Nirvanix is the canonical dead usage-based infra company. The cloud-storage provider raised ~$70M (Khosla Ventures led its Series C), competed with AWS on price per gigabyte, and shut down so abruptly in October 2013 that customers got roughly two weeks' notice to migrate their data off before bankruptcy ([Nirvanix](https://en.wikipedia.org/wiki/Nirvanix)). The lesson: usage-based revenue with no contractual floor, plus a capital-intensive infrastructure war against hyperscalers (the giant cloud providers — Amazon, Microsoft, Google), is a losing combination. More broadly, many usage-based infra companies saw growth collapse from 60% to 20% within a year in 2023 when customers optimized.

**Fit criteria:** choose when value truly scales with a measurable unit of consumption, and your buyer is technical enough to forecast their own usage.

---

### 2.3 Freemium & product-led growth (PLG)

**How it works:** PLG means the *product* is the salesperson: users sign up free (freemium = free tier + paid tiers), get value themselves, and upgrade or pull in their team. Sales gets involved late, if ever, to close the big accounts. Dropbox, Notion, Figma, Calendly.

**Revenue mechanics:** a funnel — visitors → free signups → activated users → paid conversions → team/enterprise expansion. Benchmarks: median B2B freemium-to-paid conversion is roughly 2.6%, top quartile 5–8%, and most conversions happen within the first 14 days ([OpenView Product Benchmarks](https://openviewpartners.com/2022-product-benchmarks/); [Growth Unhinged PLG benchmark guide](https://www.growthunhinged.com/p/your-guide-to-plg-benchmarks)). **[2026]** numbers; the **[Evergreen]** principle is that free users are a marketing cost you must convert or monetize indirectly.

**Worked example:** 100,000 free signups/year × 3% conversion × $180/year average = $540K new ARR. If serving a free user costs $2/year, free-tier COGS is $200K — a real cost that AI features can multiply tenfold.

**Gross margin:** 70–85% (free users drag it down). **Capital needs:** moderate — you fund a large free base before revenue. **Defensibility:** bottom-up adoption creates internal virality and switching costs once a whole team is on it.

**Failure modes:** a free tier so generous nobody pays; a product without a natural team/sharing loop (PLG needs virality); loving your signup graph while conversion stays at 0.5%. **[2026]:** AI inference costs make generous free tiers dangerous — giving away GPU time is not like giving away storage.

**Winners:** Figma, Notion, Dropbox, Calendly. **Failures:** countless dev tools with huge free adoption and no monetization path.

**Fit criteria:** choose when individual users can get value in minutes without permission from a boss, and usage naturally spreads within teams.

---

### 2.4 Enterprise sales-led

**How it works:** Sell six-to-seven-figure annual contracts to large companies through a human sales force. Long cycles (3–12 months), procurement, security reviews, pilots. Palantir, Workday, Databricks (top end).

**Revenue mechanics:** a small number of large accounts. 10 customers × $500K/year = $5M ARR. Per YC's framing, the enterprise model is judged on bookings, pipeline, and average contract value rather than self-serve funnel metrics ([YC, Nine Business Models](https://www.ycombinator.com/library/8E-nine-business-models-and-the-metrics-investors-want)). **[Evergreen]**

**Gross margin:** 70–85%, though heavy professional services (implementation consulting) drag blended margin down. **Capital needs:** high — you pay salespeople and engineers for a year before the first big check clears. **Defensibility:** deep integration, multi-year contracts, compliance certifications competitors lack.

**Failure modes:** the classic near-death experience is 18 months of runway spent on three pilots that never convert ("pilot purgatory"); a founder who can't sell and hires a VP of Sales too early; single-customer concentration (one "logo" — sales jargon for a customer account — making up 60% of revenue), which scares investors.

**Winners:** Palantir, Veeva, Workday. **Failures:** Powa Technologies is the textbook enterprise flameout. The UK mobile-commerce company raised a $76M Series A in 2013 (then the largest tech Series A on record) and claimed a $2.6B enterprise value. In February 2016 it collapsed into administration (the UK equivalent of bankruptcy protection) after it emerged that most of its trumpeted retailer "contracts" were non-binding letters of intent and a claimed China UnionPay "strategic alliance" didn't exist. The Financial Times later pegged its real value at ~$106M ([Powa Technologies](https://en.wikipedia.org/wiki/Powa_Technologies)). It's pilot purgatory in its terminal form: signed-looking paper, no converting revenue, enterprise-scale burn.

**Fit criteria:** choose when the problem is worth ≥$100K/year to a buyer, requires trust/compliance, and can't be adopted bottom-up. Requires a founder willing to personally sell for years — see `08-talking-to-users.md`.

---

### 2.5 Transactional / take-rate (payments, fintech)

**How it works:** You sit in a money flow and keep a slice of every transaction. Stripe (~2.9% + 30¢ per card payment), PayPal, Shopify Payments.

**Revenue mechanics:** revenue = TPV (Total Payment Volume) × net take rate. The catch: most of a payments take rate is passed through to card networks and banks. Stripe charging 2.9% might *keep* ~0.5% after interchange fees (the fees card networks and issuing banks charge on every transaction). So a fintech doing $1B in TPV at 0.5% net take = $5M revenue. Volume must be enormous. **[Evergreen]**

**Gross margin:** on *net* revenue, 40–70%. It looks deceptively high if you naively count gross fees as revenue — sophisticated investors always ask for net. **Capital needs:** high — regulation, licensing, fraud losses, and trust-building. **Defensibility:** being embedded in the money flow is extremely sticky; switching payment providers risks revenue.

**Failure modes:** underestimating fraud and compliance costs; building on volume that belongs to someone else's platform; take-rate compression as payments commoditize.

**Winners:** Stripe, Adyen, Square/Block. **Failures:** dozens of neobanks (app-only consumer banks) and payment startups that never reached the volume where thin margins cover fixed costs.

**Fit criteria:** choose when you can embed into a *large, recurring* money flow and add real value (fraud reduction, conversion lift) beyond moving money.

---

### 2.6 Marketplaces

**How it works:** Connect supply and demand and take a rake on transactions. Airbnb (hosts/guests), Uber (drivers/riders), eBay, DoorDash.

**The chicken-and-egg problem:** buyers won't come without sellers, and sellers won't come without buyers. Most marketplaces die right here — they never reach **liquidity** (enough density that a buyer reliably finds a seller and vice versa). a16z (Andreessen Horowitz, the venture firm) notes it's usually easier to bootstrap supply — suppliers are economically motivated — and demand aggregation is the harder, more valuable side ([a16z, Required Reading for Marketplace Entrepreneurs](https://a16z.com/required-reading-for-marketplace-entrepreneurs/); [Andrew Chen's 20 best marketplace essays](https://andrewchen.com/marketplace-startups-best-essays/)). **[Evergreen]**

**Rake economics:** Bill Gurley's canonical essay ["A Rake Too Far"](https://abovethecrowd.com/2013/04/18/a-rake-too-far-optimal-platformpricing-strategy/) argues that greedy rakes kill platforms: high fees inflate prices, push suppliers to go around you, and invite competitors ("the worship of premium pricing always creates a market for the competitor," he quotes from management writer Peter Drucker). His formula: **"high volume combined with a modest rake is the perfect formula."** Reference points from the essay and since: eBay ~10%, Amazon Marketplace ~6–15% by category, Apple's App Store 30% (which bred lasting resentment and regulation), Booking.com winning Europe with a modest ~10% agency fee. **[Evergreen]**

**Worked example:** $100M GMV × 15% take rate = $15M net revenue. On that net revenue, gross margin might be 60–70% after payments and support. So a "$100M marketplace" is economically a ~$10M-gross-profit software company — this is why investors discount GMV.

**Gross margin:** 50–70% of *net revenue* (managed marketplaces that touch logistics run much lower). **Capital needs:** high — subsidizing both sides through the cold start (the early period when neither side has a reason to show up) is expensive; Uber burned billions. **Defensibility:** the best in tech once liquidity is reached — network effects mean each new user makes the platform better for everyone.

**Failure modes:** never reaching liquidity (the #1 killer); **disintermediation** (buyer and seller meet once, then transact off-platform — this plagues home services and tutoring); raking too hard; boiling the ocean geographically instead of winning one city or category first (Uber and DoorDash both won city by city).

**Winners:** Airbnb, Uber, eBay, Etsy, DoorDash. **Failures:** countless local-services marketplaces (Homejoy is the classic case — it died of disintermediation and paid-acquisition addiction; see `11-failures.md`).

**Fit criteria:** choose when supply and demand are both fragmented, transactions are frequent, and trust/matching genuinely matter. If the same buyer and seller repeat-transact, expect disintermediation and design around it (escrow, insurance, scheduling — keep the value on the platform).

---

### 2.7 Consumer subscription

**How it works:** Individuals pay monthly/annually: Netflix, Spotify, Duolingo, Calm.

**Revenue mechanics:** the war is against churn. Consumer monthly churn of 4–8% is normal — meaning half your subscribers can be gone within a year — so you must replace huge fractions of your base annually just to stay flat. Annual plans, family plans, and habit-forming daily-use loops are the standard weapons. **[Evergreen]** dynamics; churn benchmarks **[2026]**.

**Worked example:** 100K subscribers at $10/month with 5% monthly churn lose 5,000 subs/month; you need 5,000 new paying subs monthly (at, say, $30 CAC = $150K/month spend) before you grow at all.

**Gross margin:** 60–85% depending on content/licensing costs. Spotify's had climbed only to ~32% by 2025 — up from ~26% in 2023 and still far below software norms — because record labels take most of each dollar; a warning about building on licensed supply ([Spotify financials](https://stockanalysis.com/stocks/spot/financials/)) **[2026]**. **Capital needs:** moderate-to-high (brand and content). **Defensibility:** weak-to-moderate — habit, content library, personalization data. Consumer attention is fickle.

**Failure modes:** churn forever outrunning acquisition; subscription fatigue; paying for content that walks away.

**Winners:** Netflix, Spotify, Duolingo, NYT. **Failures:** most meditation/fitness/dating apps below the top 2–3 in their category; MoviePass (sold $10 subscriptions for a product that cost far more to deliver — negative gross margin at scale is unfixable).

**Fit criteria:** choose only if the product is *habitual* (used weekly-plus) and delivers continuous fresh value. One-time-value products (tax prep, resume builders) masquerading as subscriptions churn to death.

---

### 2.8 Advertising-supported

**How it works:** The product is free; attention is sold to advertisers. Google, Meta, TikTok, Reddit.

**Revenue mechanics:** revenue = users × time spent × ad load × price per ad (CPM = cost per mille, the price per thousand impressions). Worked example: 10M DAU (daily active users) × 20 minutes/day × 3 ads/minute × $5 CPM ≈ $3M/day ≈ $1.1B/year. Note what that implies: at 100K users the same math yields ~$11K/year — advertising only works at *enormous* scale. **[Evergreen]**

Ben Thompson's **Aggregation Theory** explains why the winners are so few: internet "aggregators" own the direct user relationship, have zero marginal costs, and enjoy demand-side network effects where suppliers (content creators, advertisers) come to them for free — producing winner-take-all outcomes ([Stratechery, "Defining Aggregators"](https://stratechery.com/2017/defining-aggregators/)). **[Evergreen]**

**Gross margin:** 60–80% at scale. **Capital needs:** extreme — years of losses before an ad business turns on. **Defensibility:** the strongest moats in tech at scale (network effects + data), zero before scale.

**Failure modes:** the model *is* the failure mode for startups: you need tens of millions of engaged users before revenue is meaningful, and the "default-alive" path (Paul Graham's term for a startup that reaches profitability on its existing cash without needing another fundraise) doesn't exist. Winners: Google, Meta, TikTok. Failures: nearly every ad-supported startup of the 2010s (Vine died despite huge usage).

**Fit criteria:** almost never the right choice for a first-time founder in 2026 unless you have a credible plan to reach 10M+ users on venture subsidy. **[2026]**

---

### 2.9 Hardware, and hardware + SaaS

**How it works:** Sell physical devices; increasingly, attach recurring software revenue (Peloton bike + subscription, Tesla + FSD — its Full Self-Driving subscription, Samsara's fleet sensors + dashboard SaaS).

**Revenue mechanics & margins:** pure hardware gross margins run 20–40%, and revenue is one-shot — you re-earn every sale. (Apple's *hardware* — its Products segment — ran ~37% in FY2025, world-best for consumer devices. The ~46% figure often quoted for Apple is company-wide margin, inflated by its ~75%-margin Services line, per the segment data in Apple's 10-K — its annual SEC filing. Know the difference before you cite it in a pitch. **[2026]**) Hardware+SaaS transforms this: sell the device near cost, attach an 80%-margin subscription. Worked example: a $500 device at 30% margin yields $150 once; a $50/month attached subscription at 80% margin yields $480/year forever. This is why investors will value your *software attach rate* far above your device sales. **[Evergreen]**

**Capital needs:** the highest of any model — inventory, tooling, manufacturing runs, working capital (you pay the factory months before the customer pays you). **Defensibility:** hard to copy, real supply-chain and certification moats, physical install base lock-in.

**Failure modes:** "hardware is hard" is earned wisdom — one bad manufacturing run can kill you; inventory misforecasts strand cash; consumer hardware fights brutal retail margins. Juicero is the canonical ridicule case ($120M raised for a $400 juicer); Peloton shows the whiplash of demand misforecasting; Quibi-style content-hardware hybrids fare worse.

**Winners:** Apple, Tesla, Samsara, Anduril. **Fit criteria:** choose only when the atoms are *necessary* to the value (sensing, robotics, defense) and design a recurring software layer from day one.

---

### 2.10 Open-source commercial (open-core, hosting)

**How it works:** Give the core software away as open source (source code freely usable), then monetize via (a) **open-core** — proprietary enterprise features (SSO — single sign-on, audit logs, permissions) on top of the free core (GitLab), (b) **managed hosting/cloud** — run it for people (MongoDB Atlas, Databricks), or (c) support/services (Red Hat).

Joseph Jacks (founder of OSS Capital, a fund that invests only in **COSS** — Commercial Open Source Software) defines a COSS company as one that "would not exist if their underlying open source core didn't exist," and argues open-core will progressively replace closed SaaS because open source wins developer adoption ([Joseph Jacks / OSS Capital interviews and Open Core Summit](https://opensourceunderdogs.com/open-core-summit-the-conference-for-coss-with-joseph-jacks/); [TechCrunch profile](https://techcrunch.com/2024/10/20/joseph-jacks-bets-on-open-source-startups-a-paradox-of-philanthropy-and-capitalism/)). **[Evergreen]** thesis, contested.

**Revenue mechanics:** the open project is your zero-CAC marketing funnel. Conversion of free community to paid is typically well under 1%, so the community must be huge. **Gross margin:** 75–85% (open-core), 60–75% (hosting). **Capital needs:** high in time — years of community building before monetization. **Defensibility:** community, ecosystem, and being the canonical maintainer. But clouds can strip-mine you — AWS launching a managed version of your own project (which hit Elastic, MongoDB, and Redis, driving all three to restrictive licenses). **[2026]**

**Failure modes:** monetizing too early and alienating the community; monetizing too late and running out of money; the AWS strip-mine; drawing the open/paid line wrong (if the free version is enterprise-complete, nobody pays).

**Winners:** Red Hat ($34B acquisition), MongoDB, GitLab, Databricks, HashiCorp (acquired by IBM). **Failures:** RethinkDB is the canonical case of huge adoption with no revenue. The YC-backed open-source database was genuinely loved by developers, yet announced in October 2016 that it "had been unable to build a sustainable business" and shut down; the code survived only because the Cloud Native Computing Foundation bought the rights and re-licensed it under Apache 2.0 ([RethinkDB](https://en.wikipedia.org/wiki/RethinkDB)). Cofounder Slava Akhmechet's post-mortem essay "Why RethinkDB failed" ([discussed at length on Hacker News](https://news.ycombinator.com/item?id=13421608); the original defmacro.org host has since gone offline) is required reading: they optimized for correctness and elegance in a market where developers expected databases to be free, and "good enough" tools with better go-to-market won the paying customers.

**Fit criteria:** choose when your buyer is a developer, adoption friction is the main enemy, and you can define a crisp line between community needs and enterprise needs.

---

### 2.11 API-as-product

**How it works:** The product is a programmable building block other software calls: Stripe (payments), Twilio (telephony), OpenAI/Anthropic (intelligence). Priced per call/usage. ("API" = Application Programming Interface — a way for one program to use another program's capabilities.)

**Revenue mechanics:** usage-based (§2.2 mechanics apply), with the special property that your revenue is embedded in *customers' products* — you grow when they grow. **Gross margin:** 70–85% for pure-software APIs; **[2026]** for AI-model APIs, margins are structurally lower (inference compute on every call). **Capital needs:** moderate for pure-software APIs — the costs are engineering, developer relations, and enough infrastructure reliability that other companies will bet their product on you (an API that goes down takes its customers' products down with it, so "good enough" uptime isn't an option). For fintech APIs like Stripe, add the regulatory and fraud costs of §2.5. **[2026]** For AI-model APIs, capital needs are extreme — training frontier models costs billions before the first dollar of revenue. That is why OpenAI and Anthropic raised more pre-revenue capital than almost any startups in history, and why "become a model provider" is not a realistic first-startup plan. **Defensibility:** developer experience ("DX" — how pleasant your API is to build on), documentation, and switching costs. But thin-wrapper APIs are trivially substitutable, and AI APIs have made "swap the provider behind one interface" a standard practice.

**Failure modes:** being a thin wrapper over someone else's capability; platform dependence (your API resells another API); a single big customer building in-house.

**Winners:** Stripe, Twilio, OpenAI/Anthropic. **Failures:** Clearbit-era data APIs commoditized; many "GPT-wrapper" APIs of 2023 evaporated when the model providers shipped the feature.

**Fit criteria:** choose when many companies need the same hard capability and you can be *meaningfully* better at it than they'd be in-house.

---

### 2.12 Services-to-product

**How it works:** Start as a consulting/agency business (custom work, paid by the hour/project), notice you're building the same thing repeatedly, and productize it into software. Palantir ran quasi-services for years ("forward-deployed engineers" — its engineers who work on-site inside customer organizations) before productizing. Many vertical-SaaS companies ("vertical SaaS" = software built for one specific industry — dentists, trucking, restaurants — rather than a horizontal function like email or accounting that every industry uses) started as agencies serving that industry.

**Tradeoffs:** services revenue is immediate and non-dilutive (customers fund you, not investors) and gives unmatched customer intimacy. But gross margins are 30–50%, revenue doesn't recur automatically, and it scales only with headcount. Investors value $1 of services revenue at a fraction of $1 of SaaS ARR. The trap: services demand always feels more urgent than product investment, so most firms never escape ("the services treadmill"). **[Evergreen]**

**Gross margin:** 30–50% as a services firm; the entire game is migrating the revenue mix toward a 70%+-margin product over time. **Capital needs:** the lowest of any model on this list — customers fund you from day one, which is why this is the classic bootstrapper's path (bootstrapping = building without outside investment) and the most credible non-venture route here. **Defensibility:** low while you're services (your key assets walk out the door every evening, and clients can hire your competitors tomorrow). Once productized, you get whatever moat the product itself earns — plus something rare: years of embedded domain knowledge from living inside customers' workflows, which is exactly what made Palantir's and Mailchimp's products hard to copy. **[Evergreen]**

**Failure modes:** the services treadmill (billable client work always beats product investment in urgency, so the product never ships); building a product only your existing consulting clients want; hiring for billable utilization instead of product engineering; and the transition-specific killer — *half*-productizing, so you carry software-level R&D costs on services-level margins while investors discount you as "an agency with a demo." **[Evergreen]**

**Winners:** Mailchimp — started as a side project inside Ben Chestnut and Dan Kurzius's Atlanta web-design agency (the Rocket Science Group), productized email marketing for small businesses, took no venture money, and sold to Intuit for ~$12B in 2021, the largest bootstrapped-software exit ever. Basecamp (37signals) — a Chicago web-design shop that built a project-management tool to run its own client work, released it as a product in 2004, and shut down the agency side entirely ([37signals history](https://en.wikipedia.org/wiki/37signals)). Palantir — ran quasi-services with forward-deployed engineers for a decade before Foundry productized the repeated pattern. **Failures:** Pivotal — the famous Pivotal Labs consultancy productized into Pivotal Software (Cloud Foundry) and IPO'd in 2018 (IPO = initial public offering, listing shares on the stock market) at a ~$3.9B valuation. It then collapsed when product sales stalled against Kubernetes (Google's open-source infrastructure software, which became the free industry standard); VMware absorbed it in 2019 at $2.7B — proof that a beloved services brand doesn't guarantee the *product* wins its market ([Pivotal Software](https://en.wikipedia.org/wiki/Pivotal_Software)). And the silent majority: most agencies that attempt the jump never ship a product that outsells their billable hours.

**[2026] twist:** AI has revived this path as a hot strategy — "AI-enabled services" or "tech-enabled rollups" — because agents can push service delivery margins from 35% toward 60–70%, making a services business behave financially like software. Several 2025–26 funds explicitly back buying or building services firms and automating them. This is genuinely new and unproven at scale; treat claims skeptically. The cautionary tale already exists: Builder.ai raised over $445M (Microsoft among the backers, ~$1.5B peak valuation) selling "AI-powered" app development that in practice leaned heavily on human labor — its own 500+ employees plus outsourced "capacity partners" in India and Ukraine who did the vast majority of the build work. (A viral claim that it was exactly "700 engineers pretending to be AI" is disputed and traces to social media, not the reporting — the documented story is damning enough without it.) In March 2025 Bloomberg reported the company had inflated revenues, having forecast its 2024 revenue at roughly four times what it turned out to be. Its lender then seized most of its cash, and it filed for bankruptcy in May 2025 ([Rest of World](https://restofworld.org/2025/builderai-ai-apps-downfall/)). If the automation is fake, you don't have a software company — you have a low-margin services firm burning venture-scale cash. See `10-ai-era.md`.

**Fit criteria:** choose when you need revenue now, the domain requires earned trust, and you have the discipline to cap services and reinvest in product.

---

### 2.13 The 2026 AI-native models

This is the frontier, and the norms are still being written. Four models plus one big debate. Everything here is **[2026]** unless marked.

**(a) Per-seat AI copilot.** Classic seat SaaS with AI inside: GitHub Copilot ($10–39/seat/month), Microsoft 365 Copilot ($30/seat/month). Familiar to buyers and predictable — but it inherits seat pricing's flaw (price scales with headcount, while AI's value is *output*), and inference costs mean margins run below classic SaaS. Multiple 2026 analyses converge on AI-product gross margins of roughly 50–60% versus 80–90% for traditional SaaS, with inference the dominant COGS line ([SaaS Mag on AI COGS compression](https://www.saasmag.com/ai-cogs-saas-gross-margin-compression/); data from ICONIQ (a growth-equity firm whose annual SaaS benchmark reports are an industry standard) shows AI margins improving as inference gets cheaper). The mitigating trend: per-token model costs have fallen fast every year, so today's margin problem may partly age out — but usage per user grows too.

**Capital needs:** low-to-moderate — the same people costs as seat SaaS, plus a real inference bill that scales with usage (free trials of AI features burn actual GPU money, unlike free trials of storage). **Defensibility:** comes from distribution and workflow ownership, *not* from the AI itself — a copilot that thinly wraps a foundation model can be copied in a weekend, including by the model providers. GitHub Copilot wins on distribution (every developer is already on GitHub), not model quality. **Famous failures:** Jasper is the canonical case. The AI-copywriting copilot hit a $1.5B valuation in October 2022; then ChatGPT launched weeks later and gave away its core capability for free. By mid-2023 Jasper had laid off staff and cut its own internal valuation, and the broader 2023 "GPT-wrapper" cohort of copilots evaporated the same way. The lesson: if your copilot's value is the model, you don't have a product — you have a feature waiting to be shipped by someone bigger.

**(b) Usage-based: tokens and credits.** Sell "credits" consumed by AI actions (Cursor, many agent products). Kyle Poyar (author of Growth Unhinged, the most-followed analyst of software pricing) called credit pricing *the* defining pricing innovation of 2025: the number of tracked companies selling credits grew 126% year-over-year — from 35 to 79 companies in the PricingSaaS 500 Index, a tracker of pricing-page changes across 500 SaaS companies, whose data Poyar's coverage draws on — alongside visible customer backlash when credit schemes felt opaque or ran out mid-month ([Growth Unhinged pricing coverage](https://www.growthunhinged.com/t/pricing)). Credits abstract volatile underlying costs and let you reprice quietly — but customers hate math they can't predict. See `03-pricing.md` for mechanics.

**Gross margin:** 50–70% — better aligned to inference costs than flat seats, since heavy users pay more. **Capital needs:** moderate — prepaid credits are actually cash-flow-friendly (customers pay before consuming), but you still fund the inference behind generous starter allowances. **Defensibility:** the pricing scheme itself is zero moat — anyone can sell credits; defensibility must come from the product underneath. **Famous failures/warnings:** no dead unicorn yet (unicorn = a startup valued at $1B or more), but the cautionary episode everyone cites is Cursor's mid-2025 repricing — moving users from a flat request allowance to compute-based credit consumption triggered enough public fury that the company apologized and issued refunds. And Jasper (see (a)) sold word-credits before its fall: credits didn't save a product whose underlying capability got commoditized. The rule: credits amplify whatever trust you have — including distrust.

**(c) Outcome-based: pay per result.** Charge only when the AI achieves a defined result. The two canonical cases:
- **Intercom Fin:** $0.99 per *outcome* (Intercom's current term — it launched as "per resolution") — you pay only when the AI support agent actually delivers: the customer confirms their issue is resolved, doesn't ask for more help after Fin responds, or Fin completes a defined workflow; you're charged at most once per conversation ([Intercom pricing](https://www.intercom.com/pricing); [Fin resolution definition](https://fin.ai/help/en/articles/10772642-fin-ai-agent-resolutions)).
- **Sierra** (Bret Taylor's company): a pre-negotiated price per autonomous resolution; escalations to humans are free. Taylor argues outcome-based pricing is the future of software: you're selling resolved tickets, not seats or API calls ([Bret Taylor on Sierra's outcome pricing, Cheeky Pint interview](https://cheekypint.substack.com/p/bret-taylor-of-sierra-on-ai-agents); [Sequoia Training Data podcast](https://sequoiacap.com/podcast/training-data-bret-taylor/)). The model is working commercially: Sierra passed $100M ARR in November 2025 — about seven quarters after launch — reported $150M ARR as of early February 2026, and raised $950M at a valuation above $15B in May 2026 ([TechCrunch, May 2026](https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/)). Third-party analyst Sacra estimates ARR had reached roughly $200M by mid-2026, but that's an extrapolation, not a company-reported number ([Sacra profile](https://sacra.com/c/sierra/)). **[2026]**

**Worked example of why this sells:** a human-handled support ticket costs a company $10–20, mostly labor. An AI vendor charging $1–3 per resolution lets the customer bank $8–17 of savings per ticket while the vendor earns perhaps 5–10× its inference cost. Price is anchored to *labor value*, not software comparables. The hard parts: you carry the performance risk (no resolution, no revenue), attribution must be crisply measurable, and revenue is volatile. Outcome pricing only works where the outcome is discrete, countable, and hard to dispute — support resolutions yes, "better strategy" no.

**Capital needs:** moderate-to-high — you pay inference on every *attempt*, including the failed ones that earn nothing, and enterprise sales cycles apply on top. **Defensibility:** potentially strong — a performance-data flywheel (every resolution makes the agent better at resolving, which competitors without your traffic can't replicate) plus deep workflow integration; weak if the outcome is generic and the customer can A/B-test you against a rival monthly. **Famous failures:** none at unicorn scale yet — the model is only a couple of years old — but the predictable fight is attribution ("did the AI *really* resolve that, or did the customer give up?"), and the agent-washing collapses under (d) below show exactly what happens when outcome claims outrun what the system actually does.

**(d) Agents priced against labor budgets.** The boldest model: sell a "digital employee" for a flat monthly fee benchmarked to salary, not software. Examples: 11x (AI sales rep), Harvey (legal). Poyar's agent-pricing framework lays out the spectrum — per agent (an "FTE replacement"; FTE = full-time equivalent, i.e., one human employee's worth of work), per action, per workflow, per outcome — and notes the per-agent model's key advantage: it taps headcount budgets, which are roughly 10× larger than software budgets, while its weakness is low differentiation against cheaper copycats ([Growth Unhinged, "A new framework for AI agent pricing"](https://www.growthunhinged.com/p/ai-agent-pricing-framework)). Tunguz frames the same shift from first principles: when an agent is ~3× as productive as a human seat, sellers must choose between 3× seat prices, compute-style usage pricing, or pay-for-performance — and he calls this the biggest repricing opportunity since Salesforce's "No Software" attack on licenses ([Tunguz, "No SaaS! How AI Agents Will Change Software Pricing"](https://tomtunguz.com/ai-agent-pricing/)).

**Gross margin:** wide-ranging and often opaque — 40–75% depending on how much hidden human labor backstops the "agent." **Capital needs:** moderate-to-high — enterprise sales, inference, and (very often) humans-in-the-loop the pitch deck doesn't mention. **Defensibility:** low against copycats unless you own proprietary workflow data, integrations, or accuracy the customer can measure. "We replace an SDR" (Sales Development Representative — the junior salesperson whose job is cold outreach and booking meetings for the closers; the most commoditized role in sales, hence the first one AI startups targeted) is a pitch anyone can make, and dozens did in 2024–25. **Famous failures:** this sub-model already has a graveyard. 11x — the AI-SDR poster child — was the subject of a March 2025 TechCrunch investigation reporting that it counted churned trial customers in its ARR, displayed logos of companies (ZoomInfo, Airtable) that denied being customers, and had churn estimated at 70–80% ([OnlyCFO analysis](https://www.onlycfo.io/p/ai-company-accused-of-fraud); [summary of the controversy](https://aisdr.com/blog/11x-techcrunch/)) — the defining "agent-washing" cautionary tale. Olive AI sold hospitals "digital employees" for back-office automation, raised over $850M at a ~$4B peak valuation, and shut down in 2023 when the automation underneath couldn't cash the labor-replacement checks it had written. Adept, one of the original AI-agent labs, raised over $400M and was effectively acqui-hired by Amazon in mid-2024 ("acqui-hire" = an acquisition made mainly to get the team, not the product or business — a soft landing that returns little or nothing to investors) without ever finding a business model. The pattern: labor-anchored revenue is easy to *book* (the ROI story sells itself) and brutal to *keep* unless the agent genuinely does the job — churn is the truth serum.

**(e) The "seat collapse" debate.** The bear case for SaaS: if agents do the work, headcount shrinks, and per-seat revenue shrinks with it — the model that built a $300B industry deflates. The bull case: seats persist because buyers *want* predictable bills, and hybrid structures absorb the change. The empirical 2026 answer so far is hybrid: Poyar's 2026 State of B2B Monetization survey (230+ software companies) found **37% use hybrid pricing** — a predictable base subscription plus variable consumption — the most common structure by far, with pure outcome pricing still rare ([Poyar on why hybrid already won](https://www.revenuecreator.com/p/why-hybrid-pricing-already-won-the-ai-era-kyle-poyar-growth-unhinged)). Practical takeaway for you: don't bet your company on pure outcome pricing on day one; bet on *value-anchored hybrid* — a platform fee for predictability plus a usage or outcome component for upside. **[2026]**

---

## Part 3: Comparison table

| Model | Gross margin | Sales motion | Time to first revenue | Capital intensity | Defensibility at scale |
|---|---|---|---|---|---|
| Seat-based B2B SaaS | 75–90% | Inside sales / self-serve | Months | Low-Med | Med (switching costs) |
| Usage-based infra | 60–80% | Bottom-up + sales | Months | Med | Med-High (data gravity) |
| Freemium / PLG | 70–85% | Self-serve, sales-assist later | Months (rev lags usage) | Med | Med (team lock-in) |
| Enterprise sales-led | 70–85% | Field sales, 6–12 mo cycles | 1–2 years | High | High (integration, compliance) |
| Transactional / take-rate | 40–70% (net) | Partnerships, embedded | 1–2 years | High | High (money-flow lock-in) |
| Marketplace | 50–70% of net rev | Two-sided growth ops | 1–3 years to liquidity | High | Highest (network effects) |
| Consumer subscription | 60–85% | Performance marketing, virality | Months | Med-High | Low-Med (habit, brand) |
| Advertising | 60–80% at scale | None until huge, then ad sales | 3–7 years | Extreme | Highest at scale, none before |
| Hardware (+SaaS) | 20–40% (HW) / 80% (attach) | Direct + channel | 1–3 years | Extreme | High (physical install base) |
| Open-source commercial | 60–85% | Community → enterprise sales | 2–4 years | Med-High | Med-High (community, ecosystem) |
| API-as-product | 70–85% (lower for AI) | Developer-led | Months | Med | Med (DX, switching costs) |
| Services-to-product | 30–50% → 70%+ | Founder relationship sales | Immediate | Low | Low until productized |
| AI copilot (per-seat) | 50–60% | Same as seat SaaS | Months | Low-Med | Low-Med (distribution, not the AI) |
| AI credits / usage | 50–70% | Self-serve + sales | Months | Med | Low-Med (product, not the pricing) |
| AI outcome-based | 50–80%, volatile | Value-based enterprise sales | Months-year | Med-High | Med (performance data flywheel) |
| AI agent (per-agent / FTE) | 40–75%, opaque | Enterprise, sold against labor budget | Months | Med-High | Low-Med (copycats; workflow data helps) |

(Margins and timelines are directional **[2026]** benchmarks, not laws; the *relative ordering* is **[Evergreen]**.)

Sales-motion terms in the table, decoded: **self-serve** = the customer signs up and pays with a credit card, no salesperson involved; **inside sales** = salespeople who sell remotely by phone/video/email — cheaper per rep, suited to deals of roughly $5K–100K/year; **field sales** = salespeople who travel to meet buyers in person, run demos and dinners, and work six-to-seven-figure deals over months — the most expensive motion, only affordable when contracts are large. **[Evergreen]**

---

## Part 4: Decision framework — choosing a model for your idea

Work through these questions in order. **[Evergreen]**

1. **Who feels the pain, and who controls the budget?** Individual → PLG/consumer. Team → seat SaaS or PLG. Executive with a P&L problem (P&L = profit & loss statement; an executive who "owns a P&L" is personally accountable for a division's revenue and costs, and buys anything that improves those numbers) → enterprise or outcome-based. If the budget you're tapping is *labor* rather than software, price against labor (§2.13d).
2. **How does value scale?** With number of humans → seats. With volume of activity → usage. With transactions → take-rate. With a countable result → outcomes. Mispricing the value metric is the most common self-inflicted wound; see `03-pricing.md`.
3. **Can the user adopt it alone in 10 minutes?** Yes → PLG is available to you (the cheapest distribution in software). No (needs integration, compliance, data migration) → sales-led; budget for it.
4. **Is there a two-sided cold-start problem?** If yes, you're a marketplace whether you like it or not — plan the liquidity-first wedge (one city, one category) before anything else.
5. **What gross margin does the model force?** Investors underwrite margins, not dreams: a 30%-margin business needs 3× the revenue of a 90%-margin business for the same gross profit. If your model traps you below ~50%, you need a credible path up (attach software, automate the service) or a non-venture funding plan — see `05-fundraising.md`.
6. **How much capital does the model demand before truth?** Ads and marketplaces require years of subsidy; SaaS and services tell you the truth in months. Match the model to your risk tolerance and fundraising reality.
7. **Where's the moat once it works?** Rank: network effects > embedded money/data flows > workflow lock-in > brand > features. If your model choice forecloses moats (e.g., pure services), know you're choosing a lifestyle business or a stepping stone.

Default advice for a technical first-time founder in 2026: **B2B, hybrid-priced (base platform fee + usage/outcome component), sold to a budget you can name, with gross margins ≥60% and first revenue within 6 months.** Deviate knowingly, not accidentally.

---

## Part 5: Transitions and hybrids

Companies change models more often than the mythology suggests — but transitions are surgery, not pivots of convenience. **[Evergreen]**

- **License → SaaS:** Adobe (2012–13) moved Creative Suite from $1,800 boxes to ~$50/month subscriptions; revenue *dropped* for two years, then compounded past all prior peaks. Lesson: model transitions have a painful J-curve (revenue dips before it climbs, tracing a J shape); you need conviction and cash.
- **Services → product:** Palantir spent a decade with forward-deployed engineers before Foundry productized the pattern; margin expanded as software share grew.
- **Free/ads → subscription:** YouTube and Spotify layered subscriptions on ad bases; the New York Times converted an ad business into a 10M+ subscriber business.
- **Seat → usage:** HubSpot, Salesforce, and Zendesk have all added consumption/credit components 2024–26 as AI features made per-seat economics leaky ([Growth Unhinged's pricing-change tracking](https://www.growthunhinged.com/t/pricing)). **[2026]**
- **Hardware → hardware+services:** Apple's Services line (the App Store's 30% rake, iCloud, Music) now produces a huge share of gross profit on top of a hardware install base — the model-stacking endgame.
- **Open source → restrictive license:** Elastic, MongoDB, and Redis all retreated from pure open source under cloud strip-mining pressure — a transition that trades community goodwill for survival. **[2026]**

**Hybrids are the norm, not the exception:** Amazon is retail + marketplace + ads + AWS; Shopify is SaaS + payments take-rate (payments now the larger revenue line); Costco is retail at near-zero margin + a membership subscription that is most of its profit. The **[2026]** synthesis, per Poyar's survey data, is that the modal AI-era software company is *deliberately hybrid*: a subscription floor for predictability, consumption or outcomes for value capture. Design your v1 pricing so a second component can be added without a repricing revolt.

---

## Sources

- Bill Gurley, ["A Rake Too Far: Optimal Platform Pricing Strategy"](https://abovethecrowd.com/2013/04/18/a-rake-too-far-optimal-platformpricing-strategy/) — Above the Crowd (fetched and read)
- Anu Hariharan, ["Nine Business Models and the Metrics Investors Want"](https://www.ycombinator.com/library/8E-nine-business-models-and-the-metrics-investors-want) — YC Startup Library
- Ben Thompson, ["Defining Aggregators"](https://stratechery.com/2017/defining-aggregators/) — Stratechery (fetched and read)
- Kyle Poyar, ["A new framework for AI agent pricing"](https://www.growthunhinged.com/p/ai-agent-pricing-framework) — Growth Unhinged (fetched and read)
- Kyle Poyar, [Growth Unhinged pricing archive](https://www.growthunhinged.com/t/pricing) and [PLG benchmarks guide](https://www.growthunhinged.com/p/your-guide-to-plg-benchmarks)
- Kyle Poyar interview, ["Why hybrid pricing already won the AI era"](https://www.revenuecreator.com/p/why-hybrid-pricing-already-won-the-ai-era-kyle-poyar-growth-unhinged) — Revenue Creator
- Tomasz Tunguz, ["No SaaS! How AI Agents Will Change Software Pricing"](https://tomtunguz.com/ai-agent-pricing/) (fetched and read) and ["Per Seat or Per Use Pricing"](https://tomtunguz.com/seat-vs-usage-based-pricing/)
- Bret Taylor on Sierra's outcome-based pricing — [Cheeky Pint interview](https://cheekypint.substack.com/p/bret-taylor-of-sierra-on-ai-agents), [Sierra podcast page](https://sierra.ai/resources/podcasts/bret-taylor-of-sierra-on-ai-agents-outcome-based-pricing-and-the-openai-board), [Sequoia Training Data](https://sequoiacap.com/podcast/training-data-bret-taylor/)
- Intercom, [Fin pricing](https://www.intercom.com/pricing) and [Fin outcomes/resolutions definition](https://fin.ai/help/en/articles/10772642-fin-ai-agent-resolutions)
- a16z, [Required Reading for Marketplace Entrepreneurs](https://a16z.com/required-reading-for-marketplace-entrepreneurs/) and [Marketplaces and Network Effects](https://a16z.com/marketplaces-and-network-effects/)
- Andrew Chen, [Required reading for marketplace startups: the 20 best essays](https://andrewchen.com/marketplace-startups-best-essays/)
- Joseph Jacks / OSS Capital on COSS — [Open Source Underdogs interview](https://opensourceunderdogs.com/open-core-summit-the-conference-for-coss-with-joseph-jacks/), [TechCrunch profile (Oct 2024)](https://techcrunch.com/2024/10/20/joseph-jacks-bets-on-open-source-startups-a-paradox-of-philanthropy-and-capitalism/)
- OpenView Partners, [Product Benchmarks reports](https://openviewpartners.com/2022-product-benchmarks/) (freemium conversion data)
- [SaaS Mag, "The AI COGS Problem: SaaS Gross Margin Compression"](https://www.saasmag.com/ai-cogs-saas-gross-margin-compression/) (AI vs. SaaS gross margin benchmarks; corroborated by Bessemer and ICONIQ data cited therein)
- TechCrunch, ["Sierra raises $950M as the race to own enterprise AI gets serious"](https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/) (May 2026) and ["Bret Taylor's Sierra reaches $100M ARR in under two years"](https://techcrunch.com/2025/11/21/bret-taylors-sierra-reaches-100m-arr-in-under-two-years/) (Nov 2025); [Sacra, Sierra profile](https://sacra.com/c/sierra/) (fetched and read)
- Coverage of TechCrunch's March 2025 investigation into 11x — [OnlyCFO, "AI Company Accused of Fraud?"](https://www.onlycfo.io/p/ai-company-accused-of-fraud); [AiSDR summary](https://aisdr.com/blog/11x-techcrunch/)
- Rest of World, ["Inside the collapse of Builder.ai"](https://restofworld.org/2025/builderai-ai-apps-downfall/) (May 2025)
- [Spotify financials, stockanalysis.com](https://stockanalysis.com/stocks/spot/financials/) (gross margin history; fetched and read)
- Apple 10-K segment data (Products vs. Services gross margin, FY2025) — as reported via Statista and stock-analysis-on.net
- Wikipedia, [37signals](https://en.wikipedia.org/wiki/37signals) and [Pivotal Software](https://en.wikipedia.org/wiki/Pivotal_Software) (services-to-product histories)
- Wikipedia, [Nirvanix](https://en.wikipedia.org/wiki/Nirvanix), [Powa Technologies](https://en.wikipedia.org/wiki/Powa_Technologies), and [RethinkDB](https://en.wikipedia.org/wiki/RethinkDB) (named failure cases; each fetched and read July 2026)
- Slava Akhmechet, "Why RethinkDB failed" — original defmacro.org post now offline; [Hacker News discussion thread](https://news.ycombinator.com/item?id=13421608) (fetched and read)

*Verification note: benchmark figures (freemium conversion ~2.6% median, AI gross margins ~50–60%, hybrid pricing at 37% of companies, Sierra's $15B+ valuation and $150M reported / ~$200M estimated ARR, Spotify's ~32% gross margin) were checked against July 2026 web sources but are survey- and press-derived — treat them as directional, not audited. The Builder.ai account (500+ employees plus outsourced capacity partners; 2024 revenue forecast ~4× actual per Bloomberg) and the Intercom "$0.99 per outcome" terminology were re-verified against the cited sources in July 2026. The credit-pricing 126% figure originates from the PricingSaaS 500 Index (35 → 79 companies), reported through Growth Unhinged's coverage. The Jasper, Olive AI, Adept, and Mailchimp accounts are drawn from widely corroborated 2021–2024 reporting (TechCrunch, Axios, WSJ) and are summarized here without single-link citations.*
