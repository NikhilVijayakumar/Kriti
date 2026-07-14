# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_1_no_documentation`
**Tier:** 5
**Domains:** implementation

## Context Available

Existing repo with real code but no documentation. Tiers 1–4 have completed. Tier 5 generation uses all upstream outputs plus real code as context.

**Key difference from `repo_new`:** Real code exists. Implementation should describe what exists vs. what needs to be added — a gap analysis, not a build-from-scratch plan. The document should reference actual modules, actual file paths, actual function names where relevant.

## Procedure

Generate a complete Implementation document from scratch using the document-level generation template.

### Generation

| Domain | Template | Key code-specific context |
|---|---|---|
| implementation | `templates/generation/document/13-implementation.md` | Actual codebase structure, what exists vs. what's missing |

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** Tier 5 there has no code — Implementation describes the planned build from scratch. This use case has real code — Implementation describes the gap between what exists and what's needed.
- **vs. `repo_new/case_2_has_documention` / `repo_existing/case_2_has_documention`:** No difference — neither has pre-existing implementation docs.
