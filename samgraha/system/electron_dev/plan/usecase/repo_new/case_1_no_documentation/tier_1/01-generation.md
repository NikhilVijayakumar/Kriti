# Stage 1 — Generate or Migrate

**Use case:** `repo_new/case_1_no_documentation`
**Tier:** 1
**Domains:** vision, philosophy

## Context Available

New repo, no documentation, no code. The only input is the product idea — a description of what the product is, who it serves, and why it exists. No upstream tier outputs exist (Tier 1 is the root of the derivation chain).

## Procedure

For each domain in this tier, generate a complete document from scratch using the document-level generation template.

### Vision

- **Template:** `templates/generation/document/01-vision.md`
- **Input context:** the product idea
- **Upstream context:** none (Vision is Tier 1 — derives from nothing)
- **Output:** `vision.md` — a complete Vision document with all 10 sections (Purpose, Vision Statement, Problem, Solution, Target Audience, Platform Pillars, Philosophy, Guiding Principles, Success Criteria, Traceability)

### Philosophy

- **Template:** `templates/generation/document/02-philosophy.md`
- **Input context:** the product idea + the generated Vision document from above
- **Upstream context:** Vision (Tier 1) — Philosophy is in the same tier; Vision generates first, Philosophy uses Vision as input
- **Output:** `philosophy.md` — a complete Philosophy document with all 4 sections (Purpose, Principles, Values, Trade-offs)

## Within-Tier Ordering

No ordering constraint — both domains generate in parallel. However, Philosophy's template references Vision as upstream, so in practice Philosophy generation should read the generated Vision document as input context. This is a data dependency within the tier, not a gating constraint — Vision doesn't need to clear the audit gate before Philosophy can start generating, it just needs to exist as text.

## Output

Two documents, one per domain, ready for stage 2 (audit). No scoring at this stage — that's stage 2's job.

## Differs From Other Use Cases

- **vs. `repo_new/case_2_has_documention`:** No difference at Tier 1 — neither case has pre-existing docs at this tier.
- **vs. `repo_existing/case_1_no_documentation`:** No difference at Tier 1 — no code context applies to Vision or Philosophy.
- **vs. `repo_existing/case_2_has_documention`:** No difference at Tier 1 — no existing docs to migrate.
