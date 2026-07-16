# Incident Response — Generation Template

> **Domain:** security
> **Section:** incident_response
> **Source:** `documentation-standards/03-security-standards.md` §Incident Response
> **Relationships:** `audit/deterministic/document/03-security-relationships.yaml`

Generate the Incident Response section for a Security document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | threat_model (self-reference) | Incident Response must address the threats enumerated in Threat Model — detection and escalation cover enumerated threat categories |

## Template

```markdown
<!-- Detection Expectations: what signals indicate a security incident -->
<!-- Response Escalation: who is notified, in what order, within what timeframe -->
<!-- Communication Requirements: internal and external notification expectations -->
<!-- Recovery Objectives: expected time-to-contain, time-to-restore -->
```

## Examples

**Correct:**
> **Detection Expectations:** Unauthorized access attempts to restricted data stores must be detected within 15 minutes.
> **Response Escalation:** Security lead notified first; project lead notified within 1 hour; external counsel notified if data breach is confirmed.
> **Recovery Objectives:** Containment within 4 hours; full restoration within 24 hours.

**Incorrect:**
> We use Splunk for SIEM monitoring and PagerDuty for on-call alerting. The SOC team runs a weekly scan using Nessus.
> *Why wrong: This mandates specific tooling (Splunk, PagerDuty, Nessus) and operational cadences — those belong in Engineering's Security Standards, not at the project-wide incident response level.*

## Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** State detection and response expectations as outcomes, not tooling; define escalation paths with timeframes and notification order; specify recovery objectives (time-to-contain, time-to-restore)
- **Don't:** Mandate specific SIEM, alerting, or scanning tools; embed on-call rotation details or shift schedules; define post-mortem templates or review formats

**Required subsections:** detection expectations, response escalation, recovery objectives
**Optional subsections:** communication templates, post-incident review expectations
**Required diagrams:** escalation flowchart
**Required cross-references:** Threat Model

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
