# Crate Implementation — Generation Template

> **Domain:** feature-technical
> **Section:** crate_implementation
> **Source:** `documentation-standards/10-feature-technical-standards.md` §CrateImplementation
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Crate Implementation section for a Feature-Technical document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / crate_architecture | Implements the specified crate boundaries |
| `guided_by` | engineering / ownership_patterns | Follows memory management rules |
| `guided_by` | engineering / unsafe_guidelines | Applies safety restrictions |

> *Structural rules: `audit/deterministic/section/10-feature-technical/18-crate_implementation.yaml`*

### Template

> **minimum_content:** 2 paragraphs
> **length_guidance:** comprehensive
> **diagram_requirements:** none

```markdown
### Module Structure

[Detail the internal module tree (`mod foo;`) for the feature's crate.]

### Trait Definitions

[List the specific traits defined or implemented by this feature.]

### Core Structs

[List the core data structures and their ownership semantics.]
```

**Required subsections:** Module Structure, Trait Definitions, Core Structs
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Architecture Crate Architecture(12)

### Examples

**Correct:**
> **Trait Definitions:** Implements `MessagePublisher` for `KafkaPublisher`.
> **Core Structs:** Defines `PublishConfig` which owns its strings.

**Incorrect:**
> We will write the code in `main.rs`.
> *Why wrong: Does not decompose the implementation.*

### Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** subsections
- **Audience:** Rust developer
- **Do:** Be specific about modules, traits, and structs.

> **Generation note:** When generating this section for a specific system, ensure that the output strictly adheres to the provided writing guidance and focuses on the concrete implementation details rather than meta-level documentation standards.

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
