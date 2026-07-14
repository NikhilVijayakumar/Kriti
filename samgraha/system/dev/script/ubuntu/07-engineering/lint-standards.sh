#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=""
REPO_FINGERPRINT=""
OUT=""
LINT_COMMAND="npm run lint"

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
  "check": "lint-standards",
  "domain": "07-engineering",
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

CONFIGS=(".eslintrc" ".eslintrc.js" ".eslintrc.json" ".eslintrc.yml" ".pylintrc" ".flake8" "pyproject.toml" ".golangci.yml" ".rubocop.yml" ".stylelintrc")
FOUND_CONFIGS=""
for cfg in "${CONFIGS[@]}"; do
    if [[ -f "$REPO_ROOT/$cfg" ]]; then
        [[ -n "$FOUND_CONFIGS" ]] && FOUND_CONFIGS+=", "
        FOUND_CONFIGS+="$cfg"
    fi
done

set +e
cd "$REPO_ROOT" && eval "$LINT_COMMAND" > /tmp/lint_stdout.txt 2> /tmp/lint_stderr.txt
LINT_EXIT=$?
set -e

LINT_OUTPUT=""
[[ -f /tmp/lint_stdout.txt ]] && LINT_OUTPUT=$(cat /tmp/lint_stdout.txt)
[[ -f /tmp/lint_stderr.txt ]] && LINT_OUTPUT+=$(cat /tmp/lint_stderr.txt)

LINT_ERRORS=$(echo "$LINT_OUTPUT" | grep -cE "(error|Error|ERROR|problems|Problems)" 2>/dev/null || echo "0")

EVIDENCE=""
if [[ -n "$FOUND_CONFIGS" ]]; then
    EVIDENCE="[\"Lint configs found: $FOUND_CONFIGS\"]"
else
    EVIDENCE="[\"No lint config found (checked: ${CONFIGS[*]})\"]"
fi

if [[ $LINT_EXIT -eq 0 ]]; then
    EVIDENCE="${EVIDENCE%]}, \"Lint passed\"]"
    EVIDENCE=$(echo "$EVIDENCE" | sed 's/\]\], \[/], [/' 2>/dev/null || echo "[\"Lint passed\"]")
    EVIDENCE="[\"Lint passed\"]"
    [[ -n "$FOUND_CONFIGS" ]] && EVIDENCE="[\"Lint configs found: $FOUND_CONFIGS\", \"Lint passed\"]"
else
    STDERR=""
    [[ -f /tmp/lint_stderr.txt ]] && STDERR=$(tail -10 /tmp/lint_stderr.txt)
    if [[ -n "$STDERR" ]]; then
        while IFS= read -r line; do
            [[ -n "$line" ]] && EVIDENCE="${EVIDENCE%]}\", \"stderr: $(echo "$line" | sed 's/"/\\"/g')\"]"
        done <<< "$STDERR"
    fi
    if [[ -z "$STDERR" ]]; then
        [[ -n "$FOUND_CONFIGS" ]] && EVIDENCE="[\"Lint configs found: $FOUND_CONFIGS\", \"Lint exited with code $LINT_EXIT\"]"
        [[ -z "$FOUND_CONFIGS" ]] && EVIDENCE="[\"Lint exited with code $LINT_EXIT\"]"
    fi
fi

if [[ $LINT_EXIT -eq 0 ]]; then
    write_result "pass" "$EVIDENCE" "$LINT_EXIT" "$LINT_ERRORS"
else
    write_result "fail" "$EVIDENCE" "$LINT_EXIT" "$LINT_ERRORS"
fi
