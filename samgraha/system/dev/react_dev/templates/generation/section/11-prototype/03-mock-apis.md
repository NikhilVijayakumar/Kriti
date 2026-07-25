# Mock APIs — Generation Template

> **Domain:** prototype
> **Section:** mock_apis
> **Source:** `documentation-standards/11-prototype-standards.md` §Mock APIs
> **Relationships:** `audit/deterministic/document/11-prototype-relationships.yaml`

Generate the Mock APIs section for a Prototype document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | scope | Every mocked dependency must correspond to an in-scope item |

## Template

```markdown
## Mock APIs

| Dependency | Fidelity | Request Contract | Response Contract |
|------------|----------|------------------|-------------------|
| [name] | [low|medium|high] | [request structure] | [response structure] |

[Fidelity justification for each mock]
```

## Examples

**Correct:**
> | Dependency | Fidelity | Request Contract | Response Contract |
> |------------|----------|------------------|-------------------|
> | Payment Gateway | low | POST /charge {amount, currency} | {status: "approved", id: "ch_123"} |
> | Inventory Service | medium | GET /stock/{sku} | {sku: "WIDGET-01", quantity: 42} |
>
> Payment Gateway is low fidelity because the prototype only tests the happy path. Inventory Service is medium fidelity because it returns realistic stock levels.

**Incorrect:**
> | Dependency | Request Contract | Response Contract |
> |------------|------------------|-------------------|
> | Payment Gateway | POST /charge | {status: "approved"} |
> *Why wrong: the fidelity indicator column is missing.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** List every mocked dependency with a fidelity column; explain the fidelity choice after the table; use concrete request/response examples
- **Don't:** Omit the fidelity indicator; use vague descriptions; include real production endpoints or credentials

**Minimum content:** 1 paragraph + 1 table per mock
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Scope, Data Model

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
