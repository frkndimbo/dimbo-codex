#!/usr/bin/env bash
set -eu

cat >/dev/null

if [ -f graphify-out/graph.json ]; then
  printf '%s
' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"graphify: Knowledge graph exists. Read graphify-out/GRAPH_REPORT.md for god nodes and community structure before searching raw files."}}'
fi
