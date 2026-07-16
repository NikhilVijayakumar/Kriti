# User Experience Audit

This section details the User Experience Audit.

## Version
1.0.0

## Engineering Intent
User experience (UX) audit evaluates how a feature feels, flows, and responds from the user's perspective. It ensures the design minimizes friction, meets accessibility standards, and delivers a coherent interaction model aligned with user expectations.

## Audit Objectives
- User flows are logical and match mental models
- Visual hierarchy guides attention to primary actions
- Accessibility standards (contrast, keyboard nav, screen reader) are met
- Error states and empty states communicate clearly
- Consistency with platform patterns and existing UI conventions
- Interaction feedback (loading, hover, press) is present and meaningful

## Expected Quality
- Primary action is visually prominent and reachable within 2 taps/clicks
- All interactive elements have visible focus indicators
- Text meets WCAG AA contrast ratio
- Feature introduces no regression in existing UX patterns
- Touch targets are at least 44x44px (mobile)

## Red Flags
- No consideration of loading, empty, error, or edge states
- Inconsistent spacing, typography, or color usage
- UI pattern differs from platform convention without justification
- Feature requires unnecessary steps to complete primary task
- Accessibility treated as afterthought

## Edge Cases
- Feature used with system font scaling or high-contrast mode
- Feature used with keyboard-only navigation
- Feature used on smallest supported screen size
- Feature used while another system notification is active

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Primary user flow is logical and minimal-friction |
| C2 | mandatory | 0 or 25 | Visual hierarchy guides user to primary action |
| C3 | mandatory | 0 or 25 | Accessibility basics (contrast, keyboard nav) met |
| C4 | recommended | 0 or 20 | Interaction feedback present for all states |

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
