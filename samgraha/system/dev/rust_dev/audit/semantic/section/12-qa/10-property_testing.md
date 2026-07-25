# Property Testing Rules

This section defines the semantic validation rules for Property Testing documentation.

## Criteria

### `qa-sem-prop-001`: Invariant Validation

**Severity:** warning

**Context & Rationale:**
Property-based testing finds edge cases that manual unit tests often miss by generating arbitrary inputs.

**Audit Check:**
- Are core algorithmic logic and state machines validated using property-based testing tools (e.g., `proptest`, `quickcheck`)?

**Anti-patterns:**
- Relying solely on a few hardcoded example inputs for complex parsers.

**Remediation:**
- Document specific invariants that must hold true across all generated inputs for critical logic.
