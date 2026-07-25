# UX Principles — Generation Template

> **Domain:** design
> **Section:** ux_principles
> **Source:** `documentation-standards/06-design-standards.md` §UX Principles
> **Relationships:** `audit/deterministic/document/06-design-relationships.yaml`

Generate the UX Principles section for a Design document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `guided_by` | philosophy / guiding_principles | UX Principles must reflect the product's guiding philosophy |

## Template

```markdown
## UX Principles

[1 paragraph: how UX principles connect to the product's design philosophy and why they govern interaction decisions across all features]

### [Principle Name]

[1 paragraph: what this principle means at the product level — how it shapes user interaction across all features]

[1 cross-feature example: how this principle applies across at least two different features, showing consistency]

---

[Repeat for each principle — minimum 3]
```

## Examples

**Correct:**
> ### Feedback Visibility
> Users should always receive immediate, clear feedback when they perform an action. Whether submitting a form, navigating to a new view, or encountering an error, the system confirms the action occurred and indicates the result.
>
> When a user submits a support ticket, they see a confirmation toast and are redirected to the ticket detail view. When a user updates their profile settings, the same confirmation pattern applies. This ensures users never wonder whether their action succeeded.

**Incorrect:**
> When the user clicks the "Submit" button in React, the onClick handler should call the API endpoint and display a Material UI Snackbar component with the success message.
> *Why wrong: This is technology-specific implementation guidance (React, Material UI, Snackbar) rather than a product-level UX principle. UX principles must describe interaction philosophy, not component choices.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** mixed
- **Audience:** product owner
- **Do:** Frame each principle as a product-level interaction philosophy applicable across all features. Provide at least one cross-feature example per principle. Ground each principle in user outcomes, not UI mechanics. Minimum 3 principles.
- **Don't:** Reference specific UI frameworks, libraries, or component names. Describe feature-specific interaction workflows. Conflate UX principles with visual design specifications. Leave principles without examples or scope.

**Required subsections:** one per principle (minimum 3)
**Optional subsections:** Interaction Patterns, Navigation Philosophy, Feedback Mechanisms
**Required diagrams:** none
**Required cross-references:** Design Principles, Accessibility

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
