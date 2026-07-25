# Security Considerations Audit

This section details the Security Considerations Audit.

## Version
1.0.0

## Engineering Intent
Security considerations document the threat model, security controls, and trust boundaries relevant to the feature. This section must identify authentication and authorization mechanisms, data protection in transit and at rest, input validation rules, audit logging requirements, and any security assumptions about the operating environment.

## Audit Objectives
- Threat model for the feature is documented (at minimum: list of threats and mitigations; STRIDE or OWASP Top 10 mapping preferred)
- Attack surface for this feature is enumerated (endpoints, inputs, integrations)
- Authentication mechanism for the feature is specified
- Authorization model (RBAC, ABAC, ACLs) is documented
- Data-in-transit protection (TLS, mTLS) is defined
- Data-at-rest encryption requirements are stated
- Input validation and sanitization rules enumerate specific attack vectors (XSS, SQL injection, command injection, path traversal)
- Audit events and logging requirements are documented

## Expected Quality
- Threats are mapped to specific mitigations
- Trust boundaries are explicitly drawn
- Secrets management approach is described
- Security testing requirements are referenced
- Compliance standards (PCI, SOC2, HIPAA) are cited where applicable

## Red Flags
- "Security will be handled later" or similar deferrals
- No authentication or authorization described
- Data classified without protection requirements
- Missing input validation for external-facing endpoints
- Hard-coded secrets or credentials mentioned

## Edge Cases
- Security controls that differ between internal and external access
- Degraded security mode during maintenance windows
- Third-party identity provider outage handling

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 25 | Threat model documents threats with mitigations (STRIDE/OWASP Top 10 mapping) |
| C2 | mandatory | 0 or 25 | Authentication and authorization model documented |
| C3 | mandatory | 0 or 25 | Input validation names specific attack vectors (XSS, SQLi, command injection) |
| C4 | recommended | 0 or 25 | Data protection (transit and at rest) and audit logging defined |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 1, "excerpt": "All API endpoints require JWT bearer tokens validated by AuthService..." },
  "message": "Authentication and authorization model fully documented."
}
```
