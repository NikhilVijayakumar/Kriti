# Stage 1 — Generate or Migrate

**Use case:** `repo_new/case_2_has_documention`
**Tier:** 6
**Domains:** qa

## Context Available

New repo with some pre-existing hand-written documentation. No code. Tiers 1–5 have completed.

## Procedure

| Domain | Action if docs exist | Action if no docs |
|---|---|---|
| qa | Migrate into `templates/generation/document/12-qa.md` shape | Generate from scratch |

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** Stage 1 is migration, not pure generation.
