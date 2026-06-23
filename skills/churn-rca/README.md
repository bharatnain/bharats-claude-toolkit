# renewals.churn-rca

Root-cause analysis of full cancellation (churn) events. Identifies why an account churned, which signals were present and missed, and what process or product changes would reduce recurrence. Scoped to full cancellations only — contract contractions route to renewals.downgrade-analysis.

## Use it for

- Post-churn retrospective for a single churned account
- Portfolio-level churn pattern scan across multiple lost accounts
- Quick signal audit to identify earliest missed warning

## Don't use it for

- Active at-risk accounts (use renewals.risk-assessment)
- Contract contractions or downgrades (use renewals.downgrade-analysis)
- Expansion or renewal forecasting
- Win-loss analysis for new logos (sales domain)

## How to trigger it

Say something like:

- "why did [account] churn"
- "churn RCA"
- "post-mortem on lost account"
- "what signals did we miss"
- "churn retrospective"
- "--portfolio-scan"

## What you get

- Churn root-cause report (structured markdown)
- Signal timeline (earliest-to-latest warning indicators)
- Process gap recommendations

## Prerequisites

- Domain CLAUDE.md (reads at startup; routes to cold-start-interview if missing)
- Account name or ID, or list for portfolio scan
- {'CRM data or manual input': 'contract end date, ARR, churn reason, last meaningful contact'}
- Support history summary (optional but improves accuracy)

## Governance

- Account content is confidential — no cross-account data sharing in outputs
- CRM data older than 7 days triggers freshness warning
- Portfolio scan limited to accounts explicitly provided; no CRM bulk export without authorization

## See also

- renewals.risk-assessment
- renewals.downgrade-analysis
- renewals.renewal-forecast
- renewals.cold-start-interview

---

*Domain: `renewals` · Skill ID: `renewals.churn-rca`*
