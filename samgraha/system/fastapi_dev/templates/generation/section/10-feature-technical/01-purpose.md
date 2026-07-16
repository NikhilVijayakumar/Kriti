# Purpose — Generation Template

> **Domain:** feature-technical
> **Section:** purpose
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Purpose section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | Purpose must align with and derive from the Feature Specification's Purpose |
| `derives_from` | engineering / purpose | Purpose must be consistent with the Engineering documentation's scope |
| `derives_from` | architecture / purpose | Purpose must derive from the Architecture Documentation's purpose and scope |

## Template

```markdown
## Purpose

> **Feature Technical Design purpose:** [1-2 sentences: what this Feature Technical Design defines — how the system architecture realizes this specific feature]

> **Scope boundaries:**
> - **In scope:** [architectural concerns this document covers for this feature]
> - **Out of scope:** [concerns explicitly excluded, with the owning standard identified]

> **One-to-one relationship:** This Feature Technical Design corresponds to exactly one Feature Specification: [Feature name].
```

> **Generation note:** The standard's Purpose section defines Feature Technical Design as a concept (meta-level) AND serves as the template for system-specific documents. When generating for a specific system, fill this template with *that feature's* technical design purpose. The meta-level language belongs in the standard itself, not in a generated document.

## Examples

**Correct (system-specific):**
> **Feature Technical Design purpose:** This Feature Technical Design defines how the Authentication Feature is realized architecturally — credential validation, session management, and security boundary enforcement across the Identity, Session, and API Gateway components.
>
> **Scope boundaries:**
> - **In scope:** Component responsibilities, interaction patterns, data ownership, security boundaries for authentication
> - **Out of scope:** User login UX (Feature Design), password storage algorithms (Engineering), OAuth provider selection (Architecture)
>
> **One-to-one relationship:** This Feature Technical Design corresponds to exactly one Feature Specification: User Authentication.

**Incorrect:**
> Feature Technical Design covers all features in the system, including User Authentication, Order Processing, Payment Handling, and Notification Delivery.
> *Why wrong: violates the one-to-one relationship principle.*

## Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** Define Feature Technical Design in relation to the documentation ecosystem; explicitly state what it is not; maintain the one-to-one mapping constraint
- **Don't:** Drift into implementation specifics; conflate with Architecture or Feature Design; list features or technologies

**Minimum content:** 2 paragraphs
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Feature(04), Architecture(05)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
