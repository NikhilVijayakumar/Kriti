# Component Interactions — Generation Template

> **Domain:** feature-technical
> **Section:** component_interactions
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Component Interactions
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Component Interactions section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / communication_paths | Interaction patterns must use the communication paths defined in Architecture |
| `derives_from` | feature / purpose | Every interaction must be traceable to a feature requirement |

## Template

```markdown
## Component Interactions

### [Interaction Name]
- **Triggering condition:** [what initiates this interaction]
- **Nature of exchange:** [synchronous request, asynchronous event, etc.]
- **Expected outcome:** [what happens as a result]

### Interaction Diagram
[Sequence diagram showing component interactions]
```

## Examples

**Correct:**
> **Interaction: Order Submission**
> - Triggering condition: User submits an order through the UI Component
> - Nature of exchange: UI Component sends a synchronous request to the Order Component; Order Component validates and delegates payment to the Payment Component
> - Expected outcome: Order is created in Submitted state; payment is initiated; user receives confirmation or rejection

**Incorrect:**
> The React `OrderForm` component calls `POST /api/orders` using axios. Express router passes to `OrderController.submit()`.
> *Why wrong: describes implementation-level details rather than architectural component interactions.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** State the triggering condition, nature of exchange, and expected outcome for each interaction; trace every interaction to a Feature Specification behavior; include a sequence diagram
- **Don't:** Name specific classes, methods, or API endpoints; describe serialization formats or protocols

**Minimum content:** 1 paragraph + interaction list
**Length guidance:** moderate
**Required diagrams:** sequence diagram showing component interactions
**Required cross-references:** Participating Components, Feature Specification, Architecture communication model

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
