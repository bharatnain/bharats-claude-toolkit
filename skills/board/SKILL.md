---
name: board
description: Build and open the orchestrator board — what is waiting on you, what is happening now, in-flight beads work, sessions and subagents with model and tokens, the PR merge lane, and the backlog — generated from local data, refreshed by a hook after every turn.
disable-model-invocation: true
argument-hint: "[open|serve|publish]"
---

# /board

Engine: `scripts/board.py` (stdlib, read-only; writes only `.claude/board/`).

- First run in a repo: `mkdir -p .claude/board` and add `.claude/board/` to `.gitignore` — this opts the repo into the Stop/SubagentStop refresh hook.
- `/board` or `/board open`: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/board.py open --repo .` then open the printed `file://` URL in the browser pane (`preview_start` with that URL).
- `/board serve`: run `... serve --repo . --port 4817` in the background and open `http://127.0.0.1:4817/index.html`.
- `/board publish`: `... build --repo .` then publish `.claude/board/index.html` with the Artifact tool (private) and return the link.
- Report the one-line summary the script prints (waiting / in flight / sessions / PRs) and any `unavailable:` lines as-is.

Waiting-on-you items come from `.claude/board/waiting.md` (one `- ` line each), beads issues labelled `needs-input`, failed PR checks, and sessions ending on an unanswered question.
