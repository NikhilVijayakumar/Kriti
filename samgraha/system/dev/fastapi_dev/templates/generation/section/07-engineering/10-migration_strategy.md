## Migration Strategy

> *Structural rules: `audit/deterministic/section/07-engineering/10-migration_strategy.yaml`*

### Template

> **minimum_content:** 1 paragraph
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
Database schema changes are managed using [Alembic / other tool].

[Describe the workflow for generating, reviewing, and applying migrations.]

## Deployment Constraints

[Describe how migrations are applied during CI/CD (e.g., pre-deployment, backward-compatible only).]
```

**Required subsections:** Deployment Constraints
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Build Standards(03)

### Examples

**Correct:**
> Schema migrations are generated using Alembic. All migrations must be backward-compatible (expand-and-contract pattern) to support zero-downtime deployments. Migrations run automatically during the `pre-deploy` CI step.

**Incorrect:**
> Just run `alembic upgrade head` when you deploy.
> *Why wrong: Doesn't address backward compatibility or CI/CD integration.*

### Writing Guidance

- **Tone:** authoritative
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** backend engineer
- **Do:** Mandate backward-compatible schema changes for zero-downtime.
- **Don't:** Treat migrations as a manual post-deploy step.
