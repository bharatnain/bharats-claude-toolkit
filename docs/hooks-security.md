# Hook-layer security

This toolkit ships five hook registrations across four scripts (`hooks/hooks.json` →
`beads_init.py`, `notify.py`, `secret_scan.py`, `team_gate.py`). This doc covers three
things: an **opt-in** tamper-proofing pattern for consumers, the stdin/exit-code contract
every hook in this repo follows, and the Claude Code v2.1.207 / v2.1.214 constraints
future hook authors must respect.

## 1. Tamper-proofing (opt-in for consumers — NOT applied by this repo)

A guardrail hook (like `secret_scan.py`) is only as strong as the config that registers
it: an agent that can `Edit` the hooks file or the settings file can simply edit its own
guardrails away, then proceed. The fix is to pair the hooks with `permissions.deny` rules
covering the files that define them (pattern adapted from
[nizos/probity](https://github.com/nizos/probity)'s recommended configuration, MIT):

```json
{
  "permissions": {
    "deny": [
      "Edit(**/hooks.json)",
      "Write(**/hooks.json)",
      "Edit(**/.claude/settings*.json)",
      "Write(**/.claude/settings*.json)"
    ]
  }
}
```

Add this to your **user-level** `~/.claude/settings.json` (a project-level deny that the
agent can edit protects nothing). This repo's `settings.json` deliberately does **not**
ship these rules — this toolkit is itself a repo whose hooks and settings are routinely
edited by agents doing toolkit development. Consumers who want their guardrails
tamper-resistant should opt in.

Known limits — deny rules narrow the Edit/Write tools only:

- `Bash` can still write those files (`sed -i`, `>`, `tee`, ...). If that matters to you,
  deny or sandbox the relevant Bash forms too.
- An agent can propose the user disable a hook via its documented env switch
  (`CLAUDE_SECRET_SCAN=0`, `CLAUDE_TOOLKIT_HOOKS=off`); the switch is the user's call by
  design — the deny rules stop silent self-edits, not explicit user decisions.
- Glob anchoring changed in v2.1.214 (see §3); leading-`**/` patterns like the ones above
  match at any depth, but re-verify any single-segment `dir/**` pattern you add.

## 2. The stdin / exit-code contract our hooks follow

Every hook script in `hooks/` follows the same contract:

- **Input**: the hook event JSON arrives on stdin. Reads are **bounded at 10 MiB**
  (`MAX_STDIN`) so a hook never buffers unbounded input; a truncated payload fails JSON
  parsing and falls through to `{}` — i.e. fail-open.
- **`exit 0`** — allow. Also the outcome for *any* internal error: every entry point is
  wrapped in `try/except` that exits 0, because a broken guardrail must degrade to
  "no guardrail", never to "wedged session". `beads_init.py` and `notify.py` always
  exit 0 (SessionStart/Notification hooks must never block).
- **`exit 2`** — block, with the reason printed to **stderr** (Claude Code feeds stderr
  back to the model). Only `secret_scan.py` (PreToolUse) and `team_gate.py`
  (gate events) ever exit 2. `team_gate.py` translates the `scripts/quality_gate.py`
  runner's exit codes: runner 0 → hook 0, runner 1 → hook 2 (block), runner 2 →
  hook 0 (fail-open).
- **Env off-switches**: each hook has its own (`CLAUDE_NOTIFY=0`, `CLAUDE_BEADS=off`,
  `CLAUDE_SECRET_SCAN=0`), plus `CLAUDE_TOOLKIT_HOOKS=off` which disables all four.
- **Recursion guard**: `team_gate.py` sets `CLAUDE_TOOLKIT_HOOKS=off` in the environment
  of gate subprocesses. Gate checks run profile-configured commands; if one of them
  re-invokes `claude -p`, the nested session inherits the variable and its toolkit hooks
  no-op — otherwise PostToolUse → gate → nested edit → PostToolUse could loop forever.
- **PATH bootstrap**: hooks run in whatever environment Claude Code was launched from,
  which can be minimal (GUI launch, CI). Hooks that spawn binaries (`bd`,
  `terminal-notifier`, `notify-send`, gate tools) prepend `~/.local/bin`, `~/bin`,
  `/opt/homebrew/bin`, and `/usr/local/bin` to `PATH` when missing before resolving them.

(The bounded-read, PATH-bootstrap, and recursion-guard patterns are adapted from
zilliztech/memsearch's `plugins/claude-code/hooks/common.sh`, Apache-2.0 — reimplemented
here in stdlib Python, no code vendored.)

## 3. Constraints for future hook authors (Claude Code v2.1.207 / v2.1.214)

- **v2.1.207**: `${user_config.*}` in **shell-form** hook commands is rejected
  (shell-injection fix). If a hook needs a plugin option value, use exec form — a bare
  executable in `command` plus an `args` array — or read
  `$CLAUDE_PLUGIN_OPTION_<KEY>` inside the script.
- **v2.1.207**: plugin option values (`pluginConfigs`) are no longer read from
  project-level `.claude/settings.json`; only user, `--settings`, and managed settings
  are honored. Don't design a hook that expects per-project plugin options.
- **v2.1.214**: single-segment `dir/**` glob rules (e.g. `Edit(src/**)`) now match only
  `<cwd>/dir`, not any nested `dir/` anywhere in the tree. Audit any glob you write in
  permission rules or hook conditions against the new anchoring.

**Audit verdict (this repo, 2026-08)**: all 11 registrations in `hooks/hooks.json` use
exec form (`"command": "python3"` + `"args": [...]`); `${CLAUDE_PLUGIN_ROOT}` appears
only inside `args` (allowed — the rejection targets `${user_config.*}` in shell-form
strings). No entry uses `if:` conditions, no `${user_config.*}` anywhere, and nothing in
this repo reads `pluginConfigs`. No changes were required for either release.

House rules that keep new hooks consistent: stdlib-only Python, read stdin bounded,
fail open on internal error, per-hook env off-switch, honor `CLAUDE_TOOLKIT_HOOKS=off`,
and register in `hooks/hooks.json` using exec form.
