import json
import argparse
import os

def run_infrastructure_audit(repo_path):
    """
    Verifies the presence of uv.lock and Docker infrastructure.
    """
    result = {
        "uv_lock_present": False,
        "dockerfile_present": False,
        "docker_compose_present": False
    }
    
    if os.path.exists(os.path.join(repo_path, "uv.lock")):
        result["uv_lock_present"] = True
        
    if os.path.exists(os.path.join(repo_path, "Dockerfile")):
        result["dockerfile_present"] = True
        
    if os.path.exists(os.path.join(repo_path, "docker-compose.yaml")) or \
       os.path.exists(os.path.join(repo_path, "docker-compose.yml")):
        result["docker_compose_present"] = True

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Path to the repository")
    args = parser.parse_args()
    
    audit_results = run_infrastructure_audit(args.repo)
    print(json.dumps(audit_results, indent=2))
