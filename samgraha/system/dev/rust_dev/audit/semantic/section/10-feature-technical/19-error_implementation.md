# Error Implementation Rules

This section defines the semantic validation rules for Error Implementation documentation.

## Criteria

### `ft-sem-err-001`: Robust Error Handling

**Severity:** error

**Context & Rationale:**
Production Rust systems must handle errors gracefully without panicking.

**Audit Check:**
- Is there a custom error enum defined for the feature (e.g., using `thiserror`)?
- Do all fallible public functions return `Result<T, CustomError>`?

**Anti-patterns:**
- "If something fails, the function will panic."
- Pervasive use of `unwrap()` or `expect()`.

**Remediation:**
- Mandate the use of `Result` and explicitly forbid `unwrap()` in production code.
