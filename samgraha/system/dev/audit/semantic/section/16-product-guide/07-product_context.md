# Product Context Audit

This section details the Product Context Audit.

## Version
1.0.0

## Engineering Intent
Product Context states the prerequisites, default behavior, and version-specific context a reader needs before using a feature — grounding the guide in what's actually true for this product version, not generic assumptions.

## Audit Objectives
- Prerequisites listed explicitly (what must already be installed/configured)
- Default behavior stated (what happens without explicit configuration)
- Version-specific context noted where behavior differs across versions

## Expected Quality
- Prerequisites, default behavior, and version notes are each addressed, not merged into vague prose
- Defaults are concrete and checkable, not "sensible defaults are used"
- Version notes name the version where behavior changed

## Red Flags
- Reads as marketing copy ("this useful feature has been improved many times") instead of stating prerequisites/defaults/version context
- Default behavior left unstated — reader can't tell what happens without configuration
- Version-specific caveats omitted where the feature is known to have changed

## Edge Cases
- Feature with no meaningful prerequisites (works out of the box) — state that explicitly rather than omitting the subsection
- Product with no version-specific behavior differences yet — acceptable to note "no version-specific behavior at this time" rather than silence

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Prerequisites explicitly listed |
| C2 | mandatory | 0 or 30 | Default behavior stated concretely |
| C3 | recommended | 0 or 30 | Version-specific context noted where applicable |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.82,
  "severity": "error",
  "evidence": { "section_id": 61, "paragraph_index": 0, "excerpt": "Backup is a useful feature that helps protect your data." },
  "message": "Product Context reads as marketing copy — no prerequisites or default behavior stated."
}
```
