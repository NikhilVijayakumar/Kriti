"""persist_keyword_map.py — det step, third in build-keyword-map chain.

Parses the semantic step's output (a markdown document with keyword blocks)
and persists each (module_id, keyword) pair to academic_keyword_map.

Expected --in payload:
  {paper_id: int, module_id: int, keyword_blocks: list[
    {keyword: str, relevance_note: str, source_evidence: str, candidate: bool}
  ]}
"""
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "script"))
from _adapter import parse_step_args, write_envelope  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "script"))
import academic_schema  # noqa: E402


def _parse_keyword_blocks(markdown_text):
    """Parse keyword blocks from the semantic step's markdown output.

    Expected format:
    ### Keyword: `<keyword>`
    - **relevance_note:** <text>
    - **source_evidence:** <text>
    - **candidate:** <true/false>
    """
    blocks = []
    pattern = re.compile(
        r"### Keyword:\s*`(.+?)`\s*\n"
        r"(.*?)(?=\n###\s|\Z)",
        re.DOTALL,
    )
    for match in pattern.finditer(markdown_text):
        keyword = match.group(1).strip()
        body = match.group(2)
        relevance_note = ""
        source_evidence = ""
        candidate = False
        for line in body.split("\n"):
            line = line.strip()
            if line.startswith("- **relevance_note:**"):
                relevance_note = line.split(":", 1)[1].strip().strip("**").strip()
            elif line.startswith("- **source_evidence:**"):
                source_evidence = line.split(":", 1)[1].strip().strip("**").strip()
            elif line.startswith("- **candidate:**"):
                val = line.split(":", 1)[1].strip().lower()
                candidate = val == "true"
        if keyword:
            blocks.append({
                "keyword": keyword,
                "relevance_note": relevance_note,
                "source_evidence": source_evidence,
                "candidate": candidate,
            })
    return blocks


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    module_id = payload.get("module_id")

    # Support both pre-parsed blocks and raw markdown
    keyword_blocks = payload.get("keyword_blocks")
    if keyword_blocks is None:
        raw = payload.get("content_md", "")
        keyword_blocks = _parse_keyword_blocks(raw)

    conn = academic_schema.get_conn(db_path)
    try:
        persisted = []
        for block in keyword_blocks:
            row_id = academic_schema.upsert_keyword_map(
                conn, paper_id, module_id,
                block["keyword"],
                relevance_note=block.get("relevance_note", ""),
                source_evidence=block.get("source_evidence", ""),
            )
            persisted.append({"keyword": block["keyword"], "row_id": row_id})

        msg = f"persisted {len(persisted)} keyword_map rows for module_id={module_id}"
    finally:
        conn.close()

    write_envelope(out_path, status="ok", message=msg,
                   persisted=persisted)


if __name__ == "__main__":
    main()
