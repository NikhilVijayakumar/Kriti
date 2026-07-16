# User Flow — Generation Template

> **Domain:** feature-design
> **Section:** user_flow
> **Source:** `documentation-standards/09-feature-design-standards.md` §User Flow
> **Relationships:** `audit/deterministic/document/feature-design-relationships.yaml`

Generates navigation patterns, state flow diagrams, and route hierarchy specifications.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| derives_from | feature/requirements | Flow must satisfy all functional requirements |
| derives_from | design/ux_principles | Navigation must align with UX principles |

## Template

```markdown
# User Flow

## Route Hierarchy

| Route | Component | Auth | State |
|---|---|---|---|
| `/` | Home | public | none |
| `/dashboard` | Dashboard | private | user, stats |
| `/settings` | Settings | private | user, preferences |

### Hierarchy Rules

- Parent routes define layout shells; children render into outlets.
- Private routes sit under a single auth-guarded layout.
- Max nesting depth: 3 levels (layout → section → detail).

## Navigation Patterns

- Primary nav: top bar or sidebar, persists across all authenticated routes.
- Secondary nav: tabs within a section, scoped to parent route.
- Breadcrumbs reflect route hierarchy; always present above detail views.

## State Flow Per Route

- Each route declares required state and initialization strategy.
- Loading states show skeletons; error states show retry actions.
- State resets on route exit unless explicitly persisted.

## Deep Linking

- Every routable view must be reachable via direct URL.
- Query params encode non-critical state (filters, sort, page).
- Hash fragments reserved for in-page anchors only.

## Back Button Handling

- Browser back must restore previous route state.
- Modal routes use history push; close pops the entry.
- Never override `popstate` without explicit user confirmation.

## URL State Sync

- URL is source of truth for shareable state (filters, search, page).
- Non-shareable state (hover, focus) stays in component memory.

**Required subsections:** Route Hierarchy, Navigation, State Flow, Deep Linking, Back Button
**Optional subsections:** Transition Animations, Offline Behavior
**Required diagrams:** state flow diagram
**Required cross-references:** requirements, ux_principles, component_architecture
```

**Correct:**
> `/dashboard` route declares auth: private, state: [user, stats], with skeleton loader and error retry.

**Incorrect:**
> `/dash` route with no auth guard and hardcoded user data.
> *Why wrong: Missing auth guard and state initialization violate route declaration rules.*

## Writing Guidance

- **Tone:** descriptive
- **Voice:** imperative
- **Structure:** route tables with state declarations
- **Audience:** designer
- **Do:** Declare every route with auth and state requirements; enforce deep linking.
- **Don't:** Allow routes without auth guards or routes that bypass state initialization.

**Required subsections:** Route Hierarchy, Navigation, State Flow, Deep Linking, Back Button
**Optional subsections:** Transition Animations, Offline Behavior
**Required diagrams:** state flow diagram
**Required cross-references:** requirements, ux_principles, component_architecture

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
