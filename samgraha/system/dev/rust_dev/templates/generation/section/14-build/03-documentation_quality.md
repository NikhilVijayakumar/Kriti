# Documentation Quality — Generation Template

> **Domain:** build
> **Section:** documentation_quality
> **Source:** `documentation-standards/14-build-standards.md` §Documentation Quality
> **Relationships:** `audit/deterministic/document/14-build-relationships.yaml`

Generate the Documentation Quality section for a Build Plan document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | implementation / generation_plan | Documentation quality validates that implementation documentation compiles and passes audit |

## Template

```markdown
## Documentation Quality

[1-2 sentence description of what documentation quality checks cover]
[Statement that this stage is mandatory and gates all downstream stages]

> **Validation scope:** [which documentation domains are validated]
> **Pipeline:** [samgraha audit pipeline reference]
> **Gate behavior:** [failure blocks all downstream stages]
```

## Examples

**Correct:**
> Documentation quality checks validate that all documentation compiles without errors and passes the samgraha audit pipeline. This stage is mandatory and gates all downstream build stages.

**Incorrect:**
> Documentation quality checks verify that README files are written in clear English and follow the project's style guide.
> *Why wrong: Content style and writing quality are out of scope — documentation quality validates structural completeness and audit compliance, not prose style.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Reference the samgraha audit pipeline by name; state that this stage is mandatory and gates all downstream stages; specify what "valid" means in concrete terms
- **Don't:** Describe writing style or prose quality checks; conflate documentation quality with content decisions; omit the mandatory/gating nature of this stage

**Minimum content:** 1 paragraph
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** samgraha audit pipeline

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
