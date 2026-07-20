# Testing Analysis Prompt

Guides the per-team analysis for the Testing domain — read by whichever
agent runs it via MCP, after scoring has completed. Explains a team's
testing score grounded in actual test suite evidence. Not parsed by a
script — this is a prompt.

## Version
1.0.0

## Analysis Intent
Testing scores (weight: 12) measure whether a team has automated
validation for their core functionality. This step interprets pytest
execution results, coverage data, and test structure to explain *why*
the score is what it is.

## Inputs
- `standard_domain_scores` DB table — all teams' testing domain
  scores (queried via MCP)
- Per-team deterministic findings: `tests/` or `test/` directory
  presence, `pytest.ini` or equivalent config, pytest execution
  results (pass/fail counts), coverage percentage
- Semantic findings: test structure quality, fixture usage, assertion
  patterns

## Narrative Guidance
The Testing narrative must cover:
1. **Score Overview** — team's testing score out of 12, with
   competition average and top performer comparison.
2. **Test Suite Presence** — does a `tests/` or `test/` directory
   exist? How many test files? This is the most basic gate.
3. **Runner Configuration** — is `pytest.ini` or a `[tool.pytest]`
   section in `pyproject.toml` present? Configuration signals
   intentional test strategy.
4. **Execution Results** — if pytest was run, what were the results?
   Pass/fail counts, any skip markers, any xfail tests. Failed tests
   are high-signal findings.
5. **Coverage** — if coverage was measured, report the percentage and
   which modules are uncovered. Low coverage on core modules is a
   critical weakness.
6. **Strengths** — high test count, good coverage, proper fixture
   usage, parametrized tests, edge case coverage.
7. **Weaknesses** — no tests directory, tests that fail, zero
   coverage on core logic, tests that don't assert anything.
8. **Recommendations** — "add integration tests for the prediction
   endpoint", "increase coverage on `model.py` from 23% to 60%+",
   "fix the 3 failing tests in `test_preprocessing.py`".

## Visualization Guidance
- `domain_scores` — always include.
- `coverage_heatmap` — include if coverage data available: per-module
  coverage bar chart.
- `test_results` — include if pytest was run: pass/fail/skip stacked
  bar.

## Output Schema
```json
{
  "domain": "03-testing",
  "sections": [
    {"heading": "Score Overview", "text": "..."},
    {"heading": "Test Suite Presence", "text": "..."},
    {"heading": "Runner Configuration", "text": "..."},
    {"heading": "Execution Results", "text": "..."},
    {"heading": "Coverage", "text": "..."},
    {"heading": "Strengths", "text": "..."},
    {"heading": "Weaknesses", "text": "..."},
    {"heading": "Recommendations", "text": "..."}
  ]
}
```
