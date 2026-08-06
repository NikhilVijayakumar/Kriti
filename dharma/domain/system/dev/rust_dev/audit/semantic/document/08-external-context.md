# External Context Document Audit

This section details the External Context Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies External Context Documentation coheres as one accurate picture of the outside world the system integrates with — Integration Contract, Constraints, and Dependencies must not contradict each other. Section-level quality is owned by `audit/semantic/section/external-context/`; this file owns cross-section and cross-document consistency.

## Audit Objectives
- Integration Contract, Constraints, and Dependencies are mutually consistent — a dependency listed without a corresponding integration contract, or a constraint that contradicts what the contract promises, is a document-level failure
- All External Context documents in the domain cohere as one system — no orphaned or contradictory descriptions of the same external system
- Terminology is consistent across all External Context sections — the same external system or API isn't named differently in different sections

## Expected Quality
- Every Dependency has a matching Integration Contract describing how it's actually consumed
- Constraints imposed by an external system are reflected consistently wherever that system is discussed
- External system names are used identically across sections and documents

## Red Flags
- A Dependency is listed with no corresponding Integration Contract
- Constraints describes a limitation the Integration Contract's description contradicts (e.g. claims real-time capability the constraint rules out)
- Two documents describe the same external system with contradictory capabilities
- Same external system referred to by different names, confusing downstream Engineering/Feature Technical references

## Edge Cases
- External system currently being migrated to a new version/provider — acceptable if both old and new are explicitly marked with a transition timeline, not silently contradictory
- Multiple integration points with the same external system for different purposes — acceptable if each is separately and consistently documented, not merged into one ambiguous entry

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Integration Contract, Constraints, and Dependencies are mutually consistent |
| C2 | mandatory | 0 or 30 | Terminology (external system names) consistent across all sections and documents |
| C3 | recommended | 0 or 30 | All External Context documents cohere as one system |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.81,
  "severity": "error",
  "evidence": { "section_id": 33, "paragraph_index": 0, "excerpt": "Dependencies lists 'Payment Gateway API' with no corresponding Integration Contract entry." },
  "message": "A listed dependency has no matching integration contract describing how it's consumed."
}
```
