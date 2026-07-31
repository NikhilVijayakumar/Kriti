"""check_evidence_resolves.py — step 2 of verify-step0-claims.
Deterministic check: does source_evidence point at a file that exists on disk?

Expected --in: {paper_id: int, rows: [{table_name, row_id, source_evidence, ...}]}
Output: {findings: [{table_name, row_id, check_kind, verdict, evidence_note}]}
"""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope


def _repo_path(repo_root, evidence_path):
    if not evidence_path:
        return None
    p = Path(evidence_path)
    if p.is_absolute():
        return str(p) if p.exists() else None
    full = Path(repo_root) / evidence_path
    return str(full) if full.exists() else None


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    rows = payload.get("rows", [])
    findings = []
    for r in rows:
        evidence = r.get("source_evidence", "")
        resolved = _repo_path(repo_root, evidence)
        findings.append({
            "table_name": r["table_name"],
            "row_id": r["row_id"],
            "check_kind": "evidence-resolves",
            "verdict": "PASS" if resolved else "FAIL",
            "evidence_note": f"source_evidence='{evidence}' → {'found' if resolved else 'NOT FOUND'}",
        })
    write_envelope(out_path, status="ok",
                   message=f"checked {len(findings)} evidence paths",
                   findings=findings)


if __name__ == "__main__":
    main()
