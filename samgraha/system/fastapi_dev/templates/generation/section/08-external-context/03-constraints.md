# Constraints — Generation Template

> **Domain:** external-context
> **Section:** constraints
> **Source:** `documentation-standards/08-external-context-standards.md` §Constraints
> **Relationships:** `audit/deterministic/document/08-external-context-relationships.yaml`

Generate the Constraints section for an External Context document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `informs` | engineering / code_standards | Constraints must be expressed in terms engineers can enforce in implementation |
| `informs` | feature_design / design_rationale | Constraints must surface limitations that affect design decisions |

## Template

```markdown
## Constraints

[1 paragraph: overview of constraints the external system imposes on the repository]

### Functional Constraints

| Constraint | Limitation | Impact | Source |
|-----------|-----------|--------|--------|
| [Name] | [specific restriction] | [what this prevents] | [external source] |

### Performance Constraints

| Constraint | Limitation | Impact | Source |
|-----------|-----------|--------|--------|
| [Name] | [specific numeric limit] | [what this requires] | [external source] |

### Legal / Compliance Constraints

| Constraint | Requirement | Impact | Source |
|-----------|-------------|--------|--------|
| [Name] | [specific requirement] | [what this requires] | [external source] |
```

## Examples

**Correct:**
> The external platform enforces a maximum payload size of 1 MB per request. API calls are limited to 10 requests per second with a burst allowance of 20. Data stored by the platform must comply with GDPR; no personal data may be stored in fields the platform retains beyond 30 days.
>
> ### Functional Constraints
> | Constraint | Limitation | Impact | Source |
> |-----------|-----------|--------|--------|
> | Max payload | 1 MB per request | Large file uploads must be chunked | Platform API documentation §3.2 |
>
> ### Performance Constraints
> | Constraint | Limitation | Impact | Source |
> |-----------|-----------|--------|--------|
> | Rate limit | 100 requests/minute | Request throttling needed for batch operations | Platform service limits |
>
> ### Legal / Compliance Constraints
> | Constraint | Requirement | Impact | Source |
> |-----------|-------------|--------|--------|
> | GDPR | No personal data retained beyond 30 days | Data lifecycle management required | Platform data handling policy |

**Incorrect:**
> We decided to use connection pooling because our application needs high throughput. Our team prefers TypeScript over JavaScript for type safety.
> *Why wrong: These are internal design decisions, not constraints imposed by the external system. External Constraints must originate from the external dependency.*

## Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** bullet lists / tables
- **Audience:** architect
- **Do:** Categorize every constraint by type (functional, performance, legal, compliance); cite the external source for each constraint; state limits as specific numeric values where possible; include ALL subsections as part of this one section
- **Don't:** List internal project decisions as constraints; use vague qualifiers like "may" or "should" for hard limits; omit constraints that affect data handling or compliance; treat subsections as standalone sections

**Minimum content:** 1 subsection
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** authoritative external documentation

**Required subsections:** none
**Optional subsections:** Functional Constraints, Performance Constraints, Legal / Compliance Constraints

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
