# Semantic Audit — infrastructure

Semantic evaluation of infrastructure readiness, offline execution capability, reproducibility, deployment readiness, and project environment maturity.

## Evaluation Principles
- Evaluate only observable evidence.
- Do not assume undocumented capabilities.
- Missing documentation is considered missing evidence.
- Prefer implementation evidence over repository claims.
- Ignore generated artifacts unless they contribute to reproducibility.
- Penalize incomplete or placeholder infrastructure.

## Evaluation Dimensions
### environment_setup (weight: 20)
Evaluate whether the project provides sufficient instructions and configuration for setting up a development environment.

### dependency_management (weight: 20)
Evaluate dependency declaration, version management, reproducibility, and package consistency.

### offline_execution (weight: 20)
Evaluate whether the project can execute locally without requiring internet connectivity or external hosted services.

### reproducibility (weight: 20)
Evaluate whether another developer can reproduce the project using only repository assets and documented instructions.

### infrastructure_documentation (weight: 20)
Evaluate the completeness of infrastructure documentation including setup, configuration, execution, and troubleshooting.

## Task
Analyze the repository structure, configuration, and documentation.

Evaluate the project using the evaluation_dimensions defined in this
specification.

For every dimension:

- Evaluate only observable evidence.
- Do not infer undocumented capabilities.
- Explain the evidence supporting the score.
- Clearly justify deductions.
- Assign a score proportional to the available evidence.

Additionally determine:

- Whether the project demonstrates a reproducible infrastructure setup.
- Whether the project supports fully local execution.
- Whether dependency management is properly defined.
- Whether environment configuration is documented.
- Whether containerization or equivalent execution mechanisms exist.
- Whether infrastructure documentation is sufficient for a new developer.

Finally provide:

- Dimension scores
- Overall score (0-100)
- Strengths
- Weaknesses
- Recommendations

## Expected Output
Return exactly one JSON object matching this schema (this is what the post-script persists):
```json
{
  "overall_score": "number",
  "dimension_scores": {
    "environment_setup": {
      "score": "number",
      "evidence": "string"
    },
    "dependency_management": {
      "score": "number",
      "evidence": "string"
    },
    "offline_execution": {
      "score": "number",
      "evidence": "string"
    },
    "reproducibility": {
      "score": "number",
      "evidence": "string"
    },
    "infrastructure_documentation": {
      "score": "number",
      "evidence": "string"
    }
  },
  "reasoning": "string",
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
