"""assemble-final-document.py — assembles all domain drafts into a single
HTML document ready for rendering.

Reads the master schema (section order + cross-cutting list), fetches each
domain's latest narrative from academic_narratives, fills the corresponding
HTML fragment template, weaves cross-cutting content into target sections,
and writes the assembled HTML to disk.

Expected --in payload: {paper_id: int}
"""
import json as _json
import re as _re
import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import academic_schema  # noqa: E402

# Path to the pcems_2026 system root
SYSTEM_ROOT = _Path(__file__).resolve().parent.parent.parent
TEMPLATE_ROOT = SYSTEM_ROOT / "templates" / "generation"
HTML_TEMPLATES = TEMPLATE_ROOT / "html"
SCHEMA_YAML = TEMPLATE_ROOT / "markdown" / "_master-schema.yaml"

# Cross-cutting domain → target section mapping
# (content woven INTO the target, not rendered standalone)
CROSS_CUTTING_TARGETS = {
    "novelty": "introduction",
    "gaps": "introduction",
    "mathematics": "methodology",
    "tables": "findings",
    "figures": "findings",
}


def _load_schema():
    """Parse _master-schema.yaml into sections list and cross_cutting list."""
    import yaml
    with open(SCHEMA_YAML, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("sections", []), data.get("cross_cutting", [])


def _render_mustache(template_text, context):
    """Minimal Mustache renderer — handles {{{ key }}} and {{#list}}...{{/list}}."""
    # First: render lists {{#key}}...{{/key}}
    def _render_list(match):
        tag = match.group(1)
        body = match.group(2)
        items = context.get(tag, [])
        if not items:
            return ""
        parts = []
        for i, item in enumerate(items):
            rendered = body
            if isinstance(item, dict):
                for k, v in item.items():
                    rendered = _re.sub(r'\{\{\{?\s*' + _re.escape(k) + r'\s*\}\}\}?', str(v), rendered)
            else:
                # Simple string item — replace {{{ . }}} or {{ . }}
                rendered = _re.sub(r'\{\{\{?\s*\.\s*\}\}\}?', str(item), rendered)
            # Handle {{^last}}...{{/last}} — show separator only if not last
            rendered = _re.sub(
                r'\{\{\^last\}\}(.*?)\{\{/last\}\}',
                lambda m: m.group(1) if i < len(items) - 1 else "",
                rendered, flags=_re.DOTALL
            )
            parts.append(rendered)
        return "".join(parts)

    result = _re.sub(
        r'\{\{#(\w+)\}\}(.*?)\{\{/\1\}\}',
        _render_list, template_text, flags=_re.DOTALL
    )

    # Then: render simple keys {{{ key }}} and {{ key }}
    for key, value in context.items():
        if isinstance(value, (dict, list)):
            continue
        result = _re.sub(
            r'\{\{\{?\s*' + _re.escape(key) + r'\s*\}\}\}?',
            str(value) if value is not None else "",
            result
        )
    return result


def _parse_draft_to_context(sections):
    """Convert a list of {heading, text} sections into a flat key-value dict
    by converting headings to snake_case keys."""
    ctx = {}
    for s in sections:
        heading = s.get("heading", "")
        text = s.get("text", "")
        # Convert heading to snake_case key
        key = heading.lower().strip()
        key = _re.sub(r'[^a-z0-9]+', '_', key)
        key = key.strip('_')
        if key:
            ctx[key] = text
    return ctx


def _get_final_structural_draft(conn, paper_id, domain):
    """Read a structural domain's most finished draft. `polish` (4e) is the
    true final stage for the 6 generated domains — falls back to
    `budget-fit` (4d) if polish hasn't run yet, then `cite`, since
    `references` never goes through 4a-4e at all (collate-references
    writes it once, at stage='cite', and nothing ever advances it further
    — it would otherwise render empty under a polish/budget-fit-only
    fallback)."""
    for stage in ("polish", "budget-fit", "cite"):
        draft = academic_schema.get_narrative(conn, paper_id, domain, stage=stage)
        if draft:
            return draft
    return None


def _parse_cross_cutting(analysis_row):
    """Cross-cutting content lives in academic_cross_module_analysis (a
    single `content` blob per analysis_kind), not academic_narratives — a
    completely different table/shape than structural domains use. Wrap the
    blob as one block so the weaving loop below can treat both uniformly."""
    if not analysis_row or not analysis_row.get("content"):
        return []
    return [{"heading": analysis_row["analysis_kind"].title(),
             "text": analysis_row["content"]}]


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]

    sections_order, cross_cutting = _load_schema()

    # Read the master HTML template
    master_html = (HTML_TEMPLATES / "_master-schema.html").read_text(encoding="utf-8")

    conn = academic_schema.get_conn(db_path)
    assembled_parts = []

    try:
        # Build context for each structural domain
        domain_contexts = {}
        for domain in sections_order:
            draft = _get_final_structural_draft(conn, paper_id, domain)
            if draft:
                domain_contexts[domain] = _parse_draft_to_context(draft)
            else:
                domain_contexts[domain] = {}

        # Read cross-cutting domains — prefer academic_narratives (polished
        # drafts from generate-section-draft-{domain}) over raw
        # academic_cross_module_analysis blobs.
        cross_cutting_content = {}
        for cc_domain in cross_cutting:
            # Try polished narrative first (stage='generate' from the
            # generate-section-draft-{domain} usecase)
            draft = academic_schema.get_narrative(
                conn, paper_id, cc_domain, stage="generate")
            if draft:
                cross_cutting_content[cc_domain] = draft
            else:
                # Fall back to raw cross_module_analysis blob
                analysis_row = academic_schema.get_cross_module_analysis(
                    conn, paper_id, analysis_kind=cc_domain)
                cross_cutting_content[cc_domain] = _parse_cross_cutting(analysis_row)

        # Weave cross-cutting content into target sections
        for cc_domain, target_section in CROSS_CUTTING_TARGETS.items():
            if cc_domain in cross_cutting_content and cross_cutting_content[cc_domain]:
                blocks = cross_cutting_content[cc_domain]
                for block in blocks:
                    # Add as a subsection to the target section's context
                    key = target_section
                    if key not in domain_contexts:
                        domain_contexts[key] = {}
                    # Store with a prefixed key for the template
                    cc_key = f"cross_cutting_{cc_domain}_{block['heading'].lower().replace(' ', '_')}"
                    domain_contexts[key][cc_key] = block["text"]

        # Render each structural domain's HTML fragment
        for domain in sections_order:
            template_file = HTML_TEMPLATES / f"{domain}.html"
            if template_file.exists():
                template = template_file.read_text(encoding="utf-8")
                context = domain_contexts.get(domain, {})
                rendered = _render_mustache(template, context)
                assembled_parts.append(rendered)

    finally:
        conn.close()

    # Assemble the final document
    assembled_html = "\n\n".join(assembled_parts)
    final_html = master_html.replace("{{{ assembled_sections }}}", assembled_html)

    # Write the artifact to its own path under docs/paper/ — out_path is
    # reserved for the status envelope (write_envelope below would
    # otherwise clobber the HTML we just wrote, since both would target
    # the same file).
    html_dir = repo_root / "docs" / "paper" / f"paper-{paper_id}"
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
