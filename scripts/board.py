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
