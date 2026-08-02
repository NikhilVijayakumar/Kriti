#!/usr/bin/env bash
set -euo pipefail

# unsafe-usage-scan: fails when an `unsafe` block or `unsafe fn`/`unsafe impl`/
# `unsafe trait`/`unsafe extern` item lacks a preceding `// SAFETY:` comment, or
# when `unwrap()`/`expect()` appears outside `#[cfg(test)]`/`#[test]` code —
# per engineering.md's Rust Engineering Practices (Unsafe Code + Error Handling).
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
  "check": "unsafe-usage-scan",
  "domain": "codegen.code",
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

EMPTY_METRICS='{"files_scanned":0,"unsafe_blocks":0,"unsafe_items":0,"unwrap_uses":0,"violations":0}'

if [[ ! -d "$REPO_ROOT" ]]; then
  write_result "error" '["Cannot access repo-root: '"$REPO_ROOT"'"]' "$EMPTY_METRICS"
fi

if ! find "$REPO_ROOT" -type f -name '*.rs' -print -quit 2>/dev/null | grep -q .; then
  write_result "not_applicable" '["No .rs source files found under '"$REPO_ROOT"'"]' "$EMPTY_METRICS"
fi

AWK_PROG='
function esc(s,   r) {
    r = s
    gsub(/\\/, "\\\\", r)
    gsub(/"/, "\\\"", r)
    return r
}
FNR == 1 {
    files_scanned++
    prev_safety = 0
    pending_unsafe = 0
    pending_unsafe_needs = 0
    in_test = 0
    test_depth = 0
    pending_test_attr = 0
}
{
    line = $0
    t = line
    gsub(/^[ \t]+|[ \t]+$/, "", t)
    blank = (t == "")

    x = line; gsub(/{/, "", x); opens = length(line) - length(x)
    y = line; gsub(/}/, "", y); closes = length(line) - length(y)

    if (in_test) {
        test_depth += (opens - closes)
        if (test_depth <= 0) { in_test = 0; test_depth = 0 }
    }

    if (t ~ /^#\[(cfg\(test\)|test)\]/) {
        pending_test_attr = 1
    } else if (pending_test_attr && !blank) {
        if (t ~ /^(mod|fn)[ \t]/) {
            in_test = 1
            test_depth = opens
            pending_test_attr = 0
        } else {
            pending_test_attr = 0
        }
    }

    if (!blank) {
        safety_idx = index(line, "SAFETY:")
        unsafe_idx = index(line, "unsafe")
        safety_before_unsafe = (safety_idx > 0 && unsafe_idx > safety_idx)
        comment_idx = index(line, "//")
        starts_comment = (t ~ /^(\/\/|\/\*)/)

        if (pending_unsafe > 0) {
            if (t ~ /^\{/) {
                blocks++
                if (pending_unsafe_needs) {
                    viols[vcount++] = "\"" esc(FILENAME ":" pending_unsafe ": unsafe block missing a preceding // SAFETY: comment") "\""
                }
            }
            pending_unsafe = 0
        }

        if (!in_test && !starts_comment) {
            unw = index(line, ".unwrap()")
            exp_idx = index(line, ".expect(")
            hit = 0
            if (unw > 0) hit = unw
            if (exp_idx > 0 && (hit == 0 || exp_idx < hit)) hit = exp_idx
            if (hit > 0 && (comment_idx == 0 || hit < comment_idx)) {
                unwraps++
                viols[vcount++] = "\"" esc(FILENAME ":" FNR ": unwrap()/expect() used outside test code") "\""
            }
        }

        if (!starts_comment && line ~ /unsafe[ \t]*\{/) {
            blocks++
            if (!prev_safety && !safety_before_unsafe) {
                viols[vcount++] = "\"" esc(FILENAME ":" FNR ": unsafe block missing a preceding // SAFETY: comment") "\""
            }
        }

        if (!starts_comment && (line ~ /(^|[ \t])unsafe[ \t]+(fn|impl|trait|extern)[ \t(]/ || line ~ /(^|[ \t])unsafe[ \t]+(fn|impl|trait|extern)[ \t]*$/)) {
            items++
            if (!prev_safety && !safety_before_unsafe) {
                viols[vcount++] = "\"" esc(FILENAME ":" FNR ": unsafe item missing a preceding // SAFETY: comment") "\""
            }
        }

        if (t ~ /^unsafe$/) {
            pending_unsafe = FNR
            pending_unsafe_needs = (!prev_safety && !safety_before_unsafe)
        }

        if (t ~ /^unsafe/) {
            prev_safety = 0
        } else if (safety_idx > 0) {
            prev_safety = 1
        }
    }
}
END {
    ev = "["
    for (i = 0; i < vcount; i++) {
        if (i > 0) ev = ev ","
        ev = ev viols[i]
    }
    ev = ev "]"
    printf "%d\t%d\t%d\t%d\t%d\t%s\n", files_scanned, blocks, items, unwraps, vcount, ev
}
'

scan_out="$(find "$REPO_ROOT" \( -path '*/target' -o -path '*/.git' \) -prune -o -type f -name '*.rs' -exec awk "$AWK_PROG" {} + 2>/dev/null || true)"

if [[ -z "$scan_out" ]]; then
  write_result "error" '["unsafe-usage-scan failed: scanner produced no output"]' "$EMPTY_METRICS"
fi

IFS=$'\t' read -r FILES_SCANNED BLOCKS ITEMS UNWRAPS VCOUNT EVJSON <<< "$scan_out"

if [[ "$VCOUNT" -gt 0 ]]; then
  STATUS="fail"
else
  STATUS="pass"
fi

METRICS_JSON="{\"files_scanned\":$FILES_SCANNED,\"unsafe_blocks\":$BLOCKS,\"unsafe_items\":$ITEMS,\"unwrap_uses\":$UNWRAPS,\"violations\":$VCOUNT}"
write_result "$STATUS" "$EVJSON" "$METRICS_JSON"
