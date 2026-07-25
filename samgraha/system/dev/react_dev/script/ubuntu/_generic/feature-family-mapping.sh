#!/usr/bin/env bash
set -euo pipefail

# feature-family-mapping — Category C generic script
# Checks that every Feature has a corresponding Feature-Design and Feature-Technical,
# no orphaned Feature-Technical without a parent Feature, and IDs/names line up.

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
  echo '{"check":"feature-family-mapping","domain":"_generic","category":"C","status":"error","metrics":{"features_count":0,"feature_designs_count":0,"feature_technicals_count":0,"valid_mappings":0,"orphans":0},"evidence":["docs-root not found: '"$DOCS_ROOT"'"],"executed_at":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","repo_fingerprint":"'"$FINGERPRINT"'"}' > "$OUT"
  exit 1
fi

EXECUTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Collect feature families by extracting the name part after the domain prefix
# e.g., "04-feature-cloudbridge.md" → family "cloudbridge"
# e.g., "04-feature.md" → family "" (untitled, base feature doc)

declare -A FEATURES=()
declare -A FEATURE_DESIGNS=()
declare -A FEATURE_TECHNICALS=()

# Find Feature documents (04-feature*)
while IFS= read -r f; do
  basename="$(basename "$f" .md)"
  # Extract family name: strip "04-feature-" prefix, or "" if no suffix
  family="${basename#04-feature-}"
  if [[ "$family" == "$basename" ]]; then
    # No suffix — this is the base "04-feature.md"
    family=""
  fi
  FEATURES[$family]="$f"
done < <(find "$DOCS_ROOT" -maxdepth 1 -name '04-feature*' -name '*.md' -type f 2>/dev/null)

# Find Feature-Design documents (09-feature-design*)
while IFS= read -r f; do
  basename="$(basename "$f" .md)"
  family="${basename#09-feature-design-}"
  if [[ "$family" == "$basename" ]]; then
    family=""
  fi
  FEATURE_DESIGNS[$family]="$f"
done < <(find "$DOCS_ROOT" -maxdepth 1 -name '09-feature-design*' -name '*.md' -type f 2>/dev/null)

# Find Feature-Technical documents (10-feature-technical*)
while IFS= read -r f; do
  basename="$(basename "$f" .md)"
  family="${basename#10-feature-technical-}"
  if [[ "$family" == "$basename" ]]; then
    family=""
  fi
  FEATURE_TECHNICALS[$family]="$f"
done < <(find "$DOCS_ROOT" -maxdepth 1 -name '10-feature-technical*' -name '*.md' -type f 2>/dev/null)

FEATURES_COUNT=${#FEATURES[@]}
FEATURE_DESIGNS_COUNT=${#FEATURE_DESIGNS[@]}
FEATURE_TECHNICALS_COUNT=${#FEATURE_TECHNICALS[@]}
VALID_MAPPINGS=0
ORPHANS=0
EVIDENCE=()

# Check: every Feature should have a Feature-Design and Feature-Technical
for family in "${!FEATURES[@]}"; do
  label="${family:-<untitled>}"
  has_design=0
  has_technical=0

  if [[ -n "${FEATURE_DESIGNS[$family]+x}" ]]; then
    has_design=1
  fi
  if [[ -n "${FEATURE_TECHNICALS[$family]+x}" ]]; then
    has_technical=1
  fi

  if [[ "$has_design" -eq 1 && "$has_technical" -eq 1 ]]; then
    VALID_MAPPINGS=$((VALID_MAPPINGS + 1))
  else
    ORPHANS=$((ORPHANS + 1))
    missing=""
    [[ "$has_design" -eq 0 ]] && missing="Feature-Design"
    [[ "$has_technical" -eq 0 ]] && { [[ -n "$missing" ]] && missing+=", "; missing+="Feature-Technical"; }
    EVIDENCE+=("Feature '$label' is missing: $missing")
  fi
done

# Check: every Feature-Technical should have a parent Feature
for family in "${!FEATURE_TECHNICALS[@]}"; do
  label="${family:-<untitled>}"
  if [[ -z "${FEATURES[$family]+x}" ]]; then
    ORPHANS=$((ORPHANS + 1))
    EVIDENCE+=("Feature-Technical '$label' has no parent Feature")
  fi
done

# Check: every Feature-Design should have a parent Feature (bonus, not strictly required by proposal)
for family in "${!FEATURE_DESIGNS[@]}"; do
  label="${family:-<untitled>}"
  if [[ -z "${FEATURES[$family]+x}" ]]; then
    ORPHANS=$((ORPHANS + 1))
    EVIDENCE+=("Feature-Design '$label' has no parent Feature")
  fi
done

# Determine status
TOTAL=$((FEATURES_COUNT + FEATURE_DESIGNS_COUNT + FEATURE_TECHNICALS_COUNT))
if [[ "$TOTAL" -eq 0 ]]; then
  STATUS="not_applicable"
  EVIDENCE=("No Feature/Feature-Design/Feature-Technical documents found in docs-root")
elif [[ "$ORPHANS" -gt 0 ]]; then
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
  escaped="$(echo "${EVIDENCE[$i]}" | sed 's/\\/\\\\/g; s/"/\\"/g')"
  EVIDENCE_JSON+="\"$escaped\""
done
EVIDENCE_JSON+="]"

# Write output
cat > "$OUT" <<ENDJSON
{
  "check": "feature-family-mapping",
  "domain": "_generic",
  "category": "C",
  "status": "$STATUS",
  "metrics": {
    "features_count": $FEATURES_COUNT,
    "feature_designs_count": $FEATURE_DESIGNS_COUNT,
    "feature_technicals_count": $FEATURE_TECHNICALS_COUNT,
    "valid_mappings": $VALID_MAPPINGS,
    "orphans": $ORPHANS
  },
  "evidence": $EVIDENCE_JSON,
  "executed_at": "$EXECUTED_AT",
  "repo_fingerprint": "$FINGERPRINT"
}
ENDJSON
