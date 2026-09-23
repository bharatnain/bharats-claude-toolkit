# Design flow · Step 3 — Load the visual ruleset

Moved verbatim from `SKILL.md` § Design flow. The full loading discipline — what to load eagerly, index-then-pick, per build, conditionally, at the end, per verb, and never.

### 3. Load the visual ruleset

The non-negotiables live in [`references/`](). **Be precise about what to load when. Discipline matters — over-eager loading is the largest avoidable cost of running Hallmark.**

**Always-load (eager — 1–2 files):**
- The genre file picked in Step 1 — [`genres/editorial.md`](genres/editorial.md), [`genres/modern-minimal.md`](genres/modern-minimal.md), [`genres/atmospheric.md`](genres/atmospheric.md), or [`genres/playful.md`](genres/playful.md). Scopes everything downstream.
- **If `references/themes/<theme>.md` exists for the catalog theme picked in Step 2.6, load it eagerly.** Opt-in per-theme spec — carries signature moves, macrostructure affinity / rejection, voice fixtures, and anti-patterns that the tokens block cannot encode. Most themes have no spec file; the load is a silent no-op when absent. Studied-DNA and custom routes skip this load.

**Index-then-pick (read the slim index, then load only the picks):**
- [`macrostructures.md`](macrostructures.md) — slim index of the 21 macros. Pick one name from the index, then load ONLY `references/macrostructures/<NN-slug>.md` for that pick. **Never load the whole index plus more than one per-macro file in a single build.** ~30 lines per per-macro file vs. 660 lines for the old monolith.
- [`component-cookbook.md`](component-cookbook.md) — slim index of 50 component archetypes (9 heroes, 5 section heads, 6 features, 4 CTAs, 4 testimonials, 8 footers, 14 navs) + the nav + footer routing tables at the bottom. Pick your archetype codes (H#, S#, F#, C#, T#, Ft#, N#) from the index, then load ONLY the matching `references/components/<code>-<slug>.md` files. A typical build loads 5–7 archetype files. **Loading the cookbook end-to-end or pre-loading more than one archetype per category is the single biggest token waste in the skill — don't.**

**Load-per-build (universal rules — load every build):**
- [`typography.md`](typography.md) — fonts, scale, pairing, weights, measure, hero headline sizing
- [`color.md`](color.md) — OKLCH, palette construction, accent discipline
- [`layout-and-space.md`](layout-and-space.md) — 4 pt scale, grid-breaks, asymmetry, depth
- [`motion.md`](motion.md) — durations, easings, what to animate, reduced-motion
- [`copy.md`](copy.md) — verbs, labels, error structure, link text
- [`anti-patterns.md`](anti-patterns.md) — the named tells you must not emit

**Load-conditionally (only when the page actually needs it — be honest, do not pre-load "for safety"):**
- [`microinteractions.md`](microinteractions.md) — load whenever the output has *any* interactive element (buttons, inputs, modals, tabs, dropdowns, toasts, drag handles, copy buttons). That is most pages.
- [`interaction-and-states.md`](interaction-and-states.md) — load when the page has stateful UI (forms, command palettes, optimistic updates).
- [`responsive.md`](responsive.md) — load when mobile is in scope.
- [`structure.md`](structure.md) — load only when deviating from a named macrostructure.
- [`hero-enrichment.md`](hero-enrichment.md) — **do NOT load at Step 4 unless the image-need check in the next paragraph returns YES.** Most builds are typography-only and never touch this file. The decision is one quick read of the brief, not a defensive auto-load.
- [`custom-craft.md`](custom-craft.md) — load only when an enrichment archetype requires construction (CSS art, SVG, declarative animation, etc.).
- [`assets.md`](assets.md) — load only when an enrichment archetype needs an external asset (icons, illustration, photography, Lottie).
- [`custom-theme.md`](custom-theme.md) — load only when Step 2.6 routes to custom. The full custom branch (palette construction, font pairing, axis computation) lives there; SKILL.md only carries the dispatch.
- [`design-md.md`](design-md.md) — load only when the user explicitly asks Hallmark to lock the system into a portable file (phrases: *"lock the system"*, *"give me a design.md"*, *"make this portable"*, etc.). Opt-in; never fires on a vanilla build.
- [`preview-examples.md`](preview-examples.md) — load only if you need a worked example of the Step 5 preview block format. The bullet list in Step 5 itself is normally enough; reach for the file only when picking unusual macrostructures / custom themes.

**Load-at-the-end (Step 7 only):**
- [`slop-test.md`](slop-test.md) — **strictly Step 7, after Build.** The 58 gates are a post-emit check, not a pre-emit reference. Pre-loading slop-test.md costs ~7K tokens for nothing — the gates inform fixes, not generation. If a gate fails at Step 7, fix and re-test; do not consult the file earlier "to know what to avoid" — that's what `anti-patterns.md` is for.
- [`contract.md`](contract.md) — load at handoff time for output-contract + scope rules.
- [`export-formats.md`](export-formats.md) — load at Step 6 only when the project warrants multi-format exports (i.e. has a `design.md`). Single-page builds emit `tokens.css` from the in-memory token state and don't need this file.

**Verb-specific:**
- [`verbs/audit.md`](verbs/audit.md), [`verbs/redesign.md`](verbs/redesign.md) — load only when that verb runs.
- [`study.md`](study.md) — load only when `hallmark study` runs.

**Human-only (do NOT auto-load):**
- `docs/recipes.md` in the upstream repo (github.com/Nutlope/hallmark) — eight worked briefs for human readers.
- `docs/study-examples.md` in the upstream repo — three worked DNA-extractions for human readers.
