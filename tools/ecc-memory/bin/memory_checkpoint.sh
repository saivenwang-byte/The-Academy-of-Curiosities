#!/usr/bin/env bash
# ECC memory checkpoint · Bash
# 见 docs/learning/ecc/00_ECC_长期记忆全指南_V1.0.md
set -euo pipefail

TOPIC=""
NOTES=""
DRY_RUN=0

usage() {
  echo "Usage: $0 \"Topic\" [--notes \"...\"] [--dry-run]"
  exit 1
}

if [[ $# -lt 1 ]]; then
  usage
fi

TOPIC="$1"
shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --notes)
      NOTES="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    *)
      echo "Unknown option: $1"
      usage
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SESSIONS_DIR="$ROOT_DIR/.cursor/memory/sessions"
TEMPLATE_FILE="$ROOT_DIR/tools/ecc-memory/templates/checkpoint.md.template"

slugify() {
  local s
  s="$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^[:alnum:]_\u4e00-\u9fff]+/-/g; s/^-+|-+$//g')"
  if [[ -z "$s" ]]; then s="checkpoint"; fi
  echo "${s:0:40}" | sed 's/-$//'
}

DATE="$(date +%Y-%m-%d)"
SLUG="$(slugify)"
FILENAME="${DATE}_${SLUG}.md"
OUT_PATH="$SESSIONS_DIR/$FILENAME"

if [[ -f "$OUT_PATH" ]]; then
  n=2
  base="${DATE}_${SLUG}"
  while [[ -f "$OUT_PATH" ]]; do
    FILENAME="${base}_${n}.md"
    OUT_PATH="$SESSIONS_DIR/$FILENAME"
    ((n++)) || true
  done
fi

BRANCH="unknown"
if git -C "$ROOT_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  BRANCH="$(git -C "$ROOT_DIR" branch --show-current 2>/dev/null || echo unknown)"
fi

TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S %z')"
NOTES_BLOCK="${NOTES:-（无）}"

if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo "Missing template: $TEMPLATE_FILE" >&2
  exit 1
fi

CONTENT="$(sed \
  -e "s|{{DATE}}|$DATE|g" \
  -e "s|{{TOPIC}}|$TOPIC|g" \
  -e "s|{{BRANCH}}|$BRANCH|g" \
  -e "s|{{TIMESTAMP}}|$TIMESTAMP|g" \
  -e "s|{{NOTES}}|$NOTES_BLOCK|g" \
  "$TEMPLATE_FILE")"

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "[DryRun] Would write: $OUT_PATH"
  echo "$CONTENT"
  exit 0
fi

mkdir -p "$SESSIONS_DIR"
printf '%s\n' "$CONTENT" > "$OUT_PATH"
echo "Checkpoint written: $OUT_PATH"
echo "Next: update .cursor/memory/MEMORY.md checkpoint index table."
