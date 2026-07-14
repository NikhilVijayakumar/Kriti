# Development Audit

This section details the Development Audit.

## Version
1.0.0

## Engineering Intent
Development gets a contributor from clone to running the test suite and understanding the workflow — the audience is someone about to change code, not just run the project.

## Audit Objectives
- Local Setup with specific environment setup commands
- Running Tests with an actual test command and expected outcome
- Workflow description referencing coding standards, if applicable

## Expected Quality
- Local Setup and Running Tests present as distinct subsections
- Commands are specific to this project (not generic "clone and code")
- Workflow section links to Engineering's coding standards rather than restating them

## Red Flags
- "Clone the repo and start coding" with no setup or test commands
- No test command given, or test command doesn't match what CI actually runs
- Workflow guidance absent entirely, leaving contribution process undefined here (though it may live in Contributing instead — check for duplication, not omission of both)

## Edge Cases
- Monorepo where dev setup differs per package — cover the common path, note per-package differences briefly
- Projects with no formal test suite yet — state that explicitly rather than fabricating a test command

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Local Setup has specific setup commands |
| C2 | mandatory | 0 or 40 | Running Tests has an actual, correct test command |
| C3 | recommended | 0 or 20 | Workflow references coding standards |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.85,
  "severity": "error",
  "evidence": { "section_id": 12, "paragraph_index": 1, "excerpt": "To develop, clone the repo and start coding. Write tests for your changes." },
  "message": "Development gives no actual test command, only a general instruction to write tests."
}
```
