"""Tests for the model / autoCompactWindow / env merge in scripts/bootstrap.sh.

Runs the real script against a throwaway settings file. CLAUDE_SETTINGS points at
tmp_path, the CLAUDE.md install and the bd install are switched off, and HOME is
redirected, so nothing touches the real ~/.claude and nothing hits the network.
"""

import json
import os
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "bootstrap.sh"
TEMPLATE = json.loads((REPO / "settings.json").read_text(encoding="utf-8"))


def run_bootstrap(tmp_path, dest=None):
    target = tmp_path / "claude" / "settings.json"
    if dest is not None:
        target.parent.mkdir(parents=True)
        target.write_text(json.dumps(dest), encoding="utf-8")
    env = dict(
        os.environ,
        HOME=str(tmp_path / "home"),
        CLAUDE_SETTINGS=str(target),
        CLAUDE_DEFAULT_CLAUDE_MD="off",
        CLAUDE_BEADS="off",
    )
    proc = subprocess.run(
        ["bash", str(SCRIPT)], env=env, capture_output=True, text=True, check=True
    )
    return json.loads(target.read_text(encoding="utf-8")), proc


def test_template_declares_defaults():
    assert TEMPLATE["model"] == "opus"
    assert TEMPLATE["autoCompactWindow"] == "300k"
    assert TEMPLATE["env"]["CLAUDE_CODE_SUBAGENT_MODEL"] == "sonnet"
    assert TEMPLATE["enabledPlugins"]["codex@openai-codex"] is True


def test_absent_keys_are_added(tmp_path):
    merged, proc = run_bootstrap(tmp_path)
    assert merged["model"] == "opus"
    assert merged["autoCompactWindow"] == "300k"
    assert merged["env"] == {"CLAUDE_CODE_SUBAGENT_MODEL": "sonnet"}
    assert merged["enabledPlugins"]["codex@openai-codex"] is True
    assert "bootstrap: keeping" not in proc.stderr
    assert "model opus, window 300k" in proc.stdout


def test_existing_different_model_and_window_kept_with_notice(tmp_path):
    merged, proc = run_bootstrap(
        tmp_path, {"model": "claude-opus-5", "autoCompactWindow": "500k"}
    )
    assert merged["model"] == "claude-opus-5"
    assert merged["autoCompactWindow"] == "500k"
    assert "bootstrap: keeping model=claude-opus-5 (toolkit default: opus" in proc.stderr
    assert "bootstrap: keeping autoCompactWindow=500k (toolkit default: 300k" in proc.stderr
    assert "model claude-opus-5, window 500k" in proc.stdout


def test_env_is_add_only(tmp_path):
    dest = {"env": {"CLAUDE_CODE_SUBAGENT_MODEL": "haiku", "OTHER": "x"}}
    merged, proc = run_bootstrap(tmp_path, dest)
    assert merged["env"] == {"CLAUDE_CODE_SUBAGENT_MODEL": "haiku", "OTHER": "x"}
    assert "keeping env.CLAUDE_CODE_SUBAGENT_MODEL=haiku" in proc.stderr
    assert "OTHER" not in proc.stderr

    merged, _ = run_bootstrap(tmp_path / "b", {"env": {"OTHER": "x"}})
    assert merged["env"] == {"OTHER": "x", "CLAUDE_CODE_SUBAGENT_MODEL": "sonnet"}


def test_pct_override_notice_and_kept(tmp_path):
    merged, proc = run_bootstrap(
        tmp_path, {"env": {"CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "60"}}
    )
    assert merged["env"]["CLAUDE_AUTOCOMPACT_PCT_OVERRIDE"] == "60"
    assert "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=60" in proc.stderr
    assert "180K" in proc.stderr
    assert "remove it unless intended" in proc.stderr


def test_no_pct_notice_without_override(tmp_path):
    _, proc = run_bootstrap(tmp_path)
    assert "PCT_OVERRIDE" not in proc.stderr



def test_rerun_on_merged_output_is_silent(tmp_path):
    merged, _ = run_bootstrap(tmp_path / "first")
    _, proc = run_bootstrap(tmp_path / "second", merged)
    assert "bootstrap: keeping" not in proc.stderr
