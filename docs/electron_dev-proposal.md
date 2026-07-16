# Desktop Development using Electron - Knowledge System Proposal

## Overview

This proposal defines how to transform `electron_dev` from a clone of `base_dev` into a standalone engineering methodology for building desktop systems using Electron.

**Base System**: `base_dev` (canonical, unchanged)
**Target System**: `electron_dev` (standalone, desktop engineering methodology)

**Core Shift**: This is NOT an Electron guide. This is YOUR desktop engineering methodology implemented with Electron.

---

## Pattern Sources

Patterns derived from real-world implementations. These sources informed the standards but are NOT referenced in the generated standards.

| Source | Location | Patterns Derived |
|--------|----------|------------------|
| **Astra** | `E:\Python\astra` | MVVM, `useDataState<T>()`, Repository pattern, Platform neutrality, IPC abstraction, `IpcService` |
| **Prana** | `E:\Python\Prana` | Application Runtime (lifecycle state machine), Service Registry (13 services), Event System (pub/sub), Background Jobs (state machine), Sync Engine (mirror constraint), Storage Domains (Local/Vault/Document/Sheet), Configuration Lock (immutable post-operational) |
| **Prati** | `E:\Python\Prati` | Atomic Design, Theme sovereignty, Stateless UI |

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
- Framework-specific guidance (Electron, Node.js, etc.)
- Self-contained, independently usable standards

**How patterns are "baked in":**

| External Pattern | Standardized As (In Standard) |
|------------------|------------------------------|
| Astra MVVM | MVVM pattern (generic) |
| Astra `useDataState<T>()` | State management hooks (generic) |
| Astra Repository pattern | Data access layer (generic) |
| Astra Platform neutrality | Platform-agnostic service abstraction |
| Astra IPC abstraction | IPC abstraction layer (generic) |
| Astra `IpcService` | IPC service interface (generic) |
| Prana Application Runtime | Application lifecycle management |
| Prana Service Registry | Service registration and discovery |
| Prana Event System | Pub/sub event architecture |
| Prana Background Jobs | Background job state machine |
| Prana Sync Engine | Data synchronization patterns |
| Prana Storage Domains | Data persistence layers |
| Prana Configuration Lock | Immutable configuration post-operational |
| Prati Atomic Design | Component hierarchy (Atoms→Molecules→Organisms→Templates) |
| Prati Theme sovereignty | Token-based theming |
| Prati Stateless UI | Functional components, hooks-only state |

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

These files are NOT shared across systems. When creating `electron_dev`, copy these from `base_dev` then modify to reflect the system's domain scope.

---

## Domain Scope

### Domains KEPT (16 of 16)

| Tier | Domain | Standard File | Action |
|------|--------|---------------|--------|
| 1 | 01-vision | `01-vision-standards.md` | KEEP + add desktop engineering vision |
| 1 | 02-philosophy | `02-philosophy-standards.md` | KEEP |
| 2 | 03-security | `03-security-standards.md` | KEEP + add desktop security |
| 2 | 04-feature | `04-feature-standards.md` | KEEP + add desktop feature definition |
| 2 | 05-architecture | `05-architecture-standards.md` | KEEP + add process architecture |
| 2 | 06-design | `06-design-standards.md` | KEEP + add design system |
| 2 | 07-engineering | `07-engineering-standards.md` | KEEP + add Electron/Node.js patterns |
| 2 | 08-external-context | `08-external-context-standards.md` | KEEP + add technology categories |
| 3 | 09-feature-design | `09-feature-design-standards.md` | KEEP + add UI feature design |
| 3 | 10-feature-technical | `10-feature-technical-standards.md` | KEEP + add implementation guidance |
| 4 | 11-prototype | `11-prototype-standards.md` | KEEP + add prototyping |
| 5 | 13-implementation | `13-implementation-standards.md` | KEEP + add process patterns |
| 6 | 12-qa | `12-qa-standards.md` | KEEP + add Jest/Playwright patterns |
| 7 | 14-build | `14-build-standards.md` | KEEP + add packaging/distribution |
| 8 | 15-readme | `15-readme-standards.md` | KEEP + add desktop README |
| 8 | 16-product-guide | `16-product-guide-standards.md` | KEEP + add development workflow |

### Tier Reordering

| Tier | base_dev | electron_dev |
|------|----------|--------------|
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

### 05-architecture (11 existing, ADD 2 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add desktop architecture purpose |
| 02 | `02-system_overview.md` | MODIFY — add multi-process overview |
| 03 | `03-component_model.md` | MODIFY — add process architecture (Main/Renderer/Preload) |
| 04 | `04-communication_paths.md` | MODIFY — add IPC patterns |
| 05 | `05-data_flow.md` | MODIFY — add storage domains |
| 06 | `06-security_considerations.md` | KEEP — generic |
| 07 | `07-rationale.md` | MODIFY — add module structure rationale |
| 08 | `08-constraints.md` | MODIFY — add OS integration constraints |
| 09 | `09-traceability.md` | KEEP — generic |
| 10 | `10-operational_readiness.md` | KEEP — generic |
| 11 | `11-observability.md` | KEEP — generic |
| 12 | `12-process_architecture.md` | **NEW SLOT** — Main, Renderer, Preload |
| 13 | `13-ipc_patterns.md` | **NEW SLOT** — IPC abstraction, channel design |

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
| 01 | `01-guiding_principles.md` | MODIFY — add Electron conventions |
| 02 | `02-rationale.md` | MODIFY — add rationale for engineering choices |
| 03 | `03-build_standards.md` | MODIFY — add build standards |
| 04 | `04-testing_standards.md` | MODIFY — add testing standards |
| 05 | `05-purpose.md` | MODIFY — add config lock pattern |
| 06 | `06-code_standards.md` | MODIFY — add TypeScript, Node.js |
| 07 | `07-constraints.md` | MODIFY — add process-level error constraints |
| 08 | `08-traceability.md` | KEEP — generic |
| 09 | `09-service_registry.md` | **NEW SLOT** — service registration, lifecycle |
| 10 | `10-event_system.md` | **NEW SLOT** — pub/sub, pattern routing |
| 11 | `11-background_jobs.md` | **NEW SLOT** — job state machine |
| 12 | `12-platform_services.md` | **NEW SLOT** — OS integration, native APIs |

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

### 10-feature-technical (17 existing, ADD 2 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add desktop implementation purpose |
| 02-17 | (existing slots) | KEEP — generic |
| 18 | `18-process_implementation.md` | **NEW SLOT** — Main, Renderer, Preload |
| 19 | `19-ipc_implementation.md` | **NEW SLOT** — channel design, IPC service |

### 12-qa (9 existing, ADD 3 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add Jest patterns |
| 02-09 | (existing slots) | KEEP — generic |
| 10 | `10-visual_testing.md` | **NEW SLOT** — Playwright, Storybook |
| 11 | `11-component_testing.md` | **NEW SLOT** — React Testing Library |
| 12 | `12-process_testing.md` | **NEW SLOT** — IPC testing, process isolation |

### 13-implementation (6 existing, ADD 1 new)

| Slot | Actual File on Disk | Action |
|------|---------------------|--------|
| 01 | `01-purpose.md` | MODIFY — add feature scaffold plan |
| 02 | (gap — slot 02 missing on disk) | — |
| 03-07 | (existing slots) | KEEP — generic |
| 08 | `08-feature_folder_structure.md` | **NEW SLOT** — directory layout |

### 14-build (8 existing, ADD 2 new)

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
| 10 | `10-packaging.md` | **NEW SLOT** — electron-builder, auto-update |
| 11 | `11-distribution.md` | **NEW SLOT** — platforms, signing |

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

> How do we build desktop systems in our ecosystem?

**Answer**: We build secure, performant, maintainable desktop systems with clear process boundaries. Electron is our implementation technology, not our architecture.

### 2. Architecture

**Principle**: Architecture is YOURS. Electron is one implementation detail.

| Pattern | Standard | Alternative | Override Allowed |
|---------|----------|-------------|-----------------|
| Process Isolation | Required (Main/Renderer/Preload) | Custom process model | Yes, with justification |
| IPC Abstraction | Required (service interface) | Direct channel usage | No |
| Service Registry | Required (lifecycle management) | Ad-hoc initialization | No |
| Event System | Required (pub/sub with pattern routing) | Direct callbacks | No |
| Storage Domains | Required (Local/Vault/Document/Sheet) | Custom domains | Yes, document in 00-domain-relationships |
| Configuration Lock | Required (immutable post-operational) | Mutable config | No |

### 3. Engineering

**Principle**: Engineering is MORE than Electron. Framework is one part.

- TypeScript EVERYWHERE
- Strict process boundaries (Main/Renderer/Preload)
- No direct DOM access from Main process
- No Node.js APIs in Renderer (use Preload)
- IPC abstraction (no direct channel usage)
- Service registry for lifecycle management
- Event system for cross-process communication
- Background jobs with state machine
- Storage domains for data isolation

### 4. Audit

**Principle**: Audit ARCHITECTURAL DRIFT, not just syntax.

Weight and severity adjustments happen inside `audit/deterministic/{domain}/*.yaml` files, NOT in `calculation/*.yaml`. The calculation layer is generic and shared across all systems.

### 5. Templates

Content is injected into existing numbered slots per domain. See **Section Slot Mapping** above.

### 6. Product Guide

Answers "How do we work?" not "What is Electron?"

### 7. Engineering Decisions

| Decision | Preferred Option | Alternative | Reason |
|----------|-----------------|-------------|--------|
| Framework | Electron | Tauri, Neutralinojs | Ecosystem, maturity |
| IPC | IPC abstraction | Direct channels | Security, maintainability |
| State Management | Zustand | Redux, Context | Simplicity, performance |
| Styling | CSS Modules | Styled-components, Tailwind | Co-location, no runtime |
| Testing | Jest + Playwright | Vitest, Cypress | Coverage, E2E |
| Build | electron-builder | electron-forge | Flexibility, config |

### 8. External Context

| Category | Purpose | Options |
|----------|---------|---------|
| IPC Framework | Process communication | IPC abstraction, direct channels |
| State Management | Application state | Zustand, Redux Toolkit, Jotai |
| Styling | CSS solution | CSS Modules, Styled-components, Tailwind |
| Forms | Form handling | React Hook Form, Formik |
| Data Fetching | API integration | TanStack Query, SWR |
| Storage | Data persistence | SQLite, LevelDB, filesystem |
| Auto-Update | Application updates | electron-updater, Squirrel |
| Packaging | Distribution | electron-builder, electron-forge |

---

## New Subsystems (Not Integrated with Audit Script Pipeline)

The following are NEW artifact types proposed for creation. They are NOT part of the existing `script/` audit verification infrastructure (mapping.yaml, manifests, schema files). They would require a separate subsystem if implemented.

### Feature Scaffolding (Proposed)

| Script | Purpose |
|--------|---------|
| `create-feature.sh/ps1` | Scaffold complete feature (Main + Renderer + Preload + IPC) |
| `create-service.sh/ps1` | Scaffold service with lifecycle |
| `create-ipc-service.sh/ps1` | Scaffold IPC service with channels |
| `create-job.sh/ps1` | Scaffold background job with state machine |

---

## Files to Modify

### Domain Files

| File | Action |
|------|--------|
| `00-domain-relationships.md` | REPLACE — system-specific domain tier ordering (16 domains, same as base_dev but reordered) |
| `plan/core/tiers.yaml` | REPLACE — derived from system's 00-domain-relationships.md |
| `documentation-standards/01-vision-standards.md` | ADD — desktop engineering vision |
| `documentation-standards/02-philosophy-standards.md` | KEEP |
| `documentation-standards/03-security-standards.md` | ADD — desktop security, process isolation |
| `documentation-standards/04-feature-standards.md` | ADD — desktop feature definition |
| `documentation-standards/05-architecture-standards.md` | ADD — process architecture, IPC patterns |
| `documentation-standards/06-design-standards.md` | ADD — design system, tokens |
| `documentation-standards/07-engineering-standards.md` | ADD — Electron conventions, service registry |
| `documentation-standards/08-external-context-standards.md` | ADD — technology categories |
| `documentation-standards/09-feature-design-standards.md` | ADD — UI feature design |
| `documentation-standards/10-feature-technical-standards.md` | ADD — process implementation |
| `documentation-standards/11-prototype-standards.md` | ADD — prototyping |
| `documentation-standards/12-qa-standards.md` | ADD — Jest, Playwright, process testing |
| `documentation-standards/13-implementation-standards.md` | ADD — process patterns |
| `documentation-standards/14-build-standards.md` | ADD — packaging, distribution |
| `documentation-standards/15-readme-standards.md` | ADD — desktop README |
| `documentation-standards/16-product-guide-standards.md` | ADD — development workflow |

### Audit Knowledge (nested domain folders)

| Path | Content |
|------|---------|
| `audit/semantic/section/05-architecture/12-process_architecture.md` | Process rules |
| `audit/semantic/section/05-architecture/13-ipc_patterns.md` | IPC rules |
| `audit/semantic/section/07-engineering/10-service_registry.md` | Service registry rules |
| `audit/semantic/section/07-engineering/11-event_system.md` | Event system rules |
| `audit/semantic/section/07-engineering/12-background_jobs.md` | Background job rules |
| `audit/semantic/section/07-engineering/13-platform_services.md` | Platform service rules |
| `audit/semantic/section/12-qa/10-visual_testing.md` | Visual testing rules |
| `audit/semantic/section/12-qa/11-component_testing.md` | Component testing rules |
| `audit/semantic/section/12-qa/12-process_testing.md` | Process testing rules |
| `audit/semantic/section/14-build/09-packaging.md` | Packaging rules |
| `audit/semantic/section/14-build/10-distribution.md` | Distribution rules |

### Generation Templates (nested domain folders)

| Path | Content |
|------|---------|
| `templates/generation/section/05-architecture/12-process_architecture.md` | Main, Renderer, Preload |
| `templates/generation/section/05-architecture/13-ipc_patterns.md` | IPC abstraction, channel design |
| `templates/generation/section/06-design/07-design_tokens.md` | Token hierarchy, theme sovereignty |
| `templates/generation/section/07-engineering/09-service_registry.md` | Service registration, lifecycle |
| `templates/generation/section/07-engineering/10-event_system.md` | Pub/sub, pattern routing |
| `templates/generation/section/07-engineering/11-background_jobs.md` | Job state machine |
| `templates/generation/section/07-engineering/12-platform_services.md` | OS integration, native APIs |
| `templates/generation/section/09-feature-design/08-user_flow.md` | Navigation, state flow |
| `templates/generation/section/10-feature-technical/18-process_implementation.md` | Main, Renderer, Preload |
| `templates/generation/section/10-feature-technical/19-ipc_implementation.md` | Channel design, IPC service |
| `templates/generation/section/12-qa/10-visual_testing.md` | Playwright, Storybook |
| `templates/generation/section/12-qa/11-component_testing.md` | React Testing Library |
| `templates/generation/section/12-qa/12-process_testing.md` | IPC testing, process isolation |
| `templates/generation/section/13-implementation/08-feature_folder_structure.md` | Directory layout |
| `templates/generation/section/14-build/10-packaging.md` | electron-builder, auto-update |
| `templates/generation/section/14-build/11-distribution.md` | Platforms, signing |
| `templates/generation/section/16-product-guide/07-development_workflow.md` | How we work |

---

## Success Criteria

- [ ] `electron_dev` is independently usable
- [ ] Answers "How do we build desktop systems?" not "What is Electron?"
- [ ] Documents YOUR process architecture, not framework documentation
- [ ] Preserves core philosophy of `base_dev`
- [ ] Provides clear engineering methodology
- [ ] Enables consistent decision-making across projects
- [ ] All file paths match engine glob patterns
- [ ] No external system references in generated standards

---

# Implementation Plan

This section defines the complete execution plan for transforming `electron_dev`. Each phase lists exact files, actions, and content requirements. Verification = compare implemented file against plan entry.

---

## Phase 1: System Identity (1 file)

### 1.1 Update `00-domain-relationships.md`

**Action**: REWRITE — desktop-specific cross-domain relationships

**File**: `E:\Python\Kriti\samgraha\system\electron_dev\00-domain-relationships.md`

**Content Requirements**:
- 16 domains listed with desktop-specific tier purposes
- Cross-domain dependency matrix reflecting desktop concerns (e.g., 05-architecture depends on process isolation, 07-engineering depends on IPC patterns, service registry)
- Section breakdowns for each domain with desktop-specific section names
- Tier summary table showing desktop engineering tier purposes
- Relationship table showing how domains interact in desktop context
- Frontend-Specific Domain Concerns table (desktop variant)

**Verification**: Compare domain relationships against base_dev version — all system-name references removed, desktop context added

---

## Phase 2: Documentation Standards (14 files modified, 2 untouched)

All modifications are **APPENDS** to existing content — no existing content removed.

### 2.1 `01-vision-standards.md`

**Action**: ADD desktop engineering vision

**Content to add**:
- Desktop-specific vision statements: "We build secure, performant, maintainable desktop systems with clear process boundaries"
- Process isolation as architectural principle
- Native platform integration as engineering concern
- Offline-first capability as design constraint
- Auto-update as distribution requirement

### 2.2 `03-security-standards.md`

**Action**: ADD desktop security

**Content to add**:
- Process isolation security (Main/Renderer/Preload boundaries)
- Context isolation requirements (contextIsolation: true)
- Node.js API restrictions in Renderer
- IPC channel authorization patterns
- Code signing requirements
- Sandboxing and permissions model
- Secure storage patterns (keychain, encrypted storage)

### 2.3 `04-feature-standards.md`

**Action**: ADD desktop feature definition

**Content to add**:
- Feature = process component + IPC channels + service + tests
- Feature folder structure conventions (main/, renderer/, preload/)
- Feature isolation across process boundaries
- Feature-level IPC ownership
- Feature composition via service registry

### 2.4 `05-architecture-standards.md`

**Action**: ADD process architecture, IPC patterns

**Content to add**:
- Three-process architecture (Main, Renderer, Preload)
- IPC abstraction layer (service interface, not direct channels)
- Channel naming conventions (domain:action)
- Storage domain architecture (Local/Vault/Document)
- Service registry pattern (lifecycle management)
- Event system architecture (pub/sub with pattern routing)
- Configuration lock pattern (immutable post-operational)

### 2.5 `06-design-standards.md`

**Action**: ADD design system, tokens

**Content to add**:
- Atomic Design methodology (atoms → molecules → organisms → templates)
- Design token hierarchy (JS → theme → CSS custom properties)
- Theme sovereignty invariant: all visual values from tokens
- Native window chrome design (title bar, menus)
- Platform-specific styling (macOS vs Windows vs Linux)
- Dark mode architecture (token layer switching)

### 2.6 `07-engineering-standards.md`

**Action**: ADD Electron/Node.js patterns

**Content to add**:
- TypeScript everywhere — strict mode, no `any`
- Functional components only — no class components (except ErrorBoundary)
- Hooks for ALL state and side effects
- IPC abstraction patterns (invoke/send/receive)
- Service registry pattern (registration, lifecycle, discovery)
- Event system pattern (pub/sub, channel routing)
- Background job pattern (state machine: INIT → LOADING → COMPLETED)
- Platform service patterns (OS integration, native APIs)

### 2.7 `08-external-context-standards.md`

**Action**: ADD technology categories

**Content to add**:
- IPC Framework category: abstraction vs direct channels
- State Management category: no external libs preference, Context + useState
- Styling category: CSS-in-JS vs CSS modules decision framework
- Testing category: Jest + Playwright preference
- Build category: electron-builder preference
- Storage category: SQLite, LevelDB, filesystem
- Auto-Update category: electron-updater patterns
- Packaging category: platform-specific distribution

### 2.8 `09-feature-design-standards.md`

**Action**: ADD UI feature design

**Content to add**:
- Feature = user flow + process component + IPC map
- Component hierarchy per feature (which atoms/molecules/organisms)
- IPC channel ownership per feature (which channels, which handlers)
- Service ownership per feature (which services, which lifecycle)
- Native integration per feature (tray, menu, dialog)

### 2.9 `10-feature-technical-standards.md`

**Action**: ADD process implementation

**Content to add**:
- Process implementation checklist: IPC channels → handlers → preload → tests
- Service implementation pattern: registration → lifecycle → disposal
- IPC implementation pattern: channel definition → handler → abstraction
- Type implementation: channel types → handler types → response types
- Test implementation: unit test → IPC test → process test

### 2.10 `11-prototype-standards.md`

**Action**: ADD prototyping patterns

**Content to add**:
- Prototype = throwaway Electron app, not production code
- Mock IPC channels for prototype testing
- Prototype data patterns (fixture storage)
- User testing with prototypes
- Prototype → production conversion checklist

### 2.11 `12-qa-standards.md`

**Action**: ADD Jest/Playwright patterns

**Content to add**:
- Component testing: render, interaction, context integration
- IPC testing: mock electronAPI, verify channel calls
- Process testing: verify process isolation, preload behavior
- Visual regression: Playwright screenshot testing
- Cross-platform testing: macOS, Windows, Linux matrices
- Auto-update testing: mock updater, verify flow

### 2.12 `13-implementation-standards.md`

**Action**: ADD process patterns

**Content to add**:
- Process folder structure: main/, renderer/, preload/
- Service folder structure: services/ServiceName/
- IPC folder structure: ipc/channels/, ipc/handlers/
- Barrel export conventions at each tier
- Feature folder structure: feature/FeatureName/main/, feature/FeatureName/renderer/

### 2.13 `14-build-standards.md`

**Action**: ADD packaging/distribution

**Content to add**:
- electron-builder configuration patterns
- Code signing setup (macOS, Windows)
- Auto-update configuration (electron-updater)
- Platform-specific build targets
- Bundle optimization for Electron
- Native module handling
- Distribution channels (direct download, store)

### 2.14 `16-product-guide-standards.md`

**Action**: ADD development workflow

**Content to add**:
- How we work: feature branch → process component → IPC → tests → review → merge
- Desktop development workflow (design → implement → test → document)
- Service contribution process
- IPC channel documentation
- Cross-platform testing checklist
- Auto-update verification checklist

### 2.15 Files NOT modified

- `02-philosophy-standards.md` — KEEP (generic, no desktop additions needed)
- `15-readme-standards.md` — KEEP (generic)

---

## Phase 3: New Generation Templates (17 files)

All new files follow existing template structure: header with version/engineering_intent/purpose, relationships section, template section with numbered instructions, examples section, notes section.

### 3.1 `templates/generation/section/05-architecture/12-process_architecture.md`

**Content**: Three-process architecture (Main, Renderer, Preload), process ownership boundaries, context isolation requirements, preload script patterns, contextBridge usage

### 3.2 `templates/generation/section/05-architecture/13-ipc_patterns.md`

**Content**: IPC abstraction layer (ITransportService), channel naming conventions (domain:action), invoke/send/receive patterns, typed channel maps, handler registration

### 3.3 `templates/generation/section/06-design/07-design_tokens.md`

**Content**: Three-layer token architecture (JS constants → theme → CSS custom properties), theme sovereignty rules, dark mode implementation, native window chrome tokens

### 3.4 `templates/generation/section/07-engineering/09-service_registry.md`

**Content**: Service registration pattern, lifecycle management (init/ dispose), singleton factories, DI container patterns, service discovery

### 3.5 `templates/generation/section/07-engineering/10-event_system.md`

**Content**: Pub/sub event architecture, channel-based routing, typed event maps, unsubscribe patterns, event-to-state wiring

### 3.6 `templates/generation/section/07-engineering/11-background_jobs.md`

**Content**: Job state machine (INIT → LOADING → COMPLETED), progress tracking, cancellation tokens, retry logic, concurrent job handling

### 3.7 `templates/generation/section/07-engineering/12-platform_services.md`

**Content**: OS integration patterns (tray, menu, dialog), native API abstraction, platform detection, clipboard, shell, nativeImage usage

### 3.8 `templates/generation/section/09-feature-design/08-user_flow.md`

**Content**: Navigation patterns in desktop context, window management, multi-window flows, deep linking, protocol handlers

### 3.9 `templates/generation/section/10-feature-technical/18-process_implementation.md`

**Content**: Process implementation checklist: IPC channels → handlers → preload → tests. Main process component, Renderer component, Preload script.

### 3.10 `templates/generation/section/10-feature-technical/19-ipc_implementation.md`

**Content**: Channel definition pattern, handler registration, IPC abstraction wrapping, typed channel maps, error normalization to ServerResponse

### 3.11 `templates/generation/section/12-qa/10-visual_testing.md`

**Content**: Playwright screenshot testing, cross-platform visual comparison, baseline management, CI gate configuration

### 3.12 `templates/generation/section/12-qa/11-component_testing.md`

**Content**: Jest + Testing Library patterns, mock electronAPI conventions, render/interaction/context test categories, co-located test files

### 3.13 `templates/generation/section/12-qa/12-process_testing.md`

**Content**: IPC testing patterns, process isolation verification, preload behavior testing, mock main process, cross-process test coordination

### 3.14 `templates/generation/section/13-implementation/08-feature_folder_structure.md`

**Content**: Feature folder structure: feature/FeatureName/main/, feature/FeatureName/renderer/, feature/FeatureName/preload/, barrel exports, naming conventions

### 3.15 `templates/generation/section/14-build/10-packaging.md`

**Content**: electron-builder configuration, code signing setup, auto-update configuration, platform-specific targets, native module handling

### 3.16 `templates/generation/section/14-build/11-distribution.md`

**Content**: Distribution channels (direct download, stores), platform-specific signing, notarization, update server setup, rollback patterns

### 3.17 `templates/generation/section/16-product-guide/07-development_workflow.md`

**Content**: How we work: feature branch → process component → IPC → tests → review → merge. Service contribution workflow. Cross-platform testing checklist.

---

## Phase 4: New Audit Rules (11 semantic + 11 deterministic)

### 4.1 `audit/semantic/section/05-architecture/12-process_architecture.md`

**Content**: Process architecture audit knowledge — scoring criteria, expected patterns, red flags, edge cases for process isolation compliance

### 4.2 `audit/deterministic/section/05-architecture/12-process_architecture.yaml`

**Content**: Deterministic rules — three processes defined, context isolation enabled, preload scripts present, no Node.js in renderer

### 4.3 `audit/semantic/section/05-architecture/13-ipc_patterns.md`

**Content**: IPC patterns audit knowledge — abstraction layer verification, channel naming compliance, handler registration patterns

### 4.4 `audit/deterministic/section/05-architecture/13-ipc_patterns.yaml`

**Content**: Deterministic rules — IPC abstraction used, channel naming follows domain:action, no direct ipcRenderer in renderer

### 4.5 `audit/semantic/section/07-engineering/09-service_registry.md`

**Content**: Service registry audit knowledge — registration patterns, lifecycle management, singleton verification

### 4.6 `audit/deterministic/section/07-engineering/09-service_registry.yaml`

**Content**: Deterministic rules — services registered, lifecycle methods present, no ad-hoc initialization

### 4.7 `audit/semantic/section/07-engineering/10-event_system.md`

**Content**: Event system audit knowledge — pub/sub patterns, channel routing, unsubscribe verification

### 4.8 `audit/deterministic/section/07-engineering/10-event_system.yaml`

**Content**: Deterministic rules — event system used, unsubscribe functions returned, no direct callbacks for cross-process events

### 4.9 `audit/semantic/section/07-engineering/11-background_jobs.md`

**Content**: Background jobs audit knowledge — state machine patterns, progress tracking, cancellation support

### 4.10 `audit/deterministic/section/07-engineering/11-background_jobs.yaml`

**Content**: Deterministic rules — state machine defined, progress tracking present, cancellation tokens available

### 4.11 `audit/semantic/section/07-engineering/12-platform_services.md`

**Content**: Platform services audit knowledge — OS integration patterns, native API abstraction, platform detection

### 4.12 `audit/deterministic/section/07-engineering/12-platform_services.yaml`

**Content**: Deterministic rules — platform services abstracted, native APIs behind interface, platform detection present

### 4.13 `audit/semantic/section/12-qa/10-visual_testing.md`

**Content**: Visual testing audit knowledge — screenshot baselines, cross-platform comparison, CI gate configuration

### 4.14 `audit/deterministic/section/12-qa/10-visual_testing.yaml`

**Content**: Deterministic rules — visual tests exist, baselines stored, CI gates configured

### 4.15 `audit/semantic/section/12-qa/11-component_testing.md`

**Content**: Component testing audit knowledge — test co-location, mock patterns, test categories

### 4.16 `audit/deterministic/section/12-qa/11-component_testing.yaml`

**Content**: Deterministic rules — test files co-located, electronAPI mocked, render tests present

### 4.17 `audit/semantic/section/12-qa/12-process_testing.md`

**Content**: Process testing audit knowledge — IPC testing, process isolation verification, preload testing

### 4.18 `audit/deterministic/section/12-qa/12-process_testing.yaml`

**Content**: Deterministic rules — IPC tests present, process isolation tested, preload behavior verified

### 4.19 `audit/semantic/section/14-build/09-packaging.md`

**Content**: Packaging audit knowledge — electron-builder config, code signing, auto-update setup

### 4.20 `audit/deterministic/section/14-build/09-packaging.yaml`

**Content**: Deterministic rules — packaging config present, code signing configured, auto-update enabled

### 4.21 `audit/semantic/section/14-build/10-distribution.md`

**Content**: Distribution audit knowledge — platform targets, signing, notarization, update server

### 4.22 `audit/deterministic/section/14-build/10-distribution.yaml`

**Content**: Deterministic rules — distribution targets defined, signing configured, notarization setup

---

## Phase 5: Tier Metadata (0 files changed)

### 5.1 `plan/core/tiers.yaml`

**Action**: NO CHANGE — structurally identical to base_dev

**Rationale**: Electron keeps all 16 domains, same tier ordering as base_dev. The differentiator is content within standards/templates/audits, not tier structure.

---

## Verification Checklist

After implementation, verify against this checklist:

### System Identity
- [ ] `00-domain-relationships.md` updated with desktop-specific content
- [ ] No system-name references (Astra/Prati/Prana) in any generated file

### Documentation Standards (14 modified)
- [ ] `01-vision-standards.md` — desktop vision added
- [ ] `03-security-standards.md` — desktop security added
- [ ] `04-feature-standards.md` — desktop feature definition added
- [ ] `05-architecture-standards.md` — process architecture + IPC added
- [ ] `06-design-standards.md` — design system + tokens added
- [ ] `07-engineering-standards.md` — Electron/Node.js patterns added
- [ ] `08-external-context-standards.md` — technology categories added
- [ ] `09-feature-design-standards.md` — UI feature design added
- [ ] `10-feature-technical-standards.md` — process implementation added
- [ ] `11-prototype-standards.md` — prototyping patterns added
- [ ] `12-qa-standards.md` — Jest/Playwright/process testing added
- [ ] `13-implementation-standards.md` — process patterns added
- [ ] `14-build-standards.md` — packaging/distribution added
- [ ] `16-product-guide-standards.md` — development workflow added

### Generation Templates (17 created)
- [ ] `05-architecture/12-process_architecture.md` — exists
- [ ] `05-architecture/13-ipc_patterns.md` — exists
- [ ] `06-design/07-design_tokens.md` — exists
- [ ] `07-engineering/09-service_registry.md` — exists
- [ ] `07-engineering/10-event_system.md` — exists
- [ ] `07-engineering/11-background_jobs.md` — exists
- [ ] `07-engineering/12-platform_services.md` — exists
- [ ] `09-feature-design/08-user_flow.md` — exists
- [ ] `10-feature-technical/18-process_implementation.md` — exists
- [ ] `10-feature-technical/19-ipc_implementation.md` — exists
- [ ] `12-qa/10-visual_testing.md` — exists
- [ ] `12-qa/11-component_testing.md` — exists
- [ ] `12-qa/12-process_testing.md` — exists
- [ ] `13-implementation/08-feature_folder_structure.md` — exists
- [ ] `14-build/10-packaging.md` — exists
- [ ] `14-build/11-distribution.md` — exists
- [ ] `16-product-guide/07-development_workflow.md` — exists

### Audit Rules (11 semantic + 11 deterministic)
- [ ] `05-architecture/12-process_architecture.md` + `.yaml` — exist
- [ ] `05-architecture/13-ipc_patterns.md` + `.yaml` — exist
- [ ] `07-engineering/09-service_registry.md` + `.yaml` — exist
- [ ] `07-engineering/10-event_system.md` + `.yaml` — exist
- [ ] `07-engineering/11-background_jobs.md` + `.yaml` — exist
- [ ] `07-engineering/12-platform_services.md` + `.yaml` — exist
- [ ] `12-qa/10-visual_testing.md` + `.yaml` — exist
- [ ] `12-qa/11-component_testing.md` + `.yaml` — exist
- [ ] `12-qa/12-process_testing.md` + `.yaml` — exist
- [ ] `14-build/09-packaging.md` + `.yaml` — exist
- [ ] `14-build/10-distribution.md` + `.yaml` — exist

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
2. **Phase 3**: Generation Templates (17 new files — no conflicts)
3. **Phase 4**: Audit Rules (11 semantic + 11 deterministic — no conflicts)
4. **Phase 2**: Documentation Standards (14 modified files — append-only)
5. **Phase 5**: Tier Metadata (verify no change needed)

**Rationale**: New files first (no conflicts), then modifications (append-only, low risk), then verification.

---

## Pattern Source Reference (Astra)

Desktop patterns derived from Astra. All references confined to this proposal — not in generated standards.

| Astra Pattern | Standardized As |
|---------------|-----------------|
| IpcService (invoke/send/receive) | IPC abstraction layer |
| ITransportService interface | Platform-agnostic transport |
| channel naming (domain:action) | Channel naming convention |
| ServerResponse<T> | Uniform response contract |
| getApiService factory | Singleton service factory |
| useDataState state machine | Background job state machine |
| contextBridge pattern | Preload script pattern |
| Platform type ('WEB' \| 'ELECTRON') | Platform detection |
| readonly fields, private constructors | Configuration lock pattern |
| mountedRef unmount guard | Component lifecycle safety |
