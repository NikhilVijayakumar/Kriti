"""generate_audit_report.py — populates the audit report template from
score/audit/plagiarism results. Produces markdown + HTML audit report.
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

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "..", "..", "templates", "audit", "report")


def _load_template(name):
    path = os.path.join(TEMPLATES_DIR, name)
    if os.path.isfile(path):
        with open(path, "r") as f:
            return f.read()
    return None


def _format_domain_row(domain_key, sem_score, det_score, final_score,
                       score_band, det_verdict, plag_verdict, trend):
    return (
        f"| {domain_key} "
        f"| {sem_score or 'N/A'} "
        f"| {det_score or 'N/A'} "
        f"| {final_score or 'N/A'} "
        f"| {score_band or 'N/A'} "
        f"| {det_verdict or 'N/A'} "
        f"| {plag_verdict or 'N/A'} "
        f"| {trend or 'N/A'} |"
    )


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
        rows = []
        all_det_pass = True
        all_sem_pass = True

        for domain_id, domain_key, display_name, sort_order in domains:
            # Semantic score
            sem = conn.execute(
                "SELECT overall_score FROM academic_semantic_runs "
                "WHERE paper_id=? AND domain_id=? "
                "ORDER BY run_number DESC LIMIT 1",
                (paper_id, domain_id),
            ).fetchone()
            sem_score = round(sem["overall_score"], 1) if sem else None

            # Deterministic findings
            det = conn.execute(
                "SELECT verdict, findings FROM academic_deterministic_findings "
                "WHERE paper_id=? AND domain_id=? "
                "ORDER BY run_number DESC LIMIT 1",
                (paper_id, domain_id),
            ).fetchone()
            det_verdict = det["verdict"] if det else None
            det_score = None
            if det:
                findings = json.loads(det["findings"]) if det["findings"] else []
                if findings:
                    passed = sum(1 for f in findings if f.get("passed", False))
                    det_score = round((passed / len(findings)) * 100, 1) if findings else None

            # Plagiarism verdict
            plag = conn.execute(
                "SELECT verdict FROM academic_plagiarism_findings "
                "WHERE paper_id=? AND domain_id=? AND pass_type='forensic' "
                "ORDER BY run_number DESC LIMIT 1",
                (paper_id, domain_id),
            ).fetchone()
            plag_verdict = plag["verdict"] if plag else None

            # Score history for trend
            history = academic_schema.get_score_history(conn, paper_id, domain_key)
            trend = "N/A"
            final_score = None
            score_band = None
            if history:
                latest = history[-1]
                final_score = round(latest["final_score"], 1)
                score_band = latest["score_band"]
                if latest.get("trend_delta") is not None:
                    delta = latest["trend_delta"]
                    trend = "Improved" if delta > 0.1 else ("Regressed" if delta < -0.1 else "Unchanged")

            if det_verdict == "FAIL":
                all_det_pass = False
            if sem_score is not None and sem_score < 70:
                all_sem_pass = False

            rows.append(_format_domain_row(
                domain_key, sem_score, det_score, final_score,
                score_band, det_verdict, plag_verdict, trend
            ))

        # Generate markdown report
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        report_md = f"""# Audit Report — {paper['title'] or f'Paper {paper_id}'}

Generated: {ts}

## Score Summary

| Domain | Semantic | Deterministic | Final | Band | Det Audit | Plagiarism | Trend |
|--------|----------|---------------|-------|------|-----------|------------|-------|
{chr(10).join(rows)}

## Status

- Deterministic audit: **{'ALL PASS' if all_det_pass else 'SOME FAIL'}**
- Semantic audit: **{'ALL PASS' if all_sem_pass else 'SOME BELOW THRESHOLD'}**
"""

        # Write markdown
        output_dir = os.path.join(str(repo_root), "docs", "paper",
                                  paper.get("title", f"paper-{paper_id}"))
        os.makedirs(output_dir, exist_ok=True)
        md_path = os.path.join(output_dir, "audit-report.md")
        with open(md_path, "w") as f:
            f.write(report_md)

        # Record in report_history
        academic_schema.record_report(
            conn, paper_id, "markdown", md_path,
            report_kind="audit"
        )

        write_envelope(out_path, status="ok",
                       message=f"audit report generated: {md_path}",
                       file_path=md_path)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
