# Rationale — Generation Template

> **Domain:** architecture
> **Section:** rationale
> **Source:** `documentation-standards/05-architecture-standards.md` §Rationale
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the Rationale section for an Architecture document.

## Relationships

No section-owned outgoing relationships. Rationale is an internal architecture section with no cross-domain constraints.

## Template

```markdown
## Rationale

### [Decision Name]
- **Context:** [what prompted this decision]
- **Decision:** [what was decided]
- **Alternatives Considered:** [what else was evaluated]
- **Rejection Reason:** [why alternatives were rejected]
- **Architectural Goal:** [which goal this serves]
```

## Examples

**Correct:**
> **Event-Driven Ingestion**
> - **Context:** Multiple external systems submit data at unpredictable rates and volumes.
> - **Decision:** Ingestion publishes events asynchronously rather than processing synchronously.
> - **Alternatives Considered:** Synchronous request/response ingestion with backpressure.
> - **Rejection Reason:** Synchronous processing would couple external system availability to ingestion availability, violating the reliability pillar.
> - **Architectural Goal:** Resilient Connections.

**Incorrect:**
> We chose Kafka over RabbitMQ because it has better throughput benchmarks and our team already knows the Java client library.
> *Why wrong: justifies a specific technology choice by implementation-level benchmarks and team familiarity — that belongs in Engineering's rationale, not Architecture's. Architecture rationale should justify structural decisions (sync vs async, ownership boundaries) against architectural goals, not product-specific tooling.*

## Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Record the context that prompted each decision; name the alternatives that were actually considered; tie every decision back to an architectural goal or pillar
- **Don't:** Justify decisions by technology benchmarks, licensing, or team familiarity; record decisions without a rejected alternative; let rationale entries go stale once a decision is superseded

**Minimum content:** 1 entry per significant decision
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Vision(01), Philosophy(02)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
