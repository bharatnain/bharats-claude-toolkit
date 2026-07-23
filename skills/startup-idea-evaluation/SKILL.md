---
name: "startup-idea-evaluation"
description: "Runs any startup idea through a rigorous, YC-style evaluation gauntlet before the user commits time or money to it. Use when the user wants to evaluate, stress-test, or premortem a startup idea; compare multiple candidate ideas; check if an idea is venture-scale or a tarpit/wrapper; choose a business model for an idea; set initial pricing and a value metric; or assess whether an idea/company is fundable and seed-ready in 2026. Covers sequential evaluation gates (problem, why-now, TAM/SAM/SOM, 10x insight, moat, kill criteria, premortem), a business-model decision tree, a value-based pricing worksheet, and a fundraising-readiness checklist with SAFE dilution math. Not for competitor tracking programs (use `competitive-intel`) or ongoing pricing operations at an existing company (use `pricing`)."
license: MIT
metadata:
  version: 1.0.0
  author: Bharat Nain
  category: founder
  domain: startup-strategy
  updated: 2026-07-23
  frameworks: evaluation-gauntlet, business-model-picker, pricing-worksheet, fundraising-readiness
---

# Startup Idea Evaluation

A repeatable gauntlet for stress-testing startup ideas the way YC partners and angels do — so conviction is manufactured from evidence, not vibes. Killing an idea today costs nothing; killing it in year two costs your savings and two years of compounding.

## Keywords
startup idea evaluation, idea validation, stress test, premortem, kill criteria, founder-market fit, why now, TAM SAM SOM, market sizing, venture scale, tarpit idea, AI wrapper test, moat, business model selection, pricing strategy, value metric, willingness to pay, Van Westendorp, seed fundraising, SAFE dilution, pitch deck, fundability, YC evaluation

## Quick Start

Ask in natural language for the evaluation you need:

> "Run my startup idea through the gauntlet: [idea]" — full sequential stress test, gate by gate
> "Compare these two ideas: [A] vs [B]" — run both through gates 1–5 in parallel and score
> "Is this idea venture-scale?" — bottom-up TAM/SAM/SOM math + the $100M ARR check
> "Premortem this idea" — write its most plausible obituary and force-rank the cause of death
> "What business model fits this idea?" — decision tree + taxonomy comparison
> "What should I charge for this?" — value-based pricing worksheet with tiers
> "Am I ready to raise a seed round?" — 2026 readiness checklist + dilution math

When running an evaluation, work through the relevant reference file top to bottom, ask the user for missing inputs (segment, price hypothesis, evidence gathered so far), and give a verdict per gate: **pass / conditional pass / kill**, with the specific evidence that would change the answer.

## Framework 1: The Evaluation Gauntlet

Seven sequential gates, run in order — analysis picks the space, empiricism picks the idea, conviction arrives at the end:

1. **Problem & founder-market fit** — urgent, frequent, expensive pain; can you name 10 hair-on-fire users?
2. **Why now** — a recent, specific unlock (technology, cost, regulation, behavior) that implies a 12–36 month window
3. **Market size** — bottom-up TAM/SAM/SOM: customers × price, sliced honestly; does the best case clear ~$100M ARR?
4. **The 10x insight** — your unfair advantage and Thiel secret; 2x better loses to switching inertia
5. **Competition & moat** — tarpit graveyard check, the wrapper test, plausible eventual moat
6. **Kill criteria** — written in advance, so quitting is discipline instead of rationalization
7. **Premortem** — the past-tense obituary, force-ranked against the canonical causes of death

Each gate has questions, evidence thresholds, and red flags that kill. See `references/evaluation-gauntlet.md`.

## Framework 2: Business Model Picker

The business model is half the idea. A taxonomy comparison table (margins, sales motion, time to revenue, capital intensity, defensibility) across 16+ models — from seat SaaS and marketplaces to 2026 AI-native models (credits, outcome pricing, agents priced against labor budgets) — plus a 7-question decision tree that maps an idea's characteristics to a model. See `references/business-model-picker.md`.

## Framework 3: Pricing Worksheet

A six-step method to determine initial pricing before the product exists: hypothesize the value metric → quantify value for one segment → set the hypothesis price at 10–20% of value → test willingness to pay (Ramanujam's three questions, Van Westendorp) → package into three tiers → ship and revisit. Includes a worked example end to end. See `references/pricing-worksheet.md`.

## Framework 4: Fundraising Readiness

A seed-readiness checklist with 2026 metric bars by round (pre-seed → seed → Series A), a worked SAFE dilution example showing what stacking SAFEs actually does to founder ownership, and the canonical pitch structure (10-slide skeleton + 30-second and 2-minute versions). See `references/fundraising-readiness.md`.

---

## Deeper Reading

This skill is self-contained, but it distills a 12-document research library. For full sourcing, case studies, and the surrounding playbook, see `research/startup-business-models/` in this repo — start with `playbook.md`, then `01-idea-evaluation-and-conviction.md`, `02-business-model-taxonomy.md`, `03-pricing.md`, and `05-fundraising-mechanics-2026.md`.

## References
- `references/evaluation-gauntlet.md` — sequential stress-test gates with pass thresholds and kill signals
- `references/business-model-picker.md` — model taxonomy table + decision tree
- `references/pricing-worksheet.md` — step-by-step pricing determination with worked example
- `references/fundraising-readiness.md` — seed-readiness checklist, SAFE dilution math, pitch outline
