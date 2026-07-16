# Business Rules — Generation Template

> **Domain:** feature
> **Section:** business_rules
> **Source:** `documentation-standards/04-feature-standards.md` §Business Rules
> **Relationships:** `audit/deterministic/document/04-feature-relationships.yaml`

Generate the Business Rules section for a Feature document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| (none section-owned) | — | Business Rules are internally consistent with Functional Requirements and Acceptance Criteria |

## Template

```markdown
## Business Rules

> **semantic_type:** `business_rules`
> **scope:** [Business logic governing feature behavior]
> **out_of_scope:** [Technical constraints excluded]
> **contributes:** [How this feeds downstream design]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

- [BR-001] When [condition], then [behavior].
- [BR-002] When [condition], then [behavior].

[Optional: flowchart showing rule decision logic]
```

## Examples

**Correct:**
> - [BR-001] When a record exists in both source and target with different values, then CloudBridge shall flag the conflict and pause synchronization for that record.
> - [BR-002] When the source dataset is empty, then CloudBridge shall complete with a no-op result and log the condition.

**Incorrect:**
> - [BR-001] When a conflict is detected, then the system shall execute the `resolve_conflict()` method defined in `sync_engine.py`.
> - [BR-002] When no source data exists, then the application shall return HTTP 204 No Content from the sync endpoint.
> *Why wrong: These rules reference implementation details (specific Python files and methods, HTTP status codes) instead of describing the business logic in technology-independent terms.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** product owner
- **Do:** Express each rule as a conditional When/Then statement; capture domain-specific business logic that cannot be inferred from requirements alone; include edge cases and exception handling rules
- **Don't:** Describe technical validation, input sanitization, or database constraints; reference implementation code or system components; write rules that duplicate functional requirements

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** flowchart (when rules involve branching logic)
**Required cross-references:** Functional Requirements, Acceptance Criteria

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
