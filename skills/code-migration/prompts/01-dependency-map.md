# 01 — Dependency map

**When:** Step 1, can start immediately. **Prerequisites:** none (feeds the
work manifest and the rulebook's package map).
**Placeholders:** `[your dependency mechanism]`, `[crate / package / module]`,
`[reviewer model]` (from the Model plan signed off at the feasibility gate).
**Note:** this kit ships starter scripts — `scripts/depmap_python.py`,
`scripts/depmap_ts.mjs`, `scripts/depmap_c.py` — that implement the contract
below. Adapt one instead of writing from scratch.

---

Use a workflow. Before we migrate anything, build the **dependency map** — the
file that orders all the work, written for the agents that will read it.

Don't build it by having agents read files and report imports — you get a
different map every run, and you can't verify a nondeterministic artifact.
Write a deterministic script that parses [your dependency mechanism — imports,
include directives, build files] and emits one edge per line. In-repo files
only: third-party, vendored, and generated code are neither edges nor misses.
Trial the script on five files and check its output by hand before running it
on everything, and keep it fast — it will be re-run constantly. Commit the
script and write the map to a known path.

From the graph, compute — in the script, not by judgment — the **migration
order** (topological — files with no in-repo dependencies first, working
upward) and the strongly connected components. Every component bigger than one
file is a **cycle** and migrates as a single batch. Then condense the graph to
the target's [crate / package / module] boundaries and check for cycles again —
a clean file graph does not mean a clean partition, and the partition is the
level the compiler enforces.

Then have two **skeptic reviewers**, in parallel with separate contexts and
disjoint samples, verify the map. Run them on [reviewer model], per the
Model plan — inheriting the session default is a deviation; log it. Each takes 20 files — half random, drawn
from non-overlapping halves of the file list, and half adversarial, with the
categories split between them: one reviewer takes the largest and most
macro-heavy files, the other takes platform-specific variants and generated
files (to confirm the script excludes them). For each file, list its direct
in-repo dependencies from the source itself and return rows with file:line
evidence — not a verdict. Diff the rows against the map in both directions:
edges the script missed, and edges it invented. Check each discrepancy against
the source line before touching the script — only one confirmed in the source
counts. Two contexts cost double and are the point: the dogfood map and
inventory catches came from adversarial review, not first drafts (RUN-NOTES).

Any confirmed discrepancy is a bug in the **script**, not the map — fix the
script so it handles the pattern, not the caught files, then regenerate the
whole map and resample with fresh reviewers and fresh files. A round is clean
only when both reviewers come back empty in both directions. Stop after three
failed rounds — or sooner if the same category keeps recurring — and bring me
the misses themselves: that usually means the dependencies aren't statically
discoverable, and what to do about that is my decision, not another script
patch.

Closing action, once a round is clean: generate the work manifest from the
order —
`python3 scripts/make_manifest.py --order migration/depmap/order.txt
--out migration/manifest.tsv --sub '<source prefix>=<target prefix>' --sub
'<source ext>=<target ext>'` — substitutions encoding the rulebook's naming
rules (§4) — and report the unit count from `wc -l`, not a narrated total.
Prompt 04's queue reads `migration/manifest.tsv`; this is where it comes
from.

Then stop and show me the counts, the cycle list at both granularities, and
the file paths — not the whole map. Nothing downstream gets built until I
sign off. End the report with an estimated duration for the next step (the
gap inventory) — wall-clock and active-attention minutes, derived from the
counts you just gathered.
Append one timestamped line for this step to `migration/cost-log.tsv` —
create it with header `step\ttimestamp\twall_clock_min\ttokens\tsubagents\tmodel`
if absent; real values where available, `unknown` where not. Plain
tab-separated values, no `key=` prefixes — a valid row looks exactly like:
`3	2026-06-11T14:02Z	21	2035336	35	claude-sonnet-4-6`
(your step number and values vary; the format doesn't).
