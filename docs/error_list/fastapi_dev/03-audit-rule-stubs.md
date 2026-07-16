# fastapi_dev — Gap Analysis: Audit Rules Are Minimal Stubs

**Category:** Gaps / Audit Coverage  
**Severity:** High  
**Date:** 2026-07-15

---

## Summary

The three new FastAPI-specific semantic audit rule files created during implementation contain only 2–3 bullet-point checks each. Compare this to the existing base_dev audit files (e.g., `audit/semantic/section/05-architecture/01-purpose.md` at 2541 bytes, `audit/semantic/section/10-feature-technical/13-security_considerations.md` at 2815 bytes) — these are structured multi-criterion audit definitions.

The new FastAPI audit files are too thin to drive meaningful audit coverage.

---

## Affected Files and Their Current State

### `audit/semantic/section/05-architecture/12-layered_architecture.md` (253 bytes)

```markdown
# Layered Architecture Rules
- Check: Does the architecture define distinct boundaries for Routers, Services, and Repositories?
- Check: Are dependency directions strictly enforced?
```

**Missing:**
- Criterion IDs (e.g., `arch-sem-layered-001`)
- Severity levels
- Rationale for each check
- Anti-patterns with examples (e.g., "business logic in router is a violation")
- Remediation guidance

---

### `audit/semantic/section/07-engineering/10-versioning.md` (168 bytes)

```markdown
# API Versioning Rules
- Check: Is an API versioning convention strictly defined?
- Check: Is the backward compatibility and migration strategy specified?
```

**Missing:**
- Criterion IDs
- Specific version strategy checks (URL path `/v1/`, header `Accept-Version`)
- Deprecation timeline requirements
- Rationale and remediation

---

### `audit/semantic/section/10-feature-technical/21-layer_implementation.md` (277 bytes)

```markdown
# Layer Implementation Rules
- Check: Is business logic strictly kept out of the Router layer?
- Check: Does the Service layer correctly orchestrate calls to the Repository layer?
- Check: Are external dependencies injected rather than instantiated globally?
```

**Missing:**
- Criterion IDs
- Severity levels per check
- Specific anti-patterns with examples
- Remediation guidance per check

---

## What Well-Formed Audit Rules Look Like

Compare to `audit/semantic/section/10-feature-technical/13-security_considerations.md` (2815 bytes) which defines:
- Named criteria with IDs
- Context, rationale, severity
- Specific things to look for
- Remediation steps

---

## Additional Audit Coverage Missing from Proposal Implementation

The proposal called for FastAPI-specific audit knowledge but the implementation only created 3 files. Missing audit coverage areas per the proposal:

| Area | What Should Be Audited | Status |
|------|------------------------|--------|
| Async usage | No `sync` blocking inside `async def` | ❌ Not created |
| DI patterns | No service/repo instantiated globally | Partially covered in `21-layer_implementation.md` |
| Response models | All endpoints have declared `response_model` | ❌ Not created |
| OpenAPI | Tags, descriptions on all routes | ❌ Not created |
| Pydantic validation | No raw dict parsing, use Pydantic models | ❌ Not created |
| Error normalization | HTTPException wrappers, not raw exceptions | ❌ Not created |

---

## Fix Required

1. Expand the 3 existing audit stubs to full structured audit criteria with IDs, severity, rationale, and remediation.
2. Create at minimum 3 additional audit files for:
   - `audit/semantic/section/07-engineering/11-async_patterns.md`
   - `audit/semantic/section/07-engineering/12-response_models.md`
   - `audit/semantic/section/03-security/10-api_auth_patterns.md`
