# Purpose Audit

This section details the Purpose Audit.

## Version
1.0.0

## Engineering Intent
Design purpose defines the strategic intent behind visual and interaction decisions. Every element must serve a clear functional or communicative goal aligned with product vision.

## Audit Objectives
- Design decisions are traceable to explicit purpose statements
- Every UI element serves a documented functional or communicative goal
- Purpose aligns with user needs and business objectives
- No decorative-only elements without justified rationale
- Purpose is consistent across all screens and flows

## Expected Quality
- Each major screen has a stated design purpose
- Purpose is referenced in design decision records
- Purpose is validated against user research findings
- No unexplained visual elements

## Red Flags
- UI elements present for aesthetic reasons only with no documented purpose
- Purpose statements that are generic or copy-pasted
- Missing purpose for critical interaction paths
- Purpose contradicts user research data

## Edge Cases
- Empty states with minimal UI elements
- Error screens and system messages
- Third-party embedded components

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Design purpose documented for each major screen |
| C2 | mandatory | 0 or 30 | Purpose traceable to user or business need |
| C3 | recommended | 0 or 30 | No unexplained decorative elements |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "Dashboard designed to provide at-a-glance project status..." },
  "message": "Purpose defined and aligned for all 8 primary screens."
}
```
