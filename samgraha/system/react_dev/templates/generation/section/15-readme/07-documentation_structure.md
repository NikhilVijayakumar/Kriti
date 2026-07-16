# Documentation Structure — Generation Template

> **Domain:** readme
> **Section:** documentation_structure
> **Source:** `documentation-standards/15-readme-standards.md` §Documentation Structure
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the Documentation Structure section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / system_overview | Documentation Structure must align with Architecture(05) system overview organization |

## Template

```markdown
## Documentation Structure

[List documentation directories and key files]
[Explain the organization principle]
[Provide navigation guidance from README to detailed docs]
```

## Examples

**Correct:**
> Documentation lives under `docs/` organized by standard:
>
> - `docs/raw/vision/` — Project goals and context
> - `docs/raw/features/` — Feature specifications
> - `docs/raw/architecture/` — System design
> - `docs/raw/engineering/` — Implementation standards
>
> Start with the [Documentation Navigation](#documentation-navigation) section below for a guided reading order.

**Incorrect:**
> All documentation is in the docs folder. There is a lot of markdown in there.
> *Why wrong: Documentation Structure must list directories with their purpose and provide navigation guidance, not vague statements about file locations.*

## Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** new contributor
- **Do:** List documentation directories with one-sentence purpose descriptions; provide navigation guidance from README to detailed docs
- **Don't:** Omit directory purposes; list individual files; provide navigation without linking to specific standards

**Minimum content:** 1 subsection
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Documentation Folder, Documentation Navigation, all documentation standards

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
