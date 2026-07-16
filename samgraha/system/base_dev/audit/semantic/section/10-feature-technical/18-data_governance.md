# Data Governance Audit

This section details the Data Governance Audit.

## Version
1.0.0

## Engineering Intent
Features that handle data must classify that data, protect it appropriately, and comply with applicable regulations. This standard verifies that PII and sensitive data are identified, classified, minimized, encrypted, and subject to documented retention and deletion policies. Privacy impact is assessed before deployment, not after.

## Audit Objectives
- Data elements handled by the feature are enumerated
- Each data element is classified (public, internal, confidential, PII, sensitive-PII)
- PII fields are minimized (only fields necessary for the feature are collected)
- Data-at-rest and in-transit protection is specified per classification level
- Retention period and deletion trigger are documented per data type
- Applicable regulations are identified and control mapping provided (GDPR Article, CCPA right, HIPAA rule, etc.)
- Privacy Impact Assessment (PIA) status is referenced

## Expected Quality
- Classification follows a documented organization-wide taxonomy
- PII fields are explicitly named, not described in aggregate
- Retention periods are specific (not "as long as needed")
- Deletion is verifiable (not just policy — mechanism described)
- Third-party data processors handling PII are identified

## Red Flags
- No data classification for fields collected from users
- PII stored in logs without redaction
- Retention period set to "indefinite" without compliance justification
- No deletion mechanism for right-to-erasure requests
- Third-party processors used without data processing agreement reference

## Edge Cases
- Features that derive PII from non-PII inputs (e.g., location from IP address)
- Features that aggregate anonymized data in ways that allow re-identification
- Cross-border data transfers subject to transfer mechanism requirements (SCCs, BCRs)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All data elements enumerated and classified |
| C2 | mandatory | 0 or 30 | PII minimization and protection requirements specified |
| C3 | mandatory | 0 or 20 | Retention period and deletion mechanism documented |
| C4 | recommended | 0 or 20 | Applicable regulations mapped to controls and PIA referenced |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.91,
  "severity": "error",
  "evidence": { "section_id": 4, "paragraph_index": 0, "excerpt": "User profile data is stored in the users table." },
  "message": "Data elements referenced but not enumerated or classified by sensitivity."
}
```
