# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_2_has_documention`
**Tier:** 7
**Domains:** build

## Context Available

Existing repo with real code and existing non-conforming documentation. Tiers 1–6 have completed. Stage 1 is migration with real code verification.

## Procedure

| Domain | Target template | Code verification |
|---|---|---|
| build | `templates/generation/document/14-build.md` | Verify CI/CD claims against actual config files |

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_existing/case_1_no_documentation`:** Stage 1 is migration, not generation.
