# fastapi_dev — Gap Analysis: Deterministic Audit YAMLs Not Updated

**Category:** Gaps / Completeness  
**Severity:** Medium  
**Date:** 2026-07-15

---

## Summary

The `audit/deterministic/document/` directory still contains YAML rule files for the two dropped domains (`06-design`, `09-feature-design`). Additionally, the deterministic rules for **kept** domains were not updated to add FastAPI-specific checks. They remain identical to `base_dev`.

---

## Gap 1 — Dropped Domain YAMLs Still Present

**Directory:** `audit/deterministic/document/`

The following files should not exist in `fastapi_dev`:

| File | Status |
|------|--------|
| `06-design.yaml` | ❌ Should be deleted |
| `06-design-relationships.yaml` | ❌ Should be deleted |
| `09-feature-design.yaml` | ❌ Should be deleted |
| `09-feature-design-relationships.yaml` | ❌ Should be deleted |

---

## Gap 2 — Relationship YAMLs Reference Dropped Domains

**Directory:** `audit/deterministic/document/`

Several relationship YAML files still reference `06-design` and `09-feature-design` as valid cross-references or derivation sources. For example:
- `05-architecture-relationships.yaml` may reference feature-design
- `10-feature-technical-relationships.yaml` has 8023 bytes — unusually large, suggesting it references both feature-design and feature-technical as peer domains

**Fix Required:**
- Review all `-relationships.yaml` files and remove any reference to `06-design` or `09-feature-design`.
- Pay particular attention to `10-feature-technical-relationships.yaml` as it is the most complex.

---

## Gap 3 — No FastAPI-Specific Deterministic Rules Added to Kept Domains

The deterministic rule YAMLs for kept domains were not modified to add FastAPI-specific structural checks. For example:

| Domain YAML | What Could Be Added |
|-------------|---------------------|
| `07-engineering.yaml` | Rule: `07-engineering` must contain a section on async/await patterns |
| `07-engineering.yaml` | Rule: `07-engineering` must document error-handling strategy |
| `05-architecture.yaml` | Rule: `05-architecture` must contain `12-layered_architecture` section |
| `12-qa.yaml` | Rule: `12-qa` must contain an `api-testing` section |
| `14-build.yaml` | Rule: `14-build` must contain API contract validation steps |

**Fix Required:**
- For each key domain, add at minimum 1–2 new deterministic rules that enforce the presence of the FastAPI-specific sections added during implementation.

---

## Gap 4 — `audit/deterministic/section/` Not Updated

**Directory:** `audit/deterministic/section/`

The per-section structural rule YAML files (which validate structure within each document section) were not reviewed or updated for any domain. These drive the `> *Structural rules: ...*.yaml` directives in the documentation standards. Since the new backend sections don't have structural rule references, there is no enforcement of the required content in those new sections.

**Fix Required:**
- For each new backend section added to documentation standards, create a corresponding `audit/deterministic/section/{domain}/{NN-name}.yaml` file that enforces minimum content, required headings, and length guidance.
