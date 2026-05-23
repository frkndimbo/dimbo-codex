#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_DIR="${CODEX_DIR:-$HOME/.codex}"
TS="$(date +%Y%m%d-%H%M%S)"
DRY_RUN=0

if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

run() {
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[dry-run] %q ' "$@"
    printf '\n'
  else
    "$@"
  fi
}

backup_file() {
  local path="$1"
  if [[ -f "$path" ]]; then
    run mkdir -p "$CODEX_DIR/backups/$TS"
    run cp "$path" "$CODEX_DIR/backups/$TS/$(basename "$path")"
    run cp "$path" "$path.backup.$TS"
  fi
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "missing required command: $1" >&2
    exit 1
  }
}

require_cmd git
require_cmd python3

run mkdir -p "$CODEX_DIR" "$CODEX_DIR/vendor" "$CODEX_DIR/skills"

backup_file "$CODEX_DIR/AGENTS.md"
backup_file "$CODEX_DIR/RTK.md"
backup_file "$CODEX_DIR/hooks.json"

run cp "$ROOT/AGENTS.md" "$CODEX_DIR/AGENTS.md"
run cp "$ROOT/RTK.md" "$CODEX_DIR/RTK.md"
run cp "$ROOT/config/hooks.json" "$CODEX_DIR/hooks.json"
run cp "$ROOT/config/config.toml.example" "$CODEX_DIR/config.toml.example"

clone_or_update() {
  local url="$1"
  local dst="$2"
  if [[ -d "$dst/.git" ]]; then
    run git -C "$dst" fetch --all --prune
    run git -C "$dst" pull --ff-only
  elif [[ -e "$dst" ]]; then
    echo "skip non-git existing path: $dst" >&2
  else
    run git clone "$url" "$dst"
  fi
}

clone_or_update "https://github.com/sickn33/antigravity-awesome-skills.git" \
  "$CODEX_DIR/vendor/antigravity-awesome-skills"
clone_or_update "https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git" \
  "$CODEX_DIR/vendor/Anthropic-Cybersecurity-Skills"

if [[ "$DRY_RUN" == "1" ]]; then
  echo "[dry-run] python3 $ROOT/scripts/sync_codex_skills.py"
else
  python3 "$ROOT/scripts/sync_codex_skills.py"
fi

echo "setup complete. merge config.toml.example manually; secrets were not installed."

