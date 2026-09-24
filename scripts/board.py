#!/usr/bin/env python3
"""Orchestrator board: one generated page of everything in flight for a repo. Stdlib only, read-only."""
import argparse, datetime as dt, html, json, os, re, subprocess, sys, tempfile, webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAIL_BYTES = 512 * 1024
sys.path.insert(0, str(ROOT / "hooks"))
try:
    from secret_scan import PATTERNS as _SECRET_PATTERNS  # noqa: E402
except Exception:  # noqa: BLE001
    _SECRET_PATTERNS = []

def redact(text):
    for _name, rx, _f in _SECRET_PATTERNS:
        text = rx.sub("[redacted]", text)
    return text

def _parse_ts(ts):
    try:
        t = dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        if t.tzinfo is None: t = t.replace(tzinfo=dt.timezone.utc)
        return t
    except Exception: return None  # noqa: BLE001

def _tail_lines(path):
    with path.open("rb") as fh:
        fh.seek(0, 2); size = fh.tell(); fh.seek(max(0, size - TAIL_BYTES))
        data = fh.read().decode("utf-8", errors="replace")
    lines = data.split("\n")
    return lines[1:] if size > TAIL_BYTES else lines

def _objs(path):
    for line in _tail_lines(path):
        if not line.strip(): continue
        try: yield json.loads(line)
        except Exception: continue  # noqa: BLE001

def project_dirs_for(repo_root, projects_dir):
    enc = str(Path(repo_root).resolve()).replace("/", "-")
    return sorted(p for p in Path(projects_dir).glob(enc + "*") if p.is_dir())

def _subagents(sess_dir, now, since):
    out = []
    sub = sess_dir / "subagents"
    if not sub.is_dir(): return out
    for f in sorted(sub.glob("agent-*.jsonl")):
        aid = f.stem.replace("agent-", ""); model = None; tools = 0; last = None
        for o in _objs(f):
            ts = _parse_ts(o.get("timestamp", "")) or last; last = ts or last
            att = o.get("attachment") or {}
            if att.get("type") == "model": model = (att.get("identity") or {}).get("modelId")
            if o.get("type") == "assistant":
                for b in (o.get("message") or {}).get("content") or []:
                    if isinstance(b, dict) and b.get("type") == "tool_use": tools += 1
        meta = {}
        mp = f.with_name(f.stem + ".meta.json")
        if mp.exists():
            try: meta = json.loads(mp.read_text(encoding="utf-8"))
            except Exception: meta = {}  # noqa: BLE001
        running = bool(last and (now - last) <= dt.timedelta(minutes=since))
        out.append({"id": aid, "name": meta.get("description") or aid, "model": model, "tool_uses": tools, "running": running, "last_at": last.isoformat() if last else None})
    return out

def collect_sessions(repo_root, projects_dir, now, since_minutes=5):
    sessions = []
    for proj in project_dirs_for(repo_root, projects_dir):
        for f in sorted(proj.glob("*.jsonl")):
            sid = f.stem; title = sid; model = None; branch = None; last = None; tokens = 0; last_text = ""; question = None
            for o in _objs(f):
                t = o.get("type")
                if t == "custom-title": title = o.get("customTitle") or title
                if t != "assistant": continue
                ts = _parse_ts(o.get("timestamp", "")); last = ts or last
                branch = o.get("gitBranch") or branch
                msg = o.get("message") or {}; model = msg.get("model") or model
                u = msg.get("usage") or {}; tokens += int(u.get("input_tokens", 0)) + int(u.get("output_tokens", 0))
                question = None
                for b in msg.get("content") or []:
                    if not isinstance(b, dict): continue
                    if b.get("type") == "text" and b.get("text"): last_text = b["text"]
                    if b.get("type") == "tool_use" and b.get("name") == "AskUserQuestion":
                        qs = (b.get("input") or {}).get("questions") or []
                        question = qs[0].get("question") if qs and isinstance(qs[0], dict) else "question pending"
            running = bool(last and (now - last) <= dt.timedelta(minutes=since_minutes))
            sessions.append({"id": sid, "title": title, "model": model, "branch": branch, "last_at": last.isoformat() if last else None,
                             "running": running, "tokens": tokens, "last_text": redact(" ".join(last_text.split())[:300]),
                             "waiting_question": question, "subagents": _subagents(proj / sid, now, since_minutes)})
    sessions.sort(key=lambda s: s["last_at"] or "", reverse=True)
    return sessions

def _run(args, cwd, run):
    try:
        return run(args, cwd=str(cwd), capture_output=True, text=True, timeout=20)
    except Exception as e:  # noqa: BLE001
        class R: pass
        r = R(); r.returncode = 1; r.stdout = ""; r.stderr = str(e); return r

def _label(labels, key):
    for l in labels or []:
        if l.startswith(key + ":"): return l.split(":", 1)[1]
    return None

def collect_beads(repo_root, run=subprocess.run):
    r = _run(["bd", "list", "--json", "--status", "open,in_progress,blocked"], repo_root, run)
    if r.returncode != 0 or not r.stdout.strip():
        return {"in_flight": [], "epics": [], "counts": {}, "recent_closed": [], "error": f"bd unavailable: {(r.stderr or 'no output').strip()[:120]}"}
    try: issues = json.loads(r.stdout)
    except json.JSONDecodeError as e:
        return {"in_flight": [], "epics": [], "counts": {}, "recent_closed": [], "error": f"bd JSON: {e}"}
    counts = {}
    for i in issues: counts[i.get("status", "?")] = counts.get(i.get("status", "?"), 0) + 1
    epics = [i for i in issues if i.get("issue_type") == "epic"]
    in_flight = [{"id": i["id"], "title": i.get("title", ""), "status": i.get("status"), "owner": i.get("owner") or "", "parent": i.get("parent"),
                  "model": _label(i.get("labels"), "model"), "tries": _label(i.get("labels"), "tries"), "slice": _label(i.get("labels"), "slice"),
                  "needs_input": "needs-input" in (i.get("labels") or []), "updated": i.get("updated_at")}
                 for i in issues if i.get("issue_type") != "epic" and i.get("status") in ("in_progress", "open", "blocked")]
    in_flight.sort(key=lambda x: (x["status"] != "in_progress", x["updated"] or ""), reverse=False)
    rc = _run(["bd", "list", "--json", "--status", "closed"], repo_root, run)
    recent = []
    if rc.returncode == 0 and rc.stdout.strip():
        try: recent = sorted(json.loads(rc.stdout), key=lambda i: i.get("closed_at") or "", reverse=True)[:5]
        except json.JSONDecodeError: recent = []
    return {"in_flight": in_flight, "epics": [{"id": e["id"], "title": e.get("title", ""), "status": e.get("status")} for e in epics], "counts": counts,
            "recent_closed": [{"id": i["id"], "title": i.get("title", "")} for i in recent]}

def collect_prs(repo_root, run=subprocess.run):
    r = _run(["gh", "pr", "list", "--json", "number,title,headRefName,isDraft,statusCheckRollup,updatedAt,url", "--limit", "30"], repo_root, run)
    if r.returncode != 0 or not r.stdout.strip(): return []
    try: prs = json.loads(r.stdout)
    except json.JSONDecodeError: return []
    out = []
    for p in prs:
        concl = [(c.get("conclusion") or c.get("state") or "").upper() for c in p.get("statusCheckRollup") or []]
        checks = "none" if not concl else ("failed" if any(c in ("FAILURE", "ERROR", "CANCELLED") for c in concl) else ("passed" if all(c in ("SUCCESS", "NEUTRAL", "SKIPPED") for c in concl) else "pending"))
        out.append({"number": p["number"], "title": p.get("title", ""), "head": p.get("headRefName"), "draft": bool(p.get("isDraft")), "checks": checks, "updated": p.get("updatedAt"), "url": p.get("url")})
    return out

def collect_waiting(repo_root, sessions, beads, prs):
    items = []
    wf = Path(repo_root) / ".claude/board/waiting.md"
    if wf.exists():
        for line in wf.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip().startswith("- "): items.append({"source": "waiting.md", "text": line.strip()[2:], "at": None})
    for s in sessions:
        if s.get("waiting_question"): items.append({"source": "session", "text": f"{s['title']}: {s['waiting_question']}", "at": s["last_at"]})
    for i in beads.get("in_flight", []):
        if i["needs_input"]: items.append({"source": "beads", "text": f"{i['id']} {i['title']}", "at": i["updated"]})
    for p in prs:
        if p["checks"] == "failed": items.append({"source": "pr", "text": f"#{p['number']} {p['title']}: checks failed", "at": p["updated"]})
    seen = set(); out = []
    for it in items:
        if it["text"] in seen: continue
        seen.add(it["text"]); out.append(it)
    return sorted(out, key=lambda x: x["at"] or "", reverse=True)

def collect_now(sessions, beads):
    active = next((s for s in sessions if s["last_text"]), None)
    epic = next((e["title"] for e in beads.get("epics", []) if e.get("status") == "in_progress"), None)
    return {"text": active["last_text"] if active else "", "session": active["title"] if active else None, "epic": epic}
