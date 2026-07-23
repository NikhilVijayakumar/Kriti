"""
render_reports.py — Render all 32 markdown + 32 HTML templates using chevron.

Five markdown data-fetch functions, three HTML data-fetch extensions,
one rule-narrative builder, one HTML rendering pipeline.
"""
import sys
import chevron
import json
import os
from datetime import datetime, timezone
from render_charts import chart_to_base64

# evaluate_rules lives in usecase-2a-det-audit/ — add to path for lazy imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "usecase-2a-det-audit"))

SYSTEM_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
TEMPLATES_DIR = os.path.join(SYSTEM_DIR, "templates", "reports")
# No hardcoded domain list here — every function below takes `conn` and
# reads hackathon_domains via common/hackathon_schema.py's get_all_domains()/
# get_domain_rows() instead.


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _load_template(conn, report_type, domain_key=None):
    """Load a markdown template by (report_type, domain_key) — the file
    path itself comes from hackathon_templates, not a path built here."""
    from hackathon_schema import get_template
    path = get_template(conn, "markdown", report_type, domain_key)
    with open(path, "r", encoding="utf-8-sig") as f:
        return f.read()


def _load_partial(fmt, filename):
    """_styles.html/_narrative-block.html are chevron partials (shared
    includes), not per-report templates — not catalogued in
    hackathon_templates, which only tracks the 5 reportable types."""
    path = os.path.join(TEMPLATES_DIR, fmt, filename)
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
    from hackathon_schema import get_domain_scores
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
    if result["rules"]:
        findings.append("| Status | Rule ID | Detail |")
        findings.append("|--------|---------|--------|")
        for r in result["rules"]:
            status = "PASS" if r["passed"] else "FAIL"
            detail = str(r.get("detail", "")).replace("|", "\\|").replace("\n", "<br>")
            findings.append(f"| {status} | `{r['id']}` | {detail} |")

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
    from hackathon_schema import get_domain_scores
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
                        repo_name="", team_name=""):
    """
    Data for {domain}-summary.md templates.
    Combines det/sem scores with z-score stats.
    """
    from hackathon_schema import get_domain_scores, get_domain_id

    rows = get_domain_scores(conn, participant_id, domain_name)
    det_score = 0.0
    sem_scores = []
    for r in rows:
        if r["kind"] == "deterministic":
            det_score = r["score"]
        elif r["kind"] == "semantic":
            sem_scores.append(r["score"])

    sem_mean = round(sum(sem_scores) / len(sem_scores), 2) if sem_scores else 0

    # det_weight/sem_weight come straight from hackathon_domains, not
    # re-read from calculation/aggregation/domain/*.yaml here.
    domain_id = get_domain_id(conn, domain_name)
    row = conn.execute("SELECT det_weight, sem_weight FROM hackathon_domains WHERE id=?", (domain_id,)).fetchone()
    det_w, sem_w = (row["det_weight"], row["sem_weight"]) if row else (0.60, 0.40)

    raw_merge = round(det_w * det_score + sem_w * sem_mean, 2)

    # Get z-score stats
    ds = domain_stats.get(domain_name, {})
    team_adj = adjusted_scores.get(team_name, {}).get(domain_name, {})

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
            # Median/MAD, not mean/stdev -- the Z-score bonus below is a
            # robust (MAD-based) Z-score, so the displayed spread must match
            # the statistic it was actually computed from.
            "median": round(ds.get("global_median", 0), 2),
            "mad": round(ds.get("global_mad", 0), 2),
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
    from hackathon_schema import get_all_domains
    domains = get_all_domains(conn)

    teams = []
    for r in results:
        # Build domain scores dict. domain_details (from leaderboard.py) is
        # keyed by the hyphenated-numbered dir name ("08-team-workflow"), not
        # the underscored domain name ("team_workflow") -- map through domains.
        scores = {}
        for _domain_id, key, dir_name in domains:
            scores[key] = r.get("domain_details", {}).get(dir_name, {}).get("adjusted_score", 0)
        teams.append({
            "rank": r["rank"],
            "repo_name": r["team"],
            "final_score": r["final_score"],
            "scores": scores,
        })

    global_stats = {}
    for _domain_id, key, _dir_name in domains:
        ds = domain_stats.get(key, {})
        global_stats[key] = {
            "median": round(ds.get("global_median", 0), 2),
            "mad": round(ds.get("global_mad", 0), 2),
        }

    return {
        "report_date": _now(),
        "total_teams": len(results),
        "teams": teams,
        "global_stats": global_stats,
    }


def fetch_team_summary_data(conn, participant_id, team_name, results,
                              domain_stats, adjusted_scores, repo_name=""):
    """
    Data for team-final-summary.md template.
    """
    # Find this team's rank
    team_rank = 0
    final_score = 0
    for r in results:
        if r["team"] == team_name:
            team_rank = r["rank"]
            final_score = r["final_score"]
            break

    # Domain scores
    from hackathon_schema import get_domain_scores, get_all_domains
    scores = {}
    domain_scores_list = []
    for _domain_id, d, _dir_name in get_all_domains(conn):
        team_adj = adjusted_scores.get(team_name, {}).get(d, {})
        score_val = team_adj.get("adjusted_score", 0)
        scores[d] = score_val
        domain_scores_list.append({"domain": d, "score": score_val})

    # Model aggregate scores
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
    from hackathon_schema import list_participants, get_domain_scores, get_all_domains

    os.makedirs(output_dir, exist_ok=True)
    participants = list_participants(conn, standard)
    domains = get_all_domains(conn)

    # 1. Global leaderboard
    lb_data = fetch_leaderboard_data(conn, results, domain_stats, weights_cfg)
    lb_template = _load_template(conn, "leaderboard")
    lb_md = chevron.render(lb_template, lb_data)
    with open(os.path.join(output_dir, "global-leaderboard.md"), "w", encoding="utf-8") as f:
        f.write(lb_md)
    print(f"  global-leaderboard.md")

    # 2. Per-team reports
    for p in participants:
        pid = p["id"]
        tname = p["team_name"]
        repo_path = p["repo_path"]

        # Team final summary
        ts_data = fetch_team_summary_data(
            conn, pid, tname, results, domain_stats, adjusted_scores, tname,
        )
        ts_template = _load_template(conn, "team-final-summary")
        ts_md = chevron.render(ts_template, ts_data)
        with open(os.path.join(output_dir, f"{tname}-summary.md"), "w", encoding="utf-8") as f:
            f.write(ts_md)
        print(f"  {tname}-summary.md")

        # Per-domain reports
        rows = get_domain_scores(conn, pid)
        participant_domains = set()
        for r in rows:
            participant_domains.add(r["domain"])

        for i, (_domain_id, domain_name, dir_name) in enumerate(domains):
            template_prefix = dir_name.split("-", 1)[1]  # e.g., "infrastructure"

            # Deterministic template
            det_data = fetch_deterministic_data(conn, pid, domain_name, tname)
            det_template = _load_template(conn, "deterministic", domain_name)
            det_md = chevron.render(det_template, det_data)
            det_path = os.path.join(output_dir, f"{tname}-{template_prefix}-deterministic.md")
            with open(det_path, "w", encoding="utf-8") as f:
                f.write(det_md)

            # Semantic template
            sem_data = fetch_semantic_data(conn, pid, domain_name, tname)
            sem_template = _load_template(conn, "semantic", domain_name)
            sem_md = chevron.render(sem_template, sem_data)
            sem_path = os.path.join(output_dir, f"{tname}-{template_prefix}-semantic.md")
            with open(sem_path, "w", encoding="utf-8") as f:
                f.write(sem_md)

            # Summary template
            sum_data = fetch_summary_data(
                conn, pid, domain_name, domain_stats, adjusted_scores, tname, tname,
            )
            sum_template = _load_template(conn, "summary", domain_name)
            sum_md = chevron.render(sum_template, sum_data)
            sum_path = os.path.join(output_dir, f"{tname}-{template_prefix}-summary.md")
            with open(sum_path, "w", encoding="utf-8") as f:
                f.write(sum_md)

        print(f"  {tname}: 30 domain templates rendered")

    print(f"\nTotal: {1 + len(participants) * 31} markdown files written to {output_dir}")


# ---------------------------------------------------------------------------
# Chart spec builder + generation
# ---------------------------------------------------------------------------

def build_chart_spec(conn, results, domain_stats, adjusted_scores, weights_cfg):
    """
    Build the JSON spec dict that render_charts.generate_charts() consumes.
    Keys domain_charts by "{participant}_{domain}" so each team gets separate charts.
    """
    from hackathon_schema import list_participants, get_domain_rows

    spec = {"domain_charts": {}, "team_charts": {}, "rank_charts": {}}

    participants = list_participants(conn, "python_hackathon")

    # Per-domain, per-participant charts — det_weight/sem_weight come
    # straight from hackathon_domains (seeded once from
    # calculation/aggregation/domain/*.yaml at schema-init time), not
    # re-read from those files here.
    for d in get_domain_rows(conn):
        dir_name, domain_name, det_w, sem_w = d["dir_name"], d["key"], d["det_weight"], d["sem_weight"]

        # Global stats for this domain (median/MAD -- matches the robust
        # Z-score basis, not plain mean/stdev)
        ds = domain_stats.get(domain_name, {})
        global_median = ds.get("global_median", 0)
        global_mad = ds.get("global_mad", 0)

        # Rank distribution — once per domain (shared across all teams)
        # domain_details (from leaderboard.py) is keyed by the hyphenated-
        # numbered dir_name ("08-team-workflow"), not domain_name.
        teams_data = []
        for r in results:
            score = r.get("domain_details", {}).get(dir_name, {}).get("adjusted_score", 0)
            teams_data.append({"team": r["team"], "score": score})
        spec["rank_charts"][domain_name] = {"teams_data": teams_data}

        # Per-participant charts for this domain
        for p in participants:
            pid = p["id"]
            tname = p["team_name"]
            chart_key = f"{tname}_{domain_name}"

            dc = {
                "global_median": global_median,
                "global_mad": global_mad,
                "det_weight": det_w,
                "sem_weight": sem_w,
            }

            # Deterministic rules
            det_data = fetch_deterministic_data(conn, pid, domain_name, tname)
            dc["rules"] = det_data.get("deterministic_rules", [])

            # Semantic model results
            sem_data = fetch_semantic_data(conn, pid, domain_name, tname)
            dc["model_results"] = sem_data.get("model_results", [])
            dc["mean_score"] = sem_data.get("mean_score", 0)

            # Summary scores
            sum_data = fetch_summary_data(
                conn, pid, domain_name, domain_stats, adjusted_scores, tname, tname,
            )
            dc["team_score"] = sum_data["scores"].get("final_domain_score",
                                sum_data["scores"].get("raw_merge", 0))
            dc["det_score"] = sum_data["scores"].get("deterministic", 0)
            dc["sem_score"] = sum_data["scores"].get("semantic", 0)

            spec["domain_charts"][chart_key] = dc

    # Team radar charts
    for p in participants:
        tname = p["team_name"]
        ts_data = fetch_team_summary_data(
            conn, p["id"], tname, results, domain_stats, adjusted_scores, tname,
        )
        spec["team_charts"][tname] = {
            "domain_scores_list": ts_data.get("domain_scores_list", []),
        }

    # Global rank distribution
    global_teams_data = [{"team": r["team"], "score": r["final_score"]} for r in results]
    spec["rank_charts"]["global"] = {"teams_data": global_teams_data}

    return spec


# ---------------------------------------------------------------------------
# Rule-based narrative builder
# ---------------------------------------------------------------------------

def _build_rule_narrative(det_data):
    """Build narrative blocks from deterministic rule results.

    Returns list of {"heading": str, "text": str} for chevron rendering.
    Always available after deterministic scoring — no agent dependency.
    """
    rules = det_data.get("deterministic_rules", [])
    if not rules:
        return None

    passed = [r for r in rules if r.get("passed")]
    failed = [r for r in rules if not r.get("passed")]
    mandatory_failed = [r for r in failed if r.get("mandatory")]

    blocks = []

    # Pass rate
    total = len(rules)
    pass_count = len(passed)
    pass_pct = round(pass_count / total * 100) if total else 0
    blocks.append({
        "heading": "Pass Rate",
        "text": f"{pass_count}/{total} rules passed ({pass_pct}%).",
    })

    # Failed rules
    if failed:
        blocks.append({
            "heading": "Failed Rules",
            "is_list": True,
            "items": [
                {
                    "id": r.get("id", "?"),
                    "mandatory": bool(r.get("mandatory")),
                    "detail": r.get("detail", r.get("description", "")),
                }
                for r in failed
            ],
        })

    # Mandatory failures (subset, only if any)
    if mandatory_failed:
        blocks.append({
            "heading": "Mandatory Failures",
            "is_list": True,
            "items": [
                {"id": r.get("id", "?"), "detail": r.get("detail", "")}
                for r in mandatory_failed
            ],
        })

    return blocks if blocks else None


# ---------------------------------------------------------------------------
# Score badge helper
# ---------------------------------------------------------------------------

def _score_badge(score):
    """Map a 0-100 score to a Primer status badge dict."""
    if score >= 75:
        return {"label": "Strong", "css_class": "success"}
    if score >= 50:
        return {"label": "Attention", "css_class": "attention"}
    return {"label": "Needs Work", "css_class": "danger"}


# ---------------------------------------------------------------------------
# HTML data-fetch extensions
# ---------------------------------------------------------------------------

def _load_html_template(conn, report_type, domain_key=None):
    """Load an HTML template by (report_type, domain_key) — same DB lookup
    as _load_template(), format='html'."""
    from hackathon_schema import get_template
    path = get_template(conn, "html", report_type, domain_key)
    with open(path, "r", encoding="utf-8-sig") as f:
        return f.read()


def fetch_summary_html_data(conn, participant_id, domain_name, domain_stats,
                            adjusted_scores, repo_name, team_name,
                            chart_b64=None):
    """Extend fetch_summary_data() with agent narrative, rule narrative, chart, badge."""
    from hackathon_schema import get_narrative

    base = fetch_summary_data(conn, participant_id, domain_name,
                              domain_stats, adjusted_scores, repo_name, team_name)

    # Agent-written narrative
    agent_sections = get_narrative(conn, participant_id, domain_name)
    base["agent_narrative"] = {"sections": agent_sections} if agent_sections else None

    # Rule-based narrative
    det_data = fetch_deterministic_data(conn, participant_id, domain_name, repo_name)
    rule_sections = _build_rule_narrative(det_data)
    base["rule_narrative"] = {"sections": rule_sections} if rule_sections else None

    # Chart
    base["chart_base64"] = chart_b64 or ""

    # Badge
    base["domain_badge"] = _score_badge(base["scores"]["final_domain_score"])

    return base


def fetch_team_summary_html_data(conn, participant_id, team_name, results,
                                 domain_stats, adjusted_scores, repo_name,
                                 radar_b64=None):
    """Extend fetch_team_summary_data() with team profile, narrative, radar chart."""
    from hackathon_schema import get_narrative, get_team_profile

    base = fetch_team_summary_data(conn, participant_id, team_name,
                                   results, domain_stats, adjusted_scores, repo_name)

    # Team profile from DB
    base["team_profile"] = get_team_profile(conn, participant_id) or {}

    # Competition-wide narrative (NULL, NULL)
    sections = get_narrative(conn, None, None)
    base["narrative_blocks"] = sections or []

    # Radar chart
    base["radar_chart_base64"] = radar_b64 or ""

    # Final score badge
    base["final_badge"] = _score_badge(base["final_score"])

    # Domain badges
    base["domain_badges"] = {}
    for d, score in base.get("scores", {}).items():
        base["domain_badges"][d] = _score_badge(score)

    return base


def fetch_leaderboard_html_data(conn, results, domain_stats, weights_cfg,
                                rank_chart_b64=None):
    """Extend fetch_leaderboard_data() with competition-wide narrative, rank chart."""
    from hackathon_schema import get_narrative

    base = fetch_leaderboard_data(conn, results, domain_stats, weights_cfg)

    # Competition-wide narrative (NULL, NULL)
    sections = get_narrative(conn, None, None)
    base["narrative_blocks"] = sections or []

    # Rank chart
    base["rank_chart_base64"] = rank_chart_b64 or ""

    return base


# ---------------------------------------------------------------------------
# HTML rendering pipeline
# ---------------------------------------------------------------------------

def render_html_all(conn, standard, output_dir, results, domain_stats,
                    adjusted_scores, weights_cfg, charts_dir):
    """Render all 32 HTML templates with embedded charts + narratives."""
    from hackathon_schema import list_participants, get_domain_scores, get_all_domains

    html_out = os.path.join(output_dir, "html")
    os.makedirs(html_out, exist_ok=True)

    # Load shared CSS + narrative-block partials — not per-report templates,
    # see _load_partial()'s docstring.
    styles_html = _load_partial("html", "_styles.html")
    narrative_block_html = _load_partial("html", "_narrative-block.html")
    partials = {"styles": styles_html, "narrative-block": narrative_block_html}

    # Build chart base64 lookup from charts_dir
    # render_charts.py uses safe_key = "{pname}-{domain}" (dashes, not underscores)
    chart_b64_cache = {}

    def _get_chart_b64(filename_stem):
        """Get data-URI base64 for a chart by its filename stem (without .png)."""
        if filename_stem in chart_b64_cache:
            return chart_b64_cache[filename_stem]
        path = os.path.join(charts_dir, f"{filename_stem}.png")
        if os.path.isfile(path):
            b64 = chart_to_base64(path)
            chart_b64_cache[filename_stem] = b64
            return b64
        chart_b64_cache[filename_stem] = ""
        return ""

    participants = list_participants(conn, standard)
    domains = get_all_domains(conn)

    # 1. Global leaderboard
    lb_data = fetch_leaderboard_html_data(
        conn, results, domain_stats, weights_cfg,
        rank_chart_b64=_get_chart_b64("global-rank-distribution"),
    )
    lb_template = _load_html_template(conn, "leaderboard")
    lb_html = chevron.render(lb_template, lb_data, partials_dict=partials)
    with open(os.path.join(html_out, "global-leaderboard.html"), "w", encoding="utf-8") as f:
        f.write(lb_html)
    print("  html/global-leaderboard.html")

    # 2. Per-team reports
    for p in participants:
        pid = p["id"]
        tname = p["team_name"]

        # Team final summary
        ts_data = fetch_team_summary_html_data(
            conn, pid, tname, results, domain_stats, adjusted_scores, tname,
            radar_b64=_get_chart_b64(f"{tname}-radar"),
        )
        ts_template = _load_html_template(conn, "team-final-summary")
        ts_html = chevron.render(ts_template, ts_data, partials_dict=partials)
        with open(os.path.join(html_out, f"{tname}-summary.html"), "w", encoding="utf-8") as f:
            f.write(ts_html)
        print(f"  html/{tname}-summary.html")

        # Per-domain reports
        for _domain_id, domain_name, dir_name in domains:
            template_prefix = dir_name.split("-", 1)[1]
            safe_key = f"{tname}-{domain_name.replace('_', '-')}"

            # Deterministic
            det_data = fetch_deterministic_data(conn, pid, domain_name, tname)
            det_data["chart_base64"] = _get_chart_b64(f"{safe_key}-rule-pass-rate")
            det_template = _load_html_template(conn, "deterministic", domain_name)
            det_html = chevron.render(det_template, det_data, partials_dict=partials)
            det_path = os.path.join(html_out, f"{tname}-{template_prefix}-deterministic.html")
            with open(det_path, "w", encoding="utf-8") as f:
                f.write(det_html)

            # Semantic
            sem_data = fetch_semantic_data(conn, pid, domain_name, tname)
            sem_template = _load_html_template(conn, "semantic", domain_name)
            sem_html = chevron.render(sem_template, sem_data, partials_dict=partials)
            sem_path = os.path.join(html_out, f"{tname}-{template_prefix}-semantic.html")
            with open(sem_path, "w", encoding="utf-8") as f:
                f.write(sem_html)

            # Summary
            sum_data = fetch_summary_html_data(
                conn, pid, domain_name, domain_stats, adjusted_scores, tname, tname,
                chart_b64=_get_chart_b64(f"{safe_key}-field-distribution"),
            )
            sum_template = _load_html_template(conn, "summary", domain_name)
            sum_html = chevron.render(sum_template, sum_data, partials_dict=partials)
            sum_path = os.path.join(html_out, f"{tname}-{template_prefix}-summary.html")
            with open(sum_path, "w", encoding="utf-8") as f:
                f.write(sum_html)

        print(f"  html/{tname}: 30 domain templates + summary rendered")

    total = 1 + len(participants) * 31
    print(f"\nTotal: {total} HTML files written to {html_out}")
