# Component Implementation — Generation Template

> **Domain:** feature-technical
> **Section:** component_implementation
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Component Implementation
> **Relationships:** `audit/deterministic/document/feature-technical-relationships.yaml`

Generates a component implementation checklist covering props, types, render logic, tests, and Storybook stories.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| derives_from | architecture/component_model | Must follow declared component contracts |
| derives_from | engineering/code_standards | Must comply with coding conventions |

## Template

```markdown
# Component: [ComponentName]

## Implementation Checklist

- [ ] Props interface defined with JSDoc
- [ ] Component types exported from types/
- [ ] Render logic implemented
- [ ] Unit tests passing
- [ ] Storybook stories added
- [ ] Accessibility verified (keyboard, screen reader)
- [ ] Error boundaries wrapped

## Props

```typescript
interface [ComponentName]Props {
  [propName]: [type]; // [description]
}
```

## Hook Implementation

- [ ] Custom hooks extracted to hooks/
- [ ] Hook return types annotated
- [ ] Hook tests written

## State Implementation

- [ ] Context defined in types/
- [ ] Provider wrapping consumer components
- [ ] Consumer components use useContext

## Type Implementation

- [ ] Shared types in types/index.ts
- [ ] Barrel export configured
- [ ] No any types in public API
```

## Examples

**Correct:**
> `FeatureCard` implements `FeatureCardProps`, extracts `useFeatureData` hook, exports from `components/FeatureCard/index.ts`, and has 4 Vitest tests plus 3 Storybook stories covering default, loading, and error states.

**Incorrect:**
> A component with inline type annotations, no extracted hooks, and a single story with no tests.
> *Why wrong: Violates hook extraction rule, missing type exports, insufficient test and story coverage.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** checklist-driven
- **Audience:** engineer
- **Do:** Define every prop type, extract hooks exceeding 15 lines, test all interactive states.
- **Don't:** Use inline styles, skip TypeScript annotations, leave error states unhandled.

**Required subsections:** Implementation Checklist, Props, Hook Implementation, State Implementation, Type Implementation
**Optional subsections:** Edge Cases, Performance Notes
**Required diagrams:** none
**Required cross-references:** architecture/component_model, engineering/code_standards

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
