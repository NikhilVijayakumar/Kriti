# Short Description Audit

This section details the Short Description Audit.

## Version
1.0.0

## Engineering Intent
Short Description is the one/two-sentence answer to "what is this and who is it for" — the first thing a reader evaluates before deciding to read further. It must stay under 200 characters and free of implementation detail.

## Audit Objectives
- One to two sentences, under 200 characters
- States what the project does and who it's for
- No technology stack, installation steps, feature counts, or version numbers

## Expected Quality
- Reads as a single scannable statement, not a paragraph
- Names the user/use-case, not just the mechanism
- Free of jargon that requires already knowing the project

## Red Flags
- Exceeds 200 characters or reads as multiple sentences of prose
- Lists technology stack (language, framework, database) instead of purpose
- Doubles as an installation instruction ("install with pip install...")
- States feature counts or version numbers as if this were a changelog

## Edge Cases
- Product with multiple distinct audiences — pick the primary one, don't try to describe all in one sentence
- Internal tool with no external "user" per se — describe the team/workflow it serves instead

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Under 200 characters, 1-2 sentences |
| C2 | mandatory | 0 or 30 | States what it does and who it's for |
| C3 | recommended | 0 or 30 | No technology stack, install steps, or version/feature counts |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C3",
  "passed": false,
  "confidence": 0.85,
  "severity": "warning",
  "evidence": { "section_id": 3, "paragraph_index": 0, "excerpt": "Built with Python 3.12, uses Apache Airflow, install with pip install acme-scheduler." },
  "message": "Short Description lists technology stack and install instructions instead of purpose."
}
```
