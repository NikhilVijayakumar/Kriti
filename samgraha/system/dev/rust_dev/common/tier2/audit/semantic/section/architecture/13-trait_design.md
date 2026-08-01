# Trait Design Rules

This section defines the semantic validation rules for Trait Design documentation.

## Criteria

### `arch-sem-trait-001`: Trait-Based Abstraction

**Severity:** error

**Context & Rationale:**
Trait-based abstraction decouples implementation details from business logic, enabling testability and modularity.

**Audit Check:**
- Does the system mandate trait usage for all external dependencies (e.g., repositories, external APIs)?

**Anti-patterns:**
- The core business logic structs use concrete implementation types (like `PostgresUserRepository`) directly in their fields.

**Remediation:**
- Document the core traits that define the system's external interfaces.

### `arch-sem-trait-002`: Generic Constraints

**Severity:** warning

**Context & Rationale:**
Rust's generic bounds enforce trait conformance at compile time.

**Audit Check:**
- Is it explained how generic bounds (`<T: Trait>`) are used in the core domain to depend on traits rather than concrete types?

**Anti-patterns:**
- Using `Box<dyn Trait>` everywhere without justification when static dispatch would suffice.

**Remediation:**
- Provide guidance on when to use static dispatch (generics) vs dynamic dispatch (trait objects).
