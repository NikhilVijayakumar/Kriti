# Purpose — Generation Template

> **Domain:** feature-design
> **Section:** purpose
> **Source:** `documentation-standards/09-feature-design-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/09-feature-design-relationships.yaml`

Generate the Purpose section for a Feature Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | Feature Design Purpose must align with and derive from the Feature Specification's Purpose |
| `derives_from` | design / purpose | Feature Design Purpose must apply the shared Design Documentation principles |

## Template

```markdown
## Purpose

> **Feature Design purpose:** [1-2 sentences: what this Feature Design defines for this specific feature — how users should experience it]

> **Scope boundaries:**
> - **In scope:** [user experience concerns this document covers for this feature]
> - **Out of scope:** [concerns explicitly excluded, with the owning standard identified]

> **One-to-one relationship:** This Feature Design corresponds to exactly one Feature Specification: [Feature name].
```

> **Generation note:** The standard's Purpose section defines Feature Design as a concept (meta-level) AND serves as the template for system-specific feature design documents. When generating for a specific system, fill this template with *that feature's* design purpose: what user experience this document defines and what it intentionally excludes. The meta-level "This document defines the standard for Feature Design Documentation..." language belongs in the standard itself, not in a generated document.

## Examples

**Correct (system-specific):**
> **Feature Design purpose:** This Feature Design defines how users discover, configure, and run data export reports — including scheduling, format selection, and delivery notification.
>
> **Scope boundaries:**
> - **In scope:** Report configuration UX, export workflow, delivery notification experience
> - **Out of scope:** Data pipeline architecture (Feature Technical Design), report data schema (Architecture)
>
> **One-to-one relationship:** This Feature Design corresponds to exactly one Feature Specification: Report Export.

**Correct (meta-level — only when generating the standard itself, not a system document):**
> Feature Design translates a single Feature Specification into a user-centered design. It applies the shared principles defined by Design Documentation together with any relevant External Context. Feature Design is **not** reusable design guidance — it is the application of reusable principles to one specific feature.

**Incorrect:**
> Feature Design defines how to implement authentication using OAuth 2.0, including token storage with Redis and session management via JWT middleware.
> *Why wrong: introduces implementation details (OAuth, Redis, JWT) which belongs in Feature Technical Design or Engineering, not Feature Design.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** Define scope boundaries explicitly; state the one-to-one relationship with Feature; explain what this Feature Design is and is not
- **Don't:** Include implementation details or technology references; leave scope boundaries ambiguous; conflate with Design or Architecture standards

**Minimum content:** 1 paragraph
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** none

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
