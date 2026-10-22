export const meta = {
  name: 'migrate-sweep',
  description: 'Sweep a mechanical migration across the codebase: discover every target site, then for each site transform it in an isolated worktree and verify it with the quality gate, aggregating per-site pass/fail verdicts. The gate runs per site so regressions are attributed to the site that introduced them.',
  phases: [
    { title: 'Discover', detail: 'enumerate the sites that need the migration' },
    { title: 'Transform+Verify', detail: 'pipeline: transform each site in a worktree, then run the quality gate for that site' },
    { title: 'Aggregate', detail: 'roll per-site verdicts into one sweep report' },
  ],
}

// workflows/migrate-sweep.workflow.js
//
// TEMPLATE — copy this file and parameterize it for your repo. Run via the
// Workflow tool. See workflows/README.md.
//
// Flow: discover the target sites for a mechanical migration -> pipeline:
// transform each site (in an isolated worktree) then gate-verify THAT site ->
// aggregate per-site verdicts. The gate runs once per site so a regression is
// attributed to the site that caused it.
//
// The Workflow runtime has NO module loading and NO Node/filesystem APIs, so the
// quality gate is a cheap agent() stage (model haiku, effort low) with a JSON
// schema. See workflows/README.md.

// ---- args (defensive: string | object | undefined) -------------------------
// { target: "..." }    free-text description of the migration (e.g. "replace
//                      moment() with dayjs()"). A bare string arg is the target.
// { sites: [...] }     optional explicit list of sites (files/dirs/symbols);
//                      bypasses discovery.
// { profile: "..." }   optional profile NAME or path for the per-site gate.
//                      Omitted: the gate resolves its own profile.
// { checks: [...] }    optional gate check subset.
// { maxSites: 25 }     optional cap on sites swept this run.
let A = args
if (typeof A === 'string') { A = A.trim() ? { target: A } : {} }
if (!A || typeof A !== 'object') A = {}

const TARGET = (typeof A.target === 'string' && A.target.trim()) ? A.target.trim() : '(no migration described — set args.target)'
const EXPLICIT_SITES = (Array.isArray(A.sites) && A.sites.length) ? A.sites : null
const PROFILE = (typeof A.profile === 'string' && A.profile.trim()) ? A.profile.trim() : null
const CHECKS = Array.isArray(A.checks) && A.checks.length ? A.checks : null
const MAX_SITES = Number.isInteger(A.maxSites) && A.maxSites > 0 ? A.maxSites : 25

log(`migrate-sweep: target=${JSON.stringify(TARGET)} profile=${PROFILE || '(gate default)'} explicitSites=${EXPLICIT_SITES ? EXPLICIT_SITES.length : 'no'} maxSites=${MAX_SITES}`)

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

// ---- quality gate (inlined: Workflow scripts cannot import) -----------------
// An agent() stage shells scripts/quality_gate.py and returns raw facts (exit code
// + parsed report); the verdict is derived HERE so the semantics stay in code.
// quality_gate.py resolves the profile itself when --profile is omitted
// ($CLAUDE_TEAM_PROFILE, then .claude/team-profile.json, then built-in "active").
// Keep this block identical across the *.workflow.js files that use it.
//
// FAIL-OPEN: a gate-internal error (exit 2, unparsable output, or a failed gate
// agent) yields { ok: true, verdict: 'error' } so a broken gate never wedges the
// flow. Flip FAIL_OPEN_ON_ERROR to false for fail-CLOSED CI. Callers that must not
// act on a broken gate test verdict === 'pass', not ok.
const FAIL_OPEN_ON_ERROR = true
const GATE_CHECKS = ['lint', 'typecheck', 'test', 'build']
const GATE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['exitCode', 'parsed', 'checks'],
  properties: {
    exitCode: { type: ['integer', 'null'], description: 'process exit code of quality_gate.py' },
    parsed: { type: 'boolean', description: 'true iff stdout was a valid JSON report' },
    verdict: { type: ['string', 'null'], description: "the report's verdict field" },
    maturity: { type: ['string', 'null'], description: "maturity of the profile the gate used ('active' for the built-in)" },
    raw: { type: 'string', description: 'first 500 chars of stdout/stderr, only when not parsed' },
    checks: {
      type: 'array',
      items: {
        type: 'object',
        required: ['name', 'status', 'blocking'],
        properties: {
          name: { type: 'string' },
          status: { type: 'string' },
          blocking: { type: 'boolean' },
          detail: { type: 'string' },
        },
      },
    },
  },
}

async function runGate({ profile, checks, scope, label, phase: ph } = {}) {
  const csv = Array.isArray(checks) ? checks.filter((c) => GATE_CHECKS.includes(c)).join(',') : ''
  const cmd = 'python3 scripts/quality_gate.py --format json' + (csv ? ` --checks ${csv}` : '') + (scope === 'all' ? ' --scope all' : '')
  const profileStep = profile
    ? `Profile: "${profile}". If it contains "/" or ends in ".json" treat it as a path (relative to the repo root), otherwise the path is team-profiles/${profile}.json. If that file exists append \`--profile <path>\` to the command; if not, omit --profile.`
    : 'No profile was requested: do NOT pass --profile (the gate resolves its own).'
  const r = await agent(
    `Run the repo's quality gate and report the result. Do NOT fix, edit, stage or retry anything.
1. cd "$(git rev-parse --show-toplevel)"
2. Run: ${cmd}
   ${profileStep}
   Capture stdout and the exit code (e.g. \`...; echo "exit=$?"\`).
3. Report: exitCode (the process exit code); parsed (true iff stdout is a valid JSON report); verdict (the report's "verdict"); checks (the report's "checks" array, each item's name/status/blocking/detail, detail truncated to 300 chars); maturity (if the report's "profile" is a path to an existing file, the "maturity" string in that JSON file, else "active"). If stdout was not valid JSON set parsed=false, checks=[] and raw to its first 500 chars.`,
    { label: label || 'gate', phase: ph, schema: GATE_SCHEMA, model: 'haiku', effort: 'low' },
  )
  const gateError = (raw) => ({ ok: FAIL_OPEN_ON_ERROR, verdict: 'error', blocking_failures: [], checks: [], maturity: 'active', raw: raw || '' })
  if (!r || typeof r.exitCode !== 'number' || r.exitCode === 2 || !r.parsed) return gateError(r && r.raw)
  const gateChecks = Array.isArray(r.checks) ? r.checks : []
  return {
    ok: r.exitCode === 0,
    verdict: typeof r.verdict === 'string' ? r.verdict : (r.exitCode === 0 ? 'pass' : 'fail'),
    // derived here: checks where blocking === true && status in {fail, error}
    blocking_failures: gateChecks.filter((c) => c && c.blocking === true && (c.status === 'fail' || c.status === 'error')),
    checks: gateChecks,
    maturity: (typeof r.maturity === 'string' && r.maturity) ? r.maturity : 'active',
    raw: '',
  }
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

// ---- Phase 2: pipeline transform-in-worktree -> quality-gate verify PER site -
phase('Transform+Verify')
const results = await pipeline(
  swept,
  async (s) => {
    // transform one site in isolation
    const transform = await agent(
      `Apply this migration to EXACTLY ONE site, in an isolated worktree, as a surgical change. Do not touch other sites; do not refactor adjacent code. Report a one-line summary and the files you changed.

MIGRATION: ${TARGET}
SITE: ${s.site}
WHY THIS SITE: ${s.why}`,
      { label: `transform:${shortName(s.site)}`, phase: 'Transform+Verify', schema: TRANSFORM_SCHEMA, agentType: 'general-purpose' },
    )
    // verify THAT site with the gate
    const gate = await runGate({ profile: PROFILE, checks: CHECKS, label: `verify:${shortName(s.site)}`, phase: 'Transform+Verify' })
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
// The gate is fail-open: a gate-internal error (verdict 'error', ok true) counts
// as green here, exactly as before; set FAIL_OPEN_ON_ERROR=false to block.
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
