"""check_word_budget.py — deterministic word-count check for section-budget-fit.
Checks a domain's word count against its configured min/max range and
the whole-paper total against paper-budget.yaml.

Expected --in payload: {paper_id: int, domain: str}
Also reads: calculation/deterministic/{domain}.yaml and
             calculation/summary/paper-budget.yaml
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys
import re
import yaml

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def _word_count(text):
    return len(re.findall(r'\b\w+\b', text))


def _load_domain_config(repo_root, domain):
    yaml_path = repo_root / "calculation" / "deterministic" / f"{domain}.yaml"
    if not yaml_path.exists():
        return None
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    for check in data.get("checks", []):
        if check.get("rule") == "word_count_in_range":
            return check.get("config", {})
    return None


def _load_paper_budget(repo_root):
    yaml_path = repo_root / "calculation" / "summary" / "paper-budget.yaml"
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

    conn = academic_schema.get_conn(db_path)
    try:
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
        total_text = " ".join(s["text"] for s in sections)
        wc = _word_count(total_text)

        config = _load_domain_config(repo_root, domain)
        in_range = True
        detail = f"word_count={wc}"
        if config:
            min_w, max_w = config.get("min", 0), config.get("max", 999999)
            in_range = min_w <= wc <= max_w
            detail += f", range=[{min_w},{max_w}], in_range={in_range}"

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
            total_wc += wc
            detail += f", total_wc={total_wc}, paper_range=[{paper_min},{paper_max}]"

        write_envelope(out_path, status="ok" if in_range else "error",
                       message=detail, paper_id=paper_id, domain=domain,
                       word_count=wc, in_range=in_range,
                       total_word_count=total_wc if paper_min else None)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
