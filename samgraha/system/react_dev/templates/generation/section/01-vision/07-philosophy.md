# Philosophy — Generation Template

> **Domain:** vision
> **Section:** philosophy
> **Source:** `documentation-standards/01-vision-standards.md` §Philosophy
> **Relationships:** `audit/deterministic/document/01-vision-relationships.yaml`

Generate the Philosophy section for a Vision document. This section defines the product's core values that guide downstream decisions.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | philosophy / guiding_principles | Philosophy values must inspire the downstream Philosophy document's guiding principles |
| `derives_from` | philosophy / values (self-reference) | Vision's philosophy values and Philosophy's values must be consistent — same product, same identity |

## Template

```markdown
[Statement of the product's core philosophy — the values that guide decisions]

## [Philosophy Value 1]

[One-sentence description of this value and why it matters]

## [Philosophy Value 2]

[One-sentence description of this value and why it matters]

## [Philosophy Value 3]

[One-sentence description of this value and why it matters]
```

## Examples

**Correct:**
> **Clarity Over Cleverness** — Every feature should be immediately understandable to the person using it, even if that means a less elegant implementation.
> **Trust by Default** — Users should never have to wonder whether their data is correct; accuracy is assumed, not requested.

**Incorrect:**
> **Use FastAPI** — The product favors high-performance Python web frameworks.
> **PostgreSQL First** — All persistent data must use PostgreSQL for consistency.
> *Why wrong: States technology preferences rather than guiding values. Philosophy should influence decisions at any abstraction level, not prescribe specific tools.*

## Writing Guidance

- **Tone:** inspirational
- **Voice:** third person
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Express each value as a memorable phrase with a one-sentence rationale; tie each value back to the product's purpose; keep the language abstract enough to survive technology changes
- **Don't:** Name frameworks, databases, or deployment targets; write rules that require specific tools; list more than five values

**Required subsections:** 3-5 philosophy values
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
