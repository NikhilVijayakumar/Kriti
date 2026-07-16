# Traceability — Generation Template

> **Domain:** external-context
> **Section:** traceability
> **Source:** `documentation-standards/08-external-context-standards.md` §Traceability
> **Relationships:** `audit/deterministic/document/08-external-context-relationships.yaml`

Generate the Traceability section for an External Context document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `traceable_to` | external / source | Traceability must link to the authoritative external documentation source |
| `informs` | engineering / testing_standards | Traceability must show how External Context influences testing decisions |

## Template

```markdown
## Traceability

### Influence Diagram

```text
Vision
  ↓
Features
  ↓
Feature Design
  ↓
Architecture
  ↓
Feature Technical Design
  ↓
Engineering

         ↑

 External Context
```

External Context informs documentation. It does not redefine it.

### Consuming Standards

| Standard | How It References External Context |
|----------|-----------------------------------|
| Feature Technical Design (10) | [How this dependency's constraints and contract surface in technical designs] |
| Engineering (07) | [How this dependency's rationale and contract guide implementation] |
| Architecture (05) | [How this dependency's boundaries and platform requirements inform architecture] |
```

> **Generation note:** External Context occupies a lateral position in the documentation tier — it informs multiple downstream standards but is not itself derived from them. The Influence Diagram must show this lateral relationship. Consuming Standards must list every standard that references External Context content. The non-duplication rule must be stated: downstream standards **reference** External Context rather than duplicating its content.

## Examples

**Correct:**
> External Context informs Feature Technical Design by surfacing integration constraints before implementation begins. It informs Architecture by revealing system boundaries and platform requirements. It informs Engineering by providing rationale for technology choices tied to the external dependency. Downstream standards **reference** External Context rather than duplicating its content.
>
> ### Consuming Standards
> | Standard | How It References External Context |
> |----------|-----------------------------------|
> | Feature Technical Design (10) | Component responsibilities reference integration contract; communication paths reference endpoints |
> | Engineering (07) | Build standards reference dependency requirements; code standards reference API contract |
> | Architecture (05) | System overview references platform boundaries; constraints reference external limitations |

**Incorrect:**
> Traceability shows that External Context was last updated in March and is owned by the platform team. It includes a changelog of all edits made to the document.
> *Why wrong: Traceability in this context means showing how External Context influences downstream documentation standards, not tracking document metadata or ownership history.*

## Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** diagrams + tables
- **Audience:** architect
- **Do:** Include a text-based tier diagram showing External Context's lateral position; list every downstream standard that consumes External Context by name; explicitly state the non-duplication rule (reference, don't copy)
- **Don't:** Include version history or changelog entries; treat Traceability as document metadata; omit a standard from the consuming list if it references External Context content

**Minimum content:** 1 diagram, 1 subsection
**Length guidance:** concise
**Required diagrams:** flowchart (tier diagram)
**Required cross-references:** Feature Technical Design (10), Engineering (07), Architecture (05)

**Required subsections:** Influence Diagram, Consuming Standards
**Optional subsections:** none

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
