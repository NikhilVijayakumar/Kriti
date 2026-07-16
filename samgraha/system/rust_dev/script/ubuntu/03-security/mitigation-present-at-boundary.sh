#!/usr/bin/env bash
set -euo pipefail

# mitigation-present-at-boundary -- Category B cross-domain script
# Checks if security mitigations declared in the Security doc actually appear at claimed code boundaries.

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
  local mitigations_declared="$3"
  local mitigations_found="$4"
  local mitigations_missing="$5"
  cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$FINGERPRINT",
  "check": "mitigation-present-at-boundary",
  "domain": "03-security",
  "category": "B",
  "status": "$status",
  "metrics": {
    "mitigations_declared": $mitigations_declared,
    "mitigations_found": $mitigations_found,
    "mitigations_missing": $mitigations_missing
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

# Find security documents
SECURITY_FILES=()
while IFS= read -r -d '' f; do
  SECURITY_FILES+=("$f")
done < <(find "$DOCS_ROOT" -name '*.md' -type f -print0 2>/dev/null | while IFS= read -r -d '' f; do
  basename="$(basename "$f")"
  if echo "$basename" | grep -qE '^(03-)?security'; then
    printf '%s\0' "$f"
  fi
done)

if [[ ${#SECURITY_FILES[@]} -eq 0 ]]; then
  write_result "not_applicable" '["No security documents found in docs-root"]' 0 0 0
fi

# Concatenate all security doc content
ALL_CONTENT_FILE="$(mktemp)"
trap 'rm -f "$ALL_CONTENT_FILE"' EXIT

for sf in "${SECURITY_FILES[@]}"; do
  cat "$sf" >> "$ALL_CONTENT_FILE" 2>/dev/null || true
done

# Check which mitigation types are declared in the docs
declare -A DECLARED=()
declare -A MITIGATION_GREPS=(
  [input_sanitization]='sanitiz'
  [output_escaping]='escap'
  [input_validation]='validat'
  [authentication]='authenticat'
  [authorization]='authoriz'
  [encryption]='encrypt'
  [hashing]='\bhash'
  [rate_limiting]='rate.limit'
  [csrf_protection]='csrf\|xsrf\|cross.site.request'
  [xss_protection]='[Xx][Ss][Ss]\|cross.site.script'
)

MITIGATION_LABELS=(
  "input sanitization"
  "output escaping"
  "input validation"
  "authentication"
  "authorization"
  "encryption"
  "hashing"
  "rate limiting"
  "CSRF protection"
  "XSS protection"
)

MITIGATION_KEYS=(
  "input_sanitization"
  "output_escaping"
  "input_validation"
  "authentication"
  "authorization"
  "encryption"
  "hashing"
  "rate_limiting"
  "csrf_protection"
  "xss_protection"
)

for i in "${!MITIGATION_KEYS[@]}"; do
  key="${MITIGATION_KEYS[$i]}"
  pattern="${MITIGATION_GREPS[$key]}"
  if grep -qiE "$pattern" "$ALL_CONTENT_FILE" 2>/dev/null; then
    DECLARED["$key"]=1
  fi
done

if [[ ${#DECLARED[@]} -eq 0 ]]; then
  write_result "not_applicable" '["No security mitigations found in security documents"]' 0 0 0
fi

# Collect source code
SRC_CONTENT_FILE="$(mktemp)"
trap 'rm -f "$ALL_CONTENT_FILE" "$SRC_CONTENT_FILE"' EXIT

SRC_DIR="$REPO_ROOT/src"
if [[ -d "$SRC_DIR" ]]; then
  find "$SRC_DIR" -type f \( -name '*.rs' -o -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx' -o -name '*.py' -o -name '*.go' -o -name '*.java' -o -name '*.cs' \) -print0 2>/dev/null | xargs -0 cat >> "$SRC_CONTENT_FILE" 2>/dev/null || true
fi

# Check each declared mitigation against source code
FOUND_COUNT=0
MISSING_COUNT=0
MISSING_EVIDENCE=""

for i in "${!MITIGATION_KEYS[@]}"; do
  key="${MITIGATION_KEYS[$i]}"
  label="${MITIGATION_LABELS[$i]}"
  pattern="${MITIGATION_GREPS[$key]}"

  if [[ -z "${DECLARED[$key]+_}" ]]; then
    continue
  fi

  if grep -qiE "$pattern" "$SRC_CONTENT_FILE" 2>/dev/null; then
    FOUND_COUNT=$((FOUND_COUNT + 1))
  else
    MISSING_COUNT=$((MISSING_COUNT + 1))
    if [[ -n "$MISSING_EVIDENCE" ]]; then MISSING_EVIDENCE+=", "; fi
    MISSING_EVIDENCE+="\"Missing mitigation: $label\""
  fi
done

TOTAL=${#DECLARED[@]}

# Build evidence
EVIDENCE="[\"Scanned ${#SECURITY_FILES[@]} security document(s), found $TOTAL declared mitigation type(s)\", \"Checked code in src/, found $FOUND_COUNT of $TOTAL mitigations\""
if [[ -n "$MISSING_EVIDENCE" ]]; then
  EVIDENCE+=", $MISSING_EVIDENCE"
fi
EVIDENCE+="]"

if [[ "$MISSING_COUNT" -eq 0 ]]; then
  write_result "pass" "$EVIDENCE" "$TOTAL" "$FOUND_COUNT" "$MISSING_COUNT"
else
  write_result "fail" "$EVIDENCE" "$TOTAL" "$FOUND_COUNT" "$MISSING_COUNT"
fi
