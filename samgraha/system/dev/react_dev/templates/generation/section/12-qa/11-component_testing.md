# Component Testing — Generation Template

> **Domain:** qa
> **Section:** component_testing
> **Source:** `documentation-standards/12-qa-standards.md` §Component Testing
> **Relationships:** `audit/deterministic/document/qa-relationships.yaml`

Generates Vitest + Testing Library test patterns with mock conventions, test categories, and assertion guidelines.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| validates | implementation/component_output | Every exported component must have tests |
| references | engineering/code_standards | Must follow project test conventions |

## Template

```markdown
# Component Tests: [ComponentName]

## Test File Co-location

```
components/
  [ComponentName]/
    [ComponentName].test.tsx
    [ComponentName].tsx
    __mocks__/
```

## Mock Conventions

```typescript
vi.mock('@/hooks/useLanguage', () => ({
  useLanguage: () => ({
    t: (key: string) => key,
    locale: 'en',
  }),
}));
```

- [ ] Always mock `useLanguage` in component tests
- [ ] Mock API hooks, never the fetch layer
- [ ] Use `__mocks__/` directory for shared mocks

## Test Categories

### Render Tests
- [ ] Renders without crashing
- [ ] Displays correct default content
- [ ] Applies expected CSS classes

### Interaction Tests
- [ ] Click handlers fire correctly
- [ ] Form submissions validated
- [ ] Keyboard navigation works

### Context Tests
- [ ] Consumes context correctly
- [ ] Handles missing context gracefully
- [ ] Provider wrapping verified

## Assertion Patterns

```typescript
expect(screen.getByRole('button')).toBeInTheDocument();
expect(screen.queryByText('Error')).not.toBeInTheDocument();
```
```

## Examples

**Correct:**
> `SearchInput` has 8 tests: render, placeholder, change handler, submit, keyboard, loading state, error state, and empty state. All mocks use `__mocks__/useLanguage.ts`.

**Incorrect:**
> A component with a single test that only checks `toBeTruthy()` and no interaction or context tests.
> *Why wrong: Insufficient coverage, no interaction testing, no meaningful assertions.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** category-driven
- **Audience:** QA engineer
- **Do:** Mock `useLanguage` always, test all interactive states, use semantic queries.
- **Don't:** Test implementation details, use `getByTestId` first, skip edge case rendering.

**Required subsections:** Test File Co-location, Mock Conventions, Test Categories, Assertion Patterns
**Optional subsections:** Performance Tests, Accessibility Tests
**Required diagrams:** none
**Required cross-references:** implementation/component_output, engineering/code_standards

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
