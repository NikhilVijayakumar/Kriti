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
    local exists="$3"
    local count="$4"
    cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$REPO_FINGERPRINT",
  "check": "dependency-manifest",
  "domain": "13-implementation",
  "category": "A",
  "status": "$status",
  "metrics": {
    "manifest_exists": $exists,
    "dependency_count": $count
  },
  "evidence": $evidence,
  "executed_at": "$EXECUTED_AT"
}
ENDJSON
    if [[ "$status" == "error" ]]; then exit 1; fi
    exit 0
}

if [[ ! -d "$REPO_ROOT" ]]; then
    write_result "error" '["Cannot access repo-root: '"$REPO_ROOT"'"]' false 0
fi

manifest_files=("package.json:npm" "requirements.txt:pip" "Pipfile:pipenv" "pyproject.toml:python" "go.mod:go" "Cargo.toml:cargo" "pom.xml:maven" "build.gradle:gradle" "Gemfile:bundler" "composer.json:composer")

found_type=""
for entry in "${manifest_files[@]}"; do
    IFS=':' read -r name type <<< "$entry"
    if [[ -f "$REPO_ROOT/$name" ]]; then
        found_type="$type"
        found_name="$name"
        break
    fi
done

if [[ -z "$found_type" ]]; then
    names=""
    for entry in "${manifest_files[@]}"; do
        IFS=':' read -r name type <<< "$entry"
        [[ -n "$names" ]] && names+=", "
        names+="$name"
    done
    write_result "not_applicable" '["No dependency manifest found (checked: '"$names"')"]' false 0
fi

dep_count=0
evidence="[]"

case "$found_type" in
    npm)
        dep_count=$(cat "$REPO_ROOT/$found_name" | python3 -c "import sys,json; d=json.load(sys.stdin); deps=d.get('dependencies',{}); devdeps=d.get('devDependencies',{}); print(len(deps)+len(devdeps))" 2>/dev/null || echo 0)
        evidence='["Found '"$found_name"' with '"$dep_count"' dependencies"]'
        ;;
    pip)
        dep_count=$(grep -cE '^[a-zA-Z]' "$REPO_ROOT/$found_name" 2>/dev/null || echo 0)
        evidence='["Found '"$found_name"' with '"$dep_count"' dependencies"]'
        ;;
    go)
        dep_count=$(grep -cE '^\t' "$REPO_ROOT/$found_name" 2>/dev/null || echo 0)
        evidence='["Found '"$found_name"' with '"$dep_count"' dependencies"]'
        ;;
    *)
        evidence='["Found '"$found_name"' (type: '"$found_type"') — dependency count not parsed"]'
        ;;
esac

write_result "pass" "$evidence" true "$dep_count"
