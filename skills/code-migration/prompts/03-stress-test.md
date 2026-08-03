# 03 — Stress-test the rules

**When:** Step 2, after the rulebook, inventory, and dependency map are signed
off. **Prerequisites:** committed RULEBOOK.md and inventory; this prompt is
only valid for **structure-preserving** migrations — for redesigns the bakeoff
measures your redesign, not your rules (see README, "If you're redesigning").
**Placeholders:** `[3]` (file count), `[target language]`, `[target formatter]`,
`[implementer model]`, `[reviewer model]` — the last two from the Model plan
signed off at the feasibility gate.

---

Use a workflow. The **rulebook** has never met real code. Before any fan-out,
stress-test it on [3] real files. Nothing translated here ships — the only
output that survives is rule changes. Translating [3] files twice to throw
both away is the cost; Run 1's bakeoff bought a both-wrong bug that would
have replicated across the entire fan-out (RUN-NOTES).

Before any fan-out, two checks. First: `.claude/settings.json`. Never
install it yourself — installation is my act, because that's the moment I
decide the referee price; Run 3's orchestrator detected the missing file and
self-installed it, automating away exactly that decision. If it's missing,
STOP and wait: tell me to install `templates/settings.json`, or record my
explicit waiver in the deviation log — Run 2 ran end to end with the
guardrails silently never installed. If it exists and carries deny rules for
this migration's expensive commands — the template adapted per
`templates/settings.README.md`, including any dissolve edit I made at a
gate — proceed silently. Halt and ask only if it lacks deny rules entirely,
or you can't tell whether I sanctioned what's there; never install, never
overwrite. Second: set the model explicitly on every subagent call —
translators and the pilot implementer on [implementer model], reviewers and
the diff inspector on [reviewer model]; fixers ride [implementer model]
unless the Model plan says otherwise. Inheriting the session default is a
deviation; log it.

Pick the files by criteria, not taste: score candidates by how many of the
rulebook's riskiest sections and **gap inventory** rows they exercise, take
the top [3], and write the selection — with its scores and file:line proof —
to a report under `migration/stress-test/`, queueing its commit for me at
the gate — commits are denied in-loop by design. Easy files make a clean
diff and a useless step.

Then the **dual translators**, in separate contexts and separate workspaces.
Translator A works in a throwaway worktree on a branch that never merges. It
follows the rulebook to the letter, citing the rule behind every nontrivial
choice — and where the rulebook is silent, flags the silence inline instead of
inventing policy. Translator B gets a scratch directory outside the repo
containing only the [3] source files, copied out — not a checkout, so the
rulebook and inventory aren't on disk to find — and one instruction: port
these the way a fluent [target language] engineer would write them natively.
B must never see the rulebook or learn it exists — one glimpse and it stops
being a baseline.

A third context, the **diff inspector**, sees everything. Run both outputs
through [target formatter] first, so style noise never reaches it. Every
remaining difference becomes one row: the quoted lines from both versions, the
rule section it indicts — or the gap it exposes where the rulebook was silent —
and a verdict with evidence: rulebook right, native right, both defensible, or
both wrong. The rulebook is the defendant here, not the judge — but "native is
wrong" must stay sayable: a difference the rulebook wins indicts nothing, and
a report where every difference indicts a rule is as suspicious as one with
none.

In parallel, run the same [3] files through the **pilot run**: the production
pipeline exactly as the fan-out will use it — one **implementer**, two
adversarial **reviewers**, one **fixer**, same prompts, no special pilot
versions. The reviewers carry one extra standing question: did the implementer
follow the rulebook — citing the section for every deviation. A translation
that comes out right because the implementer quietly ignored the rules is a
failed pilot; the fan-out depends on obedience, not on three files going well.

Queue every proposed rule change for me with its evidence — never edit the
rulebook yourselves. Round 1 ends at the amendment queue: show me the queue
and the adherence findings — not the translations — delete both workspaces —
A's worktree and B's scratch directory — confirming the deletions in the
report, and exit. Applying amendments is my act at the gate; a workflow that
waits mid-run for me is forbidden (references/kit-orientation.md rule 3).
After I apply them I
re-paste this prompt, and it resumes from disk state: if round-1 artifacts
already exist under `migration/stress-test/`, skip the settings check and
the file selection and run the re-round — one more bakeoff on fresh files,
weighted toward the sections that just changed (re-running the same files
only proves the patch) — plus the pilot against the amended rules. Stop
early if the same section gets re-amended twice; that needs a decision from
me, not a third wording. The re-round ends at the same gate: amendment
queue, adherence findings, and the round-over-round delta. No fan-out starts
until I sign off. End the report with an estimated duration for the next
step (the translation fan-out) — wall-clock and active-attention minutes,
derived from the manifest size and the pilot's per-file timings.
Append one timestamped line for this step to `migration/cost-log.tsv` —
create it with header `step\ttimestamp\twall_clock_min\ttokens\tsubagents\tmodel`
if absent; real values where available, `unknown` where not. Plain
tab-separated values, no `key=` prefixes — a valid row looks exactly like:
`3	2026-06-11T14:02Z	21	2035336	35	claude-sonnet-4-6`
(your step number and values vary; the format doesn't).
