---
name: hallmark
description: "Anti-AI-slop design review and design-DNA extraction. Use ONLY when the user invokes Hallmark by name, asks whether a design 'looks AI-generated' or wants an anti-slop / slop-test audit of an existing page, or asks to extract/study the design DNA of a site from a screenshot or URL (e.g. 'make it look like stripe.com'). Do NOT use for general 'build an app/landing page' or redesign requests — those are handled by the frontend-design and ui-ux-pro-max plugins."
version: 1.1.0
---

# Hallmark

A design skill for AI coding assistants. Makes the UIs they generate look made, not generated.

Hallmark is opinionated, short, and boring on purpose. It encodes a tight set of rules — drawn from the consensus of the anti-AI-slop design field (Anthropic's frontend-design skill, the Claude cookbook on frontend aesthetics, and the 2026 "tactile rebellion" movement) — and refuses to let the model fall back to the defaults every LLM was trained on.

The differentiator: Hallmark insists on **structural variety**, not just visual variety. Two pages by Hallmark for two different briefs should not share the same hero → 3-feature → CTA → footer rhythm. They should feel like different sites, not different colour-swaps of the same template. See [`references/structure.md`](references/structure.md).

**Powered by Together AI.**

---

## How to use this skill

Hallmark has one default behaviour and three explicit verbs.

| Invocation | What it does |
| --- | --- |
| *(default)* | The user asked you to design or build something new. Follow the **Design flow** below. |
| `hallmark audit <target>` | Read the target, score it against the anti-pattern list, return a ranked punch list. **Do not edit.** |
| `hallmark redesign <target> [--mood <name>]` | Take the target's content and intent, then redesign the visual structure **inside the existing implementation boundaries unless the user explicitly confirms a full rebuild.** New section rhythm, new heading placement, new component voice. Preserve existing routes, component ownership, copy intent, brand, and information architecture; replace only the visual/interaction layer needed for the requested scope. |
| `hallmark study <screenshot \| URL>` | The user pasted or attached an image of a design they admire, **or** pasted a URL to a live page. Extract the **DNA** — macrostructure, archetypes, type-pairing, colour anchor — and produce a diagnosis report, then optionally rebuild the user's content using the extracted DNA **or** emit a portable `design.md` of the DNA. Detection is automatic: a URL (`http://` / `https://` prefix) routes to URL mode; anything else routes to image mode. **URL mode** reads the page's HTML and CSS via WebFetch — it can name exact fonts and exact colour values, but can't judge rhythm. After the diagnosis, the user has three follow-ups: build with the DNA (handoff to default), lock the DNA into a portable `design.md` (opt-in via "lock the DNA" / "give me a design.md"), or stop at the diagnosis. **Never copies pixels. Refuses template-marketplace URLs. Tighter refusal layer for `design.md` emission than for the diagnosis itself — URL-mode emission requires attestation that the source is the user's own or a public reference for their own brand. Falls back to asking for a screenshot if the URL is auth-walled, a JS-only SPA shell, or otherwise un-readable.** Load [`references/study.md`](references/study.md) before this verb runs. |

If the user types anything that does not clearly map to `audit`, `redesign`, or `study`, treat it as default. If the user attaches an image or pastes a URL without a verb prefix, ask: *"Should I `study` this (extract the DNA), or should I treat it as a reference for a fresh build?"*

**Implementation safety rail.** Hallmark is a design skill, not a license to bulldoze a codebase. In any existing project:
- Never delete production files, route trees, component directories, or an old website unless the user explicitly asks for deletion or approves a file-level plan that lists the deletions.
- Default to in-place edits of the named files, or additive new components/tokens that are wired through the existing route. If the redesign would require removing multiple components, stop and ask for confirmation first.
- Treat PDFs, README files, `.md` briefs, docs, transcripts, and pitch decks as reference material. Do **not** copy them word-for-word into the page unless the user explicitly says to use that text verbatim.
- Before editing, state the exact files you expect to modify/create/delete. Deletions require explicit confirmation.

The default Design flow always picks a theme. By default it picks one of the **21 named themes** — the *catalog* — and rotates among them per the diversification rule. There is also a quiet *custom* branch that constructs a one-off OKLCH palette + free-font pairing for the brief; the custom route fires **only when the brief carries a creative-intent signal** (the user names a brand colour, names a multi-attribute vibe the catalog can't carry, or explicitly asks for a custom theme). For vanilla briefs, the user never sees the words "catalog" or "custom" — the catalog runs silently. See Step 1 (signal detection) and Step 2.6 (dispatch); the protocol lives in [`references/custom-theme.md`](references/custom-theme.md).

---

## Disciplines that hold across every verb

Six disciplines apply to default Design, `audit`, `redesign`, `study`, and component-scope alike — **pre-emit self-critique** (six axes, anything < 3 revises), **honest copy** (no invented metrics, logos, or testimonials), **locked tokens** (every colour and `font-family` references a named token), **re-drawn chrome forbidden**, **mobile responsiveness verified at 320 / 375 / 414 / 768 px**, and **no italic headers**. The full text of each discipline, with the slop-test gate numbers it maps to, is in [references/disciplines.md](references/disciplines.md) — read it before emitting any output.

---

## When the brief is a component, not a page

Before entering the full Design flow, **check scope**. If the brief names a single UI element (button, input, card, modal, dropdown, …), is short (≤ 30 words) and refers to one element, targets a single component file, or says *"just the X"* — and at least two of those fire — run the Component-scope flow in [references/component-scope.md](references/component-scope.md) instead. It keeps pre-flight, genre, theme route, and the 2+1 font discipline; enforces all 8 interactive states; skips macrostructure, nav/footer, hero enrichment, preview, and project memory; and emits the component plus an 8-state demo wrapper with a `component:` stamp. If ambiguous, ask once and default to component.

---

## Design flow (default)

### 0. Pre-flight scan

If the project already has code, **read it before asking the user anything** — `design.md` (a locked system that overrides everything), font stack, palette, microinteraction stance, spacing scale, framework — and emit the *Pre-flight findings* block with file:line citations, cached in `.hallmark/preflight.json`. See [references/preflight.md](references/preflight.md) for the signal sources, output format, persistence rules, and edge cases (`design.md` found / safety, no signals, conflicts, user opt-out).

### 1. Design-context gate

**Always ask** for audience, use case, and tone — once, in one message, with a *"go ahead"* opt-out — then settle the **genre** (editorial default · modern-minimal · atmospheric · playful) and detect whether the brief carries a **custom-theme signal**; otherwise the catalog runs silently. If the user opts out, infer all three and **state the inferences in one sentence**. See [references/design-context-gate.md](references/design-context-gate.md) for the prompt text, genre signals, the theme-route signals, and the inference protocol.

### 2. Pick a macrostructure FIRST

Read the slim index at [references/macrostructures.md](references/macrostructures.md), pick **one** of the 21 macrostructures, and load only that per-macro file. Apply the mandatory diversification rules — macrostructure differs from the last stamp / session output; theme differs from the last on at least one of paper band · display style · accent hue; nav (N1a–N13) and footer (Ft1–Ft8) archetypes differ from the previous build — and **state the picks in plain text** before writing code. See [references/macrostructure-pick.md](references/macrostructure-pick.md) for the full rules, the axis definitions, and the nav/footer defaults to avoid.

### 2.5. Check project memory

If `.hallmark/log.json` exists, **read it before picking**: the macrostructure must not match any of the last three entries, the theme must differ from the last on one axis, and the enrichment archetype should not repeat. State the rotation in plain text before picking. See [references/project-memory.md](references/project-memory.md) for the schema, the rotation-block format, and the three sample shapes.

### 2.6. Theme route — studied-DNA, catalog, or custom

Dispatch on what is already true: a prior `study` diagnosis the user wants built → **studied-DNA** (diversification suspended); the user named custom → load [references/custom-theme.md](references/custom-theme.md) (tuned or bespoke depth); otherwise → **catalog**, silently, per the diversification rule. Custom themes obey every colour / typography / anti-pattern rule and all 58 gates. See [references/theme-route.md](references/theme-route.md) for the four conditions and the custom-branch constraints.

### 3. Load the visual ruleset

**Over-eager loading is the largest avoidable cost of running Hallmark.** Load by the schedule below; the full rationale and rules are in [references/loading-map.md](references/loading-map.md).

| When | Load |
| --- | --- |
| Always (eager) | the genre file picked in Step 1 — [genres/editorial.md](references/genres/editorial.md) · [modern-minimal](references/genres/modern-minimal.md) · [atmospheric](references/genres/atmospheric.md) · [playful](references/genres/playful.md); plus [themes/<theme>.md](references/themes/) if one exists for the catalog theme picked in Step 2.6 |
| Index, then pick | [macrostructures.md](references/macrostructures.md) → ONLY `macrostructures/<NN-slug>.md` for the pick; [component-cookbook.md](references/component-cookbook.md) → ONLY the picked `components/<code>-<slug>.md` files (5–7 per build) |
| Every build | [typography.md](references/typography.md) · [color.md](references/color.md) · [layout-and-space.md](references/layout-and-space.md) · [motion.md](references/motion.md) · [copy.md](references/copy.md) · [anti-patterns.md](references/anti-patterns.md) |
| Only when needed | [microinteractions.md](references/microinteractions.md) (any interactive element) · [interaction-and-states.md](references/interaction-and-states.md) (stateful UI) · [responsive.md](references/responsive.md) (mobile in scope) · [structure.md](references/structure.md) (deviating from a macrostructure) · [hero-enrichment.md](references/hero-enrichment.md) (image-need check = YES) · [custom-craft.md](references/custom-craft.md) · [assets.md](references/assets.md) · [imagery-kit.md](references/imagery-kit.md) · [custom-theme.md](references/custom-theme.md) (custom route) · [design-md.md](references/design-md.md) (lock request) · [preview-examples.md](references/preview-examples.md) |
| At the end | [slop-test.md](references/slop-test.md) (Step 7 only, never earlier) · [contract.md](references/contract.md) (handoff) · [export-formats.md](references/export-formats.md) (`design.md` projects only) |
| Per verb | [verbs/audit.md](references/verbs/audit.md) · [verbs/redesign.md](references/verbs/redesign.md) · [verbs/study.md](references/verbs/study.md) + [study.md](references/study.md) |

### 4. Decide on hero enrichment

Most pages don't need it — default is typography-only. Run the image-need check, state the decision in one sentence, and respect the enrichment hierarchy (typography → CSS art → hand-built SVG → generated still → library → Lottie last). See [references/enrichment-decision.md](references/enrichment-decision.md) for the decision procedure and the placeholder / imagery-kit rules.

### 5. Preview

Before emitting any code, output the **Hallmark preview block** — six required Markdown bullets (Macrostructure · Theme · Enrichment · Sections · Motion · Slop test), an optional Diversification bullet, and the quiet `lock the system` CTA line. Re-emit it if a Step 7 gate fails. See [references/preview-block.md](references/preview-block.md) for the exact format and per-bullet rules.

### 6. Build

Emit code that satisfies the tone and structural fingerprint, following every rule in [references/build-rules.md](references/build-rules.md) — headline size by copy length, section tags default OFF, OKLCH tokens at `:root`, all eight interactive states, `transform` / `opacity` motion only, an instant `:focus-visible` ring, plus the four hard contract items: **the macrostructure stamp**, **the `.hallmark/log.json` append**, **never clobbering an existing global stylesheet**, and **always emitting `tokens.css`**.

### 7. The slop test

Before handing back, run the output through the 58-gate slop test in [`references/slop-test.md`](references/slop-test.md). Every answer must be **no**. Load that file at this step (not earlier — it isn't needed until handoff). The active genre matters: some gates are universal, some are genre-scoped (atmospheric loosens the radial-bloom gate; modern-minimal loosens the zero-chroma neutral gate; etc.). The full per-genre overrides are listed inline in `slop-test.md`.

Run the slop test BEFORE writing the Slop test row in the Step 5 preview block — that row reflects the actual outcome of this step.

If any gate fails, fix it. Do not ship slop.

---

## `hallmark audit`

Load [`references/verbs/audit.md`](references/verbs/audit.md) and follow it.

---

## `hallmark redesign`

Load [`references/verbs/redesign.md`](references/verbs/redesign.md) and follow it.

---

## `hallmark study`

The user supplied a screenshot or a URL of a design they admire. Extract the **DNA** — structure, not pixels — produce a diagnosis report, then branch on the user's answer (build with the DNA · `lock the DNA` into a `design.md` · stop). Load [references/verbs/study.md](references/verbs/study.md) (source-mode detection, pipeline, output contract, limits) **and** [references/study.md](references/study.md) (extraction protocol, schemas, refusal heuristics) before this verb runs.

---

## Output contract & scope

Load [`references/contract.md`](references/contract.md) once, at handoff time, for the full output contract and scope-of-skill rules.
