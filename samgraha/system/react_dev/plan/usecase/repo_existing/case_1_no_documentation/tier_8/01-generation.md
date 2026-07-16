# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_1_no_documentation`
**Tier:** 8
**Domains:** readme, product-guide

## Context Available

Existing repo with real code but no documentation. Tiers 1–7 have completed — all 14 upstream documents exist and have cleared their tier gates. Tier 8 is the final tier.

**Key difference from `repo_new`:** Real code exists. README should reference actual file paths, actual commands, actual configuration. Product Guide should reference actual features visible in the codebase. Both documents describe the real product, not a planned one.

## Procedure

For each domain in this tier, generate a complete document from scratch using the document-level generation template.

### Per-Domain Generation

| Domain | Template | Key code-specific context |
|---|---|---|
| readme | `templates/generation/document/16-readme.md` | Actual file paths, commands, configuration, entry points |
| product-guide | `templates/generation/document/17-product-guide.md` | All 14 upstream docs + actual features visible in code |

**Product Guide special case:** Product Guide depends on everything — full-context generation from all already-completed domains.

## Within-Tier Ordering

No ordering constraint — both domains generate in parallel.

## Output

Two documents, ready for stage 2 (audit).

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** Tier 8 there has no code — README and Product Guide describe the planned product. This use case has real code — both documents describe the actual product with real file paths and commands.
- **vs. `repo_new/case_2_has_documention` / `repo_existing/case_2_has_documention`:** No difference — neither has pre-existing README/Product Guide docs.
