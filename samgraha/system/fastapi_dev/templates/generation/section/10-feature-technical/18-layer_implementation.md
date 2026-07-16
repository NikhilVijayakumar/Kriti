## Layer Implementation

> *Structural rules: `audit/deterministic/section/10-feature-technical/18-layer_implementation.yaml`*

### Template

> **minimum_content:** 3 paragraphs
> **length_guidance:** comprehensive
> **diagram_requirements:** none

```markdown
### Router Implementation

[Detail the FastAPI route definitions, dependencies (e.g., `Depends()`), and Pydantic response models.]

### Service Implementation

[Detail the business logic methods, input/output structures, and transaction boundaries.]

### Repository Implementation

[Detail the SQLAlchemy/ORM models and specific queries required.]
```

**Required subsections:** Router Implementation, Service Implementation, Repository Implementation
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Architecture Layered Architecture(12)

### Examples

**Correct:**
> **Router Implementation:** The `POST /users` endpoint uses `Depends(get_db)` to inject the session. It validates input using `UserCreate` Pydantic schema and returns a `UserResponse`.

**Incorrect:**
> The feature will create a user in the database.
> *Why wrong: Doesn't break down the implementation by architectural layers.*

### Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** subsections per layer
- **Audience:** backend developer
- **Do:** Map the implementation directly to the router, service, and repository layers.
- **Don't:** Mix concerns across layers in the description.
