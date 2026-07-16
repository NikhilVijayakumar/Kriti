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
    local status="$1" evidence="$2" has_cycles="$3" violations="$4"
    cat > "$OUT" <<ENDJSON
{
  "check": "crate-dependency-graph",
  "domain": "05-architecture",
  "category": "A",
  "status": "$status",
  "metrics": { "has_cycles": $has_cycles, "violation_count": $violations },
  "evidence": $evidence,
  "executed_at": "$EXECUTED_AT",
  "repo_fingerprint": "$REPO_FINGERPRINT"
}
ENDJSON
    if [[ "$status" == "error" ]]; then exit 1; fi
    exit 0
}

if [[ ! -d "$REPO_ROOT" ]]; then
    write_result "error" '["Cannot access repo-root: '"$REPO_ROOT"'"]' false 0
fi

if [[ ! -f "$REPO_ROOT/Cargo.toml" ]]; then
    write_result "not_applicable" '["No Cargo.toml found — not a Rust workspace"]' false 0
fi

if ! command -v cargo &>/dev/null; then
    write_result "error" '["cargo not installed"]' false 0
fi

META_OUTPUT=$(mktemp)
trap 'rm -f "$META_OUTPUT"' EXIT

set +e
cargo metadata --format-version 1 --no-deps > "$META_OUTPUT" 2>/dev/null
META_EXIT=$?
set -e
if [[ $META_EXIT -ne 0 ]]; then
    write_result "error" '["cargo metadata failed — ensure Cargo.toml is valid"]' false 0
fi

python3 -c "
import json, sys

with open('$META_OUTPUT') as f:
    data = json.load(f)

packages = {p['name']: p for p in data.get('packages', [])}
workspace_members = set(data.get('workspace_members', []))

# Build adjacency list for workspace crates only
graph = {}
for pkg_name, pkg in packages.items():
    if pkg['manifest_path'] not in workspace_members:
        continue
    deps = []
    for dep in pkg.get('dependencies', []):
        if dep['name'] in packages and packages[dep['name']]['manifest_path'] in workspace_members:
            deps.append(dep['name'])
    graph[pkg_name] = deps

# Detect cycles using DFS
WHITE, GRAY, BLACK = 0, 1, 2
color = {n: WHITE for n in graph}
cycles = []

def dfs(node, path):
    color[node] = GRAY
    path.append(node)
    for neighbor in graph.get(node, []):
        if neighbor in color:
            if color[neighbor] == GRAY:
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
            elif color[neighbor] == WHITE:
                dfs(neighbor, path)
    path.pop()
    color[node] = BLACK

for node in graph:
    if color[node] == WHITE:
        dfs(node, [])

has_cycles = len(cycles) > 0

# Check direction violations (business-logic depending on infrastructural)
infra_crates = set()
for name in graph:
    lower = name.lower()
    if any(kw in lower for kw in ['infra', 'util', 'common', 'shared', 'internal']):
        infra_crates.add(name)

violations = []
for pkg, deps in graph.items():
    if pkg not in infra_crates:
        for dep in deps:
            if dep in infra_crates:
                violations.append(f'{pkg} -> {dep}')

result = {
    'has_cycles': has_cycles,
    'cycle_count': len(cycles),
    'cycle_details': [c for c in cycles],
    'violation_count': len(violations),
    'violations': violations,
    'total_crates': len(graph)
}
print(json.dumps(result))
" > "${META_OUTPUT}.result" 2>/dev/null

HAS_CYCLES=$(python3 -c "import json; d=json.load(open('${META_OUTPUT}.result')); print('true' if d['has_cycles'] else 'false')" 2>/dev/null || echo "false")
VIOLATION_COUNT=$(python3 -c "import json; d=json.load(open('${META_OUTPUT}.result')); print(d['violation_count'])" 2>/dev/null || echo 0)
CYCLE_COUNT=$(python3 -c "import json; d=json.load(open('${META_OUTPUT}.result')); print(d['cycle_count'])" 2>/dev/null || echo 0)
TOTAL_CRATES=$(python3 -c "import json; d=json.load(open('${META_OUTPUT}.result')); print(d['total_crates'])" 2>/dev/null || echo 0)

VIOLATION_DETAILS=$(python3 -c "import json; d=json.load(open('${META_OUTPUT}.result')); vs=d.get('violations',[]); print(', '.join(vs[:5]))" 2>/dev/null || echo "")
CYCLE_DETAILS=$(python3 -c "import json; d=json.load(open('${META_OUTPUT}.result')); cs=d.get('cycle_details',[]); print('; '.join([' -> '.join(c) for c in cs[:3]]))" 2>/dev/null || echo "")

if [[ "$HAS_CYCLES" == "true" ]]; then
    write_result "fail" '["Circular dependency detected: '"$CYCLE_DETAILS"'. Total crates: '"$TOTAL_CRATES"'"]' true "$VIOLATION_COUNT"
elif [[ "$VIOLATION_COUNT" -gt 0 ]]; then
    write_result "fail" '["Dependency direction violations: '"$VIOLATION_DETAILS"'"]' false "$VIOLATION_COUNT"
else
    write_result "pass" '["No circular dependencies. All crate dependencies flow in correct direction. Total crates: '"$TOTAL_CRATES"'"]' false 0
fi
