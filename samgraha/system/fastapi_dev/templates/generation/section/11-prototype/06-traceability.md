# Traceability — Generation Template

> **Domain:** prototype
> **Section:** traceability
> **Source:** `documentation-standards/11-prototype-standards.md` §Traceability
> **Relationships:** `audit/deterministic/document/11-prototype-relationships.yaml`

Generate the Traceability section for a Prototype document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `traceable_to` | vision / vision_statement | Prototype traceability must show derivation chain back to Vision |
| `traceable_to` | feature / purpose | Prototype traceability must trace to the Feature being validated |
| `traceable_to` | feature-technical / component_responsibilities | Prototype traceability must trace to the Feature Technical Design being validated |

## Template

```markdown
```text
[Upstream Doc A] ──┐
                    ├──> Prototype ── validates ──> [downstream impact]
[Upstream Doc B] ┘
```
```

## Examples

**Correct:**
> ```text
> Feature Design(09)     ──┐
>                            ├──> Prototype ── validates ──> confidence to proceed with Implementation(13)
> Feature Technical(10)  ──┘
> ```
>
> Both upstream documents are named. The downstream impact — confidence for Implementation — is explicit.

**Incorrect:**
> ```text
> Some Docs ──┐
>              ├──> Prototype ──> ??? 
> More Docs ──┘
> ```
> *Why wrong: Upstream documents are not identified by name or number. The downstream impact is unclear. This diagram could belong to any prototype and provides no traceable lineage.*

## Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** diagrams
- **Audience:** architect
- **Do:** Name each upstream document by title and number in the diagram; show the validation direction from Prototype to downstream impact; keep the diagram minimal with one arrow per relationship
- **Don't:** Use generic labels like "some docs" or "more docs"; omit the downstream impact of the prototype; include unrelated documents or internal section-level traceability

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** traceability flowchart
**Required cross-references:** Feature Design(09), Feature Technical Design(10)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
