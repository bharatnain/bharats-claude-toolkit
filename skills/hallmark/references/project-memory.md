# Design flow · Step 2.5 — Check project memory

Moved verbatim from `SKILL.md` § Design flow. Covers `.hallmark/log.json` — schema, how the last entries constrain the next pick, and the rotation block format.

### 2.5. Check project memory

If the project has a `.hallmark/log.json` file (created by previous Hallmark runs), **read it before** picking the macrostructure or theme. The schema is a JSON array, newest entry first:

```json
[
  { "date": "2026-04-30", "macrostructure": "Bento Grid",   "theme": "Coral",   "enrichment": "E1 clipped-edge",  "brief": "Tracejam · SaaS observability" },
  { "date": "2026-04-28", "macrostructure": "Long Document","theme": "Garden",  "enrichment": "E5 hand-built SVG", "brief": "Maple Street Bread · bakery" },
  { "date": "2026-04-25", "macrostructure": "Manifesto",    "theme": "Manifesto","enrichment": "none",            "brief": "Meridian · studio manifesto" }
]
```

Use the **last 3–5 entries** to inform diversification:
- Your macrostructure pick must not match any of the last three.
- Your theme pick must differ from the last on at least one axis (see the theme-diversification rule above).
- Your enrichment pick should not be the same enrichment archetype as the last (`E1 clipped` twice in a row reads as templated, even with different content).

If the file doesn't exist, this is the first Hallmark run for this project — no constraint, but **you'll create the file in Step 6**.

If the project has a CSS stamp but no `log.json`, infer one entry from the stamp and proceed.

**State the rotation in plain text before picking.** This is the user's accountability line for diversification — picking on the page (not in your head) is what keeps the skill from drifting back into Bento-Grid-by-default. The format:

> *"Last 5 builds: Bento Grid (Tracejam) · Bento Grid (Foundry) · Long Document (Maple) · Manifesto (Meridian) · Quote-Led (Tide). Bento Grid used 2 of 5 — picking from {Marquee Hero, Stat-Led, Workbench, Letter} this time. I'll go with Marquee Hero."*

Then the theme rotation, on the next line:

> *"Last 3 themes: Coral · Bloom · Riso. Picking from {Newsprint, Atelier, Studio, Garden} — Newsprint differs on display style and accent hue."*

**Three sample shapes** to imitate:

- **First-time** (no `log.json`, fresh project): no rotation block at all — just the macrostructure pick. *"This is the first Hallmark run for this project. Picking Long Document — fits the Coffeebox brief's editorial tone."*
- **Mature project** (5+ entries in `log.json`): the format above — frequency count, exclusion list, pick.
- **User overrode last run** ("use Bento Grid again, I want the same shape"): *"Last build was Bento Grid (you requested it). You've asked for it again — I'll pick different knob values. Knob deltas: tiles=8 (was 6), accent=full-bleed (was corner-only), spans=irregular (was even). Same archetype, different fingerprint."*

The rotation block keeps the user inside the discipline without making them read the rules. Skip it and the user starts thinking the diversification is theatre.
