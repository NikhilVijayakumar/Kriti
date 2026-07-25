import json
import argparse
import os
import sys
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from repo import resolve_code_root


def run_mlops_audit(repo_path):
    """
    Checks for DVC and MLflow configurations with deeper inspection.
    """
    repo_path = resolve_code_root(repo_path)
    result = {
        "dvc_configured": False,
        "mlflow_configured": False,
        "data_directory_present": False,
        # New: deeper inspection
        "dvc_stages": [],
        "dvc_stage_count": 0,
        "mlflow_run_count": 0,
        "mlflow_runs": [],
    }

    # Check DVC
    dvc_yaml = os.path.join(repo_path, "dvc.yaml")
    dvc_dir = os.path.join(repo_path, ".dvc")

    if os.path.exists(dvc_yaml) or os.path.exists(dvc_dir):
        result["dvc_configured"] = True

    # Parse dvc.yaml for pipeline stages
    if os.path.isfile(dvc_yaml):
        try:
            with open(dvc_yaml, "r", encoding="utf-8") as f:
                dvc_cfg = yaml.safe_load(f)
            if isinstance(dvc_cfg, dict):
                stages = dvc_cfg.get("stages", {})
                if isinstance(stages, dict):
                    result["dvc_stages"] = list(stages.keys())
                    result["dvc_stage_count"] = len(stages)
        except (yaml.YAMLError, OSError):
            pass

    # Check MLflow — count actual run directories under mlruns/
    mlruns_dir = os.path.join(repo_path, "mlruns")
    if os.path.isdir(mlruns_dir):
        result["mlflow_configured"] = True
        run_count = 0
        run_ids = []
        for entry in os.listdir(mlruns_dir):
            entry_path = os.path.join(mlruns_dir, entry)
            # MLflow layout: mlruns/<experiment_id>/<run_id>/...
            # or mlruns/<experiment_name>/<run_id>/...
            if os.path.isdir(entry_path):
                for sub in os.listdir(entry_path):
                    sub_path = os.path.join(entry_path, sub)
                    if os.path.isdir(sub_path) and len(sub) >= 8:
                        # Likely a run UUID directory
                        run_count += 1
                        if len(run_ids) < 10:
                            run_ids.append(sub)
        result["mlflow_run_count"] = run_count
        result["mlflow_runs"] = run_ids

    # Check generic data dir
    if os.path.exists(os.path.join(repo_path, "data")) or \
       os.path.exists(os.path.join(repo_path, "dataset")):
        result["data_directory_present"] = True

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Path to the repository")
    args = parser.parse_args()

    audit_results = run_mlops_audit(args.repo)
    print(json.dumps(audit_results, indent=2))
