# Scalability Testing — Generation Template

> **Domain:** qa
> **Section:** scalability_testing
> **Source:** `documentation-standards/12-qa-standards.md` §Scalability Testing
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the Scalability Testing section for a QA document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / system_overview | Growth scenarios must reflect Architecture scalability decisions |

## Template

```markdown
## Scalability Testing

### Growth Scenarios

| Scenario | Load Multiplier | Expected Behavior | Breaking Point | Scaling Strategy |
|----------|----------------|-------------------|----------------|-----------------|
| Moderate growth | 2x baseline | [Expected behavior] | [Where it breaks] | [How it scales] |
| Significant growth | 5x baseline | [Expected behavior] | [Where it breaks] | [How it scales] |
| Extreme growth | 10x baseline | [Expected behavior] | [Where it breaks] | [How it scales] |

### Breaking Points

| Component | Breaking Point | Failure Mode | Recovery Strategy |
|-----------|---------------|--------------|-------------------|
| [Component] | [Threshold] | [How it fails] | [How to recover] |
```

## Examples

**Correct:**
> ### Growth Scenarios
>
> | Scenario | Load Multiplier | Expected Behavior | Breaking Point | Scaling Strategy |
> |----------|----------------|-------------------|----------------|-----------------|
> | Moderate growth | 2x baseline | Response time increases < 20% | N/A | Horizontal pod autoscaling |
> | Significant growth | 5x baseline | Response time increases < 50% | 8x — connection pool exhaustion | Add read replicas + connection pooling |
> | Extreme growth | 10x baseline | Graceful degradation with queuing | 15x — message queue overflow | Rate limiting + queue partitioning |
>
> ### Breaking Points
>
> | Component | Breaking Point | Failure Mode | Recovery Strategy |
> |-----------|---------------|--------------|-------------------|
> | Database connection pool | 800 connections | New connections rejected | Drain idle connections; scale read replicas |
> | Message queue | 100k pending messages | Messages dropped after 1h TTL | Increase consumer count; archive old messages |

**Incorrect:**
> The system should scale to handle more users as we grow. We will add servers when needed.
> *Why wrong: scalability testing requires defined growth scenarios with specific load multipliers and documented breaking points.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** architect
- **Do:** Define growth scenarios with explicit load multipliers (2x, 5x, 10x); document the breaking point and failure mode for each critical component; specify a recovery strategy per component
- **Don't:** Describe scalability as future intent; omit breaking points; list components without stating how each fails under load

**Required subsections:** Growth Scenarios table, Breaking Points table
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Architecture(05)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
