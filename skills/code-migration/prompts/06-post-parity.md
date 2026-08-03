# 06 — Post-parity burndown

**When:** only after the Step 6 done-gate — every parity test passing AND the
original suite re-run clean on the original code, both counts documented (see
README Step 6). Never alongside it. **Prerequisites:** Step 6 report with
both counts. **Placeholders:** `[target tree]`, `[reviewer model]` (from the
Model plan signed off at the feasibility gate).

---

Use a workflow. The port shipped bug-for-bug; the markers are everything it
deferred. Collect every `BUG(port)`, `TODO(port)`, and `PERF(port)` marker
from [target tree] — mechanical grep, not memory — and open the report with
the per-marker counts as a receipt: the grep output, not a narrated total.

Classify every marker: **fix now** or **document and close**, one line of
reasoning per call. Document-and-close rows get their resolution written next
to the marker, and the marker comes out in one reviewed change.

Every fix-now ships as its own flagged change — one marker, one change. Each
re-runs the parity referee and proves the ONLY behavior that changed is the
marked defect; a fix that moves any other output is two changes, and a failed
review. Reviewers run on [reviewer model], per the Model plan — inheriting
the session default is a deviation; log it. A recurring marker pattern is a
rulebook indictment, same as ever: queue the amendment for me.

Stop and show me the classification table and the per-fix parity results —
nothing merges until I sign off.
Append one timestamped line for this step to `migration/cost-log.tsv` —
create it with header `step\ttimestamp\twall_clock_min\ttokens\tsubagents\tmodel`
if absent; real values where available, `unknown` where not. Plain
tab-separated values, no `key=` prefixes — a valid row looks exactly like:
`3	2026-06-11T14:02Z	21	2035336	35	claude-sonnet-4-6`
(your step number and values vary; the format doesn't).
