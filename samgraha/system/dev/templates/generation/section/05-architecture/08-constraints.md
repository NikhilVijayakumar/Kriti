# Constraints — Generation Template

> **Domain:** architecture
> **Section:** constraints
> **Source:** `documentation-standards/05-architecture-standards.md` §Constraints
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the Constraints section for an Architecture document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `constrains` | engineering / code_standards | Constraints defined here must be respected by Engineering's code standards |

## Template

```markdown
## Constraints

### Hard Constraints
[Constraints that cannot be violated — with source and reason for each]

### Soft Constraints
[Preferences and guidelines that should be followed unless justified]

### Platform Constraints
[Hardware, OS, or runtime constraints that shape architecture]
```

## Examples

**Correct:**
> **Hard Constraints**
> - **Offline-first operation** (source: Platform Pillars) — the system must remain functional with no network connection; no component may assume live connectivity.
> - **Single-writer data ownership** (source: External Context) — the upstream partner system requires exactly one writer per record to avoid conflict resolution on their side.
>
> **Soft Constraints**
> - Prefer components that can be tested in isolation, unless a hard constraint makes isolation impractical.

**Incorrect:**
> The system must use Rust 1.75+ and target a minimum of 4GB RAM.
> *Why wrong: states a language version and hardware minimum as if they were architectural constraints, without a source or architectural reason — these are either Engineering-level technology decisions or unsourced assertions, not sourced structural bounds.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Attribute every constraint to its source (External Context, Platform Pillars, organizational rule); separate hard constraints from soft preferences explicitly; state the consequence of violating a hard constraint
- **Don't:** List a constraint without a source; mix implementation-level limits (language versions, dependency pins) into architectural constraints; present preferences as if they were immovable

**Required subsections:** Hard Constraints
**Optional subsections:** Soft Constraints, Platform Constraints
**Required diagrams:** none
**Required cross-references:** External Context, Platform Pillars(01)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
