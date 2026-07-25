# Semantic Audit — team-workflow

Semantic evaluation of collaboration maturity, engineering coordination, and overall development workflow quality.

## Evaluation Principles
- Evaluate collaboration quality rather than repository statistics.
- Evaluate only observable evidence.
- Do not infer team practices without supporting evidence.
- Consider the scope and duration of a hackathon project.
- Focus on engineering coordination and workflow maturity.

## Task
Analyze the repository, project organization, and available development
artifacts.

Evaluate the overall engineering workflow demonstrated by the project.

Consider:

- Whether responsibilities appear logically separated across the project.
- Whether the repository organization supports collaborative development.
- Whether engineering decisions appear coordinated and consistent.
- Whether documentation and project structure facilitate team collaboration.
- Whether the workflow demonstrates maintainability for future contributors.
- Whether development practices reflect good engineering discipline appropriate
  for a hackathon project.

Do not evaluate commit counts, commit cadence, pull requests,
contributor statistics, or branching strategy, as these are evaluated by
deterministic audits.

Provide:

- Overall workflow score (0-100)
- Workflow strengths
- Workflow weaknesses
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
