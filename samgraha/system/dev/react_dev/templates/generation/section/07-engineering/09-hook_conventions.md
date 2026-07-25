# Hook Conventions — Generation Template

> **Domain:** engineering
> **Section:** hook_conventions
> **Source:** `documentation-standards/07-engineering-standards.md` §Hook Conventions
> **Relationships:** `audit/deterministic/document/engineering-relationships.yaml`

Generates custom hook patterns, naming conventions, return types, and composition rules.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| constrains | feature-technical/component_implementation | All custom hooks must follow naming and return-type conventions |

## Template

```markdown
# Hook Conventions

## Naming Convention

- All custom hooks use `use` prefix: `useAuth`, `useForm`, `useLanguage`.
- Hook file name matches the hook: `useAuth.ts`, `useForm.ts`.
- No abbreviations in hook names; spell out full domain terms.

## Return Types

- Hooks always return a typed object, never bare values or tuples.
- Return type interface defined in same file as the hook.
- Name the interface `Use{Name}Return` (e.g. `UseAuthReturn`).

## Rules

- No conditional hook calls; every `use*` executes in the same order.
- Hooks compose other hooks but never call hooks conditionally.
- State ownership: hooks own state when shared; components own when local.
- No external state libraries; use Context + useState exclusively.

## Composition Patterns

- Hooks may delegate to other hooks for separation of concerns.
- Shared hooks live in `hooks/` at package root; feature hooks in feature dir.
- Each hook manages one concern; split multi-concern hooks into composites.

## Error Handling

- Hooks throw or return error state; never swallow errors silently.
- Return `error: string | null` in the return type when fallible.

**Required subsections:** Naming, Return Types, Rules, Composition Patterns
**Optional subsections:** Error Handling, Testing Hooks
**Required diagrams:** none
**Required cross-references:** component_implementation, code_standards
```

## Examples

**Correct:**
> `const { user, isLoading, error } = useAuth();` — typed object return with clear destructuring.

**Incorrect:**
> `const [user, loading] = useAuth();` — tuple return violates typed-object convention.
> *Why wrong: Tuples lack named fields; always return typed objects for clarity.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** rules and patterns with clear mandates
- **Audience:** engineer
- **Do:** Enforce `use` prefix, typed-object returns, and no conditional calls.
- **Don't:** Allow tuple returns, missing error handling, or external state libraries.

**Required subsections:** Naming, Return Types, Rules, Composition Patterns
**Optional subsections:** Error Handling, Testing Hooks
**Required diagrams:** none
**Required cross-references:** component_implementation, code_standards

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
