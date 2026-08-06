# Dependencies Audit

This section details the Dependencies Audit.

## Version
1.0.0

## Engineering Intent
Dependencies enumerate external systems, services, libraries, or teams the feature relies on. They must specify the dependency type, version, interface contract, and failure impact. Good dependency documentation prevents integration surprises and enables resilience planning.

## Audit Objectives
- Every dependency is identified with name and version
- Dependency type is specified (API, library, service, team)
- Interface contract or integration point is documented
- Failure impact of each dependency is assessed
- Dependency lifecycle (install, configure, upgrade) is clear

## Expected Quality
- Dependencies include version constraints
- Integration contracts reference external docs
- Downgrade or fallback behavior is documented
- Dependency status (required, optional, conditional) is noted

## Red Flags
- Dependencies listed without version or source
- Missing failure impact analysis
- Dependencies that are implied but not stated
- Circular or conflicting dependency chains

## Edge Cases
- Empty dependencies section (no external dependencies)
- Shared dependencies with version conflicts
- Deprecated or unmaintained dependencies

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Every dependency has a name and version |
| C2 | mandatory | 0 or 30 | Interface or integration point is documented |
| C3 | recommended | 0 or 30 | Failure impact is assessed for each dependency |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.90,
  "severity": "error",
  "evidence": { "section_id": 11, "paragraph_index": 0, "excerpt": "Auth0 SDK v3.2.1 — OAuth 2.0 / OIDC compliance required." },
  "message": "Dependency identified with name and pinned version."
}
```
