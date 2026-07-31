"""gather_domain_evidence.py — pre-script for domain-level triads.
Gathers evidence depending on mode:
  - draft: docs only, no implementation
  - generate: analysis docs + implementation evidence
  - enrich: same as generate — 3a/3b's math/architecture findings already
    land in docs/paper/{system}/cross_module/, picked up by the same
    analysis-doc scan (section-enrichment, usecase 4c)
  - audit: current draft text + rubric criteria
  - citation: deterministic extraction of in-repo grounding markers left
    in the domain's stage='generate' text by generate-section.md's Rule 1
    (section-citations, usecase 4b's non-literature-review path)

Expected --in payload: {paper_id: int, domain: str, mode: str}
"""
import json
import os
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
import academic_schema  # noqa: E402


def gather_docs_only(repo_root):
    docs = {}
    for name in ("README.md", "README.rst", "README.txt"):
        path = os.path.join(str(repo_root), name)
        if os.path.isfile(path):
            with open(path, encoding="utf-8", errors="replace") as f:
                docs["readme"] = f.read()[:8000]
            break
    src_dir = os.path.join(str(repo_root), "src")
    if not os.path.isdir(src_dir):
        src_dir = str(repo_root)
    for root, dirs, files in os.walk(src_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {"__pycache__", "node_modules", ".venv"}]
        for f in files:
            if f.endswith((".py", ".rs", ".ts")):
                fp = os.path.join(root, f)
                try:
                    with open(fp, encoding="utf-8", errors="replace") as fh:
                        content = fh.read()[:4000]
                    docs[os.path.relpath(fp, str(repo_root))] = content
                except Exception:
                    pass
                if len(docs) > 20:
                    break
        if len(docs) > 20:
            break
    return docs


# Domains whose real evidence is narrow and specific (experiment results,
# not general architecture) get scoped to matching paths instead of the
# full docs/paper/ tree — pulling in ~100+ unrelated architecture/gaps/
# mathematics docs from other modules just dilutes the signal and blows up
# evidence size. Path substrings are matched case-insensitively.
_DOMAIN_EVIDENCE_KEYWORDS = {
    "findings": ("evaluation", "results", "user_inputs"),
}


def gather_analysis_docs(repo_root, domain):
    analysis = {}
    docs_paper = os.path.join(str(repo_root), "docs", "paper")
    keywords = _DOMAIN_EVIDENCE_KEYWORDS.get(domain)
    if os.path.isdir(docs_paper):
        for root, dirs, files in os.walk(docs_paper):
            for f in files:
                if f.endswith((".md", ".yaml")):
                    fp = os.path.join(root, f)
                    rel = os.path.relpath(fp, docs_paper)
                    if keywords and not any(k in rel.lower() for k in keywords):
                        continue
                    try:
                        with open(fp, encoding="utf-8", errors="replace") as fh:
                            text = fh.read()
                        # Scoped domains get the full file (evidence set is
                        # small); unscoped domains keep the original cap so
                        # a full docs/paper/ walk doesn't blow up context.
                        analysis[rel] = text if keywords else text[:6000]
                    except Exception:
                        pass
    return analysis


def gather_draft(paper_id, domain, db_path):
    conn = academic_schema.get_conn(db_path)
    try:
        draft = academic_schema.get_narrative(conn, paper_id, domain)
    finally:
        conn.close()
    return draft or []


def extract_citation_markers(text):
    """Deterministic extraction of in-repo grounding markers — prefixed
    evidence references like [evidence: foo.py] left by generate-section.md's
    Rule 1 (now uses [evidence: ...] convention). Deduplicated, order preserved.
    Strips the 'evidence: ' prefix from stored markers."""
    markers = re.findall(r"\[evidence:\s*([^\[\]]{1,120})\]",
                         text or "", re.IGNORECASE)
    seen = []
    for m in markers:
        m = m.strip()
        if m not in seen and m != "NEEDS VERIFICATION":
            seen.append(m)
    return seen


def gather_citation_sources(paper_id, domain, db_path):
    conn = academic_schema.get_conn(db_path)
    try:
        domain_id = academic_schema.get_domain_id(conn, domain)
        narrative_row = conn.execute(
            "SELECT id FROM academic_narratives WHERE paper_id=? AND domain_id=? AND stage='generate' ORDER BY iteration DESC LIMIT 1",
            (paper_id, domain_id),
        ).fetchone()
        if not narrative_row:
            return []
        sections = conn.execute(
            "SELECT text FROM academic_narrative_sections WHERE narrative_id=?",
            (narrative_row["id"],),
        ).fetchall()
        text = " ".join(r["text"] for r in sections)
    finally:
        conn.close()
    return extract_citation_markers(text)


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    domain = payload["domain"]
    mode = payload.get("mode", "generate")

    conn = academic_schema.get_conn(db_path)
    try:
        paper = academic_schema.get_paper(conn, paper_id)
        domain_id = academic_schema.get_domain_id(conn, domain)
        map_entries = []
        for table, kind, label_col in [
            ("academic_figure_map", "figure", "caption"),
            ("academic_table_map", "table", "caption"),
            ("academic_equation_map", "equation", "latex"),
            ("academic_algorithm_map", "algorithm", "name"),
        ]:
            rows = conn.execute(
                f"SELECT map_key, {label_col} AS label FROM {table} "
                "WHERE paper_id=? AND target_section=?",
                (paper_id, domain)).fetchall()
            for r in rows:
                map_entries.append({
                    "map_key": r["map_key"], "kind": kind, "label": r["label"],
                })
        cite_rows = conn.execute(
            "SELECT citation FROM academic_section_citations "
            "WHERE paper_id=? AND domain_id=?",
            (paper_id, domain_id)).fetchall()
        for r in cite_rows:
            map_entries.append({
                "map_key": None, "kind": "citation", "label": r["citation"],
            })
    finally:
        conn.close()

    repo_root_path = paper["repo_root"] if paper else str(repo_root)

    evidence = {}
    if mode == "draft":
        evidence["documentation"] = gather_docs_only(repo_root_path)
    elif mode in ("generate", "enrich"):
        evidence["analysis_docs"] = gather_analysis_docs(repo_root_path, domain)
        evidence["documentation"] = gather_docs_only(repo_root_path)
        evidence["map_entries"] = map_entries
    elif mode == "audit":
        evidence["current_draft"] = gather_draft(paper_id, domain, db_path)
    elif mode == "citation":
        evidence["citations"] = gather_citation_sources(paper_id, domain, db_path)

    write_envelope(out_path, status="ok",
                   message=f"gathered evidence for domain={domain} mode={mode}",
                   evidence=evidence, paper_id=paper_id, domain=domain, mode=mode)


if __name__ == "__main__":
    main()
