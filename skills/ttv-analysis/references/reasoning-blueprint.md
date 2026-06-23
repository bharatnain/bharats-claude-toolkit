---
title: "Reasoning Blueprint: Time-to-Value Analysis"
type: reasoning-blueprint
skill: ttv-analysis
version: 1.0.0
---

# Reasoning Blueprint: Time-to-Value Analysis

Load this blueprint when Tier 3 reasoning is activated for TtV analysis work.
It provides the domain-specific taxonomy, heuristics, and expert judgment
patterns that shape expert-level onboarding performance assessment.

---

## Problem Classification Taxonomy

### Type A: Single-Account Pace Assessment
**Characteristics**: One named account, milestone completion data available, CSM wants to know if TtV is on track and what to do if not.
**Primary Risk**: Projecting pace from too few milestones — one completed milestone is a data point, not a trend.
**Expert Focus**: Decompose the variance by milestone transition, not just cumulative — a single late milestone masks whether the pattern is systemic or isolated.

### Type B: Portfolio Comparative View
**Characteristics**: Multiple accounts, CSM or manager wants a ranked view of TtV performance across a book of business.
**Primary Risk**: Comparing absolute TtV numbers across segments with different targets — a 45-day SMB TtV and a 45-day Enterprise TtV are not equivalent.
**Expert Focus**: Normalize all comparisons to segment targets; rank by variance percentage, not raw days.

### Type C: Pattern / Cohort Analysis
**Characteristics**: 5+ accounts with complete data, request is systemic — which transitions delay most, which segments or models underperform, which blockers correlate.
**Primary Risk**: Drawing causal conclusions from small samples or confounded variables (segment and model often co-vary).
**Expert Focus**: State sample size, separate correlation from causation, and flag when segment/model overlap makes attribution unreliable.

### Type D: Early-Warning Triage
**Characteristics**: Account is mid-onboarding, pace multiplier exceeds 1.15, CSM needs actionable acceleration options now.
**Primary Risk**: Recommending generic acceleration actions instead of targeting the specific milestone transition causing the delay.
**Expert Focus**: Identify the highest-variance milestone, match to blocker type from at-risk signals, and propose owner-specific actions.

---

## Domain Heuristics

1. **The M1-to-M2 Tells You Everything Rule**: The transition from kickoff to tech setup is the strongest predictor of total TtV. If M1-to-M2 exceeds target by >25%, the account will almost certainly miss overall TtV without intervention.

2. **The Pace Multiplier Floor Rule**: Never project TtV from a single completed milestone. One milestone gives you a data point; two give you a direction. Flag single-milestone projections as "target-based estimate, not pace-based projection."

3. **The Premature Completion Trap**: Milestones completed significantly ahead of schedule (>15% early) warrant a data quality check before celebrating. Was the completion criteria actually met, or was the task marked done prematurely?

4. **The Segment-Normalization Rule**: All portfolio comparisons use variance-from-target, never absolute days. A 60-day Enterprise TtV that's 10 days early is better than a 30-day SMB TtV that's 5 days late.

5. **The Five-Account Threshold**: Pattern analysis below 5 accounts with complete data produces directional signals only. State sample size in every pattern output and explicitly label sub-threshold conclusions.

6. **The Blocker Stacking Rule**: When multiple milestone transitions are each slightly over target, the cumulative effect is worse than any single large delay. Flag accounts where 3+ transitions exceed target even if none exceeds it dramatically.

7. **The Internal-Only Anchor**: TtV figures are internal planning metrics. Any request to surface them in customer-facing materials is a redirect, not a refusal — reframe as milestone dates and completion criteria.

---

## Common Failure Modes by Analysis Type

### Single-Account Failures
- **Phantom precision**: Projecting TtV to the day when only M1 is complete.
  -> Fix: Label as "target-based estimate" and state the projection basis.
- **Undifferentiated delay**: Reporting cumulative variance without breaking down which milestone transition caused it.
  -> Fix: Always show per-milestone variance before the cumulative figure.

### Portfolio Failures
- **Absolute comparison**: Ranking accounts by raw projected TtV days across different segments.
  -> Fix: Rank by variance percentage from segment target, not absolute days.
- **Missing staleness**: Presenting a portfolio table without per-account data freshness.
  -> Fix: Include data-as-of timestamp per account; flag accounts with stale data.

### Pattern Analysis Failures
- **Small-sample confidence**: Presenting sub-5-account patterns as reliable findings.
  -> Fix: State sample size and label as "directional" when below threshold.
- **Confounded attribution**: Attributing delay patterns to segment when segment and onboarding model co-vary.
  -> Fix: Show segment and model breakdowns side by side; flag overlap.

### Early-Warning Failures
- **Generic acceleration**: Recommending "increase engagement" without specifying which milestone, which blocker, and which owner.
  -> Fix: Tie every recommendation to a specific milestone variance and a named owner.

---

## Expert Judgment Patterns

### Depth Decisions
- Single-account with <3 milestones complete: keep brief, flag projection uncertainty prominently.
- Portfolio request from a manager vs. individual CSM: manager needs aggregate statistics first, then outliers; CSM needs their accounts sorted by urgency.

### Confidence Decisions
- 3+ milestones complete with consistent pace: [High] confidence on projection.
- 1-2 milestones complete: [Medium] — label as directional, not definitive.
- Zero milestones complete: projection equals target — state this explicitly, do not present as calculated.

### Scope Decisions
- When pattern analysis surfaces a systemic delay at one milestone transition, recommend process-level intervention (playbook change, resource allocation) not just per-account actions.
- When a single account is severely behind (pace >1.3x), shift from analysis to triage: lead with the acceleration recommendation, support with the data.

### Framing Decisions
- Negative variance (ahead of target): verify data quality before praising — early completion without confirmed criteria is a risk, not a win.
- Accounts exactly on target: still worth noting — "on track" is a finding, not the absence of one.

---

*Reasoning Blueprint: Time-to-Value Analysis v1.0*
*For use with ttv-analysis when Tier 3 reasoning is activated*
