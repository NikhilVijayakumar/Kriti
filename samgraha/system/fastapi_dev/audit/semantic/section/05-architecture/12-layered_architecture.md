# Layered Architecture Rules

This section defines the semantic validation rules for the Layered Architecture documentation.

## Criteria

### `arch-sem-layered-001`: Strict Layer Boundaries

**Severity:** error

**Context & Rationale:**
FastAPI applications can easily become entangled if business logic is placed in the router. A strict separation between Router, Service, and Repository layers ensures testability and maintainability.

**Audit Check:**
- Does the architecture explicitly define distinct boundaries for Routers, Services, and Repositories?
- Is it clearly stated that Routers handle only HTTP concerns, Services handle business logic, and Repositories handle data access?

**Anti-patterns:**
- "The router will extract the user and query the database." (Router bypassing Service).

**Remediation:**
- Explicitly define the responsibilities of each layer and mandate strict boundary enforcement.

### `arch-sem-layered-002`: Inward Dependency Direction

**Severity:** error

**Context & Rationale:**
Dependencies must point inward. Repositories should not depend on Services, and Services should not depend on Routers.

**Audit Check:**
- Are dependency directions strictly enforced in the documentation?
- Does the documentation explicitly forbid upward or circular layer dependencies?

**Anti-patterns:**
- "The Repository will use the HTTP request object to determine the tenant."

**Remediation:**
- State the permitted dependency flow (Router -> Service -> Repository).
