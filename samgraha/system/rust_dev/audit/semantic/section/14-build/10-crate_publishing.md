# Crate Publishing Rules

This section defines the semantic validation rules for Crate Publishing documentation.

## Criteria

### `build-sem-pub-001`: Automated Publishing

**Severity:** error

**Context & Rationale:**
Manual publishing introduces human error and security risks.

**Audit Check:**
- Are crate publishing steps (including `cargo publish --dry-run`) automated in the CI/CD pipeline?

**Anti-patterns:**
- A developer publishes crates manually from their laptop.

**Remediation:**
- Document the automated pipeline for publishing to public or private registries.
