---
title: "Reasoning Blueprint: Expansion Signal Identification"
type: reasoning-blueprint
skill: expansion-signal
version: 1.0.0
---

# Reasoning Blueprint: Expansion Signal Identification

Load this blueprint when Tier 3 reasoning is activated for expansion signal work.
It provides the domain-specific taxonomy, heuristics, and expert judgment patterns
that shape expert-level expansion signal identification and qualification.

---

## Problem Classification Taxonomy

### Type A: Seat/Usage Capacity Signal
**Characteristics**: Quantitative signal — active users approaching licensed seats, or usage approaching contracted volume limits. Data-driven, often surfaced automatically by CS Platform.
**Primary Risk**: Mistaking temporary spikes for sustained growth trends; recommending expansion on a seasonal anomaly.
**Expert Focus**: Compare 90-day trend vs. point-in-time; check whether the overage is organic adoption or a one-off project.

### Type B: Feature/Tier Upsell Signal
**Characteristics**: Qualitative signal — customer requesting features in a higher tier, expressing feature gaps in support tickets or calls, or fully adopting current tier features.
**Primary Risk**: Conflating feature curiosity with purchase intent; pushing tier upgrade when the customer is frustrated, not ready to buy.
**Expert Focus**: Distinguish between "I wish we had X" (interest) and "We need X to achieve Y by Z date" (budget-backed need).

### Type C: Cross-Sell / Multi-Product Signal
**Characteristics**: Adjacent product opportunity — customer solving a problem manually or with a competitor tool that your product line addresses. Often surfaces in QBR conversations or workflow discovery.
**Primary Risk**: Forcing a cross-sell narrative onto a customer who is satisfied with their current solution; damaging trust by appearing sales-driven.
**Expert Focus**: Validate that the pain point is real and active, not historical; confirm the adjacent product genuinely fits the workflow.

### Type D: Geographic/Organizational Expansion Signal
**Characteristics**: Structural signal — new offices, M&A activity, separate business units, or teams evaluating independently. Often discovered through LinkedIn, news, or executive conversation.
**Primary Risk**: Assuming corporate expansion equals product expansion; the new entity may have existing vendor relationships or different requirements.
**Expert Focus**: Verify whether the expansion entity has independent budget authority or rolls up to the existing contract holder.

### Type E: At-Risk Account with Expansion Signals
**Characteristics**: Mixed signal — expansion indicators coexist with churn risk (declining engagement, open escalations, stakeholder turnover). Requires triage before pursuit.
**Primary Risk**: Pursuing expansion on an account that hasn't resolved its renewal risk; the expansion conversation feels tone-deaf.
**Expert Focus**: Renewal risk must be addressed first. An expansion signal on a Red account is noise until the account is stabilized.

---

## Domain Heuristics

1. **The 80% Seat Rule**: When active users exceed 80% of licensed seats for 30+ days, the account is a seat expansion candidate — but only if the growth trend is sustained, not a one-time spike.

2. **The Champion vs. Buyer Test**: A champion saying "we'd love more seats" is an early signal. An economic buyer asking "what would 50 more seats cost?" is pipeline-ready. Never conflate the two.

3. **The Frustration-to-Expansion Trap**: Feature requests born from frustration ("why can't your product do X?") are support issues first, expansion signals second. Address the frustration before positioning the upsell.

4. **The 90-Day Trend Rule**: Any single data point (usage spike, seat overage, feature request) is anecdotal. Three consecutive months of directional signal is a pattern worth qualifying.

5. **The Renewal Proximity Gate**: Expansion signals within 90 days of renewal should be packaged with the renewal conversation, not pursued independently — unless the expansion is urgent and the renewal is healthy.

6. **The Silent Department Rule**: If only one department is using the product in a multi-department account, the silent departments are either unaware or uninterested. Discovery is required before assuming cross-sell opportunity.

7. **The AE Handoff Timing Rule**: Route to AE at pipeline-ready, not at early signal. Premature AE involvement on an unqualified signal wastes AE time and can pressure the customer relationship.

---

## Common Failure Modes by Signal Type

### Seat/Usage Capacity Failures
- **Seasonal spike misread**: Treating a Q4 usage surge as sustained growth.
  --> Fix: Require 90-day trend confirmation before qualifying as pipeline-ready.
- **Shared credential blindness**: Missing that 10 users share 3 logins — actual demand is higher than metrics show.
  --> Fix: Ask the qualifying question about shared credentials explicitly.

### Feature/Tier Upsell Failures
- **Curiosity-as-intent**: Treating a "that looks cool" comment as a buying signal.
  --> Fix: Apply the Champion vs. Buyer Test — who said it, and did they reference budget or timeline?
- **Support ticket misclassification**: Counting frustrated feature requests as upsell signals without resolving the underlying issue.
  --> Fix: Check support ticket sentiment; address frustration before positioning expansion.

### Cross-Sell Failures
- **Solution-in-search-of-problem**: Pitching an adjacent product the customer hasn't expressed a need for.
  --> Fix: Require an observed pain point (call notes, QBR discussion, support ticket) before flagging cross-sell.
- **Competitor displacement assumption**: Assuming the customer wants to replace their existing tool when they may be satisfied with it.
  --> Fix: Ask whether the current solution is a pain point or working fine before positioning replacement.

### Geographic/Organizational Expansion Failures
- **M&A assumption**: Assuming an acquired company will adopt the parent's tech stack.
  --> Fix: Verify with the champion whether the acquisition includes technology consolidation plans.

### At-Risk Account Failures
- **Expansion on a burning platform**: Pursuing growth signals while ignoring active churn risk.
  --> Fix: Run risk assessment first; expansion conversations on Red accounts require explicit renewal stabilization.

---

## Expert Judgment Patterns

### Qualification Decisions
- Early signal stays early until an economic buyer has been engaged — champion enthusiasm alone never upgrades the tier.
- When multiple signals exist in one account, qualify the highest-ARR-potential signal first; don't spread effort across all simultaneously.
- If the qualifying question has been asked and the answer is vague or deflecting, the signal is weaker than it appears — do not upgrade tier.

### Sequencing Decisions
- Always check renewal risk before expansion signals — a Red account's expansion signals are deferred until stabilized.
- Pull CRM expansion history before qualifying new signals — if a prior expansion attempt stalled, understand why before re-engaging.
- Surface signals to the CSM before routing to AE — the CSM validates context; the AE validates commercial viability.

### Confidence Decisions
- ARR potential estimates on early signals are always [Low Confidence] — state this explicitly; never let an estimate read as committed pipeline.
- Signals corroborated by 2+ data sources (CRM + CS Platform + call notes) can be [Moderate]; single-source signals stay [Low Confidence].
- Qualification tier assignment is a judgment call — when uncertain, default to the lower tier and note what evidence would upgrade it.

---

*Reasoning Blueprint: Expansion Signal Identification v1.0*
*For use with expansion-signal when Tier 3 reasoning is activated*
