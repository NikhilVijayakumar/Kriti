import subprocess
import json
import argparse
import os
import glob

def run_python_audit(repo_path):
    """
    Checks for Python static analysis configurations (Radon, Bandit, Mypy)
    and executes them if possible.
    """
    result = {
        "static_typing_enabled": False,
        "radon_config_found": False,
        "bandit_config_found": False,
    }
    
    # 1. Check Configurations
    pyproject_path = os.path.join(repo_path, "pyproject.toml")
    radon_cfg = os.path.join(repo_path, "radon.cfg")
    bandit_cfg = os.path.join(repo_path, ".bandit")
    
    if os.path.exists(radon_cfg):
        result["radon_config_found"] = True
        
    if os.path.exists(bandit_cfg):
        result["bandit_config_found"] = True
        
    if os.path.exists(pyproject_path):
        with open(pyproject_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if "tool.mypy" in content or "tool.pyright" in content:
                result["static_typing_enabled"] = True
            if "tool.radon" in content:
                result["radon_config_found"] = True
            if "tool.bandit" in content:
                result["bandit_config_found"] = True

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Path to the python repository")
    args = parser.parse_args()
    
    audit_results = run_python_audit(args.repo)
    print(json.dumps(audit_results, indent=2))
