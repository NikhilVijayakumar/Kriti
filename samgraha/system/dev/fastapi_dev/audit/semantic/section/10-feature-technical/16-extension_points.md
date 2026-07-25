# Extension Points Audit

This section details the Extension Points Audit.

## Version
1.0.0

## Engineering Intent
Extension points document where the feature can be customized, extended, or integrated with by other features or external consumers. This section must describe plugin interfaces, hooks, callbacks, configuration-driven behavior, override mechanisms, and the extension contract including stability guarantees.

## Audit Objectives
- Every extension point is enumerated with its interface signature
- Extension mechanism (plugin, callback, config, SPI) is specified
- Stability guarantees for each extension point are documented
- Extension lifecycle (registration, invocation, teardown) is described
- Default behavior when no extension is provided is defined

## Expected Quality
- Extension points have versioned interfaces
- Breaking changes policy for extension contracts is documented
- Extension discovery mechanism (registry, classpath, config) is described
- Extension isolation and sandboxing rules are covered
- Examples of valid extension implementations are provided

## Red Flags
- Extension points defined without interface contracts
- No stability guarantees or deprecation policy
- Extensions can break the feature's core invariants
- Extension mechanism is more complex than the feature itself
- Undocumented extension points found in the codebase

## Edge Cases
- Extension points that are only available in specific deployment tiers
- Extensions that conflict with each other
- Extension points that were deprecated but remain in code

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | All extension points enumerated with interface signature |
| C2 | mandatory | 0 or 30 | Extension mechanism and registration described |
| C3 | recommended | 0 or 20 | Stability guarantees and deprecation policy documented |
| C4 | recommended | 0 or 20 | Default behavior for unextended feature defined |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 0, "paragraph_index": 0, "excerpt": "PaymentRouter plugin interface: processPayment(Order, PaymentMethod) -> Result..." },
  "message": "All 4 extension points documented with interface contracts and stability levels."
}
```
