# Failure Handling — Generation Template

> **Domain:** feature-technical
> **Section:** failure_handling
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Failure Handling
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Failure Handling section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / operational_readiness | Failure handling must align with Architecture operational readiness |
| `derives_from` | feature-technical / component_interactions | Every failure mode must correspond to a Component Interaction |

## Template

```markdown
## Failure Handling

### [Failure Mode Name]
- **Interaction affected:** [which component interaction fails]
- **Propagation:** [how the failure propagates across components]
- **Recovery:** [what happens and how the system recovers]
- **Resilience boundary:** [where failure propagation stops]

### Failure Diagram
[Flowchart showing error propagation and recovery paths]
```

## Examples

**Correct:**
> **Failure Mode: External Service Unavailable**
> - Interaction affected: Order Service queries Payment Gateway
> - Propagation: Failure propagates from Payment Gateway to Order Service to Notification Service
> - Recovery: Order Service queues the order for retry; Notification Service informs the user that processing is delayed
> - Resilience boundary: Failure does not propagate beyond Order Service to the User Interface layer

**Incorrect:**
> Catch `PaymentTimeoutException` in `OrderService.java` line 142. Retry 3 times with exponential backoff using Spring Retry `@Retryable`.
> *Why wrong: describes implementation-level error handling rather than architectural failure modes and recovery strategies.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Define failure modes for every component interaction; trace error propagation paths across architectural boundaries; state recovery strategies and resilience boundaries; include a flowchart
- **Don't:** Name specific exception types, error codes, or try/catch patterns; describe retry implementations or logging frameworks

**Minimum content:** 1 paragraph + failure list
**Length guidance:** extensive
**Required diagrams:** flowchart showing error propagation and recovery paths
**Required cross-references:** Component Interactions, Architecture(05) error boundaries, Component Responsibilities

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
