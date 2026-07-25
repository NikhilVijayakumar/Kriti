# Internationalization — Generation Template

> **Domain:** engineering
> **Section:** internationalization
> **Source:** `documentation-standards/07-engineering-standards.md` §Internationalization
> **Relationships:** `audit/deterministic/document/engineering-relationships.yaml`

Generates useLanguage() hook patterns, translation map structures, and fallback chains.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| constrains | feature-technical/component_implementation | All user-facing strings must use translation maps with fallback chains |

## Template

```markdown
# Internationalization

## Translation Map Structure

- Translation maps live in `i18n/{locale}.ts` as typed objects.
- Keys use dot notation: `{domain}.{key}` (e.g. `auth.loginTitle`).
- Map type: `Record<string, string | Record<string, string>>`.
- Each locale file exports the same typed interface.

## useLanguage() Hook

- Returns `{ t, locale, setLocale }` as typed object.
- `t(key: string): string` resolves a translation key with fallback.
- Fallback chain: `literal['key'] ?? translations[locale][key] ?? translations['en'][key] ?? key`.
- Never call `t()` outside a component; always inside render or hooks.

## Fallback Pattern

- Primary: literal string passed to `t()` as second argument.
- Secondary: English locale value.
- Tertiary: the key itself as last resort.
- Log missing keys in development mode only.

## Provider Setup

- `LanguageProvider` wraps the app root.
- Stores current locale in state; persists to `localStorage`.
- Reads `navigator.language` on mount for initial locale.
- Exposes `useLanguage()` via context.

## Language Switching

- `setLocale(locale)` updates state, persists, and re-renders.
- Never reload the page on language change.
- Transition animation optional but recommended.

**Required subsections:** Translation Maps, useLanguage Hook, Fallback Chain, Provider, Switching
**Optional subsections:** RTL Support, Pluralization Rules
**Required diagrams:** none
**Required cross-references:** component_implementation, ux_principles
```

## Examples

**Correct:**
> `const { t } = useLanguage(); return <h1>{t('auth.loginTitle', 'Log In')}</h1>;` — typed translation with fallback.

**Incorrect:**
> `return <h1>{translations[locale]['auth']['loginTitle']}</h1>;` — direct map access bypasses fallback chain.
> *Why wrong: Direct access skips the English fallback and key-as-last-resort safety net.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** hook-first patterns with fallback rules
- **Audience:** engineer
- **Do:** Enforce useLanguage() for all strings; implement full fallback chain; persist locale.
- **Don't:** Allow direct translation map access or hardcoded user-facing strings.

**Required subsections:** Translation Maps, useLanguage Hook, Fallback Chain, Provider, Switching
**Optional subsections:** RTL Support, Pluralization Rules
**Required diagrams:** none
**Required cross-references:** component_implementation, ux_principles

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
