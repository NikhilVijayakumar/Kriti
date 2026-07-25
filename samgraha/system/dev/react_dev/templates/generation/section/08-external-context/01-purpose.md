# Purpose — Generation Template

> **Domain:** external-context
> **Section:** purpose
> **Source:** `documentation-standards/08-external-context-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/08-external-context-relationships.yaml`

Generate the Purpose section for an External Context document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `informs` | engineering / code_standards | Purpose must clearly state why this external dependency matters for engineering decisions |
| `informs` | feature_design / design_rationale | Purpose must explain how this dependency influences design choices |
| `informs` | feature_technical / component_responsibilities | Purpose must establish what knowledge contributors need about this external system |

## Template

```markdown
## Purpose

[1 sentence: what this external dependency is and why it exists in this project's ecosystem]

[1 sentence: what knowledge contributors need about this dependency to implement integrations correctly]

[1 sentence: distinction from package dependency documentation — this documents knowledge, not package manifests]

[1 sentence: the atomic-per-dependency principle — one document per external dependency]
```

> **Generation note:** The standard's Purpose section serves double duty — it defines External Context Documentation as a concept (meta-level) AND is used as the template for system-specific external context documents. When generating for a specific external dependency, fill this template with *that dependency's* specific purpose: what it is, why it matters, and what knowledge it imposes. The meta-level "This document defines the standard for External Context Documentation..." language belongs in the standard itself, not in a generated document.

## Examples

**Correct:**
> Prana is the shared runtime that provides event-driven message routing for all Saṃgraha subsystems. Contributors need to understand Prana's subscription model, delivery guarantees, and retry semantics to implement integration points correctly. This document captures knowledge dependencies — the understanding contributors need about Prana — not package manifests or version management. Each External Context document describes a single external dependency, making the collection atomic and independently maintainable.

**Incorrect:**
> External Context Documentation covers npm packages, pip dependencies, and Cargo crates required by the project. It lists version numbers and installation commands.
> *Why wrong: Conflates External Context with package dependency documentation. External Context captures knowledge about external systems, not package manifests.*

## Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State what the external dependency is in one declarative sentence; draw a clear boundary between knowledge dependencies and package dependencies; reference the atomic-per-dependency principle explicitly
- **Don't:** Describe internal architecture or implementation details; list package managers or version numbers; use inspirational or motivational language

**Minimum content:** 2 paragraphs
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** none

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
