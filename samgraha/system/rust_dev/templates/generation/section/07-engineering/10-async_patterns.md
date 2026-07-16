# Async Patterns — Generation Template

> **Domain:** engineering
> **Section:** async_patterns
> **Source:** `documentation-standards/07-engineering-standards.md` §AsyncPatterns
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate the Async Patterns section for a Engineering document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | philosophy / guiding_principles | Async patterns follow performance guidelines |

> *Structural rules: `audit/deterministic/section/07-engineering/10-async_patterns.yaml`*

### Template

> **minimum_content:** 1 paragraph
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
The system utilizes [tokio / async-std] as the asynchronous runtime.

[Describe how async/await is used for I/O bounds, and how blocking operations are handled.]

## Blocking Task Offloading

[Detail the mechanism for offloading CPU-bound tasks (e.g., `tokio::task::spawn_blocking`).]
```

**Required subsections:** Blocking Task Offloading
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> All database and network calls use async functions. Cryptographic hashing is offloaded using `tokio::task::spawn_blocking` to prevent starving the executor.

**Incorrect:**
> We call `std::thread::sleep` in our async handlers.
> *Why wrong: Blocks the async executor.*

### Writing Guidance

- **Tone:** authoritative
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** systems engineer
- **Do:** Mandate non-blocking I/O.
- **Don't:** Mix sync and async I/O indiscriminately.

> **Generation note:** When generating this section for a specific system, ensure that the output strictly adheres to the provided writing guidance and focuses on the concrete implementation details rather than meta-level documentation standards.

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
