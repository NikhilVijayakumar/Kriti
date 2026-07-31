"""extract-mermaid-images.py - rasterizes inline mermaid diagrams in an HTML
document to PNG images and replaces the <pre class="mermaid"> blocks with
<img> tags.

Uses npx @mermaid-js/mermaid-cli (mmdc) for rendering. Creates an output
directory for images next to the HTML file.

Expected --in payload: {html_path: str}
Output: modified HTML with mermaid blocks replaced by <img> references,
        PNG images in a sibling directory.

Rendering helpers (find_mmdc, render_mmdc) imported from script/common/mermaid.py
so generate_mermaid_figure.py can reuse them without duplication.
"""
import re as _re
import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope
from mermaid import find_mmdc, render_mmdc


def _extract_mermaid_blocks(html):
    """Extract mermaid diagram definitions from <pre class="mermaid"> blocks."""
    pattern = r'<pre\s+class="mermaid">(.*?)</pre>'
    return _re.findall(pattern, html, _re.DOTALL | _re.IGNORECASE)


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    html_path = _Path(payload["html_path"])

    if not html_path.is_file():
        write_envelope(out_path, status="error",
                       message=f"HTML file not found: {html_path}")
        return

    html_content = html_path.read_text(encoding="utf-8")
    mermaid_blocks = _extract_mermaid_blocks(html_content)

    if not mermaid_blocks:
        write_envelope(out_path, status="ok",
                       message="no mermaid blocks found",
                       diagrams_rendered=0, html_path=str(html_path))
        return

    # Create images directory
    images_dir = html_path.parent / "images"
    images_dir.mkdir(exist_ok=True)

    rendered_count = 0

    for i, block in enumerate(mermaid_blocks):
        img_name = f"diagram_{i+1}.png"
        img_path = images_dir / img_name

        if render_mmdc(block.strip(), img_path):
            # Replace the <pre> block with an <img> tag
            escaped_block = _re.escape(block)
            replacement = (
                f'<figure class="mermaid-figure">\n'
                f'  <img src="images/{img_name}" alt="Diagram {i+1}" '
                f'loading="lazy">\n'
                f'</figure>'
            )
            html_content = _re.sub(
                rf'<pre\s+class="mermaid">{escaped_block}</pre>',
                replacement, html_content, count=1,
                flags=_re.DOTALL | _re.IGNORECASE
            )
            rendered_count += 1

    # Overwrite html_path in place (this step modifies the assembled
    # document, it doesn't produce a separate artifact) - out_path is
    # reserved for the status envelope, same split assemble-final-
    # document.py uses, for the same reason (write_envelope would
    # otherwise clobber it).
    html_path.write_text(html_content, encoding="utf-8")

    write_envelope(
        out_path, status="ok",
        message=f"rendered {rendered_count}/{len(mermaid_blocks)} mermaid diagrams",
        diagrams_rendered=rendered_count,
        diagrams_total=len(mermaid_blocks),
        images_dir=str(images_dir),
        html_path=str(html_path),
    )


if __name__ == "__main__":
    main()
