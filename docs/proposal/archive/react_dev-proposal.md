# Frontend Development using React - Knowledge System Proposal

## Overview

This proposal defines how to transform `react_dev` from a clone of `base_dev` into a standalone engineering methodology for building frontend systems using React.

**Base System**: `base_dev` (canonical, unchanged)
**Target System**: `react_dev` (standalone, frontend engineering methodology)

**Core Shift**: This is NOT a React guide. This is YOUR frontend engineering methodology implemented with React.

---

## Pattern Sources

Patterns derived from real-world implementations. These sources informed the standards but are NOT referenced in the generated standards.

| Source | Location | Patterns Derived |
|--------|----------|------------------|
| **Astra** | `E:\Python\astra` | MVVM, `useDataState<T>()`, Repository pattern, Platform neutrality, IPC abstraction |
| **Prati** | `E:\Python\Prati` | Atomic Design, Theme sovereignty, Stateless UI, `useLanguage()`, MUI 7 |
| **Prana** | `E:\Python\Prana` | Application Runtime, Service Registry, Event System, Storage Domains |

---

## External Reference Isolation (MANDATORY)

**Rule**: All external references (Astra, Prati, Prana, etc.) are confined to THIS proposal document ONLY.

**Generated standards must NOT contain:**
- Names of external systems (Astra, Prati, Prana, etc.)
- File paths to external repositories
- References to specific implementations
- Links to external documentation

**Generated standards MUST contain:**
- Generic patterns derived from external systems
- Technology-agnostic concepts
- Framework-specific guidance (React, TypeScript, etc.)
- Self-contained, independently usable standards

**How patterns are "baked in":**

| External Pattern | Standardized As (In Standard) |
|------------------|------------------------------|
| Astra MVVM | MVVM pattern (generic) |
| Astra `useDataState<T>()` | State management hooks (generic) |
| Astra Repository pattern | Data access layer (generic) |
| Astra Platform neutrality | Platform-agnostic service abstraction |
| Astra IPC abstraction | Platform service interface |
| Prati Atomic Design | Component hierarchy (Atoms→Molecules→Organisms→Templates) |
| Prati Theme sovereignty | Token-based theming |
| Prati Stateless UI | Functional components, hooks-only state |
| Prati `useLanguage()` | i18n hook pattern |
| Prana Application Runtime | Application lifecycle management |
| Prana Service Registry | Service registration and discovery |
| Prana Event System | Pub/sub event architecture |
| Prana Storage Domains | Data persistence layers |

**Verification**: This leak-check is a natural fit for the `script/` audit pipeline (same shape as `secret-scan`). Currently unenforced — flagged as future work.

---

## Core Philosophy (PRESERVE)

All engineering principles from `base_dev` remain unchanged:

- Documentation-first engineering
- Deterministic compilation
- Explicit architecture
- Modular design
- Traceability
- Documentation-driven audit
- Local-first workflow

---

## System-Specific Files

Each system gets its own copies of these files because domain tiers differ per system:

| File | Why System-Specific |
|------|---------------------|
| `00-domain-relationships.md` | Domain tier ordering and cross-domain dependencies differ per system |
| `plan/core/tiers.yaml` | Derived from `00-domain-relationships.md` — must match system's domain list |

These files are NOT shared across systems. When creating `react_dev`, copy these from `base_dev` then modify to reflect the system's domain scope.

---

## Domain Scope

### Domains KEPT (16 of 16)

| Tier | Domain | Standard File | Action |
|------|--------|---------------|--------|
| 1 | 01-vision | `01-vision-standards.md` | KEEP + add frontend vision |
| 1 | 02-philosophy | `02-philosophy-standards.md` | KEEP |
| 2 | 03-security | `03-security-standards.md` | KEEP + add frontend security |
| 2 | 04-feature | `04-feature-standards.md` | KEEP + add frontend feature definition |
| 2 | 05-architecture | `05-architecture-standards.md` | KEEP + add component architecture |
| 2 | 06-design | `06-design-standards.md` | KEEP + add design system, atomic design |
| 2 | 07-engineering | `07-engineering-standards.md` | KEEP + add React/TypeScript patterns |
| 2 | 08-external-context | `08-external-context-standards.md` | KEEP + add technology categories |
| 3 | 09-feature-design | `09-feature-design-standards.md` | KEEP + add UI feature design |
| 3 | 10-feature-technical | `10-feature-technical-standards.md` | KEEP + add implementation guidance |
| 4 | 11-prototype | `11-prototype-standards.md` | KEEP + add prototyping |
| 5 | 13-implementation | `13-implementation-standards.md` | KEEP + add component patterns |
| 6 | 12-qa | `12-qa-standards.md` | KEEP + add Jest/Playwright patterns |
| 7 | 14-build | `14-build-standards.md` | KEEP + add Vite/Webpack guidance |
| 8 | 15-readme | `15-readme-standards.md` | KEEP + add frontend README |
| 8 | 16-product-guide | `16-product-guide-standards.md` | KEEP + add development workflow |

### Tier Reordering

| Tier | base_dev | react_dev |
|------|----------|-----------|
| 1 | 01-vision, 02-philosophy | 01-vision, 02-philosophy |
| 2 | 03-security, 04-feature, 05-architecture, 06-design, 07-engineering, 08-external-context | 03-security, 04-feature, 05-architecture, 06-design, 07-engineering, 08-external-context |
| 3 | 09-feature-design, 10-feature-technical | 09-feature-design, 10-feature-technical |
| 4 | 11-prototype | 11-prototype |
| 5 | 13-implementation | 13-implementation |
| 6 | 12-qa | 12-qa |
| 7 | 14-build | 14-build |
| 8 | 15-readme, 16-product-guide | 15-readme, 16-product-guide |

---

## Section Slot Mapping

Slot numbers match actual files on disk in `base_dev/templates/generation/section/{domain}/`. New slots are appended after the last existing slot.

### 05-architecture (11 existing, ADD 1 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add frontend architecture purpose |
| 02 | `02-system_overview.md` | KEEP — generic |
| 03 | `03-component_model.md` | MODIFY — add component hierarchy |
| 04 | `04-communication_paths.md` | MODIFY — add props, context, events |
| 05 | `05-data_flow.md` | MODIFY — add state management |
| 06 | `06-security_considerations.md` | KEEP — generic |
| 07 | `07-rationale.md` | MODIFY — add module structure rationale |
| 08 | `08-constraints.md` | MODIFY — add API integration constraints |
| 09 | `09-traceability.md` | KEEP — generic |
| 10 | `10-operational_readiness.md` | KEEP — generic |
| 11 | `11-observability.md` | KEEP — generic |
| 12 | `12-component_architecture.md` | **NEW SLOT** — component composition, hierarchy |

### 06-design (6 existing, ADD 1 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-design_principles.md` | MODIFY — add Atomic Design |
| 02 | `02-ux_principles.md` | MODIFY — add UX principles |
| 03 | `03-accessibility.md` | MODIFY — add accessibility standards |
| 04 | `04-purpose.md` | MODIFY — add design system purpose |
| 05 | `05-constraints.md` | MODIFY — add token-based theming constraints |
| 06 | `06-traceability.md` | KEEP — generic |
| 07 | `07-design_tokens.md` | **NEW SLOT** — token hierarchy, theme sovereignty |

### 07-engineering (8 existing, ADD 4 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-guiding_principles.md` | MODIFY — add React conventions |
| 02 | `02-rationale.md` | MODIFY — add rationale for engineering choices |
| 03 | `03-build_standards.md` | MODIFY — add build standards |
| 04 | `04-testing_standards.md` | MODIFY — add testing standards |
| 05 | `05-purpose.md` | MODIFY — add purpose |
| 06 | `06-code_standards.md` | MODIFY — add TypeScript, hooks |
| 07 | `07-constraints.md` | MODIFY — add error boundaries |
| 08 | `08-traceability.md` | KEEP — generic |
| 09 | `09-hook_conventions.md` | **NEW SLOT** — custom hooks, state management |
| 10 | `10-component_patterns.md` | **NEW SLOT** — compound, render props, HOC |
| 11 | `11-state_management.md` | **NEW SLOT** — Redux, Zustand, Context |
| 12 | `12-internationalization.md` | **NEW SLOT** — i18n, locale management |

### 09-feature-design (7 existing, ADD 1 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add UI feature design purpose |
| 02 | `02-user-experience.md` | KEEP — generic |
| 03 | `03-workflow.md` | KEEP — generic |
| 04 | `04-states.md` | KEEP — generic |
| 05 | `05-constraints.md` | KEEP — generic |
| 06 | `06-non_goals.md` | KEEP — generic |
| 07 | `07-traceability.md` | KEEP — generic |
| 08 | `08-user_flow.md` | **NEW SLOT** — navigation, state flow |

### 10-feature-technical (17 existing, ADD 1 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add frontend implementation purpose |
| 02-17 | (existing slots) | KEEP — generic |
| 18 | `18-component_implementation.md` | **NEW SLOT** — component, hook, state |

### 12-qa (9 existing, ADD 2 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add Jest patterns |
| 02-09 | (existing slots) | KEEP — generic |
| 10 | `10-visual_testing.md` | **NEW SLOT** — Playwright, Storybook |
| 11 | `11-component_testing.md` | **NEW SLOT** — React Testing Library |

### 13-implementation (6 existing, ADD 1 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add feature scaffold plan |
| 02 | (gap — slot 02 missing on disk) | — |
| 03-07 | (existing slots) | KEEP — generic |
| 08 | `08-feature_folder_structure.md` | **NEW SLOT** — directory layout |

### 14-build (8 existing, ADD 1 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add build purpose |
| 02 | (gap — slot 02 missing on disk) | — |
| 03 | `03-documentation_quality.md` | KEEP — generic |
| 04 | `04-security_checks.md` | KEEP — generic |
| 05 | `05-size_checks.md` | KEEP — generic |
| 06 | `06-ml_artifact_management.md` | KEEP — generic |
| 07 | `07-cicd_validation.md` | KEEP — generic |
| 08 | `08-obfuscation_optimization.md` | KEEP — generic |
| 09 | `09-versioning_naming.md` | KEEP — generic |
| 10 | `10-bundle_analysis.md` | **NEW SLOT** — bundle size, code splitting |

### 16-product-guide (6 existing, ADD 1 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-title.md` | KEEP — generic |
| 02 | `02-body.md` | KEEP — generic |
| 03 | `03-purpose.md` | KEEP — generic |
| 04 | `04-product_context.md` | KEEP — generic |
| 05 | `05-public_contract.md` | KEEP — generic |
| 06 | `06-related.md` | KEEP — generic |
| 07 | `07-development_workflow.md` | **NEW SLOT** — how we work |

---

## Engineering Methodology

### 1. Vision

> How do we build frontend systems in our ecosystem?

**Answer**: We build performant, accessible, maintainable frontend systems with clear component architecture. React is our implementation technology, not our architecture.

### 2. Architecture

**Principle**: Architecture is YOURS. React is one implementation detail.

| Pattern | Standard | Alternative | Override Allowed |
|---------|----------|-------------|-----------------|
| Component Hierarchy | Required (Atomic Design) | Custom hierarchy | Yes, with justification |
| State Management | Required (one strategy) | Multiple strategies | No — must be consistent |
| Data Flow | Unidirectional | Bidirectional in same layer | No |
| Module Boundaries | Feature isolation | Shared modules with DI | Yes, document in 00-domain-relationships |

### 3. Engineering

**Principle**: Engineering is MORE than React. Framework is one part.

- TypeScript EVERYWHERE
- Functional components ONLY
- Hooks for ALL state and side effects
- No class components
- No inline styles (use CSS modules or styled-components)
- No magic strings (use constants)
- Lazy loading for routes and heavy components

### 4. Audit

**Principle**: Audit ARCHITECTURAL DRIFT, not just syntax.

Weight and severity adjustments happen inside `audit/deterministic/{domain}/*.yaml` files, NOT in `calculation/*.yaml`. The calculation layer is generic and shared across all systems.

### 5. Templates

Content is injected into existing numbered slots per domain. See **Section Slot Mapping** above.

### 6. Product Guide

Answers "How do we work?" not "What is React?"

### 7. Engineering Decisions

| Decision | Preferred Option | Alternative | Reason |
|----------|-----------------|-------------|--------|
| UI Library | React | Vue, Angular | Ecosystem, TypeScript support |
| State Management | Zustand | Redux, Context | Simplicity, performance |
| Styling | CSS Modules | Styled-components, Tailwind | Co-location, no runtime |
| Testing | Jest + Playwright | Vitest, Cypress | Coverage, E2E |
| Build | Vite | Webpack, esbuild | Speed, simplicity |

### 8. External Context

| Category | Purpose | Options |
|----------|---------|---------|
| UI Framework | Component library | MUI, Ant Design, Chakra UI, shadcn/ui |
| State Management | Application state | Zustand, Redux Toolkit, Jotai, Recoil |
| Styling | CSS solution | CSS Modules, Styled-components, Tailwind |
| Forms | Form handling | React Hook Form, Formik |
| Data Fetching | API integration | TanStack Query, SWR, Apollo Client |
| Routing | Navigation | React Router, TanStack Router |
| i18n | Internationalization | react-i18next, react-intl |
| Animation | Motion | Framer Motion, React Spring |

---

## New Subsystems (Not Integrated with Audit Script Pipeline)

The following are NEW artifact types proposed for creation. They are NOT part of the existing `script/` audit verification infrastructure (mapping.yaml, manifests, schema files). They would require a separate subsystem if implemented.

### Feature Scaffolding (Proposed)

| Script | Purpose |
|--------|---------|
| `create-feature.sh/ps1` | Scaffold complete feature (component + hooks + types) |
| `create-component.sh/ps1` | Scaffold component with props, tests |
| `create-hook.sh/ps1` | Scaffold custom hook with types |
| `create-page.sh/ps1` | Scaffold page with routing |

---

## Files to Modify

### Domain Files

| File | Action |
|------|--------|
| `00-domain-relationships.md` | REPLACE — system-specific domain tier ordering (16 domains, same as base_dev but reordered) |
| `plan/core/tiers.yaml` | REPLACE — derived from system's 00-domain-relationships.md |
| `documentation-standards/01-vision-standards.md` | ADD — frontend engineering vision |
| `documentation-standards/02-philosophy-standards.md` | KEEP |
| `documentation-standards/03-security-standards.md` | ADD — frontend security, XSS, CSRF |
| `documentation-standards/04-feature-standards.md` | ADD — frontend feature definition |
| `documentation-standards/05-architecture-standards.md` | ADD — component architecture, state management |
| `documentation-standards/06-design-standards.md` | ADD — design system, Atomic Design, tokens |
| `documentation-standards/07-engineering-standards.md` | ADD — React conventions, hooks, TypeScript |
| `documentation-standards/08-external-context-standards.md` | ADD — technology categories |
| `documentation-standards/09-feature-design-standards.md` | ADD — UI feature design |
| `documentation-standards/10-feature-technical-standards.md` | ADD — component implementation |
| `documentation-standards/11-prototype-standards.md` | ADD — prototyping |
| `documentation-standards/12-qa-standards.md` | ADD — Jest, Playwright, component testing |
| `documentation-standards/13-implementation-standards.md` | ADD — component patterns |
| `documentation-standards/14-build-standards.md` | ADD — Vite, bundling |
| `documentation-standards/15-readme-standards.md` | ADD — frontend README |
| `documentation-standards/16-product-guide-standards.md` | ADD — development workflow |

### Audit Knowledge (nested domain folders)

| Path | Content |
|------|---------|
| `audit/semantic/section/05-architecture/12-component_architecture.md` | Component rules |
| `audit/semantic/section/07-engineering/10-hook_conventions.md` | Hook rules |
| `audit/semantic/section/07-engineering/11-component_patterns.md` | Component pattern rules |
| `audit/semantic/section/07-engineering/12-state_management.md` | State management rules |
| `audit/semantic/section/12-qa/10-visual_testing.md` | Visual testing rules |
| `audit/semantic/section/12-qa/11-component_testing.md` | Component testing rules |

### Generation Templates (nested domain folders)

| Path | Content |
|------|---------|
| `templates/generation/section/05-architecture/12-component_architecture.md` | Component composition, hierarchy |
| `templates/generation/section/06-design/07-design_tokens.md` | Token hierarchy, theme sovereignty |
| `templates/generation/section/07-engineering/09-hook_conventions.md` | Custom hooks, state management |
| `templates/generation/section/07-engineering/10-component_patterns.md` | Compound, render props, HOC |
| `templates/generation/section/07-engineering/11-state_management.md` | Redux, Zustand, Context |
| `templates/generation/section/07-engineering/12-internationalization.md` | i18n, locale management |
| `templates/generation/section/09-feature-design/08-user_flow.md` | Navigation, state flow |
| `templates/generation/section/10-feature-technical/18-component_implementation.md` | Component, hook, state |
| `templates/generation/section/12-qa/10-visual_testing.md` | Playwright, Storybook |
| `templates/generation/section/12-qa/11-component_testing.md` | React Testing Library |
| `templates/generation/section/13-implementation/08-feature_folder_structure.md` | Directory layout |
| `templates/generation/section/14-build/10-bundle_analysis.md` | Bundle size, code splitting |
| `templates/generation/section/16-product-guide/07-development_workflow.md` | How we work |

---

## Success Criteria

- [ ] `react_dev` is independently usable
- [ ] Answers "How do we build frontend systems?" not "What is React?"
- [ ] Documents YOUR component architecture, not framework documentation
- [ ] Preserves core philosophy of `base_dev`
- [ ] Provides clear engineering methodology
- [ ] Enables consistent decision-making across projects
- [ ] All file paths match engine glob patterns
- [ ] No external system references in generated standards

---

# Implementation Plan

This section defines the complete execution plan for transforming `react_dev`. Each phase lists exact files, actions, and content requirements. Verification = compare implemented file against plan entry.

---

## Phase 1: System Identity (1 file)

### 1.1 Update `00-domain-relationships.md`

**Action**: REWRITE — frontend-specific cross-domain relationships

**File**: `E:\Python\Kriti\samgraha\system\react_dev\00-domain-relationships.md`

**Content Requirements**:
- 16 domains listed with frontend-specific tier purposes
- Cross-domain dependency matrix reflecting frontend concerns (e.g., 08-frontend depends on 06-design for tokens, 07-engineering for patterns, 05-architecture for component tree)
- Section breakdowns for each domain with frontend-specific section names
- Tier summary table showing frontend engineering tier purposes
- Relationship table showing how domains interact in frontend context

**Verification**: Compare domain relationships against base_dev version — all system-name references removed, frontend context added

---

## Phase 2: Documentation Standards (14 files modified, 2 untouched)

All modifications are **APPENDS** to existing content — no existing content removed.

### 2.1 `01-vision-standards.md`

**Action**: ADD frontend engineering vision

**Content to add**:
- Frontend-specific vision statements: "We build performant, accessible, maintainable frontend systems"
- Component-driven development as architectural principle
- User experience as first-class engineering concern
- Performance budgets as architectural constraints
- Accessibility as non-negotiable requirement

### 2.2 `03-security-standards.md`

**Action**: ADD frontend security

**Content to add**:
- XSS prevention patterns (input sanitization, CSP headers, dangerouslySetInnerHTML avoidance)
- CSRF protection for API calls
- Dependency auditing for client-side packages
- Secret-free client code principle
- Content Security Policy configuration patterns

### 2.3 `04-feature-standards.md`

**Action**: ADD frontend feature definition

**Content to add**:
- Feature = component + hooks + types + tests
- Feature folder structure conventions
- Feature isolation boundaries
- Feature-level state ownership
- Feature composition patterns

### 2.4 `05-architecture-standards.md`

**Action**: ADD component architecture

**Content to add**:
- Component tree as architecture (not file structure)
- Module boundaries via barrel exports
- Data flow architecture (unidirectional, props-down)
- State architecture (context for cross-cutting, local for UI)
- Render pipeline optimization
- Virtual DOM concepts (reconciliation, keyed lists)

### 2.5 `06-design-standards.md`

**Action**: ADD design system, Atomic Design

**Content to add**:
- Atomic Design methodology (atoms → molecules → organisms → templates → pages)
- Design token hierarchy (JS → theme → CSS custom properties)
- Theme sovereignty invariant: all visual values from tokens
- Responsive design constraints (mobile-first, breakpoint system)
- Accessibility standards (WCAG 2.1 AA minimum)
- Dark mode architecture (token layer switching)

### 2.6 `07-engineering-standards.md`

**Action**: ADD React/TypeScript patterns

**Content to add**:
- TypeScript everywhere — strict mode, no `any`
- Functional components only — no class components
- Hooks for ALL state and side effects
- Named exports only — no default exports
- `FC<Props>` typing convention with explicit `ReactElement` return
- Props patterns: action config, render props, composition slots, generics
- Error boundary pattern (class component wrapping dynamic renderers)
- i18n pattern: `useLanguage()` hook with `literal['key']` and fallback chains

### 2.7 `08-external-context-standards.md`

**Action**: ADD technology categories

**Content to add**:
- UI Framework category: component library selection criteria
- State Management category: no external libs preference, Context + useState
- Styling category: CSS-in-JS vs CSS modules decision framework
- Testing category: Vitest + Testing Library preference
- Build category: Vite preference with webpack fallback
- Data Fetching category: server state vs client state separation
- i18n category: key-value translation maps, no library preference

### 2.8 `09-feature-design-standards.md`

**Action**: ADD UI feature design

**Content to add**:
- Feature = user flow + component tree + state map
- Component hierarchy per feature (which atoms/molecules/organisms)
- State ownership per feature (which contexts, which local state)
- API integration patterns (data fetching hooks, loading/error states)
- Accessibility per feature (keyboard nav, screen reader, ARIA)

### 2.9 `10-feature-technical-standards.md`

**Action**: ADD component implementation

**Content to add**:
- Component implementation checklist: props → types → render → tests → stories
- Hook implementation pattern: input types → logic → return types
- State implementation: context creation → provider → consumer hook
- Type implementation: interface export → generic constraints → union literals
- Test implementation: render test → interaction test → context test

### 2.10 `11-prototype-standards.md`

**Action**: ADD prototyping patterns

**Content to add**:
- Prototype = throwaway HTML/React, not production code
- Storybook as prototype surface
- Mock data patterns for prototypes
- User testing with prototypes
- Prototype → production conversion checklist

### 2.11 `12-qa-standards.md`

**Action**: ADD Jest/Playwright patterns

**Content to add**:
- Component testing: render, interaction, context integration
- Visual regression: Storybook + Chromatic/Percy
- Accessibility testing: axe-core integration
- Cross-browser testing matrix
- Responsive breakpoint validation
- Screen reader testing protocols
- Keyboard navigation verification

### 2.12 `13-implementation-standards.md`

**Action**: ADD component patterns

**Content to add**:
- Component folder structure: `ComponentName/ComponentName.tsx` + `ComponentName.test.tsx` + optional `ComponentName.stories.tsx`
- Hook folder structure: `useHookName.ts` co-located with consumer
- Type folder structure: `types.ts` or `*Data.ts` for complex props
- Barrel export conventions at each tier
- Feature folder structure: `feature/FeatureName/components/`, `feature/FeatureName/hooks/`, `feature/FeatureName/types/`

### 2.13 `14-build-standards.md`

**Action**: ADD Vite/Webpack guidance

**Content to add**:
- Vite configuration patterns (dev server, build optimization)
- Code splitting strategy (route-based, component-based)
- Tree shaking requirements
- Asset pipeline (images, fonts, icons)
- Environment configuration (`.env` patterns)
- Bundle size gates (CI enforcement)
- Source map strategy

### 2.14 `16-product-guide-standards.md`

**Action**: ADD development workflow

**Content to add**:
- How we work: feature branch → component → tests → review → merge
- Component development workflow (design → implement → test → document)
- Design token contribution process
- Storybook documentation workflow
- Accessibility review checklist
- Performance review checklist

### 2.15 Files NOT modified

- `02-philosophy-standards.md` — KEEP (generic, no frontend additions needed)
- `15-readme-standards.md` — KEEP (generic)

---

## Phase 3: New Generation Templates (13 files)

All new files follow existing template structure: header with version/engineering_intent/purpose, relationships section, template section with numbered instructions, examples section, notes section.

### 3.1 `templates/generation/section/05-architecture/12-component_architecture.md`

**Content**: Component composition patterns, hierarchy rules (atomic tiers), barrel export conventions, module boundaries, component reuse guidelines

### 3.2 `templates/generation/section/06-design/07-design_tokens.md`

**Content**: Three-layer token architecture (JS constants → theme → CSS custom properties), theme sovereignty rules, dark mode implementation, spacing/typography/color token files

### 3.3 `templates/generation/section/07-engineering/09-hook_conventions.md`

**Content**: Custom hooks patterns, hook naming conventions (use*), hook return types, hook composition, state ownership rules per component tier

### 3.4 `templates/generation/section/07-engineering/10-component_patterns.md`

**Content**: Compound components, render props, HOC patterns, composition vs inheritance, when to use each pattern

### 3.5 `templates/generation/section/07-engineering/11-state_management.md`

**Content**: Context + useState patterns (no external libs), cross-cutting state (theme, language) via Context, UI-local state via useState, props-down convention

### 3.6 `templates/generation/section/07-engineering/12-internationalization.md`

**Content**: useLanguage() hook pattern, translation map structure, fallback chains (`literal['key'] ?? 'fallback'`), provider setup, language switching, RTL support considerations

### 3.7 `templates/generation/section/09-feature-design/08-user_flow.md`

**Content**: Navigation patterns, state flow diagrams, route hierarchy, deep linking, back button handling, URL state synchronization

### 3.8 `templates/generation/section/10-feature-technical/18-component_implementation.md`

**Content**: Component implementation checklist: props → types → render → tests → stories. Hook implementation pattern. State implementation: context creation → provider → consumer hook.

### 3.9 `templates/generation/section/12-qa/10-visual_testing.md`

**Content**: Screenshot testing, Storybook-based visual diff, Chromatic/Percy integration, baseline management, CI gate configuration

### 3.10 `templates/generation/section/12-qa/11-component_testing.md`

**Content**: Vitest + Testing Library patterns, mock conventions (always mock useLanguage), render/interaction/context test categories, co-located test files, assertion patterns

### 3.11 `templates/generation/section/13-implementation/08-feature_folder_structure.md`

**Content**: Feature folder structure: `feature/FeatureName/components/`, `feature/FeatureName/hooks/`, `feature/FeatureName/types/`, barrel exports, naming conventions

### 3.12 `templates/generation/section/14-build/10-bundle_analysis.md`

**Content**: Bundle size budgets per route/component, webpack-bundle-analyzer usage, size CI gates, treeshaking verification, dependency audit

### 3.13 `templates/generation/section/16-product-guide/07-development_workflow.md`

**Content**: How we work: feature branch → component → tests → review → merge. Component development workflow. Design token contribution process. Storybook documentation workflow.

---

## Phase 4: New Audit Rules (6 semantic + 6 deterministic)

### 4.1 `audit/semantic/section/05-architecture/12-component_architecture.md`

**Content**: Component architecture audit knowledge — scoring criteria, expected patterns, red flags, edge cases for component hierarchy compliance

### 4.2 `audit/deterministic/section/05-architecture/12-component_architecture.yaml`

**Content**: Deterministic rules — component naming (PascalCase), barrel exports present, tier organization, no cross-tier imports, props interface exported

### 4.3 `audit/semantic/section/07-engineering/10-hook_conventions.md`

**Content**: Hook conventions audit knowledge — hook naming verification, return type patterns, hook composition rules, state ownership compliance

### 4.4 `audit/deterministic/section/07-engineering/10-hook_conventions.yaml`

**Content**: Deterministic rules — hook names start with "use", hooks return typed objects, no conditional hooks, hooks co-located with consumers

### 4.5 `audit/semantic/section/07-engineering/11-component_patterns.md`

**Content**: Component patterns audit knowledge — pattern selection criteria, composition vs inheritance verification, render prop usage

### 4.6 `audit/deterministic/section/07-engineering/11-component_patterns.yaml`

**Content**: Deterministic rules — no class components, functional components only, named exports only, FC<Props> typing present

### 4.7 `audit/semantic/section/07-engineering/12-state_management.md`

**Content**: State management audit knowledge — context usage verification, no external state libs, props-down compliance

### 4.8 `audit/deterministic/section/07-engineering/12-state_management.yaml`

**Content**: Deterministic rules — no Redux/Zustand/MobX imports, Context creation patterns, useState usage, no class components

### 4.9 `audit/semantic/section/12-qa/10-visual_testing.md`

**Content**: Visual testing audit knowledge — screenshot baselines, Storybook integration, CI gate configuration

### 4.10 `audit/deterministic/section/12-qa/10-visual_testing.yaml`

**Content**: Deterministic rules — visual test files present, baseline images stored, CI configuration for visual tests

### 4.11 `audit/semantic/section/12-qa/11-component_testing.md`

**Content**: Component testing audit knowledge — test coverage verification, mock patterns, test categories present

### 4.12 `audit/deterministic/section/12-qa/11-component_testing.yaml`

**Content**: Deterministic rules — test files co-located, useLanguage mocked, render tests present, interaction tests present

---

## Phase 5: Tier Metadata (0 files changed)

### 5.1 `plan/core/tiers.yaml`

**Action**: NO CHANGE — structurally identical to base_dev

**Rationale**: React keeps all 16 domains, same tier ordering as base_dev. The differentiator is content within standards/templates/audits, not tier structure.

---

## Verification Checklist

After implementation, verify against this checklist:

### System Identity
- [ ] `00-domain-relationships.md` updated with frontend-specific content
- [ ] No system-name references (Astra/Prati/Prana) in any generated file

### Documentation Standards (14 modified)
- [ ] `01-vision-standards.md` — frontend vision added
- [ ] `03-security-standards.md` — frontend security added
- [ ] `04-feature-standards.md` — frontend feature definition added
- [ ] `05-architecture-standards.md` — component architecture added
- [ ] `06-design-standards.md` — design system + Atomic Design added
- [ ] `07-engineering-standards.md` — React/TypeScript patterns added
- [ ] `08-external-context-standards.md` — technology categories added
- [ ] `09-feature-design-standards.md` — UI feature design added
- [ ] `10-feature-technical-standards.md` — component implementation added
- [ ] `11-prototype-standards.md` — prototyping patterns added
- [ ] `12-qa-standards.md` — Jest/Playwright patterns added
- [ ] `13-implementation-standards.md` — component patterns added
- [ ] `14-build-standards.md` — Vite/Webpack guidance added
- [ ] `16-product-guide-standards.md` — development workflow added

### Generation Templates (13 created)
- [ ] `05-architecture/12-component_architecture.md` — exists
- [ ] `06-design/07-design_tokens.md` — exists
- [ ] `07-engineering/09-hook_conventions.md` — exists
- [ ] `07-engineering/10-component_patterns.md` — exists
- [ ] `07-engineering/11-state_management.md` — exists
- [ ] `07-engineering/12-internationalization.md` — exists
- [ ] `09-feature-design/08-user_flow.md` — exists
- [ ] `10-feature-technical/18-component_implementation.md` — exists
- [ ] `12-qa/10-visual_testing.md` — exists
- [ ] `12-qa/11-component_testing.md` — exists
- [ ] `13-implementation/08-feature_folder_structure.md` — exists
- [ ] `14-build/10-bundle_analysis.md` — exists
- [ ] `16-product-guide/07-development_workflow.md` — exists

### Audit Rules (6 semantic + 6 deterministic)
- [ ] `05-architecture/12-component_architecture.md` + `.yaml` — exist
- [ ] `07-engineering/10-hook_conventions.md` + `.yaml` — exist
- [ ] `07-engineering/11-component_patterns.md` + `.yaml` — exist
- [ ] `07-engineering/12-state_management.md` + `.yaml` — exist
- [ ] `12-qa/10-visual_testing.md` + `.yaml` — exist
- [ ] `12-qa/11-component_testing.md` + `.yaml` — exist

### Tier Metadata
- [ ] `plan/core/tiers.yaml` — unchanged from base_dev

### Content Quality
- [ ] All templates follow existing structure (header/relationships/template/examples/notes)
- [ ] All deterministic YAMLs follow existing structure (rules with id/description/condition/severity/weight/evidence)
- [ ] All semantic MDs follow existing structure (version/engineering_intent/audit_objectives/expected_quality/red_flags/edge_cases/scoring_criteria/output_schema)
- [ ] All documentation standard additions are APPENDS (existing content preserved)
- [ ] No hardcoded system names in any generated file

---

## Execution Order

1. **Phase 1**: System Identity (00-domain-relationships.md)
2. **Phase 3**: Generation Templates (13 new files — no conflicts)
3. **Phase 4**: Audit Rules (6 semantic + 6 deterministic — no conflicts)
4. **Phase 2**: Documentation Standards (14 modified files — append-only)
5. **Phase 5**: Tier Metadata (verify no change needed)

**Rationale**: New files first (no conflicts), then modifications (append-only, low risk), then verification.
