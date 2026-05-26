# Dimbo Codex CLI Backup

Safe backup of Codex CLI agent instructions, policy references, graphify
integration notes, skill source locks, and restore scripts.

## Dense Policy Model

`AGENTS.md` is the dense kernel. It keeps the operational rules directly in the
prompt surface while reference docs hold routing detail.

Priority layers:

1. Safety & Harmlessness
2. Correctness & Honesty
3. Efficiency & Scalability
4. Adaptability & Style

Conflict rule: higher layers always win. L1 beats L2-L4, L2 beats L3-L4, and L3
beats L4.

## Professional Warning

This repository is opinionated. Running `scripts/setup.sh` enforces the Dimbo
Codex policy kernel on the target machine and replaces the user's global Codex
instruction files plus `~/.codex/config.toml` by default.

Use it professionally only after reviewing the policy docs and the generated
backup. Existing files are backed up first under `~/.codex/backups/<timestamp>`
and alongside the original file as `*.backup.<timestamp>`.

## Contents

- `AGENTS.md`: final global Codex agent instructions.
- `RTK.md`: local RTK command rules.
- `SKILLS_POLICY.md`: skill, MCP, docs, and web routing.
- `WORKFLOW.md`: modes, hooks, git, and failure handling.
- `VERIFY.md`: validation checklist by task type.
- `config/hooks.json`: non-secret Codex hook config.
- `config/config.toml.example`: redacted config template. Do not commit real
  `config.toml`.
- `sources.lock.json`: source repo commits, sync counts, graph tool decision.
- `scripts/setup.sh`: reinstall on another device.
- `scripts/backup.sh`: create local backup from an existing Codex install.
- `scripts/restore.sh`: restore from a local backup.

## Dependencies

- Codex CLI config directory at `~/.codex`.
- `git`, `python3`, `cp`, `mkdir`, `find`.
- `rtk` recommended for manual agent commands.
- Optional: `uv` or `uvx` if reinstalling `graphifyy` and paper-search MCP.

## Reapply On A New Device

```bash
git clone https://github.com/frkndimbo/dimbo-codex.git ~/dimbo-codex
cd ~/dimbo-codex
./scripts/setup.sh --dry-run
./scripts/setup.sh
```

`setup.sh` backs up existing policy docs, `hooks.json`, and `config.toml` before
replacing them. It does not install real secrets; any placeholder secret values
must be replaced manually after install.

To install policy docs while keeping the user's current `config.toml`:

```bash
./scripts/setup.sh --preserve-config
```

## Restore

```bash
./scripts/restore.sh ~/.codex/backups/<timestamp>
```

Restore reinstalls `AGENTS.md`, `RTK.md`, `SKILLS_POLICY.md`, `WORKFLOW.md`,
`VERIFY.md`, `config.toml`, and `hooks.json` from the selected backup when
present.

## Safety

Never commit raw `~/.codex/config.toml`, `auth.json`, sqlite state, logs,
history, private keys, API keys, tokens, or `.env` files.
