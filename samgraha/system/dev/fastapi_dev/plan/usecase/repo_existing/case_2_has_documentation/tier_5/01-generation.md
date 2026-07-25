# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_2_has_documentation`
**Tier:** 5
**Domains:** implementation

## Context Available

Existing repo with real code and existing non-conforming documentation. Tiers 1–4 have completed. Stage 1 is migration with real code verification.

## Procedure

| Domain | Target template | Code verification |
|---|---|---|
| implementation | `templates/generation/document/13-implementation.md` | Cross-reference existing implementation doc against actual code — flag gaps and inaccuracies |

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_existing/case_1_no_documentation`:** Stage 1 is migration, not generation. Existing doc changes the starting point.
