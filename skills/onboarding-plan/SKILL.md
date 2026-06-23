---
name: onboarding-plan
description: >
  Generate, update, or summarize the customer-facing onboarding plan document.
  The plan is the primary shared artifact between the CSM and the customer team
  — it defines the milestone timeline, ownership at each stage, first priorities,
  communication cadence, and success criteria placeholder. Reads onboarding model,
  milestone framework, duration targets, and plan format from your onboarding profile.
  Pulls contract start date, segment, and stakeholders from CRM if available. Use
  --draft (default) to generate a complete plan after kickoff, --update to revise
  the plan after a milestone completes or scope changes, or --summary to produce
  an abbreviated current-status view for async stakeholder updates.
argument-hint: "[<account-name-or-ID>] [--draft | --update | --summary]"
version: "1.0.0"
deployment_target: plugin
---

<!-- Status: [PROPOSED] -->

# /onboarding:onboarding-plan

Onboarding plan document — generate, update, or summarize.

---

## Pre-flight

Read both configuration files before building any plan:
1. `~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

Fields read from onboarding config:
- Onboarding model (white-glove / guided-self-serve / implementation-plus-handoff /
  partner-led — shapes ownership columns and section structure)
- Milestone framework (M1–M5 day targets, completion criteria, at-risk signals)
- Duration targets by segment (Enterprise / Mid-Market / SMB — anchors the plan timeline)
- Customer-facing plan format (Google Doc / Notion / shared tracker / PDF — sets the
  header note for where the plan lives)
- CS methodology (TARO / SuccessCOACHING / Custom — affects play references in footnotes)
- Graduation criteria (what signals readiness for the post-onboarding handoff)
- TtV targets by segment (internal reference; always labeled as planning targets, never
  as customer commitments)

Fields read from company profile:
- Company brand name (appears in plan header)
- Default communication cadence (weekly check-in / biweekly / async — populates cadence
  section)
- Success criteria review timing (when to formally review success criteria with the customer)

If either config file is missing or milestone framework fields contain `[PLACEHOLDER]`:
> "Milestone targets and onboarding model aren't configured. Run
> `/onboarding:cold-start-interview --section milestones` to set these before
> generating an onboarding plan — the output will use generic timelines without your
> actual targets."

Proceed with a general structure if the user confirms they want to continue despite
missing config.

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Trigger Precision

**Use when:**
- Generating a new onboarding plan for a customer account (`--draft`)
- Revising an existing onboarding plan after scope, timeline, or milestone changes (`--update`)
- Producing a customer-facing summary of the onboarding plan for sharing or review (`--summary`)

**Do NOT use for:**
- Milestone status tracking against an existing plan (use `/onboarding:milestone-tracker`)
- Success criteria definition — criteria must be defined before or during plan generation, not after
- Handoff document generation (use `/onboarding:handoff-doc`)

## Typical Activation
- "Draft the onboarding plan for [Account]"
- "The timeline changed — update the onboarding plan for [Account]"
- "Give me a summary of the [Account] onboarding plan to share with the customer"
- CSM runs `/onboarding:onboarding-plan [account] --draft` to generate a new post-kickoff plan
- CSM runs `/onboarding:onboarding-plan [account] --update` after a milestone completion or scope change
- CSM runs `/onboarding:onboarding-plan [account] --summary` to produce an async stakeholder update

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of onboarding plan request is this?
   - **New Plan Draft**: Post-kickoff, first plan generation. CSM has contract start date, stakeholders, and initial priorities. Optimize for completeness and model-correct structure.
   - **Plan Update**: Existing plan needs revision — milestone completed, date shifted, scope changed, or stakeholder changed. Preserve change log; update only affected sections.
   - **Status Summary**: Abbreviated current-state view for async communication (Slack, email, stakeholder update). Quiet mode — zero internal labels, no plan modifications.
   - **Incomplete Config / Recovery**: Config files missing or contain placeholders. Surface every gap explicitly; do not silently generate with defaults.

2. **CONSTRAINTS**: What limits the solution space?
   - G1 (dates anchor to contract start): All milestone dates derive from contract start date + config day targets. If contract start is unavailable, placeholder every date — never estimate.
   - G2 (TtV is internal): TtV targets appear only in Section 7 with `[review — internal planning target]` label. Zero TtV references in Sections 1-6 or `--summary` output.
   - G4 (model adaptation is structural): The onboarding model changes section structure, ownership columns, and prose tone materially. If model is `[PLACEHOLDER]`, default to white-glove and flag — never produce a generic plan silently.
   - G5 (confidentiality): Customer-facing export contains no internal labels, TtV references, at-risk signals, reviewer notes, or escalation paths. Audit before delivery.
   - G7 (success criteria is a placeholder until confirmed): Section 6 is always a placeholder on first `--draft` unless success-criteria skill has already run. Never populate from assumptions or sales notes.

3. **EXPERT CHECK**: What would a veteran onboarding CSM verify first?
   - Is the onboarding model configured and applied, or did the plan silently use a default structure? A white-glove plan shared with a guided-self-serve account damages the relationship framing from day one.
   - Are all milestone dates calculated from contract start date, not from today's date or kickoff date? One wrong anchor cascades every date in the plan.
   - For `--update` requests: is the change log preserved and are downstream milestone dates recalculated if a date shift cascades?

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - ❌ Calculating milestone dates from today's date or kickoff date instead of contract start date — creates scheduling drift from the anchor.
   - ❌ Producing a plan without applying the configured model adaptation — a partner-led plan missing the three-party header and communication structure looks like a template, not a plan.
   - ❌ Regenerating the full plan on an `--update` request instead of updating affected sections and appending to the change log — destroys milestone history.
   - ❌ Including TtV references, at-risk signals, or escalation paths in `--summary` or customer-facing output — leaks internal planning assumptions.
   - ❌ Populating Section 6 (success criteria) from sales notes or kickoff conversation when the success-criteria skill has not been run — these require explicit customer agreement.
   - ❌ Silently generating with default milestone day targets when config contains `[PLACEHOLDER]` values — surface the gap and offer the cold-start-interview path.

**After execution**, verify:
- Does the plan match the correct onboarding model with all model-specific adaptations applied?
- Are all milestone dates anchored to contract start date and internally consistent?
- Is the output mode (draft/update/summary) matched to the actual request, with internal content suppressed in customer-facing output?
- Confidence: [High] if config is complete + CRM data verified / [Medium] if config partial or CRM unavailable / [Low] if user-provided context only — state which.

## Mode

`--draft` (default): Generate a complete onboarding plan from kickoff inputs. Use
immediately after the kickoff call when the CSM has the contract start date, stakeholder
names, and first priorities. Produces the full plan document ready to share with the
customer after CSM review.

`--update`: Revise an existing plan after a milestone is completed, a scope change
occurs, or a key date shifts. Ask the CSM which milestone was completed or what changed.
Regenerate affected sections (milestone table, next priorities, cadence) while preserving
confirmed historical entries. Append a change log entry at the bottom of the plan.

`--summary`: Abbreviated current-state view — current milestone status, what's done,
what's next, and the next milestone target date. Formatted for pasting into a Slack
message, email, or async stakeholder update. Suppresses the full milestone table and
historical context. Quiet mode (no internal labels, no reviewer note).

---

## Account identification and data pull

Ask: "Which account is this plan for? I need the account name and contract start date
to calculate milestone dates."

If a CRM connector is available, pull:
- Account name, segment, and tier
- Contract start date (required for all date calculations)
- Assigned CSM and AE
- Account ARR (calibrates plan depth — strategic accounts get more detailed ownership)
- Known stakeholders: executive sponsor, champion, technical lead, billing contact
- Sales handoff notes (populates the "context coming into onboarding" section)

Confirm the pull:
> "[CRM]: [account name] · [segment] · contract start [date] · CSM: [name]
> · AE: [name] · data as of [timestamp]"

If no CRM connector is available:
> "No CRM connector configured. Provide the account name, segment, contract start date,
> and stakeholder names — I'll build the plan from what you give me."

---

## Milestone date calculation

All milestone dates are calculated from the contract start date using day targets from
the onboarding config.

Standard milestone framework (from config; these are defaults — config values override):

| Milestone | Label | Day Target | Completion Criteria |
|-----------|-------|------------|---------------------|
| M1 | Kickoff complete | Day 5 | Kickoff call held; plan shared; first priorities confirmed |
| M2 | Technical setup | Day 14 | Required integrations active; users provisioned |
| M3 | First use | Day 21 | Product used for at least one real workflow |
| M4 | First value | Day 30 | Measurable outcome against at least one success criterion |
| M5 | Handoff ready | Day 60 | All success criteria met or tracked; CSM graduation checklist complete |

Calculate each milestone date as: contract start date + milestone day target.

If a milestone date falls on a weekend, note it:
> "M2 falls on [day] — suggest confirming with the customer whether [adjusted date]
> works better."

**TtV note:** TtV targets from config are internal planning benchmarks. Every reference
to TtV in the output is labeled `[review — internal planning target]` and appears only
in the internal version of the plan. The customer-facing plan shows milestone dates
and completion criteria — not TtV labels.

---

## Plan builder

### Section 1 — Header (customer-facing)

```
[Company Brand Name] × [Account Name]
Onboarding Plan

Contract start:     [date]
Plan owner:         [CSM name]
Last updated:       [today's date]
Plan lives in:      [customer-facing plan format from config]
```

### Section 2 — Your onboarding timeline

Milestone table — customer-facing format:

| Milestone | Target date | What it means | Status |
|-----------|-------------|---------------|--------|
| M1: Kickoff complete | [date] | Kickoff call held; onboarding plan shared | Scheduled |
| M2: Technical setup | [date] | [completion criteria from config] | Upcoming |
| M3: First use | [date] | [completion criteria from config] | Upcoming |
| M4: First value | [date] | [completion criteria from config] | Upcoming |
| M5: Handoff ready | [date] | [completion criteria from config] | Upcoming |

Status values: Upcoming / In progress / Complete / At risk — updated on `--update` calls.

### Section 3 — What happens at each stage

Brief prose description of each milestone phase — what the CSM does, what the customer
team does, and what signals completion.

Keep this section brief (2–3 sentences per milestone). The goal is a shared mental model,
not a process document. For white-glove and implementation-plus-handoff models, this
section is slightly longer — see model adaptations below.

### Section 4 — First priorities

"Here's what we need to accomplish before [M2 date]:"

Populate from kickoff notes or ask: "What are the 2–3 things that must happen before
the next milestone? Who owns each?"

Present as a named list with owner and due date:
- [Priority 1] — Owner: [name] · Due: [date]
- [Priority 2] — Owner: [name] · Due: [date]
- [Priority 3 if applicable] — Owner: [name] · Due: [date]

### Section 5 — How we'll work together

Communication cadence from config:
> "We'll connect [weekly / biweekly / async] via [format]. You can always reach
> [CSM name] at [contact] between sessions."

Add preferred communication channel (Slack / email / Teams) if known from CRM notes
or kickoff.

### Section 6 — Success criteria

This section is a placeholder on the first `--draft` output:

> **Success criteria** will be defined together during our first working session.
> We'll document what "successful onboarding" looks like for [account name] —
> typically 3–5 measurable outcomes you want to achieve by [M5 date].

If the `/onboarding:success-criteria` skill has already been run for this account, replace the
placeholder with the confirmed criteria list. Ask: "Have you already run the
`/onboarding:success-criteria` skill for this account? If so, paste or describe the agreed criteria
and I'll populate this section."

### Section 7 — Internal section (suppressed in customer-facing output)

Visible only in `--draft` internal version:

**TtV context [review — internal planning target]:**
- Segment TtV target: [duration from config for this segment]
- Current projection: [M5 date — contract start date] → [X days]
- Gap/surplus vs. target: [±X days]

**At-risk signals to watch (from config):**
- M1: [at-risk signals from config]
- M2: [at-risk signals from config]
- M3: [at-risk signals from config]

**Escalation path:** [escalation contact from config]

---

## Model adaptations

**white-glove:**
- Section 3 is expanded — each milestone phase includes explicit CSM-owned actions
  and customer-owned actions as separate bullet lists
- Add an "Executive relationship" note under Section 5: who is the exec sponsor,
  how often they receive updates, and in what format
- Section 2 milestone table includes an "Owner" column naming the CSM and the
  customer champion for each milestone

**guided-self-serve:**
- Section 3 is compressed — focus on customer-owned actions; CSM is "available to
  support" rather than leading
- Add a "Resources available to you" subsection under Section 5: documentation link,
  training portal, support channel
- Section 4 First priorities emphasizes what the customer's team needs to complete
  independently before the next CSM touchpoint

**implementation-plus-handoff:**
- Add a "Phase structure" note at the top of Section 2: Implementation phase (M1–M3,
  implementation engineer lead) and Adoption phase (M3–M5, CSM lead)
- Name the implementation engineer in the plan header alongside the CSM
- Section 3 distinguishes between "Implementation phase" milestones and "Adoption
  phase" milestones with separate prose blocks
- Section 7 internal section notes the handoff milestone date and pre-handoff checklist
  items

**partner-led:**
- Plan header includes the partner name: "[Company] × [Partner] × [Account]"
- Section 5 communication cadence includes the three-party structure: who the customer
  reaches for which type of issue (partner for day-to-day; CSM for escalation;
  company support for technical)
- Section 3 milestone descriptions name the partner's role at each stage
- Internal Section 7 notes the partner contact, their scope of delivery, and the
  escalation trigger that routes to the CSM directly

---

## `--update` mode

Ask: "What changed? Options: (a) milestone completed, (b) date shift, (c) scope change,
(d) stakeholder change."

For each change type:

**Milestone completed:**
- Update the Status column in the milestone table to "Complete" with the actual
  completion date
- Advance the First priorities section to reflect the next milestone's priorities
- Append a change log entry:
  `[date] — [CSM name]: M[X] marked complete. Actual date: [date]. Next: M[X+1] target [date].`

**Date shift:**
- Recalculate downstream milestone dates if the shift cascades
- Flag if the shift puts M5 past the TtV target [internal, labeled]
- Append change log: `[date] — [CSM name]: [milestone] rescheduled to [new date]. Reason: [brief]`

**Scope change:**
- Revise the affected sections (First priorities, Section 3 descriptions if needed)
- If the scope change affects graduation criteria, flag it for the `/onboarding:success-criteria`
  skill: "This change may affect your agreed success criteria — run
  `/onboarding:success-criteria --update` to confirm."
- Append change log: `[date] — [CSM name]: Scope change — [brief description].`

**Stakeholder change:**
- Update the plan header and the relevant milestone ownership entries
- Append change log: `[date] — [CSM name]: [Role] changed from [old name] to [new name].`

---

## Output format

### `--draft` output (CSM review version)

```
[Plan header — customer-facing content]

[Sections 1–6 — customer-facing content]

---

⚠️ Internal — do not share with customer

[Section 7 — TtV context, at-risk signals, escalation path]

[Reviewer note]
```

### Customer-facing export (--draft with quiet flag or after CSM review)

```
[Plan header]

[Sections 1–6 only]

No internal labels, no reviewer notes, no TtV references, no at-risk signals.
```

### `--update` output

```
[Updated plan — full document with revised sections]

[Change log — appended at bottom]

[Reviewer note — internal only]
```

### `--summary` output (quiet mode)

```
**[Account Name] — Onboarding Status**
*As of [date]*

**Current milestone:** [M# — label] — [Complete / In progress / At risk]
**Completed:** [list of complete milestones with dates]
**Next milestone:** [M# — label] by [date]
**Current priorities:**
  - [priority 1]
  - [priority 2]

Questions? [CSM name] · [contact]
```

---

## Reviewer note (internal — `--draft` and `--update` only)

> ⚠️ Reviewer note
> - **Sources:** [CRM ✓ verified | manual input]
> - **Data as of:** [timestamp]
> - **Config fields read:** onboarding model ([value]), milestone framework ([M1–M5
>   day targets]), duration target ([segment: X days]), plan format ([value])
> - **Milestone dates calculated from:** contract start [date] + config day targets
> - **TtV projection:** [X days vs. target Y days — on track / [±Z days]]
> - **Success criteria section:** [placeholder — run /onboarding:success-criteria |
>   populated from prior run]
> - **Flagged for your judgment:** [weekend milestone dates / missing stakeholders /
>   scope not yet confirmed | none]
> - **Before sharing:** Remove the internal section (Section 7) and this reviewer
>   note. Confirm all milestone dates are accurate. Replace the success criteria
>   placeholder if criteria have been established.

---

## Reference Files

- `references/reasoning-blueprint.md` — reasoning framework for this skill

---

## Security & Permissions

This skill operates read-only against configuration files and connected MCP data sources.
No filesystem writes, no subprocess execution, no dynamic code execution.
All data access is through explicitly connected MCP connectors; no outbound network calls are made directly.

## Trust & Verification

Customer-facing outputs (`--summary` mode) apply quiet mode — TtV targets, internal health assessments, and reviewer notes are suppressed.
All CRM and PM data is timestamped and staleness-flagged per G7.
TtV figures in Section 7 (internal planning view) are always tagged `[review — internal planning target]` and never appear in `--summary` output.
CSM review is required before sharing any customer-facing plan summary.

## Guardrails

**Dates anchor to contract start — never estimate.** If the contract start date is
unavailable, leave all milestone dates as `[confirm date]`. A milestone date that
drifts from the actual contract start creates scheduling confusion from day one.

**TtV is internal.** The labels `[review — internal planning target]` and TtV
references appear only in the internal section of the plan and the reviewer note.
The customer-facing plan contains milestone dates and completion criteria — not
time-to-value framing, which is a planning metric, not a customer deliverable.

**The plan is a living document.** The `--draft` output is the baseline. Every
milestone completion, date shift, or scope change must go through `--update` to
keep the plan current. Do not regenerate the plan from scratch when an update is
needed — use `--update` to preserve the change log and milestone history.

**Success criteria is a placeholder until confirmed.** Section 6 always displays
a placeholder on the first `--draft` run unless the `/onboarding:success-criteria` skill has
already been completed for this account. Do not populate success criteria from
assumptions or sales notes — they require explicit agreement with the customer.

**Model adaptation changes the ownership structure materially.** The plan for a
partner-led account with a three-party ownership model looks substantially different
from a white-glove plan. If the model is `[PLACEHOLDER]`, default to white-glove
and flag it — do not silently produce a generic plan.

**Quiet mode for customer-facing output.** The customer-facing export contains no
internal labels, TtV references, at-risk signals, reviewer notes, or escalation
paths. The customer receives a clean, professional document that reflects shared
commitments — not internal planning assumptions.

**`--summary` is for async communication — not plan management.** The summary
output is formatted for Slack, email, or stakeholder updates. It does not replace
the full plan and should not be treated as a plan revision. Direct any plan changes
to `--update`.
