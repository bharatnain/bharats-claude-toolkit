#!/usr/bin/env python3
"""Local skill-usage report (a /skill-doctor stand-in). Stdlib only, read-only.

Scans Claude Code transcripts under ~/.claude/projects/*/*.jsonl for `Skill`
tool invocations and slash commands, then reports:

  1. invoked skills in the window (uses, sessions, last used, plugin)
  2. vendored skills in THIS repo never invoked in the window, largest
     description first (description chars are the always-on context cost)
  3. enabled plugins (settings.json) with zero invocations
  4. a summary line with the always-on description budget

Nothing is deleted or modified. Use --prune-list to print never-invoked
vendored skill directory names for a manual review.

Report family: --format human|json (like check_upstream.py / doctor.py).
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CMD_RE = re.compile(r"<command-name>/([^<\s]+)</command-name>")


def iter_events(projects_dir):
    """Yield (timestamp, session_id, kind, name) for Skill tool_use + slash commands."""
    for path in sorted(projects_dir.glob("*/*.jsonl")):
        try:
            fh = path.open(encoding="utf-8", errors="replace")
        except OSError:
            continue
        with fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except Exception:  # noqa: BLE001 - skip malformed lines
                    continue
                ts = obj.get("timestamp")
                sid = obj.get("sessionId") or path.stem
                msg = obj.get("message") or {}
                content = msg.get("content")
                if obj.get("type") == "assistant" and isinstance(content, list):
                    for block in content:
                        if (isinstance(block, dict) and block.get("type") == "tool_use"
                                and block.get("name") == "Skill"):
                            skill = (block.get("input") or {}).get("skill")
                            if skill:
                                yield ts, sid, "skill", skill
                elif obj.get("type") == "user":
                    text = content if isinstance(content, str) else json.dumps(content)
                    for m in CMD_RE.finditer(text or ""):
                        yield ts, sid, "slash", "/" + m.group(1)


def parse_ts(ts):
    if not ts:
        return None
    try:
        return dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def repo_skills(root):
    """{dir_name: description_chars} for skills/*/SKILL.md (skips _lib)."""
    out = {}
    for skill_md in sorted((root / "skills").glob("*/SKILL.md")):
        name = skill_md.parent.name
        if name.startswith("_"):
            continue
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^description:\s*(.*?)(?=^\S|\Z)", text.split("\n---", 1)[0] + "\n", re.M | re.S)
        desc = m.group(1).strip() if m else ""
        out[name] = len(desc)
    return out


def enabled_plugins(root):
    try:
        data = json.loads((root / "settings.json").read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return []
    return [k for k, v in (data.get("enabledPlugins") or {}).items() if v]


def build_report(projects_dir, root, days, now):
    cutoff = now - dt.timedelta(days=days) if days > 0 else None
    window = {}   # name -> {"uses", "sessions": set, "last"}
    ever = {}     # name -> uses (all time)
    for ts, sid, kind, name in iter_events(projects_dir):
        t = parse_ts(ts)
        ever[name] = ever.get(name, 0) + 1
        if cutoff and (t is None or t < cutoff):
            continue
        rec = window.setdefault(name, {"uses": 0, "sessions": set(), "last": None, "kind": kind})
        rec["uses"] += 1
        rec["sessions"].add(sid)
        if t and (rec["last"] is None or t > rec["last"]):
            rec["last"] = t

    vendored = repo_skills(root)
    this_plugin = "bharats-claude-toolkit"
    invoked_here = {n.split(":", 1)[1] for n in window if n.startswith(this_plugin + ":")}
    invoked_here_ever = {n.split(":", 1)[1] for n in ever if n.startswith(this_plugin + ":")}
    never = [(n, c, n in invoked_here_ever) for n, c in vendored.items() if n not in invoked_here]
    never.sort(key=lambda x: -x[1])

    plugins = enabled_plugins(root)
    used_plugins = {n.split(":", 1)[0] for n in window if ":" in n}
    idle_plugins = [p for p in plugins if p.split("@", 1)[0] not in used_plugins]

    rows = sorted(window.items(), key=lambda kv: (-kv[1]["uses"], kv[0]))
    return {
        "window_days": days,
        "generated_at": now.isoformat(timespec="seconds"),
        "invoked": [
            {"name": n, "kind": r["kind"], "uses": r["uses"], "sessions": len(r["sessions"]),
             "last_used": r["last"].date().isoformat() if r["last"] else None}
            for n, r in rows
        ],
        "never_invoked_vendored": [
            {"skill": n, "description_chars": c, "used_before_window": before} for n, c, before in never
        ],
        "idle_enabled_plugins": idle_plugins,
        "summary": {
            "invocations": sum(r["uses"] for r in window.values()),
            "distinct": len(window),
            "vendored_skills": len(vendored),
            "vendored_invoked": len(invoked_here),
            "always_on_description_chars": sum(vendored.values()),
            "always_on_description_tokens_est": sum(vendored.values()) // 4,
        },
    }


def render_human(rep, top):
    s = rep["summary"]
    lines = [
        f"Skill usage — last {rep['window_days']} days (generated {rep['generated_at']})",
        "",
        f"{s['invocations']} invocations across {s['distinct']} distinct skills/commands; "
        f"{s['vendored_invoked']} of {s['vendored_skills']} vendored skills fired. "
        f"Always-on description budget: ~{s['always_on_description_tokens_est']:,} tokens "
        f"({s['always_on_description_chars']:,} chars).",
        "",
        "| skill / command | uses | sessions | last used |",
        "|---|---|---|---|",
    ]
    for r in rep["invoked"][:top]:
        lines.append(f"| {r['name']} | {r['uses']} | {r['sessions']} | {r['last_used'] or '?'} |")
    if len(rep["invoked"]) > top:
        lines.append(f"| … {len(rep['invoked']) - top} more | | | |")
    never = rep["never_invoked_vendored"]
    lines += ["", f"Never invoked in window: {len(never)} vendored skills "
              f"({sum(x['description_chars'] for x in never):,} description chars). Largest first:", ""]
    lines += ["| skill | description chars | used before window |", "|---|---|---|"]
    for x in never[:top]:
        lines.append(f"| {x['skill']} | {x['description_chars']} | {'yes' if x['used_before_window'] else 'no'} |")
    if len(never) > top:
        lines.append(f"| … {len(never) - top} more (use --top or --format json) | | |")
    lines += ["", "Enabled plugins with zero invocations in window: "
              + (", ".join(rep["idle_enabled_plugins"]) if rep["idle_enabled_plugins"] else "none"), ""]
    lines.append("Prune candidates = never invoked AND not used before the window. "
                 "Run with --prune-list for the bare directory names. Nothing is deleted by this script.")
    return "\n".join(lines)


def main(argv):
    ap = argparse.ArgumentParser(description="Local skill-usage report from Claude Code transcripts (read-only).")
    ap.add_argument("--days", type=int, default=30, help="window in days (0 = all time)")
    ap.add_argument("--top", type=int, default=25, help="rows per table in human output")
    ap.add_argument("--projects-dir", default=os.path.expanduser("~/.claude/projects"))
    ap.add_argument("--format", choices=["human", "json"], default="human")
    ap.add_argument("--prune-list", action="store_true",
                    help="print only vendored skill dirs never invoked (window AND before), one per line")
    args = ap.parse_args(argv)

    projects_dir = Path(args.projects_dir)
    if not projects_dir.is_dir():
        print(f"no transcripts dir at {projects_dir}", file=sys.stderr)
        return 1
    rep = build_report(projects_dir, ROOT, args.days, dt.datetime.now(dt.timezone.utc))
    if args.prune_list:
        for x in rep["never_invoked_vendored"]:
            if not x["used_before_window"]:
                print(x["skill"])
        return 0
    print(json.dumps(rep, indent=2) if args.format == "json" else render_human(rep, args.top))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:  # noqa: BLE001
        print(f"internal error: {e}", file=sys.stderr)
        sys.exit(2)
