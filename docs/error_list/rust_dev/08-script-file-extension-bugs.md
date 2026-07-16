# rust_dev — Bug Report: Scripts Scan Wrong File Extensions

**Category:** Bugs / Correctness  
**Severity:** CRITICAL  
**Date:** 2026-07-15

---

## Summary

This is a **Rust** system but 6+ scripts in `script/ubuntu/` and `script/windows/` scan for web/JS/Python/Go/Java/C# file extensions. **No script scans for `*.rs` files.** These scripts will either return false negatives (no Rust code found) or false positives (finding nothing and passing vacuously).

---

## Bug 1 — `mitigation-present-at-boundary.sh` — No `*.rs` in Extension List

**File:** `script/ubuntu/mitigation-present-at-boundary.sh` (line ~149)  
**Also:** `script/windows/mitigation-present-at-boundary.ps1`

**Current code (bash):**
```bash
find "$REPO_ROOT/src" -type f \( \
    -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \
    -o -name "*.py" -o -name "*.go" -o -name "*.java" -o -name "*.cs" \
\) 2>/dev/null
```

**Problem:** Zero `*.rs` files. A Rust project's `src/` is entirely `.rs` files. This script will find nothing and report "no boundary mitigations found" — a false pass.

**Fix Required:**
- Replace extension list with `*.rs` (or add it alongside the others).

---

## Bug 2 — `integration-points-exist.sh` — Same Wrong Extensions

**File:** `script/ubuntu/integration-points-exist.sh` (line ~123)  
**Also:** `script/windows/integration-points-exist.ps1`

**Current code:**
```bash
find "$REPO_ROOT" -type f \( \
    -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \
    -o -name "*.py" -o -name "*.go" -o -name "*.java" -o -name "*.cs" \
\) 2>/dev/null
```

**Problem:** Identical to Bug 1. Scans for the wrong language entirely.

**Fix Required:**
- Add `*.rs` to the extension list.

---

## Bug 3 — `design-tokens-in-implementation.sh` — Web-Only CSS/SCSS Scan

**File:** `script/ubuntu/design-tokens-in-implementation.sh` (lines ~112-117)

**Current code:**
```bash
find "$REPO_ROOT/src" -type f \( \
    -name "*.css" -o -name "*.scss" -o -name "*.less" \
\) 2>/dev/null
```

**Problem:** Rust projects don't have CSS/SCSS/LESS files. This script is completely irrelevant for `rust_dev`. Additionally, the `06-design` domain it serves was **dropped** from `rust_dev`.

**Fix Required:**
- Either delete this script (domain dropped) or add a `not_applicable` early-exit for Rust systems.

---

## Bug 4 — `unit-test-coverage.sh` — Scans for JS/Python Test Patterns, Not `#[test]`

**File:** `script/ubuntu/unit-test-coverage.sh`  
**Also:** `script/windows/unit-test-coverage.ps1`

**Current code scans for:**
```
*.test.ts, *.spec.ts, test_*.py, *_test.py, *_test.go
```

**Problem:** Rust tests use `#[test]` attributes inside `*.rs` files (often in `tests/` dir or inline). This script will find zero test files in a Rust project.

**Fix Required:**
- Add `grep -r '#\[test\]' --include='*.rs'` scanning.
- Alternatively, integrate with `cargo test -- --coverage` for actual coverage data.

---

## Bug 5 — `public-contract-diff.sh` — Only Detects JS/Python Web Frameworks

**File:** `script/ubuntu/public-contract-diff.sh` (lines ~69-72)

**Current code detects:**
```bash
grep -r "app.get\|router.get\|@app.route\|@GetMapping\|@RequestMapping" ...
```

**Problem:** These are Express.js, Flask, and Spring patterns. Rust web frameworks use different syntax:
- **Actix/Axum:** `#[get("/")]`, `#[post("/")]`, `.route("/path", get(handler))`
- **Rocket:** `#[get("/")]`, `#[post("/")]`
- **Tide:** `app.at("/path").get(handler)`

**Fix Required:**
- Add Rust web framework patterns to the grep list.

---

## Bug 6 — `mock-api-runs.sh` — JS Mock Server Patterns Only

**File:** `script/ubuntu/mock-api-runs.sh`  
**Also:** `script/windows/mock-api-runs.ps1`

**Current code checks for:**
```
Express mock patterns, MSW handlers, WireMock
```

**Problem:** Rust projects use `mockall`, `httpmock`, `wiremock-rs`, or `wiremock` — none of which are detected. The script will always report "no mock APIs found."

**Fix Required:**
- Add Rust mock framework detection (`mockall`, `httpmock`, `wiremock`).

---

## Bug 7 — `dependency-manifest.sh` — Cargo.toml Listed But Not Parsed

**File:** `script/ubuntu/dependency-manifest.sh` (line ~47)

Cargo.toml is in the `manifest_files` array, but the `case` statement (lines ~72-88) has no `cargo)` branch:
```bash
case "$manifest" in
    package.json) ... ;;
    requirements.txt) ... ;;
    go.mod) ... ;;
    Gemfile) ... ;;
    pom.xml) ... ;;
    *) echo "dependency count not parsed" ;;
esac
```

**Problem:** Cargo.toml hits the `*)` fallback and reports "dependency count not parsed" — a misleading error.

**Fix Required:**
- Add a `cargo|Cargo.toml)` branch that parses `[dependencies]` sections from Cargo.toml.

---

## Impact Summary

| Bug | Script | Severity | Effect |
|-----|--------|----------|--------|
| 1 | mitigation-present-at-boundary | CRITICAL | False pass — no Rust code scanned |
| 2 | integration-points-exist | CRITICAL | False pass — no Rust code scanned |
| 3 | design-tokens-in-implementation | HIGH | Irrelevant for Rust + dropped domain |
| 4 | unit-test-coverage | CRITICAL | False pass — no Rust tests detected |
| 5 | public-contract-diff | HIGH | Misses all Rust web API endpoints |
| 6 | mock-api-runs | HIGH | Misses all Rust mock patterns |
| 7 | dependency-manifest | MEDIUM | Cargo.toml not parsed, misleading error |

---

## Root Cause

These scripts were inherited from `base_dev` (a web/generic system) and were never updated with Rust-specific file patterns. The `rust_dev` implementation updated documentation and audit rules but missed the script layer entirely.

---

## Recommended Fix Strategy

1. Create a shared `_rust_common.sh` (and `_rust_common.ps1`) that defines:
   ```bash
   RUST_EXTENSIONS="*.rs"
   RUST_TEST_ATTR="#\[test\]"
   RUST_MOCK_CRATES="mockall|httpmock|wiremock"
   RUST_WEB_PATTERNS="#\[get\(|#\[post\(|\.route\("
   ```
2. Source this file in each script that needs Rust-aware scanning.
3. For dropped-domain scripts (design-tokens), add early-exit guard:
   ```bash
   if [[ "$SYSTEM_ID" == "rust_dev" ]]; then
       echo '{"status":"not_applicable","evidence":["Domain 06-design dropped from rust_dev"]}'
       exit 0
   fi
   ```
