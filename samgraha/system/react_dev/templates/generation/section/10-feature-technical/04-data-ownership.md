# Data Ownership — Generation Template

> **Domain:** feature-technical
> **Section:** data_ownership
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Data Ownership
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Data Ownership section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / data_flow | Data ownership must follow Architecture data flow ownership rules |
| `derives_from` | feature / purpose | Every data element must be traceable to a feature requirement |

## Template

```markdown
## Data Ownership

| Data Element | Owner | Read Access | Write Access | Constraints |
|---|---|---|---|---|
| [element] | [owning component] | [who can read] | [who can write] | [architectural constraints] |

### Data Ownership Diagram
[ER diagram showing data ownership boundaries]
```

## Examples

**Correct:**
> | Data Element | Owner | Read Access | Write Access | Constraints |
> |---|---|---|---|---|
> | User Credentials | Authentication Component | Authentication Component only | Authentication Component only | Must not be exposed outside security boundary |
> | Order Records | Order Component | Order Component, Notification Component (read-only) | Order Component only | Order state transitions follow Runtime Behavior lifecycle |

**Incorrect:**
> | Data Element | Table | Column | Type |
> |---|---|---|---|
> | User Credentials | users | password_hash | VARCHAR(255) |
> *Why wrong: describes database schema details rather than component ownership and access boundaries.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** architect
- **Do:** Assign one owning component per data element; define read and write access boundaries explicitly; reference Architecture ownership rules; include an ER diagram
- **Don't:** Describe database schemas, column types, or ORM mappings; allow multiple owners for the same data element

**Minimum content:** 1 paragraph + ownership table or list
**Length guidance:** moderate
**Required diagrams:** ER diagram showing data ownership boundaries
**Required cross-references:** Architecture(05) ownership rules, Participating Components

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
