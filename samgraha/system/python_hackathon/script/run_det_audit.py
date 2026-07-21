#!/usr/bin/env python3
"""
run_det_audit.py — Run deterministic audits for all (or one) teams.

Reads teams from DB, runs each audit_*.py script against each team's repo,
evaluates rules, stores scores. This is use-case 2a.

Usage:
  python run_det_audit.py
  python run_det_audit.py --team "Goal GPT"
  python run_det_audit.py --db /path/to/hackathon.db
"""
import argparse
import importlib
import json
import os
import subprocess
import sys
import yaml

_script = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_script, "common"))
sys.path.insert(0, os.path.join(_script, "usecase-1-init"))
sys.path.insert(0, os.path.join(_script, "usecase-2a-det-audit"))

from db import get_conn, list_participants, upsert_domain_score, get_domain_scores

SYSTEM_DIR = os.path.join(_script, "..")
AGG_DIR = os.path.join(SYSTEM_DIR, "calculation", "aggregation", "domain")
AUDIT_DIR = os.path.join(_script, "usecase-2a-det-audit")

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


def _load_weights():
    weights_file = os.path.join(SYSTEM_DIR, "calculation", "weights.yaml")
    with open(weights_file, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return {k.replace("-", "_"): v for k, v in cfg["domains"].items()}


def _run_audit_script(script_name, repo_path, entrypoint=None):
    script_path = os.path.join(AUDIT_DIR, f"{script_name}.py")
    if not os.path.isfile(script_path):
        return None, f"Script not found: {script_path}"

    cmd = [sys.executable, script_path, "--repo", repo_path]
    if entrypoint and script_name == "audit_model_artifact":
        cmd.extend(["--entrypoint", entrypoint])

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return None, f"{script_name} timed out after 120s"

    if proc.returncode != 0 and not proc.stdout.strip():
        return None, f"{script_name} failed (rc={proc.returncode}): {proc.stderr[:500]}"

    try:
        evidence = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None, f"{script_name} output not JSON: {proc.stdout[:200]}"

    return evidence, None


def _discover_entrypoint(repo_path):
    for name in ("main.py", "app.py", "run.py"):
        if os.path.isfile(os.path.join(repo_path, name)):
            return name
    return None


def run_team(conn, participant, weights_cfg, skip_existing=False):
    """Run deterministic audits for one team. Returns (passed, failed) counts."""
    tname = participant["team_name"]
    repo_path = participant["repo_path"]
    pid = participant["id"]

    if not repo_path or not os.path.isdir(repo_path):
        print(f"  SKIP {tname}: repo_path not found ({repo_path})")
        return 0, 0

    # Check existing scores
    if skip_existing:
        existing = {r["domain"] for r in get_domain_scores(conn, pid)
                    if r["kind"] == "deterministic"}
        if len(existing) >= 10:
            print(f"  SKIP {tname}: already has 10/10 deterministic scores")
            return 10, 0

    print(f"\n  {tname} ({repo_path})")
    passed, failed = 0, 0

    for domain, module_name in DOMAIN_AUDIT_MODULES.items():
        entrypoint = None
        if domain == "runtime":
            entrypoint = _discover_entrypoint(repo_path)

        evidence, err = _run_audit_script(module_name, repo_path, entrypoint)
        if err:
            print(f"    [{domain}] ERROR: {err}")
            failed += 1
            continue

        if domain == "runtime":
            for fname in ("main.py", "app.py", "run.py"):
                evidence[fname] = os.path.isfile(os.path.join(repo_path, fname))

        # Import evaluate_domain from usecase-2a-det-audit
        spec = importlib.util.spec_from_file_location(
            "evaluate_rules", os.path.join(AUDIT_DIR, "evaluate_rules.py")
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        result = mod.evaluate_domain(domain, evidence)

        upsert_domain_score(conn, pid, domain, "deterministic", "",
                            result["score"], evidence=evidence)

        rules_passed = sum(1 for r in result["rules"] if r["passed"])
        total = len(result["rules"])
        print(f"    [{domain}] {result['score']}/100 ({rules_passed}/{total} rules)")
        passed += 1

    return passed, failed


def main():
    parser = argparse.ArgumentParser(
        description="Run deterministic audits for all teams"
    )
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--team", default=None, help="Process only this team")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip teams that already have all 10 scores")
    args = parser.parse_args()

    conn = get_conn(args.db)
    weights_cfg = _load_weights()
    participants = list_participants(conn, args.standard)

    if not participants:
        print("No teams registered. Run run_hackathon.py first.")
        sys.exit(1)

    if args.team:
        participants = [p for p in participants if p["team_name"] == args.team]
        if not participants:
            print(f"Team '{args.team}' not found")
            sys.exit(1)

    print(f"Running deterministic audits for {len(participants)} team(s)...")
    total_pass, total_fail = 0, 0

    for p in participants:
        passed, failed = run_team(conn, p, weights_cfg, args.skip_existing)
        total_pass += passed
        total_fail += failed

    print(f"\n{'='*50}")
    print(f"Done: {total_pass} domains scored, {total_fail} errors")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
