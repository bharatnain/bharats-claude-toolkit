# csm.health-score-review

Reviews health scores for a single account or full portfolio. Breaks down signal components, surfaces trend direction, and recommends remediation plays. Modes: triage (quick risk scan), deep (full signal analysis), portfolio (all accounts).

## Use it for

- Account health triage before a call
- Deep health review with component analysis
- Portfolio health sweep for at-risk identification

## Don't use it for

- Health model calibration (use cs-ops.health-model-review)
- Renewal risk scoring (use renewals.risk-assessment)

## How to trigger it

Say something like:

- "health score"
- "health review"
- "how healthy is [account]"
- "portfolio health"
- "at-risk accounts"

## What you get

- Health score breakdown with trend and recommendation

## Prerequisites

- csm CLAUDE.md

## Governance

- Health score components reflect configured model — not generic defaults

## See also

- cs-ops.health-model-review
- renewals.risk-assessment
- csm.risk-flag

---

*Domain: `csm` · Skill ID: `csm.health-score-review`*
