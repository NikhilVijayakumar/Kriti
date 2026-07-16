# Trait Design — Generation Template

> **Domain:** architecture
> **Section:** trait_design
> **Source:** `documentation-standards/05-architecture-standards.md` §TraitDesign
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the Trait Design section for a Architecture document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / crate_architecture | Trait design follows crate boundaries |

> *Structural rules: `audit/deterministic/section/05-architecture/13-trait_design.yaml`*

### Template

> **minimum_content:** 2 paragraphs
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
The system relies on trait-based abstraction to decouple implementation details from business logic.

[Describe the core traits that define the system's external interfaces (e.g., repositories, external services).]

## Generic Constraints

[Explain how generic bounds are used in the core domain to depend on traits rather than concrete types.]
```

**Required subsections:** Generic Constraints
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> The `UserRepository` trait defines the data access contract. The `UserService<R: UserRepository>` struct uses this trait, allowing the Postgres implementation to be injected at runtime.

**Incorrect:**
> The `UserService` uses the `PostgresUserRepository` struct directly.
> *Why wrong: Fails to use trait-based abstraction.*

### Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** systems engineer
- **Do:** Mandate trait usage for all external dependencies.
- **Don't:** Use concrete types in core domain signatures.

> **Generation note:** When generating this section for a specific system, ensure that the output strictly adheres to the provided writing guidance and focuses on the concrete implementation details rather than meta-level documentation standards.

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
