# Semantic Audit Rubric — unit-test

### C1: Isolation

- **criterion_id**: C1
- **points**: 35
- **mandatory**: true
- **description**: Does the test exercise one unit in isolation, per qa.md's Unit Testing scope, without reaching into integration/I-O territory?
- **pass_condition**: No network, filesystem, or database access observed; test targets a single function/component

### C2: Behavior Naming

- **criterion_id**: C2
- **points**: 25
- **mandatory**: false
- **description**: Does the test name (`test_<unit>_<scenario>_<expected>`) actually match what the test body verifies?
- **pass_condition**: Scenario and expected in the name match the Arrange/Act/Assert content

### C3: Coverage of the Unit's Own Profile

- **criterion_id**: C3
- **points**: 40
- **mandatory**: true
- **description**: Does the test suite cover every required/prohibited item listed in the code unit's own profile (e.g. error-enum.yaml's expected_content)?
- **pass_condition**: Each required/prohibited item has at least one corresponding test
