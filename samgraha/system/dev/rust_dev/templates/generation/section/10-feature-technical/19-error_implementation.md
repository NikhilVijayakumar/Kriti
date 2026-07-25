# Error Implementation — Generation Template

> **Domain:** feature-technical
> **Section:** error_implementation
> **Source:** `documentation-standards/10-feature-technical-standards.md` §ErrorImplementation
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Error Implementation section for a Feature-Technical document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / trait_design | Error types align with interface definitions |

> *Structural rules: `audit/deterministic/section/10-feature-technical/19-error_implementation.yaml`*

### Template

> **minimum_content:** 1 paragraph
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
This feature implements robust error handling using the `Result` type.

[Detail the custom error enum for this feature and how it maps to domain errors. Mention the use of `thiserror` or `anyhow`.]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> The crate defines a `UserError` enum using `thiserror`. All fallible public functions return `Result<T, UserError>`.

**Incorrect:**
> If something fails, the function will panic.
> *Why wrong: Production Rust code must use `Result`, not panics.*

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** Rust developer
- **Do:** Mandate `Result` and explicit error enums.
- **Don't:** Allow `unwrap()` or panics for recoverable errors.

> **Generation note:** When generating this section for a specific system, ensure that the output strictly adheres to the provided writing guidance and focuses on the concrete implementation details rather than meta-level documentation standards.

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
