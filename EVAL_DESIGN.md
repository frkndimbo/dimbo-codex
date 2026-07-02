# Eval Design

One-line summary: verification must be chosen before edits and tied to user-visible success criteria.

## Eval Ladder
- Static sanity: config parse, file existence, targeted grep, no secret echo.
- Unit/local checks: narrow test, lint, typecheck, or project check command.
- Integration checks: MCP list, Codex prompt-input, build, browser, DB dry run, or API smoke test.
- Review checks: diff review, risk regression, rollback confirmation.

## Required For Codex Config
- `rtk proxy codex --version`
- `rtk proxy codex mcp list`
- `rtk proxy codex debug prompt-input`
- `rtk git status --short`
- Skill changes: `rtk proxy python scripts/check_skill_hygiene.py` when available.

## Failure Policy
- If the same approach fails twice, stop and write root cause, attempts, wrong assumptions, new strategy, confidence.
- Do not report partial pass as full pass.
- If a check fails from missing env secret, state required variable name only.

## Token Rules
- Run narrow checks first.
- Summarize repeated failures instead of pasting full logs.
- Store bulky evidence in `inbox/` only when future turns need it.
