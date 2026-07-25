# Semantic Audit — security

Semantic evaluation of secure engineering practices, security awareness, defensive design, and overall security maturity.

## Evaluation Principles
- Evaluate security awareness rather than vulnerability count.
- Evaluate only observable evidence.
- Do not assume undocumented security controls.
- Consider the project scope and hackathon constraints.
- Reward secure engineering decisions and defensive programming.
- Focus on overall security maturity rather than isolated issues.

## Task
Analyze the repository for secure engineering practices and overall security
maturity.

Evaluate the project's security posture based on observable implementation
and documentation.

Consider:

- Whether sensitive information is handled appropriately.
- Whether secrets, credentials, API keys, or tokens are managed securely.
- Whether configuration separates sensitive values from source code.
- Whether input validation and defensive programming practices are evident.
- Whether authentication and authorization mechanisms are appropriately designed, where applicable.
- Whether dependency usage demonstrates awareness of security risks.
- Whether error handling avoids exposing unnecessary implementation details.
- Whether documentation reflects awareness of common security considerations.
- Whether the overall architecture demonstrates secure engineering practices appropriate for a hackathon project.

Do not evaluate purely on the absence of known vulnerabilities.
Instead, evaluate the team's demonstrated security awareness, engineering
decisions, and overall security maturity.

Provide:

- Overall security score (0-100)
- Security strengths
- Security weaknesses
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
