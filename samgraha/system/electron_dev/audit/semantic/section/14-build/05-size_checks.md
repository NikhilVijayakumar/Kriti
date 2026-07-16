# Size Checks Audit

This section details the Size Checks Audit.

## Version
1.0.0

## Engineering Intent
Size Checks defines measurable limits on artifact size (bundle, binary, image, package) and what happens when a build crosses them. It exists so bloat is caught by policy, not discovered in production.

## Audit Objectives
- Measurable size limits defined per artifact type
- Measurement method specified (how size is computed, not just "keep it small")
- Enforcement action stated for a limit breach (warn, block, require approval)

## Expected Quality
- Limits given as concrete numbers/thresholds per artifact type, not aspirational language
- Measurement method named specifically (e.g. gzip size, uncompressed, per-chunk)
- Enforcement tied to the CI/CD gate that acts on a breach

## Red Flags
- "Keep the bundle small" with no numeric threshold
- Limits stated without saying what artifact they apply to
- No enforcement action — a breach has no defined consequence

## Edge Cases
- Multi-target builds (web, mobile, embedded) with different budgets per target — each target needs its own limit, not one blanket number
- Legacy artifacts already over budget — acceptable to note a grandfathered exception, but it must be explicit, not silent

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Measurable size limit defined per artifact type |
| C2 | mandatory | 0 or 30 | Measurement method specified |
| C3 | recommended | 0 or 30 | Enforcement action stated for a breach |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.82,
  "severity": "error",
  "evidence": { "section_id": 21, "paragraph_index": 0, "excerpt": "We try to keep the bundle size reasonable." },
  "message": "Size Checks has no measurable limit, only aspirational language."
}
```
