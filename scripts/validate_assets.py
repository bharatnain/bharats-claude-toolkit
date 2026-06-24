#!/usr/bin/env python3
"""Validate agents/, commands/, and workflows/ assets.

Stdlib-only for the Python parts; the ONLY external process call is
`node --check --input-type=module` (fed via stdin; node is already a documented
toolkit dependency for workflows/, so this introduces no NEW runtime dep).
Reuses parse_frontmatter from validate_skills.py rather than copy-pasting (DRY).

Decision (RECORDED): a SEPARATE script from validate_skills.py rather than
extending it. validate_skills.py is single-domain (skill/agent frontmatter +
the SKILLS.md catalog generator); asset validation adds orthogonal concerns
(node --check on JS, workflow meta parsing). Two small single-responsibility
scripts are simpler to maintain and independently CI-wireable than one bloated
file with two validators and two CLIs (CLAUDE.md section 2).

Output, --format text|github, and exit codes are IDENTICAL to
validate_skills.py so the two validators are interchangeable in CI.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skills import parse_frontmatter  # noqa: E402

META_RE = re.compile(r"export\s+const\s+meta\s*=\s*\{")
NAME_KEY_RE = re.compile(r"\bname\s*:")
DESC_KEY_RE = re.compile(r"\bdescription\s*:")
PHASES_KEY_RE = re.compile(r"\bphases\s*:")

# A *.workflow.js script is NOT a standalone module: the Workflow runtime hoists
# its `import`s, treats `export const meta` as a module export, and wraps the rest
# of the body — which uses top-level `return`/`await` — in an async function. So a
# plain `node --check <file>` can never pass on one. To syntax-check faithfully we
# reproduce that wrap (imports stay at module top; `export const meta` becomes a
# plain `const`; everything else goes inside an async function) and check the
# result as an ES module via stdin. lib/*.js are real modules, checked as-is.
IMPORT_RE = re.compile(r"^\s*import\b.*$", re.M)
EXPORT_META_RE = re.compile(r"\bexport\s+(const\s+meta\b)")


class Finding:
    def __init__(self, asset, path, level, code, msg):
        self.asset = asset
        self.path = path
        self.level = level  # "error" or "warn"
        self.code = code
        self.msg = msg


def parse_tools_list(raw):
    """Parse an inline array form ([\"Read\", \"Grep\"] or [Read, Grep]).

    Returns a list of strings on success, or None if not a well-formed list.
    """
    s = raw.strip()
    if not (s.startswith("[") and s.endswith("]")):
        return None
    inner = s[1:-1].strip()
    if inner == "":
        return []
    # Try strict JSON first (double-quoted form).
    try:
        val = json.loads(s)
        if isinstance(val, list) and all(isinstance(x, str) for x in val):
            return val
        return None
    except (ValueError, TypeError):
        pass
    # YAML inline form: bare or single-quoted items, e.g. [Read, Grep, 'Bash'].
    items = []
    for part in inner.split(","):
        item = part.strip()
        if len(item) >= 2 and item[0] == item[-1] and item[0] in ("'", '"'):
            item = item[1:-1]
        if not item:
            return None
        items.append(item)
    return items


def check_agents(root, findings):
    """agents/*.md: A1 name==stem, A2 description present + len[40,1024],
    A3 tools (if present) well-formed list."""
    count = 0
    agents_dir = root / "agents"
    if not agents_dir.is_dir():
        return count
    for md in sorted(agents_dir.glob("*.md")):
        count += 1
        rel = f"agents/{md.name}"
        keys, _ = parse_frontmatter(md.read_text(encoding="utf-8"))
        stem = md.stem

        name = keys.get("name", "").strip()
        if not name:
            findings.append(Finding("agents", str(md), "error", "A1",
                                    f"{rel}: 'name' missing or empty"))
        elif name != stem:
            findings.append(Finding("agents", str(md), "error", "A1",
                                    f"{rel}: name '{name}' != stem '{stem}'"))

        desc = keys.get("description", "").strip()
        if not desc:
            findings.append(Finding("agents", str(md), "error", "A2",
                                    f"{rel}: 'description' missing or empty"))
        elif not (40 <= len(desc) <= 1024):
            findings.append(Finding("agents", str(md), "error", "A2",
                                    f"{rel}: description length {len(desc)} out of [40,1024]"))

        if "tools" in keys:
            tools = parse_tools_list(keys["tools"])
            if tools is None:
                findings.append(Finding("agents", str(md), "error", "A3",
                                        f"{rel}: tools not a well-formed list"))
    return count


def check_commands(root, findings):
    """commands/*.md: C1 description present and non-empty."""
    count = 0
    commands_dir = root / "commands"
    if not commands_dir.is_dir():
        return count
    for md in sorted(commands_dir.glob("*.md")):
        count += 1
        rel = f"commands/{md.name}"
        keys, _ = parse_frontmatter(md.read_text(encoding="utf-8"))
        if not keys.get("description", "").strip():
            findings.append(Finding("commands", str(md), "error", "C1",
                                    f"{rel}: 'description' missing or empty"))
    return count


def check_meta(text, rel, path, findings):
    """W2: *.workflow.js text must contain `export const meta` with name +
    description + phases keys (light regex/parse — never executes the module)."""
    m = META_RE.search(text)
    if not m:
        findings.append(Finding("workflows", path, "error", "W2",
                                f"{rel}: missing 'export const meta'"))
        return
    block = text[m.end():]
    for key, regex in (("name", NAME_KEY_RE),
                       ("description", DESC_KEY_RE),
                       ("phases", PHASES_KEY_RE)):
        if not regex.search(block):
            findings.append(Finding("workflows", path, "error", "W2",
                                    f"{rel}: meta missing '{key}'"))


def node_check_source(source):
    """`node --check --input-type=module` on `source` via stdin.

    Returns (ok, detail). detail is the first stderr line on failure, or the
    sentinel "<node-missing>" when node is not installed (caller decides how to
    report — node is a documented workflow dependency, so missing is an error)."""
    try:
        proc = subprocess.run(
            ["node", "--check", "--input-type=module"],
            input=source, capture_output=True, text=True, timeout=20,
        )
    except FileNotFoundError:
        return False, "<node-missing>"
    if proc.returncode == 0:
        return True, ""
    return False, (proc.stderr.strip().splitlines() or ["syntax error"])[0]


def wrap_workflow_source(src):
    """Reproduce the Workflow runtime's wrap so a *.workflow.js body becomes a
    syntactically valid ES module: imports hoisted to module top, `export const
    meta` demoted to a plain `const`, and the rest wrapped in an async function
    (legalizing its top-level `return`/`await`)."""
    imports = IMPORT_RE.findall(src)
    body = IMPORT_RE.sub("", src)
    body = EXPORT_META_RE.sub(r"\1", body)
    return "\n".join(imports) + "\nasync function __wf(){\n" + body + "\n}\n"


def check_workflows(root, findings):
    """workflows/*.js AND workflows/lib/*.js: W1 `node --check` passes;
    *.workflow.js also: W2 meta has name+description+phases."""
    count = 0
    workflows_dir = root / "workflows"
    if not workflows_dir.is_dir():
        return count
    js_files = sorted(workflows_dir.glob("*.js")) + sorted((workflows_dir / "lib").glob("*.js"))
    for js in js_files:
        count += 1
        rel = str(js.relative_to(root))
        src = js.read_text(encoding="utf-8")
        is_workflow = js.name.endswith(".workflow.js")
        ok, detail = node_check_source(wrap_workflow_source(src) if is_workflow else src)
        if detail == "<node-missing>":
            # node missing: fail loudly so CI does not silently pass.
            findings.append(Finding("workflows", str(js), "error", "W1",
                                    f"{rel}: 'node' not found — cannot run node --check"))
            continue
        if not ok:
            findings.append(Finding("workflows", str(js), "error", "W1",
                                    f"{rel}: node --check failed: {detail}"))
        if is_workflow:
            check_meta(src, rel, str(js), findings)
    return count


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=None)
    ap.add_argument("--format", choices=["text", "github"], default="text")
    ap.add_argument("--warn-as-error", action="store_true")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent

    findings = []
    count = 0
    count += check_agents(root, findings)
    count += check_commands(root, findings)
    count += check_workflows(root, findings)

    errors = [f for f in findings if f.level == "error"]
    warns = [f for f in findings if f.level == "warn"]

    if args.format == "github":
        for f in findings:
            kind = "error" if f.level == "error" else "warning"
            print(f"::{kind} file={f.path}::[{f.code}] {f.asset}: {f.msg}")
    else:
        by_asset = {}
        for f in findings:
            by_asset.setdefault(f.asset, []).append(f)
        for asset in sorted(by_asset):
            for f in by_asset[asset]:
                label = "ERROR" if f.level == "error" else "WARN"
                print(f"{label} [{f.code}] {f.asset}: {f.msg}")

    print(f"{count} assets, {len(errors)} errors, {len(warns)} warnings")

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
