---
paths: ["agents/**"]
---

# Agents contract

- Express behaviour through frontmatter (`effort`, `tools`, `permissionMode`, `memory`, `omitClaudeMd`), not prose; "Effort: high" in the body does nothing.
- No boilerplate defense blocks; guardrails live in hooks and `permissions`.
- `description` states the use case first, then when to use the agent.
- Reviewers may run the project's verification commands read-only and report only gaps that affect correctness or the stated acceptance criteria; everything else goes under an "Optional" heading and never fails the review.
