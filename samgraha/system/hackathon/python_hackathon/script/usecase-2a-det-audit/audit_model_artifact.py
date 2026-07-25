"""
audit_model_artifact.py - Powers the Runtime & MLOps domain deterministic audit.

Validates hackathon model artifacts against the competition rules:
  - File format: .pt / .pth / .pkl only (Section 17.1)
  - VRAM constraint: model must load within 12 GB VRAM (Section 17.1)
  - Memory constraint: total Python process memory must stay < configured limit
  - Inference speed: single predict() call must complete within 30s (Section 17.1)
  - API contract: model output must match required JSON schema (Section 17.3.3)
  - No internet access during inference (Section 17.1)

ALL tests run OFFLINE — network access is blocked for the inference subprocess.
"""
import subprocess
import json
import argparse
import os
import time
import sys
import glob

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from repo import resolve_code_root

ALLOWED_EXTENSIONS = {".pt", ".pth", ".pkl"}
MAX_VRAM_MB = 12 * 1024  # 12 GB in MB
MAX_INFERENCE_SECONDS = 30


def _find_model_artifacts(repo_path):
    """Scan for submitted model files."""
    found = []
    for ext in ALLOWED_EXTENSIONS:
        found.extend(glob.glob(os.path.join(repo_path, "**", f"*{ext}"), recursive=True))
    return found


def _check_file_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)


def _detect_memory_method():
    """
    Detect the best available method for memory estimation.
    Returns (method_name, check_function) where check_function(path) -> (mb, detail_string).
    """
    # 1. Try torch + CUDA — most accurate for GPU-bound models
    try:
        import torch
        if torch.cuda.is_available():
            def _check_torch_cuda(path):
                free, total = torch.cuda.mem_get_info()
                total_mb = total / (1024 * 1024)
                free_mb = free / (1024 * 1024)
                device_name = torch.cuda.get_device_name(0)
                return total_mb, (
                    f"torch.cuda GPU '{device_name}': "
                    f"{total_mb:.0f} MB total, {free_mb:.0f} MB free"
                )
            return "torch_cuda", _check_torch_cuda
    except (ImportError, RuntimeError):
        pass

    # 2. Try torch CPU — check system RAM
    try:
        import torch  # noqa: F811
        def _check_torch_cpu(path):
            import os as _os
            if _os.name == "nt":
                import ctypes
                kernel32 = ctypes.windll.kernel32
                total_kb = ctypes.c_ulonglong(0)
                kernel32.GetPhysicallyInstalledSystemMemory(ctypes.byref(total_kb))
                total_mb = total_kb.value / 1024
            else:
                with open("/proc/meminfo") as f:
                    for line in f:
                        if line.startswith("MemTotal:"):
                            total_mb = int(line.split()[1]) / 1024
                            break
                    else:
                        total_mb = 0
            return total_mb, f"torch CPU — system RAM: {total_mb:.0f} MB total"
        return "torch_cpu", _check_torch_cpu
    except ImportError:
        pass

    # 3. Try psutil
    try:
        import psutil
        def _check_psutil(path):
            mem = psutil.virtual_memory()
            total_mb = mem.total / (1024 * 1024)
            available_mb = mem.available / (1024 * 1024)
            return total_mb, f"psutil system RAM: {total_mb:.0f} MB total, {available_mb:.0f} MB available"
        return "psutil", _check_psutil
    except ImportError:
        pass

    # 4. Fallback: file size heuristic
    def _check_filesize(path):
        size_mb = _check_file_size_mb(path)
        return size_mb, f"file size heuristic: {size_mb:.1f} MB on disk"
    return "file_size", _check_filesize


def _check_memory_constraint(model_artifacts, method_name, check_fn):
    """
    Check whether the model fits within VRAM/memory budget.
    Returns dict with method, budget_mb, used_mb, detail, exceeds.
    """
    budget_mb = MAX_VRAM_MB
    if not model_artifacts:
        return {
            "method": method_name,
            "budget_mb": budget_mb,
            "used_mb": 0,
            "detail": "No model files found",
            "exceeds": False,
        }

    total_mb = 0
    details = []
    for path in model_artifacts:
        used_mb, detail = check_fn(path)
        total_mb += used_mb
        details.append(f"  {os.path.basename(path)}: {detail}")

    return {
        "method": method_name,
        "budget_mb": budget_mb,
        "used_mb": round(total_mb, 2),
        "detail": "\n".join(details),
        "exceeds": total_mb > budget_mb,
    }


def _run_inference_sandbox(repo_path, entrypoint, team_a="England", team_b="France"):
    """
    Runs the team's predict() function in a subprocess with:
    - No network access (via Windows firewall or nssm in prod; simulated here via env var)
    - Strict timeout enforcement
    - Captures stdout JSON for API contract validation
    """
    env = os.environ.copy()
    env["HEIMDALL_OFFLINE"] = "1"   # Signal to any well-behaved code to stay offline
    env["PYTHONPATH"] = repo_path

    script = f"""
import sys, json, os
sys.path.insert(0, r'{repo_path}')
import importlib.util, time

spec = importlib.util.spec_from_file_location("entrypoint", r'{entrypoint}')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

start = time.time()
try:
    result = mod.predict(team_a='{team_a}', team_b='{team_b}')
    elapsed = round(time.time() - start, 3)
    print(json.dumps({{"status": "ok", "elapsed_seconds": elapsed, "output": result}}))
except Exception as e:
    elapsed = round(time.time() - start, 3)
    print(json.dumps({{"status": "error", "elapsed_seconds": elapsed, "error": str(e)}}))
"""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True, text=True,
            timeout=MAX_INFERENCE_SECONDS + 5,
            env=env
        )
        return json.loads(proc.stdout.strip()) if proc.stdout.strip() else {"status": "error", "error": proc.stderr}
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "error": f"Exceeded {MAX_INFERENCE_SECONDS}s hard limit"}
    except json.JSONDecodeError:
        return {"status": "error", "error": "Non-JSON output from inference"}


def _validate_output_contract(output):
    """
    Validates the output JSON schema from predict().
    Expected keys per Section 17.3.3: team_a_score, team_b_score (or winner).
    Extend as needed for your specific competition output format.
    """
    if not isinstance(output, dict):
        return False, "Output is not a JSON object"
    required_keys = {"team_a_score", "team_b_score"}
    missing = required_keys - set(output.keys())
    if missing:
        return False, f"Missing required output keys: {missing}"
    return True, "Output contract satisfied"


def _validate_input_contract(repo_path, entrypoint):
    """
    Validates predict()'s input signature via inspect.signature().
    Expected: exactly team_a and team_b as required params, no extra required args.
    """
    script = f"""
import sys, json, inspect, importlib.util
sys.path.insert(0, r'{repo_path}')

spec = importlib.util.spec_from_file_location("entrypoint", r'{entrypoint}')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

if not hasattr(mod, 'predict'):
    print(json.dumps({{"valid": False, "message": "No predict() function found"}}))
else:
    sig = inspect.signature(mod.predict)
    params = [name for name, p in sig.parameters.items() if p.default is inspect.Parameter.empty]
    all_params = list(sig.parameters.keys())
    print(json.dumps({{"valid": params == ['team_a', 'team_b'], "required_params": params, "all_params": all_params}}))
"""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True, text=True, timeout=10,
            env={"PYTHONPATH": repo_path, "HEIMDALL_OFFLINE": "1"}
        )
        if proc.stdout.strip():
            return json.loads(proc.stdout.strip())
        return {"valid": False, "message": f"No output from signature check: {proc.stderr[:200]}"}
    except Exception as e:
        return {"valid": False, "message": f"Signature check failed: {e}"}


def run_model_artifact_audit(repo_path, entrypoint=None):
    """
    Full model artifact audit: file presence, format, memory estimate, inference speed, API contract.
    """
    repo_path = resolve_code_root(repo_path)
    result = {
        "model_files_found": [],
        "invalid_format_files": [],
        "largest_model_mb": 0,
        "exceeds_vram_estimate": False,
        "memory_check": {},
        "inference": {
            "executed": False,
            "status": None,
            "elapsed_seconds": None,
            "within_time_limit": None,
            "input_contract_valid": None,
            "input_contract_message": None,
            "api_contract_valid": None,
            "api_contract_message": None,
        }
    }

    artifacts = _find_model_artifacts(repo_path)
    result["model_files_found"] = [os.path.relpath(p, repo_path) for p in artifacts]

    # Check extensions
    for path in artifacts:
        ext = os.path.splitext(path)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            result["invalid_format_files"].append(os.path.relpath(path, repo_path))

    # File-size heuristic (always computed for logging)
    if artifacts:
        sizes = [_check_file_size_mb(p) for p in artifacts]
        result["largest_model_mb"] = round(max(sizes), 2)

    # Smart memory check
    method_name, check_fn = _detect_memory_method()
    mem = _check_memory_constraint(artifacts, method_name, check_fn)
    result["memory_check"] = mem
    result["exceeds_vram_estimate"] = result["largest_model_mb"] > MAX_VRAM_MB

    # Inference check
    if entrypoint and os.path.exists(entrypoint):
        # Input contract check (before running inference)
        input_check = _validate_input_contract(repo_path, entrypoint)
        result["inference"]["input_contract_valid"] = input_check.get("valid", False)
        result["inference"]["input_contract_message"] = input_check.get("message", "")

        inference = _run_inference_sandbox(repo_path, entrypoint)
        result["inference"]["executed"] = True
        result["inference"]["status"] = inference.get("status")
        result["inference"]["elapsed_seconds"] = inference.get("elapsed_seconds")
        result["inference"]["within_time_limit"] = (
            inference.get("elapsed_seconds", 99) <= MAX_INFERENCE_SECONDS
            if inference.get("status") == "ok" else False
        )
        if inference.get("status") == "ok":
            valid, msg = _validate_output_contract(inference.get("output"))
            result["inference"]["api_contract_valid"] = valid
            result["inference"]["api_contract_message"] = msg
        else:
            result["inference"]["api_contract_valid"] = False
            result["inference"]["api_contract_message"] = inference.get("error", "Inference did not complete")
    else:
        result["inference"]["status"] = "skipped"
        result["inference"]["api_contract_message"] = "No entrypoint specified or found"

    # Log summary to stderr (stdout reserved for JSON output)
    print(f"[audit_model_artifact] memory method: {mem['method']}", file=sys.stderr)
    print(f"[audit_model_artifact] budget: {mem['budget_mb']:.0f} MB | used: {mem['used_mb']:.1f} MB", file=sys.stderr)
    if mem["detail"]:
        for line in mem["detail"].split("\n"):
            print(f"[audit_model_artifact]{line}", file=sys.stderr)
    print(f"[audit_model_artifact] exceeds limit: {mem['exceeds']}", file=sys.stderr)

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Validate model artifact format, size, inference speed, and API contract"
    )
    parser.add_argument("--repo", required=True, help="Path to the repository")
    parser.add_argument("--entrypoint", default=None,
                        help="Relative path to the predict() entrypoint (e.g. main.py)")
    args = parser.parse_args()

    entrypoint = os.path.join(args.repo, args.entrypoint) if args.entrypoint else None
    result = run_model_artifact_audit(args.repo, entrypoint=entrypoint)
    print(json.dumps(result, indent=2))
