// workflows/lib/runner.js
//
// Dependency-free helper used by the Workflow templates in ../*.workflow.js.
// Shells the canonical quality gate (scripts/quality_gate.py) and returns a
// stable verdict object the templates use to drive control flow.
//
// No package.json, no third-party deps, no network. Only node: builtins.
//
// CANONICAL RESOLVERS: scripts/team_sentinel.py (Python) remains the source of
// truth for repo-root and profile-name resolution at runtime (it is what the
// team_gate hook and the gate runner consult). repoRoot() and loadProfileName()
// below are deliberately thin JS RE-IMPLEMENTATIONS that mirror that precedence
// exactly, so the JS workflow layer and the Python gate layer agree without
// shelling Python on every call. If you change the Python precedence, mirror it
// here too.

import { spawnSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'

// ---------------------------------------------------------------------------
// repoRoot() — walk up to a `.git` entry (file OR dir, so worktrees & submodules
// resolve), falling back to process.cwd(). Mirrors team_sentinel's resolver.
// ---------------------------------------------------------------------------
export function repoRoot(startDir) {
  let dir
  try {
    dir = path.resolve(startDir || process.cwd())
  } catch {
    return process.cwd()
  }
  // Bound the walk by the filesystem root; path.dirname('/') === '/'.
  // eslint-disable-next-line no-constant-condition
  while (true) {
    try {
      if (fs.existsSync(path.join(dir, '.git'))) {
        return dir
      }
    } catch {
      // permission error on a parent — give up, fall back to cwd
      break
    }
    const parent = path.dirname(dir)
    if (parent === dir) break // reached filesystem root
    dir = parent
  }
  return process.cwd()
}

// ---------------------------------------------------------------------------
// loadProfileName() — active profile NAME, by precedence. This MUST match
// team_sentinel.resolve_profile (scripts/team_sentinel.py) byte-for-byte in
// ordering and gating so the JS workflow layer and the Python gate agree:
//   (1) team-context marker  <root>/.claude/team-context.json -> .profile,
//                            but ONLY when .active === true
//   (2) $CLAUDE_TEAM_PROFILE used RAW (no basename, no .json strip)
//   (3) team-profile marker  <root>/.claude/team-profile.json -> .maturity
//   (4) 'active'             safe default
// Every read is guarded; a malformed/inactive marker falls through.
// ---------------------------------------------------------------------------
export function loadProfileName(root) {
  const rt = root || repoRoot()

  // (1) team-context marker — honored only when active is true.
  const ctx = readJsonSafe(path.join(rt, '.claude', 'team-context.json'))
  if (ctx && ctx.active === true && typeof ctx.profile === 'string' && ctx.profile.trim()) {
    return ctx.profile.trim()
  }

  // (2) $CLAUDE_TEAM_PROFILE — used raw, exactly as Python does.
  const env = process.env.CLAUDE_TEAM_PROFILE
  if (env && env.trim()) return env.trim()

  // (3) team-profile marker maturity
  const prof = readJsonSafe(path.join(rt, '.claude', 'team-profile.json'))
  if (prof && typeof prof.maturity === 'string' && prof.maturity.trim()) {
    return prof.maturity.trim()
  }

  // (4) default
  return 'active'
}

function readJsonSafe(p) {
  try {
    const raw = fs.readFileSync(p, 'utf8')
    const data = JSON.parse(raw)
    return data && typeof data === 'object' ? data : null
  } catch {
    return null
  }
}

// Resolve a profile NAME (e.g. 'legacy') or an explicit PATH to a profile file.
// Returns an absolute path to an existing file, or null if it does not resolve
// (in which case runGate omits --profile and the gate uses its built-in
// 'active' defaults).
function resolveProfilePath(profile, root) {
  if (!profile || typeof profile !== 'string' || !profile.trim()) return null
  const p = profile.trim()
  // An explicit path (contains a separator or .json suffix) is used as-is.
  if (p.includes('/') || p.includes(path.sep) || /\.json$/i.test(p)) {
    const abs = path.isAbsolute(p) ? p : path.join(root, p)
    return fileExists(abs) ? abs : null
  }
  // Otherwise treat as a profile NAME under <root>/team-profiles/<name>.json.
  const named = path.join(root, 'team-profiles', `${p}.json`)
  return fileExists(named) ? named : null
}

function fileExists(p) {
  try {
    return fs.statSync(p).isFile()
  } catch {
    return false
  }
}

// ---------------------------------------------------------------------------
// runGate({changedFiles, profile, checks})
//
// Shells `python3 <repoRoot>/scripts/quality_gate.py --format json` plus flags
// derived from the args, captures stdout + exit code, parses the JSON, and
// returns a stable verdict object.
//
// Inputs (all optional):
//   changedFiles  array|truthy — when present, scope is left at the runner
//                 default ('changed'); when explicitly the string 'all' (or
//                 {scope:'all'}) the whole project is scoped via --scope all.
//                 Note: quality_gate.py derives the changed set from git itself;
//                 we do not pass a file list, we only pick the scope flag.
//   profile       a profile NAME ('legacy') resolved to
//                 <root>/team-profiles/<name>.json, OR an explicit path. An
//                 unresolved name is silently ignored (gate uses its built-in
//                 'active' defaults — no --profile flag).
//   checks        array|csv-string of {lint,typecheck,test,build} — passed as
//                 --checks <csv>. Omitted ⇒ the gate runs all four.
//
// Returns: { ok, verdict, blocking_failures, checks, raw }
//   ok                 true iff the runner exit code is 0
//   verdict            parsed report.verdict, or 'error' on a runner-2/parse
//                      failure
//   blocking_failures  DERIVED here (the gate emits no such top-level field):
//                      checks where blocking===true && status in {fail,error}
//   checks             the parsed report.checks array (or [])
//   raw                the unparsed stdout
//
// EXIT-CODE → SEMANTICS (same mapping as the team_gate hook):
//   exit 0  → { ok:true,  verdict:'pass' (or parsed), blocking_failures:[] }
//   exit 1  → { ok:false, verdict:'fail', blocking_failures:[...] }
//   exit 2  → gate INTERNAL error. FAIL-OPEN: { ok:true, verdict:'error' }.
//             This matches the hook's "never wedge the developer" philosophy.
//             A copying author who wants stricter CI can flip FAIL_OPEN_ON_ERROR
//             to false below (and update the README note).
//   unparsable stdout on a 0/1 exit → treated as a parse failure: FAIL-OPEN,
//             { ok:true, verdict:'error' } (same rationale).
// ---------------------------------------------------------------------------

// Flip to false for fail-CLOSED CI (gate-internal-error ⇒ block). Documented in
// workflows/README.md.
const FAIL_OPEN_ON_ERROR = true

export function runGate(opts = {}) {
  const { changedFiles, profile, checks } = normalizeGateOpts(opts)
  const root = repoRoot()
  const script = path.join(root, 'scripts', 'quality_gate.py')

  const argv = [script, '--format', 'json']

  if (checks && checks.length) {
    argv.push('--checks', checks.join(','))
  }

  // scope flag: default ('changed') unless caller asked for the whole project.
  if (changedFiles === 'all') {
    argv.push('--scope', 'all')
  }

  const profPath = resolveProfilePath(profile, root)
  if (profPath) {
    argv.push('--profile', profPath)
  }

  let res
  try {
    res = spawnSync('python3', argv, {
      cwd: root,
      encoding: 'utf8',
      maxBuffer: 64 * 1024 * 1024,
    })
  } catch (e) {
    // Could not even spawn the runner — treat as gate-internal error.
    return errorResult(`failed to spawn quality_gate.py: ${e && e.message}`)
  }

  // spawnSync sets res.error on spawn failure (e.g. python3 not found).
  if (res.error) {
    return errorResult(`failed to spawn quality_gate.py: ${res.error.message}`)
  }

  const code = res.status
  const raw = res.stdout || ''

  // exit 2 (or null/signal) ⇒ gate internal error.
  if (code === 2 || code === null || typeof code !== 'number') {
    return errorResult(raw)
  }

  // Parse the JSON report.
  let report
  try {
    report = JSON.parse(raw)
  } catch {
    // Unparsable output on a 0/1 exit ⇒ parse failure ⇒ fail-open/closed choice.
    return errorResult(raw)
  }

  const parsedChecks = Array.isArray(report.checks) ? report.checks : []
  const blocking_failures = parsedChecks.filter(
    (c) => c && c.blocking === true && (c.status === 'fail' || c.status === 'error'),
  )

  return {
    ok: code === 0,
    verdict: typeof report.verdict === 'string' ? report.verdict : (code === 0 ? 'pass' : 'fail'),
    blocking_failures,
    checks: parsedChecks,
    raw,
  }
}

function errorResult(raw) {
  return {
    ok: FAIL_OPEN_ON_ERROR, // fail-open: error does not block the workflow
    verdict: 'error',
    blocking_failures: [],
    checks: [],
    raw: raw || '',
  }
}

// Defensive normalization: accept a bare value, an object, or undefined.
function normalizeGateOpts(opts) {
  let o = opts
  if (typeof o === 'string') {
    try {
      o = JSON.parse(o)
    } catch {
      o = {}
    }
  }
  if (!o || typeof o !== 'object') o = {}

  // changedFiles: pass through 'all' as a sentinel, else leave to default scope.
  let changedFiles = o.changedFiles
  if (o.scope === 'all' || changedFiles === 'all') changedFiles = 'all'

  // checks: accept array or csv string; keep only the canonical names.
  let checks = o.checks
  if (typeof checks === 'string') {
    checks = checks.split(',').map((s) => s.trim()).filter(Boolean)
  }
  if (Array.isArray(checks)) {
    const allowed = ['lint', 'typecheck', 'test', 'build']
    checks = checks.filter((c) => allowed.includes(c))
  } else {
    checks = null
  }

  return { changedFiles, profile: o.profile, checks }
}
