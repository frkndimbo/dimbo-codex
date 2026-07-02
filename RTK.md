# RTK - Rust Token Killer (Codex CLI)

**Usage**: Token-optimized CLI proxy for shell commands.

Current local version: `rtk 0.43.0`.

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

Native routes are narrow wrappers, not full shell replacements. Known rule:
`rtk find` supports simple find queries only. For compound predicates/actions
(`-o`, `-not`, `-exec`, complex grouping), use:

```bash
rtk proxy find <args>
rtk run "find <args>"
```

If a compact route rejects syntax, switch route once instead of retrying the
same failing form.

## Meta Commands

```bash
rtk --ultra-compact -v gain            # Token savings analytics
rtk --ultra-compact -v gain --history  # Recent command savings history
rtk proxy <cmd>           # Run raw command without filtering
```

## Verification

```bash
rtk --version
# expected: rtk 0.43.0
rtk --ultra-compact -v gain
rtk proxy which rtk
```
