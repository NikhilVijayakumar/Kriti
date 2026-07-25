# Stage 1 — Generate or Migrate

**Use case:** `repo_new/case_1_no_documentation`
**Tier:** 3
**Domains:** feature-design, feature-technical

## Context Available

New repo, no documentation, no code. Tiers 1–2 have completed — Vision, Philosophy, Security, Feature, Architecture, Design, Engineering, and External Context documents exist and have cleared their tier gates. Tier 3 generation uses all upstream outputs as context.

## Procedure

For each domain in this tier, generate a complete document from scratch using the document-level generation template.

### Upstream Context (from completed tiers)

- **Vision** — what to build and why
- **Philosophy** — principles, values, trade-offs guiding decisions
- **Feature** — feature list, priorities, acceptance criteria
- **Architecture** — system design, technology choices, component boundaries
- **Design** — user experience, interaction patterns, visual language
- **Engineering** — technical practices, coding standards, deployment approach
- **External Context** — market landscape, competitive analysis, regulatory constraints
- **Security** — threat model, security requirements, compliance needs

### Per-Domain Generation

| Domain | Template | Key upstream inputs |
|---|---|---|
| feature-design | `templates/generation/document/09-feature-design.md` | Feature, Design, External Context |
| feature-technical | `templates/generation/document/10-feature-technical.md` | Feature, Architecture, Engineering, External Context |

Each domain generates a complete document with all sections defined in its generation template.

## Within-Tier Ordering

No ordering constraint — both domains generate in full parallel. Both depend on the same upstream tiers but on different subsets of them; there is no dependency between feature-design and feature-technical.

## Output

Two documents, one per domain, ready for stage 2 (audit). No scoring at this stage.

## Differs From Other Use Cases

- **vs. `repo_new/case_2_has_documentation`:** No difference at Tier 3 — neither case has pre-existing docs for these domains.
- **vs. `repo_existing/case_1_no_documentation`:** Tier 3 generation there has real code available. Feature Technical generation should reflect actual code patterns, not invent a design.
- **vs. `repo_existing/case_2_has_documentation`:** Tier 3 there starts with existing non-conforming docs. This use case generates from scratch.
