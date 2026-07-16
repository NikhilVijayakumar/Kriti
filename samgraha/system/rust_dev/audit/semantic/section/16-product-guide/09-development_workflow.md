# Development Workflow Rules

This section defines the semantic validation rules for Development Workflow documentation.

## Criteria

### `pg-sem-flow-001`: Explicit Cargo Commands

**Severity:** error

**Context & Rationale:**
New developers need unambiguous instructions to build and test the project locally.

**Audit Check:**
- Does the guide provide exact, copy-pasteable Cargo commands for building, running, testing, and linting?

**Anti-patterns:**
- "Just figure out how to run the app."

**Remediation:**
- Mandate explicit commands (e.g., `cargo build`, `cargo clippy`, `cargo fmt`).
