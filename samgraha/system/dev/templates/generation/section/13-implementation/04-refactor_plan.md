# Refactor Plan — Generation Template

> **Domain:** implementation
> **Section:** refactor_plan
> **Source:** `documentation-standards/13-implementation-standards.md` §Refactor Plan
> **Relationships:** `audit/deterministic/document/13-implementation-relationships.yaml`

Generate the Refactor Plan section for an Implementation Plan document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / system_overview | Target Architecture must align with Architecture(05) structural goals |
| `derives_from` | engineering / code_standards | Refactor must comply with Engineering(07) code standards |

## Template

```markdown
## Refactor Plan

### Target Architecture

[1-2 paragraphs: the desired structure after refactoring, referencing Architecture(05)]

### Behavior to Preserve

| Behavior | Current Contract | Verification Method |
|---|---|---|
| [behavior name] | [current guarantee — e.g., latency, response format] | [how to verify it still works] |

### Verification Strategy

[Description of before/after test comparison — test suite must pass identically]
```

## Examples

**Correct:**
> **Target Architecture:** Consolidate the three notification modules (email, sms, push) into a single notification service with a strategy pattern dispatcher, per Architecture(05) service consolidation directive.
> **Behavior to Preserve:** All existing notification delivery contracts — email must arrive within 5 seconds, SMS within 10 seconds, push within 2 seconds. API request/response shapes remain identical.
> **Verification Strategy:** Run full integration test suite (42 tests) before and after refactor. Both runs must produce identical pass/fail results. Benchmark delivery latency for each channel.

**Incorrect:**
> **Target Architecture:** Rewrite the notification system in a new framework.
> **Behavior to Preserve:** None — this is a full rewrite.
> **Verification Strategy:** Manual testing after deployment.
> *Why wrong: Refactor must preserve existing behavior explicitly, not discard it; target architecture lacks specificity; verification strategy relies on manual testing rather than automated regression.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Specify the target architecture by referencing Architecture(05); enumerate every behavior contract that must be preserved with measurable criteria; require automated test suite pass/fail comparison before and after
- **Don't:** Introduce new features or behavior changes in a refactor; rely on manual testing for verification; omit the before/after test comparison

**Minimum content:** 3 subsections (Target Architecture, Behavior to Preserve, Verification Strategy)
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Architecture(05), Engineering(07), Feature(04)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
