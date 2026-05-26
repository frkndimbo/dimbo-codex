#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_DIR="${CODEX_DIR:-$HOME/.codex}"
TS="$(date +%Y%m%d-%H%M%S)"
OUT="$ROOT/backups/$TS"

mkdir -p "$OUT/config"

copy_if_exists() {
  local src="$1"
  local dst="$2"
  if [[ -f "$src" ]]; then
    cp "$src" "$dst"
  fi
}

copy_if_exists "$CODEX_DIR/AGENTS.md" "$OUT/AGENTS.md"
copy_if_exists "$CODEX_DIR/RTK.md" "$OUT/RTK.md"
copy_if_exists "$CODEX_DIR/SKILLS_POLICY.md" "$OUT/SKILLS_POLICY.md"
copy_if_exists "$CODEX_DIR/WORKFLOW.md" "$OUT/WORKFLOW.md"
copy_if_exists "$CODEX_DIR/VERIFY.md" "$OUT/VERIFY.md"
copy_if_exists "$CODEX_DIR/hooks.json" "$OUT/config/hooks.json"
copy_if_exists "$CODEX_DIR/skills-integration-report.json" "$OUT/skills-integration-report.json"

if [[ -f "$CODEX_DIR/config.toml" ]]; then
  python3 - "$CODEX_DIR/config.toml" "$OUT/config/config.toml.redacted" <<'PY'
from pathlib import Path
import re
import sys
src = Path(sys.argv[1]).read_text()
src = re.sub(r'([A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD)[A-Z0-9_]*\s*=\s*")[^"]*(")', r'\1REDACTED\2', src)
Path(sys.argv[2]).write_text(src)
PY
fi

echo "$OUT"
