#!/usr/bin/env python3
"""coverage_report.py — Progress snapshot showing how far along each team is.

Writes to python_hackathon/reports/coverage-status.md by default.
Answers "how far along is each team" — softer than strict yes/no verify scripts.
Useful mid-competition when most teams are legitimately incomplete.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import chevron
from db import get_conn, list_participants, get_domain_scores, get_canonical_domains

ALL_DOMAINS = get_canonical_domains()

TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "templates", "reports", "coverage-status.md"
)


def build_coverage_data(conn, standard, team_filter=None):
    participants = list_participants(conn, standard)
    if team_filter:
        participants = [p for p in participants if p["team_name"] == team_filter]

    teams_data = []
    for p in participants:
        rows = get_domain_scores(conn, p["id"])
        det_domains = {r["domain"] for r in rows if r["kind"] == "deterministic"}
        sem_domains = {r["domain"] for r in rows if r["kind"] == "semantic"}

        det_missing = [d for d in ALL_DOMAINS if d not in det_domains]
        sem_missing = [d for d in ALL_DOMAINS if d not in sem_domains]

        teams_data.append({
            "team_name": p["team_name"],
            "det_complete": len(det_domains),
            "sem_complete": len(sem_domains),
            "sem_model_note": f"{len({r['model'] for r in rows if r['kind'] == 'semantic'})} model(s)",
            "det_missing_list": ", ".join(det_missing) if det_missing else "none",
            "sem_missing_list": ", ".join(sem_missing) if sem_missing else "none",
            "ready_flag": "yes" if len(det_domains) == 10 and len(sem_domains) >= 1 else "no",
        })

    fully_det = sum(1 for t in teams_data if t["det_complete"] == 10)
    fully_sem = sum(1 for t in teams_data if t["sem_complete"] == 10)

    return {
        "generated_at": "now",
        "teams": teams_data,
        "fully_det_count": fully_det,
        "fully_sem_count": fully_sem,
        "total_teams": len(teams_data),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--team", default=None)
    parser.add_argument("--output", default=None, help="Output path (default: reports/coverage-status.md)")
    args = parser.parse_args()

    conn = get_conn(args.db)
    data = build_coverage_data(conn, args.standard, args.team)

    with open(TEMPLATE_PATH, "r", encoding="utf-8-sig") as f:
        template = f.read()

    rendered = chevron.render(template, data)

    out_path = args.output or os.path.join(
        os.path.dirname(__file__), "..", "..", "reports", "coverage-status.md"
    )
    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Coverage report -> {out_path}")

    for t in data["teams"]:
        ready = "+" if t["ready_flag"] == "yes" else "-"
        print(f"  [{ready}] {t['team_name']}: det {t['det_complete']}/10, sem {t['sem_complete']}/10")


if __name__ == "__main__":
    main()
