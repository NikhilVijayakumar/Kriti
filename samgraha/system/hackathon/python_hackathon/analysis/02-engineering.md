# Engineering Analysis Prompt

Guides the per-team analysis for the Engineering domain — read by
whichever agent runs it via MCP, after scoring has completed. Explains
why a team got their engineering quality score. Not parsed by a script
— this is a prompt.

## Version
1.0.0

## Analysis Intent
Engineering scores (weight: 12) measure code maintainability through
complexity analysis and type safety. This step interprets radon and
mypy results, connecting raw tool output to a human-understandable
assessment of code quality.

## Inputs
- `standard_domain_scores` DB table — all teams' engineering domain
  scores (queried via MCP)
- Per-team findings: radon cyclomatic complexity report, mypy/pyright
  type-checking results, `radon.cfg` or `pyproject.toml` config
- Semantic findings: code organization, naming conventions

## Narrative Guidance
The Engineering narrative must cover:
1. **Score Overview** — team's engineering score out of 12, with
   comparison to the competition average and top performer.
2. **Complexity Profile** — summarize radon results: average
   cyclomatic complexity, any functions rated C or worse. Name the
   most complex function if it exceeds threshold.
3. **Type Safety** — was mypy or pyright configured and passing? If
   enabled, how many type errors were found? If not configured, flag
   this as a gap.
4. **Configuration Evidence** — does `radon.cfg` exist? Is mypy
   configured in `pyproject.toml`? The presence of config files
   demonstrates intentional quality gates.
5. **Strengths** — low complexity scores, strict type checking
   enabled and passing, clean configuration.
6. **Weaknesses** — high-complexity functions, missing type checker
   config, ignored type errors, no complexity bounds configured.
7. **Recommendations** — "refactor `process_data()` (CC=14) into
   smaller functions", "add `[tool.mypy]` section to pyproject.toml".

## Visualization Guidance
- `domain_scores` — always include.
- `complexity_distribution` — include if radon data available: bar
  chart of functions by complexity grade (A/B/C/D/E/F).
- `type_error_counts` — include if mypy was run: error count by
  module.

## Output Schema
```json
{
  "domain": "02-engineering",
  "sections": [
    {"heading": "Score Overview", "text": "..."},
    {"heading": "Complexity Profile", "text": "..."},
    {"heading": "Type Safety", "text": "..."},
    {"heading": "Configuration Evidence", "text": "..."},
    {"heading": "Strengths", "text": "..."},
    {"heading": "Weaknesses", "text": "..."},
    {"heading": "Recommendations", "text": "..."}
  ]
}
```
