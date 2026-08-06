# ML Artifact Management Audit

This section details the ML Artifact Management Audit.

## Version
1.0.0

## Engineering Intent
ML Artifact Management defines how models and training data are versioned, tracked, and reproduced. It exists so a model in production can be traced back to the exact data and code that produced it.

## Audit Objectives
- Versioning scheme defined for models and datasets
- Experiment tracking approach specified (what's logged, where)
- Reproducibility requirements stated (can a past model be rebuilt from recorded inputs)

## Expected Quality
- Model and data versioning are addressed as distinct concerns, not conflated
- Experiment tracking names an actual mechanism (tool, convention, or process), not "we keep notes"
- Reproducibility requirement is falsifiable — someone could check whether a past run is actually reproducible

## Red Flags
- Only code is versioned; models/datasets have no versioning scheme at all
- No experiment tracking — results aren't traceable to the run that produced them
- Reproducibility claimed without stating what's captured (seed, data snapshot, environment)

## Edge Cases
- Third-party pretrained models with no versioning control on the source side — state how the pinned version is tracked on this project's side
- Continuously retrained models — versioning scheme must account for rolling updates, not just discrete releases

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Versioning scheme defined for models and data |
| C2 | mandatory | 0 or 30 | Experiment tracking approach specified |
| C3 | recommended | 0 or 30 | Reproducibility requirements stated and falsifiable |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.8,
  "severity": "error",
  "evidence": { "section_id": 22, "paragraph_index": 0, "excerpt": "Models are stored in the models/ folder." },
  "message": "No versioning scheme defined for models — storage location isn't a versioning strategy."
}
```
