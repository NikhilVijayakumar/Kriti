# Stage 1 — Generate or Migrate

**Use case:** `repo_new/case_1_no_documentation`
**Tier:** 8
**Domains:** readme, product-guide

## Context Available

New repo, no documentation, no code. Tiers 1–7 have completed — all 11 upstream documents exist and have cleared their tier gates. Tier 8 is the final tier: Product Guide cannot be generated accurately until everything upstream, all the way through Build, is real and compliant.

## Procedure

For each domain in this tier, generate a complete document from scratch using the document-level generation template.

### Upstream Context (from completed tiers)

All 11 upstream documents are available as context. This is the most context-rich generation step — every domain's output feeds into README and Product Guide.

- **README** references Vision (for product description) and requires Build (for installation/setup instructions)
- **Product Guide** needs everything — it's the comprehensive user-facing document that covers the entire product

### Per-Domain Generation

| Domain | Template | Key upstream inputs |
|---|---|---|
| readme | `tier8/templates/generation/document/readme.md` | Vision, Build |
| product-guide | `tier8/templates/generation/document/product-guide.md` | All 11 upstream documents |

**Product Guide special case:** Product Guide has zero edges in `core/tiers.yaml`'s relationships — it depends on everything, not nothing. Its generation context is all already-completed domains, not derived from relationship edges. This matches `00-domain-relationships.md`: "needs everything else, including README, to be accurate."

## Within-Tier Ordering

No ordering constraint — both domains generate in full parallel. README and Product Guide are independent of each other (README references Vision and Build; Product Guide references everything). Both can generate simultaneously.

## Output

Two documents, one per domain, ready for stage 2 (audit). No scoring at this stage.

## Differs From Other Use Cases

- **vs. `repo_new/case_2_has_documentation`:** No difference at Tier 8 — neither case has pre-existing README or Product Guide docs.
- **vs. `repo_existing/case_1_no_documentation`:** Tier 8 generation there has real code available. README installation instructions and Product Guide examples should reflect actual code structure, actual commands, actual file paths. This use case has no code — README and Product Guide describe the planned product.
- **vs. `repo_existing/case_2_has_documentation`:** Tier 8 there starts with existing non-conforming README/Product Guide docs and migrates them. This use case generates from scratch.
