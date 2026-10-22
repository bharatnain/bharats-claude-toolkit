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


def run_bootstrap(tmp_path, dest=None, known=None):
    target = tmp_path / "claude" / "settings.json"
    if dest is not None:
        target.parent.mkdir(parents=True)
        target.write_text(json.dumps(dest), encoding="utf-8")
    if known is not None:
        known_file = tmp_path / "home" / ".claude" / "plugins" / "known_marketplaces.json"
        known_file.parent.mkdir(parents=True)
        known_file.write_text(json.dumps(known), encoding="utf-8")
    env = dict(
        {k: v for k, v in os.environ.items() if k != "CLAUDE_CONFIG_DIR"},
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
    assert TEMPLATE["autoCompactWindow"] == 300000
    assert TEMPLATE["env"]["CLAUDE_CODE_SUBAGENT_MODEL"] == "sonnet"
    assert TEMPLATE["enabledPlugins"]["codex@openai-codex"] is True


def test_absent_keys_are_added(tmp_path):
    merged, proc = run_bootstrap(tmp_path)
    assert merged["model"] == "opus"
    assert merged["autoCompactWindow"] == 300000
    assert merged["env"] == {"CLAUDE_CODE_SUBAGENT_MODEL": "sonnet", "SECURITY_REVIEW_MODEL": "claude-sonnet-5-5"}
    assert merged["enabledPlugins"]["codex@openai-codex"] is True
    assert "bootstrap: keeping" not in proc.stderr
    assert "model opus, window 300000" in proc.stdout


def test_existing_different_model_and_window_kept_with_notice(tmp_path):
    merged, proc = run_bootstrap(
        tmp_path, {"model": "claude-opus-5", "autoCompactWindow": 500000}
    )
    assert merged["model"] == "claude-opus-5"
    assert merged["autoCompactWindow"] == 500000
    assert "bootstrap: keeping model=claude-opus-5 (toolkit default: opus" in proc.stderr
    assert "bootstrap: keeping autoCompactWindow=500000 (toolkit default: 300000" in proc.stderr
    assert "model claude-opus-5, window 500000" in proc.stdout


def test_env_is_add_only(tmp_path):
    dest = {"env": {"CLAUDE_CODE_SUBAGENT_MODEL": "haiku", "OTHER": "x"}}
    merged, proc = run_bootstrap(tmp_path, dest)
    assert merged["env"] == {"CLAUDE_CODE_SUBAGENT_MODEL": "haiku", "OTHER": "x", "SECURITY_REVIEW_MODEL": "claude-sonnet-5-5"}
    assert "keeping env.CLAUDE_CODE_SUBAGENT_MODEL (differs" in proc.stderr and "haiku" not in proc.stderr
    assert "OTHER" not in proc.stderr

    merged, _ = run_bootstrap(tmp_path / "b", {"env": {"OTHER": "x"}})
    assert merged["env"] == {"OTHER": "x", "CLAUDE_CODE_SUBAGENT_MODEL": "sonnet", "SECURITY_REVIEW_MODEL": "claude-sonnet-5-5"}


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


def test_invalid_string_window_is_replaced(tmp_path):
    merged, proc = run_bootstrap(tmp_path, {"autoCompactWindow": "300k"})
    assert merged["autoCompactWindow"] == 300000


INLINE = {k: v for k, v in TEMPLATE["extraKnownMarketplaces"].items() if v["source"]["source"] == "settings"}


def test_template_pins_live_on_inline_plugin_entries():
    assert INLINE and "bharats-claude-toolkit-dev" not in INLINE
    for name, entry in INLINE.items():
        assert entry["source"]["name"] == name
        for plugin in entry["source"]["plugins"]:
            assert len(plugin["source"]["sha"]) == 40, (name, plugin["name"])
    for name, entry in TEMPLATE["extraKnownMarketplaces"].items():
        assert "sha" not in entry["source"], name  # not a marketplace-source field; Claude Code drops it


def test_inline_marketplaces_are_overwritten_whole(tmp_path):
    stale = {"source": {"source": "github", "repo": "trailofbits/skills", "ref": "main"}}
    tampered = json.loads(json.dumps(INLINE["ecc"]))
    tampered["source"]["plugins"][0]["source"]["sha"] = "0" * 40
    merged, proc = run_bootstrap(
        tmp_path, {"extraKnownMarketplaces": {"trailofbits": stale, "ecc": tampered}}
    )
    for name, entry in INLINE.items():
        assert merged["extraKnownMarketplaces"][name] == entry
    assert "pinned inline marketplaces written:" in proc.stderr
    assert "trailofbits (updated)" in proc.stderr and "ecc (updated)" in proc.stderr
    assert "openai-codex (new)" in proc.stderr


def test_other_marketplace_entries_stay_add_only(tmp_path):
    custom = {"source": {"source": "github", "repo": "bharatnain/bharats-claude-toolkit", "ref": "my-branch"}}
    mine = {"source": {"source": "github", "repo": "me/mine"}}
    merged, _ = run_bootstrap(
        tmp_path,
        {"extraKnownMarketplaces": {"bharats-claude-toolkit-dev": custom, "mine": mine}},
    )
    assert merged["extraKnownMarketplaces"]["bharats-claude-toolkit-dev"] == custom
    assert merged["extraKnownMarketplaces"]["mine"] == mine


def test_retired_unpinned_marketplace_keys_are_removed(tmp_path):
    legacy = {"source": {"source": "github", "repo": "zilliztech/memsearch", "ref": "main", "sha": "a" * 40}}
    merged, proc = run_bootstrap(tmp_path, {"extraKnownMarketplaces": {"memsearch": legacy}})
    assert "memsearch" not in merged["extraKnownMarketplaces"]
    assert "memsearch-plugins" in merged["extraKnownMarketplaces"]
    assert "removed retired marketplace key memsearch" in proc.stderr


def test_rerun_reports_nothing_about_pins(tmp_path):
    merged, _ = run_bootstrap(tmp_path / "first")
    _, proc = run_bootstrap(tmp_path / "second", merged)
    assert "pinned inline marketplaces" not in proc.stderr
    assert "already registered" not in proc.stderr


def test_stale_registration_prints_migration_without_running_it(tmp_path):
    known = {
        "openai-codex": {"source": {"source": "github", "repo": "openai/codex-plugin-cc", "ref": "main"}},
        "ecc": {"source": INLINE["ecc"]["source"]},
        "pm-skills": {"source": {"source": "settings", "name": "pm-skills", "plugins": []}},
        "bharats-claude-toolkit-dev": {"source": {"source": "github", "repo": "bharatnain/bharats-claude-toolkit"}},
    }
    _, proc = run_bootstrap(tmp_path, known=known)
    assert "already registered from another source" in proc.stderr
    assert "claude plugin marketplace remove openai-codex" in proc.stderr
    assert "openai-codex (registered from: github)" in proc.stderr
    assert "claude plugin marketplace remove pm-skills" in proc.stderr  # settings entry with older pins
    assert "claude plugin marketplace remove ecc" not in proc.stderr  # already registered from the same pins
    assert "remove bharats-claude-toolkit-dev" not in proc.stderr  # not an inline entry
    assert "bash scripts/bootstrap.sh" in proc.stderr and "restart Claude Code" in proc.stderr
    known_file = tmp_path / "home" / ".claude" / "plugins" / "known_marketplaces.json"
    assert json.loads(known_file.read_text(encoding="utf-8")) == known  # read-only


def test_no_registration_notice_without_known_file(tmp_path):
    _, proc = run_bootstrap(tmp_path)
    assert "already registered" not in proc.stderr
