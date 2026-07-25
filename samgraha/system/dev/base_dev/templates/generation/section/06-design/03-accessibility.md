# Accessibility — Generation Template

> **Domain:** design
> **Section:** accessibility
> **Source:** `documentation-standards/06-design-standards.md` §Accessibility
> **Relationships:** `audit/deterministic/document/06-design-relationships.yaml`

Generate the Accessibility section for a Design document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `guided_by` | philosophy / guiding_principles | Accessibility standards must align with the product's guiding philosophy |

## Template

```markdown
## Accessibility

[1 paragraph: accessibility philosophy and why it matters for this product]

### Compliance Targets

[1 paragraph: applicable standard (e.g. WCAG 2.1 AA), enforcement scope]

### Inclusive Design Principles

[1 principle per subsection — minimum 3, each with rationale and product-level guidance]

### Assistive Technology Support

[1 paragraph: screen readers, keyboard navigation, voice control — product-level guidance]
```

## Examples

**Correct:**
> ### Compliance Targets
> The product targets WCAG 2.1 Level AA conformance across all user-facing interfaces. This applies to every feature with a user interface, including web, mobile, and desktop applications. Exceptions are documented per feature and must receive explicit approval.

**Incorrect:**
> All buttons must include `aria-label="Submit"` and use the `role="button"` attribute to comply with WCAG 2.1 Level AA.
> *Why wrong: This contains component-level ARIA patterns, which belong to Engineering, not Design. Accessibility at the design level should define compliance targets and inclusive design principles, not HTML attribute requirements.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Reference specific compliance standards (e.g. WCAG level) with enforcement scope. Define inclusive design principles at the product level before any technical requirements. State which interfaces the compliance targets apply to.
- **Don't:** Specify component-level ARIA attributes or HTML patterns. Write testing scripts or code snippets. Confuse design-level accessibility with engineering-level implementation details.

**Required subsections:** Compliance Targets, Inclusive Design Principles
**Optional subsections:** Assistive Technology Support, Testing Strategy
**Required diagrams:** none
**Required cross-references:** UX Principles, Feature Design Standard, Engineering Standard

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
