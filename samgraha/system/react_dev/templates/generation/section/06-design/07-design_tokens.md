# Design Tokens — Generation Template

> **Domain:** design
> **Section:** design_tokens
> **Source:** `documentation-standards/06-design-standards.md` §Design Tokens
> **Relationships:** `audit/deterministic/document/design-relationships.yaml`

Generates three-layer token architecture, theme sovereignty rules, and dark mode implementation.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| constrains | engineering/code_standards | All code must consume tokens, never hardcoded values |

## Template

```markdown
# Design Tokens

## Three-Layer Token Architecture

### Layer 1: JS Token Constants

- Define raw values in `tokens/constants.ts` as typed JS objects.
- Group by category: `color`, `spacing`, `typography`, `elevation`.
- Values are platform-agnostic primitives only.

### Layer 2: Theme Object

- Compose constants into a theme object in `tokens/theme.ts`.
- Theme merges light/dark variants under a single typed interface.
- Export `lightTheme` and `darkTheme` as frozen objects.

### Layer 3: CSS Custom Properties

- Theme object maps to CSS custom properties at root level.
- Property naming: `--{category}-{semantic-name}` (e.g. `--color-bg-primary`).
- Runtime theme switch updates custom properties on `<html>`.

## Token Naming Conventions

- Pattern: `{category}.{semantic}.{modifier}` in JS.
- CSS: `--{category}-{semantic}` with optional `-{modifier}` suffix.
- Never use raw hex/rgb in component code; reference tokens exclusively.

## Theme Sovereignty Rules

- All visual values MUST originate from the token pipeline.
- Hardcoded colors, sizes, or shadows in components are audit failures.
- Exceptions require explicit `/* token-exception: reason */` comment and approval.

## Dark Mode Implementation

- Dark theme redefines the same CSS custom properties at `[data-theme="dark"]`.
- Component code references the same tokens; no conditional logic needed.
- Transition: `prefers-color-scheme` media query sets default; JS toggle overrides.

**Required subsections:** Three-Layer Architecture, Token Naming, Sovereignty Rules, Dark Mode
**Optional subsections:** Token Migration, Legacy Cleanup
**Required diagrams:** none
**Required cross-references:** code_standards, ux_principles
```

## Examples

**Correct:**
> `const primaryBg = theme.color.bg.primary;` — consumed via theme object, resolved to CSS custom property.

**Incorrect:**
> `background-color: #ffffff;` inside a component stylesheet.
> *Why wrong: Hardcoded value bypasses token pipeline; use `var(--color-bg-primary)` or theme object.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** layered pipeline with rules per layer
- **Audience:** designer
- **Do:** Define every token in the pipeline; enforce sovereignty with audit checks.
- **Don't:** Allow hardcoded values or bypass the three-layer architecture.

**Required subsections:** Three-Layer Architecture, Token Naming, Sovereignty Rules, Dark Mode
**Optional subsections:** Token Migration, Legacy Cleanup
**Required diagrams:** none
**Required cross-references:** code_standards, ux_principles

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
