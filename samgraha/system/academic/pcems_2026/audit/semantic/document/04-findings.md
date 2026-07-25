# Findings Semantic Audit

This section details the Findings Semantic Audit.

## Version
1.0.0

## Engineering Intent
Enforces PCEMS 2026's strict inline media-placement rules, the section's typography spec, and that every performance claim carries a specific empirical anchor.

## Audit Objectives
- Images and tables are placed inline immediately after their first reference, never aggregated at the end of the manuscript; tables use native MS Word table structures; no embedded image contains transparent pixels.
- Section heading is Heading 1 (Arial, 12pt bold); body text is Arial 11pt.
- Every performance claim is accompanied by a specific empirical anchor, never a bare descriptor like "high accuracy".

## Expected Quality
- A reader encounters each figure/table at the exact point it's first discussed, not in an appendix-style block at the end.

## Red Flags
- Figures/tables aggregated at the end of the manuscript.
- Table built as an image or text block instead of a native MS Word table.
- "The model achieved high accuracy." (no metric).

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Images/tables are placed inline immediately after first reference, use native table structures, and contain no transparent-pixel images |
| C2 | mandatory | 0 or 35 | Heading and body typography match spec |
| C3 | mandatory | 0 or 30 | Every performance claim is accompanied by a specific empirical anchor |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.90,
  "severity": "error",
  "evidence": { "excerpt": "Figures 1-6 appear in an appendix after the References section." },
  "message": "Figures aggregated at the end of the manuscript — must be placed inline after first reference."
}
```
