# rust_dev — Gap Analysis: Deterministic Audit Rules Missing Rust-Specific Severity Adjustments

**Category:** Gaps / Audit Coverage  
**Severity:** Medium  
**Date:** 2026-07-15

---

## Summary

The deterministic audit rules in `audit/deterministic/document/` were updated to include Rust-specific `required_semantic_types` for each domain. However, the **rules themselves** were not updated to reflect the higher stakes of Rust-specific violations. Certain sections in a Rust system warrant `critical` (not just `error`) severity — especially `unsafe` usage policy and ownership correctness — but all new rules were created with a uniform default `severity: error` and `weight: 1.0`.

Additionally, the mapping file is missing Rust-specific script checks that were implied by the proposal but never wired in.

---

## Gap 1 — `unsafe` Policy Audit Has Wrong Severity

**File:** `audit/deterministic/section/07-engineering/11-unsafe_guidelines.yaml`

```yaml
severity: error
weight: 1.0
```

**Expected:**
```yaml
severity: critical
weight: 2.0
```

**Rationale:** The `rust_dev` proposal explicitly states: "Zero `unsafe` in business logic". Violating the `unsafe` policy introduces undefined behavior — this is a **critical** issue, not merely an `error`. It should be weighted at least 2× to reflect its severity.

**Fix Required:**
- Set `severity: critical` and `weight: 2.0` in `07-engineering/11-unsafe_guidelines.yaml`.

---

## Gap 2 — `architecture` Rule `eng-doc-004` Contradicts Rust Paradigm

**File:** `audit/deterministic/document/07-engineering.yaml` (rule `eng-doc-004`)

```yaml
- id: eng-doc-004
  description: "No implementation technology references"
  condition: "document does not name specific programming languages, frameworks, libraries..."
  severity: error
```

For `rust_dev`, this is a **direct contradiction**. The engineering standards files are **intentionally full of Rust technology references** — `tokio`, `thiserror`, `anyhow`, `Arc<Mutex<T>>` etc. This generic base_dev rule, if run as-is, would fail every `rust_dev` engineering document.

**Fix Required:**
- Override `eng-doc-004` for `rust_dev` to disable or relax the technology-independence check in the engineering domain.
- Add a `rust_dev_override: true` flag or create a system-specific `overrides:` block in the rule to exclude Rust-specific terminology from the technology-independence keyword scan.

---

## Gap 3 — `script/mapping.yaml` Missing Rust-Specific Checks

**File:** `script/mapping.yaml`

The mapping currently wires generic checks (`lint-standards`, `build-succeeds`, `cargo-audit`). However, the proposal and the new `script/schema/` do NOT include these Rust-critical checks:

| Missing Check | Proposed Domain | Why Critical |
|---|---|---|
| `cargo-clippy` | `07-engineering` | Enforces `#![deny(clippy::all)]` — Rust-specific linting beyond basic lint |
| `unsafe-code-scan` | `07-engineering` | Verify `#![forbid(unsafe_code)]` is present in all business-logic crates |
| `crate-dependency-graph` | `05-architecture` | Verify no circular crate dependencies in the workspace |
| `cargo-audit` | `03-security` | Scan for CVEs in `Cargo.lock` — exists as manifest but NOT yet wired into mapping |

Note: `cargo-audit.manifest.yaml` was created in `script/schema/14-build/` but this check is a **security** check (`cargo audit`), not a build check. It should be in `script/schema/03-security/` and wired to `03-security` in the mapping.

**Fix Required:**
- Move `script/schema/14-build/cargo-audit.manifest.yaml` to `script/schema/03-security/cargo-audit.manifest.yaml`.
- Add the following to `script/mapping.yaml`:
  ```yaml
  - check: cargo-audit
    domain: 03-security
    category: A
    consumed_by:
      - { audit_type: deterministic, domain: 03-security, rule_id: sec-doc-rust-001 }
  
  - check: cargo-clippy
    domain: 07-engineering
    category: A
    consumed_by:
      - { audit_type: deterministic, domain: 07-engineering, rule_id: eng-doc-rust-001 }
  ```

---

## Gap 4 — `architecture` Document Rule Does Not List `crate_architecture` as a HIGH-Weight Requirement

**File:** `audit/deterministic/document/05-architecture.yaml` (rule `arch-doc-001`)

The `crate_architecture` and `trait_design` sections were added to `required_semantic_types` but with the same weight as all other sections (`weight: 1.5`). For `rust_dev`, these two sections are the most architecturally distinctive and important — they should have a higher weight.

**Fix Required:**
- Consider creating a separate rule `arch-doc-rust-001` that specifically enforces crate architecture with `weight: 2.0` and `severity: error`.

---

## Gap 5 — `lint-standards.manifest.yaml` Uses Generic Executable

**File:** `script/schema/07-engineering/lint-standards.manifest.yaml`

The manifest has no `executable` field — it only declares `lint-standards` as a check name. For Rust, this should be `cargo clippy --all-targets --all-features -- -D warnings`.

**Fix Required:**
- Add to `lint-standards.manifest.yaml`:
  ```yaml
  executable: "cargo clippy --all-targets --all-features -- -D warnings"
  ```
