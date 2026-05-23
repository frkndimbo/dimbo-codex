# Dimbo Codex CLI Backup

Safe backup of Codex CLI agent instructions, graphify integration notes, skill
source locks, and restore scripts.

## Contents

- `AGENTS.md`: final global Codex agent instructions.
- `RTK.md`: local RTK command rules.
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

`setup.sh` backs up existing `~/.codex/AGENTS.md`, `RTK.md`, and `hooks.json`
before replacing them. It does not install real secrets. Merge
`config/config.toml.example` manually into `~/.codex/config.toml`.

## Restore

```bash
./scripts/restore.sh ~/.codex/backups/<timestamp>
```

## Safety

Never commit raw `~/.codex/config.toml`, `auth.json`, sqlite state, logs,
history, private keys, API keys, tokens, or `.env` files.

