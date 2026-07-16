# Purpose — Generation Template

> **Domain:** prototype
> **Section:** purpose
> **Source:** `documentation-standards/11-prototype-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/11-prototype-relationships.yaml`

Generate the Purpose section for a Prototype document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / purpose | The falsifiable question must ultimately serve the Vision's goals |

## Template

```markdown
## Purpose

> **Falsifiable question:** [the specific question this prototype answers]

> **Disposable nature:** This is a disposable simulation — not production code. It is evaluated once and discarded or replaced.

> **Upstream validation:** This prototype validates [upstream document 1] and [upstream document 2].
```

> **Generation note:** The standard's Purpose section defines Prototype as a concept (meta-level) AND serves as the template for system-specific documents. When generating for a specific system, fill this template with *that prototype's* purpose: the falsifiable question it answers and which upstream documents it validates. The meta-level language belongs in the standard itself, not in a generated document.

## Examples

**Correct (system-specific):**
> **Falsifiable question:** Can a real-time search interface return results within 200ms on a 3G connection?
>
> **Disposable nature:** This is a disposable simulation — not production code. It is evaluated once and discarded or replaced.
>
> **Upstream validation:** This prototype validates Feature Design(09) §Search UX and Feature Technical Design(10) §Search Component Interactions.

**Correct (meta-level — only when generating the standard itself):**
> A Prototype is an executable simulation built to answer a specific falsifiable question or de-risk a specific unknown before production engineering commits to an approach. A Prototype is **not** production implementation.

**Incorrect:**
> This document covers the Order Tracking feature and describes the system architecture.
> *Why wrong: no falsifiable question is stated, the prototype is not identified as disposable, and no upstream documents are referenced.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Lead with the falsifiable question in one sentence; state explicitly that the prototype is disposable; name the upstream documents by title and number
- **Don't:** Describe production architecture or implementation details; omit the falsifiable question; present the prototype as permanent

**Minimum content:** 2 paragraphs
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Feature Design(09), Feature Technical Design(10)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
