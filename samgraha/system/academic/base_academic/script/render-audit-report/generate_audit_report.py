"""generate_audit_report.py — populates audit report templates from
score/audit/plagiarism results. Produces 3 markdown + 3 HTML reports
(deterministic, semantic, summary) using chevron rendering.
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


def _load_template(subdir, name):
    path = os.path.join(subdir, name)
    if os.path.isfile(path):
        with open(path, "r") as f:
            return f.read()
    return None


def _get_domain_data(conn, paper_id, domains):
    """Gather per-domain data for all three reports."""
    rows = []
    det_pass_count = 0
    det_total_count = 0
    sem_scores = []
    sem_below = 0
    threshold = 70

    for domain_id, domain_key, display_name, sort_order in domains:
        sem = conn.execute(
            "SELECT overall_score FROM academic_semantic_runs "
            "WHERE paper_id=? AND domain_id=? "
            "ORDER BY run_number DESC LIMIT 1",
            (paper_id, domain_id),
        ).fetchone()
        sem_score = round(sem["overall_score"], 1) if sem else None

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

        failed_items = [f.get("check_id", "?") for f in findings
                        if not f.get("passed", False)]

        rows.append({
            "domain_key": domain_key,
            "verdict": det_verdict or "N/A",
            "verdict_class": "pass" if det_verdict == "PASS" else "fail",
            "passed_count": str(passed),
            "total_count": str(total),
            "failed_details": ", ".join(failed_items) if failed_items else "—",
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
        })

    return rows, det_pass_count, det_total_count, sem_scores, sem_below


def _get_plag_data(conn, paper_id, domains):
    """Get plagiarism verdicts per domain."""
    plag_verdicts = []
    for _, domain_key, _, _ in domains:
        domain_id = conn.execute(
            "SELECT id FROM academic_domains WHERE domain_key=?",
            (domain_id := None),  # placeholder, resolved below
        ).fetchone()

    # Simpler: query directly
    results = conn.execute(
        "SELECT d.domain_key, p.verdict FROM academic_plagiarism_findings p "
        "JOIN academic_domains d ON d.id = p.domain_id "
        "WHERE p.paper_id=? AND p.pass_type='forensic' "
        "AND p.id IN (SELECT MAX(id) FROM academic_plagiarism_findings "
        "WHERE paper_id=? AND pass_type='forensic' GROUP BY domain_id)",
        (paper_id, paper_id),
    ).fetchall()
    return {r["domain_key"]: r["verdict"] for r in results}


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

        # --- Semantic context ---
        sem_ctx = {**base_ctx, "domains": rows}
        sem_ctx["mean_score"] = str(sem_mean)
        sem_ctx["below_threshold_count"] = str(sem_below)
        sem_ctx["threshold"] = "70"

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
        sum_ctx["humanize_count"] = "0"

        # --- Output directory ---
        output_dir = os.path.join(str(repo_root), "docs", "paper",
                                  f"paper-{paper_id}", "audit")
        os.makedirs(output_dir, exist_ok=True)

        rendered = []

        # --- Render each template pair (markdown + HTML) ---
        for name, ctx in [("deterministic", det_ctx),
                          ("semantic", sem_ctx),
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


if __name__ == "__main__":
    main()
