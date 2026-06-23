---
title: "Reasoning Blueprint: Churn Analysis"
type: reasoning-blueprint
skill: churn-analysis
version: 1.0.0
---

# Reasoning Blueprint: Churn Analysis

Load this blueprint when advanced reasoning is activated for churn analysis work.
It provides the domain-specific taxonomy, heuristics, and expert judgment patterns
that shape expert-level post-loss root cause analysis and portfolio pattern detection.

---

## Problem Classification Taxonomy

### Type A: Signal-Rich Loss
**Characteristics**: CRM data, call recordings, health history, and support tickets available. Timeline reconstruction can be data-driven.
**Primary Risk**: Over-attributing to the most visible signal while missing the actual root cause buried in earlier, subtler indicators.
**Expert Focus**: Reconstruct the full signal chain chronologically — the first signal matters more than the loudest one.

### Type B: Data-Sparse Loss
**Characteristics**: Minimal CRM history, no call recordings, sparse health data. Analysis depends heavily on CSM recollection and stated close reason.
**Primary Risk**: Accepting the CRM close reason at face value — stated reasons and actual root causes diverge in 40-60% of cases [Moderate].
**Expert Focus**: Triangulate across whatever sources exist; explicitly flag confidence ceiling imposed by data gaps.

### Type C: Portfolio Pattern Scan
**Characteristics**: Root cause already established from a prior analysis. Request is to find matching signal patterns across active accounts.
**Primary Risk**: False positives — flagging accounts that share surface signals but lack the underlying structural vulnerability.
**Expert Focus**: Match on signal combination and account context (tenure, segment, relationship depth), not individual signals in isolation.

### Type D: Batch Retrospective
**Characteristics**: Multiple losses analyzed together (quarter-end, annual review). Goal is aggregate pattern extraction, not deep single-account analysis.
**Primary Risk**: Averaging across heterogeneous losses — mixing controllable and uncontrollable churn obscures actionable patterns.
**Expert Focus**: Separate controllable from uncontrollable before aggregating; weight by ARR impact, not count.

### Secondary Dimension: Data Availability
- **Connected** (CRM + CS Platform + call data): Full reconstruction possible
- **Partial** (CRM only or CS Platform only): Timeline has gaps — flag them
- **Manual** (user-provided context only): Confidence ceiling is [Moderate] at best

---

## Domain Heuristics

1. **The First Signal Rule**: The root cause almost always traces to the earliest signal in the timeline, not the most dramatic one. Work backward from churn confirmation to find when the first crack appeared.

2. **The 90-Day Threshold**: If the first visible signal appeared fewer than 90 days before renewal, the problem is likely signal coverage — the team couldn't see it. If it appeared 90+ days out, the problem is response process — the team didn't act on it. Different failures require different fixes.

3. **The Stated-vs-Actual Gap**: CRM close reasons are narratives, not diagnoses. "Budget cut" frequently masks relationship gaps; "went with competitor" frequently masks product gaps that preceded the competitive evaluation. Always look one layer deeper than the stated reason.

4. **The Single-Thread Test**: If the churned account had fewer than 3 active stakeholder relationships in the final 6 months, relationship gap is either the root cause or a critical contributing factor — regardless of what the stated reason says.

5. **The Controllability Filter**: Separate force majeure losses (acquisition, closure, regulatory) before drawing any process conclusions. Including uncontrollable losses in response-adequacy metrics corrupts the signal.

6. **The Timeline Lag Diagnostic**: The gap between signal appearance and signal recognition is the single most actionable metric in a churn analysis. A 60-day lag points to a monitoring gap; a 10-day lag with no action points to an escalation gap.

7. **The Portfolio Scan Threshold**: A signal pattern must include at least 2 co-occurring signals to warrant a portfolio scan flag. Single-signal matches produce noise that erodes trust in the scan.

---

## Common Failure Modes by Analysis Type

### Signal-Rich Loss Failures
- **Recency bias in root cause**: Assigning root cause to the last signal before churn rather than the first.
  → Fix: Build timeline chronologically first; identify the earliest signal before assigning root cause.
- **Confusing correlation with causation**: Multiple signals co-occurred; analyst picks the wrong one as primary.
  → Fix: Apply "would removing this signal have changed the outcome?" counterfactual to each candidate.

### Data-Sparse Loss Failures
- **Accepting CRM close reason as root cause**: Stated reason becomes the analysis conclusion without independent evidence.
  → Fix: Label CRM reason as "stated reason" and separately assess root cause with explicit [Low Confidence] tag if no corroborating evidence.
- **Fabricating a timeline**: Filling gaps with plausible but unverified events to create a complete narrative.
  → Fix: Leave gaps visible; mark reconstructed segments with confidence bands.

### Portfolio Scan Failures
- **Single-signal matching**: Flagging every account with one matching signal, producing an unusable list.
  → Fix: Require 2+ co-occurring signals plus contextual match (tenure, segment) before flagging.
- **Treating scan output as risk tiers**: Portfolio flags presented as risk assessments without running `/renewals:risk-assessment`.
  → Fix: Label every flagged account as "lead for risk assessment" — never assign a risk tier from scan data alone.

### Batch Retrospective Failures
- **Mixing controllable and uncontrollable**: Including force majeure losses in aggregate pattern analysis.
  → Fix: Separate into controllable and uncontrollable cohorts before any aggregation.
- **Count-based aggregation**: Treating all losses equally regardless of ARR impact.
  → Fix: Weight patterns by ARR lost, not by count of events.

---

## Expert Judgment Patterns

### Root Cause Depth Decisions
- If the stated reason is commercial (price, budget), verify whether a relationship or adoption gap preceded the commercial conversation — commercial reasons are frequently downstream of earlier failures.
- If multiple contributing factors are present, the primary root cause is the one that, if addressed, would most likely have changed the outcome.

### Response Adequacy Decisions
- Evaluate the response against what was visible at the time, not against what is known now. Hindsight bias in response assessment produces unfair conclusions and unusable lessons.
- A save strategy that was appropriate but failed is not a process gap — distinguish strategy selection failures from execution failures from unwinnable situations.

### Lesson Actionability Decisions
- A lesson must specify what to do differently, not just what went wrong. "We should have noticed the signal earlier" is an observation; "Add [signal type] to the weekly health review checklist" is a lesson.
- Route systemic lessons (missing escalation protocols, signal coverage gaps) to Head of CS. Route tactical lessons (timing, stakeholder engagement) to the team.

### Confidence Decisions
- With 2+ independent data sources corroborating root cause: [High Confidence].
- With 1 data source or partial corroboration: [Moderate].
- With stated reason only, no corroboration: [Low Confidence] — say so explicitly.

---

*Reasoning Blueprint: Churn Analysis v1.0*
*For use with churn-analysis skill*
