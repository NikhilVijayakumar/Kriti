"""assemble-markdown-document.py - assembles all domain drafts into a single
Markdown document, the section-wise draft that precedes HTML/PDF rendering.

Mirrors assemble-final-document.py (HTML) but reads templates/generation/
markdown/*.md instead of html/*.md, and concatenates fragments directly -
there is no markdown master-wrapper template (no head/style to inject),
each domain's rendered fragment already starts with its own heading.

Expected --in payload: {paper_id: int}
"""
import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import academic_schema  # noqa: E402

_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "_shared"))
import assemble_common  # noqa: E402

MARKDOWN_TEMPLATES = assemble_common.TEMPLATE_ROOT


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]

    sections_order, cross_cutting = assemble_common.load_schema()

    conn = academic_schema.get_conn(db_path)
    assembled_parts = []

    try:
        domain_contexts = assemble_common.build_domain_contexts(
            academic_schema, conn, paper_id, sections_order, cross_cutting)

        for domain in sections_order:
            template_file = MARKDOWN_TEMPLATES / f"{domain}.md"
            if template_file.exists():
                template = template_file.read_text(encoding="utf-8")
                context = domain_contexts.get(domain, {})
                rendered = assemble_common.render_mustache(template, context)
                assembled_parts.append(rendered)

    finally:
        conn.close()

    assembled_md = "\n\n---\n\n".join(assembled_parts)

    # Write under .samgraha/output/draft/paper-{id}/markdown/ - generated,
    # in-progress content, not the finished paper deliverable that belongs
    # under docs/paper/. Split by artifact type (markdown/html/docx/pdf)
    # so each format lands in its own subfolder.
    md_dir = repo_root / ".samgraha" / "output" / "draft" / f"paper-{paper_id}" / "markdown"
    md_dir.mkdir(parents=True, exist_ok=True)
    md_path = md_dir / "paper.md"
    md_path.write_text(assembled_md, encoding="utf-8")

    write_envelope(
        out_path, status="ok",
        message=f"assembled {len(assembled_parts)} sections for paper {paper_id}",
        paper_id=paper_id,
        sections_assembled=len(assembled_parts),
        md_path=str(md_path),
    )


if __name__ == "__main__":
    main()
