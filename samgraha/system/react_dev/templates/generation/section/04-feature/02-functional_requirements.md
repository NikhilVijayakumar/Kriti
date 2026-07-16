# Functional Requirements — Generation Template

> **Domain:** feature
> **Section:** functional_requirements
> **Source:** `documentation-standards/04-feature-standards.md` §Functional Requirements
> **Relationships:** `audit/deterministic/document/04-feature-relationships.yaml`

Generate the Functional Requirements section for a Feature document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature_design / design_rationale | Functional Requirements must inform Feature Design's rationale — design must satisfy every requirement |

## Template

```markdown
## Functional Requirements

> **semantic_type:** `functional_requirements`
> **scope:** [Functional behaviors the feature must exhibit]
> **out_of_scope:** [Implementation details excluded]
> **contributes:** [How this feeds downstream design]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

- [FR-001] The feature shall [behavior] when [condition].
- [FR-002] The feature shall [behavior] when [condition].
- [FR-003] The feature shall [behavior] when [condition].
```

## Examples

**Correct:**
> - [FR-001] CloudBridge shall synchronize data between source and target systems when a sync request is initiated.
> - [FR-002] CloudBridge shall detect conflicting changes when both source and target contain modifications to the same record.
> - [FR-003] CloudBridge shall preserve data integrity when a partial failure occurs during synchronization.

**Incorrect:**
> - [FR-001] CloudBridge shall use the Apache Kafka producer API to publish sync events to the broker topic.
> - [FR-002] CloudBridge shall query the PostgreSQL `sync_status` table using the SQLAlchemy ORM.
> - [FR-003] CloudBridge shall retry failed HTTP requests using exponential backoff with a maximum of 5 retries.
> *Why wrong: Each requirement describes a specific technology choice (Kafka API, PostgreSQL ORM, HTTP retry logic) rather than the functional behavior the feature must exhibit.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Write one atomic requirement per bullet using shall/must language; make each requirement independently testable; describe the behavior the product must exhibit under specific conditions
- **Don't:** Reference specific technologies, APIs, or libraries; write compound requirements that combine multiple behaviors; use vague terms like "should" or "might" without a testable condition

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision, Acceptance Criteria

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
