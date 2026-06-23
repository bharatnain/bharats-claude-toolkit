---
name: expansion-signal
description: >
  Identify and qualify expansion signals in a renewal account — seat growth,
  usage expansion, product line upsell, and adjacent team opportunities. Maps
  each signal to a qualification tier (early signal / pipeline-ready / qualified)
  and recommends a TARO play for conversion. Use during pre-renewal research,
  QBR prep, or after an adoption milestone to surface upsell and cross-sell leads.
  Expansion leads are never included in GRR calculations and require a qualifying
  economic buyer conversation before entering NRR pipeline.
argument-hint: "[<account-name-or-ID>] [--deep | --quick | --catalog]"
version: "1.0.0"
deployment_target: plugin
---

# /renewals:expansion-signal [VALIDATED]

Surface and qualify expansion signals in a renewal account. Every signal found
here is a lead until proven otherwise.

---

## Use when
- You are researching an account for expansion opportunities before a renewal or QBR
- You need to identify and qualify seat growth, usage expansion, product tier upsell, or cross-sell signals in a specific account
- An adoption milestone has occurred and you want to evaluate whether it unlocks an expansion conversation
- You need to map each expansion signal to a qualification tier and a recommended TARO play before engaging the account or routing to the AE
- You want to confirm whether an account is at Pipeline-ready or Qualified tier before involving an AE in a commercial conversation

**Downstream dependency:** After this skill produces qualified expansion signals, use the CSM plugin's expansion-business-case skill to build the formal business case document for AE engagement (if the `csm` plugin is installed, run `/csm:expansion-business-case`).

## Do NOT use for
- Accounts with active churn risk signals — run `/renewals:risk-assessment` first; expansion pursuit on at-risk accounts damages trust and is counterproductive
- GRR or renewal-rate forecasting — expansion ARR is never included in GRR calculations
- Moving an expansion opportunity into NRR pipeline without a qualifying economic buyer conversation — this skill identifies and qualifies signals; formal pipeline entry requires AE involvement
- Post-churn expansion analysis — use `/renewals:churn-rca`
- Quick renewal status checks without an expansion research goal — use `/renewals:executive-summary`

## Typical Activation
> `/renewals:expansion-signal Acme Corp` — full expansion signal audit across all six signal types with qualification tier and TARO play recommendations
> `/renewals:expansion-signal Acme Corp --quick` — targeted pass for highest-probability signal before a renewal call
> `/renewals:expansion-signal --catalog` — list all detectable signal types for your configured pricing model

---

## Pre-flight

Read both configuration files before analyzing any account:
1. `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

If either file is missing or contains `[PLACEHOLDER]` markers in the pricing,
renewal book, or methodology sections, stop and route to
`/renewals:cold-start-interview`. Without pricing model, product structure, and
configured NRR target, expansion signal outputs will be untethered from your
actual commercial posture.

Fields read from config:
- Pricing model (per seat / usage-based / flat fee / tiered / hybrid)
- Product line or tier structure (from company profile)
- NRR target
- Customer segments and average deal size
- AE partner (for expansion handoff routing)
- Configured TARO playbook sources / SuccessCOACHING methodology flag

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---


## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of expansion signal request is this?
   - **Seat/Usage Capacity**: Quantitative signal — active users near licensed seats or usage approaching contracted volume. Data-driven, often auto-surfaced by CS Platform.
   - **Feature/Tier Upsell**: Qualitative signal — customer requesting higher-tier features, expressing feature gaps in tickets or calls, or fully adopting current tier.
   - **Cross-Sell / Multi-Product**: Adjacent product opportunity — customer solving a problem manually or with a competitor tool that your product line addresses.
   - **Geographic/Organizational Expansion**: Structural signal — new offices, M&A activity, separate business units, or teams evaluating independently.
   - **At-Risk Account with Expansion Signals**: Mixed signal — expansion indicators coexist with churn risk. Requires triage: renewal risk addressed before expansion pursuit.

2. **CONSTRAINTS**: What limits the solution space?
   - G2: Expansion ARR is not counted until an economic buyer has been qualified — every signal is tagged `[early signal — not yet qualified]` until formal pipeline entry. Non-negotiable.
   - G4: AE routing is mandatory for any signal reaching Qualified tier — the CSM owns signal identification and qualification handoff; the AE owns commercial conversion.
   - G5: ARR potential estimates, contract terms, and qualification tiers are internal-only. Confidentiality check required before any output leaves the CSM's view.
   - G7: Flag stale data with source date — CRM >7 days, CS Platform >3 days. Never silently omit a data gap.
   - Pricing model from config constrains which signal types apply (usage-based expansion is irrelevant for flat-fee accounts).

3. **EXPERT CHECK**: What would a veteran renewals manager verify first?
   - Is there active churn risk on this account? If yes, expansion signals are deferred until the account is stabilized — run `/renewals:risk-assessment` first.
   - Is the signal coming from a champion or an economic buyer? Champion enthusiasm alone never upgrades qualification tier — apply the Champion vs. Buyer Test.
   - Does the 90-day trend support the signal, or is this a point-in-time anomaly? A single data point is anecdotal; three consecutive months of directional signal is a pattern.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Treating a seasonal usage spike as sustained growth — require 90-day trend confirmation before qualifying as pipeline-ready.
   - Conflating feature frustration with purchase intent — a customer saying "why can't you do X?" is a support issue first, expansion signal second.
   - Pursuing expansion on a Red account — expansion conversations on accounts with active churn risk feel tone-deaf and damage trust.
   - Presenting ARR potential estimates as committed pipeline — all pre-proposal estimates are `[Low Confidence]` and must be labeled as such.
   - Routing to AE at early signal stage — premature AE involvement wastes AE time and pressures the customer relationship. Route at pipeline-ready, not before.
   - Assuming M&A or org expansion equals product expansion — the new entity may have existing vendor relationships or independent budget authority.

**After execution**, verify:
- Does each signal have a qualification tier with explicit justification for the tier assignment?
- Are all ARR potential figures tagged `[Low Confidence]` unless a formal proposal exists?
- Is the output mode (--deep / --quick / --catalog) matched to the actual need?
- Confidence: [High] if 2+ live sources corroborate signals / [Medium] if single-source or partially stale / [Low] if user-provided context only — state which.

## Mode

`--deep` (default): Full signal audit across all expansion domains with
qualification tier assignment, TARO play mapping, and recommended next actions.
Pulls live data when connectors are available.

`--quick`: Targeted pass — asks 4–5 focused questions to surface the highest-
probability expansion signal in the account and recommend one immediate action.
Use when you have limited prep time before a renewal call.

`--catalog`: List all expansion signal types the skill can detect for the configured
pricing model, with descriptions and qualifying questions for each. Use to educate
the team or build a pre-call checklist.

---

## Account identification and data pull

Ask: "Which account are you researching for expansion signals? Provide the account
name, and tell me ARR, renewal date, and current product tier/license count if you
have them."

If a CRM connector is available, pull:
- Current ARR and product tier
- Contract seat count or usage limit
- Contract start date and renewal date
- Expansion history (prior upsell or cross-sell events and dates)
- Open expansion opportunities in pipeline

If a CS Platform connector is available, pull:
- Active user count vs. licensed seat count
- Product feature adoption breadth (which modules are in use)
- Team or department breakdown of active users
- Usage trend (growing / flat / declining) over last 90 days
- Any usage-based overage or approaching limit signals

Confirm data pull before proceeding:
> "[CRM + CS Platform]: [account name] · $[ARR] ARR · [N] licensed seats / [N]
> active users · [module adoption] · data as of [timestamp]"

---

## Signal catalog — six expansion types

Evaluate each signal type based on data pulled or user input.

### 1. Seat expansion
- Active users approaching or exceeding licensed seat count
- New team members onboarded since last renewal not yet on license
- Departments using product via shared credentials (workaround for unlicensed seats)
- Recent hiring activity in teams using the product

Qualifying question to surface: "Are there users at this account accessing the
product outside of licensed seats, or departments that would benefit from access
but aren't currently licensed?"

### 2. Usage-based expansion (usage-model accounts only)
- Usage approaching or exceeding contracted volume limit
- Recent consumption spike vs. prior period
- Seasonal usage pattern suggesting coming overage
- Usage growing faster than contracted tier covers

Qualifying question: "Their usage is at [N]% of contracted volume — have you
discussed an upgrade conversation or are they managing to stay under the cap?"

### 3. Product tier or feature upsell
- Core tier features fully adopted; advanced tier features not unlocked
- Customer requesting features that exist in a higher tier
- Feature gap expressed in support tickets or CSM notes
- Recent product release unlocking new tier features customer has expressed interest in

Qualifying question: "Which features are they asking about that they don't
currently have access to?"

### 4. Multi-product or cross-sell
- Adjacent product line that addresses a problem mentioned in calls or QBRs
- Integration between current product and a new product line customer could benefit from
- Customer currently solving a problem with a competitor product or manual process
  that your product line addresses

Qualifying question: "Is there a workflow they're handling manually or with a
point solution that [product] could replace?"

### 5. Geographic or team expansion
- New office, region, or subsidiary not yet on the product
- M&A activity — acquisition target not yet onboarded
- Separate team or business unit at the same company evaluating independently

Qualifying question: "Are there other teams or offices at this account that
aren't currently on the product?"

### 6. Professional services or implementation
- Complex use case mentioned that requires configuration or integration support
- Customer building internal workarounds that a services engagement could replace
- Expansion of use case scope that warrants a new implementation project

Qualifying question: "Are they building something internally that your PS team
would normally handle?"

---

## Qualification tier assignment

For each signal identified, assign a qualification tier:

| Tier | Definition | NRR treatment | Next action |
|------|-----------|--------------|-------------|
| **Early signal** | Data or conversation suggests expansion need; no economic buyer conversation yet | `[early signal — not yet qualified]` — not in NRR | Validate with champion; set qualifying conversation goal |
| **Pipeline-ready** | Champion has confirmed interest; economic buyer awareness but no commitment | `[early signal — not yet qualified]` — not in NRR | Book qualifying conversation with economic buyer |
| **Qualified** | Economic buyer has confirmed interest or approved expansion budget; expansion is in formal pipeline | Include in NRR forecast; create CPQ quote or opportunity | Route to AE partner; build expansion proposal |

> **Signal qualification rule (non-negotiable):** Expansion signals are tagged
> `[early signal — not yet qualified]` unless an economic buyer conversation has
> occurred AND the expansion has moved to formal pipeline (CPQ quote, opportunity
> stage, or written commitment). Do not include unqualified signals in NRR figures.

---

## TARO play recommendation

For each qualified or pipeline-ready signal, recommend a TARO play:

**Trigger:** The specific adoption, usage, or need signal that makes this expansion
timely and relevant to surface now.

**Action:** The recommended play — reference configured playbook if available.
Common expansion plays: Adoption milestone review → tier upgrade conversation;
Usage approaching limit → proactive expansion proposal; Adjacent team discovery →
multi-product introduction.

**Resource:** What to bring to the expansion conversation. Consider:
- Usage data showing value delivered to current team
- ROI evidence or case study relevant to the expanding use case
- Product roadmap items relevant to expanded tier or cross-sell product
- Pricing and packaging options within your configured discount authority

**Outcome:** Observable state marking the play successful (expansion opportunity
created in CRM / CPQ quote generated / economic buyer meeting scheduled /
expansion contract signed).

> TARO play recommendations are leads, not mandates. Validate the trigger against
> what you know from direct account experience before executing.

---

## AE handoff guidance

For any signal at Pipeline-ready or Qualified tier, note the AE handoff:

> "Expansion signals at [pipeline-ready / qualified] tier should be routed to
> [AE partner from config] for the commercial conversation. Prepare:
> - Account context brief (current ARR, expansion signal, qualifying conversation summary)
> - Proposed expansion scope (seats / tier / product)
> - Draft pricing or CPQ input within your configured parameters
> - Recommended timing relative to renewal date"

If no AE partner is configured:
> "No AE partner is configured in your company profile. Run
> `/renewals:cold-start-interview --section team` to add your AE contact."

---

## Output format

---

**Expansion Signal Report — [Account Name]**
*ARR: $[amount] · Renewal: [date] · [N] days out*
*Analyzed: [date] · Sources: [list]*

**Expansion signals found: [N]**

| Signal type | Tier | ARR potential | Qualifying question answered? |
|-------------|------|--------------|-------------------------------|
| [Type] | [Early / Pipeline-ready / Qualified] | $[estimate] `[early signal — not yet qualified]` | [Y / N] |

> Note: ARR potential figures are estimates `[Low Confidence]` until a formal
> expansion proposal is built and reviewed with the economic buyer.

**Signal detail**

*[For each signal: 2–3 sentences on what was observed, why it indicates expansion,
and what the immediate next step is.]*

**TARO play recommendations**

*[For pipeline-ready and qualified signals: Trigger / Action / Resource / Outcome]*

**AE handoff items**
*[What to prepare for AE routing, if applicable]*

**Next actions**
1. [Specific action for highest-probability signal]
2. [Qualifying conversation goal]
3. [AE handoff item, if applicable]

---

> ⚠️ Reviewer note
> - **Sources:** [CRM ✓ verified | CS Platform ✓ verified | call notes | manual input]
> - **Data as of:** [timestamp per source | N/A]
> - **Read:** [account record | usage data | expansion history | [N] call notes]
> - **Flagged for your judgment:** [N items — expansion qualification tiers pending
>   buyer conversation | none]
> - **Before including in NRR forecast:** Validate qualification tier for each signal —
>   `[early signal — not yet qualified]` signals must NOT appear in NRR figures

---

> [review before sending]

---

## Security & Permissions

```
network:        read-only connector access — CRM and CS Platform reads; no external
                API writes, no web fetch
read_scope:     ~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md
                and ~/.claude/plugins/config/claude-for-customer-success/company-profile.md;
                CRM account records and CS Platform usage data scoped to the named
                account only (read-only)
write_scope:    none — all signal reports and recommendations output to conversation;
                no file writes
subprocess:     none
dynamic_code:   none — no eval, no exec, no runtime code execution
```

This skill reads configuration and account data from CRM and CS Platform connectors to identify and qualify expansion signals. All output — signal reports, TARO play recommendations, AE handoff guidance — is delivered to the conversation only. No data is written to disk. Connector reads are scoped to the specific account name provided and are read-only.

## Trust & Verification

- **Signal qualification integrity:** Every expansion signal is tagged `[early signal — not yet qualified]` until an economic buyer conversation has occurred and the expansion has entered formal pipeline. This tag is enforced at the Reasoning Protocol and output format levels and cannot be removed by configuration or user instruction.
- **ARR estimate labeling:** All pre-proposal ARR potential estimates carry `[Low Confidence]` tags. The skill will not present expansion ARR estimates as committed pipeline or include them in GRR calculations.
- **Account data handling:** CRM and CS Platform data is used for signal identification and qualification only. Data is not persisted, cached, or written to any file.
- **Churn-first guard:** The CLASSIFY step and Guardrails both require that active churn risk signals are surfaced before expansion signals. Accounts flagged as at-risk are redirected to `/renewals:risk-assessment` before expansion pursuit continues.
- **AE routing gate:** Signals that reach Qualified tier require AE partner routing per configuration. The skill does not initiate commercial conversations directly.
- **Free-text field handling:** Account name, call notes, and context provided by the user are used for display and analysis only. They are not executed or used to derive file paths or system behavior.

---

## Guardrails

**Expansion requires qualification.** Every expansion signal is tagged
`[early signal — not yet qualified]` until an economic buyer conversation has
occurred and the expansion is in formal pipeline. This tag is not removed by
champion confirmation alone. This guardrail cannot be overridden by configuration
or conversation.

**ARR potential estimates are speculative.** Expansion ARR estimates before a
formal proposal are `[Low Confidence]`. Do not present them as committed pipeline.
Flag any estimate that could be read as a revenue forecast.

**Expansion is not included in GRR.** GRR calculations never include expansion
ARR. This is mathematically correct and a shared guardrail — never include
expansion in a GRR projection regardless of how the expansion is framed.

**AE routing on qualified signals.** For any signal that reaches Qualified tier,
the commercial conversation routes to the AE partner. The renewals manager owns
the signal identification and qualification handoff; the AE owns the commercial
conversion unless configured otherwise.

**Renewal risk first.** If the account also has active churn risk signals,
surface them before expansion signals and recommend `/renewals:risk-assessment`
before pursuing expansion. An at-risk account's priority is renewal, not growth.

---

## Reference Files

- `references/reasoning-blueprint.md` — reasoning framework for this skill
