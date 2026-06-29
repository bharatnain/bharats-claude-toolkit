# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/), and versions map to the toolkit's phases.

## [Unreleased]

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
