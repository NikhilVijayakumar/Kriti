# Communication Paths — Generation Template

> **Domain:** feature-technical
> **Section:** communication_paths
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Communication Paths
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Communication Paths section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / communication_paths | Communication paths must use Architecture-defined protocols |
| `derives_from` | feature-technical / component_interactions | Each path must trace to a Component Interaction |

## Template

```markdown
## Communication Paths

### [Source Component] → [Destination Component]
- **Direction:** [outbound/inbound]
- **Nature:** [synchronous request, asynchronous event, etc.]
- **Architectural protocol:** [reference to Architecture communication model]

### Communication Diagram
[Sequence diagram showing communication paths]
```

## Examples

**Correct:**
> **Order Component → Notification Component**
> - Direction: Outbound from Order to Notification
> - Nature: Asynchronous event publication — order completion triggers notification delivery
> - Architectural protocol: Event Bus (as defined in Architecture communication model)

**Incorrect:**
> **Order Component → Notification Component**
> - Direction: POST request to `https://notification-service/internal/events`
> - Nature: JSON payload with order ID and status fields
> *Why wrong: describes HTTP methods, URLs, and payload formats rather than architectural communication path characteristics.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Define direction, nature, and architectural protocol for every communication path; trace each path to a Component Interaction; reference the Architecture communication model
- **Don't:** Specify HTTP methods, URLs, or payload schemas; describe serialization or wire formats

**Minimum content:** 1 paragraph + path list
**Length guidance:** moderate
**Required diagrams:** sequence diagram showing communication paths
**Required cross-references:** Component Interactions, Architecture(05) communication model

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
