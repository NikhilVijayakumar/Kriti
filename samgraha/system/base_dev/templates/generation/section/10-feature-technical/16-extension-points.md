# Extension Points — Generation Template

> **Domain:** feature-technical
> **Section:** extension_points
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Extension Points
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Extension Points section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature-technical / participating_components | Extension points must involve components from Participating Components |
| `derives_from` | architecture / component_model | Extension points must align with Architecture plugin model |

## Template

```markdown
## Extension Points

### [Extension Point Name]
- **Type:** [plugin, hook, event, configuration]
- **Constraint:** [what extensions must or must not do]

### Extension Diagram
[Component diagram showing extension points]
```

## Examples

**Correct:**
> **Extension Point: Notification Dispatch**
> - Type: Event hook
> - Constraint: Extensions must implement the notification dispatch contract defined in Architecture plugin model; extensions cannot modify core notification routing

**Incorrect:**
> **Extension Point: Notification Dispatch**
> - Type: Custom JavaScript class extending BaseNotifier
> - Constraint: Must override onSend() method using the EventEmitter library API
> *Why wrong: specifies implementation-level details rather than architectural extension type and constraints.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Identify extension points with type (plugin, hook, event, configuration) and constraints; reference the Architecture plugin model
- **Don't:** Name specific programming languages, class hierarchies, or library APIs; describe callback implementations

**Minimum content:** 1 paragraph + extension list
**Length guidance:** moderate
**Required diagrams:** component diagram showing extension points
**Required cross-references:** Architecture(05) plugin architecture, Component Responsibilities

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
