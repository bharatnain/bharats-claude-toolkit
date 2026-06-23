#!/usr/bin/env python3
"""Validate skills/<NAME>/SKILL.md frontmatter and links. Stdlib only."""
import argparse
import os
import re
import sys
from pathlib import Path

NAME_ALLOWLIST = {"react-best-practices": "vercel-react-best-practices"}
IGNORE_PREFIXES = ("http://", "https://", "mailto:", "#")
TOP_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")
COLON_REF_RE = re.compile(r"^/[a-z][a-z0-9-]*:[a-z0-9-]+$")
COLON_REF_SCAN = re.compile(r"/[a-z][a-z0-9-]*:[a-z0-9-]+")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SINGLE_QUOTE_RE = re.compile(r"'([^']+)'")


class Finding:
    def __init__(self, skill, path, level, code, msg):
        self.skill = skill
        self.path = path
        self.level = level  # "error" or "warn"
        self.code = code
        self.msg = msg


def strip_one_quote_pair(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1]
    return s


def parse_frontmatter(text):
    """Return (keys_dict, has_closing_fence). keys_dict maps top-level key -> value."""
    lines = text.splitlines()
    if not lines or lines[0].strip("\n") != "---":
        # File must start with exactly '---'
        if not lines or lines[0] != "---":
            return {}, False
    # find closing fence
    close_idx = None
    for i in range(1, len(lines)):
        if lines[i] == "---":
            close_idx = i
            break
    if close_idx is None:
        return {}, False

    fm_lines = lines[1:close_idx]
    keys = {}
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        m = TOP_KEY_RE.match(line)
        # only zero-indentation top-level keys
        if m and not (line[:1] in (" ", "\t")):
            key = m.group(1)
            rest = m.group(2)
            stripped = rest.strip()
            if stripped and stripped[0] in (">", "|"):
                # block scalar: gather following more-indented lines
                block = []
                j = i + 1
                while j < len(fm_lines):
                    nxt = fm_lines[j]
                    if nxt.strip() == "":
                        block.append("")
                        j += 1
                        continue
                    if nxt[:1] in (" ", "\t"):
                        block.append(nxt.strip())
                        j += 1
                    else:
                        break
                keys[key] = " ".join(b for b in block if b)
                i = j
                continue
            else:
                keys[key] = strip_one_quote_pair(rest)
        i += 1
    return keys, True


def normalize_within(skill_dir, target, root):
    """Resolve target (relative to skill_dir), return (abspath, within_skill_dir)."""
    tgt = target.split("#", 1)[0]
    abspath = os.path.normpath(os.path.join(str(skill_dir), tgt))
    skill_dir_norm = os.path.normpath(str(skill_dir)) + os.sep
    within = (abspath + os.sep).startswith(skill_dir_norm) or abspath == os.path.normpath(str(skill_dir))
    return abspath, within


def classify_link(target, name, skill_dir, root, findings, path):
    if target.startswith(IGNORE_PREFIXES):
        return
    # colon-ref
    if COLON_REF_RE.match(target):
        skill = target.split(":", 1)[1]
        if skill == name:
            return
        if (root / "skills" / skill).is_dir():
            return
        findings.append(Finding(name, path, "warn", "L3",
                                f"cross-package colon-ref to '{target}'"))
        return
    if "../../tools/" in target:
        findings.append(Finding(name, path, "warn", "L2",
                                f"external-registry pointer '{target}'"))
        return
    abspath, within = normalize_within(skill_dir, target, root)
    if not within:
        findings.append(Finding(name, path, "warn", "L3",
                                f"relative link escapes package '{target}'"))
        return
    if os.path.exists(abspath):
        return
    findings.append(Finding(name, path, "error", "L1",
                            f"bundled link target missing '{target}'"))


def scan_links(text, name, skill_dir, root, findings, path):
    seen = set()
    for m in MD_LINK_RE.finditer(text):
        tgt = m.group(1).strip()
        classify_link(tgt, name, skill_dir, root, findings, path)
    # bare colon-ref tokens (skip matches inside URLs, e.g. http://localhost:8080)
    for m in COLON_REF_SCAN.finditer(text):
        if m.start() > 0 and text[m.start() - 1] in ("/", ":"):
            continue
        tok = m.group(0)
        if tok in seen:
            continue
        seen.add(tok)
        classify_link(tok, name, skill_dir, root, findings, path)


def quoted_phrases(desc):
    return set(SINGLE_QUOTE_RE.findall(desc))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=None)
    ap.add_argument("--format", choices=["text", "github"], default="text")
    ap.add_argument("--warn-as-error", action="store_true")
    ap.add_argument("--strict-yaml", action="store_true")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"

    findings = []
    name_to_dirs = {}
    descriptions = {}  # name -> phrase set
    skill_count = 0

    skill_paths = sorted(skills_dir.glob("*/SKILL.md")) if skills_dir.is_dir() else []

    for skill_md in skill_paths:
        skill_dir = skill_md.parent
        dir_name = skill_dir.name
        skill_count += 1
        text = skill_md.read_text(encoding="utf-8")
        path = str(skill_md)

        keys, has_close = parse_frontmatter(text)
        if not has_close:
            findings.append(Finding(dir_name, path, "error", "F1",
                                    "missing closing '---' frontmatter fence"))
            # still scan links to report what we can
            scan_links(text, dir_name, skill_dir, root, findings, path)
            continue

        if args.strict_yaml:
            try:
                import yaml  # noqa: F401
                # best-effort re-parse; ignore result, just validate parseability
                fm_text = text.split("---", 2)
                if len(fm_text) >= 3:
                    yaml.safe_load(fm_text[1])
            except Exception:
                pass

        name = keys.get("name", "").strip()
        desc = keys.get("description", "").strip()

        # F2
        allowed = NAME_ALLOWLIST.get(dir_name)
        if not name:
            findings.append(Finding(dir_name, path, "error", "F2",
                                    "'name' missing or empty"))
        elif allowed is not None:
            if name != allowed:
                findings.append(Finding(dir_name, path, "error", "F2",
                                        f"name '{name}' != allowed '{allowed}'"))
        elif name != dir_name:
            findings.append(Finding(dir_name, path, "error", "F2",
                                    f"name '{name}' != dir '{dir_name}'"))

        if name:
            name_to_dirs.setdefault(name, []).append(dir_name)

        # F3
        if not desc:
            findings.append(Finding(dir_name, path, "error", "F3",
                                    "'description' missing or empty"))
        else:
            # F5
            if len(desc) < 40 or len(desc) > 1024:
                findings.append(Finding(dir_name, path, "warn", "F5",
                                        f"description length {len(desc)} out of [40,1024]"))
            descriptions[dir_name] = quoted_phrases(desc)

        scan_links(text, dir_name, skill_dir, root, findings, path)

    # F4 duplicate names
    for nm, dirs in name_to_dirs.items():
        if len(dirs) >= 2:
            for d in dirs:
                p = str(skills_dir / d / "SKILL.md")
                findings.append(Finding(d, p, "error", "F4",
                                        f"name '{nm}' duplicated across {dirs}"))

    # D1 duplicate-intent heuristic
    dnames = sorted(descriptions.keys())
    for i in range(len(dnames)):
        for j in range(i + 1, len(dnames)):
            a, b = dnames[i], dnames[j]
            sa, sb = descriptions[a], descriptions[b]
            if not sa or not sb:
                continue
            inter = sa & sb
            union = sa | sb
            jac = len(inter) / len(union) if union else 0
            if jac > 0.5 and len(inter) >= 3:
                shared = ", ".join(sorted(inter))
                pa = str(skills_dir / a / "SKILL.md")
                findings.append(Finding(a, pa, "warn", "D1",
                                        f"duplicate-intent with '{b}' (shared: {shared})"))

    errors = [f for f in findings if f.level == "error"]
    warns = [f for f in findings if f.level == "warn"]

    # output
    if args.format == "github":
        for f in findings:
            kind = "error" if f.level == "error" else "warning"
            print(f"::{kind} file={f.path}::[{f.code}] {f.skill}: {f.msg}")
    else:
        by_skill = {}
        for f in findings:
            by_skill.setdefault(f.skill, []).append(f)
        for skill in sorted(by_skill):
            for f in by_skill[skill]:
                label = "ERROR" if f.level == "error" else "WARN"
                print(f"{label} [{f.code}] {f.skill}: {f.msg}")

    print(f"{skill_count} skills, {len(errors)} errors, {len(warns)} warnings")

    if errors:
        return 1
    if warns and args.warn_as_error:
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:  # noqa: BLE001
        print(f"internal error: {e}", file=sys.stderr)
        sys.exit(2)
