# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/), and versions map to the toolkit's phases.

## [Unreleased]

- **Added: `scripts/skill_usage.py`** — local skill-usage report from `~/.claude/projects` transcripts
  (invoked skills, never-invoked vendored skills by description size, idle plugins, `--prune-list`);
  a read-only stand-in for `/skill-doctor` when usage reports are unavailable. **Added:
  `scripts/set_eval_secret.sh`** — stores the `ANTHROPIC_API_KEY` repo secret for `plugin-eval.yml`
  via a hidden prompt piped to `gh secret set`.

## [0.9.0] - 2026-09-22

### 2026-09-22 — Backlog execution: full re-vendor wave, roster consolidation, agent-teams removal

- **Changed: re-synced 52 vendored skill directories against 8 upstream HEADs** (47 changed;
  article-writing, brand-voice, fal-ai-media, executive-mentor were already current; repo-scan
  kept at its previous content because upstream replaced it with an installer stub for an
  external tool). Local edits re-applied per skill — disambiguated descriptions kept verbatim,
  upstream-escaping links neutralized, branding and product-install instructions stripped: ecc
  (22 skills at `bf70150`, 4 ecc agents verified unchanged; 14 descriptions adopted upstream
  "Use when…" clauses; tdd-workflow gains test-runner detection and keeps the probity section;
  video-editing gains DaVinci Fusion preset bundles; eval-harness drops upstream's
  local-framework section that has no files here); marketingskills (18 skills
  at `5b2c000`; ad-creative 2.8.2, ads 2.3.2, ai-seo 2.5.0 format-volatility, onboarding/pricing/
  launch/PR/referrals/social gain new reference files; **partner-link audit** — zero
  Converly/Ploy/UTM content admitted, three non-partner vendor plugs neutralized); GRC v2.0.0
  (soc2, iso-27001, gdpr, hipaa, pci-dss — Sep-2026 regulatory currency: Uber Art. 22 fine, EDPB
  02/03-2026 drafts, HIPAA Security Rule NPRM slip, PCI FAQ 1331); workos-enterprise-auth 0.7.3
  (MCP-first, AuthKit setup); hallmark (Grid theme); executive-mentor, general-counsel-advisor
  (claude-for-legal contract-review references preserved byte-for-byte); churn-analysis 1.1.0
  (FM classification addendum), churn-rca (packaging); api-idempotency-keys. `THIRD_PARTY_SOURCES.json`
  SHAs now equal the vendored HEADs for every source.
- **Changed: plugin roster.** `superpowers` and `mattpocock-skills` are consumed from
  `claude-plugins-official` (SHA-pinned by Anthropic); their old marketplace keys are set to
  `false` and **`bootstrap.sh` now forces a repo-side `false` onto existing machines** (its merge
  was add-only, so disables never propagated), and the two marketplaces are dropped from
  `extraKnownMarketplaces` (`elements-of-style` needs `obra/superpowers-marketplace`
  re-added). Newly enabled: `claude-security`, `session-report`, `skill-creator`
  (`claude-plugins-official`). 29 plugins enabled. README Option B is now generated from
  `settings.json`.
- **Changed: supply chain.** Every external `extraKnownMarketplaces` entry is SHA-pinned
  (`ref` + `sha`); `scripts/check_upstream.py` reports marketplace pin drift next to vendored
  drift (weekly issue covers both); GitHub Actions pinned by commit SHA; beads installer pinned
  (`gastownhall/beads` v1.3.0, `BEADS_VERSION=1.3.0`); `docs/supply-chain.md` status updated.
- **Removed: experimental agent-teams gate wiring.** `TaskCreated` / `TaskCompleted` /
  `TeammateIdle` registrations dropped from `hooks/hooks.json` and `hooks/team_gate.py`
  (8 registrations remain), `docs/agent-teams-probe.md` deleted, README section and
  `team-orchestration` / `verification-loop` mentions removed. The events are still
  experimental upstream; re-add behind a verified probe if teams go GA.
- **Changed: hooks.** `MultiEdit` dropped from matchers and `secret_scan.py`; secret scanner
  gains OpenAI, npm, PyPI, Hugging Face, SendGrid, Twilio, GitLab, cloud service-account JSON
  and `aws_secret_access_key` patterns. `docs/hooks-security.md` §3 re-verified against
  Claude Code 2.1.280 (hook `if` field, MCP hooks after `/clear`, workspace trust).
- **Fixed: `scripts/release.py`** promotes the `[Unreleased]` block into the new version
  section instead of stranding it, no longer creates the tag before the release commit
  (tagging moved to the printed next commands), and its re-sync line matches the CHANGELOG.
- **Added: `evals/`** with a first `claude plugin eval` case (`claude-code-docs` must fire on
  a Claude Code capability question) and a manual-dispatch `plugin-eval.yml` workflow.
- **Changed: skill catalog.** 17 overlapping skill pairs disambiguated in their descriptions
  (lane + "not for X — use `sibling`"); `hallmark` SKILL.md split into `references/`
  (was 67 k chars) and its two remaining upstream-escaping links neutralized; `react-best-practices` frontmatter name aligned to its directory
  (validator allowlist removed); `code-migration` sample rows show `claude-sonnet-5`.
- **Changed: `team-orchestration`** limits re-verified (depth 3 via
  `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, 20 concurrent; the 200-per-session cap is no longer
  documented) and version qualifiers dropped. README notes superpowers 6.4.1's native
  `executing-plans` and `diagnosing-superpowers`.
- **Docs:** `docs/housekeeping-2026-09.md` rewritten as done/deferred with reasons;
  `THIRD_PARTY_NOTICES.md` "referenced but NOT vendored" list completed with licences.

### 2026-09-22 — Latest-model refresh (Opus 5.5 / Fable 5.1 / Sonnet 5) + housekeeping backlog

- **Changed: model defaults bumped to the current lineup.** `cost-aware-llm-pipeline` routes
  `claude-sonnet-5` / `claude-haiku-4-5` (was Sonnet 4.6 / dated Haiku pin); its pricing table is
  re-cached Sep 2026 with Sonnet 5 ($2/$10), Opus 5.5 ($4/$20) and Fable 5.1 ($10/$50); cache-minimum
  prose updated. `launch-your-agent` examples use `claude-opus-5-5` and the fast-mode model list is
  corrected (Opus 5.5 / Opus 5 / Opus 4.8). The three `references/claude-api/*.md` files are
  re-vendored from the `claude-api` skill bundled with Claude Code 2.1.280, with a dated freshness
  banner (Opus 5.5 GA 2026-09-22; Opus 4.1 retired 2026-08-05).
- **Changed: docs swept for Claude Code 2.1.280.** README tier table / bootstrap paragraph and
  THIRD_PARTY_NOTICES no longer describe `superpowers` as on-demand; README "other 25 plugins";
  `/toolkit` headline 26 plugins / 134 skills / 8 agents; `docs/hooks-security.md` counts eleven hook
  registrations; "Task tool" → "Agent tool" in `threat-model` and `context-budget`; version
  qualifier dropped in `verification-loop`. Agent-teams events verified still documented as
  experimental (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`); `agent-teams@claude-code-workflows`
  stays disabled (upstream still calls `TeamCreate`).
- **Changed: hygiene.** Dead `scripts/db-probe.sh` permission removed from `settings.json`;
  `.gitignore` covers `.claude/team-profile.json`, `__pycache__/`, `*.pyc`, `.pytest_cache/`.
  `THIRD_PARTY_SOURCES.json` `first_party` now lists `claude-code-docs`, `startup-idea-evaluation`,
  `team-orchestration`; upstream SHAs re-recorded for the 7 sources with no content drift in our
  vendored directories (16 of 22 sources had moved), with the manifest `_comment` noting the
  2026-09-22 re-record.
- **Added: `docs/housekeeping-2026-09.md`** — the ranked open backlog from the sweep (release 0.9.0
  cut + `release.py` Unreleased-insertion bug, GRC v2.0.0 re-vendor, agent-teams probe-or-remove
  decision, ecc drift policy, marketingskills/workos/hallmark re-pulls, secret-scan pattern refresh,
  `/skill-doctor` pruning, supply-chain pinning).

### 2026-08-07 — mattpocock-skills enabled by default; house skill-authoring standard

- **Enabled: `mattpocock-skills@mattpocock`** (github.com/mattpocock/skills, MIT, v1.2.3) —
  ~30 compact engineering/process skills: `grilling`/`grill-me`/`grill-with-docs`
  (frontier-driven design interviews), `domain-modeling` (CONTEXT.md ubiquitous language +
  ADRs), `wayfinder`/`triage`/`to-tickets` (tracker-abstracted planning — bind to beads via
  `/setup-matt-pocock-skills`), `diagnosing-bugs` (feedback-loop-first debugging), `teach`,
  `codebase-design`, `writing-for-agents`. Marketplace registered as `mattpocock` in
  `settings.json`; subscribe model chosen over vendoring (actively versioned upstream).
- **Changed: `tdd-workflow` description narrowed** to its plan-file-driven delivery scope, to
  avoid trigger overlap with the new plugin's general-purpose `tdd` discipline skill.
- **Docs: `writing-for-agents` adopted as the house standard** for authoring or adapting any
  SKILL.md in this repo (README "Authoring a new skill").

### 2026-08-03 — Upgrade wave: security pipeline, finance models, legal advisors, CMA, supply chain

- **Added: 18 vendored skills (116 → 134).**
  - *Security pipeline* (anthropics/defending-code-reference-harness, Apache-2.0): `threat-model`,
    `vuln-scan`, `vuln-triage`, `vuln-patch`, `dnr-hunt`, `dnr-respond` — the full
    THREAT_MODEL.md → VULN-FINDINGS.json → TRIAGE.json → PATCHES/ chain, with a shared
    `skills/_lib/checkpoint.py` helper (35 unit tests pass).
  - *Financial modeling* (anthropics/financial-services, Apache-2.0): `dcf-model`, `audit-xls`,
    `3-statement-model`, `comps-analysis`, `lbo-model` — hands-on spreadsheet construction and
    auditing; `cfo-advisor` keeps strategy scope and now cross-points at them.
  - *Legal/advisor* (anthropics/claude-for-legal, Apache-2.0): `advisor-profile` — cold-start
    interview that writes the shared `company-context.md` all C-suite advisors read; plus a
    contract-review deep-dive family (NDA/vendor/SaaS-MSA review, deal-debrief, playbook-monitor)
    vendored as `general-counsel-advisor` references.
  - *Claude Managed Agents* (anthropics/launch-your-agent, Apache-2.0): `launch-your-agent`,
    `agent-wrap-up`.
  - *Code migration* (anthropics/code-migration-kit-with-claude-code, Apache-2.0):
    `code-migration` — prompts, templates, dependency-map/queue/build scripts, fixtures.
  - *Design review* (Nutlope/hallmark, MIT): `hallmark` — anti-slop audits, slop-test,
    design-DNA extraction; scoped to explicit invocation so it never collides with
    `frontend-design`/`ui-ux-pro-max`.
  - *Supply chain* (anthropics/knowledge-work-plugins, Apache-2.0): `plugin-vetting` — LLM-judge
    review policy + verdict schema to vet third-party plugins/marketplaces BEFORE enabling;
    new `docs/supply-chain.md` documents the SHA-pinning adoption path.
- **Changed: plugin roster in `settings.json`.** Now enabled by default: `superpowers`,
  `security-guidance` + `plugin-dev` (claude-plugins-official), `differential-review` +
  `fp-check` (trailofbits-skills), `security-awareness` (trailofbits-skills-curated).
  Registered but NOT enabled: `probity`, `memsearch`, `openai-codex`, the remaining Trail of
  Bits plugins. `agent-teams@claude-code-workflows` is explicitly **disabled** — it calls the
  `TeamCreate`/`TeamDelete` tools removed in Claude Code v2.1.178.
- **Changed: orchestration docs swept for Claude Code v2.1.220.** `team-orchestration` spawns
  teammates via the Agent tool (implicit teams, background-by-default semantics, depth/concurrency
  caps); `verification-loop` hooks guidance now prefers `additionalContext` over fake blocking
  errors; `tdd-workflow` gains an "Automated Enforcement (probity)" section (MIT-attributed).
- **Changed: hooks hardened.** All four hook scripts get bounded 10 MiB stdin reads, PATH
  bootstrap, and a `CLAUDE_TOOLKIT_HOOKS=off` master switch doubling as a recursion guard;
  `bootstrap.sh` adopts byte-compare no-op writes (no backup churn); new `docs/hooks-security.md`.
- **Changed: Claude API references refreshed (Jul 2026).** `cost-aware-llm-pipeline` pricing
  and cache-minimum facts corrected, with current `models.md`/`model-migration.md`/
  `prompt-caching.md` vendored under its `references/claude-api/`.
- Attribution for everything above is in `THIRD_PARTY_NOTICES.md` / `THIRD_PARTY_SOURCES.json`;
  `SKILLS.md` catalog regenerated (134 skills, 8 agents).

- **Added: bootstrap installs a default global `CLAUDE.md`.** `bash scripts/bootstrap.sh` now
  copies this repo's [`CLAUDE.md`](CLAUDE.md) (Andrej Karpathy's four LLM-coding rules — Think
  Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution) to
  `~/.claude/CLAUDE.md`, so the rules apply in every project by default instead of only inside this
  repo. Non-destructive: it writes the file only when absent (byte-identical → reported no-op) and
  never clobbers a differing existing file unless `CLAUDE_FORCE_CLAUDE_MD` is set (which backs the
  existing file up first, mirroring the settings backup). Opt out with `CLAUDE_DEFAULT_CLAUDE_MD=off`;
  `CLAUDE_MD` overrides the destination for tests (like `CLAUDE_SETTINGS`).
- **Fixed: bootstrap wrote `enabledPlugins` as a JSON array, which current Claude Code reads as
  zero enabled plugins** — so `bash scripts/bootstrap.sh` never actually enabled the always-on
  tier and none of the vendored skills loaded. Verified on the desktop app's embedded Claude Code
  2.1.187: `Found 0 plugins (0 enabled, 0 disabled)` → 0 plugin skills. Claude Code expects an
  object map `{ "plugin@marketplace": true }`. `settings.json` now uses the object form, and the
  bootstrap merge writes/normalizes `enabledPlugins` as an object — migrating a legacy
  array-valued target and never overriding a user-set `false` (dest wins on collision).
- **Fixed: `scripts/bootstrap.sh` aborted under macOS's system bash 3.2** (`/bin/bash`). An
  apostrophe inside the `$( … <<'PY' … )` here-doc tripped bash 3.2's command-substitution lexer
  (`unexpected EOF while looking for matching '`). The here-doc comments are now apostrophe-free;
  `bash -n` passes under 3.2.
- **Added: beads (`bd`) is now the default task store.** `bootstrap.sh` auto-installs the `bd` CLI
  (non-blocking; opt out with `CLAUDE_BEADS=off`) and `settings.json` permits it (`Bash(bd:*)`). A
  new `SessionStart` hook (`hooks/beads_init.py`, matcher `startup`) runs `bd init`
  (`--skip-agents --skip-hooks`, so it never writes `CLAUDE.md`/`AGENTS.md` or installs git hooks)
  once per git repo, gitignores `.beads/`, and injects a directive to use beads — all fail-open and
  git-repo-only, with the native Task tools as the fallback.
- **Added: beads-backed workflows.** New flagship `workflows/beads-task.workflow.js` + pure helper
  `workflows/lib/beads.js` give workflows cross-session task memory: decompose a goal into
  acceptance-criteria beads issues under an epic, resume by `epicId` (closed issues skipped), and
  close each issue only when the quality-gate verdict is `pass`.
- **Fixed: `beads-contract.md` now matches the real bd 1.0.4 CLI** (`bd create` / `--acceptance` /
  `--deps` / `bd ready --exclude-type epic` / `bd close --reason`) — the previously documented
  `bd add` / `--depends-on` do not exist in current beads.
- **Re-sync:** `git pull && bash scripts/bootstrap.sh`, then fully quit and reopen Claude Code and
  start a new chat.

### Commits

- feat: execute Sep-2026 housekeeping backlog
- feat: Sep-2026 latest-model refresh + housekeeping backlog
- Merge pull request #7 from bharatnain/claude/evaluate-awesome-toolkit-ff3e40
- feat: enable mattpocock-skills by default; adopt writing-for-agents as authoring standard
- Merge pull request #6 from bharatnain/claude/evaluate-awesome-toolkit-ff3e40
- fix: neutralize hallmark upstream-escaping links; make --strict-yaml report parse errors
- feat: Aug-2026 ecosystem upgrade wave — 18 vendored skills, plugin enables, hooks hardening
- refactor: move research library to bharatnain/research repo
- feat(skills): startup-idea-evaluation gauntlet skill
- docs(research): playbook synthesis + library index
- docs(research): startup business-model evaluation library (12 deep dives)
- feat(bootstrap): install default global CLAUDE.md (Karpathy rules)
- feat(beads): default task store + beads-backed workflows
- Merge pull request #2 from bharatnain/fix/enabledplugins-object-format
- fix(bootstrap): load plugins reliably — enabledPlugins object + bash 3.2
- bootstrap: carry permissions.allow into user settings
- 0.8.1: fix duplicate-hooks load + validate_assets false positives
- **Re-sync:** `git pull && bash scripts/bootstrap.sh`, then fully quit and reopen Claude Code and start a new chat.

## [0.8.1] - 2026-06-24

- Removed the redundant `"hooks": "./hooks/hooks.json"` field from `.claude-plugin/plugin.json`.
  The standard `hooks/hooks.json` is loaded automatically, so the explicit reference caused a
  duplicate-hooks load error on `/doctor`. Hook behavior is unchanged.
- Fixed `scripts/validate_assets.py`: it ran a plain `node --check <file>` on `*.workflow.js`
  scripts, which always failed (5 false-positive errors) because those scripts use the Workflow
  runtime's top-level `return`/`await` + `export const meta` form and are not standalone modules.
  The W1 check now reproduces the runtime's wrap (imports hoisted, `meta` demoted, body wrapped in
  an async function) and checks the result as an ES module via stdin, while still catching genuine
  syntax errors. `validate_assets.py` is now clean (16 assets, 0 errors).
- **Re-sync:** `git pull && bash scripts/bootstrap.sh`, then `/reload-plugins` (or restart Claude Code).

## [0.8.0] - 2026-06-23 — Phase G: self-maintaining automation

- Added `scripts/check_upstream.py` (stdlib-only) — `git ls-remote`s every source in
  `THIRD_PARTY_SOURCES.json` and reports which vendored skills have drifted from their
  recorded upstream HEAD (`--format human|json`, never fails the build on drift).
- Added `scripts/doctor.py` plus the `/doctor` slash command — a health check over
  settings, plugins, marketplace, and optional tools that prints the exact inline fix
  for every ✗/⚠ line (`--format human|json`; exit 1 only on a critical failure).
- Added `scripts/validate_assets.py` (stdlib + `node --check`) — validates `agents/`,
  `commands/`, and `workflows/` frontmatter/meta, reusing `validate_skills.py`'s parser;
  same `--format text|github` and exit codes so it is CI-interchangeable.
- Added `scripts/release.py` — surgically bumps `plugin.json`, scaffolds this CHANGELOG
  section, optionally refreshes the manifest, and creates a local tag; it NEVER commits
  or pushes (`--bump <level>` / `--version X.Y.Z`, `--dry-run`).
- Added the CI workflows: `upstream-drift.yml` (weekly Monday cron that upserts a single
  rolling "Upstream drift report" issue) and `release.yml` (a pushed `vX.Y.Z` tag becomes
  a published GitHub Release), plus the `claude-code-docs` skill that fetches the current
  official Claude Code docs before building or explaining any Claude Code internals.
- **Re-sync:** `git pull && bash scripts/bootstrap.sh`, then `/reload-plugins` (or restart Claude Code).

## [0.7.0] - 2026-06-23 — Phase F: team orchestration

- Added `scripts/team_sentinel.py` (session-scoped `set`/`clear` marker) and the `team_gate`
  hooks that read it, so a live session activates the quality gates automatically while
  staying a pure no-op when no session is active.
- Added the multi-agent workflows: the `/team <goal>` slash command (thin) plus the
  `team-orchestration` skill (the brain) that detects the maturity profile, staffs the
  roster, sets the sentinel, decomposes the goal into acceptance-criteria-bearing tasks
  (beads or native Task tools), spawns worktree-isolated teammates, and tears the session
  down. References split into `roster-matrix.md` and `beads-contract.md`.
- Wired the additive experimental agent-teams events (`TaskCreated`, `TaskCompleted`,
  `TeammateIdle`) into the `team_gate` hook (fail-open, sentinel-gated — no-op with the
  `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` flag off), plus the `docs/agent-teams-probe.md`
  runbook for verifying the inferred event payload fields live.
- **Re-sync:** `git pull && bash scripts/bootstrap.sh`, then `/reload-plugins` (or restart Claude Code).

## [0.6.0] - 2026-06-23 — Desktop notifications

- Added a plugin hook (`hooks/hooks.json` + `hooks/notify.py`) that fires a desktop notification
  when Claude needs you: the `Notification` event (permission prompt / idle wait). Opt-in `Stop`
  ping (`CLAUDE_NOTIFY_ON_STOP=1`) for "finished" alerts that stays quiet while background work is
  pending. macOS via `osascript`/`terminal-notifier`, Linux via `notify-send`. Toggles:
  `CLAUDE_NOTIFY=0`, `CLAUDE_NOTIFY_SOUND`.
- **Re-sync:** `git pull && bash scripts/bootstrap.sh`, then `/reload-plugins` (or restart Claude Code).

## [0.5.0] - 2026-06-23 — Phase E: onboarding & UX pass

- Added `scripts/bootstrap.sh` — the recommended one-command onboarding path; safely
  deep-merges `settings.json` into `~/.claude/settings.json` with a backup, idempotent.
- Added `SKILLS.md` full skill catalog plus CI that keeps it fresh.
- Added the `/toolkit` slash command to browse vendored skills by domain in-session.
- Polished `plugin.json` (bumped to 0.5.0) and reworked the README: bootstrap.sh primary,
  manual merge/slash-commands demoted to fallbacks, new "Already set up? Re-sync" section,
  exact 20 plugins / 114 skills + 4 agents clarity line.
- **Re-sync:** `git pull && bash scripts/bootstrap.sh`, then `/reload-plugins` (or restart Claude Code).

## [0.4.0] - 2026-06-23 — Phase D: hygiene & manifest

- Neutralized dead/stale links, bumped the plugin version, and added a vendored-source manifest.

## [0.3.0] - 2026-06-23 — Phase C: ship/operate + data/ML coverage

- Enabled the wshobson ship/operate and data/ML plugins in the always-on tier
  (cloud, k8s, CI/CD, deployment, observability, incident response, backend, data, MLOps).
- **Re-sync:** `git pull && bash scripts/bootstrap.sh`, then `/reload-plugins` (or restart Claude Code).

## [0.2.0] - 2026-06-23 — Phase B: description disambiguation

- Disambiguated overlapping skill descriptions so lazy-by-description triggering picks the right skill.

## [0.1.0] - 2026-06-23 — Phase A: validator + CI

- Added a stdlib-only skill validator (`scripts/validate_skills.py`) and CI to run it.

## [0.0.2] - 2026-06-23 — Enterprise layer

- Added the enterprise layer: exec/strategy, commercial & finance, enterprise sales, customer
  success, business ops, enterprise-software engineering, and compliance-as-code skills —
  materially expanding the vendored catalog.
- **Re-sync:** `git pull && bash scripts/bootstrap.sh`, then `/reload-plugins` (or restart Claude Code).

## [0.0.1] - 2026-06-23 — Initial scaffold

- Initial plugin + marketplace scaffold: manifest, one-plugin marketplace, tiered
  `settings.json`, vendored skills + agents, attribution, and README/cheatsheet.
