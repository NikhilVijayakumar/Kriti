import json
import argparse
import os

def run_mlops_audit(repo_path):
    """
    Checks for DVC and MLflow configurations.
    """
    result = {
        "dvc_configured": False,
        "mlflow_configured": False,
        "data_directory_present": False
    }
    
    # Check DVC
    if os.path.exists(os.path.join(repo_path, ".dvc")) or \
       os.path.exists(os.path.join(repo_path, "dvc.yaml")):
        result["dvc_configured"] = True
        
    # Check MLflow (often track locally in mlruns/)
    if os.path.exists(os.path.join(repo_path, "mlruns")):
        result["mlflow_configured"] = True
        
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
