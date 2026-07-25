# Property Testing — Generation Template

> **Domain:** qa
> **Section:** property_testing
> **Source:** `documentation-standards/12-qa-standards.md` §PropertyTesting
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the Property Testing section for a Qa document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature-technical / crate_implementation | Tests properties derived from the implementation |

> *Structural rules: `audit/deterministic/section/12-qa/10-property_testing.yaml`*

### Template

> **minimum_content:** 1 paragraph
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
Core algorithmic logic and state machines are validated using property-based testing.

[Describe the use of tools like `proptest` or `quickcheck` to fuzz inputs and assert invariants.]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> The parsing logic is tested using `proptest` to ensure that for any arbitrary UTF-8 string input, the parser either succeeds or returns a formatted `ParseError` without panicking.

**Incorrect:**
> We will write a few unit tests.
> *Why wrong: Fails to address property testing invariants.*

### Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** QA engineer
- **Do:** Define invariants that hold true across all generated inputs.

> **Generation note:** When generating this section for a specific system, ensure that the output strictly adheres to the provided writing guidance and focuses on the concrete implementation details rather than meta-level documentation standards.

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
