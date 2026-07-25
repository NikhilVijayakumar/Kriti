# Stage 1 — Generate or Migrate

**Use case:** `repo_new/case_2_has_documentation`
**Tier:** 3

## Context Available

New repo with some pre-existing hand-written documentation. No code. Tiers 1–2 have completed. Tier 3 domains may have existing docs that need migration, or may need generation from scratch.

## Procedure

For each domain, check if pre-existing documentation exists.

| Domain | Action if docs exist | Action if no docs |
|---|---|---|
| feature-technical | Migrate into `templates/generation/document/10-feature-technical.md` shape | Generate from scratch |

## Within-Tier Ordering

No ordering constraint — both domains process in parallel.

## Output

Two documents, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** Stage 1 is migration, not pure generation.
- **vs. `repo_existing/case_2_has_documentation`:** No code context — identical procedure.
