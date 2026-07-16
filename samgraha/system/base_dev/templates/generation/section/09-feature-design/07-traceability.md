# Traceability — Generation Template

> **Domain:** feature-design
> **Section:** traceability
> **Source:** `documentation-standards/09-feature-design-standards.md` §Traceability
> **Relationships:** `audit/deterministic/document/09-feature-design-relationships.yaml`

Generate the Traceability section for a Feature Design document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `traceable_to` | feature / purpose | Feature Design traceability must assert one-to-one mapping with exactly one Feature Specification |
| `traceable_to` | design / purpose | Feature Design traceability must show derivation from Design Documentation shared principles |

## Template

```markdown
[Derivation chain diagram from Vision through Feature and Design to Feature Design]

[One-to-one mapping assertion with Feature Specification]

[Table of downstream consumers]

| Consumer | Relationship |
|----------|-------------|
| [Consumer Name] | [nature of relationship] |
```

## Examples

**Correct:**
> This Feature Design derives from Feature Specification "Report Export" and applies Design Documentation's Interaction Principles and Accessibility Principles. It has a strict one-to-one relationship with the "Report Export" Feature Specification.
>
> | Consumer | Relationship |
> |----------|-------------|
> | Feature Technical Design | Technical realization of this design |
> | Engineering | Implementation of the designed UX |
> | User Acceptance Testing | Validation of designed behavior |

**Incorrect:**
> This Feature Design derives from the Authentication module's architecture document and the REST API specification. It covers Export, Import, and Archive features as a unified workflow.
> *Why wrong: (1) Derivation should trace to Feature Specification and Design Documentation, not architecture or API specs. (2) Multiple features are combined, violating the one-to-one relationship constraint.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** diagrams
- **Audience:** architect
- **Do:** Show the complete derivation chain from Vision through Feature and Design; state the one-to-one mapping constraint with Feature Specification explicitly; list all downstream consumers and their relationship
- **Don't:** Include implementation-level traceability (code, tests, bugs); omit the one-to-one mapping assertion; reference unrelated standards or documents

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** custom (derivation chain diagram)
**Required cross-references:** Feature(04), Design(06), Feature Technical Design(10), Engineering(07)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
