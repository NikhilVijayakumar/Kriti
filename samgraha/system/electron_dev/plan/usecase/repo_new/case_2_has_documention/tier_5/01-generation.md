# Stage 1 — Generate or Migrate

**Use case:** `repo_new/case_2_has_documention`
**Tier:** 5
**Domains:** implementation

## Context Available

New repo with some pre-existing hand-written documentation. No code. Tiers 1–4 have completed.

## Procedure

| Domain | Action if docs exist | Action if no docs |
|---|---|---|
| implementation | Migrate into `templates/generation/document/13-implementation.md` shape | Generate from scratch |

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** Stage 1 is migration, not pure generation.
