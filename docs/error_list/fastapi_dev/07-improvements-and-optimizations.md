# fastapi_dev — Improvements and Optimization Suggestions

**Category:** Improvements / Optimizations  
**Severity:** Medium  
**Date:** 2026-07-15

---

## Improvement 1 — `script/policy.yaml` Should Have FastAPI-Specific Overrides

**File:** `script/policy.yaml`

Current state — only two overrides exist:
```yaml
overrides:
  - check: dependency-reachable
    strategy: fingerprint
    max_age_seconds: 3600
  - check: mock-api-runs
    strategy: always_rerun
```

For a FastAPI backend system, the following checks would benefit from specific cache policies:

| Proposed Check | Suggested Strategy | Reason |
|---------------|-------------------|--------|
| `api-contract-validation` | `always_rerun` | OpenAPI specs change with any route update |
| `dependency-vuln-scan` | `ttl`, max 86400s | CVE databases update daily |
| `openapi-schema-diff` | `fingerprint` | Only rerun when routes or schemas change |

**Fix Required:**
- Add at least the `api-contract-validation` and `dependency-vuln-scan` policy overrides.

---

## Improvement 2 — The `script/mapping.yaml` Should Be Updated for New FastAPI Checks

**File:** `script/mapping.yaml`

New FastAPI-specific script checks are not yet wired into the mapping. The proposal mentions API contract validation as a build check. This should be added to the mapping:

```yaml
- check: openapi-schema-valid
  domain: 14-build
  category: A
  consumed_by:
    - { audit_type: deterministic, domain: 14-build, rule_id: build-doc-fastapi-001 }

- check: api-endpoint-reachable
  domain: 11-prototype
  category: A
  consumed_by:
    - { audit_type: deterministic, domain: 11-prototype, rule_id: prot-doc-fastapi-001 }
```

---

## Improvement 3 — Add a `02-philosophy` Backend Addendum

**File:** `documentation-standards/02-philosophy-standards.md`

The proposal says KEEP for philosophy, but there is an opportunity to document backend-specific philosophical principles that underpin the FastAPI system without breaking the generic base.

Suggested additions:
- **Explicit Over Implicit:** FastAPI's design philosophy (explicit dependencies via DI, explicit type annotations) aligns with a principle that should be documented.
- **Fail Fast at Boundaries:** Validate at entry points (Pydantic) and never let invalid data propagate into business logic.
- **Transport Independence:** Business logic must not depend on HTTP transport details.

---

## Improvement 4 — Template Generation Templates Should Reference Each Other

**Issue:** The new templates (`12-layered_architecture.md`, `18-layer_implementation.md`, etc.) are standalone stubs with no cross-references.

Well-formed templates (e.g., `01-purpose.md`) include `**Required cross-references:**` to declare dependencies on other sections. The new backend templates should declare their cross-references:

| Template | Should Cross-Reference |
|----------|----------------------|
| `05-architecture/12-layered_architecture.md` | Architecture Purpose (01), Component Model (03), Communication Paths (04) |
| `07-engineering/09-versioning.md` | Engineering Constraints (07), Build Standards (03) |
| `10-feature-technical/18-layer_implementation.md` | Architecture Layered Architecture (12), Engineering Code Standards (06) |

---

## Improvement 5 — `calculation/` Directory Should Have FastAPI Domain Weights

**Directory:** `calculation/`

The `calculation/README.md` states the layer is generic and shared. However, the proposal explicitly states:

> "Weight and severity adjustments happen inside `audit/deterministic/{domain}/*.yaml` files"

The current deterministic YAMLs in `fastapi_dev` have not had weights adjusted. For a FastAPI system, some rules warrant higher severity:

| Domain | Rule Area | Suggested Weight Increase |
|--------|-----------|--------------------------|
| `07-engineering` | Async usage violations | HIGH (currently unweighted) |
| `05-architecture` | Layered boundary violations | HIGH |
| `03-security` | Auth/authz missing | CRITICAL |
| `12-qa` | No API integration test | MEDIUM |

**Fix Required:**
- Review `audit/deterministic/document/` YAML files for `07-engineering`, `05-architecture`, `03-security`, and `12-qa`.
- Increase severity weights for FastAPI-specific violations.

---

## Improvement 6 — Add a `fastapi_dev` System Identifier File

**Suggestion:** Add a `SYSTEM.md` or `system.toml` file at the root of `fastapi_dev/` that declares:

```toml
[system]
id = "fastapi_dev"
base = "base_dev"
version = "1.0.0"
domains = 14
dropped_from_base = ["06-design", "09-feature-design"]
technology = "Python / FastAPI"
methodology = "Layered Backend Engineering"
```

This would allow tools to detect system metadata without reading all documentation standards, and provides a quick audit entry point. Currently no such file exists — a developer opening `fastapi_dev/` for the first time has no quick orientation document.
