# Spec Design

One-line summary: define intent, scope, interfaces, risk, and acceptance before non-trivial code or config edits.

## Trigger
- Use for edits touching multiple files, auth, DB, infra, security, model config, skill profiles, hooks, or broad refactors.
- Skip for tiny read-only answers and single-line low-risk fixes.

## Required Shape
- Goal: exact user outcome in one sentence.
- Scope: files/systems included and excluded.
- Inputs: repo facts already verified, not guesses.
- Interfaces: config keys, commands, APIs, schemas, or user-visible behavior changed.
- Risks: secrets, destructive ops, prod impact, sandbox escape, trust boundary, stale docs.
- Acceptance: observable pass/fail criteria.
- Rollback: git path, config revert path, or feature flag/profile disable path.

## Model Routing
- Use `cx/gpt-5.5-xhigh` for ambiguous architecture, security, infra, MCP, skill policy, or cross-repo specs.
- Use medium profile for scoped fixes after the spec is stable.
- Use subagents only for bounded evidence gathering, not final decisions.

## Token Rules
- Put long working notes in `inbox/`; load only the active note.
- Prefer file paths, line refs, and concise decisions over pasted excerpts.
- Do not reread whole trees after the relevant files are known.
