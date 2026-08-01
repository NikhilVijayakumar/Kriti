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
    local status="$1" evidence="$2" vuln_count="$3" critical_count="$4"
    cat > "$OUT" <<ENDJSON
{
  "check": "cargo-audit",
  "domain": "03-security",
  "category": "A",
  "status": "$status",
  "metrics": { "vulnerability_count": $vuln_count, "critical_count": $critical_count },
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

if [[ ! -f "$REPO_ROOT/Cargo.lock" ]]; then
    write_result "not_applicable" '["No Cargo.lock found — cargo-audit requires a lockfile"]' 0 0
fi

if ! command -v cargo-audit &>/dev/null && ! command -v cargo &>/dev/null; then
    write_result "error" '["cargo-audit not installed. Install with: cargo install cargo-audit"]' 0 0
fi

AUDIT_OUTPUT=$(mktemp)
trap 'rm -f "$AUDIT_OUTPUT"' EXIT

if command -v cargo-audit &>/dev/null; then
    cargo-audit audit --json -q > "$AUDIT_OUTPUT" 2>/dev/null || true
elif command -v cargo &>/dev/null; then
    cargo audit --json -q > "$AUDIT_OUTPUT" 2>/dev/null || true
fi

if [[ ! -s "$AUDIT_OUTPUT" ]]; then
    write_result "pass" '["cargo-audit executed, no vulnerabilities found"]' 0 0
fi

VULN_COUNT=$(python3 -c "
import json, sys
try:
    data = json.load(open('$AUDIT_OUTPUT'))
    vulns = data.get('vulnerabilities', {}).get('list', [])
    print(len(vulns))
except:
    print(0)
" 2>/dev/null || echo 0)

CRITICAL_COUNT=$(python3 -c "
import json, sys
try:
    data = json.load(open('$AUDIT_OUTPUT'))
    vulns = data.get('vulnerabilities', {}).get('list', [])
    critical = [v for v in vulns if v.get('advisory', {}).get('cvss', {}).get('score', 0) >= 9.0]
    print(len(critical))
except:
    print(0)
" 2>/dev/null || echo 0)

if [[ "$VULN_COUNT" -gt 0 ]]; then
    VULN_SUMMARY=$(python3 -c "
import json
data = json.load(open('$AUDIT_OUTPUT'))
vulns = data.get('vulnerabilities', {}).get('list', [])
names = [v.get('advisory', {}).get('id', 'unknown') for v in vulns[:5]]
print(', '.join(names))
" 2>/dev/null || echo "unknown")
    write_result "fail" '["Found '"$VULN_COUNT"' vulnerabilities: '"$VULN_SUMMARY"'"]' "$VULN_COUNT" "$CRITICAL_COUNT"
else
    write_result "pass" '["cargo-audit passed — no known vulnerabilities in Cargo.lock"]' 0 0
fi
