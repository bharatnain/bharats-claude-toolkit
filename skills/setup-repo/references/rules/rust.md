# Rust rules
- Run the repo's test command after changes; add a test for every bug fix.
- Prefer `Result`/`?` over `unwrap()`/`expect()` outside tests.
- Keep modules under ~300 lines; split by responsibility.
- Never edit `Cargo.lock` by hand.
