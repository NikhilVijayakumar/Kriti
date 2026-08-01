#!/usr/bin/env bash
set -euo pipefail

# integration-points-exist -- Category B cross-domain script
# Checks if integration points declared in Feature-Technical docs actually exist in code.

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
  local points_declared="$3"
  local points_found="$4"
  local points_missing="$5"
  cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$FINGERPRINT",
  "check": "integration-points-exist",
  "domain": "10-feature-technical",
  "category": "B",
  "status": "$status",
  "metrics": {
    "points_declared": $points_declared,
    "points_found": $points_found,
    "points_missing": $points_missing
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

# Find feature-technical documents
FEATURE_FILES=()
while IFS= read -r -d '' f; do
  FEATURE_FILES+=("$f")
done < <(find "$DOCS_ROOT" -name '*.md' -type f -print0 2>/dev/null | while IFS= read -r -d '' f; do
  basename="$(basename "$f")"
  if echo "$basename" | grep -qE '^(10-)?feature-technical'; then
    printf '%s\0' "$f"
  fi
done)

if [[ ${#FEATURE_FILES[@]} -eq 0 ]]; then
  write_result "not_applicable" '["No feature-technical documents found in docs-root"]' 0 0 0
fi

# Extract integration points from code blocks in markdown
DECLARED_POINTS_FILE="$(mktemp)"
trap 'rm -f "$DECLARED_POINTS_FILE"' EXIT

for ff in "${FEATURE_FILES[@]}"; do
  # Extract from code blocks (content between ``` markers)
  awk '/^```/{inside=!inside; next} inside' "$ff" 2>/dev/null | \
    grep -oEi 'import\s+(\{[^}]+\}|[a-zA-Z_][a-zA-Z0-9_]*)\s+from\s+["\x27][^"\x27]+["\x27]' | \
    grep -oEi '["\x27][^"\x27]+["\x27]' | tr -d '"'"'" >> "$DECLARED_POINTS_FILE" 2>/dev/null || true

  awk '/^```/{inside=!inside; next} inside' "$ff" 2>/dev/null | \
    grep -oEi 'require\s*\(\s*["\x27][^"\x27]+["\x27]' | \
    grep -oEi '["\x27][^"\x27]+["\x27]' | tr -d '"'"'" >> "$DECLARED_POINTS_FILE" 2>/dev/null || true

  awk '/^```/{inside=!inside; next} inside' "$ff" 2>/dev/null | \
    grep -oEi '(function|class)\s+[A-Z][a-zA-Z0-9_]+' | \
    awk '{print $2}' >> "$DECLARED_POINTS_FILE" 2>/dev/null || true

  # Extract from prose
  grep -oEi '(imports?|api|database|connects?\s+to)\s+[`"'"'"'][a-zA-Z][a-zA-Z0-9./_-]+[`"'"'"']' "$ff" 2>/dev/null | \
    grep -oEi '[`"'"'"'][a-zA-Z][a-zA-Z0-9./_-]+[`"'"'"']' | tr -d '`"'"'"' >> "$DECLARED_POINTS_FILE" 2>/dev/null || true
done

# Deduplicate and filter
grep -v '^$' "$DECLARED_POINTS_FILE" 2>/dev/null | \
  grep -vE '^[0-9]' | \
  sort -u > "${DECLARED_POINTS_FILE}.uniq" || true
mv "${DECLARED_POINTS_FILE}.uniq" "$DECLARED_POINTS_FILE" 2>/dev/null || true

POINTS_DECLARED=$(wc -l < "$DECLARED_POINTS_FILE" | tr -d ' ')

if [[ "$POINTS_DECLARED" -eq 0 ]]; then
  write_result "not_applicable" '["No integration points found in feature-technical documents"]' 0 0 0
fi

# Collect all source code from src/
SRC_CONTENT_FILE="$(mktemp)"
trap 'rm -f "$DECLARED_POINTS_FILE" "$SRC_CONTENT_FILE"' EXIT

SRC_DIR="$REPO_ROOT/src"
if [[ -d "$SRC_DIR" ]]; then
  find "$SRC_DIR" -type f \( -name '*.rs' -o -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx' -o -name '*.py' -o -name '*.go' -o -name '*.java' -o -name '*.cs' \) -print0 2>/dev/null | xargs -0 cat >> "$SRC_CONTENT_FILE" 2>/dev/null || true
fi

POINTS_FOUND=0
POINTS_MISSING=0
MISSING_EVIDENCE=""

while IFS= read -r point; do
  if [[ -z "$point" ]]; then continue; fi
  escaped_point=$(echo "$point" | sed 's/[.[\*^$()+?{|]/\\&/g')
  short_name="$(basename "$point")"
  escaped_short=$(echo "$short_name" | sed 's/[.[\*^$()+?{|]/\\&/g')

  if grep -qE "$escaped_point" "$SRC_CONTENT_FILE" 2>/dev/null || \
     grep -qE "$escaped_short" "$SRC_CONTENT_FILE" 2>/dev/null; then
    POINTS_FOUND=$((POINTS_FOUND + 1))
  else
    POINTS_MISSING=$((POINTS_MISSING + 1))
    escaped_point_json=$(echo "$point" | sed 's/\\/\\\\/g; s/"/\\"/g')
    if [[ -n "$MISSING_EVIDENCE" ]]; then MISSING_EVIDENCE+=", "; fi
    MISSING_EVIDENCE+="\"Missing integration point: $escaped_point_json\""
  fi
done < "$DECLARED_POINTS_FILE"

# Build evidence
EVIDENCE="[\"Scanned ${#FEATURE_FILES[@]} feature-technical document(s), found $POINTS_DECLARED declared integration point(s)\", \"Checked code in src/, found $POINTS_FOUND of $POINTS_DECLARED points\""
if [[ -n "$MISSING_EVIDENCE" ]]; then
  EVIDENCE+=", $MISSING_EVIDENCE"
fi
EVIDENCE+="]"

if [[ "$POINTS_MISSING" -eq 0 ]]; then
  write_result "pass" "$EVIDENCE" "$POINTS_DECLARED" "$POINTS_FOUND" "$POINTS_MISSING"
else
  write_result "fail" "$EVIDENCE" "$POINTS_DECLARED" "$POINTS_FOUND" "$POINTS_MISSING"
fi
