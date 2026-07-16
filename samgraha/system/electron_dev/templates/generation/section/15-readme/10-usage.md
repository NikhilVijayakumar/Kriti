# Usage — Generation Template

> **Domain:** readme
> **Section:** usage
> **Source:** `documentation-standards/15-readme-standards.md` §Usage
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the Usage section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | Usage examples must demonstrate Feature(04) primary functions |

## Template

```markdown
## Usage

### Basic Usage

[Working command examples with expected output]

### Common Workflows

[Typical usage patterns]
```

**Required subsections:** Basic Usage
**Optional subsections:** Common Workflows

## Examples

**Correct:**
> ### Basic Usage
>
> ```bash
> acme-scheduler run --config config.yaml
> # Started scheduler on port 8080
> ```
>
> ### Common Workflows
>
> ```bash
> acme-scheduler status
> # Active pipelines: 3, Completed: 12, Failed: 0
> ```

**Incorrect:**
> The scheduler can be used to run pipelines. It supports many options. Check `--help` for more information.
> *Why wrong: Usage must provide working command examples with expected output demonstrating primary functions, not vague descriptions that require the reader to explore help text.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Provide working command examples with expected output; cover primary functions; show common workflows
- **Don't:** Use vague descriptions like "check --help"; omit expected output; skip primary function examples

**Minimum content:** 1 subsection
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Build, Installation, Configuration

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
