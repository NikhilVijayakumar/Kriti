# Versioning & Naming — Generation Template

> **Domain:** build
> **Section:** versioning_naming
> **Source:** `documentation-standards/14-build-standards.md` §Versioning & Naming
> **Relationships:** `audit/deterministic/document/14-build-relationships.yaml`

Generate the Versioning & Naming section for a Build Plan document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | engineering / build_standards | Versioning scheme must align with Engineering(07) build standards |

## Template

```markdown
## Versioning & Naming

[1-2 sentence description of what versioning and naming covers]
[Statement that this stage is mandatory and applies to all projects]

> **Version scheme:** [semver | calver]
> **Naming template:** `{name}-{version}.{ext}`
> **Compatibility rules:**
> - **MAJOR:** [when to increment — breaking changes]
> - **MINOR:** [when to increment — backward-compatible features]
> - **PATCH:** [when to increment — backward-compatible fixes]
```

## Examples

**Correct:**
> Artifacts use semantic versioning (MAJOR.MINOR.PATCH). Library artifacts are named `{name}-{version}.{ext}`. Breaking changes increment MAJOR. Compatibility rules: MAJOR bumps require migration guide; MINOR bumps are backward-compatible.

**Incorrect:**
> Artifacts are versioned sequentially (v1, v2, v3) with no naming convention. There are no documented compatibility rules between versions.
> *Why wrong: Sequential versioning without a defined scheme or compatibility rules makes it impossible to determine the impact of an upgrade or maintain multiple versions.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Name the versioning scheme (semver, calver) and when to use each; define the naming template (e.g., `{name}-{version}.{ext}`); document compatibility rules for each version component
- **Don't:** Use ad-hoc or sequential versioning without justification; omit compatibility rules between versions; leave naming conventions implicit

**Minimum content:** 2 paragraphs
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Engineering(07)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
