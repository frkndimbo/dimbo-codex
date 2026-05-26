#!/usr/bin/env bash
set -euo pipefail

CODEX_DIR="${CODEX_DIR:-$HOME/.codex}"
SRC="${1:-}"
TS="$(date +%Y%m%d-%H%M%S)"

if [[ -z "$SRC" || ! -d "$SRC" ]]; then
  echo "usage: $0 <backup-dir>" >&2
  exit 1
fi

mkdir -p "$CODEX_DIR/backups/$TS"

restore_file() {
  local src="$1"
  local dst="$2"
  if [[ -f "$src" ]]; then
    if [[ -f "$dst" ]]; then
      cp "$dst" "$CODEX_DIR/backups/$TS/$(basename "$dst")"
      cp "$dst" "$dst.backup.$TS"
    fi
    cp "$src" "$dst"
  fi
}

restore_file "$SRC/AGENTS.md" "$CODEX_DIR/AGENTS.md"
restore_file "$SRC/RTK.md" "$CODEX_DIR/RTK.md"
restore_file "$SRC/SKILLS_POLICY.md" "$CODEX_DIR/SKILLS_POLICY.md"
restore_file "$SRC/WORKFLOW.md" "$CODEX_DIR/WORKFLOW.md"
restore_file "$SRC/VERIFY.md" "$CODEX_DIR/VERIFY.md"
restore_file "$SRC/config.toml" "$CODEX_DIR/config.toml"
restore_file "$SRC/config/hooks.json" "$CODEX_DIR/hooks.json"

echo "restore complete. pre-restore files saved in $CODEX_DIR/backups/$TS"
