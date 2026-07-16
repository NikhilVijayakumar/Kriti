# Crate Publishing — Generation Template

> **Domain:** build
> **Section:** crate_publishing
> **Source:** `documentation-standards/14-build-standards.md` §CratePublishing
> **Relationships:** `audit/deterministic/document/14-build-relationships.yaml`

Generate the Crate Publishing section for a Build document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | implementation / crate_folder_structure | Publishing steps depend on workspace layout |

> *Structural rules: `audit/deterministic/section/14-build/10-crate_publishing.yaml`*

### Template

> **minimum_content:** 1 paragraph
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
Internal crates are managed and published according to the system's versioning strategy.

[Detail the CI/CD steps that run `cargo publish --dry-run`, manage workspace dependencies, and handle private registry publishing.]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> CI runs `cargo publish --dry-run` on every PR. On tag, crates are published to our private AWS CodeArtifact registry.

**Incorrect:**
> A developer publishes it from their laptop.
> *Why wrong: Publishing must be automated in the build pipeline.*

### Writing Guidance

- **Tone:** authoritative
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** DevOps engineer
- **Do:** Automate publishing.

> **Generation note:** When generating this section for a specific system, ensure that the output strictly adheres to the provided writing guidance and focuses on the concrete implementation details rather than meta-level documentation standards.

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
