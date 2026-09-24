# bharats-claude-toolkit

My personal Claude Code setup, packaged as a **plugin + marketplace** so I can pull it into
any codebase on any machine with one command — and pull *more* on demand, mid-project.

The design goal: **I never have to remember what I have.** Skills load lazily by their
description, so I just work and Claude reaches for the right one. The only thing I decide up
front is what sits in my *always-on* index vs. what stays *one command away*.

**Always-on = 29 enabled plugins**, which bring **137 vendored skills (52 always-on, 85 user-invoked via `/name`) + 8 agents** from this
repo plus the external plugins' own skills — all loaded lazily by description. The unit you
*enable* is the plugin; the 137 skills + 8 agents are what *this* repo's plugin contributes,
and the other 28 plugins layer their skills on top.

See [`CHANGELOG.md`](CHANGELOG.md) for the phase-by-phase history and
[`docs/housekeeping-2026-09.md`](docs/housekeeping-2026-09.md) for the open maintenance backlog.

---

## How it's structured (3 tiers)

| Tier | What | How it's wired |
|---|---|---|
| **Always-on** | This plugin + a few best-in-class external plugins, enabled in every directory | `enabledPlugins` in user-global `~/.claude/settings.json` |
| **On-demand** | The ECC firehose and other registered-but-not-enabled plugins | `extraKnownMarketplaces`; install when relevant |
| **Vendored** | Curated skills copied *into* this plugin (so it's self-contained) | `skills/` and `agents/` in this repo |

**Always-on plugins**
- `bharats-claude-toolkit` — this repo (vendored skills + agents below)
- `frontend-design` — Anthropic (`claude-plugins-official`): production-grade UI taste
- `ui-ux-pro-max` — design intelligence: 67 styles / 161 palettes / 57 font pairings
- `web-quality-skills` — Addy Osmani: accessibility (WCAG 2.2), performance, Core Web Vitals, SEO
- `pm-product-discovery` / `pm-product-strategy` / `pm-execution` — phuryn PM skills: discovery, strategy, PRDs/OKRs/roadmaps
- `superpowers` — obra, consumed from `claude-plugins-official` (SHA-pinned by Anthropic): brainstorm→plan→execute methodology. Note: since v6.4.1 `executing-plans` runs plans natively without pausing for review mid-plan; `diagnosing-superpowers` is its debugging entrypoint
- `mattpocock-skills` — Matt Pocock, consumed from `claude-plugins-official` (SHA-pinned by Anthropic): ~30 compact engineering/process skills — grilling (frontier-driven design interviews), domain-modeling (CONTEXT.md + ADRs), wayfinder/triage/to-tickets (tracker-abstracted planning; bind to beads via `/setup-matt-pocock-skills`), diagnosing-bugs (feedback-loop-first), teach, codebase-design. Its `writing-for-agents` is this toolkit's **house standard for skill authoring**.
- `security-guidance` / `plugin-dev` — Anthropic (`claude-plugins-official`): security guardrails + plugin authoring
- `claude-security` / `session-report` / `skill-creator` — Anthropic (`claude-plugins-official`): in-session vulnerability scanning with verified patches, explorable session-usage reports, and skill creation/eval tooling (pairs with the `writing-for-agents` authoring standard)
- `differential-review` / `fp-check` — Trail of Bits (`trailofbits-skills`); `security-awareness` — Trail of Bits (`trailofbits-skills-curated`)
- `agent-orchestration` — wshobson `claude-code-workflows`: multi-agent role/team setups (tech-lead, frontend, backend, ml-engineer). *`agent-teams` from the same marketplace is explicitly **disabled** — it still calls the `TeamCreate`/`TeamDelete` tools removed in Claude Code v2.1.178.*
- **ship & operate** (wshobson `claude-code-workflows`): `backend-development`, `backend-api-security`, `cloud-infrastructure`, `kubernetes-operations`, `cicd-automation`, `deployment-strategies`, `deployment-validation`, `observability-monitoring`, `incident-response` — deploy/run/monitor the product
- **data & ML** (wshobson `claude-code-workflows`): `data-engineering`, `machine-learning-ops` — pipelines/warehouses, ML training & MLOps

**On-demand (registered, install when needed)**
- `ecc@ecc` — the full 271-skill ECC collection
- `probity` — nizos: TDD/rule-enforcement hooks; `memsearch` — zilliztech: semantic session memory; `openai-codex` — OpenAI: cross-model reviews — all registered, not enabled
- the remaining `trailofbits-skills` / `trailofbits-skills-curated` plugins beyond the three enabled above
- more from `pm-skills` (`pm-go-to-market`, `pm-market-research`, `pm-data-analytics`, …) and `claude-code-workflows` (`conductor`, `frontend-mobile-development`, …)
- `beads` — agentic issue tracker (`bd` CLI + plugin); see **Agentic project management** below

---

## Bootstrap a new machine

**Recommended — run the bootstrap script:**

```bash
bash scripts/bootstrap.sh
```

It safely deep-merges this repo's [`settings.json`](settings.json) (`extraKnownMarketplaces`,
`enabledPlugins`, and the `permissions` allow/deny lists plus `defaultMode`) into your
user-global `~/.claude/settings.json`, writing a timestamped backup first, and is idempotent —
re-running it never duplicates or removes entries. Open Claude Code in any directory and the always-on
tier is live; `ecc` is registered and one command away.

It also installs [`templates/user-CLAUDE.md`](templates/user-CLAUDE.md) (Andrej Karpathy's
LLM-coding guidelines plus compaction and follow-up rules) to `~/.claude/CLAUDE.md` so the
rules apply in **every** project by default. The repo's own [`CLAUDE.md`](CLAUDE.md) holds
repo facts only (validators, release flow, gotchas), and [`.claude/rules/`](.claude/rules)
holds path-scoped rules for `skills/`, `hooks/`+`scripts/`, and `agents/`. It writes the file
only when absent and never clobbers a differing one you already have — opt out with
`CLAUDE_DEFAULT_CLAUDE_MD=off`, or overwrite-with-backup via `CLAUDE_FORCE_CLAUDE_MD=1`.

*Advanced/test:* set `CLAUDE_SETTINGS=/path/to/settings.json` to merge into a different target
file, and `CLAUDE_MD=/path/to/CLAUDE.md` to install the rules to a different target file.

<details>
<summary>Fallbacks (manual)</summary>

**Option A — committed settings (manual merge).**
Merge the contents of [`settings.json`](settings.json) into your user-global
`~/.claude/settings.json` by hand (it carries both `extraKnownMarketplaces` and
`enabledPlugins`). This is what `bootstrap.sh` does for you.

**Option B — slash commands (manual; generated from `settings.json`).**
```text
# register marketplaces (claude-plugins-official is built in)
/plugin marketplace add bharatnain/bharats-claude-toolkit
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin marketplace add addyosmani/web-quality-skills
/plugin marketplace add affaan-m/ecc
/plugin marketplace add phuryn/pm-skills
/plugin marketplace add wshobson/agents
/plugin marketplace add trailofbits/skills
/plugin marketplace add trailofbits/skills-curated
/plugin marketplace add nizos/probity
/plugin marketplace add zilliztech/memsearch
/plugin marketplace add openai/codex-plugin-cc

# enable the always-on tier
/plugin install bharats-claude-toolkit@bharats-claude-toolkit-dev
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
/plugin install web-quality-skills@addy-web-quality-skills
/plugin install frontend-design@claude-plugins-official
/plugin install pm-product-discovery@pm-skills
/plugin install pm-product-strategy@pm-skills
/plugin install pm-execution@pm-skills
/plugin install security-guidance@claude-plugins-official
/plugin install plugin-dev@claude-plugins-official
/plugin install differential-review@trailofbits-skills
/plugin install fp-check@trailofbits-skills
/plugin install security-awareness@trailofbits-skills-curated
/plugin install agent-orchestration@claude-code-workflows
/plugin install cloud-infrastructure@claude-code-workflows
/plugin install kubernetes-operations@claude-code-workflows
/plugin install cicd-automation@claude-code-workflows
/plugin install deployment-strategies@claude-code-workflows
/plugin install deployment-validation@claude-code-workflows
/plugin install observability-monitoring@claude-code-workflows
/plugin install incident-response@claude-code-workflows
/plugin install backend-development@claude-code-workflows
/plugin install backend-api-security@claude-code-workflows
/plugin install data-engineering@claude-code-workflows
/plugin install machine-learning-ops@claude-code-workflows
/plugin install superpowers@claude-plugins-official
/plugin install mattpocock-skills@claude-plugins-official
/plugin install claude-security@claude-plugins-official
/plugin install session-report@claude-plugins-official
/plugin install skill-creator@claude-plugins-official
# NOTE: do NOT install agent-teams@claude-code-workflows — it calls tools
# removed in Claude Code v2.1.178 and is explicitly disabled in settings.json.
```

</details>

**Browse the toolkit.** Once the plugin is enabled, run the [`/toolkit`](skills/toolkit/SKILL.md)
slash command to see every vendored skill grouped by domain plus the enabled external plugins —
so you never have to remember what's installed. Full catalog: see [`SKILLS.md`](SKILLS.md). Run
[`/doctor`](skills/doctor/SKILL.md) to health-check the setup, and note the always-on
`claude-code-docs` skill auto-consults the current official docs before Claude touches any
Claude Code internals — so explanations track the latest release, not stale memory.

## Already set up? Re-sync

When this repo's `settings.json` changes — a new always-on plugin or marketplace — pull and
re-run the bootstrap to pick it up:

```bash
git pull
bash scripts/bootstrap.sh   # backup + merge; keeps your own plugins, enforces repo-side disables
/reload-plugins             # activate in this session (or restart Claude Code)
```

The merge adds new entries and keeps plugins you enabled yourself, with one exception: a
plugin this repo's `settings.json` sets to `false` (a retired marketplace copy, or
`agent-teams` which calls removed tools) is forced off on every run. Returning users only need
these three lines.

---

## Fewer permission prompts

The settings template ships a permissions block that bootstrap merges into your global
settings, so it applies in every project and on every machine you bootstrap:

- `permissions.defaultMode: "auto"` — new terminal sessions start in auto mode (a classifier
  reviews actions instead of prompting you). Set only when you have no `defaultMode` of your own.
- `permissions.allow` — the routine developer commands that showed up most in real transcripts
  (`python3`, `uv`, `sqlite3`, `git add/commit/status/log/diff`, `gh` read operations, test
  runners, `mkdir/cp/mv`) plus `WebFetch`, `WebSearch`, `Agent` and `Skill`. Allowed calls never
  prompt in Manual mode and skip the classifier in auto mode.
- `permissions.deny` — credential reads (`.env` and every `.env.*` variant, `~/.ssh`, `~/.aws`,
  cloud and registry configs) and destructive git/rm forms, enforced in every mode, including
  bypass. A deny beats an allow at any scope, so committed templates like `.env.example` are
  also blocked for the Read tool; view them with `cat` when needed.

Allow and deny merge as unions, so your own rules are kept. Edit the lists in
`~/.claude/settings.json` afterwards if a rule is too broad for you; a deny at any scope wins
over an allow at any other. Rules match command text only, so pair them with `/sandbox` for
hard boundaries. `/permissions` shows what is in effect.

Other settings worth knowing, left to you (not merged by bootstrap): `syncClaudeAiSkills: false`
stops claude.ai skills from syncing into terminal sessions and inflating the skill listing;
`autoMemoryEnabled`; `workflowSizeGuideline` (`small`/`medium`/`large`/`unrestricted`);
`outputStyle: "Toolkit"` selects this plugin's output style.

## Working with this toolkit

The day-to-day loop the docs recommend, and where each piece of this repo fits:

1. **Explore, then plan, then implement.** Use plan mode (`Shift+Tab`) for anything you couldn't
   describe in one sentence; skip it for small fixes.
2. **Give Claude a check it can run.** Name the test, build, or validator in the prompt. For
   unattended runs set `/goal <condition>` so the session doesn't stop at "looks done"; the
   legacy team profile adds a Stop-hook gate.
3. **Keep context clean.** `/clear` between unrelated tasks, `/btw` for side questions, `/compact`
   with instructions; the user-level CLAUDE.md tells Claude what to preserve.
4. **Delegate reading.** Subagents for investigation and adversarial review (`/code-review`, the
   `code-reviewer` agent); `/team <goal>` for multi-agent builds with gates; a Workflow when the
   job outgrows a handful of agents.
5. **Where instructions live.** Always-on facts in `CLAUDE.md` and `.claude/rules/`; procedures
   and reference material in skills (52 always-on, the rest behind `/name`); guarantees in hooks;
   response shape in the `Toolkit` output style.
6. **Set up a repo.** `/setup-repo` prepares any repo (CLAUDE.md facts + check, rules, permissions,
   lint hook, team profile); `--check` shows drift.

## Desktop notifications (when Claude needs you)

A plugin hook pings your desktop the moment Claude is **waiting on you** — a permission prompt or
an idle wait (the `Notification` event) — so you can step away during long runs and get pulled back
exactly when needed. macOS works out of the box via `osascript` (zero install); install
`terminal-notifier` for clickable, app-branded pings; Linux uses `notify-send`.

It ships in the always-on plugin (`hooks/notify.py`) — `git pull && bash scripts/bootstrap.sh`
then `/reload-plugins` to activate. Tunables (set in your shell, or under `env` in
`~/.claude/settings.json`):

- `CLAUDE_NOTIFY_ON_STOP=1` — also ping when Claude **finishes** a turn (default off; it stays
  quiet while a background task/workflow is still running, so you're only pinged when truly done).
- `CLAUDE_NOTIFY=0` — turn all notifications off.
- `CLAUDE_NOTIFY_SOUND=Ping` — macOS sound name (empty string = silent).
- `CLAUDE_NOTIFY_FORCE=1` — also ping inside the desktop app. By default the hook stays silent
  there (`CLAUDE_CODE_ENTRYPOINT=claude-desktop`), because the app already shows its own OS
  notification and can push to your phone; without this, one event produced up to three pings.

The hook is registered with the matcher `permission_prompt|idle_prompt`, so auth, elicitation
and agent-lifecycle notifications never reach it. Phone pushes are the desktop app's own
setting (`agentPushNotifEnabled` in `~/.claude/settings.json`, or Settings → Claude Code).

> macOS first run: allow notifications for your terminal app when prompted (or System Settings →
> Notifications), otherwise pings won't appear.

---

## Pull more, mid-project (cheatsheet)

```text
/plugin install ecc@ecc                              # the 271-skill firehose
/plugin marketplace add obra/superpowers-marketplace && /plugin install elements-of-style@superpowers-marketplace  # obra style guide
/reload-plugins                                       # make them live in THIS session, no restart
```
Also registered (browse with `/plugin` and install from their marketplaces): **probity**
(TDD/rule-enforcement hooks), **memsearch** (semantic session memory), **openai-codex**
(cross-model reviews), and the remaining **trailofbits-skills** / **trailofbits-skills-curated**
plugins beyond the enabled `differential-review` / `fp-check` / `security-awareness`.

Then just work — the newly available skills auto-trigger by description.
(`/reload-plugins` may warn about prompt-cache invalidation if a plugin adds MCP servers.)

To cherry-pick a single ECC skill permanently instead of installing all of ECC, copy its
folder from `github.com/affaan-m/ecc/skills/<name>/` into this repo's `skills/`.

---

## Agentic project management (beads)

[beads](https://github.com/gastownhall/beads) (`bd`) is a graph issue-tracker built for AI
agents — persistent, dependency-aware task memory across sessions. It's a **tool**, not a
vendored skill (its license is unverified), so integrate it rather than copy it:

```bash
# 1) install the CLI
curl -sSL https://raw.githubusercontent.com/gastownhall/beads/v1.3.0/scripts/install.sh | BEADS_VERSION=1.3.0 bash
# 2) in a project
bd init
# 3) enable its Claude Code plugin (slash commands + MCP) per the repo's docs/PLUGIN.md
```
Then agents use `bd ready` / `bd show <id>` / `bd update <id> --claim` / `bd close <id>` to
track long-horizon work. For lighter needs, `pm-execution` (above) covers PRDs/roadmaps/sprints.

---

## Team orchestration

`/team <goal>` spins up a maturity-matched multi-agent team to deliver a goal end-to-end. The
thin `/team` command defers to the **`team-orchestration`** skill (the brain), which runs a
6-step loop: detect the codebase maturity profile (`team_profile_detect.py`), pick the roster
from that profile's required roles, activate a session **sentinel** (`team_sentinel.py set`)
so the **gate hooks** + `quality_gate.py` enforce the profile's checks automatically,
decompose the goal into acceptance-criteria-bearing tasks (beads if `bd` is present, native
Task tools otherwise), spawn worktree-isolated teammates per the profile's isolation flag, and
tear the session down (`team_sentinel.py clear`) at the end. Tasks pair with the beads tracker
above when available.

**Solo-safe by design:** with no sentinel marker, the gate hooks are pure no-ops — installing
this changes nothing for solo work until `/team` activates a session, and teardown returns the
hooks to no-ops.

---

## What's vendored in this plugin

**Workflow & engineering** — `tdd-workflow`, `verification-loop`, `codebase-onboarding`,
`repo-scan`, `production-audit`, `agentic-engineering`, `research-ops`

**Architecture & planning (agents)** — `architect`, `planner`, `code-architect`, `spec-miner`

**Building AI products** — `mcp-builder` (Anthropic), `eval-harness`, `cost-aware-llm-pipeline`,
`context-budget`, `launch-your-agent` + `agent-wrap-up` (Claude Managed Agents scaffolding)

**Security pipeline (Anthropic defending-code)** — `threat-model`, `vuln-scan`, `vuln-triage`,
`vuln-patch`, `dnr-hunt`, `dnr-respond` — the full THREAT_MODEL → findings → triage → patch chain,
plus `plugin-vetting` (vet third-party plugins/marketplaces before enabling; see
[`docs/supply-chain.md`](docs/supply-chain.md))

**Code migration** — `code-migration` (Anthropic's migration kit: feasibility → dependency map →
translation → parity)

**Financial modeling (Anthropic financial-services)** — `dcf-model`, `3-statement-model`,
`comps-analysis`, `lbo-model`, `audit-xls` — hands-on spreadsheet construction/auditing
(strategy stays with `cfo-advisor`)

**Python & data** — `python-patterns`, `python-testing`, `fastapi-patterns`, `postgres-patterns`

**Frontend & React** — `react-patterns`, `react-best-practices` (Vercel)

**Design & UI polish** — `design-system`, `make-interfaces-feel-better`, `motion-foundations`,
`motion-patterns`, `theme-factory`, `brand-guidelines`, `hallmark` (anti-slop design review /
design-DNA extraction — explicit invocation only)

**Copywriting & content** — `copywriting`, `copy-editing`, `content-strategy`, `content-engine`,
`article-writing`, `brand-voice`, `onboarding`

**UX writing** — `ux-writing`

**SEO** — `seo-audit`, `ai-seo`

**Market & customer research** — `market-research` (TAM/SAM/SOM, competitive, diligence),
`customer-research` (ICP/JTBD/VOC), `competitor-profiling`, `competitors`, `product-marketing`
(positioning/ICP context spine). For general research, use the vendored `research-ops`.

**Go-to-market** — `launch`, `sales-enablement`, `pricing` (with `product-marketing` + `market-research` above)

**Full-stack marketing** — `ads`, `ad-creative`, `emails`, `social`, `cro`, `analytics`, `referrals`,
`public-relations`, `marketing-psychology`, `lead-magnets`, `prospecting`, `cold-email`, `revops`

**Audio & video (creative)** — `ffmpeg-usage`, `video-editing`, `remotion-video-creation`,
`fal-ai-media`. *External deps:* `ffmpeg` (all video), `node`+Remotion (`remotion-video-creation`),
and a paid fal.ai `FAL_KEY` (`fal-ai-media`). No good Claude skill exists for streaming/codec
*product* engineering (WebRTC/HLS) — use libraries like SRS/mediamtx directly.

### Running the company (the enterprise layer)

Skills that take the toolkit from "build & market a product" to "run a company end-to-end."

**Exec & strategy (C-suite advisory)** — `ceo-advisor`, `cfo-advisor`, `cro-advisor`, `cmo-advisor`,
`cpo-advisor`, `general-counsel-advisor` (now with a vendored contract-review deep-dive family),
`advisor-profile` (guided interview → the shared `company-context.md` all advisors read),
`board-deck-builder`, `executive-mentor` (adversarial
thinking partner), `competitive-intel`, `ma-playbook`, `scenario-war-room`, `agent-protocol`
(inter-advisor coordination)

**Commercial & finance** — `pricing-strategist`, `deal-desk`, `commercial-policy`,
`commercial-forecaster`, `partnerships-architect`, `channel-economics`, `rfp-responder` (Shipley
method)

**Enterprise sales** — `sales-methodology-implementer` (MEDDIC/Challenger/SPIN), `deal-review-framework`,
`sales-forecast-builder`, `pipeline-health-analyzer`, `quota-setting-calculator`,
`territory-planning-optimizer`, `sales-comp-plan-designer`, `objection-pattern-detector`

**Customer success & retention** — `qbr-builder`, `health-score-review`, `renewal-readiness`,
`renewal-forecast`, `churn-analysis`, `churn-rca`, `expansion-business-case`, `expansion-signal`,
`success-plan-builder`, `onboarding-plan`, `kickoff-prep`, `ttv-analysis` (real GRR/NRR formulas)

**Business operations** — `procurement-optimizer`, `process-mapper`, `vendor-management`

**Enterprise software (sellable-to-enterprise engineering)** — `workos-enterprise-auth`
(SSO/SAML, SCIM, audit logs), `openfga` + `rego-skill` + `security-rbac-design` (fine-grained authz
& policy-as-code — pick the model that fits your stack), `api-webhook-design`, `api-rate-limiting`,
`microservices-api-gateway`, `api-idempotency-keys`, and `security-questionnaire-responder`
(the recurring SIG/CAIQ/VSA grind). *`workos-enterprise-auth` fetches live WorkOS docs via WebFetch.*

**Compliance-as-code** — `soc2`, `iso-27001`, `gdpr`, `hipaa`, `pci-dss` (controls, evidence,
policy templates). For an alternative ReBAC engine, SpiceDB's `authzed/authzed-marketplace` is
one clone away; for transcript-driven MEDDPICC, `extruct-ai/gtm-cowork-skills` is enable-only (no license).

> **Not duplicated:** `code-review`, `security-review`, and `simplify` ship natively with
> Claude Code — use those directly.

ECC-sourced skills have been **de-branded** (ECC-specific defaults, tool references, and
personal-voice samples removed). Attribution and licenses for everything vendored are in
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

---

## Maintaining the toolkit

Every maintenance command is **stdlib-only and read-only** — they report, they never commit
or push. `release.py` writes files, then prints the exact `git commit`, `git tag` and `git push`
for you to run by hand (the tag is created after the release commit so it points at it).

- **Health-check** — `python3 scripts/doctor.py` (or the **`/doctor`** command) checks your
  settings, plugins, marketplace, and optional tools, printing the inline fix for each issue.
- **Upstream drift** — `python3 scripts/check_upstream.py` `git ls-remote`s every source in
  `THIRD_PARTY_SOURCES.json` and flags vendored skills that have drifted from their recorded
  upstream HEAD. The **`upstream-drift.yml`** Action runs this weekly and upserts a single
  rolling **"Upstream drift report"** issue.
- **Release** — `python3 scripts/release.py --bump <level>` is the one-command release: it
  bumps the version and promotes the `[Unreleased]` CHANGELOG block into the new section — then
  prints the commit/tag/push commands. It **never commits, tags, or pushes**. Add `--dry-run` to preview. Pushing the `vX.Y.Z`
  tag triggers `release.yml`, which publishes the GitHub Release.
- **Skill usage** — `python3 scripts/skill_usage.py --days 30` reads your local Claude Code
  transcripts and reports which skills fired, which vendored skills never did (largest
  description first — that is the always-on context cost), and enabled plugins with zero use.
  `--prune-list` prints never-invoked directory names for a manual prune; nothing is deleted.
  A local stand-in for `/skill-doctor` when usage reports are unavailable on your connection.
- **Eval secret** — `bash scripts/set_eval_secret.sh` stores the `ANTHROPIC_API_KEY` repo secret
  for `plugin-eval.yml` (prompts with hidden input, pipes to `gh secret set`, never in argv).
- **Validate** — `validate_skills.py` (skills + `SKILLS.md` catalog) and `validate_assets.py`
  (`agents/`, `workflows/`) gate every change; both also run in CI.

**Authoring a new skill** — follow the `writing-for-agents` skill from the enabled
`mattpocock-skills` plugin (context pointers, the two loads, information hierarchy, leading
words, no-op pruning). It is the house standard for any SKILL.md written or adapted here.

**Refreshing a vendored skill** — vendored skills are point-in-time snapshots. Re-copy the
directory from upstream and re-apply de-branding (drop `metadata.origin: ECC`, strip ECC
tool/skill cross-references). For fast-moving upstreams (Vercel, Addy, Anthropic, ui-ux-pro-max)
prefer the *enabled-plugin* tier over vendoring so they stay current automatically.

## Layout

```
bharats-claude-toolkit/
├── .claude-plugin/
│   ├── plugin.json          # this plugin's manifest
│   └── marketplace.json     # one-plugin marketplace (name: bharats-claude-toolkit-dev)
├── skills/{toolkit,doctor,team}/  # user-invoked skills behind /toolkit, /doctor, /team
├── output-styles/toolkit.md # optional output style: intent line, evidence, stand-alone recap
├── evals/                   # `claude plugin eval` cases
├── scripts/
│   ├── check_upstream.py    # report vendored-skill drift vs THIRD_PARTY_SOURCES.json
│   ├── doctor.py            # health-check settings/plugins/tools (backs /doctor)
│   ├── validate_assets.py   # validate agents/, workflows/ assets
│   └── release.py           # bump version + promote CHANGELOG [Unreleased] (no commit/tag/push)
├── .github/workflows/
│   ├── upstream-drift.yml   # weekly cron → rolling "Upstream drift report" issue
│   └── release.yml          # pushed vX.Y.Z tag → published GitHub Release
├── settings.json            # template to merge into ~/.claude/settings.json
├── skills/<name>/SKILL.md   # vendored skills
├── agents/<name>.md         # vendored agents
├── CLAUDE.md                # repo facts (commands, release, gotchas); user rules in templates/
├── templates/user-CLAUDE.md # installed to ~/.claude/CLAUDE.md by bootstrap
├── .claude/rules/           # path-scoped rules (skills, hooks+scripts, agents)
├── THIRD_PARTY_NOTICES.md   # attribution + licenses
└── README.md
```
