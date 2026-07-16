## Development Workflow

> *Structural rules: `audit/deterministic/section/16-product-guide/07-development_workflow.yaml`*

### Template

> **minimum_content:** 1 list of commands
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
To develop within this repository, follow the standard workflow:

### Local Setup

[Provide commands for creating venv, installing dependencies, and setting up the local database.]

### Running Locally

[Provide commands for running the FastAPI dev server (e.g., uvicorn) and accessing Swagger UI.]

### Testing and Linting

[Provide commands for running pytest, black, mypy, and flake8.]
```

**Required subsections:** Local Setup, Running Locally, Testing and Linting
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> Run `uvicorn app.main:app --reload` to start the server. Access documentation at `http://127.0.0.1:8000/docs`.

**Incorrect:**
> Ask a team member how to run the app.
> *Why wrong: The product guide must explicitly document the developer workflow.*

### Writing Guidance

- **Tone:** instructional
- **Voice:** second person ("Run this command")
- **Structure:** code blocks and lists
- **Audience:** new developer
- **Do:** Provide exact, copy-pasteable CLI commands.
- **Don't:** Assume prior knowledge of the project's specific dependency manager or linting toolchain.
