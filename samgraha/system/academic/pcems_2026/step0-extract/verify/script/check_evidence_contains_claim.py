"""check_evidence_contains_claim.py — step 3 of verify-step0-claims.
Deterministic check: does the evidence file's content contain anything
resembling the claim? Crude substring match against key terms.

Expected --in: {paper_id: int, rows: [{table_name, row_id, source_evidence, relevance_note, ...}]}
Output: {findings: [{table_name, row_id, check_kind, verdict, evidence_note}]}
"""
import os
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope


def _read_file(repo_root, evidence_path, max_bytes=4096):
    if not evidence_path:
        return ""
    p = Path(evidence_path)
    if not p.is_absolute():
        p = Path(repo_root) / evidence_path
    if not p.exists():
        return ""
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read(max_bytes)
    except Exception:
        return ""


def _key_terms(text):
    """Extract meaningful key terms from a relevance note / claim text."""
    words = re.findall(r'[a-zA-Z][a-zA-Z]{2,}', text)
    stopwords = {"the", "and", "for", "this", "that", "with", "from",
                 "what", "which", "their", "than", "about", "were",
                 "been", "have", "has", "had", "does", "will", "can",
                 "its", "also", "into", "over", "such", "only", "other",
                 "more", "some", "these", "those", "very", "just", "not"}
    return [w.lower() for w in words if w.lower() not in stopwords][:10]


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    rows = payload.get("rows", [])
    repo_root_str = str(repo_root)
    findings = []
    for r in rows:
        evidence = r.get("source_evidence", "")
        note = r.get("relevance_note", "")
        content = _read_file(repo_root_str, evidence)
        if not content:
            findings.append({
                "table_name": r["table_name"],
                "row_id": r["row_id"],
                "check_kind": "evidence-contains-claim",
                "verdict": "FAIL",
                "evidence_note": "evidence file not found or empty — cannot verify claim content",
            })
            continue
        terms = _key_terms(note) if note else []
        if not terms:
            findings.append({
                "table_name": r["table_name"],
                "row_id": r["row_id"],
                "check_kind": "evidence-contains-claim",
                "verdict": "PASS",
                "evidence_note": "no relevance_note — skipping content check",
            })
            continue
        matches = [t for t in terms if t in content.lower()]
        ratio = len(matches) / len(terms)
        findings.append({
            "table_name": r["table_name"],
            "row_id": r["row_id"],
            "check_kind": "evidence-contains-claim",
            "verdict": "PASS" if ratio >= 0.3 else "FAIL",
            "evidence_note": f"{len(matches)}/{len(terms)} key terms found in evidence file (threshold 30%)",
        })
    write_envelope(out_path, status="ok",
                   message=f"checked {len(findings)} claims against evidence",
                   findings=findings)


if __name__ == "__main__":
    main()
