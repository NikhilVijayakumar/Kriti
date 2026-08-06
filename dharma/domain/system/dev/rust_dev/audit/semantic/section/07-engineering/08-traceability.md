# Traceability Audit

This section details the Traceability Audit.

## Version
1.0.0

## Engineering Intent
Traceability ensures every requirement, design decision, implementation artifact, and test case is bidirectionally linked. No orphaned artifacts, no unmotivated code.

## Audit Objectives
- Every requirement maps to one or more implementation artifacts
- Every code module traces back to a documented requirement
- Test cases are linked to the requirements they verify
- Changes cascade through the traceability graph
- Trace links are versioned alongside artifacts

## Expected Quality
- Bidirectional links exist between requirements and implementation
- Trace matrix covers all lifecycle stages (req → design → code → test)
- Each link has a type (derives, implements, verifies, depends)
- Orphaned artifacts are zero

## Red Flags
- Requirements with zero implementation links
- Code modules with zero requirement links
- Tests without linked requirements
- Trace links that reference deleted or renamed artifacts
- Manual trace maintenance (no automation)

## Edge Cases
- Generated code with synthetic trace links
- Third-party libraries with no upstream requirements
- Cross-repository traceability
- Deleted requirements with remaining implementation

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Bidirectional links exist for all requirements |
| C2 | mandatory | 0 or 30 | Every test traces to at least one requirement |
| C3 | recommended | 0 or 20 | No orphaned code modules |
| C4 | recommended | 0 or 20 | Trace links are version-controlled |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 17, "paragraph_index": 3, "excerpt": "Requirement REQ-42 traces to module auth/service.py via implements link." },
  "message": "All 47 requirements have bidirectional trace links."
}
```
