# Build Audit

This section details the Build Audit.

## Version
1.0.0

## Engineering Intent
Build documents how to produce a build artifact from source — prerequisites, exact commands, and where the output lands. Distinct from Installation (getting the published package) and from Engineering's own Build Standards (CI/CD mechanics repo-wide).

## Audit Objectives
- Build prerequisites listed with version numbers
- Specific build commands provided
- Expected output/artifact location described

## Expected Quality
- Prerequisites and Build Commands as distinct subsections
- Commands runnable as shown, not paraphrased
- States where the built artifact ends up

## Red Flags
- "Run the build, it compiles everything" with no actual command
- Missing prerequisite versions
- No mention of where output artifacts land

## Edge Cases
- Multiple build targets (dev vs. release, multiple platforms) — cover the common case fully, list others briefly
- Build requires secrets/credentials not shareable in a public README — state that a credential is required without exposing it

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Build prerequisites listed with versions |
| C2 | mandatory | 0 or 35 | Specific, runnable build commands |
| C3 | recommended | 0 or 30 | Expected output/artifact location described |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.86,
  "severity": "error",
  "evidence": { "section_id": 10, "paragraph_index": 0, "excerpt": "Run the build. It compiles everything and puts the output somewhere in the build directory." },
  "message": "Build section has no specific command and no concrete artifact location."
}
```
