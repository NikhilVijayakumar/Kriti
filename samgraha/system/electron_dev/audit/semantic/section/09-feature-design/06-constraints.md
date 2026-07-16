# Constraints Audit

This section details the Constraints Audit.

## Version
1.0.0

## Engineering Intent
Constraints document the boundaries within which a feature must be designed and built: technical, business, temporal, and regulatory. Auditing constraints ensures all limitations are surfaced early, trade-offs are explicit, and the design does not violate any hard boundary that would cause rework or compliance failure.

## Audit Objectives
- All constraint types (technical, business, timeline, regulatory, accessibility) are enumerated
- Each constraint is specific and verifiable
- Constraints distinguish hard (must) from soft (should) boundaries
- Constraints are traceable to a source (policy, API limit, law, etc.)
- Design decisions that violate constraints are flagged
- Constraints are current and not contradicting each other

## Expected Quality
- Constraints are listed with identifiers (CT1, CT2) and type labels
- Hard constraints are clearly marked vs. soft constraints
- Each constraint references its origin or source document
- Constraints are not confused with requirements or non-goals
- Constraints include minimum device/browser/OS support levels

## Red Flags
- Constraints section is missing or states "none"
- Constraints are too vague to verify ("must perform well")
- Hard constraints treated as negotiable
- Constraints contradict each other without resolution
- Constraints are copy-pasted from another project without adaptation

## Edge Cases
- New constraint discovered mid-cycle (design must adapt)
- Constraint that forces degradation of UX (acceptable trade-off?)
- Regulatory constraint that applies only to specific user segments
- Platform-specific constraints that don't apply cross-platform

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Constraints are enumerated with source attribution |
| C2 | mandatory | 0 or 30 | Hard vs. soft constraints are distinguished |
| C3 | recommended | 0 or 20 | No design-violating constraints exist |
| C4 | recommended | 0 or 20 | Constraints include device/browser/OS minimums |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "..." },
  "message": "..."
}
```
