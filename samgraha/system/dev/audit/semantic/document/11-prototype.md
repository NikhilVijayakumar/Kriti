# Prototype Document Audit

This section details the Prototype Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies a Prototype document coheres as a whole — Mock APIs match the Data Model, Scope's in/out-of-scope lists match what's actually mocked, Traceability's upstream/downstream links hold. Section-level quality is owned by `audit/semantic/section/prototype/`; this file owns whether the pieces fit together as one falsifiable experiment.

## Audit Objectives
- Mock APIs' request/response contracts use the same entities defined in Data Model — no mocked field absent from the data model or vice versa
- Scope's in-scope items are actually mocked somewhere in Mock APIs; out-of-scope items aren't accidentally implemented
- Traceability's upstream sources and downstream consumers are consistent with what Scope and Purpose claim the prototype validates
- All Prototype documents in the domain cohere — no orphaned or contradictory prototypes
- Terminology consistent across all Prototype sections

## Expected Quality
- Every entity referenced in a Mock API request/response exists in Data Model with matching shape
- Scope's in-scope list has 1:1 coverage in Mock APIs; nothing claimed as covered is silently missing
- Traceability accurately reflects what the prototype is actually validating, not an aspirational broader claim

## Red Flags
- Mock API references a field or entity not present in Data Model
- Scope claims something is in-scope that has no corresponding mock
- Traceability claims to validate a Feature Design the prototype doesn't actually touch
- Contradictory prototypes exist for the same feature with no reconciliation or superseding note

## Edge Cases
- Prototype intentionally mocking a subset of Data Model for a narrow experiment — acceptable if Scope explicitly states the narrowing, not silently partial
- Multiple prototypes exploring different approaches to the same problem — acceptable as long as each states which alternative it's exploring, not read as contradictory duplicates

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Mock APIs and Data Model use consistent entities/fields |
| C2 | mandatory | 0 or 30 | Scope's in-scope items are actually covered by Mock APIs |
| C3 | recommended | 0 or 30 | Traceability accurately reflects what's actually validated |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.82,
  "severity": "error",
  "evidence": { "section_id": 34, "paragraph_index": 1, "excerpt": "Mock response includes `user.subscription_tier`, not present in the Data Model section." },
  "message": "Mock API references a field absent from the Data Model."
}
```
