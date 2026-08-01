# Build Standards Audit

This section details the Build Standards Audit.

## Version
1.0.0

## Engineering Intent
The build pipeline must be reproducible, fast, secure, and produce identical artifacts from the same source. Build scripts are code and must be auditable, versioned, and idempotent.

## Audit Objectives
- Build is reproducible byte-for-byte from version-controlled source
- Reproducibility is verified (not just claimed): a second clean build from the same source produces bit-identical output, or deviations are documented and bounded
- Build scripts do not depend on developer machine state
- Dependencies are pinned to known versions with integrity hashes
- Build fails fast on error (no silent failures)
- Artifacts are immutable and uniquely versioned
- Supply-chain integrity is maintained: base images are pinned by digest, downloaded artifacts are verified against published checksums or signatures

## Expected Quality
- Build definition files (Dockerfile, Makefile, CI config) are present and valid
- No hardcoded absolute paths or credentials in build scripts
- Dependency lockfiles are committed and reviewed
- Build output is excluded from version control
- CI build uses the same steps as local build

## Red Flags
- Unpinned base images (latest tag in Dockerfile)
- Build scripts that download unsigned binaries from the internet
- Secret or credential values visible in build logs
- Build succeeds with warning messages ignored
- Non-reproducible timestamps or build IDs in artifacts

## Edge Cases
- Builds that require proprietary tooling or licenses
- Multi-stage builds with conditional steps per environment
- Builds for multiple target architectures from a single source
- Incremental builds that produce different results than clean builds

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 25 | Build is reproducible from source and reproducibility is verified |
| C2 | mandatory | 0 or 25 | All dependencies are pinned with integrity hashes |
| C3 | recommended | 0 or 25 | No secrets visible in build scripts or logs |
| C4 | recommended | 0 or 25 | Supply-chain integrity: base images pinned by digest, downloaded artifacts verified |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 17, "paragraph_index": 3, "excerpt": "Dockerfile line 5: FROM python:latest (unpinned base image)." },
  "message": "Dockerfile uses unpinned python:latest tag."
}
```
