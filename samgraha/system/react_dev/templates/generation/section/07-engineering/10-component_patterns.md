# Component Patterns — Generation Template

> **Domain:** engineering
> **Section:** component_patterns
> **Source:** `documentation-standards/07-engineering-standards.md` §Component Patterns
> **Relationships:** `audit/deterministic/document/engineering-relationships.yaml`

Generates compound component, render props, HOC, and composition patterns with anti-pattern guidance.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| constrains | feature-technical/component_implementation | Component implementations must follow approved composition patterns |

## Template

```markdown
# Component Patterns

## Compound Components

- Use when a family of components shares internal state or context.
- Provider wraps children; sub-components consume via context.
- Pattern: `Compound.Provider` + `Compound.Item` + `Compound.Trigger`.
- Never expose internal state through props on the parent.

## Render Props

- Use when behavior varies per consumer but structure stays constant.
- Render prop signature: `(state: T) => ReactNode`.
- Place render props as the last prop; never use `children` as render prop.

## Higher-Order Components

- Use only for cross-cutting concerns: logging, auth gating, error boundary.
- HOC naming: `with{Concern}` (e.g. `withAuth`, `withErrorBoundary`).
- HOCs must forward refs and displayName.
- Prefer hooks over HOCs when the concern is stateful.

## Composition Patterns

- Prefer composition over props drilling; pass components as props.
- Slot pattern: components accept `header`, `footer`, `sidebar` props as ReactNode.
- Never mutate props; treat all props as readonly.

## Anti-Patterns

- No `defaultProps` in function components; use destructuring defaults.
- No string refs; use `useRef` or callback refs.
- No inline object/array literals in JSX that cause re-renders.
- No `findDOMNode`; use ref-based DOM access.

**Required subsections:** Compound Components, Render Props, HOCs, Composition
**Optional subsections:** Anti-Patterns, Migration from Class Components
**Required diagrams:** none
**Required cross-references:** component_implementation, code_standards
```

## Examples

**Correct:**
> `Tabs.Provider value={state}><Tabs.List><Tabs.Item>` — compound component with shared context.

**Incorrect:**
> `<Tabs active={activeTab} onChange={setTab}>` — passing state through props instead of context.
> *Why wrong: Compound components share state via context, not prop drilling.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** pattern catalogue with when-to-use guidance
- **Audience:** engineer
- **Do:** Recommend the simplest pattern that fits; prefer hooks before HOCs.
- **Don't:** Allow anti-patterns or default props on function components.

**Required subsections:** Compound Components, Render Props, HOCs, Composition
**Optional subsections:** Anti-Patterns, Migration from Class Components
**Required diagrams:** none
**Required cross-references:** component_implementation, code_standards

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
