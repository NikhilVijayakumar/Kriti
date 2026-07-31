"""check_word_budget.py — generation-time completeness check for section-budget-fit.
Runs every text-evaluable rule from calculation/generation/{domain}.yaml
against the domain's enriched draft and reports itemized pass/fail results.

Expected --in payload: {paper_id: int, domain: str}
Also reads: calculation/generation/{domain}.yaml and
             calculation/report/summary/paper-budget.yaml
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys
import re
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
import academic_schema  # noqa: E402
import content_rules  # noqa: E402

# Pipeline-state rules that cannot be evaluated against text
_NON_TEXT_RULES = {"budget_fit_applied"}


def _word_count(text):
    return len(re.findall(r'\b\w+\b', text))


def _load_domain_rules(repo_root, domain):
    yaml_path = repo_root / "calculation" / "generation" / f"{domain}.yaml"
    if not yaml_path.exists():
        return None
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    return data.get("checks", [])


def _load_paper_budget(repo_root):
    yaml_path = repo_root / "calculation" / "report" / "summary" / "paper-budget.yaml"
    if not yaml_path.exists():
        return None
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    total = data.get("total_word_count", {})
    return total.get("min"), total.get("max")


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    domain = payload.get("domain", "")

    # Load domain rules
    checks = _load_domain_rules(repo_root, domain)
    if checks is None:
        write_envelope(out_path, status="error",
                       message=f"no rules found for {domain}")
        return

    # Filter to text-evaluable rules
    text_checks = [c for c in checks if c.get("rule", "") not in _NON_TEXT_RULES]

    if not text_checks:
        write_envelope(out_path, status="ok",
                       message=f"no text-evaluable checks for {domain}",
                       checks=[], missing=[])
        return

    conn = academic_schema.get_conn(db_path)
    try:
        # Get this domain's enriched draft
        narrative = academic_schema.get_narrative(conn, paper_id, domain, stage="enrich")
        if not narrative:
            write_envelope(out_path, status="error",
                           message=f"no enrich narrative found for {domain}")
            return

        sections = conn.execute(
            "SELECT text FROM academic_narrative_sections "
            "WHERE narrative_id=? ORDER BY sort_order",
            (narrative["id"],),
        ).fetchall()
        draft_text = "\n\n".join(s["text"] for s in sections)

        # Load other domains' drafts for cross-reference checks
        draft_texts = {}
        for other_domain in ("abstract", "results", "introduction", "conclusion"):
            other_narr = academic_schema.get_narrative(
                conn, paper_id, other_domain, stage="enrich")
            if other_narr:
                other_secs = conn.execute(
                    "SELECT text FROM academic_narrative_sections "
                    "WHERE narrative_id=? ORDER BY sort_order",
                    (other_narr["id"],),
                ).fetchall()
                draft_texts[other_domain] = "\n\n".join(
                    s["text"] for s in other_secs)

        # Run all text-evaluable rules
        check_results = []
        failed_checks = []
        for check in text_checks:
            passed, detail = content_rules.evaluate_rule(
                check, draft_text, draft_texts)
            entry = {
                "id": check.get("id", "unknown"),
                "name": check.get("name", check.get("rule", "unknown")),
                "passed": passed,
                "detail": detail,
            }
            check_results.append(entry)
            if not passed:
                failed_checks.append(entry)

        # Whole-paper word count
        paper_min, paper_max = _load_paper_budget(repo_root)
        total_wc = 0
        if paper_min is not None:
            all_narratives = conn.execute(
                "SELECT n.id FROM academic_narratives n "
                "JOIN academic_domains d ON d.id=n.domain_id "
                "WHERE n.paper_id=? AND n.stage='budget-fit'",
                (paper_id,),
            ).fetchall()
            for (nid,) in all_narratives:
                secs = conn.execute(
                    "SELECT text FROM academic_narrative_sections "
                    "WHERE narrative_id=? ORDER BY sort_order",
                    (nid,),
                ).fetchall()
                total_wc += _word_count(" ".join(s["text"] for s in secs))
            total_wc += _word_count(draft_text)

        all_passed = len(failed_checks) == 0
        message = ("; ".join(f"{c['name']}: {c['detail']}"
                             for c in failed_checks)
                   or "all checks passed")

        write_envelope(out_path,
                       status="ok" if all_passed else "error",
                       message=message,
                       paper_id=paper_id, domain=domain,
                       checks=check_results,
                       missing=[c["name"] for c in failed_checks],
                       total_word_count=total_wc if paper_min else None)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
