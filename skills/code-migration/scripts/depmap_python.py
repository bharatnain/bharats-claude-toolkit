#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Deterministic dependency mapper for Python codebases (stdlib only).

Implements the kit's dependency-map contract (prompts/01-dependency-map.md):
  - parses imports via ast (never regex, never agent judgment)
  - in-repo edges only: stdlib and third-party imports are neither edges nor misses
  - emits edges.tsv (one edge per line), order.txt (topological migration order,
    SCC-condensed), cycles.txt (every strongly connected component > 1 file)
  - all output is repo-relative FILE PATHS (e.g. toml/decoder.py), matching
    depmap_ts.mjs / depmap_c.py and the queue/manifest contract; dotted module
    names are used internally for import matching only

Usage:
  python3 depmap_python.py --root path/to/repo --out path/to/migration/depmap

Test: python3 scripts/depmap_python.py --root fixtures/python --out /tmp/depmap-py && diff /tmp/depmap-py/edges.tsv fixtures/python/expected_edges.tsv && diff /tmp/depmap-py/cycles.txt fixtures/python/expected_cycles.txt && diff /tmp/depmap-py/order.txt fixtures/python/expected_order.txt

Determinism: files walked in sorted order, edges and outputs sorted. Two runs
on the same tree produce byte-identical output.
"""

import argparse
import ast
import sys
from pathlib import Path

# Directories never walked. Any path component in this set — or starting with
# "." — is excluded. Kept visible at the top per CONTRIBUTING's requirement
# that the exclusion list be inspectable without reading the walker.
SKIP_DIRS = {"venv", "node_modules", "__pycache__", "generated"}


def find_py_files(root: Path):
    return sorted(
        p for p in root.rglob("*.py")
        if not any(part.startswith(".") or part in SKIP_DIRS
                   for part in p.relative_to(root).parts)
    )


def module_name(path: Path, root: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts) if parts else "__init__"


def build_module_index(files, root):
    return {module_name(p, root): p for p in files}


def resolve_import(node, current_mod, is_pkg, index):
    """Yield in-repo module names imported by this ast node. Unknown names are
    silently skipped — third-party is neither an edge nor a miss."""
    if isinstance(node, ast.Import):
        for alias in node.names:
            name = alias.name
            while name:
                if name in index:
                    yield name
                    break
                name = name.rpartition(".")[0]
    elif isinstance(node, ast.ImportFrom):
        if node.level:  # relative import
            # Anchor package: for pkg/__init__.py the module IS the package,
            # so level 1 means pkg itself; for pkg/mod.py drop the module name
            # first so level 1 also lands on pkg.
            base = current_mod.split(".")
            if not is_pkg:
                base = base[:-1]
            base = base[: max(0, len(base) - (node.level - 1))]
            mod = ".".join(base + ([node.module] if node.module else []))
        else:
            mod = node.module or ""
        candidates = [mod] + [f"{mod}.{alias.name}" for alias in node.names if mod]
        for cand in candidates:
            name = cand
            while name:
                if name in index:
                    yield name
                    break
                name = name.rpartition(".")[0]


def extract_edges(files, root):
    """Return (sorted path edges, sorted path nodes). Import matching happens
    on dotted module names; edges are mapped back to repo-relative paths."""
    index = build_module_index(files, root)
    rel = {p: p.relative_to(root).as_posix() for p in files}
    edges = set()
    for path in files:
        src_mod = module_name(path, root)
        is_pkg = path.name == "__init__.py"
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError as e:
            print(f"WARN unparseable, no edges emitted: {path} ({e})", file=sys.stderr)
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for dep_mod in resolve_import(node, src_mod, is_pkg, index):
                    if dep_mod != src_mod:
                        edges.add((rel[path], rel[index[dep_mod]]))
    return sorted(edges), sorted(rel.values())


def tarjan_scc(nodes, edges):
    """Iterative Tarjan. Returns list of SCCs (each a sorted list of nodes),
    in reverse topological order of the condensation."""
    adj = {n: [] for n in nodes}
    for a, b in edges:
        adj[a].append(b)
    for n in adj:
        adj[n].sort()
    index_counter = [0]
    stack, on_stack = [], set()
    index, lowlink = {}, {}
    sccs = []

    for start in sorted(nodes):
        if start in index:
            continue
        work = [(start, 0)]
        while work:
            node, pi = work[-1]
            if pi == 0:
                index[node] = lowlink[node] = index_counter[0]
                index_counter[0] += 1
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
                    lowlink[node] = min(lowlink[node], index[succ])
            if recurse:
                continue
            if lowlink[node] == index[node]:
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
                lowlink[parent] = min(lowlink[parent], lowlink[node])
    return sccs


def migration_order(nodes, edges):
    """Topological order over the SCC condensation: dependencies first.
    Returns (ordered list of SCCs, cycles)."""
    sccs = tarjan_scc(nodes, edges)
    # Tarjan emits SCCs in reverse topological order of the condensation
    # (a component is finished only after everything it depends on);
    # dependencies-first = the order Tarjan finished them.
    cycles = [s for s in sccs if len(s) > 1]
    return sccs, cycles


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    root = args.root.resolve()
    files = find_py_files(root)
    edges, nodes = extract_edges(files, root)
    order, cycles = migration_order(nodes, edges)

    args.out.mkdir(parents=True, exist_ok=True)
    with open(args.out / "edges.tsv", "w") as f:
        f.write("from\tto\n")
        for a, b in edges:
            f.write(f"{a}\t{b}\n")
    with open(args.out / "order.txt", "w") as f:
        f.write("# migration order: one batch per line, dependencies first\n")
        for scc in order:
            f.write("\t".join(scc) + "\n")
    with open(args.out / "cycles.txt", "w") as f:
        f.write(f"# strongly connected components > 1 file: {len(cycles)}\n")
        for scc in cycles:
            f.write("\t".join(scc) + "\n")

    print(f"files={len(files)} edges={len(edges)} batches={len(order)} cycles={len(cycles)}")
    print(f"wrote {args.out}/edges.tsv, order.txt, cycles.txt")
    if len(files) > 1 and not edges:
        print(
            "WARN: 0 edges across multiple files. If these files import each "
            "other, --root is probably pointing at the package directory "
            "instead of the repo root (imports like 'pkg.mod' can't resolve "
            "when the module index says 'mod').",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
