# Evidence Verification Audit (Persona & Forensics)

This section details the Evidence Verification Audit.

## Version
1.0.0

## Engineering Intent
Ensures every claim of "stability", "improvement", "high accuracy", or "robust results" is mathematically or empirically substantiated. This addresses the "Hollow Technical Claim Check" in AI forensics.

## Audit Objectives
- Ensure that subjective performance descriptors are immediately paired with specific numbers (e.g., +8.4% F1, 1,583 unique tokens).
- Verify that architectural justifications are grounded in the specific domain problem (e.g., why a CRF layer is used instead of softmax).
- Flag mechanical algorithm descriptions that simply restate formulas without intuitive reasoning.

## Expected Quality
- Abstract claims are replaced with concrete experimental anchors (Technical DNA).
- Math and algorithm sentences include a "why" clause explaining the choice for this specific implementation.

## Red Flags
- Sentences like "The model achieved high accuracy." (No specific metric provided).
- Sentences like "The Siamese network reduces dimensionality." (Mechanical restatement without intuitive reasoning).
- Unsupported claims of superiority over baselines.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 50 | Every performance claim is accompanied by a specific empirical anchor (Technical DNA) |
| C2 | mandatory | 0 or 50 | Algorithm/math sentences include intuitive reasoning, not just mechanical restatements |

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.90,
  "severity": "error",
  "evidence": { "paragraph_index": 4, "excerpt": "The model achieved high accuracy and significant improvement." },
  "message": "Hollow technical claim detected. Replace 'high accuracy' with specific F1/precision/recall numbers derived from the experimental setup."
}
```
