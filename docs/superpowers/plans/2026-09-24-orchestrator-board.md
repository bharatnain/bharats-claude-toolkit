# Orchestrator Board Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A generated HTML board showing what is waiting on the user, what is happening now, in-flight beads work, sessions and subagents with model/tokens, the PR merge lane, and the backlog — refreshed by a hook, opened in the browser pane or published as an Artifact.

**Architecture:** `scripts/board.py` collects six sources through independent, fail-soft collectors and renders one self-contained HTML page plus `board.json`. `hooks/board_refresh.py` (Stop/SubagentStop) rebuilds it only when the repo has opted in. `skills/board/SKILL.md` is the manual path (`open`, `serve`, `publish`).

**Tech Stack:** Python 3.10+ stdlib (json, subprocess, pathlib, html, http.server, datetime); `gh` and `bd` CLIs when present; pytest for tests.

**Spec:** `docs/superpowers/specs/2026-09-24-orchestrator-board-design.md`

## Global Constraints

- Stdlib only; read-only against beads, git, GitHub; writes only `.claude/board/index.html` and `.claude/board/board.json`.
- Every collector is wrapped: a failure renders an "unavailable: <reason>" panel; `build` never raises.
- Transcripts are read from the tail (last 512 KB); the build must finish in under 2 s for 30 sessions.
- Secret redaction uses `hooks/secret_scan.py` `PATTERNS`; matched spans render as `[redacted]`.
- Hook is solo-safe: exits 0 unless `.claude/board/` exists or `CLAUDE_BOARD=on`; never prints to stdout; 15 s timeout; fail open.
- Skill frontmatter: `name: board`, `disable-model-invocation: true`, `argument-hint: "[open|serve|publish]"`.

## File Structure

- `scripts/board.py` — collectors (`collect_sessions`, `collect_beads`, `collect_prs`, `collect_waiting`, `collect_now`), `render(data) -> str`, `build(repo, out) -> dict`, CLI (`build|open|serve`).
- `scripts/test_board.py` — fixtures for gh JSON, bd JSON, two transcripts, waiting.md; render smoke; failure-mode test.
- `hooks/board_refresh.py` — opt-in refresh on Stop/SubagentStop; `hooks/hooks.json` gains two entries.
- `skills/board/SKILL.md` — manual path.
- `skills/team-orchestration/SKILL.md` — one line in the progress contract (waiting.md).

---

### Task 1: Session and subagent collector

**Files:**
- Create: `scripts/board.py`
- Test: `scripts/test_board.py`

**Interfaces:**
- Produces: `collect_sessions(repo_root: Path, projects_dir: Path, now: datetime, since_minutes=5) -> list[dict]`, each `{"id", "title", "model", "branch", "last_at" (iso), "running": bool, "tokens": int, "last_text": str, "waiting_question": str|None, "subagents": [{"id","name","model","tool_uses","running","last_at"}]}`.
- Produces: `project_dirs_for(repo_root, projects_dir) -> list[Path]` — the `~/.claude/projects/<encoded>` dirs whose name starts with the repo's encoded path (covers worktrees). Encoding: absolute path with `/` replaced by `-`.

- [ ] **Step 1: Write the failing tests**

```python
# scripts/test_board.py
import json, sys, datetime as dt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import board

NOW = dt.datetime(2026, 9, 24, 12, 0, tzinfo=dt.timezone.utc)

def _line(**kw):
    return json.dumps(kw) + "\n"

def make_projects(tmp_path, repo_root):
    proj = tmp_path / "projects" / str(repo_root).replace("/", "-")
    proj.mkdir(parents=True)
    s1 = proj / "sess-1.jsonl"
    s1.write_text(
        _line(type="custom-title", customTitle="Feature A", sessionId="sess-1")
        + _line(type="assistant", timestamp="2026-09-24T11:58:00Z", sessionId="sess-1", gitBranch="claude/a",
                message={"model": "claude-opus-5-5", "usage": {"input_tokens": 1000, "output_tokens": 200},
                         "content": [{"type": "text", "text": "Merging now, sk-ant-abcdefghijklmnopqrstuvwxyz1234 is fine"}]})
    )
    sub = proj / "sess-1" / "subagents"; sub.mkdir(parents=True)
    (sub / "agent-abc.jsonl").write_text(
        _line(type="attachment", agentId="abc", timestamp="2026-09-24T11:59:00Z", attachment={"type": "model", "identity": {"modelId": "claude-opus-5-5[1m]"}})
        + _line(type="assistant", agentId="abc", timestamp="2026-09-24T11:59:30Z", message={"content": [{"type": "tool_use", "name": "Bash", "input": {}}]})
    )
    (sub / "agent-abc.meta.json").write_text(json.dumps({"description": "Review diff"}))
    s2 = proj / "sess-2.jsonl"
    s2.write_text(
        _line(type="assistant", timestamp="2026-09-24T09:00:00Z", sessionId="sess-2",
              message={"model": "claude-sonnet-5", "content": [{"type": "tool_use", "name": "AskUserQuestion", "input": {"questions": [{"question": "Ship it?"}]}}]})
    )
    return tmp_path / "projects"

def test_collect_sessions(tmp_path):
    repo = tmp_path / "repo"; repo.mkdir()
    sessions = board.collect_sessions(repo, make_projects(tmp_path, repo), NOW)
    s1 = next(s for s in sessions if s["id"] == "sess-1")
    assert s1["title"] == "Feature A" and s1["model"] == "claude-opus-5-5" and s1["running"] is True
    assert s1["tokens"] == 1200 and "[redacted]" in s1["last_text"] and "sk-ant" not in s1["last_text"]
    assert s1["subagents"][0]["name"] == "Review diff" and s1["subagents"][0]["tool_uses"] == 1
    s2 = next(s for s in sessions if s["id"] == "sess-2")
    assert s2["running"] is False and s2["waiting_question"] == "Ship it?"
```

- [ ] **Step 2: Run → FAIL** (`ModuleNotFoundError: board`)

Run: `uv run --quiet --python 3.12 --with pytest pytest -q scripts/test_board.py`

- [ ] **Step 3: Implement**

```python
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
    try: return dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
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
                             "waiting_question": question if not running else question, "subagents": _subagents(proj / sid, now, since_minutes)})
    sessions.sort(key=lambda s: s["last_at"] or "", reverse=True)
    return sessions
```

- [ ] **Step 4: Run → 1 passed**
- [ ] **Step 5: Commit** — `git add scripts/board.py scripts/test_board.py && git commit -m "feat(board): session + subagent collector with redaction"`

---

### Task 2: Beads, PR, waiting and now collectors

**Files:**
- Modify: `scripts/board.py`
- Test: `scripts/test_board.py`

**Interfaces:**
- Produces: `collect_beads(repo_root, run=subprocess.run) -> {"in_flight": [...], "epics": [...], "counts": {status: n}, "recent_closed": [...]}`; `collect_prs(repo_root, run) -> [{"number","title","head","draft","checks": "passed"|"failed"|"pending"|"none","updated","url"}]`; `collect_waiting(repo_root, sessions, beads, prs) -> [{"source","text","at"}]`; `collect_now(sessions, beads) -> {"text","session","epic"}`. All accept a `run` callable so tests inject outputs.

- [ ] **Step 1: Write the failing tests**

```python
BD_JSON = json.dumps([
  {"id": "x-1", "title": "Epic A", "issue_type": "epic", "status": "in_progress", "owner": "", "parent": None, "priority": 2, "updated_at": "2026-09-24T11:00:00Z", "dependencies": []},
  {"id": "x-2", "title": "Build parser", "issue_type": "task", "status": "in_progress", "owner": "worker-1", "parent": "x-1", "priority": 2, "updated_at": "2026-09-24T11:30:00Z", "dependencies": [], "labels": ["model:opus", "tries:2"]},
  {"id": "x-3", "title": "Need decision", "issue_type": "task", "status": "open", "owner": "", "parent": "x-1", "priority": 1, "updated_at": "2026-09-24T10:00:00Z", "dependencies": [], "labels": ["needs-input"]},
])
GH_JSON = json.dumps([
  {"number": 9, "title": "Add parser", "headRefName": "claude/parser", "isDraft": False, "updatedAt": "2026-09-24T11:40:00Z", "url": "https://x/9",
   "statusCheckRollup": [{"conclusion": "SUCCESS"}, {"conclusion": "FAILURE"}]},
  {"number": 8, "title": "Docs", "headRefName": "claude/docs", "isDraft": True, "updatedAt": "2026-09-23T11:40:00Z", "url": "https://x/8", "statusCheckRollup": []},
])

class FakeRun:
    def __init__(self, outputs): self.outputs = outputs
    def __call__(self, args, **kw):
        key = args[0]; out = self.outputs.get(key, "")
        class R: pass
        r = R(); r.returncode = 0 if out else 1; r.stdout = out; r.stderr = ""; return r

def test_collect_beads_and_prs(tmp_path):
    run = FakeRun({"bd": BD_JSON, "gh": GH_JSON})
    b = board.collect_beads(tmp_path, run=run)
    assert [i["id"] for i in b["in_flight"]] == ["x-2", "x-3"] and b["in_flight"][0]["model"] == "opus" and b["in_flight"][0]["tries"] == "2"
    assert b["counts"]["in_progress"] == 2
    prs = board.collect_prs(tmp_path, run=run)
    assert prs[0]["checks"] == "failed" and prs[1]["checks"] == "none" and prs[1]["draft"] is True

def test_collect_waiting_and_now(tmp_path):
    repo = tmp_path / "repo"; (repo / ".claude/board").mkdir(parents=True)
    (repo / ".claude/board/waiting.md").write_text("- 2026-09-24 · Approve topic name · reply 'ok'\n")
    run = FakeRun({"bd": BD_JSON, "gh": GH_JSON})
    sessions = board.collect_sessions(repo, make_projects(tmp_path, repo), NOW)
    beads = board.collect_beads(repo, run=run); prs = board.collect_prs(repo, run=run)
    w = board.collect_waiting(repo, sessions, beads, prs)
    srcs = [x["source"] for x in w]
    assert srcs.count("waiting.md") == 1 and "beads" in srcs and "pr" in srcs and "session" in srcs
    now = board.collect_now(sessions, beads)
    assert now["epic"] == "Epic A" and "Merging now" in now["text"]

def test_collectors_fail_soft(tmp_path):
    run = FakeRun({})
    assert board.collect_beads(tmp_path, run=run)["error"].startswith("bd")
    assert board.collect_prs(tmp_path, run=run) == [] or isinstance(board.collect_prs(tmp_path, run=run), list)
```

- [ ] **Step 2: Run → FAIL** (`AttributeError: collect_beads`)

- [ ] **Step 3: Implement**

```python
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
```

- [ ] **Step 4: Run → 4 passed**
- [ ] **Step 5: Commit** — `git commit -am "feat(board): beads, PR, waiting and now collectors"`

---

### Task 3: Renderer and build

**Files:**
- Modify: `scripts/board.py`
- Test: `scripts/test_board.py`

**Interfaces:**
- Produces: `render(data: dict) -> str` (self-contained HTML), `build(repo_root, out_dir=None, projects_dir=None, now=None, run=subprocess.run) -> dict` writing `index.html` and `board.json` atomically under `<repo>/.claude/board/` (or `out_dir`); `data` keys: `meta` (repo, branch, head, built_at), `waiting`, `now`, `beads`, `sessions`, `prs`, `errors` (list of "section: reason").

- [ ] **Step 1: Write the failing tests**

```python
def test_build_writes_files_and_never_raises(tmp_path):
    repo = tmp_path / "repo"; repo.mkdir()
    import subprocess as sp; sp.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    data = board.build(repo, projects_dir=make_projects(tmp_path, repo), now=NOW, run=FakeRun({}))
    html_text = (repo / ".claude/board/index.html").read_text()
    assert "Waiting on you" in html_text and "Merge lane" in html_text and "unavailable" in html_text
    assert "sk-ant" not in html_text and "[redacted]" in html_text
    assert json.loads((repo / ".claude/board/board.json").read_text())["meta"]["repo"] == "repo"
    assert data["errors"] and any(e.startswith("beads") for e in data["errors"])

def test_render_escapes_html():
    data = {"meta": {"repo": "r", "branch": "b", "head": "h", "built_at": "t"}, "waiting": [{"source": "waiting.md", "text": "<script>alert(1)</script>", "at": None}],
            "now": {"text": "", "session": None, "epic": None}, "beads": {"in_flight": [], "epics": [], "counts": {}, "recent_closed": []}, "sessions": [], "prs": [], "errors": []}
    out = board.render(data)
    assert "<script>alert(1)</script>" not in out and "&lt;script&gt;" in out
```

- [ ] **Step 2: Run → FAIL** (`AttributeError: build`)

- [ ] **Step 3: Implement**

```python
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
    parts.append(f'<h1>{_e(m["repo"])} · orchestrator board</h1><div class="meta">{_e(m["branch"])} {_e(m["head"])} · built {_e(m["built_at"])}</div>')
    w = data["waiting"]
    parts.append('<h2>Waiting on you</h2><div class="card wait">' + ("<ol>" + "".join(f"<li>{_e(x['text'])} <span class='meta'>({_e(x['source'])}, {_rel(x['at'], now)})</span></li>" for x in w) + "</ol>" if w else "Nothing.") + "</div>")
    n = data["now"]
    parts.append('<h2>Now</h2><div class="card">' + (f"<div>{_e(n['text'])}</div><div class='meta'>{_e(n['session'] or '')}{' · epic: ' + _e(n['epic']) if n['epic'] else ''}</div>" if n["text"] or n["epic"] else "No recent activity.") + "</div>")
    parts.append('<div class="grid"><div>')
    b = data["beads"]
    if b.get("error"): parts.append(f'<h2>In flight</h2><div class="card unavail">unavailable: {_e(b["error"])}</div>')
    else:
        rows = "".join(f"<tr><td>{_e(i['id'])}</td><td>{_e(i['title'])}</td><td>{_badge(i['status'], 'acc' if i['status']=='in_progress' else '')}</td><td>{_e(i['owner'])}</td><td>{_e(i['model'] or '')}</td><td>{_e(i['tries'] or '')}</td><td class='meta'>{_rel(i['updated'], now)}</td></tr>" for i in b["in_flight"])
        parts.append(f'<h2>In flight · {len(b["in_flight"])}</h2><div class="card"><table><tr><th>id</th><th>task</th><th>state</th><th>owner</th><th>model</th><th>tries</th><th></th></tr>{rows or "<tr><td colspan=7>Nothing in flight.</td></tr>"}</table></div>')
    srows = []
    for s in data["sessions"]:
        srows.append(f"<tr><td>{_badge('running' if s['running'] else 'idle', 'ok' if s['running'] else '')}</td><td>{_e(s['title'])}</td><td>{_e(s['model'] or '')}</td><td>{_e(s['branch'] or '')}</td><td>{s['tokens']:,}</td><td class='meta'>{_rel(s['last_at'], now)}</td></tr>")
        for a in s["subagents"]:
            srows.append(f"<tr><td></td><td>↳ {_e(a['name'])}</td><td>{_e(a['model'] or '')}</td><td>{_badge('running' if a['running'] else 'done', 'ok' if a['running'] else '')}</td><td>{a['tool_uses']} tools</td><td class='meta'>{_rel(a['last_at'], now)}</td></tr>")
    parts.append(f'<h2>Sessions and agents · {len(data["sessions"])}</h2><div class="card"><table><tr><th></th><th>session / agent</th><th>model</th><th>branch</th><th>tokens</th><th></th></tr>{"".join(srows) or "<tr><td colspan=6>No sessions found.</td></tr>"}</table></div>')
    parts.append('</div><div>')
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
    beads = safe("beads", lambda: collect_beads(repo_root, run=run), {"in_flight": [], "epics": [], "counts": {}, "recent_closed": [], "error": "collector failed"})
    if beads.get("error"): errors.append("beads: " + beads["error"])
    prs = safe("prs", lambda: collect_prs(repo_root, run=run), [])
    waiting = safe("waiting", lambda: collect_waiting(repo_root, sessions, beads, prs), [])
    now_block = safe("now", lambda: collect_now(sessions, beads), {"text": "", "session": None, "epic": None})
    data = {"meta": {"repo": repo_root.name, "branch": branch, "head": head, "built_at": now.strftime("%Y-%m-%d %H:%M %Z")},
            "waiting": waiting, "now": now_block, "beads": beads, "sessions": sessions, "prs": prs, "errors": errors}
    _atomic_write(out / "index.html", render(data, now)); _atomic_write(out / "board.json", json.dumps(data, indent=2, default=str))
    return data
```

- [ ] **Step 4: Run → 6 passed**
- [ ] **Step 5: Commit** — `git commit -am "feat(board): renderer + build"`

---

### Task 4: CLI (`build|open|serve`)

**Files:**
- Modify: `scripts/board.py`
- Test: `scripts/test_board.py`

- [ ] **Step 1: Write the failing test**

```python
def test_cli_build(tmp_path):
    import subprocess as sp
    repo = tmp_path / "repo"; repo.mkdir(); sp.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    r = sp.run([sys.executable, str(Path(board.__file__)), "build", "--repo", str(repo), "--projects-dir", str(tmp_path / "none"), "--quiet"], capture_output=True, text=True)
    assert r.returncode == 0 and (repo / ".claude/board/index.html").exists()
```

- [ ] **Step 2: Run → FAIL** (`returncode 2`, no CLI)

- [ ] **Step 3: Implement**

```python
def main(argv):
    ap = argparse.ArgumentParser(description="Orchestrator board (read-only; writes .claude/board/)")
    ap.add_argument("cmd", choices=["build", "open", "serve"]); ap.add_argument("--repo", default=".")
    ap.add_argument("--projects-dir", default=None); ap.add_argument("--out", default=None); ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--since-minutes", type=int, default=5); ap.add_argument("--no-gh", action="store_true"); ap.add_argument("--port", type=int, default=4817)
    a = ap.parse_args(argv)
    run = subprocess.run
    if a.no_gh:
        def run(args, **kw):  # noqa: E306
            if args and args[0] == "gh":
                class R: pass
                r = R(); r.returncode = 1; r.stdout = ""; r.stderr = "disabled"; return r
            return subprocess.run(args, **kw)
    data = build(a.repo, a.out, a.projects_dir, run=run, since_minutes=a.since_minutes)
    out = Path(a.out) if a.out else Path(a.repo).resolve() / ".claude/board"
    if not a.quiet:
        print(f"board: {out / 'index.html'} · waiting {len(data['waiting'])} · in flight {len(data['beads'].get('in_flight', []))} · sessions {len(data['sessions'])} · PRs {len(data['prs'])}")
        for e in data["errors"]: print(f"  unavailable: {e}")
    if a.cmd == "open":
        url = (out / "index.html").as_uri(); print(url); webbrowser.open(url)
    if a.cmd == "serve":
        import functools, http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(out))
        print(f"http://127.0.0.1:{a.port}/index.html")
        http.server.ThreadingHTTPServer(("127.0.0.1", a.port), handler).serve_forever()
    return 0

if __name__ == "__main__":
    try: sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt: sys.exit(0)
    except Exception as e:  # noqa: BLE001
        print(f"internal error: {e}", file=sys.stderr); sys.exit(2)
```

- [ ] **Step 4: Run → 7 passed**
- [ ] **Step 5: Commit** — `git commit -am "feat(board): CLI build/open/serve"`

---

### Task 5: Refresh hook

**Files:**
- Create: `hooks/board_refresh.py`
- Modify: `hooks/hooks.json` (add to `Stop` and `SubagentStop` lists), `docs/hooks-security.md` (one paragraph)
- Test: `scripts/test_board.py`

- [ ] **Step 1: Write the failing test**

```python
def test_hook_noop_without_optin(tmp_path):
    import subprocess as sp
    repo = tmp_path / "repo"; repo.mkdir(); sp.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    hook = Path(board.__file__).parent.parent / "hooks" / "board_refresh.py"
    env = dict(os.environ, CLAUDE_BOARD="", HOME=str(tmp_path))
    r = sp.run([sys.executable, str(hook)], input='{"hook_event_name":"Stop","cwd":"%s"}' % repo, capture_output=True, text=True, cwd=repo, env=env)
    assert r.returncode == 0 and r.stdout == "" and not (repo / ".claude/board/index.html").exists()
    (repo / ".claude/board").mkdir(parents=True)
    r = sp.run([sys.executable, str(hook)], input='{"hook_event_name":"Stop","cwd":"%s"}' % repo, capture_output=True, text=True, cwd=repo, env=env)
    assert r.returncode == 0 and r.stdout == "" and (repo / ".claude/board/index.html").exists()
```

(add `import os` at the top of the test file)

- [ ] **Step 2: Run → FAIL** (hook file missing)

- [ ] **Step 3: Implement**

```python
#!/usr/bin/env python3
"""Stop/SubagentStop hook: rebuild .claude/board/ when the repo opted in. Solo-safe, fail-open, silent.

Opt-in: the repo has a .claude/board/ directory (created by /board) or CLAUDE_BOARD=on.
Never prints to stdout (no context cost); errors go to stderr; always exits 0."""
import json, os, subprocess, sys
from pathlib import Path
MAX_STDIN = 10 * 1024 * 1024
HERE = Path(__file__).resolve().parent

def main():
    if os.environ.get("CLAUDE_TOOLKIT_HOOKS", "").strip().lower() in ("0", "false", "no", "off"): return 0
    raw = "" if sys.stdin.isatty() else sys.stdin.read(MAX_STDIN)
    try: payload = json.loads(raw) if raw.strip() else {}
    except Exception: payload = {}  # noqa: BLE001
    repo = Path(payload.get("cwd") or os.getcwd())
    if not (repo / ".claude/board").is_dir() and os.environ.get("CLAUDE_BOARD", "").lower() != "on": return 0
    try:
        subprocess.run([sys.executable, str(HERE.parent / "scripts" / "board.py"), "build", "--repo", str(repo), "--quiet"],
                       capture_output=True, text=True, timeout=15, env=dict(os.environ, CLAUDE_TOOLKIT_HOOKS="off"))
    except Exception as e:  # noqa: BLE001
        print(f"board_refresh: {e}", file=sys.stderr)
    return 0

if __name__ == "__main__":
    try: sys.exit(main())
    except Exception: sys.exit(0)  # noqa: BLE001
```

hooks.json: append to the `Stop` array and the `SubagentStop` array an entry `{"hooks": [{"type": "command", "command": "python3", "args": ["${CLAUDE_PLUGIN_ROOT}/hooks/board_refresh.py"], "timeout": 20}]}` (same one-line `args` style as the existing entries). docs/hooks-security.md: add under §2 "`board_refresh.py` (Stop/SubagentStop) is opt-in per repo (`.claude/board/` present or `CLAUDE_BOARD=on`), read-only against beads/git/gh, writes only `.claude/board/`, silent, fail-open."

- [ ] **Step 4: Run → 8 passed; `python3 scripts/validate_assets.py` 0 errors; `python3 -c "import json;json.load(open('hooks/hooks.json'))"`**
- [ ] **Step 5: Commit** — `git add hooks scripts docs && git commit -m "feat(board): opt-in Stop/SubagentStop refresh hook"`

---

### Task 6: `/board` skill, orchestration tie-in, docs

**Files:**
- Create: `skills/board/SKILL.md`
- Modify: `skills/team-orchestration/SKILL.md` (progress contract: one bullet), `.gitignore` (`.claude/board/`), `README.md` (short section), `CHANGELOG.md` (`[Unreleased]`), `SKILLS.md` (regenerated)

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: board
description: Build and open the orchestrator board — what is waiting on you, what is happening now, in-flight beads work, sessions and subagents with model and tokens, the PR merge lane, and the backlog — generated from local data, refreshed by a hook after every turn.
disable-model-invocation: true
argument-hint: "[open|serve|publish]"
---

# /board

Engine: `scripts/board.py` (stdlib, read-only; writes only `.claude/board/`).

- First run in a repo: `mkdir -p .claude/board` and add `.claude/board/` to `.gitignore` — this opts the repo into the Stop/SubagentStop refresh hook.
- `/board` or `/board open`: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/board.py open --repo .` then open the printed `file://` URL in the browser pane (`preview_start` with that URL).
- `/board serve`: run `... serve --repo . --port 4817` in the background and open `http://127.0.0.1:4817/index.html`.
- `/board publish`: `... build --repo .` then publish `.claude/board/index.html` with the Artifact tool (private) and return the link.
- Report the one-line summary the script prints (waiting / in flight / sessions / PRs) and any `unavailable:` lines as-is.

Waiting-on-you items come from `.claude/board/waiting.md` (one `- ` line each), beads issues labelled `needs-input`, failed PR checks, and sessions ending on an unanswered question.
```

- [ ] **Step 2: team-orchestration progress contract** — add: "- When a task needs the user, append `- <date> · <what> · <how to answer>` to `.claude/board/waiting.md` (if the repo has a board) and remove the line once answered."

- [ ] **Step 3: Validate + catalog** — `python3 scripts/validate_skills.py --strict-yaml && python3 scripts/validate_skills.py --catalog && python3 scripts/validate_skills.py --check-catalog`; `python3 scripts/validate_assets.py`.

- [ ] **Step 4: Smoke** — in this repo: `mkdir -p .claude/board && python3 scripts/board.py open --repo .`; open the URL in the browser pane and confirm the six sections render with this session listed. Remove `.claude/board/` afterwards if you don't want the hook active here.

- [ ] **Step 5: Docs** — README section "Orchestrator board" (what it shows, `/board`, opt-in hook, publish for phone); CHANGELOG `[Unreleased]`: "Added: orchestrator board (`scripts/board.py`, `/board`, opt-in refresh hook)."

- [ ] **Step 6: Commit** — `git add -A && git commit -m "feat: /board skill, refresh hook wiring, docs"`

---

## Self-review

Spec coverage: sources (T1–T2), render/build/redaction/fail-soft (T3), CLI open/serve (T4), hook opt-in/silent/fail-open (T5), skill + waiting.md tie-in + Artifact publish + docs (T6). Runtime budget is enforced by tail reads (T1) — measure once during the smoke with `time`. Names consistent: `collect_sessions/collect_beads/collect_prs/collect_waiting/collect_now`, `render`, `build`, `_run`, `redact`. No placeholders.
