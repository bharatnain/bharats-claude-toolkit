#!/usr/bin/env node
// Copyright 2026 Anthropic PBC
// SPDX-License-Identifier: Apache-2.0
/**
 * Deterministic dependency mapper for JS/TS codebases (node stdlib only).
 *
 * Implements the kit's dependency-map contract (prompts/01-dependency-map.md).
 * Parses `import ... from '...'`, `export ... from '...'`, and `require('...')`
 * with a line scanner. RELATIVE specifiers only — bare specifiers (npm
 * packages, node builtins) are neither edges nor misses.
 *
 * This is a starter: the scanner handles the 95% case. For production runs on
 * codebases with dynamic imports or path aliases (tsconfig "paths"), swap the
 * parse step for ts-morph or the TypeScript compiler API — keep the output
 * contract identical.
 *
 * Usage: node depmap_ts.mjs --root path/to/repo --out path/to/migration/depmap
 * Output: edges.tsv, order.txt, cycles.txt (same contract as depmap_python.py)
 *
 * Test: node scripts/depmap_ts.mjs --root fixtures/ts --out /tmp/depmap-ts && diff /tmp/depmap-ts/edges.tsv fixtures/ts/expected_edges.tsv && diff /tmp/depmap-ts/cycles.txt fixtures/ts/expected_cycles.txt && diff /tmp/depmap-ts/order.txt fixtures/ts/expected_order.txt
 */

import { readdirSync, readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { join, relative, resolve, dirname, sep } from "node:path";

const EXTS = [".ts", ".tsx", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs"];
const SKIP_DIRS = new Set(["node_modules", "dist", "build", ".git", "coverage"]);

function args() {
  const a = process.argv.slice(2), out = {};
  for (let i = 0; i < a.length; i += 2) out[a[i].replace(/^--/, "")] = a[i + 1];
  if (!out.root || !out.out) { console.error("usage: --root <dir> --out <dir>"); process.exit(1); }
  return out;
}

function walk(dir, root, acc) {
  const entries = readdirSync(dir, { withFileTypes: true })
    .sort((x, y) => (x.name < y.name ? -1 : x.name > y.name ? 1 : 0));
  for (const entry of entries) {
    const name = entry.name;
    if (name.startsWith(".") || SKIP_DIRS.has(name)) continue;
    if (entry.isSymbolicLink()) continue; // never follow symlinks: no cycles, no escapes outside --root
    const p = join(dir, name);
    if (entry.isDirectory()) walk(p, root, acc);
    else if (entry.isFile() && EXTS.some(e => name.endsWith(e)) && !name.endsWith(".d.ts")) acc.push(p);
  }
  return acc;
}

// Match the specifier in import/export-from/require lines.
const SPEC_RE = /(?:from\s+|import\s*\(\s*|require\s*\(\s*|import\s+)["']([^"']+)["']/g;

function resolveSpecifier(spec, fromFile, fileSet) {
  if (!spec.startsWith(".")) return null; // bare specifier: not in-repo
  const base = resolve(dirname(fromFile), spec);
  const candidates = [base, ...EXTS.map(e => base + e), ...EXTS.map(e => join(base, "index" + e))];
  for (const c of candidates) if (fileSet.has(c)) return c;
  return null; // unresolvable: skipped, per in-repo-only contract
}

function tarjan(nodes, adj) {
  let counter = 0;
  const index = new Map(), low = new Map(), onStack = new Set();
  const stack = [], sccs = [];
  for (const start of nodes) {
    if (index.has(start)) continue;
    const work = [[start, 0]];
    while (work.length) {
      const frame = work[work.length - 1];
      const [node, pi] = frame;
      if (pi === 0) {
        index.set(node, counter); low.set(node, counter); counter++;
        stack.push(node); onStack.add(node);
      }
      let recursed = false;
      const succs = adj.get(node) || [];
      for (let i = pi; i < succs.length; i++) {
        const s = succs[i];
        if (!index.has(s)) { frame[1] = i + 1; work.push([s, 0]); recursed = true; break; }
        else if (onStack.has(s)) low.set(node, Math.min(low.get(node), index.get(s)));
      }
      if (recursed) continue;
      if (low.get(node) === index.get(node)) {
        const scc = [];
        for (;;) { const w = stack.pop(); onStack.delete(w); scc.push(w); if (w === node) break; }
        sccs.push(scc.sort());
      }
      work.pop();
      if (work.length) {
        const parent = work[work.length - 1][0];
        low.set(parent, Math.min(low.get(parent), low.get(node)));
      }
    }
  }
  return sccs; // reverse topological order of condensation = dependencies first
}

const { root: rootArg, out: outArg } = args();
const root = resolve(rootArg);
const files = walk(root, root, []);
const fileSet = new Set(files);
const rel = p => relative(root, p).split(sep).join("/");

const edges = new Set();
for (const f of files) {
  const text = readFileSync(f, "utf8");
  for (const m of text.matchAll(SPEC_RE)) {
    const dep = resolveSpecifier(m[1], f, fileSet);
    if (dep && dep !== f) edges.add(rel(f) + "\t" + rel(dep));
  }
}
const sortedEdges = [...edges].sort();
const nodes = files.map(rel).sort();
const adj = new Map(nodes.map(n => [n, []]));
for (const e of sortedEdges) { const [a, b] = e.split("\t"); adj.get(a).push(b); }
for (const v of adj.values()) v.sort();

const sccs = tarjan(nodes, adj);
const cycles = sccs.filter(s => s.length > 1);

mkdirSync(outArg, { recursive: true });
writeFileSync(join(outArg, "edges.tsv"), "from\tto\n" + sortedEdges.map(e => e + "\n").join(""));
writeFileSync(join(outArg, "order.txt"),
  "# migration order: one batch per line, dependencies first\n" + sccs.map(s => s.join("\t") + "\n").join(""));
writeFileSync(join(outArg, "cycles.txt"),
  `# strongly connected components > 1 file: ${cycles.length}\n` + cycles.map(s => s.join("\t") + "\n").join(""));
console.log(`files=${files.length} edges=${sortedEdges.length} batches=${sccs.length} cycles=${cycles.length}`);
if (files.length > 1 && sortedEdges.length === 0) {
  console.error(
    "WARN: 0 edges across multiple files. If these files import each other, " +
    "--root is probably pointing at the wrong directory, or the imports use " +
    "bare specifiers / tsconfig path aliases (only relative specifiers are mapped)."
  );
}
