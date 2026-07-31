"""persist_claim_findings.py — step 6 of verify-step0-claims.
Writes verification findings to academic_step0_claim_findings.
Multi-model fan-out: when models: [str] is provided, writes one row per
(claim, check_kind, model) — not one row overwritten by the last model.

Expected --in: {paper_id: int, module_id: int (nullable),
                 models: [str] (optional, default ["default"]),
                 findings: [{table_name, row_id, check_kind, verdict, evidence_note}]}
Output: {written: int}
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope
import academic_schema
from academic_schema import now_iso


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    module_id = payload.get("module_id")
    models = payload.get("models", ["default"])
    findings = payload.get("findings", [])
    conn = academic_schema.get_conn(db_path)
    ts = now_iso()
    written = 0
    try:
        for model in models:
            for f in findings:
                conn.execute(
                    "INSERT OR REPLACE INTO academic_step0_claim_findings "
                    "(paper_id, module_id, table_name, row_id, check_kind, model, verdict, evidence_note, created_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (paper_id, module_id, f["table_name"], f["row_id"],
                     f["check_kind"], model, f["verdict"], f.get("evidence_note", ""), ts))
                written += 1
        conn.commit()
    finally:
        conn.close()
    write_envelope(out_path, status="ok",
                   message=f"persisted {written} claim findings across {len(models)} model(s)",
                   paper_id=paper_id, written=written)


if __name__ == "__main__":
    main()
