# API Versioning Rules

This section defines the semantic validation rules for the API Versioning documentation.

## Criteria

### `eng-sem-version-001`: Strict Versioning Convention

**Severity:** error

**Context & Rationale:**
Clients depend on stable contracts. A backend API must have a defined strategy for when and how endpoints are versioned.

**Audit Check:**
- Is an API versioning convention strictly defined (e.g., URL path vs header)?
- Does it specify what constitutes a breaking change requiring a new version?

**Anti-patterns:**
- "We will version endpoints as needed."

**Remediation:**
- Define exact URL formats (e.g., `/api/v1/`) or Header formats and rules for incrementing.

### `eng-sem-version-002`: Backward Compatibility and Deprecation

**Severity:** warning

**Context & Rationale:**
When a new version is released, older clients cannot migrate instantly.

**Audit Check:**
- Is the backward compatibility and migration strategy specified?
- Is there a defined deprecation timeline for old API versions?

**Anti-patterns:**
- "Old versions will be deleted when the new one is deployed."

**Remediation:**
- Define the support window for N-1 versions and the use of the `Warning` HTTP header for deprecation.
