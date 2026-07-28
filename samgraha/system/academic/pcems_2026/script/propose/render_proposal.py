"""render_proposal.py — renders a persisted proposal to markdown + html.

Reads from ``academic_proposal_review`` (written by approve_proposal.py
with summary/content_md/iteration from metadata_json), falls back to
generic ``proposal.metadata_json`` for backward compatibility.

Expected --in payload:
  {paper_id: int, phase: str, scope_domain_id: int (optional)}

Render output: docs/paper/paper-{id}/proposal/{phase}.md / .html
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "common"))
import academic_schema  # noqa: E402

import chevron  # noqa: E402

TEMPLATES_MD = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "..", "templates", "proposal", "markdown")
TEMPLATES_HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "..", "..", "templates", "proposal", "html")


def _load_template(template_dir, filename):
    path = os.path.join(template_dir, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def _build_context(conn, paper_id, phase, scope_domain_id):
    """Build render context from academic_proposal_review, then
    fall back to generic proposal.metadata_json."""
    # Try review table first (has all content cols)
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
    conn = academic_schema.get_conn(db_path)
    try:
        ctx = _build_context(conn, paper_id, phase, scope_domain_id)
        if not ctx:
            write_envelope(out_path, status="error",
                           message=f"no proposal for phase={phase}")
            return
    finally:
        conn.close()

    output_dir = os.path.join(
        str(repo_root), "docs", "paper", f"paper-{paper_id}", "proposal")
    os.makedirs(output_dir, exist_ok=True)

    out_stem = f"{phase}-{ctx.get('target_domain', '')}" if ctx.get("target_domain") else phase

    rendered = []
    for fmt, tpl_dir, ext in [("markdown", TEMPLATES_MD, ".md"),
                               ("html", TEMPLATES_HTML, ".html")]:
        tpl = _load_template(tpl_dir, f"{phase}{ext}")
        if tpl:
            out = chevron.render(tpl, ctx)
            out_path_file = os.path.join(output_dir, f"{out_stem}{ext}")
            with open(out_path_file, "w", encoding="utf-8") as f:
                f.write(out)
            rendered.append(out_path_file)

    write_envelope(out_path, status="ok",
                   message=f"rendered proposal to {len(rendered)} files",
                   rendered=rendered)


if __name__ == "__main__":
    main()
