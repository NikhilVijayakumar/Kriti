# Data Ownership Audit

This section details the Data Ownership Audit.

## Version
1.0.0

## Engineering Intent
Data ownership defines which component or service is the authoritative source for each data entity within the feature. This section must document data entity ownership, write authority, read replicas, data lifecycle management, and conflict resolution rules when multiple components interact with the same data.

## Audit Objectives
- Every data entity has a designated owner component
- Write authority is clearly assigned (single writer or designated writers)
- Read replicas or cached copies are identified
- Data lifecycle (create, read, update, delete) ownership per operation is specified
- Conflict resolution strategy for concurrent writes is documented
- Data retention and purging policies are defined

## Expected Quality
- Ownership is assigned to components, not individuals or teams
- Data entities are normalized and consistently named
- Ownership transfer procedures are documented
- Data consistency model (strong, eventual) is stated per entity
- Audit trail for data ownership changes is referenced

## Red Flags
- Data entities without an owner (orphan data)
- Multiple components claiming write ownership of the same entity
- Write ownership assigned but read patterns undocumented
- Missing data retention or purging policies
- Ownership contradicts implementation (different component writes the data)

## Edge Cases
- Shared data with no clear single owner (reference data)
- Data that changes ownership during its lifecycle
- Temporary data with no ownership defined (caches, derived data)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All data entities have designated owners |
| C2 | mandatory | 0 or 30 | Write authority is assigned and non-conflicting |
| C3 | recommended | 0 or 20 | Data lifecycle documented per entity |
| C4 | recommended | 0 or 20 | Data retention and purging policies defined |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "Order entity: OrderService (write owner), SearchService (read replica)..." },
  "message": "All 12 data entities have unambiguous ownership assignments."
}
```
