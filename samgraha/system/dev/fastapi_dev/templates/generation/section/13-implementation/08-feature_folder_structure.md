## Feature Folder Structure

> *Structural rules: `audit/deterministic/section/13-implementation/08-feature_folder_structure.yaml`*

### Template

> **minimum_content:** 1 file tree
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
This feature is implemented using the standard layered folder structure:

```text
{feature_name}/
├── __init__.py
├── router.py          # FastAPI HTTP routes
├── service.py         # Business logic
├── repository.py      # Data access
├── schemas.py         # Pydantic models
├── models.py          # SQLAlchemy ORM models
├── dependencies.py    # DI provider functions
└── exceptions.py      # Feature-specific exception types
```

[Explain any deviations or additions to this standard structure for this specific feature.]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> The `auth` feature follows the standard layout but adds a `jwt.py` module for token generation specifics.

**Incorrect:**
> All code is in `auth.py`.
> *Why wrong: Violates the standard layered directory structure.*

### Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** file tree blocks
- **Audience:** backend developer
- **Do:** Use the canonical FastAPI feature folder structure.
- **Don't:** Lump all layers into a single file unless explicitly justified as a micro-feature.
