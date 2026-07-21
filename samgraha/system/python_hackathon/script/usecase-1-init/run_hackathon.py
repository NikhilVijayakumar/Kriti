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
import json
import os
import sys
import yaml
from dotenv import load_dotenv

load_dotenv()

_script_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(_script_dir, "common"))
sys.path.insert(0, os.path.join(_script_dir, "usecase-1-init"))

from db import get_conn, list_participants, register_participant, get_domain_scores
from det_audit import run_domain_audit, DOMAIN_AUDIT_MODULES

SYSTEM_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
WEIGHTS_FILE = os.path.join(SYSTEM_DIR, "calculation", "weights.yaml")


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


def process_deterministic(conn, participant_id, repo_path, domains):
    """Run deterministic audit for all domains for one team."""
    for domain in domains:
        if domain not in DOMAIN_AUDIT_MODULES:
            continue
        print(f"  [{domain}] Running...", end=" ")
        score = run_domain_audit(conn, participant_id, domain, repo_path)
        if score is None:
            print("FAILED")
        else:
            print("OK")


def process_participant(conn, participant, weights_cfg, deterministic_only=False):
    """Process one team's full cycle."""
    tname = participant["team_name"]
    repo_path = participant["repo_path"]
    participant_id = participant["id"]

    print(f"\n{'='*60}")
    print(f"Processing: {tname} ({repo_path})")
    print(f"{'='*60}")

    domains = list(weights_cfg["domains"].keys())

    process_deterministic(conn, participant_id, repo_path, domains)

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
            status = f"{len(models)} model(s): {', '.join(models)}" if models else "not started"
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

    new_count = _sync_teams(conn, args.standard)
    if new_count:
        print(f"Auto-registered {new_count} team(s) from teams.json")

    if args.register:
        name, repo_path, metadata_json = args.register
        metadata = json.loads(metadata_json) if metadata_json else None
        pid = register_participant(conn, args.standard, name, repo_path, metadata=metadata)
        print(f"Registered '{name}' (id={pid})")
        return

    weights_cfg = _load_weights()

    participants = list_participants(conn, args.standard)
    if not participants:
        print("No teams registered. Use --register NAME REPO_PATH METADATA_JSON")
        return

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
