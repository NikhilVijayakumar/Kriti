# Backend Development using FastAPI - Knowledge System Proposal

## Overview

This proposal defines how to transform `fastapi_dev` from a clone of `base_dev` into a standalone engineering methodology for building backend systems using FastAPI.

**Base System**: `base_dev` (canonical, unchanged)
**Target System**: `fastapi_dev` (standalone, backend engineering methodology)

**Core Shift**: This is NOT a FastAPI guide. This is YOUR backend engineering methodology implemented with FastAPI.

---

## Pattern Sources

Patterns derived from real-world implementations. These sources informed the standards but are NOT referenced in the generated standards.

| Source | Location | Patterns Derived |
|--------|----------|------------------|
| **Astra** | `E:\Python\astra` | Repository pattern, Service layer, Transport abstraction, Error normalization |
| **Prati** | `E:\Python\Prati` | Design tokens, Component architecture (for API contract design) |

---

## External Reference Isolation (MANDATORY)

**Rule**: All external references (Astra, Prati, Prana, etc.) are confined to THIS proposal document ONLY.

**Generated standards must NOT contain:**
- Names of external systems (Astra, Prati, Prana, etc.)
- File paths to external repositories
- References to specific implementations
- Links to external documentation

**Generated standards MUST contain:**
- Generic patterns derived from external systems
- Technology-agnostic concepts
- Framework-specific guidance (FastAPI, Python, etc.)
- Self-contained, independently usable standards

**How patterns are "baked in":**

| External Pattern | Standardized As (In Standard) |
|------------------|------------------------------|
| Astra Repository pattern | Repository pattern (generic) |
| Astra Service layer | Service layer pattern (generic) |
| Astra Transport abstraction | Transport-agnostic data access |
| Astra Error normalization | Normalized response objects |
| Prati Design tokens | Token-based styling (generic) |

**Verification**: This leak-check is a natural fit for the `script/` audit pipeline (same shape as `secret-scan`). Currently unenforced — flagged as future work.

---

## Core Philosophy (PRESERVE)

All engineering principles from `base_dev` remain unchanged:

- Documentation-first engineering
- Deterministic compilation
- Explicit architecture
- Modular design
- Traceability
- Documentation-driven audit
- Local-first workflow

---

## System-Specific Files

Each system gets its own copies of these files because domain tiers differ per system:

| File | Why System-Specific |
|------|---------------------|
| `00-domain-relationships.md` | Domain tier ordering and cross-domain dependencies differ per system |
| `plan/core/tiers.yaml` | Derived from `00-domain-relationships.md` — must match system's domain list |

These files are NOT shared across systems. When creating `fastapi_dev`, copy these from `base_dev` then modify to reflect the system's domain scope.

---

## Domain Scope

### Domains KEPT (14 of 16)

| Tier | Domain | Standard File | Action |
|------|--------|---------------|--------|
| 1 | 01-vision | `01-vision-standards.md` | KEEP + add backend vision |
| 1 | 02-philosophy | `02-philosophy-standards.md` | KEEP |
| 2 | 03-security | `03-security-standards.md` | KEEP + add API security |
| 2 | 04-feature | `04-feature-standards.md` | KEEP + add backend feature definition |
| 2 | 05-architecture | `05-architecture-standards.md` | KEEP + add layered architecture |
| 2 | 07-engineering | `07-engineering-standards.md` | KEEP + add Python/FastAPI patterns |
| 2 | 08-external-context | `08-external-context-standards.md` | KEEP + add technology categories |
| 3 | 10-feature-technical | `10-feature-technical-standards.md` | KEEP + add implementation guidance |
| 4 | 11-prototype | `11-prototype-standards.md` | KEEP + add API prototyping |
| 5 | 13-implementation | `13-implementation-standards.md` | KEEP + add layer patterns |
| 6 | 12-qa | `12-qa-standards.md` | KEEP + add pytest/httpx patterns |
| 7 | 14-build | `14-build-standards.md` | KEEP + add package manager guidance |
| 8 | 15-readme | `15-readme-standards.md` | KEEP + add backend README |
| 8 | 16-product-guide | `16-product-guide-standards.md` | KEEP + add development workflow |

### Domains REMOVED (2 of 16)

| Domain | Reason |
|--------|--------|
| 06-design | UI/API design not relevant — backend has no visual layer |
| 09-feature-design | UI feature design not relevant — backend features defined in 04-feature and 10-feature-technical |

### Tier Reordering

| Tier | base_dev | fastapi_dev |
|------|----------|-------------|
| 1 | 01-vision, 02-philosophy | 01-vision, 02-philosophy |
| 2 | 03-security, 04-feature, 05-architecture, 06-design, 07-engineering, 08-external-context | 03-security, 04-feature, 05-architecture, 07-engineering, 08-external-context |
| 3 | 09-feature-design, 10-feature-technical | 10-feature-technical |
| 4 | 11-prototype | 11-prototype |
| 5 | 13-implementation | 13-implementation |
| 6 | 12-qa | 12-qa |
| 7 | 14-build | 14-build |
| 8 | 15-readme, 16-product-guide | 15-readme, 16-product-guide |

---

## Section Slot Mapping

Slot numbers match actual files on disk in `base_dev/templates/generation/section/{domain}/`. New slots are appended after the last existing slot.

### 05-architecture (11 existing, ADD 1 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add backend architecture purpose |
| 02 | `02-system_overview.md` | KEEP — generic |
| 03 | `03-component_model.md` | MODIFY — add layered architecture (Router/Service/Repository) |
| 04 | `04-communication_paths.md` | MODIFY — add DI patterns, dependency direction |
| 05 | `05-data_flow.md` | MODIFY — add ORM/Pydantic patterns |
| 06 | `06-security_considerations.md` | KEEP — generic |
| 07 | `07-rationale.md` | MODIFY — add module structure rationale |
| 08 | `08-constraints.md` | MODIFY — add API contract constraints |
| 09 | `09-traceability.md` | KEEP — generic |
| 10 | `10-operational_readiness.md` | KEEP — generic |
| 11 | `11-observability.md` | KEEP — generic |
| 12 | `12-layered_architecture.md` | **NEW SLOT** — module boundaries, dependency direction |

### 07-engineering (8 existing, ADD 2 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-guiding_principles.md` | MODIFY — add Python conventions |
| 02 | `02-rationale.md` | MODIFY — add rationale for engineering choices |
| 03 | `03-build_standards.md` | MODIFY — add build standards |
| 04 | `04-testing_standards.md` | MODIFY — add testing standards |
| 05 | `05-purpose.md` | MODIFY — add purpose |
| 06 | `06-code_standards.md` | MODIFY — add type hints, async/await, pathlib |
| 07 | `07-constraints.md` | MODIFY — add typed exceptions, Result pattern |
| 08 | `08-traceability.md` | KEEP — generic |
| 09 | `09-versioning.md` | **NEW SLOT** — API versioning, migration strategy |
| 10 | `10-migration_strategy.md` | **NEW SLOT** — database migrations, schema evolution |

### 10-feature-technical (17 existing, ADD 1 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add backend implementation purpose |
| 02-17 | (existing slots) | KEEP — generic |
| 18 | `18-layer_implementation.md` | **NEW SLOT** — Router, Service, Repository patterns |

### 12-qa (9 existing, ADD 1 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add pytest patterns |
| 02-09 | (existing slots) | KEEP — generic |
| 10 | `10-api_testing.md` | **NEW SLOT** — httpx, load testing |

### 13-implementation (6 existing, ADD 1 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add feature scaffold plan |
| 02 | (gap — slot 02 missing on disk) | — |
| 03-07 | (existing slots) | KEEP — generic |
| 08 | `08-feature_folder_structure.md` | **NEW SLOT** — directory layout |

### 14-build (8 existing, ADD 1 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add build purpose |
| 02 | (gap — slot 02 missing on disk) | — |
| 03 | `03-documentation_quality.md` | KEEP — generic |
| 04 | `04-security_checks.md` | KEEP — generic |
| 05 | `05-size_checks.md` | KEEP — generic |
| 06 | `06-ml_artifact_management.md` | KEEP — generic |
| 07 | `07-cicd_validation.md` | KEEP — generic |
| 08 | `08-obfuscation_optimization.md` | KEEP — generic |
| 09 | `09-versioning_naming.md` | KEEP — generic |
| 10 | `10-api_validation.md` | **NEW SLOT** — API contract validation, schema checks |

### 16-product-guide (6 existing, ADD 1 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-title.md` | KEEP — generic |
| 02 | `02-body.md` | KEEP — generic |
| 03 | `03-purpose.md` | KEEP — generic |
| 04 | `04-product_context.md` | KEEP — generic |
| 05 | `05-public_contract.md` | KEEP — generic |
| 06 | `06-related.md` | KEEP — generic |
| 07 | `07-development_workflow.md` | **NEW SLOT** — how we work |

---

## Engineering Methodology

### 1. Vision

> How do we build backend systems in our ecosystem?

**Answer**: We build layered, testable, maintainable backend systems with clear separation of concerns. FastAPI is our implementation technology, not our architecture.

### 2. Architecture

**Principle**: Architecture is YOURS. FastAPI is one implementation detail.

| Pattern | Standard | Alternative | Override Allowed |
|---------|----------|-------------|-----------------|
| Layered Architecture | Required | Hexagonal, Clean | Yes, with justification |
| Dependency Direction | Strict (Router→Service→Repository→Infra) | Bidirectional in same layer | No |
| Module Boundaries | Feature isolation | Shared modules with DI | Yes, document in 00-domain-relationships |

### 3. Engineering

**Principle**: Engineering is MORE than FastAPI. Framework is one part.

- Type hints EVERYWHERE
- Async/await for I/O operations
- No sync blocking in async context
- Dependency injection for cross-cutting concerns
- Response models for ALL endpoints
- No business logic in routers

### 4. Audit

**Principle**: Audit ARCHITECTURAL DRIFT, not just syntax.

Weight and severity adjustments happen inside `audit/deterministic/{domain}/*.yaml` files, NOT in `calculation/*.yaml`. The calculation layer is generic and shared across all systems.

### 5. Templates

Content is injected into existing numbered slots per domain. See **Section Slot Mapping** above.

### 6. Product Guide

Answers "How do we work?" not "What is FastAPI?"

### 7. Engineering Decisions

| Decision | Preferred Option | Alternative | Reason |
|----------|-----------------|-------------|--------|
| Framework | FastAPI | Flask, Django | Async support, auto-docs, type safety |
| ORM | SQLAlchemy (async) | Tortoise, Peewee | Mature, async support, ecosystem |
| Validation | Pydantic v2 | Marshmallow | Performance, FastAPI integration |
| Migration | Alembic | yoyo | SQLAlchemy integration |
| Testing | pytest | unittest | Fixtures, plugins, readability |

### 8. External Context

| Category | Purpose | Options |
|----------|---------|---------|
| ORM | Database abstraction | SQLAlchemy, Tortoise, SQLModel |
| Validation | Data validation | Pydantic, Marshmallow |
| Authentication | Identity verification | OAuth2, JWT, Session, API keys |
| Caching | Performance | Redis, Memcached, in-memory |
| Background Jobs | Async processing | Celery, RQ, Dramatiq |
| Messaging | Event-driven | RabbitMQ, Kafka, Redis Pub/Sub |

---

## New Subsystems (Not Integrated with Audit Script Pipeline)

The following are NEW artifact types proposed for creation. They are NOT part of the existing `script/` audit verification infrastructure (mapping.yaml, manifests, schema files). They would require a separate subsystem if implemented.

### Feature Scaffolding (Proposed)

| Script | Purpose |
|--------|---------|
| `create-feature.sh/ps1` | Scaffold complete feature (router + service + repo + schemas) |
| `create-router.sh/ps1` | Scaffold router with CRUD endpoints |
| `create-service.sh/ps1` | Scaffold service with business logic |
| `create-repository.sh/ps1` | Scaffold repository with data access |

---

## Files to Modify

### Domain Files

| File | Action |
|------|--------|
| `00-domain-relationships.md` | REPLACE — system-specific domain tier ordering (14 domains, not 16) |
| `plan/core/tiers.yaml` | REPLACE — derived from system's 00-domain-relationships.md |
| `documentation-standards/01-vision-standards.md` | ADD — backend engineering vision |
| `documentation-standards/02-philosophy-standards.md` | KEEP |
| `documentation-standards/03-security-standards.md` | ADD — API security, authentication, authorization |
| `documentation-standards/04-feature-standards.md` | ADD — backend feature definition |
| `documentation-standards/05-architecture-standards.md` | ADD — layered architecture, module boundaries |
| `documentation-standards/07-engineering-standards.md` | ADD — Python conventions, FastAPI patterns |
| `documentation-standards/08-external-context-standards.md` | ADD — technology categories |
| `documentation-standards/10-feature-technical-standards.md` | ADD — implementation guidance per layer |
| `documentation-standards/11-prototype-standards.md` | ADD — API prototyping (Swagger, ReDoc) |
| `documentation-standards/12-qa-standards.md` | ADD — pytest, httpx, API testing |
| `documentation-standards/13-implementation-standards.md` | ADD — layer implementation patterns |
| `documentation-standards/14-build-standards.md` | ADD — package manager agnostic |
| `documentation-standards/15-readme-standards.md` | ADD — backend README conventions |
| `documentation-standards/16-product-guide-standards.md` | ADD — development workflow |

### Audit Knowledge (nested domain folders)

| Path | Content |
|------|---------|
| `audit/semantic/section/05-architecture/12-layered_architecture.md` | Architectural drift rules |
| `audit/semantic/section/07-engineering/10-versioning.md` | API versioning conventions |
| `audit/semantic/section/10-feature-technical/21-layer_implementation.md` | Layer-specific rules |

### Generation Templates (nested domain folders)

| Path | Content |
|------|---------|
| `templates/generation/section/05-architecture/12-layered_architecture.md` | Module boundaries, dependency direction |
| `templates/generation/section/07-engineering/09-versioning.md` | API versioning, migration strategy |
| `templates/generation/section/07-engineering/10-migration_strategy.md` | Database migrations, schema evolution |
| `templates/generation/section/10-feature-technical/18-layer_implementation.md` | Router, service, repository |
| `templates/generation/section/12-qa/10-api_testing.md` | httpx, load testing |
| `templates/generation/section/13-implementation/08-feature_folder_structure.md` | Directory layout |
| `templates/generation/section/14-build/10-api_validation.md` | API contract validation |
| `templates/generation/section/16-product-guide/07-development_workflow.md` | How we work |

---

## Success Criteria

- [ ] `fastapi_dev` is independently usable
- [ ] Answers "How do we build backend systems?" not "What is FastAPI?"
- [ ] Documents YOUR architecture, not framework documentation
- [ ] Preserves core philosophy of `base_dev`
- [ ] Provides clear engineering methodology
- [ ] Enables consistent decision-making across projects
- [ ] All file paths match engine glob patterns
- [ ] No external system references in generated standards
