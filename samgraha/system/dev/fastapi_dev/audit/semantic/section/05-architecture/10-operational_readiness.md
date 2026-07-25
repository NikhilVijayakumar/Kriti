# Operational Readiness Audit

This section details the Operational Readiness Audit.

## Version
1.0.0

## Engineering Intent
Operational readiness ensures the system can be safely deployed, operated, scaled, and recovered by teams who did not write it. It requires documented deployment automation, rollback procedures, runbooks for known failure modes, scaling triggers, and disaster recovery plans.

## Audit Objectives
- Deployment automation is described (CI/CD pipeline stages and gating criteria)
- Rollback procedure is defined (automated vs manual, rollback time target)
- Runbooks exist for the top N known operational failure modes
- Scaling triggers are specified (horizontal and vertical, with thresholds)
- Disaster recovery plan covers RTO and RPO targets
- Change management process is documented (who approves, freeze windows)

## Expected Quality
- Rollback procedure is tested (not just documented)
- Runbooks are linked from alert definitions
- RTO/RPO targets are specific and derived from business requirements
- Deployment pipeline has a defined gate for production promotion
- Scaling policy accounts for both traffic spikes and gradual growth

## Red Flags
- No rollback procedure ("we'll redeploy the previous version manually")
- Runbooks exist only in someone's memory
- RTO/RPO stated as aspirational without validation testing
- No change freeze window or approval gate for production
- Scaling relies exclusively on manual operator intervention

## Edge Cases
- Multi-region deployments where rollback must be coordinated across regions
- Schema migrations that cannot be rolled back (requires compensating transaction doc)
- Systems with external customers where deployment windows must be announced

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Deployment automation and production promotion gating documented |
| C2 | mandatory | 0 or 30 | Rollback procedure defined with time target |
| C3 | recommended | 0 or 20 | Runbooks linked per failure mode with on-call routing |
| C4 | recommended | 0 or 20 | RTO/RPO targets and DR plan documented |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.90,
  "severity": "error",
  "evidence": { "section_id": 12, "paragraph_index": 0, "excerpt": "Rollback handled on a case-by-case basis by on-call engineer." },
  "message": "No defined rollback procedure or time target found."
}
```
