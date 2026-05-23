# Initial Audit

Date: 2026-05-24

## Codex CLI Layout

- Active Codex config root: `~/.codex`.
- Active global instructions: `~/.codex/AGENTS.md`.
- Runtime config: `~/.codex/config.toml`.
- Hooks: `~/.codex/hooks.json`.
- Active skills: `~/.codex/skills`.
- Existing additional skill root: `~/.agents/skills`.
- Local backup created before edits:
  - `~/.codex/AGENTS.md.backup.20260524-044849`
  - `~/.codex/backups/20260524-044849/`

## Sensitive Files Excluded From Git

- `~/.codex/auth.json`
- `~/.codex/history.jsonl`
- `~/.codex/logs_*.sqlite*`
- `~/.codex/state_*.sqlite*`
- `~/.codex/goals_*.sqlite*`
- raw `~/.codex/config.toml`
- private keys, tokens, credentials, `.env` files.

## Skill Integration

- Vendored source roots:
  - `~/.codex/vendor/antigravity-awesome-skills`
  - `~/.codex/vendor/Anthropic-Cybersecurity-Skills`
- Sync result:
  - 909 new active skill directories installed.
  - 1265 exact duplicate skills skipped.
  - 34 conflicting same-name skills copied to `~/.codex/skills.review`.
  - 11 candidates skipped due sensitive-looking file names.
- Detailed local report: `~/.codex/skills-integration-report.json`.

