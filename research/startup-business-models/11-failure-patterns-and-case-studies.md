# Failure Patterns & Case Studies — why seed startups die

**Why this matters to you:** A "seed" startup is a company at the earliest funding stage — it has raised (or is raising) its first real outside money. This doc is about why those companies die. Every question an investor will ever ask you traces back to a specific dead company that investor remembers. Every rule of thumb in this library is the positive image of a failure pattern; this document is the negative — the actual corpses, with names, dollar amounts, and founder confessions. Internalize how startups actually die and you get two superpowers. First, you can run a "premortem" — a structured exercise where you imagine your idea has already failed and write down why — on any candidate idea before you spend a year on it. Second, you can tell when an investor's skepticism is pattern-matching on a famous failure (which you can answer) and when it points at a real flaw in your plan (which you can't). The hardest skill this doc teaches comes in the last section: telling a genuinely bad idea apart from a "non-consensus" idea that merely *looks* bad. Airbnb, Uber, and Stripe all looked like the corpses too.

Related reading: how to evaluate ideas positively is in `01-idea-evaluation-and-conviction.md`; the money mechanics behind "ran out of cash" are in `04-unit-economics-and-money.md` and `05-fundraising-mechanics-2026.md`; what's different about AI-era failures is in `10-ai-era-2026-what-changed.md`.

---

## 1. The canonical data: what actually kills startups

### The CB Insights post-mortem analysis (the classic dataset)

CB Insights (a venture-capital data firm) read 101 public startup failure post-mortems — essays founders wrote after their companies died — and tallied the reasons cited. Two findings frame everything: **there is rarely one reason a startup fails**, and the reasons are diverse. (The percentages below sum to far more than 100% because most post-mortems cite multiple causes.) The full list, from [The Top 20 Reasons Startups Fail (CB Insights, PDF)](https://s3-us-west-2.amazonaws.com/cbi-content/research-reports/The-20-Reasons-Startups-Fail.pdf): **[Evergreen]** for the ranking's shape; the exact percentages are from a 2010s sample.

| # | Reason | % of post-mortems citing it |
|---|--------|------|
| 1 | **No market need** (built a solution looking for a problem) | **42%** |
| 2 | Ran out of cash | 29% |
| 3 | Not the right team | 23% |
| 4 | Got outcompeted | 19% |
| 5 | Pricing / cost issues | 18% |
| 6 | Poor product | 17% |
| 7 | Product without a business model | 17% |
| 8 | Poor marketing | 14% |
| 9 | Ignored customers | 14% |
| 10 | Product mistimed | 13% |
| 11 | Lost focus | 13% |
| 12 | Disharmony on team/with investors | 13% |
| 13 | Pivot gone bad | 10% |
| 14 | Lacked passion / domain expertise | 9% |
| 15 | Bad location | 9% |
| 16 | No financing / investor interest | 8% |
| 17 | Legal challenges | 8% |
| 18 | Didn't use network/advisors | 8% |
| 19 | Burned out | 8% |
| 20 | Failure to pivot | 7% |

(You will also see "no market need = 35%" quoted. That figure comes from CB Insights' later top-12 re-cut of an expanded sample, where "ran out of cash / failed to raise" edged ahead at 38%. The two-horse race at the top is always the same: *nobody wanted it* and *the money ran out*.)

The number-one killer deserves the direct quote. From the Patient Communicator post-mortem in that report: *"I realized, essentially, that we had no customers because no one was really interested in the model we were pitching. Doctors want more patients, not an efficient office."* That sentence is the entire genre in miniature — a plausible-sounding product, real technology, and a customer who simply does not care. Treehouse Logic put it structurally: *"Startups fail when they are not solving a market problem... We had great technology, great data... great advisors, etc, but what we didn't have was technology or business model that solved a pain point in a scalable way."*

**The key reading skill [Evergreen]:** "Ran out of cash" is almost never a root cause. It is the mechanism of death, the way "cardiac arrest" is technically how everyone dies. The Flud post-mortem in the same report makes this explicit: the company died because it couldn't raise more funding, but it couldn't raise *"despite multiple approaches and incarnations in pursuit of the ever elusive product-market fit."* Cash-out is downstream of no-market-need. When you read failure data, always ask: why did the cash run out?

### The updated numbers: the 2023-2026 shakeout **[2026]**

CB Insights re-ran the analysis on the post-ZIRP era. ("ZIRP" = zero interest rate policy — the 2010s–2021 period when money was cheap and startups were funded loosely.) Their [2026 analysis of 431 VC-backed companies that shut down since 2023](https://www.cbinsights.com/research/report/startup-failure-reasons-top/) ("VC-backed" = funded by venture capital firms) found:

- **70%** cited running out of capital. **43%** cited poor product-market fit ("PMF" — the state where a market actively pulls your product out of your hands). **29%** cited bad timing or macro conditions (the broader economy). **19%** cited unsustainable unit economics (losing money on each individual sale).
- Median funding raised by the dead companies: **$11M**. Combined capital destroyed: **$17.5B**.
- **Median time from last fundraise to death: 22 months.** That matches the standard advice that a round buys ~18–24 months of "runway" — the number of months your bank balance lasts at your current rate of spending. When runway hits zero, you're dead unless you've raised more or reached profitability. When the milestones don't materialize, the next round doesn't either (see `05-fundraising-mechanics-2026.md`).

Same report, same framing: *"Capital running out is where these stories end. The more telling causes — poor product-market fit (43%), bad timing (29%), and unsustainable unit economics (19%) — reveal why the capital dried up in the first place."*

### Premature scaling: the Startup Genome finding

The [Startup Genome premature-scaling report](https://s3.amazonaws.com/startupcompass-public/StartupGenomeReport2_Why_Startups_Fail_v2.pdf) (an analysis of ~3,200 high-growth internet startups, published 2011) gave the failure literature its most important mechanical concept. **Premature scaling** means spending on growth — hiring, marketing, product build-out — before you've proven that the core loop works (the basic cycle of your business: customers show up, get value, come back, and pay). Findings:

- **~70% of startups in the dataset scaled prematurely** on at least one dimension, and premature scaling was the most common self-inflicted cause of death — see also [Forbes' summary, "#1 Cause of Startup Death? Premature Scaling"](https://www.forbes.com/sites/nathanfurr/2011/09/02/1-cause-of-startup-death-premature-scaling/).
- **No startup that scaled prematurely passed 100,000 users** in their dataset.
- Startups that scaled properly grew **~20x faster** than premature scalers.

**[Evergreen]** The principle: growth spend multiplies whatever you already have. If you have a product people love, it multiplies love. If you have a product people shrug at, it multiplies shrug — at high cost. **[2026]** The modern trap is worse because AI startups can hit impressive revenue fast via curiosity-driven adoption, then churn it all away — see `10-ai-era-2026-what-changed.md` on "vibe revenue."

---

## 2. The premortem: the technique that turns this data into a tool

A **premortem** is a technique from research psychologist Gary Klein, published as [Performing a Project Premortem (Harvard Business Review, 2007)](https://hbr.org/2007/09/performing-a-project-premortem). Instead of asking "what could go wrong?" — which invites defensiveness and vague answers — you tell the team: *assume the project has already failed, spectacularly. Now write down the story of why.* This exploits "prospective hindsight": a 1989 study by Mitchell, Russo, and Pennington found that imagining an event as having *already happened* increases people's ability to correctly identify reasons for future outcomes by **~30%** (see [the Wikipedia summary of the pre-mortem literature](https://en.wikipedia.org/wiki/Pre-mortem)). **[Evergreen]**

Why it works for startup ideas specifically: the CB Insights list above is literally a menu of endings. When you premortem a candidate idea, you're asking: "Which of the 20 canonical deaths is most likely to be mine, and what would I have to believe to think otherwise?" Section 7 of this doc is a ready-to-run premortem checklist. Investors do an informal version of this in every pitch meeting — which is Section 6.

---

## 3. The tarpit graveyard: ideas that kill on repeat

Y Combinator (YC — the original startup accelerator, a program that funds and coaches batches of very early startups) partners Dalton Caldwell and Michael Seibel coined the term **"tarpit ideas"** in their talk [Avoid These Tempting Startup Ideas](https://www.ycombinator.com/library/LH-tarpit-ideas-the-sequel) (original video: ["Avoid These Tempting Startup Ideas"](https://www.youtube.com/watch?v=GMIawSAygO4); Caldwell also covers it on [Lenny's Podcast](https://www.lennysnewsletter.com/p/lessons-from-1000-yc-startups)). The metaphor: a tar pit looks like a refreshing pond. Animals keep walking in, and the ground is littered with the bones of everything that tried before. A tarpit idea is one that *seems* obviously good and underserved, attracts wave after wave of smart founders, and kills nearly all of them. **[Evergreen]**

Characteristics of tarpits, per Caldwell and Seibel:

- **They're overwhelmingly consumer ideas.** Founders are consumers themselves, so consumer problems are the ones they personally feel. And the biggest famous outcomes (Facebook, Instagram) were consumer, which makes the category feel validated.
- **The problem is real; the graveyard is invisible.** Yes, it *is* annoying to decide what to do with friends on a Friday night. The reason no product solves it is not that nobody tried — hundreds of funded teams tried. Demand for a *solution* doesn't imply demand for *any particular product*, and use cases that are low-frequency and low-intent can't sustain retention (people keeping using the product over time).
- **Canonical examples:** apps to discover new things to do / places to go / music / restaurants ("discovery" apps generally); apps to coordinate with friends; "Yelp for X"; photo-sharing-with-a-twist; travel-planning apps. Color Labs — $41M raised pre-launch in 2011 for a social photo-discovery app, dead within two years — is the genre's poster child.

The tarpit test to run on your own idea **[Evergreen]**: search Crunchbase (a public database of startups and their funding) and Google for companies that tried your exact idea. If you find many, well-funded, all dead, you need a specific answer — one you could prove wrong — to "what changed in the world that makes it work now?" A real platform shift, a regulatory change, a new capability (see the "why now" discussion in `01-idea-evaluation-and-conviction.md`). "We'll execute better" is not an answer; every skeleton in the pit said that. **[2026]** Note: "we'll do it with AI" is the current era's default fake why-now. Sometimes it's real — AI genuinely unlocks the product. But investors have already seen hundreds of "tarpit idea + LLM" pitches (LLM = large language model, the technology behind ChatGPT-style AI), so the burden of proof is on you.

---

## 4. Case studies: six well-documented corpses

Chosen across eras and business models. Each one is the source of a pattern-matching reflex you will encounter in fundraising.

### 4.1 Homejoy (2010–2015) — marketplace death by retention and subsidized demand

Home-cleaning marketplace, YC-backed, raised ~$40M, shut down July 2015. The CEO publicly blamed worker-classification lawsuits (suits over whether its cleaners were employees or independent contractors), but [Forbes' investigation, "What Really Killed Homejoy: It Couldn't Hold On To Its Customers"](https://www.forbes.com/sites/ellenhuet/2015/07/23/what-really-killed-homejoy-it-couldnt-hold-onto-its-customers/) found the real killers:

- **Acquisition via deep discounts:** a normal cleaning cost ~$85; Homejoy acquired customers with $19 Groupon-style promos. Worked example: a $19 first clean costs you ~$66 in subsidy plus ad spend. The customer must return ~4+ times at full price just to pay back that acquisition cost. So a reported repeat rate where most promo customers never book again means **every marketing dollar destroyed value**. Growth made the company worse off.
- **Both sides churned** ("churn" = the rate at which customers or workers quit): cleaners were paid less than competitors, quality was inconsistent, and good cleaners + happy customers cut Homejoy out and dealt directly. That's **disintermediation** — the marketplace-killer where supply and demand meet through you once, then transact around you.
- Management **"pushed relentlessly for high growth numbers instead of fixing its poor retention rates"** (Forbes) — a textbook premature scale, plus a costly international expansion before the home market worked.

**Lessons:** For marketplaces, retention and take-rate defensibility *are* the business. The "take rate" is the percentage cut the marketplace keeps of each transaction, and "defensibility" means whether you can keep charging it without the two sides cutting you out, as Homejoy's cleaners and customers did (see `02-business-model-taxonomy.md`). Discounted demand is fake demand. When an investor asks you "what's your repeat rate, excluding promotions?" — that's Homejoy's ghost talking.

### 4.2 MoviePass (2011–2020) — consumer subscription with negative unit economics

Movie-ticket subscription. In 2017 it dropped to **$9.95/month for unlimited movies** when the average US ticket cost ~$9 — and MoviePass paid theaters full retail price per ticket. Worked example, from [reporting on the collapse](https://www.thestreet.com/entertainment/what-happened-to-moviepass-rise-fall-and-resurrection) and [post-mortems of its unit economics](https://www.bcrschroeder.com/p/why-moviepass-failed): the average subscriber watched **2.11 movies/month** (June 2018), so per-subscriber economics were roughly $9.95 revenue − (2.11 × ~$9) ≈ **−$9 per subscriber per month**, before payment processing and support. With ~3M subscribers, losses ran to ~**$40M per month**. Subscribers surged precisely *because* the deal was irrational — a case of adverse selection, where the customers who cost you the most (the heaviest moviegoers) are exactly the ones most eager to sign up. Parent company Helios & Matheson hit Chapter 7 bankruptcy — liquidation, where the company is dissolved and its assets sold — by January 2020.

**Lessons [Evergreen]:** Growth that comes from underpricing is just borrowing customers from your own balance sheet. The gamble was "get scale, then monetize data / negotiate theater discounts" — a *hope*, not a mechanism. Contribution margin — the money left over from each sale after paying the direct costs of delivering that sale, before company-wide overhead — must be positive, or have a specific, contracted path to positive, before scaling (see `04-unit-economics-and-money.md`). MoviePass's contribution margin was roughly −$9 per subscriber per month: every new customer made the hole deeper. Investors probing "does each incremental customer make you richer or poorer?" are checking whether you're MoviePass.

### 4.3 Juicero (2013–2017) — hardware, and building the elaborate version of a simple thing

A $699 (later $399) Wi-Fi-connected juice press with proprietary QR-coded produce packs; raised ~**$120M** from Kleiner Perkins, GV (Google Ventures), and others. In April 2017 Bloomberg demonstrated that you could [squeeze the juice packs by hand](https://thevcfactory.com/juicero-doug-evans-venture-capital-failure/) — getting the juice faster than the machine did. The company was dead ~5 months later, 17 months after launch. The deeper failure wasn't the viral embarrassment. It was that the product's entire premise — you need an expensive machine — was false, and no one had forced that premise through a "would a normal person pay for this?" test before spending nine figures. VC projection bias — investors projecting their own tastes onto the market, in this case investors who personally loved cold-press juice — substituted for customer evidence.

**Lessons [Evergreen]:** Hardware amplifies every mistake: it eats capital, iteration cycles are slow, inventory is a risk, and you can't patch away a shipped device's reason for existing. Complexity is not value. "Could a dumb, cheap version do the same job?" is a question worth asking of any product — especially AI products that wrap a fancy pipeline around something a simple prompt does.

### 4.4 Quibi (2018–2020) — capital cannot substitute for evidence

Short-form mobile-only streaming from Jeffrey Katzenberg and Meg Whitman. Raised **$1.75B before launch**; shut down **six months** after launching, with ~500,000 subscribers against a 7M first-year target ([IndieWire's post-mortem](https://www.indiewire.com/features/general/quibi-shuts-down-post-mortem-failed-mobile-streaming-service-1234588080/), [Babson's case study](https://entrepreneurship.babson.edu/lessons-from-billion-dollar-failure/)). The failure stack: the core premise ("premium 10-minute episodes watched on phones during commutes") was never validated — millennials watch most video on TVs, and free TikTok/YouTube had already won short-form. The pandemic removed commutes. The product forbade screenshots and sharing, cutting off organic growth (growth from users spreading it themselves rather than from paid ads). And leadership blamed timing rather than the thesis. Because all the money was raised up front, there were **no funding checkpoints**. Normally, failing to find PMF at seed means you can't raise the A (the "Series A" — the first big institutional round), and the market forces a rethink at the $5M mark rather than the $1.75B mark.

**Lessons [Evergreen]:** The staged nature of venture funding is a *feature* — each round is a checkpoint that kills bad theses cheaply. Pedigree (Katzenberg ran Disney's film studio) doesn't exempt anyone from no-market-need, and "well-funded" makes the death bigger, not less likely.

### 4.5 Humane (2018–2025) — hardware + AI-era hype, shipping vision instead of product **[2026]**

The AI Pin: a $699 wearable AI assistant (plus $24/month subscription) from ex-Apple stars; raised ~$230M at a valuation reported near $1B (funding figure widely reported but not confirmed in the shutdown coverage I reviewed). Launched April 2024 to devastating reviews — slow, hot, unreliable answers. It targeted 100,000 unit sales, [sold ~10,000, and at one point daily returns outpaced sales](https://www.axios.com/2025/02/18/humane-ai-pin-shut-down-hp). In February 2025 [HP bought the assets for $116M and shut the product down](https://www.ghacks.net/2025/02/19/humanes-ai-pin-ceases-operations-following-hp-acquisition/) — bricking devices, since core features died with Humane's servers. The pattern: maximum secrecy + maximum hype + no cheap validation loop, in a category (replacing the smartphone) where the incumbent — the established player already in the market, here Apple — was about to bundle the same capability into the device everyone already owns.

**Lessons [2026]:** In the AI era, "the model will get better" is not a product plan. Any thin capability layer sits in the blast radius of both the foundation-model labs (the companies building the underlying AI models, like OpenAI and Anthropic) and the phone platforms — see `10-ai-era-2026-what-changed.md` on moats (durable defenses against competitors copying you). Also: a hardware subscription dies with the company's servers — buyers and acquirers both know this now.

### 4.6 Builder.ai (2016–2025) — the AI-era mega-failure: faking it past due diligence **[2026]**

"Due diligence" (often just "diligence") is the investigation investors run before writing a check — verifying that the product, revenue, and claims are real. Builder.ai got past it for years. The London-based "AI-powered app development" unicorn (a private startup valued at $1B or more) raised ~$450M total, including a 2023 Microsoft investment round, and was valued near $1.5B. It collapsed into insolvency (unable to pay its debts) in May 2025 after Bloomberg exposed [round-tripping with Indian firm VerSe Innovation](https://www.techspot.com/news/108173-builderai-collapses-after-revelation-ai-hundreds-engineers.html) — a scheme where the two firms exchanged near-identical invoices for services never rendered, inflating revenue by up to 300%. Audited 2024 revenue was **$55M versus the ~$220M projected to investors**. A creditor seized $37M from its accounts, forcing bankruptcy ([Rest of World's post-mortem](https://restofworld.org/2025/builderai-ai-apps-downfall/), [Bloomberg's feature](https://www.bloomberg.com/news/features/2025-07-30/startup-builder-ai-goes-from-1-5-billion-unicorn-to-bankruptcy)). The kicker: much of the "AI" assembly was actually [hundreds of human developers in India](https://restofworld.org/2025/builderai-ai-explainer-bankrupt/) doing the work by hand.

**Lessons [2026]:** This is the failure investors now pattern-match hardest on when they diligence AI companies: **is the AI real, and is the revenue real?** Expect questions about gross margin (revenue minus the direct cost of delivering the product — human-powered "AI" shows up as terrible margins), revenue quality, and cohort retention (whether the customers who signed up in a given month are still using and paying later). The broader 2023–2026 shakeout that CB Insights documents — 431 shutdowns, $17.5B destroyed — is the backdrop for why seed diligence got more forensic. "Fake it till you make it" now reads as "Builder.ai" (or Theranos) to every investor in the room.

### Honorable mentions worth reading on your own

The [CB Insights collection of 483 startup failure post-mortems](https://www.cbinsights.com/research/startup-failure-post-mortem/) is the primary-source archive — founders in their own words. Standouts: **Wesabe** (lost to Mint; founder Marc Hedlund's brutal line, quoted in the CB Insights report: all their principled advantages didn't matter because *"none of them matter if the product is harder to use"*), **Tutorspree** (YC company killed by dependence on a single acquisition channel — SEO, search engine optimization, i.e. free traffic from Google rankings — which Google changed overnight), and **ArsDigita** (founder/investor warfare destroying a profitable company).

---

## 5. Founder-caused deaths: the patterns behind the patterns

**Co-founder conflict.** Noam Wasserman's *The Founder's Dilemmas* (Harvard Business School research on ~10,000 founders) found that roughly **65% of high-potential startup failures are driven by people problems within the founding team** — conflict over roles, equity (ownership shares in the company), and control — rather than product or market failure ([Princeton University Press summary](https://press.princeton.edu/books/paperback/9780691158303/the-founders-dilemmas); [MassChallenge overview](https://masschallenge.org/articles/noam-wasserman-founders-dilemma-anticipating-and-avoiding-pitfalls-can-sink-startup/)). The killer disagreements are predictable and feel postponable: 50/50 equity splits decided in five minutes to avoid an awkward conversation, no vesting (the arrangement where equity is earned over ~4 years, so a departing co-founder doesn't walk off with half the company), and unresolved "who is CEO" ambiguity. **[Evergreen]** This is why investors ask "how did you meet, and how do you make decisions when you disagree?" — they're not making small talk.

**Premature scaling** (Section 1) is the second self-inflicted death: hiring ahead of revenue, buying growth ahead of retention. The tell in the 2023–2026 shutdown wave: companies with the *median $11M raised* dying 22 months after their last round — they spent like the next round was guaranteed. **[2026]** Rule restated from `00-rules-of-thumb.md`: your burn rate (how much cash you spend per month) is a bet on your worst fundraising scenario, not your best.

**Fake PMF / the sugar high.** The subtlest founder-caused death: mistaking early traction (early signs of growth and usage) for product-market fit, and scaling into it. Warning signs, per [analyses of false product-market fit](https://medium.com/design-bootcamp/false-product-market-fit-the-silent-killer-of-early-stage-startups-1416ff57e446): growth that stops when paid spend or discounts stop; high churn that product improvements don't fix; sales that require founder heroics on every deal; usage driven by curiosity rather than dependence. **[2026]** This is *the* AI-era failure mode: LLM products get tried by everyone and retained by few, so revenue can sprint to $1M+ ARR (annual recurring revenue — subscription revenue on a yearly run rate) on novelty and then evaporate. The test that matters is cohort retention — do the customers from six months ago still use and pay? (For how real PMF is measured — Sean Ellis's 40% "very disappointed" test, retention curves that flatten — see `01-idea-evaluation-and-conviction.md` and `08-talking-to-users-and-people.md`.)

---

## 6. How investors pattern-match on corpses — and the ideas that only looked dead

### Every diligence question is a tombstone

When you understand the graveyard, seed-stage diligence questions decode as follows **[Evergreen]**:

| The question | The corpse behind it |
|---|---|
| "What's retention look like, cohort by cohort, without discounts?" | Homejoy, every fake-PMF death |
| "What's the contribution margin per order/user?" | MoviePass |
| "Who desperately needs this? Have you talked to them?" | The 42% "no market need" pile |
| "Why hasn't this worked before? Why now?" | The tarpit graveyard (Color, every discovery app) |
| "How did you two meet? How's equity split? Vesting?" | Wasserman's 65% |
| "What happens when OpenAI/Apple ships this as a feature?" | Humane; every thin AI wrapper **[2026]** |
| "Walk me through how the revenue is recognized. What's gross margin?" | Builder.ai **[2026]** |
| "What's your burn multiple / months of runway?" (burn multiple = cash burned ÷ new annual recurring revenue added — how many dollars you spend to buy each dollar of growth; under ~2x is considered healthy at early stage) | The 22-months-after-last-round median **[2026]** |

You cannot bluff these. But you *can* prepare: the strongest founders answer the pattern-match by showing they know the corpse better than the investor does — "here's exactly why Homejoy died, and here are the three structural differences in our model, with the cohort data."

### The flip side: non-consensus, not bad

The failure data has a trap in it: the biggest wins *also* looked like canonical failures at seed. The skill is distinguishing **bad** (the evidence says no) from **non-consensus** (the evidence says yes, but conventional wisdom hasn't caught up).

- **Airbnb** was rejected by 7 investors in 2008 while trying to raise $150K at a $1.5M valuation — 5 wrote rejection emails, 2 didn't reply, as Brian Chesky documented in [7 Rejections](https://medium.com/@bchesky/7-rejections-7d894cbaa084). Fred Wilson of Union Square Ventures later [published his own regret](https://qz.com/452185/the-rejection-letters-of-early-round-investors-who-passed-on-airbnb): *"We couldn't wrap our heads around air mattresses on the living room floors as the next hotel room... Others saw the amazing team that we saw, funded them, and the rest is history."* He keeps a box of the founders' Obama-O's cereal in his conference room as a warning. The pattern-match said "consumer marketplace, safety nightmare, nobody will sleep at a stranger's house." What the pattern-match missed: **the thing was already happening** — real strangers were really paying real money to sleep on those air mattresses, with obsessive repeat usage in a wedge market (a small, specific entry market — here, cities where conferences had sold out the hotels).
- **Uber** was widely modeled as a niche. NYU professor Aswath Damodaran valued it at **$5.9B** in 2014 by sizing it against the ~$100B global taxi market. Investor Bill Gurley's rebuttal, [How to Miss By a Mile](https://abovethecrowd.com/2014/07/11/how-to-miss-by-a-mile-an-alternative-look-at-ubers-potential-market-size/), argued the real market was car-ownership replacement — and that a product 10x more convenient than the old one *expands* its market rather than taking share of it. Uber's later revenue exceeded the entire market size skeptics had assumed. Lesson: **TAM (total addressable market — the total yearly spend your product could theoretically capture) calculated from the incumbent category is a backward-looking number**. The interesting question is what the market becomes when the product changes behavior.
- **Stripe** entered "payments," a category everyone in 2010 considered solved (PayPal existed; banks existed). The Collison brothers' insight was that the *developer experience* of accepting payments was miserable — seven lines of code versus weeks of bank negotiations — and developers were becoming the buyers. The skeptics' category knowledge ("payments is a solved, low-margin, regulated space") was accurate about the old market and irrelevant to the new buyer.

**What distinguished them from the corpses [Evergreen]:** In every case, the founders had **direct evidence of desperate demand in a small wedge** — hosts kept hosting, riders wouldn't stop using Ubercab, developers begged for API access — while the skeptics were reasoning from **category-level priors** (marketplaces are dangerous, taxis are small, payments is solved). A bad idea has neither believers nor usage. A non-consensus idea has intense usage that the consensus explains away. So the operational test for your own idea: *do I have specific people who behave as if they can't live without this — or do I only have an argument?* Arguments are what the 42% had. (Paul Graham's version of this is doing "things that don't scale" to find those first desperate users — see `08-talking-to-users-and-people.md`.)

---

## 7. The premortem checklist: run this on any candidate idea

Sit down, set a timer for 45 minutes, and write — in past tense, as if it's 3 years from now and the company is dead — the most plausible obituary. Klein's research (Section 2) says the past-tense framing is what unlocks honesty. Then force-rank which of these killed you. **[Evergreen]** unless tagged:

**Market (the 42% killer)**
1. Who *specifically* was the first customer, and what did they do before us? If the answer is "nothing, they just lived with the problem" — was it actually a problem, or a mild annoyance? (Patient Communicator test: are we selling efficiency to someone who wants growth?)
2. Did we ever have 10 users/customers who would be "very disappointed" if we vanished? Or did we scale on curiosity?
3. Is this a tarpit? List every prior company that tried this. What specifically changed that made our attempt different — and was that change real or asserted?

**Money (the 29–70% killer)**
4. Worked math: at our price and our costs, does one more customer make us richer or poorer (MoviePass test)? Write the actual per-unit numbers down.
5. If growth spend went to zero tomorrow, does revenue hold (Homejoy test)?
6. When did we die relative to our last raise? (Median is 22 months **[2026]**.) What milestone did we bet the next round on, and what was Plan B when we missed it?

**Team (the 65% killer)**
7. Did the founders have the fight — about equity, roles, commitment, or who's CEO — before incorporating (legally forming the company), or did we defer it? Is there vesting?
8. Did anyone on the team actually love this domain, or was it "a good market" we didn't care about? (The NewsTilt confession from the CB Insights report: *"we didn't really care about journalism, and weren't even avid news readers."*)

**Product & competition**
9. Was there a simpler, dumber version that captured most of the value (Juicero test)? Did an incumbent bundle us as a feature (Humane test **[2026]**)?
10. Were we honest about what the product actually was — with investors and ourselves (Builder.ai test **[2026]**)? Would our gross margins survive an audit of how the work really gets done?

**Scaling**
11. On which dimension did we scale prematurely — headcount, marketing, product surface, geographies — before retention proved the core loop (Startup Genome test)?
12. What single channel or platform were we dependent on, and what happened when it changed (Tutorspree test)?

**The non-consensus check**
13. If everyone said the idea was bad: did we have *usage evidence* the skeptics lacked (Airbnb test) — or only a clever argument? If the latter, the skeptics were probably right.

If the obituary writes itself easily and the same cause keeps topping the ranking, that's the signal — either fix that specific vulnerability before starting, or pick a different idea. If you genuinely struggle to write a plausible obituary that isn't generic ("we ran out of money somehow"), that is what conviction with evidence feels like. Take it to `01-idea-evaluation-and-conviction.md` and run the positive evaluation.

---

## Sources

- [The Top 20 Reasons Startups Fail — CB Insights (PDF, full report with percentages and founder quotes)](https://s3-us-west-2.amazonaws.com/cbi-content/research-reports/The-20-Reasons-Startups-Fail.pdf)
- [Why Startups Fail: Top Reasons (2026 analysis of 431 post-2023 shutdowns) — CB Insights](https://www.cbinsights.com/research/report/startup-failure-reasons-top/)
- [483 Startup Failure Post-Mortems — CB Insights](https://www.cbinsights.com/research/startup-failure-post-mortem/)
- [Startup Genome Report Extra: Premature Scaling (PDF)](https://s3.amazonaws.com/startupcompass-public/StartupGenomeReport2_Why_Startups_Fail_v2.pdf)
- [#1 Cause of Startup Death? Premature Scaling — Forbes](https://www.forbes.com/sites/nathanfurr/2011/09/02/1-cause-of-startup-death-premature-scaling/)
- [Performing a Project Premortem — Gary Klein, Harvard Business Review (2007)](https://hbr.org/2007/09/performing-a-project-premortem)
- [Pre-mortem (prospective hindsight research summary) — Wikipedia](https://en.wikipedia.org/wiki/Pre-mortem)
- [Tarpit Ideas: The Sequel — Dalton Caldwell & Michael Seibel, Y Combinator](https://www.ycombinator.com/library/LH-tarpit-ideas-the-sequel) and [the original talk](https://www.youtube.com/watch?v=GMIawSAygO4)
- [Lessons from 1,000+ YC startups — Dalton Caldwell on Lenny's Podcast](https://www.lennysnewsletter.com/p/lessons-from-1000-yc-startups)
- [What Really Killed Homejoy: It Couldn't Hold On To Its Customers — Forbes](https://www.forbes.com/sites/ellenhuet/2015/07/23/what-really-killed-homejoy-it-couldnt-hold-onto-its-customers/)
- [What Happened to MoviePass — TheStreet](https://www.thestreet.com/entertainment/what-happened-to-moviepass-rise-fall-and-resurrection) and [Why MoviePass Failed — Benjamin Schroeder](https://www.bcrschroeder.com/p/why-moviepass-failed)
- [Juicero: How Founder Charisma and VC Projection Bias Led to a $120 Million Failure — The VC Factory](https://thevcfactory.com/juicero-doug-evans-venture-capital-failure/)
- [Quibi Shuts Down: A Post-Mortem — IndieWire](https://www.indiewire.com/features/general/quibi-shuts-down-post-mortem-failed-mobile-streaming-service-1234588080/) and [Lessons Learned from a $1.7 Billion Failure — Babson](https://entrepreneurship.babson.edu/lessons-from-billion-dollar-failure/)
- [Humane AI Pin shut down after HP acquisition — Axios](https://www.axios.com/2025/02/18/humane-ai-pin-shut-down-hp) and [gHacks coverage](https://www.ghacks.net/2025/02/19/humanes-ai-pin-ceases-operations-following-hp-acquisition/)
- [Builder.ai collapses — TechSpot](https://www.techspot.com/news/108173-builderai-collapses-after-revelation-ai-hundreds-engineers.html), [Inside the collapse of Builder.ai — Rest of World](https://restofworld.org/2025/builderai-ai-apps-downfall/), and [Bloomberg feature](https://www.bloomberg.com/news/features/2025-07-30/startup-builder-ai-goes-from-1-5-billion-unicorn-to-bankruptcy)
- [The Founder's Dilemmas — Noam Wasserman (Princeton University Press)](https://press.princeton.edu/books/paperback/9780691158303/the-founders-dilemmas) and [MassChallenge summary](https://masschallenge.org/articles/noam-wasserman-founders-dilemma-anticipating-and-avoiding-pitfalls-can-sink-startup/)
- [7 Rejections — Brian Chesky](https://medium.com/@bchesky/7-rejections-7d894cbaa084) and [Airbnb rejection letters — Quartz](https://qz.com/452185/the-rejection-letters-of-early-round-investors-who-passed-on-airbnb)
- [How to Miss By a Mile: An Alternative Look at Uber's Potential Market Size — Bill Gurley, Above the Crowd](https://abovethecrowd.com/2014/07/11/how-to-miss-by-a-mile-an-alternative-look-at-ubers-potential-market-size/)
- [False Product-Market Fit: The Silent Killer of Early-Stage Startups — Medium/Bootcamp](https://medium.com/design-bootcamp/false-product-market-fit-the-silent-killer-of-early-stage-startups-1416ff57e446)
