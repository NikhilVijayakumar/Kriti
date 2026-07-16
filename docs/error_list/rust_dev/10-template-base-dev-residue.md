# rust_dev — Bug Report: Base_Dev Residue in Rust Templates

**Category:** Bugs / Incorrect Content  
**Severity:** HIGH  
**Date:** 2026-07-15

---

## Summary

Several generation templates contain examples, references, and patterns from other languages (TypeScript, Python, Spring Boot/Java) that are incorrect for a Rust-specific system. These were inherited from `base_dev` and not updated during the Rust specialization.

---

## Bug 1 — TypeScript/ESLint Example in `code_standards.md`

**File:** `templates/generation/section/07-engineering/06-code_standards.md` (lines ~42-43)

**Current "correct" example:**
```
The project should follow the TypeScript Official Style Guide.
Use ESLint to enforce coding standards.
```

**Fix Required:**
Replace with Rust equivalents:
```
The project should follow the Rust Style Guide (rustfmt defaults).
Use `cargo clippy --all-targets --all-features -- -D warnings` to enforce lint standards.
Use `rustfmt` to enforce formatting.
```

---

## Bug 2 — Spring Boot/Java Reference in `system_overview.md`

**File:** `templates/generation/section/05-architecture/02-system_overview.md` (lines ~37-38)

**Current "incorrect" example includes:**
```
"Apache Kafka 3.4 with Spring Boot 3.1" ... "PostgreSQL 15"
```

**Problem:** Spring Boot is a Java/JVM framework. While Kafka is language-agnostic, Spring Boot has no place in a Rust architecture document.

**Fix Required:**
Replace with Rust ecosystem references:
```
"Tokio 1.x runtime with Axum 0.7" ... "sqlx with PostgreSQL 15"
```

---

## Bug 3 — Python Reference in `engineering/rationale.md`

**File:** `templates/generation/section/07-engineering/02-rationale.md` (lines ~34-36)

**Current "correct" example:**
```
Project Alpha uses Python 3.12+
```

**Fix Required:**
Replace with:
```
Project Alpha uses Rust 1.75+ (edition 2021)
```

---

## Bug 4 — Generic "DataSync" Product in Vision `purpose.md`

**File:** `templates/generation/section/01-vision/01-purpose.md` (line ~28)

**Current example:** Uses "DataSync" as the product name — a generic data-integration product.

**Fix Required:**
Use a Rust-appropriate example product name, e.g.:
- "RustFS" (filesystem)
- "PacketForge" (networking)
- "DataPipe CLI" (CLI tool)

---

## Bug 5 — Generic Service-Oriented Components in `component_model.md`

**File:** `templates/generation/section/05-architecture/03-component_model.md`

**Current examples:**
```
"Ingestion Service" / "Transform Engine"
```

**Problem:** These are generic distributed-system terms. For Rust, the component model should demonstrate:
- Trait-based decomposition
- Ownership boundaries between crates
- `Send + Sync` constraints
- Enum dispatch vs. trait objects

**Fix Required:**
Replace with Rust-specific component examples that demonstrate ownership/trait patterns.

---

## Bug 6 — Invalid "Incorrect" Example in `success_criteria.md`

**File:** `templates/generation/section/01-vision/09-success_criteria.md`

**Current "incorrect" examples:**
```
"API response time under 200ms" ... "code coverage above 80%"
```

**Problem:** These ARE valid success metrics for many Rust projects (especially performance-critical systems). Marking them as "incorrect" is misleading.

**Fix Required:**
Replace with genuinely poor metrics:
```
"Number of lines of code" ... "Number of GitHub stars" ... "Lines of comments per function"
```

---

## Bug 7 — Metadata Leak in Feature Generation Templates

**Files:**
- `templates/generation/section/04-feature/01-purpose.md`
- `templates/generation/section/04-feature/02-functional_requirements.md`
- `templates/generation/section/04-feature/03-acceptance_criteria.md`

**Problem:** These templates include internal metadata blocks in the rendered output:
```markdown
> **semantic_type:** `purpose`
> **scope:** [Why this feature exists]
> **generation_rules:**
> - [derivation rule]
```

This metadata (`semantic_type`, `scope`, `out_of_scope`, `contributes`, `relationships`, `responsibilities`, `generation_rules`) is internal configuration for the generation engine and should NOT appear in user-facing document output.

**Fix Required:**
- Wrap metadata in comment syntax (`<!-- ... -->`) or move to YAML front-matter.
- Ensure rendered output strips metadata blocks.

---

## Summary

| # | File | Issue | Severity |
|---|------|-------|----------|
| 1 | `07-engineering/06-code_standards.md` | TypeScript/ESLint example | HIGH |
| 2 | `05-architecture/02-system_overview.md` | Spring Boot reference | HIGH |
| 3 | `07-engineering/02-rationale.md` | Python 3.12+ reference | HIGH |
| 4 | `01-vision/01-purpose.md` | Generic product name | LOW |
| 5 | `05-architecture/03-component_model.md` | No Rust component patterns | MEDIUM |
| 6 | `01-vision/09-success_criteria.md` | Valid metrics marked wrong | LOW |
| 7 | `04-feature/01-03-*.md` | Internal metadata in output | MEDIUM |
