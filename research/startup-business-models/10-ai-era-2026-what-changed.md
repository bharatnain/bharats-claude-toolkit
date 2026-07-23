# The 2026 AI Era — what changed and what did not

**Why this matters to you:** You are starting a company in the middle of the biggest platform shift since mobile. Everyone around you talks as if the old rules are dead. Some are; most are not. If you can't tell which is which, you fail one of two ways. Either you build a 2019-style company and get lapped by a five-person team shipping daily, or you chase 2026 hype and build something a model update erases. This document is the sorting mechanism. Every claim in this library carries a tag: **[Evergreen]** (true for decades, will stay true) or **[2026]** (true right now, may expire). Read this one before you weight anything else you hear from investors, Twitter, or your successful friends. Most bad startup advice in 2026 is evergreen advice and current advice mislabeled as each other.

Quick jargon key you'll need throughout (each term is also defined where it first appears):

- **ARR** = annual recurring revenue — the annualized value of your subscriptions.
- **TAM** = total addressable market — the theoretical maximum revenue if you owned an entire market.
- **PMF** = product-market fit — the state where a market pulls the product out of you.
- **Foundation model** = a giant general-purpose AI model (GPT, Claude, Gemini, Llama) that others build on.
- **Inference** = running a trained model to get outputs — what you pay per use.
- **Moat** = a durable structural advantage that protects your profits from competitors.
- **Unicorn** = startup slang for a private company valued at $1 billion or more.
- **Series A / B / C** = the lettered sequence of venture funding rounds a startup raises as it grows. Seed comes first, then A, then B, and so on. Each round is typically bigger and at a higher valuation.
- **Gross margin** = the percentage of each revenue dollar left after the direct costs of delivering your product (servers, model inference, support). Software historically runs 80–90%+, which is much of why investors love it.
- **Due diligence** (or just "diligence") = the homework an investor does before wiring money: verifying your metrics, calling your customers, and probing your risks.

---

## The master table: changed vs. unchanged

| Area | What changed **[2026]** | What did not change **[Evergreen]** |
|---|---|---|
| **Starting** | Tiny teams ship in days; ~10 people can reach $10M ARR; code is majority AI-written for many startups | You still have to pick a real problem, and someone still has to want the thing |
| **Moats** | Day-one product defensibility is near zero; "wrappers" both dismissed and vindicated; speed itself now treated as a moat | Moats are *earned over years*, not designed on day one — this was true for SaaS in 2010 too |
| **Business models** | Selling completed work/outcomes, not software seats; TAM expands from software budgets to labor budgets | Price to value; unit economics must eventually work |
| **Funding** | AI takes roughly half of all VC dollars (estimates run ~48–61%); fastest-growing cohort ever; brutal churn scrutiny behind the hype | Power law returns; investors fund lines not dots; revenue quality > revenue quantity |
| **Competition** | "What if OpenAI does this?" is a standard diligence question; foundation labs move up the stack | Incumbents are beaten by 10x-better products or new segments — same as every prior wave |
| **Platform risk** | Model prices deflate ~10x/year — both tailwind and threat; model-layer dependence is a real risk | Building on someone else's platform has always been a devil's bargain (Windows, iOS, Facebook) |
| **Users & PMF** | Faster to first users, faster to false positives | Talk to users, retention defines PMF, make something people want |

Now each row in depth.

---

## 1. What changed about STARTING

### Tiny teams, absurd revenue **[2026]**

The single most-cited data point of this era comes from Y Combinator (YC — the most famous startup accelerator; see `06-investors-accelerators.md`). YC reported that its Winter 2025 batch grew, **in aggregate, 10% per week**. CEO Garry Tan: "It's not just the number one or two companies — the whole batch is growing 10% week on week. That's never happened before in early-stage venture" ([CNBC, "Y Combinator startups are fastest growing, most profitable in fund history because of AI," March 2025](https://www.cnbc.com/2025/03/15/y-combinator-startups-are-fastest-growing-in-fund-history-because-of-ai.html)).

Here is the worked math on what 10% weekly compounding means. 1.10^52 ≈ **142x in a year**. A company doing $2,000/week in revenue in January would be doing ~$284,000/week — ~$14.8M annualized — by the following January, *if* it sustained that rate. Almost nobody does for a full year. The point is the slope, not the destination.

The same article carries the pattern behind the headline. Tan said companies in the batch were "reaching as much as $10 million in revenue with teams of less than 10 people," and that "you don't need a team of 50 or 100 engineers." That is an aggregate claim, so here are **named, verified companies at roughly that scale** — teams of a few dozen people or fewer hitting $10M+ ARR, and far beyond:

- **Lovable** — the Swedish "describe an app in English, get a working app" tool — went from **zero to $10M ARR in its first two months** after launching in late November 2024, per the company's own retrospective ([Lovable blog, "Zero to $10M ARR in 2 months," Jan 2025](https://lovable.dev/blog/2025-01-29-zero-to-10m-arr-in-2-months)). Early-2025 coverage widely put the team at roughly 15 people at that point (that headcount comes from contemporaneous press, not the primary sources). Eight months in, it crossed **$100M ARR** with **45 full-time employees** — faster than any software company on record, per its investors — and became a **unicorn**, a private company valued at $1B+ ([TechCrunch, Jul 2025](https://techcrunch.com/2025/07/23/eight-months-in-swedish-unicorn-lovable-crosses-the-100m-arr-milestone/)). It then doubled to **$200M ARR four months later** ([TechCrunch, Nov 2025](https://techcrunch.com/2025/11/19/as-lovable-hits-200m-arr-its-ceo-credits-staying-in-europe-for-its-success/)).
- **Bolt.new (company name: StackBlitz)** — an in-browser AI app builder — hit **$4M ARR in only four weeks** after its October 2024 launch, then **$20M in three months, and ~$40M ARR in five months**. At that point the team was still **fewer than 40 employees, with fewer than 10 in go-to-market (sales/marketing) roles**. The kicker: StackBlitz had spent *seven years* as a near-dead dev-tools company before pointing its tech at AI code generation. CEO Eric Simons calls it a "seven-year overnight success" ([Growth Unhinged interview with Simons](https://www.growthunhinged.com/p/boltnew-growth-journey)).
- **Gamma** — AI-generated presentations ("the AI PowerPoint killer") — passed **$100M ARR with ~50 employees** and has been **profitable for 2+ years**. It raised a **Series B** (the second lettered round of venture funding — see the jargon key) at a **$2.1B valuation**, having previously raised only $23M ([TechCrunch, Nov 2025](https://techcrunch.com/2025/11/10/ai-powerpoint-killer-gamma-hits-2-1b-valuation-100m-arr-founder-says/)). That works out to roughly **$2M of revenue per employee**.

The same leverage pattern shows up at later, larger stages:

- **Cursor (company name: Anysphere)** — the AI code editor — crossed **$1B+ in ARR** by late 2025 with roughly **300 employees**, raising at a **$29.3B valuation** ([CNBC, Nov 2025](https://www.cnbc.com/2025/11/13/cursor-ai-startup-funding-round-valuation.html)). Earlier in its run it was doing hundreds of millions of ARR with a few dozen people. Several 2026 trackers claim ~$2B ARR now, but those figures are estimates I could not verify against a primary source, so treat them as directional.
- **Midjourney** — the image-generation company — is the canonical bootstrapped case: on the order of $200M+ revenue with ~40 people and **$0 of outside funding**. (Caveat: Midjourney publishes no numbers. The $200M figure traces to The Information's 2023 reporting and has been widely repeated since, but the company is private and unaudited, so treat it as directional.)

The **[Evergreen]** principle underneath: revenue per employee has always been the cleanest measure of business quality. What's **[2026]** is the ceiling. [Sifted's "Tiny teams, big revenue"](https://sifted.eu/articles/tiny-teams-big-revenue) cites Cursor generating "an 'amazing' $3.1m in revenue per employee" at the $1B-valuation stage. A *good* traditional SaaS company runs on the order of $200–400K per employee, so the AI-native leaders are roughly **10x** that — because the product itself does work that used to require headcount.

### Vibe coding and compressed build time **[2026]**

"Vibe coding" — a term Andrej Karpathy coined in February 2025 for letting AI write essentially all the code while you direct at the level of intent — went from joke to operating reality in about a month. Garry Tan, March 2025: ["For 25% of the Winter 2025 batch, 95% of lines of code are LLM generated. That's not a typo. The age of vibe coding is here."](https://x.com/garrytan/status/1897303270311489931) The practical consequence: the build phase of a startup, which used to take 6–12 months, now takes days to weeks. YC's Lightcone podcast (the partners' podcast — Tan, Diana Hu, Harj Taggar, Jared Friedman) has an entire episode titled "Vibe Coding Is The Future" arguing that founder leverage per engineer has permanently changed.

### The catch: lower cost to launch means faster competition **[2026]**

This is the part first-time founders miss. If *you* can build it in a weekend, **so can everyone else**. The barrier that used to protect a shipped product — the 9 months a competitor would need to replicate it — is gone. [Forbes, "VCs Rethink Startup Moats As AI Compresses Time To Build" (March 2026)](https://www.forbes.com/sites/josipamajic/2026/03/31/vcs-rethink-startup-moats-as-ai-compresses-time-to-build/) documents investors explicitly repricing this. (Note: Forbes blocks automated access, so that piece could not be re-verified for this document — but the same repricing is independently documented in the SignalFire and Elad Gil sources in section 2.) The strategic conclusion, which sets up the whole moats section: **when building is cheap, the value migrates to everything that isn't building** — distribution, data, workflow depth, brand, and sheer cadence of shipping.

The **[Evergreen]** counterweight: cheap building has *never* meant easy company-building. The dot-com era's "anyone can make a website" and the 2010s' "AWS + open source means anyone can make a SaaS app" produced the same panic and the same resolution. The product was never the hard part for long. The hard parts — finding a burning problem, winning distribution, retaining users — are exactly where they always were.

---

## 2. What changed about MOATS — the "GPT wrapper" debate in full

### Why wrappers were dismissed **[2026, argument originated 2023]**

A **"GPT wrapper"** is derisive shorthand for a startup whose product is a thin user interface over someone else's foundation model. You type into their box; they forward it to OpenAI or Anthropic with a clever prompt and mark up the answer. The dismissal case, circa 2023–2024, ran: (1) no proprietary technology; (2) the model provider can absorb your feature in one release; (3) anyone can clone you in a week; (4) your margins are rented — you pay the model provider per token. Sam Altman fed this narrative directly. In 2023 he said startups competing with OpenAI on models with $10M were ["totally hopeless"](https://www.business-standard.com/amp/technology/tech-news/not-possible-to-build-ai-with-10-mn-sam-altman-s-old-claim-resurfaces-125012900820_1.html) — and the implicit extension was that thin layers above the models were doomed too.

### Why some wrappers won anyway **[2026]**

Then Cursor — a wrapper, in the literal sense that it routes to third-party frontier models — became one of the fastest-growing software companies in history: $1B+ ARR in ~3 years from launch, per [CNBC](https://www.cnbc.com/2025/11/13/cursor-ai-startup-funding-round-valuation.html).

**Perplexity** is the other exhibit, and it is worth slowing down on. It was the single most-mocked "wrapper" of 2023: an AI search engine built substantially on OpenAI's and Anthropic's models, competing head-on with *Google*. By September 2025 it had raised $200M at a **$20 billion valuation** with ARR "approaching $200 million" ([TechCrunch, Sep 2025](https://techcrunch.com/2025/09/10/perplexity-reportedly-raised-200m-at-20b-valuation/)). Why did it win despite owning none of the underlying intelligence? Three reasons that generalize:

1. **Product speed and experience, not model quality.** Perplexity bet that search-with-cited-answers was a *product* problem — speed, clean citations, follow-up questions — not a model problem. It shipped and iterated on the experience faster than Google could reorganize itself. That is the Gil "pace of execution" moat in action.
2. **Brand in a new category.** It became *the* name for "AI answer engine" before Google's own AI search felt safe to depend on — the same category-naming effect as "just use Cursor."
3. **Consumer distribution, bought aggressively.** It signed deals that pre-installed or gave away Perplexity Pro at massive scale: pre-installs on Motorola phones, a 12-month free Pro subscription for all **360 million** Bharti Airtel customers in India ([Airtel press release, Jul 2025](https://www.airtel.in/press-release/07-2025/airtel-partners-with-perplexity-powers-every-single-of-its-360mn-customers-with-perplexity-pro/)), and a similar free-Pro deal for PayPal/Venmo users. Notice these are *distribution* moves — the evergreen moat — not model moves.

It also hedged the wrapper risk itself. It routes across multiple frontier models and trained its own cheaper "Sonar" models for routine queries, so no single supplier can cut it off or price it to death. The wrapper critique wasn't *wrong* about day one; it was wrong about what day one implies.

Elad Gil (one of the most respected solo investors in tech) made the canonical rebuttal in ["Defensibility & Competition"](https://blog.eladgil.com/p/defensibility-and-competition), and it is the single most useful reframe in this document: **"most SaaS software starts off default non-defensible."** Salesforce, at launch, was a thin CRM (customer relationship management — the software salespeople use to track customers and deals) form on a database. Dropbox was a folder that synced. Defensibility, Gil argues, is not a birthright: "most of the forms of defensibility above take a few years to build," and "serving a customer need well is often more important (and harder) to think about than defensibility." He explicitly framed this as the answer to "Is the 'wrapper on GPT' co defensible? Is any early SaaS company?" ([his own summary](https://x.com/eladgil/status/1626264268055228418)). **[Evergreen]** — this was true of SaaS in 2005 and it is true of AI apps now.

### Where defensibility actually comes from in 2026 **[2026 specifics, Evergreen structure]**

Synthesizing Gil, Sequoia, and SignalFire, these are the moats actually working for AI application companies:

1. **Workflow depth / cognitive architecture.** Sequoia's ["Generative AI's Act o1"](https://sequoiacap.com/article/generative-ais-act-o1/) argues application companies differentiate through custom "cognitive architectures" — "the flow of code and model interactions that takes user input and performs actions." These encode how experts in a domain actually work, layered with retrieval, guardrails, and integrations. A raw model can't replicate a product that has metabolized a thousand edge cases of, say, insurance claims processing. **[2026]**
2. **Proprietary data loops.** Every user interaction that improves your product (corrections, accepted/rejected outputs, outcome labels) is data your competitor doesn't have. Caution from [SignalFire's "Moats are for castles"](https://www.signalfire.com/blog/why-ai-startups-should-optimize-for-permanence-not-moats): generic "data moats" are weaker than 2015-era VCs hoped, because better base models keep reducing how much task-specific data you need. The loop only counts if the data is genuinely unobtainable elsewhere and tied to outcomes. **[2026]**
3. **Distribution.** **[Evergreen]** — the oldest moat there is, covered in `09-networks.md`. In a world of ten identical products built in ten identical weekends, the one that owns a channel wins.
4. **Brand.** Being *the* name in a category ("just use Cursor") compounds. **[Evergreen]** mechanism, unusually fast to establish in **[2026]** because categories are forming from scratch.
5. **Speed of execution as a moat.** Gil: "Pace of execution and ongoing shipping post v1 matters a lot." SignalFire goes further: defensibility is "earned by surviving multiple waves of model progress." Ask not "what's our moat?" but *"does our product get more valuable or less valuable if models dramatically improve overnight?"* If a model upgrade makes you stronger, you are on the right side. **[2026]** in emphasis, **[Evergreen]** in spirit (this was Zuckerberg-era "move fast" formalized).
6. **Context and memory lock-in.** The newest one. A product that has accumulated months of your history, preferences, codebase context, and past decisions is painful to leave even when a rival's model is 5% smarter. The switching cost is measured in accumulated context rather than data-export friction. This is the AI-native version of the **[Evergreen]** switching-cost moat.

The anti-pattern, per SignalFire: products that are "just a prompt, wrapper, or user interface layer" exploiting *current model weaknesses*. Those die on the next model release. The distinction that matters is not wrapper vs. non-wrapper. It is **whether you're building on model limitations (fragile) or on model capabilities plus your own accumulated advantages (durable)**.

---

## 3. What changed about BUSINESS MODELS (summary — full treatment in `02-business-models.md`)

The headline shift, from Sequoia's [Act o1](https://sequoiacap.com/article/generative-ais-act-o1/): **"The cloud transition was software-as-a-service... the AI transition is service-as-a-software."** Instead of selling a tool that helps a human do work — priced per **seat**, meaning per human user — you sell *the completed work itself*, priced per outcome. Their example: Sierra, the customer-service AI company, "gets paid per resolution. There is no such thing as 'a seat.'"

Why this matters mathematically — **labor-budget TAM expansion**. Global spending on software is measured in hundreds of billions of dollars a year. Global spending on the *labor* that software assists is measured in tens of trillions. Worked example: a company pays $30/seat/month for support software for 100 agents = $36,000/year of software TAM. Those same 100 agents cost ~$5M/year in fully-loaded salary. An AI that resolves 60% of tickets isn't competing for the $36K; it is competing for a slice of the $3M of labor it displaces. Even capturing a third of the saved cost is a ~$1M/year contract — roughly **28x** the software line item. This is why **[2026]** AI startups can grow revenue at rates SaaS never could: the budget they tap is two orders of magnitude bigger.

YC has institutionalized this. Its 2025 Requests for Startups (the periodic list of company types YC's partners explicitly want to fund) included **"full-stack AI companies"** — startups that *are* the accounting firm / law firm / agency, with AI doing the work and humans supervising, rather than selling software to incumbent firms. [Forbes describes the 2026 roadmap continuing this shift](https://www.forbes.com/sites/josipamajic/2026/02/04/ycs-2026-roadmap-signals-a-shift-from-human-augmented-to-ai-native-startups/). (Caveat: Forbes blocks automated access, so that article could not be re-verified; YC's own [RFS page](https://www.ycombinator.com/rfs) is the primary source and rotates as requests are filled.) **[2026]**

**[Evergreen]** anchors that survive contact with all of this: price to value delivered, not cost incurred (see `03-pricing.md`). And **gross margin** still matters — the share of each revenue dollar left after the direct costs of delivering the product, which for AI products is mostly the model-inference bill (see the jargon key). Outcome-priced AI businesses carry real inference costs per unit of work, so the unit-economics discipline in `04-unit-economics.md` applies with extra force, not less.

---

## 4. What changed about FUNDING (full treatment in `05-fundraising.md`)

### Capital concentration **[2026]**

AI firms captured **roughly half of all global venture capital in 2025** — "one out of every two VC dollars," a total of **$211B, up 85% from 2024**, per [The AI Economy's analysis of PitchBook data](https://theaieconomy.substack.com/p/ai-vc-2025-bay-area-concentration). CB Insights puts the share at ~48%. (The [OECD announced a higher figure](https://www.oecd.org/en/about/news/announcements/2026/02/ai-firms-capture-61-percent-of-global-venture-capital-in-2025.html) — 61%, $258.7B of $427.1B — but that page blocks automated access and could not be verified for this document. Methodologies differ; the direction doesn't. Whether the true number is 48% or 61%, AI is taking about half or more of all venture money.)

There is concentration inside the concentration, all per The AI Economy: **foundation-model labs alone took $87B — nearly 60% of AI VC dollars** (up 180% year over year). The **San Francisco Bay Area captured 60% of global AI funding — $126B — on only 22% of global deals**. And within the Bay Area, **$113B of that $126B (~90%) went to just 92 companies raising mega-rounds of $100M+**.

Two practical implications for you: (a) if you're raising a big AI round, the gravitational center is SF — a real argument for your "open to SF" stance, at least for fundraising trips; (b) the flip side of half of VC flowing to AI is that *everything else* is starved. An AI framing materially changes your fundability, which is exactly why investors have become suspicious of cosmetic AI framing.

### Growth expectations reset — and the churn scrutiny behind it **[2026]**

Because the YC W25 cohort grew 10%/week and companies hit $1M–$10M ARR in months, **investor expectations reset upward**. "Good" SaaS growth (T2D3 — triple, triple, double, double, double) now looks slow next to AI-native comparables. The hottest AI companies raise at revenue multiples (valuation ÷ ARR) of 30–50x+, versus the ~10x that marked good SaaS. Cursor's $29.3B on ~$1B ARR is ~29x ([CNBC](https://www.cnbc.com/2025/11/13/cursor-ai-startup-funding-round-valuation.html)).

But sophisticated investors learned to look under the hood, and what's under many hoods is ugly. Kyle Poyar's ["The AI churn wave"](https://www.growthunhinged.com/p/the-ai-churn-wave) (analyzing payments data across AI products) found **median gross revenue retention (GRR — the % of revenue you keep after churn, ignoring upsells) of just 40% for AI-native companies, and median net revenue retention (NRR — retention including expansion) of 48%** — *worse than consumer subscription apps*. Worked example of what GRR 40% means: start January with $100K of monthly recurring revenue; by the following January only $40K of it remains. You must replace 60% of your entire revenue base every year just to stay flat. Compare healthy B2B SaaS at ~90%+ GRR.

Two of his sub-findings matter for your strategy. First, retention is strongly price-tiered: products above $250/month retained like real B2B software (70% GRR / 85% NRR), while sub-$50/month products retained catastrophically at 23% GRR. Second, companies that reached $5M ARR showed roughly **2x the GRR** of early-stage peers — the survivors are the ones who solved retention. His broader [2025 SaaS Benchmarks report](https://kylepoyar.substack.com/p/2025-saas-benchmarks-report) (800+ companies) confirms "AI-native startups aren't like B2B SaaS" on nearly every metric.

The synthesis every good investor now runs: **top-line AI growth is the easiest it has ever been to fake (with churning revenue) and the hardest it has ever been to fake durably.** Which is just the **[Evergreen]** rule wearing new clothes: *revenue quality beats revenue quantity, and retention is the truth serum.* Power-law returns haven't budged either (**[Evergreen]** — a tiny number of companies produce nearly all venture profits, so VCs only want potential outliers). AI has widened the outliers, not repealed the law.

---

## 5. Competition with incumbents and foundation labs

### "What if OpenAI does this?" **[2026 form, Evergreen substance]**

This is now a standard question in investor **due diligence** — the pre-investment homework where an investor verifies your claims and probes your risks (defined in the jargon key above) — and you need a real answer. The fear is concrete. The platform's "classic playbook" is to watch what's working on top of it and absorb it, and OpenAI/Anthropic/Google have shipped features (memory, agents, coding, search, document work) that each vaporized a cohort of startups. OpenAI even offered **$2M in API tokens for equity to an entire YC batch** ([TechCrunch, May 2026](https://techcrunch.com/2026/05/20/sam-altman-makes-mic-drop-offer-to-every-y-combinator-startup/)) — simultaneously a subsidy and a statement of intent to be the infrastructure under everyone.

How experienced founders actually answer the question — a composite of Gil's and Sequoia's frameworks plus observed 2025–26 behavior:

1. **"The labs are horizontal; we are vertical."** Foundation labs must serve everyone, so they under-serve any specific workflow. Deep vertical workflow + integrations + compliance is unattractive for them to replicate (Sequoia's cognitive-architecture argument).
2. **"They validate the market; the market is bigger than one winner."** Every lab launch of a category (coding agents, search) has so far *grown* the category leaders built on top of it rather than killing them. Cursor grew fastest *after* the labs shipped competing coding tools.
3. **"Model-agnosticism is our hedge."** Treat the model as a swappable component — route to whichever lab is best or cheapest this quarter — and the labs convert from existential threat into competing suppliers. This is Ben Thompson's commoditization logic pointed downward: "a world where models are interchangeable is one where models are commodities, while most of the value flows elsewhere" ([Stratechery, "Checking In on AI and the Big Five"](https://stratechery.com/2025/checking-in-on-ai-and-the-big-five/)).
4. **"Our data/context/relationships are things they can't ship in a release."** The lock-ins from section 2.

The **[Evergreen]** frame beneath all four comes from Elad Gil's ["AI: Startup vs Incumbent Value"](https://blog.eladgil.com/p/ai-startup-vs-incumbent-value). In every platform wave, startups beat incumbents only by being ~10x better on some axis or by owning a segment or channel the incumbent structurally can't serve. The internet wave went ~60–70% to startups. Mobile went ~80% to incumbents. The *previous* AI wave (2010s machine learning) went 90%+ to incumbents, because the tech was only "0.5–3X better" than the status quo and the data lived inside Google and Facebook. His argument for why this wave differs: LLMs are 10x better at specific high-value repetitive tasks (code, content, support) where incumbent tooling was weak — which is precisely where the startup wins have clustered. And his caveat on scale is worth memorizing: "A 10% increase in Google's market cap is currently $130 Billion, or the equivalent of almost 7 Figmas." Incumbents don't need to beat you; they need only defend, and their defense budget is your entire industry.

### The "what if OpenAI does this" answer you should NOT give

"They're too busy / they won't notice us." They will. The only durable answers are structural: segments, workflows, data, or distribution they can't or won't pursue. If your honest answer is "nothing stops them," that is a finding about your idea, not about the question — see `01-idea-evaluation.md`.

---

## 6. Platform risk and model-price deflation

**The tailwind [2026]:** a16z's Guido Appenzeller coined **"LLMflation"** for the observed rate of inference price decline: "For an LLM of equivalent performance, the cost is decreasing by 10x every year." GPT-3-quality output cost $60 per million tokens in November 2021 and ~$0.06 by late 2024 — **1,000x cheaper in three years**, faster than compute costs fell during the PC era or bandwidth during the dot-com era ([a16z, "Welcome to LLMflation"](https://a16z.com/llmflation-llm-inference-cost/)).

Worked example of what this does to product economics. An AI feature that costs you $3.00 per user per day in inference is unshippable at a $20/month price: cost ≈ $90/month per user, gross margin −350%. At the same usage 12 months later (~10x cheaper), cost is ~$9/month — thin but viable. Twelve months after that, ~$0.90/month — a 95%+ gross margin feature. The strategic lesson many 2026 winners used: **price for where costs will be in 12–18 months, eat negative margins briefly, and build products that are "too expensive to be possible" today** — because "every time we decrease the cost of something by an order of magnitude, it opens up new use cases that previously were not commercially viable" (Appenzeller).

**The threat [2026]:** the same deflation cuts against you three ways. (1) If your pricing is a markup on tokens, your revenue deflates with the input. (2) Whatever is barely-possible-and-expensive today — your frontier feature — is free-tier commodity in 18 months, so your differentiation has a half-life. (3) Classic **platform risk**: you build on a foundation model under someone else's control. They set prices, rate limits, and terms; they see aggregate usage patterns; and they are moving up the stack into applications.

The **[Evergreen]** rhyme: developers on Windows in the 90s; iOS apps "Sherlocked" by Apple (startup slang for the platform copying your app as a free built-in feature — named after Apple's Sherlock search tool, which absorbed a third-party app called Watson in 2002); media companies on Facebook's algorithm. The mitigations are also evergreen: multi-source your critical dependency (multi-model routing), own your customer relationship directly, and put your accumulated value (data, context, workflow) in layers the platform can't reach.

Ben Thompson's **Aggregation Theory** — his framework for internet economics — says in plain words: the company that owns the direct relationship with millions of consumers wins, and everyone supplying it (content, goods, or in this case models) gets squeezed into an interchangeable commodity. It is the right mental model for who wins long-run: "the most important factor determining success is the user experience... suppliers can be commoditized" ([Stratechery, Aggregation Theory / "Aggregator's AI Risk"](https://stratechery.com/2024/aggregators-ai-risk/)). As an application builder, your goal is to be the aggregator of commoditized models, not the commoditized supplier of a bigger aggregator.

---

## 7. The EVERGREEN half — what did NOT change

Everything below predates AI, survived AI, and will survive whatever comes after AI. When 2026 advice and evergreen advice conflict, evergreen wins on decade timescales.

1. **Make something people want. [Evergreen]** Still YC's literal motto, still the cause of death for most startups (see `11-failures.md` — "no market need" tops every post-mortem study, AI-era included). AI changed the cost of making *something*; it did not change the scarcity of things people *want*. If anything, the flood of cheaply-built products made genuine want the bottleneck more obviously than ever.

2. **Talk to users. [Evergreen]** No model can tell you what your specific customers' workflow pain is. Only they can, and only if you ask properly (full method in `08-talking-to-users.md`). The 2026 twist is a trap: because you can ship in a weekend, founders now skip discovery and "just launch," then mistake curiosity-driven signups for demand. The AI churn-wave data in section 4 is what that mistake looks like at industry scale.

3. **Distribution beats product (in the debates that matter). [Evergreen]** The old line — first-time founders obsess over product, second-time founders obsess over distribution — got *more* true, because product advantage now decays in months while distribution advantage compounds. Notice that in section 2, most of the moats that actually work in 2026 (distribution, brand, workflow relationships) are distribution-shaped, not product-shaped. See `09-networks.md`.

4. **Retention defines PMF. [Evergreen]** Product-market fit was never "fast growth"; it was "cohorts that stick." AI made top-line growth cheap (novelty + hype + easy signups) and thereby made retention curves the *only* trustworthy PMF signal. The numbers that matter — GRR/NRR benchmarks and how to read a cohort curve — are in `04-unit-economics.md`; the 2026 AI-specific retention data is in section 4 above.

5. **Power-law returns govern venture. [Evergreen]** One or two companies per fund return everything; investors therefore only care whether you might be an outlier. AI widened outlier outcomes (which is why roughly half of VC dollars chase it) but did not change the underlying math or what it implies for how you pitch (see `05-fundraising.md` and `07-pitching.md`).

6. **Team quality is the multiplier on everything. [Evergreen]** A 5-person company doing $10M ARR is not evidence that people stopped mattering. It is evidence that *per-person* leverage exploded, which makes each hire matter **more**, not less. Every one of the tiny-team stars (Cursor, Midjourney, Lovable, Gamma) is famous internally for hiring slowly and at an extreme bar. When one mediocre engineer is 20% of your company, the evergreen rule — only hire people who raise the average — becomes existential.

7. **Speed of iteration wins. [Evergreen principle, 2026 numbers]** Learning faster than competitors has always been the startup's only structural advantage over incumbents. AI compressed the loop from weeks to hours, raising the *tempo* required to be "fast" — but the rule (ship, measure, learn, repeat) is unchanged from Lean Startup (Eric Ries's influential 2011 book — the idea that you ship a minimal version fast, measure real user behavior, and iterate, instead of building in secret for a year) or, for that matter, from HP's garage.

---

## How to actually use this document

When you hear any piece of startup advice for the next two years, run it through three questions. **(1)** Is this an evergreen principle, a current-era number, or an evergreen principle wearing current-era numbers? **(2)** If it's [2026], what would have to happen for it to expire — and is that thing (a model release, a rate cut, a hype cycle ending) plausibly less than two years away? **(3)** If it's [Evergreen], is the person telling me it's dead selling something?

The most expensive mistakes available to you in 2026 are symmetric: treating retention/users/distribution discipline as obsolete because "AI changes everything," and treating tiny-team speed, outcome pricing, and labor-budget TAM as hype because "the fundamentals never change." Both halves of the table are real. Build with 2026 leverage on evergreen foundations.

---

## Sources

- [CNBC — "Y Combinator startups are fastest growing, most profitable in fund history because of AI" (Mar 2025)](https://www.cnbc.com/2025/03/15/y-combinator-startups-are-fastest-growing-in-fund-history-because-of-ai.html) — 10%/week batch growth, $10M revenue with <10 people, 95% AI-written code quotes from Garry Tan.
- [Garry Tan on X — vibe coding stat (Mar 2025)](https://x.com/garrytan/status/1897303270311489931)
- [YC Lightcone Podcast library](https://ycombinator.com/library/carousel/Lightcone%20Podcast) — incl. "Vibe Coding Is The Future."
- [Sequoia Capital — "Generative AI's Act o1: The Reasoning Era Begins" (Oct 2024)](https://sequoiacap.com/article/generative-ais-act-o1/) — service-as-a-software, Sierra per-resolution pricing, cognitive architectures.
- [Elad Gil — "Defensibility & Competition"](https://blog.eladgil.com/p/defensibility-and-competition) — "most SaaS software starts off default non-defensible."
- [Elad Gil — "AI: Startup vs Incumbent Value"](https://blog.eladgil.com/p/ai-startup-vs-incumbent-value) — wave-by-wave startup vs incumbent value capture.
- [Kyle Poyar, Growth Unhinged — "The AI churn wave"](https://www.growthunhinged.com/p/the-ai-churn-wave) — AI-native GRR/NRR data.
- [Kyle Poyar — 2025 SaaS Benchmarks Report](https://kylepoyar.substack.com/p/2025-saas-benchmarks-report)
- [a16z (Guido Appenzeller) — "Welcome to LLMflation"](https://a16z.com/llmflation-llm-inference-cost/) — 10x/year inference price decline.
- [OECD — "AI firms capture 61% of global venture capital in 2025" (Feb 2026)](https://www.oecd.org/en/about/news/announcements/2026/02/ai-firms-capture-61-percent-of-global-venture-capital-in-2025.html) — *note: this page blocks automated access; the 61%/$258.7B figures could not be independently verified and are presented as one estimate alongside The AI Economy's ~50% and CB Insights' ~48%.*
- [The AI Economy — "2025 AI VC: $211B invested, Bay Area dominates"](https://theaieconomy.substack.com/p/ai-vc-2025-bay-area-concentration) — $211B AI VC (~1 of every 2 VC dollars), foundation-model labs $87B (~60% of AI VC), Bay Area $126B (60% of global AI funding), $113B of that in 92 mega-rounds of $100M+.
- [Axios — "AI is eating venture capital" (Jul 2025)](https://www.axios.com/2025/07/03/ai-startups-vc-investments)
- [CNBC — "Cursor raises $2.3B at $29.3B valuation" (Nov 2025)](https://www.cnbc.com/2025/11/13/cursor-ai-startup-funding-round-valuation.html) — *note: CNBC blocks automated access; figures are consistent with widely reported Nov 2025 coverage of Anysphere's round.*
- [Lovable blog — "Zero to $10M ARR in 2 months" (Jan 2025)](https://lovable.dev/blog/2025-01-29-zero-to-10m-arr-in-2-months) — primary source for the early growth figure.
- [TechCrunch — "Eight months in, Swedish unicorn Lovable crosses the $100M ARR milestone" (Jul 2025)](https://techcrunch.com/2025/07/23/eight-months-in-swedish-unicorn-lovable-crosses-the-100m-arr-milestone/) — $100M ARR in eight months, 45 full-time employees, unicorn status.
- [TechCrunch — "As Lovable hits $200M ARR, its CEO credits staying in Europe" (Nov 2025)](https://techcrunch.com/2025/11/19/as-lovable-hits-200m-arr-its-ceo-credits-staying-in-europe-for-its-success/)
- [Growth Unhinged — Eric Simons on Bolt.new's journey to $40M ARR in 5 months](https://www.growthunhinged.com/p/boltnew-growth-journey) — $4M ARR in four weeks, $20M in three months, $40M in five months; "fewer than 40 employees including less than 10 in GTM roles."
- [TechCrunch — "AI PowerPoint killer Gamma hits $2.1B valuation, $100M ARR" (Nov 2025)](https://techcrunch.com/2025/11/10/ai-powerpoint-killer-gamma-hits-2-1b-valuation-100m-arr-founder-says/) — ~50 employees, profitable 2+ years.
- [TechCrunch — "Perplexity reportedly raised $200M at $20B valuation" (Sep 2025)](https://techcrunch.com/2025/09/10/perplexity-reportedly-raised-200m-at-20b-valuation/) — ARR approaching $200M.
- [Airtel press release — Perplexity Pro free for all 360M Airtel customers (Jul 2025)](https://www.airtel.in/press-release/07-2025/airtel-partners-with-perplexity-powers-every-single-of-its-360mn-customers-with-perplexity-pro/)
- [SignalFire — "Moats are for castles: permanence over defensibility in AI startups"](https://www.signalfire.com/blog/why-ai-startups-should-optimize-for-permanence-not-moats)
- [Forbes — "VCs Rethink Startup Moats As AI Compresses Time To Build" (Mar 2026)](https://www.forbes.com/sites/josipamajic/2026/03/31/vcs-rethink-startup-moats-as-ai-compresses-time-to-build/) — *note: Forbes blocks automated access; this and the next entry could not be re-verified, and no claim in this document rests on them alone.*
- [Forbes — "YC's 2026 Roadmap Signals A Shift From Human-Augmented To AI-Native Startups" (Feb 2026)](https://www.forbes.com/sites/josipamajic/2026/02/04/ycs-2026-roadmap-signals-a-shift-from-human-augmented-to-ai-native-startups/) — see note above; YC's own [RFS page](https://www.ycombinator.com/rfs) is the primary source.
- [TechCrunch — "Sam Altman makes 'mic drop' offer to every Y Combinator startup" (May 2026)](https://techcrunch.com/2026/05/20/sam-altman-makes-mic-drop-offer-to-every-y-combinator-startup/)
- [Business Standard — Altman's 2023 "hopeless" remark resurfaces](https://www.business-standard.com/amp/technology/tech-news/not-possible-to-build-ai-with-10-mn-sam-altman-s-old-claim-resurfaces-125012900820_1.html)
- [Stratechery — "Checking In on AI and the Big Five" (2025)](https://stratechery.com/2025/checking-in-on-ai-and-the-big-five/)
- [Stratechery — "Aggregator's AI Risk" (2024)](https://stratechery.com/2024/aggregators-ai-risk/)
- [Sifted — "Tiny teams, big revenue — but for how long?"](https://sifted.eu/articles/tiny-teams-big-revenue)
