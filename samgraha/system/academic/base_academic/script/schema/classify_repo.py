"""classify_repo.py — entry router. Inspects the target repo to determine
its state: NO_DOCS_NO_IMPL (refuse), DOCS_ONLY (draft from docs),
IMPL_NO_ANALYSIS (generate analysis first), or IMPL_WITH_ANALYSIS
(generate draft directly). Persists to academic_repos.

Classification heuristic:
- has_implementation: any .py/.rs/.ts/.js source files beyond docs/config
- has_analysis_docs: docs/paper/{system}/ directory exists with content
"""
import os
import sys
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402

SOURCE_EXTENSIONS = {".py", ".rs", ".ts", ".js", ".java", ".go", ".cpp", ".c", ".h"}
CONFIG_DIRS = {".git", ".github", ".vscode", ".idea", "__pycache__", "node_modules", ".venv", "venv"}
CONFIG_FILES = {"pyproject.toml", "setup.py", "setup.cfg", "Cargo.toml", "package.json",
                "requirements.txt", "go.mod", ".env", ".env.example"}


def count_source_files(repo_root):
    count = 0
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames if d not in CONFIG_DIRS]
        rel = os.path.relpath(dirpath, repo_root)
        if rel.startswith(".") or rel.startswith("docs"):
            continue
        for f in filenames:
            if os.path.splitext(f)[1] in SOURCE_EXTENSIONS:
                count += 1
    return count


def has_analysis_docs(repo_root):
    docs_paper = os.path.join(repo_root, "docs", "paper")
    if not os.path.isdir(docs_paper):
        return False
    for item in os.listdir(docs_paper):
        item_path = os.path.join(docs_paper, item)
        if os.path.isdir(item_path):
            for root, dirs, files in os.walk(item_path):
                if any(f.endswith((".md", ".yaml")) for f in files):
                    return True
    return False


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    standard = payload.get("standard", "base_academic")

    repo_path = str(repo_root)
    src_count = count_source_files(repo_path)
    has_impl = src_count > 0
    has_docs = has_analysis_docs(repo_path)

    if not has_impl and not has_docs:
        classification = "NO_DOCS_NO_IMPL"
    elif not has_impl:
        classification = "DOCS_ONLY"
    elif not has_docs:
        classification = "IMPL_NO_ANALYSIS"
    else:
        classification = "IMPL_WITH_ANALYSIS"

    conn = academic_schema.get_conn(db_path)
    try:
        academic_schema.register_paper(conn, standard, repo_path)
        academic_schema.upsert_repo_classification(
            conn, standard, repo_path, classification,
            has_implementation=has_impl, has_analysis_docs=has_docs,
            metadata={"source_file_count": src_count},
        )
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"repo classified as {classification} (impl={has_impl}, docs={has_docs}, src_files={src_count})",
                   classification=classification, has_implementation=has_impl,
                   has_analysis_docs=has_docs, source_file_count=src_count)


if __name__ == "__main__":
    main()
