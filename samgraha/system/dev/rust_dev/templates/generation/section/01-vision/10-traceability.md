# Traceability — Generation Template

> **Domain:** vision
> **Section:** traceability
> **Source:** `documentation-standards/01-vision-standards.md` §Traceability
> **Relationships:** `audit/deterministic/document/01-vision-relationships.yaml`

Generate the Traceability section for a Vision document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `traceable_to` | null / null | Vision is Tier 1 — no upstream domain exists |
| `traceable_to` | philosophy / purpose | Vision traceability must list Philosophy as a downstream consumer |
| `traceable_to` | feature / purpose | Vision traceability must list Feature as a downstream consumer |
| `traceable_to` | security / purpose | Vision traceability must list Security as a downstream consumer |

## Template

```markdown
Tier 0: Vision (Purpose)
    ├──→ Tier 1: [Downstream Standard 1]
    ├──→ Tier 1: [Downstream Standard 2]
    └──→ Tier 2: [Downstream Standard 3]

**Non-contradiction rule:** No downstream document may state a goal, constraint, or priority that contradicts the Vision. When conflicts arise, the Vision takes precedence.
```

## Examples

**Correct:**
> Tier 0: Vision (Purpose, Problem, Solution)
>     ├──→ Tier 1: Philosophy (Values, Principles)
>     ├──→ Tier 1: Features (Feature List, Feature Details)
>     └──→ Tier 2: Architecture (System Design, Technology Choices)
>
> **Non-contradiction rule:** No downstream document may state a goal, constraint, or priority that contradicts the Vision. When conflicts arise, the Vision takes precedence.

**Incorrect:**
> Vision traces to the README and the CI/CD pipeline configuration.
> *Why wrong: References an implementation artifact (CI/CD pipeline) instead of the documentation hierarchy. Traceability should connect to other documentation standards, not to code or infrastructure.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** diagrams
- **Audience:** architect
- **Do:** Include a tier diagram showing the derivation hierarchy; list every downstream standard that derives from Vision; state the non-contradiction rule explicitly
- **Don't:** Reference source code files, CI/CD pipelines, or infrastructure artifacts; omit standards from the diagram; use prose where a diagram would be clearer

**Required subsections:** tier diagram
**Optional subsections:** derivation list
**Required diagrams:** tier hierarchy flowchart
**Required cross-references:** all downstream standards listed

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
