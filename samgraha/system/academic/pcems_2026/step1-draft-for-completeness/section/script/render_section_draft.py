import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
import academic_schema

_DOMAIN_ORDER = [
    "title-and-metadata", "introduction", "methodology",
    "findings", "conclusion", "references",
]

def _domain_sort(conn, domain_key):
    row = conn.execute(
        "SELECT id, sort_order FROM academic_domains WHERE key=?",
        (domain_key,)).fetchone()
    return (row["id"], row["sort_order"]) if row else (None, 99)


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    conn = academic_schema.get_conn(db_path)
    written = []
    try:
        paper = conn.execute(
            "SELECT title FROM academic_papers WHERE id=?",
            (paper_id,)).fetchone()
        paper_title = paper["title"] if paper else "untitled"

        output_dir = os.path.join(
            str(repo_root), ".samgraha", "output",
            "step1-draft-for-completeness", "sections",
            f"paper-{paper_id}")
        os.makedirs(output_dir, exist_ok=True)

        for domain in _DOMAIN_ORDER:
            sections = academic_schema.get_narrative(conn, paper_id, domain)
            if not sections:
                continue

            domain_id, sort_order = _domain_sort(conn, domain)

            lines = []
            lines.append(f"# {domain}")
            lines.append("")
            for s in sections:
                if s["heading"]:
                    lines.append(f"## {s['heading']}")
                    lines.append("")
                if s["text"]:
                    lines.append(s["text"])
                    lines.append("")

            out_file = os.path.join(
                output_dir, f"{sort_order:02d}-{domain}.md")
            with open(out_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            written.append(out_file)

            # Insert tracking row with scope_domain_id
            rel_path = os.path.relpath(out_file, str(repo_root))
            academic_schema.record_report(
                conn, paper_id, "markdown", rel_path,
                report_kind="section-draft",
                scope_domain_id=domain_id,
            )
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"rendered {len(written)} section drafts for paper {paper_id}",
                   written=written)

if __name__ == "__main__":
    main()
