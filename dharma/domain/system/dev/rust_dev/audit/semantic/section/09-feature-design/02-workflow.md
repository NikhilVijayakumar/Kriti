# Workflow Audit

This section details the Workflow Audit.

## Version
1.0.0

## Engineering Intent
Workflow audit examines the sequence of user actions and system responses required to accomplish a feature's goal. It ensures the workflow is complete, efficient, handles branching paths, and accounts for the full lifecycle of the interaction from entry to exit.

## Audit Objectives
- Workflow steps are logically ordered and non-redundant
- All branching paths (success, failure, cancel, skip) are defined
- Entry points and exit points are clearly identified
- Workflow handles interruptions and resumption
- Number of steps is minimal for the task complexity
- Transitions between steps are smooth and predictable

## Expected Quality
- Workflow has a defined start and end state
- Each step has a single clear action or decision
- Error recovery paths are documented alongside happy path
- Workflow does not exceed 7 steps (or justified)
- Workflow can be completed in a single session

## Red Flags
- Missing error or cancellation paths
- Workflow assumes uninterrupted completion
- Steps that could be parallelized are sequential
- No undo or back-navigation support
- Workflow contradicts existing navigation patterns

## Edge Cases
- User exits and re-enters workflow mid-way
- Network interruption during a multi-step workflow
- Workflow invoked from multiple entry points with partial pre-filled data
- Timeout or session expiry during workflow

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Workflow has clear start, steps, and end defined |
| C2 | mandatory | 0 or 35 | All branching paths (success/error/cancel) documented |
| C3 | recommended | 0 or 30 | Workflow length is justified and minimal |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "..." },
  "message": "..."
}
```
