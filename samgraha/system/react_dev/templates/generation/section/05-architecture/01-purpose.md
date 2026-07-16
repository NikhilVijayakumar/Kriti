# Purpose — Generation Template

> **Domain:** architecture
> **Section:** purpose
> **Source:** `documentation-standards/05-architecture-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the Purpose section for an Architecture document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / purpose | Architecture Purpose must align with and derive from the Vision document's Purpose |
| `guided_by` | philosophy / guiding_principles | Architecture Purpose must be consistent with the project's guiding principles |

## Template

```markdown
## Purpose

> **Architectural purpose:** [1-2 sentences: why this architecture exists, what problems it solves, what qualities it optimizes for]

> **Scope boundaries:**
> - **In scope:** [architectural concerns this document covers]
> - **Out of scope:** [architectural concerns explicitly excluded, with reason]

> **Primary goals:** [ranked list of architectural priorities — e.g. scalability > maintainability > cost]
```

> **Generation note:** The standard's Purpose section serves double duty — it defines Architecture Documentation as a concept (meta-level) AND is used as the template for system-specific architecture documents. When generating for a specific system, fill this template with *that system's* architectural purpose: why this architecture exists, what problems it solves, and what qualities it prioritizes. The meta-level "This document defines the standard for Architecture Documentation..." language belongs in the standard itself, not in a generated document.

## Examples

**Correct (system-specific):**
> **Architectural purpose:** This architecture supports real-time inventory tracking across 50 warehouses with sub-second update latency. The primary problem is maintaining consistency across distributed inventory states during concurrent modifications from warehouse operators and e-commerce orders.
>
> **Scope boundaries:**
> - **In scope:** Inventory state synchronization, conflict resolution, warehouse-side data ownership
> - **Out of scope:** E-commerce order processing (covered by Feature Design), warehouse physical layout
>
> **Primary goals:** 1. Consistency under concurrent access, 2. Sub-second propagation, 3. Offline resilience per warehouse

**Correct (meta-level — only when generating the standard itself, not a system document):**
> This document defines the standard for Architecture Documentation within the engineering documentation ecosystem. Architecture Documentation describes the structural organization of a system — how responsibilities are divided among components and how those components relate. Unlike a single Vision or Feature document, Architecture is a collection of focused documents, each covering one structural concern.

**Incorrect:**
> Architecture Documentation covers the microservices layout, the React component tree, the PostgreSQL schema, and the Kubernetes deployment manifests used by the system.
> *Why wrong: names specific technologies and implementation artifacts instead of stating the architectural purpose and scope boundaries.*

## Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State the architectural purpose specific to this system; define scope boundaries explicitly (in-scope vs. out-of-scope); rank primary goals to guide trade-off decisions; derive from Vision document's Purpose and Philosophy's guiding principles
- **Don't:** Use generic mission statements; copy purpose from project charter or README; include goals without architectural impact; leave scope boundaries implicit

**Minimum content:** 2 paragraphs
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** none

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
