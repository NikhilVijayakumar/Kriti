# Guiding Principles — Generation Template

> **Domain:** engineering
> **Section:** guiding_principles
> **Source:** `documentation-standards/07-engineering-standards.md` §Engineering Principles
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate the Engineering Principles section for an Engineering document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `guided_by` | philosophy / guiding_principles | Engineering Principles must reflect the product's guiding philosophy |
| `derives_from` | philosophy / rationale | Engineering Principles must derive from the product's rationale |

## Template

```markdown
## Engineering Principles

> [metadata block]

[1 paragraph explaining how principles guide engineering decisions]

[bulleted list of principles, each as a memorable phrase with 1–sentence explanation]
```

## Examples

**Correct:**
> * **Minimal Dependencies:** We prefer fewer external dependencies to reduce maintenance burden and security surface. When a choice exists between a library and a self-contained implementation, the trade-off is evaluated against long-term maintenance cost.
> * **Explicit Configuration:** All configuration must be declared in version-controlled files. Environment-specific overrides use a documented override mechanism, not undocumented runtime state.

**Incorrect:**
> * Use the fastest framework available.
> * Always use the latest version of every library.
> * Write clean code.
> * *Why wrong: Technology-dependent ("fastest framework"), unstable ("latest version"), and vague ("clean code") — none of these survive technology changes or guide engineering decisions when ambiguity arises.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Phrase each principle as a memorable, technology-independent value; ensure every principle is actionable when an engineering decision is ambiguous; keep the total number of principles manageable.
- **Don't:** Use technology-specific language or framework references; state vague platitudes like "write clean code"; add principles that change with technology versions or feature scope.

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Architecture(05), Vision(01)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
