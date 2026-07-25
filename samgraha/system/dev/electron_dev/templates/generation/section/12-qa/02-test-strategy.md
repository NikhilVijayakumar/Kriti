# Test Strategy — Generation Template

> **Domain:** qa
> **Section:** test_strategy
> **Source:** `documentation-standards/12-qa-standards.md` §Test Strategy
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the Test Strategy section for a QA document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / system_overview | Test types must be mapped to the system's architectural profile |

## Template

```markdown
## Test Strategy

| Test Type | Applicability | Priority |
|-----------|--------------|----------|
| Unit Testing | [condition] | Mandatory |
| Integration Testing | [condition] | Mandatory/Conditional |
| End-to-End Testing | [condition] | Conditional |
| Smoke Testing | [condition] | Conditional |
| Load Testing | [condition] | Conditional |
| Scalability Testing | [condition] | Conditional |
| Security Testing | [condition] | Mandatory |

[Paragraph explaining the testing pyramid approach and how test types were selected based on project profile]

**Project Profile:** [description of the system]
```

## Examples

**Correct:**
> | Test Type | Applicability | Priority |
> |-----------|--------------|----------|
> | Unit Testing | All projects | Mandatory |
> | Integration Testing | Multi-component system with 4 services | Mandatory |
> | End-to-End Testing | Application has web UI | Conditional |
> | Smoke Testing | Application is deployed to production | Conditional |
> | Load Testing | Expected 500+ concurrent users | Conditional |
> | Security Testing | All projects | Mandatory |
>
> **Project Profile:** Web application with REST API, background workers, and PostgreSQL database.

**Incorrect:**
> | Test Type | Applicability | Priority |
> |-----------|--------------|----------|
> | Unit Testing | Yes | High |
> | Integration Testing | Yes | High |
>
> We will test everything because all tests are important.
> *Why wrong: applicability must state a condition, not "Yes." Priority must use Mandatory/Conditional.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** tables
- **Audience:** architect
- **Do:** Use the Mandatory/Conditional priority scale consistently; state applicability as a condition; justify each test type by referencing project profile and risk areas
- **Don't:** Use adjectives like "High/Medium/Low"; list test types without applicability conditions

**Required subsections:** Test Type table with Applicability and Priority columns
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Feature(04), Architecture(05), Engineering(07)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
