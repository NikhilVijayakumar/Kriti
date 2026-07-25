# Participating Components — Generation Template

> **Domain:** feature-technical
> **Section:** participating_components
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Participating Components
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Participating Components section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / component_model | Component names and boundaries must come from the Architecture component model |
| `derives_from` | feature / purpose | Every participating component must be traceable to a feature requirement |

## Template

```markdown
## Participating Components

| Component | Reason for Participation |
|---|---|
| [Component Name from Architecture] | [why this component is involved in this feature] |
| ... | ... |

### Component Diagram
[Diagram showing participating components and their relationships]
```

## Examples

**Correct:**
> | Component | Reason for Participation |
> |---|---|
> | Authentication Component | Validates user credentials and manages session lifecycle for the login feature |
> | Data Component | Stores and retrieves user account data required for authentication |
> | Notification Component | Delivers security alerts triggered by authentication events |
> | UI Component | Presents the login interface and communicates user input to the Authentication Component |

**Incorrect:**
> | Component | Technology |
> |---|---|
> | AuthService | Node.js microservice using Express framework |
> | UserDatabase | PostgreSQL 15 with TypeORM |
> *Why wrong: lists implementation technologies rather than architectural components with their purpose.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** architect
- **Do:** Use component names from Architecture Documentation; state the reason each component participates; include a component diagram
- **Don't:** List technologies, frameworks, or library names; describe component internals; include components not directly involved

**Minimum content:** 1 paragraph + table or list
**Length guidance:** moderate
**Required diagrams:** component diagram showing participating components
**Required cross-references:** Architecture(05) component model, Feature Specification

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
