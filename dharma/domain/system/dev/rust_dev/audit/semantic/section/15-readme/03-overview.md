# Overview Audit

This section details the Overview Audit.

## Version
1.0.0

## Engineering Intent
Overview explains the problem the project solves and the approach taken, at a level a new reader can absorb before touching code. It bridges Short Description and the detailed docs — narrative, not technical.

## Audit Objectives
- States the problem before the solution
- Describes the approach at a high level, no architecture diagrams or component names
- References Vision for readers who want deeper context
- No technology stack or implementation detail

## Expected Quality
- Two-part structure: problem paragraph, then approach paragraph
- Written for a new contributor, not an existing expert
- Cross-references Vision or Key Capabilities rather than duplicating them

## Red Flags
- Describes the technology stack or internal architecture instead of problem/approach
- Jumps straight to "how to use it" without stating the problem first
- Duplicates the Short Description almost verbatim with no added context
- Includes component/module names that belong in Architecture, not README

## Edge Cases
- Well-known problem space where extensive problem restatement would be redundant — a shorter problem framing is acceptable if the approach paragraph is substantive
- Project with no single "problem" (e.g. a general-purpose library) — describe the capability gap it fills instead

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Problem stated before solution/approach |
| C2 | mandatory | 0 or 30 | No technology stack or architecture-level detail |
| C3 | recommended | 0 or 30 | References Vision or Key Capabilities for deeper context |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.82,
  "severity": "error",
  "evidence": { "section_id": 4, "paragraph_index": 1, "excerpt": "Acme Scheduler is a Python application using Celery with Redis as a broker." },
  "message": "Overview describes the technology stack instead of the problem and high-level approach."
}
```
