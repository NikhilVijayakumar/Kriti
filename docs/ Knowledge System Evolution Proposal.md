# Knowledge System Evolution Proposal

## Purpose

`base_dev` is the canonical software development Knowledge System.

Technology-specific Knowledge Systems (e.g. `react_dev`, `fastapi_dev`, `electron_dev`, `rust_dev`) are complete, standalone Knowledge Systems derived manually from `base_dev`.

There is no inheritance or runtime composition.

The purpose of this proposal is to define **what should and should not change** when creating a specialized Knowledge System.

---

# Design Principles

## Principle 1 — Preserve the Core Philosophy

Every development Knowledge System must preserve the engineering philosophy defined by `base_dev`.

Examples include:

- Documentation-first engineering
- Deterministic compilation
- Explicit architecture
- Modular design
- Traceability
- Documentation-driven audit
- Local-first workflow

Technology should never replace engineering principles.

---

## Principle 2 — Technology Adds, Not Replaces

A technology-specific Knowledge System should primarily **extend engineering guidance**, not redefine it.

For example:

React does not replace Architecture.

It adds React-specific architectural guidance.

FastAPI does not replace Engineering.

It adds Python/FastAPI engineering practices.

---

## Principle 3 — Keep Systems Complete

Every Knowledge System is independently usable.

A repository always references exactly one Knowledge System.

```toml
[documentation]
system = "react_dev"
```

The repository never loads multiple systems.

---

## Principle 4 — System-Specific Domain Tiers

Each system gets its own copies of these files because domain tiers differ per system:

| File | Why System-Specific |
|------|---------------------|
| `00-domain-relationships.md` | Domain tier ordering and cross-domain dependencies differ per system |
| `plan/core/tiers.yaml` | Derived from `00-domain-relationships.md` — must match system's domain list |

These files are NOT shared across systems. When creating a new system, copy these from `base_dev` then modify to reflect the system's domain scope.

Example tier differences:

| System | Domains | Tiers Changed |
|--------|---------|---------------|
| `base_dev` | 16 | Original — all tiers |
| `react_dev` | 16 | Same domains, reordered tiers |
| `fastapi_dev` | 14 | Drops 06-design, 09-feature-design |
| `electron_dev` | 16 | Same domains, reordered tiers |
| `rust_dev` | 13 | Drops 06-design, 09-feature-design, 11-prototype |

---

# Verification Matrix

When creating a new Knowledge System, review every exported capability.

---

## Domain Relationships

Review `00-domain-relationships.md` for tier mapping changes. Each system gets its OWN copy — this file is system-specific.

Questions

- Are domains being added or removed?
- Does the tier ordering change?
- Are cross-domain dependencies affected?
- Does `plan/core/tiers.yaml` need to be updated to match?

---

## Documentation Standards

Review every documentation standard.

| Standard | Verify |
|----------|--------|
| Vision | Generic or technology specific? |
| Philosophy | Still valid? |
| Security | Framework security considerations? |
| Feature | Generic |
| Architecture | Framework architecture patterns |
| Design | Framework design conventions |
| Engineering | Language/framework best practices |
| External Context | Additional framework references |
| Feature Design | UI/API specific additions |
| Feature Technical | Framework implementation guidance |
| Prototype | Technology prototyping differences |
| QA | Framework testing strategy |
| Implementation | Framework implementation practices |
| Build | Build tooling differences |
| README | Installation/build changes |
| Product Guide | Framework-specific guidance |

---

## Audit Knowledge

Review every audit domain. Audit knowledge lives in nested domain folders: `audit/semantic/section/{domain}/*.md`.

Questions:

- Are there framework-specific anti-patterns?
- Are there common mistakes?
- Are there framework best practices?
- Should severity change?
- Are new audit rules required?

Examples

React

- Hook misuse
- State management
- Dependency arrays
- Context overuse
- Component decomposition

FastAPI

- Async usage
- Dependency Injection
- Response models
- OpenAPI
- Validation

Rust

- Ownership
- Borrowing
- Error handling
- Unsafe
- Lifetimes

---

## Templates

Determine whether framework-specific templates are required.

Content is injected into existing numbered slots per domain. Each system gets its own domain ordering based on scope (e.g., FastAPI removes 06-design, 09-feature-design; Rust removes 06-design, 09-feature-design, 11-prototype).

Templates follow the strict numbered slot convention: `templates/generation/section/{domain}/{NN-name}.md`.

---

## Product Guide

Determine whether additional help documentation is required.

Examples

React

- Component lifecycle
- Hooks
- Routing
- Build

Electron

- IPC
- Main process
- Renderer
- Packaging

FastAPI

- Dependency Injection
- OpenAPI
- Middleware

Rust

- Cargo
- Crates
- Modules
- Traits

---

## Calculations

Review scoring. The calculation layer (`calculation/README.md`) is generic and shared across all systems — it does NOT get forked.

Weight and severity adjustments happen inside `audit/deterministic/{domain}/*.yaml` files, not in `calculation/*.yaml`.

Questions

- Do some audit rules become more important?
- Should weights change?
- Are additional metrics required?

Example

React

Accessibility rules in `audit/deterministic/03-security/*.yaml` may receive higher weight.

Rust

Unsafe rules in `audit/deterministic/07-engineering/*.yaml` may receive higher weight.

---

## Plans

The `plan/` directory is a fixed 8-tier document generation/audit engine (`plan/core/loop.yaml`, `plan/core/tiers.yaml`, `plan/usecase/`). It is NOT a feature-dev phase system.

Technology-specific Knowledge Systems do NOT fork or modify `plan/`. The engine is shared across all systems.

---

## Scripts

The `script/` directory is an audit verification pipeline (`script/schema/{domain}/{check}.manifest.yaml`, `script/mapping.yaml`, `script/policy.yaml`). It is NOT a scaffolding generator.

Scaffolding scripts (create-component, create-router, etc.) are NEW subsystems proposed for creation. They are NOT part of the existing `script/` audit verification infrastructure and would require a separate subsystem if implemented.

---

# Framework Evaluation Checklist

Before creating a new Knowledge System ask:

## Engineering

Does the framework introduce unique engineering practices?

YES → update Engineering

---

## Architecture

Does the framework encourage a different architecture?

YES → update Architecture

---

## Design

Does UI/API design differ?

YES → update Design

---

## Build

Does the framework have a unique build process?

YES → update Build

---

## QA

Does testing significantly differ?

YES → update QA

---

## Security

Does the framework introduce security considerations?

YES → update Security

---

## Implementation

Does implementation style differ?

YES → update Implementation

---

## Product Guide

Would users need framework-specific documentation?

YES → update Product Guide

---

## Templates

Would generated artifacts differ?

YES → add templates

---

## Audit

Can framework misuse be detected?

YES → add audit rules

---

# Evolution Policy

A new Knowledge System should not be created simply because a new language or framework exists.

Create a new Knowledge System only if it introduces meaningful differences in:

- Engineering
- Architecture
- Design
- Implementation
- Build
- QA
- Security
- Audit
- Templates
- Product Guide

If only minor wording changes are required, continue using `base_dev`.

---

# Maintenance Policy

`base_dev` remains the canonical engineering Knowledge System.

When `base_dev` evolves:

1. Review every derived Knowledge System.
2. Determine whether the change is:
   - Universal
   - Framework-specific
3. Apply only relevant changes.

Technology-specific systems intentionally evolve independently after creation.

No automatic synchronization or inheritance exists.

---

# Success Criteria

A Knowledge System is considered complete when:

- It is independently usable.
- It provides clear framework-specific engineering guidance.
- It preserves the core philosophy of `base_dev`.
- It introduces meaningful value beyond `base_dev`.
- It avoids unnecessary duplication while remaining self-contained.
- A repository can select it without requiring any additional Knowledge System.