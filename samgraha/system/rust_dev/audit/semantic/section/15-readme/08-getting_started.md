# Getting Started Audit

This section details the Getting Started Audit.

## Version
1.0.0

## Engineering Intent
Getting Started guides a user from zero to running the project. It must be step-by-step, copy-paste safe, and resolve all dependencies.

## Audit Objectives
- Prerequisites explicitly listed (runtime, package manager, OS)
- Installation commands are accurate and complete
- First run command works without additional config
- Troubleshooting or fallback for common failures
- No skipped steps or assumed knowledge

## Expected Quality
- Prerequisites section with version requirements
- Commands are copy-paste safe (no placeholder confusion)
- Verification step ("you should see...") after key commands
- Cleanup or reset instructions if applicable

## Red Flags
- Missing prerequisites that cause silent failure
- Placeholders not clearly marked (<your-token> vs TOKEN)
- Steps that assume a specific OS without noting it
- Outdated install URLs or package names

## Edge Cases
- Platform-specific instructions (Windows vs macOS vs Linux) missing
- Air-gapped or offline install not handled
- Docker-only setup without native alternative
- Single command list vs. explained steps

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Prerequisites listed with versions |
| C2 | mandatory | 0 or 30 | Copy-paste safe commands |
| C3 | recommended | 0 or 20 | Verification step present |
| C4 | recommended | 0 or 20 | Troubleshooting section included |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 3, "paragraph_index": 1, "excerpt": "Prerequisites: Node.js 18+, pnpm 8+" },
  "message": "Prerequisites listed with version requirements."
}
```
