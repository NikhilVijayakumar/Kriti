# Limitations Semantic Audit

This section details the Limitations Semantic Audit.

## Version
1.0.0

## Engineering Intent
Ensures Limitations is radically transparent — scalability, generalizability, computational cost, and bias/ethical risks are named specifically, with no claim that the system is perfect or universally applicable.

## Audit Objectives
- Scalability constraints, domain-dependence/generalizability limits, computational cost, and data-bias/ethical risks are each addressed specifically, not generically.
- Zero claims that the system is perfect, complete, or universally applicable without evidence.

## Expected Quality
- Each limitation names a concrete boundary condition, not a hedge like "may not work in all cases".

## Red Flags
- "Our system has no significant limitations."
- A limitation category (scalability, generalizability, cost, bias) is entirely absent.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 70 | Scalability, generalizability, cost, and bias/ethical risks are each addressed specifically, with no claim of universal applicability |
| C2 | recommended | 0 or 30 | Zero informal language or predictable AI transition-word fingerprints |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.80,
  "severity": "error",
  "evidence": { "paragraph_index": 0, "excerpt": "The proposed framework has no significant limitations and generalizes to all domains." },
  "message": "Unsupported universal-applicability claim with no evidence — Limitations must be radically transparent."
}
```
