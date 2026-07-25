"""generate_audit_report.py — populates audit report templates from
score/audit/plagiarism results. Produces 4 markdown + 4 HTML reports
(deterministic, semantic, pipeline-progress, summary) using chevron rendering.
"""
import json
import os
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
    ("enrich",            "section-supplementary-content-{d}"),
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


def _get_domain_data(conn, paper_id, domains):
    """Gather per-domain data for deterministic and semantic reports."""
    rows = []
    det_pass_count = 0
    det_total_count = 0
    sem_scores = []
    sem_below = 0
    threshold = 70

    for domain_id, domain_key, display_name, sort_order in domains:
        # --- Semantic: section-full score (scope-ambiguity fix) ---
        sem = conn.execute(
            "SELECT overall_score FROM academic_semantic_runs "
            "WHERE paper_id=? AND domain_id=? AND scope='section-full' "
            "ORDER BY run_number DESC LIMIT 1",
            (paper_id, domain_id),
        ).fetchone()
        sem_score = round(sem["overall_score"], 1) if sem else None

        # --- Deterministic: per-check breakdown ---
        det = conn.execute(
            "SELECT verdict, findings FROM academic_deterministic_findings "
            "WHERE paper_id=? AND domain_id=? "
            "ORDER BY run_number DESC LIMIT 1",
            (paper_id, domain_id),
        ).fetchone()
        det_verdict = det["verdict"] if det else None
        findings = json.loads(det["findings"]) if det and det["findings"] else []
        passed = sum(1 for f in findings if f.get("passed", False))
        total = len(findings)
        det_pass_count += passed
        det_total_count += total

        if sem_score is not None:
            sem_scores.append(sem_score)
            if sem_score < threshold:
                sem_below += 1

        # --- Per-check status projection ---
        check_map = {f.get("check_id", ""): f.get("passed", False) for f in findings}
        wc_status = "PASS" if check_map.get("word_count_in_range") else (
            "FAIL" if "word_count_in_range" in check_map else "—")
        citation_status = "PASS" if check_map.get("citation_marker_present") else (
            "FAIL" if "citation_marker_present" in check_map else "—")
        budget_status = "PASS" if check_map.get("budget_fit_applied") else (
            "FAIL" if "budget_fit_applied" in check_map else "—")
        other_checks = {k: v for k, v in check_map.items()
                        if k not in ("word_count_in_range",
                                     "citation_marker_present",
                                     "budget_fit_applied")}
        if other_checks:
            other_passed = sum(1 for v in other_checks.values() if v)
            other_summary = f"{other_passed}/{len(other_checks)}"
        else:
            other_summary = "—"

        failed_items = [f.get("check_id", "?") for f in findings
                        if not f.get("passed", False)]

        # --- Citation counts from academic_section_citations ---
        cit_row = conn.execute(
            "SELECT COUNT(*) AS total, "
            "SUM(CASE WHEN source_kind='in-repo' THEN 1 ELSE 0 END) AS in_repo, "
            "SUM(CASE WHEN source_kind='literature' THEN 1 ELSE 0 END) AS literature "
            "FROM academic_section_citations "
            "WHERE paper_id=? AND domain_id=?",
            (paper_id, domain_id),
        ).fetchone()
        citation_total = cit_row["total"] if cit_row else 0
        citation_in_repo = cit_row["in_repo"] if cit_row else 0
        citation_literature = cit_row["literature"] if cit_row else 0

        history = academic_schema.get_score_history(conn, paper_id, domain_key)
        final_score = None
        score_band = None
        trend = "N/A"
        if history:
            latest = history[-1]
            final_score = round(latest["final_score"], 1)
            score_band = latest["score_band"]
            if latest.get("trend_delta") is not None:
                delta = latest["trend_delta"]
                trend = ("Improved" if delta > 0.1
                         else "Regressed" if delta < -0.1
                         else "Unchanged")

        rows.append({
            "domain_key": domain_key,
            "verdict": det_verdict or "N/A",
            "verdict_class": "pass" if det_verdict == "PASS" else "fail",
            "passed_count": str(passed),
            "total_count": str(total),
            "failed_details": ", ".join(failed_items) if failed_items else "—",
            "wc_status": wc_status,
            "wc_class": _status_class(wc_status),
            "citation_status": citation_status,
            "citation_class": _status_class(citation_status),
            "budget_status": budget_status,
            "budget_class": _status_class(budget_status),
            "other_summary": other_summary,
            "score": str(sem_score) if sem_score else "N/A",
            "band": score_band or "N/A",
            "band_class": (score_band or "").lower(),
            "strengths": "",
            "weaknesses": "",
            "sem_score": sem_score,
            "det_verdict": det_verdict,
            "plag_verdict": None,
            "final_score": final_score,
            "score_band": score_band,
            "trend": trend,
            "citation_total": citation_total,
            "citation_in_repo": citation_in_repo,
            "citation_literature": citation_literature,
        })

    return rows, det_pass_count, det_total_count, sem_scores, sem_below


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
        # Since we ORDER BY run_number DESC and iterate sequentially,
        # first occurrence per (domain_id, part_kind) is the latest.
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


def _get_humanize_data(conn, paper_id, domains):
    """Group academic_humanize_passes by (domain, pass_kind) for the
    deterministic report's Humanize Passes section."""
    rows = conn.execute(
        "SELECT d.domain_key, h.pass_kind, h.iteration, h.risk_flags "
        "FROM academic_humanize_passes h "
        "JOIN academic_domains d ON d.id = h.domain_id "
        "WHERE h.paper_id=? "
        "ORDER BY d.sort_order, h.pass_kind, h.iteration DESC",
        (paper_id,),
    ).fetchall()

    # Group by domain_key
    by_domain = {}
    for r in rows:
        dk = r["domain_key"]
        if dk not in by_domain:
            by_domain[dk] = {"deterministic": [], "semantic": []}
        pk = r["pass_kind"] or "deterministic"
        if pk in by_domain[dk]:
            by_domain[dk][pk].append(r)

    result = []
    for _, domain_key, _, _ in domains:
        data = by_domain.get(domain_key, {"deterministic": [], "semantic": []})
        det_passes = data["deterministic"]
        sem_passes = data["semantic"]
        # Domain is flagged if it has any humanize pass record
        flagged = bool(det_passes or sem_passes)
        det_pass = "Yes" if det_passes else ("—" if not flagged else "No")
        sem_pass = "Yes" if sem_passes else ("—" if not flagged else "No")
        # Collect unique risk flags from the latest pass of each kind
        risk_flags_set = set()
        for p in det_passes[:1]:
            for flag in (p.get("risk_flags") or "").split(","):
                flag = flag.strip()
                if flag:
                    risk_flags_set.add(flag)
        for p in sem_passes[:1]:
            for flag in (p.get("risk_flags") or "").split(","):
                flag = flag.strip()
                if flag:
                    risk_flags_set.add(flag)
        result.append({
            "domain_key": domain_key,
            "flagged": "Yes" if flagged else "No",
            "det_pass": det_pass,
            "det_pass_class": _status_class("PASS" if det_pass == "Yes" else "FAIL"),
            "sem_pass": sem_pass,
            "sem_pass_class": _status_class("PASS" if sem_pass == "Yes" else "FAIL"),
            "risk_flags": ", ".join(sorted(risk_flags_set)) if risk_flags_set else "—",
        })
    return result


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

        rows, det_pass, det_total, sem_scores, sem_below = \
            _get_domain_data(conn, paper_id, domains)
        plag_map = _get_plag_data(conn, paper_id, domains)
        part_scores = _get_part_scores(conn, paper_id, domains)
        humanize_data = _get_humanize_data(conn, paper_id, domains)
        doc_budget_status = _get_whole_paper_check(conn, paper_id)

        for row in rows:
            row["plag_verdict"] = plag_map.get(row["domain_key"], "N/A")

        sem_mean = (round(sum(sem_scores) / len(sem_scores), 1)
                    if sem_scores else "N/A")

        # --- Context shared by all templates ---
        base_ctx = {
            "title": title,
            "timestamp": ts,
            "paper_id": str(paper_id),
        }

        # --- Deterministic context ---
        det_ctx = {**base_ctx, "domains": rows}
        det_ctx["total_domains"] = str(len(rows))
        det_ctx["all_pass"] = "Yes" if all(
            r["verdict"] == "PASS" for r in rows) else "No"
        det_ctx["failed_count"] = str(sum(
            1 for r in rows if r["verdict"] != "PASS"))
        det_ctx["document_budget_status"] = doc_budget_status
        det_ctx["document_budget_class"] = _status_class(doc_budget_status)
        det_ctx["humanize"] = humanize_data

        # --- Semantic context ---
        sem_ctx = {**base_ctx}
        sem_ctx["domains_full"] = rows
        sem_ctx["domains_parts"] = part_scores
        sem_ctx["mean_score"] = str(sem_mean)
        sem_ctx["below_threshold_count"] = str(sem_below)
        sem_ctx["threshold"] = "70"

        # --- Pipeline-progress context ---
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

        # --- Summary context ---
        all_pass = all(r["verdict"] == "PASS" for r in rows)
        sem_all_pass = all(
            r["sem_score"] is None or r["sem_score"] >= 70 for r in rows)

        history = academic_schema.get_score_history(conn, paper_id)
        whole_score = None
        whole_band = None
        whole_trend = "N/A"
        if history:
            latest = history[-1]
            whole_score = round(latest["final_score"], 1)
            whole_band = latest["score_band"]
            if latest.get("trend_delta") is not None:
                d = latest["trend_delta"]
                whole_trend = ("Improved" if d > 0.1
                               else "Regressed" if d < -0.1
                               else "Unchanged")

        sum_ctx = {**base_ctx}
        sum_ctx["whole_paper_score"] = str(whole_score) if whole_score else "N/A"
        sum_ctx["whole_paper_band"] = whole_band or "N/A"
        sum_ctx["whole_paper_trend"] = whole_trend
        sum_ctx["det_passed"] = str(det_pass)
        sum_ctx["det_total"] = str(det_total)
        sum_ctx["det_failed_domains"] = ", ".join(
            r["domain_key"] for r in rows if r["verdict"] != "PASS") or "—"
        sum_ctx["sem_mean"] = str(sem_mean)
        sum_ctx["sem_below"] = str(sem_below)
        sum_ctx["plag_summary"] = ", ".join(
            f"{k}: {v}" for k, v in plag_map.items()) or "N/A"
        sum_ctx["humanize_count"] = str(sum(
            1 for h in humanize_data if h["flagged"] == "Yes"))

        # --- Output directory ---
        output_dir = os.path.join(str(repo_root), "docs", "paper",
                                  f"paper-{paper_id}", "audit")
        os.makedirs(output_dir, exist_ok=True)

        rendered = []

        # --- Render each template pair (markdown + HTML) ---
        for name, ctx in [("deterministic", det_ctx),
                          ("semantic", sem_ctx),
                          ("pipeline-progress", pipe_ctx),
                          ("summary", sum_ctx)]:
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

        conn.commit()
        write_envelope(out_path, status="ok",
                       message=f"audit reports generated: {len(rendered)} files",
                       files=rendered)
    finally:
        conn.close()


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


if __name__ == "__main__":
    main()
