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
    local vulns="$3"
    local deps="$4"
    cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$REPO_FINGERPRINT",
  "check": "dependency-vuln-scan",
  "domain": "03-security",
  "category": "A",
  "status": "$status",
  "metrics": {
    "vulnerabilities_found": $vulns,
    "dependencies_scanned": $deps
  },
  "evidence": $evidence,
  "executed_at": "$EXECUTED_AT"
}
ENDJSON
    if [[ "$status" == "error" ]]; then exit 1; fi
    exit 0
}

if [[ ! -d "$REPO_ROOT" ]]; then
    write_result "error" '["Cannot access repo-root: '"$REPO_ROOT"'"]' 0 0
fi

VULNS=0
DEPS=0
EVIDENCE=""

if [[ -f "$REPO_ROOT/package.json" ]]; then
    AUDIT_OUTPUT=$(cd "$REPO_ROOT" && npm audit --json 2>/dev/null || true)
    if [[ -n "$AUDIT_OUTPUT" ]]; then
        VULNS=$(echo "$AUDIT_OUTPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    v = d.get('metadata',{}).get('vulnerabilities',{})
    total = sum(v.values())
    print(total)
except: print(0)
" 2>/dev/null || echo "0")
        DEPS=$(echo "$AUDIT_OUTPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('metadata',{}).get('totalDependencies',0))
except: print(0)
" 2>/dev/null || echo "0")
        EVIDENCE="[\"npm audit: $VULNS vulnerabilities in $DEPS dependencies\"]"
    fi
fi

if [[ "$VULNS" -eq 0 && "$DEPS" -eq 0 ]]; then
    if [[ -f "$REPO_ROOT/requirements.txt" ]]; then
        DEPS=$(grep -cE "^[a-zA-Z]" "$REPO_ROOT/requirements.txt" 2>/dev/null || echo "0")
        EVIDENCE="[\"Found requirements.txt with $DEPS dependencies (npm audit unavailable)\"]"
    elif [[ -f "$REPO_ROOT/package.json" ]]; then
        DEPS=$(python3 -c "
import json
with open('$REPO_ROOT/package.json') as f:
    d = json.load(f)
deps = d.get('dependencies',{})
dev = d.get('devDependencies',{})
print(len(deps) + len(dev))
" 2>/dev/null || echo "0")
        EVIDENCE="[\"Found package.json with $DEPS dependencies (npm audit unavailable)\"]"
    fi
fi

if [[ "$DEPS" -eq 0 && -z "$EVIDENCE" ]]; then
    write_result "not_applicable" '["No dependency manifests found to scan"]' 0 0
fi

[[ -z "$EVIDENCE" ]] && EVIDENCE="[\"Scanned $DEPS dependencies\"]"

if [[ "$VULNS" -eq 0 ]]; then
    write_result "pass" "$EVIDENCE" "$VULNS" "$DEPS"
else
    write_result "fail" "$EVIDENCE" "$VULNS" "$DEPS"
fi
