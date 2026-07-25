# Testing Standards — Generation Template

> **Domain:** engineering
> **Section:** testing_standards
> **Source:** `documentation-standards/07-engineering-standards.md` §Testing Standards
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate the Testing Standards section for an Engineering document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / observability | Testing Standards must derive from architecture's observability requirements |
| `derives_from` | philosophy / guiding_principles | Testing Standards must align with guiding philosophy |

## Template

```markdown
## Testing Standards

> [metadata block]

### Test Types

| Test Type | Purpose | Scope | Tooling | Execution |
|-----------|---------|-------|---------|-----------|
| [Type name] | [what it validates] | [what it covers] | [test runner, assertions] | [when it runs] |

### Coverage Expectations

| Metric | Target | Scope | Rationale |
|--------|--------|-------|-----------|
| [Metric name] | [threshold] | [what it covers] | [why this threshold] |

### Test Tooling

[Optional: test runner, assertion libraries, mocking frameworks]
```

## Examples

**Correct:**
> | Test Type | Purpose | Scope | Tooling | Execution |
> |-----------|---------|-------|---------|-----------|
> | Unit | Validate individual modules | Single module | Vitest | Every commit |
> | Integration | Verify module interactions | Cross-module | Vitest + supertest | Every commit |
> | E2E | Exercise critical user journeys | Full system | Playwright | Nightly |

**Incorrect:**
> We have unit tests and some integration tests. Coverage is pretty good.
> *Why wrong: Vague, no specific test type definitions, no coverage targets, and no rationale for the testing strategy.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Define each test type with its purpose, scope, and tooling; set measurable coverage targets with specific thresholds; document test tooling configuration and rationale.
- **Don't:** Use vague claims like "coverage is pretty good"; omit specific coverage thresholds; describe feature-specific test cases rather than repository-wide test strategy.

**Required subsections:** Test Types, Coverage Expectations
**Optional subsections:** Test Tooling
**Required diagrams:** Test strategy flowchart
**Required cross-references:** Architecture(05), Build Standards

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
