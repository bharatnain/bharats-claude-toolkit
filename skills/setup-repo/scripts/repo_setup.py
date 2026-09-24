#!/usr/bin/env python3
"""/setup-repo: detect a repo's stack, plan an optimal Claude Code setup, apply it. Stdlib only."""
import argparse, json, os, re, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLKIT_SCRIPTS = HERE.parents[2] / "scripts"  # skills/setup-repo/scripts -> repo root/scripts
LANG_EXT = {"python": [".py"], "typescript": [".ts", ".tsx"], "javascript": [".js", ".jsx", ".mjs"],
            "go": [".go"], "rust": [".rs"], "ruby": [".rb"]}
PM_FILES = [("uv.lock", "uv"), ("poetry.lock", "poetry"), ("Pipfile.lock", "pipenv"), ("requirements.txt", "pip"),
            ("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"), ("bun.lock", "bun"), ("bun.lockb", "bun"),
            ("package-lock.json", "npm"), ("go.mod", "go"), ("Cargo.toml", "cargo"), ("Gemfile.lock", "bundler")]
EXISTING = ["CLAUDE.md", ".claude/CLAUDE.md", "AGENTS.md", "CLAUDE.local.md", ".claude/settings.json",
            ".claude/team-profile.json", ".claude/hooks/lint_on_edit.py", ".beads", ".claude/rules"]

def _git(root, *args):
    try:
        p = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=20)
        return p.stdout.strip() if p.returncode == 0 else ""
    except Exception:  # noqa: BLE001
        return ""

def _tracked(root):
    out = _git(root, "ls-files")
    return [l for l in out.splitlines() if l]

def _languages(files):
    counts = {}
    for f in files:
        ext = os.path.splitext(f)[1]
        for lang, exts in LANG_EXT.items():
            if ext in exts:
                counts[lang] = counts.get(lang, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: -kv[1])[:5])

def _package_manager(root):
    for name, pm in PM_FILES:
        if (root / name).exists():
            return pm
    return None

def _existing(root):
    out = {}
    for rel in EXISTING:
        p = root / rel
        if p.is_file():
            out[rel] = {"exists": True, "lines": sum(1 for _ in p.open(encoding="utf-8", errors="replace"))}
        elif p.is_dir():
            out[rel] = {"exists": True, "lines": len(list(p.glob("*")))}
        else:
            out[rel] = {"exists": False, "lines": 0}
    return out

def detect(root):
    root = Path(root).resolve()
    files = _tracked(root)
    return {"root": str(root), "languages": _languages(files), "package_manager": _package_manager(root),
            "existing": _existing(root), "commands": {}, "git": {}, "team_profile": None, "size": len(files)}
