# rust_dev — Bug Report: Script Manifest and Policy Inconsistencies

**Category:** Bugs / Metadata  
**Severity:** MEDIUM  
**Date:** 2026-07-15

---

## Summary

Script manifests contain incorrect `requires_network` flags, duplicate definitions, and the policy file is missing Rust-specific cache strategies. These metadata bugs cause the audit pipeline to make wrong decisions about when to re-run checks.

---

## Bug 1 — `dependency-vuln-scan.manifest.yaml` Wrong Network Flag

**File:** `script/schema/dependency-vuln-scan.manifest.yaml`

```yaml
requires_network: false
```

**Problem:** The script runs `npm audit --json` which fetches vulnerability data from the npm registry. This requires network access.

**Fix Required:**
- Change to `requires_network: true`.

---

## Bug 2 — `build-succeeds.manifest.yaml` Wrong Network Flag

**File:** `script/schema/build-succeeds.manifest.yaml`

```yaml
requires_network: false
```

**Problem:** `cargo build` may download crate dependencies from crates.io on first run or after dependency changes.

**Fix Required:**
- Change to `requires_network: true` (or add a comment explaining the conditional nature).

---

## Bug 3 — `module-boundary-diff.ps1` Duplicate `$excludeDirs` Definition

**File:** `script/windows/module-boundary-diff.ps1` (lines ~67 and ~83)

The `$excludeDirs` variable is defined identically at two locations:
```powershell
$excludeDirs = @("node_modules", "target", "dist", ".git", "vendor", "__pycache__")
```

**Problem:** Maintenance risk — if the exclusion list needs updating, one instance may be changed while the other is missed.

**Fix Required:**
- Define `$excludeDirs` once at the top of the script and reference it throughout.

---

## Bug 4 — `dependency-reachable.sh` Missing `DOCS_ROOT` Validation

**File:** `script/ubuntu/dependency-reachable.sh` (lines ~45-55)

`REPO_ROOT` is validated at the top, but `DOCS_ROOT` parameter is never checked for emptiness. It silently falls back to `$REPO_ROOT/docs` or `$REPO_ROOT` without warning.

**Problem:** If a caller passes an invalid `DOCS_ROOT`, the script silently scans the wrong directory.

**Fix Required:**
- Add validation: warn if `DOCS_ROOT` is empty and document the fallback behavior.

---

## Bug 5 — `dependency-manifest.sh` No Cargo.toml Parsing

**File:** `script/ubuntu/dependency-manifest.sh` (lines ~72-88)

Cargo.toml is in the `manifest_files` array but the `case` statement has no `cargo)` branch. It hits the `*)` fallback:
```bash
*) echo "dependency count not parsed" ;;
```

**Fix Required:**
- Add a parsing branch for Cargo.toml that extracts `[dependencies]`, `[dev-dependencies]`, and `[build-dependencies]` sections.

---

## Bug 6 — `script/policy.yaml` Missing Rust-Specific Cache Strategies

**File:** `script/policy.yaml`

Current Rust-specific entries:
```yaml
- check: cargo-audit
  strategy: ttl
  max_age_seconds: 86400
- check: cargo-clippy
  strategy: always_rerun
```

**Missing entries:**

| Check | Recommended Strategy | Reason |
|-------|---------------------|--------|
| `crate-dependency-graph` | `fingerprint` | Only re-run when Cargo.toml files change |
| `unsafe-code-scan` | `always_rerun` | Safety checks should never be cached |
| `module-boundary-diff` | `fingerprint` | Only when crate/module files change |

**Fix Required:**
- Add the three missing policy entries.

---

## Bug 7 — `lint-standards.manifest.yaml` No Executable Specified

**File:** `script/schema/07-engineering/lint-standards.manifest.yaml`

The manifest has no `executable` field. For Rust, this should be `cargo clippy --all-targets --all-features -- -D warnings`.

**Fix Required:**
- Add `executable: "cargo clippy --all-targets --all-features -- -D warnings"` to the manifest.

---

## Bug 8 — Manifest Schema Inconsistency

Rust-specific manifests (`cargo-audit`, `cargo-fmt`, `unsafe-code-scan`, `crate-dependency-graph`) have extra fields: `description`, `executable`, `severity`.

Standard manifests (`secret-scan`, `build-succeeds`, etc.) have only: `depends_on`, `timeout_seconds`, `requires_network`.

No unified schema exists. No documentation explains the difference.

**Fix Required:**
- Create a unified manifest schema that supports both types.
- Document the extended fields in `script/README.md` or `script/schema/README.md`.

---

## Summary

| # | Bug | Severity | File |
|---|-----|----------|------|
| 1 | Wrong `requires_network` for vuln-scan | HIGH | dependency-vuln-scan.manifest.yaml |
| 2 | Wrong `requires_network` for build | MEDIUM | build-succeeds.manifest.yaml |
| 3 | Duplicate `$excludeDirs` | LOW | module-boundary-diff.ps1 |
| 4 | Missing `DOCS_ROOT` validation | MEDIUM | dependency-reachable.sh |
| 5 | No Cargo.toml parsing | MEDIUM | dependency-manifest.sh |
| 6 | Missing policy entries | MEDIUM | policy.yaml |
| 7 | No executable in lint manifest | MEDIUM | lint-standards.manifest.yaml |
| 8 | Inconsistent manifest schema | LOW | Multiple manifests |
