# Rationale Audit

This section details the Rationale Audit.

## Version
1.0.0

## Engineering Intent
Every non-obvious engineering decision must be accompanied by an explicit rationale record. Rationale captures the context, alternatives considered, trade-offs accepted, and the reasoning that led to the chosen approach.

## Audit Objectives
- Architectural and design decisions are documented with rationale
- Rationale includes rejected alternatives and why they were rejected
- Rationale is co-located or linked to the decision point
- Rationale is kept up to date when decisions are revisited
- Rationale distinguishes between reversible and irreversible decisions

## Expected Quality
- ADRs exist for every architecturally significant decision
- Code comments explain WHY not WHAT for non-obvious logic
- Configuration choices include inline justification
- Rationale records reference relevant data or experiments
- Decisions have a timestamp and author for accountability

## Red Flags
- Decisions documented with no alternatives listed
- Rationale that contains only the chosen solution (no trade-off)
- Orphaned ADRs that never link to implementation
- Rationale that contradicts the actual code behaviour
- "Because it's best practice" as the sole justification

## Edge Cases
- Decisions made under time pressure with incomplete analysis
- Reversed decisions where old rationale contradicts new code
- Long-lived decisions where context has changed but rationale is stale
- Decisions inherited from upstream or parent projects

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Every architectural decision has an ADR |
| C2 | mandatory | 0 or 30 | Each ADR lists at least two alternatives |
| C3 | recommended | 0 or 20 | Non-obvious code has inline rationale |
| C4 | recommended | 0 or 20 | Rationale is consistent with implementation |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 17, "paragraph_index": 3, "excerpt": "No ADR found for service-mesh migration decision (Q3 2025)." },
  "message": "Service-mesh migration: missing ADR."
}
```
