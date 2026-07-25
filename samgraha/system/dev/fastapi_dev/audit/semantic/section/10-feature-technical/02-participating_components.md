# Participating Components Audit

This section details the Participating Components Audit.

## Version
1.0.0

## Engineering Intent
Participating components list every module, service, class, or sub-system that takes part in the feature. This section must provide an inventory of components, their deployment unit, the feature role they play, and their state model within the feature lifecycle.

## Audit Objectives
- Every component involved in the feature is listed
- The deployment unit or container for each component is identified
- Each component's role within the feature is described
- Version compatibility between components is documented
- Components not involved are explicitly excluded where ambiguity exists

## Expected Quality
- Components are organized by layer or deployment boundary
- Each component has a stable identifier matching architecture docs
- State model (active, passive, standby) is defined per component
- Dependencies between participating components are cross-referenced

## Red Flags
- Components referenced in other sections but missing from the list
- Deployment unit unstated for critical components
- Roles that are ambiguous ("helper" or "utility")
- Outdated component names that don't match the codebase

## Edge Cases
- Components that participate conditionally based on feature flags
- Third-party or external components that participate indirectly
- Virtual components (logical groupings not in code)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All participating components enumerated |
| C2 | mandatory | 0 or 30 | Deployment unit specified per component |
| C3 | recommended | 0 or 20 | Each component has a defined feature role |
| C4 | recommended | 0 or 20 | State model documented per component |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "OrderService (order-service.jar) - validates and processes orders..." },
  "message": "All 8 participating components listed with deployment units."
}
```
