# Values — Generation Template

> **Domain:** philosophy
> **Section:** values
> **Source:** `documentation-standards/02-philosophy-standards.md` §Values
> **Relationships:** `audit/deterministic/document/02-philosophy-relationships.yaml`

Generate the Values section for a Philosophy document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / vision_statement | Values must derive from Vision's aspirational direction — they express what the product optimizes for |
| `derives_from` | architecture / component_model | Values must guide Architecture's component model — component decisions must reflect prioritized values |
| `derives_from` | design / design_principles | Values must guide Design's principles — design decisions must reflect prioritized values |

## Template

```markdown
## Values

### [Value Name 1]

[One to two sentences naming the value and why it is prioritized.]

[One sentence explaining what this value costs or what it sacrifices.]

### [Value Name 2]

[One to two sentences naming the value and why it is prioritized.]

[One sentence explaining what this value costs or what it sacrifices.]

### [Value Name 3]

[One to two sentences naming the value and why it is prioritized.]

[One sentence explaining what this value costs or what it sacrifices.]
```

## Examples

**Correct:**
> ### Developer Productivity
>
> We optimize for how quickly a developer can understand, modify, and ship a change. Fast iteration beats perfect architecture.
>
> This sometimes means choosing a straightforward solution over a more elegant one that takes longer to implement.

**Incorrect:**
> ### Use TypeScript
>
> We value TypeScript because it catches bugs at compile time and is the industry standard for modern frontend development.
> *Why wrong: Names a specific technology instead of expressing an underlying value. The value is correctness, not a language choice.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** first person plural
- **Structure:** mixed
- **Audience:** product owner
- **Do:** Name the value explicitly in the heading; state what the value costs or what it sacrifices; make trade-offs between values visible so downstream standards can reference them
- **Don't:** Use aspirational platitudes without substance; conflate values with feature priorities; name technologies as values

**Required subsections:** 2-4 named values
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Principles, Vision(01)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
