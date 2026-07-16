# Functional Requirements Audit

This section details the Functional Requirements Audit.

## Version
1.0.0

## Engineering Intent
Functional requirements describe what the system must do. They must be complete, unambiguous, testable, and implementation-independent.

## Audit Objectives
- All functional requirements are enumerated without gaps
- Each requirement is testable (can be verified by a test)
- Requirements are implementation-independent (describe WHAT not HOW)
- Requirements use consistent terminology
- No duplicate or conflicting requirements

## Expected Quality
- Every functional requirement has a unique identifier (e.g., FR1, FR2)
- Each requirement describes a single capability
- Requirements are written in active voice
- Acceptance criteria can be derived from requirements

## Red Flags
- Requirements that describe implementation details ("the system shall use React")
- Requirements that are untestable ("the system shall be fast")
- Requirements that are vague ("the system should handle errors")
- Missing identifiers for requirements

## Edge Cases
- Empty functional requirements section (document without FRs)
- Single requirement vs comprehensive list
- Requirements mixed with business rules

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All requirements uniquely identified |
| C2 | mandatory | 0 or 30 | Each requirement is testable |
| C3 | recommended | 0 or 20 | No implementation language |
| C4 | recommended | 0 or 20 | No duplicate or conflicting requirements |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 17, "paragraph_index": 3, "excerpt": "FR1. System shall..." },
  "message": "All 12 functional requirements enumerated without gaps."
}
```
