# Traceability — Generation Template

> **Domain:** security
> **Section:** traceability
> **Source:** `documentation-standards/03-security-standards.md` §Traceability
> **Relationships:** `audit/deterministic/document/03-security-relationships.yaml`

Generate the Traceability section for a Security document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `traceable_to` | vision / vision_statement | Security derives from Vision — what is being protected follows from what the product is |
| `traceable_to` | philosophy / guiding_principles | Security derives from Philosophy — security principles specialize guiding principles |
| `traceable_to` | architecture / security_considerations | Security guides Architecture — Architecture's Security Considerations realizes it structurally |

## Template

```markdown
Vision, Philosophy
       │
       ↓
   Security (03)
       │
       ├── guides ──> Architecture (05) ── Security Considerations
       ├── guides ──> Engineering (07) ── Security Standards
       └── guides ──> Feature Technical (10) ── Security Considerations

**Non-duplication rule:** Every downstream Security section references this document's threat model, data classification, or principles — it does not restate them.
```

## Examples

**Correct:**
> Vision, Philosophy
>        │
>        ↓
>    Security (03)
>        │
>        ├── guides ──> Architecture (05) ── Security Considerations
>        └── guides ──> Engineering (07) ── Security Standards
>                             │
>                             ↓
>                   Feature Technical (10) ── Security Considerations
>
> Every downstream Security section references this document's threat model, data classification, or principles — it does not restate them.

**Incorrect:**
> Security derives from Architecture's trust-boundary analysis, which feeds Engineering's SAST tooling choices, which then inform the threat model.
> *Why wrong: The derivation chain is inverted — Security must derive from Vision and Philosophy, not from downstream implementation decisions like Architecture or Engineering tooling.*

## Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** diagrams
- **Audience:** new contributor
- **Do:** Show the full derivation chain as a tier diagram; list every downstream domain that consumes Security and how it consumes it; state the non-duplication rule explicitly
- **Don't:** Omit the tier diagram; list downstream domains without explaining their consumption pattern; allow downstream sections to re-derive threat models or data classification independently

**Required subsections:** tier diagram, downstream consumers, non-duplication rule
**Optional subsections:** none
**Required diagrams:** tier derivation chain (flowchart or text diagram)
**Required cross-references:** Vision(01), Philosophy(02), Architecture(05), Engineering(07), Feature Technical(10)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
