# Diff Review

One-line summary: final review checks whether the diff matches spec, avoids scope creep, and leaves rollback clear.

## Review Order
- User intent: every changed file must map to the requested outcome.
- Safety: no secrets, broad trust, destructive commands, or silent prod impact.
- Correctness: config keys valid, links resolvable, generated files reproducible.
- Tokenomics: no bloated AGENTS text, repeated guidance, or static loading of optional resources.
- Hygiene: no `.bak`, `*.example`, `*~`, broad staging, or unrelated refactor.

## Required Output
- Changed files grouped by purpose.
- Verification commands with pass/fail.
- Known residual risk.
- Rollback path.

## Escalation
- Use `cx/gpt-5.5-xhigh` for final review of auth, infra, security, agent policy, MCP, or multi-file config.
- Use medium profile for small docs-only changes after checks pass.
