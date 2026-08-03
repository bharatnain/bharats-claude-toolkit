#!/usr/bin/env bash
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
# Build-daemon transport for the Step 4 survey build (prompts/05-survey-build.md).
#
# The contract: the daemon that owns the build is the ONLY process that runs
# the compiler. Fixers consume the numbered output files
# (migration/build-output-r<N>.txt) and never run the build themselves — with
# the migration's deny rules active they can't, and this script is what makes that
# workable past a couple of rounds. Run 3's receipt: the human served as
# build daemon by hand — fine for 2 rounds, not for 50 (RUN-NOTES).
#
# Watches the source tree by content hash (.git, target, node_modules, dist,
# build, migration excluded), reruns the build command whenever the tree
# changes — immediately on the first loop — and tees each round's combined
# stdout+stderr to migration/build-output-r<N>.txt, N auto-incrementing from
# whatever is already on disk. The filesystem is the state, same as the
# queue runner. One summary line per round: round number, exit code, output
# file.
#
# Requires bash + POSIX coreutils (find, shasum or sha256sum). Run from the
# repo root the survey build grades.
#
# Usage:
#   ./build_daemon.sh --cmd "cargo check --all-targets" [--interval 30] [--once]
#       --cmd       the build command (required)
#       --interval  seconds between tree checks (default 30)
#       --once      run a single round and exit (for testing)
#
# Test: from a temp dir, `bash <kit>/scripts/build_daemon.sh --cmd "echo hello" --once`
# (kit-rooted path — the script runs against the cwd, not its own location)
# must produce migration/build-output-r1.txt containing "hello".

set -u

CMD=""
INTERVAL=30
ONCE=0

USAGE='(use --cmd "..." [--interval N] [--once])'

while [ $# -gt 0 ]; do
  case "$1" in
    --cmd|--interval)
      if [ $# -lt 2 ]; then
        echo "missing value for $1 $USAGE" >&2
        exit 1
      fi
      case "$1" in
        --cmd)      CMD="$2" ;;
        --interval) INTERVAL="$2" ;;
      esac
      shift 2 ;;
    --once)     ONCE=1; shift ;;
    *) echo "unknown argument: $1 $USAGE" >&2; exit 1 ;;
  esac
done

if [ -z "$CMD" ]; then
  echo "missing --cmd (the build command the daemon owns)" >&2
  exit 1
fi

case "$INTERVAL" in
  '' | *[!0-9]*) echo "--interval must be a positive integer, got: '$INTERVAL'" >&2; exit 1 ;;
esac
if [ "$INTERVAL" -lt 1 ]; then
  echo "--interval must be a positive integer, got: '$INTERVAL'" >&2
  exit 1
fi

if command -v shasum >/dev/null 2>&1; then
  HASHER="shasum -a 256"
else
  HASHER="sha256sum"
fi

tree_hash() {
  # Content hash of the source tree: hash every file, sort, hash the list.
  # Exclusions mirror what the survey build doesn't grade — migration/ is
  # excluded so the daemon's own output files never retrigger a round.
  find . \
    \( -name .git -o -name target -o -name node_modules -o -name dist \
       -o -name build -o -name migration \) -prune \
    -o -type f -print 2>/dev/null \
    | sort \
    | while IFS= read -r f; do $HASHER "$f"; done \
    | $HASHER \
    | awk '{print $1}'
}

next_round() {
  # Auto-increment from what's on disk — never from memory.
  local max=0 n f
  for f in migration/build-output-r*.txt; do
    [ -e "$f" ] || continue
    n="${f##*build-output-r}"
    n="${n%.txt}"
    case "$n" in '' | *[!0-9]*) continue ;; esac
    [ "$n" -gt "$max" ] && max="$n"
  done
  echo $((max + 1))
}

run_round() {
  local round out rc
  round="$(next_round)"
  out="migration/build-output-r${round}.txt"
  mkdir -p migration
  sh -c "$CMD" 2>&1 | tee "$out"
  rc="${PIPESTATUS[0]}"
  echo "round ${round}: exit ${rc} -> ${out}"
}

LAST_HASH=""
while :; do
  HASH="$(tree_hash)"
  if [ "$HASH" != "$LAST_HASH" ]; then
    LAST_HASH="$HASH"
    run_round
  fi
  [ "$ONCE" -eq 1 ] && exit 0
  sleep "$INTERVAL"
done
