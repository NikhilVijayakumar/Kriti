## Prototype Endpoints

> *Structural rules: `audit/deterministic/section/11-prototype/03-prototype-endpoints.yaml`*

### Template

> **minimum_content:** 1 endpoint description
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
The following endpoints will be prototyped with static responses:

### [Endpoint Name]

[Method] [Path]
[Describe the static response model and any query parameters supported in the prototype.]
```

**Required subsections:** Endpoint Name
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> ### Get Users
> `GET /api/v1/users`
> Returns a static list of 3 `UserResponse` Pydantic objects. Supports the `?role=admin` filter for testing.

**Incorrect:**
> We will have a mock server running.
> *Why wrong: Lacks specifics about which endpoints are mocked and their contracts.*

### Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** subsections per endpoint
- **Audience:** frontend engineers
- **Do:** Define the exact HTTP method, path, and response schema.
- **Don't:** Rely on generic mock servers; prototype using the actual FastAPI app with mocked returns.
