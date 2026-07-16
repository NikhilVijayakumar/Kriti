#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=""
REPO_FINGERPRINT=""
OUT=""
DOCS_ROOT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo-root) REPO_ROOT="$2"; shift 2 ;;
        --repo-fingerprint) REPO_FINGERPRINT="$2"; shift 2 ;;
        --out) OUT="$2"; shift 2 ;;
        --docs-root) DOCS_ROOT="$2"; shift 2 ;;
        *) echo "Unknown arg: $1" >&2; exit 2 ;;
    esac
done

EXECUTED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

write_result() {
    local status="$1"
    local evidence="$2"
    local declared="$3"
    local actual="$4"
    local mismatches="$5"
    cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$REPO_FINGERPRINT",
  "check": "public-contract-diff",
  "domain": "16-product-guide",
  "category": "A",
  "status": "$status",
  "metrics": {
    "declared_endpoints": $declared,
    "actual_endpoints": $actual,
    "mismatches": $mismatches
  },
  "evidence": $evidence,
  "executed_at": "$EXECUTED_AT"
}
ENDJSON
    if [[ "$status" == "error" ]]; then exit 1; fi
    exit 0
}

if [[ ! -d "$REPO_ROOT" ]]; then
    write_result "error" '["Cannot access repo-root: '"$REPO_ROOT"'"]' 0 0 0
fi

if [[ -z "$DOCS_ROOT" ]]; then
    if [[ -d "$REPO_ROOT/docs" ]]; then
        DOCS_ROOT="$REPO_ROOT/docs"
    else
        DOCS_ROOT="$REPO_ROOT"
    fi
fi

DECLARED_EPS=""
while IFS= read -r -d '' file; do
    found=$(grep -oE "(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+/[\w/{}\-\.]+" "$file" 2>/dev/null || true)
    [[ -n "$found" ]] && DECLARED_EPS+=$'\n'"$found"
    found=$(grep -oE "(get|post|put|patch|delete)\s*\(\s*['\"](/[\w/{}\-\.]+)" "$file" 2>/dev/null || true)
    [[ -n "$found" ]] && DECLARED_EPS+=$'\n'"$found"
done < <(find "$DOCS_ROOT" -type f \( -name "*.md" -o -name "*.txt" -o -name "*.rst" -o -name "*.html" -o -name "*.yaml" -o -name "*.yml" \) -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/__pycache__/*" -not -path "*/.venv/*" -print0 2>/dev/null)

ACTUAL_EPS=""
while IFS= read -r -d '' file; do
    found=$(grep -oE "(app|router|server)\.(get|post|put|patch|delete|use)\s*\(\s*['\"](/[\w/{}\-\.]+)" "$file" 2>/dev/null || true)
    [[ -n "$found" ]] && ACTUAL_EPS+=$'\n'"$found"
    found=$(grep -oE "@(app|router)\.(get|post|put|patch|delete)\s*\(\s*['\"](/[\w/{}\-\.]+)" "$file" 2>/dev/null || true)
    [[ -n "$found" ]] && ACTUAL_EPS+=$'\n'"$found"
done < <(find "$REPO_ROOT" -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.java" -o -name "*.cs" -o -name "*.rb" \) -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/__pycache__/*" -not -path "*/.venv/*" -not -path "*/dist/*" -not -path "*/build/*" -not -path "*/vendor/*" -not -path "*/.opencode/*" -print0 2>/dev/null)

UNIQUE_DECLARED=$(echo "$DECLARED_EPS" | grep -v '^$' | sed 's/^[[:space:]]*//' | sort -u || true)
UNIQUE_ACTUAL=$(echo "$ACTUAL_EPS" | grep -v '^$' | sed 's/^[[:space:]]*//' | sort -u || true)

DECLARED_COUNT=$(echo "$UNIQUE_DECLARED" | grep -c . 2>/dev/null || echo "0")
ACTUAL_COUNT=$(echo "$UNIQUE_ACTUAL" | grep -c . 2>/dev/null || echo "0")

MISMATCHES=0
MISMATCH_DETAILS=""

while IFS= read -r dep; do
    [[ -z "$dep" ]] && continue
    dep_path=$(echo "$dep" | grep -oE "/[\w/{}\-\.]+" | head -1 || true)
    found=false
    while IFS= read -r act; do
        [[ -z "$act" ]] && continue
        act_path=$(echo "$act" | grep -oE "/[\w/{}\-\.]+" | head -1 || true)
        if [[ "$dep_path" == "$act_path" || "$dep" == "$act" ]]; then
            found=true
            break
        fi
    done <<< "$UNIQUE_ACTUAL"
    if [[ "$found" == false ]]; then
        MISMATCHES=$((MISMATCHES + 1))
        [[ -n "$MISMATCH_DETAILS" ]] && MISMATCH_DETAILS+=", "
        MISMATCH_DETAILS+="\"Documented but not in code: $dep\""
    fi
done <<< "$UNIQUE_DECLARED"

EVIDENCE="[\"Declared endpoints: $DECLARED_COUNT, Actual: $ACTUAL_COUNT, Mismatches: $MISMATCHES\"]"
[[ -n "$MISMATCH_DETAILS" ]] && EVIDENCE="[\"Declared: $DECLARED_COUNT, Actual: $ACTUAL_COUNT, Mismatches: $MISMATCHES\", $MISMATCH_DETAILS]"

if [[ $MISMATCHES -eq 0 ]]; then
    write_result "pass" "$EVIDENCE" "$DECLARED_COUNT" "$ACTUAL_COUNT" 0
else
    write_result "fail" "$EVIDENCE" "$DECLARED_COUNT" "$ACTUAL_COUNT" "$MISMATCHES"
fi
