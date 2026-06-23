---
name: security-questionnaire-responder
description: "Use when a prospect or customer sends a recurring vendor security questionnaire — SIG (Lite/Core), CAIQ/CSA STAR, VSA, or a custom buyer spreadsheet — and you need evidence-backed answers fast without a security team. Builds and reuses a control-answer library, maps every answer to a verifiable evidence artifact, scores answer confidence, and gates low-confidence or fabrication-risk items for human review before the questionnaire goes back to the buyer. For founders and engineers selling B2B who face the same questions on every enterprise deal. NOT pursuit/bid strategy or win-themes (use rfp-responder), NOT contract redline (use general-counsel-advisor), NOT achieving the underlying certification (use soc2 / iso-27001 / gdpr / hipaa / pci-dss)."
license: MIT
tags: [enterprise, security, sig, caiq, vsa, vendor-assessment, b2b-sales, compliance, trust]
---

# security-questionnaire-responder

## Purpose

Enterprise buyers gate every B2B purchase behind a security review. The artifact is a
questionnaire — SIG, CAIQ, a VSA, or a buyer's own spreadsheet — with 50–400 questions you
will answer **again and again**, slightly reworded, on every deal. This skill turns that
recurring grind into a maintained **answer library**: each question maps to a reusable answer,
each answer maps to a verifiable evidence artifact, and each answer carries a confidence score
so the risky ones get human eyes before they reach the buyer.

The discipline mirrors `rfp-responder`'s hard rule: **never invent a control you don't have.**
A "no" with a documented compensating control and a roadmap date wins more enterprise trust
than a fabricated "yes" that collapses under a follow-up call or a later audit.

## When to use

- A prospect's procurement or security team sends a SIG / CAIQ / VSA / custom questionnaire
- You're answering the same security questions for the third time and want a reusable library
- You need to know which answers are *defensible* (evidence exists) vs *aspirational* (no proof)
- A buyer's question implies a control you don't have and you need a compensating-control answer
- You want a single source of truth so two deals never get contradictory answers

**Do not use for:**

- Pursuit strategy, win-themes, bid / no-bid, proof-point-to-requirement matrix → `rfp-responder`
- Redlining the MSA / DPA / security exhibit after the questionnaire passes → `general-counsel-advisor`
- Actually *implementing* the controls or earning the cert → `soc2`, `iso-27001`, `gdpr`, `hipaa`, `pci-dss`
- Standing up SSO / SCIM / audit logs the buyer is asking about → `workos-enterprise-auth`

## Workflow

### Step 1 — Classify the questionnaire and triage scope

Identify the format (SIG Lite ≈ 125 Q, SIG Core ≈ 850 Q, CAIQ ≈ 261 Q across 17 CCM domains,
VSA, or custom). Group questions by domain: access control, encryption, SDLC, incident response,
business continuity, data privacy, sub-processors, physical/cloud, vendor management. Triage:
which domains you can answer from the library, which need a fresh answer, which expose a real gap.

### Step 2 — Answer from the library first

For each question, pull the canonical answer from your answer library (see structure below). Most
"new" questions are reworded versions of ones you've answered. Match on **control intent**, not
wording — "Do you encrypt data at rest?" / "Is stored customer data encrypted?" / "Describe your
data-at-rest protection" are one library entry.

### Step 3 — Map every answer to evidence

No answer ships without an evidence pointer. Acceptable evidence: a policy doc, a SOC 2 report
section, an architecture note, a config screenshot, a pen-test summary, a sub-processor list, a
DPA. Pull the substantive controls from the vendored compliance skills:
- SOC 2 Trust Services Criteria & evidence types → `soc2`
- ISO 27001 Annex A controls & SoA → `iso-27001`
- GDPR data-handling, DPAs, privacy notices → `gdpr`
- HIPAA safeguards & BAAs → `hipaa`
- PCI DSS requirements & CDE scoping → `pci-dss`
- SSO/SAML, SCIM provisioning, audit logs the buyer asks about → `workos-enterprise-auth`

If no evidence exists, the answer is **not** "yes." It is a gap (Step 5).

### Step 4 — Score confidence and gate for review

Tag every answer:
- **HIGH** — control exists, evidence current, wording matches a prior buyer-accepted answer. Ships.
- **MEDIUM** — control exists but evidence is stale, partial, or the question is ambiguous. Human reviews before send.
- **LOW** — no clear control, no evidence, or the honest answer is "no/partial." Human writes the answer; never auto-fill.

The gate is the safety mechanism. An unattended pipeline that auto-answers a security
questionnaire is how a "yes" you can't back up ends up in a signed contract.

### Step 5 — Handle gaps honestly

For a control you don't have, the answer pattern is: **(a)** state the current state plainly,
**(b)** name the compensating control that reduces the risk today, **(c)** give a roadmap date if
it's planned. Example: "We do not yet hold SOC 2 Type II. We follow the AICPA Trust Services
Criteria as operating practice (see `soc2`), enforce SSO + audit logging, and have a Type II
observation window beginning Q3." Buyers accept honest gaps with mitigation far more often than
they forgive a discovered fabrication.

### Step 6 — Capture answers back into the library

Every questionnaire answered improves the next one. New questions, buyer-accepted phrasings, and
freshly created evidence get written back to the library with a `last_reviewed` date.

## Answer library structure

Keep one file per control area (or a single sheet). Each entry:

```
- question_intent: "data at rest encryption"
  canonical_answer: "All customer data is encrypted at rest with AES-256 ..."
  evidence: ["policies/encryption.md", "soc2 CC6.1", "architecture/storage.md"]
  confidence: HIGH
  last_reviewed: 2026-06-01
  notes: "buyer-accepted phrasing from Acme deal"
```

Match incoming questions to `question_intent`; reuse `canonical_answer`; re-verify `evidence`
isn't stale; downgrade confidence and flag if `last_reviewed` is older than your refresh window.

## Anti-patterns

- **Fabricating a "yes."** The cardinal sin. A claimed control with no evidence fails the buyer's
  follow-up call, voids trust, and can become a contractual misrepresentation. Surface the gap instead.
- **Auto-sending without the confidence gate.** MEDIUM/LOW answers must be human-reviewed. Speed
  is the goal; unreviewed risk is not.
- **Contradicting a prior answer.** Two deals, two different answers to the same question = a red
  flag the buyer's security team will catch. The library is the single source of truth.
- **Stale evidence.** A SOC 2 report from two windows ago, or a policy doc nobody has opened since
  the last audit, is not current evidence. Track `last_reviewed`.
- **Over-disclosing.** Answer what's asked with what's verifiable. Volunteering architecture detail
  beyond the question widens your attack surface in the buyer's records for no win.
- **Treating it as prose.** Security reviewers score against a rubric. Answer in their format, in
  their order — the same discipline `rfp-responder` applies to RFPs.

## Distinct from

- **`rfp-responder`** — pursuit-stage strategy: parse requirements, build a proof-point matrix,
  set win-themes, estimate winrate, decide bid/no-bid. It *can* structure a one-off security Q&A;
  this skill owns the **recurring** workflow and the maintained, evidence-mapped answer library.
- **`general-counsel-advisor`** — contract/MSA/DPA redline after the security review passes.
- **`soc2` / `iso-27001` / `gdpr` / `hipaa` / `pci-dss`** — the substantive controls and how to
  *earn* the posture. This skill *answers questions about* that posture and cites it as evidence.
- **`workos-enterprise-auth`** — how to *build* the SSO/SCIM/audit-log capabilities buyers ask about.

## Forcing questions

Walk these before sending anything back to the buyer:

1. **"For every 'yes', can you name the evidence artifact?"** If not, it's a MEDIUM or a gap, not a yes.
2. **"Does any answer contradict what we told a previous buyer?"** Reconcile against the library first.
3. **"Which answers are LOW confidence, and has a human written each one?"** No auto-filled LOW answers ship.
4. **"For each gap, did we state current-state + compensating control + roadmap date?"** Honest gap beats fake yes.
5. **"Is every cited evidence artifact current?"** Stale evidence is a finding waiting to happen.
6. **"Are we answering only what was asked?"** Over-disclosure is a quiet liability.
