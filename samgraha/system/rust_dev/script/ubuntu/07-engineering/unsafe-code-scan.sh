#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=""
REPO_FINGERPRINT=""
OUT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo-root) REPO_ROOT="$2"; shift 2 ;;
        --repo-fingerprint) REPO_FINGERPRINT="$2"; shift 2 ;;
        --out) OUT="$2"; shift 2 ;;
        *) echo "Unknown arg: $1" >&2; exit 2 ;;
    esac
done

EXECUTED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

write_result() {
    local status="$1" evidence="$2" unsafe_blocks="$3" crates_without_forbid="$4"
    cat > "$OUT" <<ENDJSON
{
  "check": "unsafe-code-scan",
  "domain": "07-engineering",
  "category": "A",
  "status": "$status",
  "metrics": { "unsafe_blocks_found": $unsafe_blocks, "crates_without_forbid": $crates_without_forbid },
  "evidence": $evidence,
  "executed_at": "$EXECUTED_AT",
  "repo_fingerprint": "$REPO_FINGERPRINT"
}
ENDJSON
    if [[ "$status" == "error" ]]; then exit 1; fi
    exit 0
}

if [[ ! -d "$REPO_ROOT" ]]; then
    write_result "error" '["Cannot access repo-root: '"$REPO_ROOT"'"]' 0 0
fi

SRC_DIR="$REPO_ROOT/src"
CRATE_ROOTS_DIR="$REPO_ROOT"

if [[ ! -d "$SRC_DIR" ]]; then
    write_result "not_applicable" '["No src/ directory found"]' 0 0
fi

# Count unsafe blocks across all .rs files
UNSAFE_COUNT=0
UNSAFE_FILES=""
if command -v rg &>/dev/null; then
    UNSAFE_COUNT=$(rg -c 'unsafe\s*\{' --include='*.rs' "$SRC_DIR" 2>/dev/null | awk -F: '{s+=$2} END {print s+0}')
    UNSAFE_FILES=$(rg -l 'unsafe\s*\{' --include='*.rs' "$SRC_DIR" 2>/dev/null | head -10 | while read f; do echo "${f#$REPO_ROOT/}"; done | tr '\n' ', ')
elif command -v grep &>/dev/null; then
    UNSAFE_COUNT=$(grep -r 'unsafe\s*{' --include='*.rs' "$SRC_DIR" 2>/dev/null | wc -l || echo 0)
    UNSAFE_FILES=$(grep -rl 'unsafe\s*{' --include='*.rs' "$SRC_DIR" 2>/dev/null | head -10 | while read f; do echo "${f#$REPO_ROOT/}"; done | tr '\n' ', ')
fi

# Check for #![forbid(unsafe_code)] or #![deny(unsafe_code)] at crate roots
CRATES_WITHOUT_FORBID=0
CRATE_ROOT_LIST=""

# Find all lib.rs and main.rs files (crate roots)
while IFS= read -r crate_root; do
    if [[ -f "$crate_root" ]]; then
        if ! grep -q '#!\[forbid(unsafe_code)\]\|#!\[deny(unsafe_code)\]' "$crate_root" 2>/dev/null; then
            CRATES_WITHOUT_FORBID=$((CRATES_WITHOUT_FORBID + 1))
            REL_PATH="${crate_root#$REPO_ROOT/}"
            CRATE_ROOT_LIST+="$REL_PATH, "
        fi
    fi
done < <(find "$CRATE_ROOTS_DIR" -name "lib.rs" -o -name "main.rs" 2>/dev/null)

# Strip trailing comma
CRATE_ROOT_LIST="${CRATE_ROOT_LIST%, }"

if [[ "$UNSAFE_COUNT" -gt 0 && "$CRATES_WITHOUT_FORBID" -gt 0 ]]; then
    write_result "fail" '["Found '"$UNSAFE_COUNT"' unsafe blocks in source; '"$CRATES_WITHOUT_FORBID"' crate(s) missing forbid(unsafe_code): '"$CRATE_ROOT_LIST"'"]' "$UNSAFE_COUNT" "$CRATES_WITHOUT_FORBID"
elif [[ "$UNSAFE_COUNT" -gt 0 ]]; then
    write_result "pass" '["Found '"$UNSAFE_COUNT"' unsafe blocks but all crate roots have forbid(unsafe_code)"]' "$UNSAFE_COUNT" 0
else
    write_result "pass" '["No unsafe blocks found in source code"]' 0 0
fi
