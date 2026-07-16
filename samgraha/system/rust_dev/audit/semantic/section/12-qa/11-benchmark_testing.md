# Benchmark Testing Rules

This section defines the semantic validation rules for Benchmark Testing documentation.

## Criteria

### `qa-sem-bench-001`: Automated Performance Regression Detection

**Severity:** warning

**Context & Rationale:**
Systems programming often requires strict performance guarantees.

**Audit Check:**
- Are performance-critical paths continuously benchmarked (e.g., using `criterion`)?
- Are there defined thresholds for failing CI on performance regressions?

**Anti-patterns:**
- "We will test if it feels fast manually."

**Remediation:**
- Mandate statistical and automated benchmarking for critical paths in the CI pipeline.
