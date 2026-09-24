---
paths: ["skills/**"]
---

# Skills contract

Frontmatter:
- `name` equals the directory name.
- `description`: 40–1024 chars; the key use case first, then when to use. `description` + `when_to_use` together ≤ 1,536 chars.
- `when_to_use` holds trigger phrases, not prose.
- `disable-model-invocation: true` on user-invoked tiers (no listing cost until `/name`).
- `paths:` on file-scoped skills; `context: fork` on research-heavy skills.
- `metadata.source` records vendored provenance.

Body:
- `SKILL.md` under 500 lines; long material goes in `references/`.
- No links that escape the skill directory; neutralize them when vendoring.
- No partner or affiliate links.
- A user-invoked skill never calls another user-invoked skill.
- Cross-reference sibling skills by name in plain text, not by path or link.
