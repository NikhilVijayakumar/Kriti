# Third-Pass Audit — Scripts, Schemas, Manifests, Calculation Layer

**Review Date:** 2026-07-16 (third pass)
**Scope:** `script/ubuntu/**`, `script/windows/**`, `script/schema/**`, `calculation/**`
**Method:** Read every script pair in full, diffed bash vs PowerShell logic, extracted every schema's declared `metrics` keys and diffed against each script's actual emitted JSON keys, traced manifest fields against real script behavior, read the calculation layer's formulas end-to-end.

**Headline finding: Bugs 10-13 are the highest-impact result of this whole audit.** `build-succeeds` and `lint-standards`/`lint-pass` are core Category-A checks and, as shipped, will run `npm run build` / `npm run lint` against every audited Rust repo — the manifest-level fix from the prior pass (documenting `executable: "cargo fmt/clippy"`) never propagated into the scripts that actually execute the command.

---

## BUGS

### BUG-1 (CRITICAL) — `cargo-fmt.sh`: exit code always masked to 0, check can never fail
**File:** `E:\Python\Kriti\samgraha\system\rust_dev\script\ubuntu\07-engineering\cargo-fmt.sh:52-53`
```bash
cargo fmt --all -- --check > "$FMT_OUTPUT" 2>&1 || true
FMT_EXIT=$?
```
`|| true` makes the compound command always succeed, so `$?` next line is always `0` (true's exit code), never cargo fmt's real exit code. Script **always reports `pass`**, even when files are unformatted. Codebase's own convention elsewhere (`lint-standards.sh:58-61`, `lint-pass.sh:49-51`, `build-succeeds.sh:52-54`) correctly uses `set +e` / capture `$?` / `set -e`. PowerShell twin (`cargo-fmt.ps1:41-42`) does this correctly via `$LASTEXITCODE` — bash/PowerShell have diverged: PS can fail this check, bash cannot.
**Fix:** `set +e; cargo fmt --all -- --check > "$FMT_OUTPUT" 2>&1; FMT_EXIT=$?; set -e`.

### BUG-2 (CRITICAL) — `crate-dependency-graph.sh`: `set -e` aborts before error handling runs, no JSON output on failure
**File:** `E:\Python\Kriti\samgraha\system\rust_dev\script\ubuntu\05-architecture\crate-dependency-graph.sh:52-55`
```bash
cargo metadata --format-version 1 --no-deps > "$META_OUTPUT" 2>/dev/null
if [[ $? -ne 0 ]]; then
    write_result "error" '["cargo metadata failed — ensure Cargo.toml is valid"]' false 0
fi
```
Script has `set -euo pipefail` at top. If `cargo metadata` fails (broken workspace, bad `Cargo.toml`, missing member), `set -e` terminates immediately on that line — the `if` check is dead code, never reached. No `$OUT` file is written on this failure path, unlike every other error path (all go through `write_result`). PowerShell twin (`crate-dependency-graph.ps1:41-44`) doesn't have this problem — checks `$LASTEXITCODE` explicitly.
**Fix:** `cargo metadata --format-version 1 --no-deps > "$META_OUTPUT" 2>/dev/null || true` then check captured `$?`, or wrap in `set +e`/`set -e`.

### BUG-3 (MEDIUM) — `unsafe-code-scan.sh`: fail-path evidence never interpolates crate list (literal `$CRATE_ROOT_LIST` text emitted)
**File:** `E:\Python\Kriti\samgraha\system\rust_dev\script\ubuntu\07-engineering\unsafe-code-scan.sh:78`
```bash
write_result "fail" '["Found '"$UNSAFE_COUNT"' unsafe blocks in source; '"$CRATES_WITHOUT_FORBID"' crate(s) missing forbid(unsafe_code): $CRATE_ROOT_LIST"]' "$UNSAFE_COUNT" "$CRATES_WITHOUT_FORBID"
```
Final segment is single-quoted, so `$CRATE_ROOT_LIST` is **not** expanded — evidence string literally contains text `$CRATE_ROOT_LIST` instead of actual crate paths. PowerShell twin (`unsafe-code-scan.ps1:63`) correctly interpolates `$crateRootStr`. Bash/PowerShell diverged: only PS reports which crates are missing `forbid(unsafe_code)`.
**Fix:** Move `$CRATE_ROOT_LIST` outside single-quoted segment, e.g. `'"...": '"$CRATE_ROOT_LIST"'"]'`.

### BUG-4 (HIGH) — Schema/output mismatch: `cargo-audit.schema.json` declares field never emitted
**Files:** `script\schema\03-security\cargo-audit.schema.json:8-10` vs `script\ubuntu\03-security\cargo-audit.sh:27` / `script\windows\03-security\cargo-audit.ps1:16`
Schema declares `metrics.audit_pass` (boolean). Actual output is `{ "vulnerability_count": ..., "critical_count": ... }` — no `audit_pass` field in either script. Leftover from doc 09's spec prose never reconciled with real implementation.
**Fix:** Remove `audit_pass` from schema (or add to both scripts as `vulnerability_count == 0`).

### BUG-5 (HIGH) — Schema/output mismatch: `crate-dependency-graph.schema.json` field names entirely wrong
**Files:** `script\schema\05-architecture\crate-dependency-graph.schema.json:8-10` vs `script\ubuntu\05-architecture\crate-dependency-graph.sh:27`
Schema declares only `metrics.invalid_dependencies` (integer). Script actually emits `{ "has_cycles": bool, "violation_count": int }`. Zero overlap.
**Fix:** Replace `invalid_dependencies` with `has_cycles: boolean` and `violation_count: integer`.

### BUG-6 (HIGH) — Schema/output mismatch: `cargo-fmt.schema.json` missing `total_violations`
**Files:** `script\schema\07-engineering\cargo-fmt.schema.json:5-11` vs `script\ubuntu\07-engineering\cargo-fmt.sh:27`
Script emits `{ "unformatted_files": int, "total_violations": int }`; schema only declares `unformatted_files`.
**Fix:** Add `total_violations: integer` to schema.

### BUG-7 (HIGH) — Schema/output mismatch: `unsafe-code-scan.schema.json` missing `crates_without_forbid`
**Files:** `script\schema\07-engineering\unsafe-code-scan.schema.json:5-12` vs `script\ubuntu\07-engineering\unsafe-code-scan.sh:27`
Script emits `{ "unsafe_blocks_found": int, "crates_without_forbid": int }`; schema only declares `unsafe_blocks_found`.
**Fix:** Add `crates_without_forbid: integer` to schema.

### BUG-8 (MEDIUM) — All 4 previously-"new" Rust manifests still lack `requires_network`/`depends_on`/`timeout_seconds`
**Files:**
- `script\schema\03-security\cargo-audit.manifest.yaml` — fetches RustSec advisory DB, **needs network**, should be `requires_network: true`
- `script\schema\05-architecture\crate-dependency-graph.manifest.yaml` — `cargo metadata` is local-only, should be `false`
- `script\schema\07-engineering\cargo-fmt.manifest.yaml` — local-only, should be `false`
- `script\schema\07-engineering\unsafe-code-scan.manifest.yaml` — local grep-only, should be `false`

All other manifests consistently carry `depends_on`/`timeout_seconds`/`requires_network`; these 4 have only `check`/`description`/`executable`/`severity`. Cache-policy engine has no way to know these checks' network requirements.
**Fix:** Add the standard 3 fields to each of the 4 manifests with the values above.

### BUG-9 (LOW) — `policy.yaml` has dead cache override that can never match a real check
**File:** `E:\Python\Kriti\samgraha\system\rust_dev\script\policy.yaml:15-16`
```yaml
  - check: cargo-clippy
    strategy: always_rerun
```
No check named `cargo-clippy` exists in `script/mapping.yaml` or `script/schema/**` — real check id is `lint-standards` (`mapping.yaml:104-108`, `lint-standards.manifest.yaml:1`). Written against old doc-06/13 proposal text, never renamed to match actual implementation. `lint-standards` has **no** cache-policy override, silently falls back to generic `fingerprint` default; this dead entry never fires.
**Fix:** Rename `cargo-clippy` → `lint-standards`, confirm `always_rerun` is still right.

### BUG-10 (CRITICAL) — `lint-standards.sh`/`.ps1` still defaults to `npm run lint`; manifest's `executable` field is pure documentation, never read
**Files:** `script\ubuntu\07-engineering\lint-standards.sh:7`, `script\windows\07-engineering\lint-standards.ps1:6`
```bash
LINT_COMMAND="npm run lint"
```
Prior pass marked this "FIXED" by adding `executable: "cargo clippy --all-targets --all-features -- -D warnings"` to the manifest — but **the script never reads the manifest at all**, only a CLI flag `--lint-command`, defaulting to `npm run lint` if not passed. Nothing in `mapping.yaml`/`policy.yaml` wires the manifest's `executable` into that flag. Against a pure Rust repo (no `package.json`/npm) this fails or errors on every run. The prior fix was cosmetic only.
Also `CONFIGS` (line 49) checks `.eslintrc*`/`.pylintrc`/`.flake8`/`pyproject.toml`/`.golangci.yml`/`.rubocop.yml`/`.stylelintrc` — no `clippy.toml`/`.clippy.toml`/`Cargo.toml [lints]` detection at all.
**Fix:** Default to `cargo clippy --all-targets --all-features -- -D warnings`; add `clippy.toml`/`.clippy.toml` to `CONFIGS`.

### BUG-11 (CRITICAL) — `lint-pass.sh`/`.ps1` (13-implementation) same npm residue
**Files:** `script\ubuntu\13-implementation\lint-pass.sh:7`, `script\windows\13-implementation\lint-pass.ps1:6`
```bash
LINT_COMMAND="npm run lint"
```
Same issue as Bug-10, sibling 13-implementation domain. `lint-pass.manifest.yaml` has no `executable` field at all — not even documented.
**Fix:** Default to `cargo clippy --all-targets --all-features -- -D warnings` (or document why intentionally generic/duplicate of `lint-standards`).

### BUG-12 (CRITICAL) — `build-succeeds.sh`/`.ps1` still defaults to `npm run build`
**Files:** `script\ubuntu\14-build\build-succeeds.sh:7`, `script\windows\14-build\build-succeeds.ps1:6`
```bash
BUILD_COMMAND="npm run build"
```
Should default to `cargo build --release` for Rust. Nothing in `mapping.yaml`/`policy.yaml`/`build-succeeds.manifest.yaml` overrides it. One of the most fundamental checks in the whole system will run `npm run build` against a Rust repo and fail for the wrong reason.
**Fix:** Default to `cargo build --release`.

### BUG-13 (CRITICAL) — `artifact-exists.sh`/`.ps1` still defaults to `dist`
**Files:** `script\ubuntu\14-build\artifact-exists.sh:7`, `script\windows\14-build\artifact-exists.ps1:6`
```bash
ARTIFACT_PATH="dist"
```
Rust artifacts land in `target/release` or `target/debug`, never `dist/`. Depends on `build-succeeds` (`artifact-exists.manifest.yaml:2`) and will report "artifact not found" for every real Rust build even once Bug-12 is fixed.
**Fix:** Default to `target/release`.

---

## GAPS

### GAP-1 (MEDIUM) — `dependency-vuln-scan.sh`/`.ps1` entirely npm/pip-only, zero Cargo.toml/Cargo.lock support
**Files:** `script\ubuntu\03-security\dependency-vuln-scan.sh` (full file), `script\windows\03-security\dependency-vuln-scan.ps1` (full file)
Only checks `package.json` (`npm audit --json`) or falls back to `requirements.txt` counting. No Cargo.toml/Cargo.lock branch, unlike `dependency-manifest.sh` (which got a `cargo)` branch in the prior pass). For any pure-Rust repo this always hits `write_result "not_applicable" '["No dependency manifests found to scan"]'` — dead weight, consumes `sec-doc-016` (`mapping.yaml:89-93`) without contributing evidence. `cargo-audit.sh` already covers Rust CVE scanning in same domain.
**Fix:** Either document that `cargo-audit` supersedes this for `rust_dev` and drop from `mapping.yaml`, or fold Cargo.lock parsing in.

### GAP-2 (MEDIUM) — `module-boundary-diff.sh`/`.ps1` has no Cargo workspace support; violation regex only matches JS/Python import syntax
**Files:** `script\ubuntu\05-architecture\module-boundary-diff.sh:52-72,95`; `script\windows\05-architecture\module-boundary-diff.ps1:33-60,100`
Module declarations only read from `structure.yaml` or `package.json` `workspaces` — no branch for `Cargo.toml`'s `[workspace] members = [...]`. Typical Rust workspace repo → always `not_applicable`. Even where a module is found, violation detector greps for `(require|import|from).*['"]$other` (JS/Python keywords) — Rust uses `use crate_name::...;`/`mod foo;`, neither ever matches, even in scanned `*.rs` files.
**Fix:** Add `[workspace] members` parser (mirror `crate-dependency-graph.sh`'s `cargo metadata` approach or TOML parsing like `dependency-manifest.sh`); add `use\s+$other`/`mod\s+$other` to violation regex.

### GAP-3 (HIGH) — `unit-test-coverage.sh`/`.ps1`: test-detection heuristic assumes JS/Python file-naming, doesn't recognize Rust's idiomatic `#[cfg(test)]`
**Files:** `script\ubuntu\12-qa\unit-test-coverage.sh:9`, `script\windows\12-qa\unit-test-coverage.ps1:8`
```bash
TEST_INCLUDE="*.test.*:*.spec.*:*_test.*:test_*.py:tests_*.py"
```
Prior pass only added `*.rs` to `SOURCE_INCLUDE` (line 7); `TEST_INCLUDE` patterns untouched. Idiomatic Rust puts unit tests inline via `#[cfg(test)] mod tests { ... }` — no separate `foo_test.rs` file in most real crates. Script will count every source file "untested" and report near-0% coverage — false negative on virtually every idiomatic Rust codebase.
**Fix:** Add inline detection via `grep -l '#\[cfg(test)\]' --include='*.rs'` (or `#[test]`), treating a file as "tested" if it contains its own inline test module, in addition to the separate-file heuristic for `tests/` integration tests.

### GAP-4 (LOW, confirmed unchanged — not new, not regressed) — `calculation/` has no per-domain or per-check weighting mechanism
**Files:** `calculation/deterministic/document.yaml`, `calculation/deterministic/section.yaml`, `calculation/summary/final_score.yaml`
`weight` from audit rule YAML **is** consumed, but only at rule level inside a single document's `weighted_pass_rate` formula (`section.yaml:8`, `document.yaml:8`). No file/formula weights one *domain* against another — `final_score.yaml:4-7` combines the 4 bucket types (deterministic/semantic × whole/section) at a fixed equal 25/25/25/25 split, explicitly documented as intentionally domain-agnostic (`calculation/README.md` Key Design Decisions). Matches doc 06's prior conclusion exactly.

---

## OPTIMIZATIONS

### OPT-1 — Two incompatible manifest schemas coexist with no shared spec
4 Rust-specific manifests (`cargo-audit`, `cargo-fmt`, `unsafe-code-scan`, `crate-dependency-graph`) use `{check, description, executable, severity}`; all others use `{check, depends_on, timeout_seconds, requires_network}`. At least one `executable` field is provably dead/unread (Bug-10). Since Bug-8 already touches these 4 manifests, unify on one schema shape across all 20 and drop or wire up `executable`/`description`/`severity` consistently.

### OPT-2 — `cargo-fmt.sh`'s `total_violations` metric is meaningless
**File:** `script\ubuntu\07-engineering\cargo-fmt.sh:60`
```bash
TOTAL_LINES=$(wc -l < "$FMT_OUTPUT" 2>/dev/null || echo 0)
```
Counts raw diff output lines from `cargo fmt --check` and reports as `total_violations` — varies with diff verbosity, not actual violation count. Once Bug-6 (schema) is fixed to expose this field, compute something meaningful (count `+`/`-` diff lines) or drop the field, keep `unformatted_files` as sole metric.

---

## SUGGESTIONS

1. Since `cargo-audit.sh` is already correctly wired (Bug-8 aside), consider retiring `dependency-vuln-scan` from `rust_dev`'s `mapping.yaml` entirely (GAP-1) rather than leaving a permanently-`not_applicable` check.
2. `module-boundary-diff` (GAP-2) substantially overlaps with `crate-dependency-graph` once Cargo-workspace support is added — decide whether both checks are needed, or drop `module-boundary-diff` in favor of `crate-dependency-graph`'s already-correct crate-boundary detection.
3. `unsafe-code-scan.sh`'s `rg`-with-`grep`-fallback discipline is good and could be a model for other scripts (no action needed).

---

## Summary Table

| # | Category | File(s) | Severity |
|---|---|---|---|
| BUG-1 | cargo-fmt.sh exit code masked by `\|\| true` | `script/ubuntu/07-engineering/cargo-fmt.sh:52-53` | CRITICAL |
| BUG-2 | crate-dependency-graph.sh `set -e` skips error handling | `script/ubuntu/05-architecture/crate-dependency-graph.sh:52-55` | CRITICAL |
| BUG-3 | unsafe-code-scan.sh evidence quoting bug | `script/ubuntu/07-engineering/unsafe-code-scan.sh:78` | MEDIUM |
| BUG-4..7 | Schema/output metric mismatches (4 files) | `script/schema/{03-security,05-architecture,07-engineering}/*.schema.json` | HIGH |
| BUG-8 | 4 new manifests missing requires_network/depends_on/timeout | `script/schema/{03-security,05-architecture,07-engineering}/*.manifest.yaml` | MEDIUM |
| BUG-9 | Dead `cargo-clippy` policy override | `script/policy.yaml:15-16` | LOW |
| BUG-10..13 | npm/dist defaults never adapted to cargo (4 script pairs) | `lint-standards`, `lint-pass`, `build-succeeds`, `artifact-exists` (ubuntu+windows) | CRITICAL |
| GAP-1 | dependency-vuln-scan is npm/pip-only | `script/{ubuntu,windows}/03-security/dependency-vuln-scan.*` | MEDIUM |
| GAP-2 | module-boundary-diff has no Cargo workspace support | `script/{ubuntu,windows}/05-architecture/module-boundary-diff.*` | MEDIUM |
| GAP-3 | unit-test-coverage doesn't detect inline `#[cfg(test)]` | `script/{ubuntu,windows}/12-qa/unit-test-coverage.*` | HIGH |
| GAP-4 | No per-domain weighting (confirmed unchanged) | `calculation/**` | LOW |
| OPT-1 | Manifest schema inconsistency | `script/schema/**` | LOW |
| OPT-2 | Meaningless `total_violations` metric | `script/ubuntu/07-engineering/cargo-fmt.sh:60` | LOW |
