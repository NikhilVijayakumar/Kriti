# Abstract Semantic Audit

This section details the Abstract Semantic Audit.

## Version
1.0.0

## Engineering Intent
Verifies the Abstract compresses the whole paper into 150-250 words without resorting to the two failure modes that sink an ESWA desk-review: hollow performance claims and AI-generated prose fingerprints.

## Audit Objectives
- Quantitative Results state exact numerical improvements (e.g., +8.4% F1), never vague descriptors like "high accuracy".
- Zero informal language ("awesome", "easy", "simple", "a lot", "very").
- Low density of predictable AI transition words at sentence starts ("Furthermore", "Moreover", "Additionally").

## Expected Quality
- Every claim of improvement is paired with a specific empirical anchor.
- Writing exhibits burstiness (varied sentence lengths) and an active, direct tone ("We observed...").

## Red Flags
- "The model achieved high accuracy and significant improvement." (no metric).
- Consecutive sentences of near-identical length.
- Over-reliance on sentence-starting transitions.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 50 | Quantitative Results sentence(s) state exact numerical improvements against baselines, not vague descriptors |
| C2 | mandatory | 0 or 30 | Zero informal language and low density of predictable AI transition words |
| C3 | recommended | 0 or 20 | Active voice and varied sentence lengths (burstiness) throughout |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.90,
  "severity": "error",
  "evidence": { "paragraph_index": 0, "excerpt": "The model achieved high accuracy and significant improvement." },
  "message": "Hollow technical claim in Abstract. Replace 'high accuracy' with the specific F1/precision/recall figure from Quantitative Results."
}
```
