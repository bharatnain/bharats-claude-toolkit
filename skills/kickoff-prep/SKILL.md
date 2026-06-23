---
name: kickoff-prep
description: >
  Prepare for an onboarding kickoff — generates a customized customer-facing
  agenda and an internal pre-kickoff checklist. Reads your kickoff format,
  required attendees, onboarding model, and milestone targets from your
  onboarding profile. Pulls account-specific context (segment, contract start
  date, AE/CSM owner, known stakeholders) from connected CRM if available.
  Produces two outputs: a shareable agenda draft calibrated to your onboarding
  model and segment, and an internal preparation checklist covering pre-call
  logistics, attendee confirmation, and materials readiness. Use --agenda for
  the customer-facing agenda only, --checklist for the internal prep checklist
  only, or the default --prep to generate both.
argument-hint: "[<account-name-or-ID>] [--prep | --agenda | --checklist]"
version: "1.0.0"
deployment_target: plugin
---

<!-- Status: [PROPOSED] -->

# /onboarding:kickoff-prep

Kickoff agenda and preparation checklist for a specific account.

---

## Pre-flight

Read both configuration files before building any kickoff materials:
1. `~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

Fields read from config:
- Kickoff format (60-min call / async / in-person — determines agenda structure)
- Required kickoff attendees (who must be confirmed before the call)
- Onboarding model (white-glove / guided-self-serve / implementation-plus-handoff / partner-led — shapes agenda content)
- Milestone framework (M1 date target populates the first milestone reference)
- Success criteria review cadence (determines when to introduce success criteria on the agenda)
- CS methodology (TARO / SuccessCOACHING / Custom — affects play references in checklist)
- Customer-facing plan format (used to set expectation in the agenda about plan delivery)

If either config file is missing or kickoff-related fields contain `[PLACEHOLDER]` markers:
> "Kickoff format and required attendees aren't configured. Run
> `/onboarding:cold-start-interview --section kickoff` to set these before
> generating kickoff materials — the output will be generic without your
> actual format and attendee requirements."

Proceed with a general structure if the user confirms they want to continue
despite missing config.

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Trigger Precision

**Use when:**
- Preparing for an upcoming kickoff call — generating the internal checklist and customer-facing agenda together (`--prep`)
- Generating only the customer-facing agenda for sharing directly (`--agenda`)
- Generating only the internal preparation checklist for the CSM (`--checklist`)

**Do NOT use for:**
- Post-kickoff milestone tracking (use `/onboarding:milestone-tracker`)
- Onboarding plan generation — the kickoff prep and onboarding plan are separate artifacts
- Blocker review or risk assessment — this skill is pre-onboarding preparation only

## Typical Activation
- "Prep me for my kickoff with [Account] on [date]"
- "Generate the kickoff agenda for [Account]"
- "Give me the internal checklist for the [Account] kickoff"
- CSM runs `/onboarding:kickoff-prep [account] --prep` to generate both agenda and checklist
- CSM runs `/onboarding:kickoff-prep [account] --agenda` for the customer-facing agenda only
- CSM runs `/onboarding:kickoff-prep [account] --checklist` for the internal prep checklist only

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of kickoff preparation request is this?
   - **Standard Kickoff**: Config is populated, CRM returns account data. Apply model adaptation and generate with full context.
   - **Incomplete Config Kickoff**: Config has `[PLACEHOLDER]` markers or missing fields. Surface every default visibly — silent genericity is the primary risk.
   - **Missing Account Data Kickoff**: No CRM connector or sparse CRM data. Distinguish "leave blank for CSM" from "ask CSM now" — names and M1 date require asking.
   - **Partner-Led / Multi-Party Kickoff**: Three-party engagement requiring explicit partner naming, role clarity, and escalation paths in the agenda.
   - **Mode-Specific Request**: User asked for `--agenda` or `--checklist` only. Deliver exactly the requested mode — do not upsell `--prep` unless kickoff is <48h away with no checklist.

2. **CONSTRAINTS**: What limits the solution space?
   - G2: Expansion or upsell signals from CRM must not appear in any customer-facing output (`--agenda` mode). Internal checklist only.
   - G4: If attendee confirmation flags trigger an escalation recommendation, route through configured escalation matrix with named owner — not generic "reach out to your manager."
   - G5: Confidentiality — `--agenda` output must contain zero internal artifacts: no confidence tags, no reviewer notes, no checklist items, no staleness flags. Scan before presenting.
   - G7: Flag stale CRM data with source date and staleness indicator. CRM >7 days = stale. Never silently use stale data for M1 date calculation or stakeholder names.
   - Model adaptation is structural, not cosmetic — if the onboarding model didn't change at least 2 agenda sections, it wasn't actually applied.

3. **EXPERT CHECK**: What would a veteran onboarding CSM verify first?
   - Did the model adaptation actually change the agenda structure, or just swap a label? Compare against the default 60-minute template.
   - Is the M1 target date calculated and shown, or is it a placeholder? If contract start date is missing, the date must read `[confirm date]` — never estimate.
   - Are required attendees confirmed or flagged? Any unconfirmed attendee within 48 hours of kickoff is a blocker, not a note.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Producing an agenda that says "white-glove" but uses the same structure as guided-self-serve — model adaptation must be structural.
   - Generating a two-party agenda ("us and you") for a partner-led three-party engagement — confuses the relationship from day one.
   - Letting `[account name]` or `[CSM name]` placeholders leak into `--agenda` customer-facing output.
   - Substituting missing config values with reasonable defaults without flagging them — the CSM must know what's configured vs. defaulted.
   - Calculating M1 date from an unverified or stale contract start date — a wrong milestone in a customer document erodes trust at first contact.
   - Presenting a contact list from CRM as a complete stakeholder map without noting which required roles (exec sponsor, champion, technical lead) are missing.

**After execution**, verify:
- Does the output match the requested mode (`--prep` / `--agenda` / `--checklist`)?
- Is `--agenda` output clean of all internal content (reviewer notes, confidence tags, checklist items)?
- Is the M1 date calculated and shown (or explicitly marked `[confirm date]` if contract start is unavailable)?
- Are all required attendees from config accounted for — confirmed or flagged?
- Confidence: [High] if config complete + CRM fresh + attendees confirmed / [Medium] if config complete but CRM stale or partial / [Low] if config has placeholders or data is entirely manual — state which gaps drive the rating.

## Mode

`--prep` (default): Generate both the customer-facing agenda draft and the
internal preparation checklist. Use when preparing for an upcoming kickoff
and need both the shareable artifact and the internal readiness view.

`--agenda`: Customer-facing agenda only — formatted for sharing with the
customer contact or including in the kickoff invite. Suppresses all internal
context, checklist items, and reviewer notes from the output.

`--checklist`: Internal pre-kickoff checklist only — covers logistics,
attendee confirmation, materials readiness, and first milestone setup.
Use when the agenda is already drafted and you need the internal prep view.

---

## Account identification and data pull

Ask: "Which account is this kickoff for? Provide the account name and the
scheduled kickoff date."

If a CRM connector is available, pull:
- Account name, segment, and assigned CSM/AE
- Contract start date and contract length
- Account ARR and product tier (calibrates agenda depth for strategic accounts)
- Known stakeholders (executive sponsor, champion, technical lead)
- Any notes from the sales handoff

Confirm the pull:
> "[CRM]: [account name] · [segment] · kickoff [date] · contract start [date]
> · CSM: [name] · AE: [name] · data as of [timestamp]"

If no connector is available:
> "No CRM connector configured. Tell me the account name, segment, scheduled
> kickoff date, and any stakeholders you know of — I'll build the materials
> from what you provide."

---

## Agenda builder

Construct the agenda based on:
- **Kickoff format** from config (determines time structure and sections)
- **Onboarding model** (shapes what goes on the agenda — see model adaptations below)
- **Account segment** (strategic accounts get executive relationship framing)
- **Contract start date** (anchors the M1 milestone reference)

### Standard agenda structure — 60-minute call format

Adapt section timing based on total call length if different from 60 minutes.

| Time | Section | Purpose |
|------|---------|---------|
| 0–5 min | Introductions | Names, roles, relationship map — CSM, AE (if attending), customer team |
| 5–15 min | Partnership vision | Why this partnership, what success looks like from both sides |
| 15–25 min | Onboarding plan overview | Timeline, milestones, what happens when |
| 25–40 min | First priorities | The 2–3 things that must happen before the next milestone |
| 40–50 min | Questions and alignment | Customer's open questions; confirm shared understanding |
| 50–60 min | Next steps and close | Named actions, owners, and dates; confirm communication cadence |

Populate the agenda draft with:
- Account name and kickoff date in the header
- M1 target date (calculated from contract start date + M1 day target from config)
- Required attendees from config (presented as "we'll need from your team...")
- Customer-facing plan format note (e.g., "We'll share your onboarding plan in
  [Google Doc / Notion / shared tracker] after this call")

### Model adaptations

**white-glove:** Expand "Partnership vision" section; include an executive
sponsor introduction segment if the exec is attending. Add a dedicated
slide/section for "Our team's commitment to you" framing.

**guided-self-serve:** Compress the "Partnership vision" section; expand
"First priorities" to emphasize what the customer's team will own. Add a
"Resources available to you" section (documentation, training portal,
support channels).

**implementation-plus-handoff:** Add an "Implementation phase overview"
section between milestones and first priorities. Name the implementation
engineer (if applicable) and distinguish their role from the CSM's role.
Include the handoff milestone explicitly in the timeline overview.

**partner-led:** Add a "How we'll work together with [partner name]" section.
Clarify the three-way relationship (customer / partner / company). Describe
the escalation path if the customer needs to reach the company directly.

### Async / Loom format

If kickoff format is async (Loom + written agenda):

Structure the written document as:
1. Welcome and context (1 paragraph)
2. Your onboarding timeline (milestone table with dates)
3. What we need from you in the next [M1 days] (named list)
4. How we'll communicate (cadence and format)
5. Your next step (single action with date)

The Loom companion covers introductions and vision; the written document
handles the structured reference content.

---

## Pre-kickoff checklist

The internal checklist covers five categories.

### 1. Attendee confirmation

For each required attendee from config:
- [ ] [Role] confirmed attending — name: [name] / not yet confirmed
- [ ] Executive sponsor confirmed (if white-glove model)
- [ ] AE attending or sent intro message to customer team
- [ ] Technical lead identified (if implementation-plus-handoff)
- [ ] Partner contact introduced (if partner-led)

Flag if any required attendee is unconfirmed within 48 hours of kickoff:
> "⚠️ [Role] not yet confirmed. Reach out via [email / Slack] before the call
> — an unattended kickoff without [executive sponsor / technical lead] often
> delays M1."

### 2. Materials readiness

- [ ] Kickoff agenda sent to customer at least [24h] before call
- [ ] Onboarding plan document drafted (or template ready to complete during/after call)
- [ ] Success criteria template accessible
- [ ] Integration requirements documented (if implementation-plus-handoff)
- [ ] Partner introduction sent (if partner-led)
- [ ] Recording consent noted (if call will be recorded)

### 3. Account context review

- [ ] Sales handoff notes reviewed
- [ ] Contract terms reviewed — auto-renewal date, key contractual milestones
- [ ] Any open support tickets from trial or pre-sales reviewed
- [ ] ARR and tier confirmed (to calibrate effort level)
- [ ] Known stakeholders mapped: executive sponsor / champion / technical lead / billing contact

### 4. First milestone setup

- [ ] M1 target date confirmed: [contract start + M1 day target from config]
- [ ] M1 completion criteria clear (per config: [M1 at-risk signals noted])
- [ ] First follow-up meeting scheduled (or to be scheduled on the kickoff call)
- [ ] PM task/project created for this account (if PM connector configured)

### 5. Post-kickoff actions (prepare before the call)

- [ ] Draft follow-up email ready (to send same day with next steps)
- [ ] Onboarding plan document link ready to share
- [ ] Success criteria doc or template ready to share
- [ ] Introductions to support/implementation team drafted if needed

---

## Output format

### `--prep` output

```
[Customer-facing agenda — formatted for sharing, no internal content]

---

[Internal header: ⚠️ Internal use only — do not share with customer]

[Pre-kickoff checklist — 5 categories]

[Reviewer note]
```

### `--agenda` output (quiet mode — customer-facing only)

---

**[Company Brand Name] × [Account Name] — Onboarding Kickoff**
*[Date] · [Time and timezone] · [Format: video call / in-person / async]*

**Attendees from [Company]:** [CSM name], [AE name if attending], [IE name if applicable]
**We'll need from your team:** [Required attendees from config]

---

**Agenda**

[Time sections from agenda builder, formatted as a clean list]

**First milestone target:** [M1 target date] — [M1 completion description]

**Your onboarding plan** will be shared in [format] following this call.

Questions before we meet? Reach [CSM name] at [contact].

---

### `--checklist` output

---

**Pre-Kickoff Checklist — [Account Name]**
*Kickoff: [date] · Prepared: [today]*

[5 checklist categories with current completion status]

---

## Reviewer note (internal — `--prep` and `--checklist` modes only)

> ⚠️ Reviewer note
> - **Sources:** [CRM ✓ verified | manual input]
> - **Data as of:** [timestamp]
> - **Config fields read:** kickoff format ([value]), required attendees ([value]),
>   model ([value])
> - **Flagged for your judgment:** [unconfirmed attendees / missing handoff notes /
>   M1 date not yet calculated — contract start date not found | none]
> - **Before sending agenda:** Remove this reviewer note block. Confirm [Company Brand
>   Name] appears correctly in the header. Confirm the M1 target date is accurate
>   before the customer sees it.

---

## Reference Files

- `references/reasoning-blueprint.md` — reasoning framework for this skill

---

## Security & Permissions

This skill operates read-only against configuration files and connected MCP data sources.
No filesystem writes, no subprocess execution, no dynamic code execution.
All data access is through explicitly connected MCP connectors; no outbound network calls are made directly.

## Trust & Verification

Customer-facing outputs (`--agenda` mode) apply quiet mode — internal labels, risk flags, and CSM preparation notes are suppressed.
All CRM data is timestamped and staleness-flagged per G7 (CRM >7 days).
Kickoff agendas shared with customers contain no internal TtV targets, health scores, or escalation context.
CSM review is required before sharing any customer-facing agenda output.

---

## Guardrails

**Agenda is a draft.** The generated agenda requires CSM review before sharing.
Account-specific context (stakeholder names, integration details, known priorities)
must be verified and added. Do not send the agenda without reviewing it.

**Required attendees drive the checklist.** If a required attendee from config is
unconfirmed, flag it explicitly — do not suppress the warning. A kickoff without
the required attendees often restarts the milestone clock.

**M1 date calculation requires contract start date.** If the contract start date
is unavailable from CRM or user input, leave M1 target date as `[confirm date]`
rather than estimating. A wrong M1 date in a customer-facing document erodes
trust at the start of the relationship.

**Model adaptation is not optional.** The agenda structure changes materially
between onboarding models. If the model is configured as `[PLACEHOLDER]`, default
to the white-glove structure and flag it — do not silently produce a generic agenda.

**Quiet mode for customer-facing output.** The `--agenda` output contains no
internal labels, confidence signals, reviewer notes, or checklist items. All
internal content is suppressed. The customer receives a clean, professional document.

**Partner-led requires partner visibility.** If the model is partner-led, the
agenda must name the partner and clarify the three-way relationship. Do not produce
a two-party agenda for a three-party engagement — it creates confusion at the call.

**Post-kickoff preparation is the last checklist category.** Preparing the
follow-up email and next-steps document before the call — not after — ensures
the CSM can send a same-day follow-up without delay. This is a discipline point,
not an optional step.
