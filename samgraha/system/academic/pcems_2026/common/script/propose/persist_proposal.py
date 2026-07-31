"""persist_proposal.py — det step, emits proposal envelope key.

Output ``{"proposal": {"title": ..., "phases": [...], "metadata": {...}}}``
so that the deterministic step runner in step_execution.rs can validate
against proposal.schema.json and INSERT into the generic ``proposal``
table (execution_id, phase, title, phases_json, metadata_json).

Expected --in payload:
  {paper_id: int, phase: str, scope_domain_id: int (optional),
   source: str, commit_sha: str, summary: str, content_md: str,
   user_comment: str (optional), iteration: int (optional, default 0),
   computed_context: dict (optional — domains, findings, scores, etc.)}

Legacy academic_proposals table NO LONGER written.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _adapter import parse_step_args, write_envelope  # noqa: E402
import academic_schema  # noqa: E402
from _phase_map import get_phase_domain_keys  # noqa: E402


def _lookup_step_ids(conn, usecase_name):
    rows = conn.execute(
        "SELECT s.id FROM step s JOIN usecase u ON u.id = s.usecase_id "
        "WHERE u.name = ? ORDER BY s.step_order",
        (usecase_name,),
    ).fetchall()
    return [r["id"] for r in rows]


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    phase = payload["phase"]
    conn = academic_schema.get_conn(db_path)
    try:
        meta = conn.execute(
            "SELECT title FROM academic_papers WHERE id=?",
            (payload["paper_id"],),
        ).fetchone()

        paper_title = meta["title"] if meta else "(untitled)"
        rationale = _build_rationale(phase, payload, paper_title)

        proposal_title = f"{phase} proposal for \"{paper_title}\""
        phases = []

        if phase == "fix":
            scope_domain_id = payload.get("scope_domain_id")
            if scope_domain_id is not None:
                dk_row = conn.execute(
                    "SELECT key FROM academic_domains WHERE id=?",
                    (scope_domain_id,),
                ).fetchone()
                if dk_row:
                    dk = dk_row["key"]
                    uc_name = f"generate-section-draft-{dk}"
                    step_ids = _lookup_step_ids(conn, uc_name)
                    phases.append({
                        "domain": dk,
                        "phase_number": 1,
                        "usecases": [uc_name],
                        "steps": step_ids,
                        "rationale": f"fix {dk} domain",
                    })
        else:
            for i, dk in enumerate(get_phase_domain_keys(phase)):
                uc_name = f"generate-section-draft-{dk}"
                step_ids = _lookup_step_ids(conn, uc_name)
                phases.append({
                    "domain": dk,
                    "phase_number": i + 1,
                    "usecases": [uc_name],
                    "steps": step_ids,
                    "rationale": f"covers {dk} for {phase}",
                })

        metadata = {}
        for key in ("summary", "content_md", "computed_context", "user_comment", "iteration"):
            if payload.get(key) is not None:
                metadata[key] = payload[key]

        write_envelope(
            out_path,
            status="ok",
            message=f"proposal drafted, phase={phase}",
            proposal={
                "title": proposal_title,
                "phases": phases,
                "metadata": metadata or None,
            },
        )
    finally:
        conn.close()


def _build_rationale(phase, payload, paper_title):
    ctx = payload.get("computed_context", {})
    if phase == "input":
        return (
            f"Input proposal for \"{paper_title}\" — "
            f"paper metadata and source weight specification."
        )
    elif phase == "map":
        mk = ctx.get("map_kind", "") or payload.get("map_kind", "")
        return (
            f"Map proposal for \"{paper_title}\" — "
            f"extract {mk} entries from source materials."
        )
    elif phase == "generation":
        domain_count = len(ctx.get("domains", []))
        return (
            f"Generation proposal for \"{paper_title}\" — "
            f"{domain_count} structural domains to generate."
        )
    elif phase == "audit":
        domain_count = len(ctx.get("domains", []))
        return (
            f"Audit proposal for \"{paper_title}\" — "
            f"{domain_count} domains to audit (structural + cross-cutting)."
        )
    elif phase == "report":
        score = ctx.get("current_final_score")
        band = ctx.get("current_score_band", "")
        score_str = f"score {score} ({band})" if score else "no score yet"
        return (
            f"Report proposal for \"{paper_title}\" — {score_str}."
        )
    elif phase == "section":
        dk = payload.get("scope_domain_id", "")
        return (
            f"Section proposal for \"{paper_title}\" — "
            f"domain_id={dk}."
        )
    elif phase == "fix":
        return (
            f"Fix proposal for \"{paper_title}\" — "
            f"scope_domain_id={payload.get('scope_domain_id')}."
        )
    return f"Proposal for \"{paper_title}\" — phase={phase}."


if __name__ == "__main__":
    main()
