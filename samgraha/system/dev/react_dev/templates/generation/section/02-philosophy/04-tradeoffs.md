# Trade-offs — Generation Template

> **Domain:** philosophy
> **Section:** tradeoffs
> **Source:** `documentation-standards/02-philosophy-standards.md` §Trade-offs
> **Relationships:** `audit/deterministic/document/02-philosophy-relationships.yaml`

Generate the Trade-offs section for a Philosophy document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / vision_statement | Trade-offs must derive from Vision — what is sacrificed must be consistent with the product's purpose |
| `informs` | architecture / constraints | Trade-offs inform Architecture's constraints — architectural boundaries reflect deliberate value sacrifices |
| `derives_from` | feature / priority | Trade-offs guide Feature prioritization — what the product optimizes for determines which features ship first |

## Template

```markdown
## Trade-offs

### [Trade-off Name 1]

**Chosen:** [What the product deliberately optimizes for.]
**Sacrificed:** [What the product deliberately does not optimize for.]
**Reason:** [Why this trade-off was made — tied to a value or principle.]

### [Trade-off Name 2]

**Chosen:** [What is optimized for.]
**Sacrificed:** [What is given up.]
**Reason:** [Why.]
```

## Examples

**Correct:**
> ### Speed vs. Completeness
>
> **Chosen:** Fast iteration and rapid delivery of working features.
> **Sacrificed:** Comprehensive documentation and exhaustive test coverage at launch.
> **Reason:** Our value of Developer Productivity demands we ship early; documentation and coverage catch up after the feature is validated.

**Incorrect:**
> ### React vs. Vue
>
> **Chosen:** React for the frontend.
> **Sacrificed:** Vue's smaller bundle size.
> **Reason:** The team already knows React so it is faster to build with.
> *Why wrong: Describes a technology selection, not a deliberate trade-off in product values. This belongs in Architecture or Engineering, not Philosophy.*

## Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** tables
- **Audience:** architect
- **Do:** Use the Chosen / Sacrificed / Reason format consistently; tie each trade-off back to a named value; explain the reasoning so downstream standards can cite it
- **Don't:** Describe technology selections as trade-offs; list accidental constraints as deliberate choices; omit the reason or tie it to a named value

**Required subsections:** at least one trade-off per named value
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Values, Principles, Architecture(05)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
