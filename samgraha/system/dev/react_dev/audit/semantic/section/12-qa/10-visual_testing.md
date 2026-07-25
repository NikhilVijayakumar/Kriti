# Visual Testing Audit

This section details the Visual Testing Audit.

## Version
1.0.0

## Engineering Intent
Visual Testing defines the screenshot testing, Storybook-based visual diff, and CI gate configuration that govern how frontend UI consistency is verified. Good visual testing ensures visual regressions are caught before they reach production.

## Audit Objectives
- Verify screenshot testing is configured
- Confirm Storybook visual diff is set up
- Validate baseline images are stored
- Check CI gates are configured
- Ensure visual testing workflow is documented

## Expected Quality
- Visual tests are automated and run on every PR
- Baselines are managed and version-controlled
- CI gates prevent visual regressions from merging

## Red Flags
- No visual testing configured
- Baselines not stored or outdated
- Visual tests not run in CI
- Manual visual review only

## Edge Cases
- Dynamic content that changes between runs
- Responsive design breakpoints
- Dark mode variants
- Animation testing

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Visual tests exist and are configured for screenshot comparison |
| C2 | mandatory | 0 or 30 | Baseline images are stored and version-controlled |
| C3 | recommended | 0 or 30 | CI gates are configured to block visual regressions |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "example text" },
  "message": "Description of what was found"
}
```
