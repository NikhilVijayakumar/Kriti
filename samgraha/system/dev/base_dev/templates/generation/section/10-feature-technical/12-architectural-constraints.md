# Architectural Constraints — Generation Template

> **Domain:** feature-technical
> **Section:** architectural_constraints
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Architectural Constraints
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Architectural Constraints section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / constraints | Must reference Architecture source principles |
| `derives_from` | architecture / component_model | Must be consistent with Architecture component model |

## Template

```markdown
## Architectural Constraints

### [Constraint Name] (source: [Architecture principle])
[How this constraint applies to this specific feature]
```

## Examples

**Correct:**
> **Constraint: Component Ownership** (source: Architecture ownership rules)
> Each data element must have exactly one owning component. The Authentication Component owns credential data; no other component may write to it directly.

**Incorrect:**
> Use a single PostgreSQL database for all component data. Each component writes to its own schema using TypeORM repositories.
> *Why wrong: specifies technology choices and implementation patterns rather than architectural ownership principles.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Reference each constraint by its Architecture source principle; state how it applies to this feature; avoid redefining architectural principles
- **Don't:** Redefine Architecture principles; introduce implementation-level constraints; name technologies as constraints

**Minimum content:** 1 paragraph + constraint list
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Architecture(05) principles and constraints

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
