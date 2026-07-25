# Dependencies — Generation Template

> **Domain:** feature
> **Section:** dependencies
> **Source:** `documentation-standards/04-feature-standards.md` §Dependencies
> **Relationships:** `audit/deterministic/document/04-feature-relationships.yaml`

Generate the Dependencies section for a Feature document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| (none section-owned) | — | Dependencies list other features or systems; they are internally consistent with Functional Requirements |

## Template

```markdown
## Dependencies

> **semantic_type:** `dependencies`
> **scope:** [Features or systems this feature relies on]
> **out_of_scope:** [Implementation dependencies excluded]
> **contributes:** [How this feeds downstream design]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

| Dependency | Nature | Required |
|------------|--------|----------|
| [Feature/System Name] | [functional \| data] | [yes \| no] |
```

## Examples

**Correct:**
> | Dependency | Nature | Required |
> |------------|--------|----------|
> | User Authentication | functional | yes |
> | Data Encryption | functional | yes |
> | Audit Logging | data | no |

**Incorrect:**
> | Dependency | Nature | Required |
> |------------|--------|----------|
> | Spring Security | functional | yes |
> | Apache Kafka 3.4 | data | yes |
> | Redis 7.0 Cache | functional | no |
> *Why wrong: The dependency column lists specific software libraries and version numbers rather than the feature or system capabilities the feature relies on. These are implementation dependencies.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** architect
- **Do:** List each dependency by feature or system name; specify whether the dependency is functional or data-related; indicate whether each dependency is required or optional
- **Don't:** List software libraries, frameworks, or version-specific packages; include build dependencies or toolchain requirements; omit the nature or criticality of each dependency

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Other Feature documents, External Context

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
