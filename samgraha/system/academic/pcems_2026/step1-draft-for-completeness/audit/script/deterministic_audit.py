"""deterministic_audit.py — runs deterministic mechanical checks against a
domain's draft, per calculation/generation/{domain}.yaml rules.
Records findings in academic_deterministic_findings.
"""
import os
import sys
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
import academic_schema  # noqa: E402
import content_rules  # noqa: E402

GENERATION_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "..", "..", "calculation", "generation")


def _load_rules(domain_key):
    yaml_path = os.path.join(GENERATION_DIR, f"{domain_key}.yaml")
    if not os.path.isfile(yaml_path):
        return None, f"rules not found: {yaml_path}"
    try:
        import yaml
    except ImportError:
        return None, "pyyaml not installed"
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f), None


def _get_domain_draft(conn, paper_id, domain_key):
    domain_id = academic_schema.get_domain_id(conn, domain_key)
    if domain_id is None:
        return None
    row = conn.execute(
        "SELECT id FROM academic_narratives "
        "WHERE paper_id=? AND domain_id=? ORDER BY iteration DESC LIMIT 1",
        (paper_id, domain_id),
    ).fetchone()
    if not row:
        return None
    sections = conn.execute(
        "SELECT heading, text FROM academic_narrative_sections "
        "WHERE narrative_id=? ORDER BY sort_order",
        (row["id"],),
    ).fetchall()
    return "\n\n".join(f"## {s['heading']}\n\n{s['text']}" for s in sections)


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload.get("paper_id")
    domain_key = payload.get("domain")
    commit_sha = payload.get("commit_sha", "")

    if not paper_id or not domain_key:
        write_envelope(out_path, status="error",
                       message="missing paper_id or domain in input")
        return

    rules, err = _load_rules(domain_key)
    if err:
        write_envelope(out_path, status="error", message=err)
        return

    checks = rules.get("checks", []) if rules else []
    if not checks:
        write_envelope(out_path, status="ok",
                       message=f"no deterministic checks defined for {domain_key}",
                       verdict="PASS", findings=[])
        return

    conn = academic_schema.get_conn(db_path)
    try:
        draft_text = _get_domain_draft(conn, paper_id, domain_key)
        if not draft_text:
            write_envelope(out_path, status="error",
                           message=f"no draft found for {domain_key}")
            return

        draft_texts = {}
        for other_domain in ("abstract", "results", "introduction", "conclusion"):
            other_text = _get_domain_draft(conn, paper_id, other_domain)
            if other_text:
                draft_texts[other_domain] = other_text

        findings = []
        all_passed = True
        for check in checks:
            passed, detail = content_rules.evaluate_rule(
                check, draft_text, draft_texts)
            findings.append({
                "check_id": check.get("id", "unknown"),
                "rule": check.get("rule", "unknown"),
                "passed": passed,
                "detail": detail,
                "severity": check.get("severity", "warning"),
            })
            if not passed and check.get("severity") in ("critical", "error"):
                all_passed = False

        verdict = "PASS" if all_passed else "FAIL"

        academic_schema.record_deterministic_findings(
            conn, paper_id, domain_key, verdict, findings,
            commit_sha=commit_sha
        )

        write_envelope(out_path, status="ok",
                       message=f"deterministic audit {domain_key}: {verdict}",
                       verdict=verdict, findings=findings)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
