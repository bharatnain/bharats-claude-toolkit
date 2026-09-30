# Cost routing, compaction and OpenAI delegation — design

Date: 2026-09-30. Evidence: 7-day local transcript profile (main session ≈ 90% of spend; median
main-session context 250–313K per request, p90 up to 701K; 48 of 50 subagent dispatches were
general-purpose; Codex never invoked) and a usage report from a second machine (Opus 5 in use,
~40 concurrent API streams, 5-hour limit exhausted in 39 minutes).

## Decisions

1. **Compaction at 300K.** `settings.json` ships `autoCompactWindow: 300000` (a token count,
   100000–1000000, per the settings reference; v0.12.0 shipped the invalid string `"300k"`). `bootstrap.sh` merges it add-only and warns when a machine has
   `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`, which would compact at that percentage of 300K.
   `/setup-repo` writes the same window into the git-ignored `.claude/settings.local.json`
   (replacing the 60% env value it wrote in v0.11.0).
2. **Default model `opus`.** The alias tracks the recommended Opus (Opus 5.5 today).
   Bootstrap sets it only when absent and prints a notice when a machine pins something else.
3. **Routing rules.** A "Model routing" section in `templates/user-CLAUDE.md` (always loaded),
   mirrored in `team-orchestration`. Backstop: `env.CLAUDE_CODE_SUBAGENT_MODEL=sonnet`, so any
   dispatch that names no model runs on Sonnet. `spec-miner` (reading-heavy) moves to Sonnet.
4. **OpenAI delegation through the official plugin.** Enable `codex@openai-codex` (already
   registered and SHA-pinned; its stop-review gate defaults to off). It supplies the
   `codex:codex-rescue` subagent (task delegation, any `--model`, background jobs, `--cwd`),
   `/codex:review` and `/codex:adversarial-review`. The toolkit adds only: routing rules with
   model aliases (`sol` = `gpt-6.1-sol`, `luna` = `gpt-6-luna`, `astra` = `gpt-6-astra`), a
   cross-model section in `team-orchestration`, `codex:codex-rescue` as an optional role in every
   team profile, `/setup-repo` detection (Codex CLI, plugin, an `AGENTS.md` block pointing Codex
   at CLAUDE.md), and Codex sessions on the board. This replaces the earlier custom-wrapper design.
5. **No fan-out cap.** Measured: fan-out cost is per-agent model choice, not agent count; a cap
   serialises the same tokens. Routing research agents to Sonnet/Haiku is the lever.
