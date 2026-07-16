# Future Extensions — Generation Template

> **Domain:** feature
> **Section:** future_extensions
> **Source:** `documentation-standards/04-feature-standards.md` §Future Extensions
> **Relationships:** `audit/deterministic/document/04-feature-relationships.yaml`

Generate the Future Extensions section for a Feature document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| (none section-owned) | — | Future Extensions are internally consistent with current scope — deferred work must not contradict in-scope requirements |

## Template

```markdown
## Future Extensions

> **semantic_type:** `future_extensions`
> **scope:** [Known deferred work for this feature]
> **out_of_scope:** [Current requirements excluded]
> **contributes:** [How this informs downstream planning]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

| Extension | Rationale | Trigger |
|-----------|-----------|---------|
| [Description] | [Why deferred] | [When to revisit] |
```

## Examples

**Correct:**
> | Extension | Rationale | Trigger |
> |-----------|-----------|---------|
> | Multi-directional sync | Current scope limited to one-way transfer to reduce complexity | When bidirectional use cases are validated with users |
> | Incremental sync | Requires a change-detection mechanism not yet designed | When full-sync performance becomes a bottleneck |

**Incorrect:**
> | Extension | Rationale | Trigger |
> |-----------|-----------|---------|
> | Add Redis caching layer | Performance optimization deferred to phase 2 | When database queries exceed 200ms |
> | Implement webhook notifications | User notification feature deferred to backlog | When user feedback requests it |
> *Why wrong: The extensions describe implementation components (Redis caching, webhooks) rather than functional capabilities. These are engineering decisions, not feature-level deferred work.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables
- **Audience:** product owner
- **Do:** Describe deferred work as functional capabilities, not implementation tasks; include a clear rationale for why each item was deferred; specify the triggering condition that would prompt revisiting the item
- **Don't:** List implementation components or technical optimizations as extensions; defer items without a rationale; include current in-scope requirements disguised as future work

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision, Backlog

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
