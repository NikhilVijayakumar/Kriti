"""
det_audit.py — Shared deterministic audit logic.

Single source of truth for:
  - Audit script invocation (subprocess)
  - Domain-to-module mapping
  - Entrypoint discovery
  - Per-domain audit execution + DB write

Used by: run_hackathon.py, run_det_audit.py, run_pipeline.py
"""
import importlib.util
import json
import os
import subprocess
import sys
import yaml

AUDIT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "usecase-2a-det-audit")

# Bootstrap source only — read once by hackathon_schema.seed_domains() into
# hackathon_domains.audit_module at schema-init time, same status as
# weights.yaml. run_domain_audit() below reads the DB column at runtime, not
# this dict — every domain-to-module lookup after schema-init goes through
# the DB, same as weights/order/display_name.
DOMAIN_AUDIT_MODULES = {
    "infrastructure": "audit_infrastructure",
    "engineering": "audit_python",
    "testing": "audit_testing",
    "documentation": "audit_documentation",
    "security": "audit_security",
    "mlops": "audit_mlops",
    "runtime": "audit_model_artifact",
    "team_workflow": "audit_git",
    "data_quality": "audit_data_quality",
    "ai_explanations": "audit_ai_explanations",
}


def discover_entrypoint(repo_path):
    """Find main.py/app.py/run.py in repo root for audit_model_artifact."""
    for name in ("main.py", "app.py", "run.py"):
        if os.path.isfile(os.path.join(repo_path, name)):
            return name
    return None


def run_audit_script(script_name, repo_path, entrypoint=None):
    """
    Run an audit_*.py script and return its JSON output.
    Returns (evidence_dict_or_None, error_string_or_None).
    """
    script_path = os.path.join(AUDIT_DIR, f"{script_name}.py")
    if not os.path.isfile(script_path):
        return None, f"Script not found: {script_path}"

    cmd = [sys.executable, script_path, "--repo", repo_path]
    if entrypoint and script_name == "audit_model_artifact":
        cmd.extend(["--entrypoint", entrypoint])

    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        return None, f"{script_name} timed out after 120s"

    if proc.returncode != 0 and not proc.stdout.strip():
        return None, f"{script_name} failed (rc={proc.returncode}): {proc.stderr[:500]}"

    try:
        evidence = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None, f"{script_name} output not JSON: {proc.stdout[:200]}"

    return evidence, None


def run_domain_audit(conn, participant_id, domain, repo_path):
    """
    Run deterministic audit for one domain against a repo.
    Evaluates rules, stores score in DB.
    Returns score (0-100) or None on failure.
    """
    from hackathon_schema import upsert_domain_score, get_audit_module

    # evaluate_rules lives in usecase-2a-det-audit/, load dynamically
    _spec = importlib.util.spec_from_file_location(
        "evaluate_rules", os.path.join(AUDIT_DIR, "evaluate_rules.py")
    )
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    evaluate_domain = _mod.evaluate_domain

    # audit_module comes from hackathon_domains (seeded from DOMAIN_AUDIT_MODULES
    # once, at schema-init time) — not read from that in-code dict at runtime.
    module_name = get_audit_module(conn, domain)
    if not module_name:
        return None

    # Discover entrypoint for runtime domain
    entrypoint = None
    if domain == "runtime":
        entrypoint = discover_entrypoint(repo_path)

    evidence, err = run_audit_script(module_name, repo_path, entrypoint)
    if err:
        print(f"    [{domain}] ERROR: {err}")
        return None

    # Inject entrypoint presence for runtime domain (run-001)
    if domain == "runtime":
        for fname in ("main.py", "app.py", "run.py"):
            evidence[fname] = os.path.isfile(os.path.join(repo_path, fname))

    result = evaluate_domain(domain, evidence)
    score = result["score"]

    upsert_domain_score(conn, participant_id, domain, "deterministic", "", score, evidence=evidence)

    passed = sum(1 for r in result["rules"] if r["passed"])
    total = len(result["rules"])
    print(f"    [{domain}] {score}/100 ({passed}/{total} rules)")
    return score
