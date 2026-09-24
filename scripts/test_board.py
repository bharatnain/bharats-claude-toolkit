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
