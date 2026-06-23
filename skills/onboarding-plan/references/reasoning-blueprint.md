---
title: "Reasoning Blueprint: Onboarding Plan"
type: reasoning-blueprint
skill: onboarding-plan
version: 1.0.0
---

# Reasoning Blueprint: Onboarding Plan

Load this blueprint when Tier 3 reasoning is activated for onboarding plan work.
It provides the domain-specific taxonomy, heuristics, and expert judgment
patterns that shape expert-level onboarding plan generation, revision, and summarization.

---

## Problem Classification Taxonomy

### Type A: New Plan Draft (Post-Kickoff)
**Characteristics**: First plan generation after kickoff call. CSM has contract start date, stakeholder names, and initial priorities. No prior plan artifact exists.
**Primary Risk**: Generating a plan with unconfigured milestone targets or missing model adaptation — produces a generic document that undermines credibility at first share.
**Expert Focus**: Verify onboarding model and milestone framework are configured before building; a white-glove plan structure shared with a guided-self-serve account damages the relationship framing.

### Type B: Plan Update (Milestone or Scope Change)
**Characteristics**: Existing plan requires revision — milestone completed, date shifted, scope changed, or stakeholder changed. Change log history must be preserved.
**Primary Risk**: Regenerating sections that should be preserved, losing change log continuity, or failing to cascade date shifts to downstream milestones.
**Expert Focus**: Identify which change type triggers which section updates; a scope change that affects graduation criteria requires a cross-skill flag to success-criteria.

### Type C: Status Summary (Async Communication)
**Characteristics**: Abbreviated current-state view for Slack, email, or stakeholder update. No plan modifications. Quiet mode — no internal labels.
**Primary Risk**: Including internal-only content (TtV targets, at-risk signals, escalation paths) in output destined for customer or external stakeholders.
**Expert Focus**: Verify the summary contains zero internal labels before delivery; a single leaked TtV reference reframes the relationship as vendor-metric-driven.

### Type D: Incomplete Config / Recovery
**Characteristics**: Config files missing, contain placeholders, or contract start date unavailable. Plan cannot be fully calculated.
**Primary Risk**: Silently generating a plan with invented dates or default assumptions the CSM treats as real.
**Expert Focus**: Surface every gap explicitly and offer the cold-start-interview path; a plan with fabricated dates is worse than no plan.

---

## Domain Heuristics

1. **The Contract Anchor Rule**: Every date in the plan traces to contract start + config day target. If the contract start date is missing, no dates are calculated — use `[confirm date]` placeholders. Fabricated dates create downstream scheduling failures.

2. **The Model Shapes Everything Rule**: The onboarding model (white-glove, guided-self-serve, implementation-plus-handoff, partner-led) changes section structure, ownership columns, and prose tone. If model is placeholder, default to white-glove and flag it — never produce a model-agnostic plan silently.

3. **The TtV Firewall Rule**: TtV targets are internal planning benchmarks. Every TtV reference carries `[review — internal planning target]` and appears only in Section 7. If you find TtV language in Sections 1-6, it is a defect.

4. **The Living Document Rule**: Plans are updated, never regenerated. `--update` preserves the change log and milestone history. If a CSM asks to "redo the plan," clarify whether they mean `--update` (preserve history) or a genuine fresh `--draft` (rare — usually means the original was never shared).

5. **The Success Criteria Placeholder Rule**: Section 6 is always a placeholder on first draft unless success-criteria skill has already run. Never populate success criteria from assumptions, sales notes, or kickoff conversations — they require explicit customer agreement.

6. **The Weekend Milestone Rule**: When a calculated milestone date falls on a weekend, flag it with a suggested adjusted date. Do not silently shift the date — the CSM decides.

---

## Common Failure Modes by Classification Type

### New Plan Draft Failures
- **Generic plan despite configured model**: Produced a plan without applying model adaptations (e.g., missing partner name in partner-led header, missing implementation engineer in impl-plus-handoff).
  → Fix: Check onboarding model value before building any section; apply the matching model adaptation block completely.
- **Dates calculated from wrong anchor**: Used today's date or kickoff date instead of contract start date for milestone calculation.
  → Fix: Confirm contract start date explicitly before any date math. If unavailable, placeholder all dates.

### Plan Update Failures
- **Change log dropped**: Regenerated the plan from scratch instead of updating affected sections and appending to the change log.
  → Fix: Always use `--update` logic — identify which sections are affected, update only those, append change log entry.
- **Downstream dates not cascaded**: Updated one milestone date but left downstream milestones unchanged, creating impossible timelines.
  → Fix: When a date shifts, recalculate all downstream milestone dates and flag if M5 exceeds TtV target (internal only).

### Status Summary Failures
- **Internal content leaked**: Summary included TtV references, at-risk signals, or reviewer notes — content meant for internal section only.
  → Fix: Summary mode suppresses Section 7, reviewer note, and all internal labels. Audit output for any `[review` tags before delivery.
- **Summary treated as plan revision**: CSM used summary output to communicate a scope change rather than running `--update`.
  → Fix: If summary content implies changes, prompt: "This looks like a plan change — run `--update` to revise the plan and preserve the change log."

### Incomplete Config Failures
- **Silent default assumptions**: Generated a plan using default milestone day targets without disclosing that config values were missing.
  → Fix: If any config field is placeholder, surface the warning and offer the cold-start-interview path before proceeding.

---

## Expert Judgment Patterns

### Scope Decisions
- When model is `[PLACEHOLDER]`, default to white-glove (most complete structure) and flag — never silently produce a stripped-down plan.
- When success criteria are available from a prior skill run, populate Section 6 fully; never leave the placeholder when data exists.

### Sequencing Decisions
- Pull CRM data before building any section — the account segment calibrates plan depth (strategic accounts get more detailed ownership columns).
- Calculate all milestone dates in one pass before writing prose — date inconsistencies between sections are the most common CSM complaint.

### Depth Decisions
- `--draft` always produces both the customer-facing plan (Sections 1-6) and the internal section (Section 7) in a single output — the CSM strips Section 7 before sharing.
- `--summary` is minimal by design — if the CSM asks for "more detail in the summary," redirect to `--draft` with a quiet flag rather than inflating the summary format.

### Confidentiality Decisions
- Any output containing TtV, at-risk signals, or escalation paths is internal-only. The customer-facing export is Sections 1-6 with zero internal metadata.
- Portfolio-level summaries (multiple accounts) require extra confidentiality review — account-specific ARR and health signals must not cross account boundaries.

---

*Reasoning Blueprint: Onboarding Plan v1.0*
*For use with onboarding-plan when Tier 3 reasoning is activated*
