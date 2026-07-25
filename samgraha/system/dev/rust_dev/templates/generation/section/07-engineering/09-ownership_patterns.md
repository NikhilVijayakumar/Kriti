# Ownership Patterns — Generation Template

> **Domain:** engineering
> **Section:** ownership_patterns
> **Source:** `documentation-standards/07-engineering-standards.md` §OwnershipPatterns
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate the Ownership Patterns section for a Engineering document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | philosophy / guiding_principles | Ownership patterns enforce engineering philosophy |

> *Structural rules: `audit/deterministic/section/07-engineering/09-ownership_patterns.yaml`*

### Template

> **minimum_content:** 2 paragraphs
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
This system strictly enforces Rust's ownership semantics to guarantee memory safety and thread safety.

[Describe the general approach to ownership, borrowing, and lifetimes within the system.]

## Shared Ownership Limitations

[Specify the constraints around using `Rc`, `Arc`, `RefCell`, and `Mutex`. Require explicit justification for their use.]
```

**Required subsections:** Shared Ownership Limitations
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> Data is passed by value or reference wherever possible. `Arc<Mutex<T>>` is strictly limited to the top-level application state registry.

**Incorrect:**
> Just wrap everything in `Arc<Mutex<T>>` if the compiler complains.
> *Why wrong: Violates explicit ownership principles and incurs runtime overhead/deadlock risks.*

### Writing Guidance

- **Tone:** authoritative
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** systems engineer
- **Do:** Prefer strict lifetimes and borrowing.
- **Don't:** Allow pervasive shared ownership.

> **Generation note:** When generating this section for a specific system, ensure that the output strictly adheres to the provided writing guidance and focuses on the concrete implementation details rather than meta-level documentation standards.

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
