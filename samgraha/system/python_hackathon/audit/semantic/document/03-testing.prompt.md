# Semantic Audit — testing

Semantic evaluation of testing philosophy, validation strategy, test design, confidence in correctness, and overall testing maturity.

## Evaluation Principles
- Evaluate testing strategy rather than raw test quantity.
- Evaluate only observable evidence.
- Do not assume unimplemented testing practices.
- Consider the project scope and hackathon constraints.
- Reward meaningful validation over exhaustive coverage.
- Focus on confidence provided by the testing approach.

## Task
Analyze the repository's testing approach, validation strategy, and quality
assurance practices.

Evaluate the overall testing maturity of the project rather than counting
individual test cases.

Consider:

- Whether the testing strategy appropriately validates the implemented solution.
- Whether critical application workflows are covered.
- Whether edge cases, error conditions, and failure scenarios are considered.
- Whether unit, integration, and end-to-end testing are used where appropriate.
- Whether AI/ML models, data processing, or prediction pipelines include meaningful validation.
- Whether test organization, naming, and structure improve maintainability.
- Whether automated testing contributes confidence to future development.
- Whether testing demonstrates engineering discipline appropriate for a hackathon project.

Do not reward unnecessary test quantity.
Evaluate the effectiveness, completeness, and intent of the testing strategy.

Provide:

- Overall testing score (0-100)
- Testing strengths
- Testing weaknesses
- Recommendations for improvement
- Supporting evidence from the repository

## Expected Output
Return exactly one JSON object matching this schema (this is what the post-script persists):
```json
{
  "overall_score": "number",
  "reasoning": "string",
  "evidence": "string",
  "strengths": [
    "string"
  ],
  "weaknesses": [
    "string"
  ],
  "recommendations": [
    "string"
  ]
}
```
