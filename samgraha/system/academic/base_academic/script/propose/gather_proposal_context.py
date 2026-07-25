"""gather_proposal_context.py — det step, first in every propose-* chain.

Gathers the context needed to draft a proposal: upstream analyses,
domain lists, rubric info, failing findings, or redraft context.

Expected --in payload:
  {paper_id: int, phase: str, commit_sha: str,
   scope_domain_id: int (optional, fix only),
   user_comment: str (optional, fix/user-request only),
   models: list (optional, audit only)}
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "common"))
import academic_schema  # noqa: E402


def _load_paper_meta(conn, paper_id):
    """Shared by all four branches — title, fetched once per invocation."""
    return conn.execute(
        "SELECT title FROM academic_papers WHERE id=?", (paper_id,)).fetchone()


def _redraft_context(conn, paper_id, phase, scope_domain_id):
    """If the latest row for this (phase, scope_domain) is rejected,
    surface it for the redraft (§6a)."""
    row = conn.execute(
        "SELECT content_md, user_comment, iteration FROM academic_proposals "
        "WHERE paper_id=? AND phase=? AND scope_domain_id IS ? "
        "AND is_latest=1 AND status='rejected'",
        (paper_id, phase, scope_domain_id)).fetchone()
    return dict(row) if row else None


def _gather_generation_context(conn, paper_id):
    """Gather upstream analysis summaries + domain list for generation proposal."""
    domains = [r[0] for r in conn.execute(
        "SELECT key FROM academic_domains ORDER BY sort_order").fetchall()]

    # Latest cross-module analyses
    analyses = {}
    for kind in ("novelty", "gaps", "mathematics", "architecture"):
        row = conn.execute(
            "SELECT content FROM academic_cross_module_analysis "
            "WHERE paper_id=? AND analysis_kind=? "
            "ORDER BY created_at DESC LIMIT 1", (paper_id, kind)).fetchone()
        analyses[kind] = row["content"][:500] if row else "(none yet)"

    # Domain narrative stages
    domain_details = []
    for key in domains:
        domain_id = conn.execute(
            "SELECT id FROM academic_domains WHERE key=?", (key,)).fetchone()
        if not domain_id:
            continue
        stage_row = conn.execute(
            "SELECT stage FROM academic_narratives "
            "WHERE paper_id=? AND domain_id=? "
            "ORDER BY iteration DESC LIMIT 1",
            (paper_id, domain_id["id"])).fetchone()
        stage = stage_row["stage"] if stage_row else "not started"
        domain_details.append({"domain_key": key, "stage": stage})

    return {
        "domains": domain_details,
        "novelty_summary": analyses.get("novelty", ""),
        "gaps_summary": analyses.get("gaps", ""),
        "math_summary": analyses.get("mathematics", ""),
        "diagram_summary": analyses.get("architecture", ""),
    }


def _gather_audit_context(conn, paper_id, models=None):
    """Gather generated domains + rubric info for audit proposal."""
    domains = [r[0] for r in conn.execute(
        "SELECT key FROM academic_domains ORDER BY sort_order").fetchall()]

    domain_details = []
    for key in domains:
        domain_details.append({
            "domain_key": key,
            "det_rule_count": "(from deterministic rules)",
            "rubric_summary": "(from semantic rubric)",
        })

    return {
        "domains": domain_details,
        "models": models or ["default"],
    }


def _gather_report_context(conn, paper_id):
    """Gather latest score + report kinds for report proposal."""
    score_row = conn.execute(
        "SELECT final_score, score_band FROM academic_score_history "
        "WHERE paper_id=? ORDER BY created_at DESC LIMIT 1",
        (paper_id,)).fetchone()

    kinds = [r[0] for r in conn.execute(
        "SELECT DISTINCT report_kind FROM academic_report_history "
        "WHERE paper_id=? ORDER BY report_kind", (paper_id,)).fetchall()]

    return {
        "current_final_score": str(score_row["final_score"]) if score_row else "(not calculated)",
        "current_score_band": score_row["score_band"] if score_row else "(not calculated)",
        "report_kinds": kinds,
    }


def _gather_fix_context(conn, paper_id, domain_id, user_comment):
    """Gather failing findings or user comment for fix proposal.
    domain_id is the already-resolved academic_domains.id (request_fix.py
    resolves the key -> id itself, exact-match-or-error — see script/
    propose/request_fix.py's _resolve_domain()), not a raw key string."""
    target_domain = None
    if domain_id:
        row = conn.execute(
            "SELECT id, key FROM academic_domains WHERE id=?",
            (domain_id,)).fetchone()
        if row:
            target_domain = {"id": row["id"], "key": row["key"]}

    # Try to get failing deterministic findings
    triggering_finding = ""
    if target_domain:
        finding_row = conn.execute(
            "SELECT findings, verdict FROM academic_deterministic_findings "
            "WHERE paper_id=? AND domain_id=? AND verdict='FAIL' "
            "ORDER BY created_at DESC LIMIT 1",
            (paper_id, target_domain["id"])).fetchone()
        if finding_row:
            triggering_finding = finding_row["findings"]

    return {
        "target_domain": target_domain,
        "user_comment": user_comment,
        "triggering_finding": triggering_finding,
    }


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    phase = payload["phase"]
    conn = academic_schema.get_conn(db_path)
    try:
        meta = _load_paper_meta(conn, payload["paper_id"])
        redraft = _redraft_context(conn, payload["paper_id"], phase,
                                    payload.get("scope_domain_id"))
        if redraft and redraft["iteration"] >= 5:
            write_envelope(out_path, status="error",
                           message="proposal rejected 5 times — escalate to human_review")
            return
        if phase == "generation":
            context = _gather_generation_context(conn, payload["paper_id"])
        elif phase == "audit":
            context = _gather_audit_context(conn, payload["paper_id"],
                                             payload.get("models"))
        elif phase == "report":
            context = _gather_report_context(conn, payload["paper_id"])
        elif phase == "fix":
            context = _gather_fix_context(conn, payload["paper_id"],
                                           payload.get("scope_domain_id"),
                                           payload.get("user_comment", ""))
        else:
            write_envelope(out_path, status="error",
                           message=f"unknown phase: {phase}")
            return
        context["paper_title"] = meta["title"] if meta else ""
        context["redraft_of"] = redraft
        context["iteration"] = (redraft["iteration"] + 1) if redraft else 0
    finally:
        conn.close()
    write_envelope(out_path, status="ok", message=f"gathered {phase} context",
                   **context)


if __name__ == "__main__":
    main()
