# Philosophy Audit

This section details the Philosophy Audit.

## Version
1.0.0

## Engineering Intent
The philosophy section articulates the core beliefs, values, and design worldview that inform the vision. It explains the "why behind the what" — the deeply held convictions about how the system should be conceived, built, and evolved. Philosophy provides intrinsic consistency across decisions.

## Audit Objectives
- Philosophy is substantive and not generic platitudes
- Core beliefs are stated explicitly, not implied
- Philosophy provides decision-making guidance for trade-offs
- Philosophy is distinguishable from principles (deeper convictions)
- Philosophy aligns with the problem context and solution approach

## Expected Quality
- Philosophy statements are specific to the domain or problem space
- Each philosophical belief includes its implication for the system
- Philosophy avoids trite or copy-paste values ("innovation", "excellence")
- Philosophy informs how conflicts should be resolved
- Philosophy is internally consistent across all statements

## Red Flags
- Philosophy section reads as a list of corporate buzzwords
- Philosophy statements are interchangeable with any other product
- Philosophy contradicts the stated pillars or guiding principles
- Philosophy is aspirational but has no operational implications
- Philosophy section is significantly shorter or longer than adjacent sections

## Edge Cases
- Philosophy that must reconcile competing schools of thought (e.g., privacy vs personalization)
- Philosophy section in a regulated industry where certain beliefs are mandated
- Philosophy that evolves across document versions without clear change tracking

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Philosophy statements are domain-specific and substantive |
| C2 | mandatory | 0 or 30 | Each belief includes operational implications for decision-making |
| C3 | recommended | 0 or 30 | Philosophy internally consistent with pillars and principles |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 5, "paragraph_index": 1, "excerpt": "We believe data ownership must rest with the citizen, not the platform..." },
  "message": "Philosophy statements are domain-specific with clear operational implications."
}
```
