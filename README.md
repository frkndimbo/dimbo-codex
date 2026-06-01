# Dimbo Codex Config Template

A hardened, portable Codex CLI configuration template for people who want Codex
to behave consistently across projects, machines, and fresh sessions.

This repo is recommended when you want a practical Codex baseline instead of a
loose collection of prompts: safety rules, shell discipline, skill routing,
verification habits, backup/restore scripts, and non-secret config templates are
kept together and installed in a repeatable way.

## Why Use This Template

- **Consistent agent behavior**: installs the same global instruction kernel into
  both `$HOME/AGENTS.md` and `$HOME/.codex/AGENTS.md`, reducing directory-specific
  drift.
- **Safe by default**: backs up existing files first, preserves existing
  `~/.codex/config.toml` by default, and never stores real secrets.
- **Operational, not decorative**: rules cover real failure points: destructive
  actions, dirty git worktrees, stale memory, version-sensitive docs, verification,
  and rollback notes.
- **RTK-first shell discipline**: all agent shell work is routed through `rtk`,
  with explicit patterns for compact reads, searches, git, curl, and complex
  shell commands.
- **Skill routing without chaos**: keeps `$HOME/.codex/skills` as the canonical
  active skill root, treats `$HOME/.agents/skills` as legacy, and includes a
  read-only hygiene checker for duplicate or broken skills.
- **Portable onboarding**: one dry run, one install command, optional external
  skill sync, and a restore script if you need to roll back.

## What You Get

| Area | File | Purpose |
| --- | --- | --- |
| Global agent kernel | `AGENTS.md` | Compact rules Codex should see in every project |
| Shell policy | `RTK.md` | Mandatory `rtk` usage and command patterns |
| Skill/docs routing | `SKILLS_POLICY.md` | When to use skills, MCPs, docs, and web lookup |
| Workflow policy | `WORKFLOW.md` | Modes, hooks, git rules, and retry discipline |
| Verification policy | `VERIFY.md` | Build/test/check expectations by task type |
| Codex config template | `config/config.toml.example` | Redacted, non-secret starting point |
| Hooks config | `config/hooks.json` | Non-secret hook config |
| Installer | `scripts/setup.sh` | Apply this template to a Codex install |
| Backup/restore | `scripts/backup.sh`, `scripts/restore.sh` | Save or restore local Codex policy files |
| Skill hygiene | `scripts/check_skill_hygiene.py` | Check active skills for duplicate names and broken refs |

## Quick Start

```bash
git clone https://github.com/frkndimbo/dimbo-codex.git ~/dimbo-codex
cd ~/dimbo-codex
./scripts/setup.sh --dry-run
./scripts/setup.sh
```

The default install replaces global instruction files, backs them up first, and
preserves an existing `~/.codex/config.toml`. On a fresh machine, it creates
`config.toml` from the redacted template so Codex has a usable starting point.

## Recommended Install Modes

| Goal | Command |
| --- | --- |
| Preview changes | `./scripts/setup.sh --dry-run` |
| Install policy docs safely | `./scripts/setup.sh` |
| Replace existing Codex config with the template | `./scripts/setup.sh --force-config` |
| Install/update external skill sources too | `./scripts/setup.sh --with-skills` |
| Restore a previous backup | `./scripts/restore.sh ~/.codex/backups/<timestamp>` |

Use `--with-skills` only after reviewing the external skill impact. The normal
install intentionally skips network/vendor skill sync so the template applies
cleanly on more machines.

## Why It Works Well As A Codex Baseline

Most Codex setups fail quietly in predictable places: instructions only apply in
one directory, shell commands drift from local policy, config files leak machine
specific state, skill folders duplicate each other, or agents skip verification
after edits. This template addresses those failure modes directly:

- two global instruction surfaces are installed and kept aligned;
- real secrets and runtime state are excluded from git;
- `config.toml` is treated as local state unless explicitly forced;
- skills have one active root and a hygiene check;
- setup and restore are scripted instead of manual copy-paste;
- the README, policies, and installer describe the same behavior.

## Safety Model

This repo is intentionally opinionated. Review the policy files before applying
it to a machine you share with other users or teams.

The installer backs up existing policy docs, `hooks.json`, and config files when
they are about to be replaced. Backups are stored under
`~/.codex/backups/<timestamp>` and beside originals as `*.backup.<timestamp>`.

Never commit raw `~/.codex/config.toml`, `auth.json`, sqlite state, logs,
history, private keys, API keys, tokens, or `.env` files.

## Requirements

- Codex CLI using `~/.codex`.
- `python3`, `cp`, `mkdir`, `find`.
- `git` for cloning this repo or running `--with-skills`.
- `rtk` is recommended for interactive agent shell work.
- Optional: `uv` or `uvx` for Python tool installs such as MCP helpers.

## Verify After Install

```bash
python3 scripts/check_skill_hygiene.py
codex debug prompt-input
```

`codex debug prompt-input` is the fastest way to confirm Codex actually sees the
global `AGENTS.md` instructions from a fresh session and a non-project directory.
