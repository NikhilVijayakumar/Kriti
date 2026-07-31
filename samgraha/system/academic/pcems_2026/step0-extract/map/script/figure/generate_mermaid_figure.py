"""generate_mermaid_figure.py — validate and persist Mermaid source for
figure_map rows that need figure generation (architecture_diagram,
flowchart, concept_illustration with no existing asset_path).

This is the **deterministic persist step** in the 3d-generate-figure-assets
usecase chain:
  1. gather-flagged-figures (deterministic) — find rows needing generation
  2. generate-mermaid-source (semantic, prompt/generation/figure-mermaid.md)
     — LLM produces mermaid_source + caption for each row
  3. validate-and-persist-mermaid (deterministic, this script)
     — validates via render_mmdc, persists to DB

Idempotent: skips rows where mermaid_source is already non-null.
--force flag in payload regenerates.
"""
import json as _json
import sys
import tempfile
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent.parent / "common" / "script"))
import academic_schema
from mermaid import find_mmdc, render_mmdc

MERMAID_TYPES = ("architecture_diagram", "flowchart", "concept_illustration")


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    import sqlite3
    conn = academic_schema.get_conn(db_path=db_path)
    conn.row_factory = sqlite3.Row

    paper_id = payload.get("paper_id")
    force = payload.get("force", False)

    if not paper_id:
        write_envelope(out_path, status="error",
                       message="paper_id required in payload")
        conn.close()
        return

    # Gather rows: flagged (no asset, no mermaid) unless --force
    if force:
        rows = conn.execute(
            "SELECT * FROM academic_figure_map "
            "WHERE paper_id=? AND figure_type IN (?, ?, ?)",
            (paper_id,) + MERMAID_TYPES,
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM academic_figure_map "
            "WHERE paper_id=? AND figure_type IN (?, ?, ?) "
            "AND asset_path IS NULL "
            "AND (mermaid_source IS NULL OR mermaid_source = '')",
            (paper_id,) + MERMAID_TYPES,
        ).fetchall()

    if not rows:
        write_envelope(out_path, status="ok",
                       message="no mermaid-eligible rows to process",
                       paper_id=paper_id, rows_checked=0)
        conn.close()
        return

    processed = 0
    validated = 0
    failed = 0

    # Each row carries mermaid_source from the prior semantic step.
    # The semantic step writes mermaid_source directly to the row obj
    # via the prompt — but prompt outputs are  passed in the payload.
    # We support both: payload-level entries override DB values.
    payload_entries = {
        e["map_key"]: e.get("mermaid_source", "")
        for e in payload.get("entries", [])
    }

    for row in rows:
        map_key = row["map_key"]
        row_id = row["id"]

        src = payload_entries.get(map_key)
        if not src:
            src = row.get("mermaid_source")
        if not src:
            continue

        processed += 1

        # Validate via real mmdc render to a temp file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = _Path(tmp.name)

        try:
            ok = render_mmdc(src, tmp_path, timeout=15)
        except RuntimeError as exc:
            ok = False
        finally:
            tmp_path.unlink(missing_ok=True)

        if not ok:
            failed += 1
            continue

        # Persist mermaid_source
        conn.execute(
            "UPDATE academic_figure_map SET mermaid_source=? WHERE id=?",
            (src, row_id),
        )
        validated += 1

    conn.commit()
    conn.close()

    write_envelope(out_path, status="ok",
                   message=f"validated and persisted {validated}/{processed} "
                           f"mermaid figures ({failed} failed render) "
                           f"for paper {paper_id}",
                   paper_id=paper_id,
                   rows_checked=len(rows),
                   processed=processed,
                   validated=validated,
                   failed=failed)


if __name__ == "__main__":
    main()
