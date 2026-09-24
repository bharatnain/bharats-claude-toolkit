---
name: setup-repo
description: Set up a repository for efficient Claude Code work — detect the stack and its test/lint commands, then write a repo-facts CLAUDE.md with a verification block, path-scoped rules, project permissions and a lint-on-edit hook, a team profile and effort default, and a machine-local auto-compact threshold. Idempotent; `--check` reports drift only.
disable-model-invocation: true
argument-hint: "[--check]"
---

# /setup-repo

Engine: `scripts/repo_setup.py` (stdlib). Run every command from the repo root.

1. `python3 <skill>/scripts/repo_setup.py detect` → read the JSON. If `commands` is empty, say so and still continue (only the working/compaction blocks will be written).
2. `python3 <skill>/scripts/repo_setup.py plan` → present it as a list: `action path — reason`, then the `recommendations`. Show the rendered CLAUDE.md verbatim (it is short).
3. With `--check`: run `check` instead of `plan`, print its output, stop.
4. Ask once: "Apply these N changes?" On yes run `apply` (it re-checks and prints `check: clean`); paste that line as evidence. On no, stop.
5. Close with a short **how to use this setup** note (≤6 lines, from the profile): the check to run before done; `/goal <check passes>` for unattended runs; `/team <goal>` for multi-file work (team profile: <maturity>); effort `<effort>` for build work, `high` for design/review; auto-compact fires at 60% of the window (`.claude/settings.local.json`, machine-local). Then the **status dashboard option**: "Enable the status dashboard with `/board` (shows waiting-on-you, in-flight work, sessions and PRs; refreshes after every turn)." Then the next steps: trust the folder if this is its first session; `/reload-plugins` or restart; run `/context` to confirm what loads.

`<skill>` is this skill's directory (`${CLAUDE_PLUGIN_ROOT}/skills/setup-repo` when installed as a plugin). Never edit CLAUDE.md text outside the `<!-- setup-repo:* -->` markers by hand from this skill; users own the rest.
