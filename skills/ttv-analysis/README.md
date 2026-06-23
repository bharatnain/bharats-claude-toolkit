# onboarding.ttv-analysis

Time-to-value analysis for onboarding performance — single account or portfolio. Reads TtV targets by segment and milestone framework from the onboarding profile. Analyzes actual milestone completion dates against targets to surface pace signals and produce recommendations for accounts running behind. All TtV outputs are labeled as internal planning targets — never customer commitments.

## Use it for

- Single-account TtV assessment (--account, default)
- Comparative TtV view across closed or active onboarding accounts (--portfolio)
- Common delay pattern identification with intervention recommendations (--patterns)

## Don't use it for

- Presenting TtV data to customers as commitments
- Modifying PM connector data

## How to trigger it

Say something like:

- "time to value"
- "TtV"
- "onboarding pace"
- "behind on onboarding"
- "delay patterns"

## What you get

- TtV assessment with pace rating and variance (--account)
- Portfolio TtV comparison table (--portfolio)
- Delay pattern report with intervention recommendations (--patterns)

## Prerequisites

- onboarding CLAUDE.md (TtV targets by segment, milestone framework)

## Governance

- All TtV outputs labeled as internal planning targets — not customer commitments
- Targets sourced from profile; no hardcoded benchmarks

## See also

- onboarding.milestone-tracker
- onboarding.blocker-review

---

*Domain: `onboarding` · Skill ID: `onboarding.ttv-analysis`*
