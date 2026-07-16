# rust_dev — Bug Report: Audit Rule ID and Structural Issues

**Category:** Bugs / Correctness  
**Severity:** HIGH  
**Date:** 2026-07-15

---

## Summary

Multiple deterministic section audit YAML files have incorrect rule ID prefixes, duplicate slot numbers, invalid severity values, and inconsistent header structures. These issues will cause audit tooling to misroute rules, load wrong files, or reject invalid severity values.

---

## Bug 1 — Wrong Rule ID Prefix (8 files)

Section rules follow the pattern `{domain-abbrev}-sec-{name}-{number}`. These 8 files use bare `sec-` instead of their domain prefix:

| File | Current Rule ID | Correct Rule ID |
|------|----------------|-----------------|
| `audit/deterministic/section/01-vision/05-systems_vision.yaml` | `sec-systems-vision-001` | `vis-sec-systems-vision-001` |
| `audit/deterministic/section/04-feature/10-systems_feature_definition.yaml` | `sec-systems-feature-definition-001` | `feat-sec-systems-feature-definition-001` |
| `audit/deterministic/section/07-engineering/09-ownership_patterns.yaml` | `sec-ownership-patterns-001` | `eng-sec-ownership-patterns-001` |
| `audit/deterministic/section/07-engineering/10-async_patterns.yaml` | `sec-async-patterns-001` | `eng-sec-async-patterns-001` |
| `audit/deterministic/section/07-engineering/11-unsafe_guidelines.yaml` | `sec-unsafe-guidelines-001` | `eng-sec-unsafe-guidelines-001` |
| `audit/deterministic/section/08-external-context/06-systems_technology.yaml` | `sec-systems-technology-001` | `ext-sec-systems-technology-001` |
| `audit/deterministic/section/12-qa/10-property_testing.yaml` | `sec-property-testing-001` | `qa-sec-property-testing-001` |
| `audit/deterministic/section/12-qa/11-benchmark_testing.yaml` | `sec-benchmark-testing-001` | `qa-sec-benchmark-testing-001` |

**Impact:** Audit tooling that resolves rules by ID will fail to find these rules. The `consumed_by` references in `mapping.yaml` cannot match bare `sec-` prefixed IDs.

**Fix Required:**
- Prefix all 8 rule IDs with their domain abbreviation.

---

## Bug 2 — Duplicate Section Number in `04-feature`

**Files:**
- `audit/deterministic/section/04-feature/10-systems_feature_definition.yaml`
- `audit/deterministic/section/04-feature/10-future_extensions.yaml`

Two files share slot number `10`. Slot-sequential tools will load the wrong file.

**Fix Required:**
- Renumber `10-future_extensions.yaml` to `12-future_extensions.yaml` (or renumber `systems_feature_definition` to `11`).

---

## Bug 3 — Invalid `suggestion` Severity (10 occurrences)

Standard valid severities are `error`, `warning`, `critical`. These files use non-standard `suggestion`:

| File | Line(s) |
|------|---------|
| `audit/deterministic/section/01-vision/06-pillars.yaml` | 13, 38 |
| `audit/deterministic/section/01-vision/07-philosophy.yaml` | 13, 38 |
| `audit/deterministic/section/01-vision/08-guiding_principles.yaml` | 13, 38 |
| `audit/deterministic/section/01-vision/09-success_criteria.yaml` | 13 |
| `audit/deterministic/section/01-vision/10-traceability.yaml` | 13 |
| `audit/deterministic/section/05-architecture/10-operational_readiness.yaml` | 13 |
| `audit/deterministic/section/05-architecture/11-observability.yaml` | 13 |

**Fix Required:**
- Either change `suggestion` to `warning` in all 10 occurrences, or update the audit schema to accept `suggestion` as a valid severity level.

---

## Bug 4 — Inconsistent YAML Header Structure in Section Rules

Two distinct header formats exist across section rule files:

**Structure A (original — 5+ fields):**
```yaml
header:
  system_id: rust_dev
  domain: "01-vision"
  section_type: purpose
  standard_id: "01-vision-standards.md"
  scope: document
  kind: deterministic
```

**Structure B (newer — 4 fields, missing `section_type` and `scope`):**
```yaml
header:
  system_id: rust_dev
  standard_id: "12-qa-standards.md"
  domain: "12-qa"
  section: property_testing
```

Structure B files are in: `12-qa` (06-11), `13-implementation` (05-06), `14-build` (05-08), `16-product-guide` (07-08).

**Impact:** Any tool that reads `header.section_type` or `header.scope` will get null for Structure B files.

**Fix Required:**
- Normalize all headers to Structure A (add `section_type` and `scope` fields to Structure B files).

---

## Bug 5 — `cargo-audit` Manifest Placed in Wrong Domain

**File:** `script/schema/14-build/cargo-audit.manifest.yaml`

`cargo audit` scans `Cargo.lock` for CVE vulnerabilities — this is a **security** check, not a build check. It belongs in `script/schema/03-security/`.

**Fix Required:**
- Move to `script/schema/03-security/cargo-audit.manifest.yaml`.

---

## Bug 6 — Documentation Standards Reference Dropped Domains

**File:** `documentation-standards/12-qa-standards.md`

References `Design(06)` and `Feature Design(09)` throughout (E2E testing, relationships, inputs). These domains were dropped from `rust_dev`. The QA standard should not reference non-existent domains.

**Fix Required:**
- Remove or update all references to domains 06 and 09 in the QA standards.

---

## Bug 7 — `systems_*` Rule ID Naming Convention Inconsistent

Even among correctly-prefixed files, the convention for including the concept name varies:

| Pattern | Example |
|---------|---------|
| Short (no suffix) | `phil-sec-systems-001` |
| Full concept name | `vis-sec-systems-vision-001` |
| Full concept name | `sec-sec-systems-security-001` (if fixed) |

**Fix Required:**
- Adopt one convention (recommend: full concept name for clarity) and normalize all `systems_*` rule IDs.

---

## Summary

| # | Bug | Severity | Files Affected |
|---|-----|----------|----------------|
| 1 | Wrong rule ID prefix | HIGH | 8 |
| 2 | Duplicate section number | HIGH | 2 |
| 3 | Invalid `suggestion` severity | MEDIUM | 7 (10 occurrences) |
| 4 | Inconsistent header structure | MEDIUM | ~20 |
| 5 | Wrong domain for cargo-audit | MEDIUM | 1 |
| 6 | Standards reference dropped domains | MEDIUM | 1 |
| 7 | Inconsistent naming convention | LOW | ~5 |
