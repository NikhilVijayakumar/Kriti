# Data Classification — Generation Template

> **Domain:** security
> **Section:** data_classification
> **Source:** `documentation-standards/03-security-standards.md` §Data Classification
> **Relationships:** `audit/deterministic/document/03-security-relationships.yaml`

Generate the Data Classification section for a Security document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / vision_statement | Data Classification must derive from Vision — what the product handles determines what data exists |
| `informs` | architecture / data_flow | Data Classification must inform Architecture's data flow — data sensitivity dictates how data moves through the system |
| `traceable_to` | security / threat_model (self) | Data Classification must be traceable to Threat Model — threats are enumerated against classified data |

## Template

```markdown
<!-- Sensitivity Levels: define each level (e.g. Public, Internal, Confidential, Restricted) -->
<!--   For each level: description, one concrete example, handling expectations -->
<!-- Handling Expectations: cross-cutting rules (access control, encryption at rest/transit, retention) -->
<!-- Application: how downstream domains map their data to these levels -->
```

## Examples

**Correct:**
> **Internal:** Data intended for project members only — internal documentation, architecture diagrams, meeting notes.
> **Handling:** Access restricted to authenticated project members; no external sharing without approval.
> **Confidential:** Data whose unauthorized disclosure would cause material harm — user PII, financial records, authentication secrets.
> **Handling:** Encrypted at rest and in transit; access logged and auditable; retention policy enforced.

**Incorrect:**
> Sensitive data goes in PostgreSQL with row-level security. Non-sensitive data goes in Elasticsearch.
> *Why wrong: This classifies data by storage technology rather than by sensitivity level — a new team member reading this cannot determine what "sensitive" means without knowing the infrastructure.*

## Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** tables
- **Audience:** engineer
- **Do:** Provide one concrete example per sensitivity level; state handling expectations (access control, encryption, retention) per level; keep classification technology-independent
- **Don't:** Classify data by storage location or database; embed encryption library or access-control implementation; omit handling expectations for any defined level

**Required subsections:** sensitivity levels, handling expectations
**Optional subsections:** data inventory examples, classification decision tree
**Required diagrams:** none
**Required cross-references:** Threat Model, Security Principles

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
