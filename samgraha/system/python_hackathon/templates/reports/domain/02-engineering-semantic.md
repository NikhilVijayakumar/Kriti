# Engineering - Semantic Audit

**Repository:** `{{ repo_name }}`
**Date:** `{{ evaluation_date }}`

## LLM Ensemble Breakdown
*Tracking the specific model evaluations.*

| Model Evaluator | Assigned Score | Reasoning |
|-----------------|----------------|-----------|
{{#each model_results}}
| `{{ this.model_name }}` | {{ this.score }} | {{ this.reasoning }} |
{{/each}}

## Final Semantic Metrics
- **Median Score:** {{ median_score }}
- **Model Agreement:** {{ agreement_level }}
- **Standard Deviation:** {{ stdev_score }}
