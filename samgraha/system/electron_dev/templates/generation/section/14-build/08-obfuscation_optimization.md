# Obfuscation & Optimization — Generation Template

> **Domain:** build
> **Section:** obfuscation_optimization
> **Source:** `documentation-standards/14-build-standards.md` §Obfuscation & Optimization
> **Relationships:** `audit/deterministic/document/14-build-relationships.yaml`

Generate the Obfuscation & Optimization section for a Build Plan document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | engineering / build_standards | Transformation rules must align with Engineering(07) build standards |

## Template

```markdown
## Obfuscation & Optimization

[1-2 sentence description of what obfuscation and optimization covers]
[Statement that this stage is conditional and applies to release builds]

> **Release builds:** [transformations applied — minification, tree-shaking, etc.]
> **Development builds:** [what is preserved — source maps, debug info]
> **Impact:** [measured size reduction — e.g., 40% bundle size reduction]
```

## Examples

**Correct:**
> Release builds apply minification and tree-shaking, reducing bundle size by approximately 40%. Development builds skip obfuscation and preserve source maps for debugging. The size reduction is measured and reported in the build log.

**Incorrect:**
> All builds apply full obfuscation, including development builds. Source maps are never generated.
> *Why wrong: Obfuscating development builds breaks debugging capability — this stage must differentiate between build types and preserve debug info where needed.*

## Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Differentiate transformation rules per build type (release vs. development); quantify impact (e.g., "40% size reduction"); state what debug info is preserved and where
- **Don't:** Apply transformations uniformly across build types; omit measurable impact metrics; skip the trade-off between security/size and debuggability

**Minimum content:** 2 paragraphs
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Engineering(07)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
