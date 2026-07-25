# Acceptance Criteria — Generation Template

> **Domain:** feature
> **Section:** acceptance_criteria
> **Source:** `documentation-standards/04-feature-standards.md` §Acceptance Criteria
> **Relationships:** `audit/deterministic/document/04-feature-relationships.yaml`

Generate the Acceptance Criteria section for a Feature document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature_technical / testing_strategy | Acceptance Criteria must inform Feature Technical Design's testing strategy — test cases derive from these criteria |

## Template

```markdown
## Acceptance Criteria

> **semantic_type:** `acceptance_criteria`
> **scope:** [Verifiable conditions confirming feature completeness]
> **out_of_scope:** [Test implementation details excluded]
> **contributes:** [How this feeds downstream validation]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

- [AC-001] Given [precondition], when [action], then [expected result].
- [AC-002] Given [precondition], when [action], then [expected result].
- [AC-003] Given [precondition], when [action], then [expected result].
```

## Examples

**Correct:**
> - [AC-001] Given a dataset in the source system, when a sync request is initiated, then CloudBridge shall transfer all records to the target system without data loss.
> - [AC-002] Given conflicting records in both systems, when sync encounters a conflict, then CloudBridge shall flag the conflicting records and preserve both versions for review.
> - [AC-003] Given a partial failure during synchronization, when the process is interrupted, then CloudBridge shall resume from the last successful checkpoint without duplicating records.

**Incorrect:**
> - [AC-001] Given a sync request, when the `SyncManager.process()` method is called, then it should return a 200 status code within 500ms.
> - [AC-002] Given a conflict, when the `ConflictResolver` class is invoked, then it should insert a row into the `conflict_log` table.
> - [AC-003] Given a failure, when the retry mechanism triggers, then exponential backoff should be applied up to 3 attempts.
> *Why wrong: These criteria reference specific code components, database tables, and implementation mechanics rather than describing the verifiable conditions that confirm feature completeness from the user's perspective.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Use Given/When/Then format for each criterion; derive every criterion from a specific functional requirement or business rule; make each criterion independently verifiable without code inspection
- **Don't:** Reference specific code components, database tables, or API endpoints; write criteria that require reading source code to verify; use vague pass/fail conditions without observable outcomes

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Functional Requirements, Business Rules

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
