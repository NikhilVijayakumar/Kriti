# Constraints — Generation Template

> **Domain:** prototype
> **Section:** constraints
> **Source:** `documentation-standards/11-prototype-standards.md` §Constraints
> **Relationships:** `audit/deterministic/document/11-prototype-relationships.yaml`

Generate the Constraints section for a Prototype document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / constraints | Hard constraints must derive from Architecture constraints |
| `derives_from` | security / purpose | Security-related constraints must derive from Security Documentation |
| `derives_from` | engineering / code_standards | Engineering-related constraints must derive from Engineering standards |

## Template

```markdown
## Constraints

| Constraint | Type | Impact |
|------------|------|--------|
| [constraint] | [hard|known-shortcoming] | [effect on prototype] |
```

## Examples

**Correct:**
> | Constraint | Type | Impact |
> |------------|------|--------|
> | No network access | hard | All external services must be mocked locally |
> | Response time not measured | known-shortcoming | Prototype does not validate latency — that is deferred to Engineering |
>
> The hard constraint shapes the entire mock strategy. The known-shortcoming is honest about what the prototype does not prove.

**Incorrect:**
> | Constraint | Type | Impact |
> |------------|------|--------|
> | API latency under 200ms | hard | Response time must meet production SLA |
> *Why wrong: this is a production performance requirement, not a prototype constraint.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Classify each constraint as either hard or known-shortcoming; describe the concrete impact on the prototype; keep constraints specific to the prototype's simulation scope
- **Don't:** List production performance targets as prototype constraints; describe preferences as constraints; leave the Impact column blank

**Minimum content:** 1 constraint list
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Scope

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
