# Component Responsibilities — Generation Template

> **Domain:** feature-technical
> **Section:** component_responsibilities
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Component Responsibilities
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Component Responsibilities section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / component_model | Responsibilities must align with Architecture component model |
| `derives_from` | feature-technical / participating_components | Every component listed here must be defined in Participating Components |

## Template

```markdown
## Component Responsibilities

### [Component Name]
- **Primary responsibility:** [what this component is responsible for in this feature]
- **Alignment with Architecture:** [how this responsibility aligns with Architecture ownership rules]
- **Boundary:** [what this component must not do]

### Responsibility Diagram
[Component diagram showing responsibility assignments]
```

## Examples

**Correct:**
> **Authentication Component:**
> - Primary responsibility: Validating user credentials and issuing session tokens
> - Alignment with Architecture: Operates within the security boundary defined in Architecture
> - Boundary: Must not store user profile data — that belongs to the Data Component

**Incorrect:**
> **Authentication Component:** The `AuthService` class extends `BaseAuth` and implements the `login()` method using bcrypt.compare() for password verification.
> *Why wrong: describes class hierarchies and method implementations rather than architectural responsibilities.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Assign a primary responsibility to every participating component; ensure responsibilities do not overlap; align each responsibility with Architecture ownership rules
- **Don't:** Describe class hierarchies, method signatures, or library usage; assign shared ownership

**Minimum content:** 1 paragraph + responsibility list
**Length guidance:** moderate
**Required diagrams:** component diagram showing responsibility assignments
**Required cross-references:** Participating Components, Architecture(05) component model

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
