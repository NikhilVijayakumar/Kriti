# Traceability — Generation Template

> **Domain:** architecture
> **Section:** traceability
> **Source:** `documentation-standards/05-architecture-standards.md` §Traceability
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the Traceability section for an Architecture document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `traceable_to` | vision / vision_statement | Traceability must show Architecture's derivation from Vision |

## Template

```markdown
## Traceability

### Derivation Chain
[Diagram showing Architecture's position in the documentation tier model]

### Downstream Impact
[List of standards that Architecture constrains or feeds into]

### Non-Contradiction Rule
[Statement that no downstream document may contradict Architecture]
```

## Examples

**Correct:**
> Tier 2: Architecture (System Overview, Component Model, Security)
>     ├──→ Tier 3: Feature Technical Design
>     └──→ Tier 5: Engineering (soft, non-mandatory)
>
> **Non-contradiction rule:** No downstream document may describe a component boundary, ownership assignment, or communication path that contradicts this Architecture. When a Feature Technical Design needs a boundary Architecture doesn't define, Architecture is updated first.

**Incorrect:**
> Architecture traces to the `src/components/` directory and the deployment YAML files.
> *Why wrong: references source code and deployment configuration instead of the documentation hierarchy — Traceability connects Architecture to other standards, not to the codebase it eventually governs.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** diagrams
- **Audience:** architect
- **Do:** Show Architecture's tier position and every standard it feeds; state the non-contradiction rule explicitly; keep the diagram in sync when new standards derive from Architecture
- **Don't:** Reference source code, deployment artifacts, or CI/CD configuration; omit downstream standards from the diagram; leave the non-contradiction rule implicit

**Required subsections:** Derivation Chain, Non-Contradiction Rule
**Optional subsections:** Downstream Impact
**Required diagrams:** tier model diagram
**Required cross-references:** Vision(01), Feature Technical Design(10), Engineering(07)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
