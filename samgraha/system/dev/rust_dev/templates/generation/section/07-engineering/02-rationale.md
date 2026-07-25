# Rationale — Generation Template

> **Domain:** engineering
> **Section:** rationale
> **Source:** `documentation-standards/07-engineering-standards.md` §Technology Selection
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate the Technology Selection (Rationale) section for an Engineering document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | philosophy / tradeoffs | Technology rationale must derive from the product's tradeoffs |
| `informs` | engineering / guiding_principles | Technology rationale informs and constrains guiding principles |

## Template

```markdown
## Technology Selection

> [metadata block]

### [Technology Category]

[1 paragraph explaining why this technology was chosen, connected to architectural constraints and external context]

[repeat for each technology category: Language, Framework, Database, Tooling, etc.]
```

## Examples

**Correct:**
> **Language:** Project Alpha uses Rust 1.75+ (edition 2021) because the team values memory safety without garbage collection, the type system catches entire classes of bugs at compile time, and the architecture requires predictable latency with zero-cost abstractions. This choice is constrained by the organization's systems engineering methodology (External Context) and the need for fearless concurrency (Architecture Section 2.1).

**Incorrect:**
> **Language:** Python. **Framework:** Django. **Database:** PostgreSQL.
> *Why wrong: This is a bare list with no rationale, no connection to Architecture or External Context, and no explanation of why these technologies were chosen.*

## Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Connect every technology choice to an architectural constraint or External Context source; explain why each technology was chosen, not just what was chosen; group rationale by engineering concern.
- **Don't:** Present technology choices as bare lists without rationale; justify choices on business or trend grounds rather than engineering grounds; conflate selection rationale with implementation details.

**Required subsections:** One per technology category (Language, Framework, Database, Tooling as applicable)
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Architecture(05), External Context, Constraints

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
