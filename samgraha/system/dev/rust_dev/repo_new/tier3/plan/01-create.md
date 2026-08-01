# Stage 1 - Create

**Use case:** `repo_new/tier3`
**Tier:** 3
**Domains:** feature-technical

## Context Available

New repo, no documentation, no code. Tiers 1–2 have completed — Vision, Philosophy, Security, Feature, Architecture, Engineering, and External Context documents exist and have cleared their tier gates. Tier 3 generation uses all upstream outputs as context.

## Procedure

For each domain in this tier, generate a complete document from scratch using the document-level generation template.

### Upstream Context (from completed tiers)

- **Vision** — what to build and why
- **Philosophy** — principles, values, trade-offs guiding decisions
- **Feature** — feature list, priorities, acceptance criteria
- **Architecture** — system design, technology choices, component boundaries
- **Engineering** — technical practices, coding standards, deployment approach
- **External Context** — market landscape, competitive analysis, regulatory constraints
- **Security** — threat model, security requirements, compliance needs

### Per-Domain Generation

| Domain | Template | Key upstream inputs |
|---|---|---|
| feature-technical | `common/tier3/templates/generation/document/feature-technical.md` | Feature, Architecture, Engineering, External Context |

Each domain generates a complete document with all sections defined in its generation template.

## Within-Tier Ordering

Single domain — no ordering constraint.

## Output

One document, ready for stage 2 (audit). No scoring at this stage.

## Differs From Other Use Cases

- **vs. repo_existing/tier3:** real code available - Feature Technical generation should reflect actual code patterns, not invent a design. This use case has no code - generates from scratch.
- **vs. repo_existing_no_doc/tier3:** after bootstrap, identical to repo_existing/tier3.