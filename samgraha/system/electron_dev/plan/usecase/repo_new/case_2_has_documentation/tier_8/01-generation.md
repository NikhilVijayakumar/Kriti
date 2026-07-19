# Stage 1 — Generate or Migrate

**Use case:** `repo_new/case_2_has_documentation`
**Tier:** 8
**Domains:** readme, product-guide

## Context Available

New repo with some pre-existing hand-written documentation. No code. Tiers 1–7 have completed — all 14 upstream documents exist and have cleared their tier gates. Tier 8 is the final tier.

## Procedure

For each domain, check if pre-existing documentation exists.

| Domain | Action if docs exist | Action if no docs |
|---|---|---|
| readme | Migrate into `templates/generation/document/16-readme.md` shape | Generate from scratch |
| product-guide | Migrate into `templates/generation/document/17-product-guide.md` shape | Generate from scratch |

**Product Guide special case:** Product Guide depends on everything — full-context generation/migration from all already-completed domains.

## Within-Tier Ordering

No ordering constraint — both domains process in parallel.

## Output

Two documents, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** Stage 1 is migration, not pure generation.
- **vs. `repo_existing/case_2_has_documentation`:** No code context — identical procedure.
