# Overview — Generation Template

> **Domain:** readme
> **Section:** overview
> **Source:** `documentation-standards/15-readme-standards.md` §Overview
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the Overview section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / system_overview | Overview must be consistent with Architecture(05) system overview |

## Template

```markdown
## Overview

[Explain the problem the project solves]
[Describe the project's approach at a high level]
[Reference Vision(01) for deeper context — no implementation details, no architecture diagrams]
```

## Examples

**Correct:**
> Managing data pipelines across multiple environments requires consistent scheduling, monitoring, and error handling. Most teams build custom scripts that become difficult to maintain.
>
> Acme Scheduler provides a declarative configuration format and built-in retry logic that lets teams define and deploy pipelines without writing orchestration code.

**Incorrect:**
> Acme Scheduler is a Python application using the Celery task queue with Redis as a broker. It consists of a scheduler module, a task runner, and a REST API built with FastAPI.
> *Why wrong: Overview must explain the problem and solution at a high level, not describe the technology stack or internal architecture.*

## Writing Guidance

- **Tone:** inspirational
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** new contributor
- **Do:** Explain the problem the project solves; describe the approach at a high level; reference Vision for deeper context
- **Don't:** Describe the technology stack; include architecture diagrams; list implementation details or internal components

**Minimum content:** 2 paragraphs
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Vision(01), Key Capabilities, Repository Overview, Getting Started

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
