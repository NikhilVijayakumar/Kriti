"""scaffold.py — Generates document stubs from templates.

Reads templates/generation/document/{domain}.md for document-level structure,
and templates/generation/section/{domain}/*.md for per-section stubs.
Creates the output document with all headings already in place.

Usage:
  python scaffold.py --system-root <path> --domain <domain> --out <path>
  python scaffold.py --system-root <path> --domain <domain> --out <path> --context-dir <path>
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from _common import load_yaml, read_text, write_text, find_md_files


# ---------------------------------------------------------------------------
# Template parsing
# ---------------------------------------------------------------------------

def parse_document_template(template_content: str) -> dict[str, Any]:
    """Parse a document template into structured data.

    Extracts: domain metadata, required sections table, section definitions
    (template text, examples, writing guidance).
    """
    sections: list[dict[str, str]] = []
    current_section: dict[str, str] | None = None
    current_content_lines: list[str] = []

    for line in template_content.split("\n"):
        # Detect section headers (### level within the template)
        section_match = re.match(r"^###\s+(\d+)\.\s+(.+)$", line)
        if section_match:
            if current_section is not None:
                current_section["content"] = "\n".join(current_content_lines).strip()
                sections.append(current_section)
            current_section = {
                "number": section_match.group(1),
                "title": section_match.group(2),
            }
            current_content_lines = []
        elif current_section is not None:
            current_content_lines.append(line)

    if current_section is not None:
        current_section["content"] = "\n".join(current_content_lines).strip()
        sections.append(current_section)

    return {"sections": sections}


def extract_section_heading(template_content: str) -> str | None:
    """Extract the first markdown heading from a section template."""
    for line in template_content.split("\n"):
        match = re.match(r"^#+\s+(.+)$", line)
        if match:
            return match.group(1).strip()
    return None


def extract_template_skeleton(template_content: str) -> str:
    """Extract the 'Template' block from a section template.

    Looks for content between '## Template' and the next '##' heading.
    """
    lines = template_content.split("\n")
    in_template = False
    skeleton_lines: list[str] = []

    for line in lines:
        if re.match(r"^## Template", line, re.IGNORECASE):
            in_template = True
            continue
        if in_template and re.match(r"^## ", line):
            break
        if in_template:
            skeleton_lines.append(line)

    return "\n".join(skeleton_lines).strip()


# ---------------------------------------------------------------------------
# Context loading
# ---------------------------------------------------------------------------

def load_upstream_context(context_dir: Path, completed_domains: list[str]) -> dict[str, str]:
    """Load completed upstream domain documents as context for generation.

    Returns a dict mapping domain name to document content.
    """
    context: dict[str, str] = {}
    for domain in completed_domains:
        # Look for the domain file in context dir
        for md_file in context_dir.glob(f"{domain}*.md"):
            if md_file.is_file():
                context[domain] = md_file.read_text(encoding="utf-8")
                break
    return context


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def generate_document(
    system_root: Path,
    domain: str,
    context: dict[str, str] | None = None,
) -> str:
    """Generate a document stub for a domain from its templates.

    Returns the generated markdown content.
    """
    template_dir = system_root / "templates" / "generation"
    doc_dir = template_dir / "document"

    # Discover template files — names use prefixed format like "01-vision.md"
    doc_template_path = doc_dir / f"{domain}.md"
    if not doc_template_path.exists():
        # Glob for "*-{domain}.md" pattern
        matches = list(doc_dir.glob(f"*-{domain}.md"))
        if matches:
            doc_template_path = matches[0]
        else:
            raise FileNotFoundError(
                f"Document template not found: {doc_dir}/{{*,}}{domain}.md"
            )

    section_dir = template_dir / "section" / domain
    if not section_dir.is_dir():
        # Glob for "*-{domain}" pattern
        matches = list((template_dir / "section").glob(f"*-{domain}"))
        if matches and matches[0].is_dir():
            section_dir = matches[0]

    doc_template = read_text(doc_template_path)
    parsed = parse_document_template(doc_template)

    # Build the output document
    output_lines: list[str] = []

    # Domain header
    output_lines.append(f"# {domain.split('-', 1)[-1].replace('-', ' ').title()} Documentation")
    output_lines.append("")
    output_lines.append(f"> Auto-generated scaffold for `{domain}`. "
                        "Fill in each section with content derived from upstream domains.")
    output_lines.append("")

    # Add context summary if available
    if context:
        output_lines.append("## Upstream Context")
        output_lines.append("")
        for ctx_domain, ctx_content in context.items():
            # Extract first meaningful paragraph from context
            first_para = _extract_first_paragraph(ctx_content)
            if first_para:
                output_lines.append(f"**{ctx_domain}:** {first_para}")
                output_lines.append("")
        output_lines.append("---")
        output_lines.append("")

    # Add section stubs
    if section_dir.is_dir():
        section_files = sorted(section_dir.glob("*.md"))
        for sec_file in section_files:
            sec_content = read_text(sec_file)
            skeleton = extract_template_skeleton(sec_content)
            heading = extract_section_heading(sec_content)

            if heading:
                output_lines.append(f"## {heading}")
            else:
                # Fallback: use filename as heading
                title = sec_file.stem.replace("-", " ").replace("_", " ")
                # Remove leading number if present
                title = re.sub(r"^\d+\s+", "", title)
                output_lines.append(f"## {title.title()}")

            output_lines.append("")

            if skeleton:
                output_lines.append(skeleton)
            else:
                output_lines.append(f"<!-- TODO: Fill in {domain}/{sec_file.stem} -->")

            output_lines.append("")
    else:
        # No section templates — use document template sections
        for sec in parsed["sections"]:
            output_lines.append(f"## {sec['title']}")
            output_lines.append("")
            output_lines.append(f"<!-- TODO: Fill in {domain} {sec['title']} -->")
            output_lines.append("")

    return "\n".join(output_lines)


def _extract_first_paragraph(content: str) -> str:
    """Extract the first non-heading, non-empty paragraph from markdown."""
    lines = content.split("\n")
    in_paragraph = False
    para_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_paragraph:
                break
            continue
        if stripped.startswith("#"):
            if in_paragraph:
                break
            continue
        if stripped.startswith(">"):
            continue
        if stripped.startswith("---"):
            continue

        in_paragraph = True
        para_lines.append(stripped)

    return " ".join(para_lines)[:200]  # Cap at 200 chars


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate document scaffold from templates")
    parser.add_argument("--system-root", required=True, help="Path to system directory")
    parser.add_argument("--domain", required=True, help="Domain name (e.g. 01-vision)")
    parser.add_argument("--out", required=True, help="Output file path")
    parser.add_argument("--context-dir", help="Directory with completed upstream documents")
    parser.add_argument("--completed-domains", nargs="*", default=[],
                        help="List of completed upstream domain names")
    args = parser.parse_args()

    system_root = Path(args.system_root)
    if not system_root.is_dir():
        print(f"Error: system-root not found: {system_root}", file=sys.stderr)
        sys.exit(1)

    context = None
    if args.context_dir and args.completed_domains:
        context = load_upstream_context(Path(args.context_dir), args.completed_domains)

    try:
        content = generate_document(system_root, args.domain, context)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    write_text(Path(args.out), content)
    print(f"Scaffold written to {args.out}")


if __name__ == "__main__":
    main()
