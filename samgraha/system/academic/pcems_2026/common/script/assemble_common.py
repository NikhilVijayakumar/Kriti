"""assemble_common.py — shared logic for assemble-final-document.py (HTML)
and assemble-markdown-document.py (Markdown): schema loading, the minimal
mustache renderer, and domain narrative -> template-context conversion.
"""
import json as _json
import re as _re
from pathlib import Path as _Path


def _strip_comments(text):
    """Strip mustache {{! ... }} comments with depth tracking.

    Uses a bracket-depth scanner instead of a regex because comments
    may contain literal {{...}} example text (e.g. {{! ... {{#tables}}
    ... }}) — the inner }} would close a non-greedy .*? regex early,
    leaking everything after it into the rendered output.

    Every {{ increments depth, }} decrements it.  The scanner only
    stops at the }} that brings depth back to 0, correctly handling
    nested {{...}} inside the comment body.
    """
    result = []
    i = 0
    while True:
        start = text.find("{{!", i)
        if start == -1:
            result.append(text[i:])
            break
        result.append(text[i:start])
        j = start + 3
        depth = 1
        while j < len(text) and depth > 0:
            if text[j:j+2] == "{{":
                depth += 1
                j += 2
            elif text[j:j+2] == "}}":
                depth -= 1
                j += 2
            else:
                j += 1
        i = j
    return "".join(result)

SYSTEM_ROOT = _Path(__file__).resolve().parent.parent.parent
TEMPLATE_ROOT = SYSTEM_ROOT / "step1-draft-for-completeness" / "section" / "templates"
SCHEMA_YAML = TEMPLATE_ROOT / "_master-schema.yaml"

# Cross-cutting domain -> target section mapping
# (content woven INTO the target, not rendered standalone)
CROSS_CUTTING_TARGETS = {
    "novelty": "introduction",
    "gaps": "introduction",
    "mathematics": "methodology",
    "tables": "findings",
    "figures": "findings",
}


def load_schema():
    """Parse _master-schema.yaml into sections list and cross_cutting list."""
    import yaml
    with open(SCHEMA_YAML, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("sections", []), data.get("cross_cutting", [])


def render_mustache(template_text, context):
    """Minimal Mustache renderer — handles {{{ key }}}, {{#list}}...{{/list}},
    and {{! comment }} (stripped via depth-counting scanner,_strip_comments).
    """
    template_text = _strip_comments(template_text)

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
                    # lambda replacement, not a raw string — a raw string
                    # gets scanned for regex backreferences (\1, \g<name>),
                    # which crashes on LaTeX/backslash-bearing content
                    # ("bad escape \m" for e.g. \mathcal{L}).
                    rendered = _re.sub(r'\{\{\{?\s*' + _re.escape(k) + r'\s*\}\}\}?', lambda m, v=v: str(v), rendered)
            else:
                rendered = _re.sub(r'\{\{\{?\s*\.\s*\}\}\}?', lambda m, item=item: str(item), rendered)
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

    for key, value in context.items():
        if isinstance(value, (dict, list)):
            continue
        text = str(value) if value is not None else ""
        # lambda replacement — see note above, avoids re interpreting
        # backslashes in `text` (LaTeX, Windows paths, etc.) as regex
        # backreferences.
        result = _re.sub(
            r'\{\{\{?\s*' + _re.escape(key) + r'\s*\}\}\}?',
            lambda m, text=text: text,
            result
        )
    return result


def parse_draft_to_context(sections):
    """Convert a list of {heading, text} sections into a flat key-value dict
    by converting headings to snake_case keys. If text is a JSON array
    (starts with '['), parse it as a list — enables structured data like
    references entries to survive the flat-text pipeline."""
    ctx = {}
    for s in sections:
        heading = s.get("heading", "")
        text = s.get("text", "")
        key = heading.lower().strip()
        key = _re.sub(r'[^a-z0-9]+', '_', key)
        key = key.strip('_')
        if key:
            # Detect JSON arrays — parse into list for template iteration
            if isinstance(text, str) and text.strip().startswith("["):
                try:
                    parsed = _json.loads(text)
                    if isinstance(parsed, list):
                        ctx[key] = parsed
                        continue
                except (_json.JSONDecodeError, ValueError):
                    pass
            ctx[key] = text
    return ctx


def get_final_structural_draft(academic_schema, conn, paper_id, domain):
    """Read a structural domain's most finished draft. `polish` (4e) is the
    true final stage for the 6 generated domains — falls back to
    `budget-fit` (4d) if polish hasn't run yet, then `cite`, since
    `references` never goes through 4a-4e at all (collate-references
    writes it once, at stage='cite', and nothing ever advances it further)."""
    for stage in ("polish", "budget-fit", "enrich", "cite", "generate"):
        draft = academic_schema.get_narrative(conn, paper_id, domain, stage=stage)
        if draft:
            return draft
    return None


def parse_cross_cutting(analysis_row):
    """Cross-cutting content lives in academic_cross_module_analysis (a
    single `content` blob per analysis_kind), not academic_narratives —
    wrap the blob as one block so the weaving loop can treat both uniformly."""
    if not analysis_row or not analysis_row.get("content"):
        return []
    return [{"heading": analysis_row["analysis_kind"].title(),
             "text": analysis_row["content"]}]


def _strip_evidence_markers(text):
    """Remove [evidence: ...] markers from rendered prose. These are
    internal grounding markers left by generation prompts (Rule 1) —
    already captured into academic_section_citations by the cite stage.
    Literature citations ([N]) have no prefix and are never stripped.
    Also consumes optional whitespace before the marker."""
    if isinstance(text, str):
        return _re.sub(r'\s*\[evidence:[^\]]+\]', '', text)
    return text


def _strip_evidence_from_context(ctx):
    """Recursively strip evidence markers from all string values in a
    template context dict (or list of dicts)."""
    if isinstance(ctx, dict):
        return {k: _strip_evidence_from_context(v) for k, v in ctx.items()}
    if isinstance(ctx, list):
        return [_strip_evidence_from_context(item) for item in ctx]
    if isinstance(ctx, str):
        return _strip_evidence_markers(ctx)
    return ctx


def _build_title_metadata_context(metadata_json):
    """Flatten academic_papers.metadata JSON into the shape
    templates/generation/markdown/title-and-metadata.md's
    {{#authors}}/{{#affiliations}}/{{#keywords}} loops expect.

    Template expects:
      authors: [{name, affiliation_number}]
      affiliations: [{number, name}]
      keywords: [str, ...]

    Yaml/DB metadata shape:
      authors: {authors: [{full_name, affiliation: <id>}]}
      affiliations: [{id, institution, department, city, state, country}]
    """
    m = _json.loads(metadata_json)
    aff_list = m.get("affiliations", [])
    aff_id_to_number = {a["id"]: i + 1 for i, a in enumerate(aff_list)}
    affiliations_ctx = [
        {"number": aff_id_to_number[a["id"]],
         "name": f'{a["institution"]}, {a["department"]}'}
        for a in aff_list
    ]
    authors_ctx = [
        {"name": a["full_name"],
         "affiliation_number": aff_id_to_number.get(a.get("affiliation"))}
        for a in m.get("authors", {}).get("authors", [])
    ]
    keywords_ctx = m.get("classification", {}).get("keywords", [])
    return {"authors": authors_ctx, "affiliations": affiliations_ctx,
            "keywords": keywords_ctx}


def build_domain_contexts(academic_schema, conn, paper_id, sections_order, cross_cutting):
    """Shared assembly logic: fetch each structural domain's draft, fetch
    cross-cutting content, weave cross-cutting into its target section's
    context. Strips [evidence: ...] markers from all rendered prose.
    Returns {domain_key: {template_key: text}}."""
    domain_contexts = {}
    for domain in sections_order:
        draft = get_final_structural_draft(academic_schema, conn, paper_id, domain)
        ctx = parse_draft_to_context(draft) if draft else {}
        # Strip [evidence: ...] markers — captured by cite stage, not for reader
        domain_contexts[domain] = _strip_evidence_from_context(ctx)

    # raw_markdown_html conversion: render **bold** → <strong>, *italic* → <em>
    # in reference entries for non-markdown output formats (HTML, DOCX, PDF).
    # Scoped to the two constructs confirmed in real citation data.
    refs = domain_contexts.get("references", {}).get("references", [])
    if refs:
        _BOLD_RE = _re.compile(r'\*\*(.+?)\*\*')
        _ITALIC_RE = _re.compile(r'\*(.+?)\*')
        for item in refs:
            raw = item.get("raw_markdown", "")
            html = _BOLD_RE.sub(r'<strong>\1</strong>', raw)
            html = _ITALIC_RE.sub(r'<em>\1</em>', html)
            item["raw_markdown_html"] = html

    cross_cutting_content = {}
    for cc_domain in cross_cutting:
        draft = academic_schema.get_narrative(conn, paper_id, cc_domain, stage="generate")
        if draft:
            cross_cutting_content[cc_domain] = draft
        else:
            analysis_row = academic_schema.get_cross_module_analysis(
                conn, paper_id, analysis_kind=cc_domain)
            cross_cutting_content[cc_domain] = parse_cross_cutting(analysis_row)

    for cc_domain, target_section in CROSS_CUTTING_TARGETS.items():
        if cc_domain in cross_cutting_content and cross_cutting_content[cc_domain]:
            blocks = cross_cutting_content[cc_domain]
            for block in blocks:
                key = target_section
                if key not in domain_contexts:
                    domain_contexts[key] = {}
                cc_key = f"cross_cutting_{cc_domain}_{block['heading'].lower().replace(' ', '_')}"
                domain_contexts[key][cc_key] = block["text"]

    # metadata merge: inject authors/affiliations/keywords from
    # academic_papers.metadata into title-and-metadata domain context.
    # These are static facts (human-authored in metadata.yaml), not
    # LLM-generated prose — injected at render time, not generation time.
    if "title-and-metadata" in domain_contexts:
        paper = academic_schema.get_paper(conn, paper_id)
        if paper and paper["metadata"] and paper["metadata"] != "{}":
            try:
                meta_ctx = _build_title_metadata_context(paper["metadata"])
                domain_contexts["title-and-metadata"].update(meta_ctx)
            except (_json.JSONDecodeError, KeyError, TypeError):
                pass  # If metadata is malformed, skip injection — don't crash the render

    # map-table injection: populate {{#table_map}} / {{#figure_map}} /
    # {{#equation_map}} / {{#algorithm_map}} template loops from the
    # extraction map tables so generation prompts can cite specific
    # evidence by map_key rather than guessing.
    _MAP_INJECTIONS = {
        "findings": [
            ("table_map", "table"),
            ("figure_map", "figure"),
        ],
        "methodology": [
            ("equation_map", "equation"),
            ("algorithm_map", "algorithm"),
        ],
    }
    for target_section, injections in _MAP_INJECTIONS.items():
        if target_section not in domain_contexts:
            continue
        for template_key, domain_kind in injections:
            entries = academic_schema.get_map(
                conn, paper_id, domain_kind, order_by="number")
            if entries:
                domain_contexts[target_section][template_key] = entries

    return domain_contexts
