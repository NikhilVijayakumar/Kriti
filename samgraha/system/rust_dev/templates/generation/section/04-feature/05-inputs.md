# Inputs — Generation Template

> **Domain:** feature
> **Section:** inputs
> **Source:** `documentation-standards/04-feature-standards.md` §Inputs
> **Relationships:** `audit/deterministic/document/04-feature-relationships.yaml`

Generate the Inputs section for a Feature document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / vision_statement | Feature Documentation derives from Vision — the product's strategic direction and goals |
| `guided_by` | philosophy / guiding_principles | Feature purpose must be guided by Philosophy guiding principles |

## Template

```markdown
Feature Documentation derives from:

* [Source Name]
* [Source Name]

Feature Documentation should not derive from implementation.
```

## Examples

**Correct:**
> Feature Documentation derives from:
> * Vision — the product's strategic direction and goals
> * Business Requirements — domain rules and constraints
> * User Needs — validated user problems and expectations
>
> Feature Documentation should not derive from implementation.

**Incorrect:**
> Feature Documentation derives from:
> * Existing codebase — reverse-engineering features from source code
> * API documentation — deriving feature specs from endpoint definitions
> * Database schemas — extracting feature behavior from table structures
> *Why wrong: These sources are implementation artifacts. Deriving feature documentation from code, APIs, or schemas introduces technology-specific details that violate the technology-independence requirement.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** product owner
- **Do:** List each upstream source by name and describe what it contributes; explicitly state that implementation is not a valid source; reference Vision as the primary upstream source
- **Don't:** List downstream standards as inputs; include code, APIs, or database schemas as sources; omit the derivation direction between source and Feature Documentation

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision, Traceability

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
