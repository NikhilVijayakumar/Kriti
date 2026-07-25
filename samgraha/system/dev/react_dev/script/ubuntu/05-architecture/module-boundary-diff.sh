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
    local declared="$3"
    local actual="$4"
    local violations="$5"
    cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$REPO_FINGERPRINT",
  "check": "module-boundary-diff",
  "domain": "05-architecture",
  "category": "A",
  "status": "$status",
  "metrics": {
    "declared_modules": $declared,
    "actual_modules": $actual,
    "boundary_violations": $violations
  },
  "evidence": $evidence,
  "executed_at": "$EXECUTED_AT"
}
ENDJSON
    if [[ "$status" == "error" ]]; then exit 1; fi
    exit 0
}

if [[ ! -d "$REPO_ROOT" ]]; then
    write_result "error" '["Cannot access repo-root: '"$REPO_ROOT"'"]' 0 0 0
fi

SOURCE=""
DECLARED_MODULES=()

if [[ -f "$REPO_ROOT/structure.yaml" ]]; then
    SOURCE="structure.yaml"
    while IFS= read -r line; do
        trimmed=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        [[ "$trimmed" =~ ^# ]] && continue
        [[ -z "$trimmed" ]] && continue
        dir=$(echo "$trimmed" | sed 's/^- //;s/\/$//')
        [[ -n "$dir" ]] && DECLARED_MODULES+=("$dir")
    done < "$REPO_ROOT/structure.yaml"
elif [[ -f "$REPO_ROOT/package.json" ]]; then
    SOURCE="package.json workspaces"
    while IFS= read -r ws; do
        [[ -n "$ws" ]] && DECLARED_MODULES+=("$ws")
    done < <(python3 -c "
import json
with open('$REPO_ROOT/package.json') as f:
    d = json.load(f)
for w in d.get('workspaces', []):
    print(w)
" 2>/dev/null)
fi

if [[ ${#DECLARED_MODULES[@]} -eq 0 ]]; then
    write_result "not_applicable" '["No module declarations found (no structure.yaml or package.json workspaces)"]' 0 0 0
fi

ACTUAL_DIRS=()
while IFS= read -r -d '' dir; do
    rel="${dir#$REPO_ROOT/}"
    ACTUAL_DIRS+=("$rel")
done < <(find "$REPO_ROOT" -maxdepth 1 -type d -not -path "$REPO_ROOT" -not -path "*/node_modules" -not -path "*/.git" -not -path "*/__pycache__" -not -path "*/.venv" -not -path "*/dist" -not -path "*/build" -not -path "*/.opencode" -not -path "*/vendor" -print0 2>/dev/null)

VIOLATIONS=0
VIOLATION_DETAILS=""

for mod in "${DECLARED_MODULES[@]}"; do
    mod_dir="$REPO_ROOT/$mod"
    [[ ! -d "$mod_dir" ]] && continue
    while IFS= read -r -d '' file; do
        content=$(cat "$file" 2>/dev/null || true)
        [[ -z "$content" ]] && continue
        for other in "${DECLARED_MODULES[@]}"; do
            [[ "$other" == "$mod" ]] && continue
            if echo "$content" | grep -qE "(require|import|from).*['\"]$other" 2>/dev/null; then
                rel="${file#"$REPO_ROOT"/}"
                VIOLATIONS=$((VIOLATIONS + 1))
                [[ -n "$VIOLATION_DETAILS" ]] && VIOLATION_DETAILS+=", "
                VIOLATION_DETAILS+="\"$rel imports from $other (boundary violation)\""
            fi
        done
    done < <(find "$mod_dir" -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.java" -o -name "*.cs" \) -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/__pycache__/*" -not -path "*/vendor/*" -print0 2>/dev/null)
done

evidence="[\"Declared modules: ${#DECLARED_MODULES[@]} (source: $SOURCE), Actual top-level dirs: ${#ACTUAL_DIRS[@]}\"]"
if [[ $VIOLATIONS -gt 0 ]]; then
    evidence="[\"Declared modules: ${#DECLARED_MODULES[@]}, Actual: ${#ACTUAL_DIRS[@]}, Violations: $VIOLATIONS\", $VIOLATION_DETAILS]"
    write_result "fail" "$evidence" "${#DECLARED_MODULES[@]}" "${#ACTUAL_DIRS[@]}" "$VIOLATIONS"
else
    evidence="[\"Declared modules: ${#DECLARED_MODULES[@]}, Actual: ${#ACTUAL_DIRS[@]}, No boundary violations\"]"
    write_result "pass" "$evidence" "${#DECLARED_MODULES[@]}" "${#ACTUAL_DIRS[@]}" 0
fi
