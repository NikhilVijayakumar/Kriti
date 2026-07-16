# Workflow — Generation Template

> **Domain:** feature-design
> **Section:** workflow
> **Source:** `documentation-standards/09-feature-design-standards.md` §Workflow
> **Relationships:** `audit/deterministic/document/09-feature-design-relationships.yaml`

Generate the Workflow section for a Feature Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | Workflow steps must fulfill the feature's stated requirements |
| `derives_from` | design / workflow | Workflow must apply Design Documentation's workflow principles |

## Template

```markdown
## Workflow

> **semantic_type:** `workflow`
> **scope:** [what workflow concerns this section covers]
> **out_of_scope:** [what workflow concerns are excluded]
> **contributes:** [how this section feeds downstream documents]
> **relationships:** [which upstream documents this derives from]
> **responsibilities:** [what this section is responsible for defining]
> **generation_rules:** [rules for generating this section]
> **enhancement_rules:** [rules for improving this section]
> **validation_rules:** [rules for validating this section]
> **audit_rules:** [rules for auditing this section]

### Primary Workflow

[Step-by-step sequence of user actions and system responses]

1. User does X → System responds with Y
2. User does A → System responds with B
3. ...

### Alternative Workflows

[Branching paths for different user choices or conditions]

### Error Recovery

[What happens and what users can do when a step fails]
```

## Examples

**Correct:**
> **Primary Workflow**
>
> 1. User selects the item to modify → System displays the edit form with current values pre-filled
> 2. User updates one or more fields → System validates each field inline as the user types
> 3. User submits the form → System processes the update and displays a confirmation message with the saved values
>
> **Error Recovery**
>
> If submission fails due to a validation error, the system highlights the invalid fields, displays a message describing the issue, and keeps the user's entered values so they can correct the problem without re-entering data.

**Incorrect:**
> 1. User clicks submit → `handleSubmit()` dispatches an action to the Redux store
> 2. The middleware calls `POST /api/items/:id` with the form payload
> 3. On success, the router navigates to `/items/:id`
> *Why wrong: describes implementation mechanics (Redux, API routes, router navigation) instead of user actions and observable system responses.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Write each step as user action → observable system response; include error recovery paths for every failure point; ensure every functional requirement maps to at least one workflow step
- **Don't:** Describe implementation mechanics or API calls; skip error recovery or branching paths; use function names, class names, or route paths

**Minimum content:** 1 workflow with at least 3 steps
**Length guidance:** moderate
**Required diagrams:** flowchart (primary workflow)
**Required cross-references:** Feature Specification, User Experience

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
