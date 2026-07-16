# Project Name — Generation Template

> **Domain:** readme
> **Section:** project_name
> **Source:** `documentation-standards/15-readme-standards.md` §Project Name
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the Project Name section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | build / versioning_naming | Project Name must match the canonical name in package manifests per Build(14) naming conventions |

## Template

```markdown
## Project Name

[Canonical project name exactly as it appears in package manifests]
```

## Examples

**Correct:**
> Acme Platform

**Incorrect:**
> The Acme Platform is a comprehensive project management solution.
> *Why wrong: Project Name section must state only the canonical name, not a description of the project.*

## Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Use the exact canonical name from package manifests; verify name matches across documentation
- **Don't:** Add descriptions or taglines; abbreviate the name; use marketing or codenames

**Minimum content:** 1 paragraph
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Vision(01), Repository Overview, Documentation Navigation

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
