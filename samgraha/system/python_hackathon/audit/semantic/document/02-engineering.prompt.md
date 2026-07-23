# Semantic Audit — engineering

Semantic evaluation of engineering quality, maintainability, architectural maturity, code readability, and long-term sustainability.

## Evaluation Principles
- Evaluate engineering quality rather than implementation completeness.
- Evaluate only observable evidence.
- Do not assume undocumented design decisions.
- Prefer implementation quality over stated intentions.
- Consider the scope and complexity expected for a hackathon project.
- Focus on maintainability rather than feature count.

## Task
Analyze the source code, project organization, and engineering practices.

Evaluate the overall engineering maturity of the project rather than
individual programming errors.

Consider:

- Code organization and logical project structure.
- Separation of concerns and modular decomposition.
- Readability and maintainability of the codebase.
- Consistency of coding style across the project.
- Architectural coherence and design decisions.
- Appropriate abstraction without unnecessary complexity.
- Reusability and extensibility of components.
- Appropriate use of type annotations where beneficial.
- Naming quality for modules, classes, functions, and variables.
- Balance between engineering quality and hackathon delivery speed.

Do not penalize teams solely for having fewer features.
Evaluate the quality of the implemented solution.

Provide:

- Overall engineering score (0-100)
- Engineering strengths
- Engineering weaknesses
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
