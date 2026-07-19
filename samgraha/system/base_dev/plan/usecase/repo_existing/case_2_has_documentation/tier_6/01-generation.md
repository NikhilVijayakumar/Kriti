# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_2_has_documentation`
**Tier:** 6
**Domains:** qa

## Context Available

Existing repo with real code and existing non-conforming documentation. Tiers 1–5 have completed. Stage 1 is migration with real code verification.

## Procedure

| Domain | Target template | Code verification |
|---|---|---|
| qa | `templates/generation/document/12-qa.md` | Verify test coverage claims against actual test files |

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_existing/case_1_no_documentation`:** Stage 1 is migration, not generation.
