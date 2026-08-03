# 05 — Survey build

**When:** Step 4, after the translation queue is empty. **SKIP ENTIRELY** if
Step 4 dissolved into Step 3 per the README — your cheap referee already ran
in-loop. **Prerequisites:** Step 3 queue at zero (`queue_runner.mjs status`).
**Placeholders:** `[build command]`, `[module]` (your target's module
granularity), `[fixer model]`, `[reviewer model]` (from the Model plan
signed off at the feasibility gate).

---

Use a workflow. Run ONE scripted survey build — `[build command]` over
everything, once. Parse its diagnostics into a machine queue: a TSV of file,
module, error code, message — sliced by [module], ordered leaves-to-root per
the dependency map. The error list is the queue; nobody re-derives it by
judgment.

Fan out fixers per module slice with **no compiler access** — they write
patches from the error text and the source alone. Fixers run on
[fixer model], reviewers on [reviewer model], per the Model plan —
inheriting the session default is a deviation; log it. Adversarial review on
every fix, same contract as Step 3: separate contexts, every finding cites a
rule or a source line. The review doubles each slice's cost; Run 1 skipped
the per-file review pass entirely, and the exact failure class it catches
survived to the compiler (RUN-NOTES, Run 1 deviations). The daemon that owns the build is the only process that reruns
the survey build — once per round, to produce the next queue. Repeat to zero.

Transport: prefer `scripts/build_daemon.sh` as the referee — I start it once
(`./build_daemon.sh --cmd "[build command]"`), it reruns the build whenever
the tree changes, and each round lands in `migration/build-output-rN.txt`;
fixers consume the numbered output files and never run the compiler. Run 3
ran this step with the human relaying every build by hand — fine for 2
rounds, not for 50. Zero-setup fallback: I run
`[build command] 2>&1 | tee migration/build-output-rN.txt` myself each round
— same files, same contract.

Fixer post-write check: after writing a file, `grep -c 'TODO(port)' <file>`
must equal the `todos=` value in its PORT STATUS trailer — recount
mechanically, never narrate. Run 3 shipped a trailer claiming todos=1 where
grep said 2; the grep is the receipt, the trailer is the claim.

A recurring error pattern is a rulebook indictment, not N hand-fixes: queue
the amendment for me and propose regenerating the slice that rule touched.
Stop and show me the round-over-round error counts. End the report with an
estimated duration for the next step (Step 5 — hello world, then smoke) —
wall-clock and active-attention minutes, from the rounds you just timed.
Append one timestamped line for this step to `migration/cost-log.tsv` —
create it with header `step\ttimestamp\twall_clock_min\ttokens\tsubagents\tmodel`
if absent; real values where available, `unknown` where not. Plain
tab-separated values, no `key=` prefixes — a valid row looks exactly like:
`3	2026-06-11T14:02Z	21	2035336	35	claude-sonnet-4-6`
(your step number and values vary; the format doesn't).
