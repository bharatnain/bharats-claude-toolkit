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

CSS = """:root{--bg:#fff;--fg:#111;--mut:#666;--card:#f6f6f7;--ok:#1a7f37;--bad:#b42318;--warn:#b54708;--acc:#2f5fdc}
@media(prefers-color-scheme:dark){:root{--bg:#0f1115;--fg:#e6e6e6;--mut:#9a9a9a;--card:#171a21;--ok:#3fb950;--bad:#f85149;--warn:#d29922;--acc:#79a6ff}}
body{margin:0;padding:16px;font:14px/1.45 -apple-system,Segoe UI,sans-serif;background:var(--bg);color:var(--fg)}
h1{font-size:20px;margin:0 0 4px}h2{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);margin:20px 0 8px}
.card{background:var(--card);border-radius:8px;padding:12px}.meta{color:var(--mut)}.grid{display:grid;gap:12px;grid-template-columns:1fr}
@media(min-width:900px){.grid{grid-template-columns:3fr 2fr}}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:4px 6px;vertical-align:top}
th{color:var(--mut);font-weight:600;font-size:12px}.b{display:inline-block;padding:1px 7px;border-radius:10px;font-size:11px;border:1px solid var(--mut)}
.ok{color:var(--ok);border-color:var(--ok)}.bad{color:var(--bad);border-color:var(--bad)}.warn{color:var(--warn);border-color:var(--warn)}.acc{color:var(--acc);border-color:var(--acc)}
.wait{border-left:4px solid var(--warn)}.unavail{color:var(--mut);font-style:italic}"""

def _e(x): return html.escape(str(x if x is not None else ""))
def _badge(text, cls=""): return f'<span class="b {cls}">{_e(text)}</span>'
def _rel(ts, now):
    t = _parse_ts(ts) if ts else None
    if not t: return "?"
    m = int((now - t).total_seconds() // 60)
    return f"{m}m ago" if m < 60 else (f"{m // 60}h ago" if m < 1440 else f"{m // 1440}d ago")

def render(data, now=None):
    now = now or dt.datetime.now(dt.timezone.utc); m = data["meta"]; parts = []
    unavail = {e.split(":", 1)[0]: e.split(":", 1)[1].strip() for e in data["errors"] if ":" in e}
    parts.append(f'<h1>{_e(m["repo"])} · orchestrator board</h1><div class="meta">{_e(m["branch"])} {_e(m["head"])} · built {_e(m["built_at"])}</div>')
    w = data["waiting"]
    parts.append('<h2>Waiting on you</h2><div class="card wait">' + ("<ol>" + "".join(f"<li>{_e(x['text'])} <span class='meta'>({_e(x['source'])}, {_rel(x['at'], now)})</span></li>" for x in w) + "</ol>" if w else "Nothing.") + "</div>")
    n = data["now"]
    parts.append('<h2>Now</h2><div class="card">' + (f"<div>{_e(n['text'])}</div><div class='meta'>{_e(n['session'] or '')}{' · epic: ' + _e(n['epic']) if n['epic'] else ''}</div>" if n["text"] or n["epic"] else "No recent activity.") + "</div>")
    parts.append('<div class="grid"><div>')
    b = data["beads"]
    beads_reason = b.get("error") or unavail.get("beads")
    if beads_reason: parts.append(f'<h2>In flight</h2><div class="card unavail">unavailable: {_e(beads_reason)}</div>')
    else:
        rows = "".join(f"<tr><td>{_e(i['id'])}</td><td>{_e(i['title'])}</td><td>{_badge(i['status'], 'acc' if i['status']=='in_progress' else '')}</td><td>{_e(i['owner'])}</td><td>{_e(i['model'] or '')}</td><td>{_e(i['tries'] or '')}</td><td class='meta'>{_rel(i['updated'], now)}</td></tr>" for i in b["in_flight"])
        parts.append(f'<h2>In flight · {len(b["in_flight"])}</h2><div class="card"><table><tr><th>id</th><th>task</th><th>state</th><th>owner</th><th>model</th><th>tries</th><th></th></tr>{rows or "<tr><td colspan=7>Nothing in flight.</td></tr>"}</table></div>')
    if "sessions" in unavail:
        parts.append(f'<h2>Sessions and agents</h2><div class="card unavail">unavailable: {_e(unavail["sessions"])}</div>')
    else:
        srows = []
        for s in data["sessions"]:
            srows.append(f"<tr><td>{_badge('running' if s['running'] else 'idle', 'ok' if s['running'] else '')}</td><td>{_e(s['title'])}</td><td>{_e(s['model'] or '')}</td><td>{_e(s['branch'] or '')}</td><td>{s['tokens']:,}</td><td class='meta'>{_rel(s['last_at'], now)}</td></tr>")
            for a in s["subagents"]:
                srows.append(f"<tr><td></td><td>↳ {_e(a['name'])}</td><td>{_e(a['model'] or '')}</td><td>{_badge('running' if a['running'] else 'done', 'ok' if a['running'] else '')}</td><td>{a['tool_uses']} tools</td><td class='meta'>{_rel(a['last_at'], now)}</td></tr>")
        parts.append(f'<h2>Sessions and agents · {len(data["sessions"])}</h2><div class="card"><table><tr><th></th><th>session / agent</th><th>model</th><th>branch</th><th>tokens</th><th></th></tr>{"".join(srows) or "<tr><td colspan=6>No sessions found.</td></tr>"}</table></div>')
    parts.append('</div><div>')
    if "prs" in unavail:
        parts.append(f'<h2>Merge lane</h2><div class="card unavail">unavailable: {_e(unavail["prs"])}</div>')
    else:
        prs = data["prs"]; cls = {"passed": "ok", "failed": "bad", "pending": "warn", "none": ""}
        prow = "".join(f"<tr><td><a href='{_e(p['url'])}'>#{p['number']}</a></td><td>{_e(p['title'])}{' ' + _badge('draft') if p['draft'] else ''}</td><td>{_badge(p['checks'], cls[p['checks']])}</td><td class='meta'>{_rel(p['updated'], now)}</td></tr>" for p in prs)
        parts.append(f'<h2>Merge lane · {len(prs)} open</h2><div class="card"><table>{prow or "<tr><td>No open PRs (or gh unavailable).</td></tr>"}</table></div>')
    counts = ", ".join(f"{k}: {v}" for k, v in sorted(b.get("counts", {}).items()))
    closed = "".join(f"<li>{_e(i['id'])} {_e(i['title'])}</li>" for i in b.get("recent_closed", []))
    parts.append(f'<h2>Backlog</h2><div class="card">{_e(counts) or "—"}<ul>{closed}</ul></div>')
    if data["errors"]: parts.append('<h2>Unavailable</h2><div class="card unavail">' + "<br>".join(_e(e) for e in data["errors"]) + "</div>")
    parts.append('</div></div>')
    return f"<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>{_e(m['repo'])} board</title><style>{CSS}</style>" + "".join(parts)

def _atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".board.")
    with os.fdopen(fd, "w", encoding="utf-8") as fh: fh.write(text)
    os.replace(tmp, path)

def build(repo_root, out_dir=None, projects_dir=None, now=None, run=subprocess.run, since_minutes=5):
    repo_root = Path(repo_root).resolve(); now = now or dt.datetime.now(dt.timezone.utc)
    projects_dir = Path(projects_dir) if projects_dir else Path(os.path.expanduser("~/.claude/projects"))
    out = Path(out_dir) if out_dir else repo_root / ".claude/board"; errors = []
    def safe(name, fn, default):
        try: return fn()
        except Exception as e:  # noqa: BLE001
            errors.append(f"{name}: {e}"); return default
    r = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo_root, run); branch = r.stdout.strip() if r.returncode == 0 else "?"
    r = _run(["git", "rev-parse", "--short", "HEAD"], repo_root, run); head = r.stdout.strip() if r.returncode == 0 else "?"
    sessions = safe("sessions", lambda: collect_sessions(repo_root, projects_dir, now, since_minutes), [])
    beads = safe("beads", lambda: collect_beads(repo_root, run=run), {"in_flight": [], "epics": [], "counts": {}, "recent_closed": [], "error": None})
    if beads.get("error"): errors.append("beads: " + beads["error"])
    prs = safe("prs", lambda: collect_prs(repo_root, run=run), [])
    waiting = safe("waiting", lambda: collect_waiting(repo_root, sessions, beads, prs), [])
    now_block = safe("now", lambda: collect_now(sessions, beads), {"text": "", "session": None, "epic": None})
    data = {"meta": {"repo": repo_root.name, "branch": branch, "head": head, "built_at": now.strftime("%Y-%m-%d %H:%M %Z")},
            "waiting": waiting, "now": now_block, "beads": beads, "sessions": sessions, "prs": prs, "errors": errors}
    _atomic_write(out / "index.html", render(data, now)); _atomic_write(out / "board.json", json.dumps(data, indent=2, default=str))
    return data
