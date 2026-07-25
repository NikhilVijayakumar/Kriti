# Design Standard

> *Deterministic rules for this domain: `audit/deterministic/document/06-design.yaml`*

## Table of Contents
- [Purpose](#purpose)
- [UX Principles](#ux-principles)
- [Accessibility](#accessibility)
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
- [Design as a Documentation Collection](#design-as-a-documentation-collection)
- [Single Responsibility](#single-responsibility)
- [Design Principles](#design-principles)
- [Technology Independence](#technology-independence)
- [Cross-Repository Design](#cross-repository-design)
- [Quality Requirements](#quality-requirements)

---


## Purpose

> *Structural rules: `audit/deterministic/section/06-design/04-purpose.yaml`*

### Template

> **minimum_content:** 2 paragraphs
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
## Purpose

[1 paragraph: problem statement — what Design Documentation solves and why it exists]

[1 paragraph: scope — what it defines and what it does not; distinction from Feature Design]
```

### Examples

**Correct:**
> Design Documentation solves the problem of inconsistent design across features by establishing reusable design principles, interaction philosophy, and UX standards that govern an entire product ecosystem. It defines how products should be designed at the product level — not how individual features behave.

**Incorrect:**
> Design Documentation defines the checkout flow for the payment module, including screen layouts and button placement for the order form.
> *Why wrong: This describes a feature-specific workflow, not a product-level design standard. Design Documentation must not contain feature-specific content.*

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision, Feature Design Standard

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State the problem Design Documentation solves before describing what it defines. Distinguish Design Documentation from Feature Design explicitly. Keep scope boundaries firm and technology-free.
- **Don't:** List specific features or products. Reference implementation technologies or frameworks. Describe how individual features behave.

This document defines the standard for Design Documentation within the engineering documentation ecosystem.

Design Documentation establishes the shared design language, design principles, interaction philosophy, and user experience standards that govern an entire product or product ecosystem.

Unlike Feature Design, Design Documentation is **not feature specific**.

Instead, it provides reusable guidance that ensures every feature delivers a consistent and predictable user experience.

Design Documentation defines **how products should be designed**.

It does not describe how individual features behave.

---

## UX Principles

> *Structural rules: `audit/deterministic/section/06-design/02-ux_principles.yaml`*

### Template

> **minimum_content:** 3 principles with rationale
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
## UX Principles

[1 paragraph: how UX principles relate to design philosophy and product experience]

### [Principle Name]

[1 paragraph: what this principle means at the product level]

[1 example: how this principle applies across features]

---

[Repeat for each principle — minimum 3]
```

### Examples

**Correct:**
> ### Feedback Visibility
> Users should always receive immediate, clear feedback when they perform an action. Whether submitting a form, navigating to a new view, or encountering an error, the system confirms the action occurred and indicates the result. This applies across all features — a user submitting feedback gets the same feedback pattern as a user updating settings.

**Incorrect:**
> When the user clicks the "Submit" button in React, the onClick handler should call the API endpoint and display a Material UI Snackbar component with the success message.
> *Why wrong: This is technology-specific implementation guidance (React, Material UI, Snackbar) rather than a product-level UX principle. UX principles must describe interaction philosophy, not component choices.*

**Required subsections:** one per principle (minimum 3)
**Optional subsections:** Interaction Patterns, Navigation Philosophy, Feedback Mechanisms
**Required diagrams:** none
**Required cross-references:** Design Principles, Accessibility

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** mixed
- **Audience:** product owner
- **Do:** Frame each principle as a product-level interaction philosophy applicable across all features. Provide at least one cross-feature example per principle. Ground each principle in user outcomes, not UI mechanics.
- **Don't:** Reference specific UI frameworks, libraries, or component names. Describe feature-specific interaction workflows. Conflate UX principles with visual design specifications.

*(To be written by the domain expert. This section defines user experience principles governing interaction, navigation, feedback, and discoverability.)*

---

## Accessibility

> *Structural rules: `audit/deterministic/section/06-design/03-accessibility.yaml`*

### Template

> **minimum_content:** 1 compliance target + 3 inclusive design principles
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
## Accessibility

[1 paragraph: accessibility philosophy and why it matters for this product]

### Compliance Targets

[1 paragraph: applicable standard (e.g. WCAG 2.1 AA), enforcement scope]

### Inclusive Design Principles

[1 principle per subsection — minimum 3, each with rationale and product-level guidance]

### Assistive Technology Support

[1 paragraph: screen readers, keyboard navigation, voice control — product-level guidance]
```

### Examples

**Correct:**
> ### Compliance Targets
> The product targets WCAG 2.1 Level AA conformance across all user-facing interfaces. This applies to every feature with a user interface, including web, mobile, and desktop applications. Exceptions are documented per feature and must receive explicit approval.

**Incorrect:**
> All buttons must include `aria-label="Submit"` and use the `role="button"` attribute to comply with WCAG 2.1 Level AA.
> *Why wrong: This contains component-level ARIA patterns, which belong to Engineering, not Design. Accessibility at the design level should define compliance targets and inclusive design principles, not HTML attribute requirements.*

**Required subsections:** Compliance Targets, Inclusive Design Principles
**Optional subsections:** Assistive Technology Support, Testing Strategy
**Required diagrams:** none
**Required cross-references:** UX Principles, Feature Design Standard, Engineering Standard

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Reference specific compliance standards (e.g. WCAG level) with enforcement scope. Define inclusive design principles at the product level before any technical requirements. State which interfaces the compliance targets apply to.
- **Don't:** Specify component-level ARIA attributes or HTML patterns. Write testing scripts or code snippets. Confuse design-level accessibility with engineering-level implementation details.

*(To be written by the domain expert. This section defines accessibility standards and inclusive design principles for the product.)*

---

## Constraints

> *Structural rules: `audit/deterministic/section/06-design/05-constraints.yaml`*

### Template

> **minimum_content:** 1 constraint category with source and enforcement scope
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
## Constraints

[1 paragraph: how constraints relate to design decisions and what makes them binding]

### [Constraint Category] (e.g. Regulatory, Platform, Organizational)

> **source:** [regulatory body, platform requirement, organizational mandate]
> **enforcement:** [binding / advisory]
> **scope:** [which features or capabilities this applies to]

[1 paragraph: what this constraint requires and why it is binding]

[Repeat for each constraint category — minimum 1]
```

### Examples

**Correct:**
> ### Regulatory
> > **source:** Federal accessibility regulation
> > **enforcement:** binding
> > **scope:** All user-facing interfaces
>
> The product must comply with federal accessibility requirements. All features must be usable by individuals with disabilities. This constraint is non-negotiable and applies regardless of timeline or budget.

**Incorrect:**
> We prefer using a specific CSS framework because the team knows it well and it speeds up development.
> *Why wrong: This is a team preference, not a binding constraint. Constraints must come from regulatory, platform, or organizational mandates and state their binding nature explicitly.*

**Required subsections:** one per constraint category (minimum 1)
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision, Feature Design Standard, Architecture Standard

### Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** State each constraint with its source, enforcement level, and scope. Clearly distinguish binding constraints from advisory guidance. Explain why each constraint is non-negotiable.
- **Don't:** List team preferences as constraints. Omit the source or enforcement level. Conflate platform requirements with organizational preferences.

*(To be written by the domain expert. This section defines design-level constraints, non-functional requirements, and regulatory or organizational mandates.)*

---

## Required Sections

Every Design document must contain the following sections.
Sections are identified by heading text; the compiler maps each to a semantic type.

| Section | semantic_type | Required | Aliases | Content Requirements |
|---------|--------------|----------|---------|---------------------|
| Design Principles | `design_principles` | ✓ | Principles, Core Design | 3+ named principles with rationale and product-level examples |
| UX Principles | `ux_principles` | ✓ | User Experience Principles, UX Guidelines | 3+ interaction principles covering navigation, feedback, and discoverability |
| Accessibility | `accessibility` | ✓ | A11y, Accessibility Standards | Compliance target (e.g. WCAG level), inclusive design principles, assistive technology guidance |
| Purpose | `purpose` | | Overview, Summary | Problem statement, scope definition, distinction from Feature Design |
| Constraints | `constraints` | | Limitations, Non-Functional Requirements | Binding constraints with source (regulatory, platform, organizational) and enforcement scope |
| Traceability | `traceability` | | Traces To, Derived From | Tier diagram, upstream derivation paths, downstream consumers, non-contradiction rule |

Section headings are case-insensitive. Sections not listed here are stored as `generic` type — preserved but not queryable by type.

---

## Goals

Design Documentation aims to:

* Give every feature-specific design a shared set of reusable principles instead of reinventing them.
* Keep the product's user experience consistent across features.
* Separate reusable design guidance from any single feature's design.

---

## Non-Goals

Design Documentation does not define:

* Product requirements
* Feature specifications
* Feature workflows
* Screen implementations
* Technical architecture
* Engineering decisions
* Technology selection
* Source code
* Component implementation

These responsibilities belong to other documentation standards.

---

## Success Criteria

Design Documentation is successful when:

* Every feature follows a common design language.
* Multiple applications exhibit consistent user experiences.
* Designers and engineers share a common understanding of design principles.
* Feature Design can be created without redefining design philosophy.
* Architecture complements rather than replaces design.
* AI systems can consistently apply design principles across repositories.

---

## Responsibilities

Design Documentation is responsible for defining:

* Product Design Philosophy
* Design Principles
* User Experience Principles
* Interaction Principles
* Information Design Principles
* Navigation Principles
* Accessibility Principles
* Localization Principles
* Visual Language
* Design System Guidelines
* Cross-Application Consistency
* Content Design Principles

Design Documentation establishes common design rules that every feature should follow.

---

## Scope

Design Documentation may include:

* Design Philosophy
* Product Design Principles
* User Experience Principles
* Interaction Guidelines
* Navigation Standards
* Information Architecture Principles
* Visual Design Language
* Typography Guidelines
* Color Principles
* Spacing Principles
* Iconography Principles
* Accessibility Standards
* Localization Standards
* Content Guidelines
* Error Communication Principles
* Notification Principles
* Responsive Design Principles
* Animation Principles
* Design Tokens
* Component Usage Principles

Projects should document only the design domains relevant to the repository.

Design Documentation is intentionally modular.

---

## Out of Scope

Design Documentation must not describe:

* Product Vision
* Feature Requirements
* Feature Workflows
* Feature Behavior
* Screen Specifications
* User Stories
* Technical Architecture
* Technology Selection
* Frameworks
* Source Code
* APIs
* Algorithms
* Implementation Details

These responsibilities belong to other documentation standards.

---

## Inputs

Design Documentation derives from:

* Vision
* Philosophy (02)
* User Experience Goals
* Product Principles
* Organizational Standards

Design Documentation should not derive from feature implementation.

---

## Outputs

Design Documentation provides guidance for:

* Feature Design
* Architecture
* Engineering Decisions
* Design Systems
* UI Libraries
* Mockups
* Prototypes
* Product Development

Every Feature Design should align with the Design Documentation.

---

## Traceability

> *Structural rules: `audit/deterministic/section/06-design/06-traceability.yaml`*

### Template

> **minimum_content:** 1 tier diagram + 2 derivation paths
> **length_guidance:** concise
> **diagram_requirements:** flowchart

```markdown
## Traceability

### Tier Diagram

[ASCII or Mermaid diagram showing Design Documentation's position in the documentation hierarchy]

### Upstream Derivation

[1 paragraph per upstream source: Vision, Philosophy — how Design derives from them]

### Downstream Consumers

[1 paragraph per downstream: Feature Design, Architecture — how they consume Design]

### Non-Contradiction Rule

[1 paragraph: downstream documents must not contradict design principles]
```

### Examples

**Correct:**
> ### Tier Diagram
> Vision → Design Documentation → Feature Design → Engineering → Implementation
>
> Design Documentation derives its principles from the product Vision and Philosophy. It feeds Feature Design, which applies those principles to specific features. No downstream document may contradict the design principles established here.

**Incorrect:**
> Traceability shows that module A calls module B, which calls module C, through a dependency graph of the codebase.
> *Why wrong: This describes code-level implementation traceability, not documentation hierarchy traceability. Design Traceability must show the derivation chain across documentation standards, not source code dependencies.*

**Required subsections:** Tier Diagram, Upstream Derivation, Downstream Consumers, Non-Contradiction Rule
**Optional subsections:** none
**Required diagrams:** tier/derivation flowchart
**Required cross-references:** Vision, Feature Design, Architecture, Feature Technical Design

### Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** diagrams
- **Audience:** AI agent
- **Do:** Include a visual tier diagram showing the full derivation chain. List every upstream source and downstream consumer explicitly. State the non-contradiction rule as a binding constraint, not a suggestion.
- **Don't:** Describe code-level module dependencies or call graphs. Omit any standard in the derivation chain. Leave the non-contradiction rule implicit or optional.

Design Documentation remains traceable.

```text
Vision
    │
    ├────────────────────────┐
    ↓                        ↓
Feature                Design Documentation
    │                        │
    │                External Context (optional)
    │                        │
    └────────────────────────┘
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

Design principles influence every downstream design decision.

---

## Relationships

| Document       | Relationship                       |
| -------------- | ---------------------------------- |
| Vision         | Design supports the product vision |
| Feature        | Independent                        |
| Feature Design | Derived from Design principles     |
| Architecture   | Complements Design                 |
| Engineering    | Influenced by Design constraints   |
| README         | May reference Design philosophy    |

---

## Required Characteristics

Design Documentation should be:

* Consistent across features
* Reusable rather than feature-specific
* Accessible by default
* Technology-independent
* User-centered
* Stable across releases

---

## Audit Rules

An audit should verify:

* Design principles are reusable.
* Design remains technology independent.
* Feature-specific behavior has not been introduced.
* Design philosophy is clearly defined.
* Accessibility guidance exists where appropriate.
* Localization guidance exists where appropriate.
* Documents remain modular.
* Responsibilities do not overlap.
* Cross-repository reuse is encouraged.

Design quality is evaluated across the complete Design Documentation collection.

---

## Validation Rules

Design Documentation is considered valid when:

* Design philosophy is clearly defined.
* Design principles are documented.
* User experience principles are reusable.
* Accessibility guidance is documented where applicable.
* Localization guidance exists where applicable.
* Design remains implementation independent.
* Design documents remain modular.
* No feature-specific workflows dominate the documentation.

Validation applies to the Design Documentation collection rather than individual files.

---

## Generation Rules

When generating Design Documentation:

* Focus on reusable design principles.
* Describe product-wide guidance.
* Separate principles from feature behavior.
* Keep documents modular.
* Avoid implementation terminology.
* Maintain technology independence.
* Optimize for reuse across multiple features and applications.

---

## Enhancement Rules

When enhancing Design Documentation:

* Improve clarity.
* Strengthen design consistency.
* Remove feature-specific content.
* Remove implementation leakage.
* Improve organization.
* Split oversized documents.
* Preserve design philosophy.
* Strengthen cross-product reuse.

Design should become more reusable through refinement.

---

## Summary

Design Documentation is the reusable design knowledge of the product or product ecosystem.

It is a modular collection of documents that defines design philosophy, interaction principles, accessibility, localization, navigation, visual language, and other shared design standards.

Its purpose is to establish a consistent design language that guides every feature, architecture, and implementation while remaining independent of both feature-specific behavior and implementation technologies.

---

## Common Mistakes

Examples include:

* Describing individual feature workflows.
* Documenting application screens.
* Embedding mockups for specific features.
* Explaining implementation.
* Discussing frontend frameworks.
* Mixing architecture with design.
* Mixing feature behavior with design philosophy.

These should be reported during audits.

---

## Documentation Folder

Design documents live under:

```text
docs/raw/design/
```

---

## Usage

Written once and shared across every feature — designers/UX leads author it, Feature Design authors reference it rather than redefine it. Use `samgraha search --domain design` to pull shared design principles into a Feature Design writing session, and `samgraha audit --domain design` to catch feature-specific content that leaked in.

## Related

- [Feature Design Standard](09-feature-design-standards.md) — applies these principles to one feature
- [Philosophy Standard](02-philosophy-standards.md) — guides Design's principles
- [Standards Reference Standard](standards.md) — how this standard itself is documented

## Design as a Documentation Collection

Design Documentation is a collection of related documents.

Example:

```text
design/

    philosophy/

        design-philosophy.md

        design-principles.md

    interaction/

        interaction-principles.md

        navigation-principles.md

        feedback-principles.md

    accessibility/

        accessibility-principles.md

    localization/

        localization-principles.md

    visual/

        color-principles.md

        typography-principles.md

        spacing-principles.md

        iconography-principles.md

    content/

        writing-guidelines.md

        terminology.md

    responsive/

        responsive-principles.md
```

Each document should describe one design concern.

Responsibilities should not overlap.

---

## Single Responsibility

Every Design document should describe one reusable design concern.

Examples include:

* Navigation Principles
* Accessibility Principles
* Localization Principles
* Visual Language
* Design Philosophy
* Typography
* Content Guidelines
* Interaction Principles

Large documents should be decomposed into smaller focused documents.

---

## Design Principles

> *Structural rules: `audit/deterministic/section/06-design/01-design_principles.yaml`*

### Template

> **minimum_content:** 3 named principles with rationale
> **length_guidance:** extensive
> **diagram_requirements:** none

```markdown
## Design Principles

[1 paragraph: how design principles anchor the design language and guide decisions]

### [Principle Name] (e.g. Consistency)

> **definition:** [one-sentence definition of this principle]
> **scope:** [which design decisions this applies to]

[1 paragraph: why this principle matters — what it prevents and what it enables]

[1–2 examples: how this principle applies across different features or products]

[Contrast: what violating this principle looks like]

---

[Repeat for each principle — minimum 3]

### Principle Prioritization

[1 paragraph: how to resolve conflicts when principles compete]
```

### Examples

**Correct:**
> ### Consistency
> > **definition:** Every feature uses the same interaction patterns, visual language, and terminology for the same type of action.
> > **scope:** Navigation, feedback, input, error handling, and layout across all features.
>
> Consistency ensures users transfer learning between features. When one feature uses a swipe gesture for deletion, every feature should use the same gesture for the same action. This prevents users from relearning interaction patterns per feature.
>
> *Contrast:* If one feature requires a long-press to delete and another requires a swipe, users must relearn the pattern — eroding trust and increasing cognitive load.

**Incorrect:**
> Consistency means all buttons should use the same CSS class (`btn-primary`) and follow the design tokens defined in the component library's theme configuration.
> *Why wrong: This conflates design consistency (a product-level principle about interaction patterns) with CSS implementation details. Design Principles must describe values and behaviors, not technology-specific styling rules.*

**Required subsections:** one per principle (minimum 3), Principle Prioritization
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision, Philosophy, UX Principles, Feature Design Standard

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** mixed
- **Audience:** new contributor
- **Do:** Define each principle with a one-sentence definition and explicit scope. Include at least one cross-feature example and a contrast showing what violates the principle. Add a Principle Prioritization subsection resolving conflicts between competing principles.
- **Don't:** Reference specific CSS classes, frameworks, or design tokens. Describe feature-specific behavior as a principle. Leave principle conflicts unaddressed or implicitly resolved.

Design Documentation should establish reusable principles such as:

* Consistency
* Simplicity
* Predictability
* Accessibility
* Discoverability
* Learnability
* Inclusiveness
* Feedback
* Flexibility
* Progressive Disclosure
* Error Prevention
* User Empowerment

Projects may define additional principles appropriate to their domain.

---

## Technology Independence

Design Documentation should remain implementation independent.

It should describe:

* user experience
* interaction philosophy
* presentation principles
* communication principles

rather than

* UI frameworks
* CSS libraries
* frontend frameworks
* component implementations
* rendering technologies

Technology belongs to Engineering.

---

## Cross-Repository Design

Design Documentation may be shared across multiple repositories.

Examples include:

* Shared Design Language
* Shared Accessibility Standards
* Shared Localization Standards
* Shared Navigation Principles
* Shared Design System Guidelines

Repositories should reference shared Design Documentation rather than duplicating it.

---

## Quality Requirements

Design Documentation should be:

* Reusable
* Modular
* Consistent
* Technology Independent
* Product Focused
* Human Centered
* Maintainable
* Reviewable
* Scalable

Design principles should remain stable over time.

---

## Frontend Engineering Context

This standard applies to frontend engineering with the following focus areas:

### Atomic Design Methodology

Components follow a 4-tier hierarchy: atoms (basic UI elements) → molecules (combinations of atoms) → organisms (complex UI sections) → templates (page layouts). Each tier has specific composition rules and barrel exports.

### Design Token Hierarchy

Tokens flow through three layers: JS constants (colors, spacing, typography) → theme object (MUI createTheme or equivalent) → CSS custom properties. All visual values originate from tokens.

### Theme Sovereignty Invariant

ALL visual styling MUST originate from the theme token system. FORBIDDEN: hardcoded hex/rgb/hsl values, pixel spacing, inline font sizes, raw CSS files, component-local style constants. ALLOWED: theme prop references, token imports, styled-components with theme function.

### Responsive Design

Mobile-first approach with breakpoint system. Breakpoints defined as tokens. Layout uses flexible grids, not fixed widths. Container queries preferred over media queries where supported.

### Accessibility Standards

WCAG 2.1 AA minimum. Semantic HTML required. ARIA roles for dynamic content. Keyboard navigation for all interactive elements. Color contrast ratios enforced via tokens.

### Dark Mode Architecture

Dark mode implemented through token layer switching. Two complete token sets: light and dark. Theme provider handles switching. Components never reference light/dark directly — they reference token names.
