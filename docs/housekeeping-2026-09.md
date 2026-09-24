# Housekeeping — September 2026 refresh

Two sweeps on 2026-09-22. The first (research + audit, 4 teammates) produced a 23-item
backlog; the second (7 re-vendor/research teammates + 2 catalog teammates) executed it.
This file records what was **done**, what was **deferred with a reason**, and what only
the maintainer can do. Re-run the sweep when Claude Sonnet 5.5 / Haiku 5.5 ship
(announced "in the coming weeks" on 2026-09-22 — no IDs, prices, or dates yet).

Ground truth at sweep time: Claude Code **2.1.280** (Opus 5.5 is the default `opus`);
models **Fable 5.1** (`claude-fable-5-1`), **Opus 5.5** (`claude-opus-5-5`, GA 2026-09-22),
**Opus 5**, **Sonnet 5** (`claude-sonnet-5`, $2/$10 permanent), **Haiku 4.5**
(`claude-haiku-4-5`). Opus 4.1 retired 2026-08-05. Sonnet 4.5's earliest retirement date
(2026-09-29) has no notice posted yet — watch the deprecations page.

## Done (2026-09-22)

| # | Item | Outcome |
|---|---|---|
| 1 | Release 0.9.0 | `release.py` fixed (promotes `[Unreleased]`; tag now follows the release commit). 0.9.0 is cut from branch `claude/silly-raman-f64f90` as the commit after this doc (`[0.9.0]` in CHANGELOG), local tag `v0.9.0`, **not pushed**. Push the branch, merge, then `git push --tags`. |
| 2 | GRC v2.0.0 re-vendor | soc2, iso-27001, gdpr, hipaa, pci-dss at `3483277` — Sep-2026 regulatory currency. New upstream skills not vendored (candidates: cyber-essentials, sox-itgc, tprm, eu-cra, dora, cmmc). |
| 3 | Agent-teams gates | **Removed** (user decision): 3 hook registrations, `team_gate.py` branches, probe doc, README section, skill mentions. Events remain experimental upstream. |
| 4 | ecc drift | **Full re-pull** (user decision): 22 skills at `bf70150` (4 agents verified unchanged); local edits re-applied; 14 descriptions adopted upstream "Use when…" clauses (then re-disambiguated in the overlap pass). `repo-scan` kept at its previous content — upstream replaced it with an installer stub for an external tool. |
| 5 | marketingskills | 18 skills at `5b2c000`; partner-link audit clean; 3 non-partner vendor plugs neutralized; 28 upstream-escaping links neutralized. |
| 6 | workos 0.7.3 + hallmark Grid | Done; hallmark SKILL.md link neutralization (5133db9) re-applied, and two remaining `references/custom-theme.md` links to upstream `site/css/tokens.css` neutralized. |
| 7 | mattpocock subscription | Now consumed SHA-pinned from `claude-plugins-official` (`c55ee46`); `writing-for-agents` still exists; README bullet updated. |
| 8 | superpowers 6.4.1 | Consumed from `claude-plugins-official`; README notes native `executing-plans` + `diagnosing-superpowers`. |
| 9 | team-orchestration / hooks-security re-verify | Limits re-verified (depth 3, 20 concurrent; 200/session no longer documented); hooks-security §3 dated 2026-09-22 with 2.1.280 additions. |
| 10 | Official plugins | `claude-security`, `session-report`, `skill-creator` enabled (user decision). Note: machines with the separate `anthropic-skills` plugin also have `anthropic-skills:skill-creator`; both resolve by `@`-namespace. |
| 12 | `secret_scan.py` patterns | +9 patterns (OpenAI, npm, PyPI, HF, SendGrid, Twilio, GitLab, service-account JSON, `aws_secret_access_key`). |
| 13 | Hook cleanup | `MultiEdit` dropped; `TeammateIdle` exit-2 steer gone with the agent-teams removal. |
| 14 | Manifest SHA bumps | Every source's `upstream_head_at_manifest` now equals the HEAD it was vendored from. |
| 15 | README truth-ups | Option B generated from `settings.json`; duplicate agent-teams warnings removed; native-skill list corrected (`deep-research`/`verify` dropped). |
| 16 | NOTICES not-vendored list | Completed with licences (Trail of Bits CC-BY-SA-4.0; memsearch MIT; codex Apache-2.0; probity MIT). |
| 17 | Supply chain | External marketplaces SHA-pinned (`ref`+`sha`); `check_upstream.py` reports pin drift; Actions pinned by SHA; beads installer pinned to `gastownhall/beads` v1.3.0 with `BEADS_VERSION`. |
| 18 | Plugin evals | `evals/claude-code-docs-triggers` + manual `plugin-eval.yml`. `plugin.json` unchanged: components auto-discover; `workflows` is not a documented field. |
| 20 | Overlap pass | 17 pairs disambiguated in descriptions; SKILLS.md regenerated. |
| 21 | Cosmetic | `react-best-practices` name aligned (validator allowlist removed); code-migration sample rows show `claude-sonnet-5`. |

## Applied 2026-09-24 (practice review, PR after #10)

All 12 items in `docs/claude-code-practices-gap-2026-09.md` are applied except: evals per skill
family (one case exists; grow as skills change); `if:` filters on hook entries (matchers are
already specific); exposing `syncClaudeAiSkills` / `autoMemoryEnabled` / `workflowSizeGuideline`
in the settings template (user preferences, documented in README instead). Decision recorded:
`agents/tech-lead.md` stays as the roster's required orchestrator role; the skill casts the main
session as tech-lead when run via `/team`. Permission-prompt reduction (allow/deny/defaultMode,
notification routing) shipped in the same PR; on other machines run
`CLAUDE_FORCE_CLAUDE_MD=1 bash scripts/bootstrap.sh` (the force flag replaces an older
`~/.claude/CLAUDE.md`, with a backup).

## Deferred (with reason)

- **11 — SKILL.md splits.** Only `hallmark` (67 k, already diverged) was split into
  `references/`. The other 33 files over 15 k are freshly re-vendored upstream skills; splitting
  them would re-diverge them right after a re-sync, and skills load lazily (size costs only on
  invocation). Revisit per-skill if `/skill-doctor` shows a large one firing often.
- **19 — Managed Agents capability gates.** `cma-primitives.md` still says `system.message` is
  "Opus 4.8 only" and memory consolidation supports "opus-4-8/4-7, sonnet-4-6"; current docs do
  not document either, so nothing verifiable to replace them with. Fast-mode list is corrected.
- **22 — Candidate additions** (`anti-slop` ×2, `sepia`, `modern-web-guidance`, `video-shotcraft`,
  `lieflat-charts`): not evaluated; overlap existing `avoid-ai-writing`/`humanizer`,
  `web-quality-skills`, `remotion-video-creation`, built-in `dataviz`.
- **Supply-chain step 3** (automated bump → scan → auto-drop loop): not built; pins are moved
  by hand after `plugin-vetting`.
- **ecc description clauses**: upstream's "Use when…" clauses were adopted for 14 skills; the
  overlap pass re-checked the 17 known pairs but not every adopted clause. Skim
  `SKILLS.md` once for surprises.
- **Dangling sibling pointers.** Several marketingskills descriptions/bodies name upstream skills
  we do not vendor (`signup`, `popups`, `offers`, `schema`, `programmatic-seo`, `attribution`,
  `marketing-loops`, `positioning`, `free-tools`). They are plain names (no links), so nothing
  breaks; vendor them or strip the pointers in a later pass.
- **churn-rca `README.md`** inside the skill dir (matches every customer-success sibling) —
  keep or drop repo-wide; not decided.

## Maintainer-only

- Prune never-invoked vendored skills. `/skill-doctor` reports are not available on this
  connection, so use the local stand-in: `python3 scripts/skill_usage.py --days 30` (add
  `--prune-list` for bare directory names). Review the list by hand before removing anything.
- Run `bash scripts/bootstrap.sh` on each other machine so the roster change lands (done on the primary machine 2026-09-22)
  (`superpowers@superpowers-marketplace` and `mattpocock-skills@mattpocock` flip to `false`,
  the five new `claude-plugins-official` plugins enable — `bootstrap.sh` now forces repo-side
  `false` values, which its add-only merge previously could not). Fully quit and reopen Claude Code.
- Set the `ANTHROPIC_API_KEY` repo secret if you want `plugin-eval.yml` to run:
  `bash scripts/set_eval_secret.sh` (hidden prompt, or reads `$ANTHROPIC_API_KEY`).
- Watch the model deprecations page for Sonnet 4.5 and the Sonnet 5.5 / Haiku 5.5 launches.
