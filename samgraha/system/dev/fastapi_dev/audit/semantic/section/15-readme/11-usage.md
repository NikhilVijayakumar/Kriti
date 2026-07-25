# Usage Audit

This section details the Usage Audit.

## Version
1.0.0

## Engineering Intent
Usage demonstrates the project's primary functions with real, runnable examples and their expected output — proof the thing works, not a description of what it could do.

## Audit Objectives
- Working command examples covering primary functions
- Expected output shown alongside each example
- Common workflows demonstrated, not just single isolated commands

## Expected Quality
- Basic Usage as a required subsection with at least one full example
- Common Workflows (optional) shows realistic multi-step sequences
- Examples are copy-paste runnable, not pseudocode

## Red Flags
- "Check --help for more information" instead of actual examples
- Examples without expected output — reader can't verify correctness
- Only covers a trivial/toy case, not the primary function the project exists for

## Edge Cases
- Interactive/GUI-driven tool where CLI examples don't fully apply — use screenshots or described interaction sequences instead, but still concrete
- Library (not a CLI/service) — usage examples should be code snippets showing the primary API call

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Working command/code examples for primary functions |
| C2 | mandatory | 0 or 30 | Expected output shown |
| C3 | recommended | 0 or 30 | Common workflows demonstrated beyond a single command |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.89,
  "severity": "error",
  "evidence": { "section_id": 11, "paragraph_index": 0, "excerpt": "The scheduler can be used to run pipelines. It supports many options. Check --help for more information." },
  "message": "Usage has no runnable example, defers to --help instead of demonstrating primary functions."
}
```
