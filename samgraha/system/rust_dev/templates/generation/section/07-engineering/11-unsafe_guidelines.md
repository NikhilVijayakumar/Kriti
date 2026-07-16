# Unsafe Guidelines — Generation Template

> **Domain:** engineering
> **Section:** unsafe_guidelines
> **Source:** `documentation-standards/07-engineering-standards.md` §UnsafeGuidelines
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate the Unsafe Guidelines section for a Engineering document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | philosophy / guiding_principles | Unsafe guidelines strictly follow safety philosophy |

> *Structural rules: `audit/deterministic/section/07-engineering/11-unsafe_guidelines.yaml`*

### Template

> **minimum_content:** 1 paragraph
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
The use of `unsafe` Rust is strictly regulated within this system.

[State the policy for `unsafe` code (e.g., totally forbidden, or allowed only in specific FFI crates with mandatory safety comments).]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> `unsafe` is strictly forbidden in all business logic crates (`#![forbid(unsafe_code)]`). It is only permitted in the `sys_bindings` crate, and every unsafe block must be preceded by a `// SAFETY:` comment explaining why it is sound.

**Incorrect:**
> Use `unsafe` when you need more performance.
> *Why wrong: Dangerous and violates safety guarantees.*

### Writing Guidance

- **Tone:** strict
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** systems engineer
- **Do:** Enforce `#![forbid(unsafe_code)]` by default.
- **Don't:** Leave the `unsafe` policy ambiguous.

> **Generation note:** When generating this section for a specific system, ensure that the output strictly adheres to the provided writing guidance and focuses on the concrete implementation details rather than meta-level documentation standards.

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
