# Scope — Generation Template

> **Domain:** prototype
> **Section:** scope
> **Source:** `documentation-standards/11-prototype-standards.md` §Scope
> **Relationships:** `audit/deterministic/document/11-prototype-relationships.yaml`

Generate the Scope section for a Prototype document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | Scope items must trace to feature requirements |
| `derives_from` | feature-technical / component_responsibilities | Scope boundaries must align with component responsibilities |

## Template

```markdown
## Scope

**Falsifiable question:** [the question this prototype answers]

**In-scope:**
- [item] — fidelity: [mocked|stubbed|partial|full]

**Out-of-scope:**
- [item] — reason: [why excluded]
```

## Examples

**Correct:**
> **Falsifiable question:** Can a search-as-you-type interface return results within 200ms on a 3G connection?
>
> **In-scope:**
> - Search input field — fidelity: full
> - Results list rendering — fidelity: mocked
> - Network latency simulation — fidelity: partial
>
> **Out-of-scope:**
> - User authentication — reason: not relevant to the search interaction
> - Result ranking algorithm — reason: deferred to Feature Technical Design(10)

**Incorrect:**
> **Falsifiable question:** Can the search feature work?
>
> **In-scope:**
> - Search
> - Results
> - Filters
>
> **Out-of-scope:**
> - Nothing — the prototype covers everything
> *Why wrong: the question is not falsifiable, no fidelity levels are assigned, and nothing is excluded.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** State the falsifiable question before listing scope; assign a fidelity level to every in-scope item; provide a reason for every out-of-scope exclusion
- **Don't:** Leave the question vague or untestable; list items without fidelity levels; claim "nothing is out of scope"

**Minimum content:** 2 lists (in-scope + out-of-scope)
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Goals, Success Criteria

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
