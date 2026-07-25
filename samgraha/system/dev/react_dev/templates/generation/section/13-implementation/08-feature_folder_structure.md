# Feature Folder Structure — Generation Template

> **Domain:** implementation
> **Section:** feature_folder_structure
> **Source:** `documentation-standards/13-implementation-standards.md` §Feature Folder Structure
> **Relationships:** `audit/deterministic/document/implementation-relationships.yaml`

Generates feature folder structure with subdirectories, barrel exports, and naming conventions.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| derives_from | feature-technical/component_implementation | Folder layout must support component contracts |
| derives_from | engineering/code_standards | Must follow naming conventions |

## Template

```markdown
# Feature Folder: [FeatureName]

## Directory Structure

```
features/
  [FeatureName]/
    components/
      [ComponentName]/
        index.ts
        [ComponentName].tsx
        [ComponentName].test.tsx
        [ComponentName].stories.tsx
    hooks/
      index.ts
      use[HookName].ts
      use[HookName].test.ts
    types/
      index.ts
      [feature-name].types.ts
    index.ts          # barrel export
    README.md         # feature overview
```

## Barrel Export Pattern

```typescript
// features/[FeatureName]/index.ts
export { FeatureComponent } from './components/FeatureComponent';
export type { FeatureProps } from './types';
export { useFeatureHook } from './hooks';
```

## Naming Conventions

- [ ] Folders: PascalCase (`UserProfile/`)
- [ ] Components: PascalCase (`UserProfile.tsx`)
- [ ] Hooks: camelCase with `use` prefix (`useUserProfile.ts`)
- [ ] Types: kebab-case with `.types.ts` suffix (`user-profile.types.ts`)
- [ ] Tests: co-located with `.test.tsx` suffix
- [ ] Stories: co-located with `.stories.tsx` suffix
```

## Examples

**Correct:**
> `features/UserProfile/` contains `components/UserAvatar/`, `hooks/useUserAvatar.ts`, `types/user-profile.types.ts`, and a barrel `index.ts` re-exporting the public API.

**Incorrect:**
> A flat `components/UserProfile/` folder with all files at the same level, no types directory, and no barrel exports.
> *Why wrong: Violates feature-based structure, missing type isolation, no public API boundary.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** directory-tree-driven
- **Audience:** engineer
- **Do:** Create every subdirectory, maintain barrel exports, use consistent suffixes.
- **Don't:** Mix feature folders, skip barrel exports, use inconsistent casing.

**Required subsections:** Directory Structure, Barrel Export Pattern, Naming Conventions
**Optional subsections:** Shared Features, Cross-Feature Dependencies
**Required diagrams:** directory tree
**Required cross-references:** feature-technical/component_implementation, engineering/code_standards

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
