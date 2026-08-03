# 04 — Translation kickoff

**When:** Step 3, after the stress test is signed off. **Prerequisites:**
amended RULEBOOK.md, complete inventory, manifest at `migration/manifest.tsv`
(source path → target path per the rulebook's naming rules), and
`templates/settings.json` copied to the target repo's `.claude/settings.json`
so the banned commands actually deny.
**Placeholders:** `[100]` (batch size), `[TODO(port)]` (your
greppable markers — TODO/PERF/BUG per rulebook §3), `[implementer model]`,
`[reviewer model]` (from the Model plan signed off at the feasibility gate).
Swap "file" for whatever your queue emits — modules, units.

This prompt is deliberately short. By Step 3 the rulebook is the prompt — if
your kickoff needs to be longer than this, your rulebook isn't done.

---

Before any fan-out, verify `.claude/settings.json`. Never install it
yourself — installation is my act, because that's the moment I decide the
referee price; Run 3's orchestrator detected the missing file and
self-installed it, automating away exactly that decision. If it's missing,
STOP and wait: tell me to install `templates/settings.json`, or record my
explicit waiver in the deviation log — Run 2 ran end to end with the
guardrails silently never installed. If it exists and carries deny rules for
this migration's expensive commands — the template adapted per
`templates/settings.README.md`, including any dissolve edit I made at a
gate — proceed silently. Halt and ask only if it lacks deny rules entirely,
or you can't tell whether I sanctioned what's there; never install, never
overwrite. Set the model explicitly on every agent call: implementers on
[implementer model], reviewers on [reviewer model]; fixers ride
[implementer model] unless the Model plan says otherwise. Inheriting the
session default is a deviation; log it.

Use a workflow. The queue is every `migration/manifest.tsv` entry with no
translated file on disk yet — so reruns resume for free. Work down it in
batches of [100]. Every
agent reads the **rulebook**; each implementer translates its one file —
[TODO(port)] anything the rulebook doesn't decide, status trailer at the
bottom. Two adversarial **reviewers** per file, separate contexts, assume it's
wrong, touch nothing — every finding cites a rule or a source line; a third
rules on anything they don't agree on, defaulting to not-confirmed. **Fix
agents** apply confirmed findings only — can't fix it, flag it. Don't run the
compiler — it grades everything next step (exception: if Step 4 has dissolved
into this loop per README Step 4, the rulebook's §0 names the cheap in-loop
referee). Four agents per file is the multiplier and the product: Run 1's
catches came from adversarial review at the map, inventory, and bakeoff
stages — and the one run that skipped this per-file pass ate the exact
failure class it exists to catch in the compile step (RUN-NOTES, Run 1
deviations).

Progress invariant: translated-file count on disk must grow between polls.
No growth from a worker for three minutes means treat it as failed — recover
its output from the journal or disk, and report the stall. Stalls are yours
to heal, not mine to notice. At each batch gate, report burndown plus an
estimated duration for the next step (survey build — or Steps 5–6 if Step 4
dissolved) — wall-clock and active-attention minutes, from the batch timings
you just measured.
Append one timestamped line for this step to `migration/cost-log.tsv` —
create it with header `step\ttimestamp\twall_clock_min\ttokens\tsubagents\tmodel`
if absent; real values where available, `unknown` where not. Plain
tab-separated values, no `key=` prefixes — a valid row looks exactly like:
`3	2026-06-11T14:02Z	21	2035336	35	claude-sonnet-4-6`
(your step number and values vary; the format doesn't).
