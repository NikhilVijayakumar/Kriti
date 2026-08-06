# Solution Audit

This section details the Solution Audit.

## Version
1.0.0

## Engineering Intent
The solution section describes the high-level approach to solving the identified problem without descending into implementation detail. It outlines the conceptual model, key capabilities, and how the solution differs from existing approaches. The solution must be plausible, scoped, and traceable back to the problem.

## Audit Objectives
- Solution addresses each aspect of the stated problem
- Solution is described at capability level, not implementation level
- Key differentiators from existing solutions are clear
- Solution scope boundaries are defined
- Solution feasibility is plausible given known constraints

## Expected Quality
- Solution narrative connects causally to the problem statement
- Capabilities are described in user-facing language
- Solution avoids prescribing specific technologies or architectures
- Solution acknowledges constraints (regulatory, technical, operational)
- Solution scope is realistic for the envisioned timeline

## Red Flags
- Solution section reads as a system architecture or design document
- Solution proposes technologies by name without explaining why
- Solution does not map back to the problem it solves
- Solution scope is unrealistic or aspirational beyond feasibility
- Solution uses weasel words ("may", "could", "potentially") for core claims

## Edge Cases
- Solution that involves multiple phases or incremental delivery
- Solution that requires ecosystem or partnership dependencies
- Solution section that must balance innovation with existing system constraints

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Solution addresses all aspects of the stated problem |
| C2 | mandatory | 0 or 30 | Solution described at capability level without technology prescription |
| C3 | recommended | 0 or 30 | Constraints and feasibility considerations acknowledged |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 3, "paragraph_index": 2, "excerpt": "The solution provides automated data capture and real-time validation..." },
  "message": "Solution capabilities map directly to each problem dimension."
}
```
