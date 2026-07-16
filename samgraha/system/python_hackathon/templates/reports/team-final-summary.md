# Team Final Aggregate Report

**Repository / Team:** `{{ repo_name }}`
**Date:** `{{ evaluation_date }}`
**Overall Rank:** `{{ team_rank }}` out of `{{ total_teams }}`

---

## 1. Hackathon Final Score
### Final Adjusted Mark: {{ final_score }} / 20

## 2. LLM Model Breakdown
*Tracking the aggregate mean assigned by each LLM across all semantic domains.*

| Model Evaluator | Aggregate Mean Score |
|-----------------|----------------------|
{{#each model_aggregate_scores}}
| `{{ this.model_name }}` | {{ this.mean_score }} |
{{/each}}

## 3. Domain Mark Summary
*The finalized scores for all 10 independent sections.*

| Domain Section | Final Adjusted Mark |
|----------------|---------------------|
| Infrastructure | {{ scores.infrastructure }} |
| Engineering Quality | {{ scores.engineering }} |
| Testing | {{ scores.testing }} |
| Documentation | {{ scores.documentation }} |
| Security | {{ scores.security }} |
| MLOps | {{ scores.mlops }} |
| Runtime | {{ scores.runtime }} |
| Team Workflow | {{ scores.team_workflow }} |
| Data Quality | {{ scores.data_quality }} |
| AI Explanations | {{ scores.ai_explanations }} |

## 4. Notable Strengths & Areas for Improvement
{{ executive_summary }}
