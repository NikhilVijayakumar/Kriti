# Build Standards — Generation Template

> **Domain:** engineering
> **Section:** build_standards
> **Source:** `documentation-standards/07-engineering-standards.md` §Build Standards
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate the Build Standards section for an Engineering document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / operational_readiness | Build Standards must derive from architecture's operational readiness requirements |
| `derives_from` | philosophy / guiding_principles | Build Standards must align with guiding philosophy |

## Template

```markdown
## Build Standards

> [metadata block]

### Build System

[1–2 paragraphs: build tool name and configuration, rationale for choosing this build system]

### Pipeline Stages

> **diagram:** flowchart of pipeline stages

[1 paragraph per stage explaining purpose, inputs, outputs, quality gates]

| Stage | Purpose | Inputs | Outputs | Quality Gate |
|-------|---------|--------|---------|-------------|
| [Stage name] | [what it does] | [what feeds it] | [what it produces] | [pass/fail criteria] |

### Quality Gates

[Optional: criteria that must pass before proceeding]
```

## Examples

**Correct:**
> **Build System:** The repository uses a task runner configured via `build.config.toml`. Each pipeline stage runs in an isolated container to ensure reproducibility. Rationale: deterministic builds ensure that any commit produces the same artifact regardless of the build environment.

**Incorrect:**
> **Build System:** We use Jenkins. Our pipeline is: checkout → build → deploy to staging.
> *Why wrong: Missing rationale, missing quality gates, describes deployment which is out of scope, and does not explain why the pipeline is structured this way.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Document each pipeline stage with purpose, inputs, outputs, and quality gates. Explain the rationale for each stage. Include a pipeline flowchart showing stage ordering.
- **Don't:** Describe deployment or release details that are out of scope. Omit quality gates between stages. List pipeline stages without explaining why they exist.

**Required subsections:** Build System, Pipeline Stages
**Optional subsections:** Quality Gates
**Required diagrams:** Pipeline flowchart
**Required cross-references:** Architecture(05), Testing Standards

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
