# Operational Readiness — Generation Template

> **Domain:** architecture
> **Section:** operational_readiness
> **Source:** `audit/semantic/section/05-architecture/10-operational_readiness.md`
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the Operational Readiness section for an Architecture document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | engineering / build_standards | Operational Readiness must be consistent with Engineering's build standards |

## Template

```markdown
## Operational Readiness

### Deployment Automation
[CI/CD pipeline stages, gating criteria for production promotion]

### Rollback Procedure
[Automated vs. manual rollback, time target, tested status]

### Runbooks
[Top N known failure modes with linked runbooks and on-call routing]

### Scaling
[Horizontal and vertical scaling triggers with thresholds]

### Disaster Recovery
[RTO and RPO targets, derived from business requirements]

### Change Management
[Approval process, freeze windows, production promotion gates]
```

## Examples

**Correct:**
> **Deployment Automation**
> - Pipeline: Build → Integration Tests → Staging → Production
> - Gating: All integration tests pass; staging smoke test passes; one human approval for production
> - Production promotion: Automated after approval gate
>
> **Rollback Procedure**
> - Automated rollback to previous version on health check failure
> - Rollback time target: < 5 minutes
> - Tested: Yes, weekly during game day exercises
>
> **Runbooks**
> - **Data ingestion stall:** Check ingestion queue depth; if > 10k for 5 min, restart ingestion service. [Runbook: ingestion-stall.md]
> - **Transformation failures:** Check dead letter queue; if > 100 messages, alert on-call. [Runbook: transform-failure.md]
>
> **Scaling**
> - Horizontal: Add ingestion replicas when queue depth > 5k per replica
> - Vertical: Increase transform engine memory when GC pause > 200ms
>
> **Disaster Recovery**
> - RPO: 1 hour (snapshot-based backup)
> - RTO: 4 hours (full re-deployment from last snapshot)

**Incorrect:**
> We deploy using Kubernetes. Rollback is handled on a case-by-case basis by the on-call engineer. Scaling is manual.
> *Why wrong: lacks specific procedures, time targets, and tested status — the audit expects documented, testable operational readiness, not vague statements.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** operator
- **Do:** Document deployment pipeline stages with gating criteria; define rollback procedure with time target; link runbooks to specific failure modes; specify scaling triggers with thresholds; state RTO/RPO targets derived from business requirements
- **Don't:** Describe deployment tools without procedures; state rollback as aspirational ("we'll figure it out"); omit time targets for RTO/RPO; leave scaling triggers vague

**Minimum content:** Deployment automation, rollback procedure
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Component Model, Engineering(07)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
