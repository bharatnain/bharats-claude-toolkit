# Run notes — receipts from this kit's own test runs

This kit's prompts and scripts were dogfooded before publishing. This file is
the receipts: what ran, what broke, what changed because of it.

## Run 1 — Python → TypeScript (sandbox, 2026-06-10) — COMPLETE

- Target: **toml 0.10.2** (PyPI, MIT) — 5 files, 1,425 lines, zero deps,
  Python test suite imports internals (dies with the language → parity-referee
  path for Step 6, as the feasibility calls predicted).
- Result: full port, **strict tsc clean**, smoke + round-trip pass, and a
  12-scenario parity referee against the live Python original: **12/12
  byte-identical** after JSON normalization — including error messages with
  line/column positions, and one bug-for-bug fidelity check (both
  implementations emit the same defective output for embedded control chars,
  per the BUG(port) rule).
- Agent topology: 1 inventory proposer, 2 skeptic reviewers (separate
  contexts, disjoint batches), 1 fix agent, 2 bakeoff translators (B
  quarantined in a scratch dir outside the repo), 1 diff inspector, 3
  implementers. ~1.1M subagent tokens.

### What the process caught (the receipts)

1. **Step 1, depmap trial**: pointing `--root` at the package dir instead of
   the repo root produced **0 edges silently** — a wrong map that looks like a
   clean map. → kit fix: script now warns on 0-edges-with-multiple-files.
2. **Step 1, skeptic round**: 20/20 inventory rows confirmed but 7
   evidence-quality defects found (off-by-one citations; one row claimed
   Python and JS "misbehave identically" where Python raises TypeError and JS
   silently no-ops). One TS-inexpressible construct (dynamically-created
   sentinel class) surfaced as UNKNOWN → rulebook amendment A1 (Symbol brand).
3. **Step 2, bakeoff**: 14 material differences; rulebook right 9, native
   right 2, both defensible 2, **both wrong 1** — the rule-following
   translator silently emitted corrupted output (`"01xundefined"`) where
   Python crashes, fully legal under the pre-amendment rules. 9 rulebook
   silences flagged. → 10 amendments applied at the gate. This bug class
   would have replicated across the whole fan-out.
4. **Step 2, side discovery**: the quarantined native translator independently
   found 2 behaviors in the upstream Python library we classified as defects
   for porting purposes (upstream issue candidates: invalid TOML emitted near
   control characters; crash on leading control char). Ruling: reproduce
   bug-for-bug, mark BUG(port), fix only post-parity — now amendment A2.1.
5. **Steps 3–4**: 5 files translated against the amended rulebook; queue
   runner reported burndown and `verify` confirmed no empty targets. tsc
   (in-loop, Step 4 dissolved as documented) caught exactly 2 cross-file
   errors: a duplicated type alias and a callback signature narrower than the
   source's duck typing. Both fixed in one referee round.
6. **Step 6**: the parity referee itself shipped 2 bugs before the port showed
   any — whitespace differences in the comparator and JSON.stringify silently
   converting NaN/-Infinity to null. Lesson now in the README: debug the
   referee before believing its verdicts; 12/12 "diverge" usually means a
   broken referee, not a broken port.

### Deviations from the full process (budget scaling — a production run must not skip these)

- **Step 3's two-adversarial-reviewers-per-file pass was skipped** (implementer
  + in-loop tsc + parity only). Observed consequence, exactly as the process
  predicts: the cross-file type conflict reviewers would have caught landed in
  the compile step instead. Cheap here (tsc, seconds); expensive in a
  cargo-class target. The deviation produced the precise failure class the
  review stage exists to prevent — strongest evidence in this run that the
  stage earns its cost.
- Bakeoff re-round on fresh files and the pilot run were folded into Step 3's
  first unit. Logged in the target repo's RULEBOOK deviation log.

Limitation, stated up front: tsc is a cheap referee, so this run exercises
Step 4 only in its dissolved-into-Step-3 form (see README). Run 2 (C → Rust)
covers the expensive-referee path.

Run artifacts: `examples/run1-toml/` in the upstream repo (not vendored here).

## Run 2 — C → Rust (Claude Code, developer workstation, 2026-06-11) — COMPLETE

- Target: **tinyexpr** (~730-line C expression parser, zlib license, function-
  pointer-heavy core). Cold-start condition: driven by a non-engineer
  following only the kit's docs, with the kit's author firewalled — every doc
  gap became a logged finding instead of a question.
- Result: full port. 11/11 translated integration tests; original C smoke
  suite re-run: **4,930/4,930, zero inherited failures**; 23 TODO(port) and
  1 BUG(port) marker, all accounted for.

### What the process caught

- One failing test (`test_syntax`, an error-position mismatch — the exact gap
  class the feasibility report predicted). Protocol held: the referee was
  checked first (the C binary confirmed all 14 expected error positions, so
  the translated test was exonerated), then the divergence traced to TWO port
  bugs — the second an identifier-start mismatch, `_` accepted where C's
  `isalpha()` rejects it (the rulebook's §2 example row cites this) — sharing
  one root cause: a silent rulebook gap. The source uses one
  sentinel (NULL) for both allocation failure and structural parse errors;
  the translation mapped both the same way. Rule amendment written, then the
  sweep found the same pattern in **three more places no test exercises**.
  One failing test, one amended rule, four corrected sites — the
  fix-the-rule-not-the-instance loop on receipts.

### What the run caught about the kit (13 findings, all since fixed)

- `.claude/settings.json` was never installed and nothing checked — the
  guardrails were silently absent for the whole run. → prompts 03/04 now
  verify and refuse to fan out without it.
- Model selection silently defaulted for every agent. → feasibility now
  produces a Model plan as an explicit human gate decision.
- Five parallel inventory classifiers contended on one shared TSV; one
  stalled mid-append and the user had to notice. → shard-then-merge with
  mechanical `wc -l` receipts and a self-healing progress invariant.
- Cost was unreconstructable after the fact. → every gate now appends to
  `migration/cost-log.tsv`.
- Step 6 had no defined done-gate; BUG(port) markers had no post-parity
  process. → done-gate defined; `prompts/06-post-parity.md` added.
- Side receipt: the repo was relocated mid-run (a workstation security policy
  on freshly built binaries) and a brand-new session resumed correctly at
  "Step 5, one failing test" from disk state alone — the resume thesis
  proven under harsher conditions than planned.

## Run 3 — C → Rust, forced expensive-referee path (2026-06-11) — COMPLETE

Purpose: exercise the two paths Runs 1–2 dissolved away — deny rules firing
in anger and the Step 4 survey build — and live-test the Run 2 fixes. Same
repo; Steps 1–2 artifacts (rulebook with all amendments, inventory, depmap)
reused; translated targets deleted to reopen the queue.

- Result: 7/7 files (2,513 lines of Rust) translated **compiler-blind**;
  survey build round 1 = 2 errors, round 2 = 0; **11/11 tests on the first
  Step 5/6 run**. The amended rulebook is why round 1 was small — Run 2's
  rule fixes translated clean the second time.
- **The deny receipt:** an agent attempted `cargo check` → denied by
  settings.json. It then attempted to edit settings.json to clear the deny →
  blocked by the platform's self-modification guard. It then cited this
  kit's no-routing-around rule and escalated to the human, who served as
  build daemon per prompt 05. Three defensive layers observed in one
  incident; the mechanical layers did the stopping.
- Cost, finally on receipts: Step 3 ≈ 2.04M subagent tokens, 35 agents,
  ~21 min; Step 4 fixers ≈ 0.51M tokens, 12 agents, ~3.5 min. All subagents
  ran on the mid-tier model — the model plan was again an untriggered
  default, the second consecutive run, which is exactly why the Model plan
  gate now exists.
- New findings → fixes: the gate-time settings.json amendment can itself be
  blocked by platform safeguards (references/kit-orientation.md now documents the
  human-makes-the-edit fallback); the orchestrator self-installed
  settings.json instead of stopping for the human (prompt 04 now forbids
  self-install); human-as-build-daemon works but doesn't scale
  (`scripts/build_daemon.sh`); PORT STATUS trailers drifted from grep truth
  (fixers now post-write-verify counts); cost-log rows came out malformed
  (prompts now show a literal example row).

Target-repo artifacts (cost logs, scenario lists) live in the run repo, not
here; figures above come from session receipts.

## Designed, not yet dogfooded

`prompts/00b-judge-setup.md` — the pre-Step-1 judge build (categorize tests,
rewrite for portability under adversarial review, validate against the original
*and* against deliberately broken code) — has not been exercised by a run. All
three runs built their judge inside Step 6 instead, which is the late-judge
failure 00b exists to prevent: Run 1's parity referee shipped two comparator
bugs and reported 12/12 false divergences before it could be trusted. The
prompt is reconstructed from the blog's stated method plus that Run 1 lesson;
the "validate against broken code" step in particular is new to the kit and
unrun. Treat its output as a draft to debug until a future run dogfoods it —
the same honesty bar the survey-build path held before Run 3 exercised it.

## Script verification (sandbox, 2026-06-10)

- `depmap_python.py`: fixture with 3-file relative-import cycle + stdlib +
  third-party imports → cycle detected as one batch, externals excluded,
  byte-identical across runs ✓
- `depmap_ts.mjs`: fixture with import/export-from/require cycle, bare
  specifiers, index resolution → cycle detected, bare specifiers excluded,
  deterministic ✓
- `depmap_c.py`: fixture with quoted-include header cycle + angle includes →
  cycle detected (bar.h ⇄ foo.h), system headers excluded ✓
- `make_manifest.py`: order.txt + substitution rules -> manifest TSV, fixture
  diff-verified; refuses when substitutions don't apply ✓
- `queue_runner.mjs`: status burndown, next-batch JSON, and verify catching a
  zero-byte "done" file (the touch cheat) ✓
- `build_daemon.sh` (2026-06-11): `--once` produces the numbered output file,
  round counter resumes from disk, bad `--interval` and missing flag values
  rejected ✓
