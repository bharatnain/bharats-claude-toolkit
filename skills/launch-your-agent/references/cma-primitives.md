<!-- Copyright 2026 Anthropic PBC -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Claude Managed Agents — Features & Primitives Inventory

> Source: full read of https://platform.claude.com/docs/en/managed-agents/* on 2026-06-14.
> Truth order if anything here drifts: **live public docs win** over this file.
> This is the design substrate for the "launch your agent in ~60 min" skill.

## What CMA is

A **hosted agent harness**. You define an agent (model, prompt, tools); Anthropic runs the agent loop, tool execution, and a **sandboxed Linux container** server-side. The alternative is the Messages API (you build your own loop). CMA is for **long-running, asynchronous, stateful** work.

- **Beta:** every request needs header `anthropic-beta: managed-agents-2026-04-01` (SDK sets it automatically). Enabled by default for all API accounts.
- **API base:** `https://api.anthropic.com/v1` + `-H "anthropic-version: 2023-06-01"`. Many examples also append `?beta=true` on the URL.
- **Two surfaces:** `ant` CLI (`brew install anthropics/tap/ant`, or release binary, or `go install`) and curl/SDK (Python, TS, Java, Go, C#, Ruby, PHP). Plus a **Console** UI (platform.claude.com) for session list + tracing timeline + tool execution view.
- **Not eligible** for Zero Data Retention or HIPAA BAA (stateful by design). You can delete sessions/files anytime.
- **In-Claude-Code helper:** `/claude-api managed-agents-onboard` gives a guided setup.

---

## The 4 core primitives

| Primitive | What it is | ID prefix |
|---|---|---|
| **Agent** | Reusable, **versioned** config: model + system prompt + tools + MCP servers + skills (+ multiagent roster) | `agent_…` |
| **Environment** | Where sessions run: Anthropic cloud sandbox, or self-hosted. **Not versioned.** | (env id) |
| **Session** | One running agent instance in an environment; holds conversation history + sandbox state | `sesn_…` |
| **Events** | Bi-directional messages: you send `user.*`/`system.*`; you receive `agent.*`/`session.*`/`span.*` | (event ids) |

Minimal launch = create agent → create environment → create session → send a user event (or define an outcome). The agent provisions a sandbox, runs the loop, executes tools, streams events, and emits `session.status_idle` when done.

---

## Agent

**Config fields:** `name`* , `model`* , `system`, `tools`, `mcp_servers`, `skills`, `multiagent`, `description`, `metadata`. (*required)

- **model:** any Claude 4.5-family or later. String form `"claude-opus-4-8"`, or object `{"id":"claude-opus-4-8","speed":"fast"}` for fast mode (Opus 4.6/4.7/4.8). Response stores `{id, speed}` (speed defaults `standard`).
- **Versioning:** create once, reference by ID forever. Each config-changing update mints a **new version** (`version` starts at 1, increments). No-op updates return the existing version.
- **Update semantics:** pass current `version` (concurrency guard). Omitted fields preserved. Scalars replaced (`system`/`description` clearable with `null`; `model`/`name` mandatory). **Array fields `tools`/`mcp_servers`/`skills` are FULL replacement** — omit to preserve, `null`/`[]` to clear. `metadata` merges per-key (empty string deletes a key).
- **Lifecycle:** Update (new version) · List versions (full history) · Archive (read-only; existing sessions keep running, new sessions can't reference). 
- **Sessions can pin a version**: pass `agent` as string = latest; as `{"type":"agent","id":…,"version":N}` = pinned.

---

## Environment

Created once, referenced by many sessions; **each session gets its own fresh isolated container** (no shared FS). Not versioned (log your own changes if you mutate them).

- **`config.type`:** `cloud` (Anthropic-managed) or `self_hosted` (your infra, via `ant beta:worker`).
- **`config.packages`:** pre-install + cache across sessions. Managers: `apt`, `cargo`, `gem`, `go`, `npm`, `pip` (run alphabetically). Version pinning supported (`pandas==2.2.0`, `express@4.18.0`, etc.).
- **`config.networking`:**
  - `unrestricted` (default) — full outbound minus a safety blocklist.
  - `limited` — only `allowed_hosts` (bare hostnames / `*.wildcard`, no scheme) + booleans `allow_mcp_servers` (default false) and `allow_package_managers` (default false). Recommended for production (least privilege).
  - Networking does NOT affect the `web_search`/`web_fetch` tools' own domain handling.
- **Pre-installed runtimes** out of the box (langs, DBs, utilities) — see Sandbox reference page.
- **Lifecycle:** list · retrieve · archive (read-only; running sessions continue) · delete (only if no sessions reference it). `name` must be unique per org+workspace.

---

## Session

Two-step: **create** (provisions sandbox, starts `idle`) → **send event** to start work. Acts as a state machine; events drive execution.

- **Create fields:** `agent` (id string or pinned object), `environment_id`, `title`, `vault_ids[]`, `resources[]`.
- **`resources[]`** can attach: **memory_store**, **file**, and **repository** resources. (Memory stores attach only at creation; file/repo resources can change on a running session.)
- **Statuses:** `idle` (waiting for input/tool confirmation; sessions start here) · `running` · `rescheduling` (transient retry) · `terminated` (unrecoverable).
- **Mid-session agent update:** can update a session's `agent.tools` and `agent.mcp_servers` (incl. permission policies) **without a new agent version** — session-local, full-replacement, session must be `idle` (interrupt first if running).
- **Checkpointing & resume:** on idle, sandbox is checkpointed (FS, installed packages, files). Resume by sending a `user.message`. **Checkpoints kept 30 days** after last activity (history kept until deleted); ping with a message to reset the timer if you need sandbox state longer.
- **`usage` field:** cumulative `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`. 5-min cache TTL. Use for cost tracking/budgets.
- **Ops:** retrieve · list (filter `agent_id`) · update · archive (preserves history, blocks new events; can't archive `running`) · delete (removes record+events+sandbox; can't delete `running`). Files/memory/vaults/skills/environments/agents survive session deletion.
- **Deliverables convention:** agent writes outputs to `/mnt/session/outputs/`; fetch via Files API scoped `?scope_id=<session_id>`.

---

## Events

`{domain}.{action}` naming. Every event has `processed_at` (null = queued).

**User events (you send):** `user.message` · `user.interrupt` (stop mid-execution; can pair with a follow-up message) · `user.custom_tool_result` · `user.tool_confirmation` (allow/deny gated tools) · `user.define_outcome` · `user.tool_result` (self-hosted only).

**System event:** `system.message` — update system prompt mid-session. **Opus 4.8 only**; 1–1000 text items; not while `requires_action`.

**Agent events (you receive):** `agent.message` · `agent.thinking` · `agent.tool_use` / `agent.tool_result` · `agent.mcp_tool_use` / `agent.mcp_tool_result` · `agent.custom_tool_use` · `agent.thread_context_compacted` (auto context compaction) · `agent.thread_message_received` / `agent.thread_message_sent` (multiagent).

**Session events:** `session.status_running` · `session.status_idle` (carries `stop_reason`: `end_turn`, `requires_action`, etc.) · `session.status_rescheduled` · `session.status_terminated` · `session.deleted` · `session.updated` · `session.error` (typed `error` + `retry_status`) · plus `session.thread_*` (multiagent).

**Span events (observability):** `span.model_request_start`/`_end` (with `model_usage` token counts) · `span.outcome_evaluation_start`/`_ongoing`/`_end`.

**Streaming:** SSE at `/v1/sessions/:id/events/stream?beta=true`. **Open stream BEFORE sending events** (only post-open events delivered). Reconnect pattern: open stream → list history to seed seen-IDs → tail live, skipping seen. List past events at `/v1/sessions/:id/events` (filter with `types[]=`).

**Steering:** send a `user.message` mid-run (agent may pick it up at next turn boundary). **Interrupt + redirect:** send `user.interrupt` then `user.message`.

---

## Tools

Enable the prebuilt toolset with `{"type":"agent_toolset_20260401"}`. Tools (all on by default): `bash`, `read`, `write`, `edit`, `glob`, `grep`, `web_fetch`, `web_search`. (Tool output >100k tokens auto-spills to a sandbox file with a truncated preview.)

- **Disable specific:** `configs:[{"name":"web_fetch","enabled":false}]`.
- **Allow-list only:** `default_config:{"enabled":false}` + per-tool `configs[].enabled:true`.
- **Custom tools** (`{"type":"custom", name, description, input_schema}`): client-executed. Flow = `agent.custom_tool_use` → session idles `requires_action` → you run it → `user.custom_tool_result` (with `custom_tool_use_id`). Best practices: very detailed descriptions, consolidate related ops under one tool with an `action` param, namespace names, return high-signal output only.
- **MCP toolset:** `{"type":"mcp_toolset","mcp_server_name":"…"}` referencing an entry in the agent's `mcp_servers`.

---

## Outcomes (the "definition of done" loop)

Elevates a session from conversation → graded work. Send `user.define_outcome` after creating the session (no separate user.message needed — agent starts immediately).

- **Fields:** `description` (the task), `rubric` (**required**), `max_iterations` (optional, **default 3, max 20**).
- **Rubric:** markdown with explicit per-criterion checks. Either inline `{"type":"text","content":"…"}` or `{"type":"file","file_id":"…"}` (Files API upload, needs `files-api-2025-04-14` beta header too).
- **Grader:** auto-provisioned, **separate context window** (isolated from the agent's choices); returns pass/fail explanation fed back for the next iteration.
- **Results** (`span.outcome_evaluation_end.result`): `satisfied` (→idle) · `needs_revision` (new cycle) · `max_iterations_reached` (maybe one final revision →idle) · `failed` (rubric fundamentally mismatched →idle) · `interrupted`.
- **Only one outcome at a time**, but chainable (send a new `user.define_outcome` after the prior terminal event). Outcome sessions still accept `user.message` steering. `user.interrupt` marks current eval `interrupted`.
- **Check status:** stream `span.outcome_evaluation_end`, or poll `GET /v1/sessions/:id` → `outcome_evaluations[].result`.

---

## Permission policies (safety rails)

Govern server-executed tools (agent toolset + MCP toolset). NOT custom tools (you gate those yourself).

- **Types:** `always_allow` (auto) · `always_ask` (pause → wait for your `user.tool_confirmation`).
- **Defaults:** agent toolset → `always_allow`; **MCP toolset → `always_ask`** (so new MCP tools can't run unapproved).
- **Set:** `default_config.permission_policy` on the toolset; override per-tool in `configs[].permission_policy` (e.g. allow everything but `always_ask` on `bash`).
- **Confirmation flow:** `agent.tool_use`/`agent.mcp_tool_use` → `session.status_idle` `requires_action` (ids in `stop_reason.event_ids`) → send `user.tool_confirmation` per id with `result:"allow"|"deny"` (+ optional `deny_message`).

---

## Skills

Filesystem-based, on-demand expertise. `skills[]` entries: `type` (`anthropic` | `custom`), `skill_id`, `version` (custom only; pin or `latest`).
- **Prebuilt Anthropic skills:** document tasks — `xlsx`, `docx`, `pptx`, `pdf` (use short name as `skill_id`).
- **Custom skills:** author + upload to workspace (`skill_*` id).
- **Limit: 20 skills per session** (counted across all agents in a multiagent session).

---

## Memory stores (cross-session persistence — the "managed" payoff)

Workspace-scoped collections of text docs that survive across sessions. Without one, every session starts fresh.

- **Create:** `name` + `description` (description shown to agent). ID `memstore_…`. Seed via `memories.create` (`path` + `content`).
- **Attach:** in session `resources[]` as `{type:"memory_store", memory_store_id, access, instructions}`. **Only at session creation.** `access`: `read_write` (default) | `read_only`. `instructions` ≤ 4096 chars.
- **Runtime:** mounted at `/mnt/memory/`; agent reads/writes with normal file tools (agent toolset required); a mount note is auto-added to the system prompt. Writes sync back across sessions sharing the store.
- **Limits:** memory ≤ 100 kB (~25k tokens); **≤ 2,000 memories/store**; **≤ 8 stores/session**. Use many small focused files + multiple scoped stores (per-user, shared read-only reference, etc.).
- **Audit:** every write creates an immutable **memory version** (`memver_…`); list/retrieve/redact; retained 30 days (recent always kept). No restore endpoint — re-write old `content`. Optimistic concurrency via `content_sha256` precondition.
- **Security warning:** `read_write` + untrusted input = prompt-injection can poison memory for future sessions. Use `read_only` for reference material.
- **Manage:** retrieve/update/list/archive (one-way, read-only)/delete.

---

## Vaults & credentials (auth without your own secret store)

Register third-party creds once, reference by `vault_ids` at session creation. Anthropic handles OAuth refresh. **Workspace-scoped** (anyone with a workspace key can reference; revoke by delete/archive).

- **Vault:** `display_name` + optional `metadata`. ID `vlt_…`.
- **Credential categories** (all secret values are **write-only**, never returned):
  - **`mcp_oauth`** — keyed by `mcp_server_url`; `access_token` + `expires_at` + optional `refresh` block (Anthropic auto-refreshes; `token_endpoint_auth.type` ∈ `none`/`client_secret_basic`/`client_secret_post`).
  - **`static_bearer`** — keyed by `mcp_server_url`; fixed `token`.
  - **`environment_variable`** — keyed by `secret_name`; stored as opaque placeholder, **substituted at egress only** (agent never sees value). Has its own `networking.allowed_hosts` (controls which hosts the secret is used for — separate from env-level networking; both must allow the host). Not yet supported on self-hosted. Breaks SigV4/signature-based clients.
- **Runtime:** unmatched MCP cred → unauthenticated connection. First matching vault wins. Constraints: unique key/vault, keys immutable (archive+recreate to change), ≤ 20 creds/vault.
- **Rotation:** update secret value + display_name (structural fields locked). Re-resolved periodically (propagates rotation/archival to running sessions). Diagnose OAuth refresh failures via `…/mcp_oauth_validate` (`valid`/`invalid`/`unknown`). Webhooks: `vault.archived/deleted`, `vault_credential.archived/deleted/refresh_failed`.

---

## Multi-agent sessions

One **coordinator** delegates to a roster of agents, each in its own **session thread** (context-isolated). All threads share the sandbox, filesystem, and vault credentials; tools/MCP/context are NOT shared.

- **Declare:** `multiagent:{type:"coordinator", agents:[…]}` on the coordinator agent. Roster entries: `{type:"agent",id}` (latest at create time), `{type:"agent",id,version}` (pinned), or `{type:"self"}` (spawn copies). Roster snapshotted at coordinator create/update — update the coordinator to pick up newer sub-agent versions.
- **Depth 1 only.** ≤ 20 unique agents in roster; ≤ **25 concurrent threads** (coordinator may call multiple copies of one agent).
- **Threads:** primary thread = session-level stream (condensed view: start/end of subagents + blocking events). Drill into a thread via `/v1/sessions/:id/threads/:tid/stream`. List threads; interrupt a thread (`user.interrupt` + `session_thread_id`); archive an idle thread to free the 25-cap.
- **Patterns:** parallelization, specialization, escalation. MCP servers are agent-scoped; vault creds are session-scoped (apply to all threads — supply a cred for every MCP server used across agents).

---

## MCP connectivity

- **Remote MCP servers** over HTTP (streamable HTTP transport). Declare on agent: `mcp_servers:[{type:"url", name, url}]` + a `mcp_toolset` tool entry referencing `mcp_server_name`.
- **Private servers** via **MCP tunnels** (limited research preview — request access).
- Auth via vaults (match `mcp_server_url` to the agent's `mcp_servers[].url` exactly incl. scheme/trailing slash).

---

## Files API

- Upload (`/v1/files`, needs `files-api-2025-04-14` beta header) — used for rubric files, inputs.
- List session outputs: `/v1/files?scope_id=<session_id>`; download `/v1/files/:id/content`.
- Files are independent resources; deletable anytime; survive session deletion.

---

## Scheduled deployments (native cron — "runs without you")

Launched ~June 2026. A **deployment** kicks off sessions autonomously on a recurring cron schedule — **no external scheduler needed**. ID `depl_…`.

- **Create** `POST /v1/deployments`: `name`, `agent` (id/pinned), `environment_id`, **`initial_events`** (must include a `user.message` that starts the work — can also carry `user.define_outcome`), `schedule:{type:"cron", expression, timezone}`. Optionally attach **files**, **GitHub**, **memory stores**, **vaults** (same session config surface).
- **Schedule:** standard 5-field POSIX cron (`min hour dom month dow`), **minute granularity**; `timezone` = IANA id; **wall-clock DST** (literal local time; nonexistent spring-forward times skipped, fall-back times fire twice — use 1–3 AM-avoidance or UTC if that matters). Up to 10s jitter. Response returns `schedule.upcoming_runs_at` (next fire times) to confirm. Console has a cron builder/validator at `/workspaces/default/deployments`.
- **Each firing → a session.** Tracked as a **deployment run** (`drun_…`) with `trigger_context:{type:"schedule"|"manual", scheduled_at}`. Success → `session_id`; failure → `error.type` (e.g. `environment_archived_error`, `agent_archived_error`, `session_rate_limited_error`). List `GET /v1/deployment_runs?deployment_id=…` (filter `has_error=true`). Rate-limited triggers are recorded (no retry) and retried next occurrence.
- **Lifecycle:** **pause** (suppress future triggers; running sessions continue; manual `run` still allowed; sets `paused_reason`) · **unpause** (resume from next occurrence, no backfill) · **archive** (terminal). **Manual run:** `POST /v1/deployments/:id/run` — fires immediately (test before committing to the schedule).
- **Auto-behavior:** if the agent is archived/deleted the deployment auto-archives; if a subagent is archived the next run fails and the deployment auto-**pauses** so you can fix + resume.
- **Limit: 1,000 deployments/org** (contact support for more).

This is the real path to a "managed agent that works while you sleep" — a single API call, fully hosted.

---

## Dreams (research preview — needs `dreaming-2026-04-21` header + access)

Async job that reads a memory store + 1–100 past session transcripts and produces a **new, reorganized output memory store** (dedup, replace stale, surface insights). Input never modified — review/discard the output. Models: opus-4-8/4-7, sonnet-4-6. Statuses: pending/running/completed/failed/canceled. Billed at standard token rates (`usage` reports totals). Use to keep memory stores under their 2,000 cap.

---

## Rate limits & key limits

- API: create endpoints **300 req/min**; read endpoints **600 req/min** (per org). Plus org spend limits + tier rate limits.
- Outcome `max_iterations`: default 3, max 20. Skills: 20/session. Memory: 100kB/memory, 2000/store, 8 stores/session. Multiagent: 20 roster, 25 threads, depth 1. Vault: 20 creds. Checkpoints: 30 days.

---

## ⚠️ Notable constraints

- **Scheduling IS native** — see Scheduled deployments above (`POST /v1/deployments`, cron + timezone). Doc lives at `/managed-agents/scheduled-deployments` (the `/deployments` path 404s, which is what misled my first pass — corrected).
- **No spend cap inside CMA** — spend limits are set at the **workspace/Console** level, not per-agent.
- Not ZDR / not HIPAA-eligible (stateful by design).
- `system.message` mid-session is Opus-4.8-only.
- Webhooks exist for session + vault lifecycle events (`/managed-agents/webhooks`) — an alternative to polling/streaming for unattended deployments.

---

## Design implications for the 60-minute skill (technical founder)

1. **Happy path is short:** agent → environment → session → `user.define_outcome`. A technical founder can run curl/`ant`/SDK directly — expose it, don't hide it.
2. **The "managed agent" payoff = Outcomes + Memory.** Outcomes give a self-grading stop condition (the safety rail + quality loop). A memory store is what makes run #10 smarter than run #1 — strong candidate for the headline differentiator vs. a chat.
3. **Safety rails are first-class & native:** `always_ask` permission policies, `limited` networking allowlist, `read_only` memory, `max_iterations` bound, workspace spend limit. Use these instead of hand-rolled guardrails.
4. **"Runs without you" is native and one call** — a **scheduled deployment** (cron + timezone + initial events) is the headline "this is a *worker*, not a chat" moment. The 60-min arc can credibly end with the founder's agent live on a recurring schedule. Use a **manual `run`** to test it instantly before trusting the cron.
5. **Iteration is cheap & version-safe:** sharper rubric = edit + re-kickoff (no agent version bump); prompt/tool change = agent update (new version). Sessions resume from checkpoint for 30 days.
