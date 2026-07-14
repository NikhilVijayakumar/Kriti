# User Experience — Generation Template

> **Domain:** feature-design
> **Section:** user_experience
> **Source:** `documentation-standards/09-feature-design-standards.md` §User Experience
> **Relationships:** `audit/deterministic/document/09-feature-design-relationships.yaml`

Generate the User Experience section for a Feature Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | UX must fulfill the feature's stated purpose and scope |
| `derives_from` | design / user_experience | UX must apply Design Documentation's interaction principles and UX guidelines |

## Template

```markdown
## User Experience

> **semantic_type:** `user_experience`
> **scope:** [what UX concerns this section covers]
> **out_of_scope:** [what UX concerns are excluded]
> **contributes:** [how this section feeds downstream documents]
> **relationships:** [which upstream documents this derives from]
> **responsibilities:** [what this section is responsible for defining]
> **generation_rules:** [rules for generating this section]
> **enhancement_rules:** [rules for improving this section]
> **validation_rules:** [rules for validating this section]
> **audit_rules:** [rules for auditing this section]

[Introduction: overall UX intent for the feature, derived from Feature Specification]

### Discovery

[How users first encounter and access the feature — entry points, labels, onboarding]

### Primary Interaction

[Core user flow — what users do to accomplish the feature's purpose]

### Feedback and Response

[How the system communicates results of user actions — confirmations, status messages]

### Error Handling

[What users see and can do when something goes wrong — messages, retry options, fallback paths]

### Empty State

[What users see when there is no data or content to display — guidance, next steps]

### Loading State

[What users see while the system is processing — spinners, progress indicators, status text]

### Success State

[What users see when the task completes successfully — confirmation, summary, next actions]

### Accessibility

[How the experience accommodates assistive technologies — screen reader support, keyboard navigation, color contrast]

### Localization

[How the experience adapts for different languages and regions — text expansion, RTL layout, date/number formats]
```

## Examples

**Correct:**
> **Discovery:** Users encounter the feature via a dedicated entry point in the main navigation. The entry point uses a consistent label and icon matching the design system. First-time users see a brief onboarding tooltip.
>
> **Error Handling:** When the feature cannot complete the primary action, users see a clear inline message explaining what went wrong and a specific suggestion for resolution. A retry button is available. No technical error codes are shown to the user.

**Incorrect:**
> The `DataFetchError` component renders when the API call returns a 500 status. It calls `retryRequest()` with exponential backoff (initial delay 1000ms, max 5 retries). The error boundary catches exceptions from the `FeatureController` class.
> *Why wrong: describes implementation internals (API status codes, retry logic, class names) rather than the user-facing experience.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Describe every interaction from the user's perspective; cover all states including error, empty, loading, and success; reference Design Principles that govern the UX
- **Don't:** Reference APIs, frameworks, or component names; describe internal system behavior or processing logic; skip error, empty, or loading states

**Minimum content:** 2 paragraphs plus subsections
**Length guidance:** extensive
**Required diagrams:** flowchart (primary user interaction flow)
**Required cross-references:** Feature Specification, Design Documentation UX Principles

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
