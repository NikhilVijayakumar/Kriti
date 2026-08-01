#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=""
REPO_FINGERPRINT=""
OUT=""
EXPECTED_STRUCTURE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo-root) REPO_ROOT="$2"; shift 2 ;;
        --repo-fingerprint) REPO_FINGERPRINT="$2"; shift 2 ;;
        --out) OUT="$2"; shift 2 ;;
        --expected-structure) EXPECTED_STRUCTURE="$2"; shift 2 ;;
        *) echo "Unknown arg: $1" >&2; exit 2 ;;
    esac
done

EXECUTED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

write_result() {
    local status="$1"
    local evidence="$2"
    local expected="$3"
    local actual="$4"
    local mismatch="$5"
    cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$REPO_FINGERPRINT",
  "check": "folder-structure",
  "domain": "13-implementation",
  "category": "A",
  "status": "$status",
  "metrics": {
    "expected_count": $expected,
    "actual_count": $actual,
    "mismatch_count": $mismatch
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

if [[ -z "$EXPECTED_STRUCTURE" ]]; then
    if [[ -f "$REPO_ROOT/structure.yaml" ]]; then
        EXPECTED_STRUCTURE=$(cat "$REPO_ROOT/structure.yaml")
    else
        write_result "not_applicable" '["No expected structure provided (pass --expected-structure or create structure.yaml)"]' 0 0 0
    fi
fi

expected_dirs=()
while IFS= read -r line; do
    trimmed=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    [[ "$trimmed" =~ ^# ]] && continue
    [[ -z "$trimmed" ]] && continue
    dir=$(echo "$trimmed" | sed 's/^- //;s/\/$//')
    [[ -n "$dir" ]] && expected_dirs+=("$dir")
done <<< "$EXPECTED_STRUCTURE"

actual_dirs=()
while IFS= read -r -d '' dir; do
    rel="${dir#$REPO_ROOT/}"
    actual_dirs+=("$rel")
done < <(find "$REPO_ROOT" -type d -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/__pycache__/*" -not -path "*/.venv/*" -not -path "*/dist/*" -not -path "*/build/*" -not -path "*/.opencode/*" -print0 2>/dev/null)

mismatches=0
found=0
mismatch_list=""
for expected in "${expected_dirs[@]}"; do
    found_match=false
    for actual in "${actual_dirs[@]}"; do
        if [[ "$actual" == "$expected" || "$actual" == *"$expected"* ]]; then
            found_match=true
            break
        fi
    done
    if [[ "$found_match" == true ]]; then
        found=$((found + 1))
    else
        mismatches=$((mismatches + 1))
        [[ -n "$mismatch_list" ]] && mismatch_list+=", "
        mismatch_list+="\"Missing: $expected\""
    fi
done

evidence="[\"Expected: ${#expected_dirs[@]} directories, Found: ${#actual_dirs[@]} directories, Matches: $found, Mismatches: $mismatches\""
[[ -n "$mismatch_list" ]] && evidence+=", $mismatch_list"
evidence+="]"

if [[ $mismatches -eq 0 ]]; then
    write_result "pass" "$evidence" "${#expected_dirs[@]}" "${#actual_dirs[@]}" 0
else
    write_result "fail" "$evidence" "${#expected_dirs[@]}" "${#actual_dirs[@]}" "$mismatches"
fi
