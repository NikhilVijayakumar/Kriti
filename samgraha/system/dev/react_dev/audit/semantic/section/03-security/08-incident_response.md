# Incident Response Audit

This section details the Incident Response Audit.

## Version
1.0.0

## Engineering Intent
Incident Response defines how a security incident is detected, escalated, communicated, and recovered from — at the outcome level, not a tooling mandate. It exists so a real incident has a known process instead of improvisation.

## Audit Objectives
- Detection expectations stated (what triggers recognition of an incident)
- Escalation paths defined (who is notified, in what order)
- Communication requirements specified (internal and external, as applicable)
- Recovery objectives stated (time-to-recovery, data-loss tolerance)

## Expected Quality
- Detection, escalation, communication, and recovery each addressed distinctly
- Escalation path names roles/responsibilities, not just "the team is notified"
- Recovery objectives are measurable (RTO/RPO-style targets), not "we recover as fast as possible"
- Framed at outcome level — doesn't mandate specific tools, which belong in Engineering

## Red Flags
- "We have an incident response plan" with no actual content describing it
- Escalation path undefined — unclear who acts when an incident is detected
- No recovery objective — success/failure of the response has no measurable target
- Section mandates specific security tooling instead of describing the process at outcome level

## Edge Cases
- Incidents involving third-party/vendor systems — escalation path should include how the vendor relationship is engaged
- Regulatory notification requirements tied to certain incident types (breach notification laws) — should cross-reference Compliance Requirements rather than restate it

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Detection expectations stated |
| C2 | mandatory | 0 or 30 | Escalation paths defined with roles |
| C3 | mandatory | 0 or 20 | Communication requirements specified |
| C4 | recommended | 0 or 20 | Recovery objectives are measurable |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.85,
  "severity": "error",
  "evidence": { "section_id": 52, "paragraph_index": 0, "excerpt": "In case of an incident, the team is notified." },
  "message": "Incident Response has no defined escalation path or named roles."
}
```
