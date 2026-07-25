# Security Principles — Generation Template

> **Domain:** security
> **Section:** security_principles
> **Source:** `documentation-standards/03-security-standards.md` §Security Principles
> **Relationships:** `audit/deterministic/document/03-security-relationships.yaml`

Generate the Security Principles section for a Security document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | philosophy / guiding_principles | Security Principles must specialize Philosophy's guiding principles for the security context |
| `derives_from` | architecture / security_considerations | Security Principles must guide Architecture's security considerations — architectural decisions must be evaluable against these principles |
| `derives_from` | engineering / code_standards | Security Principles must guide Engineering's code standards — implementation decisions must be evaluable against these principles |

## Template

```markdown
<!-- State each security principle with: -->
<!--   - Name: memorable, stable phrase -->
<!--   - Rationale: why this principle constrains design decisions -->
<!--   - Example decision it would constrain (optional but recommended) -->
<!-- Link principles back to Philosophy(02) guiding principles they specialize -->
```

## Examples

**Correct:**
> **Principle:** Least Privilege by Default
> **Rationale:** Every component, service, and user must start with the minimum permissions required for its function — no more.
> **Decision it constrains:** Architecture's service-to-service communication design must not grant blanket access between services.

**Incorrect:**
> Security Principle: Be Secure. All code must follow security best practices.
> *Why wrong: This is a generic platitude that cannot constrain any concrete design decision — "best practices" is undefined, and "be secure" gives no evaluative criteria for a proposed design.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State each principle with name, rationale, and at least one example decision it constrains; specialize Philosophy(02) guiding principles for the security context; ensure every principle is evaluable against a concrete design
- **Don't:** Write generic platitudes ("be secure", "follow best practices"); embed specific technology choices or library recommendations; list more than seven principles — keep the set focused and memorable

**Required subsections:** none
**Optional subsections:** principle-to-decision examples, derivation from Philosophy
**Required diagrams:** none
**Required cross-references:** Philosophy(02), Threat Model

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
