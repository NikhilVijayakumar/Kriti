"""render-docx.py — converts assembled HTML to DOCX via pandoc.

Wraps the pandoc CLI to produce a .docx file from the assembled HTML
document. Uses pandoc's built-in HTML-to-DOCX conversion with reference
doc support if a .docx template is provided.

Expected --in payload: {html_path: str, reference_docx: str (optional)}
"""
import shutil
import subprocess
import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope

# Default reference doc — Arial font hierarchy per the official template
# spec (reference/template/extracted/Template_PCEMS2026.txt), built by
# generate_reference_docx.py. Without this, pandoc's default DOCX styles
# use Calibri, not the template's required Arial 14/12/12/11pt hierarchy.
DEFAULT_REFERENCE_DOCX = (_Path(__file__).resolve().parent.parent
                          / "reference" / "template"
                          / "Template_PCEMS2026_reference.docx")


def _find_pandoc():
    on_path = shutil.which("pandoc")
    if on_path:
        return on_path
    # Fall back to pypandoc-binary's bundled pandoc (requirements.txt) —
    # no system-level pandoc install needed.
    try:
        import pypandoc
        return pypandoc.get_pandoc_path()
    except (ImportError, OSError):
        return None


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    html_path = _Path(payload["html_path"])

    if not html_path.is_file():
        write_envelope(out_path, status="error",
                       message=f"HTML file not found: {html_path}")
        return

    pandoc = _find_pandoc()
    if not pandoc:
        write_envelope(out_path, status="error",
                       message="pandoc not found in PATH — install from https://pandoc.org/installing.html")
        return

    docx_path = html_path.with_suffix(".docx")

    cmd = [pandoc, str(html_path), "-o", str(docx_path),
           "--from", "html", "--to", "docx"]

    # Reference doc for custom styles — explicit payload override, else
    # the template's own Arial style set.
    ref_doc = payload.get("reference_docx") or str(DEFAULT_REFERENCE_DOCX)
    if ref_doc and _Path(ref_doc).is_file():
        cmd.extend(["--reference-doc", ref_doc])

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    if result.returncode != 0:
        write_envelope(out_path, status="error",
                       message=f"pandoc failed: {result.stderr[:500]}",
                       pandoc_stderr=result.stderr[:2000])
        return

    write_envelope(
        out_path, status="ok",
        message=f"rendered DOCX: {docx_path.name}",
        docx_path=str(docx_path),
    )


if __name__ == "__main__":
    main()
