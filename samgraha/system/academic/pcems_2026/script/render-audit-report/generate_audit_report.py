"""generate_audit_report.py — populates per-domain and shared audit report
templates from score/audit/plagiarism results. Produces 12×6 per-domain reports
plus shared pipeline-progress and whole-paper-summary using chevron rendering.
"""
import json
import os
import statistics
import sys
from datetime import datetime, timezone
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402

import chevron  # noqa: E402

TEMPLATES_MD = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "..", "templates", "report", "markdown")
TEMPLATES_HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "..", "..", "templates", "report", "html")

# Per-domain pipeline stages for the progress matrix.
# Order matters — matches the column order in pipeline-progress.md.
_PIPELINE_STAGES = [
    ("generate",          "generate-section-draft-{d}"),
    ("cite",              "section-citations-{d}"),
    ("enrich",            "section-enrichment-{d}"),
    ("budget",            "section-budget-fit-{d}"),
    ("det_audit",         "deterministic-audit-{d}"),
    ("sem_audit",         "semantic-audit-{d}"),
    ("plagiarism",        "plagiarism-forensic-audit-{d}"),
    ("humanize_det",      "humanize-deterministic-{d}"),
    ("humanize_sem",      "humanize-semantic-{d}"),
]

# Whole-pipeline usecases for the progress matrix.
_WHOLE_PIPELINE_STAGES = [
    ("collation_status",          "section-citations-references"),
    ("budget_total_status",       "section-budget-fit-total"),
    ("polish_status",             "document-narrative-polish"),
    ("cross_section_status",      "cross-section-semantic-audit"),
    ("document_status",           "document-semantic-audit"),
]


def _load_template(subdir, name):
    path = os.path.join(subdir, name)
    if os.path.isfile(path):
        with open(path, "r") as f:
            return f.read()
    return None


def _score_class(score_str):
    """Return CSS class for a score value (pass/medium/low/na)."""
    if score_str in ("N/A", "—", ""):
        return "na"
    try:
        v = float(score_str)
    except (ValueError, TypeError):
        return "na"
    if v >= 80:
        return "pass"
    if v >= 60:
        return "medium"
    return "low"


def _status_class(status_str):
    """Return CSS class for a pass/fail/pending status string."""
    if status_str == "PASS" or status_str == "✓":
        return "pass"
    if status_str == "FAIL" or status_str == "✗":
        return "fail"
    return "pending"


# ---------------------------------------------------------------------------
# Single-domain context builders
# ---------------------------------------------------------------------------

def _get_single_deterministic_data(conn, paper_id, domain_id, domain_key):
    """Return deterministic audit context for one domain."""
    det = conn.execute(
        "SELECT verdict, findings FROM academic_deterministic_findings "
        "WHERE paper_id=? AND domain_id=? "
        "ORDER BY run_number DESC LIMIT 1",
        (paper_id, domain_id),
    ).fetchone()
    verdict = det["verdict"] if det else "N/A"
    findings = json.loads(det["findings"]) if det and det["findings"] else []
    checks = []
    for f in findings:
        checks.append({
            "check_id": f.get("check_id", ""),
            "status": "PASS" if f.get("passed") else "FAIL",
            "status_class": "pass" if f.get("passed") else "fail",
            "detail": f.get("detail", ""),
        })
    return {"verdict": verdict, "checks": checks}


def _get_single_semantic_full_data(conn, paper_id, domain_id):
    """Return semantic full-score context for one domain, with model breakdown."""
    rows = conn.execute(
        "SELECT model, overall_score, reasoning FROM academic_semantic_runs "
        "WHERE paper_id=? AND domain_id=? AND scope='section-full' "
        "ORDER BY run_number DESC",
        (paper_id, domain_id),
    ).fetchall()
    # Deduplicate by model (keep latest run per model)
    seen_models = set()
    models = []
    scores = []
    for r in rows:
        m = r["model"]
        if m not in seen_models:
            seen_models.add(m)
            models.append({"model": m, "score": round(r["overall_score"], 1), "agreement": ""})
            scores.append(r["overall_score"])
    # Also get dimension scores from the latest run
    latest_run = conn.execute(
        "SELECT id FROM academic_semantic_runs "
        "WHERE paper_id=? AND domain_id=? AND scope='section-full' "
        "ORDER BY run_number DESC LIMIT 1",
        (paper_id, domain_id),
    ).fetchone()
    dimensions = []
    if latest_run:
        dim_rows = conn.execute(
            "SELECT dimension_key, score, evidence FROM academic_semantic_dimension_scores "
            "WHERE run_id=?",
            (latest_run["id"],),
        ).fetchall()
        for d in dim_rows:
            dimensions.append({
                "dimension_key": d["dimension_key"],
                "score": round(d["score"], 1) if d["score"] is not None else "N/A",
                "evidence": d["evidence"] or "",
            })
    # Strengths/weaknesses/recommendations
    strengths, weaknesses, recommendations = [], [], []
    if latest_run:
        for ft, lst in [("strength", strengths), ("weakness", weaknesses), ("recommendation", recommendations)]:
            fr = conn.execute(
                "SELECT text FROM academic_semantic_findings "
                "WHERE run_id=? AND finding_type=?",
                (latest_run["id"], ft),
            ).fetchall()
            for r in fr:
                lst.append(r["text"])
    # Ensemble stats
    mean_score = round(statistics.mean(scores), 1) if scores else "N/A"
    stdev_score = round(statistics.stdev(scores), 1) if len(scores) > 1 else "N/A"
    if stdev_score == "N/A":
        agreement_level = "N/A"
    elif stdev_score <= 5:
        agreement_level = "High"
    elif stdev_score <= 15:
        agreement_level = "Medium"
    else:
        agreement_level = "Low"
    return {
        "models": models,
        "dimensions": dimensions,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "mean_score": mean_score,
        "stdev_score": stdev_score,
        "agreement_level": agreement_level,
    }


def _get_single_semantic_part_data(conn, paper_id, domain_id):
    """Return semantic part-score context for one domain."""
    rows = conn.execute(
        "SELECT part_kind, overall_score FROM academic_semantic_runs "
        "WHERE paper_id=? AND domain_id=? AND scope='section-part' "
        "AND part_kind IS NOT NULL "
        "ORDER BY run_number DESC",
        (paper_id, domain_id),
    ).fetchall()
    seen = set()
    parts = []
    for r in rows:
        pk = r["part_kind"]
        if pk not in seen:
            seen.add(pk)
            score = round(r["overall_score"], 1)
            parts.append({
                "part_kind": pk,
                "score": score,
                "verdict": "PASS" if score >= 70 else "FAIL",
                "findings": [],
            })
    return {"parts": parts}


def _get_single_plagiarism_data(conn, paper_id, domain_id):
    """Return plagiarism audit context for one domain."""
    row = conn.execute(
        "SELECT verdict, findings FROM academic_plagiarism_findings "
        "WHERE paper_id=? AND domain_id=? AND pass_type='forensic' "
        "ORDER BY id DESC LIMIT 1",
        (paper_id, domain_id),
    ).fetchone()
    if not row:
        return {"verdict": "N/A", "findings": []}
    findings_list = json.loads(row["findings"]) if row["findings"] else []
    findings = [{"check_id": f.get("check_id", ""), "detail": f.get("detail", ""), "severity": f.get("severity", "")} for f in findings_list]
    return {"verdict": row["verdict"], "findings": findings}


def _get_single_humanize_data(conn, paper_id, domain_id):
    """Return humanize pass context for one domain."""
    rows = conn.execute(
        "SELECT pass_kind, iteration, risk_flags FROM academic_humanize_passes "
        "WHERE paper_id=? AND domain_id=? "
        "ORDER BY pass_kind, iteration DESC",
        (paper_id, domain_id),
    ).fetchall()
    det_iter, det_flags = "", ""
    sem_iter, sem_flags = "", ""
    all_flags = set()
    for r in rows:
        pk = r["pass_kind"]
        flags = r["risk_flags"] or ""
        if pk == "deterministic" and not det_iter:
            det_iter = str(r["iteration"])
            det_flags = flags
        elif pk == "semantic" and not sem_iter:
            sem_iter = str(r["iteration"])
            sem_flags = flags
        for f in flags.split(","):
            f = f.strip()
            if f:
                all_flags.add(f)
    return {
        "det_iteration": det_iter,
        "det_risk_flags": det_flags or "None",
        "sem_iteration": sem_iter,
        "sem_risk_flags": sem_flags or "None",
        "risk_flag_list": sorted(all_flags),
    }


def _get_single_domain_summary_data(conn, paper_id, domain_id, domain_key):
    """Return domain aggregate summary context for one domain."""
    # Get deterministic score (PASS=100, FAIL=0 for simplicity, or count passed/total)
    det = conn.execute(
        "SELECT verdict, findings FROM academic_deterministic_findings "
        "WHERE paper_id=? AND domain_id=? "
        "ORDER BY run_number DESC LIMIT 1",
        (paper_id, domain_id),
    ).fetchone()
    det_score = None
    if det:
        findings = json.loads(det["findings"]) if det["findings"] else []
        if findings:
            passed = sum(1 for f in findings if f.get("passed"))
            det_score = round(passed / len(findings) * 100, 1)

    # Get semantic blended score (from section-full, latest)
    sem = conn.execute(
        "SELECT overall_score FROM academic_semantic_runs "
        "WHERE paper_id=? AND domain_id=? AND scope='section-full' "
        "ORDER BY run_number DESC LIMIT 1",
        (paper_id, domain_id),
    ).fetchone()
    sem_score = round(sem["overall_score"], 1) if sem else None

    # Final score = 50/50 blend
    final_score = None
    if det_score is not None and sem_score is not None:
        final_score = round(0.5 * det_score + 0.5 * sem_score, 1)
    elif det_score is not None:
        final_score = det_score
    elif sem_score is not None:
        final_score = sem_score

    # Score band from score_bands.yaml (inline lookup)
    score_band = "N/A"
    if final_score is not None:
        if final_score >= 95: score_band = "Excellent"
        elif final_score >= 90: score_band = "Very Good"
        elif final_score >= 80: score_band = "Good"
        elif final_score >= 70: score_band = "Acceptable"
        else: score_band = "Needs Improvement"

    # Trend
    history = academic_schema.get_score_history(conn, paper_id, domain_key)
    trend = "N/A"
    if history:
        latest = history[-1]
        if latest.get("trend_delta") is not None:
            d = latest["trend_delta"]
            trend = "Improved" if d > 0.1 else "Regressed" if d < -0.1 else "Unchanged"

    return {
        "final_score": str(final_score) if final_score is not None else "N/A",
        "score_band": score_band,
        "deterministic_score": str(det_score) if det_score is not None else "N/A",
        "semantic_score": str(sem_score) if sem_score is not None else "N/A",
        "trend": trend,
    }


# ---------------------------------------------------------------------------
# Legacy helpers kept for backward-compat (pipeline-progress, whole-paper)
# ---------------------------------------------------------------------------

def _get_part_scores(conn, paper_id, domains):
    """Pivot section-part semantic scores into per-domain rows:
    {domain_key, citations_score, enrichment_score, budget_fit_score}."""
    rows = conn.execute(
        "SELECT domain_id, part_kind, overall_score "
        "FROM academic_semantic_runs "
        "WHERE paper_id=? AND scope='section-part' "
        "AND part_kind IS NOT NULL",
        (paper_id,),
    ).fetchall()

    # Build a map: domain_id -> {part_kind -> score}
    latest = {}
    for r in rows:
        did = r["domain_id"]
        pk = r["part_kind"]
        if did not in latest:
            latest[did] = {}
        if pk not in latest[did]:
            latest[did][pk] = round(r["overall_score"], 1)

    result = []
    for domain_id, domain_key, display_name, sort_order in domains:
        scores = latest.get(domain_id, {})
        cs = str(scores.get("citations", "—"))
        es = str(scores.get("enrichment", "—"))
        bs = str(scores.get("budget-fit", "—"))
        result.append({
            "domain_key": domain_key,
            "citations_score": cs,
            "citations_class": _score_class(cs),
            "enrichment_score": es,
            "enrichment_class": _score_class(es),
            "budget_fit_score": bs,
            "budget_fit_class": _score_class(bs),
        })
    return result


def _get_plag_data(conn, paper_id, domains):
    """Get plagiarism verdicts per domain."""
    results = conn.execute(
        "SELECT d.domain_key, p.verdict FROM academic_plagiarism_findings p "
        "JOIN academic_domains d ON d.id = p.domain_id "
        "WHERE p.paper_id=? AND p.pass_type='forensic' "
        "AND p.id IN (SELECT MAX(id) FROM academic_plagiarism_findings "
        "WHERE paper_id=? AND pass_type='forensic' GROUP BY domain_id)",
        (paper_id, paper_id),
    ).fetchall()
    return {r["domain_key"]: r["verdict"] for r in results}


def _get_whole_paper_check(conn, paper_id):
    """Check for a document-scope deterministic finding (whole-paper budget)."""
    row = conn.execute(
        "SELECT verdict, findings FROM academic_deterministic_findings "
        "WHERE paper_id=? AND scope='document' "
        "ORDER BY run_number DESC LIMIT 1",
        (paper_id,),
    ).fetchone()
    if not row:
        return "—"
    findings = json.loads(row["findings"]) if row["findings"] else []
    for f in findings:
        if f.get("check_id") == "total_word_count_in_range":
            return "PASS" if f.get("passed") else "FAIL"
    return "—"


def _get_pipeline_progress_data(conn, paper_id, domains):
    """Build the 12×9 domain×stage pipeline-progress matrix plus
    whole-pipeline statuses."""
    domain_rows = []
    for domain_id, domain_key, display_name, sort_order in domains:
        row = {"domain_key": domain_key}
        for col_key, usecase_tpl in _PIPELINE_STAGES:
            usecase_name = usecase_tpl.replace("{d}", domain_key)
            complete, _ = academic_schema.usecase_status(
                conn, paper_id, usecase_name)
            status = "✓" if complete else "✗"
            row[col_key] = status
            row[f"{col_key}_class"] = _status_class(status)
        domain_rows.append(row)

    whole = {}
    for ctx_key, usecase_name in _WHOLE_PIPELINE_STAGES:
        complete, _ = academic_schema.usecase_status(
            conn, paper_id, usecase_name)
        status = "✓" if complete else "✗"
        whole[ctx_key] = status
        whole[f"{ctx_key}_class"] = _status_class(status)

    # Summary stats
    complete_count = 0
    for drow in domain_rows:
        if all(drow[k] == "✓" for k, _ in _PIPELINE_STAGES):
            complete_count += 1

    return domain_rows, whole, complete_count


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload.get("paper_id")

    if not paper_id:
        write_envelope(out_path, status="error", message="missing paper_id")
        return

    conn = academic_schema.get_conn(db_path)
    try:
        paper = academic_schema.get_paper(conn, paper_id)
        if not paper:
            write_envelope(out_path, status="error",
                           message=f"paper {paper_id} not found")
            return

        domains = academic_schema.get_all_domains(conn)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        title = paper["title"] or f"Paper {paper_id}"

        # --- Context shared by all templates ---
        base_ctx = {
            "title": title,
            "timestamp": ts,
            "paper_id": str(paper_id),
        }

        # --- Output directory ---
        output_dir = os.path.join(str(repo_root), "docs", "paper",
                                  f"paper-{paper_id}", "audit")
        os.makedirs(output_dir, exist_ok=True)

        rendered = []

        # --- Per-domain render loop ---
        for domain_id, domain_key, display_name, sort_order in domains:
            domain_out = os.path.join(output_dir, "domain", domain_key)
            os.makedirs(domain_out, exist_ok=True)

            ctx_builders = {
                "deterministic": lambda _did=domain_id, _dk=domain_key: _get_single_deterministic_data(conn, paper_id, _did, _dk),
                "semantic-full": lambda _did=domain_id: _get_single_semantic_full_data(conn, paper_id, _did),
                "semantic-part": lambda _did=domain_id: _get_single_semantic_part_data(conn, paper_id, _did),
                "plagiarism": lambda _did=domain_id: _get_single_plagiarism_data(conn, paper_id, _did),
                "humanize": lambda _did=domain_id: _get_single_humanize_data(conn, paper_id, _did),
                "summary": lambda _did=domain_id, _dk=domain_key: _get_single_domain_summary_data(conn, paper_id, _did, _dk),
            }

            for kind, ctx_builder in ctx_builders.items():
                ctx = {**base_ctx, **ctx_builder()}
                # Markdown
                md_tpl = _load_template(TEMPLATES_MD, f"domain/{domain_key}/{kind}.md")
                if md_tpl:
                    md_out = chevron.render(md_tpl, ctx)
                    md_path = os.path.join(domain_out, f"{kind}.md")
                    with open(md_path, "w") as f:
                        f.write(md_out)
                    academic_schema.record_report(conn, paper_id, "markdown", md_path, report_kind=f"audit-{domain_key}-{kind}")
                    rendered.append(md_path)
                # HTML
                html_tpl = _load_template(TEMPLATES_HTML, f"domain/{domain_key}/{kind}.html")
                if html_tpl:
                    html_out = chevron.render(html_tpl, ctx)
                    html_path = os.path.join(domain_out, f"{kind}.html")
                    with open(html_path, "w") as f:
                        f.write(html_out)
                    academic_schema.record_report(conn, paper_id, "html", html_path, report_kind=f"audit-{domain_key}-{kind}")
                    rendered.append(html_path)

        # --- Shared reports (pipeline-progress, whole-paper-summary) ---
        # Pipeline-progress
        pipeline_domains, pipeline_whole, complete_count = \
            _get_pipeline_progress_data(conn, paper_id, domains)
        pipe_ctx = {**base_ctx}
        pipe_ctx["domains"] = pipeline_domains
        pipe_ctx.update(pipeline_whole)
        pipe_ctx["total_domains"] = str(len(domains))
        pipe_ctx["complete_count"] = str(complete_count)
        pending_list = []
        for drow in pipeline_domains:
            for col_key, _ in _PIPELINE_STAGES:
                if drow[col_key] == "✗":
                    pending_list.append(f"{drow['domain_key']}:{col_key}")
        pipe_ctx["pending_summary"] = (", ".join(pending_list[:10])
                                       if pending_list else "none")

        for name, ctx in [("pipeline-progress", pipe_ctx)]:
            # Markdown
            md_tpl = _load_template(TEMPLATES_MD, f"{name}.md")
            if md_tpl:
                md_out = chevron.render(md_tpl, ctx)
                md_path = os.path.join(output_dir, f"{name}.md")
                with open(md_path, "w") as f:
                    f.write(md_out)
                academic_schema.record_report(
                    conn, paper_id, "markdown", md_path,
                    report_kind=f"audit-{name}")
                rendered.append(md_path)
            # HTML
            html_tpl = _load_template(TEMPLATES_HTML, f"{name}.html")
            if html_tpl:
                html_out = chevron.render(html_tpl, ctx)
                html_path = os.path.join(output_dir, f"{name}.html")
                with open(html_path, "w") as f:
                    f.write(html_out)
                academic_schema.record_report(
                    conn, paper_id, "html", html_path,
                    report_kind=f"audit-{name}")
                rendered.append(html_path)

        # Whole-paper-summary (with domain_aggregates)
        plag_map = _get_plag_data(conn, paper_id, domains)
        part_scores = _get_part_scores(conn, paper_id, domains)
        humanize_data_legacy = []
        for _, domain_key, _, _ in domains:
            sd = _get_single_domain_summary_data(
                conn, paper_id,
                next(d[0] for d in domains if d[1] == domain_key),
                domain_key,
            )
            humanize_data_legacy.append({"domain_key": domain_key, **sd})

        whole_history = academic_schema.get_score_history(conn, paper_id)
        whole_score = None
        whole_band = None
        whole_trend = "N/A"
        if whole_history:
            latest = whole_history[-1]
            whole_score = round(latest["final_score"], 1)
            whole_band = latest["score_band"]
            if latest.get("trend_delta") is not None:
                d = latest["trend_delta"]
                whole_trend = ("Improved" if d > 0.1
                               else "Regressed" if d < -0.1
                               else "Unchanged")

        det_pass_count = 0
        det_total_count = 0
        sem_scores = []
        sem_below = 0
        for domain_id, domain_key, _, _ in domains:
            det = conn.execute(
                "SELECT verdict, findings FROM academic_deterministic_findings "
                "WHERE paper_id=? AND domain_id=? "
                "ORDER BY run_number DESC LIMIT 1",
                (paper_id, domain_id),
            ).fetchone()
            if det:
                findings = json.loads(det["findings"]) if det["findings"] else []
                passed = sum(1 for f in findings if f.get("passed", False))
                det_pass_count += passed
                det_total_count += len(findings)
            sem = conn.execute(
                "SELECT overall_score FROM academic_semantic_runs "
                "WHERE paper_id=? AND domain_id=? AND scope='section-full' "
                "ORDER BY run_number DESC LIMIT 1",
                (paper_id, domain_id),
            ).fetchone()
            if sem:
                sem_scores.append(sem["overall_score"])
                if sem["overall_score"] < 70:
                    sem_below += 1

        sem_mean = (round(sum(sem_scores) / len(sem_scores), 1)
                    if sem_scores else "N/A")

        sum_ctx = {**base_ctx}
        sum_ctx["whole_paper_score"] = str(whole_score) if whole_score else "N/A"
        sum_ctx["whole_paper_band"] = whole_band or "N/A"
        sum_ctx["whole_paper_trend"] = whole_trend
        sum_ctx["det_passed"] = str(det_pass_count)
        sum_ctx["det_total"] = str(det_total_count)
        failed_domain_keys = []
        for domain_id, domain_key, _, _ in domains:
            det = conn.execute(
                "SELECT verdict FROM academic_deterministic_findings "
                "WHERE paper_id=? AND domain_id=? "
                "ORDER BY run_number DESC LIMIT 1",
                (paper_id, domain_id),
            ).fetchone()
            if det and det["verdict"] != "PASS":
                failed_domain_keys.append(domain_key)
        sum_ctx["det_failed_domains"] = ", ".join(failed_domain_keys) or "—"
        sum_ctx["sem_mean"] = str(sem_mean)
        sum_ctx["sem_below"] = str(sem_below)
        sum_ctx["plag_summary"] = ", ".join(
            f"{k}: {v}" for k, v in plag_map.items()) or "N/A"
        sum_ctx["humanize_count"] = str(sum(
            1 for h in humanize_data_legacy if h.get("final_score") is not None))

        # domain_aggregates for the whole-paper-summary template
        domain_aggregates = []
        for domain_id, domain_key, display_name, sort_order in domains:
            sd = _get_single_domain_summary_data(conn, paper_id, domain_id, domain_key)
            domain_aggregates.append({
                "domain_key": domain_key,
                "final_score": sd["final_score"],
                "score_band": sd["score_band"],
            })
        sum_ctx["domain_aggregates"] = domain_aggregates

        # Render whole-paper-summary
        md_tpl = _load_template(TEMPLATES_MD, "whole-paper-summary.md")
        if md_tpl:
            md_out = chevron.render(md_tpl, sum_ctx)
            md_path = os.path.join(output_dir, "whole-paper-summary.md")
            with open(md_path, "w") as f:
                f.write(md_out)
            academic_schema.record_report(
                conn, paper_id, "markdown", md_path,
                report_kind="audit-whole-paper-summary")
            rendered.append(md_path)

        html_tpl = _load_template(TEMPLATES_HTML, "whole-paper-summary.html")
        if html_tpl:
            html_out = chevron.render(html_tpl, sum_ctx)
            html_path = os.path.join(output_dir, "whole-paper-summary.html")
            with open(html_path, "w") as f:
                f.write(html_out)
            academic_schema.record_report(
                conn, paper_id, "html", html_path,
                report_kind="audit-whole-paper-summary")
            rendered.append(html_path)

        conn.commit()
        write_envelope(out_path, status="ok",
                       message=f"audit reports generated: {len(rendered)} files",
                       files=rendered)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
