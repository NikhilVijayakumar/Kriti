# rust_dev — Improvements and Optimization Suggestions

**Category:** Improvements / Optimizations  
**Severity:** Medium  
**Date:** 2026-07-15

---

## Improvement 1 — `script/policy.yaml` Should Have Rust-Specific Cache Strategy Overrides

**File:** `script/policy.yaml`

The current additions to `policy.yaml` added:
```yaml
- check: cargo-audit
  strategy: ttl
  max_age_seconds: 86400
- check: cargo-clippy
  strategy: always_rerun
```

This is good but incomplete. For a Rust systems project, the following additional checks should have policy entries:

| Proposed Check | Suggested Strategy | Reason |
|---|---|---|
| `crate-dependency-graph` | `fingerprint` | Only re-run when `Cargo.toml` files change |
| `unsafe-code-scan` | `always_rerun` | Code safety checks should never be cached |
| `module-boundary-diff` | `fingerprint` | Only when crate/module files change |

**Fix Required:**
- Add the three additional check policies to `script/policy.yaml`.

---

## Improvement 2 — `02-philosophy-standards.md` Addendum Should Reference Rust Ownership Model Explicitly

**File:** `documentation-standards/02-philosophy-standards.md`

The Systems Philosophy Addendum was added with three principles. However, the most foundational principle of Rust engineering — **Ownership over garbage collection** — is missing. Users coming from GC languages (Go, Python, Java) need the philosophy to explicitly explain WHY ownership exists and why cloning is discouraged.

Suggested addition:
```markdown
* **Ownership over Garbage Collection:** We leverage Rust's ownership system as a design tool, not just a compiler requirement. Ownership makes resource lifecycles explicit and eliminates an entire class of bugs at compile time.
```

**Fix Required:**
- Add the "Ownership over GC" principle to the Systems Philosophy Addendum.

---

## Improvement 3 — New Templates Should Cross-Reference Each Other

**Issue:** The 12 new Rust generation templates at various domains are standalone, with no cross-reference declarations.

Well-formed base_dev templates (e.g., `01-purpose.md`) include `**Required cross-references:**`. The new Rust templates declare them, but the template body's `Required cross-references` entries do not map to the same relationship IDs that appear in the relationship YAML files.

| Template | Current Cross-Reference | Should Match Relationship ID |
|---|---|---|
| `05-architecture/12-crate_architecture.md` | `Component Model(03)` | `arch-component-model-derives-feature-technical` |
| `10-feature-technical/18-crate_implementation.md` | `Architecture Crate Architecture(12)` | No matching relationship in `05-architecture-relationships.yaml` |
| `07-engineering/09-ownership_patterns.md` | none declared | Should reference Engineering → Architecture |

**Fix Required:**
- Add a relationship entry to `05-architecture-relationships.yaml` for `crate-architecture` → `component_model`.
- Align the `Required cross-references` in templates with actual relationship IDs in the relationship YAML files.

---

## Improvement 4 — `calculation/` Directory Should Have Rust-Specific Severity Weights

**Directory:** `calculation/`

The proposal states: "Weight and severity adjustments happen inside `audit/deterministic/{domain}/*.yaml` files." However, the calculation layer should also be aware of which domains are **higher-stakes** in a systems context. Currently all domain weights in the calculation layer appear to treat all 13 active domains equally.

For `rust_dev`, the following domains should carry elevated weight:
| Domain | Reason for Elevated Weight |
|---|---|
| `07-engineering` | Ownership/unsafe violations are catastrophic |
| `05-architecture` | Crate boundary violations propagate across the workspace |
| `03-security` | CVE vulnerabilities and unsafe code are existential |
| `10-feature-technical` | Incorrect error propagation (`unwrap()`) causes panics in production |

**Fix Required:**
- Review `calculation/` to understand if per-domain weights exist.
- If so, increase weights for the four domains above.
- If not, document this as a future capability gap.

---

## Improvement 5 — `SYSTEM.md` Should Include Domain Tier Map

**File:** `SYSTEM.md`

The current `SYSTEM.md` is:
```toml
[system]
id = "rust_dev"
base = "base_dev"
version = "1.0.0"
domains = 13
dropped_from_base = ["06-design", "09-feature-design", "11-prototype"]
technology = "Rust / Cargo"
methodology = "Systems Engineering"
```

This is helpful but doesn't include the tier reordering that is one of the key differences between `rust_dev` and `base_dev`. A developer opening `rust_dev` for the first time has no quick reference for the authoring order.

**Fix Required:**
- Add a `domain_tiers` block to `SYSTEM.md`:
```toml
[domain_tiers]
tier_1 = ["01-vision", "02-philosophy"]
tier_2 = ["03-security", "04-feature", "05-architecture", "07-engineering", "08-external-context"]
tier_3 = ["10-feature-technical"]
tier_4 = ["13-implementation"]
tier_5 = ["12-qa"]
tier_6 = ["14-build"]
tier_7 = ["15-readme", "16-product-guide"]
```

---

## Improvement 6 — `migration-guide.md` Is Too Brief

**File:** `migration-guide.md`

The current migration guide (439 bytes) is a 3-step list. It does not address:
- How to rename existing docs when slot numbers shift (e.g., slot 09 shifts to 09-ownership_patterns)
- How to handle existing feature design documents that must be absorbed into `04-feature` and `10-feature-technical`
- What happens to existing `11-prototype` documents (do they map to `10-feature-technical/18-crate_implementation`?)

**Fix Required:**
- Expand `migration-guide.md` to include:
  - A `Domain Mapping` table showing where each dropped domain's content should live in `rust_dev`
  - Step-by-step instructions for migrating existing prototype documentation
