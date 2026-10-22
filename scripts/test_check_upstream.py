"""Tests for the plugin-pin drift report in scripts/check_upstream.py (no network: resolve_head is stubbed)."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_upstream  # noqa: E402

OLD, NEW = "a" * 40, "b" * 40


def settings_file(tmp_path, marketplaces):
    path = tmp_path / "settings.json"
    path.write_text(json.dumps({"extraKnownMarketplaces": marketplaces}), encoding="utf-8")
    return path


def inline(name, *plugins):
    return {"source": {"source": "settings", "name": name, "plugins": list(plugins)}}


def plugin(name, **src):
    return {"name": name, "source": src}


def test_pins_come_from_inline_plugin_entries(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(check_upstream, "resolve_head", lambda url: calls.append(url) or NEW)
    path = settings_file(tmp_path, {
        "dev": {"source": {"source": "github", "repo": "me/dev", "sha": OLD}},  # not inline: ignored
        "mk": inline(
            "mk",
            plugin("a", source="git-subdir", url="o/r", path="plugins/a", ref="main", sha=OLD),
            plugin("b", source="git-subdir", url="o/r", path="plugins/b", ref="main", sha=OLD),
            plugin("c", source="github", repo="o/c", ref="main", sha=NEW),
            plugin("unpinned", source="github", repo="o/u"),
        ),
    })
    rows = check_upstream.build_marketplace_results(path)
    assert [(r["repo"], r["recorded"], r["status"]) for r in rows] == [
        ("mk: a, b (o/r)", OLD, check_upstream.STATUS_UPDATE_AVAILABLE),
        ("mk: c (o/c)", NEW, check_upstream.STATUS_UP_TO_DATE),
    ]
    assert calls == ["https://github.com/o/r", "https://github.com/o/c"]  # one ls-remote per repo


def test_unreachable_upstream_is_unknown(tmp_path, monkeypatch):
    monkeypatch.setattr(check_upstream, "resolve_head", lambda url: None)
    path = settings_file(tmp_path, {"mk": inline("mk", plugin("a", source="github", repo="o/r", sha=OLD))})
    (row,) = check_upstream.build_marketplace_results(path)
    assert row["status"] == check_upstream.STATUS_UNKNOWN and row["current"] == "unknown"


def test_repo_settings_have_a_pin_row_per_pinned_repo(monkeypatch):
    monkeypatch.setattr(check_upstream, "resolve_head", lambda url: None)
    rows = check_upstream.build_marketplace_results(Path(__file__).resolve().parent.parent / "settings.json")
    assert len(rows) >= 10
    assert all(len(r["recorded"]) == 40 for r in rows)
