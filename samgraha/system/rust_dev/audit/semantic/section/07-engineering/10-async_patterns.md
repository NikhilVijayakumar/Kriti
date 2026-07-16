# Async Patterns Rules

This section defines the semantic validation rules for Async Patterns documentation.

## Criteria

### `eng-sem-async-001`: Non-Blocking I/O

**Severity:** error

**Context & Rationale:**
Blocking the async event loop degrades throughput across the entire application.

**Audit Check:**
- Does the engineering standard explicitly mandate non-blocking I/O operations using the chosen async runtime (e.g., `tokio`)?

**Anti-patterns:**
- Using `std::thread::sleep` or synchronous HTTP clients in async handlers.

**Remediation:**
- Mandate the use of async equivalents (e.g., `tokio::time::sleep`, `reqwest`).

### `eng-sem-async-002`: Blocking Task Offloading

**Severity:** error

**Context & Rationale:**
CPU-bound tasks will stall the async executor if not handled properly.

**Audit Check:**
- Is there a defined mechanism for offloading CPU-bound tasks?

**Anti-patterns:**
- Running heavy cryptography directly in an async route handler.

**Remediation:**
- Require the use of `tokio::task::spawn_blocking` for CPU-intensive operations.
