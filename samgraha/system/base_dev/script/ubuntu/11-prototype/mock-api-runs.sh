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
    local status="$1"
    local evidence="$2"
    local server_started="$3"
    local endpoints_tested="$4"
    local endpoints_passed="$5"
    cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$REPO_FINGERPRINT",
  "check": "mock-api-runs",
  "domain": "11-prototype",
  "category": "A",
  "status": "$status",
  "metrics": {
    "server_started": $server_started,
    "endpoints_tested": $endpoints_tested,
    "endpoints_passed": $endpoints_passed
  },
  "evidence": $evidence,
  "executed_at": "$EXECUTED_AT"
}
ENDJSON
    if [[ "$status" == "error" ]]; then exit 1; fi
    exit 0
}

if [[ ! -d "$REPO_ROOT" ]]; then
    write_result "error" '["Cannot access repo-root: '"$REPO_ROOT"'"]' false 0 0
fi

MOCK_CONFIGS=("mock-server.js" "mockapi.config.js" "mock-server.ts" "mock-server.py" "mock_routes.json")
CONFIG_FILE=""

for cfg in "${MOCK_CONFIGS[@]}"; do
    if [[ -f "$REPO_ROOT/$cfg" ]]; then
        CONFIG_FILE="$cfg"
        break
    fi
done

if [[ -z "$CONFIG_FILE" ]]; then
    CONFIG_FILE=$(find "$REPO_ROOT" -type f -name "mock*server*" -o -name "mock*api*" -o -name "mock*route*" 2>/dev/null | grep -v node_modules | grep -v .git | head -1 || true)
    if [[ -n "$CONFIG_FILE" ]]; then
        CONFIG_FILE=$(basename "$CONFIG_FILE")
    fi
fi

if [[ -z "$CONFIG_FILE" ]]; then
    write_result "not_applicable" '["No mock server config found"]' false 0 0
fi

TEST_PORT=3099
SERVER_STARTED=false
ENDPOINTS_TESTED=0
ENDPOINTS_PASSED=0
MOCK_PID=""

cleanup() {
    if [[ -n "$MOCK_PID" ]] && kill -0 "$MOCK_PID" 2>/dev/null; then
        kill "$MOCK_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT

if [[ "$CONFIG_FILE" == *.py ]]; then
    cd "$REPO_ROOT" && python3 "$CONFIG_FILE" &
else
    cd "$REPO_ROOT" && node "$CONFIG_FILE" &
fi
MOCK_PID=$!
sleep 3

if ! kill -0 "$MOCK_PID" 2>/dev/null; then
    write_result "fail" '["Mock server exited immediately"]' false 0 0
fi

SERVER_STARTED=true

HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}" --max-time 5 "http://localhost:$TEST_PORT/" 2>/dev/null || echo "000")
ENDPOINTS_TESTED=1
if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 400 ]]; then
    ENDPOINTS_PASSED=1
fi

if [[ "$SERVER_STARTED" == true && "$ENDPOINTS_PASSED" -gt 0 ]]; then
    write_result "pass" "[\"Mock server started on port $TEST_PORT using $CONFIG_FILE\"]" true "$ENDPOINTS_TESTED" "$ENDPOINTS_PASSED"
else
    write_result "fail" '[\"Mock server started but no endpoints responded\"]' true "$ENDPOINTS_TESTED" "$ENDPOINTS_PASSED"
fi
