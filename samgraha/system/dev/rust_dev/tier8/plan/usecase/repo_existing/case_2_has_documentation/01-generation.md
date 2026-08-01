# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_2_has_documentation`
**Tier:** 8
**Domains:** readme, product-guide

## Context Available

Existing repo with real code and existing non-conforming documentation. Tiers 1–7 have completed — all 11 upstream documents exist and have cleared their tier gates. Tier 8 is the final tier.

## Procedure

For each domain, migrate the existing document into the template shape, using real code as verification.

| Domain | Target template | Code verification |
|---|---|---|
| readme | `tier8/templates/generation/document/readme.md` | Verify file paths, commands, config against actual codebase |
| product-guide | `tier8/templates/generation/document/product-guide.md` | Verify feature descriptions against actual functionality |

**Product Guide special case:** Product Guide depends on everything — full-context migration from all already-completed domains.

## Within-Tier Ordering

No ordering constraint — both domains migrate in parallel.

## Output

Two documents, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_existing/case_1_no_documentation`:** Stage 1 is migration, not generation.
- **vs. `repo_new/case_2_has_documentation`:** Real code context for verification.
