# Design Constraints Audit

This section details the Design Constraints Audit.

## Version
1.0.0

## Engineering Intent
Design constraints define the boundaries within which design decisions must operate—platform limitations, brand guidelines, technical dependencies, and regulatory requirements that shape the feasible solution space.

## Audit Objectives
- All design constraints are explicitly documented
- Platform-specific constraints (responsive breakpoints, device capabilities) are captured
- Brand guideline constraints (colors, typography, spacing) are enumerated
- Technical constraints (component library, rendering engine limits) are listed
- Regulatory constraints (data privacy, accessibility law) are identified
- Constraints are validated against actual platform capabilities

## Expected Quality
- Constraints are categorized (platform, brand, technical, regulatory)
- Each constraint has a source or rationale
- Responsive breakpoints are defined with supported viewports
- Brand tokens (colors, type scale, spacing units) are documented
- Known platform limitations have fallback strategies

## Red Flags
- Undocumented assumptions about platform capabilities
- Brand constraints referenced but not defined in a token system
- Technical constraints discovered late in implementation
- Regulatory constraints treated as optional
- Constraints listed without validation against actual platform limits

## Edge Cases
- Constraints that conflict with each other (e.g., brand color fails contrast)
- Constraints inherited from upstream design systems that may not apply
- Disappearing constraints when platform or brand guidelines are updated

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | All design constraints documented and categorized |
| C2 | mandatory | 0 or 30 | Brand and platform constraints have defined sources |
| C3 | recommended | 0 or 30 | Constraint conflicts identified with fallback strategies |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "Responsive breakpoints: 320px, 768px, 1024px, 1440px. Brand palette: 8 colors defined..." },
  "message": "All 22 design constraints documented across 4 categories with validated sources."
}
```
