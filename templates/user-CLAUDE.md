# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

## Model routing

The main session plans, decides and reviews. Cheaper models do the reading and the typing.

- Name a model on every Agent call. An unnamed dispatch runs on Sonnet (`CLAUDE_CODE_SUBAGENT_MODEL`); built-in Explore and Plan inherit the session model unless you pass one.
- Reading, search, log or doc triage: Explore with `model: haiku`. Ask for conclusions with file:line pointers, never file dumps.
- Web research: one agent per question on `sonnet` (`haiku` for fetch-and-extract). Findings go to a file; the reply stays under 10 lines.
- Implementing a complete spec or brief: `sonnet`. The same mechanical edit across many files: one `haiku` agent with the whole list.
- A substantial, well-bounded coding task with its own tests: delegate to Codex through `codex:codex-rescue` (background; `--cwd <worktree>` when other agents edit the same tree). Review its diff like any teammate's.
- Diff review: `sonnet` for small mechanical diffs; `opus` for security, concurrency, data migrations, public interfaces and whole-branch reviews. Add `/codex:adversarial-review` on risky changes: a second model family catches different mistakes.
- Architecture, design and hard debugging: `opus`. Use `fable` only after `opus` has failed at it, or when asked.
- Edit directly only when the change is a few lines in files already in context.
- Codex models, passed as `--model`: `sol` = `gpt-6.1-sol` (default for delegated coding), `luna` = `gpt-6-luna` (fast, high-volume), `astra` = `gpt-6-astra` (hardest work). Codex runs on the ChatGPT plan, not Claude limits. If an id is rejected or Codex is not set up, run `/codex:setup` and fall back to `sonnet`.

## Compaction

When compacting, preserve: the list of files modified this session, the last validator/test results, open task ids, and any decision stated exactly.

## Unrequested findings

Report out-of-scope problems as follow-ups in your summary; do not fix them unless asked.
