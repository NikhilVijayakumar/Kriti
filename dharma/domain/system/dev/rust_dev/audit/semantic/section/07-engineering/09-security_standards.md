# Security Standards Audit

This section details the Security Standards Audit.

## Version
1.0.0

## Engineering Intent
Engineering security standards govern how code handles secrets, applies cryptography, integrates static and dynamic analysis into the build pipeline, and manages supply-chain risk. Security is enforced at the tooling level, not just through policy. This standard audits whether the build and code practices enforce security by default.

## Audit Objectives
- Secrets management approach is documented (vault, environment variables, sealed secrets — no hardcoded values)
- Cryptographic algorithm selection is documented and follows current guidance (no MD5, SHA-1, DES, ECB mode)
- SAST tool is integrated into CI pipeline with a defined failure threshold
- Dependency vulnerability scanning is integrated (e.g., Dependabot, Snyk, OWASP Dependency-Check)
- Supply-chain integrity measures are present (lockfiles with hashes, signed artifacts)
- Secure coding guidelines are referenced or linked

## Expected Quality
- Secrets rotation policy is documented
- Cryptographic choices include algorithm, key length, and mode
- SAST scan failures block merge (not just advisory)
- Vulnerability scan policy defines severity threshold for blocking (e.g., CVSS ≥ 7.0 blocks)
- Transitive dependency scanning is included, not just direct dependencies

## Red Flags
- Secrets committed to version control (even in non-default branches)
- SHA-1 or MD5 used for integrity or authentication purposes
- SAST tool present but failures are advisory-only with no enforcement
- Dependency scanner not integrated into CI (run ad hoc only)
- No supply-chain verification for downloaded artifacts or base images

## Edge Cases
- Air-gapped environments where SaaS vulnerability databases are unavailable (require mirrored feed)
- Legacy dependencies with known vulnerabilities where no fix exists (require documented risk acceptance)
- Cryptographic code in hardware or embedded context with constrained algorithm support

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Secrets management documented; no hardcoded secrets |
| C2 | mandatory | 0 or 30 | Cryptographic algorithm selection documented and current |
| C3 | recommended | 0 or 20 | SAST and dependency scanning integrated in CI with blocking thresholds |
| C4 | recommended | 0 or 20 | Supply-chain integrity measures present (hashed lockfiles, signed artifacts) |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 8, "paragraph_index": 2, "excerpt": "Password hashing uses MD5." },
  "message": "MD5 is cryptographically broken. Replace with bcrypt, argon2id, or PBKDF2."
}
```
