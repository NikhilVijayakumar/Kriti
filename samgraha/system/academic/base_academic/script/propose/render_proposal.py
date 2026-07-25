"""render_proposal.py — renders a persisted proposal to markdown + html.

Expected --in payload:
  {paper_id: int, phase: str, scope_domain_id: int (optional)}

Reads the latest proposal row for (paper_id, phase, scope_domain_id),
renders through the matching template, writes to docs/paper/paper-{id}/
proposal/. scope_domain_id must be passed for domain-scoped fix
proposals — persist_proposal.py's is_latest flag is scoped per
(paper, phase, scope_domain_id), so more than one domain can have its
own latest=1 fix-proposal row concurrently; omitting it here would pick
an arbitrary one via ORDER BY created_at DESC LIMIT 1 instead of the
one actually being rendered.
"""
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


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    phase = payload["phase"]
    scope_domain_id = payload.get("scope_domain_id")
    conn = academic_schema.get_conn(db_path)
    try:
        row = conn.execute(
            "SELECT * FROM academic_proposals "
            "WHERE paper_id=? AND phase=? AND scope_domain_id IS ? "
            "AND is_latest=1 ORDER BY created_at DESC LIMIT 1",
            (paper_id, phase, scope_domain_id)).fetchone()
        if not row:
            write_envelope(out_path, status="error",
                           message=f"no proposal for phase={phase}")
            return
        ctx = dict(row)
        # Flatten for chevron — scope_domain_id -> target_domain key
        if ctx.get("scope_domain_id"):
            dom_row = conn.execute(
                "SELECT key FROM academic_domains WHERE id=?",
                (ctx["scope_domain_id"],)).fetchone()
            ctx["target_domain"] = dom_row["key"] if dom_row else ""
        else:
            ctx["target_domain"] = ""
    finally:
        conn.close()

    # Build output directory
    output_dir = os.path.join(
        str(repo_root), "docs", "paper", f"paper-{paper_id}", "proposal")
    os.makedirs(output_dir, exist_ok=True)

    # Output filename disambiguates by domain for domain-scoped fix
    # proposals — the template itself (fix.md) is shared across domains,
    # but two domains' rendered fix proposals must not overwrite each
    # other on disk the way their DB rows don't overwrite each other.
    out_stem = f"{phase}-{ctx['target_domain']}" if ctx["target_domain"] else phase

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
