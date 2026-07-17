# Tone and Language Verification Audit (Persona & Forensics)

This section details the Tone and Language Verification Audit.

## Version
1.0.0

## Engineering Intent
Verifies that the document maintains the formal, empirical tone required for a PCEMS 2026 submission while avoiding linguistic fingerprints associated with AI generation (e.g., passive voice overuse, hollow precision).

## Audit Objectives
- Ensure terminology is robust, statistically significant, and computationally tractable.
- Prevent informal language ("awesome", "easy", "simple", "a lot", "very").
- Detect and flag AI linguistic fingerprints, including uniform sentence lengths (low burstiness) and predictable transition words at sentence starts ("Furthermore", "Moreover", "Additionally").
- Flag passive voice constructions ("It was observed that...", "The model was trained...").

## Expected Quality
- Writing exhibits burstiness (varied sentence lengths).
- Transitions are smoothly integrated mid-sentence.
- Claims of precision are anchored to specific numbers or architectural choices (Technical DNA).
- The text reads with an active, direct explanation tone ("We observed...").

## Red Flags
- Informal adjectives.
- Consecutive sentences of identical length (clusters of 15-20 words).
- Over-reliance on sentence-starting transitions.
- "Hollow" sentences lacking specific experimental anchors.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Zero instances of informal language |
| C2 | mandatory | 0 or 30 | Low density of predictable AI transition words at sentence starts |
| C3 | recommended | 0 or 30 | Presence of active voice and varied sentence lengths (burstiness) |

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "paragraph_index": 2, "excerpt": "The proposed model is very easy to implement." },
  "message": "Informal language detected: 'very easy'. Replace with 'computationally tractable' or 'straightforward'."
}
```
