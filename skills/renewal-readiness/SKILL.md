---
name: renewal-readiness
description: >
  Assess renewal readiness for an account — health, relationship, value delivery,
  stakeholder coverage, and commercial risk — and produce a renewal action plan.
  Use 90–180 days before renewal to identify and close gaps before the commercial
  conversation begins. Produces an internal readiness brief, a renewal timeline,
  and (optionally) a customer-facing renewal prep summary. Distinct from risk-flag:
  this skill assesses the full renewal picture including Green accounts, not only
  accounts in distress.
argument-hint: "[account name] [--brief | --timeline | --customer-summary]"
version: "1.0.0"
deployment_target: plugin
---

# /renewal-readiness

[PROPOSED]

## Use When
- Renewal is within 90 days and you need a structured readiness assessment
- Preparing for the renewal conversation and need to surface known objections and risks
- Executive sponsor engagement needs to be confirmed before the renewal window closes
- Value delivered needs to be documented before the commercial conversation begins

## Do NOT Use For
- Pricing, discount, or negotiation prep — that is AE/AM scope
- Accounts outside the 90-day renewal window — use /csm:health-score-review for general health
- Expansion positioning — use /csm:expansion-business-case
- Post-renewal success planning — use /csm:success-plan-builder

## Typical Activation
"/csm:renewal-readiness Acme Corp"
"Prep for [account]'s renewal"
"Renewal is in 60 days for [customer] — what do I need?"
"Run renewal readiness for [account]"

---

Know where you stand before the renewal conversation starts — health, relationship,
value story, and commercial risk, all in one place.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/csm:cold-start-interview`.

Critical configuration to apply:
- Renewal readiness timeline — when the company typically starts renewal motion
  (e.g., 90-day standard; 180-day for Enterprise)
- Renewal owner — CSM-owned or splits between CSM and AE/renewals team
- Commercial motion — what the CSM is authorized to discuss vs. what routes to AE
- Escalation matrix — what ARR level triggers executive-level renewal involvement
- Health model thresholds — Red/Yellow/Green classifications
- Primary value metric — anchor for renewal value conversation

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---


## Reasoning Protocol

> Load `references/reasoning-blueprint.md` for full taxonomy, heuristics, failure modes, and expert judgment patterns.

Before generating output, apply these primers:

1. **CLASSIFY** — Determine renewal type before generating output:
- **Type A** — Green account, routine renewal: health solid, stakeholders engaged, success criteria met
- **Type B** — Yellow account, gap closure needed: one or more dimensions require action within the renewal window
- **Type C** — Red account, intervention before renewal: stabilize first, then commercial motion
- **Type D** — High-ARR escalation renewal: ARR exceeds configured threshold, executive involvement required
- **Type E** — Non-standard contract: multi-year, auto-renewal, or month-to-month with different mechanics

2. **CONSTRAINTS** — Apply before generating:
- **G1** — Renewal readiness is distinct from risk; Green accounts still get a full brief
- **G2** — Expansion signals require economic buyer qualification; route to AE, never combine with renewal conversation
- **G4** — No commercial commitments in customer-facing summary; ARR, pricing, and contract terms stay internal
- **G5** — Single-threaded relationships are flagged in every brief regardless of health status
- **G7** — Executive sponsor decay: 60+ days since contact = decaying; 90+ days = re-engagement required

3. **EXPERT CHECK** — What a veteran CSM verifies first:
- Is there a value story, and is it strong enough to lead the renewal conversation?
- Is the executive sponsor genuinely engaged or just listed in the CRM?
- Has internal CSM + AE alignment happened, or is the renewal motion starting without it?
- Does the timeline allow enough runway to close identified gaps before the commercial window?
- If prior renewal was late or contentious, what structurally changed since then?

4. **ANTI-PATTERNS** — Common mistakes to avoid:
- Skipping the brief for Green accounts ("they'll renew anyway")
- Opening renewal conversation with contract or pricing before value is established
- Treating all Yellow gaps equally instead of triaging by renewal impact and time-to-close
- Initiating commercial motion on a Red account before stabilization
- Escalating to executives without a context-rich briefing tied to customer priorities
- Assuming auto-renewal means no readiness work is needed

**After execution**, verify:
- Does the output match the classified renewal type and selected mode?
- Scan for failure modes specific to this classification type (see blueprint)
- Are all `[review]` flags placed where human judgment is required?
- Is the action plan sequenced correctly — value before contract, stabilization before commercial motion, internal alignment before external?
- Confidence: [High] if CRM and CS Platform live with full component data / [Medium] if partially connected or some data from CSM context / [Low] if user-provided context only — state which.

## Mode

`--brief`: Full internal renewal readiness assessment. Default.

`--timeline`: Produce a renewal timeline only — key dates, milestones, and owner
assignments from now to renewal close. Lightweight; suitable for weekly tracking.

`--customer-summary`: Clean, customer-facing renewal prep communication — not a
commercial push; a forward-looking partnership summary with next-step ask.
Appropriate to send 60-90 days before renewal.

---

## Data gathering


**Connector error categorization:** When a connector call fails, distinguish the error type before proceeding:
- **Rate-limited (transient):** Connector returns HTTP 429 or equivalent throttle signal. Note the rate limit explicitly in output ("CRM data temporarily rate-limited — retry in 60 seconds recommended") and offer to retry rather than proceeding with degraded output.
- **Unavailable (permanent for this session):** Connector is not configured, authentication has expired, or service is down. Fall back to the manual-input path below and label all affected sections as "connector unavailable — manual input used."
Do not conflate these — a rate-limited connector will return data shortly; an unavailable connector will not.

Pull from connected integrations:
- CRM: ARR, renewal date, contract terms, prior renewal history, AE/AM contact
- CS Platform: current health score, component breakdown, lifecycle stage, CTAs
- Call recording: last 2-3 calls for relationship signals; any renewal discussion mentioned
- Document storage: current success plan, last QBR, any open commitments

If nothing is connected:
> "I need some basic account data to assess renewal readiness. Tell me: What's
> the renewal date and ARR? What's the current health status? Has there been
> any renewal conversation yet? I'll build the brief from what you share."

Minimum required before proceeding: renewal date, ARR, and at least one data
point on current health or recent customer engagement.

---

## Internal readiness brief (`--brief`)

---

**Renewal Readiness Brief — [Account Name]**
*[Date] · INTERNAL — not for distribution*
*Renewal: [date] — [N] days*

---

**Renewal snapshot**

| Field | Value |
|-------|-------|
| ARR | $[amount] |
| Renewal date | [date] — [N] days |
| Contract type | [Annual / Multi-year / Month-to-month] |
| Renewal owner | [CSM / AE / Renewals team — per configured commercial motion] |
| Segment | [SMB / Mid-market / Enterprise] |
| Health | [Red / Yellow / Green] |
| Prior renewal outcome | [On-time / Late / Expanded / Contracted / Churned — if CRM data available] |

---

**Readiness dimensions — summary**

Rate each dimension before the detail. Green = renewal-ready, Yellow = needs work,
Red = block to renewal.

| Dimension | Status | Top gap |
|-----------|--------|---------|
| Health & product usage | [🟢 / 🟡 / 🔴] | [1-line gap or "None"] |
| Value delivered vs. success criteria | [🟢 / 🟡 / 🔴] | |
| Stakeholder coverage & relationship | [🟢 / 🟡 / 🔴] | |
| Commercial readiness | [🟢 / 🟡 / 🔴] | |
| Internal alignment (CSM + AE) | [🟢 / 🟡 / 🔴] | |

**Overall renewal readiness:** [🟢 Renewal-ready / 🟡 Needs attention — [N] gaps /
🔴 At risk — intervention required]

---

### Dimension 1 — Health & product usage

Pull from configured health model.

| Component | Signal | Direction | Threshold status |
|-----------|--------|-----------|-----------------|
| [Component 1, e.g., usage] | [current value] | [↑↓→] | [Above / At / Below threshold] |
| [Component 2] | | | |
| [Component 3] | | | |

**Overall health:** [Red / Yellow / Green] per configured thresholds.

**Usage trend over 60–90 days:**
[Increasing / Stable / Declining] — [interpretation in 1-2 sentences]

**Churn signals present?** [Yes — [signals] / No / Unknown — data insufficient]

---

### Dimension 2 — Value delivered vs. success criteria

Pull from success plan if available.

| Success Criterion | Target | Actual | Status |
|-------------------|--------|--------|--------|
| [Criterion 1] | [target] | [actual] | ✅ / 🟡 / ⛔ |
| [Primary value metric] | [configured target] | [actual] | |

**Value story strength:** [Strong — all criteria met / Partial — [N] criteria met,
[N] gap(s) / Weak — criteria not established or most below target]

If no formal success criteria exist:
> "Success criteria have not been formally established for this account. Entering
> a renewal conversation without defined success criteria removes the CSM's
> strongest retention argument. Recommend establishing criteria with the customer
> before initiating renewal motion." `[review]`

**Primary value metric ([configured metric]):** [result vs. target]

---

### Dimension 3 — Stakeholder coverage & relationship

| Stakeholder | Role | Last contact | Engagement | Renewal risk |
|-------------|------|-------------|------------|-------------|
| [Executive sponsor] | [Role] | [date — N days] | [Active / Declining / Dormant] | [Low / Med / High] |
| [Champion] | | | | |
| [Economic buyer] | | | | |

**Executive sponsor status:** [Confirmed and engaged / Declining — needs re-engagement /
Unknown or departed]

If executive sponsor is declining or unknown:
> "Executive sponsor risk is present. Route per escalation matrix before renewal
> conversation begins. An executive sponsor who isn't engaged during renewal will
> not protect ARR." `[review]`

**Single-threaded relationship?** [Yes — [name] is the only contact / No — [N]
contacts active]

If single-threaded:
> "Relationship is single-threaded through [contact]. Single-threaded renewal
> conversations carry elevated risk. Identify at least one secondary stakeholder
> before the commercial conversation begins." `[review]`

---

### Dimension 4 — Commercial readiness

**Has the renewal conversation started?** [Yes — [date of first discussion] /
No / Implicitly — renewal was mentioned on [date] in [context]]

**Known commercial risks:**
- [Risk 1 — e.g., "Budget freeze announced by champion in last call"]
- [Risk 2 — e.g., "Competitor mentioned by name on [date]"]
- [Risk 3 — e.g., "Prior year contract was late by [N] days — may indicate internal
  procurement friction"]

**Price change anticipated?** [Yes — [amount or %] increase / No / Unknown]
If yes: "Price increase at renewal requires executive-level positioning. See
`/csm:renewal-readiness --price-increase-prep`."

**ARR escalation:** If ARR meets the configured escalation threshold:
> "ARR ($[amount]) exceeds the configured escalation threshold. Executive-level
> renewal involvement is required per the configured commercial motion. Route to
> [configured contact] no later than [date — N days before renewal]."

---

### Dimension 5 — Internal alignment

**Has the CSM + AE sync occurred?** [Yes — [date] / No — needed before [date]]

**Renewal strategy agreed internally?** [Yes / No — pending sync]

**Open internal actions required before renewal motion:**
1. [e.g., "AE to pull contract for price increase scenario modeling"]
2. [e.g., "CS lead to approve executive sponsor outreach"]
3. [e.g., "Confirm CRM renewal date is accurate — system shows [date] but CSM reports [date]"] `[review]`

---

### Renewal action plan

Specific actions to close readiness gaps before the renewal conversation. Ordered
by priority. Not generic.

**Immediate (do this week):**
1. [Action — e.g., "Schedule executive sponsor touch. Last contact was [N] days ago.
   Purpose: relationship maintenance before commercial motion begins. Do not mention
   renewal — this is a strategic relationship call."]
2. [Action — e.g., "Run `/csm:value-statement [account]` to build the value story
   before the renewal conversation. The value case is currently [strong/partial/weak]."]
3. [Action — escalation if applicable]

**Before renewal conversation begins ([date — recommended start]):**
1. [Action — e.g., "Internal CSM + AE sync to agree renewal strategy and roles."]
2. [Action — e.g., "Establish success criteria if not already documented."]
3. [Action — e.g., "Confirm economic buyer identity and engagement plan."]

**Renewal conversation itself:**
1. [Action — e.g., "Lead with value delivered against [primary value metric].
   Do not open with contract or pricing."]
2. [Action — e.g., "Have the success plan open — walk through each criterion
   together before discussing next year."]
3. [Action — expansion, if signals exist: "Pass expansion signal to AE prior to
   renewal call. Do not introduce expansion in the same conversation as renewal
   risk — sequence matters."]

---

## Renewal timeline (`--timeline`)

---

**Renewal Timeline — [Account Name]**
*Renewal: [date] · ARR: $[amount] · [N] days remaining*

| Date | Milestone | Owner | Status |
|------|-----------|-------|--------|
| [today] | Renewal readiness brief complete | CSM | ✅ |
| [date] | Executive sponsor touch scheduled | CSM | |
| [date] | Value statement built | CSM | |
| [date] | CSM + AE renewal sync | CSM + AE | |
| [date] | Success criteria confirmed with customer | CSM | |
| [date] | Customer renewal conversation initiated | [Renewal owner] | |
| [date] | Commercial proposal delivered | AE | |
| [date] | Executive sponsor confirmation call (if required) | CS Lead + [Exec] | |
| [date — 30 days before renewal] | Renewal committed in CRM | AE | |
| [date — 14 days before renewal] | Contract out for signature | AE | |
| [Renewal date] | Contract signed | | |

Dates are calculated from renewal date. Adjust if your configured commercial motion
uses different lead times.

---

## Customer-facing renewal prep summary (`--customer-summary`)

Appropriate to send 60-90 days before renewal. This is not a renewal push —
it is a forward-looking partnership communication that positions the renewal
as a natural continuation of shared work.

---

**[Customer contact name],**

As we approach [date], I wanted to take stock of where we are and make sure
we're aligned on what comes next.

**What we've accomplished:**
[2-3 sentences on the most meaningful outcomes achieved this period —
in the customer's business terms, with specific results. Not a feature list.]

**What's ahead:**
[1-2 sentences on what the customer has said they want to accomplish in the
next period. Connect it to what they told you at kickoff or in the last QBR.]

I'd like to set up time with you in the next [2-4 weeks] to discuss [next year /
the upcoming renewal period / our work together going forward] and make sure
we're aligned on priorities and the right structure to support them.

[Call to action: specific time or scheduling link. One clear next step.]

Looking forward to it.

[CSM name]

---

> **Note:** This is a relationship communication — not a commercial document.
> Edit the draft to match your relationship tone. Do not include ARR, pricing,
> contract dates, or renewal language in this version. The commercial conversation
> comes after this touch.

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [CRM ✓ live — renewal date, ARR, contract | CRM [configured but unverified] | CS Platform ✓ live — health, usage | CS Platform [configured but unverified] | call recording: [date] | user provided | not connected — conversation context only]
> - **Health model applied:** [Configured model — [components] | signals only — no formal model]
> - **Success criteria source:** [Account-specific from [doc] | not established — see action plan]
> - **Data as of:** [timestamp per source]
> - **ARR escalation:** [Applies — route to [contact] by [date] | Does not apply]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Revenue accountability:** Renewal ARR figures and any contraction/expansion estimates must be validated with AE before reaching CRM forecast or leadership reporting.

---

## Output

Renewal readiness output — format driven by flag (`--brief`, `--timeline`,
`--customer-summary`). Internal brief covers risk rating, deal health, and
recommended actions. Timeline produces a milestone table. Customer-facing summary
produces a value-forward narrative. See mode-specific sections for field-level structure.

## Guardrails

**Renewal readiness is distinct from risk.** This skill assesses all accounts
approaching renewal — not only at-risk ones. A Green account with a strong health
score still needs a readiness brief to ensure the commercial conversation is prepared.

**Value story must precede commercial conversation.** A renewal conversation that
opens with contract or pricing before value is established gives the customer no
reason to say yes. The action plan always places value preparation before commercial
motion.

**Success criteria gap is a renewal risk.** If formal success criteria were never
established, note it explicitly. The absence of criteria removes the strongest
retention argument.

**No commercial commitments in customer summary.** The customer-facing renewal prep
communication does not discuss ARR, pricing, or contract terms. Those belong in the
commercial conversation, which the CSM schedules separately.

**Single-threaded risk is renewal risk.** If only one stakeholder knows the product,
any change to that person's role, engagement, or availability creates immediate
renewal exposure.

**Expansion sequencing.** Expansion conversations are initiated after renewal is
committed, not simultaneously. If expansion signals are present, route to AE
before the renewal call — do not introduce both topics in one customer conversation.

---

## After the brief

- "Value story needs work — build it now: `/csm:value-statement [account]`"
- "Executive sponsor risk flagged — check stakeholder map: `/csm:stakeholder-map [account] --sponsor-risk`"
- "Account is Red — run risk memo before renewal motion: `/csm:risk-flag [account]`"
- "Renewal conversation starting — prep the call: `/csm:call-prep [account] renewal`"
- "Ready for the QBR before renewal — build it: `/csm:qbr-builder [account]`"

---

## Reference Files

The following reference files govern this skill's detailed behavior. They are loaded on-demand when the relevant behavior is being applied — they are not front-loaded into every response.

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

---

## Security & Permissions
- network_access: outbound_allowlist (CRM, CS platform, document storage per configured integrations)
- filesystem_write: false
- filesystem_read: config files only (~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md and company-profile.md)
- subprocess_execution: false
- dynamic_code_execution: false

## Trust & Verification
- Pricing, discount, and negotiation content is strictly out of scope — redirect to AE/AM if raised
- ARR and contract value are internal references only — not included in customer-facing output
- Expansion signals are internal — do not surface in renewal prep materials shared with the customer
- If config files are missing or contain [PLACEHOLDER] markers, halt and prompt for /csm:cold-start-interview
