# Guiding Principles Audit

This section details the Guiding Principles Audit.

## Version
1.0.0

## Engineering Intent
Architecture and code should demonstrably follow the project's stated design principles. Principles (modularity, separation of concerns, DRY, YAGNI, least astonishment, etc.) provide the rationale for design decisions and must be consistently applied.

## Audit Objectives
- Design principles are explicitly documented and discoverable
- Code structure reflects the declared architectural patterns
- Principles are applied consistently, not selectively
- Trade-offs between competing principles are documented
- Violations of core principles are flagged and justified

## Expected Quality
- Source tree layout matches architectural layers (UI, business, data)
- No circular dependencies between modules
- Reusable logic is extracted, not duplicated
- Each function or method has a single responsibility
- Magic numbers and strings are named constants

## Red Flags
- God classes or modules with no clear responsibility boundary
- Copy-pasted code blocks exceeding a configurable threshold
- Layer skipping (UI directly accessing data layer)
- Mutually dependent packages in the same layer
- Global mutable state used for cross-cutting concerns

## Edge Cases
- Performance optimisations that deliberately violate DRY
- Legacy modules under migration with grandfathered violations
- Framework-imposed patterns that conflict with project principles
- Auto-generated code that cannot follow project conventions

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | No circular dependencies between modules |
| C2 | mandatory | 0 or 30 | No copy-pasted code above threshold |
| C3 | recommended | 0 or 20 | Layer separation is enforced |
| C4 | recommended | 0 or 20 | No god classes or god modules |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 17, "paragraph_index": 3, "excerpt": "Module A imports B, B imports C, C imports A (circular)." },
  "message": "Circular dependency detected between auth, user, and session modules."
}
```
