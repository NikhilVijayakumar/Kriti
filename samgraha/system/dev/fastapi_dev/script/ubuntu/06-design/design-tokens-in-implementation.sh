#!/usr/bin/env bash
set -euo pipefail

# design-tokens-in-implementation -- Category B cross-domain script
# Checks if design tokens declared in the Design doc actually appear in implementation styling code.

usage() {
  echo "Usage: $0 --repo-root <path> --repo-fingerprint <value> --out <path> --docs-root <path>" >&2
  exit 1
}

REPO_ROOT=""
FINGERPRINT=""
OUT=""
DOCS_ROOT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-root) REPO_ROOT="$2"; shift 2 ;;
    --repo-fingerprint) FINGERPRINT="$2"; shift 2 ;;
    --out) OUT="$2"; shift 2 ;;
    --docs-root) DOCS_ROOT="$2"; shift 2 ;;
    *) usage ;;
  esac
done

if [[ -z "$REPO_ROOT" || -z "$FINGERPRINT" || -z "$OUT" || -z "$DOCS_ROOT" ]]; then
  usage
fi

EXECUTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

write_result() {
  local status="$1"
  local evidence="$2"
  local tokens_declared="$3"
  local tokens_found="$4"
  local tokens_missing="$5"
  cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$FINGERPRINT",
  "check": "design-tokens-in-implementation",
  "domain": "06-design",
  "category": "B",
  "status": "$status",
  "metrics": {
    "tokens_declared": $tokens_declared,
    "tokens_found": $tokens_found,
    "tokens_missing": $tokens_missing
  },
  "evidence": $evidence,
  "executed_at": "$EXECUTED_AT"
}
ENDJSON
  if [[ "$status" == "error" ]]; then exit 1; fi
  exit 0
}

if [[ ! -d "$DOCS_ROOT" ]]; then
  write_result "error" '["Cannot access docs-root: '"$DOCS_ROOT"'"]' 0 0 0
fi

if [[ ! -d "$REPO_ROOT" ]]; then
  write_result "error" '["Cannot access repo-root: '"$REPO_ROOT"'"]' 0 0 0
fi

# Find design documents
DESIGN_FILES=()
while IFS= read -r -d '' f; do
  DESIGN_FILES+=("$f")
done < <(find "$DOCS_ROOT" -name '*.md' -type f -print0 2>/dev/null | while IFS= read -r -d '' f; do
  basename="$(basename "$f")"
  if echo "$basename" | grep -qE '^(06-)?design'; then
    printf '%s\0' "$f"
  fi
done)

if [[ ${#DESIGN_FILES[@]} -eq 0 ]]; then
  write_result "not_applicable" '["No design documents found in docs-root"]' 0 0 0
fi

# Extract tokens from design docs
DECLARED_TOKENS_FILE="$(mktemp)"
trap 'rm -f "$DECLARED_TOKENS_FILE"' EXIT

for df in "${DESIGN_FILES[@]}"; do
  # Hex colors
  grep -oE '#[0-9a-fA-F]{3,8}\b' "$df" 2>/dev/null >> "$DECLARED_TOKENS_FILE" || true
  # Pixel values
  grep -oE '[0-9]+(\.[0-9]+)?px\b' "$df" 2>/dev/null >> "$DECLARED_TOKENS_FILE" || true
  # Rem values
  grep -oE '[0-9]+(\.[0-9]+)?rem\b' "$df" 2>/dev/null >> "$DECLARED_TOKENS_FILE" || true
  # Font family declarations
  grep -oE 'font-family\s*:\s*[^;]+' "$df" 2>/dev/null | sed 's/font-family\s*:\s*//' >> "$DECLARED_TOKENS_FILE" || true
done

sort -u "$DECLARED_TOKENS_FILE" > "${DECLARED_TOKENS_FILE}.uniq"
mv "${DECLARED_TOKENS_FILE}.uniq" "$DECLARED_TOKENS_FILE"

TOKENS_DECLARED=$(wc -l < "$DECLARED_TOKENS_FILE" | tr -d ' ')

if [[ "$TOKENS_DECLARED" -eq 0 ]]; then
  write_result "not_applicable" '["No design tokens found in design documents"]' 0 0 0
fi

# Collect all style content from src/
STYLE_CONTENT_FILE="$(mktemp)"
trap 'rm -f "$DECLARED_TOKENS_FILE" "$STYLE_CONTENT_FILE"' EXIT

SRC_DIR="$REPO_ROOT/src"
if [[ -d "$SRC_DIR" ]]; then
  find "$SRC_DIR" -type f \( -name '*.css' -o -name '*.scss' -o -name '*.less' -o -name '*.styled.*' -o -name '*.styles.*' \) -print0 2>/dev/null | xargs -0 cat >> "$STYLE_CONTENT_FILE" 2>/dev/null || true
  find "$SRC_DIR" -type f \( -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx' \) -print0 2>/dev/null | while IFS= read -r -d '' jf; do
    if grep -qEi '(styled|css|style)' "$jf" 2>/dev/null; then
      cat "$jf" >> "$STYLE_CONTENT_FILE" 2>/dev/null || true
    fi
  done
fi

TOKENS_FOUND=0
TOKENS_MISSING=0
MISSING_EVIDENCE=""

while IFS= read -r token; do
  if [[ -z "$token" ]]; then continue; fi
  escaped_token=$(echo "$token" | sed 's/[.[\*^$()+?{|]/\\&/g')
  if grep -qE "$escaped_token" "$STYLE_CONTENT_FILE" 2>/dev/null; then
    TOKENS_FOUND=$((TOKENS_FOUND + 1))
  else
    TOKENS_MISSING=$((TOKENS_MISSING + 1))
    escaped_token_json=$(echo "$token" | sed 's/\\/\\\\/g; s/"/\\"/g')
    if [[ -n "$MISSING_EVIDENCE" ]]; then MISSING_EVIDENCE+=", "; fi
    MISSING_EVIDENCE+="\"Missing token: $escaped_token_json\""
  fi
done < "$DECLARED_TOKENS_FILE"

# Build evidence
EVIDENCE="[\"Scanned ${#DESIGN_FILES[@]} design document(s), found $TOKENS_DECLARED declared token(s)\", \"Checked style files in src/, found $TOKENS_FOUND of $TOKENS_DECLARED tokens in code\""
if [[ -n "$MISSING_EVIDENCE" ]]; then
  EVIDENCE+=", $MISSING_EVIDENCE"
fi
EVIDENCE+="]"

if [[ "$TOKENS_MISSING" -eq 0 ]]; then
  write_result "pass" "$EVIDENCE" "$TOKENS_DECLARED" "$TOKENS_FOUND" "$TOKENS_MISSING"
else
  write_result "fail" "$EVIDENCE" "$TOKENS_DECLARED" "$TOKENS_FOUND" "$TOKENS_MISSING"
fi
