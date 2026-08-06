# Generic Engineering Audit

This section details the Generic Engineering Audit.

## Version
1.0.0

## Engineering Intent
A baseline audit that applies to all engineering artifacts regardless of domain. It checks structural soundness, documentation completeness, naming conventions, and adherence to repository standards.

## Audit Objectives
- Files are well-named and organised by convention
- Code includes appropriate header comments and licensing
- No stale or placeholder content survives in production
- Repository root contains required manifest files
- Language and framework idioms are respected

## Expected Quality
- File names are descriptive and follow project naming conventions
- Every source file starts with a license or project header where required
- No TODO, FIXME, or HACK comments in production code
- README, LICENSE, and CHANGELOG present at repository root
- `.gitignore` excludes build artifacts and secrets

## Red Flags
- Files named `temp.py`, `test123.js`, `untitled.ipynb`
- Placeholder comments ("change this", "your code here")
- Missing license on open-source projects
- Binary artifacts committed to version control
- Inconsistent indentation or line endings within a file

## Edge Cases
- Auto-generated files with machine-names
- Third-party vendored code with different conventions
- Monorepo with mixed-language standards
- Empty files (valid placeholders vs. incomplete work)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All files follow naming convention |
| C2 | mandatory | 0 or 30 | No placeholder comments in production code |
| C3 | recommended | 0 or 20 | Repository root has required manifest files |
| C4 | recommended | 0 or 20 | No build artifacts committed |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 17, "paragraph_index": 3, "excerpt": "File src/utils/temp.py does not follow naming convention." },
  "message": "File src/utils/temp.py: naming convention violation."
}
```
