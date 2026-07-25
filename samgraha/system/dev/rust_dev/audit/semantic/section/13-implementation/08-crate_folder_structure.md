# Crate Folder Structure Rules

This section defines the semantic validation rules for Crate Folder Structure documentation.

## Criteria

### `impl-sem-folder-001`: Canonical Cargo Layout

**Severity:** error

**Context & Rationale:**
Consistent project structure reduces cognitive load and aligns with Cargo ecosystem conventions.

**Audit Check:**
- Does the implemented folder structure follow standard Cargo conventions (`src/`, `tests/`, `benches/`)?

**Anti-patterns:**
- Lumping all code into a single massive `lib.rs` file.

**Remediation:**
- Enforce a standard, modular folder layout for the crate.
