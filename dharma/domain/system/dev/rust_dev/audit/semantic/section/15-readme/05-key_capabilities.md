# Key Capabilities Audit

This section details the Key Capabilities Audit.

## Version
1.0.0

## Engineering Intent
Key Capabilities is a scannable list of what the project can do, letting a reader assess fit in seconds. It stays at the capability level — not a feature changelog, not a spec.

## Audit Objectives
- 3 to 7 capabilities listed
- Each capability is a short, independent, scannable phrase
- No implementation details, library versions, or test counts

## Expected Quality
- Bullet list, each item a noun phrase or short clause
- Capabilities are non-overlapping — no near-duplicate entries
- Ordered by importance or by the order a user would discover them

## Red Flags
- Fewer than 3 or more than 7 items (too thin to be useful, or too long to scan)
- Items describe library/dependency choices instead of user-facing capability
- Items reference test counts, coverage percentages, or version numbers
- Items require already knowing the project's internals to parse

## Edge Cases
- Project with genuinely one core capability — acceptable to have fewer than 3 if the single capability is substantial and well-stated, note as an exception rather than silently under-count
- Platform/framework with dozens of features — pick the top-level capabilities, not an exhaustive feature list

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | 3-7 capabilities listed as scannable phrases |
| C2 | mandatory | 0 or 30 | No implementation details, versions, or test counts |
| C3 | recommended | 0 or 30 | Capabilities are non-overlapping and independently understandable |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.83,
  "severity": "error",
  "evidence": { "section_id": 6, "paragraph_index": 0, "excerpt": "- Uses Celery 5.3.2 with Redis broker\n- Has 47 unit tests" },
  "message": "Key Capabilities lists implementation details and test counts instead of user-facing capabilities."
}
```
