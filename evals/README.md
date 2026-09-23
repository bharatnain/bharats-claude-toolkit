# Plugin evals

Test cases for `claude plugin eval` (Claude Code 2.1.269+). Each case directory holds a
`prompt.md` (frontmatter + prompt) and `graders/*.md` (regex / tool_used / tool_order /
file_exists / llm / baseline). Run locally from the repo root:

```bash
claude plugin eval . --json evals/results/latest.json --threshold 0.8 --trust-plugin
```

Exit 0 means every case scored at or above the threshold. Runs cost API tokens, so CI
runs only on manual dispatch (`.github/workflows/plugin-eval.yml`) with an
`ANTHROPIC_API_KEY` secret. `evals/results/` is git-ignored.
