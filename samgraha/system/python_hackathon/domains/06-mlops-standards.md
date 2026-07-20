# 06. MLOps Standards

**Domain:** MLOps
**Audit Target:** `.dvc`, `dvc.yaml`, `mlruns/`

## Standard Definition
For AI and ML-focused hackathons, experiment reproducibility is critical. The project should track data and model lineage alongside the Git history, and record MLflow experiments.

### Expected Evidence
1. **Data Versioning:** The presence of DVC configuration files to track datasets and models.
2. **DVC Stages:** At least one pipeline stage defined in `dvc.yaml`.
3. **MLflow Runs:** At least one experiment recorded in `mlruns/`.
