# Translation Rulebook — [source language] → [target language]

> **The meta-rule: if two agents could answer a question differently, the
> answer goes in this file.** This document is read by every implementer,
> reviewer, and fixer before they touch code. It is read-only inside any loop —
> amendments are queued for the human and applied between batches.
>
> For a filled-in example at production scale, see Bun's
> [PORTING.md](https://github.com/oven-sh/bun/commit/46d3bc29f270fa881dd5730ef1549e88407701a5)
> (576 lines, Zig→Rust) — the shape below is that document, generalized.

Read this whole document before writing any code.

## 0. Scope and posture

- This is a **structure-preserving** migration: same architecture, same data
  structures, same file boundaries unless a rule below says otherwise. You are
  translating, not improving. <!-- If redesigning, replace this section with
  your ARCHITECTURE.md and delete the bakeoff from your Step 2. -->
- Drafts do not need to compile. **Do not run the compiler** — it grades
  everything in Step 4.
  <!-- Cheap typechecker (tsc, go vet)? Replace this bullet with the cheap-referee variant — see README Step 4. -->
- First pass optimizes for **correct translation**, not performance. Known
  slow-but-faithful translations are fine: mark them `PERF(port):` with one
  line on what the fast version would be, and move on.

## 1. Ecosystem adoption — what we use and what we ban

The target ecosystem will offer idiomatic alternatives for everything. Decide
once, here, which are adopted and which are banned — or every agent decides
differently and the codebase becomes a museum of styles.

| Area | Decision | Why |
|---|---|---|
| Async model | [e.g., BANNED: no async runtime; keep the source's threading model] | [why] |
| Standard library I/O | [e.g., use X, never Y] | [why] |
| String/bytes policy | [e.g., bytes everywhere internals, convert at boundaries] | [why] |
| Third-party deps | [default: NONE without a rule here naming the crate/package] | [why] |
| Error model | see §2 | |

## 2. Constructs with no equivalent — one canonical mapping each

Every source construct the target lacks gets exactly one translation, listed
here. An implementer who invents a second mapping for a listed construct is
violating a rule; a reviewer who sees an unlisted construct flags it for this
table.

| Source construct | Canonical target translation | Notes / evidence |
|---|---|---|
| [e.g., error union / exceptions] | [e.g., Result<T, E> with this E] | |
| [e.g., null / optional] | [e.g., Option<T>, never sentinel values] | |
| [e.g., inheritance] | [e.g., trait + composition, this shape] | |
| [e.g., out-of-bounds indexing] | [source raises / returns sentinel / UB — replicate the source's behavior explicitly; a target that silently returns undefined where the source raises is a defect factory] | |
| `isalpha()` at identifier start — **example row, C-family sources** | [decide the identifier-start and continuation sets explicitly; never reach for the target's "is alphabetic" helper unchecked] | Target helpers disagree with C's `isalpha()` on underscore and locale — Run 2: `_` accepted at identifier start gave one-byte-off error offsets |
| [add rows as the survey finds them] | | |

**The BUG rule:** when the source's behavior is itself defective (malformed
output, crash), reproduce it bug-for-bug and mark the site `BUG(port):` with a
repro — behavior matching (Step 6) asserts the defective output; fixes ship
only in a flagged post-parity change. The port's job is fidelity; improvement
is a separate, reviewable commit.

**The error-recovery rule:** allocation-failure returns and structural-error
returns often share one sentinel in the source (NULL, None, -1). They must
not share one target construct: an allocation failure aborts the operation;
a structural error records the error and returns whatever partial result the
source returned. Every guard row in the inventory records which kind it is —
`allocation-guard` or `precondition-guard` (see `templates/inventory.tsv`).
Run 2 collapsed the two and got wrong error positions; the rule sweep that
followed fixed three more sites no test covered.

**The UNKNOWN rule:** when neither this table nor the inventory decides a
case, translate to the most conservative representation the target offers,
mark it `TODO(port):` with the open question, and keep moving. UNKNOWN is an
answer; a stalled batch is not.

## 3. The sanctioned escape hatch

Translations that can't be expressed safely get exactly one pressure valve,
used visibly:

- [e.g., `unsafe` is allowed where the source was already unsafe — never to
  silence the borrow checker on safe logic.]
- Every use carries a justification comment: `// SAFETY: <why this is sound>`.
- Every deferred decision carries a greppable marker: `TODO(port):`,
  `PERF(port):`, `BUG(port):` (plus `SAFETY:` on every escape-hatch use).
  These markers are the queue for later steps — the format is load-bearing,
  do not vary it.

## 4. Naming and output paths

Done-ness is detected by output files existing on disk, so these rules are
what make the whole run resumable. They are not style preferences.

- Source `[path pattern]` → target `[path pattern]`. One source file, one
  target file, no exceptions without a rule here.
- [Module/package naming rule.]
- [Test file naming rule.]
- Import specifier convention for the target's module system (e.g., TS
  nodenext requires `./mod.js` specifiers for `.ts` files — decide once or
  every implementer rediscovers it).
- Home module for every shared type and helper the translations import (the
  canonical owner of the value union, type-dispatch helpers, repr emulation).
  An unassigned shared type becomes N incompatible local copies.

## 5. The gap inventory

Decisions about [your gap — lifetimes, ownership, nullability] are **not made
by implementers**. They are looked up: `migration/inventory.tsv`, one row per
site. If your site isn't in the inventory, that's an inventory bug — flag it,
apply the UNKNOWN rule, keep moving.

## 6. Per-file obligations

Every translated file ends with a status trailer:

```
// PORT STATUS: confidence=[high|medium|low] todos=[N]
```

Reviewers check the trailer against the file's actual `TODO(port)` count —
a trailer that undercounts is a finding.

## 7. Deviation log

Every departure from the documented process gets one line here — skipped
passes, waived checks, untriggered defaults. ID'd `DEV-001` style: ID, date,
what was skipped or waived, who sanctioned it. Written at gates, by the
human or with the human's sign-off. A deviation nobody logged is a deviation
nobody approved — Run 1's skipped review pass is the model entry.

| ID | Date | Deviation | Sanctioned by |
|---|---|---|---|
| DEV-001 | [date] | [e.g., Step 3 per-file review pass skipped — budget] | [who] |
