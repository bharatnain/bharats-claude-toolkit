# Go rules
- Run the repo's test command after changes; add a test for every bug fix.
- Check every returned `error`; no bare `_` discards on error results.
- Keep packages under ~300 lines per file; split by responsibility.
- Never edit `go.sum` by hand.
