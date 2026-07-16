# Response Models Rules

This section defines the semantic validation rules for Response Models documentation.

## Criteria

### `eng-sem-resp-001`: Explicit Schema Definition

**Severity:** error

**Context & Rationale:**
Explicit response models prevent data leakage (e.g., password hashes) and power OpenAPI schema generation.

**Audit Check:**
- Does the standard mandate explicit `response_model` declarations on all FastAPI endpoints?
- Are raw dictionaries or untyped JSON responses forbidden?

**Anti-patterns:**
- `return {"id": user.id, "name": user.name}` directly from the router without a Pydantic model.

**Remediation:**
- Mandate the use of Pydantic models for all input and output payloads.

### `eng-sem-resp-002`: Error Normalization

**Severity:** error

**Context & Rationale:**
Clients expect a consistent error format.

**Audit Check:**
- Is there a defined strategy for normalizing exceptions into standard HTTP error responses?

**Anti-patterns:**
- Catching exceptions and returning custom dicts inconsistently across routers.

**Remediation:**
- Document the use of global FastAPI exception handlers to normalize all errors into a standard RFC 7807 problem details format or similar JSON structure.
