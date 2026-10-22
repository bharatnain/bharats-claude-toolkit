#!/usr/bin/env bash
set -euo pipefail

# Bootstrap: merge this repo's settings.json into the user's Claude Code
# settings (default ~/.claude/settings.json), enabling the always-on tier.
# Activation (registering marketplaces / restarting Claude) is left to the user.

# Source = the repo's settings.json, resolved relative to this script's own
# location so it works regardless of the caller's cwd.
SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/settings.json"

# Destination = env override, else the user-global settings file. This is the
# sole testability hook: tests point CLAUDE_SETTINGS at a temp file.
TARGET="${CLAUDE_SETTINGS:-$HOME/.claude/settings.json}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required but was not found on PATH." >&2
  exit 1
fi

if [ ! -f "$SOURCE" ]; then
  echo "Error: source settings not found at $SOURCE" >&2
  exit 1
fi

# Ensure the target directory exists; a missing target is treated as {}.
mkdir -p "$(dirname "$TARGET")"

# Backup happens AFTER the merge is rendered and only when the write is not a
# no-op (see below) — an idempotent re-run must not churn backups.
BACKUP=""

# Render the merged settings to a temp file in the same directory (for an
# atomic mv) using an inline python3 program. The program prints the summary
# counts ("<marketplaces> <plugins>") to stdout, which we capture.
TMP="$(mktemp "$(dirname "$TARGET")/.settings.XXXXXX")"
# Clean up the temp file on any unexpected exit.
trap 'rm -f "$TMP"' EXIT

# Read-only: where Claude Code records the marketplaces it has registered (used to spot a
# name registered from a different source than the pinned inline entry).
KNOWN_MARKETPLACES="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/known_marketplaces.json"

if ! COUNTS="$(SOURCE="$SOURCE" TARGET="$TARGET" TMP="$TMP" KNOWN_MARKETPLACES="$KNOWN_MARKETPLACES" python3 <<'PY'
import json
import os
import sys

source_path = os.environ["SOURCE"]
target_path = os.environ["TARGET"]
tmp_path = os.environ["TMP"]

with open(source_path, "r", encoding="utf-8") as f:
    src = json.load(f)

if os.path.exists(target_path):
    with open(target_path, "r", encoding="utf-8") as f:
        dest = json.load(f)
else:
    dest = {}

if not isinstance(dest, dict):
    print("Error: destination settings is not a JSON object.", file=sys.stderr)
    sys.exit(1)
if not isinstance(src, dict):
    print("Error: source settings is not a JSON object.", file=sys.stderr)
    sys.exit(1)

# Result preserves the dest key order first, then any new keys.
merged = dict(dest)

# extraKnownMarketplaces: the repo is authoritative for inline `source: "settings"`
# marketplaces (they carry the per-plugin sha pins, so a stale or hand-edited copy
# must not survive): those keys are overwritten whole and any change is reported.
# Every other entry (github/git/...) is add-only: a key already on the machine is
# kept. Dest-only keys are preserved, except retired keys this repo itself once
# wrote as unpinned github entries.
def is_inline(entry):
    return (isinstance(entry, dict) and isinstance(entry.get("source"), dict)
            and entry["source"].get("source") == "settings")

RETIRED_MARKETPLACE_KEYS = ("memsearch", "trailofbits-skills", "trailofbits-skills-curated")

src_mkt = src.get("extraKnownMarketplaces", {})
if src_mkt:
    dest_mkt = dict(merged.get("extraKnownMarketplaces", {}))
    for key in RETIRED_MARKETPLACE_KEYS:
        old = dest_mkt.get(key)
        if key not in src_mkt and old is not None and not is_inline(old):
            del dest_mkt[key]
            print(f"bootstrap: removed retired marketplace key {key} (superseded by a pinned inline entry)",
                  file=sys.stderr)
    changed = []
    for name, entry in src_mkt.items():
        if is_inline(entry):
            if dest_mkt.get(name) != entry:
                changed.append(f"{name} ({'updated' if name in dest_mkt else 'new'})")
            dest_mkt[name] = entry
        elif name not in dest_mkt:
            dest_mkt[name] = entry
    if changed:
        print("bootstrap: pinned inline marketplaces written: " + ", ".join(changed), file=sys.stderr)
    merged["extraKnownMarketplaces"] = dest_mkt

    # Claude Code registers a settings-declared marketplace only if it does not
    # already know the name, so a name registered earlier from a GitHub source (or
    # from an older pin set) keeps tracking that source. Detect it read-only from
    # known_marketplaces.json and PRINT the migration; never run it.
    known_path = os.environ.get("KNOWN_MARKETPLACES", "")
    stale = []
    try:
        with open(known_path, "r", encoding="utf-8") as f:
            known = json.load(f)
        for name, entry in src_mkt.items():
            if not is_inline(entry) or not isinstance(known, dict) or name not in known:
                continue
            ksrc = (known[name] or {}).get("source") or {}
            if ksrc.get("source") != "settings":
                stale.append((name, ksrc.get("source") or "unknown"))
            elif "plugins" in ksrc and ksrc["plugins"] != entry["source"].get("plugins"):
                stale.append((name, "settings, older pins"))
    except (OSError, ValueError):
        pass
    if stale:
        print("bootstrap: these marketplaces are already registered from another source, so Claude Code\n"
              "           will not re-register them from the pinned inline entries until you switch them:\n"
              + "\n".join(f"             {n} (registered from: {s})" for n, s in stale)
              + "\n           Run these yourself (bootstrap does not):\n"
              + "\n".join(f"             claude plugin marketplace remove {n}" for n, _ in stale)
              + "\n             bash scripts/bootstrap.sh    # remove also drops the settings entry; this restores it\n"
              "           then restart Claude Code. Removing a marketplace uninstalls its plugins, so reinstall the\n"
              "           ones you use afterwards (e.g. claude plugin install codex@openai-codex).",
              file=sys.stderr)

# enabledPlugins: object map {plugin: true}. Claude Code reads this as a
# JSON object, NOT an array -- an array silently enables zero plugins. Merge
# the source map into dest key-by-key; dest wins on collision so an explicit
# user enable/disable is never overridden -- EXCEPT that a plugin the repo
# template sets to false is forced off, so repo-side disables (a plugin moved
# to another marketplace, or one that calls removed tools) reach machines that
# already had it on. A legacy array-valued dest (or an array-valued source) is
# normalized to the object form first.
src_plugins = src.get("enabledPlugins")
if src_plugins:
    src_map = ({p: True for p in src_plugins}
               if isinstance(src_plugins, list) else dict(src_plugins))
    dest_ep = merged.get("enabledPlugins", {})
    dest_map = ({p: True for p in dest_ep}
                if isinstance(dest_ep, list) else dict(dest_ep))
    for p, is_on in src_map.items():
        if p not in dest_map:
            dest_map[p] = is_on
        elif is_on is False and dest_map[p] is not False:
            dest_map[p] = False  # repo-side disable wins (see settings.json $comment)
    merged["enabledPlugins"] = dest_map

# permissions.allow / permissions.deny: order-preserving unions nested under
# the permissions object. Existing dest rules are kept first, then any source
# rules not already present. permissions.defaultMode is set only when the dest
# has none (a mode the user chose is never overridden). Other permissions keys
# (ask, additionalDirectories) and any dest-only fields are preserved untouched.
src_perms = src.get("permissions", {})
if src_perms:
    dest_perms = dict(merged.get("permissions", {}))
    for key in ("allow", "deny"):
        src_rules = src_perms.get(key, [])
        if not src_rules:
            continue
        dest_rules = list(dest_perms.get(key, []))
        seen = set(dest_rules)
        for rule in src_rules:
            if rule not in seen:
                dest_rules.append(rule)
                seen.add(rule)
        dest_perms[key] = dest_rules
    if src_perms.get("defaultMode") and not dest_perms.get("defaultMode"):
        dest_perms["defaultMode"] = src_perms["defaultMode"]
    merged["permissions"] = dest_perms

# model / autoCompactWindow / env: add-only. A top-level key is set only when
# the dest has no value; a differing dest value is kept and reported on stderr
# (the summary on stdout stays machine-readable). env is merged per key the same
# way. Only the keys the template names are touched. Model/window values are
# echoed; env values never are (only the key name), since env can hold secrets.
for key, hint in (("model", "run /model {v} to switch"),
                  ("autoCompactWindow", "edit autoCompactWindow in settings.json to change it")):
    if key not in src:
        continue
    # A non-integer window is invalid (the key takes a token count) and Claude Code drops it;
    # v0.12.0 shipped the string "300k", so replace any non-integer value.
    if not merged.get(key) or (key == "autoCompactWindow" and not isinstance(merged[key], int)):
        merged[key] = src[key]
    elif merged[key] != src[key]:
        print(f"bootstrap: keeping {key}={merged[key]} (toolkit default: {src[key]}; "
              + hint.format(v=src[key]) + ")", file=sys.stderr)

src_env = src.get("env", {})
if src_env:
    dest_env = dict(merged.get("env", {}))
    for k, v in src_env.items():
        if k not in dest_env:
            dest_env[k] = v
        elif dest_env[k] != v:
            print(f"bootstrap: keeping env.{k} (differs from the toolkit default)",
                  file=sys.stderr)
    merged["env"] = dest_env

pct = merged.get("env", {}).get("CLAUDE_AUTOCOMPACT_PCT_OVERRIDE")
if pct is not None:
    print(f"bootstrap: env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE={pct} compacts at that percentage "
          f"of the window (60 with a 300K window compacts near 180K); remove it unless intended",
          file=sys.stderr)

# The source $comment documents the template, not the user config: never
# propagate it. (Any pre-existing dest $comment is preserved untouched.)

with open(tmp_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)
    f.write("\n")

mkt_count = len(merged.get("extraKnownMarketplaces", {}))
ep = merged.get("enabledPlugins", {})
plugin_count = sum(1 for v in ep.values() if v) if isinstance(ep, dict) else len(ep)
allow_count = len(merged.get("permissions", {}).get("allow", []))
deny_count = len(merged.get("permissions", {}).get("deny", []))
mode = merged.get("permissions", {}).get("defaultMode") or "unset"
model = "".join(str(merged.get("model") or "unset").split())
window = "".join(str(merged.get("autoCompactWindow") or "unset").split())
print(f"{mkt_count} {plugin_count} {allow_count} {deny_count} {mode} {model} {window}")
PY
)"; then
  echo "Error: merge failed." >&2
  rm -f "$TMP"
  exit 1
fi

read -r MKT_COUNT PLUGIN_COUNT ALLOW_COUNT DENY_COUNT DEFAULT_MODE MODEL_VAL WINDOW_VAL <<<"$COUNTS"

# Idempotent no-op: if the merged output is byte-identical to what is already
# on disk, skip the write entirely — no backup churn, no mtime churn.
# (Pattern: graphify install.py `_write_settings_with_backup`.)
if [ -f "$TARGET" ] && cmp -s "$TMP" "$TARGET"; then
  rm -f "$TMP"
  trap - EXIT
  echo "settings: $TARGET already up to date (no changes written)"
else
  # Back up the existing target before overwriting. No backup if absent.
  if [ -f "$TARGET" ]; then
    BACKUP="$TARGET.bak.$(date +%Y%m%d%H%M%S)"
    cp "$TARGET" "$BACKUP"
    echo "Backup written: $BACKUP"
  fi

  # Atomically move the rendered file into place.
  mv "$TMP" "$TARGET"
  trap - EXIT

  # Validate the written file parses as JSON. On failure restore the backup
  # (if any) and exit non-zero.
  if ! python3 -c 'import json,sys; json.load(open(sys.argv[1], encoding="utf-8"))' "$TARGET"; then
    echo "Error: written settings did not parse as JSON." >&2
    if [ -n "$BACKUP" ]; then
      cp "$BACKUP" "$TARGET"
      echo "Restored backup: $BACKUP" >&2
    fi
    exit 1
  fi
fi

echo "merged: $MKT_COUNT marketplaces, $PLUGIN_COUNT enabled plugins, $ALLOW_COUNT allow rules, $DENY_COUNT deny rules, defaultMode $DEFAULT_MODE, model $MODEL_VAL, window $WINDOW_VAL"
echo
echo "Activation: restart Claude Code OR run /reload-plugins in an open session"
echo "for the always-on tier to take effect. ecc remains one"
echo "'/plugin install' away."

# ---------------------------------------------------------------------------
# Install the default global CLAUDE.md (Andrej Karpathy's LLM-coding guidelines,
# shipped as templates/user-CLAUDE.md; the repo's own CLAUDE.md holds repo
# facts only) to the user-level memory file so the
# rules apply in every project by default. NON-BLOCKING and non-destructive:
#   - default on; set CLAUDE_DEFAULT_CLAUDE_MD=off to skip.
#   - writes the file only when absent (or byte-identical -> reported no-op).
#   - never clobbers a DIFFERING existing file unless CLAUDE_FORCE_CLAUDE_MD is
#     set, which backs the existing file up first (mirrors the settings backup).
# CLAUDE_MD overrides the destination (tests point it at a temp file, exactly
# like CLAUDE_SETTINGS above). bash 3.2 safe: plain ifs, cmp for identity, no
# arrays, lives outside the python here-doc.
# ---------------------------------------------------------------------------
if [ "${CLAUDE_DEFAULT_CLAUDE_MD:-on}" != "off" ]; then
  SRC_CLAUDE_MD="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/templates/user-CLAUDE.md"
  DEST_CLAUDE_MD="${CLAUDE_MD:-$HOME/.claude/CLAUDE.md}"
  if [ ! -f "$SRC_CLAUDE_MD" ]; then
    echo "CLAUDE.md: source not found at $SRC_CLAUDE_MD; skipping."
  else
    mkdir -p "$(dirname "$DEST_CLAUDE_MD")"
    if [ ! -f "$DEST_CLAUDE_MD" ]; then
      cp "$SRC_CLAUDE_MD" "$DEST_CLAUDE_MD"
      echo "CLAUDE.md: installed default rules -> $DEST_CLAUDE_MD"
    elif cmp -s "$SRC_CLAUDE_MD" "$DEST_CLAUDE_MD"; then
      echo "CLAUDE.md: $DEST_CLAUDE_MD already up to date"
    elif [ -n "${CLAUDE_FORCE_CLAUDE_MD:-}" ]; then
      CMD_BACKUP="$DEST_CLAUDE_MD.bak.$(date +%Y%m%d%H%M%S)"
      cp "$DEST_CLAUDE_MD" "$CMD_BACKUP"
      cp "$SRC_CLAUDE_MD" "$DEST_CLAUDE_MD"
      echo "CLAUDE.md: backed up existing -> $CMD_BACKUP, then wrote defaults"
    else
      echo "CLAUDE.md: existing $DEST_CLAUDE_MD left untouched (differs from default)."
      echo "           re-run with CLAUDE_FORCE_CLAUDE_MD=1 to overwrite (a backup is made)."
    fi
  fi
fi

# ---------------------------------------------------------------------------
# Optional: make the beads (bd) task tracker present machine-wide. beads is the
# default task manager for the always-on tier. This step is NON-BLOCKING and
# idempotent: it runs only when bd is missing, never fails the bootstrap, and is
# skipped entirely when CLAUDE_BEADS=off. It never runs "bd init" -- per-repo
# init is the SessionStart hook job. bash 3.2 safe: plain if, no arrays, and it
# lives OUTSIDE the python here-doc so no apostrophe can trip the 3.2 lexer.
# ---------------------------------------------------------------------------
if [ "${CLAUDE_BEADS:-on}" != "off" ]; then
  if command -v bd >/dev/null 2>&1; then
    echo "beads: bd already on PATH ($(command -v bd))"
  elif ! command -v curl >/dev/null 2>&1; then
    echo "beads: bd not found and curl unavailable; skipping optional install. See README."
  else
    echo "beads: bd not found; attempting optional install (non-blocking)..."
    if curl -fsSL https://raw.githubusercontent.com/gastownhall/beads/v1.3.0/scripts/install.sh | BEADS_VERSION=1.3.0 bash; then
      echo "beads: bd installed."
    else
      echo "beads: optional bd install did not complete; continuing. Bootstrap is unaffected."
    fi
  fi
fi
