# Public Contract — Generation Template

> **Domain:** product-guide
> **Section:** public_contract
> **Source:** `documentation-standards/16-product-guide-standards.md` §Public Contract
> **Relationships:** `audit/deterministic/document/16-product-guide-relationships.yaml`

Generate the Public Contract section for a Product Guide document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| (none) | — | Public Contract documents the shipped product interface — no formal derivation relationships |

## Template

```markdown
## Public Contract

### CLI Interface

| Flag | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `--flag` | string | — | yes | [Description] |

### Inputs

| Input | Type | Description |
|-------|------|-------------|
| [name] | [type] | [Description] |

### Outputs

| Output | Type | Description |
|--------|------|-------------|
| [name] | [type] | [Description] |

### Error Conditions

| Error | Cause | Resolution |
|-------|-------|------------|
| `[error message]` | [What went wrong] | [How to fix it] |
```

**Required subsections:** CLI Interface or Inputs (at least one), Error Conditions
**Optional subsections:** Config Keys, MCP Parameters

## Examples

**Correct:**
> ### CLI Interface
>
> | Flag | Type | Default | Required | Description |
> |------|------|---------|----------|-------------|
> | `--dir` | string | `/data/backups` | no | Target directory for snapshots |
>
> ### Error Conditions
>
> | Error | Cause | Resolution |
> |-------|-------|------------|
> | `Backup directory not writable` | Target directory lacks write permissions | Run `chmod u+w` on the target directory |

**Incorrect:**
> The backup command accepts a directory flag and writes files. Errors may occur if the directory is not writable.
> *Why wrong: No structured tables, missing types/defaults/required status, and error conditions are buried in prose instead of listed with causes and resolutions.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Use structured tables for every parameter, input, output, and error condition; include type, default value, and required/optional status for every flag; list error conditions with a Resolution column the user can act on
- **Don't:** Bury interface details in prose paragraphs; omit type or default information; list error messages without actionable resolutions

**Minimum content:** 1 subsection
**Length guidance:** extensive
**Required diagrams:** none
**Required cross-references:** none

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
