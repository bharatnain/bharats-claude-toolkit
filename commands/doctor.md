---
description: Health-check the toolkit setup — settings, plugins, tools — and walk through the exact fixes
---

Run the toolkit health check and help the user act on it.

1. Run `python3 scripts/doctor.py` and read the checklist it prints. The script is
   the single source of truth — do not hardcode or re-derive any check logic here.
2. Summarize the results for the user: lead with whether the system is healthy
   (exit 0) or has a CRITICAL failure (exit 1), then surface any ✗/⚠ lines.
3. For each failing or warning line, relay the exact fix the script already
   printed inline (overwhelmingly `bash scripts/bootstrap.sh` for settings/plugin/
   marketplace gaps, or the one-line install hint for a missing tool). Offer to run
   `bash scripts/bootstrap.sh` for them when that is the fix.
4. Reassure on optionals: `bd`, `ffmpeg`, `FAL_KEY`, and the notifier are OPTIONAL —
   a minimal setup that only ⚠'s on those is still healthy and exits 0.
