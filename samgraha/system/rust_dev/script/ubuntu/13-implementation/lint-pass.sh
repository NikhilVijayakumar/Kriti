#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=""
REPO_FINGERPRINT=""
OUT=""
LINT_COMMAND="cargo clippy --all-targets --all-features -- -D warnings"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo-root) REPO_ROOT="$2"; shift 2 ;;
        --repo-fingerprint) REPO_FINGERPRINT="$2"; shift 2 ;;
        --out) OUT="$2"; shift 2 ;;
        --lint-command) LINT_COMMAND="$2"; shift 2 ;;
        *) echo "Unknown arg: $1" >&2; exit 2 ;;
    esac
done

EXECUTED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

write_result() {
    local status="$1"
    local evidence="$2"
    local exit_code="$3"
    local errors="$4"
    cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$REPO_FINGERPRINT",
  "check": "lint-pass",
  "domain": "13-implementation",
  "category": "A",
  "status": "$status",
  "metrics": {
    "lint_exit_code": $exit_code,
    "lint_errors": $errors
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

set +e
cd "$REPO_ROOT" && eval "$LINT_COMMAND" > /tmp/lint_stdout.txt 2> /tmp/lint_stderr.txt
exit_code=$?
set -e

stderr=""
if [[ -f /tmp/lint_stderr.txt ]]; then
    stderr=$(tail -15 /tmp/lint_stderr.txt)
fi

evidence="[]"
if [[ $exit_code -ne 0 ]]; then
    evidence='["Lint command exited with code '"$exit_code"'", "Command: '"$LINT_COMMAND"'"]'
    if [[ -n "$stderr" ]]; then
        while IFS= read -r line; do
            [[ -n "$line" ]] && evidence=$(echo "$evidence" | sed 's/]$/, "lint: '"$(echo "$line" | sed 's/"/\\"/g')"'"]/')
        done <<< "$stderr"
    fi
else
    evidence='["Lint passed"]'
fi

if [[ $exit_code -eq 0 ]]; then
    write_result "pass" "$evidence" "$exit_code" 0
else
    write_result "fail" "$evidence" "$exit_code" 0
fi
