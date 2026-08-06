# Documentation Structure Audit

This section details the Documentation Structure Audit.

## Version
1.0.0

## Engineering Intent
Documentation Structure tells a reader where the rest of the documentation lives and in what order to read it. It's the navigation layer between README and every other standard.

## Audit Objectives
- Lists documentation directories/key files with their purpose
- States the organization principle (by standard, by feature, by audience, etc.)
- Provides concrete navigation guidance — a reading order or entry point, not just a directory dump

## Expected Quality
- Directory list mirrors Repository Structure's documentation entry but goes one level deeper into docs organization
- Explicit guidance on where to start reading
- Links or references resolve to real paths in the repo

## Red Flags
- Vague statement ("there is a lot of markdown in the docs folder") with no structure or navigation
- Lists directories without stating what's in each
- No guidance on reading order for a new contributor

## Edge Cases
- Very flat documentation (single docs.md) — state that explicitly rather than describing a structure that doesn't exist
- Documentation split across multiple repos — note the split and where each part lives

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Documentation directories listed with purpose |
| C2 | mandatory | 0 or 30 | Organization principle stated |
| C3 | recommended | 0 or 30 | Concrete navigation/reading-order guidance provided |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.84,
  "severity": "error",
  "evidence": { "section_id": 8, "paragraph_index": 0, "excerpt": "All documentation is in the docs folder. There is a lot of markdown in there." },
  "message": "Documentation Structure gives no directory breakdown or navigation guidance."
}
```
