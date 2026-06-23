# renewals.renewal-forecast

Builds a weighted renewal forecast across the full book or a scoped subset. Applies five pipeline stage weights, produces three scenarios (best/likely/worst), and calculates GRR and NRR correctly. All figures flagged as not-yet-a-revenue-commitment. Expansion included in NRR only when Qualified + formal pipeline confirmed.

## Use it for

- Full book renewal forecast
- 90/60/30-day cohort forecast
- Segment-level forecast
- Single-account pipeline addition

## Don't use it for

- Individual account risk assessment (use risk-assessment)
- Expansion opportunity identification (use expansion-signal)
- Price increase planning (use price-increase-prep)

## How to trigger it

Say something like:

- "renewal forecast"
- "what's my renewal number"
- "forecast this quarter's renewals"
- "GRR forecast"
- "NRR forecast"
- "--full"
- "--cohort"
- "--segment"
- "--account"

## What you get

- Forecast table (per-account weighted ARR by stage)
- Three-scenario summary (best/likely/worst)
- GRR and NRR calculations with formula documentation
- At-risk accounts with named escalation owners

## Prerequisites

- Domain CLAUDE.md
- {'Account list with': 'ARR, pipeline stage, contract end date, risk tier'}
- CRM data or manual input
- Expansion pipeline data (for NRR; only if Qualified + formal pipeline)

## Governance

- All ARR figures flagged "[review — not yet a revenue commitment]"
- Expansion in NRR only when economic buyer qualified + formal pipeline confirmed
- {'Expansion never in GRR — formula strictly': '(Starting ARR − Churn − Contraction) / Starting ARR'}
- {'Pipeline stage weights': 'Open 70%, Verbal commitment 90%, At risk 25%, Won 100%, Lost 0%'}
- At-risk accounts require named escalation owner in output
- CRM data older than 7 days triggers freshness warning
- No fabricated ARR figures

## See also

- renewals.risk-assessment (risk tiers required input)
- renewals.expansion-signal (NRR expansion source)
- renewals.negotiation-prep (downstream for at-risk accounts)
- renewals.price-increase-prep (affects ARR inputs)
- renewals.executive-summary (consumes forecast output)
- renewals.cold-start-interview (domain config pre-flight)

---

*Domain: `renewals` · Skill ID: `renewals.renewal-forecast`*
