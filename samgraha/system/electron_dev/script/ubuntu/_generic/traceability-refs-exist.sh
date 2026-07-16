#!/usr/bin/env bash
set -euo pipefail

# traceability-refs-exist — Category C generic script
# Checks that every downstream document referenced in a domain's Traceability
# section actually exists in --docs-root.

usage() {
  echo "Usage: $0 --docs-root <path> --repo-fingerprint <value> --out <path>" >&2
  exit 1
}

DOCS_ROOT=""
FINGERPRINT=""
OUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --docs-root) DOCS_ROOT="$2"; shift 2 ;;
    --repo-fingerprint) FINGERPRINT="$2"; shift 2 ;;
    --out) OUT="$2"; shift 2 ;;
    *) usage ;;
  esac
done

if [[ -z "$DOCS_ROOT" || -z "$FINGERPRINT" || -z "$OUT" ]]; then
  usage
fi

if [[ ! -d "$DOCS_ROOT" ]]; then
  echo '{"check":"traceability-refs-exist","domain":"_generic","category":"C","status":"error","metrics":{"domains_checked":0,"refs_found":0,"refs_valid":0,"refs_missing":0},"evidence":["docs-root not found: '"$DOCS_ROOT"'"],"executed_at":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","repo_fingerprint":"'"$FINGERPRINT"'"}' > "$OUT"
  exit 1
fi

EXECUTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DOMAINS_CHECKED=0
REFS_FOUND=0
REFS_VALID=0
REFS_MISSING=0
EVIDENCE=()

# Domain number → name mapping for resolving standard references
declare -A DOMAIN_NUMS=(
  [01]="vision" [02]="philosophy" [03]="security" [04]="feature"
  [05]="architecture" [06]="design" [07]="engineering"
  [08]="external-context" [09]="feature-design" [10]="feature-technical"
  [11]="prototype" [12]="qa" [13]="implementation" [14]="build"
  [15]="readme" [16]="product-guide"
)

find "$DOCS_ROOT" -name '*.md' -type f | while read -r docfile; do
  # Check if file has a Traceability section
  if ! grep -q '^## Traceability' "$docfile" 2>/dev/null; then
    continue
  fi

  DOMAINS_CHECKED=$((DOMAINS_CHECKED + 1))
  docname="$(basename "$docfile" .md)"

  # Extract content between "## Traceability" and the next "##" heading
  in_traceability=0
  traceability_content=""
  while IFS= read -r line; do
    if [[ "$line" == ^##\ * && "$in_traceability" -eq 1 ]]; then
      break
    fi
    if [[ "$line" == ^##\ Traceability ]]; then
      in_traceability=1
      continue
    fi
    if [[ "$in_traceability" -eq 1 ]]; then
      traceability_content+="$line"$'\n'
    fi
  done < "$docfile"

  # Find the Consuming Standards table — look for "| Standard |" header
  in_table=0
  while IFS= read -r line; do
    if echo "$line" | grep -qE '^\|[[:space:]]*Standard[[:space:]]*\|'; then
      in_table=1
      continue
    fi
    if [[ "$in_table" -eq 1 ]]; then
      # Skip separator line
      if echo "$line" | grep -qE '^\|[[:space:]]*-+'; then
        continue
      fi
      # End of table
      if ! echo "$line" | grep -qE '^\|'; then
        break
      fi
      # Extract standard name from first column
      standard="$(echo "$line" | awk -F'|' '{gsub(/^[[:space:]]+|[[:space:]]+$/, "", $2); print $2}')"
      if [[ -z "$standard" ]]; then
        continue
      fi

      # Extract domain number from standard name — expect "(NN)" pattern
      domain_num="$(echo "$standard" | grep -oE '\([0-9]{2}\)' | tr -d '()')"
      if [[ -z "$domain_num" ]]; then
        EVIDENCE+=("$docname: Cannot resolve domain number from standard '$standard'")
        REFS_FOUND=$((REFS_FOUND + 1))
        REFS_MISSING=$((REFS_MISSING + 1))
        continue
      fi

      REFS_FOUND=$((REFS_FOUND + 1))

      # Check if any file in docs-root starts with this domain number
      domain_name="${DOMAIN_NUMS[$domain_num]:-unknown}"
      match_count="$(find "$DOCS_ROOT" -maxdepth 1 -name "${domain_num}-${domain_name}*" -type f 2>/dev/null | wc -l)"
      if [[ "$match_count" -gt 0 ]]; then
        REFS_VALID=$((REFS_VALID + 1))
      else
        REFS_MISSING=$((REFS_MISSING + 1))
        EVIDENCE+=("$docname: Referenced standard '$standard' (domain ${domain_num}-${domain_name}) has no matching document in docs-root")
      fi
    fi
  done <<< "$traceability_content"
done

# Determine status
if [[ "$DOMAINS_CHECKED" -eq 0 ]]; then
  STATUS="not_applicable"
  EVIDENCE=("No domains with Traceability sections found in docs-root")
elif [[ "$REFS_MISSING" -gt 0 ]]; then
  STATUS="fail"
else
  STATUS="pass"
fi

# Build evidence JSON array
EVIDENCE_JSON="["
for i in "${!EVIDENCE[@]}"; do
  if [[ $i -gt 0 ]]; then
    EVIDENCE_JSON+=","
  fi
  # Escape double quotes and backslashes in evidence strings
  escaped="$(echo "${EVIDENCE[$i]}" | sed 's/\\/\\\\/g; s/"/\\"/g')"
  EVIDENCE_JSON+="\"$escaped\""
done
EVIDENCE_JSON+="]"

# Write output
cat > "$OUT" <<ENDJSON
{
  "check": "traceability-refs-exist",
  "domain": "_generic",
  "category": "C",
  "status": "$STATUS",
  "metrics": {
    "domains_checked": $DOMAINS_CHECKED,
    "refs_found": $REFS_FOUND,
    "refs_valid": $REFS_VALID,
    "refs_missing": $REFS_MISSING
  },
  "evidence": $EVIDENCE_JSON,
  "executed_at": "$EXECUTED_AT",
  "repo_fingerprint": "$FINGERPRINT"
}
ENDJSON
