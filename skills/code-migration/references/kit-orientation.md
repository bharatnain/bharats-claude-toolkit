# Kit orientation — the migration operating manual

This is the Claude Code Migration Kit's operating manual (the upstream kit
ships it as its `CLAUDE.md`; it is vendored here as a reference doc). Copy or
`@`-import it into the target repo's `CLAUDE.md` before a migration begins.
You are working with the kit, or inside a repository that has adopted it.
Read this before acting on any migration request. Kit paths below
(`prompts/`, `scripts/`, `templates/`) are relative to the `code-migration`
skill directory.

## What this kit is

A six-step process for migrating a codebase from one language to another:
(1) create the map and the rules, (2) stress-test the rules, (3) translate
everything, (4) compile, (5) run it, (6) match behavior. The README defines
each step. The prompts in `prompts/` run them. Do not improvise a different
process when a prompt exists for the step.

## Standing rules — these override convenience

1. **The rulebook is read-only inside any loop.** Implementers, reviewers, and
   fixers cite it; they never edit it. Rulebook amendments are queued for the
   human and applied between batches. The graded party does not relax its own
   grader.
2. **Queues live on disk.** A unit of work is done when its output file exists
   at the path the naming rules dictate — never when an orchestrator remembers
   it. If you find yourself tracking state in conversation, stop and write a
   manifest instead (`scripts/queue_runner.mjs`).
3. **Sign-off gates end the workflow.** When a prompt says "stop and show me"
   or "no fan-out until I sign off," the phase is over: return the evidence and
   exit. Do not proceed on inferred approval. The human re-invokes the next
   phase; resumability is free because of rule 2.
4. **Reviewers are adversarial, separate, and read-only.** Two reviewers per
   unit, separate contexts, assume the work is wrong, touch nothing. Every
   finding cites a rule or a source line. A third rules on disagreements,
   defaulting to not-confirmed. Fixers apply confirmed findings only.
5. **Banned operations are banned by configuration.** `templates/settings.json`
   denies the expensive commands inside loops (mutating version control, the
   compiler, long-running test commands). If a denied command blocks you, that
   is the design working: flag it, don't route around it. Exception: a cheap
   typecheck (tsc, go vet) may be promoted into the loop per README Step 4 —
   that swap is made by editing settings.json at a gate, never by routing
   around a live deny. If the platform's own safeguards block you from
   editing settings.json (self-modification protection), that is not an
   error to work around: the human makes the edit manually, or serves as
   build daemon per prompts/05. Routing around a live deny is forbidden no
   matter which layer enforces it — Run 3's agent was blocked at exactly
   this point and correctly escalated.
6. **Recurring failures move upstream.** Fix one instance, fine. See the same
   failure twice more, stop fixing instances: write up which rule produced it,
   queue the rulebook amendment, and propose regenerating the slice that rule
   touched.
7. **The old code is the spec.** It stays runnable until behavior matching is
   done. When a test fails on the new code, run it on the old code before
   classifying: old-fails-too = inherited, not yours. Never skip, delete, or
   weaken a test to make a queue shrink; slow-but-passing goes in a ledger,
   not a commit.
8. **Unknown is an answer.** When neither the rulebook nor the inventory
   decides a question, translate to the most conservative representation the
   target offers, leave a greppable TODO marker, and keep moving. A searchable
   artifact beats a stalled batch.

## Where things live

| Artifact | Path | Created by |
|---|---|---|
| Rulebook | `migration/RULEBOOK.md` (copy from `templates/`) | Step 1 |
| Dependency map | `migration/depmap/` (edges.tsv, order.txt, cycles.txt) | `scripts/depmap_*` |
| Gap inventory | `migration/inventory.tsv` | Step 1, prompt 02 |
| Work manifest | `migration/manifest.tsv` | Step 1, prompt 01's closing action (`scripts/make_manifest.py`) → Step 3 input |
| Stress-test report | `migration/stress-test/` | Step 2 |
| Translated output | path per the rulebook's naming rules | Step 3 |
| Cost log | `migration/cost-log.tsv` | every prompt, one line per gate |
| Deviation log | `migration/RULEBOOK.md`, Deviation log section | written at gates |

If these paths don't exist yet, the migration hasn't started: run
`prompts/00-feasibility.md` first and stop at its verdict.

## Model guidance

Token spend concentrates in loops; blast radius decides the tier, not task
prestige. Rulebook authorship and amendments: largest available model —
one-time work, and every error replicates into every translated file.
Skeptic reviewers: largest or mid tier, depending on gap complexity.
High-volume translation implementers: mid or small tier — two reviewers and
a compiler stand behind them. Fixers: mid tier — the compiler is the real
referee. The model plan is the human's decision, made at the feasibility
gate (prompt 00's Model plan section), and it binds every post-feasibility
prompt — 01 through 06 take the chosen tiers as explicit `[model]`
placeholders. Running subagents on an untriggered default is a process
violation — log it in the deviation log (RULEBOOK.md, Deviation log
section).
