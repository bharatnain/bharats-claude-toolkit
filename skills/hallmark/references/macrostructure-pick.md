# Design flow · Step 2 — Pick a macrostructure FIRST

Moved verbatim from `SKILL.md` § Design flow. Covers the macrostructure pick, the macrostructure / theme / nav + footer diversification rules, and the accountability line.

### 2. Pick a macrostructure FIRST

Before loading any visual ruleset, **read the slim index at [`references/macrostructures.md`](macrostructures.md) and pick one of the twenty-one named macrostructures.** The index is one-line-per-macro; pick a name, then **load ONLY that one per-macro file** from `references/macrostructures/` (e.g. `references/macrostructures/05-workbench.md`). Do not load the whole catalogue — that's ~37 KB of dead weight for a single pick. Each macrostructure is a complete page-shape — heading placement, body composition, divider language, button voice, image treatment, reveal — bundled as a single named choice. Picking one named macrostructure is faster and more varied than choosing six independent axes from scratch.

**Diversification rule (mandatory).** Before you pick:

1. Look in the target codebase for an existing `/* Hallmark · macrostructure: <name> · ... */` stamp at the top of any CSS file. If you find one, your pick must be a *different* macrostructure.
2. If you have produced any other Hallmark output for this user in this session, your pick must be a different macrostructure than the last one.
3. **The Specimen macrostructure (numbered left-margin labels + huge serif + asymmetric spans + typographic CTA) is no longer a default.** Reach for it only when the brief is explicitly editorial, foundry-adjacent, or the user has named it.

**Theme-diversification rule (mandatory).** Picking a different macrostructure isn't enough on its own — two consecutive Hallmark outputs can share a theme even if their structures differ, and the result reads as repetition. Two consecutive themes must differ on **at least one** of three axes:

- **Paper band** — dark (L < 30 %) / mid (30–85 %) / light (> 85 %), per the theme's `--color-paper` lightness
- **Display style** — high-contrast-serif (Specimen, Studio, Atelier) / roman-serif (Newsprint) / classical-serif (Lumen — Instrument Serif, upright; verb landmark via accent + underline) / geometric-sans (Manifesto) / grotesk-sans (Cobalt — Space Grotesk, mono-paired) / rounded-sans (Hum — Plus Jakarta Sans, warm humanist) / mono (Terminal) / display-condensed (Sport — roman) / display-heavy (Brutal, Carnival) / risograph-bold (Riso). All display is roman — italic headers are banned globally.
- **Accent hue** — warm (red / orange / amber: 10–60°) / cool (blue / indigo / cyan: 200–300°) / neutral (no chromatic accent) / chromatic-other (green: Studio · leaf-green: Garden · phosphor: Terminal)

If the previous output was Specimen (light · high-contrast-serif · warm), the next can be Studio (light · high-contrast-serif · chromatic-green) — the *accent hue* differs. But the next can't be Newsprint (light · roman-serif · warm) which only differs on display style and shares both paper band and accent — pick a more distant theme.

The per-theme axis values live as comments at the top of each theme's tokens block in `site/css/tokens.css` (upstream repo, github.com/Nutlope/hallmark; the vendored theme files under [`references/themes/`](themes/) carry the same axis values). When in doubt, name your candidate theme out loud and identify its three axis values; if two of three match the previous output, redirect.

**State your pick.** Before writing any code, say "Macrostructure: <name>. Theme: <name>. Differs from the last on: <axes>." in plain text. This is a deliberate accountability step — picking on the page (not in your head) prevents the default-attractor sameness that kept the skill emitting Specimen output.

If the brief is genuinely vague (no theme, no tone), do **not** default. Offer the user three macrostructures from *categorically different* groups (e.g. one grid-led like Bento, one document-led like Long Document, one poster-led like Manifesto). Three concrete choices, not seven abstract tones.

The macrostructure picks five of the six structural axes for you; you only need to pick the reveal yourself. The deeper axis catalogue is still in [`references/structure.md`](structure.md) when you need to deviate from the macrostructure's defaults.

**Pick a nav archetype (N1a–N13) and a footer archetype (Ft1–Ft8) at this step.** They are not optional chrome; they are part of the page's structural fingerprint. Read the slim index at [`references/component-cookbook.md`](component-cookbook.md) and the routing tables at its bottom — the genre's default plus the acceptable alternates. The nav catalogue is **fourteen archetypes**: N1a (minimal 2-link), N1b (canonical SaaS three-section), N2 (floating chip), N3 (side-rail), N4 (hidden ⌘K), N5 (floating pill), N6 (masthead), N7 (brutal slab), N8 (terminal), N9 (edge-aligned), N10 (scroll-morph), N11 (mega-menu), N12 (banner + retract), N13 (inline ⌘K-pill). Then **load ONLY the picked archetype files** from `references/components/`. A typical build loads 5–7 archetype files total. State both picks alongside the macrostructure: *"Macrostructure: Marquee Hero. Nav: N5 Floating pill. Footer: Ft5 Statement. Theme: Bloom."*

**Default away from N1a and Ft3.** N1a (wordmark + a couple inline links + button-right) and Ft3 (4 columns of links + social row + tiny copyright) are the most-recognised AI fingerprints. For a real product nav reach for N1b / N5 / N11 / N13 by default; reach for N1a only when the page genuinely has 2 destinations. Reach for Ft3 only on a genuine docs root or hub.

**Diversification extends to nav + footer — and is the single most-violated rule in practice.** Across consecutive Hallmark runs in the same project session (per `.hallmark/log.json`) **and across multiple test builds of the same theme**, no two outputs may share the same nav archetype OR the same footer archetype. **Before writing any nav markup, state one line out loud:** *"Previous nav: <X>. This build: <Y>, because <reason>."* The failure mode this prevents: reaching for the genre *default* on every build, so eight builds ship two navs. A theme with four test builds must show four different navs (e.g. Hum across Curio/Sprout/Tally/Mixtape: N5 → N1b → N12 → N13). Rotate deliberately through the routing table's "Acceptable also" column. The nav and footer picks are recorded in the macrostructure stamp at Step 6.
