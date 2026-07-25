# Semantic Audit — runtime

Semantic evaluation of runtime architecture, inference efficiency, operational readiness, API usability, and execution maturity.

## Evaluation Principles
- Evaluate runtime quality rather than benchmark numbers.
- Evaluate only observable evidence.
- Do not assume undocumented optimizations.
- Consider the scope and complexity expected for a hackathon project.
- Reward efficient runtime design and operational readiness.
- Focus on architectural quality rather than implementation size.

## Task
Analyze the repository's runtime architecture, inference workflow,
and operational characteristics.

Evaluate the overall runtime maturity of the project based on
observable implementation and documentation.

Consider:

- Whether the inference pipeline is well-structured and maintainable.
- Whether runtime design demonstrates awareness of performance and resource efficiency.
- Whether memory usage and execution efficiency appear appropriate for the intended deployment environment.
- Whether optimization techniques are applied where beneficial.
- Whether inference workflows are predictable, reliable, and repeatable.
- Whether public APIs are intuitive, stable, and consistently designed.
- Whether runtime configuration and execution behavior are clearly documented.
- Whether error handling and failure recovery contribute to runtime robustness.
- Whether deployment constraints and operational limitations are acknowledged.
- Whether the overall runtime architecture is appropriate for a hackathon project.

Do not reward projects solely for performance claims or benchmark results.
Evaluate the quality of the runtime design, engineering decisions,
and operational maturity.

Provide:

- Overall runtime score (0-100)
- Runtime strengths
- Runtime weaknesses
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
