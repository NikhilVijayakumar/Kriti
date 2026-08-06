# Business Rules Audit

This section details the Business Rules Audit.

## Version
1.0.0

## Engineering Intent
Business rules encode domain logic, policies, calculations, and decision logic the system must enforce. They must be atomic, unambiguous, and expressed declaratively. Good business rules are independent of implementation and can be validated by domain experts.

## Audit Objectives
- Each business rule is atomic (single condition or action)
- Business rules are expressed declaratively (what, not how)
- Rules are unambiguous and deterministic
- Rules have identifiable owners or sources
- Rules handle edge cases and exceptions

## Expected Quality
- Business rules use consistent condition → outcome format
- Rules include real-world examples
- Exception paths are documented alongside happy path
- Rules reference regulatory or policy source

## Red Flags
- Business rules mixed with functional requirements
- Rules that are contradictory or overlapping
- Rules that depend on undefined data or state
- Rules expressed as pseudocode rather than declaratively

## Edge Cases
- Empty business rules section (acceptable for simple features)
- Rules that apply only under specific temporal conditions
- Rules with competing outcomes requiring prioritization

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Each rule is atomic and unambiguous |
| C2 | mandatory | 0 or 30 | Rules are expressed declaratively |
| C3 | recommended | 0 or 30 | Exception paths are documented |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.89,
  "severity": "error",
  "evidence": { "section_id": 7, "paragraph_index": 3, "excerpt": "IF order_total > 1000 THEN require_manager_approval = true." },
  "message": "Business rule is atomic with a single condition and outcome."
}
```
