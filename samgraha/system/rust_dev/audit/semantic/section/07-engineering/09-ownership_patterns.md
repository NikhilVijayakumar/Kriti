# Ownership Patterns Rules

This section defines the semantic validation rules for Ownership Patterns documentation.

## Criteria

### `eng-sem-own-001`: Strict Ownership Semantics

**Severity:** error

**Context & Rationale:**
Rust's primary feature is its ownership model. Bypassing it pervasivey leads to runtime overhead and logic errors.

**Audit Check:**
- Does the standard explicitly mandate strict adherence to Rust's ownership and borrowing rules?

**Anti-patterns:**
- Encouraging `clone()` everywhere just to satisfy the compiler.

**Remediation:**
- Mandate passing by value or reference wherever possible.

### `eng-sem-own-002`: Shared Ownership Limitations

**Severity:** error

**Context & Rationale:**
Shared ownership (`Arc`, `Rc`, `Mutex`, `RefCell`) introduces runtime overhead and potential deadlocks.

**Audit Check:**
- Are there strict constraints around using shared ownership primitives?
- Is explicit justification required for their use?

**Anti-patterns:**
- "Just wrap everything in `Arc<Mutex<T>>` if the compiler complains."

**Remediation:**
- Limit shared ownership to specific architectural boundaries (e.g., top-level application state registry).
