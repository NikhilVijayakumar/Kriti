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
    local status="$1" evidence="$2" unformatted="$3" total_violations="$4"
    cat > "$OUT" <<ENDJSON
{
  "check": "cargo-fmt",
  "domain": "07-engineering",
  "category": "A",
  "status": "$status",
  "metrics": { "unformatted_files": $unformatted, "total_violations": $total_violations },
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

if [[ ! -f "$REPO_ROOT/Cargo.toml" ]]; then
    write_result "not_applicable" '["No Cargo.toml found — not a Rust project"]' 0 0
fi

if ! command -v cargo &>/dev/null; then
    write_result "error" '["cargo not installed — cannot run cargo fmt"]' 0 0
fi

FMT_OUTPUT=$(mktemp)
trap 'rm -f "$FMT_OUTPUT"' EXIT

set +e
cargo fmt --all -- --check > "$FMT_OUTPUT" 2>&1
FMT_EXIT=$?
set -e

if [[ $FMT_EXIT -eq 0 ]]; then
    write_result "pass" '["All Rust source files are properly formatted (cargo fmt)"]' 0 0
fi

UNFORMATTED_COUNT=$(grep -c "^Diff" "$FMT_OUTPUT" 2>/dev/null || echo 0)
TOTAL_LINES=$(wc -l < "$FMT_OUTPUT" 2>/dev/null || echo 0)

UNFORMATTED_FILES=$(grep "^Diff" "$FMT_OUTPUT" 2>/dev/null | sed 's/^Diff in //' | head -10 | while read f; do echo "$f"; done | tr '\n' ', ')
UNFORMATTED_FILES="${UNFORMATTED_FILES%, }"

write_result "fail" '["'"$UNFORMATTED_COUNT"' file(s) need formatting. Run: cargo fmt --all. Files: '"$UNFORMATTED_FILES"'"]' "$UNFORMATTED_COUNT" "$TOTAL_LINES"
