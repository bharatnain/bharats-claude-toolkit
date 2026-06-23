---
name: health-score-review
description: >
  Structured health review for one account or a portfolio cohort — health signal
  breakdown, trend analysis, risk classification, and recommended actions. Use
  for weekly account reviews, portfolio triage, or when a health alert fires.
  Applies your configured health model components and thresholds.
argument-hint: "[account name | --portfolio] [--triage | --deep]"
version: "1.0.0"
deployment_target: plugin
---

# /health-score-review

[PROPOSED]

## Use When
- Reviewing the health state of a specific account before a call or intervention
- Running portfolio triage to identify which accounts need attention this week
- A health signal has triggered (usage drop, NPS decline, support spike, champion departure)
- Preparing for QBR or renewal and need a structured health narrative
- Escalation routing requires a confirmed health classification before proceeding

## Do NOT Use For
- Real-time health score calculation — this skill interprets signals, it does not compute scores
- Replacing call-prep — use /csm:call-prep after health review for the full pre-call brief
- Generating the escalation memo — use /csm:escalation-memo once risk is confirmed
- Portfolio reporting for leadership — this skill is CSM-facing, not exec-facing
- Producing the structured risk memo or determining escalation routing once health review confirms an at-risk classification — use /csm:risk-flag

## Typical Activation
"/csm:health-score-review Acme Corp"
"/csm:health-score-review --triage"
"What's the health status of [account]?"
"Run a portfolio triage"
"Flag any at-risk accounts in my book"

---

Review account health using your configured health model — signal by signal,
not just a color verdict.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/csm:cold-start-interview`.

Critical configuration to load:
- Health model components and weights (e.g., usage 40%, engagement 20%, support 20%, NPS 20%)
- Red threshold and Yellow threshold
- Churn signal definitions
- Escalation matrix — what triggers escalation and to whom

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---


## Reasoning Protocol

> Blueprint: `references/reasoning-blueprint.md`

Before generating output, apply these primers:

1. **CLASSIFY** — Determine input type before proceeding:
- **A: Single Account — Data-Rich** — CS Platform connected, component scores and trends available
- **B: Single Account — Data-Sparse** — partial signals, user-provided data, missing components
- **C: Portfolio Triage** — multiple accounts, ranked prioritization needed
- **D: Alert-Triggered** — reactive review fired by health alert, usage drop, or escalation event
- **E: Pre-Renewal** — renewal within 90 days, proactive review with stakeholder visibility

2. **CONSTRAINTS** — Apply before generating any output:
- **G1:** Health scores are heuristics — never frame output as churn prediction or likelihood. Show components and evidence; classification is the CSM's judgment.
- **G2:** No churn signal marked "Present" without direct evidence. Absence of data = "Unknown," never "No."
- **G4:** No escalation recommendation without a named escalation path from config (person, channel, SLA). Flag missing path before proceeding.
- **G5:** Portfolio triage contains ARR and health classifications — run destination check before any output distributed beyond the CSM.
- **G7:** Flag any health data older than 30 days with source date and staleness indicator. Stale NPS (>6 months) treated as Unknown.

3. **EXPERT CHECK** — What a veteran CSM would verify first:
- Which single component is driving the overall score? (Score-anchoring trap: composite hides the signal)
- Is there a usage drop >20% in 30 days? (H1 — usage drops precede churn by 60-90 days)
- Has the executive sponsor changed? (H4 — sponsor departure overrides component scores)
- Are multiple moderate signals converging across independent components? (H7 — convergence > single strong signal)
- For renewals <90 days: apply renewal proximity amplifier (H6 — Yellow becomes Red-tier urgency)
- For portfolio: is ranking compound (health x ARR x renewal proximity), not health-only?

4. **ANTI-PATTERNS** — Mistakes to avoid:
- Reporting composite score without component decomposition
- Classifying Red/Yellow/Green without naming which components are missing or stale
- Flat portfolio ranking by health score alone (ignores ARR and renewal proximity)
- Investigating only the triggering alert signal without full component scan
- Treating days-since-contact as standalone metric (H3 — weight by current health tier)
- Producing generic interventions ("monitor closely") instead of specific who/what/when actions

**After execution**, verify:
- Does the output answer the actual request (single review, triage, deep dive)? Is mode selection appropriate?
- Check against classification-specific failure modes in blueprint. For Type B: are all gaps named? For Type C: is ranking compound? For Type E: was optimism bias checked?
- How many components have live data? Flag partial-data classifications. Any component >30 days old flagged in reviewer note?
- Confidence: [High] if CS Platform live with all configured components / [Medium] if partial integrations or some stale data / [Low] if user-provided context only — state which.

## Mode

**Single account review:** Default. Produce a full health breakdown for one account.

`--triage`: Portfolio triage — rapid scan of all accounts in the book; surface
Yellow and Red accounts only; no deep analysis per account. Returns a prioritized
list with top risk factor per account.

`--deep`: Full account analysis — health signal breakdown, trend direction over
30/60/90 days, root cause hypothesis, and recommended intervention.

`--portfolio`: Alias for `--triage`.

---

## Data gathering


**Connector error categorization:** When a connector call fails, distinguish the error type before proceeding:
- **Rate-limited (transient):** Connector returns HTTP 429 or equivalent throttle signal. Note the rate limit explicitly in output ("CRM data temporarily rate-limited — retry in 60 seconds recommended") and offer to retry rather than proceeding with degraded output.
- **Unavailable (permanent for this session):** Connector is not configured, authentication has expired, or service is down. Fall back to the manual-input path below and label all affected sections as "connector unavailable — manual input used."
Do not conflate these — a rate-limited connector will return data shortly; an unavailable connector will not.

### Single account

Pull from connected integrations per configured profile:
- CS Platform: current health score, component breakdown, lifecycle stage, CTAs
- Product data / CRM: usage metrics (DAU, feature adoption, last login)
- Support: open tickets, P1/P2 history, ticket velocity
- Call recording: engagement frequency, last call date, attendees
- NPS: most recent score and date

Fallback if nothing connected:
> "I need health signal data for this account. Share what you have — a CS Platform
> export, recent usage numbers, last call date, or NPS score. Even partial data
> produces a more useful review than a blank sheet."

### Portfolio triage

Pull account list from CRM or CS Platform. For each account: current health
score (or last known), days since last contact, renewal date.

If CRM is not connected:
> "For portfolio triage, paste your account list with current health status,
> ARR, and renewal dates. I'll prioritize from there."

---

## Single account health review

---

**Health Review — [Account Name]**
*[Date] · [CS motion] · [Segment]*

---

### Health summary

| Component | Weight | Signal | Direction | Score contribution |
|-----------|--------|--------|-----------|-------------------|
| [Component 1: e.g., Product usage] | [configured %] | [current value] | [↑↓→ vs 30-day] | [Red/Yellow/Green for this component] |
| [Component 2: e.g., Engagement] | [configured %] | [last contact: N days] | [↑↓→] | |
| [Component 3: e.g., Support] | [configured %] | [N open tickets / P1: Y/N] | [↑↓→] | |
| [Component 4: e.g., NPS] | [configured %] | [score / date] | [↑↓→] | |
| [Additional configured component] | | | | |

**Overall health:** [Red / Yellow / Green]
*Threshold applied: Red = [configured], Yellow = [configured]*

If no CS Platform configured and components are not defined: use the manual
signal prompts from the company profile (what signals make you worried).
Classify as [At Risk / Watch / Healthy] based on signals present.

---

### Signal narrative

3-5 sentences interpreting the component breakdown. Do not just restate the table.

> "The account's product usage component is the primary concern — weekly active
> users dropped 22% over 30 days, which puts this below the configured Yellow
> threshold. Engagement is holding: the last call was [N] days ago, within the
> [configured threshold] for [high-touch/tech-touch]. Support load increased
> (3 open tickets vs. 1 last month), but none are P1/P2. NPS is from [N] months
> ago — stale enough to flag for update."

Language always shows components and evidence — not a verdict like "this account
is likely to churn."

---

### Churn signals present

From configured churn signal definitions:

| Signal | Present | Evidence | Weight |
|--------|---------|----------|--------|
| Executive sponsor departure | [Yes / No / Unknown] | [context] | High |
| Product usage drop >20% | [Yes / No] | [% change] | High |
| Open escalation or P1 ticket | [Yes / No] | [ticket details] | High |
| NPS detractor + no recovery | [Yes / No] | [score + date] | Medium |
| Missed QBR or no-show pattern | [Yes / No] | [last attended: date] | Medium |
| Competitor evaluation underway | [Yes / No / Unknown] | [source] | High |
| No contact in >[threshold] days | [Yes / No] | [last contact: date] | Medium |

Flag each present signal as `[review]` with the specific evidence.

---

### Risk classification

Based on configured thresholds and signals present:

**Classification:** [Red — immediate intervention / Yellow — monitor and engage /
Green — healthy / Unknown — data insufficient]

**Escalation trigger:** [Does this account meet the configured escalation threshold?]
If yes: "Route per matrix — [escalation route from config] within [SLA]."
If no: "Below escalation threshold. CSM-managed watch."

---

### Trend analysis

If historical data is available (CS Platform or prior account-research sessions):

| Metric | 90 days ago | 60 days ago | 30 days ago | Today | Trend |
|--------|------------|------------|------------|-------|-------|
| [Health score or primary metric] | | | | | [↑↓→ and rate] |
| [Usage metric] | | | | | |

If trend data is unavailable: "Trend analysis not available — no historical signal
data retrieved this session. Point-in-time assessment only."

**Trend interpretation:** Is the account stable, improving, or declining? Name
the direction and the rate of change. A slow decline is different from a sudden
drop.

---

### Recommended interventions

Calibrate to the risk classification and configured CS motion.

**Red account:**
1. [Specific action with timeline] — e.g., "Escalate to [route from matrix] within [SLA]"
2. [Specific outreach action] — e.g., "Request executive sponsor check-in within 48h"
3. [Recovery action] — e.g., "Run risk-flag to prepare structured memo: `/csm:risk-flag [account]`"

**Yellow account:**
1. [Specific monitoring action] — e.g., "Proactive check-in call within 7 days focused on [specific signal]"
2. [Prevention action] — e.g., "Engage champion on usage drop — ask what changed"
3. [Escalation prep] — e.g., "If [specific trigger] occurs, escalate per matrix"

**Green account:**
1. [Growth action] — e.g., "Schedule QBR if >90 days since last one"
2. [Expansion awareness] — internal note only, tagged `[early signal — not yet qualified]`

Do not produce generic interventions like "monitor closely" or "improve
engagement." Every recommendation is specific — who, what, when.

---

## Portfolio triage (`--triage`)

Return a ranked list — highest risk first.

---

**Portfolio Health Triage**
*[Date] · [N accounts reviewed]*

---

**Red accounts — immediate action:**

| Account | ARR | Renewal | Top risk signal | Recommended action |
|---------|-----|---------|----------------|-------------------|
| [Account] | $[ARR] | [Date] | [1-line signal] | [Specific action] |

**Yellow accounts — watch:**

| Account | ARR | Renewal | Top risk signal | Recommended action |
|---------|-----|---------|----------------|-------------------|
| [Account] | $[ARR] | [Date] | [1-line signal] | [Specific action] |

**Accounts approaching renewal (<90 days):**

| Account | ARR | Renewal | Health | Risk signal |
|---------|-----|---------|--------|------------|
| [Account] | $[ARR] | [Date] | [R/Y/G] | [Signal] |

**Summary:**
- [N] Red accounts · [N] Yellow accounts · [N] approaching renewal
- Total ARR at risk: $[sum of Red + Yellow + <90 day]
- Highest priority: [account name] — [reason]

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [CS Platform ✓ live — health score + components | CS Platform [configured but unverified] | CRM ✓ live — usage + engagement | CRM [configured but unverified] | user provided | not connected — conversation context only]
> - **Health model applied:** [Components and weights from config | user-defined signals | no formal model — signals only]
> - **Data as of:** [timestamp per source]
> - **Staleness flags:** [NPS from [N] months ago — stale | usage data confirmed live | engagement from last call [date]]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]

---

## Output

Health review report — format driven by `--single` (default) or `--triage` flag.
Single-account mode produces a structured markdown brief with signal inventory,
score justification, and recommended actions. Portfolio triage produces a ranked
table with risk tier, primary driver, and next action per account.

## Guardrails

**Health scores are heuristics, not verdicts.** The output shows component signals
and the account's position relative to configured thresholds. It does not say "this
account will churn." That inference is the CSM's judgment.

**No escalation without context.** When the skill recommends escalation, it names
the route (person, channel, SLA) from the configured escalation matrix. A flag
without a path does not help.

**No silent data gaps.** If a component is missing (NPS not available, usage data
stale, no CS Platform connected), the reviewer note names the gap and the health
classification is adjusted accordingly ("classification is based on partial signal
data — [component] unavailable").

**Churn signals require evidence.** A signal is marked present only if there is
direct evidence. Absence of data is "Unknown," not "No."

**Portfolio triage contains account-level data.** Distribution of the triage
report outside the CS team requires a destination check — ARR values and health
classifications are confidential.

---

## After the review

- Red account: "Want a structured risk memo? `/csm:risk-flag [account]`"
- Approaching renewal + Yellow/Red: "Run renewal readiness: `/csm:renewal-readiness [account]`"
- Executive sponsor signal: "Check stakeholder map: `/csm:stakeholder-map [account] --sponsor-risk`"
- Portfolio triage complete: "Want deep reviews on the top 3 Red accounts? Name them and I'll run `/csm:health-score-review --deep` on each."

---

## Reference Files

The following reference files govern this skill's detailed behavior. They are loaded on-demand when the relevant behavior is being applied — they are not front-loaded into every response.

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

---

## Security & Permissions
- network_access: outbound_allowlist (CS platform, CRM, call recording tool per configured integrations)
- filesystem_write: false
- filesystem_read: config files only (~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md and company-profile.md)
- subprocess_execution: false
- dynamic_code_execution: false

## Trust & Verification
- Health classifications (Green/Yellow/Red/Critical/Unknown) must align with configured health model thresholds
- Health scores and risk classifications are internal — must not appear in any customer-visible output
- If config files are missing or contain [PLACEHOLDER] markers, halt and prompt for /csm:cold-start-interview
- Reviewer note must flag data freshness and any signals that require CSM judgment before acting
