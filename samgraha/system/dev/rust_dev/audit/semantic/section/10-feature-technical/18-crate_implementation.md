# Crate Implementation Rules

This section defines the semantic validation rules for Crate Implementation documentation.

## Criteria

### `ft-sem-crate-001`: Module and Trait Specificity

**Severity:** error

**Context & Rationale:**
A technical design must provide sufficient detail for implementation without ambiguity.

**Audit Check:**
- Does the technical design detail the internal module tree (`mod foo;`)?
- Are the specific traits and core structs (along with their ownership semantics) explicitly listed?

**Anti-patterns:**
- "We will write the code in `main.rs`."

**Remediation:**
- Require explicit definition of modules, traits, and core structs before implementation begins.
