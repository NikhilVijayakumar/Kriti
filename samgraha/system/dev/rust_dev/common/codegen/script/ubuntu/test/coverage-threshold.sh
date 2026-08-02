#!/usr/bin/env bash
set -euo pipefail

# coverage-threshold: measures line coverage with cargo-tarpaulin and reports
# pass/fail against the crate's configured threshold. qa.md leaves the concrete
# number and measurement tool project-specific; the tool is named here only as
# this check's implementation detail, not as generation policy (see
# test/profile-default/unit.yaml, which keeps the tool a per-crate [Tool] slot).
# Same fixed contract as tier5's lint-pass.sh: result envelope written to --out.

REPO_ROOT=""
REPO_FINGERPRINT=""
OUT=""
THRESHOLD=80

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-root) REPO_ROOT="$2"; shift 2 ;;
    --repo-fingerprint) REPO_FINGERPRINT="$2"; shift 2 ;;
    --out) OUT="$2"; shift 2 ;;
    --threshold) THRESHOLD="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$REPO_ROOT" || -z "$REPO_FINGERPRINT" || -z "$OUT" ]]; then
  echo "Usage: $0 --repo-root <path> --repo-fingerprint <value> --out <path> [--threshold <pct>]" >&2
  exit 2
fi

EXECUTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

write_result() {
  local status="$1" evidence="$2" metrics="$3"
  cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$REPO_FINGERPRINT",
  "check": "coverage-threshold",
  "domain": "codegen.test",
  "category": "A",
  "status": "$status",
  "metrics": $metrics,
  "evidence": $evidence,
  "executed_at": "$EXECUTED_AT"
}
ENDJSON
  if [[ "$status" == "error" ]]; then exit 1; fi
  exit 0
}

ERROR_METRICS='{"line_coverage_pct":null,"threshold_pct":'"$THRESHOLD"',"files_measured":0}'

if [[ ! -d "$REPO_ROOT" ]]; then
  write_result "error" '["Cannot access repo-root: '"$REPO_ROOT"'"]' "$ERROR_METRICS"
fi

if ! command -v cargo-tarpaulin >/dev/null 2>&1; then
  write_result "error" '["cargo-tarpaulin not installed (cargo install cargo-tarpaulin)"]' "$ERROR_METRICS"
fi

set +e
pushd "$REPO_ROOT" >/dev/null
raw="$(cargo tarpaulin --out Json 2>/dev/null)"
tarpaulin_exit=$?
popd >/dev/null
set -e

if [[ -z "$raw" ]]; then
  for candidate in tarpaulin-report.json coverage.json; do
    if [[ -f "$REPO_ROOT/$candidate" ]]; then
      raw="$(cat "$REPO_ROOT/$candidate")"
      break
    fi
  done
fi

if [[ $tarpaulin_exit -ne 0 && -z "$raw" ]]; then
  write_result "error" '["cargo tarpaulin exited with code '"$tarpaulin_exit"'"]' "$ERROR_METRICS"
fi

if [[ -z "$raw" ]]; then
  write_result "error" '["cargo tarpaulin produced no JSON output"]' "$ERROR_METRICS"
fi

# aggregate line coverage: tarpaulin's top-level "coverage":"NN.N" string,
# else compute covered/total lines across files[].coverage arrays.
# NOTE: no `head` and every pipeline is `|| true`-guarded — under `set -euo
# pipefail` a closed pipe (SIGPIPE) or a no-match grep would otherwise kill the
# script before write_result can run.
COV="$(printf '%s' "$raw" | grep -oE '"coverage"[[:space:]]*:[[:space:]]*"[0-9]+(\.[0-9]+)?"' | grep -oE '[0-9]+(\.[0-9]+)?' || true)"
COV="${COV%%$'\n'*}"

if [[ -z "$COV" ]]; then
  COV="$(printf '%s' "$raw" | awk '
    /"coverage"[[:space:]]*:[[:space:]]*\[/ {
      in_arr = 1
      line = $0
      sub(/^.*\[/, "", line)
      while (line ~ /[0-9.]/) {
        if (match(line, /[0-9.]+/)) {
          v = substr(line, RSTART, RLENGTH)
          total++
          if (v + 0 > 0) covered++
          line = substr(line, RSTART + RLENGTH)
        }
      }
      if (line ~ /\]/) in_arr = 0
      next
    }
    in_arr {
      line = $0
      while (line ~ /[0-9.]/) {
        if (match(line, /[0-9.]+/)) {
          v = substr(line, RSTART, RLENGTH)
          total++
          if (v + 0 > 0) covered++
          line = substr(line, RSTART + RLENGTH)
        }
      }
      if ($0 ~ /\]/) in_arr = 0
    }
    END { if (total > 0) printf "%.2f\n", covered * 100 / total }
  ')"
fi

if [[ -z "$COV" ]]; then
  write_result "error" '["tarpaulin returned no line coverage data"]' "$ERROR_METRICS"
fi

FILES_MEASURED="$(printf '%s' "$raw" | grep -oE '"name"[[:space:]]*:' | wc -l | tr -d ' ' || true)"

METRICS_JSON="{\"line_coverage_pct\":$COV,\"threshold_pct\":$THRESHOLD,\"files_measured\":$FILES_MEASURED}"

if awk -v c="$COV" -v t="$THRESHOLD" 'BEGIN { exit !(c + 0 >= t + 0) }'; then
  write_result "pass" '["Line coverage '"$COV"'% meets threshold '"$THRESHOLD"'%"]' "$METRICS_JSON"
else
  write_result "fail" '["Line coverage '"$COV"'% is below threshold '"$THRESHOLD"'%"]' "$METRICS_JSON"
fi
