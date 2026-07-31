"""render_proposal.py — renders a persisted proposal to markdown + html.

Reads from ``academic_proposal_review`` (written by approve_proposal.py
with summary/content_md/iteration from metadata_json), falls back to
generic ``proposal.metadata_json`` for backward compatibility.

Expected --in payload:
  {paper_id: int, phase: str, scope_domain_id: int (optional)}

Render output: .samgraha/output/proposal/{phase}/paper-{id}/{phase}.md / .html
(phase is generation/audit/fix/report — the proposal category)
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _adapter import parse_step_args, write_envelope  # noqa: E402
import academic_schema  # noqa: E402

import chevron  # noqa: E402

PCEMS_ROOT = Path(__file__).resolve().parent.parent.parent.parent

def _template_dirs_for_phase(phase):
    if phase in ("input", "map"):
        return [PCEMS_ROOT / "step0-extract" / phase / "templates"]
    if phase in ("section", "audit"):
        return [PCEMS_ROOT / "step1-draft-for-completeness" / phase / "templates"]
    if phase == "fix":
        return [PCEMS_ROOT / "common" / "templates" / "propose"]
    return [PCEMS_ROOT / "templates" / "proposal" / "markdown"]  # report — Final-render, unmoved


def _load_template(template_dir, filename):
    path = os.path.join(template_dir, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def _build_context(conn, paper_id, phase, scope_domain_id, map_kind=None):
    """Build render context from academic_proposal_review, then
    fall back to generic proposal.metadata_json."""
    # Try review table first (has all content cols)
    if phase == "map" and map_kind:
        row = conn.execute(
            "SELECT r.*, p.title FROM academic_proposal_review r "
            "JOIN proposal p ON p.id = r.proposal_id "
            "WHERE r.paper_id=? AND r.phase=? AND r.map_kind=? "
            "AND r.is_latest=1 ORDER BY r.id DESC LIMIT 1",
            (paper_id, phase, map_kind),
        ).fetchone()
    else:
        row = conn.execute(
            "SELECT r.*, p.title FROM academic_proposal_review r "
            "JOIN proposal p ON p.id = r.proposal_id "
            "WHERE r.paper_id=? AND r.phase=? AND r.scope_domain_id IS ? "
            "AND r.is_latest=1 ORDER BY r.id DESC LIMIT 1",
            (paper_id, phase, scope_domain_id),
        ).fetchone()
    if row:
        ctx = dict(row)
        if ctx.get("computed_context"):
            try:
                extra = json.loads(ctx["computed_context"])
                ctx.update(extra)
            except (json.JSONDecodeError, TypeError):
                pass
        if ctx.get("scope_domain_id"):
            dom_row = conn.execute(
                "SELECT key FROM academic_domains WHERE id=?",
                (ctx["scope_domain_id"],),
            ).fetchone()
            ctx["target_domain"] = dom_row["key"] if dom_row else ""
        else:
            ctx["target_domain"] = ""
        return ctx

    # Fallback to generic proposal metadata_json
    row = conn.execute(
        "SELECT p.title, p.metadata_json FROM proposal p "
        "JOIN execution e ON e.id = p.execution_id "
        "JOIN step s ON s.id = e.step_id "
        "JOIN usecase u ON u.id = s.usecase_id "
        "WHERE u.name LIKE ? "
        "ORDER BY e.id DESC LIMIT 1",
        (f"persist-proposal-{phase}%",),
    ).fetchone()
    if row:
        ctx = {"title": row["title"], "target_domain": ""}
        if row["metadata_json"]:
            try:
                meta = json.loads(row["metadata_json"])
                ctx.update(meta)
            except (json.JSONDecodeError, TypeError):
                pass
        return ctx
    return None


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    phase = payload["phase"]
    scope_domain_id = payload.get("scope_domain_id")
    map_kind = payload.get("map_kind") if phase == "map" else None
    # Phase → step output directory mapping (Proposal 17 convention).
    # input/map are Step 0's own gates (Proposal 15 moved their usecases
    # into step0-extract/); report is Final-render's own phase — routing
    # either to step1 was a bug, not a real convention.
    _PHASE_TO_STEP_DIR = {
        "input": "step0-extract",
        "map": "step0-extract",
        "section": "step1-draft-for-completeness",
        "audit": "step1-draft-for-completeness",
        "fix": "step1-draft-for-completeness",
        "report": "step4-final-render",
    }

    step_dir = _PHASE_TO_STEP_DIR.get(phase, "step1-draft-for-completeness")

    output_dir = os.path.join(
        str(repo_root), ".samgraha", "output",
        step_dir, "proposal", phase, f"paper-{paper_id}")
    os.makedirs(output_dir, exist_ok=True)

    conn = academic_schema.get_conn(db_path)
    try:
        ctx = _build_context(conn, paper_id, phase, scope_domain_id, map_kind)
        if not ctx:
            write_envelope(out_path, status="error",
                           message=f"no proposal for phase={phase}")
            return
    finally:
        pass  # keep conn open for tracking insert below

    out_stem = f"{phase}-{ctx.get('target_domain', '')}" if ctx.get("target_domain") else phase

    rendered = []
    for tpl_dir in _template_dirs_for_phase(phase):
        # Try category-specific template first (e.g. map-figures.md), fall back to generic (map.md)
        tpl_name = f"{phase}-{map_kind}.md" if map_kind else None
        tpl = _load_template(tpl_dir, tpl_name) if tpl_name else None
        if not tpl:
            tpl = _load_template(tpl_dir, f"{phase}.md")
        if tpl:
            out = chevron.render(tpl, ctx)
            out_path_file = os.path.join(output_dir, f"{out_stem}.md")
            with open(out_path_file, "w", encoding="utf-8") as f:
                f.write(out)
            rendered.append(out_path_file)
            break

    # Insert tracking row
    for fp in rendered:
        rel_path = os.path.relpath(fp, str(repo_root))
        academic_schema.record_report(
            conn, paper_id, "markdown", rel_path,
            report_kind="proposal",
            scope_domain_id=scope_domain_id,
            map_kind=map_kind,
        )

    write_envelope(out_path, status="ok",
                   message=f"rendered proposal to {len(rendered)} files",
                   rendered=rendered)
    conn.close()


if __name__ == "__main__":
    main()
