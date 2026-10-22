# Supply-chain hardening for external plugins and marketplaces

This toolkit registers a dozen external marketplaces in `settings.json`
(`extraKnownMarketplaces`) and enables several third-party plugins from them. A marketplace
registered as a plain `github` source is consumed at **branch HEAD**: whatever the upstream repo's
branch points at when Claude Code fetches it is what runs on your machine. A `sha` placed on such a
marketplace source is not a field Claude Code recognises; it drops it and keeps tracking the `ref`.
A compromised or careless upstream commit would flow straight into every session — no review, no
diff, no pin. The pins below are therefore set on the **plugin entries of inline marketplaces**, the
only place a commit SHA is enforced.

Two controls close that gap:

1. **Inbound gate** — vet a repo *before* registering/enabling it: the
   [`plugin-vetting`](../skills/plugin-vetting/SKILL.md) skill (LLM-judge policy review of
   the whole shipped payload, structured pass/fail verdict).
2. **Pin what you consume** — the SHA-pinning pattern documented below, so a passing
   verdict stays tied to the exact revision it was issued for.

## The SHA-pinning pattern (from anthropics/knowledge-work-plugins)

Anthropic's [knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
curated marketplace consumes external (partner-built) plugins pinned by commit SHA in its
`.claude-plugin/marketplace.json`. First-party plugins use plain relative-path sources
(`"source": "./productivity"`), but every external entry carries an explicit revision:

- `"source": { "source": "url", "url": "<repo>.git", "sha": "<40-char commit>" }` — whole
  repo at an exact commit; or
- `"source": { "source": "git-subdir", "url": "<repo>.git", "path": "plugins/<name>",
  "ref": "main", "sha": "<40-char commit>" }` — a subdirectory of a repo, still resolved
  at the pinned SHA (the `ref` is informational; the `sha` is what installs).

The effect: installs are deterministic and reviewable. Upstream can force-push, get
compromised, or ship a hostile update — consumers keep getting the audited commit until the
pin itself is deliberately moved.

### How the pins stay fresh (automation, described — not vendored here)

The same repo pairs the pins with a nightly workflow loop so pinning does not mean
"frozen forever". Described for reference; the workflows themselves are upstream's
(`.github/workflows/` in that repo) and are **not** copied into this toolkit:

- **Nightly bump** (`bump-plugin-shas.yml`) — for each external entry whose upstream HEAD
  has moved past the pinned SHA, validate the plugin at the new SHA and open one PR per
  bumped entry on its own branch, so a failing entry stays isolated and passing bumps merge
  independently. A per-night cap bounds the work.
- **Policy scan as a required check** (`scan-plugins.yml`) — an LLM-judge review of every
  changed external entry against the same policy this toolkit vendors in
  `skills/plugin-vetting/references/`. `scan` is a required status check on `main`, so no
  pin moves without a fresh verdict. Verdicts are cached per `(plugin, sha)` pair and the
  cache is keyed on the policy hash, so an unchanged SHA is never re-scanned and a policy
  change invalidates all prior verdicts.
- **Auto-drop of failing bumps** (`revert-failed-bumps.yml`) — when a scan on a bump
  branch fails, the failing entries' `sha` is reverted to the last-good pin in a
  follow-up commit and the scan re-dispatched, so one bad upstream never blocks the rest.
  The job is tightly scoped (only the bump branch, only the `sha` field, bounded retries;
  any other diff aborts for human triage).
- Supporting guards: MCP-URL liveness checks for local-source plugins and a scope guard
  that keeps external PRs from touching files outside their own plugin directory.

The net design: **pin by SHA, gate every pin move behind a policy scan, and auto-quarantine
failures**. That is the recommended way to consume the external marketplaces this toolkit
registers.

## Applying this to bharats-claude-toolkit

Current state: every third-party marketplace in `settings.json` is an inline marketplace
(`"source": "settings"`, `name` equal to its key) whose plugin entries carry the pin:

```json
"trailofbits": { "source": { "source": "settings", "name": "trailofbits", "plugins": [
  { "name": "fp-check", "source": { "source": "git-subdir", "url": "trailofbits/skills",
      "path": "plugins/fp-check", "ref": "main", "sha": "<40-char commit>" } } ] } }
```

- **Enforced per plugin.** Claude Code checks out the `sha` of each plugin entry (the `ref` only
  says where to look). A plugin at the repo root uses `"source": "github"` with `repo`; a plugin in a
  subdirectory uses `git-subdir` with `url: "owner/repo"` and `path`.
- **Names are unchanged,** so every `plugin@marketplace` key in `enabledPlugins` keeps working
  (`memsearch` is registered as `memsearch-plugins`, the name its repo declares). A catalog lists
  only the plugins this toolkit names; another plugin from the same repo needs its own vetted,
  pinned entry. `bharats-claude-toolkit-dev` stays a plain `github` source so consumers track this repo.
- **Bootstrap enforces the repo's pins.** `scripts/bootstrap.sh` overwrites these inline entries whole
  in `~/.claude/settings.json` and keeps every other marketplace entry add-only. Claude Code registers
  a settings-declared marketplace only when it does not already know the name, so for a name registered
  earlier from GitHub bootstrap prints the migration instead of running it: `claude plugin marketplace
  remove <name>` for each (this uninstalls that marketplace's plugins and also drops its settings
  entry), then `bash scripts/bootstrap.sh` again, then restart Claude Code and reinstall the plugins
  you use.
- **Bumping a pin.** `scripts/check_upstream.py` reports pin drift alongside vendored-skill drift, and
  the weekly `upstream-drift` job posts both to the rolling issue. To move a pin: run `plugin-vetting`
  on the new revision, then edit the `sha` of that plugin's entry in `settings.json` (plugins of one
  repo in one marketplace share a sha). If a machine that already registered the marketplace from
  settings does not pick up the new pin, repeat the remove / bootstrap / restart sequence. Step 3
  below (automated bump, scan, auto-drop) is still not implemented.

The pattern here, in increasing order of effort:

1. **Vet-then-register** (available now) — run `plugin-vetting` on every candidate repo
   before adding it to `settings.json`; record repo + vetted SHA + verdict date.
2. **Pin the plugins** (done) — pin each consumed plugin to its vetted revision on an inline
   marketplace entry, as described above. This changes what `scripts/bootstrap.sh` installs
   for every consumer of this toolkit, and it needs a deliberate re-vet-and-bump routine
   (manual or CI, as above) so pins don't rot.
3. **Bump automation** — a scheduled job in this repo mirroring the
   bump → scan → auto-drop loop described above, with `plugin-vetting`'s vendored policy as
   the scan.

## External tooling

Trail of Bits maintains [skills-curated](https://github.com/trailofbits/skills-curated), a
public marketplace of Claude Code plugins that their staff have security-reviewed — this
toolkit already registers it (`skills-curated` in `settings.json`). Their
reviewer tooling includes a plugin scanner,
[`scripts/scan_plugin.py`](https://github.com/trailofbits/skills-curated/blob/main/scripts/scan_plugin.py),
usable as a second, independent opinion alongside `plugin-vetting`.

> Licensing note: `trailofbits/skills-curated` is CC BY-SA. It is referenced here **by URL
> only** — do not copy its code or text into this repo (the share-alike clause is
> incompatible with this repo's licensing).
