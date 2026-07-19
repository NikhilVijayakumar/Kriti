# Stage 1 — Generate or Migrate

**Use case:** `repo_new/case_1_no_documentation`
**Tier:** 4
**Domains:** prototype

## Context Available

New repo, no documentation, no code. Tiers 1–3 have completed — all upstream documents exist and have cleared their tier gates. Tier 4 generation uses all upstream outputs as context.

## Procedure

Generate a complete Prototype document from scratch using the document-level generation template.

### Upstream Context (from completed tiers)

- **Vision** — what to build and why
- **Philosophy** — principles, values, trade-offs
- **Feature** — feature list, priorities
- **Architecture** — system design, component boundaries
- **Design** — user experience, interaction patterns
- **Engineering** — technical practices
- **External Context** — market landscape, constraints
- **Security** — threat model, requirements
- **Feature Design** — detailed feature specifications
- **Feature Technical** — technical feature specifications

### Generation

| Domain | Template | Key upstream inputs |
|---|---|---|
| prototype | `templates/generation/document/11-prototype.md` | Feature Design, Feature Technical, Design |

Prototype validates Feature Design and Feature Technical — its generation should produce a prototype plan that exercises the most critical feature paths.

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit). No scoring at this stage.

## Differs From Other Use Cases

- **vs. `repo_existing/case_1_no_documentation`:** Tier 4 generation there has real code available. Prototype should reflect actual code structure and be buildable against the existing codebase.
- **vs. `repo_new/case_2_has_documentation` / `repo_existing/case_2_has_documentation`:** No difference at Tier 4 — neither has pre-existing prototype docs.
