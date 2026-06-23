---
title: Health Score Review Reasoning Blueprint
type: reasoning-blueprint
skill: health-score-review
version: 1.0.0
---

# Health Score Review — Reasoning Blueprint

## Problem Classification Taxonomy

### Type A: Single Account — Data-Rich
- **Characteristics:** CS Platform connected, health model configured, component scores available, trend data present
- **Primary Risk:** Over-reliance on composite score masks deteriorating individual components
- **Expert Focus:** Component-level trend direction; which signal is driving the score, not the score itself

### Type B: Single Account — Data-Sparse
- **Characteristics:** Partial signals only (e.g., user-provided notes, no CS Platform), missing components, stale NPS
- **Primary Risk:** Incomplete classification presented with false confidence; gaps not surfaced
- **Expert Focus:** Name every gap explicitly; classify with caveats; never fill unknowns with assumptions

### Type C: Portfolio Triage — Prioritization
- **Characteristics:** Multiple accounts, need ranked risk output, time-constrained review
- **Primary Risk:** ARR-blind prioritization (treating a $5K Red the same as a $500K Yellow approaching renewal)
- **Expert Focus:** Compound risk factors — renewal proximity x health status x ARR; not health alone

### Type D: Alert-Triggered Review
- **Characteristics:** Fired by a health alert, usage drop, or escalation event; reactive context
- **Primary Risk:** Anchoring on the triggering signal and missing concurrent deterioration in other components
- **Expert Focus:** Full component scan even when one signal triggered the review; alerts are symptoms, not diagnoses

### Type E: Pre-Renewal Health Check
- **Characteristics:** Renewal within 90 days, proactive review, stakeholder visibility likely
- **Primary Risk:** Optimism bias — CSM minimizes Yellow signals near renewal to avoid escalation overhead
- **Expert Focus:** Honest classification with escalation path ready; renewal proximity amplifies every signal

## Domain Heuristics

### H1: The 20% Usage Drop Rule
A 20%+ decline in primary usage metric over 30 days is never noise. Even if other signals are Green, this warrants a proactive outreach within 7 days. Usage drops precede churn signals by 60-90 days on average.

### H2: Stale NPS is Worse Than Bad NPS
An NPS score older than 6 months tells you nothing about current sentiment. Treat it as Unknown, not as the last recorded value. A detractor score from 3 months ago with no recovery action is an active risk.

### H3: The Contact Gap Multiplier
Days-since-last-contact risk compounds with health status. A Green account silent for 45 days is a watch item. A Yellow account silent for 45 days is approaching Red. Apply the configured threshold, but weight it by current health tier.

### H4: Executive Sponsor Departure Overrides Everything
When the executive sponsor leaves, the account's effective health drops one tier regardless of component scores. Product usage and NPS mean little when the internal champion is gone.

### H5: Ticket Velocity Over Ticket Count
Three open tickets is less concerning than going from zero to three in two weeks. Rate of change in support load signals emerging frustration before severity escalation.

### H6: Renewal Proximity Amplifier
Any Yellow or Red signal within 90 days of renewal gets treated one severity level higher for action planning. A Yellow account renewing in 30 days gets Red-tier intervention urgency.

### H7: The Multi-Signal Convergence Rule
Two moderate signals in different components (e.g., usage dip + missed QBR) are more concerning than one strong signal. Convergence across independent components indicates systemic disengagement, not an isolated event.

## Common Failure Modes

### Type A (Data-Rich) Failures
1. **Score-anchoring:** Reporting the composite score without decomposing components. Fix: Always lead with component-level breakdown; composite score is a summary, not the analysis.
2. **Trend blindness:** Showing current values without 30/60/90-day direction. Fix: Include trend arrows and rate of change for every component with historical data.
3. **Green complacency:** Skipping churn signal scan for Green accounts. Fix: Run churn signal checklist regardless of overall health tier.

### Type B (Data-Sparse) Failures
1. **Confidence inflation:** Classifying Red/Yellow/Green without flagging which components are missing. Fix: Append data sufficiency note to every classification; mark missing components as Unknown.
2. **Assumption-filling:** Treating no news as good news for missing signals. Fix: Absence of data is Unknown, never No. Surface the gap in the reviewer note.

### Type C (Portfolio Triage) Failures
1. **Flat prioritization:** Sorting by health score alone without weighting ARR or renewal proximity. Fix: Compound ranking = health tier x ARR x renewal proximity.
2. **Confidentiality leak:** Distributing portfolio-level ARR and health data without audience check. Fix: G5 destination check before any portfolio output leaves the CSM's view.

### Type D (Alert-Triggered) Failures
1. **Tunnel vision:** Investigating only the triggering signal. Fix: Full component scan — the alert is the entry point, not the diagnosis.
2. **Premature escalation:** Escalating on alert alone before confirming severity with component context. Fix: Classify after full review; escalate per matrix, not per alert.

### Type E (Pre-Renewal) Failures
1. **Optimism bias:** Downgrading Yellow signals to avoid escalation conversation before renewal. Fix: Apply H6 — renewal proximity amplifies, never dampens.
2. **Missing stakeholder context:** Reviewing health without checking sponsor status. Fix: Always verify executive sponsor and champion status for pre-renewal reviews.

## Expert Judgment Patterns

### Scope Decisions
- Single account with live data: full component breakdown + trend + churn signals + interventions
- Single account with partial data: component breakdown with gaps named + point-in-time classification + data acquisition recommendations
- Portfolio triage: ranked table with compound risk score; deep dives only for top 3 Red accounts unless requested

### Sequencing Decisions
- Always: config check -> data gather -> component breakdown -> churn signal scan -> classification -> interventions
- Never classify before completing the churn signal scan — signals can override component-based classification
- Trend analysis before interventions — direction determines urgency of the recommended action

### Depth Decisions
- Green accounts get a maintenance-level review: component table + next QBR date + any approaching staleness flags
- Yellow accounts get full analysis: all components + trend + specific outreach recommendation with timeline
- Red accounts get full analysis plus escalation routing and recovery action plan with named owners and SLAs

### Stakeholder Decisions
- CSM-only output: full detail including ARR, internal notes, escalation recommendations
- Cross-functional distribution (e.g., to VP CS): strip internal notes, add context for non-CSM readers, include executive summary
- Portfolio reports leaving CS org: G5 confidentiality gate — ARR and health classifications require authorization

### Confidence Decisions
- Three or more components with live data: classify with standard confidence
- One or two components only: classify with explicit partial-data caveat
- No live data (user-provided only): classify as point-in-time assessment, flag data acquisition as first recommended action
- Any component older than 30 days: flag as stale in reviewer note with source date
