# Runtime Behavior — Generation Template

> **Domain:** feature-technical
> **Section:** runtime_behavior
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Runtime Behavior
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Runtime Behavior section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / data_flow | Runtime lifecycle must follow Architecture data flow patterns |
| `derives_from` | feature-technical / component_interactions | Every runtime event must trace to a Component Interaction |

## Template

```markdown
## Runtime Behavior

### Initialization
[How components start and register with the system]

### Execution Flow
[How components process requests and produce responses]

### State Transitions
[How component states change during feature execution]

### Shutdown
[How components gracefully stop]

### Runtime Lifecycle Diagram
[Flowchart showing runtime lifecycle and state transitions]
```

## Examples

**Correct:**
> **Lifecycle: Order Processing**
> 1. **Initialization:** The Order Component starts and registers with the Event Bus. It subscribes to order submission events.
> 2. **Execution Flow:** When an order submission event arrives, the Order Component validates the request, delegates payment to the Payment Component, and updates order state.
> 3. **State Transitions:** An order moves through states: Submitted → Validated → PaymentPending → Confirmed → Completed (or Failed).
> 4. **Shutdown:** The Order Component unsubscribes from the Event Bus and completes any in-flight order processing before terminating.

**Incorrect:**
> Initialize Spring Boot application context and connect to RabbitMQ using `amqp://guest:guest@localhost:5672`. `OrderService.processOrder()` method validates input.
> *Why wrong: describes Spring Boot initialization and specific method names rather than architectural runtime lifecycle.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Describe the full lifecycle at the architectural level; define each state and valid transitions; include a flowchart
- **Don't:** Name specific runtime frameworks, connection strings, or configuration files; describe threading or process models

**Minimum content:** 1 paragraph + lifecycle description
**Length guidance:** extensive
**Required diagrams:** flowchart showing runtime lifecycle and state transitions
**Required cross-references:** Component Interactions, Architecture(05) runtime boundaries

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
