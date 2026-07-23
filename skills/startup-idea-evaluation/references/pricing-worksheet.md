# Pricing Worksheet — determining what to charge, step by step

Pricing is the highest-leverage decision most founders treat as an afterthought: a 1% price improvement flows almost entirely to profit. The technical founder's instinct — charge little because the code cost "nothing" — is exactly backwards and structurally fatal: your price determines whether you can ever afford salespeople, and cheapness signals toy. [Evergreen]

Three pricing logics exist; only one is correct:
- **Cost-plus** — wrong for software; your cost is invisible and irrelevant to the buyer ("the demand curve is external to you" — patio11). [2026] caveat: AI inference makes cost a *floor* you must know, but still not how you set price.
- **Competitor-based** — a sanity check and an anchor in the buyer's head, dangerous as a strategy.
- **Value-based** — the winner: quantify the economic value for one segment, charge ~10–20% of it. [Evergreen]

Run the worksheet below on any idea: half a day of desk work plus 15–20 conversations. Steps are [Evergreen] method; calibrate numbers against the [2026] benchmarks noted.

---

## Step 1 — Hypothesize the value metric

Complete the sentence: "My customer gets more value from this when ___ increases."

- [ ] List 2–3 candidate metrics (seats? invoices processed? tickets resolved? meetings booked?).
- [ ] Test each against the three properties of a good value metric: (1) tracks the value the customer receives; (2) the customer can understand and predict it; (3) it grows as the customer grows, so revenue expands without a re-sale (this is what produces >100% net revenue retention).
- [ ] Circle one. The metric matters more than the number — get it right and "there is no reason for your customers to churn" (Patrick Campbell).

Quick reference:

| Metric | Best when | Failure mode |
|---|---|---|
| Per seat | Value scales with humans using it | AI does the work → fewer seats → revenue shrinks as product improves [2026] |
| Per usage | Value scales with volume; technical buyer can forecast | Unpredictable bills scare buyers |
| Per outcome | Result is countable and attributable | Attribution fights; you underwrite performance risk |
| Flat / tiered | Simplicity sells; SMB self-serve | Big customers underpay; no expansion path |

## Step 2 — Quantify the value for ONE segment

- [ ] Pick one tight segment (e.g., "Shopify merchants doing $5–50M GMV"), not "businesses."
- [ ] Build the value equation with real numbers: hours saved × **fully-loaded** hourly cost (≈1.3× base salary ÷ ~2,000 hrs/yr) + revenue gained + risk reduced. Write down the annual value number.
- [ ] Choose the comparable: software budget or labor budget? If your product *does the work* rather than helping a human do it, price against labor — labor budgets are ~10x bigger, which is why AI products sign contracts SaaS never could. [2026]

## Step 3 — Set the hypothesis price at ~10–20% of value

- [ ] Charge a fraction of value delivered (the "10x rule": save them $500K/yr, charge $50K/yr — they keep 90% of the surplus and still feel like winners).
- [ ] Sanity-check three ways: (a) competitor/adjacent anchors the buyer already knows; (b) your unit cost floor — require ≥70% gross margin at the hypothesis price ([2026]: know your inference cost per unit of value, e.g., "one resolved ticket costs us $0.11 of compute," and never price below a floor above it); (c) the go-to-market it implies — under ~$5K/yr must be self-serve; $25K+/yr can carry salespeople.
- [ ] Then apply the most-validated pricing advice in startup history: **whatever you were planning to charge is probably too low** ("Raise Prices" — Andreessen's billboard). Underpricing forecloses sales hiring, signals low quality, and doesn't even maximize adoption.

## Step 4 — Test willingness to pay (before building)

72% of new products miss revenue targets and ~80% of companies never ask about price until the product is done (Ramanujam/Simon-Kucher). Have the price conversation first. [Evergreen]

- [ ] In 15–20 prospect conversations, after walking through problem + proposed solution, ask Ramanujam's three questions:
  1. "What would be an **acceptable** price?" (a lowball)
  2. "What would be an **expensive** price — you'd think hard but might still buy?" (closest to true willingness to pay)
  3. "What would be a **prohibitively expensive** price — a non-starter?" (your ceiling)
- [ ] When someone reacts to a price, ask *why*. "Too expensive" + silence is negotiation; "too expensive because our whole tooling budget is $X" is data.
- [ ] Ask the follow-up nobody asks: "How would you prefer to pay — per person, per [unit of work], flat?" — this validates your Step-1 metric.
- [ ] Never ask "would you pay for this?" Everyone says yes to be polite.
- [ ] Optional: field a Van Westendorp survey (≥30 respondents, one segment): four questions — too expensive / too cheap (quality doubt) / getting expensive / bargain. Plot cumulative curves; read PMC (floor), OPP (fewest rejections), PME (ceiling). Treat it as a floor- and range-finder, not gospel — it systematically compresses the top end.
- [ ] Then the real seed-stage A/B test: **quote your hypothesis price in live sales conversations with a straight face.** If nobody flinches, double it for the next prospect. You're correctly priced when ~20–30% of qualified prospects push back. Losing zero deals on price means you're too cheap. (Skip landing-page price A/B tests — you lack the conversion volume, and your uncertainty is $99 vs $999, not $99 vs $119.)

## Step 5 — Package into three tiers

Good-better-best exploits robust buyer psychology: **Goldilocks** (buyers pick the middle — make it the one you want to sell), **anchoring** (show value, then price; show top tier, then middle), **decoy** (Ariely's Economist experiment: an unattractive option flipped bundle choice from 32% to 84%). [Evergreen]

- [ ] Middle tier = the package and price you actually want to sell, aimed at your core segment.
- [ ] Top tier = anchor + enterprise gates: SSO, audit logs, compliance, SLAs, "contact sales" (don't publish enterprise pricing — enterprise value varies 10x between customers).
- [ ] Bottom tier = entry point, capped on the usage metric so growth forces upgrades.
- [ ] Gate features by demand, not engineering effort — classify as **leaders** (people pay for these; anchor tiers on them), **fillers** (bundle in), **killers** (unbundle; forcing payment for these kills deals).
- [ ] If PLG: free tier capped on an engagement dimension that grows with dependence (Slack's 10K-message history — teams hit it exactly when hooked), never on core value.
- [ ] Annual prepay at ~15–20% off monthly — cash upfront is the cheapest financing you'll ever get, and annual commitment slashes churn.

## Step 6 — Ship, measure, revisit in 6 months

- [ ] Watch: close rate by price quoted; discount depth; expansion revenue (is the metric growing inside accounts?); gross margin per account ([2026]: token burn by cohort).
- [ ] Raise prices for new customers first (zero churn risk, immediate market signal); grandfather existing customers 6–12 months, then migrate with notice and a value story, ideally sweetened with features.
- [ ] Revisit every 6–12 months; early on, treat every 5–10 new customers as a chance to test a higher quote. Price is a product — version it.

---

## Worked example (end to end)

**Product:** automated invoice reconciliation for mid-size e-commerce companies.

1. **Value metric:** invoices processed per month (tracks value, predictable, grows with the customer). Runner-up "seats" rejected — finance teams are small and shrinking.
2. **Value quantified:** target segment's finance team spends 2 FTEs × $80K fully-loaded = $160K/yr on reconciliation; product eliminates ~70% = **$112K/yr of value**. Comparable: labor budget.
3. **Hypothesis price:** 10–20% of value → **$10K–25K/yr**. Cost floor check: serving cost ~$100/customer/month → ≥95% gross margin at hypothesis price. GTM check: $15K/yr supports inside sales. (Cost-plus logic would have said "$99/month" — leaving ~95% of the achievable price on the table *and* signaling toy.)
4. **WTP tested:** 18 interviews → median acceptable $8K, expensive $18K, prohibitive $40K. Quoted $15K in live calls; 4 of 15 pushed back (~27%) → correctly priced.
5. **Tiers:** Starter **$500/mo** (1 entity, 500 invoices/mo, email support) → Growth **$1,500/mo** (3 entities, 5,000 invoices, approval workflows, priority support) → Enterprise **from $60K/yr** (unlimited, SSO, audit log, ERP integrations, dedicated support). The Enterprise anchor makes $1,500 look moderate; the invoice metric grows with the customer; SSO/audit gates make serious mid-market self-select upward. Annual prepay: 15% off.
6. **Revisit plan:** 6 months; new price for new customers first.

---

## 2026 checkpoints for AI products

- [ ] Know your inference cost per unit of value, and price with a floor above it. **Flat-rate unlimited plans are how AI startups die** — 10% of power users burn 70–80% of compute.
- [ ] Default structure: **hybrid** — platform/seat fee for predictability + usage/credits for consumption (37% of B2B software companies and the fastest-growing structure; investors prefer hybrid 35% / outcome 26% / usage 24% over flat 10% and pure seats 5%). [2026]
- [ ] Credits: publish a legible exchange rate, offer spend caps and alerts, bundle a predictable base allotment — buyers hate black-box math, and credit repricing revolts are the canonical 2026 failure (Cursor's apology-and-refunds episode).
- [ ] Outcome pricing: run the **CAMP** test first — Consistency of outcomes, Attribution, Measurability, Predictability. Use only when the outcome is unambiguous, countable, and cleanly attributable (Intercom Fin's $0.99 per resolution), and you have performance data to underwrite the risk. Otherwise you've reinvented a contingency-fee law firm with worse margins.

*Deeper reading: [`03-pricing.md`](https://github.com/bharatnain/research/blob/main/startup-business-models/03-pricing.md) in the `bharatnain/research` repo (frameworks, Van Westendorp mechanics, Slack/HubSpot/Fin case studies).*
