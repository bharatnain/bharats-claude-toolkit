#!/usr/bin/env bash
# Store the ANTHROPIC_API_KEY repo secret that .github/workflows/plugin-eval.yml needs.
# The key is read from $ANTHROPIC_API_KEY if set, otherwise prompted for (no echo).
# It is piped to gh on stdin, so it never appears in argv or shell history.
set -euo pipefail
REPO="${REPO:-bharatnain/bharats-claude-toolkit}"
command -v gh >/dev/null 2>&1 || { echo "gh CLI not found" >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "gh is not authenticated: run 'gh auth login'" >&2; exit 1; }
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  read -r -s -p "Paste the Anthropic API key for ${REPO} (input hidden): " ANTHROPIC_API_KEY; echo
fi
[ -n "$ANTHROPIC_API_KEY" ] || { echo "empty key; nothing set" >&2; exit 1; }
printf '%s' "$ANTHROPIC_API_KEY" | gh secret set ANTHROPIC_API_KEY --repo "$REPO"
echo "Secret ANTHROPIC_API_KEY set on $REPO. Run the eval with: gh workflow run plugin-eval.yml --repo $REPO"
