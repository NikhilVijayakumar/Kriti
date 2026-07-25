# Purpose — Generation Template

> **Domain:** product-guide
> **Section:** purpose
> **Source:** `documentation-standards/16-product-guide-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/16-product-guide-relationships.yaml`

Generate the Purpose section for a Product Guide document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / purpose | Product Context must align with Vision(01) product purpose |

## Template

```markdown
## Purpose

[One sentence or short paragraph describing the user-facing problem this topic solves.]
```

> **Generation note:** When generating for a specific system, fill this template with *that system's* user-facing problem: what the reader wants to accomplish and why this topic helps. The meta-level "This document defines the standard for Product Guide..." language belongs in the standard itself, not in a generated document.

## Examples

**Correct:**
> This topic explains how to configure automatic backups so your data is never lost.

**Incorrect:**
> This topic covers the backup feature.
> *Why wrong: Vague and passive — describes what the topic "covers" rather than the user-facing problem it solves.*

## Writing Guidance

- **Tone:** conversational
- **Voice:** second person
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** Write from the reader's perspective — "you" language; lead with the benefit or outcome the user gets; keep to one sentence or a short paragraph
- **Don't:** Use passive voice or vague phrasing like "this topic covers…"; describe internal implementation details or engineering rationale; exceed two sentences

**Minimum content:** 1 paragraph
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** none

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
