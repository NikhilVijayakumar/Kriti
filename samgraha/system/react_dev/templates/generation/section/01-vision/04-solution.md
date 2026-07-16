# Solution — Generation Template

> **Domain:** vision
> **Section:** solution
> **Source:** `documentation-standards/01-vision-standards.md` §Solution
> **Relationships:** `audit/deterministic/document/01-vision-relationships.yaml`

Generate the Solution section for a Vision document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | Solution must inspire each Feature's purpose — the solution approach determines what features are needed |
| `derives_from` | architecture / system_overview | Solution must inform Architecture's system overview — how the product approach maps to system structure |

## Template

```markdown
[High-level description of what the product does to solve the stated problem]
[How the product's approach delivers value to the target audience]
```

## Examples

**Correct:**
> DataSync automates the collection, transformation, and delivery of data across connected systems. It provides a single place to define data flows and ensures that information stays consistent wherever it is used.

**Incorrect:**
> DataSync uses Python with Celery workers and RabbitMQ to queue data jobs, storing results in a PostgreSQL database with a React dashboard for monitoring.
> *Why wrong: Describes architecture and implementation technology instead of the product-level approach to solving the problem.*

## Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** Describe the approach at the product level using action verbs; connect the solution directly back to the Problem section; keep descriptions at the "what it does" level
- **Don't:** Name libraries, frameworks, or databases; describe data flows, APIs, or internal system boundaries; discuss trade-offs between technology options

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Problem

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
