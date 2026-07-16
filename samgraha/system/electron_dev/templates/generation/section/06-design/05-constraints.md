# Constraints — Generation Template

> **Domain:** design
> **Section:** constraints
> **Source:** `documentation-standards/06-design-standards.md` §Constraints
> **Relationships:** `audit/deterministic/document/06-design-relationships.yaml`

Generate the Constraints section for a Design document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `constrains` | philosophy / guiding_principles | Design Constraints bound what the guiding philosophy can prescribe |

## Template

```markdown
## Constraints

[1 paragraph: how constraints relate to design decisions and what makes them binding]

### [Constraint Category] (e.g. Regulatory, Platform, Organizational)

> **source:** [regulatory body, platform requirement, organizational mandate]
> **enforcement:** [binding / advisory]
> **scope:** [which features or capabilities this applies to]

[1 paragraph: what this constraint requires and why it is binding]

[Repeat for each constraint category — minimum 1]
```

## Examples

**Correct:**
> ### Regulatory
> > **source:** Federal accessibility regulation
> > **enforcement:** binding
> > **scope:** All user-facing interfaces
>
> The product must comply with federal accessibility requirements. All features must be usable by individuals with disabilities. This constraint is non-negotiable and applies regardless of timeline or budget.

**Incorrect:**
> We prefer using a specific CSS framework because the team knows it well and it speeds up development.
> *Why wrong: This is a team preference, not a binding constraint. Constraints must come from regulatory, platform, or organizational mandates and state their binding nature explicitly.*

## Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** State each constraint with its source, enforcement level, and scope. Clearly distinguish binding constraints from advisory guidance. Explain why each constraint is non-negotiable.
- **Don't:** List team preferences as constraints. Omit the source or enforcement level. Conflate platform requirements with organizational preferences.

**Required subsections:** one per constraint category (minimum 1)
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision, Feature Design Standard, Architecture Standard

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
