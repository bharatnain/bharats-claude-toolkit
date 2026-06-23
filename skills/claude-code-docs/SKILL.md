---
name: claude-code-docs
description: Fetch the current official Claude Code docs before building or explaining any Claude Code internals. Use when building, updating, or debugging Claude Code features in this toolkit — hooks, skills, plugins, plugin marketplaces, settings, subagents, slash commands, statusline, output-styles, memory — OR when the user asks what Claude Code can do, how a feature works, or how to configure it. Trigger this BEFORE answering from built-in knowledge, which may be stale relative to the latest release.
---

# Claude Code Docs

## Discipline: fetch first, then act

Claude Code ships fast and its features (hooks, plugins, settings keys, slash-command and subagent formats) change between releases. Your training has a cutoff, so built-in knowledge of these internals is likely stale.

**Rule: WebFetch the relevant official doc page below BEFORE implementing, configuring, or explaining any Claude Code feature.** Confirm field names, file paths, schema, and behavior against the live page — do not answer from memory.

## Canonical doc index

Base: https://code.claude.com/docs/en/

- Overview: https://code.claude.com/docs/en/overview
- Settings: https://code.claude.com/docs/en/settings
- Skills: https://code.claude.com/docs/en/skills
- Plugins: https://code.claude.com/docs/en/plugins
- Plugins reference: https://code.claude.com/docs/en/plugins-reference
- Plugin marketplaces: https://code.claude.com/docs/en/plugin-marketplaces
- Slash commands: https://code.claude.com/docs/en/slash-commands
- Subagents: https://code.claude.com/docs/en/sub-agents
- Hooks: https://code.claude.com/docs/en/hooks
- Output styles: https://code.claude.com/docs/en/output-styles
- Statusline: https://code.claude.com/docs/en/statusline
- Memory: https://code.claude.com/docs/en/memory

## Delegation

- Deep, interactive Q&A about Claude Code usage — hand off to the claude-code-guide agent.
- Claude API or Anthropic SDK specifics (model ids, params, streaming, tool use) — use the claude-api skill, not these docs.
