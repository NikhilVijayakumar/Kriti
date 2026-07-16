# Principles — Generation Template

> **Domain:** philosophy
> **Section:** guiding_principles
> **Source:** `documentation-standards/02-philosophy-standards.md` §Principles
> **Relationships:** `audit/deterministic/document/02-philosophy-relationships.yaml`

Generate the Principles section for a Philosophy document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / vision_statement | Principles must derive from Vision's aspirational direction — they operationalize vision into decision rules |
| `derives_from` | architecture / purpose | Principles must guide Architecture's purpose — architectural decisions must be evaluable against these principles |
| `derives_from` | design / purpose | Principles must guide Design's purpose — design decisions must be evaluable against these principles |
| `derives_from` | engineering / purpose | Principles must guide Engineering's purpose — engineering decisions must be evaluable against these principles |

## Template

```markdown
## Principles

### [Principle Name 1]

[One to two sentences stating the principle as a stable, technology-independent decision rule.]

[One example of how this principle resolves an ambiguous decision.]

### [Principle Name 2]

[One to two sentences stating the principle.]

[One example of application.]

### [Principle Name 3]

[One to two sentences stating the principle.]

[One example of application.]
```

## Examples

**Correct:**
> ### Simplicity First
>
> When two designs solve the same problem, choose the simpler one. Complexity is a cost, not a feature.
>
> If adding a framework means the team must learn a new paradigm, it must clearly reduce complexity in the rest of the system to justify itself.

**Incorrect:**
> ### Use REST Over GraphQL
>
> We prefer REST because it is easier to implement with Express.js and integrates well with our React frontend.
> *Why wrong: Technology-specific — names concrete frameworks and technologies instead of expressing a stable, technology-independent decision rule.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** architect
- **Do:** State each principle as a decision rule that resolves ambiguity; include a concrete example of the principle in action; keep phrasing memorable enough to cite in Architecture or Design
- **Don't:** Name specific frameworks, languages, or libraries; write principles as aspirations without a decision outcome; list more than five principles

**Required subsections:** 3-5 named principles
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Values, Vision(01)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
