# Code Standards Audit

This section details the Code Standards Audit.

## Version
1.0.0

## Engineering Intent
Code Standards define the coding conventions, style guides, and quality requirements that govern implementation within the engineering domain. Good code standards ensure consistency, maintainability, and adherence to established best practices across all code contributions.

## Audit Objectives
- Verify code standards cover naming conventions, formatting, and file organization
- Ensure language-specific idioms and patterns are documented
- Confirm static analysis and linting requirements are defined
- Validate that review criteria align with stated standards
- Check that code standards address both new code and refactoring

## Expected Quality
- Standards are specific and actionable, not vague preferences
- Examples demonstrate both acceptable and unacceptable patterns
- Tools and automation enforcing standards are referenced
- Exceptions and override processes are documented

## Red Flags
- All style guidance is subjective ("code should be clean") without specifics
- Missing language or framework context for multi-lingual repos
- No mention of automated enforcement or CI integration

## Edge Cases
- Mixed-language projects where standards conflict between languages
- Legacy code exempted from current standards
- Generated code that bypasses normal standards

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Standards document naming conventions and file organization |
| C2 | mandatory | 0 or 30 | Standards reference tooling and automated enforcement |
| C3 | recommended | 0 or 30 | Standards provide examples of acceptable and unacceptable patterns |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "Use PascalCase for public types, camelCase for local variables" },
  "message": "Naming conventions are clearly documented"
}
```
