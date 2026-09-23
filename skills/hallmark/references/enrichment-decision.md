# Design flow · Step 4 — Decide on hero enrichment

Moved verbatim from `SKILL.md` § Design flow. The per-build enrichment decision; the archetype catalogue itself lives in [hero-enrichment.md](hero-enrichment.md).

### 4. Decide on hero enrichment

Most pages don't need it. The strongest hero is often a typographic one. **Reach for [`hero-enrichment.md`](hero-enrichment.md) only when the brief points there** — a SaaS / dev-tool brief wants a demo video or mockup; a bakery / café / atelier brief wants a hand-built illustration; a manifesto wants nothing.

**First — does the brief need imagery at all?** Run the image-need table at [`hero-enrichment.md` § Image-need detection](hero-enrichment.md). Default is typography-only. If the brief signals "needs photographic content" (e-commerce, team, food, travel) AND the user hasn't supplied real assets, use the placeholder strategy in [`assets.md` § Placeholder strategy](assets.md). If the brief allows non-photographic imagery (SaaS landing, manifesto, agency splash, editorial-led), prefer the [`imagery-kit.md`](imagery-kit.md) over photo placeholders. **Never ship invented stock photos as if they were the final design.**

Eyeball the brief or ask one short question. State the decision in one sentence (e.g., *"Enrichment: E1 Clipped-Edge Demo Video, Tier-A CSS-art mockup."* or *"Enrichment: none — typography only."*). The decision goes into the macrostructure stamp at Step 6.

**The enrichment hierarchy is non-negotiable.** Reach for the highest tier you can ship: typography only → Tier A pure CSS art → Tier B hand-built SVG → Tier C generated still (Nanobanana / Recraft) → Tier D library + customisation → **Tier E Lottie is last resort**, only for complex character motion that hand-build can't reach. Reaching for Lottie when CSS would have built it is the new tell.

When an enrichment archetype requires construction, also load [`custom-craft.md`](custom-craft.md). When it requires an external asset, load [`assets.md`](assets.md).
