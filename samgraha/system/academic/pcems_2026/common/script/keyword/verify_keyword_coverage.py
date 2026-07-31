"""verify_keyword_coverage.py — det step, fourth in build-keyword-map chain.

Compares academic_keyword_map's discovered keywords against the paper's
declared classification.keywords.  Flags two categories:
1. gaps — declared keywords never found in any module
2. candidates — keywords strongly supported by module evidence but not in
   the declared set (surfaced for human review).

Expected --in payload:
  {paper_id: int}
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "script"))
from _adapter import parse_step_args, write_envelope  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "script"))
import academic_schema  # noqa: E402


def _get_declared_keywords(conn, paper_id):
    """Read declared keywords from academic_papers.metadata."""
    paper = academic_schema.get_paper(conn, paper_id)
    if not paper or not paper["metadata"]:
        return []
    try:
        meta = json.loads(paper["metadata"])
        return (
            meta.get("classification", {}).get("keywords", [])
            or meta.get("keywords", [])
        )
    except (json.JSONDecodeError, TypeError):
        return []


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]

    conn = academic_schema.get_conn(db_path)
    try:
        declared = _get_declared_keywords(conn, paper_id)
        result = academic_schema.verify_keyword_coverage(conn, paper_id, declared)
        verdict = "ok"
        gaps = result["gaps"]
        candidates = result["candidates"]
        lines = []
        if gaps:
            lines.append(f"GAPS ({len(gaps)}): {', '.join(gaps)}")
            verdict = "warning"
        if candidates:
            lines.append(f"CANDIDATES ({len(candidates)}): {', '.join(candidates)}")
            if verdict == "ok":
                verdict = "info"
        if not lines:
            lines.append("all declared keywords covered, no unexpected candidates")
        message = "; ".join(lines)
    finally:
        conn.close()

    write_envelope(out_path, status=verdict, message=message,
                   keyword_coverage=result)


if __name__ == "__main__":
    main()
