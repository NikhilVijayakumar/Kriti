# rust_dev — Additional Suggestions

**Category:** Suggestions / Nice-to-Have  
**Severity:** Low-Medium  
**Date:** 2026-07-15

---

## Suggestion 1 — Add `cargo-audit` to `script/schema/03-security/` (Correct Domain)

**Current State:**
`script/schema/14-build/cargo-audit.manifest.yaml` exists but `cargo audit` is a **security** tool, not a build tool. It scans `Cargo.lock` for CVE vulnerabilities.

**Recommendation:**
- Move the manifest to `script/schema/03-security/cargo-audit.manifest.yaml`.
- Add a full `cargo-audit.schema.json` defining the output schema (`audit_pass: bool`, `vulnerability_count: int`, `critical_count: int`).
- Wire it to `sec-doc-rust-001` in the mapping.

---

## Suggestion 2 — Add `unsafe-code-scan` Script Schema

**Gap:** The proposal mandates `#![forbid(unsafe_code)]` in business logic crates but there is no script check enforcing this at the audit layer.

**Recommendation:**
- Create `script/schema/07-engineering/unsafe-code-scan.manifest.yaml`:
  ```yaml
  check: unsafe-code-scan
  description: >
    Scans all Rust source files for `unsafe` blocks and verifies that business-logic
    crates have `#![forbid(unsafe_code)]` at the crate root.
  executable: "grep -r 'unsafe' src/ --include='*.rs'"
  severity: critical
  ```
- Create a corresponding `unsafe-code-scan.schema.json` to define output metrics.
- Wire it into `script/mapping.yaml` under the `07-engineering` domain.

---

## Suggestion 3 — Add `crate-dependency-graph` Script Schema

**Gap:** Crate Architecture is mandated to have strict dependency direction (infrastructural → core, never core → infrastructural), but there is no automated check for this.

**Recommendation:**
- Create `script/schema/05-architecture/crate-dependency-graph.manifest.yaml`:
  ```yaml
  check: crate-dependency-graph
  description: >
    Uses `cargo metadata` to extract the crate dependency graph and checks that no
    business-logic or domain crates depend on infrastructural crates.
  executable: "cargo metadata --format-version 1"
  severity: error
  ```
- Wire to a new `arch-doc-rust-001` rule in `05-architecture.yaml`.

---

## Suggestion 4 — `00-domain-relationships.md` Should Document the New Rust-Specific Relationships

**File:** `00-domain-relationships.md`

The `00-domain-relationships.md` file defines cross-domain dependency flows. With 3 domains dropped and 12 new section slots added, several new relationships exist that are NOT documented:

| New Relationship | Description |
|---|---|
| `architecture/crate_architecture` → `feature-technical/crate_implementation` | Crate boundaries constrain how features are implemented |
| `architecture/trait_design` → `feature-technical/error_implementation` | Error types must implement system-level error traits |
| `engineering/ownership_patterns` → `feature-technical/crate_implementation` | Ownership policies flow down to implementations |
| `engineering/unsafe_guidelines` → `feature-technical/crate_implementation` | Unsafe policy is enforced at the implementation level |
| `qa/property_testing` → `feature-technical/crate_implementation` | Properties to test must be derivable from the implementation design |

**Recommendation:**
- Add a `## Rust-Specific Cross-Domain Relationships` section to `00-domain-relationships.md` documenting these new flows.

---

## Suggestion 5 — Add a `CONTRIBUTING.md` to `rust_dev` Documentation

**Gap:** `rust_dev` has a `SYSTEM.md`, `CHANGELOG.md`, and `migration-guide.md` but no guide for how to *extend* the system itself.

**Recommendation:**
- Create `CONTRIBUTING.md` at the root of `rust_dev/` with guidance on:
  - How to add a new generation template slot
  - How to add a new semantic audit rule
  - How to update the deterministic rules when adding a section
  - How to update `00-domain-relationships.md` when cross-domain dependencies change

---

## Suggestion 6 — `02-philosophy-standards.md` "Systems Philosophy Addendum" Should Be Position-Sensitive

**Current State:** The Systems Philosophy Addendum is appended at the very end of `02-philosophy-standards.md` after hundreds of lines of base content.

**Issue:** In a system like `rust_dev` where Rust's ownership model IS the philosophy (not an addendum), this buried placement is misleading. A new developer reading the philosophy standard would spend hundreds of lines on generic philosophy before reaching the Rust-specific principles.

**Recommendation:**
- Consider placing the Systems Philosophy Addendum **immediately after** the main philosophy sections (e.g., after the `guiding_principles` section) rather than at the very end.
- Alternatively, create a `02-philosophy-rust-addendum-standards.md` file specifically for Rust extensions.

---

## Suggestion 7 — Add `cargo fmt` Check to `script/schema/07-engineering/`

**Gap:** The proposal mentions code formatting as part of engineering standards, but `cargo fmt` is not represented in the script schemas.

**Recommendation:**
- Create `script/schema/07-engineering/cargo-fmt.manifest.yaml`:
  ```yaml
  check: cargo-fmt
  description: Verifies that all Rust source files are formatted according to rustfmt
  executable: "cargo fmt --all -- --check"
  severity: warning
  ```
- Wire this to a new engineering rule `eng-doc-rust-002` in `script/mapping.yaml`.
