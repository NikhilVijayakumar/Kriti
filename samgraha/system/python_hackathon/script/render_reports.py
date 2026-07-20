"""
render_reports.py — Render all 32 markdown templates using chevron.

Five data-fetch functions, one per template kind, feeding chevron.render().
"""
import chevron
import json
import os
import yaml
from datetime import datetime, timezone

SYSTEM_DIR = os.path.join(os.path.dirname(__file__), "..")
TEMPLATES_DIR = os.path.join(SYSTEM_DIR, "templates", "reports")
DOMAINS = [
    "01-infrastructure", "02-engineering", "03-testing",
    "04-documentation", "05-security", "06-mlops",
    "07-runtime", "08-team-workflow", "09-data-quality",
    "10-ai-explanations",
]
DOMAIN_NAMES = [
    "infrastructure", "engineering", "testing",
    "documentation", "security", "mlops",
    "runtime", "team_workflow", "data_quality",
    "ai_explanations",
]


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _load_template(relative_path):
    """Load a template file and return its content string."""
    path = os.path.join(TEMPLATES_DIR, relative_path)
    with open(path, "r", encoding="utf-8-sig") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Data-fetch functions
# ---------------------------------------------------------------------------

def fetch_deterministic_data(conn, participant_id, domain_name, repo_name=""):
    """
    Data for {domain}-deterministic.md templates.
    Reads raw_evidence_json from the deterministic score row.
    """
    from db import get_domain_scores
    rows = get_domain_scores(conn, participant_id, domain_name)
    det_row = None
    for r in rows:
        if r["kind"] == "deterministic":
            det_row = r
            break

    evidence = {}
    if det_row and det_row["raw_evidence_json"]:
        evidence = json.loads(det_row["raw_evidence_json"])

    # Build rule results from evidence
    # The rules are in audit/deterministic/document/{domain}.yaml
    from evaluate_rules import evaluate_domain
    result = evaluate_domain(domain_name, evidence)

    findings = []
    for r in result["rules"]:
        status = "PASS" if r["passed"] else "FAIL"
        findings.append(f"- [{status}] **{r['id']}**: {r['detail']}")

    return {
        "repo_name": repo_name,
        "evaluation_date": _now(),
        "deterministic_rules": result["rules"],
        "deterministic_findings": "\n".join(findings) if findings else "No findings.",
    }


def fetch_semantic_data(conn, participant_id, domain_name, repo_name=""):
    """
    Data for {domain}-semantic.md templates.
    Reads all semantic rows for this (participant, domain).
    """
    from db import get_domain_scores
    import math

    rows = get_domain_scores(conn, participant_id, domain_name)
    model_results = []
    scores = []
    for r in rows:
        if r["kind"] == "semantic" and r["model"]:
            evidence = json.loads(r["raw_evidence_json"]) if r["raw_evidence_json"] else {}
            model_results.append({
                "model_name": r["model"],
                "score": r["score"],
                "reasoning": evidence.get("reasoning", ""),
            })
            scores.append(r["score"])

    mean_score = round(sum(scores) / len(scores), 2) if scores else 0
    stdev_score = round(math.sqrt(sum((x - mean_score) ** 2 for x in scores) / max(len(scores) - 1, 1)), 2) if len(scores) > 1 else 0
    if stdev_score <= 5:
        agreement = "High"
    elif stdev_score <= 15:
        agreement = "Medium"
    else:
        agreement = "Low"

    return {
        "repo_name": repo_name,
        "evaluation_date": _now(),
        "model_results": model_results,
        "mean_score": mean_score,
        "agreement_level": agreement,
        "stdev_score": stdev_score,
    }


def fetch_summary_data(conn, participant_id, domain_name, domain_stats, adjusted_scores,
                        repo_name="", participant_name=""):
    """
    Data for {domain}-summary.md templates.
    Combines det/sem scores with z-score stats.
    """
    from db import get_domain_scores, get_all_scores_as_dict

    rows = get_domain_scores(conn, participant_id, domain_name)
    det_score = 0.0
    sem_scores = []
    for r in rows:
        if r["kind"] == "deterministic":
            det_score = r["score"]
        elif r["kind"] == "semantic":
            sem_scores.append(r["score"])

    sem_mean = round(sum(sem_scores) / len(sem_scores), 2) if sem_scores else 0

    # Read aggregation weights
    import glob as globmod
    agg_dir = os.path.join(SYSTEM_DIR, "calculation", "aggregation", "domain")
    det_w, sem_w = 0.60, 0.40
    matches = globmod.glob(os.path.join(agg_dir, f"*-{domain_name.replace('_', '-')}.yaml"))
    if matches:
        try:
            with open(matches[0], "r", encoding="utf-8") as f:
                agg = yaml.safe_load(f)
            w = agg.get("weights", {})
            det_w = w.get("deterministic", 0.60)
            sem_w = w.get("semantic", 0.40)
        except (yaml.YAMLError, OSError):
            pass

    raw_merge = round(det_w * det_score + sem_w * sem_mean, 2)

    # Get z-score stats
    ds = domain_stats.get(domain_name, {})
    team_adj = adjusted_scores.get(participant_name, {}).get(domain_name, {})

    final_domain_score = team_adj.get("adjusted_score", raw_merge)

    return {
        "repo_name": repo_name,
        "evaluation_date": _now(),
        "scores": {
            "deterministic": det_score,
            "semantic": sem_mean,
            "raw_merge": raw_merge,
            "final_domain_score": final_domain_score,
        },
        "global_stats": {
            "mean": round(ds.get("global_mean", 0), 2),
            "stdev": round(ds.get("global_stdev", 0), 2),
        },
        "team_stats": {
            "z_score": round(team_adj.get("z_score", 0), 4),
            "relative_bonus": round(team_adj.get("bonus_applied", 0), 3),
        },
    }


def fetch_leaderboard_data(conn, results, domain_stats, weights_cfg):
    """
    Data for global-leaderboard.md template.
    """
    teams = []
    for r in results:
        # Build domain scores dict
        scores = {}
        for d in DOMAIN_NAMES:
            scores[d] = r.get("domain_details", {}).get(d, {}).get("adjusted_score", 0)
        teams.append({
            "rank": r["rank"],
            "repo_name": r["team"],
            "final_score": r["final_score"],
            "scores": scores,
        })

    global_stats = {}
    for d in DOMAIN_NAMES:
        ds = domain_stats.get(d, {})
        global_stats[d] = {
            "mean": round(ds.get("global_mean", 0), 2),
            "stdev": round(ds.get("global_stdev", 0), 2),
        }

    return {
        "report_date": _now(),
        "total_teams": len(results),
        "teams": teams,
        "global_stats": global_stats,
    }


def fetch_team_summary_data(conn, participant_id, participant_name, results,
                              domain_stats, adjusted_scores, repo_name=""):
    """
    Data for team-final-summary.md template.
    """
    # Find this team's rank
    team_rank = 0
    final_score = 0
    for r in results:
        if r["team"] == participant_name:
            team_rank = r["rank"]
            final_score = r["final_score"]
            break

    # Domain scores
    scores = {}
    domain_scores_list = []
    for d in DOMAIN_NAMES:
        team_adj = adjusted_scores.get(participant_name, {}).get(d, {})
        score_val = team_adj.get("adjusted_score", 0)
        scores[d] = score_val
        domain_scores_list.append({"domain": d, "score": score_val})

    # Model aggregate scores
    from db import get_domain_scores
    all_rows = get_domain_scores(conn, participant_id)
    model_scores = {}
    for r in all_rows:
        if r["kind"] == "semantic" and r["model"]:
            model_scores.setdefault(r["model"], []).append(r["score"])

    model_aggregate = []
    for model, s_list in sorted(model_scores.items()):
        model_aggregate.append({
            "model_name": model,
            "mean_score": round(sum(s_list) / len(s_list), 2),
        })

    return {
        "repo_name": repo_name,
        "evaluation_date": _now(),
        "team_rank": team_rank,
        "total_teams": len(results),
        "final_score": final_score,
        "scores": scores,
        "domain_scores_list": domain_scores_list,
        "model_aggregate_scores": model_aggregate,
        "executive_summary": "(Agent-written narrative goes here — §8)",
    }


# ---------------------------------------------------------------------------
# Render all reports
# ---------------------------------------------------------------------------

def render_all(conn, standard, output_dir, results, domain_stats, adjusted_scores, weights_cfg):
    """Render all 32 markdown templates and write to output_dir."""
    from db import list_participants, get_domain_scores

    os.makedirs(output_dir, exist_ok=True)
    participants = list_participants(conn, standard)

    # 1. Global leaderboard
    lb_data = fetch_leaderboard_data(conn, results, domain_stats, weights_cfg)
    lb_template = _load_template("global-leaderboard.md")
    lb_md = chevron.render(lb_template, lb_data)
    with open(os.path.join(output_dir, "global-leaderboard.md"), "w", encoding="utf-8") as f:
        f.write(lb_md)
    print(f"  global-leaderboard.md")

    # 2. Per-participant reports
    for p in participants:
        pid = p["id"]
        pname = p["participant_name"]
        repo_path = p["repo_path"]

        # Team final summary
        ts_data = fetch_team_summary_data(
            conn, pid, pname, results, domain_stats, adjusted_scores, pname,
        )
        ts_template = _load_template("team-final-summary.md")
        ts_md = chevron.render(ts_template, ts_data)
        with open(os.path.join(output_dir, f"{pname}-summary.md"), "w", encoding="utf-8") as f:
            f.write(ts_md)
        print(f"  {pname}-summary.md")

        # Per-domain reports
        rows = get_domain_scores(conn, pid)
        participant_domains = set()
        for r in rows:
            participant_domains.add(r["domain"])

        for i, (dir_name, domain_name) in enumerate(zip(DOMAINS, DOMAIN_NAMES)):
            template_prefix = dir_name.split("-", 1)[1]  # e.g., "infrastructure"

            # Deterministic template
            det_data = fetch_deterministic_data(conn, pid, domain_name, pname)
            det_template = _load_template(f"domain/{dir_name}/deterministic.md")
            det_md = chevron.render(det_template, det_data)
            det_path = os.path.join(output_dir, f"{pname}-{template_prefix}-deterministic.md")
            with open(det_path, "w", encoding="utf-8") as f:
                f.write(det_md)

            # Semantic template
            sem_data = fetch_semantic_data(conn, pid, domain_name, pname)
            sem_template = _load_template(f"domain/{dir_name}/semantic.md")
            sem_md = chevron.render(sem_template, sem_data)
            sem_path = os.path.join(output_dir, f"{pname}-{template_prefix}-semantic.md")
            with open(sem_path, "w", encoding="utf-8") as f:
                f.write(sem_md)

            # Summary template
            sum_data = fetch_summary_data(
                conn, pid, domain_name, domain_stats, adjusted_scores, pname, pname,
            )
            sum_template = _load_template(f"domain/{dir_name}/summary.md")
            sum_md = chevron.render(sum_template, sum_data)
            sum_path = os.path.join(output_dir, f"{pname}-{template_prefix}-summary.md")
            with open(sum_path, "w", encoding="utf-8") as f:
                f.write(sum_md)

        print(f"  {pname}: 30 domain templates rendered")

    print(f"\nTotal: {1 + len(participants) * 31} markdown files written to {output_dir}")
