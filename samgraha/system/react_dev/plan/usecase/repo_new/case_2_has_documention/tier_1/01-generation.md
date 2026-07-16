# Stage 1 — Generate or Migrate

**Use case:** `repo_new/case_2_has_documention`
**Tier:** 1
**Domains:** vision, philosophy

## Context Available

New repo with some pre-existing hand-written documentation (written before onboarding to this system). No code. Tier 1 domains may have existing docs that need migration, or may need generation from scratch.

**Key difference from `case_1_no_documentation`:** Some domains already have hand-written docs. These are migrated into the template shape — the existing prose is restructured to match the generation template's section requirements, not discarded and regenerated from scratch. The content is preserved; only the structure changes.

## Procedure

For each domain in this tier, check if pre-existing documentation exists.

### Per-Domain Decision

| Domain | Existing docs? | Action |
|---|---|---|
| vision | Depends on scenario | If yes → migrate: restructure existing prose into `templates/generation/document/01-vision.md`'s section shape. If no → generate from scratch. |
| philosophy | Depends on scenario | If yes → migrate: restructure existing prose into `templates/generation/document/02-philosophy.md`'s section shape. If no → generate from scratch. |

### Migration Process

1. Read the existing document.
2. Map existing content to the generation template's required sections.
3. Restructure: move content into the correct section order, fill any missing sections using the template's writing guidance, remove content that belongs in a different domain.
4. Output: a document that matches the template's section structure with the original content preserved where it fits.

### Generation Process (if no existing docs)

Same as `repo_new/case_1_no_documentation/tier_1/01-generation.md`.

## Within-Tier Ordering

No ordering constraint — both domains process in parallel. Philosophy reads Vision as data dependency (same as case_1).

## Output

Two documents, ready for stage 2 (audit). No scoring at this stage.

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** Stage 1 is migration, not pure generation. Existing hand-written docs are preserved and restructured, not discarded.
- **vs. `repo_existing/case_2_has_documention`:** No code context at Tier 1 — identical procedure.
