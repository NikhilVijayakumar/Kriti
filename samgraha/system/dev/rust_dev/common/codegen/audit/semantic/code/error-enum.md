# Semantic Audit Rubric — error-enum

### C1: Failure Mode Coverage

- **criterion_id**: C1
- **points**: 40
- **mandatory**: true
- **description**: Does every failure mode named in Feature-Technical(10)'s Error Implementation subsection have exactly one corresponding enum variant?
- **pass_condition**: Each named failure mode maps 1:1 to a variant; no unnamed catch-all variant substitutes for a real failure mode

### C2: Message Quality

- **criterion_id**: C2
- **points**: 30
- **mandatory**: false
- **description**: Would a caller matching on this error know what to do differently per variant, based on the `#[error("...")]` message alone?
- **pass_condition**: Messages are actionable and distinct, not generic wrapping of the inner error's Display output

### C3: Policy Compliance

- **criterion_id**: C3
- **points**: 30
- **mandatory**: true
- **description**: Does the enum follow engineering.md's Error Handling policy (thiserror for libraries, no unwrap() in production code)?
- **pass_condition**: `thiserror::Error` derive present; no `unwrap()`/`expect()` found outside `#[cfg(test)]`
