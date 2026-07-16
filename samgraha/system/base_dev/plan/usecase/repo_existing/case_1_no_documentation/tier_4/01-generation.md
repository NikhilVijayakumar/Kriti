# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_1_no_documentation`
**Tier:** 4
**Domains:** prototype

## Context Available

Existing repo with real code but no documentation. Tiers 1–3 have completed. Tier 4 generation uses all upstream outputs plus real code as context.

**Key difference from `repo_new`:** Real code exists. Prototype should be buildable against the actual codebase — it should exercise real module interfaces, real data flows, real entry points. The prototype plan describes what to build against what exists, not a standalone exercise.

## Procedure

Generate a complete Prototype document from scratch using the document-level generation template.

### Generation

| Domain | Template | Key code-specific context |
|---|---|---|
| prototype | `templates/generation/document/11-prototype.md` | Actual entry points, module interfaces, data flows |

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** Tier 4 there has no code — Prototype invents a buildable exercise. This use case has real code — Prototype describes validation against actual modules.
- **vs. `repo_new/case_2_has_documention` / `repo_existing/case_2_has_documention`:** No difference — neither has pre-existing prototype docs.
