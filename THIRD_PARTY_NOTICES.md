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
  `content-engine`, `design-system`, `fastapi-patterns`, `make-interfaces-feel-better`,
  `market-research`, `motion-foundations`, `motion-patterns`, `postgres-patterns`, `production-audit`,
  `python-patterns`, `python-testing`, `react-patterns`, `repo-scan`, `research-ops`,
  `tdd-workflow`, `verification-loop`
- Agents: `architect`, `planner`, `code-architect`, `spec-miner`

### Corey Haines marketing skills — https://github.com/coreyhaines31/marketingskills
Copyright (c) 2025 Corey Haines

- Skills: `copywriting`, `copy-editing`, `content-strategy`, `onboarding`, `seo-audit`, `ai-seo`,
  `customer-research`, `competitor-profiling`, `competitors`, `product-marketing`

### UX Writing — https://github.com/content-designer/ux-writing-skill
Copyright (c) 2026 Christopher Greer

- Skill: `ux-writing`

### Vercel agent skills — https://github.com/vercel-labs/agent-skills
Copyright (c) Vercel, Inc.

- Skill: `react-best-practices` (frontmatter name: `vercel-react-best-practices`)

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
- Skills: `theme-factory`, `brand-guidelines`

Each retains its original Apache License 2.0 in its own directory
(`skills/theme-factory/LICENSE.txt`, `skills/brand-guidelines/LICENSE.txt`).
Licensed under the Apache License, Version 2.0 — https://www.apache.org/licenses/LICENSE-2.0

> Note: Anthropic's document skills (`docx`, `pdf`, `pptx`, `xlsx`) are source-available,
> **not** open source, and are intentionally **not** vendored here. They are available
> natively in Claude Code regardless.

---

## Plugins referenced but NOT vendored

These are installed/enabled as upstream plugins (see `README.md`), so their code is not
copied into this repo and stays auto-updated from source:

- `frontend-design` — Anthropic, `claude-plugins-official`
- `ui-ux-pro-max` — https://github.com/nextlevelbuilder/ui-ux-pro-max-skill (MIT)
- `web-quality-skills` — https://github.com/addyosmani/web-quality-skills (MIT)
- `ecc` — https://github.com/affaan-m/ecc (MIT) — registered, on-demand
- `superpowers` / `elements-of-style` — https://github.com/obra/superpowers-marketplace (MIT) — registered, on-demand
