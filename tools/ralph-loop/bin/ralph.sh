#!/usr/bin/env bash
# Ralph Loop · 手动 Bash 版 · 见 docs/learning/ralph-loop/00_全指南_V1.0.md
set -euo pipefail

MAX_ITERATIONS="${1:-10}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE="${RALPH_WORKSPACE:-$ROOT_DIR/workspace}"
PROMPT_FILE="${RALPH_PROMPT:-$WORKSPACE/prompt.md}"
AGENT_CMD="${RALPH_AGENT_CMD:-claude --continue}"
COMPLETE_TAG="${RALPH_COMPLETE_TAG:-<promise>COMPLETE</promise>}"
PROGRESS_FILE="$WORKSPACE/progress.txt"

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "Missing prompt: $PROMPT_FILE"
  echo "Copy templates/prompt.md.template to workspace/prompt.md"
  exit 1
fi

mkdir -p "$WORKSPACE"
echo "Ralph Loop start · max=$MAX_ITERATIONS · workspace=$WORKSPACE"

for i in $(seq 1 "$MAX_ITERATIONS"); do
  echo "═══ Iteration $i / $MAX_ITERATIONS ═══"
  {
    echo ""
    echo "--- iteration $i $(date -Iseconds) ---"
  } >> "$PROGRESS_FILE"

  OUTPUT=$(cat "$PROMPT_FILE" | eval "$AGENT_CMD" 2>&1 | tee /dev/stderr) || true

  if echo "$OUTPUT" | grep -qF "$COMPLETE_TAG"; then
    echo "Done at iteration $i"
    exit 0
  fi

  sleep 2
done

echo "Max iterations reached without COMPLETE"
exit 1
