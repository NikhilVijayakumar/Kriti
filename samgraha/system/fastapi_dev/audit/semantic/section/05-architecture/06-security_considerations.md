# Security Considerations Audit

This section details the Security Considerations Audit.

## Version
1.0.0

## Engineering Intent
Security considerations document the security-relevant aspects of the architecture, including threat model boundaries, trust zones, authentication and authorization flows, data protection mechanisms, and compliance requirements. Good coverage identifies risks and maps mitigations to architectural decisions.

## Audit Objectives
- Security-relevant architectural decisions are documented
- Trust boundaries between components are identified
- Threat model scope and assumptions are stated using a structured methodology (STRIDE, PASTA, or OWASP Threat Modeling)
- Threats are enumerated and mapped to specific mitigations
- Authentication and authorization mechanisms are described
- Data-at-rest and in-transit protection is addressed
- Compliance requirements are mapped to controls
- Attack surface is enumerated (external entry points, ingress protocols, exposed ports)

## Expected Quality
- Security mechanisms reference specific architecture components
- Threat mitigations are linked to identified risks
- Data sensitivity classifications are defined
- Security assumptions are explicit and justified
- Compliance obligations cite specific regulations or standards

## Red Flags
- No security considerations section (system presumed insecure by default)
- Security mechanisms described in isolation without threat context
- Authentication discussed without authorization
- Missing data sensitivity classification
- Compliance mentioned without specific control mapping
- "Security will be handled later" deferred language

## Edge Cases
- System with no external attack surface (air-gapped)
- Third-party security controls (SaaS, managed services)
- Inherited compliance from platform (FedRAMP, SOC 2)
- Security-by-obscurity claims

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Trust boundaries and attack surface are enumerated |
| C2 | mandatory | 0 or 30 | Threat model uses structured methodology (STRIDE/PASTA/OWASP) with threats mapped to mitigations |
| C3 | mandatory | 0 or 20 | Authentication and authorization mechanisms are described |
| C4 | recommended | 0 or 20 | Data protection (at rest and in transit) is addressed per classification |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.85,
  "severity": "error",
  "evidence": { "section_id": 50, "paragraph_index": 0, "excerpt": "All internal services communicate over mTLS." },
  "message": "Trust boundary identified but threat model scope and assumptions not stated."
}
```
