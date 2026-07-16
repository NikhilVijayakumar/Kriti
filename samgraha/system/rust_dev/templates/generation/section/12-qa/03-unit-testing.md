# Unit Testing — Generation Template

> **Domain:** qa
> **Section:** unit_testing
> **Source:** `documentation-standards/12-qa-standards.md` §Unit Testing
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the Unit Testing section for a QA document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | engineering / testing_standards | Unit testing conventions must align with Engineering testing standards |

## Template

```markdown
## Unit Testing

### Coverage Targets

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Line coverage | [X%] | [Tool] |
| Branch coverage | [X%] | [Tool] |
| Function coverage | [X%] | [Tool] |

### Conventions

- **Naming:** [pattern, e.g., `test_<unit>_<scenario>_<expected>`]
- **Pattern:** Arrange-Act-Assert
- **One assertion per behavior**
```

## Examples

**Correct:**
> ### Coverage Targets
>
> | Metric | Target | Measurement Method |
> |--------|--------|-------------------|
> | Line coverage | 80% | ProjectNova test runner |
> | Branch coverage | 75% | ProjectNova test runner |
> | Function coverage | 90% | ProjectNova test runner |
>
> ### Conventions
>
> - **Naming:** `test_<unit>_<scenario>_<expected>`
> - **Pattern:** Arrange-Act-Assert
> - **One assertion per behavior**

**Incorrect:**
> Unit tests should cover most of the code. The team writes unit tests for all new features.
> *Why wrong: coverage targets must be measurable with explicit percentages and a defined measurement method.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Specify numeric coverage thresholds per metric; name the measurement tool; define one behavior per test in conventions
- **Don't:** Use qualitative targets like "good coverage"; list frameworks instead of behavioral conventions

**Required subsections:** Coverage Targets table
**Optional subsections:** Conventions
**Required diagrams:** none
**Required cross-references:** Feature(04), Engineering(07)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
