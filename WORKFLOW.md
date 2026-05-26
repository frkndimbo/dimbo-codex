# Workflow Policy

## Modes
- `build mode`: implement fast with minimal explanation.
- `research mode`: prioritize reading, docs, comparison, then findings.
- `review mode`: analyze only; findings first, ordered by severity with file/line references.
- `debug mode`: hypothesis -> test -> conclusion; stop after repeated failure and change strategy.
- `normal mode`: reset user-facing mode overrides.

Modes persist until explicitly changed by the user or higher-priority runtime instructions.

## Decision Rules
- Act immediately when task is clear, risk is low, and local context can settle details.
- Ask first when intent is ambiguous, choices materially change outcome, action is irreversible, or scope is broad.
- Scope to the requested task; avoid opportunistic refactors.
- In monorepos, work inside the relevant package/service and respect nested `AGENTS.md` files.

## Hooks
- `preToolUse`: read hook output; if access is denied, stop.
- `postToolUse`: incorporate feedback before next action.
- `fileEdited`, `fileCreated`, `fileDeleted`: acknowledge and follow hook prompt.
- `runCommand`: wait for command output before continuing.
- Never fight hook output or retry blocked actions unchanged.

## Failure Postmortem
After the same approach fails twice, use this format before trying a new strategy:

```markdown
### Postmortem
Root Cause: <one-line diagnosis>
Attempted: <numbered attempts>
Why It Failed: <concise reason per attempt>
Next Strategy: <different approach>
Confidence: <low|medium|high>
```

## Git
- Use Conventional Commits: `<type>(<scope>): <description>`.
- Subject max 50 characters.
- Types: feat, fix, refactor, docs, test, chore, perf, ci, style.
- Stage specific files only.
- Prefer new commits over amend.
- Never force-push without explicit permission.
- Push to a new branch unless the user asks for main/master.

## Project Defaults
- Match the project toolchain over global preferences.
- If multiple tools are valid and the project has no established choice, prefer: Bun > pnpm > npm > yarn; biome > eslint > tslint; vitest > jest > mocha; vite > webpack > parcel; fetch > axios > got; Tailwind > CSS modules > styled-components.
- Known `9router` constraints: Node.js >=18, Bun, better-sqlite3, esbuild; never bundle native binaries; never output `jwt-secret` or `machine-id`; back up `~/.9router/db/` before schema migrations.

## Self-Improvement
- When the same correction or workaround repeats more than twice, propose a concise AGENTS rule addition.
- Apply the rule only after user confirmation.
- Add it to the most specific applicable AGENTS file.
