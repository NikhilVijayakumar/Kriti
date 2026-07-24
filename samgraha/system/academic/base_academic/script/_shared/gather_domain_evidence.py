"""gather_domain_evidence.py — pre-script for domain-level triads.
Gathers evidence depending on mode:
  - draft: docs only, no implementation
  - generate: analysis docs + implementation evidence
  - audit: current draft text + rubric criteria

Expected --in payload: {paper_id: int, domain: str, mode: str}
"""
import json
import os
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
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


def gather_analysis_docs(repo_root, domain):
    analysis = {}
    docs_paper = os.path.join(str(repo_root), "docs", "paper")
    if os.path.isdir(docs_paper):
        for root, dirs, files in os.walk(docs_paper):
            for f in files:
                if f.endswith((".md", ".yaml")):
                    fp = os.path.join(root, f)
                    rel = os.path.relpath(fp, docs_paper)
                    try:
                        with open(fp, encoding="utf-8", errors="replace") as fh:
                            analysis[rel] = fh.read()[:6000]
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


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    domain = payload["domain"]
    mode = payload.get("mode", "generate")

    conn = academic_schema.get_conn(db_path)
    try:
        paper = academic_schema.get_paper(conn, paper_id)
    finally:
        conn.close()

    repo_root_path = paper["repo_root"] if paper else str(repo_root)

    evidence = {}
    if mode == "draft":
        evidence["documentation"] = gather_docs_only(repo_root_path)
    elif mode == "generate":
        evidence["analysis_docs"] = gather_analysis_docs(repo_root_path, domain)
        evidence["documentation"] = gather_docs_only(repo_root_path)
    elif mode == "audit":
        evidence["current_draft"] = gather_draft(paper_id, domain, db_path)

    write_envelope(out_path, status="ok",
                   message=f"gathered evidence for domain={domain} mode={mode}",
                   evidence=evidence, paper_id=paper_id, domain=domain, mode=mode)


if __name__ == "__main__":
    main()
