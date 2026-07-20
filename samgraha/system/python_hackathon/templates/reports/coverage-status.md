# Coverage Status — {{ standard }}

Generated: {{ generated_at }}

## Per-Team Summary

{{#teams}}
### {{ team_name }}
- Deterministic: {{ det_complete }}/10 domains
- Semantic: {{ sem_complete }}/10 domains ({{ sem_model_note }})
- Missing domains (deterministic): {{ det_missing_list }}
- Missing domains (semantic): {{ sem_missing_list }}
- Ready for final report: {{ ready_flag }}
{{/teams}}

## Competition-Wide

- Teams fully audited (deterministic): {{ fully_det_count }}/{{ total_teams }}
- Teams with at least one semantic model per domain: {{ fully_sem_count }}/{{ total_teams }}
