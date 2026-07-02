#!/usr/bin/env sh
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
BACKUP_DIR="$CODEX_HOME/backups/$(date +%Y%m%d-%H%M%S)"
DRY_RUN=0
FORCE_CONFIG=0

usage() {
  echo "usage: sh scripts/install.sh [--dry-run] [--force-config]" >&2
}

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --force-config) FORCE_CONFIG=1 ;;
    *) usage; exit 1 ;;
  esac
done

run() {
  if [ "$DRY_RUN" = 1 ]; then
    printf '[dry-run] %s\n' "$*"
  else
    "$@"
  fi
}

backup_path() {
  BACKUP_SRC="$1"
  BACKUP_REL="$2"
  if [ -e "$BACKUP_SRC" ]; then
    run mkdir -p "$BACKUP_DIR/$(dirname "$BACKUP_REL")"
    run cp -R "$BACKUP_SRC" "$BACKUP_DIR/$BACKUP_REL"
  fi
}

copy_file() {
  COPY_SRC="$1"
  COPY_DST="$2"
  COPY_REL="${COPY_DST#"$CODEX_HOME/"}"
  backup_path "$COPY_DST" "$COPY_REL"
  run mkdir -p "$(dirname "$COPY_DST")"
  run cp "$COPY_SRC" "$COPY_DST"
}

copy_dir() {
  COPY_SRC="$1"
  COPY_DST="$2"
  COPY_REL="${COPY_DST#"$CODEX_HOME/"}"
  backup_path "$COPY_DST" "$COPY_REL"
  run mkdir -p "$(dirname "$COPY_DST")"
  run cp -R "$COPY_SRC" "$COPY_DST"
}

run mkdir -p "$CODEX_HOME"

for file in AGENTS.md RTK.md WORKFLOW.md VERIFY.md SKILLS_POLICY.md SPEC_DESIGN.md EVAL_DESIGN.md DIFF_REVIEW.md TOKENOMICS.md SKILL_PRUNING.md; do
  [ -f "$ROOT/$file" ] && copy_file "$ROOT/$file" "$CODEX_HOME/$file"
done

if [ -d "$ROOT/skills" ]; then
  copy_dir "$ROOT/skills" "$CODEX_HOME/skills"
fi

copy_file "$ROOT/config/config.toml.template" "$CODEX_HOME/config.toml.template"

if [ "$FORCE_CONFIG" = 1 ] || [ ! -f "$CODEX_HOME/config.toml" ]; then
  copy_file "$ROOT/config/config.toml.template" "$CODEX_HOME/config.toml"
else
  echo "config.toml preserved; use --force-config to replace it."
fi

echo "install complete: $CODEX_HOME"
echo "backup: $BACKUP_DIR"
