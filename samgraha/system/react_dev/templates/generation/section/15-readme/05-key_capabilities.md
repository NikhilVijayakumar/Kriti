# Key Capabilities — Generation Template

> **Domain:** readme
> **Section:** key_capabilities
> **Source:** `documentation-standards/15-readme-standards.md` §Key Capabilities
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the Key Capabilities section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | Key Capabilities must summarize Feature(04) capabilities |

## Template

```markdown
## Key Capabilities

- [Capability 1: short descriptive phrase]
- [Capability 2: short descriptive phrase]
- [Capability 3: short descriptive phrase]
<!-- List 3 to 7 capabilities; no implementation details -->
```

## Examples

**Correct:**
> - Declarative pipeline configuration
> - Automatic retry and error recovery
> - Multi-environment deployment support
> - Built-in monitoring and alerting
> - CLI and web interface

**Incorrect:**
> - Uses Celery 5.3.2 with Redis broker
> - Supports Python 3.10, 3.11, and 3.12
> - Has 47 unit tests and 12 integration tests
> - Deploys via Docker Compose or Kubernetes Helm chart
> *Why wrong: Key Capabilities must list high-level capabilities as scannable phrases, not implementation details like library versions, test counts, or deployment mechanisms.*

## Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** product owner
- **Do:** List three to seven capabilities as short descriptive phrases; keep each capability independent and scannable
- **Don't:** Include library versions or test counts; describe deployment mechanisms; use technical jargon or implementation details

**Minimum content:** 1 subsection
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Vision(01) goals, Feature Documentation

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
