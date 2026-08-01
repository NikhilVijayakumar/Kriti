# Stage 1 - Create

**Use case:** `repo_new/tier2`
**Tier:** 2
**Domains:** security, feature, architecture, engineering, external-context

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
- **Engineering** reads Philosophy ( principles that constrain engineering choices)
- **External Context** reads Vision ( what the product aspires to be, for market/landscape framing)

### Per-Domain Generation

| Domain | Template | Key upstream inputs |
|---|---|---|
| security | `common/tier2/templates/generation/document/security.md` | Vision, Philosophy |
| feature | `common/tier2/templates/generation/document/feature.md` | Vision, Philosophy |
| architecture | `common/tier2/templates/generation/document/architecture.md` | Philosophy |
| engineering | `common/tier2/templates/generation/document/engineering.md` | Philosophy |
| external-context | `common/tier2/templates/generation/document/external-context.md` | Vision |

Each domain generates a complete document with all sections defined in its generation template.

## Within-Tier Ordering

**External Context must complete before Engineering starts.** External Context informs Engineering — Engineering's generation needs External Context as input context (market landscape, competitive analysis, regulatory constraints).

All other domains in this tier generate in full parallel. Architecture and Engineering have a `soft_aligns_with` relationship (mutual, non-mandatory) — this is non-blocking.

Execution order:
1. External Context, Security, Feature, Architecture — parallel
2. Engineering — after External Context completes

## Output

Five documents, one per domain, ready for stage 2 (audit). No scoring at this stage.

## Differs From Other Use Cases

- **vs. repo_existing/tier2:** real code available as additional context - Architecture, Engineering, and Feature Technical generation should reflect the actual code structure, not invent a design. This use case has no code - generation produces a plausible design from the product idea alone.
- **vs. repo_existing_no_doc/tier2:** after bootstrap, identical to repo_existing/tier2 - audits first, same code context available.