# Semantic Audit — {{ unit }}

## Task

1. Read the rubric from `common/codegen/audit/semantic/{{ branch }}/{{ unit }}.md`
2. Read the generated artifact for this unit (the crate's error type / test
   file / CI config, as located by the calling script) and the upstream
   documentation sections named in the unit's own profile
   (`common/codegen/{{ branch }}/profile/{{ unit }}.yaml` `required_inputs`)
3. For each criterion in the rubric:
   - Determine if the criterion **passes** or **fails** based on observable
     evidence
   - Assign **points** proportional to evidence quality
   - Record **evidence** — quote or paraphrase the specific passage
4. Compute the total score:
   ```
   score = sum(points where passed=true), capped at 100
   ```
   Mandatory criterion failure forfeits that criterion's points entirely.
5. Output the result as structured JSON:
   ```json
   {
     "unit": "{{ unit }}",
     "score": 0,
     "criteria": [
       {"criterion_id": "C1", "passed": true, "points_awarded": 0, "evidence": ""}
     ]
   }
   ```
