# Graph Tool Decision

## Current Graphify State

- Binary: `~/.local/bin/graphify`.
- Package: `graphifyy` 0.8.13.
- Source: https://github.com/safishamsi/graphify.
- Existing Codex hook: `~/.codex/hooks.json` injects graphify context when
  `graphify-out/graph.json` exists.
- Existing skill: `~/.agents/skills/graphify`.

## Comparison

| Criterion | graphify | codegraph | Decision |
|---|---|---|---|
| Codex fit | Already installed and Codex-aware | Would need new integration | graphify |
| Current env risk | Low | Medium, changes active tooling | graphify |
| Analysis scope | Code, docs, PDFs, images, video | Code graph focus | graphify |
| Install burden | Already satisfied via uv tool | Additional repo/tooling | graphify |
| Rollback | Existing backups and no change needed | Would require graphify disable path | graphify |

## Final Decision

Keep `graphify`. Do not install `codegraph` now. Revisit only if a future task
needs codegraph-specific behavior and a rollback plan exists.

