# Purpose — Generation Template

> **Domain:** engineering
> **Section:** purpose
> **Source:** `documentation-standards/07-engineering-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate the Purpose section for an Engineering document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | philosophy / purpose | Engineering Purpose must derive from the product's purpose |
| `guided_by` | philosophy / guiding_principles | Engineering Purpose must align with the product's guiding philosophy |

## Template

```markdown
## Purpose

[1–2 paragraphs explaining this document's role in the documentation ecosystem, its scope boundaries, and how it differs from adjacent standards]
```

## Examples

**Correct:**
> This document defines Engineering Documentation's role in the documentation ecosystem. It establishes repository-wide engineering decisions, implementation standards, technology selection rationale, and development conventions. Unlike Feature Technical Design, Engineering Documentation is not feature-specific — it provides reusable knowledge that governs the entire repository.

**Incorrect:**
> This document describes the login page implementation, including the OAuth2 flow, JWT token storage, and session management using Redis.
> *Why wrong: This is feature-specific and describes implementation details, not the repository-wide role of Engineering Documentation in the ecosystem.*

## Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** Define the document's role in the documentation ecosystem explicitly; distinguish Engineering Documentation from adjacent standards (Architecture, Feature Technical Design); set clear scope boundaries with what is included and excluded.
- **Don't:** Include implementation details or feature-specific content; blur boundaries with adjacent documentation standards; describe what the document contains rather than why it exists.

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Architecture(05), adjacent documentation standards

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
