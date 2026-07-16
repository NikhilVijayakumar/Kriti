# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_2_has_documention`
**Tier:** 3
**Domains:** feature-design, feature-technical

## Context Available

Existing repo with real code and existing non-conforming documentation. Tiers 1–2 have completed. Stage 1 is migration with real code verification.

## Procedure

| Domain | Target template | Code verification |
|---|---|---|
| feature-design | `templates/generation/document/09-feature-design.md` | Check specs against actual UI components |
| feature-technical | `templates/generation/document/10-feature-technical.md` | Check specs against actual module interfaces |

## Within-Tier Ordering

No ordering constraint — both domains migrate in parallel.

## Output

Two documents, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_existing/case_1_no_documentation`:** Stage 1 is migration, not generation.
- **vs. `repo_new/case_2_has_documention`:** Real code context for verification.
