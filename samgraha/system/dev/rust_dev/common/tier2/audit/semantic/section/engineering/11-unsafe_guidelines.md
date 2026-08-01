# Unsafe Guidelines Rules

This section defines the semantic validation rules for Unsafe Guidelines documentation.

## Criteria

### `eng-sem-unsafe-001`: Strict Unsafe Policy

**Severity:** critical

**Context & Rationale:**
`unsafe` code bypasses Rust's safety guarantees and can introduce undefined behavior.

**Audit Check:**
- Is the use of `unsafe` Rust strictly regulated or forbidden?
- If allowed, is there a mandatory requirement for `// SAFETY:` comments explaining why the block is sound?

**Anti-patterns:**
- "Use `unsafe` when you need more performance."

**Remediation:**
- Enforce `#![forbid(unsafe_code)]` in all business logic crates, restricting `unsafe` to specific FFI or low-level infrastructural crates.
