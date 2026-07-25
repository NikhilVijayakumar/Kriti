# Semantic Audit — documentation

Semantic evaluation of project documentation quality, clarity, completeness, onboarding experience, and communication of engineering decisions.

## Evaluation Principles
- Evaluate documentation quality rather than document length.
- Evaluate only observable evidence.
- Do not assume undocumented capabilities.
- Consider documentation from the perspective of a new contributor.
- Reward clarity, consistency, and completeness.
- Consider hackathon scope while evaluating documentation maturity.

## Task
Analyze the project documentation, including the README and any supporting
documentation contained within the repository.

Evaluate the overall documentation quality rather than the presence of
individual sections.

Consider:

- Whether the project vision clearly explains the problem being solved.
- Whether the project objectives and scope are well communicated.
- Whether installation and setup instructions are understandable.
- Whether execution and usage instructions are complete.
- Whether project architecture or design decisions are sufficiently explained.
- Whether configuration requirements are documented.
- Whether the documentation helps new contributors understand the project.
- Whether examples, diagrams, or usage demonstrations improve understanding.
- Whether documentation remains consistent with the implemented solution.
- Whether the documentation demonstrates good engineering communication.

Do not reward documentation solely based on length.
Evaluate its usefulness, clarity, organization, and completeness.

Provide:

- Overall documentation score (0-100)
- Documentation strengths
- Documentation weaknesses
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
