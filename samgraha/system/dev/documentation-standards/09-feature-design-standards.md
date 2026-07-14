# Feature Design Standard

## Table of Contents

> *Deterministic rules for this domain: `audit/deterministic/document/09-feature-design.yaml`*

- [Purpose](#purpose)
- [User Experience](#user-experience)
- [Workflow](#workflow)
- [States](#states)
- [Constraints](#constraints)
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
- [One-to-One Mapping](#one-to-one-mapping)
- [Design Principle Application](#design-principle-application)
- [External Context Application](#external-context-application)
- [Feature Design Principles](#feature-design-principles)
- [Technology Independence](#technology-independence)
- [Quality Requirements](#quality-requirements)

---


## Purpose

> *Structural rules: `audit/deterministic/section/09-feature-design/04-purpose.yaml`*

### Template

> **minimum_content:** 1 paragraph
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
[1 paragraph: what Feature Design is and its role in the documentation ecosystem]
[1 paragraph: what it defines — user-centered design for a single feature]
[1 paragraph: what it does not define — no implementation, architecture, or technology]
[1 sentence: one-to-one relationship with Feature Specification]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> Feature Design translates a single Feature Specification into a user-centered design. It applies the shared principles defined by Design Documentation together with any relevant External Context. Feature Design is **not** reusable design guidance — it is the application of reusable principles to one specific feature.

**Incorrect:**
> Feature Design defines how to implement authentication using OAuth 2.0, including token storage with Redis and session management via JWT middleware.
> *Why wrong: This introduces implementation details (OAuth, Redis, JWT), which belongs in Feature Technical Design or Engineering, not Feature Design.*

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** Define scope boundaries explicitly; State the one-to-one relationship with Feature; Explain what Feature Design is and is not
- **Don't:** Include implementation details or technology references; Leave scope boundaries ambiguous; Conflate with Design or Architecture standards

This document defines the standard for Feature Design Documentation within the engineering documentation ecosystem.

Feature Design translates a single Feature Specification into a complete user-centered design by applying the shared principles defined by the Design Documentation together with any relevant External Context.

Feature Design is **not** reusable design guidance.

It is the application of reusable design principles to one specific feature.

Every Feature Design document has a strict one-to-one relationship with a Feature Specification.

Feature Design explains **how users should experience a feature**.

It does not define implementation, architecture, or engineering decisions.

---

## User Experience

> *Structural rules: `audit/deterministic/section/09-feature-design/01-user_experience.yaml`*

### Template

> **minimum_content:** 2 paragraphs plus subsections
> **length_guidance:** extensive
> **diagram_requirements:** flowchart

```markdown
### User Experience

> **semantic_type:** `user_experience`
> **scope:** ...
> **out_of_scope:** ...
> **contributes:** ...
> **relationships:** ...
> **responsibilities:** ...
> **generation_rules:** ...
> **enhancement_rules:** ...
> **validation_rules:** ...
> **audit_rules:** ...

[Introduction: overall UX intent for the feature, derived from Feature Specification]

### Discovery

[How users first encounter and access the feature]

### Primary Interaction

[Core user flow — what users do to accomplish the feature's purpose]

### Feedback and Response

[How the system communicates results of user actions]

### Error Handling

[What users see and can do when something goes wrong]

### Empty State

[What users see when there is no data or content to display]

### Loading State

[What users see while the system is processing]

### Success State

[What users see when the task completes successfully]

### Accessibility

[How the experience accommodates assistive technologies]

### Localization

[How the experience adapts for different languages and regions]
```

**Required subsections:** Discovery, Primary Interaction, Feedback and Response, Error Handling, Empty State, Loading State, Success State
**Optional subsections:** Accessibility, Localization
**Required diagrams:** flowchart (primary user interaction flow)
**Required cross-references:** Feature Specification, Design Documentation UX Principles

### Examples

**Correct:**
> **Discovery:** Users encounter the feature via a dedicated entry point in the main navigation. The entry point uses a consistent label and icon matching the design system. First-time users see a brief onboarding tooltip.
>
> **Error Handling:** When the feature cannot complete the primary action, users see a clear inline message explaining what went wrong and a specific suggestion for resolution. A retry button is available. No technical error codes are shown to the user.

**Incorrect:**
> The `DataFetchError` component renders when the API call returns a 500 status. It calls `retryRequest()` with exponential backoff (initial delay 1000ms, max 5 retries). The error boundary catches exceptions from the `FeatureController` class.
> *Why wrong: This describes implementation internals (API status codes, retry logic, class names) rather than the user-facing experience. Feature Design should describe what the user sees and can do, not how the system is coded.*

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Describe every interaction from the user's perspective; Cover all states including error, empty, loading, and success; Reference Design Principles that govern the UX
- **Don't:** Reference APIs, frameworks, or component names; Describe internal system behavior or processing logic; Skip error, empty, or loading states

*(To be written by the domain expert. This section defines the complete user experience for the feature.)*

---

## Workflow

> *Structural rules: `audit/deterministic/section/09-feature-design/02-workflow.yaml`*

### Template

> **minimum_content:** 1 workflow with at least 3 steps
> **length_guidance:** moderate
> **diagram_requirements:** flowchart

```markdown
### Workflow

> **semantic_type:** `workflow`
> **scope:** ...
> **out_of_scope:** ...
> **contributes:** ...
> **relationships:** ...
> **responsibilities:** ...
> **generation_rules:** ...
> **enhancement_rules:** ...
> **validation_rules:** ...
> **audit_rules:** ...

### Primary Workflow

[Step-by-step sequence of user actions and system responses]

1. User does X → System responds with Y
2. User does A → System responds with B
3. ...

### Alternative Workflows

[Branching paths for different user choices or conditions]

### Error Recovery

[What happens and what users can do when a step fails]
```

**Required subsections:** Primary Workflow, Error Recovery
**Optional subsections:** Alternative Workflows
**Required diagrams:** flowchart (primary workflow)
**Required cross-references:** Feature Specification, User Experience

### Examples

**Correct:**
> **Primary Workflow**
>
> 1. User selects the item to modify → System displays the edit form with current values pre-filled
> 2. User updates one or more fields → System validates each field inline as the user types
> 3. User submits the form → System processes the update and displays a confirmation message with the saved values
>
> **Error Recovery**
>
> If submission fails due to a validation error, the system highlights the invalid fields, displays a message describing the issue, and keeps the user's entered values so they can correct the problem without re-entering data.

**Incorrect:**
> 1. User clicks submit → `handleSubmit()` dispatches an action to the Redux store
> 2. The middleware calls `POST /api/items/:id` with the form payload
> 3. On success, the router navigates to `/items/:id`
> *Why wrong: This describes implementation mechanics (Redux, API routes, router navigation) instead of user actions and observable system responses. The workflow must be technology-independent.*

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Write each step as user action → observable system response; Include error recovery paths for every failure point; Ensure every functional requirement maps to at least one workflow step
- **Don't:** Describe implementation mechanics or API calls; Skip error recovery or branching paths; Use function names, class names, or route paths

*(To be written by the domain expert. This section defines the step-by-step user workflow for the feature.)*

---

## States

> *Structural rules: `audit/deterministic/section/09-feature-design/03-states.yaml`*

### Template

> **minimum_content:** state table plus transition descriptions
> **length_guidance:** moderate
> **diagram_requirements:** state

```markdown
### States

> **semantic_type:** `states`
> **scope:** ...
> **out_of_scope:** ...
> **contributes:** ...
> **relationships:** ...
> **responsibilities:** ...
> **generation_rules:** ...
> **enhancement_rules:** ...
> **validation_rules:** ...
> **audit_rules:** ...

### State Definitions

| State | Description | What User Sees |
|-------|-------------|----------------|
| Initial | ... | ... |
| Active | ... | ... |
| Empty | ... | ... |
| Error | ... | ... |
| Success | ... | ... |

### State Transitions

| From | To | Trigger | User Action |
|------|----|---------|-------------|
| Initial | Active | ... | ... |
| Active | Success | ... | ... |
| Active | Error | ... | ... |
| ... | ... | ... | ... |
```

**Required subsections:** State Definitions, State Transitions
**Optional subsections:** none
**Required diagrams:** state (state transition diagram)
**Required cross-references:** User Experience, Workflow

### Examples

**Correct:**
> **State Definitions**
>
> | State | Description | What User Sees |
> |-------|-------------|----------------|
> | Initial | Feature has not been activated | Entry point with a prompt to begin |
> | Active | Feature is in use | Interactive form with current data |
> | Processing | System is handling user input | Inline spinner with status message |
> | Empty | No data exists to display | Friendly message explaining why and suggesting next steps |
> | Error | Processing failed | Error message with retry option |
> | Success | Task completed | Confirmation message with saved result |

**Incorrect:**
> | State | Description | What User Sees |
> |-------|-------------|----------------|
> | IDLE | Store state is `idle` | Component renders null |
> | FETCHING | Axios request in flight | `<Loader />` component mounted |
> | CACHED | Data in localStorage | Data hydrated into store |
> *Why wrong: This describes internal state management (Redux store states, Axios, localStorage, component rendering) rather than observable user-facing states. States must be described from the user's perspective.*

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Enumerate every observable UI state including empty and error states; Document all valid transitions with explicit triggers; Describe what the user sees in each state, not what the system does internally
- **Don't:** Describe internal state management or component lifecycle; Omit transition triggers or leave them implicit; Reference framework-specific state concepts (Redux, stores, context)

*(To be written by the domain expert. This section defines the observable states and state transitions for the feature.)*

---

## Constraints

> *Structural rules: `audit/deterministic/section/09-feature-design/06-constraints.yaml`*

### Template

> **minimum_content:** constraint list with sources
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
### Constraints

> **semantic_type:** `constraints`
> **scope:** ...
> **out_of_scope:** ...
> **contributes:** ...
> **relationships:** ...
> **responsibilities:** ...
> **generation_rules:** ...
> **enhancement_rules:** ...
> **validation_rules:** ...
> **audit_rules:** ...

| Constraint | Type | Source | Impact on Design |
|-----------|------|--------|-----------------|
| [description] | Hard/Advisory | [External Context source] | [what it prevents or requires] |
| ... | ... | ... | ... |
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** External Context, Platform requirements

### Examples

**Correct:**
> | Constraint | Type | Source | Impact on Design |
> |-----------|------|--------|-----------------|
> | Maximum password length is 128 characters | Hard | Platform Security Policy | Input field must accept and display up to 128 characters without truncation |
> | Feature must support right-to-left text | Hard | Localization Requirements | Layout must mirror for RTL locales; labels and icons must flip alignment |
> | Dark mode support is preferred but not mandatory | Advisory | Design System Guidelines | Color choices should work in both themes if feasible |

**Incorrect:**
> | Constraint | Type | Source | Impact on Design |
> |-----------|------|--------|-----------------|
> | Use `maxlength="128"` on the input element | Hard | HTML spec | Input validation in the DOM layer |
> | Must use CSS `direction: rtl` for Arabic | Hard | W3C CSS spec | Stylesheet must set text direction |
> *Why wrong: These describe implementation techniques (HTML attributes, CSS properties) rather than user-facing design constraints. Constraints should state what the design must accommodate, not how to code it.*

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables
- **Audience:** architect
- **Do:** Cite the source of every constraint; Distinguish hard constraints from advisory preferences; State the concrete impact on design decisions
- **Don't:** Describe implementation techniques (HTML attributes, CSS properties); Omit source attribution; Conflate constraints with implementation preferences

*(To be written by the domain expert. This section defines user-facing constraints from external systems.)*

---

## Required Sections

Every Feature Design document must contain the following sections.
Sections are identified by heading text; the compiler maps each to a semantic type.

| Section | semantic_type | Required | Aliases | Content Requirements |
|---------|--------------|----------|---------|---------------------|
| User Experience | `user_experience` | ✓ | UX, User Flow | Complete user-facing experience covering discovery, interaction, feedback, errors, empty, loading, and success states |
| Workflow | `workflow` | ✓ | User Workflow, Flow | Ordered sequence of user actions and system responses including branching and error recovery |
| States | `states` | ✓ | UI States, Application States, State Transitions | Every observable UI state and all valid transitions between them |
| Purpose | `purpose` | | Overview, Summary | Definition of Feature Design, scope boundaries, and one-to-one relationship with Feature |
| Non-Goals | `non_goals` | | Non Goals, Out of Scope, Not In Scope | Excluded responsibilities with the owning standard identified for each |
| Constraints | `constraints` | | Limitations, Non-Functional Requirements | External user-facing constraints with source citation and binding vs. advisory distinction |
| Traceability | `traceability` | | Traces To, Derived From | Derivation chain, one-to-one mapping assertion, and downstream consumers |

Section headings are case-insensitive. Sections not listed here are stored as `generic` type — preserved but not queryable by type.

---

## Goals

Feature Design aims to:

* Give every feature a single authoritative user-experience specification.
* Keep UX decisions traceable to shared Design principles rather than invented per feature.
* Bridge functional requirements and architecture without prescribing implementation.

---

## Non-Goals

> *Structural rules: `audit/deterministic/section/09-feature-design/05-non_goals.yaml`*

### Template

> **minimum_content:** bulleted list with owning standards
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
### Non-Goals

> **semantic_type:** `non_goals`
> **scope:** ...
> **out_of_scope:** ...
> **contributes:** ...
> **relationships:** ...
> **responsibilities:** ...
> **generation_rules:** ...
> **enhancement_rules:** ...
> **validation_rules:** ...
> **audit_rules:** ...

Feature Design does not define:

* [Responsibility] — owned by [Standard Name]
* [Responsibility] — owned by [Standard Name]
* ...
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Goals, owning standard for each excluded item

### Examples

**Correct:**
> Feature Design does not define:
>
> * Product Vision — owned by Vision(01)
> * Feature Requirements — owned by Feature Specification(04)
> * Database schema for storing user preferences — owned by Architecture(05)
> * API endpoint design — owned by Feature Technical Design(10)

**Incorrect:**
> Feature Design does not define:
>
> * The look and feel of the feature
> * How users navigate the feature
> * What the feature does for users
> * Whether the feature is accessible
> *Why wrong: Every item listed here actually belongs within Feature Design scope (look and feel, navigation, user purpose, accessibility). Non-Goals must only list responsibilities that belong to other standards, not the feature's own design concerns.*

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Name the owning standard for each excluded responsibility; List only responsibilities that genuinely belong to other standards; Keep the list current as the ecosystem evolves
- **Don't:** Include items that belong in Feature Design scope; List goals or positive scope statements; Leave ownership of excluded items ambiguous

Feature Design does not define:

* Product Vision
* Shared Design Principles
* Feature Requirements
* Architecture
* Technical Design
* Engineering Decisions
* Technology Selection
* Source Code

These responsibilities belong to other documentation standards.

---

## Success Criteria

Feature Design is successful when:

* Every Feature has one corresponding Feature Design.
* Shared Design principles are consistently applied.
* Relevant External Context has been incorporated where necessary.
* Users experience consistent interactions across the product.
* Engineers understand how the feature should behave.
* Architecture can realize the design without redefining user behavior.
* AI systems can implement user experience consistently without inventing workflows or violating external platform conventions.

---

## Responsibilities

Feature Design is responsible for defining:

* User experience
* User workflow
* User journey
* Interaction model
* Navigation within the feature
* Information presentation
* User feedback
* Validation behavior
* Empty states
* Loading states
* Success states
* Error experience
* Accessibility application
* Localization considerations
* Responsive behavior
* User-facing constraints introduced by external systems

Feature Design transforms functional requirements into a complete user experience.

---

## Scope

Feature Design may describe:

* User interactions
* User workflows
* Navigation
* Screen relationships
* Interaction states
* Validation behavior
* Error behavior
* Empty states
* Loading states
* Responsive behavior
* Accessibility behavior
* Localization behavior
* User guidance
* User feedback

Every Feature Design document should remain focused on one feature.

---

## Out of Scope

Feature Design must not describe:

* Product Vision
* Design Philosophy
* Design Principles
* Architecture
* Component responsibilities
* Runtime behavior
* Programming languages
* Frameworks
* APIs
* Databases
* Algorithms
* Source code
* Engineering decisions

Shared Design belongs to Design Documentation.

Implementation belongs to downstream documentation.

---

## Inputs

Feature Design derives from:

* Feature Specification
* Design Documentation
* Relevant External Context
* Product Constraints

Feature Design should not derive from implementation.

---

## Outputs

Feature Design provides direction for:

* Architecture
* Feature Technical Design
* UI Prototypes
* Mockups
* User Acceptance Testing
* Engineering

Implementation should realize the documented feature design.

---

## Traceability

> *Structural rules: `audit/deterministic/section/09-feature-design/07-traceability.yaml`*

### Template

> **minimum_content:** derivation diagram plus relationship list
> **length_guidance:** concise
> **diagram_requirements:** custom

```markdown
### Traceability

> **semantic_type:** `traceability`
> **scope:** ...
> **out_of_scope:** ...
> **contributes:** ...
> **relationships:** ...
> **responsibilities:** ...
> **generation_rules:** ...
> **enhancement_rules:** ...
> **validation_rules:** ...
> **audit_rules:** ...

[Derivation chain diagram from Vision through Feature and Design to Feature Design]

[One-to-one mapping assertion with Feature Specification]

[Table of downstream consumers]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** custom (derivation chain diagram)
**Required cross-references:** Feature(04), Design(06), Feature Technical Design(10), Engineering(07)

### Examples

**Correct:**
> This Feature Design derives from Feature Specification "Report Export" and applies Design Documentation's Interaction Principles and Accessibility Principles. It has a strict one-to-one relationship with the "Report Export" Feature Specification.
>
> | Consumer | Relationship |
> |----------|-------------|
> | Feature Technical Design | Technical realization of this design |
> | Engineering | Implementation of the designed UX |
> | User Acceptance Testing | Validation of designed behavior |

**Incorrect:**
> This Feature Design derives from the Authentication module's architecture document and the REST API specification. It covers Export, Import, and Archive features as a unified workflow.
> *Why wrong: (1) Derivation should trace to Feature Specification and Design Documentation, not architecture or API specs. (2) Multiple features are combined, violating the one-to-one relationship constraint.*

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** diagrams
- **Audience:** architect
- **Do:** Show the complete derivation chain from Vision through Feature and Design; State the one-to-one mapping constraint with Feature Specification explicitly; List all downstream consumers and their relationship
- **Don't:** Include implementation-level traceability (code, tests, bugs); Omit the one-to-one mapping assertion; Reference unrelated standards or documents

Feature Design remains traceable.

```text
Vision
    │
    ├──────────────────────┐
    ↓                      ↓
Feature                  Design
    │                      │
    │              External Context (optional)
    │                      │
    └──────────────────────┘
               ↓
          Feature Design
               ↓
      Feature Technical Design
      (converges with Architecture)
               ↓
           Engineering
               ↓
         Implementation
```

Every Feature Design should trace directly to exactly one Feature Specification.

---

## Relationships

| Document                 | Relationship                             |
| ------------------------ | ---------------------------------------- |
| Feature                  | One-to-one mapping                       |
| Design                   | Applies shared design principles         |
| External Context         | Applies user-facing external constraints |
| Architecture             | Provides structural realization          |
| Feature Technical Design | Provides technical realization           |
| Engineering              | Explains implementation decisions        |

---

## Required Characteristics

Feature Design should be:

* User-centered
* Feature-specific
* Cohesive
* Traceable to exactly one Feature
* Technology-independent
* Accessible and localizable by default

---

## Audit Rules

An audit should verify:

* A one-to-one mapping exists between Feature and Feature Design.
* Shared Design Documentation has been applied.
* Relevant External Context has been identified.
* User workflows are complete.
* Accessibility has been considered.
* Localization has been considered where applicable.
* User-facing external constraints are reflected.
* Design remains technology independent.
* No implementation details appear.
* No architectural decisions appear.
* Design Documentation and External Context are referenced instead of duplicated.

Feature Design quality is evaluated individually and across the feature collection.

---

## Validation Rules

Feature Design is considered valid when:

* One document corresponds to one Feature.
* User workflows are complete.
* Shared Design Documentation has been applied.
* Relevant External Context has been identified.
* Accessibility considerations exist where applicable.
* Localization considerations exist where applicable.
* User-facing external constraints are documented.
* No implementation details appear.
* Feature Design remains traceable to the Feature Specification.
* Shared Design and External Context are referenced rather than duplicated.

---

## Generation Rules

When generating Feature Design:

* Start from the Feature Specification.
* Apply Design Documentation.
* Apply relevant External Context.
* Focus on user experience.
* Keep one document per feature.
* Maintain technology independence.
* Reference shared Design Documentation.
* Reference External Context rather than duplicating it.
* Do not redefine reusable design guidance.

---

## Enhancement Rules

When enhancing Feature Design:

* Improve workflow clarity.
* Improve user experience.
* Strengthen consistency with Design Documentation.
* Strengthen consistency with External Context.
* Remove duplicated design principles.
* Remove duplicated external documentation.
* Remove implementation leakage.
* Improve traceability.
* Preserve feature intent.

Feature Design should become clearer without changing feature requirements.

---

## Summary

Feature Design Documentation is the design realization of a single Feature Specification.

Each document maintains a strict one-to-one relationship with its corresponding Feature, applying the shared principles defined by the Design Documentation together with any relevant External Context to describe how users should experience that feature.

Its purpose is to bridge functional requirements and system architecture while preserving consistency, usability, accessibility, localization, platform conventions, and technology independence across the product ecosystem.

---

## Common Mistakes

Examples include:

* Combining multiple features.
* Rewriting Design Documentation.
* Rewriting External Context.
* Introducing architecture.
* Discussing implementation.
* Defining frameworks.
* Embedding source code.
* Ignoring shared design principles.
* Ignoring external UX constraints.

These should be reported during audits.

---

## Documentation Folder

Feature Design documents live under:

```text
docs/raw/feature-design/
```

---

## Usage

Written one-to-one with a Feature, by whoever owns UX for that feature, after the Feature spec exists and before Feature Technical Design starts. Use `samgraha audit --domain feature-design` to confirm every Feature has a matching Feature Design and that shared Design principles were applied rather than redefined.

## Related

- [Feature Standard](04-feature-standards.md) — one-to-one mapping
- [Design Standard](06-design-standards.md) — shared principles this standard applies
- [Feature Technical Standard](10-feature-technical-standards.md) — technical realization of this design
- [Standards Reference Standard](standards.md) — how this standard itself is documented

## One-to-One Mapping

Every Feature Specification should have exactly one corresponding Feature Design document.

Example:

```text
features/

    authentication.md

feature-design/

    authentication.md
```

Both documents describe the same feature from different perspectives.

No Feature Design should describe multiple unrelated features.

---

## Design Principle Application

Feature Design applies the reusable principles defined by Design Documentation.

Examples include:

* Design Philosophy
* Interaction Principles
* Navigation Principles
* Accessibility Principles
* Localization Principles
* Visual Language
* Content Guidelines
* Responsive Design Principles

Feature Design should reference these principles rather than redefining them.

---

## External Context Application

Feature Design should identify any External Context that influences the user experience of the feature.

Examples include:

* Native operating system interaction patterns
* Authentication provider user flows
* Platform UX guidelines
* Accessibility standards
* Localization requirements
* Regulatory user-facing requirements
* Third-party interaction constraints

External Context should be referenced rather than duplicated.

Only context relevant to the feature should be included.

---

## Feature Design Principles

Every Feature Design should be:

* User-centered
* Feature-specific
* Cohesive
* Traceable
* Technology independent
* Consistent with Design Documentation
* Consistent with External Context
* Independently reviewable
* Independently implementable

---

## Technology Independence

Feature Design should remain implementation independent.

Feature Design should describe:

* user interaction
* user workflow
* expected behavior
* information presentation
* accessibility behavior
* localization behavior

rather than:

* frontend frameworks
* component libraries
* APIs
* source code
* implementation patterns

Technology belongs in Engineering Documentation.

---

## Quality Requirements

Feature Design should be:

* Complete
* User-centered
* Consistent
* Accessible
* Localizable
* Technology independent
* Traceable
* Atomic

Each document should remain focused on one feature.

---
