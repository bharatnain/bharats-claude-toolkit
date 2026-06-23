# Third-Party Notices

This toolkit **vendors** (copies in) skills and agents from the projects below. Their
original licenses and copyright notices are reproduced (MIT) or retained in-tree
(Apache-2.0) as required.

Skills and agents adapted from ECC have had ECC-specific defaults, tool references, and
branding removed. The underlying technical guidance remains the original authors' work.

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
- `beads` (`bd`) — https://github.com/steveyegge/beads — agentic issue tracker; integrated as CLI + plugin/MCP (license unverified → integrated, not vendored)
