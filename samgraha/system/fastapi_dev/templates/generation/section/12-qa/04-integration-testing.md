# Integration Testing — Generation Template

> **Domain:** qa
> **Section:** integration_testing
> **Source:** `documentation-standards/12-qa-standards.md` §Integration Testing
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the Integration Testing section for a QA document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / communication_paths | Integration boundaries must map to Architecture communication paths |

## Template

```markdown
## Integration Testing

### Integration Boundaries

| Boundary | Components | Contract | Verification Method |
|----------|-----------|----------|-------------------|
| [Boundary 1] | [Component A ↔ Component B] | [API/Protocol] | [Test approach] |
| [Boundary 2] | [Component B ↔ Component C] | [API/Protocol] | [Test approach] |

### Component Diagram
[Diagram showing component boundaries and communication paths]
```

## Examples

**Correct:**
> ### Integration Boundaries
>
> | Boundary | Components | Contract | Verification Method |
> |----------|-----------|----------|-------------------|
> | API Gateway ↔ Auth Service | Gateway ↔ Auth | OAuth2 token endpoint | Contract test with mock IdP |
> | Auth Service ↔ User Database | Auth ↔ PostgreSQL | SQL schema + query contracts | Integration test with test database |

**Incorrect:**
> We test that the API works with the database and the cache.
> *Why wrong: integration boundaries must be explicitly listed as a table mapping specific component pairs, their contracts, and verification methods.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Map each boundary to specific component pairs from Architecture(05); state the contract type; define a concrete verification method per boundary; include a component diagram
- **Don't:** Describe integration testing in prose without a boundary table; use vague terms; omit the contract type

**Required subsections:** Integration Boundaries table
**Optional subsections:** none
**Required diagrams:** component diagram showing integration boundaries
**Required cross-references:** Architecture(05), Feature(04)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
