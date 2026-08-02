# Semantic Audit Rubric — lint-stage

### C1: Gate Ordering

- **criterion_id**: C1
- **points**: 40
- **mandatory**: true
- **description**: Does the lint stage run first and block every downstream stage, per build.md's CI/CD Validation gate sequence?
- **pass_condition**: fmt-check and clippy both run before any test/security/package stage; failure halts the pipeline

### C2: Strictness

- **criterion_id**: C2
- **points**: 30
- **mandatory**: true
- **description**: Does clippy run with `-D warnings` (warnings treated as failures), not just default (warnings allowed)?
- **pass_condition**: `-D warnings` flag present in the clippy invocation

### C3: No Silent Continuation

- **criterion_id**: C3
- **points**: 30
- **mandatory**: false
- **description**: Is there no continue-on-error / allow-failure annotation on either step?
- **pass_condition**: Neither step is marked non-blocking
