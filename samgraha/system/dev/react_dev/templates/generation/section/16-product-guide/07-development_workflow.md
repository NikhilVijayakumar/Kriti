# Development Workflow — Generation Template

> **Domain:** product-guide
> **Section:** development_workflow
> **Source:** `documentation-standards/16-product-guide-standards.md` §Development Workflow
> **Relationships:** `audit/deterministic/document/product-guide-relationships.yaml`

Generates the team development workflow covering branching, component development, review, and merge processes.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| references | engineering/code_standards | All code must comply with standards before merge |
| references | design/design_tokens | Components must use design tokens, not hardcoded values |

## Template

```markdown
# Development Workflow: [TeamName]

## Feature Branch Workflow

1. `git checkout -b feature/[TicketID]-[short-description]`
2. Create component in `features/[FeatureName]/`
3. Write tests co-located with component
4. Add Storybook stories
5. Open PR with description template
6. Address review comments
7. Squash merge after approval

## Component Development Workflow

1. Define props interface from design spec
2. Implement component with design tokens
3. Write render, interaction, and context tests
4. Add Storybook stories (default, loading, error, empty)
5. Run `npm run test` and `npm run lint`
6. Request visual review in Storybook
7. Request code review

## Design Token Contribution

- [ ] Use tokens from `design/tokens/` directory
- [ ] Do not hardcode colors, spacing, or typography
- [ ] Propose new tokens via design review

## Storybook Documentation

- [ ] Every component has a story file
- [ ] Stories cover all prop variants
- [ ] MDX docs page with usage examples
- [ ] Accessibility annotations included

## A11y Review Checklist

- [ ] Keyboard navigation: tab order correct
- [ ] Screen reader: all interactive elements labeled
- [ ] Color contrast: WCAG AA minimum
- [ ] Focus indicators: visible on all focusable elements
- [ ] Reduced motion: animations respect prefers-reduced-motion
```

## Examples

**Correct:**
> Engineer creates `feature/TICKET-123-user-search/`, implements `SearchBar` with design tokens, writes 6 tests, adds 4 stories, and opens PR with Storybook preview link for visual review.

**Incorrect:**
> Engineer commits directly to `main`, uses hardcoded `#333` color, has no tests, and no Storybook stories.
> *Why wrong: No branching strategy, hardcoded values bypass tokens, missing test and story coverage.*

## Writing Guidance

- **Tone:** instructional
- **Voice:** imperative
- **Structure:** process-driven
- **Audience:** developer
- **Do:** Follow branch naming conventions, always use design tokens, document every component in Storybook.
- **Don't:** Commit directly to main, hardcode design values, skip a11y review.

**Required subsections:** Feature Branch Workflow, Component Development Workflow, Design Token Contribution, Storybook Documentation, A11y Review Checklist
**Optional subsections:** Release Process, Hotfix Workflow
**Required diagrams:** workflow diagram
**Required cross-references:** engineering/code_standards, design/design_tokens

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
