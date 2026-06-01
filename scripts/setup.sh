#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_DIR="${CODEX_DIR:-$HOME/.codex}"
HOME_AGENTS="${HOME_AGENTS:-$HOME/AGENTS.md}"
TS="$(date +%Y%m%d-%H%M%S)"
DRY_RUN=0
FORCE_CONFIG=0
SYNC_SKILLS=0
CONFIG_WRITTEN=0
POLICY_FILES=(AGENTS.md RTK.md SKILLS_POLICY.md WORKFLOW.md VERIFY.md)

usage() {
  echo "usage: $0 [--dry-run] [--preserve-config] [--force-config] [--with-skills]" >&2
}

for arg in "$@"; do
  case "$arg" in
    --dry-run)
      DRY_RUN=1
      ;;
    --preserve-config)
      FORCE_CONFIG=0
      ;;
    --force-config)
      FORCE_CONFIG=1
      ;;
    --with-skills)
      SYNC_SKILLS=1
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done

warn_professional_use() {
  cat >&2 <<'EOF'
PROFESSIONAL WARNING: this installer enforces the Dimbo Codex policy kernel.
It replaces global Codex instruction files. Existing files are backed up first.
Existing config.toml is preserved by default; use --force-config to replace it.
Use --with-skills only after reviewing external skill source impact.
EOF
}

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
  local backup_name="${2:-$(basename "$path")}"
  if [[ -f "$path" ]]; then
    run mkdir -p "$CODEX_DIR/backups/$TS"
    run cp "$path" "$CODEX_DIR/backups/$TS/$backup_name"
    run cp "$path" "$path.backup.$TS"
  fi
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "missing required command: $1" >&2
    exit 1
  }
}

require_cmd python3
if [[ "$SYNC_SKILLS" == "1" ]]; then
  require_cmd git
fi

warn_professional_use

run mkdir -p "$CODEX_DIR" "$CODEX_DIR/vendor" "$CODEX_DIR/skills"

for file in "${POLICY_FILES[@]}"; do
  backup_file "$CODEX_DIR/$file"
done
backup_file "$HOME_AGENTS" "HOME_AGENTS.md"
backup_file "$CODEX_DIR/hooks.json"
if [[ "$FORCE_CONFIG" == "1" || ! -f "$CODEX_DIR/config.toml" ]]; then
  backup_file "$CODEX_DIR/config.toml"
fi

for file in "${POLICY_FILES[@]}"; do
  run cp "$ROOT/$file" "$CODEX_DIR/$file"
done
run cp "$ROOT/AGENTS.md" "$HOME_AGENTS"
run cp "$ROOT/config/hooks.json" "$CODEX_DIR/hooks.json"
run cp "$ROOT/config/config.toml.example" "$CODEX_DIR/config.toml.example"
if [[ "$FORCE_CONFIG" == "1" || ! -f "$CODEX_DIR/config.toml" ]]; then
  run cp "$ROOT/config/config.toml.example" "$CODEX_DIR/config.toml"
  CONFIG_WRITTEN=1
fi

if [[ "$DRY_RUN" == "0" && "$HOME" != "/home/d0mb1" ]]; then
  rewrite_paths=(
    "$HOME_AGENTS"
    "$CODEX_DIR/AGENTS.md"
    "$CODEX_DIR/RTK.md"
    "$CODEX_DIR/SKILLS_POLICY.md"
    "$CODEX_DIR/WORKFLOW.md"
    "$CODEX_DIR/VERIFY.md"
    "$CODEX_DIR/config.toml.example"
  )
  if [[ "$CONFIG_WRITTEN" == "1" ]]; then
    rewrite_paths+=("$CODEX_DIR/config.toml")
  fi
  python3 - "$HOME" "${rewrite_paths[@]}" <<'PY'
from pathlib import Path
import sys
home = sys.argv[1]
for name in sys.argv[2:]:
    path = Path(name)
    if path.exists():
        path.write_text(path.read_text().replace("/home/d0mb1", home))
PY
fi

if [[ "$DRY_RUN" == "1" && "$CONFIG_WRITTEN" == "1" && "$FORCE_CONFIG" == "1" ]]; then
  echo "[dry-run] config.toml would be enforced from config/config.toml.example." >&2
elif [[ "$DRY_RUN" == "1" && "$CONFIG_WRITTEN" == "1" ]]; then
  echo "[dry-run] config.toml would be created from config/config.toml.example." >&2
elif [[ "$CONFIG_WRITTEN" == "1" && "$FORCE_CONFIG" == "1" ]]; then
  echo "config.toml enforced from config/config.toml.example; backup: $CODEX_DIR/backups/$TS" >&2
elif [[ "$CONFIG_WRITTEN" == "1" ]]; then
  echo "config.toml created from config/config.toml.example; review placeholders." >&2
else
  echo "config.toml preserved; template installed as config.toml.example only." >&2
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

if [[ "$SYNC_SKILLS" == "1" ]]; then
  clone_or_update "https://github.com/sickn33/antigravity-awesome-skills.git" \
    "$CODEX_DIR/vendor/antigravity-awesome-skills"
  clone_or_update "https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git" \
    "$CODEX_DIR/vendor/Anthropic-Cybersecurity-Skills"

  if [[ "$DRY_RUN" == "1" ]]; then
    echo "[dry-run] python3 $ROOT/scripts/sync_codex_skills.py"
  else
    python3 "$ROOT/scripts/sync_codex_skills.py"
    python3 "$ROOT/scripts/check_skill_hygiene.py"
  fi
else
  echo "skill sync skipped; rerun with --with-skills to install/update external skills." >&2
fi

echo "setup complete. review config.toml placeholders; secrets were not installed."
