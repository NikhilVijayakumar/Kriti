# Testing Standards Audit

This section details the Testing Standards Audit.

## Version
1.0.0

## Engineering Intent
Automated tests must be deterministic, isolated, fast, and provide meaningful coverage. Test suites are first-class artifacts subject to the same quality bar as production code.

## Audit Objectives
- Tests are deterministic (same result every run)
- Tests are isolated (no shared mutable state, no interdependencies)
- Test coverage meets project thresholds
- Tests fail with clear messages that aid debugging
- Test suites run within defined time budgets
- Performance tests exist with defined pass/fail thresholds (p95 latency, throughput targets)
- Security test coverage includes at minimum: authentication bypass, authorization escalation, and input injection paths
- Test data strategy is documented: seed data source, fixture management, no reliance on production data

## Expected Quality
- Each test asserts a single behavior (one logical assertion per test)
- Tests use fixtures or factories, not production databases
- No test depends on test execution order
- Test names describe the scenario and expected outcome
- Flaky tests are quarantined and tracked

## Red Flags
- Tests that pass in CI but fail locally (environment-dependent)
- Sleep statements or race-condition timeouts in tests
- Tests with no assertions (vacuous pass)
- Shared global state between tests
- Skipped tests without documented reason and owner

## Edge Cases
- Integration tests that legitimately depend on external services
- Snapshot tests that are never reviewed on update
- Tests for generated code (coverage blind spots)
- Stress or performance tests that use probabilistic assertions

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 20 | No flaky or non-deterministic tests |
| C2 | mandatory | 0 or 20 | Coverage threshold met for all modules |
| C3 | mandatory | 0 or 20 | Test data strategy documented; no production data in test fixtures |
| C4 | recommended | 0 or 20 | Performance tests defined with numeric pass/fail thresholds |
| C5 | recommended | 0 or 20 | Security paths (auth bypass, privilege escalation, injection) have test coverage |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 17, "paragraph_index": 3, "excerpt": "test_auth_login.py: line 24 uses sleep(2) instead of wait condition." },
  "message": "test_auth_login.py uses non-deterministic sleep pattern."
}
```
