# Stage 1 — Generate or Migrate

**Use case:** `repo_existing/case_1_no_documentation`
**Tier:** 1
**Domains:** vision, philosophy

## Context Available

Existing repo with real code but no documentation. The only input is the product idea — a description of what the product is, who it serves, and why it exists. No upstream tier outputs exist (Tier 1 is the root of the derivation chain). Real code exists but is not referenced at this tier — Vision and Philosophy are technology-independent by design.

## Procedure

For each domain in this tier, generate a complete document from scratch using the document-level generation template.

### Vision

- **Template:** `templates/generation/document/01-vision.md`
- **Input context:** the product idea
- **Upstream context:** none (Vision is Tier 1 — derives from nothing)
- **Output:** `vision.md` — a complete Vision document with all 10 sections

### Philosophy

- **Template:** `templates/generation/document/02-philosophy.md`
- **Input context:** the product idea + the generated Vision document from above
- **Upstream context:** Vision (Tier 1) — Philosophy uses Vision as input
- **Output:** `philosophy.md` — a complete Philosophy document with all 4 sections

## Within-Tier Ordering

No ordering constraint — both domains generate in parallel. Philosophy reads Vision as data dependency.

## Output

Two documents, ready for stage 2 (audit). No scoring at this stage.

## Differs From Other Use Cases

- **vs. `repo_new/case_1_no_documentation`:** No difference at Tier 1 — neither case references code. Vision and Philosophy are technology-independent; real code doesn't change how they're generated.
- **vs. `repo_new/case_2_has_documentation`:** No difference — no pre-existing docs at Tier 1.
- **vs. `repo_existing/case_2_has_documentation`:** No difference — no existing docs to migrate at Tier 1.
