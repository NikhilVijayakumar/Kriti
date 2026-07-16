# Security Considerations — Generation Template

> **Domain:** feature-technical
> **Section:** security_considerations
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Security Considerations
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Security Considerations section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / security_considerations | Must derive from Architecture security boundaries |
| `derives_from` | feature-technical / participating_components | Security rules must apply to specific components from Participating Components |

## Template

```markdown
## Security Considerations

### Security Boundary
[Where trust changes in this feature]

### Authentication
[Authentication requirements for this feature]

### Authorization
[What each component can and cannot access]

### Sensitive Data
[What data is classified as sensitive and how it is protected]
```

## Examples

**Correct:**
> **Security Boundary:** The Authentication Component operates within the security boundary defined by Architecture. Only authenticated requests may access the Data Component.
> **Authorization:** The Notification Component may read user preferences but may not modify account data.
> **Sensitive Data:** User credentials and session tokens are classified as sensitive; they must not appear in communication paths that cross the external boundary.

**Incorrect:**
> Use bcrypt for password hashing with 12 salt rounds. Implement JWT tokens using the jsonwebtoken npm library with RS256 algorithm.
> *Why wrong: specifies implementation-level security details rather than architectural security boundaries and authorization rules.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Define security boundaries, authentication requirements, and authorization rules at the architectural level; identify sensitive data; reference Architecture security boundaries and External Context
- **Don't:** Name specific encryption algorithms, libraries, or token formats; describe code-level security patterns

**Minimum content:** 1 paragraph + security list
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Architecture(05) security boundaries, External Context(08), Security Documentation(03)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
