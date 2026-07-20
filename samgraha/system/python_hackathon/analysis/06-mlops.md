# MLOps Analysis Prompt

Guides the per-team analysis for the MLOps domain — read by whichever
agent runs it via MCP, after scoring has completed. Explains a team's
experiment reproducibility posture. Not parsed by a script — this is a
prompt.

## Version
1.0.0

## Analysis Intent
MLOps scores (weight: 10) measure experiment reproducibility through
DVC and MLflow adoption. In a hackathon context, tracking data/model
lineage separates professional-grade submissions from quick scripts.
This step interprets MLOps tooling evidence.

## Inputs
- `standard_domain_scores` DB table — all teams' mlops domain scores
  (queried via MCP)
- Per-team deterministic findings: `.dvc` directory, `dvc.yaml` pipeline,
  `mlruns/` directory, `mlflow` usage in code
- Semantic findings: pipeline stage quality, run tracking completeness,
  data versioning coverage

## Narrative Guidance
The MLOps narrative must cover:
1. **Score Overview** — team's MLOps score out of 10, with competition
   average comparison. MLOps is the differentiator between a script
   and a system.
2. **DVC Presence** — does `.dvc/` or `dvc.yaml` exist? DVC config
   is the primary evidence of data versioning intent.
3. **Pipeline Stages** — if `dvc.yaml` exists, what stages are defined?
   List them (e.g., `prepare`, `train`, `evaluate`). Empty or single-
   stage pipelines score lower than multi-stage ones.
4. **MLflow Integration** — is `mlruns/` present or is MLflow imported
   in code? Experiment tracking with MLflow demonstrates professional
   ML workflow discipline.
5. **Data Versioning** — are actual data files tracked via DVC (`.gitignore`
   + `.dvc` tracking files)? Or is DVC installed but unused?
6. **Strengths** — complete DVC pipeline with multiple stages, MLflow
   tracking with parameters/metrics logged, data and models both
   versioned.
7. **Weaknesses** — no DVC config, DVC installed but no pipeline
   defined, no experiment tracking, model artifacts not versioned.
8. **Recommendations** — "define `dvc.yaml` with prepare/train/evaluate
   stages", "add `mlflow.log_param()` calls in training script",
   "track `data/` directory with `dvc add`".

## Visualization Guidance
- `domain_scores` — always include.
- `pipeline_stages` — include if DVC data available: pipeline DAG
  visualization.
- `tool_adoption` — include: stacked bar of DVC/MLflow/both/neither
  across teams.

## Output Schema
```json
{
  "domain": "06-mlops",
  "sections": [
    {"heading": "Score Overview", "text": "..."},
    {"heading": "DVC Presence", "text": "..."},
    {"heading": "Pipeline Stages", "text": "..."},
    {"heading": "MLflow Integration", "text": "..."},
    {"heading": "Data Versioning", "text": "..."},
    {"heading": "Strengths", "text": "..."},
    {"heading": "Weaknesses", "text": "..."},
    {"heading": "Recommendations", "text": "..."}
  ]
}
```
