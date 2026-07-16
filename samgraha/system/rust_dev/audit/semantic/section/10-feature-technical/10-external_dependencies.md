# External Dependencies Audit

This section details the External Dependencies Audit.

## Version
1.0.0

## Engineering Intent
External dependencies document all third-party libraries, services, APIs, databases, and infrastructure the feature relies on. This section must capture the dependency name, version, purpose, integration method, and any licensing or operational constraints.

## Audit Objectives
- Every external dependency is listed with its name and version
- The purpose each dependency serves is documented
- Integration method (import, API call, sidecar, plugin) is specified
- License compatibility is verified
- Deprecated or unmaintained dependencies are flagged

## Expected Quality
- Dependencies are grouped by category (runtime, build, test, infra)
- Each dependency has a version constraint (not floating latest)
- Direct vs transitive dependencies are distinguished
- Security advisory status is referenced

## Red Flags
- Missing version information for any dependency
- Undocumented open-source dependencies without license check
- Dependencies pulling in excessive transitive bloat
- Dependencies with known CVEs left unremarked

## Edge Cases
- Platform-provided capabilities mistaken for external dependencies
- Dependencies that are conditionally loaded (feature flags, OS-specific)
- Dual-use dependencies (both internal and external depending on deployment)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All external dependencies enumerated with version |
| C2 | mandatory | 0 or 30 | Integration method documented for each dependency |
| C3 | recommended | 0 or 20 | License compatibility verified |
| C4 | recommended | 0 or 20 | No dependencies with known unresolved CVEs |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 2, "excerpt": "PostgreSQL 16.2 (runtime database)..." },
  "message": "All 9 external dependencies listed with version and integration method."
}
```
