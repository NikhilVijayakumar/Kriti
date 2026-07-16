# Design Principles — Generation Template

> **Domain:** design
> **Section:** design_principles
> **Source:** `documentation-standards/06-design-standards.md` §Design Principles
> **Relationships:** `audit/deterministic/document/06-design-relationships.yaml`

Generate the Design Principles section for a Design document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `guided_by` | philosophy / guiding_principles | Design Principles must align with the product's guiding philosophy |

## Template

```markdown
## Design Principles

[1 paragraph: how design principles anchor the design language and guide decisions]

### [Principle Name] (e.g. Consistency)

> **definition:** [one-sentence definition of this principle]
> **scope:** [which design decisions this applies to]

[1 paragraph: why this principle matters — what it prevents and what it enables]

[1–2 examples: how this principle applies across different features or products]

[Contrast: what violating this principle looks like]

---

[Repeat for each principle — minimum 3]

### Principle Prioritization

[1 paragraph: how to resolve conflicts when principles compete]
```

## Examples

**Correct:**
> ### Consistency
> > **definition:** Every feature uses the same interaction patterns, visual language, and terminology for the same type of action.
> > **scope:** Navigation, feedback, input, error handling, and layout across all features.
>
> Consistency ensures users transfer learning between features. When one feature uses a swipe gesture for deletion, every feature should use the same gesture for the same action. This prevents users from relearning interaction patterns per feature.
>
> *Contrast:* If one feature requires a long-press to delete and another requires a swipe, users must relearn the pattern — eroding trust and increasing cognitive load.

**Incorrect:**
> Consistency means all buttons should use the same CSS class (`btn-primary`) and follow the design tokens defined in the component library's theme configuration.
> *Why wrong: This conflates design consistency (a product-level principle about interaction patterns) with CSS implementation details. Design Principles must describe values and behaviors, not technology-specific styling rules.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** mixed
- **Audience:** new contributor
- **Do:** Define each principle with a one-sentence definition and explicit scope. Include at least one cross-feature example and a contrast showing what violates the principle. Add a Principle Prioritization subsection resolving conflicts between competing principles.
- **Don't:** Reference specific CSS classes, frameworks, or design tokens. Describe feature-specific behavior as a principle. Leave principle conflicts unaddressed or implicitly resolved.

**Required subsections:** one per principle (minimum 3), Principle Prioritization
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision, Philosophy, UX Principles, Feature Design Standard

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
