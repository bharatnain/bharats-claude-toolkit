---
title: "Reasoning Blueprint: Renewal Forecast"
type: reasoning-blueprint
skill: renewal-forecast
version: 1.0.0
---

# Reasoning Blueprint: Renewal Forecast

Load this blueprint when Tier 3 reasoning is activated for renewal forecasting work.
It provides the domain-specific taxonomy, heuristics, and expert judgment patterns
that shape expert-level weighted renewal forecast construction.

---

## Problem Classification Taxonomy

### Type A: Full Book Forecast
**Characteristics**: Complete book-of-business forecast with all pipeline stages, scenario modeling, cohort breakdown, and GRR/NRR projection. Default mode.
**Primary Risk**: Stale CRM data produces a confident-looking forecast built on outdated pipeline stages — the numbers look precise but the inputs are wrong.
**Expert Focus**: Validate data freshness per account before weighting; a 7-day-old "verbal commitment" may already be lost.

### Type B: Cohort-Scoped Forecast
**Characteristics**: Focused on a single renewal window (90/60/30-day). Narrows the aperture to accounts in active negotiation.
**Primary Risk**: Treating 30-day cohort accounts with the same rigor as 90-day — the 30-day window demands escalation paths and decision-forcing actions, not pipeline projections.
**Expert Focus**: Every at-risk account in the 30-day cohort must have a named escalation owner or get flagged immediately.

### Type C: Segment Forecast
**Characteristics**: Single customer segment (enterprise, mid-market, SMB). Compares segment GRR/NRR against overall book targets.
**Primary Risk**: Applying book-level default weights to a segment where the renewal motion differs — enterprise verbal commitments are more reliable than SMB ones.
**Expert Focus**: Check whether configured methodology provides segment-specific forecast weights; flag if defaults are applied to a segment with different dynamics.

### Type D: Single-Account Pipeline Addition
**Characteristics**: Adding one account's renewal to the pipeline view. Smallest scope — collects ARR, stage, risk signals, and places the account.
**Primary Risk**: Accepting the user's stated stage without cross-referencing risk signals — an account described as "open" with active churn signals belongs in "at risk."
**Expert Focus**: Validate stage placement against available risk signals before accepting the user's classification.

### Secondary Dimension: Data Availability
- **CRM-Connected**: Live pipeline data available; validate freshness and completeness.
- **Manual Input**: User-provided context only; no timestamp, higher fabrication risk — request ARR explicitly, never interpolate.

---

## Domain Heuristics

1. **The Freshness Floor Rule**: Any CRM data older than 7 days is stale for forecasting. At-risk and 30-day accounts older than 3 days should be flagged for immediate refresh.

2. **The Expansion Exclusion Rule**: Expansion ARR never enters GRR. It enters NRR only after economic buyer qualification AND formal pipeline stage (CPQ quote or opportunity). Everything else is tagged `[early signal]`.

3. **The Likely-Is-Leadership Rule**: The "likely" scenario is the one you submit to leadership. Best case is aspiration; worst case is risk planning. Likely must be defensible — it uses default weights and zero expansion.

4. **The Escalation Completeness Rule**: A risk flag without a named escalation owner is an incomplete forecast item. Surface it as a recommended action, not just a pipeline annotation.

5. **The Stage-Signal Alignment Rule**: Pipeline stage must be consistent with observable signals. If a user says "open" but describes active churn signals, classify as "at risk" and explain the reclassification.

6. **The No-Fabrication Rule**: Unknown ARR is excluded from totals, never estimated. Mark the account `[ARR unknown — excluded from totals]` and request the figure.

7. **The Commitment Language Rule**: Every scenario total, GRR projection, and NRR figure gets flagged with `[review — could be read as a revenue commitment]`. No exceptions, even for internal-only output.

---

## Common Failure Modes by Forecast Type

### Full Book Failures
- **Stale pipeline mirage**: CRM data is old but presented without freshness flags.
  -> Fix: Timestamp every data source; flag >7-day CRM and >3-day CS Platform data in reviewer note.
- **Expansion leakage into GRR**: Expansion ARR accidentally included in gross retention math.
  -> Fix: Calculate GRR before NRR; verify expansion appears only in the NRR line with qualification tags.

### Cohort-Scoped Failures
- **30-day cohort without escalation**: At-risk accounts in the decision window listed without named owners.
  -> Fix: Run escalation completeness check on every at-risk account in 30-day cohort before presenting.
- **Cohort boundary miscalculation**: Account renewal dates placed in wrong cohort due to date math errors.
  -> Fix: Calculate days-to-renewal from today's date; double-check boundary accounts (exactly 30, 60, 90 days).

### Segment Failures
- **Default weight misapplication**: Book-level weights applied to a segment with different renewal dynamics.
  -> Fix: Check configured methodology for segment-specific weights; flag when defaults are used for non-default segments.

### Single-Account Failures
- **Stage acceptance without validation**: User-stated stage accepted when risk signals contradict it.
  -> Fix: Cross-reference stated stage against risk signals; if contradictory, propose reclassification with reasoning.
- **Missing ARR interpolation**: ARR not provided, so a figure is estimated from averages.
  -> Fix: Never interpolate. Mark `[ARR unknown — excluded from totals]` and request the actual figure.

---

## Expert Judgment Patterns

### Scenario Calibration Decisions
- When historical save rates are available, use them instead of defaults; note the substitution.
- When an account has been at-risk for >60 days with no escalation progress, apply 0% save rate in likely scenario regardless of default.
- Best-case expansion conversion at 30% is a ceiling, not a target — reduce if qualification signals are weak.

### Data Confidence Decisions
- Two or more live sources corroborating = [High Confidence]; single source or partially stale = [Medium]; manual input only = [Low].
- When CRM and user-provided data conflict on ARR or stage, flag both and ask — never silently prefer one.

### Escalation Routing Decisions
- At-risk + 30-day cohort = immediate escalation recommendation, not optional.
- At-risk + no discount authority for save strategy = flag the approval chain gap before presenting the save scenario.
- Multiple at-risk accounts from same segment = pattern signal; recommend segment-level review in addition to account-level actions.

---

*Reasoning Blueprint: Renewal Forecast v1.0*
*For use with renewal-forecast when Tier 3 reasoning is activated*
