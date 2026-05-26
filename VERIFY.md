# Verification Policy

## Code Changes
- Run the narrowest relevant checks first, then broader checks if risk warrants.
- Use project scripts when present; otherwise use language/tool defaults.
- Fix feasible failures before final response.
- If no build/test system exists, state `no build verification available`.

## Default Commands
- Bun projects: `rtk bun test`, `rtk bun run check`, `rtk bun run build` when scripts exist.
- npm projects: `rtk npm run lint`, `rtk npm run test`, `rtk npm run build` when scripts exist.
- Go projects: `rtk go test ./...`; if cache is blocked, use a writable `GOCACHE` under `/tmp`.
- Rust projects: `rtk cargo test` and `rtk cargo clippy` when configured.
- Python projects: use the project runner (`uv`, `pytest`, `ruff`, `mypy`) already present.

## File Operations
- Verify paths before writing outside the current project.
- Make a backup before overwriting important files.
- After file creation or edit, confirm existence and inspect relevant content.
- Use `apply_patch` for manual tracked-file edits.

## Research And Docs
- Cite sources used.
- Check current docs for version-sensitive libraries, APIs, CLIs, and cloud services.
- Use `paper-search-mcp` for academic paper discovery before generic web.

## Frontend/UI
- Run build/type checks.
- For visual changes, inspect rendered output or screenshots when tooling is available.
- Confirm text does not overflow or overlap on desktop and mobile when the change affects layout.

## Security
- Treat security testing as authorized defensive work only.
- Avoid printing secrets.
- For auth, DB, infrastructure, or production config changes, include rollback notes or confirm reversibility.

## Completion Report
- Summarize changed files.
- Report commands run and pass/fail status.
- State any skipped verification and why.
