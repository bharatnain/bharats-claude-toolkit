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

# Back up an existing target before writing. No backup if it didn't pre-exist.
BACKUP=""
if [ -f "$TARGET" ]; then
  BACKUP="$TARGET.bak.$(date +%Y%m%d%H%M%S)"
  cp "$TARGET" "$BACKUP"
  echo "Backup written: $BACKUP"
fi

# Render the merged settings to a temp file in the same directory (for an
# atomic mv) using an inline python3 program. The program prints the summary
# counts ("<marketplaces> <plugins>") to stdout, which we capture.
TMP="$(mktemp "$(dirname "$TARGET")/.settings.XXXXXX")"
# Clean up the temp file on any unexpected exit.
trap 'rm -f "$TMP"' EXIT

if ! COUNTS="$(SOURCE="$SOURCE" TARGET="$TARGET" TMP="$TMP" python3 <<'PY'
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

# extraKnownMarketplaces: dict update. Start from the dest map, apply source
# entries key-by-key (source wins on collision); dest-only keys preserved.
src_mkt = src.get("extraKnownMarketplaces", {})
if src_mkt:
    dest_mkt = dict(merged.get("extraKnownMarketplaces", {}))
    dest_mkt.update(src_mkt)
    merged["extraKnownMarketplaces"] = dest_mkt

# enabledPlugins: object map {plugin: true}. Claude Code reads this as a
# JSON object, NOT an array -- an array silently enables zero plugins. Merge
# the source map into dest key-by-key; dest wins on collision so an explicit
# user enable/disable is never overridden. A legacy array-valued dest (or an
# array-valued source) is normalized to the object form first.
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
    merged["enabledPlugins"] = dest_map

# permissions.allow: order-preserving union nested under the permissions
# object. Existing dest allow rules are kept first, then any source rules
# not already present. Other permissions keys (deny, ask,
# additionalDirectories) and any dest-only fields are preserved untouched.
src_allow = src.get("permissions", {}).get("allow", [])
if src_allow:
    dest_perms = dict(merged.get("permissions", {}))
    dest_allow = list(dest_perms.get("allow", []))
    seen = set(dest_allow)
    for rule in src_allow:
        if rule not in seen:
            dest_allow.append(rule)
            seen.add(rule)
    dest_perms["allow"] = dest_allow
    merged["permissions"] = dest_perms

# The source $comment documents the template, not the user config: never
# propagate it. (Any pre-existing dest $comment is preserved untouched.)

with open(tmp_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)
    f.write("\n")

mkt_count = len(merged.get("extraKnownMarketplaces", {}))
plugin_count = len(merged.get("enabledPlugins", []))
allow_count = len(merged.get("permissions", {}).get("allow", []))
print(f"{mkt_count} {plugin_count} {allow_count}")
PY
)"; then
  echo "Error: merge failed." >&2
  rm -f "$TMP"
  exit 1
fi

read -r MKT_COUNT PLUGIN_COUNT ALLOW_COUNT <<<"$COUNTS"

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

echo "merged: $MKT_COUNT marketplaces, $PLUGIN_COUNT enabled plugins, $ALLOW_COUNT allow rules"
echo
echo "Activation: restart Claude Code OR run /reload-plugins in an open session"
echo "for the always-on tier to take effect. ecc and superpowers remain one"
echo "'/plugin install' away."

# ---------------------------------------------------------------------------
# Install the default global CLAUDE.md (Andrej Karpathy's LLM-coding guidelines,
# shipped as this repo's own CLAUDE.md) to the user-level memory file so the
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
  SRC_CLAUDE_MD="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/CLAUDE.md"
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
    if curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash; then
      echo "beads: bd installed."
    else
      echo "beads: optional bd install did not complete; continuing. Bootstrap is unaffected."
    fi
  fi
fi
