#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=""
REPO_FINGERPRINT=""
OUT=""
BUILD_COMMAND="npm run build"
TIMEOUT_SECONDS=600

while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo-root) REPO_ROOT="$2"; shift 2 ;;
        --repo-fingerprint) REPO_FINGERPRINT="$2"; shift 2 ;;
        --out) OUT="$2"; shift 2 ;;
        --build-command) BUILD_COMMAND="$2"; shift 2 ;;
        --timeout) TIMEOUT_SECONDS="$2"; shift 2 ;;
        *) echo "Unknown arg: $1" >&2; exit 2 ;;
    esac
done

EXECUTED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

write_result() {
    local status="$1"
    local evidence="$2"
    local exit_code="$3"
    local duration="$4"
    cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$REPO_FINGERPRINT",
  "check": "build-succeeds",
  "domain": "14-build",
  "category": "A",
  "status": "$status",
  "metrics": {
    "build_exit_code": $exit_code,
    "build_duration_seconds": $duration
  },
  "evidence": $evidence,
  "executed_at": "$EXECUTED_AT"
}
ENDJSON
    if [[ "$status" == "error" ]]; then exit 1; fi
    exit 0
}

if [[ ! -d "$REPO_ROOT" ]]; then
    write_result "error" '["Cannot access repo-root: '"$REPO_ROOT"'"]' -1 0
fi

start_time=$(date +%s)
set +e
timeout "$TIMEOUT_SECONDS" bash -c "cd \"$REPO_ROOT\" && $BUILD_COMMAND" > /tmp/build_stdout.txt 2> /tmp/build_stderr.txt
exit_code=$?
set -e
end_time=$(date +%s)
duration=$((end_time - start_time))

if [[ $exit_code -eq 124 ]]; then
    write_result "error" '["Build timed out after '"$TIMEOUT_SECONDS"'s"]' -1 "$duration"
fi

stderr=""
if [[ -f /tmp/build_stderr.txt ]]; then
    stderr=$(tail -10 /tmp/build_stderr.txt)
fi

evidence="[]"
if [[ $exit_code -ne 0 ]]; then
    evidence='["Build command exited with code '"$exit_code"'", "Command: '"$BUILD_COMMAND"'"]'
    if [[ -n "$stderr" ]]; then
        while IFS= read -r line; do
            [[ -n "$line" ]] && evidence=$(echo "$evidence" | sed 's/]$/, "stderr: '"$(echo "$line" | sed 's/"/\\"/g')"'"]/')
        done <<< "$stderr"
    fi
else
    evidence='["Build succeeded in '"$duration"'s"]'
fi

if [[ $exit_code -eq 0 ]]; then
    write_result "pass" "$evidence" "$exit_code" "$duration"
else
    write_result "fail" "$evidence" "$exit_code" "$duration"
fi
