# Async Patterns Rules

This section defines the semantic validation rules for Async Patterns documentation.

## Criteria

### `eng-sem-async-001`: Non-Blocking I/O

**Severity:** error

**Context & Rationale:**
FastAPI is an asynchronous framework. Blocking the event loop degrades throughput across the entire application.

**Audit Check:**
- Does the engineering standard explicitly mandate non-blocking I/O operations?
- Are synchronous libraries (like `requests` or `psycopg2`) forbidden in async contexts?

**Anti-patterns:**
- "We use `requests.get()` inside our FastAPI routes."

**Remediation:**
- Mandate the use of `httpx.AsyncClient` or `aiohttp` for network requests, and async DB drivers (e.g., `asyncpg`).

### `eng-sem-async-002`: Threadpool Offloading

**Severity:** warning

**Context & Rationale:**
Sometimes CPU-bound or legacy sync I/O tasks are unavoidable.

**Audit Check:**
- Is there a defined pattern for offloading blocking tasks to a threadpool (e.g., `run_in_threadpool` or `starlette.concurrency`)?

**Anti-patterns:**
- Running heavy cryptography directly in the async route handler.

**Remediation:**
- Provide guidance on identifying CPU-bound tasks and executing them in worker threads.
