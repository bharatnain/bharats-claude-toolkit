# Business Model Picker — taxonomy table + decision tree

The business model is not a detail you figure out later — it *is* half the idea. Two startups attacking the same problem with different models have wildly different margins, funding needs, and endgames. Investors pattern-match your model in the first two minutes of a pitch. [Evergreen]

Core vocabulary: **Gross margin** = revenue minus direct cost of serving the customer (servers, inference, support), as a %. **ARR/MRR** = annual/monthly recurring revenue. **GMV** = total value transacted *through* a marketplace (not your revenue — your revenue is the take rate you keep). **PLG** = product-led growth: the product is the salesperson; users adopt self-serve before sales gets involved.

---

## Part 1: The comparison table

Margins and timelines are directional [2026] benchmarks; the *relative ordering* is [Evergreen].

| Model | Gross margin | Sales motion | Time to first revenue | Capital intensity | Defensibility at scale | Canonical winner / corpse |
|---|---|---|---|---|---|---|
| Seat-based B2B SaaS | 75–90% | Inside sales / self-serve | Months | Low-Med | Med (switching costs) | Salesforce, Figma / the $1–5M-ARR plateau graveyard |
| Usage-based infra | 60–80% | Bottom-up + sales | Months | Med | Med-High (data gravity) | AWS, Twilio / Nirvanix |
| Freemium / PLG | 70–85% | Self-serve, sales-assist later | Months (revenue lags usage) | Med | Med (team lock-in) | Notion, Slack / dev tools with adoption, no monetization |
| Enterprise sales-led | 70–85% | Field sales, 6–12 mo cycles | 1–2 years | High | High (integration, compliance) | Palantir, Veeva / Powa Technologies |
| Transactional / take-rate | 40–70% (net) | Partnerships, embedded | 1–2 years | High | High (money-flow lock-in) | Stripe, Adyen / sub-scale neobanks |
| Marketplace | 50–70% of net rev | Two-sided growth ops | 1–3 years to liquidity | High | Highest (network effects) | Airbnb, DoorDash / Homejoy |
| Consumer subscription | 60–85% | Performance marketing, virality | Months | Med-High | Low-Med (habit, brand) | Netflix, Duolingo / MoviePass |
| Advertising | 60–80% at scale | None until huge | 3–7 years | Extreme | Highest at scale, none before | Google, Meta / Vine |
| Hardware (+SaaS) | 20–40% HW / ~80% attach | Direct + channel | 1–3 years | Extreme | High (install base) | Apple, Samsara / Juicero, Humane |
| Open-source commercial | 60–85% | Community → enterprise | 2–4 years | Med-High | Med-High (community) | MongoDB, GitLab / RethinkDB |
| API-as-product | 70–85% (lower for AI) | Developer-led | Months | Med | Med (DX, switching costs) | Stripe, Twilio / GPT-wrapper APIs |
| Services-to-product | 30–50% → 70%+ | Founder relationship sales | Immediate | Low | Low until productized | Mailchimp, Basecamp / half-productized agencies |
| AI copilot (per-seat) [2026] | 50–60% | Same as seat SaaS | Months | Low-Med | Low-Med (distribution, not the AI) | GitHub Copilot / Jasper |
| AI credits / usage [2026] | 50–70% | Self-serve + sales | Months | Med | Low-Med (product, not pricing) | Cursor / (repricing revolts) |
| AI outcome-based [2026] | 50–80%, volatile | Value-based enterprise | Months–year | Med-High | Med (performance-data flywheel) | Sierra, Intercom Fin / attribution fights |
| AI agent (per-agent / FTE) [2026] | 40–75%, opaque | Enterprise, vs labor budget | Months | Med-High | Low-Med (copycats) | Harvey / 11x, Olive AI |

Sales motions decoded: **self-serve** = credit card, no salesperson; **inside sales** = remote reps, ~$5K–100K/yr deals; **field sales** = in-person, six-to-seven-figure deals, the most expensive motion. [Evergreen]

---

## Part 2: The decision tree

Work through in order. Answers map an idea's characteristics to a model; note the model, then sanity-check against the table above. [Evergreen]

**Q1. Who feels the pain, and who controls the budget?**
- [ ] Individual → self-serve consumer or PLG
- [ ] Team → seat-based SaaS or PLG
- [ ] Executive with a P&L problem → enterprise sales-led or outcome-based
- [ ] The budget you tap is *labor*, not software (your product does the work) → price against labor (agent/outcome models); labor budgets are ~10x software budgets [2026]

**Q2. How does value scale?**
- [ ] With number of humans using it → per-seat
- [ ] With volume of activity (API calls, GB, invoices) → usage-based
- [ ] With transactions in a money flow → take-rate
- [ ] With a countable, attributable result → outcome-based
- [ ] Mispricing the value metric is the most common self-inflicted wound — see `pricing-worksheet.md`

**Q3. Can the user adopt it alone in 10 minutes?**
- [ ] Yes → PLG is available (the cheapest distribution in software); needs a natural team/sharing loop to spread
- [ ] No (integration, compliance, data migration) → sales-led; budget for salespeople, which requires price ≥ ~$25K/yr

**Q4. Is there a two-sided cold-start problem?**
- [ ] Yes → you're a marketplace whether you like it or not. Plan the liquidity-first wedge (one city, one category) before anything else. Bootstrap supply first (suppliers are economically motivated); design against disintermediation if buyer/seller repeat-transact (escrow, insurance, scheduling — keep the value on-platform). Keep the rake modest: "high volume combined with a modest rake is the perfect formula" (Gurley).

**Q5. What gross margin does the model force?**
- [ ] Investors underwrite margins, not dreams: a 30%-margin business needs 3x the revenue of a 90%-margin one for the same gross profit.
- [ ] If the model traps you below ~50%, you need a credible path up (attach software, automate the service) or a non-venture funding plan.
- [ ] [2026] AI products: inference is real COGS — expect 50–65% starting margins vs SaaS's 75–90%, and be able to say how it improves (caching, routing, model price declines).

**Q6. How much capital before the truth?**
- [ ] Ads and marketplaces need years of subsidy before revealing whether they work; SaaS and services tell the truth in months. Match the model to your risk tolerance and fundraising reality. Advertising is almost never right for a first-time founder unless you can credibly reach 10M+ users on venture subsidy. [2026]

**Q7. Where's the moat once it works?**
- [ ] Rank: network effects > embedded money/data flows > workflow lock-in > brand > features.
- [ ] If your model forecloses moats (e.g., pure services), know you're choosing a lifestyle business or a stepping stone — a legitimate, different game.

---

## Part 3: 2026 adjustments

- [ ] **Per-seat is breaking for AI products.** If the AI does the work, headcount shrinks and your revenue shrinks as your product improves. Pure seat pricing is losing share fast. [2026]
- [ ] **The modal winning structure is hybrid**: a predictable platform/subscription fee plus a usage or outcome component — 37% of B2B software companies run hybrid, the most common structure by far (Poyar survey). Design v1 pricing so a second component can be added without a repricing revolt. [2026]
- [ ] **Outcome pricing is powerful only where outcomes are discrete, countable, and attributable** (support resolutions: yes; "better strategy": no). You carry the performance risk — you pay inference on failed attempts that earn nothing. [2026]
- [ ] **Agent-washing is a diligence trigger.** "Digital employee" revenue is easy to book and brutal to keep unless the agent genuinely does the job (11x, Olive AI, Builder.ai). If hidden human labor backstops the agent, you have a low-margin services firm burning venture-scale cash. [2026]
- [ ] **AI-enabled services** (agents pushing service margins from ~35% toward 60–70%) is a genuinely new, unproven-at-scale path — treat claims skeptically, but it revives services-to-product as a hot strategy. [2026]

---

## Part 4: The default recommendation

For a technical first-time founder in 2026: **B2B, hybrid-priced (base platform fee + usage/outcome component), sold to a budget you can name, gross margin ≥60%, first revenue within 6 months.** Deviate knowingly, not accidentally. [2026]

Transitions are possible but are surgery, not convenience pivots (Adobe's license→SaaS J-curve took two down years; services→product takes a decade of discipline). Hybrids are the norm at scale — Amazon, Shopify, Apple all stack models — so pick the *wedge* model now and design for the stack later. [Evergreen]

## Output format for a model-picker run

State: (1) the recommended model with the Q1–Q7 answers that drove it, (2) the runner-up and why it lost, (3) the forced gross margin and what it implies for fundraising, (4) the 2026 hybrid component to design in from day one, and (5) the model's canonical corpse and how the idea avoids that death.

*Deeper reading: `research/startup-business-models/02-business-model-taxonomy.md`.*
