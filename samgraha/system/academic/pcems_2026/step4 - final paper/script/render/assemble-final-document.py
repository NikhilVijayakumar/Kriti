"""assemble-final-document.py - assembles all domain drafts into a single
HTML document ready for rendering.

Reads the master schema (section order + cross-cutting list), fetches each
domain's latest narrative from academic_narratives, fills the corresponding
HTML fragment template, weaves cross-cutting content into target sections,
and writes the assembled HTML to disk.

Expected --in payload: {paper_id: int}
"""
import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import academic_schema  # noqa: E402

_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "_shared"))
import assemble_common  # noqa: E402

HTML_TEMPLATES = assemble_common.TEMPLATE_ROOT / "html"


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]

    sections_order, cross_cutting = assemble_common.load_schema()

    master_html = (HTML_TEMPLATES / "_master-schema.html").read_text(encoding="utf-8")

    conn = academic_schema.get_conn(db_path)
    assembled_parts = []

    try:
        domain_contexts = assemble_common.build_domain_contexts(
            academic_schema, conn, paper_id, sections_order, cross_cutting)

        for domain in sections_order:
            template_file = HTML_TEMPLATES / f"{domain}.html"
            if template_file.exists():
                template = template_file.read_text(encoding="utf-8")
                context = domain_contexts.get(domain, {})
                rendered = assemble_common.render_mustache(template, context)
                assembled_parts.append(rendered)

    finally:
        conn.close()

    assembled_html = "\n\n".join(assembled_parts)
    final_html = master_html.replace("{{{ assembled_sections }}}", assembled_html)

    # Write the artifact under .samgraha/output/draft/paper-{id}/html/ -
    # this is generated, in-progress content, not the finished paper
    # deliverable that belongs under docs/paper/. Split by artifact type
    # (markdown/html/docx/pdf) so each format lands in its own subfolder.
    # out_path is reserved for the status envelope (write_envelope below
    # would otherwise clobber the HTML we just wrote, since both would
    # target the same file).
    html_dir = repo_root / ".samgraha" / "output" / "draft" / f"paper-{paper_id}" / "html"
    html_dir.mkdir(parents=True, exist_ok=True)
    html_path = html_dir / "assembled.html"
    html_path.write_text(final_html, encoding="utf-8")

    write_envelope(
        out_path, status="ok",
        message=f"assembled {len(assembled_parts)} sections for paper {paper_id}",
        paper_id=paper_id,
        sections_assembled=len(assembled_parts),
        html_path=str(html_path),
    )


if __name__ == "__main__":
    main()
