# Related Work Semantic Audit

This section details the Related Work Semantic Audit.

## Version
1.0.0

## Engineering Intent
Enforces Q1 Reviewer Persona citation-quality rules and verifies the Gap-Closing Bridge actually motivates Problem Definition, not a generic segue. This file owns the receiving end of the Introduction → Related Work bridge and the sending end of the Related Work → Problem Definition bridge.

## Audit Objectives
- Zero unverified/predatory sources (blogs, non-peer-reviewed URLs, known predatory journals).
- 60-70% of citations fall within the recent 3-4 year window (2022-2026); 2-4 citations are directly from ESWA.
- The Gap-Closing Bridge explicitly identifies the unresolved challenge that motivates Problem Definition — not a disconnected segue.

## Expected Quality
- Citations are exclusively from high-impact (Q1/Q2 Scopus, CORE A/A*) venues.
- The taxonomy is organized by approach (rule-based / learning-based / hybrid), not chronologically.
- The final sentence of the section names the specific gap Problem Definition will formalize.

## Red Flags
- Links to Medium articles, generic tech blogs, or excessive pre-print servers.
- Section ends without an explicit gap-closing statement.
- Chronological listing instead of taxonomic grouping.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Zero unverified/predatory sources |
| C2 | mandatory | 0 or 40 | Gap-Closing Bridge explicitly identifies the unresolved challenge that motivates Problem Definition |
| C3 | recommended | 0 or 20 | Meets recent-citation ratio (60-70%) and ESWA citation quota (2-4) |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.80,
  "severity": "error",
  "evidence": { "paragraph_index": 9, "excerpt": "In summary, many approaches exist in this space." },
  "message": "Gap-Closing Bridge is a generic segue, not an explicit statement of the unresolved challenge Problem Definition must formalize."
}
```
