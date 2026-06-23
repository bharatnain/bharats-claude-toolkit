---
description: Spin up a maturity-matched multi-agent team to deliver a goal end-to-end, with quality gates enforced automatically
---

Run `/team <goal>` to orchestrate a multi-agent build for **<goal>**.

This command is intentionally **thin**: it does not contain the orchestration logic.
The brain lives in the **`team-orchestration`** skill — defer to it for the full loop.

## The `/team <goal>` flow

1. Invoke the **`team-orchestration`** skill.
2. Hand it the goal (everything after `/team`).
3. The skill detects the team-profile maturity, picks the roster, activates the
   session sentinel/gates, decomposes the goal into acceptance-criteria-bearing tasks,
   spawns the teammates, and tears the session down at the end.

If no goal is given, ask the user what they want the team to build, then proceed.

> Solo-safe: until `/team` activates a session, the gate hooks are pure no-ops —
> installing this changes nothing for solo work.
