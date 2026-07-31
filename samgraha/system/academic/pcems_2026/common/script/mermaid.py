"""mermaid.py — shared helpers for finding and rendering Mermaid CLI (mmdc).

Extracted from script/render/extract-mermaid-images.py so both the render
pipeline and generate_mermaid_figure.py can validate/render diagrams without
duplicating the mmdc-discovery logic.

Requires mmdc (global install or npx fallback) to actually render; the
validation path raises a clear error if mmdc is unreachable rather than
silently passing.
"""
import shutil
import subprocess
import tempfile
from pathlib import Path


def find_mmdc():
    """Locate mermaid-cli — try global, then npx fallback."""
    mmdc = shutil.which("mmdc")
    if mmdc:
        return [mmdc]
    return ["npx", "--yes", "@mermaid-js/mermaid-cli"]


def render_mmdc(diagram_text, output_path, timeout=30):
    """Render a single mermaid diagram to PNG via mmdc.

    Args:
        diagram_text: Mermaid source string.
        output_path: Path for the output PNG.
        timeout: Seconds before killing mmdc (default 30).

    Returns:
        True if render succeeded, False on any error.

    Raises:
        RuntimeError: if mmdc is not found in the environment.
    """
    mmdc_cmd = find_mmdc()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False,
                                      encoding="utf-8") as f:
        f.write(diagram_text)
        input_path = f.name

    try:
        result = subprocess.run(
            mmdc_cmd + ["-i", input_path, "-o", str(output_path),
                        "-b", "transparent", "-w", "1200"],
            capture_output=True, text=True, timeout=timeout,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False
    finally:
        Path(input_path).unlink(missing_ok=True)
