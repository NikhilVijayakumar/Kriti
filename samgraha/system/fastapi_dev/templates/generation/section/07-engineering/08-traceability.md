# Traceability — Generation Template

> **Domain:** engineering
> **Section:** traceability
> **Source:** `documentation-standards/07-engineering-standards.md` §Traceability
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate the Traceability section for an Engineering document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `traceable_to` | philosophy / guiding_principles | Traceability must connect engineering principles back to guiding philosophy |
| `traceable_to` | architecture / purpose | Traceability must connect engineering documentation to architecture purpose |

## Template

```markdown
## Traceability

> [metadata block]

[1 paragraph stating the non-contradiction constraint and traceability principle]

> **diagram:** flowchart showing derivation chain

### Upstream Sources

[List of upstream documents that feed into Engineering]

### Downstream Consumers

[List of downstream documents that derive from Engineering]
```

## Examples

**Correct:**
> **Upstream Sources:** Architecture(05) provides system-wide design decisions. External Context provides compliance and platform constraints. **Downstream Consumers:** Implementation derives build, test, and code conventions from this document. Feature Technical Design references engineering standards for technology conformance. **Non-contradiction rule:** No downstream document may contradict a standard established here.

**Incorrect:**
> This document traces to Architecture.
> *Why wrong: Missing downstream consumers, no non-contradiction rule, no derivation diagram, and incomplete traceability chain.*

## Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** architect
- **Do:** Include a derivation diagram showing the full chain; list every upstream source and downstream consumer explicitly; state the non-contradiction rule as an enforceable constraint.
- **Don't:** Leave derivation paths implicit or assume they are obvious; omit downstream consumers; use traceability as a summary rather than a verifiable chain.

**Required subsections:** Upstream Sources, Downstream Consumers
**Optional subsections:** none
**Required diagrams:** Derivation chain flowchart
**Required cross-references:** Architecture(05), Feature Technical Design(10), Implementation

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
