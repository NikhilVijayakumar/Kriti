# Component Architecture — Generation Template

> **Domain:** architecture
> **Section:** component_architecture
> **Source:** `documentation-standards/05-architecture-standards.md` §Component Architecture
> **Relationships:** `audit/deterministic/document/architecture-relationships.yaml`

Generates component composition patterns, atomic tier hierarchy, and barrel export conventions.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| derives_from | feature-technical/component_responsibilities | Must align component tiers with declared responsibilities |

## Template

```markdown
# Component Architecture

## Atomic Design Tiers

| Tier | Scope | Reuse | Example |
|---|---|---|---|
| Atoms | Single element, no children | Universal | Button, Input, Icon |
| Molecules | Small composites of atoms | High | SearchBar, CardHeader |
| Organisms | Complex UI sections | Medium | NavBar, DashboardPanel |
| Templates | Page-level layout shells | Low | AuthLayout, AppShell |

### Tier Rules

- Atoms must not import other atoms from different feature modules.
- Molecules compose exactly one atom tier plus optional primitives.
- Organisms may reference molecules but never reach into atom internals.
- Templates compose organisms; they contain zero business logic.

## Barrel Export Conventions

- Each tier directory exports via `index.ts` re-export barrel.
- Barrel files re-export only public API; internal helpers stay unexported.
- Feature modules expose one barrel at module root, never nested barrels.

## Composition Rules

- Prefer composition over inheritance in all tiers.
- Pass data down via props; never access context inside atoms.
- Container/presentational split applies at organism tier and above.

## Reuse Guidelines

- Atoms and molecules are shared across all features.
- Organisms may be feature-scoped when domain coupling is unavoidable.
- Duplication below organism tier is preferred over premature abstraction.

**Required subsections:** Atomic Design Tiers, Barrel Export Conventions, Composition Rules
**Optional subsections:** Reuse Guidelines, Migration Patterns
**Required diagrams:** none
**Required cross-references:** component_responsibilities, code_standards
```

## Examples

**Correct:**
> Atoms directory contains `Button.tsx`, `Input.tsx`, `Icon.tsx` with a single `index.ts` barrel re-exporting all three.

**Incorrect:**
> `OrganismCard` imports `Button` from `../../atoms/shared/Button` via relative deep path.
> *Why wrong: Atoms must be accessed through barrel exports, never via relative deep imports.*

## Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** hierarchical tables and rules
- **Audience:** architect
- **Do:** Define clear boundaries per tier; enforce barrel-only access patterns.
- **Don't:** Allow cross-tier circular dependencies or deep relative imports.

**Required subsections:** Atomic Design Tiers, Barrel Export Conventions, Composition Rules
**Optional subsections:** Reuse Guidelines, Migration Patterns
**Required diagrams:** none
**Required cross-references:** component_responsibilities, code_standards

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
