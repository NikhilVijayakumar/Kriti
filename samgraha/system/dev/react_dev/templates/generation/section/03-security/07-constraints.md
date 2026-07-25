# Constraints — Generation Template

> **Domain:** security
> **Section:** constraints
> **Source:** `documentation-standards/03-security-standards.md` §Constraints
> **Relationships:** `audit/deterministic/document/03-security-relationships.yaml`

Generate the Constraints section for a Security document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | philosophy / tradeoffs | Constraints must derive from Philosophy's trade-offs — hard boundaries reflect deliberate value sacrifices |
| `constrains` | architecture / security_considerations | Constraints must be evaluable against Architecture's security considerations — every constraint narrows architectural choices |
| `constrains` | engineering / code_standards | Constraints must be evaluable against Engineering's code standards — every constraint narrows implementation choices |

## Template

```markdown
<!-- For each constraint: -->
<!--   - Source: regulatory, contractual, infrastructure, or organizational -->
<!--   - Statement: hard boundary expressed as pass/fail evaluable condition -->
<!--   - Impact: which downstream domains are affected -->
<!-- Avoid embedding solutions — state the boundary, not how to satisfy it -->
```

## Examples

**Correct:**
> **Source:** Regulatory (data residency law)
> **Statement:** All user personal data must be stored and processed within the European Economic Area.
> **Impact:** Architecture (data storage design), Engineering (database deployment region), Feature Technical (data flow design)

**Incorrect:**
> We should use a European cloud provider because it's closer to our users and reduces latency.
> *Why wrong: This is a soft preference disguised as a constraint — latency is not a hard boundary, and it embeds a solution (cloud provider selection) instead of stating the non-negotiable limitation (data must remain in the EEA).*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** State each constraint as a hard boundary expressed as a pass/fail condition; identify which downstream domains are affected by each constraint; attribute each constraint to its source (regulatory, contractual, infrastructure, organizational)
- **Don't:** Embed implementation solutions within constraint statements; state soft preferences (performance, convenience) as hard constraints; omit source attribution for any listed constraint

**Required subsections:** none
**Optional subsections:** constraint-to-domain impact matrix
**Required diagrams:** none
**Required cross-references:** Vision(01), External Context

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
