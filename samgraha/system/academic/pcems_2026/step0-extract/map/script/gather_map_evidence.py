"""gather_map_evidence.py — gather source evidence for a map extraction
domain (tables, figures, equations, algorithms). Reads the relevant source
files from the repo and passes them as `source_evidence` for the LLM to
structure into map entries.

Unlike the existing gather_tables_figures_evidence.py, this is an EXTRACTION
pre-script (runs before generation, not after) — it reads real evidence
files, not the LLM's own draft.

Expected --in payload:
  {paper_id: int, domain: str ("tables"|"figures"|"equations"|"algorithms")}
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
import academic_schema

_EVIDENCE_PATH_RELS = {
    "tables": [
        "docs/paper/Bodha/drafts/5. Experimental Evaluation.md",
        "docs/paper/Bodha/drafts/6. Results and Discussion.md",
    ],
    "figures": [
        "docs/paper/Bodha/drafts/visualizations",
    ],
    "equations": [
        "docs/paper/Bodha/cross_module/mathematics.md",
    ],
    "algorithms": [
        "docs/paper/Bodha/cross_module/mathematics.md",
    ],
}


def _gather_paths(domain, repo_root):
    paths = []
    for entry in _EVIDENCE_PATH_RELS.get(domain, []):
        resolved = repo_root / entry
        if resolved.is_dir():
            paths.extend(sorted(resolved.iterdir()))
        elif resolved.is_file():
            paths.append(resolved)
    return paths


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    domain = payload["domain"]

    evidence_paths = _gather_paths(domain, repo_root)
    evidence = []
    for fp in evidence_paths:
        if fp.suffix.lower() in (".md", ".txt", ".py", ".csv", ".tex"):
            try:
                text = fp.read_text(encoding="utf-8")
                evidence.append({"path": str(fp), "text": text})
            except (UnicodeDecodeError, OSError):
                evidence.append({"path": str(fp), "text": "[binary or unreadable]"})
        elif fp.suffix.lower() in (".svg", ".png", ".jpg", ".jpeg"):
            evidence.append({"path": str(fp), "text": f"[asset: {fp.name}]"})

    write_envelope(out_path, status="ok",
                   message=f"gathered {len(evidence)} evidence files for {domain}",
                   paper_id=paper_id, domain=domain,
                   evidence_count=len(evidence),
                   evidence=evidence)


if __name__ == "__main__":
    main()
