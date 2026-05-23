# RTK - Rust Token Killer (Codex CLI)

**Usage**: Token-optimized CLI proxy for shell commands.

## Rule

Always prefix shell commands with `rtk`.
Default form: `rtk <command>`.
Use `rtk --ultra-compact -v <rtk-subcommand> ...` only for RTK subcommands that
are confirmed compatible. For passthrough/native commands, prefer
`rtk <command>`.
Never run native commands as `rtk --ultra-compact -v <command>`.

Examples:

```bash
rtk git status
rtk cargo test
rtk npm run build
rtk pytest -q
```

Prefer compact RTK-native routes:

```bash
rtk read <file>        # instead of cat <file>
rtk grep ...           # instead of grep ...
rtk ls ...             # instead of ls ...
rtk find ...           # instead of find ...
rtk gh api ...         # instead of gh api ...
rtk curl ...           # instead of curl ...
rtk wc ...             # instead of wc ...
```

## Meta Commands

```bash
rtk --ultra-compact -v gain            # Token savings analytics
rtk --ultra-compact -v gain --history  # Recent command savings history
rtk proxy <cmd>           # Run raw command without filtering
```

## Verification

```bash
rtk --version
rtk --ultra-compact -v gain
rtk proxy which rtk
```
