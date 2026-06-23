# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/), and versions map to the toolkit's phases.

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
