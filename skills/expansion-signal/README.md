# renewals.expansion-signal

Detects and qualifies expansion opportunities within the existing customer base. Six signal types across three qualification tiers. AE routing is mandatory at Qualified tier. Expansion never included in GRR; tracked separately.

## Use it for

- Identify expansion signals before or during renewal cycle
- Qualify expansion opportunity to Pipeline-ready or Qualified tier
- Catalog all detectable signal types for the configured pricing model

## Don't use it for

- New logo expansion (sales domain)
- GRR forecasting (expansion excluded by definition)
- Accounts with active churn risk — run risk-assessment first

## How to trigger it

Say something like:

- "find expansion opportunities"
- "expansion signals for [account]"
- "upsell audit"
- "growth signals"
- "--deep"
- "--quick"
- "--catalog"

## What you get

- Expansion signal report (detected signals with qualification tier)
- AE routing notice (if Qualified tier reached)
- ARR potential estimate (Low Confidence — flagged)

## Prerequisites

- Domain CLAUDE.md
- Account usage data or summary
- Pricing model configuration (seat, usage-based, or hybrid)
- Risk-assessment output if any churn risk signals present

## Governance

- Expansion ARR potential estimates flagged "[Low Confidence]" — not revenue commitments
- AE routing mandatory when opportunity reaches Qualified tier (non-negotiable)
- Renewal risk must be addressed before expansion pursuit; skill blocks if active Critical risk
- Expansion never in GRR calculation

## See also

- renewals.risk-assessment (must check first if churn risk present)
- renewals.negotiation-prep (downstream if expansion pursued)
- renewals.renewal-forecast (NRR includes Qualified expansion in pipeline)
- renewals.cold-start-interview (domain config pre-flight)

---

*Domain: `renewals` · Skill ID: `renewals.expansion-signal`*
