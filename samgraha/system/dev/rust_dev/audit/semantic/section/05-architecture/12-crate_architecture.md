# Crate Architecture Rules

This section defines the semantic validation rules for Crate Architecture documentation.

## Criteria

### `arch-sem-crate-001`: Strict Crate Boundaries

**Severity:** error

**Context & Rationale:**
Systems engineering in Rust requires strict modularity to manage compilation time and dependency graphs.

**Audit Check:**
- Does the architecture explicitly define distinct boundaries for crates within the workspace?
- Are the responsibilities of each crate clearly defined?

**Anti-patterns:**
- A single monolithic crate with no internal boundaries described.

**Remediation:**
- Explicitly define the workspace crates and their roles (e.g., `core`, `api`, `infra`).

### `arch-sem-crate-002`: Dependency Direction

**Severity:** error

**Context & Rationale:**
Dependencies must point inward toward the core domain.

**Audit Check:**
- Are dependency directions strictly enforced in the documentation?
- Does the documentation explicitly forbid upward or circular crate dependencies?

**Anti-patterns:**
- The `core` crate depends on the `postgres_impl` crate.

**Remediation:**
- State the permitted dependency flow (e.g., infrastructural crates depend on core, never the reverse).
