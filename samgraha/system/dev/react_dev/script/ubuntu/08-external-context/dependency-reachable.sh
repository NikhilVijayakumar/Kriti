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
    local checked="$3"
    local reachable="$4"
    cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$REPO_FINGERPRINT",
  "check": "dependency-reachable",
  "domain": "08-external-context",
  "category": "A",
  "status": "$status",
  "metrics": {
    "dependencies_checked": $checked,
    "dependencies_reachable": $reachable
  },
  "evidence": $evidence,
  "executed_at": "$EXECUTED_AT"
}
ENDJSON
    if [[ "$status" == "error" ]]; then exit 1; fi
    exit 0
}

if [[ ! -d "$REPO_ROOT" ]]; then
    write_result "error" '["Cannot access repo-root: '"$REPO_ROOT"'"]' 0 0
fi

if [[ -z "$DOCS_ROOT" ]]; then
    if [[ -d "$REPO_ROOT/docs" ]]; then
        DOCS_ROOT="$REPO_ROOT/docs"
    else
        DOCS_ROOT="$REPO_ROOT"
    fi
fi

URLS=""
while IFS= read -r -d '' file; do
    found=$(grep -oE "https?://[^\s\"'\)>\\]]+" "$file" 2>/dev/null | sed 's/[.,;:)]*$//' || true)
    [[ -n "$found" ]] && URLS+=$'\n'"$found"
done < <(find "$DOCS_ROOT" -type f \( -name "*.md" -o -name "*.txt" -o -name "*.rst" -o -name "*.html" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" \) -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/__pycache__/*" -not -path "*/.venv/*" -print0 2>/dev/null)

UNIQUE_URLS=$(echo "$URLS" | grep -v '^$' | sort -u || true)
CHECKED=0
REACHABLE=0
UNREACHABLE=""

if [[ -z "$UNIQUE_URLS" ]]; then
    write_result "not_applicable" '["No URLs found in docs"]' 0 0
fi

while IFS= read -r url; do
    [[ -z "$url" ]] && continue
    CHECKED=$((CHECKED + 1))
    HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}" --head --max-time 10 --max-redirs 5 "$url" 2>/dev/null || echo "000")
    if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 400 ]]; then
        REACHABLE=$((REACHABLE + 1))
    else
        [[ -n "$UNREACHABLE" ]] && UNREACHABLE+=", "
        UNREACHABLE+="\"$url (HTTP $HTTP_CODE)\""
    fi
done <<< "$UNIQUE_URLS"

EVIDENCE="[\"Checked $CHECKED unique URLs, $REACHABLE reachable\"]"
[[ -n "$UNREACHABLE" ]] && EVIDENCE="[\"Checked $CHECKED URLs, $REACHABLE reachable\", $UNREACHABLE]"

if [[ "$CHECKED" -eq 0 ]]; then
    write_result "not_applicable" '["No URLs found in docs"]' 0 0
fi

if [[ -z "$UNREACHABLE" ]]; then
    write_result "pass" "$EVIDENCE" "$CHECKED" "$REACHABLE"
else
    write_result "fail" "$EVIDENCE" "$CHECKED" "$REACHABLE"
fi
