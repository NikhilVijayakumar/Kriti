# State Management — Generation Template

> **Domain:** engineering
> **Section:** state_management
> **Source:** `documentation-standards/07-engineering-standards.md` §State Management
> **Relationships:** `audit/deterministic/document/engineering-relationships.yaml`

Generates Context + useState patterns, cross-cutting state providers, and props-down conventions.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| constrains | feature-technical/component_implementation | All state management must use Context + useState; no external libraries |

## Template

```markdown
# State Management

## Context Creation Pattern

- Create context in a dedicated file: `contexts/{Domain}Context.ts`.
- Export a typed context with `createContext<Use{Name}Return | null>(null)`.
- Always provide a custom hook `use{Name}Context()` that throws if null.

## Provider Pattern

- Provider component owns state via `useState` or composed hooks.
- Provider accepts `children` only; never accept state as props.
- Memoize provider value with `useMemo` to prevent unnecessary re-renders.
- Nest providers by domain: `<AuthProvider><ThemeProvider>`.

## Consumer Hook Pattern

- Consumers use `use{Name}Context()` to access shared state.
- Never pass context value through intermediate components.
- Derived state computes in the consumer, not the provider.

## Local State Convention

- Use `useState` for component-local state not shared outside the component.
- Lift state to the nearest common ancestor when two siblings need it.
- Cross-cutting state moves to a dedicated Context provider.

## Props-Down Convention

- Data flows top-down via props; events flow bottom-up via callbacks.
- Never mutate props; create new state from old state immutably.
- No external state libraries; Context + useState covers all cases.

**Required subsections:** Context Creation, Provider, Consumer Hook, Local State, Props-Down
**Optional subsections:** Performance Patterns, Debugging State
**Required diagrams:** none
**Required cross-references:** component_implementation, code_standards
```

## Examples

**Correct:**
> `const AuthProvider = ({ children }) => { const [user, setUser] = useState(null); return <AuthContext.Provider value={useMemo(() => ({ user, setUser }), [user])}>{children}</AuthContext.Provider>; };`

**Incorrect:**
> `const store = createStore(reducer);` — external state library violates Context + useState mandate.
> *Why wrong: External state libraries are prohibited; use Context + useState exclusively.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** layered patterns from creation to consumption
- **Audience:** engineer
- **Do:** Enforce Context + useState; memoize provider values; throw on null context.
- **Don't:** Allow external state libraries or prop mutation.

**Required subsections:** Context Creation, Provider, Consumer Hook, Local State, Props-Down
**Optional subsections:** Performance Patterns, Debugging State
**Required diagrams:** none
**Required cross-references:** component_implementation, code_standards

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
