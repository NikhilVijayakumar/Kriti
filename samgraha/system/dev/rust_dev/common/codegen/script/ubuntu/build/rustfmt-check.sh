#!/usr/bin/env bash
set -euo pipefail

# rustfmt-check: first gate in build.md's CI/CD Validation sequence
# (fmt -> clippy -> tests -> ...). `cargo fmt --check` must exit 0.
# Same fixed contract as tier5's lint-pass.sh: result envelope written to --out.

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

if [[ -z "$REPO_ROOT" || -z "$REPO_FINGERPRINT" || -z "$OUT" ]]; then
  echo "Usage: $0 --repo-root <path> --repo-fingerprint <value> --out <path>" >&2
  exit 2
fi

EXECUTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

write_result() {
  local status="$1" evidence="$2" metrics="$3"
  cat > "$OUT" <<ENDJSON
{
  "repo_fingerprint": "$REPO_FINGERPRINT",
  "check": "rustfmt-check",
  "domain": "codegen.build",
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

EMPTY_METRICS='{"fmt_exit_code":null,"diff_excerpt_bytes":0}'

if [[ ! -d "$REPO_ROOT" ]]; then
  write_result "error" '["Cannot access repo-root: '"$REPO_ROOT"'"]' '{"fmt_exit_code":-1,"diff_excerpt_bytes":0}'
fi

if ! command -v cargo >/dev/null 2>&1; then
  write_result "error" '["cargo not installed"]' '{"fmt_exit_code":-1,"diff_excerpt_bytes":0}'
fi

if [[ ! -f "$REPO_ROOT/Cargo.toml" ]]; then
  write_result "not_applicable" '["No Cargo.toml found at '"$REPO_ROOT"'"]' "$EMPTY_METRICS"
fi

LOG_FILE="$(mktemp)"
FMT_EXIT=0
set +e
pushd "$REPO_ROOT" >/dev/null
cargo fmt --check >"$LOG_FILE" 2>&1
FMT_EXIT=$?
popd >/dev/null
set -e

excerpt="$(head -c 2000 "$LOG_FILE")"
bytes="$(wc -c < "$LOG_FILE" | tr -d ' ')"
rm -f "$LOG_FILE"

METRICS_JSON="{\"fmt_exit_code\":$FMT_EXIT,\"diff_excerpt_bytes\":$bytes}"

if [[ $FMT_EXIT -eq 0 ]]; then
  write_result "pass" '["cargo fmt --check passed"]' "$METRICS_JSON"
else
  evidence='["cargo fmt --check failed with exit code '"$FMT_EXIT"'"]'
  if [[ -n "$excerpt" ]]; then
    esc_excerpt="$(printf '%s' "$excerpt" | sed 's/\\/\\\\/g; s/"/\\"/g' | tr '\n' ' ')"
    evidence='["cargo fmt --check failed with exit code '"$FMT_EXIT"'", "'"$esc_excerpt"'"]'
  fi
  write_result "fail" "$evidence" "$METRICS_JSON"
fi
