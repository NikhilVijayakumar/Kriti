# Security Fix Plan — Generation Template

> **Domain:** implementation
> **Section:** security_fix_plan
> **Source:** `documentation-standards/13-implementation-standards.md` §Security Fix Plan
> **Relationships:** `audit/deterministic/document/13-implementation-relationships.yaml`

Generate the Security Fix Plan section for an Implementation Plan document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | security / threat_model | Vulnerability must be identified in Security(03) threat model |
| `traceable_to` | security / mitigation_strategies | Fix approach must trace to Security(03) mitigation strategies |

## Template

```markdown
## Security Fix Plan

### Vulnerability Description

- **Location:** [endpoint, parameter, file path]
- **Severity:** [critical | high | medium | low]
- **Threat model reference:** Security(03) [threat ID or entry]
- **Description:** [what was found and how it was discovered]

### Fix Approach

[1-2 paragraphs: how the vulnerability is addressed, referencing Engineering(07) secure coding standards]

### Verification

[Concrete steps to confirm the fix resolves the vulnerability — include specific test payloads]

### Re-test Requirements

| Test Suite | Category | Count | Source |
|---|---|---|---|
| [suite name] | [security category] | [number of tests] | QA(12) |
```

## Examples

**Correct:**
> **Vulnerability Description:** SQL injection vulnerability in the user search endpoint (GET /api/users?name=). User-supplied `name` parameter is interpolated directly into a SQL query string without parameterization. Identified in Security(03) threat model as high-severity for data exfiltration.
> **Fix Approach:** Replace string interpolation with parameterized queries using the database driver's prepared statement API, per Engineering(07) secure coding standards. Apply fix to all three search endpoints (users, products, orders).
> **Verification:** Confirm parameterized queries reject injected payloads — test with `'; DROP TABLE users; --` and `1' OR '1'='1`. Verify legitimate search results are unchanged.
> **Re-test Requirements:** Run QA(12) full security test suite (15 tests). specifically the SQL injection test category (5 tests). Verify no new injection vectors introduced in affected endpoints.

**Incorrect:**
> **Vulnerability Description:** Security bug in search.
> **Fix Approach:** Add input validation.
> **Verification:** Tested manually.
> **Re-test Requirements:** None specified.
> *Why wrong: Vulnerability description lacks location, severity, and upstream reference; fix approach is vague without specifying the exact remediation technique; verification is manual rather than reproducible; re-test requirements are missing entirely.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Specify the exact vulnerability location (endpoint, parameter, file path) and its severity; reference the Security(03) threat model entry; define reproducible verification steps with specific attack payloads; list the QA(12) security test suite and category counts
- **Don't:** Write vague descriptions like "security issue in search"; use manual testing as the sole verification method; omit re-test requirements or skip checking for new vulnerability introduction

**Minimum content:** 4 subsections (Vulnerability Description, Fix Approach, Verification, Re-test Requirements)
**Length guidance:** extensive
**Required diagrams:** none
**Required cross-references:** Security(03), QA(12), Architecture(05), Engineering(07)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
