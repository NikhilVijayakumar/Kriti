# Compliance Requirements Audit

This section details the Compliance Requirements Audit.

## Version
1.0.0

## Engineering Intent
Compliance Requirements names the regulatory regimes the system must satisfy (GDPR, HIPAA, SOC 2, etc.), their scope of applicability, and traces each obligation to the control that satisfies it. It exists so "we're compliant" is a checkable claim, not an assertion.

## Audit Objectives
- Named compliance regimes are specific (GDPR, HIPAA, PCI-DSS), not "we follow best practices"
- Scope and applicability stated per regime — which data/users/jurisdictions it applies to
- Each obligation traces to a downstream control that satisfies it

## Expected Quality
- Regimes named explicitly with the reason they apply (e.g. "GDPR — processes EU resident data")
- Applicability scoped, not assumed to blanket-cover the whole system
- Obligation-to-control traceability is concrete (which section/control satisfies which regime's requirement)

## Red Flags
- "We take compliance seriously" with no named regime
- Regime named but scope/applicability unstated — reader can't tell if it applies to this system at all
- No traceability from obligation to control — compliance claimed without showing how it's met

## Edge Cases
- Multi-jurisdiction product with different regimes per region — state applicability per region, not one blanket claim
- Regime the project doesn't yet fully satisfy — acceptable to state as a gap with a remediation plan, not silently omitted

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Compliance regimes named specifically |
| C2 | mandatory | 0 or 30 | Scope and applicability stated per regime |
| C3 | recommended | 0 or 30 | Obligation-to-downstream-control traceability shown |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.87,
  "severity": "error",
  "evidence": { "section_id": 51, "paragraph_index": 0, "excerpt": "We take data privacy and compliance seriously." },
  "message": "Compliance Requirements names no specific regulatory regime."
}
```
