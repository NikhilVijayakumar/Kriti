# Purpose — Generation Template

> **Domain:** readme
> **Section:** purpose
> **Source:** `documentation-standards/15-readme-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the Purpose section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / purpose | README Purpose must align with Vision(01) project purpose |

## Template

```markdown
## Purpose

This README introduces the [Project Name] repository and guides readers toward detailed documentation. It covers [scope], establishes boundaries via [out of scope], and references the broader documentation ecosystem.

> **What this README is:** [high-level summary of README's role]
> **What this README is not:** [what belongs in other documentation]
```

> **Generation note:** When generating for a specific system, fill this template with *that system's* README purpose: what this file introduces, what boundaries apply, and where readers should go for detail. The meta-level "This document defines the standard for README..." language belongs in the standard itself, not in a generated document.

## Examples

**Correct:**
> This README introduces the Acme Platform repository and guides readers toward detailed documentation. It covers project overview, setup, usage, and links to architecture, features, and engineering documentation. It does not contain feature specifications, API documentation, or implementation details.

**Incorrect:**
> This README covers all project documentation including API references, database schemas, and deployment procedures.
> *Why wrong: Purpose section must define README scope and boundaries, not duplicate detailed documentation from other standards.*

## Writing Guidance

- **Tone:** conversational
- **Voice:** first person plural
- **Structure:** paragraphs
- **Audience:** new contributor
- **Do:** State what the README is and what it is not; reference the broader documentation ecosystem
- **Don't:** Include feature lists; duplicate content from other documentation standards; use vague scope language

**Minimum content:** 2 paragraphs
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Vision(01) for deeper context

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
