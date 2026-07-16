#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=""
REPO_FINGERPRINT=""
OUT=""
SCAN_INCLUDE="*.ts;*.js;*.py;*.go;*.java;*.cs;*.env;*.yml;*.yaml;*.json;*.toml;*.xml;*.config;*.cfg;*.ini;*.properties"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo-root) REPO_ROOT="$2"; shift 2 ;;
        --repo-fingerprint) REPO_FINGERPRINT="$2"; shift 2 ;;
        --out) OUT="$2"; shift 2 ;;
        --scan-include) SCAN_INCLUDE="$2"; shift 2 ;;
        *) echo "Unknown arg: $1" >&2; exit 2 ;;
    esac
done

EXECUTED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

write_result() {
    local status="$1"
    local evidence="$2"
    local secrets_found="$3"
    local files_scanned="$4"
    cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$REPO_FINGERPRINT",
  "check": "secret-scan",
  "domain": "03-security",
  "category": "A",
  "status": "$status",
  "metrics": {
    "secrets_found": $secrets_found,
    "files_scanned": $files_scanned
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

PATTERNS=(
    "AKIA[0-9A-Z]{16}"
    "-----BEGIN.*PRIVATE KEY-----"
    "(?i)password\s*[:=]\s*[\"'][^\"']+[\"']"
    "(?i)api[_-]?key\s*[:=]\s*[\"'][^\"']+[\"']"
    "(?i)token\s*[:=]\s*[\"'][^\"']+[\"']"
    "(?i)secret\s*[:=]\s*[\"'][^\"']+[\"']"
)
PATTERN_NAMES=(
    "AWS Key"
    "Private Key"
    "Password Assignment"
    "API Key Assignment"
    "Token Assignment"
    "Secret Assignment"
)

EXCLUDE_DIRS="node_modules|\.git|__pycache__|\.venv|dist|build|\.opencode|vendor"
FILES_SCANNED=0
SECRETS_FOUND=0
FINDINGS=""
IFS=';' read -ra INCLUDE_PATTERNS <<< "$SCAN_INCLUDE"

for pattern in "${INCLUDE_PATTERNS[@]}"; do
    pattern=$(echo "$pattern" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    while IFS= read -r -d '' file; do
        FILES_SCANNED=$((FILES_SCANNED + 1))
        for i in "${!PATTERNS[@]}"; do
            matches=$(grep -cE "${PATTERNS[$i]}" "$file" 2>/dev/null || true)
            if [[ "$matches" -gt 0 ]]; then
                rel="${file#"$REPO_ROOT"/}"
                SECRETS_FOUND=$((SECRETS_FOUND + matches))
                if [[ -n "$FINDINGS" ]]; then FINDINGS+=", "; fi
                FINDINGS+="\"${PATTERN_NAMES[$i]} in $rel\""
            fi
        done
    done < <(find "$REPO_ROOT" -type f -name "$pattern" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/__pycache__/*" -not -path "*/.venv/*" -not -path "*/dist/*" -not -path "*/build/*" -not -path "*/.opencode/*" -not -path "*/vendor/*" -print0 2>/dev/null)
done

if [[ $SECRETS_FOUND -eq 0 ]]; then
    evidence="[\"No secrets found in $FILES_SCANNED files\"]"
    write_result "pass" "$evidence" "$SECRETS_FOUND" "$FILES_SCANNED"
else
    evidence="[\"Found $SECRETS_FOUND potential secrets in $FILES_SCANNED files\", $FINDINGS]"
    write_result "fail" "$evidence" "$SECRETS_FOUND" "$FILES_SCANNED"
fi
