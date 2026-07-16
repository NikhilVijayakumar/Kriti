# External Dependencies — Generation Template

> **Domain:** feature-technical
> **Section:** external_dependencies
> **Source:** `documentation-standards/10-feature-technical-standards.md` §External Dependency Integration
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the External Dependencies section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / component_model | External dependencies must align with Architecture component model |
| `derives_from` | engineering / build_standards | External dependencies must be compatible with Engineering build constraints |

## Template

```markdown
## External Dependency Integration

### [Dependency Name] (reference: [External Context document])
- **Role in feature:** [what this dependency does for the feature]
- **Nature of integration:** [how the system interacts with it]
- **Constraints:** [what constraints this dependency imposes]

### Dependency Diagram
[Component diagram showing external dependencies]
```

## Examples

**Correct:**
> **Dependency: Identity Provider** (reference: External Context identity services)
> - Role in feature: Authenticates user credentials during login flow
> - Nature of integration: The Authentication Component delegates credential verification to the Identity Provider
> - Constraints: Requires network connectivity; authentication is unavailable if the provider is unreachable

**Incorrect:**
> **Dependency: Identity Provider**
> - Use Auth0 SDK v4.2.1 to call the `/oauth/token` endpoint
> - Store refresh tokens in memory using the `auth0-spa-js` library
> *Why wrong: describes SDK versions and library APIs rather than the architectural role and constraints.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Reference External Context documents by name; state the role of each dependency; describe constraints without duplicating External Context content; include a component diagram
- **Don't:** Duplicate External Context content; describe SDK versions or library APIs; specify implementation-level integration patterns

**Minimum content:** 1 paragraph + dependency list
**Length guidance:** moderate
**Required diagrams:** component diagram showing external dependencies
**Required cross-references:** External Context(08), Integration Points

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
