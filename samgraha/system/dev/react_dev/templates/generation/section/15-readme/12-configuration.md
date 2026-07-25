# Configuration — Generation Template

> **Domain:** readme
> **Section:** configuration
> **Source:** `documentation-standards/15-readme-standards.md` §Configuration
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the Configuration section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | Configuration options must support Feature(04) workflows |

## Template

```markdown
## Configuration

### Environment Variables

| Variable | Default | Description |
| --- | --- | --- |
| [name] | [default] | [purpose] |

### Configuration Files

[List settings files and their purpose]
[State valid values and defaults]
[Provide examples]
```

**Required subsections:** Environment Variables or Configuration Files

## Examples

**Correct:**
> ### Environment Variables
>
> | Variable | Default | Description |
> | --- | --- | --- |
> | `SCHEDULER_PORT` | `8080` | HTTP port for the API server |
> | `SCHEDULER_DB` | `sqlite:///local.db` | Database connection string |
>
> ### Configuration Files
>
> `config.yaml` controls pipeline scheduling behavior. See `config.example.yaml` for a documented reference.

**Incorrect:**
> The config file is in YAML. You can set environment variables too. Change things as needed.
> *Why wrong: Configuration must list specific options with their defaults, valid values, and examples, not vague statements about available configuration mechanisms.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** List configuration options by category; state defaults and valid values; provide working examples for each option
- **Don't:** Omit default values; list internal configuration mechanisms; use vague descriptions without valid value ranges

**Minimum content:** 1 subsection
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Usage, Development, Getting Started

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
