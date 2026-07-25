# Purpose — Generation Template

> **Domain:** philosophy
> **Section:** purpose
> **Source:** `documentation-standards/02-philosophy-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/02-philosophy-relationships.yaml`

Generate the Purpose section for a Philosophy document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / purpose | Purpose must trace to Vision's purpose — Philosophy explains *how* the team decides, given *why* the product exists |
| `guided_by` | philosophy / guiding_principles (self) | Purpose must be consistent with the guiding principles it introduces |

## Template

```markdown
## Purpose

> **Philosophical purpose:** [1-2 sentences: what decision-making philosophy guides this team, what values it establishes]

> **Distinction from Vision:**
> - **Vision says:** [why the product exists — one sentence]
> - **Philosophy says:** [how the team chooses to think and decide — one sentence]

> **Scope boundaries:**
> - **In scope:** [principles, values, trade-offs this document defines]
> - **Out of scope:** [what this document does not define — features, architecture, engineering decisions]
```

> **Generation note:** The standard's Purpose section serves double duty — it defines Philosophy Documentation as a concept (meta-level) AND is used as the template for system-specific documents. When generating for a specific system, fill this template with *that system's* philosophical purpose: what Philosophy establishes and how it differs from Vision. The meta-level "This document defines the standard for Philosophy Documentation..." language belongs in the standard itself, not in a generated document.

## Examples

**Correct (system-specific):**
> **Philosophical purpose:** This document establishes Project Horizon's decision-making philosophy — the principles, values, and trade-offs that guide every downstream choice.
>
> **Distinction from Vision:**
> - **Vision says:** Why Project Horizon exists and what problem it solves for users.
> - **Philosophy says:** How the team building it chooses to think, prioritize, and decide.
>
> **Scope boundaries:**
> - **In scope:** Guiding principles, named values with priority rankings, explicit trade-offs
> - **Out of scope:** Feature specifications, architectural decisions, implementation choices

**Correct (meta-level — only when generating the standard itself):**
> This document defines the standard for Philosophy Documentation within the engineering documentation ecosystem. Philosophy Documentation establishes the product's guiding principles, values, and the deliberate trade-offs that shape every downstream decision. Unlike Vision, which explains **why** the product exists, Philosophy explains **how the people building it choose to think and decide**.

**Incorrect:**
> This document defines the Philosophy for the React frontend and PostgreSQL backend of Project Horizon.
> *Why wrong: Technology-specific — references concrete technologies instead of describing Philosophy's role in the ecosystem.*

## Writing Guidance

- **Tone:** inspirational
- **Voice:** first person plural
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** State the philosophical purpose specific to this system; distinguish from Vision explicitly (Vision=why, Philosophy=how); define scope boundaries (principles/values/trade-offs in scope, features/architecture out of scope); use language that endures across technology changes
- **Don't:** Use generic mission statements; copy purpose from project charter; mention specific technologies or frameworks; describe features or architecture

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision(01)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
