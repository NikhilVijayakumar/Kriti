# rust_dev — Bug Report: Missing Rust-Specific Script Implementations

**Category:** Gaps / Missing Implementation  
**Severity:** CRITICAL  
**Date:** 2026-07-15

---

## Summary

Four Rust-critical script checks have **manifests** (`*.manifest.yaml`) and **mapping entries** in `script/mapping.yaml`, but **no actual `.sh` or `.ps1` script implementations** exist in `script/ubuntu/` or `script/windows/`. These checks will silently skip or error when the audit pipeline tries to run them.

---

## Gap 1 — `cargo-audit` — No Script Implementation

**Manifest:** `script/schema/14-build/cargo-audit.manifest.yaml`  
**Mapping:** `script/mapping.yaml` (referenced in domain `14-build`)  
**Script:** ❌ **MISSING** from both `script/ubuntu/` and `script/windows/`

**What it should do:**
- Run `cargo audit` against `Cargo.lock`
- Parse JSON output for vulnerability counts
- Return `audit_pass: bool`, `vulnerability_count: int`, `critical_count: int`
- Exit 0 on success, non-zero on failure

**Impact:** CVE scanning for Rust dependencies is completely non-functional. A project with known vulnerabilities will pass the security audit.

---

## Gap 2 — `unsafe-code-scan` — No Script Implementation

**Manifest:** `script/schema/07-engineering/unsafe-code-scan.manifest.yaml` (referenced in mapping)  
**Mapping:** `script/mapping.yaml` (referenced in domain `07-engineering`)  
**Script:** ❌ **MISSING** from both `script/ubuntu/` and `script/windows/`

**What it should do:**
- Scan all `*.rs` files for `unsafe` blocks
- Verify business-logic crates have `#![forbid(unsafe_code)]` at crate root
- Report which crates lack the forbid attribute
- Return `unsafe_blocks_found: int`, `crates_without_forbid: list[str]`

**Impact:** The "zero unsafe in business logic" policy is unenforceable without this script. The audit rule `eng-doc-rust-001` references script evidence that doesn't exist.

---

## Gap 3 — `cargo-fmt` — No Script Implementation

**Manifest:** `script/schema/07-engineering/cargo-fmt.manifest.yaml` (referenced in mapping)  
**Mapping:** `script/mapping.yaml`  
**Script:** ❌ **MISSING** from both `script/ubuntu/` and `script/windows/`

**What it should do:**
- Run `cargo fmt --all -- --check`
- Report which files are not formatted
- Return `unformatted_files: list[str]`, `total_violations: int`

**Impact:** Code formatting standards are unverifiable. The engineering audit will not catch formatting drift.

---

## Gap 4 — `crate-dependency-graph` — No Script Implementation

**Manifest:** `script/schema/05-architecture/crate-dependency-graph.manifest.yaml`  
**Mapping:** `script/mapping.yaml` (referenced in domain `05-architecture`)  
**Script:** ❌ **MISSING** from both `script/ubuntu/` and `script/windows/`

**What it should do:**
- Run `cargo metadata --format-version 1`
- Build the crate dependency graph
- Check for circular dependencies
- Verify directional dependency rules (infrastructural → core, never reverse)
- Return `has_cycles: bool`, `violations: list[str]`, `total_crates: int`

**Impact:** Crate boundary violations and circular dependencies go undetected. Architecture audit rule `arch-doc-rust-001` has no ground truth.

---

## Summary

| Script | Manifest Exists | Mapping Entry | Script Implementation | Status |
|--------|----------------|---------------|----------------------|--------|
| `cargo-audit` | ✅ | ✅ | ❌ | **BROKEN** |
| `unsafe-code-scan` | ✅ | ✅ | ❌ | **BROKEN** |
| `cargo-fmt` | ✅ | ✅ | ❌ | **BROKEN** |
| `crate-dependency-graph` | ✅ | ✅ | ❌ | **BROKEN** |

---

## Recommended Implementation Priority

1. **`cargo-audit`** — Security critical. Implement first.
2. **`unsafe-code-scan`** — Core Rust safety policy. Implement second.
3. **`cargo-fmt`** — Low complexity, high value. Implement third.
4. **`crate-dependency-graph`** — Complex but important for architecture. Implement last.

---

## Implementation Template

Each script should follow the standard pattern used by existing scripts:

**Arguments:**
```
--repo-root <path>       # Root of the repository
--repo-fingerprint <hash> # Cache key
--out <path>             # Output JSON file path
```

**Output JSON schema:**
```json
{
  "check": "<check-name>",
  "domain": "<domain-id>",
  "category": "A|B|C",
  "status": "pass|fail|error|not_applicable",
  "metrics": { ... },
  "evidence": ["..."],
  "executed_at": "ISO-8601",
  "repo_fingerprint": "<hash>"
}
```

**Exit codes:**
- `0` — Success (check passed or failed, but script ran correctly)
- `1` — Error (script could not run, missing dependencies, etc.)
