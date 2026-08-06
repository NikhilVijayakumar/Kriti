# Problem Audit

This section details the Problem Audit.

## Version
1.0.0

## Engineering Intent
The problem section articulates the real-world pain point, gap, or opportunity that the vision addresses. It grounds the vision in evidence by describing the current state, who is affected, and why existing solutions fall short. A well-defined problem ensures the vision solves something real rather than a hypothetical.

## Audit Objectives
- Problem is stated from the user or stakeholder perspective
- Evidence or data supports the problem's existence and severity
- Affected parties or personas are identified
- Current workarounds or existing solutions are acknowledged
- Problem scope is bounded (what is included and excluded)

## Expected Quality
- Problem description includes observable symptoms, not assumed causes
- Quantitative or qualitative evidence supports the problem claim
- Problem is framed neutrally without prescribing the solution
- Impact of not solving the problem is articulated
- Language is precise and avoids exaggeration

## Red Flags
- Problem section describes the solution instead of the problem
- Problem is vague or generic ("users need better tools")
- No evidence or data supports the problem claim
- Problem blames specific technologies or vendors without justification
- Problem scope is unbounded or infinite in scale

## Edge Cases
- Problem that affects multiple disparate user groups with conflicting needs
- Problem that is well-understood internally but lacks external validation
- Problem section that overlaps with market analysis or competitive research

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Problem stated from user/stakeholder perspective with evidence |
| C2 | mandatory | 0 or 30 | Affected parties identified and problem scope bounded |
| C3 | recommended | 0 or 30 | Current workarounds or alternatives acknowledged |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 2, "paragraph_index": 1, "excerpt": "Currently, field agents spend 4+ hours per day on manual data entry..." },
  "message": "Problem is grounded in user evidence with measurable impact."
}
```
