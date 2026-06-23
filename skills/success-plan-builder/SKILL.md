---
name: success-plan-builder
description: >
  Build or update a customer success plan — account-specific success criteria,
  measurable milestones, engagement cadence, and mutual commitments. Use at
  kickoff for new accounts, when success criteria have drifted, or when an
  account needs a plan reset. Produces a co-authored document, not a CSM
  internal tracker.
argument-hint: "[account name] [--new | --reset | --review]"
version: "1.0.0"
deployment_target: plugin
---

# /success-plan-builder

[PROPOSED]

## Use When
- Starting a new customer engagement and need to establish a formal success plan — in free-form narrative or co-authored document format, without requiring the OCV canvas structure
- An existing success plan needs to be updated after a QBR, health review, or goal change
- Renewal is approaching and the success plan needs to reflect value delivered and next-period goals
- Executive sponsor has changed and the plan needs to be refreshed for the new stakeholder
- The organization does not use the OCV (Outcome-to-Customer Value) system, or the OCV canvas format is not applicable to this account or engagement

**Upstream dependency:** Before building a success plan for a new engagement, define the 3–5 success criteria that form the plan's foundation using the Onboarding plugin's success-criteria skill (if the `onboarding` plugin is installed, run `/onboarding:success-criteria`).

## Do NOT Use For
- The structured success plan canvas format — use /csm:success-plan-canvas for OCV-aligned canvas output
- Progress tracking against an existing canvas — use /csm:success-plan-progress-review
- QBR deck construction — use /csm:qbr-builder
- Value statements for renewal — use /csm:value-statement

## Typical Activation
"/csm:success-plan-builder Acme Corp"
"/csm:success-plan-builder Acme Corp --update"
"/csm:success-plan-builder Acme Corp --review"
"Build a success plan for [account]" (free-form narrative, no OCV canvas required)
"Update the success plan for [customer]"

---

Build a success plan that the customer will actually sign off on — account-specific
success criteria, measurable milestones, joint ownership, and a cadence that
reflects your configured CS motion.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/csm:cold-start-interview`.

Note from config:
- Success criteria model (account-specific vs. standard template)
- Primary value metric
- CS motion — shapes plan depth, cadence, and co-authorship approach
- Customer-facing plan format preference
- Playbook sources — use configured success plan template if available

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---


## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of success plan request is this?
   - **New Account Plan**: Fresh account post-kickoff; no prior plan exists; goals from sales handoff or kickoff notes.
   - **Plan Reset**: Existing plan has drifted — sponsor change, use case pivot, criteria never validated, or material context shift.
   - **Plan Review**: User submits an existing plan for quality assessment against measurability, co-ownership, and CS motion alignment.
   - **Milestone Recalibration**: Sound plan but timelines or targets need adjustment due to adoption pace, customer delays, or scope changes.

2. **CONSTRAINTS**: What limits the solution space?
   - Success criteria must originate from customer-stated business outcomes, never inferred from product features.
   - Primary value metric from company profile must be traceable in the success criteria.
   - Customer-facing plan must contain zero internal health scores, expansion signals, or escalation routing.
   - Engagement cadence must match configured CS motion (high-touch / tech-touch / hybrid).
   - Renewal language requires reviewer validation before sharing with leadership or finance.
   - G5: Internal data (health scores, ARR, expansion signals) must never appear in customer-facing output
   - G7: Flag any data older than 30 days with source date and staleness indicator

3. **EXPERT CHECK**: What would a veteran CSM verify first?
   - Are the success criteria stated in the customer's own language, or has the CSM translated them into product-speak?
   - Does the mutual commitments section include actual customer commitments, or is this a one-sided CSM delivery plan?
   - Is the renewal-ready milestone (M5) positioned at least 60 days before renewal date?

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Building criteria from product features because kickoff notes are thin — ask for customer goals explicitly instead.
   - Generic milestones that don't trace to specific success criteria from Section 3.
   - Plans with no `[review]` flags — either perfect information (rare) or insufficient scrutiny.
   - Patching dates on a fundamentally misaligned plan instead of rebuilding from current goals.
   - Mutual commitments section with only CSM commitments — this isn't a co-authored plan.
   - Adjusting targets downward without documenting the rationale or addressing root cause.

**After execution**, verify:
- Does the output answer the implicit question the CSM is asking?
- Are all data sources timestamped and staleness-flagged?
- Is the output mode matched to the actual need?
- Confidence: [High] if 2+ live sources corroborate / [Medium] if single-source or partially stale / [Low] if user-provided context only — state which.

**For complex scenarios**, load additional reasoning:
- Domain blueprint: `references/reasoning-blueprint.md`

## Mode

`--new`: Build a success plan from scratch for a new or recently kicked-off account.

`--reset`: Rebuild success criteria for an existing account where the original
plan has drifted, criteria were never properly established, or account context
has materially changed (new sponsor, new use case, new segment).

`--review`: User provides an existing success plan; skill reviews it for
completeness, specificity, and whether criteria are actually measurable. Returns
specific edits.

Default: prompt once — "Is this a new plan or an update to an existing one?"

---

## Data gathering


**Connector error categorization:** When a connector call fails, distinguish the error type before proceeding:
- **Rate-limited (transient):** Connector returns HTTP 429 or equivalent throttle signal. Note the rate limit explicitly in output ("CRM data temporarily rate-limited — retry in 60 seconds recommended") and offer to retry rather than proceeding with degraded output.
- **Unavailable (permanent for this session):** Connector is not configured, authentication has expired, or service is down. Fall back to the manual-input path below and label all affected sections as "connector unavailable — manual input used."
Do not conflate these — a rate-limited connector will return data shortly; an unavailable connector will not.

**What's needed before building:**

1. **Account goals** — what the customer said they wanted to accomplish
   (from kickoff notes, sales handoff notes, or user-provided context)

2. **Product context** — which features / modules are in scope for this account

3. **Stakeholder context** — who owns success on the customer side; who measures it

4. **Timelines** — contract duration, key milestones already committed, renewal date

5. **Existing success criteria** — if a plan exists, pull it before rebuilding

Pull from connected sources where available:
- CRM: contract duration, renewal date, stakeholder contacts, sales handoff notes
- Document storage: existing success plan, kickoff deck, onboarding notes
- CS Platform: account lifecycle stage, current health signals

Minimum viable prompt if nothing is connected:

> "To build a success plan that the customer will actually own, I need the customer's
> stated goals. What did they tell you — during the sales process or kickoff — that
> they want to accomplish with [product]? Paste notes, a handoff doc, or a
> quote if you have one."

Do not build a generic success plan from product features alone. Success criteria
must come from the customer's stated business outcomes, not assumed use cases.

---

## Success plan structure

---

**[Account Name] — Customer Success Plan**
*[Quarter / date range]*
*Prepared jointly by: [CSM name], [Company] · [Customer sponsor name], [Account]*

---

### 1. About this plan

One paragraph. Plain language. Why this document exists and how it will be used.

> "This success plan captures what [Account] is trying to accomplish with [product],
> the milestones we'll use to measure progress, and the commitments both teams are
> making to get there. We'll review it at each [cadence per CS motion: monthly /
> quarterly] check-in and update it as priorities shift."

---

### 2. Your goals

The customer's goals in their language — not product feature descriptions.

**Business goal [1]:** [What the customer said they want to achieve]
*Why it matters:* [Business context — e.g., "the team is scaling from 50 to 200
users and needs faster onboarding" — not assumed]

**Business goal [2]:** [...]

Do not translate customer goals into product language here. Keep the customer's
framing. Translation to product features happens in Section 3.

If goals are unclear or unstated: flag in the reviewer note and add a `[review]`
marker — "Customer's stated goals not confirmed. Review with sponsor before plan
is finalized."

---

### 3. Success criteria

For each business goal, define one or more observable, measurable criteria.

Apply configured success criteria model:
- If account-specific model: build criteria in collaboration with the customer
- If standard template: start from the template and customize per account goals

**Success criterion format:**

> **[Criterion name]**
> - **Measure:** [Specific metric — e.g., "% of licensed users who complete first workflow within 30 days of license activation"]
> - **Baseline:** [Where the account is today, if known]
> - **Target:** [The agreed number or milestone — e.g., ">70% within 90 days"]
> - **Evidence source:** [Where this will be measured — CS Platform / product analytics / customer-reported]
> - **Review cadence:** [When this will be checked — e.g., "monthly at check-in"]

Criteria that cannot be measured get a `[review]` flag: "This criterion as stated
is not measurable — agree on a specific metric with the customer before finalizing."

**Primary value metric:** [Configured primary value metric from company profile]
— this should appear as one of the success criteria or as an explicit success
criterion overlay.

---

### 4. Milestones

Time-bound markers that show the account is on track. Not a task list — milestones
mark when something meaningful has been accomplished.

| Milestone | Description | Target date | Owner | Health signal if missed |
|-----------|-------------|------------|-------|------------------------|
| M1 | [First meaningful event — e.g., "All users activated and first workflow completed"] | [Date] | [Customer / CSM / Joint] | [Flag if missed by [date+buffer]] |
| M2 | [Second milestone] | | | |
| M3 | [First value milestone — primary value metric achieved] | [Date — ideally within configured TtV target] | | |
| M4 | [Adoption milestone — criteria threshold reached] | | | |
| M5 | [Renewal-ready milestone — all success criteria at target] | [Date before renewal] | | |

Milestones are co-owned — mark the owner. A milestone owned entirely by the CSM
is an internal commitment, not a joint one.

---

### 5. Engagement cadence

What the customer can expect — and what's expected of them.

| Touchpoint | Frequency | Format | Attendees | Purpose |
|-----------|-----------|--------|-----------|---------|
| Check-in call | [Monthly / quarterly — per CS motion] | [Video call / async update] | [CSM + customer sponsor] | [Progress review, issue triage] |
| QBR | Quarterly | [60-min video] | [CSM + AE + exec sponsor] | [Value review, next-quarter alignment] |
| Health review | [As needed / triggered by health signal] | [Email or call] | [CSM] | [Risk identification] |
| Executive sponsor call | [Semi-annually or as needed] | [30-min video] | [CS lead + exec sponsor] | [Strategic alignment] |

Calibrate frequency to configured CS motion:
- High-touch: monthly minimum; QBR at each quarter
- Tech-touch: quarterly check-in standard; no standing monthly call
- Hybrid: match the segment this account sits in

---

### 6. Mutual commitments

What each party commits to. Both sides have responsibilities — a plan that only
lists CSM commitments is not a mutual plan.

**[Company] commits to:**
- [Specific commitment — e.g., "Respond to support tickets within [SLA]"]
- [Specific commitment — e.g., "Provide a dedicated CSM point of contact"]
- [Specific commitment — e.g., "Share product roadmap quarterly"]

**[Account name] commits to:**
- [Customer commitment — e.g., "Assign an internal project champion with time allocation"]
- [Customer commitment — e.g., "Provide feedback within 5 business days of deliverables"]
- [Customer commitment — e.g., "Ensure executive sponsor attends semi-annual reviews"]

If mutual commitments section is left to generic placeholders, flag `[review]` —
a plan without customer commitments isn't co-owned.

---

### 7. How to reach us

| Need | Contact | Channel | Response time |
|------|---------|---------|--------------|
| Day-to-day | [CSM name] | [email / Slack] | [1 business day] |
| Urgent | [Support] | [channel] | [per SLA] |
| Escalation | [CS lead or VP] | [email] | [per escalation matrix] |

---

### 8. Plan history

| Date | Change | Updated by |
|------|--------|-----------|
| [Date] | Initial plan created | [CSM name] |

---

## Review mode (`--review`)

When reviewing a submitted success plan, check:

- [ ] Success criteria are measurable — specific metric, target, evidence source
- [ ] Customer's goals are stated in the customer's language, not product feature language
- [ ] Milestones have owners — not just the CSM
- [ ] Engagement cadence matches configured CS motion
- [ ] Mutual commitments section includes customer commitments, not only CSM
- [ ] Primary value metric from company profile is reflected in criteria
- [ ] No internal health signals or escalation routing in the customer-facing document
- [ ] Plan has a review / update cadence — it's a living document, not a one-time deliverable

Return specific edits with section references.

---

## Reviewer note (internal)

> **⚠️ Reviewer note**
> - **Sources:** [Customer goals: [source] | CRM ✓ live | CRM [configured but unverified] | Document: [doc name, date] | user-provided | not connected — conversation context only]
> - **Success criteria source:** [Account-specific from [source] | configured standard template — customize before finalizing]
> - **Data as of:** [timestamp]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before sending:** Verify customer has reviewed and agreed to the success criteria in Section 3 before treating this as a mutual plan. Success criteria agreed verbally but not in writing are flagged `[review]`.

---

## Output

Success plan document — format driven by `--draft` (default) or `--review` flag.
Draft mode produces a full structured plan with goals, milestones, metrics, and
owner assignments. Review mode produces a gap analysis against an existing plan.
See **Success plan structure** section for field-level detail.

## Guardrails

**No invented goals.** Do not infer success criteria from product features or
industry benchmarks. Criteria come from stated customer goals. If goals are
unknown, the reviewer note says so explicitly and the plan is marked `[DRAFT]`.

**Co-authorship is the goal.** A plan the customer never saw is an internal CSM
document. The plan is not finalized until the customer sponsor has reviewed and
agreed to the success criteria.

**Quiet mode.** The customer-facing plan contains no internal health scores,
no expansion signal tags, no escalation routing. Those stay in the reviewer note.

**Renewal language.** If the plan covers a period that includes the renewal window,
do not include language that implies renewal likelihood — flag for reviewer
validation before sharing with leadership or finance.

**Primary value metric.** The configured primary value metric from the company
profile must be traceable in the success criteria. If it's absent, flag it.

---

## After the plan

- "Plan drafted. Want to walk through the success criteria with the customer?
  I can prepare talking points. `/csm:call-prep [account] kickoff`"
- "Want to set a milestone review reminder? Run `/csm:renewal-readiness [account]`
  when you reach M5."
- "Ready to build the QBR when M4 or M5 are complete? `/csm:qbr-builder [account]`"

---

## Reference Files

The following reference files govern this skill's detailed behavior. They are loaded on-demand when the relevant behavior is being applied — they are not front-loaded into every response.

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

---

## Security & Permissions
- network_access: outbound_allowlist (CRM, CS platform, document storage per configured integrations)
- filesystem_write: outbound to document storage only (per configured integration)
- subprocess_execution: false
- dynamic_code_execution: false

## Trust & Verification
- Internal signals (health scores, expansion flags, ARR) must not appear in customer-facing plan output
- Output documents are routed to configured document storage only — customer-facing plan to the configured customer portal or collaboration platform; reviewer notes and internal context to the CSM workspace; do not distribute outside configured destinations
- Success criteria must be validated against the customer's stated goals — do not invent metrics
- If config files are missing or contain [PLACEHOLDER] markers, halt and prompt for /csm:cold-start-interview
