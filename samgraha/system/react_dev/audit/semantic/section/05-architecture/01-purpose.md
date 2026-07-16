# Purpose Audit

This section details the Purpose Audit.

## Version
1.0.0

## Engineering Intent
The purpose section defines the architectural intent, scope, and key goals for the system. It establishes why the architecture exists, what problems it solves, and the primary qualities it optimizes for. A clear purpose enables readers to evaluate architectural fitness.

## Audit Objectives
- Architectural purpose is stated clearly and concisely
- Primary goals and qualities (performance, scalability, maintainability) are identified
- Scope boundaries (in-scope vs. out-of-scope) are defined
- Stakeholder concerns addressed by the architecture are listed
- The purpose is consistent with downstream architecture sections

## Expected Quality
- Purpose is specific to this architecture (not a generic mission statement)
- Goals are ranked or prioritized to guide trade-off decisions
- Scope boundaries are explicit and falsifiable
- Stakeholder mapping is referenced or implied
- Purpose aligns with documented requirements

## Red Flags
- Generic mission or vision statements in place of architectural purpose
- Contradiction between stated purpose and design decisions in other sections
- Missing scope boundaries (everything is in-scope)
- Goals that are not architecturally relevant (business goals without architectural impact)
- Purpose copied verbatim from project charter or README

## Edge Cases
- Greenfield project vs. legacy migration (different purpose types)
- System serving multiple conflicting stakeholder goals
- Purpose that is implicit but not documented
- Incremental architecture where purpose evolves across milestones

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Architectural purpose is clearly stated with scope boundaries |
| C2 | mandatory | 0 or 30 | Primary architectural goals and their priorities are defined |
| C3 | recommended | 0 or 30 | Purpose is consistent with requirements and downstream sections |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.93,
  "severity": "error",
  "evidence": { "section_id": 5, "paragraph_index": 0, "excerpt": "This architecture supports real-time inventory tracking across 50 warehouses with sub-second update latency." },
  "message": "Purpose is specific, scoped, and falsifiable."
}
```
