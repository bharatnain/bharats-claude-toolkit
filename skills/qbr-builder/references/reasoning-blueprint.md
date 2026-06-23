---
title: QBR Builder Reasoning Blueprint
type: reasoning-blueprint
skill: qbr-builder
version: 1.0.0
---

# QBR Builder — Reasoning Blueprint

## Problem Classification Taxonomy

### 1. Net-New QBR (--draft, no prior QBR exists)
- **Characteristics:** No baseline quarter, no prior success criteria scorecard, stakeholder list may be incomplete
- **Primary Risk:** Fabricating value claims without evidence; defaulting to generic language that erodes credibility
- **Expert Focus:** Establish measurable success criteria before writing; anchor every claim to a data source or flag it

### 2. Continuation QBR (--draft, prior QBR exists)
- **Characteristics:** Prior QBR provides baseline priorities, commitments, and metrics to score against
- **Primary Risk:** Ignoring prior commitments — cherry-picking wins while dropping missed items silently
- **Expert Focus:** Score every prior-period commitment explicitly (achieved / partial / missed); surface accountability gaps

### 3. Review of Existing Draft (--review)
- **Characteristics:** User-provided QBR draft; skill operates as editor, not author
- **Primary Risk:** Rubber-stamping unsourced claims or letting internal data leak into customer-facing content
- **Expert Focus:** Line-level audit for evidence backing, guardrail compliance, and internal/external separation

### 4. Executive Brief (--exec-brief)
- **Characteristics:** C-level audience, 1-page constraint, narrative-only (no tables)
- **Primary Risk:** Over-compressing nuance into platitudes; losing the "so what" behind each metric
- **Expert Focus:** Every sentence must carry a decision-relevant insight; ruthlessly cut anything that doesn't change executive understanding

### 5. At-Risk Account QBR
- **Characteristics:** Health score red/yellow, escalation active, renewal within 90 days, or known detractor
- **Primary Risk:** Either sugar-coating problems (losing trust) or over-indexing on negatives (triggering procurement review)
- **Expert Focus:** Lead with acknowledged challenges and concrete remediation plan; frame forward priorities around retention drivers

## Domain Heuristics

### H1 — The 72-Hour Data Freshness Rule
CRM and usage data older than 72 hours before a QBR presentation risks contradiction by the customer. Timestamp every data pull and flag staleness.

### H2 — No Success Criteria = No Value Story
If account-specific success criteria don't exist, the QBR cannot demonstrate value — only activity. Escalate criteria establishment as the top next-quarter priority.

### H3 — The Challenges Section Test
A QBR with zero challenges listed is not credible. If none surfaced in data, probe: adoption gaps, support ticket patterns, stakeholder turnover, feature requests unfulfilled.

### H4 — Internal/External Bleed Check
Expansion signals, health scores, and stakeholder relationship notes appearing in the customer-facing document is a career-limiting mistake. Verify separation before any output.

### H5 — The "So What" Filter
Every metric needs a narrative sentence explaining why it matters to the customer's business outcome. A usage number without context is noise.

### H6 — Renewal Proximity Escalation
When renewal is within 90 days, any QBR content touching renewal likelihood or ARR trajectory requires CS leadership review before distribution. Never let this ship unreviewed.

### H7 — Joint Priority Framing
Next-quarter priorities framed as "CSM will do X" signal a vendor relationship. Reframe as "Together we will..." with explicit customer-side owners and actions.

## Common Failure Modes

### Net-New QBR
- **Generic value language:** Claims like "we drove strong adoption" with no metric. **Fix:** Require metric + source or flag `[review]`.
- **Missing baseline:** No prior quarter to compare against. **Fix:** Use onboarding goals or implementation milestones as the baseline anchor.

### Continuation QBR
- **Dropped commitments:** Prior QBR promised actions that aren't scored. **Fix:** Pull prior QBR priorities and score each one explicitly — even if missed.
- **Stale success criteria:** Criteria from 3+ quarters ago that no longer reflect the customer's priorities. **Fix:** Flag for refresh discussion during QBR call.

### Review Mode
- **Surface-level review:** Checking formatting instead of evidence quality. **Fix:** Audit every value claim for a named data source; flag unsourced claims.
- **Internal data leakage:** Health scores or expansion tags left in customer-facing content. **Fix:** Separate-pass scan for internal-only markers.

### Executive Brief
- **Metric dumping:** Cramming tables into a 1-page narrative. **Fix:** Convert metrics to insight sentences; zero tables in exec briefs.
- **Missing forward view:** Summarizing the past without a clear "what's next." **Fix:** Final paragraph must state the top 2 joint priorities and what the exec needs to decide.

### At-Risk Account
- **Over-optimism:** Glossing over known problems to avoid difficult conversation. **Fix:** Name challenges explicitly with remediation timeline.
- **Doom framing:** Leading with every negative signal. **Fix:** Open with what's working, then pivot to "here's what needs attention and our plan."

## Expert Judgment Patterns

### Scope Decisions
- **Depth calibration:** Enterprise accounts get full QBR with all 6 sections; SMB/tech-touch accounts get streamlined 3-section version (wins, challenges, next priorities)
- **Data sufficiency:** If fewer than 2 data sources are available, produce a draft framework and flag data gaps rather than inventing content

### Sequencing Decisions
- **Prior QBR first:** Always read the prior QBR before writing — it sets the accountability baseline
- **Success criteria before metrics:** Establish what "good" looks like before presenting numbers
- **Internal before external:** Build the internal working document first; derive the customer-facing version by removal, never by addition

### Depth Decisions
- **Metric context threshold:** Any metric with >15% change quarter-over-quarter gets a narrative explanation
- **Challenge depth:** Each challenge needs a "what happened," "why it matters," and "what we're doing" — never just a label
- **Roadmap inclusion gate:** Only include roadmap items confirmed for external sharing; when in doubt, omit

### Stakeholder Decisions
- **Audience-appropriate language:** Technical metrics for practitioner QBRs; business outcomes for executive QBRs
- **Expansion signal routing:** Expansion signals route to AE/AM only — never surface in customer-facing content without explicit authorization
- **Escalation awareness:** If account has active escalation, QBR content must acknowledge it — pretending it doesn't exist destroys trust

### Confidence Decisions
- **Data-backed vs. inferred:** Claims sourced from CRM/CS platform are stated directly; claims inferred from call notes are flagged `[review]`
- **Metric precision:** Report metrics at the precision available in the source — don't round 47.3% to "about half"
- **Forecast hedging:** Any forward-looking statement about outcomes uses conditional language ("on track to" / "targeting") not certainty language ("will achieve")
