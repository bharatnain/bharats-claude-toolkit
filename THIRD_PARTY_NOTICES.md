# Third-Party Notices

This toolkit **vendors** (copies in) skills and agents from the projects below. Their
original licenses and copyright notices are reproduced (MIT) or retained in-tree
(Apache-2.0) as required.

Skills and agents adapted from ECC have had ECC-specific defaults, tool references, and
branding removed. The underlying technical guidance remains the original authors' work.

**Local modifications:** vendored skills carry local edits — descriptions were disambiguated
for reliable auto-triggering, and dead cross-references (to external tool registries and
un-vendored sibling plugins) were neutralized. Per-source upstream repos, licenses, and the
upstream HEAD SHA recorded at divergence are tracked in
[`THIRD_PARTY_SOURCES.json`](THIRD_PARTY_SOURCES.json) for deterministic refresh.

---

## MIT-licensed components

The following vendored components are licensed under the MIT License.

### ECC — https://github.com/affaan-m/ecc
Copyright (c) 2026 Affaan Mustafa

- Skills: `agentic-engineering`, `article-writing`, `brand-voice`, `codebase-onboarding`,
  `content-engine`, `context-budget`, `cost-aware-llm-pipeline`, `design-system`, `eval-harness`,
  `fal-ai-media`, `fastapi-patterns`, `make-interfaces-feel-better`, `market-research`,
  `motion-foundations`, `motion-patterns`, `postgres-patterns`, `production-audit`,
  `python-patterns`, `python-testing`, `react-patterns`, `remotion-video-creation`, `repo-scan`,
  `research-ops`, `tdd-workflow`, `verification-loop`, `video-editing`
- Agents: `architect`, `planner`, `code-architect`, `spec-miner`

### Corey Haines marketing skills — https://github.com/coreyhaines31/marketingskills
Copyright (c) 2025 Corey Haines

- Skills: `copywriting`, `copy-editing`, `content-strategy`, `onboarding`, `seo-audit`, `ai-seo`,
  `customer-research`, `competitor-profiling`, `competitors`, `product-marketing`,
  `launch`, `sales-enablement`, `pricing`, `ads`, `ad-creative`, `emails`, `social`, `cro`,
  `analytics`, `referrals`, `public-relations`, `marketing-psychology`, `lead-magnets`,
  `prospecting`, `cold-email`, `revops`

### UX Writing — https://github.com/content-designer/ux-writing-skill
Copyright (c) 2026 Christopher Greer

- Skill: `ux-writing`

### Vercel agent skills — https://github.com/vercel-labs/agent-skills
Copyright (c) Vercel, Inc.

- Skill: `react-best-practices` (frontmatter name: `vercel-react-best-practices`)

### FFmpeg skill — https://github.com/ychoi-kr/claude-ffmpeg-skill
Copyright (c) the claude-ffmpeg-skill authors

- Skill: `ffmpeg-usage`

### Alireza Rezvani — business & C-suite skills — https://github.com/alirezarezvani/claude-skills
Copyright (c) 2025 Alireza Rezvani

- Commercial: `pricing-strategist`, `deal-desk`, `commercial-forecaster`, `commercial-policy`,
  `partnerships-architect`, `channel-economics`, `rfp-responder`
- C-suite advisory: `board-deck-builder`, `executive-mentor`, `ceo-advisor`, `cfo-advisor`,
  `cro-advisor`, `cmo-advisor`, `cpo-advisor`, `general-counsel-advisor`, `competitive-intel`,
  `ma-playbook`, `scenario-war-room`, `agent-protocol`
- Business operations: `procurement-optimizer`, `process-mapper`, `vendor-management`

### OneWave AI — enterprise sales skills — https://github.com/OneWave-AI/claude-skills
Copyright (c) 2025 OneWave AI

- Skills: `sales-methodology-implementer`, `deal-review-framework`, `sales-forecast-builder`,
  `pipeline-health-analyzer`, `quota-setting-calculator`, `territory-planning-optimizer`,
  `sales-comp-plan-designer`, `objection-pattern-detector`

### WorkOS — enterprise identity skill — https://github.com/workos/skills
Copyright (c) 2026 WorkOS

- Skill: `workos-enterprise-auth` (SSO/SAML, SCIM directory sync, RBAC, audit logs, AuthKit;
  fetches live WorkOS docs via WebFetch at runtime)

### Void3110 — OPA/Rego policy-as-code skill — https://github.com/Void3110/rego-skill
Copyright (c) 2026 Void3110

- Skill: `rego-skill`

### Intense Visions, Inc. — API & RBAC engineering skills — https://github.com/intense-visions/harness-engineering
Copyright (c) 2026 Intense Visions, Inc.

- Skills: `security-rbac-design`, `api-webhook-design`, `api-rate-limiting`,
  `microservices-api-gateway`, `api-idempotency-keys` (vendored from `agents/skills/claude-code/`)

### Hemant Naik — compliance-as-code skills — https://github.com/Sushegaad/Claude-Skills-Governance-Risk-and-Compliance
Copyright (c) 2026 Hemant Naik

- Skills: `soc2`, `iso-27001`, `gdpr`, `hipaa`, `pci-dss` (extracted from upstream `.skill` archives)

### Hallmark — https://github.com/Nutlope/hallmark
Copyright (c) 2026 Hallmark contributors

- Skill: `hallmark`

### Probity — https://github.com/nizos/probity
Copyright (c) 2026 Nizar Selander

- Skill: `tdd-workflow` — the "Automated Enforcement (probity)" section adapts the TDD
  judging rules from `src/rules/enforce-tdd.ts` (`DEFAULT_TDD_RULES` / `PROCESS_INSTRUCTIONS`).
  Probity itself is not vendored; it is registered as an installable marketplace in
  `settings.json` and installs its own `PreToolUse` hook when enabled.

### MIT License text

The MIT terms below apply to each MIT-licensed component listed above, with its
respective copyright holder:

```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Apache-2.0-licensed components

### Anthropic skills — https://github.com/anthropics/skills
- Skills: `theme-factory`, `brand-guidelines`, `mcp-builder`

Each retains its original Apache License 2.0 in its own directory
(`skills/theme-factory/LICENSE.txt`, `skills/brand-guidelines/LICENSE.txt`, `skills/mcp-builder/LICENSE.txt`).
Licensed under the Apache License, Version 2.0 — https://www.apache.org/licenses/LICENSE-2.0

> Note: Anthropic's document skills (`docx`, `pdf`, `pptx`, `xlsx`) are source-available,
> **not** open source, and are intentionally **not** vendored here. They are available
> natively in Claude Code regardless.

### Anthropic skills — https://github.com/anthropics/skills (claude-api reference files)

- Reference files: `skills/cost-aware-llm-pipeline/references/claude-api/`
  (`models.md`, `model-migration.md`, `prompt-caching.md`) — vendored from the upstream
  `claude-api` skill's `shared/` directory (not a full-skill vendor; the full claude-api
  skill ships built into Claude Code and is intentionally not vendored here).

Retains the original Apache License 2.0 as
`skills/cost-aware-llm-pipeline/references/claude-api/LICENSE.txt`.
Licensed under the Apache License, Version 2.0 — https://www.apache.org/licenses/LICENSE-2.0

### SuccessCOACHING — enterprise customer-success skills — https://github.com/t0ddc3by/claude-for-customer-success
Copyright 2026 SuccessCOACHING

- Skills: `qbr-builder`, `health-score-review`, `renewal-readiness`, `renewal-forecast`,
  `churn-analysis`, `churn-rca`, `expansion-business-case`, `expansion-signal`,
  `success-plan-builder`, `onboarding-plan`, `kickoff-prep`, `ttv-analysis`

Each retains the original Apache License 2.0 as `LICENSE.txt` in its own skill directory.
(GitHub's API mislabels the repo `NOASSERTION`; the in-repo `LICENSE` is verbatim Apache 2.0.)

### OpenFGA — fine-grained authorization skill — https://github.com/openfga/agent-skills
- Skill: `openfga` (ReBAC/Zanzibar modeling: types, relations, tuples, CEL/ABAC conditions, `.fga.yaml` tests)

Retains the original Apache License 2.0 as `skills/openfga/LICENSE.txt`.

### Anthropic defending-code reference harness — https://github.com/anthropics/defending-code-reference-harness
Copyright 2026 Anthropic PBC

- Skills: `threat-model`, `vuln-scan`, `vuln-triage` (upstream `triage`), `vuln-patch`
  (upstream `patch`), `dnr-hunt`, `dnr-respond`
- Shared helper: `skills/_lib/checkpoint.py` and `skills/_lib/test_checkpoint.py`
  (upstream `.claude/skills/_lib/checkpoint.py` and `tests/test_skill_checkpoint.py`)

Each retains the original Apache License 2.0 as `LICENSE.txt` in its own skill directory,
and in `skills/_lib/`. Scripts keep their upstream SPDX headers.

Local modifications: `triage` → `vuln-triage` and `patch` → `vuln-patch` (renamed to avoid
colliding with the product-management `triage-requests` skill), with every cross-skill
handoff reference, state directory, and invocation string updated; the repo-specific
`vuln-pipeline` CLI delegation path removed (`vuln-patch` is static-review-only); the
`dnrcanary` demo target and its grader removed from the D&R skills; and the checkpoint
helper re-pointed from `.claude/skills/_lib/` to `skills/_lib/`.

### Anthropic — Claude for Legal — https://github.com/anthropics/claude-for-legal
Copyright Anthropic

- Skill: `advisor-profile` (the `commercial-legal` cold-start interview + shared company-profile
  template, genericized from a legal practice profile into the persistent company/advisor
  context profile read by the C-suite advisor skills)
- References vendored under `skills/general-counsel-advisor/references/contract-review/`:
  contract-review routing, `nda-review` (GREEN/YELLOW/RED triage), `vendor-agreement-review`,
  `saas-msa-review`, and the `deal-debrief` / `playbook-monitor` agent workflows
  (deviation-log → playbook-amendment loop)

Retains the original Apache License 2.0 as `skills/advisor-profile/LICENSE.txt` and
`skills/general-counsel-advisor/references/contract-review/LICENSE.txt`. Local adaptations:
upstream plugin-config paths replaced with the toolkit's `company-context.md` profile, upstream
slash-commands neutralized, and matter-workspace/connector machinery not present in this
toolkit removed.

### Anthropic — Claude for Financial Services (Model Builder skills) — https://github.com/anthropics/financial-services
- Skills: `dcf-model`, `audit-xls`, `3-statement-model`, `comps-analysis`, `lbo-model`
  (vendored from `plugins/vertical-plugins/financial-analysis/skills/`)

Each retains the original Apache License 2.0 as `LICENSE.txt` in its own skill directory.
Licensed under the Apache License, Version 2.0 — https://www.apache.org/licenses/LICENSE-2.0

### Anthropic — Claude Code Migration Kit — https://github.com/anthropics/code-migration-kit-with-claude-code
Copyright 2026 Anthropic PBC

- Skill: `code-migration` (prompts, templates, dependency-map/queue/build scripts, fixtures, and the kit's operating manual vendored as `references/kit-orientation.md`)

Retains the original Apache License 2.0 as `skills/code-migration/LICENSE.txt`; scripts keep their upstream SPDX headers.
Licensed under the Apache License, Version 2.0 — https://www.apache.org/licenses/LICENSE-2.0

> Note: the upstream kit's `examples/` directory (a complete example run) is intentionally not vendored.

### Anthropic — launch-your-agent (Claude Managed Agents scaffolding) — https://github.com/anthropics/launch-your-agent
Copyright 2026 Anthropic PBC

- Skills: `launch-your-agent` (the repo-root `cma-primitives.md` inventory is vendored into its
  `references/`), `agent-wrap-up` (upstream `.claude/skills/wrap-up`, renamed to avoid a
  generic `wrap-up` trigger)

Each retains the original Apache License 2.0 as `LICENSE.txt` in its own skill directory,
and SPDX headers are kept on all vendored files. Upstream explicitly invites vendoring.

### Anthropic knowledge-work-plugins — plugin review policy — https://github.com/anthropics/knowledge-work-plugins
- Skill: `plugin-vetting` (LLM-judge plugin/marketplace security-review policy and structured verdict schema, vendored from the repo's `.github/policy/` into `skills/plugin-vetting/references/`)

Retains the original Apache License 2.0 as `skills/plugin-vetting/LICENSE.txt`.

---

## First-party skills

Authored for this toolkit (not third-party), MIT-licensed under this repo:

- `security-questionnaire-responder` — recurring vendor-security-questionnaire (SIG/CAIQ/VSA)
  workflow with an evidence-mapped answer library; complements `rfp-responder` and the compliance skills.

---

## Plugins referenced but NOT vendored

These are installed/enabled as upstream plugins (see `README.md`), so their code is not
copied into this repo and stays auto-updated from source:

- `frontend-design` — Anthropic, `claude-plugins-official`
- `ui-ux-pro-max` — https://github.com/nextlevelbuilder/ui-ux-pro-max-skill (MIT)
- `web-quality-skills` — https://github.com/addyosmani/web-quality-skills (MIT)
- `pm-skills` (`pm-product-discovery`, `pm-product-strategy`, `pm-execution`, …) — https://github.com/phuryn/pm-skills (MIT) — enabled
- `claude-code-workflows` (`agent-teams`, `agent-orchestration`, `conductor`, role bundles) — https://github.com/wshobson/agents (MIT) — enabled
- `ecc` — https://github.com/affaan-m/ecc (MIT) — registered, on-demand
- `superpowers` / `elements-of-style` — https://github.com/obra/superpowers-marketplace (MIT) — registered, on-demand
- `beads` (`bd`) — https://github.com/steveyegge/beads — agentic issue tracker; the **default task store** for the toolkit. `bootstrap.sh` auto-installs the CLI (non-blocking), a `SessionStart` hook runs `bd init` per git repo, and workflows/teams persist tasks to it — all opt-out via `CLAUDE_BEADS=off`, with the native Task tools as the fallback. Integrated as **CLI only** (MCP deferred). **License unverified → integrated by reference, NOT vendored**; it is therefore intentionally absent from `THIRD_PARTY_SOURCES.json` (that manifest tracks vendored skills for upstream refresh).
