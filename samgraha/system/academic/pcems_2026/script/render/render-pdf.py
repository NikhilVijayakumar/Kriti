"""render-pdf.py — converts assembled HTML to PDF via Playwright.

Opens the HTML in a headless Chromium browser and uses page.pdf() to
produce an A4 PDF. Adapted from the hackathon's export_team_pdfs.py
precedent.

Expected --in payload: {html_path: str}
"""
import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent
                        / "base_academic" / "script" / "common"))
from _adapter import parse_step_args, write_envelope


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    html_path = _Path(payload["html_path"])

    if not html_path.is_file():
        write_envelope(out_path, status="error",
                       message=f"HTML file not found: {html_path}")
        return

    pdf_path = html_path.with_suffix(".pdf")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        write_envelope(out_path, status="error",
                       message="playwright not installed — pip install playwright && playwright install chromium")
        return

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            file_url = "file:///" + str(html_path.resolve()).replace("\\", "/")
            page.goto(file_url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(1000)  # let fonts/images settle

            page.pdf(
                path=str(pdf_path),
                format="A4",
                print_background=True,
                margin={"top": "16mm", "bottom": "16mm",
                        "left": "12mm", "right": "12mm"},
            )
            browser.close()
    except Exception as e:
        write_envelope(out_path, status="error",
                       message=f"playwright PDF failed: {e}")
        return

    write_envelope(
        out_path, status="ok",
        message=f"rendered PDF: {pdf_path.name}",
        pdf_path=str(pdf_path),
    )


if __name__ == "__main__":
    main()
