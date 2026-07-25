# References Semantic Audit

This section details the References Semantic Audit.

## Version
1.0.0

## Engineering Intent
Enforces PCEMS 2026's strict APA formatting/typography rule for References and the Q1 Reviewer Persona citation-quality rules.

## Audit Objectives
- All references are formatted in strict APA style; section heading is Heading 1 (Arial, 12pt bold); reference items are strictly 8pt font.
- Zero unverified/predatory sources (blogs, non-peer-reviewed URLs, known predatory journals).
- 100% match between in-text citations and the References list.

## Expected Quality
- Every reference entry is independently verifiable and APA-formatted without exception.

## Red Flags
- Reference items in a font size other than 8pt.
- Non-APA formatted entries.
- An in-text citation with no matching References entry, or vice versa.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | All references are APA-formatted, heading is Heading 1 Arial 12pt bold, entries are 8pt font |
| C2 | mandatory | 0 or 30 | Zero unverified/predatory sources |
| C3 | mandatory | 0 or 30 | 100% match between in-text citations and the References list |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.90,
  "severity": "error",
  "evidence": { "excerpt": "Reference list rendered at 10pt font." },
  "message": "Reference entries must be strictly 8pt font per PCEMS 2026 typography rules."
}
```
