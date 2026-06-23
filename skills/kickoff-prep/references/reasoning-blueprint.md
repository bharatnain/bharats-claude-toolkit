---
title: "Reasoning Blueprint: Kickoff Preparation"
type: reasoning-blueprint
skill: kickoff-prep
version: 1.0.0
---

# Reasoning Blueprint: Kickoff Preparation

Load this blueprint when Tier 3 reasoning is activated for onboarding kickoff
preparation. It provides the domain-specific taxonomy, heuristics, and expert
judgment patterns that shape expert-level kickoff agenda and checklist generation.

---

## Problem Classification Taxonomy

### Type A: Standard Kickoff (Known Config, Known Account)
**Characteristics**: Config is populated (format, model, attendees), CRM returns account data. Straightforward generation with model adaptation.
**Primary Risk**: Producing a generic agenda that ignores the onboarding model adaptation — white-glove and guided-self-serve require materially different agendas.
**Expert Focus**: Whether the model adaptation actually changed the agenda structure, not just swapped a label.

### Type B: Incomplete Config Kickoff
**Characteristics**: Config has `[PLACEHOLDER]` markers or missing kickoff fields. User chose to proceed anyway.
**Primary Risk**: Generating output that looks complete but is built on defaults the CSM doesn't realize are defaults — silent genericity.
**Expert Focus**: Every default assumption is surfaced visibly, not buried in a reviewer note the CSM skips.

### Type C: Missing Account Data Kickoff
**Characteristics**: No CRM connector or CRM returns sparse data. Manual input required for account context.
**Primary Risk**: Producing an agenda with blank fields or placeholder names that the CSM sends without filling — erodes customer trust at first contact.
**Expert Focus**: Distinguish between "leave blank for CSM to fill" vs. "ask CSM now before generating" — stakeholder names and M1 date fall in the latter category.

### Type D: Partner-Led or Multi-Party Kickoff
**Characteristics**: Onboarding model is partner-led or involves implementation handoff with a named third party.
**Primary Risk**: Producing a two-party agenda for a three-party engagement — confuses relationship structure from day one.
**Expert Focus**: Whether the partner's role, escalation path, and three-way relationship are explicit, not assumed.

---

## Domain Heuristics

1. **The First-Impression Rule**: The kickoff agenda is the first artifact the customer receives from their CSM. Errors here — wrong names, wrong dates, generic content — set a tone that takes weeks to repair. Verify names and dates before generating.

2. **The Model-Shapes-Structure Rule**: Onboarding model is not a metadata tag — it changes which agenda sections exist, their relative weight, and what language is used. If the model adaptation didn't change at least 2 structural elements, it wasn't actually applied.

3. **The 48-Hour Attendee Rule**: Any required attendee unconfirmed within 48 hours of kickoff must be flagged as a blocker, not a note. Unattended kickoffs frequently delay M1 by 2+ weeks.

4. **The M1 Anchor Rule**: Every kickoff agenda must reference a concrete M1 target date calculated from contract start + config milestone days. If contract start date is unavailable, leave the date as `[confirm date]` — never estimate. A wrong milestone date in a customer document is worse than a blank.

5. **The Quiet-Mode Rule**: Customer-facing output (`--agenda`) must contain zero internal artifacts — no confidence tags, no reviewer notes, no checklist items, no staleness flags. If any internal content leaks into quiet mode, the output fails.

6. **The Pre-Call Prep Rule**: Post-kickoff follow-up materials (email draft, plan link, success criteria doc) must be prepared before the call, not after. Same-day follow-up signals operational maturity; next-day follow-up signals scrambling.

---

## Common Failure Modes by Classification Type

### Standard Kickoff Failures
- **Model label without adaptation**: Agenda says "white-glove" in metadata but structure is identical to guided-self-serve.
  -> Fix: Verify at least 2 structural differences exist between the generated agenda and the default template.
- **M1 date miscalculation**: Contract start date parsed incorrectly or milestone day offset applied wrong.
  -> Fix: Show the calculation explicitly in the reviewer note: `[contract start] + [M1 days] = [M1 date]`.

### Incomplete Config Failures
- **Silent default substitution**: Missing config values replaced with reasonable defaults without flagging them.
  -> Fix: Every default must appear with a `[default — not configured]` marker visible to the CSM.
- **Skipped pre-flight warning**: User said "continue anyway" but the output doesn't remind them what's missing.
  -> Fix: Include a summary of missing config fields at the top of the reviewer note.

### Missing Account Data Failures
- **Placeholder leakage**: `[account name]` or `[CSM name]` appears in customer-facing output.
  -> Fix: Scan the `--agenda` output for any bracket-enclosed placeholders before presenting.
- **Incomplete stakeholder list presented as complete**: Three contacts pulled from CRM presented without noting that executive sponsor is unknown.
  -> Fix: Explicitly state which required roles are identified vs. missing.

### Partner-Led Failures
- **Two-party framing**: Agenda describes "us and you" when three parties are involved.
  -> Fix: Check for partner name in at least 2 agenda sections; verify escalation path names all three parties.
- **Missing partner escalation path**: Customer has no documented way to reach the company directly if the partner is unresponsive.
  -> Fix: Include a direct escalation contact in the agenda and verify it's populated.

---

## Expert Judgment Patterns

### Scope Decisions
- If the CSM asks for "just the agenda," deliver `--agenda` mode — don't upsell `--prep` unless the kickoff is <48 hours away and no checklist exists.
- If config is heavily incomplete (3+ placeholder fields), recommend running cold-start-interview first rather than generating a low-quality artifact.

### Depth Decisions
- Strategic accounts (high ARR, enterprise segment) get expanded "Partnership vision" regardless of model — the executive relationship framing matters more than the time saved by compressing it.
- Async/Loom kickoffs require tighter written structure because there's no live Q&A to recover from ambiguity.

### Sequencing Decisions
- Always resolve attendee confirmation status before generating the agenda — an agenda addressed to "your team" instead of named people signals the CSM hasn't done their homework.
- Pull CRM data before asking the CSM for manual input — avoid asking for information that's already available.

### Confidence Decisions
- [High] when config is complete + CRM data is fresh (<7 days) + all required attendees confirmed.
- [Medium] when config is complete but CRM data is stale or partially missing.
- [Low] when config has placeholders or account data is entirely manual — state which gaps drive the lower confidence.

---

*Reasoning Blueprint: Kickoff Preparation v1.0*
*For use with kickoff-prep when Tier 3 reasoning is activated*
