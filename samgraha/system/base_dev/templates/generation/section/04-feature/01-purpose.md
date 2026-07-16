# Purpose — Generation Template

> **Domain:** feature
> **Section:** purpose
> **Source:** `documentation-standards/04-feature-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/04-feature-relationships.yaml`

Generate the Purpose section for a Feature document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / vision_statement | Purpose must trace to Vision — every feature exists because the product's vision demands it |
| `guided_by` | philosophy / guiding_principles | Purpose must be consistent with Philosophy — the feature's value proposition reflects the team's guiding principles |

## Template

```markdown
## Purpose

> **semantic_type:** `purpose`
> **scope:** [Why this feature exists — its role in the product]
> **out_of_scope:** [What this feature does not define]
> **contributes:** [How this section feeds downstream standards]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

[1-2 paragraphs stating what the feature is and why it exists]
```

**Note:** When generating for a specific system, produce system-specific content — what THIS feature does for THIS system — not meta-level language about documentation types. The generation note above (semantic_type, scope, etc.) is structural metadata; the actual content is the paragraph(s) describing the feature's purpose.

## Examples

**Correct:**
> CloudBridge is a data synchronization feature that transfers datasets between distributed storage systems. It exists to ensure data consistency across environments without requiring manual intervention. CloudBridge focuses on the capability of synchronization, not the underlying protocol or transport mechanism.

**Incorrect:**
> CloudBridge is a feature built with Python 3.12 using Apache Kafka for message streaming and PostgreSQL for state tracking. It exists to move data between clusters.
> *Why wrong: The purpose section contains implementation details (Python, Kafka, PostgreSQL) that belong in Engineering Documentation, not Feature Documentation.*

## Writing Guidance

- **Tone:** inspirational
- **Voice:** first person plural
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** State the feature's existence and value in business terms; explain what capability the feature provides to users; keep scope boundaries explicit and clear
- **Don't:** Mention specific technologies, frameworks, or implementation patterns; describe how the feature works internally; include lists of requirements or detailed specifications

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
