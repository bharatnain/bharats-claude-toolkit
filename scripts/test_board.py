import json, os, sys, datetime as dt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import board

NOW = dt.datetime(2026, 9, 24, 12, 0, tzinfo=dt.timezone.utc)

def _line(**kw):
    return json.dumps(kw) + "\n"

def make_projects(tmp_path, repo_root):
    proj = tmp_path / "projects" / board._encode_project(repo_root)
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

def test_collect_sessions_edge_cases(tmp_path):
    repo = tmp_path / "repo"; repo.mkdir()
    proj = tmp_path / "projects" / board._encode_project(repo)
    proj.mkdir(parents=True)
    (proj / "sess-3.jsonl").write_text(
        "{not json\n"
        + _line(type="assistant", timestamp="2026-09-24T11:58:00", sessionId="sess-3",
                message={"model": "claude-sonnet-5", "content": [{"type": "text", "text": "hi"}]})
    )
    (proj / "empty.jsonl").write_text("")

    sessions = board.collect_sessions(repo, tmp_path / "projects", NOW)

    s3 = next(s for s in sessions if s["id"] == "sess-3")
    assert s3["running"] is True

    empty = next(s for s in sessions if s["id"] == "empty")
    assert empty["last_at"] is None and empty["running"] is False and empty["tokens"] == 0 and empty["title"] == "empty"

def test_project_dirs_encode_dots(tmp_path):
    import re
    repo = tmp_path / "bharat.nain" / "my_repo"
    repo.mkdir(parents=True)
    encoded = re.sub(r"[^A-Za-z0-9]", "-", str(repo.resolve()))
    projects = tmp_path / "projects"
    projects.mkdir()
    expected = projects / encoded
    expected.mkdir()
    (projects / "-other").mkdir()

    def fake_run(*a, **kw):
        class R: pass
        r = R(); r.returncode = 1; r.stdout = ""; r.stderr = ""; return r

    assert board.project_dirs_for(repo, projects, run=fake_run) == [expected]

def test_project_dirs_from_worktree(tmp_path):
    import re
    main = tmp_path / "main"
    worktree = main / ".claude" / "worktrees" / "wt"
    worktree.mkdir(parents=True)
    projects = tmp_path / "projects"
    projects.mkdir()
    main_dir = projects / re.sub(r"[^A-Za-z0-9]", "-", str(main.resolve()))
    main_dir.mkdir()
    wt_dir = projects / re.sub(r"[^A-Za-z0-9]", "-", str(worktree.resolve()))
    wt_dir.mkdir()

    def fake_run_ok(args, **kw):
        class R: pass
        r = R(); r.returncode = 0; r.stderr = ""
        r.stdout = f"worktree {main}\nHEAD abc\n\nworktree {worktree}\nHEAD def\n" if "worktree" in args else str(main / ".git") + "\n"
        return r

    assert board.project_dirs_for(worktree, projects, run=fake_run_ok) == sorted([main_dir, wt_dir])

    def fake_run_fail(*a, **kw):
        class R: pass
        r = R(); r.returncode = 1; r.stdout = ""; r.stderr = ""; return r

    assert board.project_dirs_for(worktree, projects, run=fake_run_fail) == [wt_dir]

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
    prs, err = board.collect_prs(tmp_path, run=run)
    assert err is None and prs[0]["checks"] == "failed" and prs[1]["checks"] == "none" and prs[1]["draft"] is True

def test_collect_waiting_and_now(tmp_path):
    repo = tmp_path / "repo"; (repo / ".claude/board").mkdir(parents=True)
    (repo / ".claude/board/waiting.md").write_text("- 2026-09-24 · Approve topic name · reply 'ok'\n")
    run = FakeRun({"bd": BD_JSON, "gh": GH_JSON})
    sessions = board.collect_sessions(repo, make_projects(tmp_path, repo), NOW)
    beads = board.collect_beads(repo, run=run); prs, _ = board.collect_prs(repo, run=run)
    w = board.collect_waiting(repo, sessions, beads, prs)
    srcs = [x["source"] for x in w]
    assert srcs.count("waiting.md") == 1 and "beads" in srcs and "pr" in srcs and "session" in srcs
    now = board.collect_now(sessions, beads)
    assert now["epic"] == "Epic A" and "Merging now" in now["text"]

def test_collectors_fail_soft(tmp_path):
    run = FakeRun({})
    assert board.collect_beads(tmp_path, run=run)["error"].startswith("bd")
    assert board.collect_prs(tmp_path, run=run)[0] == []

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

def test_build_marks_failed_sources_inline(tmp_path, monkeypatch):
    repo = tmp_path / "repo"; repo.mkdir()
    import subprocess as sp; sp.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    monkeypatch.setattr(board, "collect_sessions", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    monkeypatch.setattr(board, "collect_beads", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    data = board.build(repo, projects_dir=tmp_path / "none", now=NOW, run=FakeRun({}))
    html_text = (repo / ".claude/board/index.html").read_text()
    assert "unavailable: boom" in html_text
    assert sum(1 for e in data["errors"] if e.startswith("beads:")) == 1
    in_flight_segment = html_text.split("<h2>In flight", 1)[1].split("<h2", 1)[0]
    assert "unavailable: boom" in in_flight_segment

def test_cli_build(tmp_path):
    import subprocess as sp
    repo = tmp_path / "repo"; repo.mkdir(); sp.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    r = sp.run([sys.executable, str(Path(board.__file__)), "build", "--repo", str(repo), "--projects-dir", str(tmp_path / "none"), "--quiet"], capture_output=True, text=True)
    assert r.returncode == 0 and (repo / ".claude/board/index.html").exists()

def test_cli_open_relative_out(tmp_path, monkeypatch):
    import subprocess as sp
    repo = tmp_path / "repo"; repo.mkdir(); sp.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    monkeypatch.chdir(repo)
    monkeypatch.setattr(board.webbrowser, "open", lambda url: True)
    rc = board.main(["open", "--repo", ".", "--projects-dir", str(tmp_path / "none"), "--out", "relout", "--quiet"])
    assert rc == 0 and (repo / "relout" / "index.html").exists()

def test_cli_build_no_gh(tmp_path):
    import subprocess as sp
    repo = tmp_path / "repo"; repo.mkdir(); sp.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    rc = board.main(["build", "--repo", str(repo), "--projects-dir", str(tmp_path / "none"), "--no-gh", "--quiet"])
    assert rc == 0
    assert json.loads((repo / ".claude/board/board.json").read_text())["prs"] == []

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

GHP = "gh" + "p_" + "A1b2C3d4" * 5
SKA = "sk-" + "ant-" + "Zy9Xw8Vu7Ts6Rq5Po4Nm3"

def test_redacts_every_field(tmp_path):
    import subprocess as sp
    repo = tmp_path / "repo"; repo.mkdir(); sp.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    (repo / ".claude/board").mkdir(parents=True)
    (repo / ".claude/board/waiting.md").write_text(f"- rotate {GHP} please\n")
    proj = tmp_path / "projects" / board._encode_project(repo); proj.mkdir(parents=True)
    (proj / "s.jsonl").write_text(
        _line(type="custom-title", customTitle=f"title {SKA}")
        + _line(type="assistant", timestamp="2026-09-24T11:58:00Z", message={"content": [
            {"type": "text", "text": "hello"},
            {"type": "tool_use", "name": "AskUserQuestion", "input": {"questions": [{"question": f"use {GHP}?"}]}}]}))
    sub = proj / "s" / "subagents"; sub.mkdir(parents=True)
    (sub / "agent-z.jsonl").write_text(_line(type="assistant", timestamp="2026-09-24T11:59:00Z", message={"content": []}))
    (sub / "agent-z.meta.json").write_text(json.dumps({"description": f"agent {SKA}"}))
    bd = json.dumps([
        {"id": "e-1", "title": f"epic {GHP}", "issue_type": "epic", "status": "in_progress"},
        {"id": "t-1", "title": f"task {SKA}", "issue_type": "task", "status": "in_progress", "owner": f"o {GHP}", "labels": ["needs-input"], "closed_at": "x"}])
    gh = json.dumps([{"number": 1, "title": f"pr {SKA}", "headRefName": f"b-{GHP}", "isDraft": False, "updatedAt": "2026-09-24T11:00:00Z", "url": "u",
                      "statusCheckRollup": [{"conclusion": "FAILURE"}]}])
    out = tmp_path / "out"
    data = board.build(repo, out_dir=out, projects_dir=tmp_path / "projects", now=NOW, run=FakeRun({"bd": bd, "gh": gh}))
    assert data["sessions"] and data["prs"] and data["waiting"]
    for text in ((out / "index.html").read_text(), (out / "board.json").read_text()):
        assert GHP not in text and SKA not in text and "[redacted]" in text

def test_prs_unavailable_panel(tmp_path):
    prs, err = board.collect_prs(tmp_path, run=FakeRun({}))
    assert prs == [] and err.startswith("gh unavailable")
    import subprocess as sp
    repo = tmp_path / "repo"; repo.mkdir(); sp.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    data = board.build(repo, out_dir=tmp_path / "out", projects_dir=tmp_path / "none", now=NOW, run=FakeRun({"bd": BD_JSON}))
    assert any(e.startswith("prs: gh unavailable") for e in data["errors"]) and data["prs"] == []
    merge = (tmp_path / "out/index.html").read_text().split("<h2>Merge lane", 1)[1].split("<h2", 1)[0]
    assert "unavailable: gh unavailable" in merge

def test_session_ai_title(tmp_path):
    repo = tmp_path / "repo"; repo.mkdir()
    proj = tmp_path / "projects" / board._encode_project(repo); proj.mkdir(parents=True)
    (proj / "a.jsonl").write_text(_line(type="ai-title", aiTitle="AI named"))
    (proj / "b.jsonl").write_text(_line(type="custom-title", customTitle="Mine") + _line(type="ai-title", aiTitle="AI named"))
    titles = {s["id"]: s["title"] for s in board.collect_sessions(repo, tmp_path / "projects", NOW)}
    assert titles == {"a": "AI named", "b": "Mine"}

def test_tokens_counted_once_per_message_id(tmp_path):
    repo = tmp_path / "repo"; repo.mkdir()
    proj = tmp_path / "projects" / board._encode_project(repo); proj.mkdir(parents=True)
    msg = lambda block: {"id": "msg_1", "usage": {"input_tokens": 100, "output_tokens": 10}, "content": [block]}
    (proj / "t.jsonl").write_text(
        _line(type="assistant", timestamp="2026-09-24T11:00:00Z", message=msg({"type": "text", "text": "a"}))
        + _line(type="assistant", timestamp="2026-09-24T11:00:01Z", message=msg({"type": "tool_use", "name": "Bash", "input": {}})))
    assert board.collect_sessions(repo, tmp_path / "projects", NOW)[0]["tokens"] == 110

def test_project_dirs_exact_and_worktrees(tmp_path):
    repo = tmp_path / "repo"; repo.mkdir()
    wt = tmp_path / "elsewhere" / "wt"; wt.mkdir(parents=True)
    projects = tmp_path / "projects"; projects.mkdir()
    repo_dir = projects / board._encode_project(repo); repo_dir.mkdir()
    (projects / board._encode_project(tmp_path / "repo-v2")).mkdir()
    wt_dir = projects / board._encode_project(wt); wt_dir.mkdir()
    calls = []
    def fake_run(args, cwd=None, **kw):
        calls.append((args, cwd))
        class R: pass
        r = R(); r.returncode = 0; r.stderr = ""
        r.stdout = f"worktree {repo}\nHEAD abc\n\nworktree {wt}\nHEAD def\n" if "worktree" in args else str(repo / ".git") + "\n"
        return r
    assert board.project_dirs_for(repo, projects, run=fake_run) == sorted([repo_dir, wt_dir])
    assert any("worktree" in a and c == str(repo.resolve()) for a, c in calls)

def test_bd_list_unlimited(tmp_path):
    calls = []
    def run(args, **kw):
        calls.append(args)
        class R: pass
        r = R(); r.returncode = 0; r.stdout = BD_JSON; r.stderr = ""; return r
    board.collect_beads(tmp_path, run=run)
    assert len(calls) == 2 and all(a[a.index("--limit") + 1] == "0" for a in calls if "--limit" in a) and all("--limit" in a for a in calls)
