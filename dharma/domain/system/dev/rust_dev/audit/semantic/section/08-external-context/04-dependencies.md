# Dependencies Audit

This section details the Dependencies Audit.

## Version
1.0.0

## Engineering Intent
Dependencies document the external libraries, services, APIs, SDKs, and infrastructure that the system relies on at build time, deploy time, and runtime. They must capture version pinning, license compatibility, upgrade cadence, and end-of-life risk for every dependency.

## Audit Objectives
- All external dependencies are cataloged with versions
- Dependency type is classified (runtime, build-time, dev, test)
- License type is recorded for each dependency
- Upgrade frequency or deprecation date is documented
- Dependency chain (transitive dependencies) is accounted for
- No zombie dependencies (no longer used but still listed)

## Expected Quality
- Versions are pinned (not ranges or "latest")
- License compatibility with project license is verified
- Security vulnerability reporting channel is documented
- Dependency health indicators (maintenance status, community activity) are tracked
- Security patch velocity is assessed: how quickly does each critical dependency ship fixes for CVEs? Dependencies with a patch latency > 90 days for high-severity CVEs are flagged
- "Zombie" dependency definition is operational: a dependency is zombie if it has had no release in 24 months AND has no documented successor or vendored copy

## Red Flags
- Dependency list omits transitive dependencies
- Licensing information is missing or marked "unknown"
- Dependencies on unmaintained or deprecated projects
- Private dependencies without documented ownership
- Dependency version conflicts across subsystems

## Edge Cases
- Dependency with incompatible license detected post-integration
- Internal shared library treated as external dependency
- Dependency used in tests but not deployed with production code
- Two dependencies that conflict at the classloader or linker level

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 25 | All dependencies cataloged with pinned versions |
| C2 | mandatory | 0 or 25 | Dependency type and license recorded |
| C3 | mandatory | 0 or 25 | Runtime vs build-time dependency separation |
| C4 | recommended | 0 or 25 | Upgrade cadence, deprecation tracking, and security patch velocity documented |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "stripe-python v7.8.0, MIT license, runtime" },
  "message": "All 23 dependencies cataloged with pinned versions and license metadata."
}
```
