#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=""
REPO_FINGERPRINT=""
OUT=""
SOURCE_INCLUDE="*.ts:*.js:*.py:*.go:*.rs:*.java:*.cs"
SOURCE_EXCLUDE="*.test.*:*.spec.*:*.min.*:node_modules:vendor:__pycache__:dist:build"
TEST_INCLUDE="*.test.*:*.spec.*:*_test.*:test_*.py:tests_*.py"
THRESHOLD=80

while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo-root) REPO_ROOT="$2"; shift 2 ;;
        --repo-fingerprint) REPO_FINGERPRINT="$2"; shift 2 ;;
        --out) OUT="$2"; shift 2 ;;
        --source-include) SOURCE_INCLUDE="$2"; shift 2 ;;
        --source-exclude) SOURCE_EXCLUDE="$2"; shift 2 ;;
        --test-include) TEST_INCLUDE="$2"; shift 2 ;;
        --threshold) THRESHOLD="$2"; shift 2 ;;
        *) echo "Unknown arg: $1" >&2; exit 2 ;;
    esac
done

EXECUTED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

write_result() {
    local status="$1"
    shift
    local evidence="$1"
    shift
    local source_files="$1"
    local tested_files="$1"
    local coverage_pct="$1"
    cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$REPO_FINGERPRINT",
  "check": "unit-test-coverage",
  "domain": "12-qa",
  "category": "A",
  "status": "$status",
  "metrics": {
    "source_files": $source_files,
    "tested_files": $tested_files,
    "coverage_percent": $coverage_pct
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

IFS=':' read -ra SRC_PATTERNS <<< "$SOURCE_INCLUDE"
IFS=':' read -ra EXCL_PATTERNS <<< "$SOURCE_EXCLUDE"
IFS=':' read -ra TST_PATTERNS <<< "$TEST_INCLUDE"

source_count=0
tested_count=0
untested=()

while IFS= read -r -d '' file; do
    excluded=false
    for excl in "${EXCL_PATTERNS[@]}"; do
        if [[ "$file" == *"$excl"* ]]; then excluded=true; break; fi
    done
    [[ "$excluded" == true ]] && continue

    is_source=false
    for pat in "${SRC_PATTERNS[@]}"; do
        if [[ "$(basename "$file")" == $pat ]]; then is_source=true; break; fi
    done
    [[ "$is_source" == false ]] && continue

    source_count=$((source_count + 1))
    base=$(basename "$file")
    base_no_ext="${base%.*}"
    dir=$(dirname "$file")
    has_test=false
    while IFS= read -r -d '' testfile; do
        if [[ "$(dirname "$testfile")" == "$dir" && "$(basename "$testfile")" == *"$base_no_ext"* ]]; then
            has_test=true
            break
        fi
    done < <(find "$REPO_ROOT" -type f \( $(printf -- "-name %s -o " "${TST_PATTERNS[@]}" | sed 's/ -o $//') ) \) -print0 2>/dev/null)

    if [[ "$has_test" == true ]]; then
        tested_count=$((tested_count + 1))
    else
        rel="${file#$REPO_ROOT/}"
        untested+=("$rel")
    fi
done < <(find "$REPO_ROOT" -type f \( $(printf -- "-name %s -o " "${SRC_PATTERNS[@]}" | sed 's/ -o $//') ) \) -print0 2>/dev/null)

if [[ $source_count -eq 0 ]]; then
    write_result "not_applicable" '["No source files found matching patterns: '"$SOURCE_INCLUDE"'"]' 0 0 0
fi

coverage_pct=$(awk "BEGIN { printf \"%.1f\", ($tested_count / $source_count) * 100 }")

evidence="[]"
if (( $(echo "$coverage_pct < $THRESHOLD" | bc -l) )); then
    evidence="[\"Coverage ${coverage_pct}% is below threshold ${THRESHOLD}%\""
    count=0
    for f in "${untested[@]}"; do
        count=$((count + 1))
        [[ $count -le 20 ]] && evidence+=", \"  No test: $f\""
    done
    [[ ${#untested[@]} -gt 20 ]] && evidence+=", \"  ... and $((${#untested[@]} - 20)) more untested files\""
    evidence+="]"
fi

if (( $(echo "$coverage_pct >= $THRESHOLD" | bc -l) )); then
    write_result "pass" "$evidence" "$source_count" "$tested_count" "$coverage_pct"
else
    write_result "fail" "$evidence" "$source_count" "$tested_count" "$coverage_pct"
fi
