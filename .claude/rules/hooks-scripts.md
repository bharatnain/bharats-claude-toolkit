---
paths: ["hooks/**", "scripts/**"]
---

# Hooks and scripts contract

- Python stdlib only.
- Read stdin bounded at 10 MiB.
- Exit 0 = allow. Exit 2 = block, with the reason on stderr.
- Guardrail hooks (`secret_scan`) fail closed: exit 2 on any internal error. `notify` and `beads_init` fail open.
- Honour `CLAUDE_TOOLKIT_HOOKS=off` (master switch) and the per-hook switches (`CLAUDE_NOTIFY`, `CLAUDE_BEADS`).
- Bootstrap `PATH` at the top of each hook so GUI launches find user bin dirs.
- Never make network calls from a hook.
- Report-family scripts (`check_upstream`, `doctor`, `skill_usage`) take `--format human|json`; `validate_skills` and `validate_assets` take `--format text|github` (`validate_profiles` predates the split and takes `human|github`).
