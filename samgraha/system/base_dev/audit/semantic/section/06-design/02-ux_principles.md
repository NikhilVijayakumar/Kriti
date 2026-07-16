# UX Principles Audit

This section details the UX Principles Audit.

## Version
1.0.0

## Engineering Intent
UX principles operationalize human-centered design into actionable heuristics. They govern interaction patterns, information architecture, and user flows to ensure intuitive and efficient experiences.

## Audit Objectives
- UX principles are documented and grounded in HCI best practices
- Interaction patterns follow established UX heuristics (e.g., Nielsen's)
- User flows minimize cognitive load and task completion time
- Error prevention and recovery mechanisms are present
- Consistency in navigation, labeling, and feedback across all screens
- Task completion paths are bounded: primary user tasks complete within a documented maximum number of steps, with no unjustified exceptions

## Expected Quality
- Key UX heuristics (visibility, consistency, feedback, error prevention) are addressed
- Each user flow has a defined happy path and error path
- Common interaction patterns use platform conventions
- UX decisions are justified by usability evidence

## Red Flags
- UX principles not documented or purely aspirational
- Inconsistent navigation patterns or labeling
- No error recovery mechanisms for critical flows
- Hidden or hard-to-find functionality without rationale
- Task step limits stated as "X steps or justified" with no definition of what constitutes valid justification — the escape clause must name specific acceptable exception categories

## Edge Cases
- Multi-step forms with conditional branches
- Offline and degraded-mode interactions
- Cross-device continuity of user state

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | UX principles documented and grounded in HCI heuristics |
| C2 | mandatory | 0 or 30 | User flows define happy and error paths |
| C3 | recommended | 0 or 20 | Consistency in navigation, labeling, and feedback |
| C4 | recommended | 0 or 20 | Primary task step count is bounded with numeric limit and explicit exception criteria (not open-ended "or justified") |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "UX follows Nielsen's heuristics: visibility of system status, match between system and real world..." },
  "message": "All 10 UX heuristics addressed with documented interaction patterns."
}
```
