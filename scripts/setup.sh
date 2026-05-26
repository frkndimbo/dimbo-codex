#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_DIR="${CODEX_DIR:-$HOME/.codex}"
TS="$(date +%Y%m%d-%H%M%S)"
DRY_RUN=0
POLICY_FILES=(AGENTS.md RTK.md SKILLS_POLICY.md WORKFLOW.md VERIFY.md)

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

for file in "${POLICY_FILES[@]}"; do
  backup_file "$CODEX_DIR/$file"
done
backup_file "$CODEX_DIR/hooks.json"

for file in "${POLICY_FILES[@]}"; do
  run cp "$ROOT/$file" "$CODEX_DIR/$file"
done
run cp "$ROOT/config/hooks.json" "$CODEX_DIR/hooks.json"
run cp "$ROOT/config/config.toml.example" "$CODEX_DIR/config.toml.example"

if [[ "$DRY_RUN" == "0" && "$HOME" != "/home/d0mb1" ]]; then
  python3 - "$HOME" \
    "$CODEX_DIR/AGENTS.md" \
    "$CODEX_DIR/RTK.md" \
    "$CODEX_DIR/SKILLS_POLICY.md" \
    "$CODEX_DIR/WORKFLOW.md" \
    "$CODEX_DIR/VERIFY.md" \
    "$CODEX_DIR/config.toml.example" <<'PY'
from pathlib import Path
import sys
home = sys.argv[1]
for name in sys.argv[2:]:
    path = Path(name)
    if path.exists():
        path.write_text(path.read_text().replace("/home/d0mb1", home))
PY
fi

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
