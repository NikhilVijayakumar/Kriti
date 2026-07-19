# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_2_has_documentation`
**Tier:** 1
**Domains:** vision, philosophy

## Context Available

Existing repo with real code and existing non-conforming documentation. Tier 1 domains have hand-written docs that don't conform to `documentation-standards/`. Stage 1 is migration — restructure existing prose into the template shape.

**Key difference from `case_1_no_documentation`:** Every domain starts with existing docs (Path B). No generation from scratch. The existing content is preserved and restructured, not discarded.

## Procedure

For each domain, migrate the existing document into the template shape.

### Per-Domain Migration

| Domain | Existing doc | Target template |
|---|---|---|
| vision | Existing Vision doc | `templates/generation/document/01-vision.md` |
| philosophy | Existing Philosophy doc | `templates/generation/document/02-philosophy.md` |

### Migration Process

1. Read the existing document.
2. Map existing content to the generation template's required sections.
3. Restructure: correct section order, fill missing sections using template guidance, remove content that belongs in a different domain.
4. Output: template-shaped document with original content preserved where it fits.

## Within-Tier Ordering

No ordering constraint — both domains migrate in parallel.

## Output

Two documents, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** Stage 1 is migration, not generation. Every domain has existing docs.
- **vs. `repo_existing/case_1_no_documentation`:** Stage 1 is migration, not generation. Same code context, but existing docs change the starting point.
- **vs. `repo_new/case_2_has_documentation`:** Identical at Tier 1 — no code context applies to Vision/Philosophy.
