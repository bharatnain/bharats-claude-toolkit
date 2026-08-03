#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Deterministic dependency mapper for C/C++ codebases (stdlib only).

Implements the kit's dependency-map contract (prompts/01-dependency-map.md).
Parses `#include "..."` directives — quoted includes only. Angle-bracket
includes (<stdio.h>, <vector>) are system/third-party: neither edges nor
misses. Each .c/.cc/.cpp file is also linked to its same-stem header when one
exists, since implementation→own-header is a real migration-order edge.

This is a starter: it does not run the preprocessor, so includes hidden behind
#ifdef are all counted (conservative: more edges, never fewer). For production
runs on macro-heavy trees, generate edges with `gcc -MM` per file instead and
keep the output contract identical.

Usage:
  python3 depmap_c.py --root path/to/repo --out path/to/migration/depmap
Output: edges.tsv, order.txt, cycles.txt (same contract as depmap_python.py)

Test: python3 scripts/depmap_c.py --root fixtures/c --out /tmp/depmap-c && diff /tmp/depmap-c/edges.tsv fixtures/c/expected_edges.tsv && diff /tmp/depmap-c/cycles.txt fixtures/c/expected_cycles.txt && diff /tmp/depmap-c/order.txt fixtures/c/expected_order.txt
"""

import argparse
import re
import sys
from pathlib import Path

EXTS = {".c", ".h", ".cc", ".cpp", ".hpp", ".cxx", ".hxx"}
INCLUDE_RE = re.compile(r'^\s*#\s*include\s+"([^"]+)"', re.MULTILINE)
SKIP_DIRS = {".git", "build", "vendor", "third_party", "node_modules"}


def find_files(root: Path):
    return sorted(
        p for p in root.rglob("*")
        if p.suffix in EXTS
        and not any(part in SKIP_DIRS or part.startswith(".") for part in p.relative_to(root).parts)
    )


def extract_edges(files, root):
    rel = {p: p.relative_to(root).as_posix() for p in files}
    by_rel = {v: k for k, v in rel.items()}
    edges = set()
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for inc in INCLUDE_RE.findall(text):
            # resolve relative to including file, then repo root
            for cand in ((path.parent / inc), (root / inc)):
                try:
                    cand_rel = cand.resolve().relative_to(root).as_posix()
                except ValueError:
                    continue
                if cand_rel in by_rel:
                    if cand_rel != rel[path]:
                        edges.add((rel[path], cand_rel))
                    break
        # implementation -> own header
        if path.suffix in {".c", ".cc", ".cpp", ".cxx"}:
            for hext in (".h", ".hpp", ".hxx"):
                hdr = path.with_suffix(hext)
                if hdr in rel and rel[hdr] != rel[path]:
                    edges.add((rel[path], rel[hdr]))
    return sorted(edges), sorted(rel.values())


def tarjan_scc(nodes, edges):
    adj = {n: [] for n in nodes}
    for a, b in edges:
        adj[a].append(b)
    for n in adj:
        adj[n].sort()
    counter = [0]
    stack, on_stack = [], set()
    index, low = {}, {}
    sccs = []
    for start in nodes:
        if start in index:
            continue
        work = [(start, 0)]
        while work:
            node, pi = work[-1]
            if pi == 0:
                index[node] = low[node] = counter[0]
                counter[0] += 1
                stack.append(node)
                on_stack.add(node)
            recurse = False
            for i in range(pi, len(adj[node])):
                succ = adj[node][i]
                if succ not in index:
                    work[-1] = (node, i + 1)
                    work.append((succ, 0))
                    recurse = True
                    break
                elif succ in on_stack:
                    low[node] = min(low[node], index[succ])
            if recurse:
                continue
            if low[node] == index[node]:
                scc = []
                while True:
                    w = stack.pop()
                    on_stack.discard(w)
                    scc.append(w)
                    if w == node:
                        break
                sccs.append(sorted(scc))
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[node])
    return sccs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    root = args.root.resolve()
    files = find_files(root)
    edges, nodes = extract_edges(files, root)
    sccs = tarjan_scc(nodes, edges)
    cycles = [s for s in sccs if len(s) > 1]

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "edges.tsv").write_text("from\tto\n" + "".join(f"{a}\t{b}\n" for a, b in edges))
    (args.out / "order.txt").write_text(
        "# migration order: one batch per line, dependencies first\n"
        + "".join("\t".join(s) + "\n" for s in sccs))
    (args.out / "cycles.txt").write_text(
        f"# strongly connected components > 1 file: {len(cycles)}\n"
        + "".join("\t".join(s) + "\n" for s in cycles))
    print(f"files={len(files)} edges={len(edges)} batches={len(sccs)} cycles={len(cycles)}")
    if len(files) > 1 and not edges:
        print(
            "WARN: 0 edges across multiple files. If these files include each "
            "other, --root is probably pointing at the wrong directory, or the "
            '#include paths only resolve against -I include dirs (quoted '
            "includes are resolved relative to the including file, then the "
            "repo root; angle brackets are never edges).",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
