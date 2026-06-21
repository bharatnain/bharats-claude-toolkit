# bharats-claude-toolkit

My personal Claude Code setup, packaged as a **plugin + marketplace** so I can pull it into
any codebase on any machine with one command — and pull *more* on demand, mid-project.

The design goal: **I never have to remember what I have.** Skills load lazily by their
description, so I just work and Claude reaches for the right one. The only thing I decide up
front is what sits in my *always-on* index vs. what stays *one command away*.

---

## How it's structured (3 tiers)

| Tier | What | How it's wired |
|---|---|---|
| **Always-on** | This plugin + a few best-in-class external plugins, enabled in every directory | `enabledPlugins` in user-global `~/.claude/settings.json` |
| **On-demand** | The ECC firehose + superpowers — registered but *not* enabled | `extraKnownMarketplaces`; install when relevant |
| **Vendored** | Curated skills copied *into* this plugin (so it's self-contained) | `skills/` and `agents/` in this repo |

**Always-on plugins**
- `bharats-claude-toolkit` — this repo (vendored skills + agents below)
- `frontend-design` — Anthropic (`claude-plugins-official`): production-grade UI taste
- `ui-ux-pro-max` — design intelligence: 67 styles / 161 palettes / 57 font pairings
- `web-quality-skills` — Addy Osmani: accessibility (WCAG 2.2), performance, Core Web Vitals, SEO

**On-demand (registered, install when needed)**
- `ecc@ecc` — the full 271-skill ECC collection
- `superpowers@superpowers-marketplace`, `elements-of-style@superpowers-marketplace` — obra

---

## Bootstrap a new machine

**Option A — committed settings (recommended, reproducible).**
Merge the contents of [`settings.json`](settings.json) into your user-global
`~/.claude/settings.json` (it carries both `extraKnownMarketplaces` and `enabledPlugins`).
Open Claude Code in any directory and the always-on tier is live; `ecc`/`superpowers` are
registered and one command away.

**Option B — slash commands (manual).**
```text
# register marketplaces
/plugin marketplace add bharatnain/bharats-claude-toolkit
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin marketplace add addyosmani/web-quality-skills
/plugin marketplace add affaan-m/ecc
/plugin marketplace add obra/superpowers-marketplace

# enable the always-on tier
/plugin install bharats-claude-toolkit@bharats-claude-toolkit-dev
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
/plugin install web-quality-skills@addy-web-quality-skills
/plugin install frontend-design@claude-plugins-official
```

---

## Pull more, mid-project (cheatsheet)

```text
/plugin install ecc@ecc                              # the 271-skill firehose
/plugin install superpowers@superpowers-marketplace  # brainstorm→plan→execute methodology
/plugin install elements-of-style@superpowers-marketplace
/reload-plugins                                       # make them live in THIS session, no restart
```
Then just work — the newly available skills auto-trigger by description.
(`/reload-plugins` may warn about prompt-cache invalidation if a plugin adds MCP servers.)

To cherry-pick a single ECC skill permanently instead of installing all of ECC, copy its
folder from `github.com/affaan-m/ecc/skills/<name>/` into this repo's `skills/`.

---

## What's vendored in this plugin

**Workflow & engineering** — `tdd-workflow`, `verification-loop`, `codebase-onboarding`,
`repo-scan`, `production-audit`, `agentic-engineering`, `research-ops`

**Architecture & planning (agents)** — `architect`, `planner`, `code-architect`, `spec-miner`

**Python & data** — `python-patterns`, `python-testing`, `fastapi-patterns`, `postgres-patterns`

**Frontend & React** — `react-patterns`, `react-best-practices` (Vercel)

**Design & UI polish** — `design-system`, `make-interfaces-feel-better`, `motion-foundations`,
`motion-patterns`, `theme-factory`, `brand-guidelines`

**Copywriting & content** — `copywriting`, `copy-editing`, `content-strategy`, `content-engine`,
`article-writing`, `brand-voice`, `onboarding`

**UX writing** — `ux-writing`

**SEO** — `seo-audit`, `ai-seo`

> **Not duplicated:** `code-review`, `security-review`, `deep-research`, `verify`, and `simplify`
> ship natively with Claude Code — use those directly.

ECC-sourced skills have been **de-branded** (ECC-specific defaults, tool references, and
personal-voice samples removed). Attribution and licenses for everything vendored are in
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

---

## Maintaining vendored skills

Vendored skills are point-in-time snapshots. To refresh one, re-copy its directory from the
upstream repo and re-apply the de-branding (drop `metadata.origin: ECC`, strip ECC tool/skill
cross-references). For frequently-updated upstreams (Vercel, Addy, Anthropic, ui-ux-pro-max)
prefer the *enabled-plugin* tier over vendoring so they stay current automatically.

## Layout

```
bharats-claude-toolkit/
├── .claude-plugin/
│   ├── plugin.json          # this plugin's manifest
│   └── marketplace.json     # one-plugin marketplace (name: bharats-claude-toolkit-dev)
├── settings.json            # template to merge into ~/.claude/settings.json
├── skills/<name>/SKILL.md   # vendored skills
├── agents/<name>.md         # vendored agents
├── CLAUDE.md                # behavioral guidelines
├── THIRD_PARTY_NOTICES.md   # attribution + licenses
└── README.md
```
