# Why each deny rule exists

`settings.json` goes in `.claude/settings.json` of the repo being migrated —
installed by the human **before prompt 03** (Step 2's pilot needs the denies
live), active **through Step 4** (prompt 05), with the test denies
**re-activated for Step 6's fix loops** (fixers read failure evidence; only
the build daemon re-runs tests). The install is a copy, not a suggestion:
`cp templates/settings.json <target repo>/.claude/settings.json`. Prompts 03
and 04 verify the file exists and refuse to fan out without it — in Run 2 the
install was silently skipped and the deny rules were never active for the
entire run. These are the in-loop bans from the process: banned
by configuration, not by asking nicely. Remove or adjust them for the phases
where the human (or the build daemon) needs the commands back. The deny list
is a template — substitute your target's build/test commands. These rules are
guardrails against accidental invocation inside loops, not a security boundary
— a determined wrapper script can bypass pattern matching.

## The git rules

One agent running `git reset` or `git checkout` in a shared worktree destroys
the in-flight work of every other agent in that worktree — with sixteen agents
sharing a worktree, one reset destroys fifteen agents' in-flight work. Mutating git
commands are denied; read-only ones (`status`, `diff`, `log`) stay allowed
because reviewers use them as evidence. `git clean` is denied with special
prejudice: translated outputs are untracked files until the batch commit, so
it is the single most destructive command for a fan-out. Commits happen at
batch boundaries, by the orchestrating session, not by loop agents.

## The compiler rules

The compiler is banned inside the translation loop for two reasons. The cheap
reason: an expensive build run by 64 agents independently turns the machine
into a space heater. The important reason: Step 3's contract is "drafts don't
need to compile," and an agent that *can* compile will start optimizing for
the compiler instead of the rulebook — playing it safe, translating less. The
compiler gets its turn in Step 4, run once per round by a single survey-build
script, and its error list arrives as a machine queue.

If your target's typecheck is cheap (tsc, go vet), delete those rules and run
the typechecker inside the loop — see README: every referee has a price, and
the price decides its position.

## The test rules

Same logic as the compiler, applied to Step 6: fixers work read-only from
failure evidence; only the build daemon re-runs tests. Long test commands run
by parallel agents also exhaust sockets, disk, and process limits — heavy
suites may need OS-level resource isolation (e.g., cgroups) on top of these
denies. If your suite is heavy, consider the same.

## What's deliberately NOT here

No deny rule for editing the rulebook — because permission rules can't express
"read-only for loop agents, writable for the human." That rule is enforced by
prompt contract (every kit prompt queues amendments instead of applying them)
and by review: a diff touching RULEBOOK.md inside a batch is an automatic
finding.
