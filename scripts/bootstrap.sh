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

# Result preserves dest's existing key order first, then any new keys.
merged = dict(dest)

# extraKnownMarketplaces: dict update. Start from dest's map, apply source
# entries key-by-key (source wins on collision); dest-only keys preserved.
src_mkt = src.get("extraKnownMarketplaces", {})
if src_mkt:
    dest_mkt = dict(merged.get("extraKnownMarketplaces", {}))
    dest_mkt.update(src_mkt)
    merged["extraKnownMarketplaces"] = dest_mkt

# enabledPlugins: order-preserving union. Dest order kept first, then any
# source entries not already present, appended in source order. No dupes.
src_plugins = src.get("enabledPlugins", [])
if src_plugins:
    dest_plugins = list(merged.get("enabledPlugins", []))
    seen = set(dest_plugins)
    for p in src_plugins:
        if p not in seen:
            dest_plugins.append(p)
            seen.add(p)
    merged["enabledPlugins"] = dest_plugins

# permissions.allow: order-preserving union nested under the permissions
# object. Dest's existing allow rules are kept first, then any source rules
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

# Source's $comment documents the template, not the user's config: never
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
