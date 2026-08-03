#!/usr/bin/env node
// Copyright 2026 Anthropic PBC
// SPDX-License-Identifier: Apache-2.0
/**
 * Mechanical work queue for the translation fan-out (node stdlib only).
 *
 * The contract (prompts/04-translation-kickoff.md): the queue is every
 * manifest entry whose output file does not exist on disk yet. Done-ness is
 * the filesystem, not memory — so runs resume for free after a crash, and no
 * orchestrator invents its own state tracking. This is the pattern from the
 * Bun port's port-batch script, generalized.
 *
 * Manifest: TSV with header `source\ttarget`, one unit of work per line.
 * Targets are paths the rulebook's naming rules dictate (RULEBOOK.md §4).
 *
 * Run from the repo root that the manifest's paths are relative to.
 *
 * Usage:
 *   node queue_runner.mjs --manifest migration/manifest.tsv status
 *       → burndown: done/total, per-directory breakdown
 *   node queue_runner.mjs --manifest migration/manifest.tsv next --batch 100
 *       → JSON array of the next N pending {source, target} pairs (for a
 *         workflow to fan out over)
 *   node queue_runner.mjs --manifest migration/manifest.tsv verify
 *       → exit 1 if any "done" target is empty (zero bytes) — catches the
 *         touch-the-file cheat
 *
 * Test (self-contained; <kit> = path to this kit):
 *   cd "$(mktemp -d)" && printf 'source\ttarget\nsrc/a.py\tout/a.ts\nsrc/b.py\tout/b.ts\n' > m.tsv \
 *     && mkdir -p out && touch out/a.ts \
 *     && node <kit>/scripts/queue_runner.mjs --manifest m.tsv status | grep -q '^1/2 done' \
 *     && ! node <kit>/scripts/queue_runner.mjs --manifest m.tsv verify && echo PASS
 *   status must report 1/2 done; verify must exit 1 (out/a.ts is the
 *   zero-byte touch cheat); the one-liner prints PASS.
 */

import { readFileSync, existsSync, statSync } from "node:fs";
import { dirname } from "node:path";

function parseArgs() {
  const a = process.argv.slice(2);
  const out = { _: [] };
  for (let i = 0; i < a.length; i++) {
    if (a[i].startsWith("--")) { out[a[i].slice(2)] = a[i + 1]; i++; }
    else out._.push(a[i]);
  }
  return out;
}

const args = parseArgs();
const cmd = args._[0] || "status";
const manifestPath = args.manifest || "migration/manifest.tsv";

const lines = readFileSync(manifestPath, "utf8").trim().split("\n");
const header = lines.shift().split("\t");
if (header[0] !== "source" || header[1] !== "target") {
  console.error(`manifest must have header "source\\ttarget", got: ${header.join("\\t")}`);
  process.exit(1);
}
const units = lines.filter(Boolean).map(l => {
  const [source, target] = l.split("\t");
  return { source, target, done: existsSync(target) };
});

if (units.length === 0) {
  if (cmd === "next") { console.log("[]"); process.exit(0); }
  console.log("0/0 done (nothing in manifest)");
  process.exit(0);
}

if (cmd === "status") {
  const done = units.filter(u => u.done);
  const byDir = {};
  for (const u of units) {
    const d = dirname(u.source);
    byDir[d] = byDir[d] || { done: 0, total: 0 };
    byDir[d].total++;
    if (u.done) byDir[d].done++;
  }
  console.log(`${done.length}/${units.length} done (${(100 * done.length / units.length).toFixed(1)}%)`);
  for (const d of Object.keys(byDir).sort()) {
    const { done: dd, total } = byDir[d];
    console.log(`  ${d}: ${dd}/${total}`);
  }
} else if (cmd === "next") {
  const n = parseInt(args.batch || "100", 10);
  const pending = units.filter(u => !u.done).slice(0, n);
  console.log(JSON.stringify(pending.map(({ source, target }) => ({ source, target })), null, 2));
} else if (cmd === "verify") {
  const empty = units.filter(u => u.done && statSync(u.target).size === 0);
  if (empty.length) {
    console.error(`FAIL: ${empty.length} target(s) exist but are empty:`);
    for (const u of empty) console.error(`  ${u.target}`);
    process.exit(1);
  }
  console.log(`OK: all ${units.filter(u => u.done).length} done targets are non-empty`);
} else {
  console.error(`unknown command: ${cmd} (use status | next | verify)`);
  process.exit(1);
}
