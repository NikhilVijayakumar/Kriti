# Purpose — Generation Template

> **Domain:** security
> **Section:** purpose
> **Source:** `documentation-standards/03-security-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/03-security-relationships.yaml`

Generate the Purpose section for a Security document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / purpose | Purpose must trace to Vision — what the product is determines what must be defended |
| `guided_by` | philosophy / guiding_principles | Purpose must be consistent with Philosophy's guiding principles — security posture reflects the team's values |

## Template

```markdown
<!-- One paragraph: what Security defines and its role in the documentation hierarchy -->
<!-- One paragraph: what Security does not define, and where enforcement lives -->
```

## Examples

**Correct:**
> Security(03) establishes the project-wide threat model, data classification scheme, and security principles. It is the single source of truth for what the project defends against and why — every downstream domain's Security Considerations or Security Standards section derives from this document rather than re-deriving its own posture.

**Incorrect:**
> Security(03) defines the authentication middleware, rate-limiting configuration, and WAF rule set used across all services.
> *Why wrong: This describes specific control implementations (authentication middleware, rate limiting, WAF rules) — those belong in Engineering's Security Standards, not in the project-wide Security document.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** new contributor
- **Do:** State Security's role as the single project-wide authority; define the boundary between Security and per-domain sections explicitly; reference derivation from Vision(01) and Philosophy(02)
- **Don't:** Name specific controls, libraries, or tooling; use imperative voice; embed implementation details that belong in downstream domains

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision(01), Philosophy(02)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
