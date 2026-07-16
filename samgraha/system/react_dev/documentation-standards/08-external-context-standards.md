# External Context Standard

> *Deterministic rules for this domain: `audit/deterministic/document/08-external-context.yaml`*

## Table of Contents
- [Purpose](#purpose)
  - [Template](#template-1)
- [Integration Contract](#integration-contract)
  - [Template](#template-2)
- [Constraints](#constraints)
  - [Template](#template-3)
- [Dependencies](#dependencies)
  - [Template](#template-4)
- [Required Sections](#required-sections)
- [Goals](#goals)
- [Non-Goals](#non-goals)
- [Success Criteria](#success-criteria)
- [Responsibilities](#responsibilities)
- [Scope](#scope)
- [Out of Scope](#out-of-scope)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [Traceability](#traceability)
  - [Template](#template-5)
- [Relationships](#relationships)
- [Required Characteristics](#required-characteristics)
- [Audit Rules](#audit-rules)
- [Validation Rules](#validation-rules)
- [Generation Rules](#generation-rules)
- [Enhancement Rules](#enhancement-rules)
- [Summary](#summary)
- [Common Mistakes](#common-mistakes)
- [Documentation Folder](#documentation-folder)
- [Usage](#usage)
- [Related](#related)
- [External Context as an Atomic Collection](#external-context-as-an-atomic-collection)
- [Atomicity](#atomicity)
- [Dependency Types](#dependency-types)
- [Internal Dependencies](#internal-dependencies)
- [External Platforms](#external-platforms)
- [Standards and Protocols](#standards-and-protocols)
- [Domain Knowledge](#domain-knowledge)
- [Knowledge Dependency Principles](#knowledge-dependency-principles)
- [Documentation Ownership](#documentation-ownership)
- [Technology Selection](#technology-selection)
- [Quality Requirements](#quality-requirements)

---


## Purpose

> *Structural rules: `audit/deterministic/section/08-external-context/01-purpose.yaml`*

### Template

> **minimum_content:** 2 paragraphs
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
[One sentence stating what External Context Documentation is and its role in the documentation ecosystem]
[One sentence distinguishing External Context from traditional dependency documentation]
[One sentence stating what External Context documents — knowledge dependencies, not package dependencies]
[One sentence on the atomic-per-dependency principle]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> External Context Documentation captures knowledge dependencies that live outside the repository but materially influence implementation. It is distinct from package dependency documentation, which tracks library versions and build artifacts. External Context documents **knowledge dependencies** — the understanding contributors need about external systems to design and implement integrations correctly. Each document describes a single external dependency, making the collection atomic and independently maintainable.

**Incorrect:**
> External Context Documentation covers npm packages, pip dependencies, and Cargo crates required by the project. It lists version numbers, installation commands, and upgrade procedures for each library.
> *Why wrong: This conflates External Context with package dependency documentation. External Context captures knowledge about external systems, not package manifests or version management.*

### Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State what External Context is in one declarative sentence; draw a clear boundary between knowledge dependencies and package dependencies; reference the atomic-per-dependency principle explicitly
- **Don't:** Describe internal architecture or implementation details; list package managers or version numbers; use inspirational or motivational language

This document defines the standard for External Context Documentation within the engineering documentation ecosystem.

External Context Documentation describes knowledge that exists **outside the current repository** but is required to correctly understand, design, implement, or maintain the repository.

Unlike traditional dependency documentation, External Context does not document package dependencies.

Instead, it documents **knowledge dependencies**.

Each External Context document describes one external system, library, platform, protocol, or project that materially influences the repository.

Projects may contain zero, one, or many External Context documents depending on their dependencies.

---

## Integration Contract

> *Structural rules: `audit/deterministic/section/08-external-context/02-integration_contract.yaml`*

### Template

> **minimum_content:** 1 subsection
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
[Integration surface overview — what the external system exposes]

## Endpoints / Protocols

[Description of available endpoints, protocols, and communication patterns]

## Data Formats

[Request and response formats, encoding, content types]

## Authentication

[Authentication mechanisms, credentials handling, token lifecycle]

## Error Handling

[Error codes, retry policies, rate limiting behavior]

## Versioning

[Version compatibility, deprecation policy, migration guidance]
```

**Required subsections:** Endpoints / Protocols, Authentication
**Optional subsections:** Data Formats, Error Handling, Versioning
**Required diagrams:** none
**Required cross-references:** authoritative external documentation

### Examples

**Correct:**
> The external system exposes a REST API over HTTPS. Authentication uses OAuth 2.0 client credentials flow. Requests must include a Bearer token in the Authorization header. The API supports JSON request and response bodies. Rate limiting is enforced at 100 requests per minute. Versioning follows a URL path prefix model (`/v1/`, `/v2/`). Authoritative documentation: `https://docs.externalsystem.example/api`.

**Incorrect:**
> Here is the code we use to call the API:
> ```python
> import requests
> resp = requests.post("https://api.externalsystem.example/v1/data",
>                       headers={"Authorization": f"Bearer {token}"},
>                       json=payload)
> ```
> *Why wrong: This includes implementation code rather than describing the contract. The Integration Contract should define what the external system exposes, not how the repository calls it. Implementation details belong in Engineering.*

### Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Describe the external system's contract surface in implementation-neutral terms; always include the authoritative documentation URL; distinguish required endpoints from optional ones
- **Don't:** Paste code snippets or client implementations; document internal request/response transformation logic; omit authentication mechanism details

*(To be written by the integrating engineer. This section defines the formal interface contract with the external system.)*

---

## Constraints

> *Structural rules: `audit/deterministic/section/08-external-context/03-constraints.yaml`*

### Template

> **minimum_content:** 1 subsection
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
[Overview of constraints the external system imposes on the repository]

## Functional Constraints

[Limitations on what the integration can or cannot do]

## Performance Constraints

[Rate limits, latency requirements, throughput boundaries]

## Legal / Compliance Constraints

[Licensing restrictions, regulatory obligations, data handling rules]
```

**Required subsections:** none
**Optional subsections:** Functional Constraints, Performance Constraints, Legal / Compliance Constraints
**Required diagrams:** none
**Required cross-references:** authoritative external documentation

### Examples

**Correct:**
> The external platform enforces a maximum payload size of 1 MB per request. API calls are limited to 10 requests per second with a burst allowance of 20. Data stored by the platform must comply with GDPR; no personal data may be stored in fields the platform retains beyond 30 days. The platform requires a minimum TLS version of 1.2. All constraints are sourced from the platform's published service limits documentation.

**Incorrect:**
> We decided to use connection pooling because our application needs high throughput. Our team prefers TypeScript over JavaScript for type safety. We chose PostgreSQL for the database layer.
> *Why wrong: These are internal design decisions, not constraints imposed by the external system. External Constraints must originate from the external dependency, not from internal project choices.*

### Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Categorize every constraint by type (functional, performance, legal, compliance); cite the external source for each constraint; state limits as specific numeric values where possible
- **Don't:** List internal project decisions as constraints; use vague qualifiers like "may" or "should" for hard limits; omit constraints that affect data handling or compliance

*(To be written by the integrating engineer. This section defines the limitations imposed by the external dependency.)*

---

## Dependencies

> *Structural rules: `audit/deterministic/section/08-external-context/04-dependencies.yaml`*

### Template

> **minimum_content:** 1 subsection
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
[Overview of what the external system itself requires to function]

## Runtime Dependencies

[Transitive runtime requirements — platforms, services, companion systems]

## Build-Time Dependencies

[Development or build-time prerequisites, if any]
```

**Required subsections:** none
**Optional subsections:** Runtime Dependencies, Build-Time Dependencies
**Required diagrams:** none
**Required cross-references:** other External Context documents for transitive dependencies

### Examples

**Correct:**
> The external platform requires a running message broker as a runtime dependency — without it, webhook delivery fails silently. It also requires a valid TLS certificate for all inbound connections. At build time, the platform's CLI tool must be installed for schema validation. These are transitive requirements of the platform itself, not choices made by this repository.

**Incorrect:**
> This project depends on Express.js for HTTP routing, Mongoose for database access, and Jest for testing.
> *Why wrong: These are internal project dependencies (package.json entries), not transitive dependencies of the external system. The Dependencies section describes what the external dependency itself requires, not what this repository packages.*

### Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Distinguish runtime dependencies from build-time dependencies explicitly; note criticality level for each transitive dependency; cross-reference other External Context documents when a transitive dependency is itself documented
- **Don't:** List this repository's package.json or requirements.txt entries; include development tooling or test frameworks; omit companion systems that the integration silently depends on

*(To be written by the integrating engineer. This section defines what the external dependency itself requires.)*

---

## Required Sections

Every External Context document must contain the following sections.
Sections are identified by heading text; the compiler maps each to a semantic type.

| Section | semantic_type | Required | Aliases | Content Requirements |
|---------|--------------|----------|---------|----------------------|
| Purpose | `purpose` | ✓ | Overview, Summary | State why external context exists, what it documents, what it does not; distinguish from package dependency documentation |
| Integration Contract | `integration_contract` | ✓ | Contract, API Contract, Interface | Endpoints, protocols, data formats, authentication, error behaviors, versioning; reference authoritative API docs |
| Constraints | `constraints` | | Limitations, Non-Functional Requirements | Categorized limitations (functional, performance, legal, compliance) sourced from the external system |
| Dependencies | `dependencies` | | Dependency, Depends On | Transitive requirements, platform prerequisites, companion systems; distinguish runtime from build-time; note criticality |
| Traceability | `traceability` | | Traces To, Derived From | Tier diagram showing External Context's influence; list of consuming standards; non-duplication rule stated |

Section headings are case-insensitive. Sections not listed here are stored as `generic` type — preserved but not queryable by type.

---

## Goals

External Context Documentation aims to:

* Document why each external dependency exists and what it's used for.
* Prevent tribal knowledge about integrations from living only in one engineer's head.
* Make external constraints traceable to the features and technical designs they affect.

---

## Non-Goals

External Context does not define:

* Internal Features
* Internal Design
* Internal Architecture
* Engineering Decisions
* Package Management
* Dependency Versions
* Source Code
* API Reference Manuals

These responsibilities belong to other documentation standards or to the external project's own documentation.

---

## Success Criteria

External Context Documentation is successful when:

* Engineers understand why external dependencies exist.
* AI systems understand how external systems influence implementation.
* Internal documentation avoids duplicating external knowledge.
* Repository-specific dependency decisions are clear.
* Contributors know where authoritative documentation resides.
* External changes can be accommodated without rewriting internal documentation.

---

## Responsibilities

External Context Documentation is responsible for describing:

* External systems
* External libraries
* Internal shared projects
* Shared frameworks
* Shared protocols
* External platforms
* Integration contracts
* Knowledge dependencies
* Constraints introduced by external systems
* Referenced documentation

External Context explains **what external knowledge contributors must understand**.

It does not replace the documentation owned by the external project.

---

## Scope

External Context may describe:

* Internal shared libraries
* Internal frameworks
* Shared runtime platforms
* Shared protocols
* External APIs
* Operating system services
* Platform capabilities
* AI platforms
* Communication standards
* File formats
* Industry specifications
* Regulatory standards

Each document should describe one external dependency.

---

## Out of Scope

External Context must not describe:

* Internal repository architecture
* Internal feature specifications
* Source code
* Package manifests
* Build configuration
* Version management
* Library APIs
* Installation procedures
* Complete third-party documentation

External Context should summarize and reference.

It should not duplicate.

---

## Inputs

External Context derives from:

* External documentation
* Project documentation
* Architecture
* Engineering decisions

External Context should summarize relevant knowledge.

It should not replace the original documentation.

---

## Outputs

External Context provides guidance for:

* Features
* Feature Design
* Architecture
* Feature Technical Design
* Engineering
* Implementation

Any document may reference External Context rather than duplicating external knowledge.

---

## Traceability

> *Structural rules: `audit/deterministic/section/08-external-context/05-traceability.yaml`*

### Template

> **minimum_content:** 1 diagram, 1 subsection
> **length_guidance:** concise
> **diagram_requirements:** flowchart

```markdown
## Influence Diagram

[Text-based tier diagram showing External Context's position relative to downstream standards]

## Consuming Standards

[List of documentation domains that reference External Context]
```

**Required subsections:** Influence Diagram, Consuming Standards
**Optional subsections:** none
**Required diagrams:** flowchart (tier diagram)
**Required cross-references:** Feature Technical Design(10), Engineering(07), Architecture(05)

### Examples

**Correct:**
> External Context informs Feature Technical Design by surfacing integration constraints before implementation begins. It informs Architecture by revealing system boundaries and platform requirements. It informs Engineering by providing rationale for technology choices tied to the external dependency. Downstream standards **reference** External Context rather than duplicating its content.

**Incorrect:**
> Traceability shows that External Context was last updated in March and is owned by the platform team. It includes a changelog of all edits made to the document.
> *Why wrong: Traceability in this context means showing how External Context influences downstream documentation standards, not tracking document metadata or ownership history. Version tracking belongs in change management, not in the Traceability section.*

### Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** diagrams
- **Audience:** architect
- **Do:** Include a text-based tier diagram showing External Context's lateral position; list every downstream standard that consumes External Context by name; explicitly state the non-duplication rule (reference, don't copy)
- **Don't:** Include version history or changelog entries; treat Traceability as document metadata; omit a standard from the consuming list if it references External Context content

External Context supports multiple documentation domains.

```text
Vision

↓

Features

↓

Feature Design

↓

Architecture

↓

Feature Technical Design

↓

Engineering

         ↑

 External Context
```

External Context informs documentation.

It does not redefine it.

---

## Relationships

| Document                 | Relationship                               |
| ------------------------ | ------------------------------------------ |
| Vision                   | Usually independent                        |
| Feature                  | May reference functional capabilities      |
| Feature Design           | May reference design constraints           |
| Architecture             | May reference architectural constraints    |
| Feature Technical Design | Frequently references External Context     |
| Engineering              | Frequently references technology rationale |

---

## Required Characteristics

External Context Documentation should be:

* Accurate to the actual external system, not aspirational
* Current — reviewed when the dependency's contract changes
* Traceable to the feature/technical design it affects
* Ownership-clear (who's responsible for tracking upstream changes)
* Non-duplicative of the dependency's own documentation

---

## Audit Rules

An audit should verify:

* External dependencies are documented only when necessary.
* One document describes one dependency.
* Dependency purpose is clearly explained.
* Constraints are documented.
* External documentation is referenced rather than duplicated.
* Repository relevance is obvious.
* No internal architecture has leaked into External Context.

External Context quality is evaluated individually and across the documentation collection.

---

## Validation Rules

External Context is considered valid when:

* One document describes one external dependency.
* The dependency is clearly identified.
* The purpose of the dependency is explained.
* Constraints are documented.
* Repository usage is described.
* External documentation is referenced where appropriate.
* Duplicate documentation has been avoided.

Validation applies independently to each External Context document.

---

## Generation Rules

When generating External Context:

* Create one document per dependency.
* Explain why the dependency exists.
* Explain how it influences the repository.
* Reference authoritative documentation.
* Keep documentation concise.
* Avoid duplication.
* Focus on repository relevance rather than completeness.

---

## Enhancement Rules

When enhancing External Context:

* Improve clarity.
* Improve dependency justification.
* Remove duplicated documentation.
* Strengthen repository relevance.
* Improve references.
* Split oversized documents.
* Preserve dependency intent.

External Context should become easier to understand and maintain.

---

## Summary

External Context Documentation is a collection of atomic knowledge documents that describe external dependencies required to understand and implement a repository.

Its purpose is not to replace external documentation, but to explain **why a dependency exists, how it influences the repository, and where the authoritative knowledge resides**, allowing project documentation to remain concise, maintainable, and free of unnecessary duplication.

---

## Common Mistakes

Examples include:

* Copying vendor documentation.
* Documenting package manifests.
* Explaining every API.
* Duplicating Architecture.
* Duplicating Engineering.
* Describing implementation.
* Mixing multiple unrelated dependencies.

These should be reported during audits.

---

## Documentation Folder

External Context documents live under:

```text
docs/raw/external-context/
```

---

## Usage

Written by whoever integrates a new external dependency, one document per dependency, only when the dependency materially influences implementation. Use `samgraha search --domain external-context` to check whether a dependency is already documented before writing a new one, avoiding duplicate External Context files for the same system.

## Related

- [Feature Technical Standard](10-feature-technical-standards.md) — frequently references External Context
- [Engineering Standard](07-engineering-standards.md) — frequently references technology rationale
- [Standards Reference Standard](standards.md) — how this standard itself is documented

## External Context as an Atomic Collection

External Context Documentation is organized as a collection of independent documents.

Example:

```text
external-context/

    astra.md

    prana.md

    mcp.md

    electron.md

    sqlite.md
```

Each document describes one external dependency.

Projects may have:

* No External Context
* One External Context
* Multiple External Context documents

depending on project requirements.

---

## Atomicity

Every External Context document should describe one external dependency.

Examples include:

* Astra
* Prana
* MCP
* Electron
* SQLite
* Google Drive
* OAuth

Large documents should be decomposed into multiple focused documents.

---

## Dependency Types

External Context may describe:

## Internal Dependencies

Projects maintained within the same engineering ecosystem.

Examples:

* Astra
* Prana
* Prati
* Saṃgraha

---

## External Platforms

External systems that influence implementation.

Examples:

* Electron
* Android
* Windows
* Azure

---

## Standards and Protocols

Shared specifications.

Examples:

* MCP
* OAuth
* OpenAPI
* JSON Schema

---

## Domain Knowledge

Knowledge required to correctly implement the project.

Examples:

* Accessibility Guidelines
* Security Standards
* Regulatory Requirements

---

## Knowledge Dependency Principles

External Context should:

* Explain why the dependency exists.
* Explain which capabilities are used.
* Explain architectural constraints.
* Explain implementation implications.
* Reference authoritative documentation.
* Avoid duplication.

The purpose is understanding, not documentation ownership.

---

## Documentation Ownership

External Context does **not** own the external documentation.

It should:

* summarize
* explain relevance
* define dependency boundaries
* reference the authoritative source

If the external project changes, External Context should be updated accordingly.

---

## Technology Selection

External Context should document technologies only when they materially influence implementation.

Examples:

Appropriate:

* Astra Framework
* Prana Runtime
* MCP
* Electron
* SQLite

Generally unnecessary:

* React
* Axios
* Lodash
* Zod

Widely understood libraries should not require External Context unless project-specific conventions exist.

---

## Quality Requirements

External Context should be:

* Atomic
* Concise
* Relevant
* Traceable
* Maintainable
* Repository focused
* Easy to reference
* Free of duplication

Each document should justify why the dependency matters.

---

## Frontend Engineering Context

This standard applies to frontend engineering with the following focus areas:

### UI Framework

Component library selection criteria: TypeScript support, theme customization, accessibility compliance, bundle size, community support. Preference for MUI or equivalent with token-based theming.

### State Management

No external state management libraries. Context + useState for all state. Cross-cutting state via Context providers. UI-local state via useState. Props-down convention.

### Styling

CSS-in-JS vs CSS modules decision framework: CSS modules preferred for co-location and no runtime. CSS-in-JS acceptable for dynamic theming. Tailwind acceptable for utility-first approach. No inline styles.

### Testing

Vitest as test runner. @testing-library/react for component testing. @testing-library/user-event for interactions. vi.mock() for mocking. Co-located test files.

### Build

Vite preferred for dev server speed and build optimization. Webpack acceptable for legacy projects. Code splitting required for routes and heavy components.

### Data Fetching

Server state vs client state separation. Server state via data fetching hooks. Client state via Context + useState. No global cache for server state.

### i18n

Key-value translation maps. No library preference. useLanguage() hook pattern. Translation files per language. Fallback chains for missing keys.
