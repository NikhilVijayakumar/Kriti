# Documentation - Semantic Audit

**Repository:** `{{ repo_name }}`
**Date:** `{{ evaluation_date }}`

## LLM Ensemble Breakdown
*Tracking the specific model evaluations.*

| Model Evaluator | Assigned Score | Reasoning |
|-----------------|----------------|-----------|
{{#model_results}}
| `{{ model_name }}` | {{ score }} | {{ reasoning }} |
{{/model_results}}

## Final Semantic Metrics
- **Mean Score:** {{ mean_score }}
- **Model Agreement:** {{ agreement_level }}
- **Standard Deviation:** {{ stdev_score }}

## Model Reasoning
{{#model_results}}
#### {{ model_name }} — {{ score }}/100
{{ reasoning }}
{{/model_results}}
