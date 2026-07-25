# Non-Goals — Generation Template

> **Domain:** feature-design
> **Section:** non_goals
> **Source:** `documentation-standards/09-feature-design-standards.md` §Non-Goals
> **Relationships:** `audit/deterministic/document/09-feature-design-relationships.yaml`

Generate the Non-Goals section for a Feature Design document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / non_goals | Feature Design non-goals must align with Feature non-goals — same exclusions, design-scoped framing |
| `derives_from` | design / non_goals | Feature Design non-goals must align with Design Documentation non-goals |

## Template

```markdown
### Non-Goals

> **semantic_type:** `non_goals`
> **scope:** ...
> **out_of_scope:** ...
> **contributes:** ...
> **relationships:** ...
> **responsibilities:** ...
> **generation_rules:** ...
> **enhancement_rules:** ...
> **validation_rules:** ...
> **audit_rules:** ...

Feature Design does not define:

* [Responsibility] — owned by [Standard Name]
* [Responsibility] — owned by [Standard Name]
```

## Examples

**Correct:**
> Feature Design does not define:
>
> * Product Vision — owned by Vision(01)
> * Feature Requirements — owned by Feature Specification(04)
> * Database schema for storing user preferences — owned by Architecture(05)
> * API endpoint design — owned by Feature Technical Design(10)

**Incorrect:**
> Feature Design does not define:
>
> * The look and feel of the feature
> * How users navigate the feature
> * What the feature does for users
> * Whether the feature is accessible
> *Why wrong: Every item listed here actually belongs within Feature Design scope (look and feel, navigation, user purpose, accessibility). Non-Goals must only list responsibilities that belong to other standards.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Name the owning standard for each excluded responsibility; list only responsibilities that genuinely belong to other standards; keep the list current as the ecosystem evolves
- **Don't:** Include items that belong in Feature Design scope; list goals or positive scope statements; leave ownership of excluded items ambiguous

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Goals, owning standard for each excluded item

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
