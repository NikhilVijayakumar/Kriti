# Stage 1 — Generate or Migrate

**Use case:** `repo_new/case_1_no_documentation`
**Tier:** 2
**Domains:** security, feature, architecture, design, engineering, external-context

## Context Available

New repo, no documentation, no code. Tier 1 has completed — Vision and Philosophy documents exist and have cleared the tier gate. Tier 2 generation uses Tier 1 outputs as upstream context.

## Procedure

For each domain in this tier, generate a complete document from scratch using the document-level generation template.

### Upstream Context (from completed tiers)

- **Vision** — `vision.md` (Tier 1): product purpose, problem, solution, target audience, pillars, philosophy, guiding principles, success criteria
- **Philosophy** — `philosophy.md` (Tier 1): principles, values, trade-offs

All Tier 2 domains read both Tier 1 documents as input context. The specific relevance varies by domain:
- **Security** reads Vision ( threat landscape framing) and Philosophy ( values that constrain security decisions)
- **Feature** reads Vision ( what to build) and Philosophy ( how to prioritize)
- **Architecture** reads Philosophy ( principles that constrain architectural choices)
- **Design** reads Philosophy ( principles that guide design decisions)
- **Engineering** reads Philosophy ( principles that constrain engineering choices)
- **External Context** reads Vision ( what the product aspires to be, for market/landscape framing)

### Per-Domain Generation

| Domain | Template | Key upstream inputs |
|---|---|---|
| security | `templates/generation/document/06-security.md` | Vision, Philosophy |
| feature | `templates/generation/document/04-feature.md` | Vision, Philosophy |
| architecture | `templates/generation/document/05-architecture.md` | Philosophy |
| design | `templates/generation/document/07-design.md` | Philosophy |
| engineering | `templates/generation/document/08-engineering.md` | Philosophy |
| external-context | `templates/generation/document/15-external-context.md` | Vision |

Each domain generates a complete document with all sections defined in its generation template.

## Within-Tier Ordering

**External Context must complete before Engineering starts.** External Context informs Engineering — Engineering's generation needs External Context as input context (market landscape, competitive analysis, regulatory constraints).

All other domains in this tier generate in full parallel. Architecture and Engineering have a `soft_aligns_with` relationship (mutual, non-mandatory) — this is non-blocking.

Execution order:
1. External Context, Security, Feature, Architecture, Design — parallel
2. Engineering — after External Context completes

## Output

Six documents, one per domain, ready for stage 2 (audit). No scoring at this stage.

## Differs From Other Use Cases

- **vs. `repo_new/case_2_has_documention`:** No difference at Tier 2 — neither case has pre-existing docs for these domains.
- **vs. `repo_existing/case_1_no_documentation`:** Tier 2 generation there has real code available as additional context. Architecture, Engineering, and Feature Technical generation should reflect the actual code structure, not invent a design. This use case has no code — generation produces a plausible design from the product idea alone.
- **vs. `repo_existing/case_2_has_documention`:** Tier 2 there starts with existing non-conforming docs and migrates them. This use case generates from scratch.
