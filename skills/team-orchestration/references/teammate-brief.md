# Teammate brief template

Every spawn prompt carries all seven blocks. Teammates do not inherit the orchestrator's
history, so anything not in the brief does not exist for them. Fill the angle brackets;
delete nothing except the AUTONOMY block on attended runs.

```
OBJECTIVE
<one paragraph: the deliverable and the acceptance criteria, written as a /goal-style
condition — one measurable end state, the check that proves it, the constraints>

WRITE SCOPE
Write only inside: <explicit directory/file list, e.g. skills/foo/**, workflows/bar.js>
Do not touch: <shared files the orchestrator owns — README.md, CHANGELOG.md, manifests,
catalogs — plus any sibling teammate's scope>

OUTPUT
Report path: <scratchpad>/<report-name>.md
Report contents: files created / changed / deleted; validator output (verbatim lines);
open findings.
Reply format: first line is one of DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED,
then at most 10 lines.

CHECK AFTER EACH UNIT
Run <validator/test command> after each completed unit; do not move on while it fails.
Paste its output in the report — show the command and its result, not a claim.

OUT-OF-SCOPE FINDINGS
Report them in the report file (file path, one-line description). Do not fix them.
Do not edit outside WRITE SCOPE even to fix something obvious.

CONTEXT
<repo path / worktree, branch, do-not-commit rule, spec file to read first, any facts
the teammate cannot derive from the tree>

AUTONOMY  (unattended runs only)
You are operating autonomously. The user is not watching in real time. Work through the
objective end to end without checking in. The scope is the deliverable: do not quietly
narrow, widen, or swap it. Stop only for destructive actions (deleting data, force-pushing,
rewriting history) or genuine scope changes; otherwise decide, record the decision in the
report, and continue.
```

## Rules of thumb

- One brief per teammate; no two briefs share a writable path.
- Name the check by its exact command; "run the tests" is not a check.
- Put the report path in the scratchpad, never in the repo.
- Attended run: drop the AUTONOMY block, keep everything else.
