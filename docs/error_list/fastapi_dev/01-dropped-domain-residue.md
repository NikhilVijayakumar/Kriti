# fastapi_dev — Gap Analysis: Dropped Domain Residue

**Category:** Gaps / Correctness  
**Severity:** High  
**Date:** 2026-07-15

---

## Summary

The `fastapi_dev` implementation was supposed to drop `06-design` and `09-feature-design` completely. While the `documentation-standards/` files were deleted, several artefacts from the old 16-domain `base_dev` clone were **not cleaned up**. These are orphaned references and files that belong to dropped domains.

---

## Gap 1 — `script/mapping.yaml` References Dropped Domains

**File:** `script/mapping.yaml`

The mapping file still contains explicit entries for `06-design` and `09-feature-design`:

```yaml
# Line 23
- { audit_type: deterministic, domain: 06-design, rule_id: des-doc-006 }
# Line 26
- { audit_type: deterministic, domain: 09-feature-design, rule_id: fd-doc-006 }
# Line 40
- { audit_type: deterministic, domain: 09-feature-design, rule_id: fd-doc-009 }
# Line 139-143
- check: design-tokens-in-implementation
  domain: 06-design
  ...
```

These are dead references. If the audit engine ever resolves these, it will fail to find the domain.

**Fix Required:**
- Remove all `06-design` and `09-feature-design` entries from `mappings` in `script/mapping.yaml`.
- The `design-tokens-in-implementation` check block (lines 138–143) must also be deleted entirely.

---

## Gap 2 — `script/mapping.yaml` References `11-prototype`

**File:** `script/mapping.yaml`

`fastapi_dev` keeps `11-prototype` (unlike `rust_dev`). However, the mock-api-runs check references the prototype domain which **is a UI/frontend workflow** (mock APIs, visual mockups). For a backend system, this check is misleading.

```yaml
# Line 122-127
- check: mock-api-runs
  domain: 11-prototype
  ...
```

**Fix Required:**
- Either redefine `mock-api-runs` for FastAPI as "prototype endpoint runs" (i.e., a live Swagger/ReDoc check that the dev server starts), or rename the check to `prototype-endpoint-runs` for clarity.

---

## Gap 3 — `audit/deterministic/document/` Still Contains Dropped Domain YAMLs

**Directory:** `audit/deterministic/document/`

The following files exist but should have been removed:
- `06-design.yaml`
- `06-design-relationships.yaml`
- `09-feature-design.yaml`
- `09-feature-design-relationships.yaml`

**Fix Required:**
- Delete all four files.

---

## Gap 4 — `audit/semantic/section/11-prototype` Contains UI-Oriented Checks

**Directory:** `audit/semantic/section/11-prototype/`

Contains `01-scope.md`, `02-mock_apis.md`, `03-data_model.md`, `04-purpose.md`, `05-constraints.md`, `06-traceability.md`.

These are carried forward from `base_dev` and reference generic or UI-oriented prototype concerns. There are no FastAPI-specific API prototype checks here (e.g., validating that Swagger `/docs` endpoint is accessible, or that the prototype OpenAPI spec matches the implementation spec).

**Fix Required:**
- Update prototype audit checks to be backend-specific: OpenAPI contract validation, running the prototype server, verifying response schemas.

---

## Gap 5 — `script/schema/06-design/` Still Exists

**Directory:** `script/schema/06-design/`

Contains:
- `design-tokens-in-implementation.manifest.yaml`
- `design-tokens-in-implementation.schema.json`

This is a frontend/UI check that has no place in a pure backend system. Design tokens are irrelevant to FastAPI.

**Fix Required:**
- Delete `script/schema/06-design/` entirely.

---

## Gap 6 — `templates/generation/section/11-prototype/` Contains UI-Oriented Templates

**Directory:** `templates/generation/section/11-prototype/`

Contains templates (`01-purpose.md`, `02-scope.md`, `03-mock-apis.md`, etc.) that were not updated with FastAPI-specific content. They remain as generic placeholders with no backend-engineering guidance.

**Fix Required:**
- Rewrite prototype templates to address FastAPI API prototyping:
  - Validating endpoint schemas with Swagger UI
  - Creating mock endpoints that return static Pydantic response models
  - Documenting the OpenAPI spec structure before implementation
