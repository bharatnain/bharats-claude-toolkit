# 02 — Gap inventory

**When:** Step 1, after a draft rulebook exists. **Prerequisites:** draft
RULEBOOK.md committed (the inventory records what its defaults won't cover).
**Placeholders:** `[name your gap]` — the thing the target language demands
that the source let you keep in your heads: ownership and lifetimes (→ Rust),
interface contracts, nullability (→ TypeScript strict), error propagation —
and `[reviewer model]` (from the Model plan signed off at the feasibility
gate).
**Template:** `templates/inventory.tsv` defines the columns.

---

Use a workflow. Before we migrate anything, build the **gap inventory** — one
flat table the implementers will grep before translating a file, not a
document anyone reads top to bottom. One row per site: file, symbol, source
construct, classification, the answer (target translation), the evidence, the
status. It captures whatever the target language
demands that the source let us keep in our heads: [name your gap]. A draft
rulebook should exist first; the inventory records what its defaults won't
cover.

Start with a sweep: enumerate every site where the gap appears — by grep and
script, not judgment — and write the list to a file with a count. Put the
inventory at a fixed, committed path and queue a rulebook rule that
delegates these decisions to the inventory by path — applied by me with the
first amendment batch, never by you — because the rulebook is how every
implementer finds out the inventory exists. That list is the definition of
done: the inventory is complete when every site on it has a row, and not
before.

Then work the list, complex cases first. For each site, trace how the value
actually flows through the code and propose the answer, citing the call sites
that prove it — where it's created, where it changes, where it escapes. Then
two **skeptic reviewers** attack the entries, batched by file or struct — in
parallel, in separate contexts, neither seeing the other's verdict, each
required to cite the line that justifies their call. Run them on
[reviewer model], per the Model plan — inheriting the session default is a
deviation; log it. Two reviewers per batch double the
spend; Run 1's skeptic round bought seven evidence defects in twenty
otherwise-confirmed rows (RUN-NOTES). If a reviewer refutes
with evidence, revise once and resubmit; still contested, the row is UNKNOWN.
No guessing: UNKNOWN rows go into the table with the question I need answered
— and UNKNOWN still gets a deterministic translation: the most conservative
representation the target language offers, plus a greppable TODO marker, so an
implementer who hits one ports it mechanically and the open question survives
as a searchable artifact, not a stalled batch.

Do the first 20 rows, then stop and show me before fanning out.

When you fan out, parallel agents never contend on one file — same disk-state
pattern as the translation queue. Each classifier writes its own shard,
`migration/inventory.<category>.tsv`; the orchestrator merges them at the
end: dedupe on (file, symbol, source_construct) keys — so a partial write costs nothing
on retry — sort deterministically, and report a mechanical receipt, the
`wc -l` output of the merged file, not a narrated total (Run 2's narrated
total didn't reconcile; the count is the audit). Progress invariant while
workers run: shard row counts must grow between polls — no growth for three
minutes means treat that worker as failed, recover its rows from the journal
or disk, and report the stall. Stalls are yours to heal, not mine to notice.

When every site has a row, run the **joint audit**: adversarial agents read
the gap inventory and the **rulebook** together and hunt for contradictions —
a row the rules would translate wrong, a rule no row exercises. Each conflict
must name the rule, the row, and the concrete translation that goes wrong — no
contradiction without an example. Write it into the file with a proposed fix;
apply confirmed fixes on the inventory side, but queue rulebook changes for me
— don't apply them. Then stop and show me the counts, the UNKNOWN rows, and
the conflict list. No implementer starts until I sign off. End the report
with an estimated duration for the next step (the stress test) — wall-clock
and active-attention minutes, derived from the row counts you just produced.
Append one timestamped line for this step to `migration/cost-log.tsv` —
create it with header `step\ttimestamp\twall_clock_min\ttokens\tsubagents\tmodel`
if absent; real values where available, `unknown` where not. Plain
tab-separated values, no `key=` prefixes — a valid row looks exactly like:
`3	2026-06-11T14:02Z	21	2035336	35	claude-sonnet-4-6`
(your step number and values vary; the format doesn't).
