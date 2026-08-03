---
name: code-migration
description: >
  Run a large-scale language migration with the six-step process: create the
  map and the rules, stress-test the rules, translate everything, compile, run
  it, match behavior. Use when the user wants to migrate, port, or rewrite a
  codebase from one language to another ("migrate this to Rust", "port our
  Python CLI to TypeScript", "should we rewrite this in Go?"), or asks for a
  migration feasibility assessment. Not for incremental JS→TS adoption — that
  needs no machinery — or single-file conversions.
---

# Code migration (six-step process)

You are orchestrating a language migration using the Claude Code Migration
Kit, vendored in this skill's directory (the directory containing this
SKILL.md — referred to below as the kit directory; all `prompts/`,
`templates/`, and `scripts/` paths are relative to it). `README.md` there
defines the process; `references/kit-orientation.md` defines your standing
rules — read both before acting. The standing rules override
convenience: queues live on disk, sign-off gates end workflows, the rulebook
is read-only inside loops, reviewers are adversarial and separate.

## Routing

1. **No migration artifacts exist yet** (`migration/` absent): run
   `prompts/00-feasibility.md`. Produce the report, deliver the verdict, STOP.
   Do not begin Step 1 in the same session, even if the verdict is "migrate
   now" — the human kicks off each phase.
1b. **Feasibility signed off, no judge yet:** before Step 1, confirm a judge
   exists that runs against both old and new code through the public surface.
   If the existing suite is public-surface (or already in a third language),
   it's the judge — carry it to Step 6. If it imports internals, run
   `prompts/00b-judge-setup.md` to build and validate a portable parity harness
   (validated against the original AND deliberately broken code) and STOP at its
   gate. Never start Step 1 without a judge — there's no exit condition without
   one.
2. **Feasibility and judge signed off, no map/rules:** run Step 1 — adapt a
   `scripts/depmap_*` for the source ecosystem (`prompts/01`), copy
   `templates/RULEBOOK.md` to `migration/RULEBOOK.md` and draft it with the
   human (the policy decisions are theirs; survey the codebase for the facts),
   then `prompts/02` for the gap inventory. Each ends at its own gate.
3. **Step 1 signed off:** confirm the HUMAN has installed
   `.claude/settings.json` from `templates/settings.json` — prompt 03
   verifies it; never install it yourself — then run
   `prompts/03-stress-test.md`. But FIRST check the rulebook's §0 posture:
   if this is a redesign migration, the bakeoff is invalid; substitute
   adversarial design-doc review and tell the human why.
4. **Stress test signed off:** confirm `migration/manifest.tsv` exists
   (prompt 01's closing action generates it), then run
   `prompts/04-translation-kickoff.md` with `scripts/queue_runner.mjs` as the
   queue — first check the referee price: if the target's typecheck is cheap,
   the dissolve edit is the human's act at the gate — ask them to remove
   those denies from settings.json; never edit it yourself (README Step 4
   dissolves into Step 3).
5. **Translation queue empty:** Step 4 via `prompts/05-survey-build.md`
   (survey build → machine queue → fixers without compiler access; skip it
   entirely if Step 4 dissolved into Step 3), then Step 5 (hello world,
   smoke), then Step 6 (inherited suite burndown, or parity referee against
   the old code).
6. **Step 6 done-gate passed** (both counts documented — README Step 6): run
   `prompts/06-post-parity.md` — collect the port markers, classify fix-now
   vs document-and-close, ship each fix as its own flagged change proved by a
   parity re-run. Ends at its own gate.

## Constant behaviors

- Report progress as burndown numbers (`queue_runner.mjs status`), not prose.
- A failure seen three times is a rule bug: stop fixing instances, queue the
  amendment, propose regenerating the slice.
- "Don't migrate" and "stop here" are valid recommendations at every gate.
