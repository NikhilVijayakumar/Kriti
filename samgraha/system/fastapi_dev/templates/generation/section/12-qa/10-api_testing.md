## API Testing Strategy

> *Structural rules: `audit/deterministic/section/12-qa/10-api_testing.yaml`*

### Template

> **minimum_content:** 2 paragraphs
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
API endpoints are tested using [Test Client (e.g., httpx)] within the [Test Framework (e.g., pytest)] framework.

[Describe the strategy for fixture generation, database mocking vs test database, and status code assertions.]

## Validation Boundaries

[Specify what must be validated in integration tests (e.g., JSON schema structure, error payloads, auth failures).]
```

**Required subsections:** Validation Boundaries
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> All endpoints are tested using `httpx.AsyncClient`. A clean PostgreSQL test database is spun up per test session. Tests must assert both the HTTP 200 success path and the 422 validation error path.

**Incorrect:**
> We will test the API manually using Postman.
> *Why wrong: Automated API testing via code is required for backend systems.*

### Writing Guidance

- **Tone:** authoritative
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** QA engineer / Backend engineer
- **Do:** Specify the use of programmatic HTTP clients and assertions on response schemas.
- **Don't:** Rely on manual API testing.
