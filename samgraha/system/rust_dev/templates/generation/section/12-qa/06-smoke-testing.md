# Smoke Testing — Generation Template

> **Domain:** qa
> **Section:** smoke_testing
> **Source:** `documentation-standards/12-qa-standards.md` §Smoke Testing
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the Smoke Testing section for a QA document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | implementation | Smoke tests must verify artifacts from Implementation |
| `derives_from` | build | Smoke tests validate Build output |

## Template

```markdown
## Smoke Testing

### Core Functions

- [ ] Application starts successfully
- [ ] [Core function 1] responds correctly
- [ ] [Core function 2] responds correctly
- [ ] Database connectivity verified
- [ ] Authentication endpoint responds

**Maximum execution time:** [X minutes]
**Pass criteria:** All checks pass
**Fail criteria:** Any check fails
```

## Examples

**Correct:**
> ### Core Functions
>
> - [ ] Application starts and responds on port 8080
> - [ ] Health check endpoint returns 200 OK
> - [ ] Database connection pool initializes (max 10 connections)
> - [ ] Authentication endpoint accepts valid credentials
> - [ ] Primary API endpoint returns expected response schema
>
> **Maximum execution time:** 3 minutes
> **Pass criteria:** All checks pass
> **Fail criteria:** Any check fails — block deployment rollback

**Incorrect:**
> Smoke test: make sure the app works. Check that users can log in and the dashboard loads.
> *Why wrong: smoke tests require a structured checklist with pass/fail criteria and a maximum execution time.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Use a checkbox list format; state a maximum execution time in minutes; define pass as "all checks pass" and fail as "any check fails"
- **Don't:** Write as prose narratives; include edge cases or deep functional checks; omit the maximum execution time

**Required subsections:** Core Functions checklist
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Implementation(13), Build(14)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
