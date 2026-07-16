# Platform Pillars — Generation Template

> **Domain:** vision
> **Section:** pillars
> **Source:** `documentation-standards/01-vision-standards.md` §Platform Pillars
> **Relationships:** `audit/deterministic/document/01-vision-relationships.yaml`

Generate the Platform Pillars section for a Vision document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | philosophy / guiding_principles | Pillars must inspire Philosophy's guiding principles — pillars are the foundational capabilities that philosophy operationalizes |

## Template

```markdown
## [Pillar Name 1]

[One-sentence description of this pillar and its role in the product]

## [Pillar Name 2]

[One-sentence description of this pillar and its role in the product]

## [Pillar Name 3]

[One-sentence description of this pillar and its role in the product]
```

## Examples

**Correct:**
> **Reliable Connections** — Every connection to an external system is resilient, recoverable, and transparent in its status.
> **Data Integrity** — Information delivered through the product is always accurate and traceable to its source.
> **Simple Configuration** — Setting up a new data flow requires no coding and minimal manual steps.

**Incorrect:**
> **Microservices** — The product uses a microservices architecture for scalability.
> **Docker Containers** — All components run in Docker for consistent deployment.
> **CI/CD Pipeline** — Continuous integration ensures code quality.
> *Why wrong: Describes technology choices and implementation architecture instead of foundational capability pillars that organize the product.*

## Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Name each pillar with a memorable, two-word phrase; write one sentence per pillar that explains its role in the product; ensure pillars cover the full product scope without overlap
- **Don't:** Name specific technologies or components; use abstract nouns without a clear product connection; list more than five pillars

**Required subsections:** 3-5 named pillars
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
