# Semantic Audit — {{ domain }}

Score the current draft for the **{{ domain }}** domain against the rubric.

## Input Files

- **Rubric**: `audit/semantic/document/{{ domain }}.md` — scoring criteria with weights and pass/fail thresholds
- **Draft**: `docs/paper/{{ system }}/domains/{{ domain }}.md` — current section draft to audit

## Task

1. Read the rubric from `audit/semantic/document/{{ domain }}.md`
2. Read the current draft from `docs/paper/{{ system }}/domains/{{ domain }}.md`
3. For each criterion in the rubric:
   - Determine if the criterion **passes** or **fails** based on observable evidence in the draft
   - Assign **points** proportional to evidence quality (0 = no evidence, full = strong evidence)
   - Record **evidence** — quote or paraphrase the specific passage that supports the score
4. Compute the total score:
   ```
   score = sum(points where passed=true), capped at 100
   ```
   Mandatory criterion failure forfeits that criterion's points entirely (no partial credit).
5. Output the result as structured JSON.

## Output Format

```json
{
  "domain": "{{ domain }}",
  "score": <number 0-100>,
  "criteria": [
    {
      "criterion_id": "<C1|C2|...>",
      "description": "<brief description>",
      "mandatory": <true|false>,
      "weight": <number>,
      "points": <number 0-weight>,
      "passed": <true|false>,
      "evidence": "<quote or paraphrase from draft>"
    }
  ],
  "strengths": ["<list of strongest areas>"],
  "weaknesses": ["<list of areas needing improvement>"],
  "recommendations": ["<list of actionable fixes>"]
}
```

## Rules

- Evaluate only observable evidence in the draft — do not assume capabilities not demonstrated
- Missing evidence = score 0 for that criterion
- Mandatory criterion failure = 0 points for that criterion (no partial credit)
- If the draft file does not exist, return score 0 with empty criteria and a note that the draft is missing
- If the rubric file does not exist, return an error with `"error": "rubric not found: audit/semantic/document/{{ domain }}.md"`
