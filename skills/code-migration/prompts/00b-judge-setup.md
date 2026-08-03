# 00b — Judge setup

**When:** after the feasibility gate signs off "migrate," before Step 1 — but
only when the feasibility report's call #3 found too few public-surface tests
to judge parity (the common case). If your existing suite already exercises the
public surface, or already lives in a third language, you have your judge: skip
this prompt and carry that suite into Step 6.
**Prerequisites:** signed-off feasibility verdict; the call #3 test census
(which tests hit the public surface, which import internals).
**Placeholders:** `[target language]`, `[reviewer model]` (from the Model plan
signed off at the feasibility gate).

> Designed, not yet dogfooded — see RUN-NOTES. Runs 1–3 built their judge inside
> Step 6, which is exactly the late-judge failure this prompt exists to prevent
> (Run 1's referee shipped two comparator bugs before it could be trusted). Treat
> the output as a draft to debug, not a verdict to believe.

---

Use a workflow. The migration has no exit condition until a **judge** exists: a
single harness that evaluates the original code and the port on equal terms, so
"are we done?" has a mechanical answer instead of a feeling. The original code
is the executable spec; the judge is how you query it. Build it now, while the
old code still runs and nothing has been translated to bias you.

The judge must run against **both** implementations through the same external
interface — CLI, HTTP, file I/O, exported API — never through source-language
internals. A test that imports an internal function dies with the old language
and can't see the new code, so it can't judge anything. Three steps:

**1. Categorize.** Take the call #3 census and confirm it against the source:
classify every existing test as **portable** (expressible as an external call
that both implementations answer) or **internal-bound** (depends on functions,
private state, or language features that won't exist in [target language]).
Internal-bound tests are not judge material — note what behavior they were
guarding so it isn't lost, but they stay behind. Report the two counts as a
grep/file receipt, not a narrated total.

**2. Rewrite for portability.** Convert the portable tests into assertions that
run against both old and new through the external interface — same inputs, same
expected outputs, diffed mechanically. Where no test exists for a behavior the
old code clearly has, write a real-world scenario instead — a small harness of a
handful of real-world scenarios diffed against the original is enough. Then have two
**adversarial reviewers**, separate contexts and disjoint batches, check that no
rewrite weakened an assertion — a loosened tolerance, a dropped field, an
`assert truthy` where the original checked an exact value. Run them on
[reviewer model], per the Model plan — inheriting the session default is a
deviation; log it. Every weakening they confirm against the original test is a
bug in the rewrite, not the reviewer; fix the harness and resample.

**3. Validate the judge against known answers.** A judge you haven't tested is a
guess. Run the full harness against the **original** code: it must pass clean —
any failure here is a bug in the judge, because the spec passes its own spec.
Then run it against **deliberately broken** original code — mutate a handful of
behaviors by hand (flip a comparison, drop an error path, change an output
format) and confirm the judge **fails** on each. A judge that doesn't catch
breakage isn't a judge; it's a green light wired to nothing. Report both runs:
N/N pass on the original, and one caught failure per injected mutation.

Stop and show me the harness, the portable/internal-bound counts, the reviewer
findings, and both validation runs — the clean pass and every caught mutation.
Nothing in Step 1 starts until I sign off that the judge is real. This harness
is the artifact Step 6 runs to call the migration done; keep it under version
control and keep it running until the end.
Append one timestamped line for this step to `migration/cost-log.tsv` —
create it with header `step\ttimestamp\twall_clock_min\ttokens\tsubagents\tmodel`
if absent; real values where available, `unknown` where not. Plain
tab-separated values, no `key=` prefixes — a valid row looks exactly like:
`3	2026-06-11T14:02Z	21	2035336	35	claude-sonnet-4-6`
(your step number and values vary; the format doesn't).
