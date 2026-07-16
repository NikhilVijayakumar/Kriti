# Short Description — Generation Template

> **Domain:** readme
> **Section:** short_description
> **Source:** `documentation-standards/15-readme-standards.md` §Short Description
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the Short Description section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / vision_statement | Short Description must summarize the project's purpose from Vision(01) |

## Template

```markdown
## Short Description

[One to two sentences stating what the project does and who it is for — under 200 characters]
```

## Examples

**Correct:**
> A lightweight task scheduler that automates data pipeline orchestration across distributed environments.

**Incorrect:**
> Acme Scheduler is a tool built with Python 3.12, uses Apache Airflow as its backend, stores data in PostgreSQL, and supports Docker deployment. Install it with pip install acme-scheduler. It has 15 commands and supports cron expressions.
> *Why wrong: Short Description must be one to two sentences under 200 characters summarizing what the project does, not listing technology stack, installation instructions, or feature counts.*

## Writing Guidance

- **Tone:** conversational
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** Write one to two sentences under 200 characters; state what the project does and who it is for
- **Don't:** Include technology stack details; mention installation steps; list feature counts or version numbers

**Minimum content:** 1 paragraph
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Vision(01), Overview, Repository Overview

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
