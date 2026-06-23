---
name: qbr-builder
description: >
  Build or review a Quarterly Business Review — value delivered against success
  criteria, metrics summary, next-period priorities, and executive narrative.
  Use for QBR prep, mid-quarter health reviews, and executive business reviews.
  Produces an internal working document and a customer-facing deliverable separately.
argument-hint: "[account name] [--draft | --review | --exec-brief]"
version: "1.0.0"
deployment_target: plugin
---

# /qbr-builder

[PROPOSED]

## Use When
- Preparing a Quarterly Business Review or Executive Business Review for a customer
- Building the internal prep brief before a QBR call
- QBR cadence has triggered and you need a structured output for the executive audience
- Renewal is approaching and the QBR doubles as the value review before the commercial conversation

## Do NOT Use For
- Routine check-in prep — use /csm:call-prep
- Success plan construction — use /csm:success-plan-builder
- Value statements without the full QBR structure — use /csm:value-statement
- Expansion business case — use /csm:expansion-business-case

## Typical Activation
"/csm:qbr-builder Acme Corp"
"Build the QBR for [account]"
"Prep for [customer]'s quarterly review"
"Create an EBR for [account]"

---

Produce a QBR that demonstrates value realized, aligns on next-period priorities,
and gives the customer a clear forward view — calibrated to your success criteria
model and CS motion.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/csm:cold-start-interview`.

Note from config:
- Primary value metric and success criteria model
- CS motion — shapes QBR depth, cadence, and formality
- Playbook sources — use configured QBR template if available
- Customer-facing plan format preference (Google Doc / Notion / slide deck)
- Escalation matrix — know routing if account surfaces risk during QBR

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---


## Reasoning Protocol

> Full reasoning blueprint: `references/reasoning-blueprint.md`

Before generating output, apply these primers:

1. **CLASSIFY**: What type of QBR is this?
- **Net-New QBR** — no prior QBR exists; build from scratch with available data
- **Continuation QBR** — prior QBR provides baseline; score prior commitments before writing new ones
- **Review of Existing Draft** — user-provided draft; audit for evidence quality and guardrail compliance
- **Executive Brief** — 1-page C-level narrative; every sentence must carry a decision-relevant insight
- **At-Risk Account QBR** — health red/yellow, escalation active, or renewal <90 days; lead with acknowledged challenges

2. **CONSTRAINTS** — enforce before generating:
- **G1 — Data freshness:** Timestamp every data pull; flag anything >72 hours stale before QBR presentation
- **G2 — Expansion stays internal:** Expansion signals appear only in the internal working document; never in customer-facing content without explicit AE/AM authorization
- **G4 — Evidence-backed claims only:** Every value claim requires a named data source; unsourced claims are flagged `[review]` internally and omitted from customer-facing output
- **G5 — Renewal language review:** Any content touching renewal probability or ARR trajectory requires CS leadership validation before distribution
- **G7 — Internal/external separation:** Health scores, expansion tags, stakeholder relationship notes, and `[review]` flags must never appear in the customer-facing deliverable

3. **EXPERT CHECK** — what a veteran CSM verifies first:
1. Do account-specific success criteria exist? If not, the QBR demonstrates activity, not value — escalate criteria establishment as top priority
2. If a prior QBR exists, is every prior-period commitment scored (achieved / partial / missed)?
3. Does the challenges section contain at least one real challenge? Zero challenges = zero credibility
4. Are next-quarter priorities framed as joint actions with customer-side owners, not a CSM to-do list?
5. Is metric context provided — does every number have a "so what" sentence tied to a business outcome?

4. **ANTI-PATTERNS** — common QBR mistakes to block:
- Generic value language without metrics ("we drove strong adoption") — require specific numbers or flag
- Dropped prior commitments — cherry-picking wins while silently omitting missed items
- Metric dumping without narrative — tables of numbers with no insight about what they mean
- Over-optimism on at-risk accounts — glossing over known problems destroys trust faster than naming them
- Internal data leakage — health scores or expansion signals bleeding into customer-facing content

**After execution**, verify:
1. **Implicit need check:** Did the CSM ask for a QBR type that doesn't match their situation? (e.g., requesting Net-New when a prior QBR exists — redirect to Continuation to avoid dropping prior commitments.)
2. **Intent satisfaction:** Does the output match the classified input type and requested mode (`--draft` / `--review` / `--exec-brief`)?
3. **Failure mode scan:** Review output against the failure modes for the classified type in the reasoning blueprint
4. **Staleness check (G7):** Is every data source timestamped? Flag CRM data >7 days stale, CS platform data >3 days stale, call/meeting data >14 days stale. Stale metrics get a `[stale: <source> as of <date>]` tag in the internal working document.
5. **Confidence calibration:** [High] if all value claims sourced from live data / [Medium] if some claims inferred or partially stale / [Low] if working primarily from CSM-provided narrative without corroborating system data — state which.

## Mode

`--draft`: Build a new QBR from scratch. Pulls data from configured integrations;
prompts for missing context.

`--review`: User provides an existing QBR draft; skill reviews it for completeness,
accuracy vs. data sources, and guardrail compliance. Returns specific edits.

`--exec-brief`: Produce a 1-page executive summary version only — designed for
a C-level audience who won't read the full QBR. No supporting metrics tables.

Default: `--draft`.

---

## Data gathering


**Connector error categorization:** When a connector call fails, distinguish the error type before proceeding:
- **Rate-limited (transient):** Connector returns HTTP 429 or equivalent throttle signal. Note the rate limit explicitly in output ("CRM data temporarily rate-limited — retry in 60 seconds recommended") and offer to retry rather than proceeding with degraded output.
- **Unavailable (permanent for this session):** Connector is not configured, authentication has expired, or service is down. Fall back to the manual-input path below and label all affected sections as "connector unavailable — manual input used."
Do not conflate these — a rate-limited connector will return data shortly; an unavailable connector will not.

**First, check if account-research was run this session.** If yes, use that context.

**If not, pull from connected integrations:**

- CRM: ARR, renewal date, contract terms, stakeholder list, account history
- CS Platform: health score, product usage trends, NPS, lifecycle stage, CTAs
- Call recording: last 2-3 QBR-relevant calls — topics, commitments, action items
- Document storage: previous QBR (date and stated priorities), success plan

**Success criteria source:** from the configured success criteria model. If the
account has account-specific success criteria in a connected document, pull them.
If not, prompt:

> "I need this account's success criteria to build a meaningful QBR — generic
> criteria produce generic reviews. Do you have a success plan or agreed success
> metrics for [account name]? Paste them or link the doc."

If the user provides nothing: build with configured defaults and flag every
value claim as `[review — unverified against actual success criteria]`.

---

## QBR structure

Produce in two parts:

**Part 1 — Internal working document** (CSM-facing; includes internal context,
health signals, escalation flags, and reviewer notes)

**Part 2 — Customer-facing deliverable** (clean; no internal health scores,
no expansion signal tags, no stakeholder relationship notes, no internal routing)

If `--exec-brief`, produce only the 1-page executive narrative — no tables.

---

### Part 1: Internal Working Document

---

**QBR Working Brief — [Account Name]**
*[Quarter] QBR · [Date] · INTERNAL — not for distribution*

---

**Account snapshot (internal)**

| Field | Value |
|-------|-------|
| ARR | $[amount] |
| Renewal | [date] — [N] days |
| Segment | [SMB / Mid-market / Enterprise] |
| Health | [Red / Yellow / Green] — [key signal] |
| Last QBR | [date] — [1-line headline from prior QBR] |
| CSM | [name] |
| AE / AM | [name] |

**Health signals for internal context:**
Pull from configured health model. Show components.

> Health components as of [timestamp]:
> - [Component 1, e.g., usage]: [signal]
> - [Component 2, e.g., engagement]: [signal]
> - [Component 3, e.g., NPS]: [signal]
> - Overall: [Red / Yellow / Green] per configured thresholds

Escalation status: [None / [Trigger] — route per matrix to [person] via [channel]]

**Expansion signals (internal):**
[Signal if detected] `[early signal — not yet qualified — route to AE]`
If none: "No expansion signals in available data."

---

### Part 2: Customer-Facing QBR

---

**[Account Name] — Quarterly Business Review**
*[Quarter] · [Date]*

*Prepared by: [CSM name], [Company]*

---

#### 1. Looking back — what we accomplished this quarter

**Against your success criteria:**

For each agreed success criterion, show: criterion → target → actual → status.

| Success Criterion | Target | Actual | Status |
|-------------------|--------|--------|--------|
| [Criterion 1] | [metric / milestone] | [result] | ✅ Achieved / 🟡 Partial / ⛔ Missed |
| [Criterion 2] | | | |

If success criteria are unknown or unverified: replace with "progress to date"
framing and add `[review]` flag in the internal version.

**Key wins:**
2-4 specific accomplishments. Concrete and evidence-based.
- [Win 1]: [1-2 sentences. Named metric or outcome. Source: [data source].]
- [Win 2]: [...]

Do not use: "We had a great quarter together." Use: "Your team activated [N] users
in [feature], exceeding the target of [M] by [%]."

---

#### 2. Product usage highlights

Pull from CS Platform / product data. Show direction, not just snapshots.

| Metric | Last Quarter | This Quarter | Trend |
|--------|-------------|--------------|-------|
| [Primary metric, e.g., weekly active users] | [N] | [N] | [↑/↓/→ + %] |
| [Secondary metric, e.g., feature X usage] | [N] | [N] | [↑/↓/→] |
| [NPS or satisfaction score] | [N] | [N] | [↑/↓/→] |

If data unavailable: "Usage metrics not available for this review — contact [CSM]
to access your product dashboard."

---

#### 3. Challenges and what we're doing about them

Name the things that didn't go as planned. QBRs that skip this lose credibility.

- **[Challenge 1]:** [What happened] → [What's being done / what we're asking from the customer]
- **[Challenge 2]:** [...]

If there were no notable challenges: "No material obstacles this quarter — the
team maintained [metric]. We'll continue [approach] in Q[N+1]."

---

#### 4. Next quarter — priorities and plan

Frame as joint priorities, not a CSM to-do list.

**Joint priorities for Q[N+1]:**

| Priority | Why it matters | Actions | Owner | Timeline |
|----------|---------------|---------|-------|----------|
| [Priority 1] | [Customer outcome] | [Specific actions] | [Customer / CSM / Joint] | [Date range] |
| [Priority 2] | | | | |

**Aligned success criteria for Q[N+1]:**
Restate or update the success criteria the account will measure at the next QBR.
If new criteria need to be agreed: leave a placeholder and flag for discussion
during the QBR call.

---

#### 5. Roadmap alignment

What's coming from the product that's relevant to this account's priorities?

Note: only include roadmap items that have been approved for external sharing.
Flag anything speculative: "Please verify roadmap commitments with your AE before
including in the customer-facing version."

- [Feature/initiative]: [Relevance to this account's success criteria] — [Estimated timeline]

If no relevant roadmap items or roadmap is not available: omit this section.

---

#### 6. How to reach us

| Need | Contact | Channel | Response time |
|------|---------|---------|--------------|
| Day-to-day questions | [CSM name] | [email / Slack] | [1 business day] |
| Urgent issue | [Support channel] | [link] | [SLA from your contract] |
| Executive / escalation | [CS lead or VP name] | [email] | [per configured escalation matrix] |

---

### QBR review checklist (for `--review` mode)

When reviewing a submitted QBR draft, check:

- [ ] Every value claim is sourced — not generic ("we drove great adoption")
- [ ] Success criteria are account-specific, not template-default
- [ ] Challenges section is present — no QBR is challenge-free
- [ ] Next-quarter priorities are joint, not unilateral CSM actions
- [ ] No internal health scores, expansion signals, or stakeholder relationship
  notes in the customer-facing version
- [ ] Renewal language (if present) doesn't imply committed revenue — flag for
  reviewer validation before leadership distribution
- [ ] No roadmap commitments without verified approval for external sharing
- [ ] Reviewer note is populated

Return specific edits with line references, not a summary score.

---

## Reviewer note

Every QBR output includes:

> **⚠️ Reviewer note**
> - **Sources:** [CRM ✓ live | CRM [configured but unverified] | CS Platform ✓ live | CS Platform [configured but unverified] | user-provided success plan | prior QBR from [date] | not connected — conversation context only]
> - **Data as of:** [timestamp per source]
> - **Success criteria source:** [account-specific from [doc] | configured default — verify with customer]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before sending:** Remove internal version content. Verify roadmap items approved for external sharing. If renewal language is present, validate with CS lead before distribution.

---

## Output

QBR presentation document — structured markdown with executive summary, period
review (goals vs. actuals), value delivered, key metrics, strategic themes, and
next-period plan. Adapts depth to `--exec` or `--full` flag. See **QBR structure**
section for field-level detail.

## Guardrails

**Quiet mode.** The customer-facing QBR contains no skill narration, no internal
notes, no `[review]` flags, no source attributions. Those are in the internal
working document only.

**Value claims must be evidence-based.** Generic language ("we partnered closely")
is not a value claim. If a claim can't be sourced, it's flagged `[review]` in the
internal version and omitted from the customer-facing version until verified.

**Renewal language.** If the QBR includes any language about renewal probability
or ARR trajectory, it's flagged in the reviewer note as requiring validation before
distribution to leadership or finance.

**Expansion stays internal.** Any expansion signal is in the internal working
document only. It never appears in the customer-facing QBR without explicit
authorization from the AE/AM.

**No invented metrics.** If product usage data is unavailable, omit the metrics
table rather than estimating. If success criteria were never formally agreed,
state that and propose establishing them as a next-quarter action.

---

## After the QBR

Post-QBR actions to offer:
- "Want call prep for the QBR presentation? `/csm:call-prep [account] qbr`"
- "Want to run a stakeholder map before the QBR? `/csm:stakeholder-map [account]`"
- "QBR showed risk signals — want a risk memo? `/csm:risk-flag [account]`"
- "Renewal is approaching — want a renewal readiness check? `/csm:renewal-readiness [account]`"

---

## Reference Files

The following reference files govern this skill's detailed behavior. They are loaded on-demand when the relevant behavior is being applied — they are not front-loaded into every response.

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

---

## Security & Permissions
- network_access: outbound_allowlist (CRM, CS platform, call recording tool, document storage per configured integrations)
- filesystem_write: outbound to document storage only (per configured integration)
- subprocess_execution: false
- dynamic_code_execution: false

## Trust & Verification
- The internal prep brief and customer-facing EBR deck are distinct outputs — internal health scores, expansion signals, and stakeholder assessments must not appear in the customer deck
- Output documents are routed to configured document storage only — customer-facing deliverable to the configured customer portal or presentation platform; internal working document to the CSM workspace; do not distribute outside configured destinations
- Value metrics must reference configured success criteria — do not invent outcomes
- If config files are missing or contain [PLACEHOLDER] markers, halt and prompt for /csm:cold-start-interview
