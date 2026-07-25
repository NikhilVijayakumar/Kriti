# Integration Points — Generation Template

> **Domain:** feature-technical
> **Section:** integration_points
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Integration Points
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Integration Points section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / communication_paths | Integration points must follow Architecture communication boundaries |
| `derives_from` | feature-technical / participating_components | Each integration point must involve a component from Participating Components |

## Template

```markdown
## Integration Points

### [Integration Name]
- **Systems involved:** [component(s) and external system]
- **Nature:** [synchronous request-response, asynchronous event, etc.]
- **Boundary type:** [Internal, External, Third-party]

### Integration Diagram
[Component diagram showing integration boundaries]
```

## Examples

**Correct:**
> **Integration Point: Payment Processing**
> - Systems involved: Order Component and external Payment Processor
> - Nature: Synchronous request-response for transaction authorization
> - Boundary type: External — crosses the system boundary to a third-party service

**Incorrect:**
> **Integration Point: Payment Processing**
> - Call `POST https://api.paymentprocessor.com/v2/charge` with API key in `Authorization: Bearer` header
> *Why wrong: describes API endpoint URLs and HTTP headers rather than architectural integration boundary characteristics.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Identify every integration point with systems involved, nature, and boundary type; classify each as internal, external, or third-party; include a component diagram
- **Don't:** Describe API endpoints, authentication token formats, or request/response schemas; name client libraries

**Minimum content:** 1 paragraph + integration list
**Length guidance:** moderate
**Required diagrams:** component diagram showing integration boundaries
**Required cross-references:** Feature Specification, Architecture(05) boundaries

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
