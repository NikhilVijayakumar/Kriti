# Size Checks — Generation Template

> **Domain:** build
> **Section:** size_checks
> **Source:** `documentation-standards/14-build-standards.md` §Size Checks
> **Relationships:** `audit/deterministic/document/14-build-relationships.yaml`

Generate the Size Checks section for a Build Plan document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | engineering / build_standards | Size limits must align with Engineering(07) build standards |

## Template

```markdown
## Size Checks

[1-2 sentence description of what size checks cover]
[Statement that this stage is conditional and applies to size-sensitive projects]

> **Applicability:** [projects with size constraints — mobile, embedded, CLI]
> **Limits:**
> | Artifact Type | Max Size | Measurement | Enforcement |
> |---|---|---|---|
> | [artifact type] | [size limit] | [compressed/uncompressed] | [block/warn] |
```

## Examples

**Correct:**
> Size checks enforce a 5 MB limit on the distributable package. Measurement uses uncompressed artifact size. Exceeding the limit blocks the build with an actionable error message.

**Incorrect:**
> Size checks monitor documentation line counts and report the total without any thresholds or enforcement.
> *Why wrong: Without defined limits and enforcement actions, size checks provide no value — they must specify measurable thresholds and what happens when they are exceeded.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Define numeric limits per artifact type (e.g., "5 MB for distributable package"); specify the measurement method (compressed vs. uncompressed); state enforcement action (block vs. warn)
- **Don't:** Leave size limits undefined or use relative terms like "reasonable"; omit the measurement method; skip enforcement action definition

**Minimum content:** 2 paragraphs
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Engineering(07)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
