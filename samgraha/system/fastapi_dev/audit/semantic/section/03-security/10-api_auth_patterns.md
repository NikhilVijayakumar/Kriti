# API Auth Patterns Rules

This section defines the semantic validation rules for API Authentication and Authorization.

## Criteria

### `sec-sem-auth-001`: Mandatory Authentication

**Severity:** critical

**Context & Rationale:**
APIs are public interfaces; unprotected endpoints can lead to data breaches.

**Audit Check:**
- Is there a documented pattern ensuring all endpoints are authenticated by default, with explicit opt-out for public routes?

**Anti-patterns:**
- Developers manually adding `Depends(get_current_user)` to every single route, risking omission.

**Remediation:**
- Document a global dependency or middleware for authentication, or a strict review process for endpoint dependencies.

### `sec-sem-auth-002`: Token Handling and Validation

**Severity:** error

**Context & Rationale:**
Improper token validation can allow forged access.

**Audit Check:**
- Does the documentation specify how tokens (e.g., JWT) are validated (signature, expiration, audience)?
- Are secrets securely managed and not hardcoded?

**Anti-patterns:**
- Using symmetric keys checked into the repository or failing to check token expiration.

**Remediation:**
- Mandate strict JWT validation practices and secure secret injection.
