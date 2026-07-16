# Traceability — Generation Template

> **Domain:** feature
> **Section:** traceability
> **Source:** `documentation-standards/04-feature-standards.md` §Traceability
> **Relationships:** `audit/deterministic/document/04-feature-relationships.yaml`

Generate the Traceability section for a Feature document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `traceable_to` | vision / vision_statement | Feature traceability must show derivation from Vision — every feature supports the documented Vision |

## Template

```markdown
Feature Documentation should remain traceable.

```text
Vision → Feature → Feature Design → Architecture → Feature Technical Design → Engineering → Implementation
```

Every feature should support the documented Vision.
```

## Examples

**Correct:**
> Feature Documentation should remain traceable.
>
> ```text
> Vision → Feature → Feature Design → Architecture → Feature Technical Design → Engineering → Implementation
> ```
>
> CloudBridge derives from the Vision goal of "automated data consistency across environments." Its Feature Design and Architecture must not contradict this intent.

**Incorrect:**
> Feature Documentation should remain traceable.
>
> CloudBridge uses Python 3.12 with FastAPI and connects to PostgreSQL. The implementation uses a message queue pattern.
> *Why wrong: This section presents an implementation summary rather than showing the derivation chain from Vision to downstream standards. It contains technology choices that violate the traceability section's purpose.*

## Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** diagrams
- **Audience:** new contributor
- **Do:** Include the tier model diagram showing Vision through Implementation; name which downstream standards derive from Features; state the non-contradiction rule
- **Don't:** Present an implementation summary or technology stack overview; describe how individual features are coded; omit the derivation chain

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** flowchart (tier model)
**Required cross-references:** Vision, all downstream standards

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
