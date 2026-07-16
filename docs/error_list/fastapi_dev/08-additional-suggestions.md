# fastapi_dev — Additional Suggestions

**Category:** Suggestions / Future Work  
**Severity:** Low–Medium  
**Date:** 2026-07-15

---

## Suggestion 1 — Create a FastAPI-Specific External Reference Isolation Check

The proposal explicitly flagged external reference isolation as future work:

> *"Verification: This leak-check is a natural fit for the `script/` audit pipeline (same shape as `secret-scan`). Currently unenforced — flagged as future work."*

This is never implemented. A `script/schema/` manifest + schema pair should be created:

**Proposed file:** `script/schema/03-security/external-ref-isolation.manifest.yaml`

```yaml
check: external-ref-isolation
description: >
  Scans all documentation-standards/ files for references to external
  system names (Astra, Prati, Prana, etc.) and external file paths.
patterns:
  - "\\bAstra\\b"
  - "\\bPrati\\b"
  - "\\bPrana\\b"
  - "E:\\\\Python\\\\"
severity: error
```

This would enforce the MANDATORY rule from the proposal without relying on manual review.

---

## Suggestion 2 — Create a FastAPI `CHANGELOG.md`

There is no record of what changed from `base_dev` to `fastapi_dev`. A `CHANGELOG.md` at the root of `fastapi_dev/` would help maintainers understand:

- Which domains were dropped and why
- Which new slots were added and in which tier
- Which standards were modified vs kept

This is especially important when `base_dev` evolves and changes need to be selectively propagated (per the Maintenance Policy in the Evolution Proposal).

**Proposed location:** `E:\Python\Kriti\samgraha\system\fastapi_dev\CHANGELOG.md`

---

## Suggestion 3 — Add a FastAPI-Specific `script/schema/` Manifest for `openapi-schema-valid`

The proposal lists `10-api_validation.md` as a new build template for "API contract validation, schema checks." This implies a new script check. The check schema should be created:

**Proposed:** `script/schema/14-build/openapi-schema-valid.manifest.yaml`

This check would:
- Parse the FastAPI app's auto-generated OpenAPI JSON
- Validate it against a project-defined contract baseline
- Diff new endpoints against documented ones in `16-product-guide`

---

## Suggestion 4 — Prototype Domain Should Have an API-Centric Audit Approach

Since `fastapi_dev` **keeps** the `11-prototype` domain (unlike `rust_dev`), it should be renamed conceptually to reflect its backend purpose. The files inside `templates/generation/section/11-prototype/` (`02-scope.md`, `03-mock-apis.md`) use frontend-oriented language.

**Suggested rename/rethink:**
- `03-mock-apis.md` → `03-prototype-endpoints.md` — focusing on FastAPI prototype routers with static responses
- Update `01-purpose.md` to state that backend prototypes use live FastAPI routes with hardcoded Pydantic responses, not visual mockups

---

## Suggestion 5 — Add a `migration-guide.md` for Upgrading Projects

When a project using `base_dev` wants to switch to `fastapi_dev`, there is no migration guide. A `migration-guide.md` could document:

1. Which document sections are no longer required (06-design, 09-feature-design)
2. Which new sections to author
3. How to update the repository's `[documentation] system = "fastapi_dev"` config
4. What new audit rules will now apply

**Proposed location:** `E:\Python\Kriti\samgraha\system\fastapi_dev\migration-guide.md`

---

## Suggestion 6 — `templates/generation/section/13-implementation/08-feature_folder_structure.md` Should Include a Standard Folder Tree

The current stub says `[Define the directory layout...]`. A good standard for FastAPI feature folder structure should be documented here. **Suggested canonical layout:**

```
{feature}/
├── __init__.py
├── router.py          # FastAPI router, HTTP-only
├── service.py         # Business logic
├── repository.py      # Data access (SQLAlchemy)
├── schemas.py         # Pydantic request/response models
├── models.py          # SQLAlchemy ORM models
├── dependencies.py    # DI provider functions
└── exceptions.py      # Feature-specific exception types
```

This should be embedded directly into the template as the "Correct" example.

---

## Suggestion 7 — Cross-Link the QA Section 12 `Related` Links to Remove `09-feature-design`

**File:** `documentation-standards/12-qa-standards.md` (viewed at the tail of generation)

The `Related` section at the bottom of QA standards still has:
```
- [Feature Design Standard](09-feature-design-standards.md) — defines how Implementation should look
```

Since `09-feature-design-standards.md` was deleted, this is a **broken link**. It should be removed or replaced with the appropriate FastAPI documentation that serves the same purpose.

**Same issue likely exists in:**
- `documentation-standards/13-implementation-standards.md` (references feature-design as a derivation source)
- `documentation-standards/10-feature-technical-standards.md` (may reference feature-design as a peer)

**Fix Required:**
- Search all `documentation-standards/*.md` files for references to `09-feature-design-standards.md` and `06-design-standards.md` and remove or replace them.
