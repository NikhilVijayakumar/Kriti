# Traceability — Generation Template

> **Domain:** design
> **Section:** traceability
> **Source:** `documentation-standards/06-design-standards.md` §Traceability
> **Relationships:** `audit/deterministic/document/06-design-relationships.yaml`

Generate the Traceability section for a Design document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `traceable_to` | philosophy / guiding_principles | Traceability must connect design principles back to guiding philosophy |
| `derives_from` | feature_design / design_rationale | Traceability must show how design derives from feature design rationale |

## Template

```markdown
## Traceability

### Tier Diagram

[ASCII or Mermaid diagram showing Design Documentation's position in the documentation hierarchy]

### Upstream Derivation

[1 paragraph per upstream source: Vision, Philosophy — how Design derives from them]

### Downstream Consumers

[1 paragraph per downstream: Feature Design, Architecture — how they consume Design]

### Non-Contradiction Rule

[1 paragraph: downstream documents must not contradict design principles]
```

## Examples

**Correct:**
> ### Tier Diagram
> Vision → Design Documentation → Feature Design → Engineering → Implementation
>
> Design Documentation derives its principles from the product Vision and Philosophy. It feeds Feature Design, which applies those principles to specific features. No downstream document may contradict the design principles established here.

**Incorrect:**
> Traceability shows that module A calls module B, which calls module C, through a dependency graph of the codebase.
> *Why wrong: This describes code-level implementation traceability, not documentation hierarchy traceability. Design Traceability must show the derivation chain across documentation standards, not source code dependencies.*

## Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** diagrams
- **Audience:** AI agent
- **Do:** Include a visual tier diagram showing the full derivation chain. List every upstream source and downstream consumer explicitly. State the non-contradiction rule as a binding constraint, not a suggestion.
- **Don't:** Describe code-level module dependencies or call graphs. Omit any standard in the derivation chain. Leave the non-contradiction rule implicit or optional.

**Required subsections:** Tier Diagram, Upstream Derivation, Downstream Consumers, Non-Contradiction Rule
**Optional subsections:** none
**Required diagrams:** tier/derivation flowchart
**Required cross-references:** Vision, Feature Design, Architecture, Feature Technical Design

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
