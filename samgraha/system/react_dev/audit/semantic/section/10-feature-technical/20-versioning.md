# Versioning and Change Management Audit

This section details the Versioning and Change Management Audit.

## Version
1.0.0

## Engineering Intent
APIs, schemas, and message formats are contracts with callers. Breaking changes without versioning destroy integrations silently. This standard verifies that the feature defines an explicit versioning strategy, a deprecation lifecycle with timelines, a backward compatibility guarantee per version, and a rollout strategy that allows safe progressive delivery.

## Audit Objectives
- API or schema versioning strategy is defined (URL path, header, content negotiation)
- Backward compatibility guarantee per version is stated (semver contract or equivalent)
- Deprecation lifecycle is documented: deprecation notice period, migration guide, sunset date
- Rollout strategy is specified (canary, blue-green, feature flags, or phased)
- Breaking change definition is explicit (what counts as breaking for this contract)
- Consumer notification process for breaking changes is described

## Expected Quality
- Versioning strategy is consistent with system-wide API conventions
- Deprecation timeline is long enough for consumers to migrate (minimum 2 release cycles)
- Migration guide accompanies every deprecation notice
- Rollout strategy includes rollback gate criteria
- Breaking change definition covers: removed fields, type changes, changed semantics, renamed endpoints

## Red Flags
- No versioning strategy ("we'll cross that bridge when we come to it")
- Breaking changes shipped without version bump
- Deprecation announced with no migration guide
- Rollout strategy is "deploy to all at once"
- Backward compatibility undefined

## Edge Cases
- Internal APIs where all callers are owned by the same team (lighter process acceptable if documented)
- Event schemas in message queues where consumers may be offline during deprecation window
- Database schema changes where backward compatibility spans migration scripts

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Versioning strategy defined with breaking change definition |
| C2 | mandatory | 0 or 35 | Deprecation lifecycle documented with notice period and migration guide |
| C3 | recommended | 0 or 30 | Rollout strategy specified with rollback gate criteria |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.85,
  "severity": "error",
  "evidence": { "section_id": 2, "paragraph_index": 0, "excerpt": "API changes will be communicated in release notes." },
  "message": "No versioning strategy or breaking change definition found."
}
```
