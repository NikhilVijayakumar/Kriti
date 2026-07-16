## API Validation

> *Structural rules: `audit/deterministic/section/14-build/10-api_validation.yaml`*

### Template

> **minimum_content:** 1 paragraph
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
The OpenAPI schema is automatically generated and validated during the build pipeline.

[Detail the CI/CD steps that generate the `openapi.json` from the FastAPI app and validate it against the documented contract to catch breaking changes.]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> The CI pipeline runs `python -c "import app; print(app.openapi())"` to extract the schema and runs `openapi-diff` to ensure no backward-incompatible changes were introduced to the API contract.

**Incorrect:**
> We check the Swagger UI after deployment.
> *Why wrong: API validation must be automated in the build pipeline before deployment.*

### Writing Guidance

- **Tone:** authoritative
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** DevOps engineer
- **Do:** Automate OpenAPI schema validation in CI.
- **Don't:** Rely on manual inspection of Swagger UI.
