#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=""
REPO_FINGERPRINT=""
OUT=""
ARTIFACT_PATH="dist"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo-root) REPO_ROOT="$2"; shift 2 ;;
        --repo-fingerprint) REPO_FINGERPRINT="$2"; shift 2 ;;
        --out) OUT="$2"; shift 2 ;;
        --artifact-path) ARTIFACT_PATH="$2"; shift 2 ;;
        *) echo "Unknown arg: $1" >&2; exit 2 ;;
    esac
done

EXECUTED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

write_result() {
    local status="$1"
    local evidence="$2"
    local exists="$3"
    cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$REPO_FINGERPRINT",
  "check": "artifact-exists",
  "domain": "14-build",
  "category": "A",
  "status": "$status",
  "metrics": {
    "artifact_path": "$ARTIFACT_PATH",
    "artifact_exists": $exists
  },
  "evidence": $evidence,
  "executed_at": "$EXECUTED_AT"
}
ENDJSON
    if [[ "$status" == "error" ]]; then exit 1; fi
    exit 0
}

if [[ ! -d "$REPO_ROOT" ]]; then
    write_result "error" '["Cannot access repo-root: '"$REPO_ROOT"'"]' false
fi

full_path="$REPO_ROOT/$ARTIFACT_PATH"

if [[ -e "$full_path" ]]; then
    if [[ -d "$full_path" ]]; then
        file_count=$(find "$full_path" -type f | wc -l)
        write_result "pass" '["Artifact found at '"$ARTIFACT_PATH"'", "Directory contains '"$file_count"' files"]' true
    else
        size=$(du -k "$full_path" | cut -f1)
        write_result "pass" '["Artifact found at '"$ARTIFACT_PATH"'", "File size: '"$size"'KB"]' true
    fi
else
    write_result "fail" '["Artifact not found at '"$ARTIFACT_PATH"'"]' false
fi
