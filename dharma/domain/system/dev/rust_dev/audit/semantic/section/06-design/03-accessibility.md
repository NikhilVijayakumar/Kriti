# Accessibility Audit

This section details the Accessibility Audit.

## Version
1.0.0

## Engineering Intent
Accessibility ensures the product is usable by people with diverse abilities. Compliance with WCAG standards is both a legal requirement and a design quality benchmark.

## Audit Objectives
- UI meets WCAG 2.1 AA standards (or documented target level)
- Color contrast ratios meet minimum thresholds
- All interactive elements are keyboard navigable
- Screen reader support with proper ARIA labels and roles
- Content is perceivable, operable, understandable, and robust
- Internationalization readiness: UI supports RTL text direction where applicable, string externalization is documented, date/number/currency formats are locale-aware
- Cultural sensitivity: no iconography, color symbolism, or phrasing with known negative connotations in target markets

## Expected Quality
- Color contrast ≥ 4.5:1 for normal text, ≥ 3:1 for large text
- All images have meaningful alt text or marked decorative
- Focus indicators visible on all interactive elements
- Semantic HTML structure with proper heading hierarchy

## Red Flags
- Color-only information conveyance
- Missing focus indicators
- Keyboard traps in navigation or forms
- Auto-playing media without pause controls
- Missing form label associations

## Edge Cases
- Custom UI components (dropdowns, modals, carousels) with no ARIA
- Dynamic content updates without screen reader announcements
- Touch targets smaller than 44x44 CSS pixels on mobile

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | WCAG 2.1 AA compliance for all screens |
| C2 | mandatory | 0 or 30 | Keyboard navigation and focus management work |
| C3 | recommended | 0 or 20 | ARIA labels and semantic structure correct |
| C4 | recommended | 0 or 20 | Internationalization readiness: RTL support, string externalization, locale-aware formatting |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "All text elements pass minimum contrast ratio of 4.5:1 against background..." },
  "message": "All 24 screens pass WCAG 2.1 AA accessibility audit."
}
```
