import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
import academic_schema

# table/figure/equation share academic_schema's generic map-table helper
# (same dispatch persist_map_entries.py already uses) — real per-table
# columns (caption/figure_type/table_type/latex/explanation/...) come
# straight from the entry dict, never a hardcoded universal column list.
_GENERIC_MAP_KINDS = ("table", "figure", "equation")


def _extract_entries(row):
    """Pull the entries list out of the approved proposal's content_md or
    computed_context (whichever holds valid JSON with an 'entries' key)."""
    for key in ("content_md", "computed_context"):
        raw = row[key] if key in row.keys() else None
        if raw:
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, dict) and "entries" in parsed:
                    return parsed["entries"]
            except (json.JSONDecodeError, TypeError):
                continue
    return []


def _commit_citation_entries(conn, paper_id, entries):
    """academic_section_citations has no map_key/caption concept — it's
    (paper_id, domain_id, source_kind, citation). Step 0 extracts and
    commits citations without deciding which section they belong to —
    domain_id stays NULL here; a Step 1 assignment step fills it in
    (target_section, if the LLM still supplies it as a guess, is
    intentionally ignored at this stage — extraction, not drafting)."""
    committed = 0
    for entry in entries:
        conn.execute(
            "INSERT INTO academic_section_citations "
            "(paper_id, domain_id, source_kind, citation, created_at) "
            "VALUES (?, NULL, ?, ?, ?)",
            (paper_id, entry.get("source_kind", "literature"),
             entry.get("citation", ""), academic_schema.now_iso()),
        )
        committed += 1
    conn.commit()
    return committed


def _commit_generic_map_entries(conn, paper_id, map_kind, entries):
    """table/figure/equation share academic_schema's generic map-table
    helper. target_section is stripped here, not persisted — Step 0
    extracts, it doesn't decide which manuscript section an asset
    belongs in; a Step 1 assignment step fills target_section in later."""
    committed = 0
    for entry in entries:
        map_key = entry.get("map_key")
        if not map_key:
            continue
        cols = {k: v for k, v in entry.items() if k not in ("map_key", "target_section")}
        academic_schema.insert_map_entry(conn, paper_id, map_kind, map_key, **cols)
        committed += 1
    return committed


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    map_kind = payload["map_kind"]
    conn = academic_schema.get_conn(db_path)
    try:
        row = conn.execute(
            "SELECT content_md, computed_context FROM academic_proposal_review "
            "WHERE paper_id=? AND phase='map' AND map_kind=? AND is_latest=1 AND review_status='approved' "
            "ORDER BY id DESC LIMIT 1",
            (paper_id, map_kind),
        ).fetchone()
        if not row:
            write_envelope(out_path, status="error",
                           message=f"no approved {map_kind} map proposal found")
            return

        entries = _extract_entries(row)
        if not entries:
            write_envelope(out_path, status="error",
                           message=f"no map entries found in approved {map_kind} proposal")
            return

        if map_kind == "citation":
            committed = _commit_citation_entries(conn, paper_id, entries)
        elif map_kind in _GENERIC_MAP_KINDS:
            committed = _commit_generic_map_entries(conn, paper_id, map_kind, entries)
        else:
            write_envelope(out_path, status="error",
                           message=f"unknown map_kind: {map_kind}")
            return
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"committed {committed} {map_kind} map entries for paper {paper_id}")


if __name__ == "__main__":
    main()
