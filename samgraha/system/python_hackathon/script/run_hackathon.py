"""
run_hackathon.py — Orchestrator for the python_hackathon scoring pipeline.

Processes one participant's full deterministic-then-semantic cycle before
starting the next. Follows loop.yaml's stage order.

Usage:
  python run_hackathon.py --standard python_hackathon
  python run_hackathon.py --standard python_hackathon --participant team_alpha
  python run_hackathon.py --standard python_hackathon --deterministic-only
"""
import argparse
import importlib
import json
import os
import subprocess
import sys
import yaml
from dotenv import load_dotenv

load_dotenv()

# Add script dir to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from db import (
    get_conn, list_participants, register_participant,
    upsert_domain_score, now_iso,
)
from evaluate_rules import evaluate_domain, load_rules

SYSTEM_DIR = os.path.join(os.path.dirname(__file__), "..")
WEIGHTS_FILE = os.path.join(SYSTEM_DIR, "calculation", "weights.yaml")
AGG_DIR = os.path.join(SYSTEM_DIR, "calculation", "aggregation", "domain")

# Map domain names to their audit script module names
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

# Domains with no audit script (§0 bug #3) — deterministic pass is skipped
DOMAINS_NO_AUDIT_SCRIPT = set()


def _load_teams():
    """Load teams from TEAMS_JSON env path. Returns list of team dicts or empty list."""
    teams_path = os.environ.get("PYTHON_HACKATHON_TEAMS_JSON", "")
    if not teams_path or not os.path.isfile(teams_path):
        return []
    with open(teams_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _sync_teams(conn, standard):
    """Register any teams from teams.json not already in DB. Returns count of new."""
    teams = _load_teams()
    if not teams:
        return 0
    count = 0
    for t in teams:
        team_name = t.get("team_name")
        if not team_name:
            continue
        existing = conn.execute(
            "SELECT id FROM standard_participants WHERE standard=? AND team_name=?",
            (standard, team_name),
        ).fetchone()
        if existing:
            continue
        register_participant(
            conn, standard, team_name,
            repo_path=t.get("repo_path", ""),
            team_leader=t.get("team_leader"),
            members=t.get("members"),
            repo_https=t.get("repo_https"),
            repo_ssh=t.get("repo_ssh"),
            team_code=t.get("team_code"),
        )
        count += 1
        print(f"  Registered from teams.json: {team_name}")
    return count


def _load_weights():
    with open(WEIGHTS_FILE, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["domains"] = {k.replace("-", "_"): v for k, v in cfg["domains"].items()}
    return cfg


def _discover_entrypoint(repo_path):
    """Discover main.py/app.py/run.py in the repo root for audit_model_artifact.py."""
    for name in ("main.py", "app.py", "run.py"):
        if os.path.isfile(os.path.join(repo_path, name)):
            return name
    return None


def _run_audit_script(script_name, repo_path, entrypoint=None):
    """
    Run an audit_*.py script and return its JSON output.
    Returns (raw_evidence_dict, error_string_or_None).
    """
    script_path = os.path.join(os.path.dirname(__file__), f"{script_name}.py")
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


def _get_domain_agg_weights(domain_dirname):
    """Read det/sem weights from calculation/aggregation/domain/{domain_dirname}.yaml."""
    agg_file = os.path.join(AGG_DIR, f"{domain_dirname}.yaml")
    if os.path.isfile(agg_file):
        with open(agg_file, "r", encoding="utf-8") as f:
            agg = yaml.safe_load(f)
        w = agg.get("weights", {})
        return w.get("deterministic", 0.60), w.get("semantic", 0.40)
    return 0.60, 0.40


def process_deterministic(conn, participant_id, team_name, repo_path, domain, weights_cfg):
    """Run deterministic audit for one team + domain. Stores score in DB."""
    audit_module_name = DOMAIN_AUDIT_MODULES.get(domain)

    if domain in DOMAINS_NO_AUDIT_SCRIPT:
        print(f"  [{domain}] No audit script — skipping deterministic (missing-domain handling)")
        return None

    if not audit_module_name:
        print(f"  [{domain}] Unknown audit module — skipping")
        return None

    # Discover entrypoint for runtime domain
    entrypoint = None
    if domain == "runtime":
        entrypoint = _discover_entrypoint(repo_path)
        if not entrypoint:
            print(f"  [{domain}] No entrypoint found (main.py/app.py/run.py) — run-001 will fail")

    # Run the audit script
    print(f"  [{domain}] Running {audit_module_name}...", end=" ")
    evidence, err = _run_audit_script(audit_module_name, repo_path, entrypoint)
    if err:
        print(f"ERROR: {err}")
        return None
    print("OK")

    # Inject entrypoint presence for runtime domain (run-001)
    if domain == "runtime":
        for name in ("main.py", "app.py", "run.py"):
            evidence[name] = os.path.isfile(os.path.join(repo_path, name))

    # Evaluate rules against raw evidence
    result = evaluate_domain(domain, evidence)
    score = result["score"]

    # Store in DB
    upsert_domain_score(
        conn, participant_id, domain, "deterministic", "",
        score, evidence=evidence,
    )

    passed = sum(1 for r in result["rules"] if r["passed"])
    total = len(result["rules"])
    print(f"  [{domain}] Score: {score}/100 ({passed}/{total} rules passed)")
    return score


def process_participant(conn, participant, weights_cfg, deterministic_only=False):
    """Process one team's full cycle."""
    tname = participant["team_name"]
    repo_path = participant["repo_path"]
    participant_id = participant["id"]

    print(f"\n{'='*60}")
    print(f"Processing: {tname} ({repo_path})")
    print(f"{'='*60}")

    domains = list(weights_cfg["domains"].keys())

    for domain in domains:
        # Deterministic pass
        process_deterministic(conn, participant_id, tname, repo_path, domain, weights_cfg)

        if not deterministic_only:
            # Semantic pass is agent-driven — nothing to run here.
            # The semantic scores accumulate as agent sessions write to DB.
            # Print coverage info.
            pass

    # Print semantic coverage summary
    if not deterministic_only:
        from db import get_domain_scores
        rows = get_domain_scores(conn, participant_id)
        sem_by_domain = {}
        for r in rows:
            if r["kind"] == "semantic":
                sem_by_domain.setdefault(r["domain"], []).append(r["model"])
        print(f"\n  Semantic coverage:")
        for d in domains:
            models = sem_by_domain.get(d, [])
            if d in DOMAINS_NO_AUDIT_SCRIPT:
                status = "no audit script"
            elif models:
                status = f"{len(models)} model(s): {', '.join(models)}"
            else:
                status = "not started"
            print(f"    {d}: {status}")


def main():
    parser = argparse.ArgumentParser(
        description="Orchestrate the python_hackathon scoring pipeline"
    )
    parser.add_argument("--standard", default="python_hackathon", help="Standard name")
    parser.add_argument("--db", default=None, help="Path to SQLite DB")
    parser.add_argument("--team", default=None, help="Process only this team")
    parser.add_argument("--deterministic-only", action="store_true",
                        help="Only run deterministic audits (skip semantic tracking)")
    parser.add_argument("--register", nargs=3, metavar=("TEAM_NAME", "REPO_PATH", "METADATA_JSON"),
                        help="Register a team: TEAM_NAME REPO_PATH METADATA_JSON")
    args = parser.parse_args()

    conn = get_conn(args.db)

    # Auto-register teams from teams.json if present
    new_count = _sync_teams(conn, args.standard)
    if new_count:
        print(f"Auto-registered {new_count} team(s) from teams.json")

    # Register mode
    if args.register:
        name, repo_path, metadata_json = args.register
        metadata = json.loads(metadata_json) if metadata_json else None
        pid = register_participant(conn, args.standard, name, repo_path, metadata=metadata)
        print(f"Registered '{name}' (id={pid})")
        return

    weights_cfg = _load_weights()

    # List participants
    participants = list_participants(conn, args.standard)
    if not participants:
        print("No teams registered. Use --register NAME REPO_PATH METADATA_JSON")
        return

    # Filter to single team if specified
    if args.team:
        participants = [p for p in participants if p["team_name"] == args.team]
        if not participants:
            print(f"Team '{args.team}' not found")
            return

    print(f"Processing {len(participants)} team(s) for {args.standard}")

    for p in participants:
        process_participant(conn, p, weights_cfg, args.deterministic_only)

    print(f"\n{'='*60}")
    print("Done. Scores stored in DB.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
