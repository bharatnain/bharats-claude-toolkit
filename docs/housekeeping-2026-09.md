# Housekeeping backlog — September 2026 refresh

Produced 2026-09-22 by a four-teammate sweep (model lineup research, Claude Code platform
research, marketplace/vendored-upstream drift research, repo staleness audit). Items already
applied in the same sweep are listed at the bottom; everything above it is **open** and
ordered by impact. Re-run this sweep when Claude Sonnet 5.5 / Haiku 5.5 ship (announced
"in the coming weeks" on 2026-09-22 — no IDs, prices, or dates yet).

Ground truth at sweep time: Claude Code **2.1.280** (Opus 5.5 is the default `opus`);
models **Fable 5.1** (`claude-fable-5-1`), **Opus 5.5** (`claude-opus-5-5`, GA 2026-09-22),
**Opus 5**, **Sonnet 5** (`claude-sonnet-5`, $2/$10 permanent), **Haiku 4.5**
(`claude-haiku-4-5`). Opus 4.1 retired 2026-08-05. Sonnet 4.5's earliest retirement date
(2026-09-29) is a week out with no notice posted — watch the deprecations page.

## P1 — do next

1. **Cut release 0.9.0.** `[Unreleased]` holds two Aug-2026 waves (18 skills, roster
   change, hooks hardening, mattpocock) plus this sweep; `plugin.json` is still 0.8.1 and
   **0.8.1 was never tagged** (only `v0.8.0` exists, so no GitHub Release for it).
   Blocker first: `scripts/release.py` `insert_changelog_section` inserts the new
   `## [X.Y.Z]` block *above* `## [Unreleased]`, stranding its bullets — fix it to promote
   the Unreleased block (or promote manually), then `python3 scripts/release.py --bump minor`.
   Also align `RESYNC_LINE` wording ("`/reload-plugins`") with the CHANGELOG's
   "fully quit and reopen" guidance.
2. **Re-vendor the 5 GRC skills** (`soc2`, `iso-27001`, `gdpr`, `hipaa`, `pci-dss`) from
   Sushegaad v2.0.0 — "September 2026 regulatory changes reflected" (adds UK Cyber Essentials,
   SOX ITGC, TPRM, EU CRA, DORA, CMMC upstream). Stale compliance content is actively harmful.
   Re-apply the Phase B/D description + dead-link edits, then bump its SHA in
   `THIRD_PARTY_SOURCES.json`.
3. **Decide the agent-teams gates.** `TaskCreated` / `TaskCompleted` / `TeammateIdle` are
   still *documented, experimental* events behind `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
   (verified 2026-09-22), so the wiring in `hooks/hooks.json` + `hooks/team_gate.py` is not
   dead — but the payload field names (`task.acceptance_criteria`, etc.) were inferred and
   `docs/agent-teams-probe.md` has never been run. Either run the probe once
   (`GATE_HOOK_DEBUG=1`) and pin the fields, or remove the three registrations, the
   `team_gate.py` branches, README §"Experimental: agent-teams gates" and the probe doc.
   `agent-teams@claude-code-workflows` stays **disabled**: upstream still calls `TeamCreate`
   in 5 files (last touched 2026-08-15).
4. **Set an ecc drift policy.** 22 of 26 ecc-derived skills and all 4 ecc-derived agents
   changed upstream (626 commits; upstream is now a 292-skill "harness-native operator
   layer"). Options: (a) record "intentionally frozen" in the manifest, or (b) targeted
   re-pull of the workflow-critical set only — `tdd-workflow`, `verification-loop`,
   `eval-harness`, `production-audit`, `python-patterns`, `python-testing`,
   `fastapi-patterns`, `postgres-patterns`. Full re-sync is not worth the edit-reapply cost.

## P2 — this quarter

5. **Selective re-pull from marketingskills** (18 of 26 drifted; biggest: `ai-seo` 2.5.0,
   `ads`, `ad-creative`, `pricing`, `onboarding`, `public-relations`, `social`). Upstream
   now runs a paid "Skill Partner" program (Converly, Ploy) — audit re-pulled bodies for
   partner/affiliate links, and consider adding a partner-link check to
   `scripts/validate_skills.py`.
6. **Re-pull `workos-enterprise-auth`** (0.7.3: AuthKit sign-out / initiate-login
   requirements, SvelteKit fixes) and **`hallmark`** (new Grid theme) — small, low-risk;
   re-neutralize hallmark's upstream-escaping links (commit 5133db9 pattern).
7. **Verify the mattpocock subscription.** Tag is still v1.2.3 but HEAD is 54 commits past
   it: skills reorganised into `engineering/ productivity/ misc/`, new `implement-spec`,
   `retro`, `wait-what`, `grill-with-docs`; "stop skills from calling other user-invoked
   skills". Users already get this (source is unpinned). Confirm the README's
   `writing-for-agents` house-standard reference still resolves; consider mentioning the
   new skills in the README bullet.
8. **Note the superpowers 6.4.1 behaviour change** in `team-orchestration` / README:
   `executing-plans` no longer pauses for review mid-plan ("Native execution");
   `diagnosing-superpowers` is a new debugging entrypoint.
9. **Re-verify `team-orchestration` hard-coded limits** (depth 3, 20 concurrent / 200 per
   session, `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` / `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`,
   "v2.1.198+") against current docs via the `claude-code-docs` skill; drop version
   qualifiers. Same for `docs/hooks-security.md` §3 (v2.1.207/214 constraints — add a
   "verified against" date and re-run the audit on 2.1.280).
10. **Evaluate official first-party plugins** now in `claude-plugins-official`:
    `claude-security` (in-session vuln scanning), `skill-creator`, `session-report`,
    `hookify`, `code-review`, `pr-review-toolkit`, `remember`. The official marketplace
    also hosts SHA-pinned `superpowers` and `mattpocock-skills` — a consolidation path that
    would drop two `extraKnownMarketplaces` entries at the cost of Anthropic's bump cadence.
11. **Run `/skill-doctor` once** (2.1.261+) — 7-day context-cost + never-invoked report —
    and prune or demote unused vendored skills. Related: 34 `SKILL.md` files exceed 15 k
    chars (hallmark 67 k, dcf-model 50 k, vuln-triage 44 k, expansion-business-case 37 k,
    comps-analysis 29 k, launch-your-agent 29 k …) — split bodies into `references/`,
    prioritising first-party/diverged ones.
12. **Refresh `hooks/secret_scan.py` patterns** (2024-era set). Missing: OpenAI
    `sk-proj-…`, npm `npm_…`, PyPI `pypi-…`, Hugging Face `hf_…`, SendGrid `SG.…`, Twilio,
    Azure/GCP service-account JSON, 40-char AWS secret keys, Vercel/Netlify/Cloudflare
    tokens — or defer to a maintained rule set (gitleaks).
13. **Hook cleanup.** Drop `MultiEdit` from both `hooks.json` matchers and the
    `secret_scan.py` branch (tool no longer exists; harmless but dead). Align
    `team_gate.py`'s `TeammateIdle` branch (exit-2 stderr "steer") with
    `verification-loop`'s own guidance to prefer `additionalContext`.
14. **Bookkeeping SHA bumps still pending** for sources with partial drift once their changed
    skills are reviewed: `alirezarezvani/claude-skills` (only `executive-mentor`,
    `general-counsel-advisor` changed), `intense-visions/harness-engineering` (only
    `api-idempotency-keys`), `t0ddc3by/claude-for-customer-success` (`churn-analysis`,
    `churn-rca` — packaging only), `nizos/probity` (skim `tdd-workflow`'s "Automated
    Enforcement (probity)" section against the new setup docs).

## P3 — when convenient

15. **README truth-ups.** Option B manual fallback (lines ~82-105) lists 7 of 13
    marketplaces and 9 of 27 plugins — mark it abridged or generate it from
    `settings.json`. Three separate "agent-teams removed in v2.1.178" warnings — keep one.
    Verify the "ship natively with Claude Code" list (`deep-research`, `verify` are not
    visible as native skills today; `code-review`, `security-review`, `simplify` are).
    Drop the "now" from "superpowers … now enabled by default".
16. **`THIRD_PARTY_NOTICES.md` "referenced but NOT vendored" list** omits
    `mattpocock-skills`, `security-guidance`, `plugin-dev`, the three Trail of Bits plugins,
    `probity`, `memsearch`, `openai-codex` — add them with licences.
17. **Supply-chain follow-through** (`docs/supply-chain.md` advocates it, the repo doesn't
    do it): SHA-pin `actions/checkout@v4` / `setup-python@v5` in the four workflows; adopt
    SHA pins for `extraKnownMarketplaces`; `bootstrap.sh` / `doctor.py` curl-pipe-bash the
    beads installer from unpinned `main`.
18. **Plugin manifest modernisation.** `plugin.json` could declare `workflows`,
    `defaultEnabled`, `metadata.catalogId`; add an `evals/` directory so
    `claude plugin eval` can run in CI (`.github/workflows/`).
19. **Launch-your-agent CMA capability gates** to re-verify against current Managed Agents
    docs: `cma-primitives.md` says `system.message` is "Opus 4.8 only" and memory
    consolidation supports "opus-4-8/4-7, sonnet-4-6" — likely broader now.
20. **Skill-name overlap pass** (17 pairs; listed, not judged): `pricing`/`pricing-strategist`,
    `competitors`/`competitor-profiling`/`competitive-intel`, `churn-analysis`/`churn-rca`,
    `cro`/`cro-advisor`, `onboarding`/`onboarding-plan`, `content-engine`/`content-strategy`,
    `copywriting`/`copy-editing`, `renewal-forecast`/`renewal-readiness`,
    `expansion-signal`/`expansion-business-case`, `deal-desk`/`deal-review-framework`,
    `motion-foundations`/`motion-patterns`, `react-patterns`/`react-best-practices`,
    `python-patterns`/`python-testing`, `sales-forecast-builder`/`commercial-forecaster`,
    `market-research`/`research-ops`/`customer-research`, `seo-audit`/`ai-seo`,
    `security-questionnaire-responder`/`rfp-responder`. Extend the cross-reference pattern
    already used by `pricing` / `market-research` / `copywriting`.
21. **Cosmetic.** `skills/react-best-practices` frontmatter `name:` is
    `vercel-react-best-practices` (documented as intentional; Claude Code exposes the
    directory name). Eight `skills/code-migration/prompts/*.md` sample log rows still show
    `claude-sonnet-4-6` — illustrative, bulk-sed if you want examples to look current.
22. **Candidate additions to watch** (not evaluated): `dmmulroy/anti-slop`,
    `miqdadbadjuber/anti-slop`, `Nanako0129/sepia` (de-AI writing — overlaps
    `avoid-ai-writing` / `humanizer`), `GoogleChrome/modern-web-guidance` (overlaps
    `web-quality-skills`), `video-shotcraft`, `lieflat-charts`. `trailofbits/skills-curated`
    has been dormant since July (security-awareness still fine); `openai/codex-plugin-cc`
    quiet since July.
23. **Local machine, not repo:** the CLI reports 2.1.92 while the desktop app bundles
    2.1.280 — run `claude update`.

## Applied in this sweep (2026-09-22)

- Model defaults: `cost-aware-llm-pipeline` constants → `claude-sonnet-5` / `claude-haiku-4-5`,
  pricing table re-cached Sep 2026 with Sonnet 5 / Opus 5.5 / Fable 5.1, cache-minimum prose
  updated; `launch-your-agent` example slugs `claude-opus-4-8` → `claude-opus-5-5` and the
  fast-mode model list corrected (Opus 5.5 / Opus 5 / Opus 4.8; Opus 4.7 errors).
- `references/claude-api/{models,model-migration,prompt-caching}.md` re-vendored from the
  `claude-api` skill bundled with Claude Code 2.1.280, with a dated freshness banner
  (Opus 5.5 GA; Opus 4.1 retired).
- Count/contradiction fixes: README "other 25 plugins", superpowers no longer described as
  on-demand (README tier table, bootstrap paragraph, THIRD_PARTY_NOTICES); `commands/toolkit.md`
  headline 26 / 134 / 8; `docs/hooks-security.md` "eleven hook registrations".
- Claude Code naming: "Task tool" → "Agent tool" in `threat-model/bootstrap.md` and
  `context-budget/SKILL.md`; dropped the "(v2.1.163+)" qualifier in `verification-loop`.
- Hygiene: removed the dead `scripts/db-probe.sh` permission from `settings.json`;
  `.gitignore` gains `.claude/team-profile.json`, `__pycache__/`, `*.pyc`, `.pytest_cache/`.
- Manifest: `first_party` now lists `claude-code-docs`, `startup-idea-evaluation`,
  `team-orchestration` (also added to THIRD_PARTY_NOTICES); `upstream_head_at_manifest`
  re-recorded for the 7 sources whose vendored directories were unchanged upstream
  (vercel-labs, OneWave, openfga, anthropics/skills, knowledge-work-plugins,
  financial-services, defending-code-reference-harness), and the manifest `_comment`
  says so.
