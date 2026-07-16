# fastapi_dev — Gap Analysis: Template Content is Placeholder-Only

**Category:** Gaps / Content Quality  
**Severity:** High  
**Date:** 2026-07-15

---

## Summary

The new FastAPI-specific generation templates created during the implementation phase are **stub files only** — single-line bracket placeholders. They cannot guide document generation and provide no meaningful authoring direction. This defeats the purpose of having specialized templates.

---

## Affected Files

| File | Current Content | Required Content |
|------|----------------|-----------------|
| `templates/generation/section/05-architecture/12-layered_architecture.md` | `[Define the module boundaries...]` (1 line) | Full template with headings, examples, required subsections |
| `templates/generation/section/07-engineering/09-versioning.md` | `[Define the API versioning strategy...]` (1 line) | Template with URL versioning vs header versioning guidance |
| `templates/generation/section/07-engineering/10-migration_strategy.md` | `[Define the database migration strategy...]` (1 line) | Template with Alembic workflow, schema evolution patterns |
| `templates/generation/section/10-feature-technical/18-layer_implementation.md` | `[Detail the specific implementation...]` (1 line) | Template with Router/Service/Repository section structure |
| `templates/generation/section/12-qa/10-api_testing.md` | `[Detail how endpoints are tested...]` (1 line) | Template with pytest fixtures, httpx client setup, status assertions |
| `templates/generation/section/13-implementation/08-feature_folder_structure.md` | `[Define the directory layout...]` (1 line) | Template with standard feature folder tree |
| `templates/generation/section/14-build/10-api_validation.md` | `[Specify how the API contract...]` (1 line) | Template with OpenAPI schema validation steps |
| `templates/generation/section/16-product-guide/07-development_workflow.md` | `[Guide developers on how to work...]` (1 line) | Template with step-by-step workflow |

---

## Required Standard for Templates

Compare against a well-formed template in `templates/generation/section/05-architecture/01-purpose.md` (4088 bytes) — it contains:
- A heading
- `minimum_content` guidance block
- A proper markdown template with named placeholders
- `Required subsections`, `Optional subsections`, `Required diagrams`, `Required cross-references`
- **Correct** and **Incorrect** examples
- Writing guidance (Tone, Voice, Structure, Audience, Do/Don't)

All 8 FastAPI-specific templates must be expanded to match this structure.

---

## Fix Required

Each stub template must be fully written out with:

1. **Section heading** matching the slot name
2. **Guidance block** (`minimum_content`, `length_guidance`, `diagram_requirements`)
3. **Markdown template** with named `[Placeholder]` fields
4. **Required/Optional subsections** declared
5. **Correct/Incorrect examples** specific to FastAPI backend context
6. **Writing guidance** (Tone, Voice, Audience, Do/Don't)
