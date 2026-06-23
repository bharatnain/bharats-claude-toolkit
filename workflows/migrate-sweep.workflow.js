// workflows/migrate-sweep.workflow.js
//
// TEMPLATE — copy this file and parameterize it for your repo. Run via the
// Workflow tool. See workflows/README.md.
//
// Flow: discover the target sites for a mechanical migration -> pipeline:
// transform each site (in an isolated worktree) then runGate-verify THAT site ->
// aggregate per-site verdicts. The gate runs once per site so a regression is
// attributed to the site that caused it.

import { runGate, loadProfileName } from './lib/runner.js'

export const meta = {
  name: 'migrate-sweep',
  description:
    'Sweep a mechanical migration across the codebase: discover every target site, then for each site transform it in an isolated worktree and verify it with runGate, aggregating per-site pass/fail verdicts. The gate runs per site so regressions are attributed to the site that introduced them.',
  phases: [
    { title: 'Discover', detail: 'enumerate the sites that need the migration' },
    { title: 'Transform+Verify', detail: 'pipeline: transform each site in a worktree, then runGate that site' },
    { title: 'Aggregate', detail: 'roll per-site verdicts into one sweep report' },
  ],
}

// ---- args (defensive: string | object | undefined) -------------------------
// { target: "..." }    free-text description of the migration (e.g. "replace
//                      moment() with dayjs()"). A bare string arg is the target.
// { sites: [...] }     optional explicit list of sites (files/dirs/symbols);
//                      bypasses discovery.
// { profile: "..." }   optional profile NAME or path for the per-site gate.
// { checks: [...] }    optional gate check subset.
// { maxSites: 25 }     optional cap on sites swept this run.
let A = args
if (typeof A === 'string') { A = A.trim() ? { target: A } : {} }
if (!A || typeof A !== 'object') A = {}

const TARGET = (typeof A.target === 'string' && A.target.trim()) ? A.target.trim() : '(no migration described — set args.target)'
const EXPLICIT_SITES = (Array.isArray(A.sites) && A.sites.length) ? A.sites : null
const PROFILE = (typeof A.profile === 'string' && A.profile.trim()) ? A.profile.trim() : loadProfileName()
const CHECKS = Array.isArray(A.checks) && A.checks.length ? A.checks : null
const MAX_SITES = Number.isInteger(A.maxSites) && A.maxSites > 0 ? A.maxSites : 25

log(`migrate-sweep: target=${JSON.stringify(TARGET)} profile=${PROFILE} explicitSites=${EXPLICIT_SITES ? EXPLICIT_SITES.length : 'no'} maxSites=${MAX_SITES}`)

const DISCOVER_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['sites'],
  properties: {
    sites: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['site', 'why'],
        properties: {
          site: { type: 'string', description: 'file path / directory / symbol that needs the migration' },
          why: { type: 'string', description: 'the concrete construct at this site that matches the migration' },
        },
      },
    },
  },
}

const TRANSFORM_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['summary', 'changedFiles'],
  properties: {
    summary: { type: 'string' },
    changedFiles: { type: 'array', items: { type: 'string' } },
  },
}

// ---- Phase 1: discover ------------------------------------------------------
phase('Discover')
let sites
if (EXPLICIT_SITES) {
  log(`Explicit site list supplied (${EXPLICIT_SITES.length}) — sweeping exactly these.`)
  sites = EXPLICIT_SITES.map((s) => (typeof s === 'string' ? { site: s, why: '(explicit)' } : s))
} else {
  const disc = await agent(
    `Discover every SITE in this codebase that needs the following mechanical migration. READ-ONLY for now — do NOT transform anything yet, just enumerate. For each site give the path/symbol and quote the construct that matches.

MIGRATION: ${TARGET}`,
    { label: 'discover', phase: 'Discover', schema: DISCOVER_SCHEMA, agentType: 'general-purpose' },
  )
  sites = (disc && disc.sites) || []
}
const swept = sites.slice(0, MAX_SITES)
const deferred = sites.slice(MAX_SITES).map((s) => s.site)
log(`Discover: ${sites.length} site(s); sweeping ${swept.length}${deferred.length ? `, ${deferred.length} deferred past maxSites` : ''}`)

// ---- Phase 2: pipeline transform-in-worktree -> runGate verify PER site -----
phase('Transform+Verify')
const results = await pipeline(
  swept,
  // map: transform one site in isolation
  (s) => agent(
    `Apply this migration to EXACTLY ONE site, in an isolated worktree, as a surgical change. Do not touch other sites; do not refactor adjacent code. Report a one-line summary and the files you changed.

MIGRATION: ${TARGET}
SITE: ${s.site}
WHY THIS SITE: ${s.why}`,
    { label: `transform:${shortName(s.site)}`, phase: 'Transform+Verify', schema: TRANSFORM_SCHEMA, agentType: 'general-purpose' },
  ),
  // reduce: verify THAT site with the gate
  (transform, s) => {
    const gate = runGate({ profile: PROFILE, checks: CHECKS })
    log(`Verify ${shortName(s.site)}: verdict=${gate.verdict} ok=${gate.ok} blocking_failures=${gate.blocking_failures.length}`)
    return {
      site: s.site,
      why: s.why,
      transform,
      gate: { ok: gate.ok, verdict: gate.verdict, blocking_failures: gate.blocking_failures },
    }
  },
)

// ---- Phase 3: aggregate -----------------------------------------------------
phase('Aggregate')
const rows = results.filter(Boolean)
const passed = rows.filter((r) => r.gate.ok && r.gate.blocking_failures.length === 0)
const failed = rows.filter((r) => !(r.gate.ok && r.gate.blocking_failures.length === 0))
log(`Sweep complete: ${passed.length}/${rows.length} site(s) green, ${failed.length} with blocking failures${deferred.length ? `, ${deferred.length} deferred` : ''}`)

return {
  target: TARGET,
  profile: PROFILE,
  swept: rows.length,
  deferred,
  passed: passed.map((r) => r.site),
  failed: failed.map((r) => ({ site: r.site, verdict: r.gate.verdict, blocking_failures: r.gate.blocking_failures })),
  perSite: rows,
  verdict: failed.length ? 'fail' : 'pass',
}

function shortName(s) {
  return String(s || '').split('/').pop() || String(s || '')
}
