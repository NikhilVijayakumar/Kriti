# Layer Implementation Rules

This section defines the semantic validation rules for Layer Implementation documentation.

## Criteria

### `ft-sem-layer-001`: Router Isolation

**Severity:** error

**Context & Rationale:**
Routers should only contain dependency injection, input validation, and delegation.

**Audit Check:**
- Is business logic strictly kept out of the Router layer?
- Are Pydantic models explicitly used for request and response mapping in the router description?

**Anti-patterns:**
- Checking business rules or throwing domain exceptions directly inside the FastAPI route function.

**Remediation:**
- Move business logic to the service layer; keep the router limited to mapping.

### `ft-sem-layer-002`: Service Orchestration

**Severity:** error

**Context & Rationale:**
Services coordinate transactions and domain logic.

**Audit Check:**
- Does the Service layer correctly orchestrate calls to the Repository layer?
- Are transactions managed at the Service layer?

**Anti-patterns:**
- Services making direct SQL queries using string execution instead of calling the repository.

**Remediation:**
- Ensure the documentation shows the service orchestrating abstract repository methods.

### `ft-sem-layer-003`: Dependency Injection

**Severity:** error

**Context & Rationale:**
Global state makes testing difficult. Dependencies should be injected.

**Audit Check:**
- Are external dependencies (DB sessions, external clients) injected rather than instantiated globally?

**Anti-patterns:**
- `from db import session; session.query(...)`

**Remediation:**
- Document the use of FastAPI's `Depends()` or a dedicated DI container.
